#!/usr/bin/env python3
"""
tests/gap_outcome_join.py — v1.3 — 2026-08-02

v1.3 — 2026-08-02 — --since / --until, AND A DEFAULT THAT REFUSES TO POOL ACROSS
       A DOCUMENTED CONFOUND. v1.2 fixed the join and the per-date column then
       showed the real problem: FOUR DAYS CARRY 73% OF ALL TRADES. 07-13 and
       07-14 have 225 each, 07-16/17 have 111/128, 07-31 has 116 — while the nine
       sessions 07-20..07-30 produced 134 COMBINED, about 15/day across 29 boxes.
       That is not one population and pooling pnl_usd across it is not analysis.
       WHAT ACTUALLY CHANGED, from docs/HISTORY.md — 2026-07-18 is "day zero on a
       materially changed engine":
         07-20  orb_engine v3.9 — the stale-retest timeout had been counting 15s
                loop ticks as bars and dying in ~3 minutes; fixed to real 1m bars,
                and expiry now RE-ARMS instead of terminating.
         07-21  main.py v4.0 — L2.5 live, the L1→L2 committed label now drives
                primary_regime. sweep_reversal v3.2 ORB-ownership gate.
         07-22  regime_confluence v1.2 ramp de-saturation AND, riding the same
                push, the MARK-LIMIT EXECUTION workstream — limit_ladder v1.2,
                entry_engine v3.8 mark-limit entries, mark-limit exit closes.
       And the volume cliff has a NAMED cause rather than being a mystery: the
       v2.5 row records that UNKNOWN's veto power was REMOVED FOR THE ORB —
       "Sample restored. The safety was removed before the replacement was built."
       Pre-07-20 volume was a deliberate un-gating, not a defect firing randomly.
       THE REPO ALREADY WARNED ABOUT THIS. HISTORY.md, on the 07-22 push:
       "label-gated regime metrics stay attributable to v1.2; P&L / FILL-DEPENDENT
       STATS ARE CONFOUNDED BY BOTH CHANGES. The ~2-week frozen-baseline window
       gets one week added to its back end to preserve a clean stretch."
       This tool reports pnl_usd, which is exactly a fill-dependent stat. So the
       DEFAULT is now --since 2026-07-23, the first session after mark-limit
       landed. Pooling the whole range requires --since 1970-01-01 and prints a
       warning, because it should be a deliberate act rather than the default.
       BE HONEST ABOUT WHAT THAT LEAVES: ~215 trades, 116 of them from 07-31
       alone. Over half the clean sample is ONE SESSION. Gap-conditioned P&L may
       simply not be answerable yet, and "not yet" is a legitimate answer.
v1.2 — 2026-08-02 — NORMALISE THE JOIN KEY. --diagnose immediately earned its
       keep: of the 450 unjoined, 225 were the first tape date (legitimate — no
       prior session to gap against) and 225 were ONE DATE, 2026-07-14, where the
       `box` field carries the SOURCE DB FILENAME (`AVGO_2026-07-14_TRADES.DB`)
       rather than the ticker. My join used `box` verbatim, so every trade that
       day missed. Recovering them is ~24% of the sample.
       `box` stays authoritative — consolidate_trades deliberately leaves the
       row's own `symbol` column untouched so a mislabeled db can be caught, so
       switching fields would discard that safeguard. The suffix is stripped
       instead.
v1.1 — 2026-08-02 — --diagnose. The first real run joined only 489 of 939 closed
       trades: 450 had NO GAP RECORD, which is ~48% of the sample discarded by an
       unknown selection rule. That is not a caveat, it is a hole — a cell drawn
       from half the trades with unknown bias tells you nothing. This flag says
       exactly which side is missing (date absent from the lookup vs symbol absent
       within a present date) and breaks it down by date and by symbol, so the
       cause is measured rather than guessed.
       Two priors worth checking against the output, both of which would be
       LEGITIMATE rather than defects: (a) the FIRST tape date has no prior
       session, so every symbol on it is a first-appearance skip by construction —
       gap_backfill reported 29 of those; (b) only a SUBSET of boxes wakes on a
       typical day, so a symbol that traded today but whose PRIOR session was
       never harvested has no gap to compute. If the 450 is mostly (b), the join
       is honest but the sample is structurally thin and that is the finding.

DOES GAP CLASS SEPARATE GOOD TRADING DAYS FROM BAD ONES? Joins already-banked
trade outcomes to the gap classification. No new collection, no waiting.

WHY THIS AND NOT THE A2 STATE ITSELF
    The clean-corpus A2 work (AQ, AR) killed most of what it set out to find:
    drift shows NO EDGE at any horizon or elapsed bucket, so paused_trend as a
    live drift factor is unsupported; the wrong-theta-sign hypothesis for
    continuation's -$2,024 is not supported; and the excursion difference is real
    but ~3% at p90, which does not move a condor's economics.

    What SURVIVED was something the A2 work was not looking for. From the clean
    partition grid:

                     OPEN         DECAY        CLEAN
        FLAT          3.60   →    13.78   →     3.55
        CONT          9.89   →     5.91   →     1.46
        REV           9.55   →     5.98   →     1.83

    **Gap class x time of day is a strong conditioning variable, and nothing in
    the fleet keys on it.** On a flat open the first 70 minutes are statistically
    indistinguishable from midday, then 10:40-12:00 runs ~4x hotter. On gap days
    the open is hot and decays monotonically. Two completely different day
    shapes, and every strategy currently treats them identically.

    So A2 was never the tradeable signal. It was the INSTRUMENT that made day type
    visible — a sensitive proxy for regime ambiguity that exposed a structure in
    the tape we had no other way to measure. That is a legitimate outcome for a
    diagnostic, and it is worth saying plainly rather than pretending the state
    itself pays.

THE SHARPEST TEST, and why ORB is first
    ORB forms its opening range 09:30-10:00 — PRECISELY the window that is dead
    on flat-open days and hot on gap days. Item **AH** has ORB at **-0.24R over
    252 trades** with no explanation offered. If that decomposes into something
    like "+0.3R on gap days, -0.8R on flat opens", it is a gate with a real
    sample behind it, no new collection, and it lands well before the freeze.
    The same split applies to the 362 condors and to continuation's
    handoff-vs-standalone problem.

WHAT THIS IS NOT
    It is not a backtest and it does not size, gate or recommend anything. It
    reports outcomes already realised, partitioned by a variable that was always
    computable and never computed. Any gate that follows needs its own
    pre-registered validation — this only says whether there is something there.

HONEST LIMITS, stated up front rather than discovered later
    - The fleet has been PAPER trading, so fills are simulated. A split that
      depends on fill quality will not show here.
    - Sample per cell will be small. 252 ORB trades over 15 sessions across 3 gap
      classes is ~84 per class BEFORE any strategy or grade split. The n>=30
      floor below is low for a mean-with-CI and cells are refused under it.
    - Gap class is assigned per (date, symbol), so every trade on a symbol-day
      inherits one class. That is correct — the gap is a property of the session,
      not of the trade — but it means cells are not independent samples.
    - pnl_usd is used, not R. Position sizes vary, so a big loser on one symbol
      can dominate a cell's net. Win rate and median are reported alongside the
      mean for exactly that reason.

USAGE (single line, control box, repo root)
    python3 tests/gap_outcome_join.py
    python3 tests/gap_outcome_join.py --by strategy
    python3 tests/gap_outcome_join.py --by strategy --window OPEN

Read-only. Reads reports/gap_pct.json and reports/fleet_trades_<date>.json.
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import math
import os
import re
import sys

DEFAULT_GAPS = "~/day_trader_pro/reports/gap_pct.json"
TRADES_GLOB = "~/day_trader_pro/reports/fleet_trades_*.json"
DATE_RE = re.compile(r"(20\d\d-\d\d-\d\d)")
CLASSES = ("CONT", "FLAT", "REV")

# Low, because the samples are what they are. A cell under this is REFUSED
# rather than read — the same discipline a2_partition uses at n>=500, scaled to
# trade counts instead of tick counts.
MIN_CELL_N = 30

# First session AFTER the mark-limit execution workstream landed (2026-07-22).
# Before this, fills came from a different execution path, so pnl_usd on either
# side is not the same measurement. HISTORY.md flags this explicitly.
CONFOUND_CUTOFF = "2026-07-23"

# Entry-time buckets, matching a2_partition's so the two can be read together.
BUCKETS = (("OPEN", "09:30", "10:40"),
           ("DECAY", "10:40", "12:00"),
           ("CLEAN", "12:00", "16:00"))


_DBNAME_RE = re.compile(r"_\d{4}-\d{2}-\d{2}_TRADES\.DB$", re.I)


def _symbol_of(t):
    """Ticker from a trade row.

    `box` is the authoritative tag (consolidate_trades stamps it from the source
    file and leaves the row's own `symbol` column untouched on purpose, so a
    mislabeled db stays detectable). But on some dates it carries the whole
    filename — `AVGO_2026-07-14_TRADES.DB` — so the suffix is stripped rather
    than falling back to `symbol`, which would throw the safeguard away.
    """
    raw = str(t.get("box") or t.get("symbol") or "?")
    raw = _DBNAME_RE.sub("", raw)
    if raw.lower().endswith(".db"):
        raw = raw[:-3]
    return raw.upper()


def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _mean_ci(xs):
    n = len(xs)
    if n < 2:
        return (xs[0] if n else 0.0), 0.0, n
    m = sum(xs) / n
    var = sum((x - m) ** 2 for x in xs) / (n - 1)
    return m, 1.96 * math.sqrt(var / n), n


def _median(xs):
    if not xs:
        return 0.0
    s = sorted(xs)
    return s[len(s) // 2]


def _entry_bucket(t):
    """Time bucket from whichever entry-time field the row carries. Returns None
    when no usable timestamp exists — those trades are counted and reported, not
    silently assigned to a bucket."""
    for key in ("entry_time", "entry_ts", "opened_at", "timestamp", "time"):
        v = t.get(key)
        if not v:
            continue
        m = re.search(r"(\d{2}):(\d{2})", str(v))
        if not m:
            continue
        hhmm = f"{m.group(1)}:{m.group(2)}"
        for name, lo, hi in BUCKETS:
            if lo <= hhmm < hi:
                return name
        return "OTHER"
    return None


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gaps", default=DEFAULT_GAPS)
    ap.add_argument("--by", default="strategy",
                    help="row dimension: strategy, setup_grade, regime, box")
    ap.add_argument("--since", default=CONFOUND_CUTOFF,
                    help=f"first date to include (default {CONFOUND_CUTOFF}, the "
                         f"session after mark-limit landed). Widening this pools "
                         f"pnl_usd across a documented execution change.")
    ap.add_argument("--until", default="9999-12-31",
                    help="last date to include")
    ap.add_argument("--diagnose", action="store_true",
                    help="report WHY trades failed to join, by date and symbol")
    ap.add_argument("--window", default="ALL",
                    help="restrict to an entry bucket: OPEN / DECAY / CLEAN / ALL")
    a = ap.parse_args(argv[1:])

    gaps_path = os.path.expanduser(a.gaps)
    if not os.path.isfile(gaps_path):
        print(f"No gap lookup at {gaps_path} — run tests/gap_backfill.py first.")
        return 2
    gaps = json.load(open(gaps_path)).get("sessions", {})

    paths = sorted(glob.glob(os.path.expanduser(TRADES_GLOB)))
    if not paths:
        print(f"No fleet_trades_*.json found under {TRADES_GLOB}")
        return 2

    # (row_key, gap_class) -> [pnl]
    cells = collections.defaultdict(list)
    totals = collections.Counter()
    no_gap_record = 0
    no_bucket = 0
    n_closed = 0
    in_window = 0
    # v1.1 diagnostics: split the miss by WHICH side is absent
    miss_date = collections.Counter()      # date not in the gap lookup at all
    miss_sym = collections.Counter()       # date present, symbol absent
    miss_class = collections.Counter()     # record present, class not CONT/FLAT/REV
    joined_by_date = collections.Counter()
    excluded_dates = {}

    for p in paths:
        m = DATE_RE.search(os.path.basename(p))
        if not m:
            continue
        date = m.group(1)
        if not (a.since <= date <= a.until):
            excluded_dates[date] = 0
            continue
        day = gaps.get(date)
        try:
            bundle = json.load(open(p))
        except Exception:                                        # noqa: BLE001
            continue
        for t in bundle.get("trades", []):
            if str(t.get("status", "")).lower() != "closed":
                continue
            n_closed += 1
            in_window += 1
            sym = _symbol_of(t)
            grec = (day or {}).get(sym)
            if not grec or grec.get("gap_class") not in CLASSES:
                no_gap_record += 1
                if day is None:
                    miss_date[date] += 1
                elif grec is None:
                    miss_sym[f"{date}/{sym}"] += 1
                else:
                    miss_class[str(grec.get("gap_class"))] += 1
                continue
            joined_by_date[date] += 1
            if a.window.upper() != "ALL":
                b = _entry_bucket(t)
                if b is None:
                    no_bucket += 1
                    continue
                if b != a.window.upper():
                    continue
            key = str(t.get(a.by) or "?")
            cells[(key, grec["gap_class"])].append(_num(t.get("pnl_usd")))
            totals[grec["gap_class"]] += 1

    if a.diagnose:
        print(f"closed trades      : {n_closed}")
        print(f"joined             : {sum(totals.values())}")
        print(f"NOT joined         : {no_gap_record}\n")
        print("WHY, by cause")
        print(f"  date absent from the gap lookup : {sum(miss_date.values())}")
        for d, n in miss_date.most_common():
            print(f"      {d}  {n} trades   <- no gap record for this date at all")
        print(f"  symbol absent within a present date : {sum(miss_sym.values())}")
        by_sym = collections.Counter()
        by_date2 = collections.Counter()
        for k, n in miss_sym.items():
            d, sy = k.split("/")
            by_sym[sy] += n
            by_date2[d] += n
        print("      top symbols:", ", ".join(f"{s_}:{n}" for s_, n in by_sym.most_common(8)))
        print("      top dates  :", ", ".join(f"{d}:{n}" for d, n in by_date2.most_common(8)))
        print(f"  gap_class not CONT/FLAT/REV : {sum(miss_class.values())}"
              f"   {dict(miss_class)}")
        print("\nJOINED per date (to see whether the loss is one date or spread)")
        for d in sorted(set(list(joined_by_date) + list(miss_date) + list(by_date2))):
            print(f"  {d}   joined {joined_by_date[d]:>4}   "
                  f"missed {miss_date[d] + by_date2[d]:>4}")
        print("\nREADING IT: a loss concentrated on the FIRST tape date is the")
        print("first-appearance skip and is correct by construction. A loss spread")
        print("across dates and symbols means the PRIOR session was never harvested")
        print("for those symbols — the join is honest, but the sample is")
        print("structurally thin and that is itself the finding.")
        return 0

    if not cells:
        print("Nothing joined. Check that trade dates overlap the gap lookup.")
        return 2

    if a.since <= "2026-07-22":
        print("⚠ WARNING: --since is at or before 2026-07-22, so this pools "
              "pnl_usd ACROSS\n  the mark-limit execution change. HISTORY.md: "
              "\"P&L / fill-dependent stats\n  are confounded by both changes.\" "
              "Fills differ on either side of that date.\n")
    print(f"window             : {a.since} .. {a.until}"
          f"   ({len(excluded_dates)} date(s) excluded)")
    print(f"fleet_trades files : {len(paths)}")
    print(f"closed trades      : {n_closed}")
    print(f"joined to a gap    : {sum(totals.values())}"
          f"   (CONT {totals['CONT']}  FLAT {totals['FLAT']}  REV {totals['REV']})")
    print(f"no gap record      : {no_gap_record}")
    if a.window.upper() != "ALL":
        print(f"window             : {a.window.upper()}  "
              f"(no usable entry time: {no_bucket})")
    print(f"row dimension      : {a.by}")
    print("units              : pnl_usd. PAPER fills — see the header's limits.\n")

    rows = sorted({k for k, _ in cells})
    print(f"{'':<26}" + "".join(f"{c:>26}" for c in CLASSES))
    for r in rows:
        line = f"{r[:25]:<26}"
        for c in CLASSES:
            xs = cells.get((r, c), [])
            if len(xs) < MIN_CELL_N:
                line += f"{f'n={len(xs)} (refused)':>26}"
                continue
            mean, hw, n = _mean_ci(xs)
            wins = sum(1 for x in xs if x > 0)
            line += f"{f'{mean:+.1f}±{hw:.1f} {wins/n:.0%} n={n}':>26}"
        print(line)

    print(f"\n  mean pnl_usd ±95%, win rate, n. Cells under n={MIN_CELL_N} refused.")

    # ── the one comparison worth calling out explicitly ─────────────────────
    print("\n" + "=" * 62)
    print("READING IT")
    print("=" * 62)
    print("  A row whose CONT and FLAT cells differ by more than their bands is")
    print("  a strategy whose outcome depends on the day type — and nothing in")
    print("  the fleet currently keys on that.")
    print("  ORB is the one to look at first: it forms its range 09:30-10:00,")
    print("  the window the clean A2 grid shows is DEAD on flat opens and HOT on")
    print("  gap days. AH has it at -0.24R over 252 trades with no explanation.")
    print("  Medians are printed below because one large loser can dominate a")
    print("  small cell's mean.")
    print()
    for r in rows:
        parts = []
        for c in CLASSES:
            xs = cells.get((r, c), [])
            parts.append(f"{c} med {_median(xs):+.1f}" if len(xs) >= MIN_CELL_N
                         else f"{c} —")
        print(f"  {r[:25]:<26} " + "   ".join(parts))
    print("\nNot a backtest. Reports realised outcomes partitioned by a variable")
    print("that was always computable and never computed. Any gate that follows")
    print("needs its own pre-registered validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
