# analysis/trade_readiness.py — options_trader_v3
# v1.2 — 2026-07-28 — ALL FACTOR BOUNDS ENV-OVERRIDABLE (OT_TR_*). v1.0/v1.1
#         env-ified only the STATE-MACHINE bars and left every FACTOR ramp as
#         a hardcoded literal — inconsistent with L1, where all 14 ramp bounds
#         are OT_RC_* overridable, and that property is exactly what let the
#         room_s refit be trialled on one box with instant rollback instead of
#         a fleet redeploy. First live day (2026-07-28) proved the cost: the
#         conviction ramp topped out at 0.65 while fleet L2 conviction ran
#         0.59-0.83, so conv_val pegged at 1.0 on roughly half the boxes and
#         ten symbols reported an identical r=0.65. Correcting that guess
#         should be an env flip, not a bake. Now: 13 factor bounds + 8
#         categorical momentum weights are OT_TR_*.
#         DEFAULTS DELIBERATELY UNCHANGED. The pegged bound is NOT re-guessed
#         here — every readiness row already journals the RAW conv/approach/
#         distance alongside the ramped value, so the digest (v1.1) fits the
#         bounds from the observed distribution the way room_s was fitted.
#         Guessing a second time is the error this whole workstream exists to
#         stop. Pegging does not corrupt the fit: the raw inputs are logged
#         un-ramped, and nothing gates on R.
# v1.1 — 2026-07-27 — STAGED PICKS (still LOG-ONLY). While a directional
#         strategy (continuation, sweep) is ARMED and a chain is on ctx, the
#         engine now computes the contract it WOULD select — through the SAME
#         selector the live entry uses (options_chain.select_sweep_strike) —
#         using a SMOOTHED conviction (wall-clock EMA, same half-life idiom as
#         slope) instead of the instantaneous spike, and journals it as
#         `readiness_staged_pick` (throttled to the heartbeat cadence + always
#         beside would_fire). When the real trigger later fires, the journal
#         holds staged-pick rows next to the trigger-tick pick, so the chain
#         archive can answer IN DOLLARS whether calm selection beats spike
#         selection — before staged picks ever touch an order. The PLTR strike
#         (0.62 spike -> 0.16 delta -> unreachable) is the failure class this
#         measures. Condor/butterfly staged ladders deferred (multi-leg).
# v1.0 — 2026-07-27 — NEW FILE. Trade-trigger READINESS engine (LOG-ONLY).
#
#   The L1 excavation (regime_confluence v1.3) made the REGIME scores honest
#   graded evidence. This module applies the same thinking one layer up, to the
#   TRADE TRIGGERS: each strategy's pre-trigger confluence becomes a graded
#   readiness R in [0,1] evaluated every ~15s tick, with a dt-aware SLOPE so
#   the system can tell whether a trade's confluence is RISING or FALLING, and
#   an arming state machine (DORMANT -> STAGING -> ARMED -> would_fire) that
#   anticipates when a trade will be ready to fire.
#
#   Operator's framing (2026-07-27): assessment of what the market is doing in
#   the context of where it IS right now, where it's BEEN, and where the
#   lowest-timeframe signals suggest it is HEADING.
#     - now:     instantaneous strategy-local geometry + L1-derived state
#     - been:    the L2 committed conviction (persistence lives in Layer 2)
#     - heading: EMA'd dR/dt on the 15-second tick cadence
#
#   The last gate is binary regardless — that is the nature of a trigger. This
#   module's job is to make that bit the LAST place information collapses, not
#   the first: everything upstream stays graded, journaled, and visible.
#
#   LOG-ONLY BY DESIGN (pitchfork weight-0 precedent): this engine gates
#   NOTHING and changes NO fire decision. It observes and journals. It runs
#   inside the frozen-baseline window precisely because it cannot move a label
#   or a trade; its journal rows are the calibration data for the bars that
#   will eventually gate. It does not validate the Layer-1 data — it gives
#   clues about what the Layer-1 data believes, per tick, per strategy.
#
#   LAYER BOUNDARY: this is L3/strategy-level. Referencing tradability context
#   is legal here. It reads L1/L2 OUTPUTS (regime label, conviction) and engine
#   states; it writes nothing back. L1 stays instantaneous and frozen.
#
#   TICK-VS-BAR RULE (July-20 audit): all temporal math is WALL-CLOCK dt-aware.
#   No per-evaluate counters anywhere in this file — the 15s loop can call
#   assess() at any cadence, including the 4x-duplicated-candle case that
#   inflated bars_since_break.
#
#   RESTART: state is in-memory and resets on restart. Acceptable for a
#   log-only observer — a restart shows up in the journal as a DORMANT reset,
#   which is itself useful evidence.
#
#   ORB IS EXEMPT (standing directive): the ORB is intentionally mechanical
#   and already has its own arming machine + retest_check journaling.

from __future__ import annotations

import os as _os
import time
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

log = logging.getLogger(__name__)

# ── Engine idiom: same grammar as the confluence scorer ───────────────────────
try:
    from analysis.regime_confluence import ramp, _combine, momentum_val
except Exception:                              # pragma: no cover — isolation
    def ramp(x, lo, hi):
        if hi <= lo:
            return 1.0 if x >= hi else 0.0
        return min(max((x - lo) / (hi - lo), 0.0), 1.0)

    def _combine(hard_vetoes, soft_necessary, corroborators):
        for v in hard_vetoes:
            if v <= 0.0:
                return 0.0
        prod = 1.0
        for s in soft_necessary:
            prod *= max(0.0, min(1.0, s))
        csum = sum(w * max(0.0, min(1.0, val)) for w, val in corroborators) \
            if corroborators else 1.0
        return max(0.0, min(1.0, prod * csum))

    def momentum_val(mom):
        return {"ACCELERATING": 1.0, "FLAT": 0.5, "DECELERATING": 0.0,
                "": 0.0}.get(mom, 0.0)


def _envf(name: str, default: float) -> float:
    try:
        return float(_os.environ.get("OT_TR_" + name, default))
    except (TypeError, ValueError):
        return default


# ── Knobs (ALL PRIOR — calibrate from the readiness journal, never one day) ──
# Bars are on R in [0,1]. Slope is in R-units PER MINUTE.
TR_STAGE_BAR        = _envf("STAGE_BAR", 0.35)   # R >= this -> STAGING
TR_ARM_BAR          = _envf("ARM_BAR", 0.55)     # R >= this AND slope > 0 -> ARMED
TR_FIRE_BAR         = _envf("FIRE_BAR", 0.70)    # R >= this AND slope > 0 -> would_fire (log event)
TR_DEARM_SLOPE      = _envf("DEARM_SLOPE", -0.15)  # ARMED + slope <= this -> de-arm (collapse)
TR_HYSTERESIS       = _envf("HYSTERESIS", 0.05)  # bars relax by this on the way DOWN
TR_SLOPE_HALFLIFE_S = _envf("SLOPE_HALFLIFE_S", 60.0)   # EMA half-life for dR/dt
TR_HEARTBEAT_S      = _envf("HEARTBEAT_S", 60.0)  # journal sample cadence while >= STAGING
TR_MAX_DT_S         = _envf("MAX_DT_S", 120.0)   # dt gaps beyond this reset the slope (stale)
TR_CONT_TARGET_DELTA = _envf("CONT_TARGET_DELTA", 0.45)  # continuation staged-pick delta (PRIOR)
TR_CONV_HALFLIFE_S   = _envf("CONV_HALFLIFE_S", 90.0)    # smoothed-conviction EMA half-life

# ── v1.2 FACTOR BOUNDS (all PRIOR, all OT_TR_* overridable) ──────────────────
# Shared conviction ramp — used by all four strategies. KNOWN MIS-FIT as of
# 2026-07-28: fleet L2 conviction observed 0.59-0.83, so HI=0.65 pegs. Refit
# from the digest's conv percentiles (p25->p95 convention), not by guess.
TR_CONV_LO          = _envf("CONV_LO", 0.25)
TR_CONV_HI          = _envf("CONV_HI", 0.65)
# Continuation: distance from the BB midline in ATR. Beyond HI the trend is
# still extended and the pullback has not arrived — 0 is correct there.
TR_PULL_ATR_LO      = _envf("PULL_ATR_LO", 0.35)
TR_PULL_ATR_HI      = _envf("PULL_ATR_HI", 1.05)
# Sweep freshness half-life, in bars.
TR_FRESH_HALFLIFE_B = _envf("FRESH_HALFLIFE_B", 3.0)
# Condor: approach fraction toward the band edge (the trigger's own graded
# input, kept graded here), and range room.
TR_APPROACH_LO      = _envf("APPROACH_LO", 0.30)
TR_APPROACH_HI      = _envf("APPROACH_HI", 0.90)
TR_ROOM_LO          = _envf("ROOM_LO", 0.17)
TR_ROOM_HI          = _envf("ROOM_HI", 1.00)
# Butterfly: BB-width narrowness, measured below this pivot across this span.
TR_NARROW_PIVOT     = _envf("NARROW_PIVOT", 0.20)
TR_NARROW_SPAN      = _envf("NARROW_SPAN", 0.15)
# Categorical momentum weights. Continuation reads momentum as RESUMPTION
# (accelerating = resuming now); sweep reads it as EXHAUSTION (decelerating =
# move spent). Empty string = no 5m vote and earns NOTHING in both, per the
# trend_engine v3.2 contract.
TR_CONT_MOM_ACC     = _envf("CONT_MOM_ACC", 1.0)
TR_CONT_MOM_FLAT    = _envf("CONT_MOM_FLAT", 0.6)
TR_CONT_MOM_DEC     = _envf("CONT_MOM_DEC", 0.3)
TR_SWEEP_MOM_DEC    = _envf("SWEEP_MOM_DEC", 1.0)
TR_SWEEP_MOM_FLAT   = _envf("SWEEP_MOM_FLAT", 0.5)
TR_SWEEP_MOM_ACC    = _envf("SWEEP_MOM_ACC", 0.0)

# Machine states
DORMANT, STAGING, ARMED = "DORMANT", "STAGING", "ARMED"

# Corroborator weights (PRIOR; sum ≈ 1.0 per strategy). Same design-derived
# convention as regime_confluence v1.3: each block states the minimum evidence
# that should just barely stage, and a lone factor stays under TR_ARM_BAR.
W_CONT_CONV, W_CONT_PULL, W_CONT_MOM = 0.40, 0.35, 0.25
W_SWEEP_CONV, W_SWEEP_FRESH, W_SWEEP_EXH = 0.40, 0.25, 0.35
W_CNDR_APPROACH, W_CNDR_CONV, W_CNDR_ROOM = 0.45, 0.35, 0.20
W_BFLY_CONV, W_BFLY_SQZ, W_BFLY_NARROW = 0.40, 0.30, 0.30


@dataclass
class ReadinessState:
    """Per-strategy readiness track. All temporal fields are wall-clock."""
    machine:    str   = DORMANT
    r:          float = 0.0
    slope:      float = 0.0        # R-units per MINUTE, EMA'd
    last_ts:    float = 0.0        # wall-clock of last assess
    last_beat:  float = 0.0        # wall-clock of last heartbeat journal row
    peak_r:     float = 0.0        # session peak while >= STAGING (resets on DORMANT)
    conv_ema:   float = 0.0        # v1.1: smoothed conviction (wall-clock EMA)
    factors:    dict  = field(default_factory=dict)


class TradeReadinessEngine:
    """
    One instance per box. assess_all() every tick; emits journal rows through
    the injected emit callable (signal_journal.journal) on state transitions
    and on a throttled heartbeat while a strategy is >= STAGING.
    """

    STRATEGIES = ("continuation", "sweep", "condor_call", "condor_put", "butterfly")

    def __init__(self, emit=None, clock=time.time, contract_ctx=None):
        self._emit = emit          # callable(event:str, **sections) or None
        self._clock = clock
        self._contract_ctx = contract_ctx   # signal_journal.contract_ctx (None-safe)
        try:                                # the LIVE selector — same code path
            from data.options_chain import get_chain_fetcher
            self._fetcher = get_chain_fetcher()
        except Exception:
            self._fetcher = None
        self.tracks: Dict[str, ReadinessState] = {
            k: ReadinessState() for k in self.STRATEGIES
        }

    # ── factor computation (READ-ONLY over already-computed state) ───────────

    def _continuation(self, ctx, regime) -> Tuple[float, dict]:
        """Trend pullback: trending label, conviction, midline proximity, resumption."""
        label = getattr(regime, "primary_regime", "") or ""
        conv  = float(getattr(regime, "conviction", 0.0) or 0.0)
        vol   = ctx.get("vol"); trend = ctx.get("trend")
        px    = float(ctx.get("price") or 0.0)
        trending = 1.0 if str(label).upper().endswith(("TRENDING_BULL", "TRENDING_BEAR")) else 0.0
        mid = float(getattr(vol, "bb_middle", 0.0) or 0.0) if vol else 0.0
        atr = float(getattr(vol, "atr_current", 0.0) or 0.0) if vol else 0.0
        # proximity: 1.0 at the midline, fading to 0 at 3x the entry tolerance
        # (0.35 ATR is the strategy's at-midline band; readiness sees the approach)
        if mid > 0 and atr > 0 and px > 0:
            dist_atr = abs(px - mid) / atr
            pull_val = 1.0 - ramp(dist_atr, TR_PULL_ATR_LO, TR_PULL_ATR_HI)
        else:
            pull_val = 0.0
        mom = getattr(trend, "primary_momentum", "") if trend else ""
        # resumption wants DECELERATING -> ACCELERATING; readiness grades the
        # precondition state: ACCELERATING = resuming now, FLAT = coiled, DECEL = still pulling back
        mom_val = {"ACCELERATING": TR_CONT_MOM_ACC, "FLAT": TR_CONT_MOM_FLAT,
                   "DECELERATING": TR_CONT_MOM_DEC, "": 0.0}.get(mom, 0.0)
        conv_val = ramp(conv, TR_CONV_LO, TR_CONV_HI)   # graded, not a cliff
        r = _combine(hard_vetoes=[trending], soft_necessary=[],
                     corroborators=[(W_CONT_CONV, conv_val),
                                    (W_CONT_PULL, pull_val),
                                    (W_CONT_MOM,  mom_val)])
        return r, {"label": label, "conv": round(conv, 3), "conv_val": round(conv_val, 3),
                   "dist_atr": (None if not (mid > 0 and atr > 0 and px > 0)
                                else round(abs(px - mid) / atr, 3)),
                   "pull_val": round(pull_val, 3), "mom": mom, "mom_val": mom_val}

    def _sweep(self, ctx, regime) -> Tuple[float, dict]:
        """Exhaustion reversal: sweep label conviction, freshness, trend spent."""
        label = str(getattr(regime, "primary_regime", "") or "")
        conv  = float(getattr(regime, "conviction", 0.0) or 0.0)
        liq   = ctx.get("liq_map"); trend = ctx.get("trend")
        is_sweep = 1.0 if label.upper().endswith("SWEEP_REVERSAL") else 0.0
        age = float(getattr(liq, "sweep_age_bars", 999) or 999) if liq else 999.0
        fresh_val = 0.5 ** (age / max(TR_FRESH_HALFLIFE_B, 1e-6))
        mom = getattr(trend, "primary_momentum", "") if trend else ""
        exh_val = {"DECELERATING": TR_SWEEP_MOM_DEC, "FLAT": TR_SWEEP_MOM_FLAT,
                   "ACCELERATING": TR_SWEEP_MOM_ACC, "": 0.0}.get(mom, 0.0)
        conv_val = ramp(conv, TR_CONV_LO, TR_CONV_HI)
        r = _combine(hard_vetoes=[is_sweep], soft_necessary=[],
                     corroborators=[(W_SWEEP_CONV, conv_val),
                                    (W_SWEEP_FRESH, fresh_val),
                                    (W_SWEEP_EXH, exh_val)])
        return r, {"label": label, "conv": round(conv, 3), "age_bars": age,
                   "fresh_val": round(fresh_val, 3), "mom": mom, "exh_val": exh_val}

    def _condor_side(self, ctx, regime, side: str) -> Tuple[float, dict]:
        """
        One condor side. The graded approach fraction the entry trigger already
        computes and then collapses at CONDOR_TRIGGER_APPROACH — here it is
        KEPT graded. Band edges proxy the short strikes (readiness runs before
        strike selection; the real trigger still uses the selected strikes).
        """
        label = str(getattr(regime, "primary_regime", "") or "")
        conv  = float(getattr(regime, "conviction", 0.0) or 0.0)
        vol   = ctx.get("vol"); px = float(ctx.get("price") or 0.0)
        ranging = 1.0 if label.upper().endswith("RANGING") else 0.0
        mid = float(getattr(vol, "bb_middle", 0.0) or 0.0) if vol else 0.0
        up  = float(getattr(vol, "bb_upper", 0.0) or 0.0) if vol else 0.0
        lo  = float(getattr(vol, "bb_lower", 0.0) or 0.0) if vol else 0.0
        approach = 0.0
        if px > 0 and mid > 0 and up > lo:
            if side == "call" and up > mid:
                approach = max(0.0, min((px - mid) / (up - mid), 1.5))
            elif side == "put" and mid > lo:
                approach = max(0.0, min((mid - px) / (mid - lo), 1.5))
        # graded through the 0.65 trigger point: staging begins well before it
        appr_val = ramp(approach, TR_APPROACH_LO, TR_APPROACH_HI)
        room_val = ramp(float(getattr(vol, "bb_width_pct", 0.0) or 0.0) if vol else 0.0,
                        TR_ROOM_LO, TR_ROOM_HI)   # a condor needs room
        conv_val = ramp(conv, TR_CONV_LO, TR_CONV_HI)
        r = _combine(hard_vetoes=[ranging], soft_necessary=[],
                     corroborators=[(W_CNDR_APPROACH, appr_val),
                                    (W_CNDR_CONV, conv_val),
                                    (W_CNDR_ROOM, room_val)])
        return r, {"label": label, "conv": round(conv, 3), "side": side,
                   "approach": round(approach, 3), "appr_val": round(appr_val, 3),
                   "room_val": round(room_val, 3)}

    def _butterfly(self, ctx, regime) -> Tuple[float, dict]:
        """Compression play: coil conviction, squeeze, narrowness degree."""
        label = str(getattr(regime, "primary_regime", "") or "")
        conv  = float(getattr(regime, "conviction", 0.0) or 0.0)
        vol   = ctx.get("vol")
        coil = 1.0 if label.upper().endswith("COMPRESSION") else 0.0
        sqz_val = 1.0 if (getattr(vol, "bb_state", "") == "SQUEEZE" if vol else False) else 0.0
        width = float(getattr(vol, "bb_width_pct", 0.5) or 0.5) if vol else 0.5
        narrow_val = ramp(TR_NARROW_PIVOT - width, 0.0, TR_NARROW_SPAN)
        conv_val = ramp(conv, TR_CONV_LO, TR_CONV_HI)
        r = _combine(hard_vetoes=[coil], soft_necessary=[],
                     corroborators=[(W_BFLY_CONV, conv_val),
                                    (W_BFLY_SQZ, sqz_val),
                                    (W_BFLY_NARROW, narrow_val)])
        return r, {"label": label, "conv": round(conv, 3),
                   "squeeze_val": sqz_val, "narrow_val": round(narrow_val, 3)}

    # ── the temporal core: slope + state machine ─────────────────────────────

    def _advance(self, key: str, r: float, factors: dict, now: float):
        tr = self.tracks[key]
        # dt-aware slope: EMA of dR/dt in R-units/minute. Wall-clock only.
        dt = now - tr.last_ts if tr.last_ts > 0 else 0.0
        if dt <= 0 or dt > TR_MAX_DT_S:
            tr.slope = 0.0                       # cold start or stale gap: no heading claim
        else:
            inst = (r - tr.r) / (dt / 60.0)
            alpha = 1.0 - 0.5 ** (dt / TR_SLOPE_HALFLIFE_S)
            tr.slope = tr.slope + alpha * (inst - tr.slope)
        prev_machine, prev_r = tr.machine, tr.r
        tr.r, tr.last_ts, tr.factors = r, now, factors

        # state machine with hysteresis; bars relax by TR_HYSTERESIS going down
        m = tr.machine
        if m == DORMANT:
            if r >= TR_STAGE_BAR:
                m = STAGING
        if m == STAGING:
            if r >= TR_ARM_BAR and tr.slope > 0:
                m = ARMED
            elif r < TR_STAGE_BAR - TR_HYSTERESIS:
                m = DORMANT
        if m == ARMED:
            if tr.slope <= TR_DEARM_SLOPE or r < TR_ARM_BAR - TR_HYSTERESIS:
                m = STAGING if r >= TR_STAGE_BAR else DORMANT
        would_fire = (m == ARMED and r >= TR_FIRE_BAR and tr.slope > 0)

        if m != DORMANT:
            tr.peak_r = max(tr.peak_r, r)
        elif prev_machine != DORMANT:
            tr.peak_r = 0.0

        transition = (m != prev_machine)
        tr.machine = m
        return transition, would_fire, prev_machine

    def _journal(self, key: str, event: str, prev: Optional[str] = None):
        if self._emit is None:
            return
        tr = self.tracks[key]
        try:
            self._emit(event, readiness={
                "strategy": key, "machine": tr.machine, "prev": prev,
                "r": round(tr.r, 3), "slope_per_min": round(tr.slope, 4),
                "peak_r": round(tr.peak_r, 3), "factors": tr.factors,
                "bars": {"stage": TR_STAGE_BAR, "arm": TR_ARM_BAR,
                         "fire": TR_FIRE_BAR}})
        except Exception as e:                    # noqa: BLE001 — log-only, never the loop
            log.debug(f"readiness journal skipped: {e}")

    # ── public entry point ───────────────────────────────────────────────────

    def assess_all(self, ctx: dict, regime) -> Dict[str, ReadinessState]:
        """
        Evaluate every strategy's readiness for this tick. Never raises.
        Call every tick, including while halted or holding a position — the
        observational record is the point.
        """
        now = self._clock()
        try:
            computed = {
                "continuation": self._continuation(ctx, regime),
                "sweep":        self._sweep(ctx, regime),
                "condor_call":  self._condor_side(ctx, regime, "call"),
                "condor_put":   self._condor_side(ctx, regime, "put"),
                "butterfly":    self._butterfly(ctx, regime),
            }
        except Exception as e:                    # noqa: BLE001
            log.debug(f"readiness assess skipped: {e}")
            return self.tracks
        conv_now = float(getattr(regime, "conviction", 0.0) or 0.0)
        for key, (r, factors) in computed.items():
            tr = self.tracks[key]
            # v1.1: smoothed conviction — the calm number staged picks use.
            dtc = now - tr.last_ts if tr.last_ts > 0 else 0.0
            if dtc <= 0 or dtc > TR_MAX_DT_S:
                tr.conv_ema = conv_now
            else:
                a = 1.0 - 0.5 ** (dtc / TR_CONV_HALFLIFE_S)
                tr.conv_ema = tr.conv_ema + a * (conv_now - tr.conv_ema)
            transition, would_fire, prev = self._advance(key, r, factors, now)
            beat = (tr.machine != DORMANT and (now - tr.last_beat) >= TR_HEARTBEAT_S)
            if transition:
                self._journal(key, "readiness", prev=prev)
            elif beat:
                tr.last_beat = now
                self._journal(key, "readiness")
            if would_fire:
                self._journal(key, "readiness_would_fire")
            # v1.1: staged pick — ARMED only, throttled to beats/transitions/fires.
            if tr.machine == ARMED and (transition or beat or would_fire):
                self._staged_pick(key, ctx, tr, would_fire)
        return self.tracks

    # ── v1.1: the staged pick (LOG-ONLY — never touches an order) ────────────

    def _staged_pick(self, key: str, ctx: dict, tr: ReadinessState, at_fire: bool):
        if key not in ("continuation", "sweep") or self._fetcher is None:
            return
        chain = ctx.get("chain")
        if chain is None:
            return
        try:
            if key == "sweep":
                liq = ctx.get("liq_map")
                sweep = getattr(liq, "recent_sweep", None) if liq else None
                kind = getattr(sweep, "kind", "") if sweep else ""
                direction = "short" if kind == "high_sweep" else ("long" if kind == "low_sweep" else "")
                if not direction:
                    return
                try:
                    from strategy.sweep_reversal_strategy import _sweep_target_delta
                    target = _sweep_target_delta(tr.conv_ema)
                except Exception:
                    target = 0.20
            else:  # continuation: with the trend
                label = str(tr.factors.get("label", "") or "")
                direction = "long" if label.upper().endswith("TRENDING_BULL") else                             ("short" if label.upper().endswith("TRENDING_BEAR") else "")
                if not direction:
                    return
                target = TR_CONT_TARGET_DELTA
            contract = self._fetcher.select_sweep_strike(chain, direction, target)
            if contract is None or self._emit is None:
                return
            cctx = self._contract_ctx(contract) if self._contract_ctx else {
                "strike": getattr(contract, "strike", None),
                "delta":  getattr(contract, "delta", None),
                "bid":    getattr(contract, "bid", None),
                "ask":    getattr(contract, "ask", None),
                "mark":   getattr(contract, "mark", None)}
            self._emit("readiness_staged_pick", staged={
                "strategy": key, "direction": direction, "at_would_fire": at_fire,
                "target_delta": round(float(target), 4),
                "conv_ema": round(tr.conv_ema, 3),
                "r": round(tr.r, 3), "slope_per_min": round(tr.slope, 4),
                "contract": cctx})
        except Exception as e:                    # noqa: BLE001 — log-only
            log.debug(f"staged pick skipped: {e}")


# ── Standalone smoke test ─────────────────────────────────────────────────────
if __name__ == "__main__":                        # pragma: no cover
    from types import SimpleNamespace as NS

    rows = []
    eng = TradeReadinessEngine(emit=lambda ev, **s: rows.append((ev, s)),
                               clock=lambda: eng._t)
    eng._t = 1000.0

    vol = NS(bb_middle=100.0, bb_upper=102.0, bb_lower=98.0,
             atr_current=0.5, bb_width_pct=0.45, bb_state="NORMAL")
    trend = NS(primary_momentum="DECELERATING")

    def tick(px, conv, mom, dt=15.0):
        eng._t += dt
        trend.primary_momentum = mom
        ctx = {"vol": vol, "trend": trend, "liq_map": None, "price": px}
        regime = NS(primary_regime="TRENDING_BULL", conviction=conv)
        eng.assess_all(ctx, regime)
        return eng.tracks["continuation"]

    # RISING confluence: pullback approaches the midline, conviction firms,
    # momentum flips DECEL -> FLAT -> ACCELERATING. Readiness must climb
    # DORMANT -> STAGING -> ARMED and emit would_fire at the top.
    seq = [(101.2, 0.30, "DECELERATING"), (101.0, 0.35, "DECELERATING"),
           (100.8, 0.40, "DECELERATING"), (100.6, 0.45, "FLAT"),
           (100.45, 0.50, "FLAT"), (100.3, 0.55, "FLAT"),
           (100.2, 0.60, "ACCELERATING"), (100.1, 0.62, "ACCELERATING"),
           (100.05, 0.65, "ACCELERATING")]
    path = []
    for px, cv, mom in seq:
        tr = tick(px, cv, mom)
        path.append((round(tr.r, 3), round(tr.slope, 3), tr.machine))
    print("rising path (r, slope/min, machine):")
    for p in path:
        print("  ", p)
    assert path[0][2] == DORMANT and path[-1][2] == ARMED, "must climb to ARMED"
    assert any(m == STAGING for _, _, m in path), "must pass through STAGING"
    assert all(b[0] >= a[0] for a, b in zip(path, path[1:])), "R must be monotone rising here"
    assert any(ev == "readiness_would_fire" for ev, _ in rows), "would_fire must emit at the top"

    # FALLING confluence: same level, slope collapses (wick-flicker class).
    # ARMED must de-arm on slope, not wait for the level to break.
    for px, cv, mom in [(100.6, 0.50, "FLAT"), (101.1, 0.40, "DECELERATING"),
                        (101.5, 0.32, "DECELERATING")]:
        tr = tick(px, cv, mom)
    print("after collapse:", (round(tr.r, 3), round(tr.slope, 3), tr.machine))
    assert tr.machine != ARMED, "slope collapse must de-arm"

    trans = [s["readiness"]["machine"] for ev, s in rows if ev == "readiness"]
    print(f"journal rows: {len(rows)} (transitions+beats), machines seen: {sorted(set(trans))}")
    print("smoke test OK — readiness rises with confluence, arms with slope, de-arms on collapse")
