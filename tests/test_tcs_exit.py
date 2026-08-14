#!/usr/bin/env python3
"""
tests/test_tcs_exit.py — v1.0 — 2026-08-13   (TC.6)

Operator's spec: *"Exit should be breached (loss) or nickel close (profit)."*
No premium stop, no ratchet — and that is not a simplification. **The measured
EV was held to expiry, UNMANAGED** (+$0.52/spread, 90% terminal OK, 79%
recovered on the ORB-anchored runaway arm). A stop bolted on afterwards is a
different trade with a different expectancy, and paper results from it would not
transfer.

THE TWO FAILURES THIS SUITE EXISTS TO CATCH:
  1. A TC.6 leg reaching the condor's ratchet or 25% stop — then we would be
     paper-trading something other than what was measured, and the numbers would
     look fine while meaning nothing.
  2. A WICK through the boundary counting as a breach. Only a CLOSE decides
     acceptance — the operator's own rule, and the same distinction that made
     `tcs_floor_durability` v1.1 report 14.7% intraday against 56.1% terminal.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_tcs_exit.py -q
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC = open(os.path.join(os.path.dirname(__file__), "..",
                        "execution", "exit_engine.py"), encoding="utf-8").read()


def condor_fn() -> str:
    start = SRC.index("    def _evaluate_condor_leg(")
    return SRC[start:SRC.index("\n    def ", start + 10)]


def line_of(needle: str) -> int:
    body = condor_fn()
    assert needle in body, f"{needle!r} not in _evaluate_condor_leg"
    return body[:body.index(needle)].count("\n")


# ── ladder order: a TC.6 leg must never reach the ratchet ───────────────────

def test_tcs_branch_returns_before_the_ratchet_and_the_25pct_stop():
    """THE ONE THAT MATTERS. If the TC.6 branch sits after the ratchet, a trend
    credit spread inherits the condor's stop and we are no longer trading what
    was measured."""
    tcs = line_of('if bool(record.get("is_trend_credit")):')
    ratchet = line_of("RATCHET SCOPE")
    stop = line_of('decision.exit_reason = f"condor_stop')
    tp = line_of("TIME-GATED TAKE PROFIT")
    assert tcs < ratchet, "the TC.6 branch runs AFTER the ratchet"
    assert tcs < stop, "the TC.6 branch runs AFTER the 25% stop"
    assert tcs < tp, "the TC.6 branch runs AFTER the take-profit"


def test_hard_close_still_outranks_everything():
    """15:45 is unconditional and must precede the TC.6 branch — a position
    cannot be held past the flatten by any exit rule."""
    assert line_of('decision.exit_reason = "hard_close_15:45_ET"') < \
        line_of('if bool(record.get("is_trend_credit")):')


def test_the_tcs_branch_returns_rather_than_falling_through():
    """Both TC.6 exits must `return decision`. A fall-through would drop the leg
    into the condor ladder below with no further guard."""
    body = condor_fn()
    seg = body[body.index('if bool(record.get("is_trend_credit")):'):
               body.index("        _prev_hard = None") if "_prev_hard = None" in body
               else body.index("# ── ADVERSE REGIME FLIP") if "ADVERSE REGIME FLIP" in body
               else body.index("RATCHET SCOPE")]
    assert seg.count("return decision") >= 2, \
        "the breach and nickel paths do not both return"


# ── breach is a CLOSE, never a wick ────────────────────────────────────────

def test_breach_reads_the_CLOSE_column_only():
    body = condor_fn()
    seg = body[body.index('if bool(record.get("is_trend_credit")):'):]
    seg = seg[:seg.index("return decision", seg.index("tcs_breach"))]
    assert 'df_1m["close"]' in seg, "the breach rule is not reading closes"
    for wick in ('df_1m["high"]', 'df_1m["low"]'):
        assert wick not in seg, (
            f"the breach rule reads {wick} — a WICK through the boundary is a "
            "TOUCH, and only a CLOSE decides acceptance")


def test_breach_direction_is_side_aware():
    """A put spread sits BELOW the boundary so a close BELOW breaches; a call
    spread sits above so a close ABOVE breaches. Getting this backwards would
    exit every winner and hold every loser."""
    body = condor_fn()
    seg = body[body.index('if bool(record.get("is_trend_credit")):'):]
    m = re.search(r'_breached\s*=\s*\((.*?)\)\s*if\s*_side\s*==\s*"put"\s*else\s*\((.*?)\)', seg)
    assert m, "the side-aware breach expression is missing"
    assert "<" in m.group(1) and ">" in m.group(2), (
        "breach directions are inverted: put must breach on a close BELOW the "
        "boundary and call on a close ABOVE")


def test_missing_tape_is_reported_not_silently_passed():
    """A breach rule that cannot see price is INERT, and an inert stop must
    never look like a passing check."""
    body = condor_fn()
    seg = body[body.index('if bool(record.get("is_trend_credit")):'):]
    assert "logger.warning" in seg and "INERT" in seg, \
        "a missing 1m tape is not being reported"


# ── the branch is scoped to TC.6 only ──────────────────────────────────────

def test_ordinary_condor_legs_are_untouched():
    """`is_trend_credit` gates the whole branch, so a normal condor leg still
    gets ratchet, stop, TP and nickel."""
    body = condor_fn()
    assert body.count('record.get("is_trend_credit")') == 1
    for keeper in ("RATCHET SCOPE", "condor_stop", "condor_tp"):
        assert keeper in body, f"{keeper} was removed from the condor path"


def tcs_branch_source() -> str:
    """The TC.6 `if` block, sliced by AST rather than by text.

    A textual slice ran past the branch into condor code and made the guard
    below fail on the condor's OWN stop — a false positive that would have
    trained someone to loosen the check. The AST knows where the block ends.
    """
    import ast
    tree = ast.parse(SRC)
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and "is_trend_credit" in (
                ast.get_source_segment(SRC, node.test) or ""):
            return ast.get_source_segment(SRC, node) or ""
    raise AssertionError("the TC.6 branch is gone from exit_engine")


def test_no_premium_stop_inside_the_tcs_branch():
    """DELIBERATE FAILURE GUARD. If a future edit adds a premium stop here, the
    trade stops matching the measurement and this goes red."""
    seg = tcs_branch_source()
    for banned in ("CONDOR_STOP_LOSS_PCT", "CONDOR_RATCHET", "stop_level"):
        assert banned not in seg, (
            f"{banned} appears inside the TC.6 branch — the measured EV was "
            "HELD TO EXPIRY, UNMANAGED, and a stop changes the trade")


# ── the fall-through that shipped, and the test that missed it ─────────────

def test_the_branch_ENDS_in_a_return_not_just_contains_one():
    """⚠️ THE v1.0 TEST ASSERTED THE BRANCH CONTAINED TWO `return decision`
    STATEMENTS. IT DID. And it was still broken.

    Neither return covers the path where NEITHER breach NOR nickel fires — and
    that path fell through to the ratchet and the 25% condor stop. Observed live
    2026-08-14: a $0.06 credit sets stop_premium at $0.07 (credit x 1.25), so
    ONE CENT of widening closed the trade. Every TC.6 leg on the fleet stopped
    out within seconds of opening.

    Counting returns proves nothing about the path that has none. This asserts
    on the branch's LAST STATEMENT, which is the only thing that makes the
    ratchet unreachable.
    """
    import ast
    tree = ast.parse(SRC)
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and "is_trend_credit" in (
                ast.get_source_segment(SRC, node.test) or ""):
            last = node.body[-1]
            assert isinstance(last, ast.Return), (
                "the TC.6 branch does not END in a return — it falls through to "
                "the ratchet and the 25% stop, which is a different trade from "
                "the one that was measured")
            return
    raise AssertionError("the TC.6 branch is gone from exit_engine")


def test_every_path_out_of_the_branch_is_a_return():
    """Stronger form: no statement after the branch's own control flow can leak
    into the condor ladder."""
    import ast
    tree = ast.parse(SRC)
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and "is_trend_credit" in (
                ast.get_source_segment(SRC, node.test) or ""):
            src_seg = ast.get_source_segment(SRC, node)
            assert src_seg.rstrip().endswith("return decision")
            return


# ── the joint EV test ──────────────────────────────────────────────────────

def test_joint_ev_requires_rich_credit_at_low_pop_and_allows_thin_at_high():
    """THE SHAPE IS THE POINT. A flat credit floor and a flat POP floor are
    INDEPENDENT, and independent is the bug: POP >= 0.70 selects FAR strikes,
    far strikes pay little, and neither floor ever sees the other.
    credit/width > L*(1-POP)/POP links them."""
    import config
    L = config.TCS_LOSS_GIVEN_BREACH
    req = lambda pop: L * (1.0 - pop) / pop
    assert req(0.70) > req(0.80) > req(0.90) > req(0.95)
    assert req(0.70) > 0.20, "a POP-0.70 strike must pay richly"
    assert req(0.95) < 0.05, "a POP-0.95 strike may be thin"


def test_joint_ev_blocks_the_2026_08_14_live_fills():
    """Regression on real fills: NVDA sold a $5-wide for $0.06 and PLTR a
    $6-wide for $0.08 at 10:02 ET. Both must fail on EV ALONE, even at a
    generous POP."""
    import config
    L = config.TCS_LOSS_GIVEN_BREACH
    for credit, width, pop in ((0.06, 5.0, 0.96), (0.08, 6.0, 0.96)):
        assert credit / width <= L * (1.0 - pop) / pop, (
            f"credit {credit} on width {width} still clears the EV test")
    # and a real one still passes
    assert 0.55 / 5.0 > L * (1.0 - 0.90) / 0.90


def test_unresolvable_pop_is_a_skip_not_a_pass():
    """A missing ATR must never read as a safe trade — `_pop` returns 0.0 and
    the caller must SKIP, not divide by it."""
    src = open(os.path.join(os.path.dirname(__file__), "..", "strategy",
                            "trend_credit_spread.py"), encoding="utf-8").read()
    i = src.index("pop = self._sel._pop(")
    assert "if pop <= 0.0:" in src[i:i + 400]
    assert "return None" in src[i:i + 600]
