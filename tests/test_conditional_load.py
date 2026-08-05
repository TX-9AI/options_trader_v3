"""
tests/test_conditional_load.py — v1.0 — 2026-08-05

Guards conditional_tables v1.5's two load fixes. Both are about SILENT ZEROS,
which is the failure family that has cost this project the most.

(a) THE GLOB HAD NEVER MATCHED ANYTHING. Harvested DBs are named
    `<SYM>_trades_<date>.db`. The tool globbed `*_trades.db`, which requires the
    name to END in `_trades.db`. `excursion_report` hit the identical bug and
    documented the fix; it was never carried across.

(b) AN EMPTY LOAD REPORTED A VERDICT. On 2026-08-05 a manual run printed
    "0 closed trades / 10 session(s) · no cell separated from chance yet" while
    the conductor's run of the SAME tool found 717 trades. A null result and a
    failed load shared one sentence — in the tool the Aug 8-9 calibration fits
    are read from.

Deliberate-failure check performed when written: reverting the glob to
`*_trades.db` turns test_both_filename_spellings_load red; removing the
zero-row guard turns test_an_empty_load_refuses_instead_of_reporting_a_null red.
"""

import glob
import os
import sqlite3
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "tests", "conditional_tables.py")

COLS = ("symbol,strategy,setup_type,setup_grade,direction,regime,"
        "vix_at_entry,is_condor_leg,contracts,pnl_usd,entry_time,"
        "exit_reason,paper_trade").split(",")
VALS = ("AAA", "ORBStrategy", "ORB Long", "A", "long", "TRENDING_BULL",
        15.0, 0, 1, 50.0, "2026-08-04T14:00:00", "bos_exit", 1)
DATE = "2026-08-04"


def _db(dirpath, name):
    con = sqlite3.connect(os.path.join(dirpath, name))
    con.execute("CREATE TABLE trades (%s)" % ", ".join(f"{c} TEXT" for c in COLS))
    con.execute("INSERT INTO trades VALUES (%s)" % ",".join("?" * len(COLS)), VALS)
    con.commit()
    con.close()


def _run(root, *extra):
    return subprocess.run(
        [sys.executable, TOOL, "--since", DATE, "--trades-root", root,
         "--journal-root", tempfile.mkdtemp(),
         "--reports-dir", tempfile.mkdtemp()] + list(extra),
        capture_output=True, text=True, cwd=REPO)


def _world(names):
    root = tempfile.mkdtemp()
    day = os.path.join(root, DATE)
    os.makedirs(day)
    for n in names:
        _db(day, n)
    return root


def test_both_filename_spellings_load():
    """THE ONE THAT MATTERS. The dated spelling is what the fleet actually
    writes, and it is the one the old glob missed entirely."""
    r = _run(_world([f"AAA_trades_{DATE}.db", "BBB_trades.db"]), "--quiet")
    assert "2 closed trades" in r.stdout, (r.stdout, r.stderr[:400])


def test_the_dated_spelling_alone_is_enough():
    """A fleet that only ever writes the dated form must not read as empty —
    which is exactly what happened before v1.5."""
    r = _run(_world([f"AAA_trades_{DATE}.db"]), "--quiet")
    assert "1 closed trades" in r.stdout, (r.stdout, r.stderr[:400])


def test_the_old_glob_would_have_missed_it():
    """Pins the bug itself, so a revert is visible as a fact and not just as a
    failing assertion elsewhere."""
    root = _world([f"AAA_trades_{DATE}.db", "BBB_trades.db"])
    day = os.path.join(root, DATE)
    assert len(glob.glob(os.path.join(day, "*_trades.db"))) == 1
    assert len(glob.glob(os.path.join(day, "*_trades*.db"))) == 2


def test_an_empty_load_refuses_instead_of_reporting_a_null():
    """Dated folders present, no matching DB — a PATH/NAMING fault, not a quiet
    night. It must not print a verdict."""
    root = tempfile.mkdtemp()
    day = os.path.join(root, DATE)
    os.makedirs(day)
    open(os.path.join(day, "notes.txt"), "w").write("x")
    r = _run(root)
    assert r.returncode == 2, r.stdout
    assert "LOAD FAILED" in r.stdout
    assert "NOT a null result" in r.stdout
    assert "separated from chance" not in r.stdout, \
        "an empty corpus must not produce a statistical verdict"


def test_no_dated_folders_is_still_a_quiet_night_not_a_failure():
    """The pre-existing behaviour, deliberately preserved: an empty root before
    any session has run is rc=0. The conductor must never be marked failed by a
    quiet night — only by a load that SHOULD have found something."""
    r = _run(tempfile.mkdtemp())
    assert r.returncode == 0, r.stdout
    assert "no dated folders" in r.stdout
