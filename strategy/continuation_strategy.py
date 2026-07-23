"""
strategy/continuation_strategy.py — Trend-continuation on pullback.
v1.2 — 2026-07-22 — stop backstop 40%% -> 25%% (CONTINUATION_STOP_LOSS_PCT now
        lives in config, env OT_CONT_STOP_PCT). Paired with exit_engine v4.0:
        5m-anchored trail + theta-bleed enabled for this strategy.
v1.1 — 2026-07-22 — UNBLOCKED (defect W). This strategy could NEVER fire.
        It read `getattr(trend, "momentum", "")`, but momentum lives on
        TrendVote (per-timeframe) and was never aggregated onto TrendState —
        the object main.py actually passes in. So momentum was ALWAYS "",
        and BOTH paths dead-ended before ever reaching strike selection:
          standalone: "" != "ACCELERATING"          -> return None, every tick
          handoff:    "" not in (ACCELERATING,...)  -> return None, every tick
        Every gate above it (trending regime, conviction floor, midline
        proximity, pullback depth) could pass perfectly and the trade still
        died here. The getattr default swallowed the missing attribute, so it
        threw no error and logged nothing — it looked exactly like "conditions
        never set up". Live from 2026-07-18 deploy to this fix: ZERO fires
        fleet-wide, by construction.
        FIX: read trend.primary_momentum (trend_engine v3.2 surfaces it from
        the 5m vote, same as primary_adx).
        ALSO: the resumption vocabulary was wrong. This checked for "STEADY",
        which trend_engine NEVER emits — its values are ACCELERATING /
        DECELERATING / FLAT. "STEADY" was a phantom, so even correctly wired
        the handoff path would have been stricter than designed. The intent
        ("handoff accepts steady, standalone demands acceleration") now maps
        onto the REAL vocabulary: handoff accepts ACCELERATING or FLAT (i.e.
        not actively decelerating against us); standalone demands
        ACCELERATING. "" (no 5m vote) blocks BOTH — unknown is never a green
        light.

v1.0 — 2026-07-18 — The trend-native trade the trend_engine v3.1 fix enables.
        Fires ONLY when regime is trending (a high bar now that direction
        resolves). Waits for price to pull back to the BB midline, then enters
        on a LOW-BAR resumption (momentum flips back toward the trend). The
        intelligence lives in the EXIT (exhaustion detection), not the entry —
        "make entry easy, make exit smart."

DESIGN (per spec, options_trader_v3 continuation-trade decisions):
  GATE       regime TRENDING_BULL/BEAR + conviction floor + pullback not so
             deep the trend is arguably broken.
  LEVEL      BB midline (vol_state.bb_middle) — dynamic support in an uptrend,
             resistance in a downtrend. Reuses the condor anchor.
  ENTRY      low bar: trend alive + price returned to the midline + momentum
             flipping back toward the trend (DECELERATING -> ACCELERATING).
  STOP       regime-change OR MAX_LOSS_PCT (40%), whichever first. Regime
             invalidation IS the smart stop (the trade is defined by the trend).
             underlying_stop set just past the pullback extreme for reference /
             structure, but the governing exits are regime-flip + the 40% floor.
  EXIT       exhaustion-based (owned by exit_engine, informed here via setup):
             momentum divergence + extension-from-midline; trail arms on the
             resumption confirmation so theta goes silent immediately.
  VEHICLE    debit directional (long call in an uptrend, long put in a downtrend).
  CONTEXT    two entry paths — ORB-runaway HANDOFF (looser: the runaway already
             proved directional force) and STANDALONE mid-session (stricter:
             self-sourced trend+pullback+resumption). handoff flag toggles it.

SAFETY: this module is inert until wired in AND enabled. main.py registers it
NOTE (v1.1): earlier text here described a CONTINUATION_ENABLED flag
(default False, "ships dark"). No such flag was ever defined or checked
anywhere in the repo — the strategy dispatches live from main.py
Priority 2.5. The claim was stale doc, not a real gate; what actually
kept it dark was the momentum defect above. Left here so nobody goes
hunting for a flag that does not exist. Historical text follows:
behind CONTINUATION_ENABLED (default False) so it ships dark and is proven in
paper/backtest before it can affect live dispatch.
"""

from __future__ import annotations

import logging
from typing import Optional

from analysis.regime_classifier import RegimeState, Regime
from analysis.volatility_engine import VolatilityState
from analysis.trend_engine import TrendState
from strategy.base_strategy import BaseOptionsStrategy, OptionsSignal

logger = logging.getLogger(__name__)

# ── Tunables (env-overridable at wire-in time; conservative defaults) ─────────
CONTINUATION_CONV_FLOOR      = 0.45   # min regime conviction to consider the trade
CONTINUATION_MIDLINE_ATR     = 0.35   # "at the midline": |price-mid| <= this * ATR
CONTINUATION_MAX_PULLBACK_R  = 0.60   # pullback deeper than this frac of the leg = trend broken, skip
# v1.2 (2026-07-22): sourced from config (env OT_CONT_STOP_PCT), tightened
# 0.40 -> 0.25. Regime-flip remains the PRIMARY exit; this is the backstop.
from config import CONTINUATION_STOP_LOSS_PCT   # 0.25 default
CONTINUATION_TP_PCT          = 1.0    # nominal; runner is exhaustion-trailed, not TP-capped
CONTINUATION_HANDOFF_CONV_RELAX = 0.10  # handoff path lowers the conviction floor by this


class ContinuationStrategy(BaseOptionsStrategy):
    """Trend-continuation entry on a pullback to the BB midline."""

    def name(self) -> str:
        return "ContinuationStrategy"

    def generate_signal(self,
                        *,
                        regime: RegimeState,
                        vol_state: VolatilityState,
                        trend: TrendState,
                        chain,
                        current_price: float,
                        is_handoff: bool = False,
                        macro=None) -> Optional[OptionsSignal]:
        """
        Return an OptionsSignal if a trend-continuation pullback entry sets up,
        else None. `is_handoff=True` is the looser ORB-runaway path.
        """
        # ── 1. GATE: must be a trending regime ──────────────────────────────
        rgm = regime.primary_regime
        if rgm == Regime.TRENDING_BULL:
            direction, option_side = "long", "call"
        elif rgm == Regime.TRENDING_BEAR:
            direction, option_side = "short", "put"
        else:
            return None  # not trending → this trade does not exist

        conv_floor = CONTINUATION_CONV_FLOOR
        if is_handoff:
            conv_floor -= CONTINUATION_HANDOFF_CONV_RELAX  # runaway vouched for direction
        if regime.conviction < conv_floor:
            return None

        # ── 2. LEVEL: price must have pulled back TO the BB midline ─────────
        mid = getattr(vol_state, "bb_middle", 0.0)
        atr = getattr(vol_state, "atr_current", 0.0)
        if mid <= 0 or atr <= 0:
            return None
        at_midline = abs(current_price - mid) <= CONTINUATION_MIDLINE_ATR * atr
        if not at_midline:
            return None

        # pullback not so deep the trend is broken: price should still be on the
        # trend side of the midline structurally (bull: not far below; bear: not
        # far above). Depth measured in ATR as a proxy for "fraction of the leg".
        if direction == "long"  and current_price < mid - CONTINUATION_MAX_PULLBACK_R * atr:
            return None
        if direction == "short" and current_price > mid + CONTINUATION_MAX_PULLBACK_R * atr:
            return None

        # ── 3. ENTRY (LOW BAR): momentum flipping back toward the trend ─────
        # Resumption is intentionally easy — protection lives in the exit. We
        # require the trend engine's momentum to be re-asserting in the trend
        # direction (not still decelerating against us).
        # v1.1: primary_momentum (5m vote, surfaced by trend_engine v3.2).
        # NOT `trend.momentum` — that attribute does not exist on TrendState
        # and getattr silently returned "", hard-blocking this trade forever.
        momentum = getattr(trend, "primary_momentum", "") or ""
        if not momentum:
            return None          # no 5m vote this tick — unknown is not a green light
        # Real vocabulary: ACCELERATING / DECELERATING / FLAT.
        #   standalone -> must be ACCELERATING (self-sourced, so demand thrust)
        #   handoff    -> ACCELERATING or FLAT (the runaway ORB already proved
        #                 directional force; we only need "not decelerating
        #                 against us"). FLAT is what the old code meant by the
        #                 phantom value "STEADY".
        if is_handoff:
            if momentum not in ("ACCELERATING", "FLAT"):
                return None
        elif momentum != "ACCELERATING":
            return None

        # direction agreement between regime and trend engine (cheap sanity)
        tdir = (getattr(trend, "overall_direction", "") or "").upper()
        if direction == "long"  and tdir not in ("BULLISH", "BULL", "UP"):
            return None
        if direction == "short" and tdir not in ("BEARISH", "BEAR", "DOWN"):
            return None

        # ── 4. Build the signal (debit directional) ────────────────────────
        # Stop reference: just past the pullback extreme (approximated as the
        # midline minus/plus a small ATR buffer). Governing exits are regime-flip
        # + the 40% premium floor; this underlying_stop is structural context.
        if direction == "long":
            underlying_stop = mid - 0.5 * atr
        else:
            underlying_stop = mid + 0.5 * atr

        signal = OptionsSignal(
            strategy_name    = self.name(),
            setup_type       = "trend_continuation" + ("_handoff" if is_handoff else "_standalone"),
            direction        = direction,
            option_side      = option_side,
            underlying_entry = current_price,
            underlying_stop  = underlying_stop,
            regime           = rgm if isinstance(rgm, str) else str(rgm),
            stop_loss_pct    = CONTINUATION_STOP_LOSS_PCT,
            tp_pct           = CONTINUATION_TP_PCT,
        )

        # conviction: inherit regime conviction (trending is the whole thesis),
        # small bump for a clean midline tag + momentum re-assertion.
        signal.conviction = regime.conviction
        self._add_confluence(signal, f"Trending regime ({signal.regime}) conv={regime.conviction:.2f}")
        self._add_confluence(signal, f"Pullback to BB midline ({mid:.2f}), price {current_price:.2f}")
        self._add_confluence(signal, f"Momentum {momentum} (resumption)")
        if is_handoff:
            self._add_confluence(signal, "ORB-runaway handoff (directional force pre-proven)")

        logger.info(
            f"[continuation] {direction} {option_side} @ {current_price:.2f} "
            f"midline={mid:.2f} atr={atr:.2f} mom={momentum} "
            f"conv={regime.conviction:.2f} {'HANDOFF' if is_handoff else 'STANDALONE'}"
        )
        return signal
