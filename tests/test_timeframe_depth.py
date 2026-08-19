#!/usr/bin/env python3
"""
tests/test_timeframe_depth.py — v1.0 — 2026-08-19   (L1.9a)

A TIMEFRAME CONFIGURED BELOW ITS CONSUMER'S REQUIREMENT CAN NEVER VOTE.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_timeframe_depth.py -q

`trend_engine` refuses to vote on any timeframe with fewer than `EMA_SLOW + 5`
= **55** bars. `TIMEFRAMES["1h"]` asked for exactly **50**. So the 1h trend vote
**could never fire** — not on a thin day, not after a restart, **never** — and
1h is the second-heaviest timeframe in the blend (1d 0.15 · **1h 0.20** ·
15m 0.30). Its *"declared weight contributes nothing"* warning has been firing
on every box since the engine shipped, and was read as a transient.

⚠️ THIS IS WHY L1.6/L1.7 WERE STUCK. The TRENDING row needs a session
*"dominant ~50% with RANGING vetoed through it."* A permanently absent
structure-timeframe vote depresses TRENDING and inflates RANGING: TSLA 08-04
showed **99% TRENDING dominance with RANGING still scoring on 64% of ticks**
and A2 failing at 14%. **26 TREND sessions were already labeled and the row was
still open.** The roadmap called the remaining work *"habit, not code."* It was
code.

⚠️ THE GENERAL LESSON: a numeric config below a hard consumer threshold is a
PERMANENT silent failure, and it announces itself as a warning that looks
transient. This test makes the class impossible to reintroduce by deriving the
requirement from the engine rather than hardcoding it here.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config                                                    # noqa: E402


def _required_bars():
    """Derived, never hardcoded — if the engine's rule changes, this follows."""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "analysis", "trend_engine.py"), encoding="utf-8").read()
    assert "len(df) < EMA_SLOW + 5" in src, \
        "the trend engine's depth rule changed — update this derivation"
    return config.EMA_SLOW + 5


def test_every_timeframe_can_actually_vote():
    need = _required_bars()
    starved = {tf: d["candles"] for tf, d in config.TIMEFRAMES.items()
               if d.get("candles", 0) < need}
    assert not starved, (
        f"configured below the engine's requirement of {need}: {starved} — "
        "these timeframes can NEVER vote and their declared weight contributes "
        "nothing")


def test_1h_specifically_since_it_carries_0_20_weight():
    assert config.TIMEFRAMES["1h"]["candles"] >= _required_bars()


def test_there_is_margin_not_just_a_bare_pass():
    """⚠️ THE MINIMUM IS A CLIFF, NOT A TARGET. A frame that only just clears it
    starves again on any short session, a restart, or a holiday half-day — and
    the failure is silent."""
    need = _required_bars()
    assert config.TIMEFRAMES["1h"]["candles"] >= need + 20, \
        "1h has no margin above the starvation threshold"


def test_the_feed_can_actually_supply_what_is_configured():
    """A config the feed cannot fill is the same defect one layer up. 1h
    backfills 16 days at ~7 RTH bars/day = ~112, and pruning is OFF."""
    import data.candle_feed as cf
    days = cf.BACKFILL_DAYS.get("1h", 0)
    assert days * 7 >= config.TIMEFRAMES["1h"]["candles"], \
        "1h asks for more bars than the backfill window can supply"
    assert cf.PRUNE_KEEP_ROWS == 0, \
        "pruning is on again — re-check that it keeps enough 1h bars"
