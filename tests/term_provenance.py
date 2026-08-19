#!/usr/bin/env python3
"""
tests/term_provenance.py — v1.0 — 2026-08-19   (L1.13)

WHICH SCORER TERMS ACTUALLY MOVE TOGETHER?

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/term_provenance.py ~/day_trader_pro/reports/regime_replay_*.jsonl

────────────────────────────────────────────────────────────────────────────
WHY THIS IS MEASURED AND NOT READ
────────────────────────────────────────────────────────────────────────────
`_combine` is  score = (∏ hard_vetoes) × (∏ soft_necessary) × (Σ w·corroborators).
A corroborator that merely restates a soft-necessary is **the same input
multiplied by itself** — it does not corroborate, it squares.

⚠️ THAT DEFECT IS CONFIRMED IN TRENDING AND IT COST REAL SCORE.
    align_val = max(align_frac, ramp(adx, adx_trend,     ADX_STRONG_SOLO))
    adx_s     =                 ramp(adx, adx_trend - 5, ADX_STRONG_SOLO)
Same input, same upper bound, lower bounds 5 apart. Measured on AMD 2026-08-13:
removing the mask moved the TRENDING score on **110 of 390 ticks (28%)** by a
constant **0.2167** — `W_TREND_ALIGN × (1.0 − 0.667)`. It was inflating TRENDING
by 0.22 on more than a quarter of the session, enough to flip an argmax against
RANGING at p90 0.47.

⚠️ AND READING THE SOURCE IS NOT SUFFICIENT — I GOT TWO CALLS WRONG BY DOING IT.
  · **QQQ 2026-08-17 showed ZERO score movement** from the same fix. `adx_s`
    p50 1.000 and `mom_val` p50 1.000 — fully saturated, no room for a
    corroborator to matter. The duplication only costs where the score is
    GRADING. One session said "inert"; the next said "0.22 on 28% of ticks".
  · **BREAKOUT was flagged on shared provenance and it is complementary, not
    redundant.** `outside_s` is 1.0 when price is outside the band while
    `clear_val` grades the distance; inside, `outside_s` grades on ADX while
    `clear_val` is 0.0. **One is always pinned while the other varies** — the
    opposite of TRENDING, where both ramped the same variable over the same
    range and moved together.

**Shared provenance is not shared behaviour.** This tool measures the second.

────────────────────────────────────────────────────────────────────────────
WHAT IT REPORTS
────────────────────────────────────────────────────────────────────────────
Per regime, for every (soft-necessary × corroborator) pair:
  · **r**        Pearson correlation across ticks where both are defined
  · **n**        pairs compared
  · **pinned**   % of ticks where either term is at 0.0 or 1.0 — a pair cannot
                 be judged on ticks where one of them is a constant

⚠️ HIGH |r| ALONE IS NOT A DEFECT. Two terms measuring genuinely related market
facts SHOULD correlate — `bb_width` and `atr` both describe volatility and a
compression regime is entitled to use both. The defect is a corroborator that is
**the same COMPUTATION** as its damper, which shows as r near 1.0 AND a low
pinned rate AND identical bounds in the source. This tool narrows the list; the
source read confirms it. Neither alone is sufficient.
"""

import argparse
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (regime breakdown key) -> (soft-necessaries, corroborators), from _combine
TERMS = {
    "TRENDING":          (["adx_s"], ["align_val", "mom_val"]),
    "RANGING":           (["flat_s", "room_s"], ["osc_s"]),
    "BREAKOUT_VOLATILE": (["outside_s"], ["expand_val", "clear_val"]),
    "COMPRESSION":       (["narrow_s"], ["atr_contract_val"]),
    "SWEEP_REVERSAL":    (["trend_opp", "age_decay"],
                          ["rejq_val", "exh_val", "spent_val"]),
}


def _pearson(xs, ys):
    n = len(xs)
    if n < 30:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None                     # a constant has no correlation
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", nargs="+")
    a = ap.parse_args(argv[1:])

    files = []
    for pat in a.jsonl:
        files.extend(sorted(glob.glob(os.path.expanduser(pat))))
    if not files:
        print("no replay logs matched. ABSENT MEASUREMENT, not a null.")
        return 1

    cols = {rk: {} for rk in TERMS}
    n_rows = 0
    for fp in files:
        with open(fp) as fh:
            for line in fh:
                if '"breakdown"' not in line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                n_rows += 1
                bds = r.get("breakdown") or {}
                for rk in TERMS:
                    bd = bds.get(rk) or {}
                    if not bd:
                        continue
                    for t in TERMS[rk][0] + TERMS[rk][1]:
                        v = bd.get(t)
                        if isinstance(v, (int, float)):
                            cols[rk].setdefault(t, []).append(float(v))

    print("=" * 84)
    print("TERM PROVENANCE — does a corroborator restate its own soft-necessary?")
    print(f"  {n_rows:,} tick(s) across {len(files)} file(s)")
    print("=" * 84)

    flagged = []
    for rk in sorted(TERMS):
        softs, corrs = TERMS[rk]
        have = cols.get(rk) or {}
        if not have:
            print(f"\n  {rk:20} (no breakdown rows — not scored in this pool)")
            continue
        print(f"\n  {rk}")
        print(f"    {'soft-necessary':18}{'corroborator':18}{'n':>7}{'r':>8}"
              f"{'pinned':>9}  note")
        print("    " + "-" * 70)
        for s_ in softs:
            for c_ in corrs:
                xs, ys = have.get(s_), have.get(c_)
                if not xs or not ys:
                    continue
                m = min(len(xs), len(ys))
                xs, ys = xs[:m], ys[:m]
                # ⚠️ CORRELATE ON THE GRADED SUBSET, NOT THE WHOLE COLUMN.
                # Ramps saturate: two terms both sitting at 1.0 correlate
                # perfectly and tell you nothing. **The question is whether they
                # move together WHERE THEY ARE ACTUALLY MOVING.** A first draft
                # used whole-column r with a pinned-rate filter and dismissed a
                # PLANTED duplication (r=+0.979) as "mostly pinned" — the
                # statistic was measuring co-saturation.
                grd = [(x, y) for x, y in zip(xs, ys)
                       if 0.0 < x < 1.0 and 0.0 < y < 1.0]
                pin_pct = 100.0 * (m - len(grd)) / m if m else 0.0
                r = _pearson([x for x, _ in grd], [y for _, y in grd])
                if r is None:
                    note = ("too few GRADED ticks to judge (%d)" % len(grd)
                            if len(grd) < 30 else "a term is constant here")
                    rtxt = "  -  "
                else:
                    rtxt = f"{r:+.3f}"
                    if abs(r) >= 0.90:
                        note = "*** SAME COMPUTATION? confirm in source ***"
                        flagged.append((rk, s_, c_, r, len(grd)))
                    elif abs(r) >= 0.60:
                        note = "related market fact — not necessarily a defect"
                    else:
                        note = "independent"
                print(f"    {s_:18}{c_:18}{len(grd):>7}{rtxt:>8}{pin_pct:>8.0f}%"
                      f"  {note}")

    print("\n  HOW TO READ IT")
    print("    ⚠️ HIGH |r| ALONE IS NOT A DEFECT. Two terms measuring related")
    print("       market facts SHOULD correlate — bb_width and atr both describe")
    print("       volatility and COMPRESSION is entitled to use both.")
    print("    The defect is a corroborator that is the SAME COMPUTATION as its")
    print("    damper: r near 1.0, a LOW pinned rate, and identical bounds in")
    print("    the source. **This narrows the list; the source read confirms.**")
    print("    ⚠️ AND A PAIR THAT IS MOSTLY PINNED CANNOT BE JUDGED HERE —")
    print("       BREAKOUT's outside_s is 1.0 whenever price is outside the band")
    print("       while clear_val grades, and inside they swap. Complementary,")
    print("       not redundant, and the correlation number will mislead.")
    if flagged:
        print(f"\n  {len(flagged)} pair(s) worth a source read:")
        for rk, s_, c_, r, ng in flagged:
            print(f"    {rk} {s_} vs {c_}  r={r:+.3f} on {ng} graded tick(s)")
    else:
        print("\n  No pair met the flag threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
