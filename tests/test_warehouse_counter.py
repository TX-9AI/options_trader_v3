#!/usr/bin/env python3
"""
tests/test_warehouse_counter.py — v1.0 — 2026-08-18   (WH.6)

TWO DAYS OF "DATA STRANDED ON BOX" ALARMS FOR A FENCEPOST.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_warehouse_counter.py -q

`_confirm` bumped its prefix counter **on every PUT, with no key-level dedupe**,
and the ledger persists to disk. Push the same key twice and `n` reads 2 while
S3 holds 1 — **permanently**. A prefix re-pushed once is short forever and the
gap can only grow.

**MEASURED 2026-08-18.** Ten prefixes, each short by exactly ONE:
1561/1560 · 1147/1146 · 1260/1259 · 2280/2279 · 2359/2358 · 1961/1960 ·
1197/1196 · 1263/1262 · 2046/2045. Then the bucket was listed directly:
`raw/shadow/dt=2026-07-24/sym=META/` held **1560** objects and
`raw/trades/dt=2026-08-17/sym=GS/` held **33** — exactly what the verify's own
LIST reported. **NOTHING WAS EVER MISSING.**

⚠️ AND THE MODULE PREDICTED IT. Its 2026-07-27 header: *"wrong counters make
the verify line lie in both directions."* The hazard was known; there was no
evidence of it until WH.5 stopped truncating the diagnosis at the log boundary.

⚠️ TEN OFF-BY-ONES IS A SIGNATURE. Real loss scatters; a systematic count error
does not. That heuristic is now printed alongside the shortfall so the reader
knows which question to ask first.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib.util as _u                                     # noqa: E402

_spec = _u.spec_from_file_location(
    "s3push", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "warehouse", "s3_push.py"))
sp = _u.module_from_spec(_spec)
try:
    _spec.loader.exec_module(sp)
except SystemExit:
    pass


def setup_function(_):
    sp._SEEN_KEYS.clear()


def test_a_duplicate_PUT_no_longer_inflates_the_counter():
    """THE BUG, in one assertion. Three PUTs, two distinct keys, count of 2."""
    c = {}
    sp._confirm("raw/x/dt=1/sym=A/k1.json", b"aaa", c)
    sp._confirm("raw/x/dt=1/sym=A/k2.json", b"bb", c)
    sp._confirm("raw/x/dt=1/sym=A/k1.json", b"aaa", c)
    assert c["raw/x/dt=1/sym=A/"]["n"] == 2
    assert c["raw/x/dt=1/sym=A/"]["bytes"] == 5


def test_distinct_keys_still_count_independently():
    c = {}
    for i in range(5):
        sp._confirm(f"raw/x/dt=1/sym=A/k{i}.json", b"z", c)
    assert c["raw/x/dt=1/sym=A/"]["n"] == 5


def test_prefixes_are_kept_separate():
    c = {}
    sp._confirm("raw/x/dt=1/sym=A/k.json", b"z", c)
    sp._confirm("raw/x/dt=1/sym=B/k.json", b"z", c)
    assert len(c) == 2


class _FakeS3:
    """Minimal paginator surface: two objects under the prefix."""
    def __init__(self, n):
        self._n = n

    def get_paginator(self, _name):
        outer = self

        class _P:
            def paginate(self, Bucket=None, Prefix=None):
                return [{"Contents": [{"Size": 10} for _ in range(outer._n)]}]
        return _P()


def test_reconcile_resets_an_inflated_counter_to_the_S3_truth():
    counters = {"raw/x/dt=1/sym=A/": {"n": 1561, "bytes": 99999}}
    fixed = sp.reconcile(_FakeS3(1560), "b", counters)
    assert counters["raw/x/dt=1/sym=A/"]["n"] == 1560
    assert fixed["raw/x/dt=1/sym=A/"] == (1561, 1560)


def test_reconcile_reports_nothing_when_already_correct():
    counters = {"raw/x/dt=1/sym=A/": {"n": 1560, "bytes": 15600}}
    assert sp.reconcile(_FakeS3(1560), "b", counters) == {}


def test_reconcile_is_NOT_automatic():
    """⚠️ A DELIBERATE REFUSAL. Self-healing on every verify would ALSO silently
    erase a GENUINE loss — if S3 really dropped an object, reconciling would
    quietly agree with the smaller number and the alarm this exists to raise
    would never fire again. **A verification that repairs itself is not a
    verification.**"""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "warehouse", "s3_push.py"),
               encoding="utf-8").read()
    assert "if do_reconcile:" in src
    assert '"--reconcile" in argv' in src
    i = src.index("short, loc, remote = verify(")
    assert "reconcile(" not in src[i:i + 400], \
        "verify must not silently repair the ledger"


def test_the_drift_signature_is_explained_not_just_flagged():
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "warehouse", "s3_push.py"),
               encoding="utf-8").read()
    assert "COUNTER DRIFT, not data loss" in src
    assert "SHORTFALL VARIES" in src, \
        "the non-drift case must be named too, or the heuristic only ever reassures"
