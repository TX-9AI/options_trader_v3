#!/usr/bin/env python3
"""
tests/test_sweep_age.py — v1.0 — 2026-08-19   (SWP.10)

THE SWEEP WAS AGED FROM A BAR IT COULD NOT BE TRADED ON.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_sweep_age.py -q

`bars_ago` counted from the SWEEP bar. **The setup is not tradeable until price
closes back INSIDE the level** — and the mapper runs on 5m/15m with
`SWEEP_REJECTION_CANDLES = 3`, so confirmation lands **5-20 minutes** after the
sweep. `age_decay = 0.5**(age/3)` therefore charged the signal for every bar of
a delay it had no way to act inside.

⚠️ MEASURED (SWP.9, 269,027 named-pool rows across 27 sessions):
  · **95.9% hard-vetoed to 0.000** before scoring — 67% of those by
    `veto_accept`, the `closes_beyond >= 2` rule.
  · Of the 4.1% that survive, `age_decay` median **0.062** — which solves to
    ~12 bars ≈ **60 MINUTES** on a 5m frame. `trend_opp` median was **1.000**,
    so age was the sole binding damper.
  · Median surviving score ≈ 1.0 × 0.062 × 0.5 ≈ **0.031**, against
    `SWEEP_SETUP_FLOOR = 0.05`. **The survivors did not clear their own
    dispatch floor.**

⚠️ THIS IS NOT A RECALIBRATION, AND THAT DISTINCTION IS THE POINT. No constant
changes — not `SWEEP_HALFLIFE_BARS`, not the floor. It corrects WHAT the age
measures. At the observed median the score moves **0.031 -> 0.062**: past the
floor on the arithmetic alone. **If a fit had been needed, this would not have
been sufficient — and it is.**
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MAPPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                      "analysis", "liquidity_mapper.py")


def _src():
    return open(MAPPER, encoding="utf-8").read()


def test_age_is_measured_from_the_reclaim_not_the_sweep():
    s = _src()
    assert "bars_ago=(n - 1 - _rc_bar)" in s
    assert "bars_ago=(n - 1 - i)" not in s, \
        "a site still ages from the sweep bar"


def test_both_sweep_directions_were_fixed():
    """High and low sweeps are separate branches with mirrored comparisons —
    fixing one and not the other would leave half the population stale."""
    assert _src().count("_rc_bar = next((k for k in window") == 2
    assert _src().count("bars_ago=(n - 1 - _rc_bar)") == 2


def test_the_sweep_bar_is_still_recorded():
    """`bar_index` stays: the sweep bar is the diagnostic anchor even though it
    is no longer the aging clock."""
    s = _src()
    assert "bar_index=i," in s
    assert "reclaim_bar_index=_rc_bar," in s


def test_reclaim_bar_falls_back_to_the_sweep_bar():
    """`next(..., i)` — if no close in the window returns inside, the sweep is
    not `reclaimed` and will not be emitted; the default must still be a real
    bar index rather than raising or yielding None."""
    assert "if closes[k] <= pool.price), i)" in _src()
    assert "if closes[k] >= pool.price), i)" in _src()


def test_no_constant_was_touched():
    """⚠️ THE CLAIM THIS FILE RESTS ON. A fix that moves the median past the
    floor WITHOUT changing a threshold is a defect correction; changing
    SWEEP_HALFLIFE_BARS or SWEEP_SETUP_FLOOR to achieve the same result would
    be fitting the score to the outcome we want."""
    import config
    from analysis.regime_confluence import SWEEP_HALFLIFE_BARS
    assert SWEEP_HALFLIFE_BARS == 3.0
    assert config.SWEEP_SETUP_FLOOR == 0.05


def test_the_arithmetic_clears_the_floor_at_the_observed_median():
    """age 12 (old) -> 9 (new) at the measured median confirmation latency."""
    from analysis.regime_confluence import SWEEP_HALFLIFE_BARS as H
    import config
    corrob = 0.5
    old = (0.5 ** (12 / H)) * corrob
    new = (0.5 ** (9 / H)) * corrob
    assert old < config.SWEEP_SETUP_FLOOR <= new, \
        f"old {old:.3f} new {new:.3f} floor {config.SWEEP_SETUP_FLOOR}"
