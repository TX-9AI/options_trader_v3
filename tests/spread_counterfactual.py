#!/usr/bin/env python3
"""
tests/spread_counterfactual.py — v1.2 — 2026-08-13   (TC.7)

v1.2 — 2026-08-13 — OOM-KILLED ON THE FIRST WORKING RUN. Bounded work, UNBOUNDED
        MEMORY. v1.1 cached every parsed chain snapshot for every (date, symbol)
        it touched and never evicted: ~78 snapshots x ~120 contracts x 13 fields
        as Python dicts, times a couple of hundred symbol-days, resident at once.
        The kernel killed it before a single row printed.
        THE FIX IS SCOPE, NOT CLEVERNESS — process ONE SYMBOL-DAY AT A TIME:
        group the population by (date, symbol), collect that group's target
        minutes FIRST, stream the .jsonl.gz once keeping ONLY snapshots within
        the match window of a target, price the group, then drop it. Peak
        residency is one symbol-day instead of all of them, and the file is
        still read exactly once.
        ⚠️ WHY NO FIXTURE CAUGHT THIS: the fixture is one symbol, one date, one
        chain file. **A single-symbol-day fixture cannot exercise a cache that
        only grows across symbol-days** — the same blind spot as v1.0's
        single-snapshot fixture missing the sort tie, one level up. Scale
        failures need a fixture with scale, and this one still does not have
        one; the guard is the restructure, not a test.
        Also reports peak group size so a pathological symbol-day is visible.

v1.1 — 2026-08-13 — CRASH FIX: `sorted(snaps)` on `(minute, dict)` tuples.
        When two snapshots share a minute Python falls through to comparing the
        DICTS and raises `TypeError: '<' not supported between instances of
        'dict' and 'dict'`. Now sorted on the KEY ONLY.
        ⚠️ WHY THE FIXTURE MISSED IT, and this is the reusable part: the fixture
        wrote ONE snapshot per symbol-day, so the tuple comparator was never
        reached — a single-element list cannot exercise a sort. A fixture that
        cannot produce a TIE cannot test a tie-break. The fixture now writes two
        snapshots at the SAME minute, which reproduces the crash against v1.0.

WOULD THESE TRADES HAVE PAID AS SHORT VERTICALS INSTEAD OF LONG PREMIUM?

Operator, 2026-08-13: *"I think those opportunities would have fared better as
vertical spreads instead of paying long premium to chase spent moves."* And,
correcting the statistic this tool was nearly built on: **"With a credit spread,
it doesn't matter that it turned against me as long as it doesn't breach."**

────────────────────────────────────────────────────────────────────────────
THE POPULATION, AND WHY IT IS THIS ONE
────────────────────────────────────────────────────────────────────────────
`factor_sweep --setup-type trend_continuation_handoff` split by
`reg.conviction` found ONE band carrying more than the whole strategy's loss:

    conviction EXACTLY 1.00, handoff path — n=128, 41%% win, **-$52/trade,
    -$6,623** — against ContinuationStrategy's total of -$6,351.

The same peg through the STANDALONE path is n=128, 50%% win, **+$1/trade**. Same
conviction, same count, opposite outcome. The handoff's licence is that the
label is UNRELIABLE after a runaway; when the label is also pegged at maximum
you have the runaway AND total regime confidence, i.e. the move is finished and
obvious. That is the population this prices a counterfactual for.

────────────────────────────────────────────────────────────────────────────
TERMINAL ONLY. THIS IS THE WHOLE METHOD AND IT IS THE OPERATOR'S CORRECTION.
────────────────────────────────────────────────────────────────────────────
The first design counted MAXIMUM ADVERSE EXCURSION against candidate short
strikes. **That is wrong**, and it is the same error `tcs_floor_durability` v1.1
was rewritten to fix: MAE counts a TOUCH, a defined-risk spread held to expiry
only loses on ACCEPTANCE. On the impulse population that distinction was worth
everything — intraday held 14.7%%, terminal OK **56.1%%**, **41.4%% RECOVERED**.

**Every trade that dipped through a candidate short strike and came back is a
LOSS for the long and a WIN for the spread.** An MAE-based test measures that
entire population out of existence. So this reports INTRADAY / TERMINAL /
RECOVERED separately and never merges them, exactly as the durability tool does.

⚠️ "Never favorable" is IRRELEVANT here. It says the LONG never went green. For
   a short vertical sold beneath the move that is neutral-to-good.

GEOMETRY, the one place direction still bites: a bull handoff BUYS CALLS, so the
credit equivalent (the operator's "vertical spread at the floor of the Move")
SELLS A PUT SPREAD BENEATH ENTRY. Price moving against the long is price moving
TOWARD the short strike — so the adverse side is the side that matters, but only
at the close, never on the way.

────────────────────────────────────────────────────────────────────────────
⚠️ THE ASYMMETRY. READ THIS BEFORE READING THE TABLE.
────────────────────────────────────────────────────────────────────────────
The LONG side is REAL: real fills, real slippage, real management — stops fired,
trails engaged, positions closed early. The SPREAD side is MODELLED: archived
quotes, held to expiry, no management, no early assignment, no commission, and
a fill at the posted bid.

**That tilts the comparison toward the counterfactual by construction.** The gap
has to be LARGE to survive it. A narrow win for the spread is a NULL, not a
result, and this tool says so rather than leaving it to the reader.

READ-ONLY. stdlib only. Imports the join from `scorer_backtest` and the pricing
from `credit_edge` — ONE implementation of each, never a third.

USAGE (control)
    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/spread_counterfactual.py --since 2026-07-20
    ... --setup-type trend_continuation_standalone      # the control arm
    ... --conv-min 0.0 --conv-max 1.01                  # the whole path
"""

import argparse
import collections
import csv
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.scorer_backtest import (load_scored, load_trades,                # noqa: E402
                                   JOIN_TOL_S, JOURNAL)
from tests.credit_edge import (CHAINS, ohlc_root, price_vertical,           # noqa: E402
                               settle_loss, OFFSETS, MIN_CREDIT)

MIN_N = 30


def session_path(date, root):
    """{symbol: [(minute, high, low, close)]} for the whole session."""
    out = {}
    if not root:
        return out
    for path in sorted(glob.glob(os.path.join(root, date, "*.csv"))):
        sym = os.path.basename(path).split("_")[0]
        bars = []
        try:
            with open(path, encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    t = r.get("timestamp") or r.get("time") or ""
                    try:
                        m = int(t[11:13]) * 60 + int(t[14:16])
                        bars.append((m, float(r["high"]), float(r["low"]),
                                     float(r["close"])))
                    except Exception:                          # noqa: BLE001
                        continue
        except Exception:                                      # noqa: BLE001
            continue
        if bars:
            out[sym] = sorted(bars)
    return out


def load_group_chain(date, sym, minutes, window=10):
    """Snapshots for ONE symbol-day, keeping only those near a target minute.

    v1.2 — the memory fix. `minutes` is every entry minute in this group, known
    before the file is opened, so the stream can discard the ~95%% of snapshots
    no trade needs instead of parsing them into a cache that never shrinks.
    Returns [(minute, {(side, strike): contract})] sorted by minute.
    """
    path = os.path.join(CHAINS, date, f"{sym}.jsonl.gz")
    if not os.path.isfile(path) or not minutes:
        return []
    import gzip
    keep = []
    try:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                ts = r.get("ts_et") or ""
                if len(ts) < 16 or not r.get("underlying"):
                    continue
                try:
                    m = int(ts[11:13]) * 60 + int(ts[14:16])
                except Exception:                              # noqa: BLE001
                    continue
                if min(abs(m - t) for t in minutes) > window:
                    continue                    # nothing in this group wants it
                rows = {}
                for c in (r.get("contracts") or []):
                    t = str(c.get("type") or "").lower()
                    t = "call" if t.startswith("c") else (
                        "put" if t.startswith("p") else "")
                    if not t:
                        continue
                    try:
                        rows[(t, round(float(c.get("strike")), 4))] = c
                    except Exception:                          # noqa: BLE001
                        continue
                if rows:
                    keep.append((m, rows))
    except Exception:                                          # noqa: BLE001
        return []
    # KEY ONLY (v1.1) — bare-tuple sort falls through to the dict on a tie.
    keep.sort(key=lambda x: x[0])
    return keep


def nearest(snaps, minute, window=10):
    if not snaps:
        return None
    best = min(snaps, key=lambda s: abs(s[0] - minute))
    return best[1] if abs(best[0] - minute) <= window else None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-07-20")
    ap.add_argument("--strategy", default="ContinuationStrategy")
    ap.add_argument("--setup-type", default="trend_continuation_handoff")
    ap.add_argument("--conv-min", type=float, default=1.0,
                    help="regime conviction floor (default 1.0 = the pegged "
                         "band that carries the whole loss)")
    ap.add_argument("--conv-max", type=float, default=1.01)
    ap.add_argument("--width", type=float, default=5.0)
    ap.add_argument("--min-n", type=int, default=MIN_N)
    a = ap.parse_args(argv[1:])

    if not os.path.isdir(JOURNAL):
        print(f"no journal at {JOURNAL}")
        return 0
    dates = sorted(d for d in os.listdir(JOURNAL)
                   if len(d) == 10 and d >= a.since)
    root = ohlc_root()

    # ── join, reusing scorer_backtest's implementation ──────────────────────
    pop, seen, unmatched = [], set(), 0
    for date in dates:
        sc = load_scored(date)
        idx = collections.defaultdict(list)
        for s in sc:
            idx[(s["sym"], s["strategy"])].append(s)
        for t in load_trades(date, seen):
            if t["strategy"] != a.strategy:
                continue
            if a.setup_type and t["setup_type"] != a.setup_type:
                continue
            best, bd = None, JOIN_TOL_S + 1
            for s in idx.get((t["sym"], t["strategy"])) or []:
                d = abs((s["ts"] - t["ts"]).total_seconds())
                if d < bd:
                    best, bd = s, d
            if best is None or bd > JOIN_TOL_S:
                unmatched += 1
                continue
            conv = ((best.get("raw") or {}).get("regime") or {}).get("conviction")
            if conv is None or not (a.conv_min <= float(conv) < a.conv_max):
                continue
            pop.append({**t, "date": date, "conv": float(conv)})

    print("=" * 84)
    print("  SPREAD COUNTERFACTUAL (TC.7) — long premium vs a short vertical")
    print(f"  {a.strategy} / {a.setup_type or 'ALL'} / conviction "
          f"[{a.conv_min}, {a.conv_max})   width {a.width:g}")
    print(f"  {len(dates)} session(s) since {a.since}   population {len(pop)}"
          f"   unmatched-to-journal {unmatched}")
    print("=" * 84)
    if not pop:
        print("\n  empty population. ABSENT MEASUREMENT, not a null.")
        return 0

    cells = collections.defaultdict(list)
    sym_days, no_chain, no_tape, no_entry = set(), 0, 0, 0
    long_pnl = 0.0
    peak_group = 0

    # v1.2 — ONE SYMBOL-DAY AT A TIME. Group first, so the chain file for a
    # group is opened once, filtered to that group's minutes, and DROPPED before
    # the next group is touched. Peak residency is one symbol-day.
    groups = collections.defaultdict(list)
    for t in pop:
        groups[(t["date"], t["sym"])].append(t)

    for (date, sym), grp in sorted(groups.items()):
        usable = []
        for t in grp:
            raw = t.get("raw") or {}
            try:
                entry = float(raw.get("underlying_entry") or 0)
            except Exception:                                  # noqa: BLE001
                entry = 0.0
            direction = str(raw.get("direction") or "").lower()
            if entry <= 0 or direction not in ("long", "short"):
                no_entry += 1
                continue
            usable.append((t, entry, direction,
                           t["ts"].hour * 60 + t["ts"].minute))
        if not usable:
            continue

        bars = (session_path(date, root) or {}).get(sym) or []
        if not bars:
            no_tape += len(usable)
            continue

        snaps = load_group_chain(date, sym, [u[3] for u in usable])
        peak_group = max(peak_group, len(snaps))

        for t, entry, direction, minute in usable:
            rows = nearest(snaps, minute)
            if not rows:
                no_chain += 1
                continue
            fwd = [b for b in bars if b[0] >= minute]
            if len(fwd) < 2:
                no_tape += 1
                continue
            term_close = fwd[-1][3]
            long_pnl += t["pnl"]
            sym_days.add((date, sym))

            # THE ADVERSE SIDE. A long (bull) handoff is replaced by a PUT
            # spread BENEATH entry; a short by a CALL spread above it.
            side = "put" if direction == "long" else "call"
            strikes = sorted({k[1] for k in rows})
            for off in OFFSETS:
                target = entry * (1 - off) if side == "put" else entry * (1 + off)
                cand = [k for k in strikes
                        if (k <= target if side == "put" else k >= target)]
                if not cand:
                    continue
                k = max(cand) if side == "put" else min(cand)
                pv = price_vertical(rows, side, k, a.width)
                if pv is None:
                    continue
                credit, ks, kl = pv
                touched = any((b[2] < ks) if side == "put" else (b[1] > ks)
                              for b in fwd)
                loss = settle_loss(side, ks, kl, term_close, a.width)
                cells[off].append((credit, loss, touched))
        snaps = None                      # explicit — the whole point of v1.2

    print(f"\n  priced {sum(len(v) for v in cells.values()):,} spreads over "
          f"{len(sym_days)} SYMBOL-DAYS — read every n against that, not itself.")
    print(f"  skipped — no chain within 10 min {no_chain} · no tape {no_tape} ·"
          f" no entry/direction {no_entry}")
    print(f"  peak snapshots resident for any one symbol-day: {peak_group}"
          f"  ({len(groups)} symbol-day groups processed one at a time)")
    print(f"\n  ACTUAL LONG RESULT on the same trades: net ${long_pnl:+,.0f}"
          f"  ({len(sym_days)} symbol-days)")

    if not cells:
        print("\n  nothing priced. ABSENT MEASUREMENT, not a null.")
        return 0

    print(f"\n  {'offset':>8}{'n':>7}{'touched':>9}{'terminal OK':>13}"
          f"{'RECOVERED':>11}{'credit':>9}{'E[loss]':>9}{'EV/spread':>11}")
    for off in OFFSETS:
        g = cells.get(off) or []
        if not g:
            continue
        n = len(g)
        safe = sum(1 for c, l, tch in g if l <= 0.0)
        tch_n = sum(1 for c, l, tch in g if tch)
        rec = sum(1 for c, l, tch in g if tch and l <= 0.0)
        cr = sum(c for c, _, _ in g) / n
        el = sum(l for _, l, _ in g) / n
        flag = "" if n >= a.min_n else "  <- UNDERPOWERED"
        print(f"  {off*100:>7.2f}%{n:>7}{100.0*tch_n/n:>8.0f}%"
              f"{100.0*safe/n:>12.0f}%"
              f"{(f'{100.0*rec/tch_n:.0f}%' if tch_n else '—'):>11}"
              f"{cr:>9.2f}{el:>9.2f}{cr-el:>+11.2f}{flag}")

    print("\n  RECOVERED = of the spreads price TOUCHED through, the share that")
    print("  still closed safe. THAT COLUMN IS THE OPERATOR'S POINT: every one")
    print("  of those is a loss for the long and a win for the spread, and an")
    print("  MAE-based test would have counted it as a breach.")

    print(f"\n{'=' * 84}")
    print("  ⚠️ THE ASYMMETRY, and it decides how you read the table above.")
    print("  The LONG number is REAL — real fills, real slippage, real")
    print("  management (stops fired, trails engaged, early closes). The SPREAD")
    print("  number is MODELLED — archived quotes, filled at the posted bid,")
    print("  held to expiry, no management, no early assignment, no commission.")
    print("  That tilts the comparison TOWARD the counterfactual by")
    print("  construction. A NARROW WIN FOR THE SPREAD IS A NULL, NOT A RESULT.")
    print("=" * 84)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
