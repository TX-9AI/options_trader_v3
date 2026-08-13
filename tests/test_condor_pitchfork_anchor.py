#!/usr/bin/env python3
"""
tests/test_condor_pitchfork_anchor.py — v1.0 — 2026-08-13   (PF.5)

The operator's spec is three filters and an ordering rule, and every test here
exists because one of them can fail silently:

  1. beyond the RAIL          — "just outside the range of the rail"
  2. beyond the MIN DISTANCE  — the surviving 0.80*EM floor
  3. NOT EXCEEDED by price    — beyond the session extreme
  then: MOST LIQUID among survivors, tie-break NEAREST the rail
  and:  leg order from the apparent SLOPE, flat falls back to proximity

⚠️ THE ONE THAT WOULD HAVE SHIPPED BROKEN. `_liquidity_rank` replaces an
`open_interest + volume` sum that factor_sweep found CONSTANT across the whole
joined sample — so `max_liq` was 0, the `else: top = eligible` branch took every
call, and "most liquid" silently resolved to "nearest the floor" from
v-dualfloor onward. A test that only checks the happy path with populated OI
would pass against the broken version too, so the suite asserts the ranking
works with OI and volume BOTH ZERO — the state the fleet is actually in.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_condor_pitchfork_anchor.py -q
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy.iron_condor_strategy import IronCondorStrategy   # noqa: E402


class C:
    """Minimal OptionContract stand-in — only the fields the selector reads."""

    def __init__(self, strike, bid=1.00, ask=1.10, mark=None, oi=0, vol=0):
        self.strike = float(strike)
        self.bid, self.ask = float(bid), float(ask)
        self.mark = float(mark if mark is not None else (bid + ask) / 2.0)
        self.open_interest, self.volume = oi, vol

    def __repr__(self):
        return f"C({self.strike})"


def S():
    return IronCondorStrategy.__new__(IronCondorStrategy)      # no __init__ needed


# ── the three filters ───────────────────────────────────────────────────────

def test_call_must_clear_the_rail():
    sel = S()._select_beyond_rail(
        [C(100), C(105), C(110)], "call",
        rail=104.0, min_distance_level=0.0, session_extreme=None)
    assert sel.strike == 105.0, "a strike inside the rail was selected"


def test_put_must_clear_the_rail():
    sel = S()._select_beyond_rail(
        [C(90), C(95), C(100)], "put",
        rail=96.0, min_distance_level=1e9, session_extreme=None)
    assert sel.strike == 95.0


def test_min_distance_survives_a_rail_sitting_on_spot():
    """v-dualfloor's floor is retained as a MINIMUM. A rail near spot must not
    produce a strike with no breathing room — the ~3-week bleed."""
    sel = S()._select_beyond_rail(
        [C(101), C(103), C(108)], "call",
        rail=100.5, min_distance_level=107.0, session_extreme=None)
    assert sel.strike == 108.0, "the min-distance floor was not applied"


def test_session_extreme_blocks_a_strike_price_already_reached():
    """A level price has traded through today is one the market has PROVEN it
    can reach. THE NEW CONSTRAINT — nothing tested this before PF.5."""
    sel = S()._select_beyond_rail(
        [C(105), C(110), C(115)], "call",
        rail=104.0, min_distance_level=0.0, session_extreme=112.0)
    assert sel.strike == 115.0, "a strike below the session high was selected"


def test_all_three_filters_compose():
    sel = S()._select_beyond_rail(
        [C(105), C(110), C(115), C(120)], "call",
        rail=106.0, min_distance_level=111.0, session_extreme=113.0)
    assert sel.strike == 115.0


def test_no_inside_fallback_returns_None():
    """No eligible strike must SKIP the leg, never fall back inward."""
    assert S()._select_beyond_rail(
        [C(100), C(101)], "call",
        rail=150.0, min_distance_level=0.0, session_extreme=None) is None


def test_unpriced_contracts_are_ineligible():
    assert S()._select_beyond_rail(
        [C(110, bid=0.0, ask=0.0, mark=0.0)], "call",
        rail=100.0, min_distance_level=0.0, session_extreme=None) is None


# ── liquidity: the part that was silently dead ──────────────────────────────

def test_liquidity_ranks_on_width_with_OI_AND_VOLUME_BOTH_ZERO():
    """THE STATE THE FLEET IS ACTUALLY IN. The old ranker summed OI+volume,
    both zero, so every selection fell through to the fallback. Width must pick
    the tight quote even with no depth data at all."""
    wide = C(110, bid=1.00, ask=1.60, oi=0, vol=0)      # 46% of mid
    tight = C(115, bid=1.00, ask=1.02, oi=0, vol=0)     # 2% of mid
    sel = S()._select_beyond_rail([wide, tight], "call",
                                  rail=105.0, min_distance_level=0.0,
                                  session_extreme=None)
    assert sel.strike == 115.0, (
        "the wide-quote strike was selected — ranking is not reading bid/ask "
        "width, which is the only populated liquidity signal")


def test_tie_break_is_nearest_the_rail():
    """Equally liquid survivors: take the one closest to the rail — the richest
    premium that still clears everything, not the deepest OTM."""
    a = C(110, bid=1.00, ask=1.02)
    b = C(120, bid=1.00, ask=1.02)
    sel = S()._select_beyond_rail([a, b], "call", rail=105.0,
                                  min_distance_level=0.0, session_extreme=None)
    assert sel.strike == 110.0


def test_depth_only_breaks_ties_when_width_is_equal():
    equal_a = C(110, bid=1.00, ask=1.02, oi=0, vol=0)
    equal_b = C(112, bid=1.00, ask=1.02, oi=5000, vol=900)
    sel = S()._select_beyond_rail([equal_a, equal_b], "call", rail=105.0,
                                  min_distance_level=0.0, session_extreme=None)
    # both in the cohort; nearest-the-rail still decides
    assert sel.strike == 110.0


# ── leg order from slope ────────────────────────────────────────────────────

def test_up_slope_fills_the_PUT_side_first():
    assert IronCondorStrategy._leg_order_from_slope(0.001, 0.00002) == ("put", "call")


def test_down_slope_fills_the_CALL_side_first():
    assert IronCondorStrategy._leg_order_from_slope(-0.001, 0.00002) == ("call", "put")


def test_flat_fork_returns_None_so_the_caller_keeps_proximity():
    """A SIGN IS NOT A SLOPE. Below the epsilon the drift is noise and ordering
    off it reads a coin flip as structure."""
    assert IronCondorStrategy._leg_order_from_slope(0.000001, 0.00002) is None
    assert IronCondorStrategy._leg_order_from_slope(0.0, 0.00002) is None
    assert IronCondorStrategy._leg_order_from_slope(None, 0.00002) is None


# ── deliberate failure ──────────────────────────────────────────────────────

def test_deliberate_failure_each_filter_is_load_bearing():
    """Relax each constraint in turn; the selection MUST move. If it does not,
    that filter is not being applied and the happy-path tests above would pass
    against a version that ignores it."""
    contracts = [C(105), C(110), C(115), C(120)]
    base = S()._select_beyond_rail(contracts, "call", rail=106.0,
                                   min_distance_level=111.0,
                                   session_extreme=113.0)
    assert base.strike == 115.0

    no_extreme = S()._select_beyond_rail(contracts, "call", rail=106.0,
                                         min_distance_level=111.0,
                                         session_extreme=None)
    assert no_extreme.strike == 115.0      # min-dist already binds at 111

    no_mindist = S()._select_beyond_rail(contracts, "call", rail=106.0,
                                         min_distance_level=0.0,
                                         session_extreme=None)
    assert no_mindist.strike == 110.0, (
        "dropping the min-distance floor did not move the selection — the "
        "floor is not being applied")

    no_rail = S()._select_beyond_rail(contracts, "call", rail=0.0,
                                      min_distance_level=0.0,
                                      session_extreme=None)
    assert no_rail.strike == 105.0, (
        "dropping the rail did not move the selection — the rail is not being "
        "applied")


def test_deliberate_failure_width_actually_decides():
    """Flip which contract carries the tight quote; the selection must follow
    it. If the same strike wins both ways, width is not being read."""
    tight_far = [C(110, bid=1.00, ask=1.60), C(120, bid=1.00, ask=1.02)]
    tight_near = [C(110, bid=1.00, ask=1.02), C(120, bid=1.00, ask=1.60)]
    a = S()._select_beyond_rail(tight_far, "call", rail=105.0,
                                min_distance_level=0.0, session_extreme=None)
    b = S()._select_beyond_rail(tight_near, "call", rail=105.0,
                                min_distance_level=0.0, session_extreme=None)
    assert (a.strike, b.strike) == (120.0, 110.0), (
        "the selection did not follow the tight quote — width is not deciding")
