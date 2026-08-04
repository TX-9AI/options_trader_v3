"""
tests/test_tcs_floor_durability.py — v1.0 — 2026-08-04

Plants worlds with a known answer and asserts the tool recovers each, the same
way tests/test_a2_partition_recovers.py and tests/test_gap_pool.py do.

Two of these guard against ways the tool could be confidently WRONG rather than
merely empty:

  - DEDUP. The readiness track scores every tick, so one impulse appears on
    hundreds of consecutive journal rows. Counting them all would report a
    sample size that does not exist and weight a long-lived impulse hundreds of
    times. The test plants 200 rows describing ONE impulse and asserts n=1.

  - CLOSE, NOT WICK. A world where price wicks through the floor and closes
    back above it must read HELD, with the penetration recorded separately. If
    the two ever merge, the durability number silently becomes a stop-out
    statistic and stops answering the question the strategy asks.

Deliberate-failure check performed when written: dropping the dedup key turns
test_one_impulse_counts_once red (n becomes 200); switching the break test from
close to low turns test_a_wick_through_the_floor_still_holds red.
"""

import json
import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "tests", "tcs_floor_durability.py")
DATE = "2026-07-30"


def _world(tmp, bars, floor=100.0, direction="long", sd=2.2, n_rows=1,
           sym="AAA", t0="14:00"):
    """bars: list of (hhmm, close, high, low) AFTER the impulse."""
    jdir = os.path.join(tmp, "signal_journal", DATE)
    odir = os.path.join(tmp, "ohlc", DATE)
    os.makedirs(jdir, exist_ok=True)
    os.makedirs(odir, exist_ok=True)

    with open(os.path.join(jdir, f"{sym}.jsonl"), "w") as fh:
        for _ in range(n_rows):
            fh.write(json.dumps({
                "ts_et": f"{DATE}T{t0}:00",
                "readiness": {"strategy": "trend_credit_spread",
                              "factors": {"floor_px": floor, "dir": direction,
                                          "sd_ratio": sd}},
            }) + "\n")

    with open(os.path.join(odir, f"{sym}_ohlc_{DATE}.csv"), "w") as fh:
        fh.write("timestamp,open,high,low,close\n")
        for hhmm, c, h, lo in bars:
            fh.write(f"{DATE}T{hhmm}:00,{c},{h},{lo},{c}\n")
    return tmp


def _run(tmp, *extra):
    p = subprocess.run(
        [sys.executable, TOOL,
         "--journal", os.path.join(tmp, "signal_journal", "*", "*.jsonl"),
         "--ohlc", os.path.join(tmp, "ohlc"),
         "--since", "2026-07-01"] + list(extra),
        capture_output=True, text=True, cwd=REPO)
    return p.stdout + p.stderr


def _held_bars():
    """Six bars that never close through 100.0 — the floor holds."""
    return [("14:0" + str(i), 101.0 + i, 102.0 + i, 100.5) for i in range(1, 7)]


def _broken_bars():
    """Closes back through the floor at 14:03."""
    return [("14:01", 101.0, 102.0, 100.5), ("14:02", 100.6, 101.0, 100.2),
            ("14:03", 99.0, 100.4, 98.5), ("14:04", 98.0, 99.5, 97.0),
            ("14:05", 97.5, 98.5, 97.0), ("14:06", 97.0, 98.0, 96.5)]


def test_a_holding_floor_reads_held():
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, _held_bars()))
        assert "floor HELD    : 1 (100.0%)" in out, out[:900]


def test_a_broken_floor_reads_broken():
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, _broken_bars()))
        assert "floor HELD    : 0 (0.0%)" in out, out[:900]


def test_one_impulse_counts_once():
    """200 journal rows, one impulse. The track scores every tick; counting the
    rows would invent a sample that does not exist."""
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, _held_bars(), n_rows=200))
        assert "impulses      : 1 distinct (deduped from 200 scored rows)" in out, \
            out[:900]


def test_a_wick_through_the_floor_still_holds():
    """Price trades to 98 but every close stays above 100 — the strike was
    threatened, not taken. Durability must say HELD and record the wick."""
    bars = [("14:01", 101.0, 102.0, 98.0), ("14:02", 100.5, 101.5, 99.0),
            ("14:03", 101.0, 102.0, 100.2), ("14:04", 101.5, 102.5, 100.9),
            ("14:05", 102.0, 103.0, 101.0), ("14:06", 102.5, 103.5, 101.5)]
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, bars))
        assert "floor HELD    : 1 (100.0%)" in out, out[:900]


def test_short_direction_is_mirrored():
    """A bear impulse fails when price closes ABOVE the floor."""
    bars = [("14:01", 99.0, 99.5, 98.0), ("14:02", 101.0, 101.5, 100.0),
            ("14:03", 102.0, 102.5, 101.0), ("14:04", 102.5, 103.0, 102.0),
            ("14:05", 103.0, 103.5, 102.5), ("14:06", 103.5, 104.0, 103.0)]
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, bars, direction="short"))
        assert "floor HELD    : 0 (0.0%)" in out, out[:900]


def test_an_impulse_with_no_forward_window_is_dropped_not_scored():
    """Armed at 15:58 there is nothing to measure. Scoring it either way would
    be a fabricated observation."""
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, [("15:59", 101.0, 101.5, 100.5)], t0="15:58"),
                   "--diagnose")
        assert "no_forward_window    1" in out, out[:900]


def test_thin_buckets_are_refused_not_reported():
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, _held_bars()))
        assert "REFUSED (under n=30)" in out, out[:900]


def test_min_sd_filters():
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(_world(tmp, _held_bars(), sd=1.0), "--min-sd", "1.5",
                   "--diagnose")
        assert "below_min_sd         1" in out, out[:900]
