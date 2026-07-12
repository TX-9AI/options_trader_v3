"""
options_trader_v2/analysis/conviction_integrator.py — Persistence (conviction-integrator) regime engine.

v1.0 — 2026-07-09 — NEW FILE. SHADOW-MODE ONLY: this module drives nothing.
        It runs alongside regime_classifier v1.x, consumes the same per-tick
        state objects, and maintains a RUNNING CONVICTION PER REGIME that
        integrates evidence over time — rising on agreement, decaying on
        disagreement, with decay resistance scaled by banked conviction.
        The emitted regime is the argmax conviction past a commit threshold,
        with hysteresis and displacement-by-competitor; UNKNOWN is the
        genuine-ambiguity fallback (rare by construction), and remains a hard
        NO-TRADE gate wherever it is consumed.

        Design contract (see docs/persistence_integrator_design.md):
        • Fast to recognize, slow to abandon. Recognition is instantaneous at
          the evidence level; COMMITMENT (emitting a tradeable regime) and
          ABANDONMENT (dropping a held regime) are durational.
        • A single-tick flicker can never force UNKNOWN over a held regime.
        • A held regime is displaced by a COMPETING regime accumulating its
          own conviction (belief yields to better belief), not by decaying
          into UNKNOWN.
        • Updates are dt-aware (wall-clock), so irregular tick spacing and
          bar-vs-tick evidence cadence are handled identically.
        • The integrator governs CLASSIFICATION ONLY. It must never sit in
          the path of price-based stops/targets/trails (exit_engine) — those
          stay instantaneous.

        THRESHOLDS ARE PRIORS, not calibration: every number in
        IntegratorParams was set against one synthetic validation suite
        seeded by the 2026-07-09 regime_log post-mortem. They MUST be
        re-fit on accumulated candle-logger tape (multi-day) before this
        engine is allowed to drive the live classify path.
"""

import json
import logging
import math
import os
import tempfile
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Regime names duplicated as plain strings so this module stays importable in
# isolation (backtests, shadow harness, notebooks) without the repo on path.
# They MUST match analysis.regime_classifier.Regime verbatim.
TRENDING_BULL     = "TRENDING_BULL"
TRENDING_BEAR     = "TRENDING_BEAR"
RANGING           = "RANGING"
BREAKOUT_VOLATILE = "BREAKOUT_VOLATILE"
COMPRESSION       = "COMPRESSION"
SWEEP_REVERSAL    = "SWEEP_REVERSAL"
UNKNOWN           = "UNKNOWN"

INTEGRATED_REGIMES = (
    TRENDING_BULL, TRENDING_BEAR, RANGING,
    BREAKOUT_VOLATILE, COMPRESSION, SWEEP_REVERSAL,
)

# Deterministic tie-break priority when convictions are exactly equal
# (mirrors the v1.x decision hierarchy; in practice ties are measure-zero).
_TIEBREAK_ORDER = {r: i for i, r in enumerate((
    SWEEP_REVERSAL, BREAKOUT_VOLATILE, COMPRESSION,
    TRENDING_BULL, TRENDING_BEAR, RANGING,
))}


# ─── Parameters (PRIORS — recalibrate from multi-day tape) ────────────────────

@dataclass
class RegimeParams:
    """Per-regime integration constants (units: seconds)."""
    tau_up:   float   # rise time constant: C approaches evidence as 1-exp(-t/tau_up)
    tau_dn0:  float   # decay time constant floor (at zero banked conviction)
    lam:      float   # conviction-scaling of decay: tau_dn(C) = tau_dn0 * exp(lam*C)


@dataclass
class IntegratorParams:
    theta_commit: float = 0.65   # conviction needed to EMIT a regime (enter)
    theta_hold:   float = 0.45   # conviction needed to KEEP a held regime (hysteresis)
    delta_displace: float = 0.12 # margin a challenger needs over the incumbent
    dt_max:       float = 90.0   # gap > dt_max seconds ⇒ do not integrate; mark stale
    tau_stale:    float = 600.0  # decay constant while evidence is UNOBSERVABLE (None)

    per_regime: Dict[str, RegimeParams] = field(default_factory=lambda: {
        # Directional regimes: fast to commit (3 integrating ticks / ~60 s wall ⇒
        # roughly one confirmed candle — "one candle isn't a pattern" means
        # commitment needs a sustained read, not that recognition is slow).
        TRENDING_BULL:     RegimeParams(tau_up=40.0,  tau_dn0=25.0, lam=2.2),
        TRENDING_BEAR:     RegimeParams(tau_up=40.0,  tau_dn0=25.0, lam=2.2),
        BREAKOUT_VOLATILE: RegimeParams(tau_up=40.0,  tau_dn0=25.0, lam=2.2),
        # Sweeps are events: recognized fast, and must DIE fast when stale —
        # low lam so banked sweep conviction cannot squat over a breakout.
        SWEEP_REVERSAL:    RegimeParams(tau_up=25.0,  tau_dn0=15.0, lam=1.5),
        # Compression builds over minutes.
        COMPRESSION:       RegimeParams(tau_up=180.0, tau_dn0=40.0, lam=2.0),
        # RANGING commits SLOWLY by design: on real tape, trends held a
        # false-flat angle for 12–15 bars while true ranges held 24–29.
        # tau_up is chosen so sustained flat evidence commits at ~17–19 bars —
        # past the impostor window, inside the genuine-range window. This is
        # the premium-selling gate; slow is correct.
        RANGING:           RegimeParams(tau_up=780.0, tau_dn0=60.0, lam=2.0),
    })


# ─── Output state ─────────────────────────────────────────────────────────────

@dataclass
class IntegratorState:
    regime:      str = UNKNOWN            # emitted regime (argmax past threshold, hysteresis applied)
    conviction:  float = 0.0              # conviction of the emitted regime
    convictions: Dict[str, float] = field(default_factory=dict)  # full vector
    trigger:     str = ""                 # why the emission changed this tick ("" if unchanged)
    stale:       bool = False             # True after a gap/restart until warmed


# ─── The integrator ───────────────────────────────────────────────────────────

class ConvictionIntegrator:
    """
    Per-regime leaky integrator with conviction-scaled decay.

    Update law (per regime r, elapsed wall-clock dt, evidence e ∈ [0,1] or None):

        rise  (e ≥ C):  C ← C + (1 − exp(−dt/τ_up)) · (e − C)
        fall  (e < C):  C ← C − (1 − exp(−dt/τ_dn(C))) · (C − e)
                        with τ_dn(C) = τ_dn0 · exp(λ·C)
        stale (e None): C ← C · exp(−dt/τ_stale)

    Properties: C stays in [0,1]; for constant evidence C converges to e (it
    tracks evidence, it does not saturate past it); the decay time constant
    GROWS exponentially with banked conviction, so a 0.95 regime shrugs off
    the single-tick contradiction that tears down a 0.55 regime — the
    operator's rule, exactly, and the reason a flicker cannot force UNKNOWN.

    Emission law (hysteresis + displacement):
      1. If an incumbent is held and C_inc ≥ θ_hold: keep it — UNLESS some
         challenger has C ≥ θ_commit AND C ≥ C_inc + δ, in which case switch
         to the challenger (belief yields to better belief, not to noise).
      2. Otherwise: take argmax C. If it clears θ_commit, commit it.
         Else emit UNKNOWN (genuine ambiguity — nothing holds conviction).

    θ_hold < θ_commit is the hysteresis band: harder to enter than to keep,
    so the emitted label cannot chatter across a single threshold.
    """

    def __init__(self, params: Optional[IntegratorParams] = None):
        self.p = params or IntegratorParams()
        self.C: Dict[str, float] = {r: 0.0 for r in INTEGRATED_REGIMES}
        self.incumbent: Optional[str] = None
        self.last_ts: Optional[float] = None
        self.stale: bool = True   # unwarmed until first update/replay

    # ── core update ──────────────────────────────────────────────────────────

    def update(self, ts: float, evidence: Dict[str, Optional[float]]) -> IntegratorState:
        """
        Advance the integrator to wall-clock time `ts` (epoch seconds) with the
        instantaneous evidence vector, and return the emitted state.
        Missing keys in `evidence` are treated as None (unobservable), which is
        NOT the same as 0.0 (contradicted): unobservable bleeds slowly toward 0
        instead of being torn down — an engine outage must not shred conviction.
        """
        if self.last_ts is None:
            dt = 0.0
        else:
            dt = ts - self.last_ts
            if dt < 0:
                logger.warning("integrator: non-monotonic ts (dt=%.1fs); clamping to 0", dt)
                dt = 0.0
        gap = self.last_ts is not None and dt > self.p.dt_max
        self.last_ts = ts

        if gap:
            # A gap (restart, feed outage) means the tape moved while we were
            # blind. Do NOT pretend continuity: decay everything on the stale
            # constant and flag the state so the caller can warm-start via
            # replay() from the candle logger before trusting emissions.
            for r in INTEGRATED_REGIMES:
                self.C[r] *= math.exp(-dt / self.p.tau_stale)
            self.stale = True
            logger.warning("integrator: %.0fs gap — state marked STALE, replay recommended", dt)
        elif dt > 0:
            for r in INTEGRATED_REGIMES:
                e = evidence.get(r, None)
                c = self.C[r]
                rp = self.p.per_regime[r]
                if e is None:
                    c *= math.exp(-dt / self.p.tau_stale)
                else:
                    e = min(max(float(e), 0.0), 1.0)
                    if e >= c:
                        beta = 1.0 - math.exp(-dt / rp.tau_up)
                        c += beta * (e - c)
                    else:
                        tau_dn = rp.tau_dn0 * math.exp(rp.lam * c)
                        beta = 1.0 - math.exp(-dt / tau_dn)
                        c -= beta * (c - e)
                self.C[r] = min(max(c, 0.0), 1.0)
            if all(evidence.get(r) is not None for r in INTEGRATED_REGIMES):
                self.stale = False
        else:
            # dt == 0 (first sample): seed toward evidence at rise rate of one
            # nominal tick is NOT done — first sample only registers the clock.
            pass

        return self._emit()

    # ── emission ─────────────────────────────────────────────────────────────

    def _emit(self) -> IntegratorState:
        p = self.p
        trigger = ""

        # sorted challenger view: highest conviction first, deterministic ties
        ranked = sorted(
            self.C.items(),
            key=lambda kv: (-kv[1], _TIEBREAK_ORDER[kv[0]]),
        )
        top_r, top_c = ranked[0]

        if self.incumbent is not None and self.C[self.incumbent] >= p.theta_hold:
            inc_c = self.C[self.incumbent]
            # displacement: a challenger must be COMMITTED and clearly better
            if (top_r != self.incumbent
                    and top_c >= p.theta_commit
                    and top_c >= inc_c + p.delta_displace):
                trigger = f"displaced {self.incumbent}({inc_c:.2f}) → {top_r}({top_c:.2f})"
                self.incumbent = top_r
        else:
            if self.incumbent is not None:
                trigger = f"{self.incumbent} fell below hold ({self.C[self.incumbent]:.2f} < {p.theta_hold})"
                self.incumbent = None
            if top_c >= p.theta_commit:
                self.incumbent = top_r
                trigger = (trigger + "; " if trigger else "") + f"committed {top_r}({top_c:.2f})"

        if self.incumbent is not None:
            regime, conviction = self.incumbent, self.C[self.incumbent]
        else:
            regime, conviction = UNKNOWN, 0.0

        return IntegratorState(
            regime=regime,
            conviction=conviction,
            convictions=dict(self.C),
            trigger=trigger,
            stale=self.stale,
        )

    # ── warm start / persistence across restarts ─────────────────────────────
    # The v1.x classifier was memoryless, so restarts were free. An integrator
    # has state; a mid-session restart (the NVDA lesson) must not reset the
    # book to UNKNOWN for the RANGING commit window (~18 min). Two mechanisms:
    #   1. Periodic snapshot to disk; reload if fresh (< dt_max old).
    #   2. Otherwise replay recent evidence history (candle-logger tape) to
    #      rebuild conviction deterministically.

    def replay(self, samples: List[Tuple[float, Dict[str, Optional[float]]]]) -> IntegratorState:
        """Rebuild state by replaying (ts, evidence) samples in time order.
        Resets state first. Returns the final emitted state."""
        self.C = {r: 0.0 for r in INTEGRATED_REGIMES}
        self.incumbent = None
        self.last_ts = None
        self.stale = True
        out = IntegratorState()
        for ts, ev in samples:
            out = self.update(ts, ev)
        return out

    def to_dict(self) -> dict:
        return {
            "C": dict(self.C),
            "incumbent": self.incumbent,
            "last_ts": self.last_ts,
        }

    def save(self, path: str) -> None:
        """Atomic snapshot (write temp + rename) — safe against mid-write kills."""
        d = os.path.dirname(path) or "."
        os.makedirs(d, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=d, prefix=".integrator_")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(self.to_dict(), f)
            os.replace(tmp, path)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def load(self, path: str, now_ts: float) -> bool:
        """Load a snapshot if it is fresh enough to trust (age ≤ dt_max).
        Returns True on success; on False the caller should replay()."""
        try:
            with open(path) as f:
                d = json.load(f)
            last_ts = d.get("last_ts")
            if last_ts is None or (now_ts - last_ts) > self.p.dt_max:
                return False
            self.C = {r: float(d["C"].get(r, 0.0)) for r in INTEGRATED_REGIMES}
            self.incumbent = d.get("incumbent")
            self.last_ts = float(last_ts)
            self.stale = False
            return True
        except (OSError, ValueError, KeyError, TypeError):
            return False


# ─── Evidence: graded signals from the existing engine states ────────────────
# The v1.x boolean `_is_*` conditions become graded evidence in [0,1].
# ramp() is the universal primitive: 0 below lo, 1 above hi, linear between.

def ramp(x: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 1.0 if x >= hi else 0.0
    return min(max((x - lo) / (hi - lo), 0.0), 1.0)


def flat_angle_deg(closes: List[float], atr: float) -> Optional[float]:
    """
    Instrument-agnostic trend/flat read over a window of closes (validated on
    real tape; fixed the SPX raw-percent false-positive, 48% → 17%):

        angle = arctan( |slope·n| / (ATR·√n) )   in degrees, 0=flat … 90=steep

    Numerator: net regression drift over the window. Denominator: the
    random-walk noise scale — the drift a pure noise process of this ATR
    would exhibit over n bars. The ratio is dimensionless, so one angle
    cutoff serves SPX and a $4 name alike.
    """
    n = len(closes)
    if n < 8 or atr is None or atr <= 0:
        return None
    xbar = (n - 1) / 2.0
    ybar = sum(closes) / n
    sxx = sum((i - xbar) ** 2 for i in range(n))
    sxy = sum((i - xbar) * (closes[i] - ybar) for i in range(n))
    slope = sxy / sxx if sxx > 0 else 0.0
    drift = abs(slope * n)
    noise = atr * math.sqrt(n)
    return math.degrees(math.atan2(drift, noise))


def midline_crossings(closes: List[float]) -> int:
    """Crossings of the window's regression midline. Used ONLY as graded
    confirmation AFTER the flat-angle veto has passed: conditional on a flat
    center, many crossings = two-sided rotation (a range that oscillates),
    few = a pin/drift. NO R²/fit-quality filter — shark-fin scatter is
    expected and allowed; only the CENTER must hold."""
    n = len(closes)
    if n < 8:
        return 0
    xbar = (n - 1) / 2.0
    ybar = sum(closes) / n
    sxx = sum((i - xbar) ** 2 for i in range(n))
    sxy = sum((i - xbar) * (closes[i] - ybar) for i in range(n))
    slope = sxy / sxx if sxx > 0 else 0.0
    resid = [closes[i] - (ybar + slope * (i - xbar)) for i in range(n)]
    return sum(
        1 for a, b in zip(resid, resid[1:])
        if a != 0 and b != 0 and (a > 0) != (b > 0)
    )


# Evidence calibration knobs (PRIORS — recalibrate from candle-logger tape).
FLAT_ANGLE_CUT_DEG   = 20.0   # hard veto: at/above this the center is not flat
FLAT_ANGLE_SOFT_DEG  = 8.0    # full flat credit at (CUT − SOFT) = 12°
RANGE_WINDOW_BARS    = 25     # window for angle + crossings (matches tape study)
ADX_STRONG_SOLO      = 35.0   # ADX above which trend carries without alignment
SWEEP_HALFLIFE_BARS  = 3.0    # sweep evidence half-life without follow-through


class EvidenceAdapter:
    """
    Maps the per-tick engine states (VolatilityState, TrendState, StructureMap,
    LiquidityMap) plus a rolling window of 1-min closes+ATR into the graded
    evidence vector the integrator consumes. Field names below are the REAL
    attributes read off regime_classifier v1.2 / the engines at HEAD ef76b4a.

    Contract notes:
    • Evidence is INSTANTANEOUS and may be noisy — that is the design. The
      integrator supplies the persistence; the adapter must NOT smooth.
    • Return None (not 0.0) for a regime whose inputs are unavailable.
    """

    def __init__(self,
                 adx_trend_threshold: float = 25.0,   # config.ADX_TREND_THRESHOLD
                 adx_range_threshold: float = 20.0):  # config.ADX_RANGE_THRESHOLD
        self.adx_trend = adx_trend_threshold
        self.adx_range = adx_range_threshold

    def evidence(self, vol_state, trend_state, structure, liq_map,
                 closes: Optional[List[float]] = None,
                 atr: Optional[float] = None) -> Dict[str, Optional[float]]:
        ev: Dict[str, Optional[float]] = {}

        adx = trend_state.primary_adx
        align_frac = trend_state.aligned_timeframes / max(trend_state.total_timeframes, 1)

        # ── TRENDING (directional) ────────────────────────────────────────────
        # ADX strength ramps in from the config threshold; alignment CORROBORATES
        # marginal ADX rather than hard-gating strong ADX (the v1.3 coverage fix,
        # graded): above ADX_STRONG_SOLO the alignment factor is forgiven.
        adx_s = ramp(adx, self.adx_trend - 5, ADX_STRONG_SOLO)
        align_s = max(align_frac, ramp(adx, self.adx_trend, ADX_STRONG_SOLO))
        contra = "LH_LL" if trend_state.is_bullish else "HH_HL"
        struct_ok = 0.0 if structure.structure_sequence == contra else 1.0
        trend_e = adx_s * align_s * struct_ok
        if trend_state.overall_direction == "BULLISH":
            ev[TRENDING_BULL], ev[TRENDING_BEAR] = trend_e, 0.0
        elif trend_state.overall_direction == "BEARISH":
            ev[TRENDING_BULL], ev[TRENDING_BEAR] = 0.0, trend_e
        else:
            ev[TRENDING_BULL] = ev[TRENDING_BEAR] = 0.0

        # ── BREAKOUT_VOLATILE ────────────────────────────────────────────────
        # v1.2 booleans, graded — with the momentum carry: when ADX is clearly
        # high, a momentary BB re-entry does NOT zero the evidence (defense in
        # depth against the flicker, beneath the integrator's own persistence).
        atr_ratio = vol_state.atr_current / max(vol_state.atr_avg_20, 1e-3)
        expand_s = ramp(atr_ratio, 1.0, 1.5) if vol_state.is_expanding else \
                   ramp(atr_ratio, 1.1, 1.6) * 0.6
        outside_s = 1.0 if vol_state.price_vs_bb != "INSIDE" else ramp(adx, 38.0, 50.0)
        ev[BREAKOUT_VOLATILE] = expand_s * outside_s

        # ── COMPRESSION ──────────────────────────────────────────────────────
        squeeze_s = ramp(0.20 - vol_state.bb_width_pct, 0.0, 0.15)
        quiet = 1.0 if (vol_state.atr_state in ("CONTRACTING", "STABLE")
                        and not vol_state.is_expanding) else 0.0
        ev[COMPRESSION] = squeeze_s * quiet

        # ── SWEEP_REVERSAL ───────────────────────────────────────────────────
        # Definitional gates (v1.1) stay binary: location (named zone),
        # rejection (reclaimed), non-acceptance. Age then DECAYS the evidence —
        # a sweep is an event; without follow-through its evidence must die,
        # which is what lets a rising breakout displace a stale sweep label.
        sweep = liq_map.recent_sweep
        if sweep and getattr(sweep, "reclaimed", False) \
                and getattr(sweep, "swept_named_level", "") \
                and getattr(sweep, "closes_beyond", 0) < 2:
            strength = ramp(sweep.rejection_pct, 0.002, 0.008)
            age_decay = 0.5 ** (liq_map.sweep_age_bars / SWEEP_HALFLIFE_BARS)
            ev[SWEEP_REVERSAL] = strength * age_decay
        else:
            ev[SWEEP_REVERSAL] = 0.0

        # ── RANGING ──────────────────────────────────────────────────────────
        # The validated definition: flat center is the HARD VETO (a trend cannot
        # have a flat center — its value migrates), oscillation around the LOCAL
        # center (the window's own regression midline — valid precisely because
        # the veto has certified that midline flat) is graded confirmation.
        # Elevated ADX and BB pokes are ALLOWED: energetic shark-fin chop stabs
        # the edges by nature. Scatter is fine; only the center must hold.
        if closes is not None and atr is not None and len(closes) >= RANGE_WINDOW_BARS:
            w = closes[-RANGE_WINDOW_BARS:]
            ang = flat_angle_deg(w, atr)
            if ang is None:
                ev[RANGING] = None
            elif ang >= FLAT_ANGLE_CUT_DEG:
                ev[RANGING] = 0.0                                    # veto
            else:
                flat_s = ramp(FLAT_ANGLE_CUT_DEG - ang, 0.0, FLAT_ANGLE_SOFT_DEG)
                osc_s = ramp(midline_crossings(w), 2.0, 5.0)
                ev[RANGING] = flat_s * (0.4 + 0.6 * osc_s)
        else:
            # Bars unavailable: fall back to the v1.2 quiet-range read so the
            # regime is not blind, at reduced ceiling (it cannot see energetic
            # chop — that is exactly what the angle read adds).
            quiet_range = (adx < self.adx_range
                           and not vol_state.is_expanding
                           and vol_state.price_vs_bb == "INSIDE")
            ev[RANGING] = 0.6 if quiet_range else 0.0

        return ev
