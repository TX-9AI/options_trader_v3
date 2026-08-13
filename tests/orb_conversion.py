#!/usr/bin/env python3
"""
tests/orb_conversion.py — v1.0 — 2026-08-13

DID ORB STOP FIRING BECAUSE THE SETUPS STOPPED, OR BECAUSE A GATE STARTED?

ENG.1 measured the single largest number in the project: ORB earned **$5,966
per session** before the 2026-07-27 confluence excavation and **$1,551 after**
— 533 trades across 10 sessions falling to 63 across 7, while PER-TRADE value
ROSE ($111.9 -> $172.4) and never-favorable IMPROVED (38% -> 22%). The engine
did not get worse at picking ORBs. It got better, and it nearly stopped.

~$4,400 per session is the gap. That is larger than every item on the entry
punch list combined, so it is worth knowing which of two things happened:

  A. FEWER SETUPS. Mid-July trended; a trending tape produces more breakouts
     without producing more total movement. If breaks fell as hard as entries,
     there is nothing to restore and the ORB gap is July's tape.
  B. THE SAME SETUPS, FEWER ENTRIES. If breaks held and CONVERSION collapsed,
     a gate is eating them and the gate is recoverable.

⚠️ AVAILABLE MOVEMENT DOES NOT SETTLE THIS. ENG.1 measured it at 0.322 vs
   0.344 — flat — but that statistic is DIRECTIONLESS by construction. A tape
   can offer identical movement with far fewer clean range breaks. Do not read
   the flat move figure as evidence that setup supply was constant; it is not
   evidence either way, which is exactly why this tool exists.

────────────────────────────────────────────────────────────────────────────
THE COUNT, AND WHAT EACH SIDE OF IT IS
────────────────────────────────────────────────────────────────────────────
BREAKS   `retest_check` events, emitted by orb_engine while it evaluates a
         retest. Their existence means a break registered and the engine was
         working the setup. Deduplicated to (symbol, date, direction, attempt)
         so a break evaluated over many ticks counts ONCE — the tick-inflation
         trap that made the sweep opportunity audit read 4,303 "opportunities"
         from a handful of real events.
ENTRIES  ORBStrategy rows in trades.db for the same session.

CONVERSION = entries / distinct break-attempts.

⚠️ THE JOURNAL IS THE WEAK LEG AND THE TOOL SAYS SO PER SESSION. It covers
   2026-07-20 onward, and `retest_check` may itself postdate some of that. A
   session with trades but no journal coverage is reported as UNCOVERED and
   excluded from the conversion rate rather than counted as zero breaks —
   counting missing telemetry as absent setups would invent finding A.

READ-ONLY. stdlib only. Writes nothing, touches no fleet, no live path.

USAGE (control)
    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/orb_conversion.py
    ... --split 2026-07-28
"""

import argparse
import collections
import glob
import json
import os
import sqlite3
import sys

DTP = os.path.expanduser("~/day_trader_pro")
TRADES = os.path.join(DTP, "trades")
ARCHIVE = os.path.join(TRADES, "_archive_pre_2026-07-23")
JOURNAL = os.path.join(DTP, "signal_journal")


def sessions_map():
    out = {}
    for root in (ARCHIVE, TRADES):
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            if len(name) == 10 and name[4] == "-":
                out[name] = os.path.join(root, name)
    return out


def breaks_for(date):
    """Distinct ORB break-attempts, and whether the journal covered this date.

    Returns (n_attempts, covered, n_events). `covered` is False when there is
    no journal directory or no files — which is NOT the same as zero breaks.
    """
    day_dir = os.path.join(JOURNAL, date)
    if not os.path.isdir(day_dir):
        return 0, False, 0
    paths = sorted(glob.glob(os.path.join(day_dir, "*.jsonl")))
    if not paths:
        return 0, False, 0
    seen, events = set(), 0
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if "retest_check" not in line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                if r.get("event") != "retest_check":
                    continue
                events += 1
                orb = r.get("orb") or {}
                # Dedupe to the ATTEMPT, not the tick. One break evaluated over
                # 200 ticks is one setup, not 200 opportunities.
                seen.add((r.get("symbol"), str(orb.get("direction") or ""),
                          orb.get("attempt")))
    return len(seen), True, events


def orb_entries(day_dir):
    n = 0
    for path in sorted(glob.glob(os.path.join(day_dir, "*.db"))):
        try:
            conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            for (c,) in conn.execute(
                    "SELECT COUNT(*) FROM trades WHERE strategy='ORBStrategy'"
                    " AND status='closed'"):
                n += c
            conn.close()
        except Exception:                                      # noqa: BLE001
            continue
    return n


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="2026-07-28",
                    help="FIRST session of ARM B (post-excavation)")
    ap.add_argument("--b-end", default="2026-08-04",
                    help="last ARM B session — do NOT cross 2026-08-05")
    a = ap.parse_args(argv[1:])

    smap = sessions_map()
    if not smap:
        print(f"no dated trade folders under {TRADES}")
        return 0

    rows = []
    for date in sorted(smap):
        if date > a.b_end:
            continue
        arm = "A" if date < a.split else "B"
        nb, covered, nev = breaks_for(date)
        ne = orb_entries(smap[date])
        rows.append((date, arm, nb, ne, covered, nev))

    print("=" * 78)
    print("  ORB CONVERSION — did the setups stop, or did a gate start?")
    print(f"  split: arm B begins {a.split}   |   arm B ends {a.b_end}")
    print("=" * 78)
    print(f"\n  {'date':12}{'arm':>4}{'breaks':>8}{'entries':>9}{'conv':>8}"
          f"{'retest evts':>13}   journal")
    tot = collections.defaultdict(lambda: [0, 0, 0, 0])   # br, en, sess, cov
    for date, arm, nb, ne, covered, nev in rows:
        conv = (f"{100.0 * ne / nb:.0f}%" if (covered and nb) else "—")
        print(f"  {date:12}{arm:>4}{(nb if covered else 0):>8}{ne:>9}{conv:>8}"
              f"{nev:>13}   {'ok' if covered else 'UNCOVERED'}")
        t = tot[arm]
        t[2] += 1
        if covered:
            t[0] += nb
            t[1] += ne
            t[3] += 1

    print(f"\n  {'-' * 74}")
    print(f"  {'arm':6}{'sessions':>10}{'covered':>9}{'breaks':>8}"
          f"{'entries':>9}{'br/sess':>9}{'ent/sess':>10}{'conv':>7}")
    for arm in ("A", "B"):
        br, en, sess, cov = tot[arm]
        if not sess:
            continue
        print(f"  {arm:6}{sess:>10}{cov:>9}{br:>8}{en:>9}"
              f"{(br / cov if cov else 0):>9.1f}{(en / cov if cov else 0):>10.1f}"
              f"{(f'{100.0 * en / br:.0f}%' if br else '—'):>7}")

    a_cov, b_cov = tot["A"][3], tot["B"][3]
    print()
    if not a_cov or not b_cov:
        print("  ⚠️ ONE ARM HAS NO JOURNAL COVERAGE. The break count for it is")
        print("     UNMEASURED, not zero. This tool cannot answer the question")
        print("     on this data — absent measurement, not a null. The entries")
        print("     column is still valid and comes from trades.db.")
        print("     Fallback: ORB entries per session per arm above is a real")
        print("     number; what is missing is the DENOMINATOR.")
    else:
        print("  READING IT: if br/sess held roughly flat and conv fell, a GATE")
        print("  is eating the setups and the ORB gap is recoverable. If br/sess")
        print("  fell in step with ent/sess, the SETUPS stopped and the gap is")
        print("  July's tape — nothing to restore.")
        print("  ⚠️ Entries are counted from trades.db and breaks from the")
        print("     journal. A session where the box traded but journalling was")
        print("     off would understate breaks and overstate the gate.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
