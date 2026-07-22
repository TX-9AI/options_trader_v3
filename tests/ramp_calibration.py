# options_trader_v3/tests/ramp_calibration.py — v1.0
"""
Ramp calibration — find WHICH scoring term is saturating and where its ramp
bounds should actually sit, fitted to observed tape instead of priors.

Read-only, offline. Consumes the replay JSONL that validate_regime.sh writes.

For each ramped term it reports:
  * SATURATION  — %% of scored ticks where the term is pegged at 1.0 (and at 0.0).
                  A term pegged most of the time is a switch, not a dial.
  * INPUT SPREAD— percentiles of the raw input feeding that ramp.
  * CURRENT     — the ramp bounds in force today, and what percentile of real
                  tape each bound lands on. A hi-bound sitting at p40 means
                  60%% of ticks max the term out.
  * SUGGESTED   — bounds placed at target percentiles so the ramp spans the
                  range the tape actually occupies.

Nothing is changed. The output is the evidence for a config change.

Usage:
    python -m tests.ramp_calibration                 # auto-discovers sessions
    python -m tests.ramp_calibration --lo-pct 25 --hi-pct 95
    python -m tests.ramp_calibration <explicit.jsonl> ...
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import statistics
import sys
from typing import Dict, List, Optional, Tuple

SEARCH_PATHS = [
    "~/day_trader_pro/reports/regime_replay_*.jsonl",
    "~/day_trader_pro/data/harvest/*/regime_replay_*.jsonl",   # legacy
    "~/day_trader_pro/reports/*/regime_replay_*.jsonl",
]

# (label, regime-breakdown key, input field, scored field, current lo, current hi,
#  higher_input_means_higher_score)
TERMS = [
    ("TRENDING adx_s      (soft-necessary)", "TRENDING", "adx",          "adx_s",   10.0, 35.0, True),
    ("TRENDING align_val  (corroborator)",   "TRENDING", "align_frac",   "align_val", 0.0,  1.0, True),
    ("RANGING  flat_s     (soft-necessary)", "RANGING",  "angle",        "flat_s",  12.0, 20.0, False),
    ("RANGING  room_s     (soft-necessary)", "RANGING",  "bb_width_pct", "room_s",   0.05, 0.20, True),
    ("RANGING  osc_s      (corroborator)",   "RANGING",  "crossings",    "osc_s",    2.0,  5.0, True),
]


def discover() -> List[str]:
    for pat in SEARCH_PATHS:
        hits = sorted(glob.glob(os.path.expanduser(pat)))
        if hits:
            return hits
    return []


def load(paths: List[str]) -> List[dict]:
    recs, loaded = [], []
    for pat in paths:
        for path in sorted(glob.glob(os.path.expanduser(pat))) or [pat]:
            try:
                with open(path) as fh:
                    n0 = len(recs)
                    for line in fh:
                        line = line.strip()
                        if line:
                            recs.append(json.loads(line))
                    loaded.append((os.path.basename(path), len(recs) - n0))
            except FileNotFoundError:
                print(f"  ! not found: {path}", file=sys.stderr)
    if loaded:
        print(f"loaded {len(loaded)} file(s):")
        for name, n in loaded:
            print(f"   {name:<34} {n:>7d} ticks")
        print()
    return recs


def pctile(vals: List[float], p: float) -> Optional[float]:
    if not vals:
        return None
    s = sorted(vals)
    k = (len(s) - 1) * (p / 100.0)
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def pct_rank(vals: List[float], x: float) -> Optional[float]:
    """What percentile of vals does value x sit at?"""
    if not vals:
        return None
    s = sorted(vals)
    below = sum(1 for v in s if v < x)
    return 100.0 * below / len(s)


def collect(recs: List[dict], regime: str, in_key: str,
            out_key: str) -> Tuple[List[float], List[float]]:
    ins, outs = [], []
    for r in recs:
        bd = (r.get("breakdown") or {}).get(regime) or {}
        iv, ov = bd.get(in_key), bd.get(out_key)
        if isinstance(iv, (int, float)):
            ins.append(float(iv))
        if isinstance(ov, (int, float)):
            outs.append(float(ov))
    return ins, outs


def fmt(v: Optional[float], w: int = 7, d: int = 2) -> str:
    return f"{v:>{w}.{d}f}" if v is not None else " " * (w - 3) + "n/a"


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="ramp saturation + bound calibration")
    ap.add_argument("jsonl", nargs="*", help="replay jsonl; omit to auto-discover")
    ap.add_argument("--lo-pct", type=float, default=25.0,
                    help="target percentile for the ramp LOW bound (default 25)")
    ap.add_argument("--hi-pct", type=float, default=95.0,
                    help="target percentile for the ramp HIGH bound (default 95)")
    args = ap.parse_args(argv[1:])

    paths = args.jsonl or discover()
    if not paths:
        print("No replay jsonl found. Looked in:")
        for p in SEARCH_PATHS:
            print(f"   {p}")
        return 2
    recs = load(paths)
    if not recs:
        print("no records loaded")
        return 2

    print("=" * 78)
    print(f"RAMP CALIBRATION — {len(recs)} ticks")
    print("A term pegged at 1.0 on most scored ticks is a SWITCH, not a dial.")
    print("=" * 78)

    for label, regime, in_key, out_key, cur_lo, cur_hi, ascending in TERMS:
        ins, outs = collect(recs, regime, in_key, out_key)
        if not outs:
            print(f"\n{label}\n   (no data)")
            continue

        n = len(outs)
        peg1 = sum(1 for v in outs if v >= 0.999)
        peg0 = sum(1 for v in outs if v <= 0.001)
        mid = n - peg1 - peg0

        print(f"\n{label}")
        print(f"   SATURATION   pegged 1.0: {100.0*peg1/n:5.1f}%   "
              f"pegged 0.0: {100.0*peg0/n:5.1f}%   "
              f"graded in between: {100.0*mid/n:5.1f}%")

        if ins:
            ps = {p: pctile(ins, p) for p in (5, 25, 50, 75, 90, 95, 99)}
            print(f"   INPUT {in_key:<13} p5{fmt(ps[5])}  p25{fmt(ps[25])}  "
                  f"p50{fmt(ps[50])}  p75{fmt(ps[75])}  p90{fmt(ps[90])}  "
                  f"p95{fmt(ps[95])}  p99{fmt(ps[99])}")
            r_lo, r_hi = pct_rank(ins, cur_lo), pct_rank(ins, cur_hi)
            print(f"   CURRENT      lo={cur_lo:<7g} (input p{r_lo:.0f})   "
                  f"hi={cur_hi:<7g} (input p{r_hi:.0f})")
            if ascending:
                s_lo, s_hi = pctile(ins, args.lo_pct), pctile(ins, args.hi_pct)
            else:
                # descending input (e.g. angle): low score at high angle
                s_lo, s_hi = pctile(ins, 100 - args.hi_pct), pctile(ins, 100 - args.lo_pct)
            print(f"   SUGGESTED    lo={s_lo:<7.2f}(p{args.lo_pct:.0f})   "
                  f"hi={s_hi:<7.2f}(p{args.hi_pct:.0f})", end="")
            if r_hi is not None and r_hi < 60:
                print("   <-- hi bound is too low; term maxes out on ordinary tape")
            else:
                print()

    print("\n" + "=" * 78)
    print("Reading this: a term with <25% 'graded in between' is behaving as a")
    print("switch. Moving its hi bound out to a genuinely rare percentile restores")
    print("grading. Do NOT push a bound past ~p99 of real tape or the term becomes")
    print("unreachable — the failure v3.1 just fixed, in reverse.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
