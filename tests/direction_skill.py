#!/usr/bin/env python3
"""
tests/direction_skill.py — v1.0 — 2026-08-19   (NULL.1)

DOES THE CLASSIFIER PICK DIRECTION BETTER THAN A COIN FLIP?

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/direction_skill.py

────────────────────────────────────────────────────────────────────────────
THE HYPOTHESIS UNDER TEST (operator, 2026-08-19)
────────────────────────────────────────────────────────────────────────────
> *"entries on a 50% randomized long/short entry would be equally or more
> successful than what we have."*

⚠️ **WHY THIS IS THE RIGHT TEST AND "NEGATE THE P&L" IS NOT.** Flipping an
options trade's direction does NOT flip its P&L sign: a long call and a long put
BOTH bleed theta when price does not move, so a randomly-directed book averages
to LOSSES, not to zero. Comparing the real book against its own negation would
flatter the coin and prove nothing.

The claim reduces to something cleaner and decisive: **does the engine pick the
correct SIDE more often than 50%?** If it does not, the regime layer contributes
nothing to entry direction, and whatever the book earns comes from the exits and
from ORB's self-validating geometry — not from the classifier.

────────────────────────────────────────────────────────────────────────────
METHOD
────────────────────────────────────────────────────────────────────────────
For each CLOSED directional trade: read `direction`/`option_side` and
`underlying_entry`, find the underlying at `exit_time` from the banked OHLC
tape, and ask whether price moved the way the trade was pointed.

  · **ORB EXCLUDED** (operator's instruction). ORB is deliberately
    regime-agnostic — break-and-retest geometry that never consults the
    classifier — so including it would credit the regime engine with ORB's
    record. **That exclusion is the whole point: it isolates the layer under
    test.**
  · **NEUTRAL STRUCTURES EXCLUDED.** Condors and butterflies have no side to be
    right about.
  · **EXITS ARE THE CONTROL.** They are untouched here and are measured
    winners (`orb_trail_stop` 95%/107, `theta_bleed` 100%/107,
    `continuation_trail` 85%/149). This asks ONLY whether the ENTRY direction
    carried information.

⚠️ WHAT A NULL RESULT MEANS, STATED BEFORE THE RUN: direction accuracy
statistically indistinguishable from 50% does NOT mean the system loses money —
the exits can and do rescue badly-pointed trades. It means **the classifier is
not the reason it makes any**, and a coin would serve the entry equally well.
⚠️ AND A POSITIVE RESULT IS NOT VINDICATION EITHER: 53% with a wide interval on
n=200 is a coin with a good week.
"""

import argparse
import bisect
import collections
import csv
import glob
import math
import os
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DTP = os.path.expanduser("~/day_trader_pro")
TRADES = os.path.join(DTP, "trades", "*", "*_trades_*.db")
OHLC = os.path.join(DTP, "ohlc")

EXCLUDE_STRATEGIES = {"ORBStrategy"}
NEUTRAL = ("condor", "butterfly", "iron")


def _wilson(k, n):
    if n == 0:
        return (0.0, 1.0)
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _load_tape(day, sym, root=OHLC):
    for pat in (f"{sym}_ohlc_{day}.csv", f"{sym.upper()}_ohlc_{day}.csv"):
        p = os.path.join(root, day, pat)
        if os.path.exists(p):
            ts, px = [], []
            with open(p) as fh:
                for r in csv.DictReader(fh):
                    try:
                        ts.append(r["timestamp"][11:19])
                        px.append(float(r["close"]))
                    except Exception:                          # noqa: BLE001
                        continue
            return ts, px
    return None, None


def _px_at(ts, px, hhmmss):
    if not ts:
        return None
    i = bisect.bisect_right(ts, hhmmss) - 1
    return px[i] if 0 <= i < len(px) else None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--trades", default=TRADES)
    ap.add_argument("--since", default="2026-07-13")
    ap.add_argument("--ohlc", default=OHLC,
                    help="OHLC root; the exit-side underlying comes from here")
    a = ap.parse_args(argv[1:])

    rows = []
    tapes = {}
    for db in sorted(glob.glob(os.path.expanduser(a.trades))):
        if "_archive" in db or db.endswith(".bak"):
            continue
        import re
        m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(db))
        if not m or m.group(1) < a.since or m.group(1) == "2026-08-14":
            continue                    # 08-14 is identity-chain polluted
        day = m.group(1)
        try:
            con = sqlite3.connect("file:" + db + "?mode=ro", uri=True)
            con.row_factory = sqlite3.Row
            recs = con.execute(
                "SELECT * FROM trades WHERE status='closed'").fetchall()
        except Exception:                                      # noqa: BLE001
            continue
        for r in recs:
            r = dict(r)
            strat = str(r.get("strategy") or "")
            setup = str(r.get("setup_type") or "").lower()
            if strat in EXCLUDE_STRATEGIES:
                continue
            if any(k in setup or k in strat.lower() for k in NEUTRAL):
                continue
            side = str(r.get("option_side") or "").lower()
            if side not in ("call", "put"):
                continue
            ue = r.get("underlying_entry")
            xt = str(r.get("exit_time") or "")
            sym = str(r.get("symbol") or "")
            if not ue or len(xt) < 19 or not sym:
                continue
            key = (day, sym)
            if key not in tapes:
                tapes[key] = _load_tape(day, sym, a.ohlc)
            ts, px = tapes[key]
            ux = _px_at(ts, px, xt[11:19])
            if ux is None:
                continue
            try:
                ue = float(ue)
            except Exception:                                  # noqa: BLE001
                continue
            if ue <= 0:
                continue
            move = (ux - ue) / ue
            right = (move > 0) if side == "call" else (move < 0)
            rows.append({"day": day, "sym": sym, "strategy": strat,
                         "side": side, "move_pct": 100.0 * move,
                         "right": right, "pnl": r.get("pnl_usd") or 0.0})

    if not rows:
        print("no directional non-ORB trades with a usable tape join.")
        print("  ABSENT MEASUREMENT, not a null.")
        return 1

    n = len(rows)
    k = sum(1 for r in rows if r["right"])
    lo, hi = _wilson(k, n)
    print("=" * 80)
    print("DIRECTION SKILL — does the classifier beat a coin on SIDE?")
    print(f"  {n} closed directional trade(s), ORB and neutral structures EXCLUDED")
    print(f"  {len({r['day'] for r in rows})} session(s)")
    print("=" * 80)
    print(f"\n  correct side: {k}/{n} = {100.0*k/n:.1f}%")
    print(f"  95% CI: [{100*lo:.1f}%, {100*hi:.1f}%]")
    print(f"  coin flip: 50.0%")
    if lo > 0.50:
        v = "✅ BEATS THE COIN — the interval excludes 50%."
    elif hi < 0.50:
        v = "🔴 WORSE THAN A COIN — the interval is entirely BELOW 50%."
    else:
        v = ("❌ INDISTINGUISHABLE FROM A COIN — 50% sits inside the interval. "
             "The classifier is not choosing direction.")
    print(f"\n  {v}")

    print(f"\n  BY STRATEGY")
    print(f"    {'strategy':26}{'n':>6}{'right%':>9}{'95% CI':>18}{'net $':>10}")
    by = collections.defaultdict(list)
    for r in rows:
        by[r["strategy"]].append(r)
    for s_, v_ in sorted(by.items(), key=lambda kv: -len(kv[1])):
        kk = sum(1 for x in v_ if x["right"])
        l2, h2 = _wilson(kk, len(v_))
        net = sum(float(x["pnl"] or 0) for x in v_)
        print(f"    {s_[:25]:26}{len(v_):>6}{100.0*kk/len(v_):>8.1f}%"
              f"   [{100*l2:>4.0f}%,{100*h2:>4.0f}%]{net:>10.0f}")

    print(f"\n  BY SIDE  (a directional bias shows here, not in the total)")
    for sd in ("call", "put"):
        v_ = [r for r in rows if r["side"] == sd]
        if not v_:
            continue
        kk = sum(1 for x in v_ if x["right"])
        l2, h2 = _wilson(kk, len(v_))
        print(f"    {sd:8}{len(v_):>6}{100.0*kk/len(v_):>8.1f}%"
              f"   [{100*l2:.0f}%, {100*h2:.0f}%]")

    print("\n  ⚠️ HOW TO READ A NULL. Direction accuracy indistinguishable from")
    print("     50% does NOT mean the system loses money — the EXITS rescue")
    print("     badly-pointed trades and they are measured winners. It means the")
    print("     CLASSIFIER IS NOT THE REASON IT MAKES ANY, and a coin would")
    print("     serve the entry equally well.")
    print("  ⚠️ AND A POSITIVE IS NOT VINDICATION: 53% with a wide interval on")
    print("     n=200 is a coin with a good week. Read the CI, not the point.")
    print("  ⚠️ ORB IS EXCLUDED BY INSTRUCTION — it never consults the regime")
    print("     engine, so including it would credit the classifier with ORB's")
    print("     record. That exclusion is what isolates the layer under test.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
