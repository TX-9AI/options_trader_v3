"""
strategy/trend_credit_spread.py — options_trader_v3 — v1.0 — 2026-08-13  (TC.6)

TREND PARTICIPATION BY SELLING PREMIUM BENEATH THE MOVE.

Operator's design, assembled over 2026-08-13:
  · *"The afternoon trend participation is going to be a vertical spread at the
     floor of the Move. We don't have to catch the very beginning. We just have
     to catch it near the beginning."*
  · *"set the put spread at the top of the orb range for a runaway long and the
     bottom of the orb range for the call spread on a runaway short."*
  · *"that's when we don't wanna be long premium."*
  · Exit: *breached (loss) or nickel close (profit)*. No per-session limit.
    Trend label NOT required at fire time.

WHY THE ORB BOUNDARY IS THE ANCHOR — and it is a structural claim, not a fit.
A runaway broke the opening range and never came back to retest it, so the
broken boundary IS the floor of that move and the level `orb_structure_stop`
already calls thesis death. A put spread short there loses only if the setup
was wrong. Structure and invalidation become the SAME event, which is exactly
the accepted risk the operator stated: *"If it gets breached, then our fork may
also become invalid & I can live with that because we are accepting that risk
for an asymmetric payoff if it holds."*

────────────────────────────────────────────────────────────────────────────
WHAT WAS MEASURED, AND THE ONE CONDITION THE EV DEPENDS ON
────────────────────────────────────────────────────────────────────────────
`spread_counterfactual --anchor orb`, runaway-handoff arm, 18 sessions:
  EV/spread POSITIVE AT EVERY OFFSET; the 0.00%% cell — the strike AT the
  boundary, the operator's literal proposal — was **n=30, +$0.52, 90%% terminal
  OK, 79%% RECOVERED**. Entry sat p50 **+0.91%%** above the boundary.
The STANDALONE control was mostly NEGATIVE on the same anchor, because without
a runaway the boundary sits at or above the fill 64%% of the time and the
"structural strike" lands inside the money. **So the edge is runaway-specific by
construction** — which is why `orb.invalidation_reason == "runaway"` is a HARD
gate here and not a preference.

⚠️ **THE EV WAS MEASURED HELD TO EXPIRY, UNMANAGED** — no stop, no ratchet, no
   early close. A premium stop bolted on afterwards is NOT the trade that was
   measured. Hence breach-or-nickel only, per the operator's spec, and hence
   `is_trend_credit` on the signal so `exit_engine` can tell this apart from a
   condor leg rather than inheriting the condor's 25%% stop by accident.

────────────────────────────────────────────────────────────────────────────
TIMING IS THE POP GATE, NOT A CLOCK
────────────────────────────────────────────────────────────────────────────
Proximity cannot be the trigger: in a runaway price moves AWAY from the
boundary, so waiting for it to come back is waiting for the thesis to fail. The
runaway confirmation is the event. What decides WHEN it can fire is
`POP = Phi(distance / (sigma * sqrt(bars_left)))` — the same distance is a
larger z later in the session, so an identical setup fails in the morning and
passes in the afternoon. That is the operator's afternoon-credit thesis arriving
from the arithmetic instead of from a hardcoded hour.

STRIKE SELECTION HAS ONE OWNER. `IronCondorStrategy._select_beyond_rail` already
implements rail -> min-distance -> not-exceeded -> quote-width -> POP -> most
liquid. It is imported, not reimplemented: a second copy of that logic is the
lineage split WORKING_AGREEMENT 7 forbids, and it would drift the first time
either side is tuned.
"""

import logging
from datetime import datetime
from typing import Optional

import pytz

from config import (
    CONDOR_MIN_POP, CONDOR_POP_BAR_MIN, CONDOR_MAX_QUOTE_WIDTH,
    CONDOR_EM_FLOOR_FRAC, GLOBAL_NO_ENTRY_ET, INSTRUMENT,
    CONDOR_WING_WIDTH_SPX, CONDOR_WING_WIDTH_QQQ,
)
from strategy.iron_condor_strategy import IronCondorStrategy

logger = logging.getLogger(__name__)
ET = pytz.timezone("US/Eastern")


class TrendCreditSpread:
    """Sell a defined-risk vertical beyond the broken ORB boundary."""

    name = "TrendCreditSpread"

    def __init__(self):
        # Borrow the condor's selector rather than clone it — ONE owner.
        self._sel = IronCondorStrategy.__new__(IronCondorStrategy)

    @staticmethod
    def _wing_width() -> float:
        return (CONDOR_WING_WIDTH_SPX if INSTRUMENT in ("SPX", "SPXW")
                else CONDOR_WING_WIDTH_QQQ)

    def generate_signal(self, orb, regime, vol_state, chain, macro,
                        current_price: float,
                        session_high: Optional[float] = None,
                        session_low: Optional[float] = None,
                        condor_active: bool = False,
                        now_et: Optional[datetime] = None):
        """Returns a condor-leg-shaped OptionsSignal, or None.

        GATES, in the order they can refuse and each logged:
          1. RUNAWAY REQUIRED — the control arm was negative without one.
          2. NOT past the global entry cutoff.
          3. NO ACTIVE CONDOR on this symbol. The condor is already the only
             strategy allowed two concurrent positions; stacking a third credit
             spread on one underlying is unmanaged risk, and the condor holds
             the slot because it got there first.
          4. A strike clearing rail / min-distance / session-extreme / quote
             width / POP — delegated to the condor's selector.
        """
        try:
            now = now_et or datetime.now(ET)
            if (now.hour, now.minute) >= GLOBAL_NO_ENTRY_ET:
                return None

            if getattr(orb, "invalidation_reason", "") != "runaway":
                return None
            direction = str(getattr(orb, "break_direction", "") or "").lower()
            if direction not in ("long", "short"):
                return None

            if condor_active:
                logger.info("[tcs] deferring — a condor plan holds this symbol; "
                            "stacking a third credit spread is unmanaged risk")
                return None

            orb_high = float(getattr(orb, "orb_high", 0) or 0)
            orb_low = float(getattr(orb, "orb_low", 0) or 0)
            if orb_high <= 0 or orb_low <= 0:
                return None

            # A runaway LONG broke UP, so the boundary below is the ORB HIGH and
            # the credit trade is a PUT spread beneath it. Mirrored for a short.
            if direction == "long":
                side, boundary, extreme = "put", orb_high, session_low
            else:
                side, boundary, extreme = "call", orb_low, session_high

            em = self._sel._expected_move_from_straddle(chain, current_price)
            if em <= 0:
                logger.debug("[tcs] no expected move — cannot set the minimum "
                             "distance floor")
                return None
            em_floor = em * CONDOR_EM_FLOOR_FRAC
            min_dist = (current_price - em_floor if side == "put"
                        else current_price + em_floor)

            sigma = float(getattr(vol_state, "atr_current", 0.0) or 0.0)
            bars = self._sel._bars_left(now, CONDOR_POP_BAR_MIN)

            contracts = chain.puts if side == "put" else chain.calls
            short = self._sel._select_beyond_rail(
                contracts, side, boundary, min_dist, extreme,
                spot=current_price, sigma=sigma, bars_left=bars,
                min_pop=CONDOR_MIN_POP, max_width_pct=CONDOR_MAX_QUOTE_WIDTH)
            if short is None:
                logger.info(
                    "[tcs] no %s strike clears boundary %.2f / min-dist %.2f / "
                    "extreme %s / POP>=%.2f at %.1f bars — SKIP",
                    side, boundary, min_dist,
                    f"{extreme:.2f}" if extreme else "n/a",
                    CONDOR_MIN_POP, bars)
                return None

            width = self._wing_width()
            long_strike = (short.strike - width if side == "put"
                           else short.strike + width)
            long_c = self._sel._find_contract_at_strike(contracts, long_strike)
            if long_c is None or long_c.strike == short.strike:
                logger.info("[tcs] no protective wing at %.2f — SKIP "
                            "(undefined risk is never sold)", long_strike)
                return None

            return self._build_signal(side, short, long_c, direction, boundary,
                                      current_price, regime, bars)
        except Exception as exc:                               # noqa: BLE001
            logger.warning("[tcs] generate_signal failed: %s", exc)
            return None

    def _build_signal(self, side, short, long_c, direction, boundary,
                      current_price, regime, bars):
        """Condor-leg shape, so `_execute_condor_leg` runs it unchanged.

        `is_trend_credit` is the flag `exit_engine` keys on. WITHOUT IT this leg
        inherits the condor's 25%% premium stop and ratchet — and the measured
        EV was HELD TO EXPIRY, UNMANAGED. A stop bolted on afterwards is a
        different trade with a different expectancy.
        """
        from strategy.base_strategy import OptionsSignal
        sig = OptionsSignal(
            strategy_name=self.name,
            setup_type=f"trend_credit_{direction}",
            direction="neutral",              # a credit spread has no side to be on
            option_side=side,
            underlying_entry=current_price,
            # THE INVALIDATION LEVEL, and the exit. A close beyond the broken
            # boundary is thesis death — the same event orb_structure_stop names.
            underlying_stop=boundary,
            regime=str(getattr(regime, "primary_regime", "")),
        )
        sig.is_iron_condor = True             # credit-vertical math, not debit
        sig.is_trend_credit = True            # exit_engine: breach-or-nickel ONLY
        sig.net_credit = max(0.0, (short.bid or 0.0) - (long_c.ask or 0.0))
        if side == "call":
            sig.short_call_contract, sig.long_call_contract = short, long_c
        else:
            sig.short_put_contract, sig.long_put_contract = short, long_c
        sig.contract = short
        sig.conviction = 1.0
        logger.info(
            "[tcs] %s spread: short %.2f / long %.2f, credit %.2f, boundary "
            "%.2f, %.1f bars left — exit is BREACH or NICKEL, no premium stop",
            side, short.strike, long_c.strike, sig.net_credit, boundary, bars)
        return sig
