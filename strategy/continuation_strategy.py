"""
strategy/continuation_strategy.py — Trend-continuation on pullback.
v1.3 — 2026-07-28 — PULLBACK TRIGGER REWIRED: BB-midline -> 1-min wick TAGGING
        the nearest unfilled 5-min FVG (edge-tag, >= 1 cent penetration,
        CONTINUATION_FVG_TAG_MIN). The midline trigger was too conservative — a
        strong trend outruns the midline so it never presented (continuation sat
        out the SPX 2026-07-28 rip for exactly this). FVGs are where price
        actually returns in a trend. Uses the existing structure_analyzer FVG
        primitive (smap.fvgs, already built every tick in main). Removed the
        orphaned CONTINUATION_MIDLINE_ATR / CONTINUATION_MAX_PULLBACK_R. New
        params structure + df_1m threaded from the main dispatch. STRATEGY change
        (not an L1 definition) — freeze-safe, live this week to observe fires.
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

v1.3.1 — 2026-07-29 — HOTFIX. v1.3 deleted the BB-midline block (which defined
        `mid`) but left four references to it: the structural stop
        (`underlying_stop = mid +/- 0.5*atr`), the confluence string, and the log
        line. Result: NameError: name 'mid' is not defined, raised EVERY TICK,
        killing the main loop before any strategy could evaluate. Fleet-wide, 15
        boxes, ZERO trades taken 2026-07-29 open through ~09:55 ET.
        Fix: the stop now anchors to the FVG, which is structurally correct --
        the gap IS the level the entry was taken on. Long tags gap.top from
        above, so a close through gap.bottom means the pullback became a
        breakdown -> stop = gap.bottom - 0.5*atr. Short mirrors on gap.top.
        Confluence and log lines now report the gap range instead of a midline
        that no longer exists.
        LESSON: v1.3 compiled and its FVG-tag geometry was unit-tested, but the
        full generate_signal path was never executed -- the tastytrade SDK is not
        installable in the sandbox, so only the extracted block was exercised. A
        compile check does not catch an unbound name on a branch that never ran.
        The canary must import and CALL the strategy on a box before deploy.
"""
# v-runaway-fix (2026-07-24) — accepts runaway handoff_direction so it can enter on a flipped-off-trending label; conviction floor steps aside when the runaway (not the label) is the directional evidence.


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
# v-fvg-pullback (2026-07-28): pullback trigger is now a 1-min wick TAGGING the
# nearest unfilled 5-min FVG (edge-tag, >= 1 cent penetration). The old BB-midline
# trigger (CONTINUATION_MIDLINE_ATR / _MAX_PULLBACK_R) was removed — too
# conservative, a strong trend outruns the midline so it never presented.
CONTINUATION_FVG_TAG_MIN     = 0.01   # cents the 1m wick must penetrate the FVG edge to "tag" it
# v1.2 (2026-07-22): sourced from config (env OT_CONT_STOP_PCT), tightened
# 0.40 -> 0.25. Regime-flip remains the PRIMARY exit; this is the backstop.
from config import CONTINUATION_STOP_LOSS_PCT   # 0.25 default
CONTINUATION_TP_PCT          = 1.0    # nominal; runner is exhaustion-trailed, not TP-capped
CONTINUATION_HANDOFF_CONV_RELAX = 0.10  # handoff path lowers the conviction floor by this


class ContinuationStrategy(BaseOptionsStrategy):
    """Trend-continuation entry on a pullback: 1-min wick tagging a 5-min FVG."""

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
                        handoff_direction: str = "",
                        structure=None,
                        df_1m=None,
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
        elif is_handoff and handoff_direction in ("long", "short"):
            # v-runaway-fix: a runaway ORB proved directional force even if the
            # regime LABEL has since flipped (commonly to SWEEP_REVERSAL/BREAKOUT).
            # Trust the runaway's direction for the handoff entry. Non-handoff
            # (standalone) continuation still requires a trending label.
            direction   = handoff_direction
            option_side = "call" if direction == "long" else "put"
        else:
            return None  # not trending and no runaway handoff → trade does not exist

        conv_floor = CONTINUATION_CONV_FLOOR
        if is_handoff:
            conv_floor -= CONTINUATION_HANDOFF_CONV_RELAX  # runaway vouched for direction
        # v-runaway-fix: when the handoff is driving direction because the label
        # FLIPPED off trending (rgm not TRENDING_*), regime.conviction is the
        # conviction of the NEW label (e.g. sweep), not the trend — applying it
        # would wrongly kill the handoff. The runaway IS the directional evidence;
        # skip the floor in that specific case. A still-trending handoff keeps it.
        _label_trending = rgm in (Regime.TRENDING_BULL, Regime.TRENDING_BEAR)
        if _label_trending and regime.conviction < conv_floor:
            return None

        # ── 2. PULLBACK = 1-min WICK TAGS the nearest unfilled 5-min FVG ───────
        # v-fvg-pullback 2026-07-28: the BB-midline trigger was too conservative
        # — a strong trend outruns the midline and it NEVER presents (continuation
        # sat out the SPX 2026-07-28 rip for exactly this). FVGs are where price
        # ACTUALLY returns in a trend (the imbalance fills), so the pullback is a
        # 1-min wick TAGGING (>= 1 cent into) the nearest unfilled 5-min FVG in
        # the trend direction. Edge-tag is preferred: price often reverses at the
        # proximal edge without filling deep. Midline logic REMOVED entirely.
        atr = getattr(vol_state, "atr_current", 0.0)
        if atr <= 0 or df_1m is None or structure is None:
            return None

        fvgs = [g for g in getattr(structure, "fvgs", []) if not getattr(g, "filled", False)]
        # direction filter: a long pulls back DOWN into a bullish gap below price;
        # a short pulls back UP into a bearish gap above price.
        want = "bullish" if direction == "long" else "bearish"
        cands = []
        for g in fvgs:
            if getattr(g, "direction", "") != want:
                continue
            if direction == "long"  and g.top < current_price:   # gap sits below
                cands.append(g)
            elif direction == "short" and g.bottom > current_price:  # gap sits above
                cands.append(g)
        if not cands:
            return None
        # nearest unfilled gap in favor: for a long, the highest such gap top;
        # for a short, the lowest such gap bottom (the one price is closest to).
        gap = (max(cands, key=lambda g: g.top) if direction == "long"
               else min(cands, key=lambda g: g.bottom))

        # TAG test: the most recent 1-min candle must penetrate the gap's proximal
        # edge by >= TAG_MIN_PENETRATION (1 cent). Long: 1m low pokes at/under the
        # gap TOP. Short: 1m high pokes at/over the gap BOTTOM.
        try:
            last_low  = float(df_1m["low"].iloc[-1])
            last_high = float(df_1m["high"].iloc[-1])
        except Exception:
            return None
        if direction == "long":
            tagged = last_low <= (gap.top - CONTINUATION_FVG_TAG_MIN)
        else:
            tagged = last_high >= (gap.bottom + CONTINUATION_FVG_TAG_MIN)
        if not tagged:
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
            # v-fvg-pullback fix: anchor the stop to the FVG, not the deleted
            # midline. Long entered by tagging gap.top from above; if price closes
            # THROUGH the gap (below gap.bottom) the pullback became a breakdown.
            underlying_stop = gap.bottom - 0.5 * atr
        else:
            # short entered by tagging gap.bottom from below; through gap.top = dead
            underlying_stop = gap.top + 0.5 * atr

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
        signal.adx_at_signal = regime.adx
        signal.flat_angle_deg = getattr(regime, 'flat_angle_deg', 0.0) or 0.0
        self._add_confluence(signal, f"Trending regime ({signal.regime}) conv={regime.conviction:.2f}")
        self._add_confluence(signal, f"1m wick tagged 5m FVG {gap.bottom:.2f}-{gap.top:.2f}, price {current_price:.2f}")
        self._add_confluence(signal, f"Momentum {momentum} (resumption)")
        if is_handoff:
            self._add_confluence(signal, "ORB-runaway handoff (directional force pre-proven)")

        logger.info(
            f"[continuation] {direction} {option_side} @ {current_price:.2f} "
            f"fvg={gap.bottom:.2f}-{gap.top:.2f} atr={atr:.2f} mom={momentum} "
            f"conv={regime.conviction:.2f} {'HANDOFF' if is_handoff else 'STANDALONE'}"
        )
        return signal
