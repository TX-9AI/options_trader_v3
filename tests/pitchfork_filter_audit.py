#!/usr/bin/env python3
"""
tests/pitchfork_filter_audit.py — v1.1 — 2026-08-01

v1.1 — 2026-08-01 — VERDICT BINNING CORRECTED, AND WHAT 6.8% ACTUALLY MEASURES.
       v1.0 swept STRUCTURAL_* into "filter tightness" and reported
       "FILTER TIGHTNESS (2064 vs 77)" on the first real run. That overstates it
       badly: `P2_not_above_P0` does NOT mean a threshold is too tight, it means
       the last three pivots are NOT A DIRECTIONAL STRUCTURE — a correct
       rejection of chop, with no parameter behind it. Re-binned honestly the
       same counts read ~52% no-structure-exists (STRUCTURAL 1,128 + fewer-than-3
       77), ~41% parameter-sensitive (SEPARATION 915 + SIGNIFICANCE 21), 6.8%
       built. Three bins now, not two.
       AND THE HEADLINE NUMBER IS MISNAMED. 6.8% is the fork BIRTH rate — this
       tool calls the stateless build_fork at EVERY index. But §5.2 says a fork
       HOLDS UNTIL INVALIDATED, so with lifecycle implemented one birth covers
       every bar until it dies. 156 births across 29 symbols is ~5 anchor events
       per symbol in three weeks, which is entirely reasonable for a PERSISTENT
       object. Coverage is the number that matters and it is not measured here.

WHY THE HOURLY FORK ALMOST NEVER BUILDS — corpus length, or filter tightness?

`a2_rail_drift` reported **1,030 ticks with no usable fork** and only n=78 for
both median-line regressions, so Predictor 2 was REFUSED at every horizon. That
is a NON-RESULT, not a negative — the question was never measured. But the two
possible causes have opposite responses:

    CORPUS LENGTH   15 sessions is ~105 hourly bars per symbol. If most
                    rejections are FRAME_TOO_SHORT or
                    FEWER_THAN_3_ALTERNATING_PIVOTS, the series simply does not
                    yet contain qualifying structure -> WAIT. Bars accrue at ~7
                    per session; PF.2 is blocked on time, not on design.

    FILTER TIGHTNESS  If most rejections are SIGNIFICANCE / SEPARATION /
                    RECENCY, the §4.3 priors (S=1.0 ATR, 2k+1 separation, R=40)
                    are too tight for a series this short -> REVISIT THE PRIORS.
                    §10 already names the ten-parameter surface as an overfitting
                    risk, so any loosening must be pre-registered and justified
                    from THIS audit rather than tuned until forks appear.

This walks each symbol's hourly series bar by bar, calls the REAL build_fork at
every index (so the confirmation-lag rule and every filter are exactly the
shipped ones), and tallies `last_reject_reason()`. It duplicates no filter logic —
that was the point of adding the reasons to pitchfork.py v1.1 rather than
reimplementing the gate chain here and creating a second lineage of it.

Read-only. Builds nothing, changes no threshold, recommends no value.

USAGE (single line, control box, repo root)
    python3 tests/pitchfork_filter_audit.py
    python3 tests/pitchfork_filter_audit.py --symbols SPX,QQQ
"""

from __future__ import annotations

import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd  # noqa: E402

from analysis.pitchfork import build_fork, last_reject_reason  # noqa: E402
from utils.math_utils import atr_series  # noqa: E402

TAPE_ROOTS = ["~/day_trader_pro/ohlc", "./ohlc"]
DATE_RE = re.compile(r"^20\d\d-\d\d-\d\d$")


def _tape_root(explicit: str = ""):
    for r in ([explicit] if explicit else TAPE_ROOTS):
        p = os.path.expanduser(r)
        if os.path.isdir(p):
            return p
    return None


def _symbols(root: str):
    syms = set()
    for d in os.listdir(root):
        if not DATE_RE.match(d):
            continue
        for f in os.listdir(os.path.join(root, d)):
            low = f.lower()
            if "_ohlc_" in low and low.endswith(".csv"):
                syms.add(f.split("_ohlc_")[0].upper())
    return sorted(syms)


def _hourly(root: str, sym: str):
    frames = []
    for date in sorted(d for d in os.listdir(root) if DATE_RE.match(d)):
        day = os.path.join(root, date)
        for f in os.listdir(day):
            low = f.lower()
            if low.startswith(sym.lower() + "_ohlc_") and low.endswith(".csv"):
                try:
                    df = pd.read_csv(os.path.join(day, f), parse_dates=["timestamp"])
                except Exception:                                # noqa: BLE001
                    continue
                frames.append(df.set_index("timestamp").sort_index()
                              [["open", "high", "low", "close"]])
    if not frames:
        return None
    df1m = pd.concat(frames).sort_index()
    agg = {"open": "first", "high": "max", "low": "min", "close": "last"}
    return df1m.resample("1h", label="right", closed="right").agg(agg).dropna(subset=["close"])


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape-root", default="")
    ap.add_argument("--symbols", default="")
    a = ap.parse_args(argv[1:])

    root = _tape_root(a.tape_root)
    if not root:
        print("No tape root found (looked in " + ", ".join(TAPE_ROOTS) + ")")
        return 2
    syms = ([s.strip().upper() for s in a.symbols.split(",") if s.strip()]
            or _symbols(root))
    if not syms:
        print(f"No symbols found under {root}")
        return 2

    print(f"tape {root} | {len(syms)} symbol(s)\n")
    totals = collections.Counter()
    built = 0
    attempts = 0
    bars_by_sym = {}

    for sym in syms:
        h1 = _hourly(root, sym)
        if h1 is None or len(h1) < 20:
            bars_by_sym[sym] = 0 if h1 is None else len(h1)
            continue
        bars_by_sym[sym] = len(h1)
        for idx in range(20, len(h1)):
            sub = h1.iloc[:idx + 1]
            atr = float(atr_series(sub, 14).iloc[-1]) if len(sub) > 15 else 0.0
            attempts += 1
            f = build_fork(sym, sub, "1h", atr)
            if f is not None:
                built += 1
                totals["__BUILT__"] += 1
            else:
                totals[last_reject_reason() or "UNKNOWN"] += 1

    bars = list(bars_by_sym.values())
    print(f"hourly bars per symbol: min {min(bars)}  median "
          f"{sorted(bars)[len(bars)//2]}  max {max(bars)}")
    print(f"build attempts {attempts}   forks built {built} "
          f"({100.0*built/max(attempts,1):.1f}%)\n")
    print("REJECTIONS, most common first")
    for reason, n in totals.most_common():
        if reason == "__BUILT__":
            continue
        print(f"  {n:>7}  {100.0*n/max(attempts,1):5.1f}%  {reason}")

    # ── the verdict this file exists to give ────────────────────────────────
    # v1.1 — THREE bins. STRUCTURAL is neither a length problem nor a tight
    # parameter: it means the last three pivots are not a directional structure,
    # which is a correct rejection of chop and has no threshold behind it.
    # Binning it with SEPARATION/SIGNIFICANCE (as v1.0 did) manufactures a
    # "filter tightness" verdict out of the engine working properly.
    length_side = sum(totals[r] for r in
                      ("FRAME_TOO_SHORT", "FEWER_THAN_3_ALTERNATING_PIVOTS",
                       "NO_ATR"))
    no_structure = sum(totals[r] for r in totals if r.startswith("STRUCTURAL"))
    filter_side = sum(totals[r] for r in totals
                      if r.startswith(("SIGNIFICANCE", "SEPARATION", "RECENCY")))
    print(f"\n  binned:  no qualifying structure {length_side + no_structure}"
          f"   parameter-sensitive {filter_side}   built {built}")
    print("\n" + "=" * 60)
    if attempts == 0:
        print("VERDICT  REFUSED — no build attempts.")
    elif built and 100.0 * built / attempts > 20:
        print(f"VERDICT  NEITHER — forks build {100.0*built/attempts:.0f}% of the "
              f"time. a2_rail_drift's\n         starvation is elsewhere: check the "
              f"hidx>=20 warmup cut and the\n         is_born_by() gate in that "
              f"tool, not these filters.")
    elif (length_side + no_structure) > filter_side:
        print(f"VERDICT  NO QUALIFYING STRUCTURE ({length_side + no_structure} vs "
              f"{filter_side}). Most rejections are\n         the engine correctly "
              f"refusing chop, not a threshold turning work away.\n         Do NOT "
              f"loosen the §4.3 priors to force forks.")
    else:
        print(f"VERDICT  FILTER TIGHTNESS ({filter_side} vs {length_side}). Structure "
              f"EXISTS and the\n         §4.3 priors are rejecting it. Revisit them — "
              f"but pre-register the\n         change from these counts (§10: ten "
              f"parameters is a large overfitting\n         surface). The dominant "
              f"reason above names which prior to look at.")
    print("=" * 60)
    print("REMEMBER: the percentage above is the BIRTH rate, not COVERAGE. A fork")
    print("holds until invalidated (§5.2), so once lifecycle exists one birth")
    print("covers many bars. A low birth rate is expected for a persistent object.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
