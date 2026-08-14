#!/usr/bin/env python3
"""
tests/test_cnt1_breakout_exit.py — v1.0 — 2026-08-14

CNT.1 SHIPPED HALF A FEATURE ON 2026-08-07 AND NOBODY NOTICED FOR A WEEK.

`continuation_strategy` (CNT.1) lets continuation OPEN on BREAKOUT_VOLATILE,
taking direction from the trend vote instead of the label and gating on ADX. It
tags those `trend_continuation_breakout`.

`exit_engine._evaluate_continuation`'s `still_trending` only ever accepted
TRENDING_BULL / TRENDING_BEAR.

**So a breakout continuation was BORN ALREADY FAILING ITS OWN EXIT TEST.** It
opens on tick N with the label at BREAKOUT_VOLATILE; on tick N+1 the exit reads
the SAME UNCHANGED LABEL, finds it is not TRENDING_*, and closes as
`regime_flip`. THE LABEL NEVER FLIPPED — the exit reason was a lie.

MEASURED LIVE 2026-08-14, and the timestamps are the proof:
    SMH  14:24:19 -> 14:24:34   (15s = exactly one tick)
         14:24:49 -> 14:25:04
         14:25:19 -> 14:25:34   ... eight in a row
P&L was symmetric noise (SMH's eight netted -$29, GS's eight +$331) because a
one-tick hold is one tick of random walk minus the spread. **The repetition was
a side effect; each trade was incoherent on its own.**

⚠️ THE DIAGNOSTIC TRAP THIS ALSO RECORDS: the obvious reading of eight identical
15-second trades is "churn — add a cooldown." A cooldown would have hidden the
loop and fixed nothing, which is WORSE than leaving it alone, because the
symptom is what exposed the defect. The operator caught that:
*"It's not a re-entry or cooldown problem... If they were profitable it wouldn't
be a problem."*

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_cnt1_breakout_exit.py -q
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC = open(os.path.join(os.path.dirname(__file__), "..", "execution",
                        "exit_engine.py"), encoding="utf-8").read()


def still_trending(setup_type, direction, regime):
    """Mirrors the engine's test. Kept honest by
    `test_mirror_matches_the_engine_source` below."""
    rgm = (regime or "").upper()
    is_breakout = str(setup_type or "").endswith("_breakout")
    return (
        (direction == "long" and "TRENDING_BULL" in rgm) or
        (direction == "short" and "TRENDING_BEAR" in rgm) or
        (is_breakout and "BREAKOUT_VOLATILE" in rgm)
    )


# ── the defect ─────────────────────────────────────────────────────────────

def test_a_breakout_continuation_survives_its_own_entry_label():
    """THE ONE THAT MATTERS. A trade opened on BREAKOUT_VOLATILE must not be
    closed by BREAKOUT_VOLATILE on the next tick."""
    for direction in ("long", "short"):
        assert still_trending("trend_continuation_breakout", direction,
                              "BREAKOUT_VOLATILE"), (
            f"a {direction} breakout continuation still exits on the label it "
            f"was OPENED on — it is born failing its own exit test")


def test_a_genuine_flip_still_exits_a_breakout_continuation():
    """The fix must not make breakout trades unkillable. Any label that is
    neither its own nor its direction's still closes it."""
    for regime in ("RANGING", "COMPRESSION", "CHOP"):
        assert not still_trending("trend_continuation_breakout", "short", regime)


def test_direction_still_matters_for_non_breakout_setups():
    """Scope check: only `_breakout` gains the exemption."""
    assert not still_trending("trend_continuation_standalone", "short",
                              "BREAKOUT_VOLATILE")
    assert not still_trending("trend_continuation_handoff", "long",
                              "BREAKOUT_VOLATILE")


def test_ordinary_continuation_behaviour_is_unchanged():
    assert still_trending("trend_continuation_standalone", "long", "TRENDING_BULL")
    assert still_trending("trend_continuation_handoff", "short", "TRENDING_BEAR")
    assert not still_trending("trend_continuation_standalone", "long", "TRENDING_BEAR")


def test_a_missing_setup_type_does_not_grant_the_exemption():
    """`record.get("setup_type")` can be None on an old row. None must NOT
    read as a breakout trade — failing closed here means an ordinary trade
    keeps its ordinary exit."""
    assert not still_trending(None, "short", "BREAKOUT_VOLATILE")
    assert not still_trending("", "long", "BREAKOUT_VOLATILE")


# ── the mirror is only evidence if the engine still matches it ─────────────

def test_mirror_matches_the_engine_source():
    assert '_is_breakout_cont = str(record.get("setup_type") or "").endswith("_breakout")' in SRC
    assert '(_is_breakout_cont and "BREAKOUT_VOLATILE" in rgm)' in SRC


def test_the_flip_check_still_precedes_bos_exit():
    """Ordering is load-bearing: the flip block runs BEFORE bos_exit, which is
    why nothing else ever got a look at these trades. If that order changes,
    the reasoning in the changelog stops being true."""
    i_flip = SRC.index("still_trending = (")
    i_bos = SRC.index('exit_reason = f"bos_exit pnl=', i_flip)
    assert i_flip < i_bos


# ── deliberate failure ─────────────────────────────────────────────────────

def test_deliberate_failure_the_exemption_is_load_bearing():
    """Without the breakout clause the live case MUST fail. Proves the new
    term is doing the work rather than the test passing for another reason."""
    def without(setup_type, direction, regime):
        rgm = (regime or "").upper()
        return ((direction == "long" and "TRENDING_BULL" in rgm) or
                (direction == "short" and "TRENDING_BEAR" in rgm))
    assert not without("trend_continuation_breakout", "short", "BREAKOUT_VOLATILE")
    assert still_trending("trend_continuation_breakout", "short", "BREAKOUT_VOLATILE")


def test_deliberate_failure_a_cooldown_would_not_have_fixed_this():
    """RECORDED AS A METHOD LESSON, not as executable coverage. Eight identical
    15-second trades read as churn; the obvious fix is a cooldown. But the
    trades were incoherent INDIVIDUALLY — a cooldown would have spaced out
    incoherent trades and hidden the evidence that exposed the defect.
    The symptom is not the bug."""
    entries = ["14:24:19", "14:24:49", "14:25:19", "14:25:49"]
    holds_sec = [15, 15, 15, 15]
    assert len(set(holds_sec)) == 1 and holds_sec[0] == 15, (
        "a hold time equal to the TICK INTERVAL, identical every time, is a "
        "structural exit firing immediately — not a market outcome")
    assert len(entries) == 4
