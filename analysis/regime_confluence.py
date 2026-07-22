# analysis/regime_confluence.py — options_trader_v3
# v1.1 — 2026-07-12 — FIX silent config-import failure. The guarded import
#         requested SWEEP_ACCEPT_CLOSES from config, but it lives in
#         analysis/regime_classifier.py; the whole block threw, the except
#         swallowed it, and every constant ran on standalone fallbacks
#         (_HAVE_CONFIG=False on every box — verified at runtime). Split into
#         two independent guards: config constants from config,
#         SWEEP_ACCEPT_CLOSES from its real home. Zero behavioral delta today
#         (fallbacks equal live config values); future config tunes now reach
#         the scorer. No scoring-logic change.
# v1.0 — 2026-07-11 — NEW FILE (not present at HEAD 49d7af8).
#         Layer 1 — Regime Confluence Scorer. Instantaneous, graded, per-regime
#         evidence in [0,1] (or None = unobservable) computed every tick from the
#         engine state objects. Implements REGIME_TRUTHS.md v0.1 in the three-tier
#         grammar:  score_R = (∏ hard_veto ∈{0,1}) · (∏ soft_necessary ∈[0,1])
#                            · (Σ w_k · corroborator_k),   Σ w_k = 1
#
# LAYER BOUNDARY (enforced):
#   • Instantaneous only. No smoothing, no memory, no count-over-N, no accumulation.
#     The 25-bar angle/crossings window is a property of the CURRENT window (legal),
#     not accumulated belief. Persistence is Layer 2 (conviction integrator).
#   • No reference to strikes, premium, sizing, fills, ROI, or tradability (Layer 3).
#   • Unobservable ≠ contradicted:  None = inputs unavailable;  0.0 = actively refuted.
#   • Instrument-agnostic: every input is ATR-relative, a percentile, an angle, or a
#     categorical engine state — one parameter set serves SPX and a $4 name alike.
#
# Output contract: score(...) -> ConfluenceResult(scores, breakdown).
#   scores:   Dict[str, Optional[float]] keyed by the six regime labels — the exact
#             vector the conviction integrator's update()/replay() consumes.
#   breakdown: Dict[str, dict] — every raw input and mapped factor per regime, for
#             shadow logging and PRIOR calibration. (No I/O here; caller logs it.)
#
# Standalone: guards the repo config import; duck-types the state objects; no side
# effects at import. Importable and testable in isolation ( __main__ smoke test ).

from __future__ import annotations

import os as _os
import math
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

log = logging.getLogger(__name__)

# ── Guarded repo imports (module runs standalone if the repo is absent) ───────
# v1.1: split into TWO independent guards. The v1.0 block requested
# SWEEP_ACCEPT_CLOSES from config, but that constant lives in
# analysis/regime_classifier.py — the whole import threw, the except swallowed
# it, and ALL FOUR constants silently ran on the standalone fallbacks
# (_HAVE_CONFIG was False on every box). Harmless only while the fallback
# values equal config's; any future config tune would never have reached this
# scorer. Now each import fails independently.
try:
    from config import (                       # type: ignore
        ADX_TREND_THRESHOLD,
        ADX_RANGE_THRESHOLD,
        BB_WIDTH_COMPRESSION_PCT,
    )
    _HAVE_CONFIG = True
except Exception:                              # pragma: no cover - isolation path
    ADX_TREND_THRESHOLD      = 25.0
    ADX_RANGE_THRESHOLD      = 20.0
    BB_WIDTH_COMPRESSION_PCT = 0.20
    _HAVE_CONFIG = False

try:
    from analysis.regime_classifier import SWEEP_ACCEPT_CLOSES  # type: ignore
except Exception:                              # pragma: no cover - isolation path
    SWEEP_ACCEPT_CLOSES      = 2

# ── Regime labels (MUST match conviction_integrator.py string constants) ──────
TRENDING_BULL     = "TRENDING_BULL"
TRENDING_BEAR     = "TRENDING_BEAR"
RANGING           = "RANGING"
BREAKOUT_VOLATILE = "BREAKOUT_VOLATILE"
COMPRESSION       = "COMPRESSION"
SWEEP_REVERSAL    = "SWEEP_REVERSAL"
REGIMES = (TRENDING_BULL, TRENDING_BEAR, RANGING,
           BREAKOUT_VOLATILE, COMPRESSION, SWEEP_REVERSAL)

# ── Calibration knobs (ALL PRIOR — recalibrate from candle-logger tape) ───────
# --- env-tunable PRIOR bounds -------------------------------------------------
# v3.1: every ramp bound below is overridable via OT_RC_<NAME> so calibration is
# a config change (instant rollback, no deploy) rather than a code edit. Defaults
# are UNCHANGED, so importing this module with no env set is behaviour-identical.
def _envf(name: str, default: float) -> float:
    try:
        return float(_os.environ.get("OT_RC_" + name, default))
    except (TypeError, ValueError):
        return default


FLAT_ANGLE_CUT_DEG   = _envf("FLAT_ANGLE_CUT_DEG", 20.0)   # RANGING/COMPRESSION hard veto: ≥ ⇒ center not flat
FLAT_ANGLE_SOFT_DEG  = _envf("FLAT_ANGLE_SOFT_DEG", 8.0)    # full flat credit at (CUT − SOFT) = 12°
RANGE_WINDOW_BARS    = 25     # angle + crossings window (matches tape study)
ADX_STRONG_SOLO      = _envf("ADX_STRONG_SOLO", 35.0)   # ADX above which strength carries a trend solo
SWEEP_HALFLIFE_BARS  = 3.0    # sweep evidence half-life, absent follow-through
OSC_CROSS_LO         = _envf("OSC_CROSS_LO", 2.0)    # crossings ramp lo (few = pin/coil)
OSC_CROSS_HI         = _envf("OSC_CROSS_HI", 5.0)    # crossings ramp hi (many = two-sided rotation)
RANGE_ROOM_LO        = _envf("RANGE_ROOM_LO", 0.05)   # RANGING "room to oscillate": below this width, not ranging
RANGE_ROOM_HI        = _envf("RANGE_ROOM_HI", 0.20)   #   … at/above this width, full room (= BB_WIDTH_COMPRESSION_PCT)
BREAKOUT_ADX_LO      = _envf("BREAKOUT_ADX_LO", 38.0)   # momentum-carry ramp: inside-band forgiven from here
BREAKOUT_ADX_HI      = _envf("BREAKOUT_ADX_HI", 50.0)   #   … to here (fully forgiven)
EXPAND_RATIO_LO      = _envf("EXPAND_RATIO_LO", 1.0)    # atr_current/atr_avg_20 expansion ramp
EXPAND_RATIO_HI      = _envf("EXPAND_RATIO_HI", 1.5)
SWEEP_REJ_LO         = _envf("SWEEP_REJ_LO", 0.002)  # rejection_pct → strength ramp
SWEEP_REJ_HI         = _envf("SWEEP_REJ_HI", 0.008)
COMPRESS_WIDTH_SPAN  = _envf("COMPRESS_WIDTH_SPAN", 0.15)   # narrowness ramp span below BB_WIDTH_COMPRESSION_PCT

# Corroborator weights (PRIOR; each block sums to 1.0).
W_TREND_ALIGN, W_TREND_MOM   = 0.65, 0.35
W_RANGE_BASE,  W_RANGE_OSC   = 0.40, 0.60
W_COMP_BASE, W_COMP_SQZ, W_COMP_STORED = 0.30, 0.35, 0.35


# ── Pure helpers ──────────────────────────────────────────────────────────────
def ramp(x: float, lo: float, hi: float) -> float:
    """Monotone [lo,hi] → [0,1] clamp."""
    if hi <= lo:
        return 1.0 if x >= hi else 0.0
    return min(max((x - lo) / (hi - lo), 0.0), 1.0)


def flat_angle_deg(closes: List[float], atr: float) -> Optional[float]:
    """
    Instrument-agnostic trend/flat read over a window of closes:
        angle = arctan( |slope·n| / (ATR·√n) )   in degrees, 0=flat … 90=steep
    Numerator = net regression drift; denominator = the random-walk excursion a
    pure-noise process of this ATR would show over n bars. Dimensionless ratio ⇒
    one cutoff serves SPX and a $4 name. Returns None if inputs unusable.
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
    """
    Crossings of the window's own regression midline. Graded confirmation ONLY,
    valid AFTER the flat-angle veto certifies the center flat. Many crossings =
    two-sided rotation (RANGING spends energy); few = pin/coil (COMPRESSION stores
    it). No R²/fit filter — shark-fin scatter is expected; only the center holds.
    """
    n = len(closes)
    if n < 8:
        return 0
    xbar = (n - 1) / 2.0
    ybar = sum(closes) / n
    sxx = sum((i - xbar) ** 2 for i in range(n))
    sxy = sum((i - xbar) * (closes[i] - ybar) for i in range(n))
    slope = sxy / sxx if sxx > 0 else 0.0
    resid = [closes[i] - (ybar + slope * (i - xbar)) for i in range(n)]
    return sum(1 for a, b in zip(resid, resid[1:])
               if a != 0 and b != 0 and (a > 0) != (b > 0))


def _combine(hard_vetoes: List[float],
             soft_necessary: List[float],
             corroborators: List[Tuple[float, float]]) -> float:
    """
    score = (∏ hard_veto ∈{0,1}) · (∏ soft_necessary ∈[0,1]) · (Σ w·corroborator).
    Empty corroborator block ⇒ sum term defaults to 1.0 (veto·necessary only).
    """
    for v in hard_vetoes:
        if v <= 0.0:
            return 0.0
    prod = 1.0
    for s in soft_necessary:
        prod *= max(0.0, min(1.0, s))
    if corroborators:
        csum = sum(w * max(0.0, min(1.0, val)) for w, val in corroborators)
    else:
        csum = 1.0
    return max(0.0, min(1.0, prod * csum))


# ── Result container ──────────────────────────────────────────────────────────
@dataclass
class ConfluenceResult:
    scores:    Dict[str, Optional[float]] = field(default_factory=dict)
    breakdown: Dict[str, dict]            = field(default_factory=dict)

    def evidence(self) -> Dict[str, Optional[float]]:
        """The bare score vector the conviction integrator consumes."""
        return dict(self.scores)


# ── The scorer ────────────────────────────────────────────────────────────────
class RegimeConfluenceScorer:
    """
    Layer 1. One instance per box; `score()` is pure w.r.t. its arguments (no
    retained state between ticks — persistence is Layer 2's job by design).
    """

    def __init__(self,
                 adx_trend_threshold: float = float(ADX_TREND_THRESHOLD),
                 adx_range_threshold: float = float(ADX_RANGE_THRESHOLD)):
        self.adx_trend = adx_trend_threshold
        self.adx_range = adx_range_threshold

    # -- individual regime scorers each return (score|None, breakdown_dict) -----

    def _trending(self, trend_state, structure) -> Tuple[Dict[str, Optional[float]], dict]:
        if trend_state is None:
            return {TRENDING_BULL: None, TRENDING_BEAR: None}, {"reason": "no trend_state"}
        adx        = getattr(trend_state, "primary_adx", 0.0)
        aligned    = getattr(trend_state, "aligned_timeframes", 0)
        total      = max(getattr(trend_state, "total_timeframes", 0), 1)
        direction  = getattr(trend_state, "overall_direction", "NEUTRAL")
        is_bullish = getattr(trend_state, "is_bullish", direction == "BULLISH")
        seq        = getattr(structure, "structure_sequence", "NEUTRAL") if structure else "NEUTRAL"

        align_frac = aligned / total
        # v1.3 fix: alignment CORROBORATES marginal ADX; strong ADX forgives it.
        align_val  = max(align_frac, ramp(adx, self.adx_trend, ADX_STRONG_SOLO))

        # momentum corroborator (primary/5m vote if present; neutral otherwise)
        mom = "FLAT"
        votes = getattr(trend_state, "votes", None)
        if votes:
            v = votes.get("5m") or votes.get("1m") or next(iter(votes.values()), None)
            if v is not None:
                mom = getattr(v, "momentum", "FLAT")
        mom_val = {"ACCELERATING": 1.0, "FLAT": 0.5, "DECELERATING": 0.0}.get(mom, 0.5)

        contra    = "LH_LL" if is_bullish else "HH_HL"
        veto_struct = 0.0 if seq == contra else 1.0
        veto_dir    = 0.0 if direction not in ("BULLISH", "BEARISH") else 1.0
        adx_s       = ramp(adx, self.adx_trend - 5, ADX_STRONG_SOLO)   # soft-necessary

        trend_e = _combine(
            hard_vetoes=[veto_struct, veto_dir],
            soft_necessary=[adx_s],
            corroborators=[(W_TREND_ALIGN, align_val), (W_TREND_MOM, mom_val)],
        )
        bd = {"adx": round(adx, 2), "adx_s": round(adx_s, 3),
              "align_frac": round(align_frac, 3), "align_val": round(align_val, 3),
              "momentum": mom, "mom_val": mom_val, "structure_sequence": seq,
              "veto_struct": veto_struct, "veto_dir": veto_dir,
              "direction": direction, "trend_e": round(trend_e, 3)}

        if direction == "BULLISH":
            return {TRENDING_BULL: trend_e, TRENDING_BEAR: 0.0}, bd
        if direction == "BEARISH":
            return {TRENDING_BULL: 0.0, TRENDING_BEAR: trend_e}, bd
        return {TRENDING_BULL: 0.0, TRENDING_BEAR: 0.0}, bd

    def _breakout(self, vol_state, trend_state) -> Tuple[Optional[float], dict]:
        if vol_state is None:
            return None, {"reason": "no vol_state"}
        adx        = getattr(trend_state, "primary_adx", 0.0) if trend_state else 0.0
        atr_cur    = getattr(vol_state, "atr_current", 0.0)
        atr_avg    = max(getattr(vol_state, "atr_avg_20", 0.0), 1e-3)
        is_exp     = getattr(vol_state, "is_expanding", False)
        price_vs_bb = getattr(vol_state, "price_vs_bb", "INSIDE")

        atr_ratio = atr_cur / atr_avg
        expand_s  = ramp(atr_ratio, EXPAND_RATIO_LO, EXPAND_RATIO_HI) if is_exp \
                    else ramp(atr_ratio, EXPAND_RATIO_LO + 0.1, EXPAND_RATIO_HI + 0.1) * 0.6
        # momentum carry: current-ADX forgives a momentary inside-band print (Layer-1 legal)
        outside_s = 1.0 if price_vs_bb != "INSIDE" else ramp(adx, BREAKOUT_ADX_LO, BREAKOUT_ADX_HI)

        score = _combine(hard_vetoes=[], soft_necessary=[expand_s, outside_s], corroborators=[])
        bd = {"atr_ratio": round(atr_ratio, 3), "is_expanding": is_exp,
              "expand_s": round(expand_s, 3), "price_vs_bb": price_vs_bb,
              "adx": round(adx, 2), "outside_s": round(outside_s, 3),
              "score": round(score, 3)}
        return score, bd

    def _compression(self, vol_state, closes, atr) -> Tuple[Optional[float], dict]:
        if vol_state is None:
            return None, {"reason": "no vol_state"}
        bb_width_pct = getattr(vol_state, "bb_width_pct", 0.5)
        atr_state    = getattr(vol_state, "atr_state", "STABLE")
        bb_state     = getattr(vol_state, "bb_state", "NORMAL")
        is_exp       = getattr(vol_state, "is_expanding", False)

        narrow_s   = ramp(BB_WIDTH_COMPRESSION_PCT - bb_width_pct, 0.0, COMPRESS_WIDTH_SPAN)
        veto_notexp = 0.0 if (is_exp or atr_state == "EXPANDING") else 1.0
        squeeze_val = 1.0 if bb_state == "SQUEEZE" else 0.0

        bd = {"bb_width_pct": round(bb_width_pct, 3), "narrow_s": round(narrow_s, 3),
              "atr_state": atr_state, "bb_state": bb_state, "veto_notexp": veto_notexp}

        # Potential-energy read: flat center (veto) + tightening container + FADED
        # excursions (low crossings = energy stored, not released). Window path when
        # bars available; else a reduced-ceiling vol-only fallback (not blind).
        if closes is not None and atr is not None and len(closes) >= RANGE_WINDOW_BARS:
            w = closes[-RANGE_WINDOW_BARS:]
            ang = flat_angle_deg(w, atr)
            if ang is None:
                return None, {**bd, "reason": "angle uncomputable"}
            veto_flat = 0.0 if ang >= FLAT_ANGLE_CUT_DEG else 1.0
            osc_s = ramp(midline_crossings(w), OSC_CROSS_LO, OSC_CROSS_HI)
            stored_val = 1.0 - osc_s          # few crossings ⇒ energy absorbed, not spent
            score = _combine(
                hard_vetoes=[veto_flat, veto_notexp],
                soft_necessary=[narrow_s],
                corroborators=[(W_COMP_BASE, 1.0), (W_COMP_SQZ, squeeze_val),
                               (W_COMP_STORED, stored_val)],
            )
            bd.update({"angle": round(ang, 2), "veto_flat": veto_flat,
                       "crossings": midline_crossings(w), "osc_s": round(osc_s, 3),
                       "stored_val": round(stored_val, 3), "squeeze_val": squeeze_val,
                       "path": "window", "score": round(score, 3)})
            return score, bd
        else:
            # vol-only fallback: no flat veto, no crossings; reduced ceiling.
            score = _combine(hard_vetoes=[veto_notexp], soft_necessary=[narrow_s],
                             corroborators=[(0.5, 1.0), (0.5, squeeze_val)]) * 0.7
            bd.update({"squeeze_val": squeeze_val, "path": "vol_only_fallback",
                       "score": round(score, 3)})
            return score, bd

    def _ranging(self, vol_state, trend_state, closes, atr) -> Tuple[Optional[float], dict]:
        adx     = getattr(trend_state, "primary_adx", 0.0) if trend_state else 0.0
        is_exp  = getattr(vol_state, "is_expanding", False) if vol_state else False
        pbb     = getattr(vol_state, "price_vs_bb", "INSIDE") if vol_state else "INSIDE"

        if closes is not None and atr is not None and len(closes) >= RANGE_WINDOW_BARS:
            w = closes[-RANGE_WINDOW_BARS:]
            ang = flat_angle_deg(w, atr)
            if ang is None:
                return None, {"reason": "angle uncomputable"}
            if ang >= FLAT_ANGLE_CUT_DEG:
                return 0.0, {"angle": round(ang, 2), "veto_flat": 0.0, "score": 0.0}
            flat_s = ramp(FLAT_ANGLE_CUT_DEG - ang, 0.0, FLAT_ANGLE_SOFT_DEG)   # soft-necessary
            bb_width_pct = getattr(vol_state, "bb_width_pct", 0.5) if vol_state else 0.5
            room_s = ramp(bb_width_pct, RANGE_ROOM_LO, RANGE_ROOM_HI)           # soft-necessary
            cross  = midline_crossings(w)
            osc_s  = ramp(cross, OSC_CROSS_LO, OSC_CROSS_HI)                    # corroborator
            score  = _combine(hard_vetoes=[1.0], soft_necessary=[flat_s, room_s],
                              corroborators=[(W_RANGE_BASE, 1.0), (W_RANGE_OSC, osc_s)])
            bd = {"angle": round(ang, 2), "veto_flat": 1.0, "flat_s": round(flat_s, 3),
                  "bb_width_pct": round(bb_width_pct, 3), "room_s": round(room_s, 3),
                  "crossings": cross, "osc_s": round(osc_s, 3),
                  "path": "window", "score": round(score, 3)}
            return score, bd
        else:
            # reduced-ceiling quiet-range fallback (cannot see energetic chop —
            # that is exactly what the angle read adds when bars are present).
            quiet = (adx < self.adx_range and not is_exp and pbb == "INSIDE")
            score = 0.6 if quiet else 0.0
            return score, {"path": "quiet_fallback", "adx": round(adx, 2),
                           "is_expanding": is_exp, "price_vs_bb": pbb,
                           "score": score}

    def _sweep(self, liq_map) -> Tuple[Optional[float], dict]:
        if liq_map is None:
            return None, {"reason": "no liq_map"}
        sweep = getattr(liq_map, "recent_sweep", None)
        if sweep is None:
            return 0.0, {"reason": "no recent_sweep", "score": 0.0}
        reclaimed = getattr(sweep, "reclaimed", False)
        named     = getattr(sweep, "swept_named_level", "")
        beyond    = getattr(sweep, "closes_beyond", 0)
        rej_pct   = getattr(sweep, "rejection_pct", 0.0)
        age_bars  = getattr(liq_map, "sweep_age_bars", 999)

        veto_loc    = 1.0 if named else 0.0
        veto_reclaim = 1.0 if reclaimed else 0.0
        veto_accept  = 1.0 if beyond < SWEEP_ACCEPT_CLOSES else 0.0
        strength   = ramp(rej_pct, SWEEP_REJ_LO, SWEEP_REJ_HI)               # soft-necessary
        age_decay  = 0.5 ** (age_bars / SWEEP_HALFLIFE_BARS)                 # soft-necessary
        score = _combine(hard_vetoes=[veto_loc, veto_reclaim, veto_accept],
                         soft_necessary=[strength, age_decay], corroborators=[])
        bd = {"named": named, "reclaimed": reclaimed, "closes_beyond": beyond,
              "rejection_pct": round(rej_pct, 4), "strength": round(strength, 3),
              "age_bars": age_bars, "age_decay": round(age_decay, 3),
              "veto_loc": veto_loc, "veto_reclaim": veto_reclaim,
              "veto_accept": veto_accept, "score": round(score, 3)}
        return score, bd

    # -- public entry point -----------------------------------------------------

    def score(self, vol_state, trend_state, structure, liq_map,
              closes: Optional[List[float]] = None,
              atr: Optional[float] = None) -> ConfluenceResult:
        """
        Compute the instantaneous confluence vector. `closes` is the rolling
        1-min close window (≥ RANGE_WINDOW_BARS for the angle path); `atr` is the
        current ATR (VolatilityState.atr_current is the natural source). Both
        optional — absent, RANGING/COMPRESSION use reduced-ceiling fallbacks.
        """
        res = ConfluenceResult()

        tr_scores, tr_bd = self._trending(trend_state, structure)
        res.scores.update(tr_scores)
        res.breakdown["TRENDING"] = tr_bd

        res.scores[BREAKOUT_VOLATILE], res.breakdown[BREAKOUT_VOLATILE] = \
            self._breakout(vol_state, trend_state)
        res.scores[RANGING], res.breakdown[RANGING] = \
            self._ranging(vol_state, trend_state, closes, atr)
        res.scores[COMPRESSION], res.breakdown[COMPRESSION] = \
            self._compression(vol_state, closes, atr)
        res.scores[SWEEP_REVERSAL], res.breakdown[SWEEP_REVERSAL] = \
            self._sweep(liq_map)

        return res

    def evidence(self, vol_state, trend_state, structure, liq_map,
                 closes: Optional[List[float]] = None,
                 atr: Optional[float] = None) -> Dict[str, Optional[float]]:
        """Convenience: bare score vector for direct hand-off to the integrator."""
        return self.score(vol_state, trend_state, structure, liq_map, closes, atr).evidence()


# ── Standalone smoke test (runs only when executed directly; no import side effects)
if __name__ == "__main__":                     # pragma: no cover
    from types import SimpleNamespace as NS

    def mk_closes(kind, n=30, base=100.0):
        import random; random.seed(3)
        if kind == "trend":
            return [base + 0.5 * i + random.gauss(0, 0.1) for i in range(n)]
        if kind == "range":  # two-sided rotation about a flat center (whole cycles)
            return [base + 1.2 * math.sin(i / 1.6) + random.gauss(0, 0.05) for i in range(n)]
        if kind == "coil":   # flat center, excursions fading toward the close
            return [base + 1.2 * math.sin(i / 1.6) * (1 - 0.85 * i / n) + random.gauss(0, 0.03)
                    for i in range(n)]
        return [base] * n

    def derive_atr(closes):
        # mean absolute step = the random-walk excursion scale the angle models;
        # self-consistent stand-in for ATR on close-only synthetic tape.
        d = [abs(closes[i] - closes[i - 1]) for i in range(1, len(closes))]
        return sum(d) / max(len(d), 1)

    sc = RegimeConfluenceScorer()

    def show(tag, vol, tr, st, lq, closes, atr=None):
        atr = derive_atr(closes[-RANGE_WINDOW_BARS:])
        r = sc.score(vol, tr, st, lq, closes, atr)
        line = "  ".join(f"{k.split('_')[0][:5]}:{('None' if v is None else f'{v:.2f}')}"
                          for k, v in r.scores.items())
        print(f"{tag:10} {line}")
        return r

    # RANGING: flat center, active crossings, normal width
    vol_r = NS(atr_current=0.4, atr_avg_20=0.4, is_expanding=False, price_vs_bb="INSIDE",
               bb_width_pct=0.45, atr_state="STABLE", bb_state="NORMAL")
    tr_r  = NS(primary_adx=15, aligned_timeframes=1, total_timeframes=4,
               overall_direction="NEUTRAL", is_bullish=False, votes={})
    st_n  = NS(structure_sequence="MIXED")
    lq_0  = NS(recent_sweep=None, sweep_age_bars=999)
    r1 = show("RANGE", vol_r, tr_r, st_n, lq_0, mk_closes("range"), 0.4)

    # COMPRESSION: flat center, SQUEEZE, faded crossings, narrow width
    vol_c = NS(atr_current=0.2, atr_avg_20=0.4, is_expanding=False, price_vs_bb="INSIDE",
               bb_width_pct=0.08, atr_state="CONTRACTING", bb_state="SQUEEZE")
    r2 = show("COIL", vol_c, tr_r, st_n, lq_0, mk_closes("coil"), 0.2)

    # TRENDING_BULL: strong ADX, aligned, HH_HL, migrating center
    vol_t = NS(atr_current=0.6, atr_avg_20=0.4, is_expanding=True, price_vs_bb="ABOVE_UPPER",
               bb_width_pct=0.6, atr_state="EXPANDING", bb_state="EXPANDING")
    tr_t  = NS(primary_adx=40, aligned_timeframes=4, total_timeframes=4,
               overall_direction="BULLISH", is_bullish=True,
               votes={"5m": NS(momentum="ACCELERATING")})
    st_up = NS(structure_sequence="HH_HL")
    r3 = show("TREND_UP", vol_t, tr_t, st_up, lq_0, mk_closes("trend"), 0.6)

    # SWEEP: named zone, reclaimed, not accepted, fresh
    lq_s = NS(recent_sweep=NS(reclaimed=True, swept_named_level="PDH",
                              closes_beyond=0, rejection_pct=0.006), sweep_age_bars=1)
    r4 = show("SWEEP", vol_r, tr_r, st_n, lq_s, mk_closes("range"), 0.4)

    # sanity assertions
    assert r1.scores[RANGING] > r1.scores[COMPRESSION], "range should beat coil on range tape"
    assert r2.scores[COMPRESSION] > r2.scores[RANGING], "coil should beat range on coil tape"
    assert r3.scores[TRENDING_BULL] > 0.4 and r3.scores[RANGING] == 0.0, "trend up, range vetoed"
    assert r4.scores[SWEEP_REVERSAL] > 0.0, "fresh reclaimed named sweep should score"
    print("\nsmoke test OK — RANGING/COMPRESSION separate on the crossings axis as designed")
