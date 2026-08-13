#!/usr/bin/env python3
"""
tests/test_condor_ratchet_scope.py — v1.0 — 2026-08-13

Operator ruling: *"the ratchet is inappropriate for this trade if the condor is
fully formed. It should only be in effect if there's one side open."* And:
*"don't close a leg if it hasn't been tested — that's what the roll is for."*

THE DEFECT, stated as the test that would have caught it:

  The base -25% stop only ever fires on the TESTED side, because a credit
  spread's value RISES as price approaches your short. The RATCHET does the
  opposite — it tightens the UNTESTED side's stop to breakeven at +20% and
  +20%-locked at +40%, precisely BECAUSE that side is winning. On the reversal
  the tested leg stops at -25% and the untested leg hits its ratcheted stop as
  well. **A leg price never went near, closed by a stop that exists only because
  it was profitable.** That is the double-stop — 5 of 14 condor symbol-days had
  both sides stopped — and it fires BEFORE the roll is available, because the
  roll needs a tested side.

These tests exercise the RATCHET ARITHMETIC directly rather than standing up an
exit engine, because the arithmetic is the defect: `min(stop_level, prev)`
applied to a leg whose sibling is open.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_condor_ratchet_scope.py -q
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config                                                   # noqa: E402


def stop_level(entry_prem, pnl_pct, prev, formed,
               standalone_only=True):
    """The scoped ratchet, mirroring exit_engine._evaluate_condor_leg.

    Kept in step with the engine by `test_mirror_matches_the_engine_source`
    below, which asserts the engine still contains the branch this models — so
    a future edit that removes the scope makes this file go red rather than
    quietly diverge.
    """
    base = entry_prem * (1 + config.CONDOR_STOP_LOSS_PCT)
    lvl = base
    if pnl_pct >= config.CONDOR_RATCHET_LOCK_AT:
        lvl = min(lvl, entry_prem * (1 - config.CONDOR_RATCHET_LOCK_PCT))
    elif pnl_pct >= config.CONDOR_RATCHET_BE_AT:
        lvl = min(lvl, entry_prem)
    if standalone_only and formed:
        return base                       # base floor ONLY — tested side only
    if prev is not None:
        lvl = min(lvl, prev)
    return lvl


ENTRY = 1.00


# ── the defect, directly ────────────────────────────────────────────────────

def test_formed_condor_untested_leg_is_NOT_closed_on_a_reversal():
    """THE DOUBLE-STOP. Untested leg runs to +40%, ratchets, then reverses to
    flat. Under the old behaviour the ratcheted stop fires; scoped, it does not
    and only the -25% base floor can close it."""
    ratcheted = stop_level(ENTRY, 0.40, None, formed=False)
    assert ratcheted < ENTRY, "the +40% tier did not tighten below entry"

    # price reverses; spread value back to the entry credit
    current = ENTRY
    assert current >= ratcheted, "precondition: the old stop WOULD have fired"

    scoped = stop_level(ENTRY, 0.0, prev=ratcheted, formed=True)
    assert current < scoped, (
        "a leg that was never tested is still being closed on a formed condor")


def test_formed_leg_can_still_be_stopped_when_genuinely_TESTED():
    """Scoping the ratchet must not make a formed leg unstoppable. The -25%
    base floor still fires — that is the tested side."""
    base = stop_level(ENTRY, -0.30, None, formed=True)
    assert base == ENTRY * (1 + config.CONDOR_STOP_LOSS_PCT)
    tested_premium = ENTRY * 1.30
    assert tested_premium >= base


def test_standalone_leg_keeps_the_full_ratchet():
    """The gain the ratchet earned came mostly from STANDALONES — 18 of 46 legs
    never got a second side, and condor_stop went 0% -> 19% win. Scoping must
    not touch that."""
    assert stop_level(ENTRY, 0.40, None, formed=False) == \
        ENTRY * (1 - config.CONDOR_RATCHET_LOCK_PCT)
    assert stop_level(ENTRY, 0.25, None, formed=False) == ENTRY
    assert stop_level(ENTRY, 0.05, None, formed=False) == \
        ENTRY * (1 + config.CONDOR_STOP_LOSS_PCT)


def test_stored_highwater_is_ignored_while_formed_but_survives():
    """While formed the stored value is neither applied NOR updated, so a leg
    returning to standalone resumes from the high-water it genuinely earned
    rather than one set while the structure was intact."""
    hw = stop_level(ENTRY, 0.40, None, formed=False)
    assert stop_level(ENTRY, 0.0, prev=hw, formed=True) == \
        ENTRY * (1 + config.CONDOR_STOP_LOSS_PCT)
    assert stop_level(ENTRY, 0.0, prev=hw, formed=False) == hw


def test_kill_switch_restores_old_behaviour():
    assert stop_level(ENTRY, 0.0, prev=0.60, formed=True,
                      standalone_only=False) == 0.60


# ── deliberate failure ──────────────────────────────────────────────────────

def test_deliberate_failure_the_scope_is_load_bearing():
    """Same inputs, scope off vs on, MUST differ. If they match, the branch is
    not being taken and every test above would pass against the broken code."""
    hw = stop_level(ENTRY, 0.40, None, formed=False)
    on = stop_level(ENTRY, 0.0, prev=hw, formed=True, standalone_only=True)
    off = stop_level(ENTRY, 0.0, prev=hw, formed=True, standalone_only=False)
    assert on != off, "the standalone scope is not changing the stop level"
    assert on > off, "scoping must LOOSEN the stop on a formed condor, not tighten it"


def test_mirror_matches_the_engine_source():
    """The model above is only evidence if the engine still has the branch.
    Asserts on SOURCE SHAPE, not on a name appearing anywhere — an absence
    canary tests for a definition, never a mention (WORKING_AGREEMENT 20)."""
    src = open(os.path.join(os.path.dirname(__file__), "..",
                            "execution", "exit_engine.py"),
               encoding="utf-8").read()
    assert "_formed = (CONDOR_RATCHET_STANDALONE_ONLY" in src, \
        "the ratchet scope branch is gone from exit_engine"
    assert "stop_level, tier = base_stop" in src, \
        "the formed-condor path no longer falls back to the base floor"
