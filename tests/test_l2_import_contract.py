"""
tests/test_l2_import_contract.py — v1.0 — 2026-07-29.

THE DEFECT THIS EXISTS FOR (fleet-wide, 2026-07-29):
    main.py imported RANGE_WINDOW_BARS from analysis.conviction_integrator,
    which does not define it — the symbol is owned by analysis.regime_confluence
    and was only reachable because conviction_integrator re-exported a tuple of
    constants. The v1.3 excavation trimmed that tuple, the import raised, and
    main.py's `except Exception` guard turned a hard contract break into one
    WARNING per start. All 15 boxes traded a full session on the v1.3 fallback
    classifier instead of the L2.5 conviction integrator. Nothing crashed;
    nothing alerted; every conviction value logged that day was off-engine.

WHY UNIT TESTS MISSED IT:
    every existing suite imports the analysis modules DIRECTLY, so they all
    passed. Nothing asserted the import contract main.py itself depends on, and
    main.py is not importable in the test environment (SDK, env, systemd).

THE RULE THESE TESTS ENFORCE:
    a symbol is imported from the module that DEFINES it. A re-export is a
    convenience, never a contract — it can be trimmed by an unrelated refactor
    in a module that has no idea who is leaning on it.

Run: PYTHONPATH=. pytest tests/test_l2_import_contract.py -v
"""

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(REPO, "main.py")


def test_l2_symbols_resolve_from_their_owning_modules():
    """The exact import main.py performs must succeed with no guard."""
    from analysis.regime_confluence import (  # noqa: F401
        RegimeConfluenceScorer, RANGE_WINDOW_BARS,
    )
    from analysis.conviction_integrator import ConvictionIntegrator  # noqa: F401

    assert isinstance(RANGE_WINDOW_BARS, int)
    assert RANGE_WINDOW_BARS > 0


def test_range_window_bars_is_owned_by_regime_confluence():
    """Ownership assertion. If this symbol ever legitimately moves, this test
    should be updated deliberately — not discovered at runtime on 15 boxes."""
    import analysis.regime_confluence as rc
    import analysis.conviction_integrator as ci

    assert hasattr(rc, "RANGE_WINDOW_BARS"), \
        "RANGE_WINDOW_BARS must be defined in regime_confluence (its owner)"
    assert not hasattr(ci, "RANGE_WINDOW_BARS"), \
        ("conviction_integrator must NOT re-export RANGE_WINDOW_BARS — if it "
         "does, main.py can silently start depending on the re-export again "
         "and the 2026-07-29 outage becomes reachable a second time")


def test_main_does_not_import_range_window_bars_via_conviction_integrator():
    """Source-level guard: the broken import form must not return on a stale
    sync or a bad merge. Read as text — main.py is not importable here."""
    src = open(MAIN, encoding="utf-8").read()
    bad = re.search(
        r"from\s+analysis\.conviction_integrator\s+import\s+[^\n]*RANGE_WINDOW_BARS",
        src)
    assert bad is None, \
        f"main.py re-imports RANGE_WINDOW_BARS via conviction_integrator: {bad.group(0) if bad else ''}"

    good = re.search(
        r"from\s+analysis\.regime_confluence\s+import\s+[^\n]*RANGE_WINDOW_BARS",
        src)
    assert good is not None, \
        "main.py must import RANGE_WINDOW_BARS from regime_confluence (its owner)"


def test_l2_fallback_is_loud():
    """Trading survives a degraded regime engine, so the ONLY thing that makes
    it visible is the alert. Assert the fallback path pages and logs at ERROR —
    a WARNING is what let this run unnoticed for a full session."""
    src = open(MAIN, encoding="utf-8").read()
    guard = src[src.index("_L2_OK = False"):]
    window = guard[:1200]

    assert "logger.error" in window, \
        "the L2 fallback must log at ERROR — WARNING is why this hid for a session"
    assert "send_regime_engine_degraded_alert" in window, \
        "the L2 fallback must page: a silent engine swap invalidates the session's conviction data"


def test_degraded_alert_exists_on_the_alert_manager():
    from notifications.alert_manager import AlertManager
    assert hasattr(AlertManager, "send_regime_engine_degraded_alert")


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-v"]))
