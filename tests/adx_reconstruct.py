#!/usr/bin/env python3
"""
tests/adx_reconstruct.py — v1.0 — 2026-08-03

BACKFILL `adx_at_entry` ON PRE-2026-07-27 TRADE ROWS by timestamp-joining
`regime_log` to `trades`. Backlog item: "Historical ADX reconstruction",
deferred at the 07-24 fix and worth doing now that the warm rebuild has landed.

WHAT THIS UNBLOCKS
    `adx_at_entry` arrived with the v-obs migration on 2026-07-24, so rows before
    that carry the schema default 0.0 rather than a real reading. Every study
    that wants to condition on trend strength at entry — and after the 08-03
    gap-day session that is a live question — silently treats those rows as
    ADX=0 or drops them. Reconstructing lengthens the usable sample without
    collecting anything new.

THE JOIN, and why nearest-PRECEDING rather than nearest
    For each trade, take the regime_log row with the LARGEST `logged_at` that is
    <= the trade's `entry_time`, same db, tolerance <= 60s. Nearest-preceding, not
    nearest-absolute: a regime row stamped AFTER the entry describes a world the
    trade could not have seen, and joining to it would leak hindsight into a
    column that is supposed to record what was known at the moment of entry. That
    is the same look-ahead error `a2_rail_drift`'s --persistent-only had, and it
    is worth not repeating.

TOLERANCE
    60s, per the item. regime_log writes on the tick cadence, so a gap wider than
    that means the nearest row genuinely describes a different moment. Rows with
    no match inside tolerance are LEFT ALONE — not filled with a best guess.

PROVENANCE — every written row is tagged
    Reconstructed values go in with `notes` gaining a `source=reconstructed`
    marker, so a later reader can always separate measured from inferred. A
    backfilled column that cannot be distinguished from a live one is a trap: the
    next person to find a surprising ADX distribution has no way to tell whether
    it is the market or the backfill.

THE VALIDATION IS FREE, and it is the reason to trust the result
    Rows since 2026-07-27 carry a REAL adx_at_entry. Run the identical join
    against those and compare the reconstruction to the recorded value. That is a
    held-out check costing nothing, and it measures the join rather than assuming
    it. `--verify-only` runs exactly that and writes nothing.
    **If the overlap does not agree, the backfill does not run.** Agreement is
    defined up front as median |error| <= 1.0 ADX point and >= 90% of overlap rows
    within 5 points — stated here before the numbers are seen.

USAGE (control box, repo root)
    python3 tests/adx_reconstruct.py --db <path> --verify-only      # check first
    python3 tests/adx_reconstruct.py --db <path> --dry-run          # what would change
    python3 tests/adx_reconstruct.py --db <path> --apply            # write

Read-only unless --apply. Never touches a row that already has a real value.
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta

# The v-obs migration that added adx_at_entry. Rows entered on or after this
# carry a real reading and are the held-out overlap.
REAL_FROM = "2026-07-27"
TOLERANCE_S = 60

# Pre-registered agreement bar — stated before the overlap is measured.
MAX_MEDIAN_ERR = 1.0
MIN_WITHIN_5 = 0.90

TS_RE = re.compile(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}):(\d{2}):(\d{2})")


def _parse(ts):
    m = TS_RE.search(str(ts or ""))
    if not m:
        return None
    d = m.group(1)
    return datetime(int(d[:4]), int(d[5:7]), int(d[8:10]),
                    int(m.group(2)), int(m.group(3)), int(m.group(4)))


def _median(xs):
    if not xs:
        return 0.0
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def _load_regime(conn):
    """(datetime, adx) sorted ascending. regime_log has no symbol column, so the
    join is per-DB — which is correct, because each box's db holds exactly one
    symbol's rows."""
    out = []
    for logged_at, adx in conn.execute(
            "SELECT logged_at, adx FROM regime_log WHERE adx IS NOT NULL"):
        t = _parse(logged_at)
        if t is not None:
            out.append((t, float(adx)))
    out.sort(key=lambda r: r[0])
    return out


def _nearest_preceding(rows, t, tol_s):
    """Largest logged_at <= t, within tolerance. Binary search on a sorted list.

    PRECEDING ONLY: a regime row stamped after the entry describes a world the
    trade could not have seen.
    """
    lo, hi = 0, len(rows) - 1
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if rows[mid][0] <= t:
            best = rows[mid]
            lo = mid + 1
        else:
            hi = mid - 1
    if best is None:
        return None
    if (t - best[0]) > timedelta(seconds=tol_s):
        return None
    return best[1]


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, help="path to a trades.db")
    ap.add_argument("--tolerance", type=int, default=TOLERANCE_S)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--verify-only", action="store_true",
                   help="run the held-out overlap check and stop")
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv[1:])

    path = os.path.expanduser(a.db)
    if not os.path.isfile(path):
        print(f"No db at {path}")
        return 2
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row

    regime = _load_regime(conn)
    if not regime:
        print("regime_log has no usable rows — nothing to join against.")
        return 2
    print(f"db {os.path.basename(path)} | regime_log rows {len(regime)} "
          f"({regime[0][0].date()} .. {regime[-1][0].date()})")

    trades = list(conn.execute(
        "SELECT trade_id, entry_time, adx_at_entry, notes FROM trades"))
    print(f"trades {len(trades)}")

    # ── the held-out overlap check, always run ──────────────────────────────
    errs, within5 = [], 0
    overlap = 0
    for t in trades:
        et = _parse(t["entry_time"])
        if et is None or et.strftime("%Y-%m-%d") < REAL_FROM:
            continue
        real = float(t["adx_at_entry"] or 0.0)
        if real <= 0:
            continue                      # nothing to compare against
        got = _nearest_preceding(regime, et, a.tolerance)
        if got is None:
            continue
        overlap += 1
        e = abs(got - real)
        errs.append(e)
        if e <= 5.0:
            within5 += 1

    print(f"\nHELD-OUT OVERLAP (rows since {REAL_FROM} with a real value)")
    if overlap == 0:
        print("  REFUSED — no overlap rows. The join cannot be validated on this")
        print("  db, so nothing is written. Run against a db that spans the")
        print("  migration date.")
        return 2
    med = _median(errs)
    frac = within5 / overlap
    print(f"  n={overlap}   median |error| {med:.2f} ADX   "
          f"within 5 pts {frac:.0%}")
    ok = med <= MAX_MEDIAN_ERR and frac >= MIN_WITHIN_5
    print(f"  bar (pre-registered): median <= {MAX_MEDIAN_ERR}, "
          f">= {MIN_WITHIN_5:.0%} within 5   ->  {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("\n  The reconstruction does NOT reproduce values we already know.")
        print("  Backfilling on this evidence would write plausible-looking")
        print("  numbers that are wrong, which is worse than leaving 0.0 —")
        print("  a zero is obviously missing; a wrong ADX is not. Nothing written.")
        return 1
    if a.verify_only:
        print("\n--verify-only: stopping here, nothing written.")
        return 0

    # ── the backfill ────────────────────────────────────────────────────────
    to_write, no_match, already = [], 0, 0
    for t in trades:
        et = _parse(t["entry_time"])
        if et is None or et.strftime("%Y-%m-%d") >= REAL_FROM:
            continue
        if float(t["adx_at_entry"] or 0.0) > 0:
            already += 1
            continue                      # never overwrite a real value
        got = _nearest_preceding(regime, et, a.tolerance)
        if got is None:
            no_match += 1
            continue
        to_write.append((t["trade_id"], got, t["notes"] or ""))

    print(f"\nBACKFILL (rows before {REAL_FROM})")
    print(f"  would write   {len(to_write)}")
    print(f"  no match <={a.tolerance}s  {no_match}   (left at 0.0, NOT guessed)")
    print(f"  already real  {already}   (never overwritten)")

    if a.apply and to_write:
        cur = conn.cursor()
        for tid, adx, notes in to_write:
            tag = "source=reconstructed"
            newnotes = notes if tag in notes else (notes + " " + tag).strip()
            cur.execute(
                "UPDATE trades SET adx_at_entry=?, notes=? WHERE trade_id=?",
                (adx, newnotes, tid))
        conn.commit()
        print(f"  ✅ wrote {len(to_write)} row(s), each tagged "
              f"source=reconstructed")
    elif to_write:
        print("  (dry-run — nothing written; re-run with --apply)")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
