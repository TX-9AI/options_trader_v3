#!/usr/bin/env python3
"""
tests/conditional_tables.py — v1.0 — Conditional-probability tables from the
        fleet's own record: P(win), fee-adjusted expectancy, and sample counts
        per conditioning cell. The empirical substrate for placing the L3
        conviction bars (ROADMAP Phase 3): a bar belongs at the fee-adjusted-ROI
        zero crossing of exactly these cells.
v1.0 — 2026-07-23 — initial. OFFLINE, control-server, stdlib-only (sqlite3 +
        json). Reads what already lands on 1-REPORTER; touches NO bot code and
        does not disturb the frozen baseline window.

        TWO SOURCES, each optional, both if present:

        (1) TRADES MODE (works tonight): per-symbol snapshot DBs at
            ~/day_trader_pro/trades/<date>/<SYMBOL>_<date>_trades.db
            (the EOD chain's product). Closed trades only. Dimensions:
            regime label x strategy x grade x direction x time bucket x
            VIX band x condor-leg flag. Emits one-dim marginals, the useful
            two-dim crosses, and full-tuple cells above --min-n.

        (2) JOURNAL MODE (matures once the jsonl harvest lands — the 07-18
            decision deferred wiring data/signal_journal/ into the EOD chain):
            <journal_root>/<date>/<SYM>.jsonl. Uses `scored` + `disposition`
            events: fire rate, grade distribution, and REJECT share by regime
            label and conviction decile — the counterfactual side the DBs
            cannot see ("a gate you can't counterfactual is a gate you can't
            calibrate").

        Honesty guards: Wilson 95% interval printed next to every P(win) so a
        7-sample 71% cell reads as the noise it is; cells below --min-n are
        suppressed from the cross tables (marginals always print with n).
        Fees default to $0 round-trip per contract (paper); set
        CT_FEES_RT_PER_CONTRACT to make expectancy fee-adjusted.

        Usage (control server):
          python3 -m tests.conditional_tables                      # all dates on disk
          python3 -m tests.conditional_tables --since 2026-07-20   # window
          python3 -m tests.conditional_tables --date 2026-07-22    # one day
          CT_FEES_RT_PER_CONTRACT=1.30 python3 -m tests.conditional_tables
        Output: reports/conditional_tables_<first>_<last>.txt (+ .jsonl cells)
        under --reports-dir (default ~/day_trader_pro/reports).
"""

import argparse
import glob
import json
import math
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime

TRADES_ROOT_DEFAULT  = os.path.expanduser("~/day_trader_pro/trades")
JOURNAL_ROOT_DEFAULT = os.path.expanduser("~/day_trader_pro/signal_journal")
REPORTS_DIR_DEFAULT  = os.path.expanduser("~/day_trader_pro/reports")

FEES_RT = float(os.environ.get("CT_FEES_RT_PER_CONTRACT", "0.0"))

# ── dimension extractors ─────────────────────────────────────────────────────

def time_bucket(entry_time: str) -> str:
    """ET session bucket from the stored entry_time text (None-safe)."""
    if not entry_time:
        return "unknown"
    try:
        t = entry_time.strip().replace("T", " ")
        hhmm = None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%H:%M:%S"):
            try:
                hhmm = datetime.strptime(t.split("+")[0].split(".")[0], fmt)
                break
            except ValueError:
                continue
        if hhmm is None:
            return "unknown"
        m = hhmm.hour * 60 + hhmm.minute
        if m < 9 * 60 + 30:   return "premarket"
        if m < 10 * 60 + 30:  return "0930-1030"
        if m < 11 * 60 + 30:  return "1030-1130"
        if m < 13 * 60:       return "1130-1300"
        if m < 14 * 60:       return "1300-1400"
        if m < 15 * 60 + 45:  return "1400-1545"
        return "1545+"
    except Exception:
        return "unknown"


def vix_band(v) -> str:
    try:
        v = float(v or 0.0)
    except (TypeError, ValueError):
        return "unknown"
    if v <= 0:  return "unknown"
    if v < 15:  return "vix<15"
    if v < 20:  return "vix15-20"
    if v < 27:  return "vix20-27"
    return "vix27+"


def conviction_decile(c) -> str:
    try:
        c = max(0.0, min(1.0, float(c)))
    except (TypeError, ValueError):
        return "unknown"
    lo = int(c * 10) * 10
    if lo == 100:
        lo = 90
    return f"conv{lo:02d}-{lo + 10:02d}"


def wilson(p_hat: float, n: int, z: float = 1.96):
    """Wilson 95% score interval — the honest error bar for small cells."""
    if n == 0:
        return (0.0, 1.0)
    denom  = 1.0 + z * z / n
    centre = (p_hat + z * z / (2 * n)) / denom
    half   = (z / denom) * math.sqrt(p_hat * (1 - p_hat) / n + z * z / (4 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))


# ── trades mode ──────────────────────────────────────────────────────────────

TRADE_COLS = ("symbol,strategy,setup_type,setup_grade,direction,regime,"
              "vix_at_entry,is_condor_leg,contracts,pnl_usd,entry_time,"
              "exit_reason,paper_trade")


def load_trades(trades_root: str, dates):
    rows = []
    for d in dates:
        for db in sorted(glob.glob(os.path.join(trades_root, d, "*_trades.db"))):
            try:
                con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
                cur = con.execute(
                    f"SELECT {TRADE_COLS} FROM trades "
                    "WHERE pnl_usd IS NOT NULL AND exit_reason IS NOT NULL")
                for r in cur.fetchall():
                    rows.append(dict(zip(TRADE_COLS.split(","), r), _date=d))
                con.close()
            except sqlite3.Error as e:
                print(f"  warn: {os.path.basename(db)}: {e}", file=sys.stderr)
    return rows


def trade_dims(t: dict) -> dict:
    return {
        "regime":   (t.get("regime") or "unknown"),
        "strategy": (t.get("strategy") or t.get("setup_type") or "unknown"),
        "grade":    (t.get("setup_grade") or "unknown"),
        "direction": (t.get("direction") or "unknown"),
        "bucket":   time_bucket(t.get("entry_time")),
        "vix":      vix_band(t.get("vix_at_entry")),
        "condor_leg": "leg" if t.get("is_condor_leg") else "single",
    }


class Cell:
    __slots__ = ("n", "wins", "pnl")

    def __init__(self):
        self.n, self.wins, self.pnl = 0, 0, 0.0

    def add(self, net):
        self.n += 1
        self.wins += 1 if net > 0 else 0
        self.pnl += net


TRADE_GROUPINGS = [
    ("regime",),
    ("strategy",),
    ("grade",),
    ("bucket",),
    ("vix",),
    ("condor_leg",),
    ("regime", "strategy"),
    ("strategy", "grade"),
    ("strategy", "bucket"),
    ("regime", "bucket"),
    ("regime", "strategy", "grade"),
]


def build_trade_tables(rows):
    tables = {g: defaultdict(Cell) for g in TRADE_GROUPINGS}
    for t in rows:
        try:
            net = float(t["pnl_usd"]) - FEES_RT * float(t.get("contracts") or 0)
        except (TypeError, ValueError):
            continue
        d = trade_dims(t)
        for g in TRADE_GROUPINGS:
            tables[g][tuple(d[k] for k in g)].add(net)
    return tables


# ── journal mode ─────────────────────────────────────────────────────────────

def load_journal(journal_root: str, dates):
    """scored/disposition counters keyed by (regime label, conviction decile)."""
    scored  = defaultdict(lambda: defaultdict(int))   # key -> grade -> n
    fired   = defaultdict(int)
    reject  = defaultdict(int)                        # sizing_rejected+invalid
    total_events = 0
    for d in dates:
        for jf in sorted(glob.glob(os.path.join(journal_root, d, "*.jsonl"))):
            try:
                with open(jf, encoding="utf-8") as fh:
                    for line in fh:
                        try:
                            ev = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        total_events += 1
                        reg = ev.get("regime") or {}
                        key = ((reg.get("label") or "unknown"),
                               conviction_decile(reg.get("conviction")))
                        kind = ev.get("event") or ev.get("kind") or ""
                        if kind == "scored":
                            grade = ((ev.get("score") or {}).get("grade")
                                     or "REJECT")
                            scored[key][grade] += 1
                        elif kind == "disposition":
                            out = ev.get("outcome") or ""
                            if out == "fired":
                                fired[key] += 1
                            elif out in ("sizing_rejected", "invalid_signal"):
                                reject[key] += 1
            except OSError as e:
                print(f"  warn: {os.path.basename(jf)}: {e}", file=sys.stderr)
    return scored, fired, reject, total_events


# ── report ───────────────────────────────────────────────────────────────────

def fmt_cell(key, c: Cell) -> str:
    p = c.wins / c.n if c.n else 0.0
    lo, hi = wilson(p, c.n)
    exp = c.pnl / c.n if c.n else 0.0
    name = " × ".join(key)
    return (f"  {name:<46} n={c.n:<4} P(win)={p:5.1%} "
            f"[{lo:4.0%},{hi:4.0%}]  E[net]=${exp:8.2f}  Σ=${c.pnl:9.2f}")


def write_report(out_txt, out_jsonl, dates, rows, tables,
                 journal_stats, min_n):
    lines = []
    push = lines.append
    push("=" * 78)
    push(f"CONDITIONAL TABLES — {dates[0]} → {dates[-1]}  "
         f"({len(dates)} session(s), {len(rows)} closed trades, "
         f"fees=${FEES_RT:.2f}/contract RT)")
    push("The L3 bar belongs at the fee-adjusted expectancy zero crossing of")
    push("these cells. Expect most cells ≈ coin flip; the edge is the few that")
    push("persistently are not. Wilson 95% intervals are the honesty check —")
    push("do NOT act on a cell whose interval still straddles 50%.")
    push("=" * 78)

    cells_out = []
    for g in TRADE_GROUPINGS:
        push("")
        push(f"── by {' × '.join(g)} " + "─" * max(1, 60 - 6 * len(g)))
        table = tables[g]
        shown = 0
        for key in sorted(table, key=lambda k: -table[k].n):
            c = table[key]
            if len(g) > 1 and c.n < min_n:
                continue
            push(fmt_cell(key, c))
            shown += 1
            p = c.wins / c.n
            lo, hi = wilson(p, c.n)
            cells_out.append({"group": list(g), "key": list(key), "n": c.n,
                              "p_win": round(p, 4),
                              "wilson95": [round(lo, 4), round(hi, 4)],
                              "expectancy_net": round(c.pnl / c.n, 2),
                              "pnl_net_total": round(c.pnl, 2)})
        if shown == 0:
            push(f"  (all cells below min-n={min_n})")

    scored, fired, reject, total_events = journal_stats
    push("")
    push("── journal (counterfactual side) " + "─" * 44)
    if total_events == 0:
        push("  no journal events found — the signal journal is not harvested")
        push("  off-box yet (deliberate 07-18 deferral). These tables light up")
        push("  automatically once data/signal_journal/<date>/ is pulled to the")
        push("  journal root. The DB tables above cannot see REJECTs; this")
        push("  section is where the counterfactual calibration will live.")
    else:
        push(f"  {total_events} events")
        keys = sorted(set(scored) | set(fired) | set(reject))
        for key in keys:
            grades = scored.get(key, {})
            n_sc = sum(grades.values())
            n_f, n_r = fired.get(key, 0), reject.get(key, 0)
            gtxt = " ".join(f"{g}:{n}" for g, n in sorted(grades.items()))
            push(f"  {key[0]:<18} {key[1]:<12} scored={n_sc:<4} "
                 f"fired={n_f:<4} rejected={n_r:<4} [{gtxt}]")

    push("")
    push("=" * 78)
    text = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(out_txt), exist_ok=True)
    with open(out_txt, "w", encoding="utf-8") as fh:
        fh.write(text)
    with open(out_jsonl, "w", encoding="utf-8") as fh:
        for c in cells_out:
            fh.write(json.dumps(c) + "\n")
    return text


def discover_dates(trades_root, journal_root, since, only_date):
    seen = set()
    for root in (trades_root, journal_root):
        if os.path.isdir(root):
            for name in os.listdir(root):
                if len(name) == 10 and name[4] == "-" and name[7] == "-":
                    seen.add(name)
    dates = sorted(seen)
    if only_date:
        dates = [d for d in dates if d == only_date]
    elif since:
        dates = [d for d in dates if d >= since]
    return dates


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--since")
    ap.add_argument("--date")
    ap.add_argument("--trades-root",  default=TRADES_ROOT_DEFAULT)
    ap.add_argument("--journal-root", default=JOURNAL_ROOT_DEFAULT)
    ap.add_argument("--reports-dir",  default=REPORTS_DIR_DEFAULT)
    ap.add_argument("--min-n", type=int, default=5,
                    help="suppress cross-table cells below this sample count")
    args = ap.parse_args()

    dates = discover_dates(args.trades_root, args.journal_root,
                           args.since, args.date)
    if not dates:
        print("no dated folders found under "
              f"{args.trades_root} or {args.journal_root}")
        return 1

    rows = load_trades(args.trades_root, dates)
    tables = build_trade_tables(rows)
    journal_stats = load_journal(args.journal_root, dates)

    stem = f"conditional_tables_{dates[0]}_{dates[-1]}"
    out_txt   = os.path.join(args.reports_dir, stem + ".txt")
    out_jsonl = os.path.join(args.reports_dir, stem + ".jsonl")
    text = write_report(out_txt, out_jsonl, dates, rows, tables,
                        journal_stats, args.min_n)
    print(text)
    print(f"written: {out_txt}\nwritten: {out_jsonl}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
