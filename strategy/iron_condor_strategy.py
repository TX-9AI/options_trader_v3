"""
v-pfanchor — 2026-08-13 — PF.5: THE PITCHFORK BECOMES THE CONDOR'S ANCHOR, and
  this is the overlay's FIRST CONSUMER. It has been live as a weight-0 observer
  since 2026-08-12 with one call site and nothing reading the rails back.
  OPERATOR'S SPEC, verbatim where it matters:
    · "It's a guardrail, not the road."  -> DAILY fork only.
    · "consider the condor off the table if we don't have guardrails. That is
       the insurance policy that eliminates a bad decision in an unpredictable
       session."                          -> NO FORK, NO PLAN.
    · "The tine should be the trigger for 'rich premium' and the short strike
       should be just outside the range of the rail at the MOST LIQUID strike
       WHERE PRICE HAS STILL NOT EXCEEDED."
    · leg order from the apparent slope: an UP-sloping fork fills the PUT side
       first (price travels lower rail -> upper rail over the session), a
       DOWN-sloping fork fills the CALL side first. Mirrored, and it falls out
       of the geometry rather than being asserted.
  THREE THINGS THIS CHANGES AND ONE IT DOES NOT:
   (1) ANCHOR — short call rides the UPPER rail, short put the LOWER rail,
       replacing the BB half of the dual floor. `0.80 * EM` SURVIVES AS A
       MINIMUM DISTANCE: a rail sitting on top of spot must not produce a strike
       with no breathing room, which is the exact failure v-dualfloor was
       written to fix after ~3 weeks of bleed.
   (2) NOT-EXCEEDED — a strike price has ALREADY TRADED THROUGH today is a
       strike the market has proven it can reach. New constraint; nothing in the
       codebase tested a short strike against the session's own extremes before.
   (3) LIQUIDITY NOW KEYS ON BID/ASK WIDTH. The old `liq()` summed
       `open_interest + volume`, and factor_sweep found BOTH CONSTANT across the
       whole joined sample — so `max_liq` was 0, the `else: top = eligible`
       branch took every call, and "most liquid" has silently resolved to
       "nearest the floor" since v-dualfloor shipped. The comment even
       anticipated it ("no OI/vol data"), which is why it degraded quietly
       instead of failing. Width is populated and is also the measure that
       matters on a 0DTE credit spread, where a nickel-wide quote is what trips
       a stop on noise. OI/volume are kept ONLY as a tie-break, and only when
       genuinely non-zero.
   (4) UNCHANGED: the RANGING gate, the leg-2 pause, the ratchet, the nickel
       close, the 11:11 window. This is strike SELECTION and leg ORDER, not a
       new trade.
  ⚠️ ACCEPTED RISK, operator's words: "If it gets breached, then our fork may
     also become invalid & I can live with that because we are accepting that
     risk for an asymmetric payoff if it holds." So a breach and a fork
     invalidation are THE SAME EVENT — the structure and the overlay agree on
     when the thesis died instead of arguing about it.
v-audibleabandon — 2026-08-05 — `_journal_abandon`'s handler logs inside its
  except body. Flagged by the swallow census as a new TIER-1 silent handler the
  morning after it shipped. The swallow itself is correct and unchanged — a
  journal failure must never reach the trading loop — but a bare `pass` makes
  "deliberate" and "accidental" indistinguishable to the audit, which is the
  whole point of the audit.
v-approachalways — 2026-08-04 — APPROACH TELEMETRY ON EVERY PLAN DEATH.
  The numbers already existed and were UNREACHABLE. `max_price_seen` /
  `min_price_seen` are tracked from a plan's first tick and
  `_abandon_past_cutoff` reported them — but only on the CUTOFF path.
  Measured fleet-wide 2026-08-04: 23 plans, 23 deaths, **cutoff fired ZERO
  times**; every plan died on CANCELLED-before-Leg-1, which reported nothing
  but the regime it flipped to. The one instrument that answers "how close did
  price get?" sat behind the one door that never opens.
  WHAT IT UNBLOCKS — item AI, and the two answers need OPPOSITE fixes:
  an approach fraction near ZERO means the trigger sits where price never goes
  on this tape (the MIDPOINT is wrong — pitchfork/VWAP anchor work); near 0.6
  means it is merely a little too far (CONDOR_TRIGGER_APPROACH is a parameter
  to fit). A plan that reports only its cause of death cannot tell them apart.
  Both death paths now log the same line and emit a `condor_abandon` journal
  row, so the fleet answer is a JOIN rather than a night of greps.
  WHY THE LIFETIME DATA MATTERS FOR READING IT: the same session showed plan
  lifetimes of 1-94 minutes, median ~30, several running 88-94. These plans
  were ALIVE across most of the window — so a low approach is not "no time",
  it is "price never went there".
v-declineloud — 2026-07-31 — AC: the "no liquid strike beyond dual floor" path
  was a SILENT return. On 2026-07-30 `grep -c "no liquid strike"` returned 0
  across all history and was read as "the dual floor never rejects" — it
  actually meant "the dual floor rejects in silence". Now logs the floor level,
  how many contracts were priced, and the nearest priced strike.
v-holdcompression + v-selfdiag — 2026-07-30 — TWO CHANGES, both about a plan
  that dies without saying anything.
  (1) HOLD ON COMPRESSION. Any non-RANGING tick used to cancel an un-filled
      plan; CVX lost three in one session to COMPRESSION alone, each after ~19
      minutes, so none reached the entry cutoff. Compression is a TIGHTENING
      range — where a neutral short-premium structure most belongs — so it is
      now a HOLD, as are SWEEP_REVERSAL and UNKNOWN. Only TRENDING_*/BREAKOUT
      cancel. Mirrors Leg 2's pause-and-hold since v3.2.
  (2) SELF-DIAGNOSING ABANDONMENT. The cutoff line now reports how far price
      travelled toward each trigger, the high-water marks, and EM at plan vs at
      abandonment — because holding through compression means waiting to sell
      into CONTRACTING premium, and strikes are validated against EM once and
      never re-checked. Makes the anchor question (VWAP? pitchfork median?)
      answerable with a number instead of an argument.
  ORDERING: the cutoff check sits ABOVE the regime block on purpose — the first
  cut had HOLD first, which meant a held plan returned early every tick and never
  reached the cutoff at all. Caught by test, not by reasoning.
v-dualfloor + v-indep-legs — 2026-07-28 — TWO FIXES to strike selection and legging.
  (1) STRIKE FLOOR: short strike must clear BOTH 0.80*expected_move from spot
      AND the BB band (whichever is farther). The old code anchored to the BB
      band, had a fallback that placed strikes INSIDE the band when nothing
      liquid sat outside, and only rejected strikes that were too FAR — there
      was NO minimum-distance floor. It sold calls/puts on top of spot with no
      room to breathe (~3 weeks of bleed). Verified against the 2026-07-28
      entries: all six sold at 6-28% of EM; the 0.80 floor rejects every one.
      `_select_beyond_floor` keeps the liquidity-based selection but biases
      OUTWARD and has NO inside fallback — no liquid strike beyond the floor
      means the leg is SKIPPED, never sold close.
  (2) INDEPENDENT LEGS: the call and put sides are independent credit spreads
      sharing a plan. Both triggers are checked EVERY tick; whichever side's
      conditions are met fires, regardless of order. Previously leg 2 was
      state-gated behind leg 1, so if price only ever visited leg 2's side that
      leg never fired at all. call_filled/put_filled tracked separately;
      COMPLETE only when both are in. leg1/leg2 now mean only first/second to
      fill (preserved for the entry_engine interface and the roll path).
strategy/iron_condor_strategy.py — Legged Iron Condor for RANGING regime.
v3.2 — 2026-07-23 — LEG 2 PAUSES INSTEAD OF CANCELLING on a non-RANGING tick,
        and its short strike is RE-DERIVED from the CURRENT bands at fire time
        rather than the value frozen at plan time. Rationale: if price wanders
        for 40 minutes the plan-time strike is stale, so the second side would
        not actually be premium-rich when it fires. The strike should be a
        consequence of where the band is NOW.
v3.1 — 2026-07-12 — FIX missing import (latent since v1.0, 2026-06-30):
        OptionContract/OptionsChain were referenced in CondorPlan's dataclass
        annotations and in method signatures but never imported. Python 3.14's
        lazy annotation evaluation (PEP 649) masked it on the fleet; on any
        Python <= 3.13 the module raises NameError at import, which kills
        main.py at startup (verified 3.12 vs 3.14 A/B on the identical tree).
        One import line added, matching the canonical form used by
        base_strategy.py and gex_data.py. No logic change.
v3.0 — 2026-06-30 — initial release (simultaneous entry placeholder)
v1.1 — 2026-06-30 — full redesign: legged entry via price-triggered verticals.
v1.2 — 2026-07-02 — docstring/comment cleanup: strike selection is BB-band
        anchored ONLY (no delta anywhere in the code). Removed stale
        "delta-primary" / "delta as secondary" / "falls back to delta-primary"
        wording that contradicted the implementation and the architecture
        decision. No logic change.
v3.0 — 2026-07-10 — repo-wide v3.0 bump: Yahoo-Finance purge & data stream
        mapping optimization (all market data now flows from the single
        shared TastyTrade candle feed — see data/candle_feed.py). No logic
        change in this file.

Strategy design:
  At decision time, the bot identifies both vertical spread strike locations
  by anchoring the short strikes to the Bollinger Band boundaries (short call
  at/just outside the BB upper band, short put at/just outside the BB lower
  band), with an ATM straddle-based expected-move sanity guardrail. No delta
  targeting is used. No order is placed yet.

  Leg 1 fires when price reaches within CONDOR_PROXIMITY_STRIKES of the
  first side's short strike — whichever side price is moving toward first.
  (e.g. short call at 7545 → leg 1 fires when price hits 7540, 2 strikes away)

  Leg 2 is queued after Leg 1 fills. It fires when price reaches within
  CONDOR_PROXIMITY_STRIKES of the opposite side's short strike.

  Invalidation: if regime flips away from RANGING (to ANY other regime)
  before a leg fires, that pending leg is permanently cancelled. An
  already-filled leg stays open and manages independently — it is NEVER
  cancelled after the order is placed.

  Exit per leg: 25% stop loss OR close at $0.05 (nickel) — whichever
  comes first. No take-profit target, no trail, no BOS. Hold to nickel
  or stop, independently per leg.

  If Leg 2 never fires (price never approached the second side before
  close), Leg 1 remains as a standalone vertical and manages the same way.

State machine:
  IDLE -> DECIDED (both strikes identified, watching for Leg 1 trigger)
       -> LEG1_TRIGGERED (Leg 1 order placed, waiting for fill)
       -> LEG1_FILLED (Leg 1 live, Leg 2 queued, watching for Leg 2 trigger)
       -> LEG2_TRIGGERED (Leg 2 order placed, waiting for fill)
       -> COMPLETE (both legs filled — full iron condor assembled)
  Any state -> CANCELLED (regime flipped before a pending leg fired)
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Tuple
from zoneinfo import ZoneInfo

from strategy.base_strategy import BaseOptionsStrategy, OptionsSignal
from analysis.regime_classifier import RegimeState, Regime
from analysis.volatility_engine import VolatilityState, VolatilityEngine
from data.options_chain import OptionContract, OptionsChain
from data.macro_data import MacroSnapshot
from config import (
    CONDOR_WING_WIDTH_SPX, CONDOR_WING_WIDTH_QQQ,
    CONDOR_EXPECTED_MOVE_GUARDRAIL_MULT,
    CONDOR_EM_FLOOR_FRAC,
    CONDOR_PROXIMITY_STRIKES,
    CONDOR_TRIGGER_APPROACH,
    CONDOR_NICKEL_CLOSE, CONDOR_STOP_LOSS_PCT,
    CONDOR_ENTRY_START_ET, CONDOR_ENTRY_CUTOFF_ET,
    HARD_CLOSE_ET,                                  # v-pfanchor: POP horizon
    CONDOR_PITCHFORK_ANCHOR, CONDOR_REQUIRE_FORK,   # v-pfanchor
    CONDOR_PF_FLAT_SLOPE, CONDOR_MIN_POP, CONDOR_POP_BAR_MIN,
    STRIKE_INCREMENT, INSTRUMENT, VIX_BUTTERFLY_DISABLE
)

logger = logging.getLogger(__name__)
ET = ZoneInfo("US/Eastern")


class CondorState:
    IDLE         = "IDLE"          # No active condor plan
    DECIDED      = "DECIDED"       # Strikes identified, watching for Leg 1 trigger
    LEG1_FILLED  = "LEG1_FILLED"   # Leg 1 live, Leg 2 queued
    COMPLETE     = "COMPLETE"      # Both legs filled
    CANCELLED    = "CANCELLED"     # Regime flipped before a pending leg fired
    EXPIRED      = "EXPIRED"       # Past entry cutoff


@dataclass
class CondorPlan:
    """
    The full condor plan computed at decision time.
    Both verticals are identified upfront; legs fire independently as
    price visits each side's trigger level.
    """
    # Call spread (upper side)
    short_call_strike:  float = 0.0
    long_call_strike:   float = 0.0
    call_trigger_price: float = 0.0   # Price level that fires Leg 1 or Leg 2

    # Put spread (lower side)
    short_put_strike:   float = 0.0
    long_put_strike:    float = 0.0
    put_trigger_price:  float = 0.0

    # Which side is Leg 1 (the one price is more likely to hit first)
    leg1_side:          str   = ""    # "call" or "put"
    leg2_side:          str   = ""

    # Expected move at decision time (for logging/reference)
    expected_move:      float = 0.0
    underlying_at_decision: float = 0.0

    # Actual contracts (populated when legs fill)
    leg1_short: Optional[OptionContract] = None
    leg1_long:  Optional[OptionContract] = None
    leg2_short: Optional[OptionContract] = None
    leg2_long:  Optional[OptionContract] = None

    leg1_credit: float = 0.0
    leg2_credit: float = 0.0

    # v-selfdiag 2026-07-30 — high-water marks while a plan is HELD, so an
    # abandoned plan reports how close price actually came to firing. Before
    # this a plan that never triggered left nothing behind, which is why the
    # condor drought had to be diagnosed by inference.
    max_price_seen: float = 0.0
    min_price_seen: float = 0.0
    state: str = CondorState.IDLE
    decided_at: str = ""
    leg1_filled_at: str = ""
    # v-indep-legs 2026-07-28: the two sides are INDEPENDENT credit spreads that
    # merely share a plan. Each fills on ITS OWN trigger; order is irrelevant.
    # (Was: leg2 was state-gated behind leg1, so if price visited leg2's side
    # first that leg never fired at all.) leg1/leg2 now mean only "first/second
    # to fill", preserved for the entry_engine interface and the roll logic.
    call_filled: bool = False
    put_filled:  bool = False
    pending_side: str = ""    # side of the signal currently out for fill


class IronCondorStrategy(BaseOptionsStrategy):
    """
    Legged iron condor — price-triggered vertical spreads.
    Each leg fires independently when price visits that side's trigger level.
    """

    def __init__(self):
        self._plan: Optional[CondorPlan] = None
        self._last_reset_date: Optional[str] = None

    @property
    def name(self) -> str:
        return "IronCondorStrategy"

    def _reset_if_new_day(self):
        today = datetime.now(ET).strftime("%Y-%m-%d")
        if self._last_reset_date != today:
            self._plan            = None
            self._last_reset_date = today

    @property
    def has_active_plan(self) -> bool:
        return (self._plan is not None and
                self._plan.state in (CondorState.DECIDED, CondorState.LEG1_FILLED))

    @property
    def plan(self) -> Optional[CondorPlan]:
        return self._plan

    def _wing_width(self) -> int:
        if INSTRUMENT == "SPX":
            return CONDOR_WING_WIDTH_SPX // STRIKE_INCREMENT
        return CONDOR_WING_WIDTH_QQQ // STRIKE_INCREMENT

    def _expected_move_from_straddle(self, chain: OptionsChain,
                                      underlying: float) -> float:
        """ATM straddle = ATM call mark + ATM put mark. Most accurate EM basis."""
        try:
            atm_call = min(
                [c for c in chain.calls if c.mark > 0],
                key=lambda c: abs(c.strike - underlying)
            )
            atm_put = min(
                [c for c in chain.puts if c.mark > 0],
                key=lambda c: abs(c.strike - underlying)
            )
            if atm_call.mark > 0 and atm_put.mark > 0:
                return atm_call.mark + atm_put.mark
        except Exception:
            pass
        return 0.0

    def _select_by_band(self, contracts: List[OptionContract],
                         band_level: float, side: str) -> Optional[OptionContract]:
        """
        BB-anchored strike selection — no delta involvement.
        Finds the nearest liquid strike at or outside the BB boundary:
          - Call side: lowest strike that is >= bb_upper
          - Put side:  highest strike that is <= bb_lower
        If no liquid strike exists outside the band (very tight chain),
        returns the nearest liquid strike to the band level as fallback.
        Delta is deliberately not used here — it is relative to current
        price, not the structural range boundary, and would place strikes
        incorrectly depending on where price happens to sit at decision time.
        """
        candidates = [c for c in contracts if c.mark > 0.01]
        if not candidates:
            return None

        if side == "call":
            outside = [c for c in candidates if c.strike >= band_level]
            if outside:
                return min(outside, key=lambda c: c.strike)
            # Fallback: nearest liquid strike to band
            return min(candidates, key=lambda c: abs(c.strike - band_level))
        else:  # put
            outside = [c for c in candidates if c.strike <= band_level]
            if outside:
                return max(outside, key=lambda c: c.strike)
            return min(candidates, key=lambda c: abs(c.strike - band_level))

    @staticmethod
    def _liquidity_rank(c) -> tuple:
        """Rank key for "most liquid". LOWER IS BETTER.

        BID/ASK WIDTH FIRST, because it is the only liquidity signal that is
        actually populated: factor_sweep found `open_interest` and `volume`
        CONSTANT across the entire joined sample, so the old
        `open_interest + volume` sum was 0 for every contract and the selector
        fell through to its "no OI/vol data" branch on every call. Width is also
        what matters on a 0DTE credit spread — a nickel-wide quote is what trips
        a stop on quote noise rather than on price.

        OI/volume survive ONLY as a tie-break and ONLY when non-zero, so this is
        correct whether or not the feed starts populating them later.
        """
        try:
            bid, ask = float(getattr(c, "bid", 0) or 0), float(getattr(c, "ask", 0) or 0)
            mid = (bid + ask) / 2.0
            width = (ask - bid) / mid if (mid > 0 and ask >= bid) else 9.99
        except Exception:                                      # noqa: BLE001
            width = 9.99
        depth = (getattr(c, "open_interest", 0) or 0) + (getattr(c, "volume", 0) or 0)
        return (round(width, 4), -depth)

    @staticmethod
    def _pop(distance: float, sigma_per_bar: float, bars_left: float) -> float:
        """P(terminal close on the SAFE side of the short strike).

            z   = distance / (sigma * sqrt(bars_left))
            POP = Phi(z)

        TIME IS THE WHOLE POINT. The same distance is a LARGER z late in the
        session, so a strike that fails at 11:15 passes at 14:30 on identical
        geometry. Every offset table built so far pooled hours and could not
        express that.

        Driftless and normal — deliberately. A drift term would be a forecast,
        and the one thing measured all day is that this system's directional
        forecasts do not separate. Normal understates fat tails, so this reads
        slightly OPTIMISTIC on the extremes; the floor sits at 0.70 rather than
        0.50 partly to absorb that.

        Degenerate inputs return 0.0, which FAILS the floor. A missing ATR must
        not read as a safe trade.
        """
        try:
            import math
            d, sig, n = float(distance), float(sigma_per_bar), float(bars_left)
            if d <= 0 or sig <= 0 or n <= 0:
                return 0.0
            z = d / (sig * math.sqrt(n))
            return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        except Exception:                                      # noqa: BLE001
            return 0.0

    @staticmethod
    def _bars_left(now_et_dt, bar_minutes: float) -> float:
        """Bars of `bar_minutes` remaining until the 15:45 flatten.

        15:45, not 16:00: a condor leg is closed at the hard close, so that is
        when the position actually ends. Using the bell would overstate T and
        make every POP look worse than the trade really is.
        """
        try:
            end = now_et_dt.replace(hour=HARD_CLOSE_ET[0], minute=HARD_CLOSE_ET[1],
                                    second=0, microsecond=0)
            mins = (end - now_et_dt).total_seconds() / 60.0
            return max(0.0, mins / max(1e-9, float(bar_minutes)))
        except Exception:                                      # noqa: BLE001
            return 0.0

    @staticmethod
    def _quote_ok(c, max_width_pct: float) -> bool:
        """Reject a short leg quoted wider than `max_width_pct` of its mid.

        RANKING ALONE NEVER REFUSES — it returns the least-bad strike even when
        every candidate is broken. On a 0DTE credit spread a nickel of quote
        noise on a wide market moves the spread enough to trip the 25% stop on
        the QUOTE rather than on price, which is the failure the ratchet and the
        floor cannot survive. So width needs a FLOOR as well as an ordering.
        """
        try:
            if max_width_pct <= 0:
                return True
            bid, ask = float(getattr(c, "bid", 0) or 0), float(getattr(c, "ask", 0) or 0)
            mid = (bid + ask) / 2.0
            if mid <= 0 or ask < bid:
                return False
            return (ask - bid) / mid <= max_width_pct
        except Exception:                                      # noqa: BLE001
            return False

    def _select_beyond_rail(self, contracts: List[OptionContract], side: str,
                            rail: float, min_distance_level: float,
                            session_extreme: Optional[float],
                            spot: float = 0.0, sigma: float = 0.0,
                            bars_left: float = 0.0, min_pop: float = 0.0,
                            max_width_pct: float = 0.0
                            ) -> Optional[OptionContract]:
        """PF.5 — the operator's rule, in the order he stated it.

        A strike qualifies only if it is ALL THREE of:
          1. BEYOND THE RAIL          — "just outside the range of the rail"
          2. BEYOND THE MIN DISTANCE  — the surviving `0.80 * EM` floor, so a
             rail sitting on top of spot cannot produce a strike with no room
          3. NOT EXCEEDED BY PRICE    — beyond the session high (calls) or low
             (puts). A level price has already traded through today is a level
             the market has PROVEN it can reach; selling there is selling a
             strike that has been touched and is being offered as untouched.
        Among survivors: MOST LIQUID by bid/ask width, tie-break to the strike
        NEAREST the rail — richest premium that still clears everything.

        Returns None rather than falling back inward. No inside fallback, ever:
        that fallback is what sold calls on top of spot for ~3 weeks.
        """
        def beyond(k, level):
            return k >= level if side == "call" else k <= level

        eligible = []
        for c in contracts:
            if not (getattr(c, "mark", 0) or 0) > 0.01:
                continue
            k = c.strike
            if not beyond(k, rail):
                continue
            if not beyond(k, min_distance_level):
                continue
            if session_extreme is not None and not beyond(k, session_extreme):
                continue
            if not self._quote_ok(c, max_width_pct):
                continue
            if min_pop > 0 and spot > 0:
                if self._pop(abs(k - spot), sigma, bars_left) < min_pop:
                    continue
            eligible.append(c)

        if not eligible:
            _priced = [c for c in contracts if (getattr(c, "mark", 0) or 0) > 0.01]
            logger.info(
                "Condor: no %s strike clears rail %.2f / min-dist %.2f / "
                "session-extreme %s — %d/%d priced. SKIP (no inside fallback).",
                side, rail, min_distance_level,
                f"{session_extreme:.2f}" if session_extreme is not None else "n/a",
                len(_priced), len(contracts))
            return None

        best_rank = min(self._liquidity_rank(c) for c in eligible)
        cohort = [c for c in eligible
                  if self._liquidity_rank(c)[0] <= best_rank[0] * 1.5 + 1e-9]
        return (min(cohort, key=lambda c: c.strike) if side == "call"
                else max(cohort, key=lambda c: c.strike))

    @staticmethod
    def _leg_order_from_slope(slope: float, flat_eps: float):
        """Leg order from the fork's apparent slope. Returns (leg1, leg2) or
        None when the fork is FLAT and the caller should fall back to proximity.

        UP-sloping channel: price travels the LOWER rail toward the UPPER one
        across the session, so the PUT side is the one price is leaving and it
        fills FIRST; the call side fills later as price approaches the top.
        DOWN-sloping: mirrored. A SIGN IS NOT A SLOPE — below `flat_eps` the
        drift is noise and ordering off it would be reading a coin flip as
        structure, so the caller keeps its existing proximity rule.
        """
        if slope is None or abs(slope) < flat_eps:
            return None
        return ("put", "call") if slope > 0 else ("call", "put")

    def _select_beyond_floor(self, contracts: List[OptionContract],
                             floor_level: float, side: str) -> Optional[OptionContract]:
        """
        v-dualfloor 2026-07-28: select the MOST LIQUID strike that sits BEYOND
        the floor (call: strike >= floor; put: strike <= floor). Preserves the
        elegant liquidity-based selection the operator wanted to keep — but
        (1) biases OUTWARD (only strikes beyond the floor are eligible) and
        (2) has NO inside fallback: if nothing liquid exists beyond the floor,
        return None so the leg is SKIPPED rather than sold with no room. This is
        the reversal of the old bug (nearest-to-band fallback placed strikes
        INSIDE the range, on top of spot, with no breathing room — ~3 weeks of
        bleed). Liquidity = mark (proxy); ties break to the strike CLOSEST to the
        floor among the eligible outside strikes (richest premium still beyond
        the floor), not deepest OTM.
        """
        eligible = [c for c in contracts
                    if c.mark > 0.01 and
                    (c.strike >= floor_level if side == "call" else c.strike <= floor_level)]
        if not eligible:
            # AC 2026-07-31 — was a SILENT return. The floor is the 0.80*EM /
            # BB dual floor; when nothing clears it the condor dies with no
            # reason given. `grep -c "no liquid strike"` returned 0 across the
            # whole log history on 2026-07-30 — which was read as "the floor
            # never rejects" when it actually meant "the floor rejects in
            # silence". That cost a round of wrong conclusions.
            _priced = [c for c in contracts if c.mark > 0.01]
            _near = (min((c.strike for c in _priced),
                         key=lambda k: abs(k - floor_level)) if _priced else None)
            logger.info(
                f"Condor: no liquid {side} strike beyond dual floor "
                f"{floor_level:.2f} — {len(_priced)}/{len(contracts)} priced, "
                f"nearest priced strike {_near if _near is not None else 'n/a'}. "
                f"SKIP"
            )
            return None
        # most liquid; tie-break to the one nearest the floor (richest still-safe).
        def liq(c):
            return (getattr(c, "open_interest", 0) or 0) + (getattr(c, "volume", 0) or 0)
        max_liq = max(liq(c) for c in eligible)
        if max_liq > 0:
            top = [c for c in eligible if liq(c) >= max_liq * 0.5]  # liquid cohort
        else:
            top = eligible                                          # no OI/vol data: all eligible
        # among the liquid cohort, take the strike nearest the floor (richest premium
        # that still clears the floor — closest to spent-move edge without going inside)
        if side == "call":
            return min(top, key=lambda c: c.strike)
        return max(top, key=lambda c: c.strike)

    def _find_contract_at_strike(self, contracts: List[OptionContract],
                                  target_strike: float) -> Optional[OptionContract]:
        """Find contract at exact strike, or nearest with a valid mark."""
        exact = [c for c in contracts if c.strike == target_strike and c.mark > 0]
        if exact:
            return exact[0]
        liquid = [c for c in contracts if c.mark > 0]
        if not liquid:
            return None
        return min(liquid, key=lambda c: abs(c.strike - target_strike))

    def decide(self, regime: RegimeState, vol_state: VolatilityState,
               chain: OptionsChain, macro: MacroSnapshot,
               current_price: float) -> Optional[CondorPlan]:
        """
        Evaluate whether to plan an iron condor. If conditions are met,
        identify both vertical spreads and set up the plan. No orders placed.
        Returns the plan if one was created, None otherwise.
        """
        self._reset_if_new_day()

        now_et = datetime.now(ET)
        hm     = (now_et.hour, now_et.minute)

        if hm < CONDOR_ENTRY_START_ET or hm >= CONDOR_ENTRY_CUTOFF_ET:
            return None

        if self._plan is not None:
            return None  # Already have an active plan this session

        if regime.primary_regime != Regime.RANGING:
            return None

        if macro.vix >= VIX_BUTTERFLY_DISABLE:
            logger.info(f"Condor blocked: VIX={macro.vix:.1f} above threshold")
            return None

        # Compute expected move
        em = self._expected_move_from_straddle(chain, current_price)
        if em <= 0:
            logger.debug("Condor: could not compute expected move")
            return None

        # ── DUAL-FLOOR STRIKE SELECTION (v-dualfloor 2026-07-28) ─────────────
        # RULES (operator, reversing the old broken logic that sold spreads with
        # NO breathing room — bled P&L for ~3 weeks):
        #   1. the short strike must be OUTSIDE the expected move (>= spot ± em)
        #   2. AND outside the widest Bollinger point (>= bb_upper / <= bb_lower)
        # The floor is the FARTHER of the two — a short strike must clear BOTH.
        # The OLD code anchored to the BB band then only rejected strikes that
        # were too FAR; it had NO minimum-distance floor and a fallback that
        # placed strikes INSIDE the band when nothing liquid sat outside it — so
        # it sold calls/puts right on top of spot, inside the range, with no room
        # to breathe. That fallback is REMOVED: if no liquid strike exists beyond
        # the floor, the leg is SKIPPED (return None), never placed inside.
        bb_upper = vol_state.bb_upper if vol_state.bb_upper > 0 else current_price + em
        bb_lower = vol_state.bb_lower if vol_state.bb_lower > 0 else current_price - em

        # the dual floor: farther of (80%-of-expected-move edge, BB band).
        # 80% EM is the operator's "premium is rich here" line — the short strike
        # must sit at least 0.80*EM from spot (so ~80% of the move is already
        # priced past it) AND beyond the BB band. Whichever is farther wins.
        em_floor = em * CONDOR_EM_FLOOR_FRAC
        call_floor = max(current_price + em_floor, bb_upper)
        put_floor  = min(current_price - em_floor, bb_lower)

        short_call = self._select_beyond_floor(chain.calls, call_floor, "call")
        short_put  = self._select_beyond_floor(chain.puts,  put_floor,  "put")

        if short_call is None or short_put is None:
            logger.info(
                f"Condor: no liquid strike beyond dual floor "
                f"(call>={call_floor:.2f}, put<={put_floor:.2f}) — SKIP, "
                f"will not sell inside the expected move / BB band")
            return None

        call_dist = short_call.strike - current_price
        put_dist  = current_price - short_put.strike

        # Upper guardrail unchanged: reject absurdly-far (illiquid-skew) strikes.
        guardrail = em * CONDOR_EXPECTED_MOVE_GUARDRAIL_MULT
        if max(call_dist, put_dist) > guardrail:
            logger.info(
                f"Condor: dual-floor strikes exceed {guardrail:.1f}pt guardrail "
                f"— unusual skew, skip")
            return None

        # Wing widths (fixed, instrument-appropriate)
        wing = self._wing_width()
        long_call_strike = short_call.strike + wing * STRIKE_INCREMENT
        long_put_strike  = short_put.strike  - wing * STRIKE_INCREMENT

        # ── PREMIUM-RICH SEQUENTIAL TRIGGERS ─────────────────────────────────
        # Intent: each short is sold only when price has traveled to THAT side's
        # band, so its premium is rich at the moment of sale — sell the call up
        # near the upper band, sell the put down near the lower band, and mean-
        # reversion carries the structure. The old rule placed the trigger
        # CONDOR_PROXIMITY_STRIKES (2) *inside* each short — measured in
        # strikes*increment. For increment-5 names that is 10pt inside a ~10pt-
        # wide condor, so both triggers overshot PAST the channel centre and
        # crossed: both fire-conditions were true the instant price touched the
        # middle, filling both legs at once with neither premium rich (and
        # starving the risk-free roll of the credit it needs).
        #
        # Now: anchor to the BB midline (the range centre) and require price to
        # travel CONDOR_TRIGGER_APPROACH of the way from the midline to each
        # short before that side fires. Scale-free across strike increments and
        # widths; keeps each trigger up near its own band.
        mid = vol_state.bb_middle if vol_state.bb_middle > 0 else current_price
        call_trigger = mid + CONDOR_TRIGGER_APPROACH * (short_call.strike - mid)
        # Put spread: fires only when price drops most of the way to the lower band
        put_trigger  = mid - CONDOR_TRIGGER_APPROACH * (mid - short_put.strike)

        # Determine which leg is more likely to fill first based on current price
        # — whichever side's trigger is closer to current price is Leg 1
        call_trigger_dist = abs(current_price - call_trigger)
        put_trigger_dist  = abs(current_price - put_trigger)

        if call_trigger_dist <= put_trigger_dist:
            leg1_side = "call"
            leg2_side = "put"
        else:
            leg1_side = "put"
            leg2_side = "call"

        plan = CondorPlan(
            short_call_strike  = short_call.strike,
            long_call_strike   = long_call_strike,
            call_trigger_price = call_trigger,
            short_put_strike   = short_put.strike,
            long_put_strike    = long_put_strike,
            put_trigger_price  = put_trigger,
            leg1_side          = leg1_side,
            leg2_side          = leg2_side,
            expected_move      = em,
            underlying_at_decision = current_price,
            state              = CondorState.DECIDED,
            decided_at         = now_et.strftime("%H:%M ET")
        )

        self._plan = plan

        logger.info(
            f"\U0001F985 CONDOR PLANNED: "
            f"call_spread={short_call.strike:.0f}/{long_call_strike:.0f} "
            f"(trigger@{call_trigger:.0f}) "
            f"put_spread={long_put_strike:.0f}/{short_put.strike:.0f} "
            f"(trigger@{put_trigger:.0f}) "
            f"leg1={leg1_side.upper()} "
            f"EM=${em:.2f} VIX={macro.vix:.1f} "
            f"bb_upper={bb_upper:.2f} bb_lower={bb_lower:.2f}"
        )
        return plan

    # ── v3.9 — APPROACH TELEMETRY ON EVERY DEATH, NOT JUST THE CUTOFF ────────
    # The numbers below already existed, and were unreachable. `max_price_seen`
    # / `min_price_seen` are tracked from a plan's first tick, and
    # _abandon_past_cutoff reported them — but ONLY on the cutoff path. Measured
    # 2026-08-04 fleet-wide: 23 plans, 23 deaths, **cutoff fired ZERO times**.
    # Every plan died on the CANCELLED-before-Leg-1 branch, which reported
    # nothing but the regime it flipped to. The one instrument that could answer
    # "how close did price get?" was behind the one door that never opens.
    # THE QUESTION IT UNBLOCKS is item AI: whether CONDOR_TRIGGER_APPROACH=0.65
    # is a parameter to fit or the MIDPOINT is wrong. Those need opposite fixes,
    # and a plan that reports only its cause of death cannot tell them apart.
    @staticmethod
    def _approach(plan, chain, current_price) -> dict:
        """How far price travelled toward each trigger, as a fraction of the
        distance it needed. 1.0 means the trigger was reached.

        Denominator is trigger-minus-spot-at-plan, NOT the band width: the
        question is how much of the REQUIRED journey happened. A fraction near
        zero says the trigger sits somewhere price never goes on this tape,
        which is a geometry finding; a fraction near 0.6 says the trigger is
        merely a little too far, which is a parameter finding.
        """
        s0 = plan.underlying_at_decision or current_price
        cd = plan.call_trigger_price - s0
        pd = s0 - plan.put_trigger_price
        return {
            "spot_at_plan": round(s0, 2),
            "call_approach": round((plan.max_price_seen - s0) / cd, 4) if cd > 0 else None,
            "put_approach": round((s0 - plan.min_price_seen) / pd, 4) if pd > 0 else None,
            "max_seen": round(plan.max_price_seen, 2),
            "min_seen": round(plan.min_price_seen, 2),
            "call_trigger": round(plan.call_trigger_price, 2),
            "put_trigger": round(plan.put_trigger_price, 2),
            "short_put": plan.short_put_strike,
            "short_call": plan.short_call_strike,
            "em_at_plan": round(plan.expected_move or 0.0, 2),
            "decided_at": plan.decided_at,
        }

    @staticmethod
    def _approach_text(plan, a: dict) -> str:
        def _p(v):
            return "n/a" if v is None else f"{v:.0%}"
        return (f"approach call {_p(a['call_approach'])} (max ${a['max_seen']:.2f} "
                f"vs trig ${a['call_trigger']:.2f}) · put {_p(a['put_approach'])} "
                f"(min ${a['min_seen']:.2f} vs trig ${a['put_trigger']:.2f}) · "
                f"spot@plan ${a['spot_at_plan']:.2f} · strikes "
                f"{a['short_put']:g}/{a['short_call']:g}")

    @staticmethod
    def _journal_abandon(plan, a: dict, cause: str) -> None:
        """One row per dead plan, so the fleet's answer is a JOIN and not a
        night of greps. Lazy import and fully swallowed: a journal failure must
        never reach the trading loop (this module has never imported the
        journal, and it must not start being able to break it)."""
        try:
            from analysis.signal_journal import journal
            journal("condor_abandon", cause=cause, approach=a)
        except Exception as exc:                                   # noqa: BLE001
            # v-audibleabandon — logged INLINE. The 2026-08-05 swallow census
            # flagged this as a new TIER-1 silent handler, and it was right to:
            # I called the bare `pass` deliberate when I wrote it, but the
            # census reads the handler BODY, and "deliberately swallowed" and
            # "accidentally swallowed" are indistinguishable from the outside.
            # The swallow is still correct — a journal failure must never reach
            # the trading loop — it just has to be AUDIBLE. Debug level, because
            # this fires per dead plan and a warning would be spam.
            logger.debug("condor_abandon journal failed (%s: %s)",
                         type(exc).__name__, exc)

    def _abandon_past_cutoff(self, plan, chain, current_price):
        """Close out an un-filled plan at the cutoff — loudly, with numbers.

        Reports how far price travelled toward EACH trigger as a fraction, and
        expected move at plan time vs now. The second matters because a plan
        HELD through a tightening range waits to sell into decayed premium: the
        strikes are validated against EM exactly once, at plan time, and never
        re-checked. A short at 1.0x EM when EM was $5.00 is at 1.25x EM if EM
        decays to $4.00 — which would FAIL the 1.2x guardrail if planned fresh.
        """
        _a = self._approach(plan, chain, current_price)
        logger.info("Condor: past cutoff, Leg 1 never fired — abandoned | %s",
                    self._approach_text(plan, _a))
        self._journal_abandon(plan, _a, "cutoff")
        plan.state = CondorState.CANCELLED
        self._plan = None
        return None

    def check_leg_triggers(self, regime: RegimeState,
                            chain: OptionsChain,
                            current_price: float) -> Optional[OptionsSignal]:
        """
        Called every tick when a condor plan is active.
        Returns an OptionsSignal if a leg should fire now, None otherwise.
        Also cancels pending legs if regime has flipped away from RANGING.
        """
        plan = self._plan
        if plan is None:
            return None

        # v-selfdiag: record the extremes this plan actually saw. Cheap, and it
        # turns an abandoned plan from silence into a measurement.
        if plan.max_price_seen <= 0.0:
            plan.max_price_seen = plan.min_price_seen = current_price
        plan.max_price_seen = max(plan.max_price_seen, current_price)
        plan.min_price_seen = min(plan.min_price_seen, current_price)

        # ORDERING MATTERS: the cutoff is evaluated BEFORE the regime block.
        # If HOLD came first, a plan held through COMPRESSION would return early
        # every tick and NEVER reach the cutoff — sitting alive to end of session
        # and producing exactly the silence this change exists to remove.
        _now = datetime.now(ET)
        if (_now.hour, _now.minute) >= CONDOR_ENTRY_CUTOFF_ET \
                and plan.state == CondorState.DECIDED:
            return self._abandon_past_cutoff(plan, chain, current_price)

        # Invalidation: regime flipped to a DIRECTIONAL regime.
        #
        # v-holdcompression 2026-07-30 — CANCELLING ON COMPRESSION WAS BACKWARDS.
        # Any flip off RANGING used to kill an un-filled plan. On 2026-07-30 CVX
        # built three plans and lost all three the same way — PLANNED 15:11 ->
        # CANCELLED 15:30, rebuilt 15:33 -> 15:51, rebuilt 15:53 -> 16:05. Each
        # lived ~19 minutes; none reached the cutoff, which is also why the
        # "Leg 1 never fired" line never appeared and the drought looked like a
        # trigger problem.
        # MECHANISM (operator): compression is a TIGHTENING range — where a
        # short-premium NEUTRAL structure is most comfortable, not least. Only a
        # DIRECTIONAL regime breaks the neutral thesis. Leg 2 has held rather
        # than cancelled since v3.2; Leg 1 never got the same treatment.
        _DIRECTIONAL = (Regime.TRENDING_BULL, Regime.TRENDING_BEAR,
                        Regime.BREAKOUT_VOLATILE)
        if regime.primary_regime != Regime.RANGING:
            if plan.state == CondorState.DECIDED:
                if regime.primary_regime not in _DIRECTIONAL:
                    logger.debug(
                        f"Condor Leg 1 HELD: regime {regime.primary_regime} is "
                        f"non-directional — plan alive, awaiting trigger"
                    )
                    return None
                # v3.9: report the APPROACH here too. This is the branch that
                # actually fires — 23 of 23 deaths on 2026-08-04 — so reporting
                # only the regime made the fleet's real behaviour unmeasurable.
                _a = self._approach(plan, chain, current_price)
                logger.info(
                    "Condor CANCELLED before Leg 1: regime flipped to %s "
                    "(directional) | %s",
                    regime.primary_regime, self._approach_text(plan, _a)
                )
                self._journal_abandon(plan, _a, "regime_flip")
                plan.state = CondorState.CANCELLED
                self._plan = None
                return None
            elif plan.state == CondorState.LEG1_FILLED:
                # v3.2 (2026-07-23): PAUSE, do not cancel. Leg 2 must not FILL
                # into a trending regime, but the plan stays alive — if regime
                # returns to RANGING and price is at the far band, Leg 2 fires.
                # (Previously this set COMPLETE, permanently killing the
                # structure on a single non-RANGING tick.)
                logger.debug(
                    f"Condor Leg 2 PAUSED: regime {regime.primary_regime} "
                    f"!= RANGING — plan held, Leg 1 remains open"
                )
                return None

        now_et = datetime.now(ET)
        hm = (now_et.hour, now_et.minute)
        if hm >= CONDOR_ENTRY_CUTOFF_ET:
            if plan.state == CondorState.DECIDED:
                logger.info("Condor: past cutoff, Leg 1 never fired — abandoned")
                plan.state = CondorState.EXPIRED
                self._plan = None
            elif plan.state == CondorState.LEG1_FILLED:
                logger.info("Condor: past cutoff, Leg 2 never fired — Leg 1 standalone")
                plan.state = CondorState.COMPLETE
            return None

        # ── INDEPENDENT LEGS (v-indep-legs 2026-07-28) ───────────────────────
        # Check BOTH sides every tick. Each side fires on its own trigger, with
        # identical entry logic, regardless of what the other side has done. No
        # ordering: whichever side's conditions are met first fills first. The
        # only coupling is the shared plan (and, later, the roll).
        if plan.state in (CondorState.DECIDED, CondorState.LEG1_FILLED):
            call_hit = (not plan.call_filled) and current_price >= plan.call_trigger_price
            put_hit  = (not plan.put_filled)  and current_price <= plan.put_trigger_price

            # If both trigger on the same tick (rare), take the side price has
            # travelled FURTHER past — its premium is the richer of the two.
            if call_hit and put_hit:
                call_excess = current_price - plan.call_trigger_price
                put_excess  = plan.put_trigger_price - current_price
                side = "call" if call_excess >= put_excess else "put"
            elif call_hit:
                side = "call"
            elif put_hit:
                side = "put"
            else:
                return None

            first_fill = not (plan.call_filled or plan.put_filled)
            plan.pending_side = side
            return self._build_leg_signal(plan, side, chain, is_leg1=first_fill)

        return None

    def notify_leg_filled(self, is_leg1: bool, credit: float,
                          short_contract: OptionContract,
                          long_contract: OptionContract):
        """Call from entry_engine after a condor leg order fills."""
        if self._plan is None:
            return
        plan = self._plan
        # mark the side that actually filled (v-indep-legs)
        side = plan.pending_side or (plan.leg1_side if is_leg1 else plan.leg2_side)
        if side == "call":
            plan.call_filled = True
        elif side == "put":
            plan.put_filled = True
        plan.pending_side = ""
        if is_leg1:
            plan.state         = CondorState.LEG1_FILLED
            plan.leg1_credit   = credit
            plan.leg1_short    = short_contract
            plan.leg1_long     = long_contract
            plan.leg1_filled_at = datetime.now(ET).strftime("%H:%M ET")
            logger.info(
                f"Condor Leg 1 FILLED ({plan.leg1_side.upper()}): "
                f"credit=${credit:.2f} — queuing Leg 2 ({plan.leg2_side.upper()})"
            )
        else:
            # COMPLETE only when BOTH independent sides are filled
            plan.state       = (CondorState.COMPLETE if (plan.call_filled and plan.put_filled)
                                else CondorState.LEG1_FILLED)
            plan.leg2_credit = credit
            plan.leg2_short  = short_contract
            plan.leg2_long   = long_contract
            logger.info(
                f"Condor Leg 2 FILLED ({plan.leg2_side.upper()}): "
                f"credit=${credit:.2f} — full condor assembled "
                f"total_credit=${plan.leg1_credit + credit:.2f}"
            )

    def _build_leg_signal(self, plan: CondorPlan, side: str,
                           chain: OptionsChain,
                           is_leg1: bool) -> Optional[OptionsSignal]:
        """Build an OptionsSignal for a single condor leg (vertical spread)."""
        if side == "call":
            contracts = chain.calls
            short_strike = plan.short_call_strike
            long_strike  = plan.long_call_strike
            leg_label    = "Call Credit Spread"
        else:
            contracts = chain.puts
            short_strike = plan.short_put_strike
            long_strike  = plan.long_put_strike
            leg_label    = "Put Credit Spread"

        short_contract = self._find_contract_at_strike(contracts, short_strike)
        long_contract  = self._find_contract_at_strike(contracts, long_strike)

        if short_contract is None or long_contract is None:
            logger.warning(
                f"Condor Leg {'1' if is_leg1 else '2'}: "
                f"could not find {side} spread contracts "
                f"({short_strike}/{long_strike})"
            )
            return None

        net_credit = short_contract.mark - long_contract.mark
        if net_credit <= 0:
            logger.info(
                f"Condor: {leg_label} credit <= 0 ({net_credit:.2f}) — skip"
            )
            return None

        wing_width = abs(long_strike - short_strike)
        max_loss   = wing_width - net_credit

        leg_num = "1" if is_leg1 else "2"
        signal = OptionsSignal(
            strategy_name     = self.name,
            setup_type        = f"Condor Leg {leg_num}: {leg_label}",
            direction         = "neutral",
            option_side       = side,
            is_iron_condor    = True,
            # Use the short/long contract fields for this leg
            short_call_contract  = short_contract if side == "call" else None,
            long_call_contract   = long_contract  if side == "call" else None,
            short_put_contract   = short_contract if side == "put"  else None,
            long_put_contract    = long_contract  if side == "put"  else None,
            net_credit           = net_credit,
            max_loss_condor      = max_loss,
            underlying_entry     = plan.underlying_at_decision,
            regime               = Regime.RANGING,
            stop_loss_pct        = CONDOR_STOP_LOSS_PCT,
            tp_pct               = 0.0,   # No TP — hold to nickel or stop
            notes                = (
                f"Condor leg {leg_num}/{2} | "
                f"EM=${plan.expected_move:.2f} | "
                f"{'Leg 2 queued after fill' if is_leg1 else 'Full condor on fill'}"
            )
        )

        self._add_confluence(signal, f"RANGING regime — condor leg {leg_num}")
        self._add_confluence(
            signal,
            f"Price reached trigger ({plan.call_trigger_price if side == 'call' else plan.put_trigger_price:.0f}) — "
            f"{int(CONDOR_TRIGGER_APPROACH*100)}% of the way to the {side} band (premium rich)"
        )

        logger.info(
            f"\U0001F985 CONDOR LEG {leg_num} SIGNAL ({side.upper()}): "
            f"sell={short_strike:.0f} buy={long_strike:.0f} "
            f"credit=${net_credit:.2f} max_loss=${max_loss:.2f} "
            f"stop=${net_credit * (1 + CONDOR_STOP_LOSS_PCT):.2f} "
            f"nickel_close=${CONDOR_NICKEL_CLOSE:.2f}"
        )
        return signal

    def reset_plan(self):
        """Clear the active plan (e.g. end of session)."""
        self._plan = None

    # generate_signal required by ABC — routes to decide() for initial call
    def generate_signal(self, *args, **kwargs) -> Optional[OptionsSignal]:
        """
        For the condor, main.py calls decide() and check_leg_triggers()
        separately rather than using generate_signal() directly.
        This stub satisfies the ABC requirement.
        """
        return None
