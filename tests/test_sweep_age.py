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


# ── SWP.11 — acceptance is counted AFTER the reclaim ───────────────────────

def _sweep_frame():
    """A textbook high sweep: poke above the pool, close back inside, hold."""
    import pandas as pd
    idx = pd.date_range("2026-08-19 09:30", periods=40, freq="5min",
                        tz="America/New_York")
    h = [100.0] * 40; l = [99.0] * 40; c = [99.5] * 40; o = [99.5] * 40
    h[20], c[20] = 101.5, 100.4          # sweep bar — closes ABOVE the pool
    h[21], c[21] = 100.8, 99.6           # reclaim  — closes back INSIDE
    h[22], c[22] = 100.2, 99.5
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c}, index=idx)


def test_the_path_EXECUTES_no_NameError():
    """⚠️ THIS TEST EXISTS BECAUSE I NEARLY SHIPPED THE SAME BUG TWICE.
    SWP.11's first draft used `_rc_bar` in `closes_beyond` while `_rc_bar` was
    defined FOURTEEN LINES LATER — a NameError on every sweep evaluation. That
    is the exact defect class as the `ctx` P0 that stopped boxes trading on
    2026-08-18, and an import check cannot catch either: the name resolves at
    RUNTIME, inside the function. **The path must be EXECUTED (WA §21).**"""
    from analysis.liquidity_mapper import LiquidityMapper
    df = _sweep_frame()
    LiquidityMapper().analyze(df, df, 99.5)          # must not raise


def test_the_sweep_bar_close_no_longer_counts_as_acceptance():
    """⚠️ THE VETO WINDOW AND THE CONFIRMATION WINDOW WERE THE SAME WINDOW.
    `window` starts at the SWEEP BAR, and on a high sweep price is BY
    DEFINITION above the pool there — so the sweep's own close (100.4 here)
    was counted as acceptance, and `closes_beyond >= 2` vetoed the setup.
    Measured 2026-08-15: that veto blocked 64.5% of named-pool ticks and of
    25,792 vetoed ticks post-08-11, **100% were reclaimed and 0% were genuine
    acceptance.**"""
    from analysis.liquidity_mapper import LiquidityMapper
    df = _sweep_frame()
    r = LiquidityMapper().analyze(df, df, 99.5)
    sw = getattr(r, "recent_sweep", None)
    assert sw is not None, "a textbook sweep must still be detected"
    assert getattr(sw, "closes_beyond", 99) == 0, \
        "the sweep bar's own close is being counted as acceptance again"


def test_the_reclaim_bar_is_after_the_sweep_bar():
    from analysis.liquidity_mapper import LiquidityMapper
    df = _sweep_frame()
    sw = getattr(LiquidityMapper().analyze(df, df, 99.5), "recent_sweep", None)
    assert sw.reclaim_bar_index > sw.bar_index


def test_genuine_acceptance_is_still_vetoed():
    """⚠️ THE FIX MUST NOT BE A BLANKET UNGATE. If price reclaims and then
    leaves again and STAYS out, that IS acceptance and the veto must fire —
    otherwise this trades every failed reversal."""
    import pandas as pd
    from analysis.liquidity_mapper import LiquidityMapper
    idx = pd.date_range("2026-08-19 09:30", periods=40, freq="5min",
                        tz="America/New_York")
    h = [100.0] * 40; l = [99.0] * 40; c = [99.5] * 40; o = [99.5] * 40
    h[20], c[20] = 101.5, 100.4          # sweep
    h[21], c[21] = 100.8, 99.6           # reclaim
    h[22], c[22] = 101.0, 100.6          # left again...
    h[23], c[23] = 101.2, 100.9          # ...and STAYED out -> acceptance
    df = pd.DataFrame({"open": o, "high": h, "low": l, "close": c}, index=idx)
    r = LiquidityMapper().analyze(df, df, 99.5)
    sw = getattr(r, "recent_sweep", None)
    if sw is not None:
        assert getattr(sw, "closes_beyond", 0) >= 2, \
            "post-reclaim closes beyond the level must still count as acceptance"
