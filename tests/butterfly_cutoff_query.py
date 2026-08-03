#!/usr/bin/env python3
"""
tests/butterfly_cutoff_query.py — v1.0 — 2026-08-03

BACKLOG ITEM I — "butterfly cutoff branch decision". `can_enter(is_butterfly=...)`
is unreachable: either fix the main.py call site (if a 15:00 butterfly cutoff is
ever wanted) or DELETE the branch so config and code stop disagreeing.

The item says "decision today; code post-freeze", and specifies the evidence:

    "one query on collected trades — the butterfly entry-time distribution
     (trades.db). If no fill has ever wanted the 15:00 window, delete the branch
     (loose-code principle); if late entries exist and lost, wire the call."

This is that query. It answers the decision rather than restating it, so the
decision costs a glance instead of a debate.

WHAT MAKES THIS DECIDABLE FROM DATA
    The branch exists to stop butterflies opening after 15:00 ET. Whether it is
    worth wiring depends entirely on whether butterflies ever HAVE opened then:
      - zero late entries ever      -> the branch guards nothing. DELETE it.
                                       Unreachable code that config believes in is
                                       worse than no code, because the config is
                                       lying about the system's behaviour.
      - late entries exist and LOST -> the cutoff is earning its keep. WIRE IT.
      - late entries exist and WON  -> the cutoff would have COST money. Delete
                                       the branch AND correct the config, which is
                                       the outcome nobody expects and the one most
                                       worth catching.

    That third branch is why this is a query and not a coin flip. "Wire the guard"
    is the intuitive answer and the data can say it is wrong.

HONEST LIMIT, stated because the sample is small
    Butterfly has ~3 lifetime trades in the cross-day report. A distribution over
    3 rows cannot support "late entries lose"; it CAN support "no fill has ever
    wanted the window", which is the branch the item leans toward and the only one
    a tiny n can establish. If late entries exist but are few, this prints them
    individually rather than computing a win rate over four trades.

USAGE (control box, repo root) — accepts one db or a directory of them
    python3 tests/butterfly_cutoff_query.py --db ~/day_trader_pro/trades/
    python3 tests/butterfly_cutoff_query.py --db /path/to/trades.db --cutoff 15:00

Read-only. Touches nothing.
"""

from __future__ import annotations

import argparse
import collections
import glob
import os
import re
import sqlite3
import sys

TS_RE = re.compile(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}):(\d{2})")
DEFAULT_CUTOFF = "15:00"


def _hhmm(ts):
    m = TS_RE.search(str(ts or ""))
    return f"{m.group(2)}:{m.group(3)}" if m else None


def _date(ts):
    m = TS_RE.search(str(ts or ""))
    return m.group(1) if m else "?"


def _dbs(path):
    p = os.path.expanduser(path)
    if os.path.isfile(p):
        return [p]
    if os.path.isdir(p):
        return sorted(glob.glob(os.path.join(p, "**", "*.db"), recursive=True))
    return []


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, help="a trades.db, or a dir of them")
    ap.add_argument("--cutoff", default=DEFAULT_CUTOFF)
    a = ap.parse_args(argv[1:])

    dbs = _dbs(a.db)
    if not dbs:
        print(f"No .db found at {a.db}")
        return 2

    rows, scanned, no_time = [], 0, 0
    for d in dbs:
        try:
            conn = sqlite3.connect(f"file:{d}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
            cur = conn.execute(
                "SELECT trade_id, symbol, strategy, setup_type, entry_time, "
                "exit_time, pnl_usd, status, is_butterfly FROM trades")
        except Exception:                                        # noqa: BLE001
            continue
        for t in cur:
            scanned += 1
            is_bfly = (int(t["is_butterfly"] or 0) == 1
                       or "butterfly" in str(t["strategy"] or "").lower()
                       or "butterfly" in str(t["setup_type"] or "").lower())
            if not is_bfly:
                continue
            hm = _hhmm(t["entry_time"])
            if hm is None:
                no_time += 1
                continue
            rows.append({"id": t["trade_id"], "sym": t["symbol"],
                         "date": _date(t["entry_time"]), "hhmm": hm,
                         "pnl": float(t["pnl_usd"] or 0.0),
                         "status": str(t["status"] or ""),
                         "setup": str(t["setup_type"] or "")})
        conn.close()

    print(f"scanned {scanned} trade row(s) across {len(dbs)} db(s)")
    print(f"butterfly trades found: {len(rows)}"
          + (f"   ({no_time} dropped: unparseable entry_time)" if no_time else ""))
    if not rows:
        print("\nNo butterfly trades on record at all. The 15:00 branch has never")
        print("had an opportunity to matter, so this query cannot yet distinguish")
        print("'guards nothing' from 'never tested'. NOT a decision — say so.")
        return 0

    print(f"\nENTRY-TIME DISTRIBUTION (cutoff under test: {a.cutoff} ET)")
    by_hour = collections.Counter(r["hhmm"][:2] + ":00" for r in rows)
    for h in sorted(by_hour):
        bar = "█" * by_hour[h]
        print(f"  {h}  {by_hour[h]:>3}  {bar}")

    late = [r for r in rows if r["hhmm"] >= a.cutoff]
    early = [r for r in rows if r["hhmm"] < a.cutoff]
    print(f"\n  before {a.cutoff}: {len(early)}      "
          f"at/after {a.cutoff}: {len(late)}")

    print("\n" + "=" * 62)
    if not late:
        print(f"VERDICT  NO BUTTERFLY HAS EVER OPENED AT/AFTER {a.cutoff}.")
        print("         The branch guards nothing. Per the item's loose-code")
        print("         principle: DELETE it, so config and code stop disagreeing.")
        print(f"         Evidence: {len(early)} butterfly entries, latest "
              f"{max(r['hhmm'] for r in early)} ET.")
    else:
        wins = [r for r in late if r["pnl"] > 0]
        net = sum(r["pnl"] for r in late)
        print(f"VERDICT  {len(late)} LATE ENTR{'Y' if len(late)==1 else 'IES'} "
              f"EXIST — net ${net:+.2f}, {len(wins)} winner(s).")
        print("         Listed individually below: with a sample this small a win")
        print("         rate would be theatre, so read the rows, not a percentage.")
        for r in sorted(late, key=lambda r: r["hhmm"]):
            print(f"           {r['date']} {r['hhmm']} {r['sym']:<6} "
                  f"{r['pnl']:+9.2f}  {r['setup'][:34]}")
        if net < 0:
            print("\n         Net NEGATIVE -> the cutoff would have helped. WIRE the")
            print("         call site.")
        else:
            print("\n         Net POSITIVE -> the cutoff would have COST money. This")
            print("         is the outcome nobody expects: delete the branch AND")
            print("         correct the config, rather than wiring a guard that")
            print("         the tape says is wrong.")
    print("=" * 62)
    print("Read-only. No code changed — item I says decision now, code post-freeze.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
