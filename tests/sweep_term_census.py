#!/usr/bin/env python3
"""
tests/sweep_term_census.py — v1.0 — 2026-08-19   (SWP.9)

WHICH TERM CAPS THE SWEEP SCORE?

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/sweep_term_census.py

────────────────────────────────────────────────────────────────────────────
THE QUESTION
────────────────────────────────────────────────────────────────────────────
Across **1,564 named-pool sweeps in 27 sessions the SWEEP ceiling is 0.171**
out of 1.0. TRENDING pins at 1.00 and RANGING reaches p90 0.615, so SWEEP loses
the L1 argmax by construction — and the hard label gate at `main.py:1325` was
never the binding constraint. **Ungating a score that cannot win the argmax
changes nothing.**

`_combine` is
    score = (∏ hard_vetoes) × (∏ soft_necessary) × (Σ w·corroborators)

and the soft-necessary count is NOT the same across regimes:

    TRENDING   1 damper   (adx_s)
    BREAKOUT   1 damper   (outside_s)
    RANGING    2 dampers  (flat_s, room_s)
    SWEEP      2 dampers  (trend_opp, age_decay)

⚠️ BUT TWO DAMPERS IS NOT AUTOMATICALLY FATAL — **RANGING also has two and
still reaches 0.615.** So SWEEP's ceiling is about the VALUES its terms take,
not merely how many there are. This tool reports the distribution of every term
so the binding one is identified rather than assumed.

⚠️ AND THERE ARE **TWO SEPARATE MECHANISMS**, which the report's `closes_beyond`
column already hints at: the qualifying rows show **1**, the zero-scoring ones
show **9, 87, 90**. Most sweeps are not scoring low — they are **HARD-VETOED to
exactly 0.000** by `closes_beyond >= 2` before any multiplication happens.
(Measured 2026-08-15: that veto blocks 64.5% of named-pool ticks, and of 25,792
vetoed ticks post-08-11, **100% were reclaimed and 0% were genuine acceptance**.)
Reporting the two populations separately is the whole point — averaging them
would hide both.

⚠️ READ-ONLY. Reads the replay logs; touches no box, changes no behaviour.
"""

import argparse
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPLAY = os.path.expanduser("~/day_trader_pro/reports/regime_replay_*.jsonl")

# every term `_sweep` puts in its breakdown, in evaluation order
VETOES = ["veto_loc", "veto_reclaim", "veto_accept"]
DAMPERS = ["trend_opp", "age_decay"]
CORROB = ["rejq_val", "exh_val", "spent_val"]


def _pct(vals, p):
    if not vals:
        return float("nan")
    s = sorted(vals)
    return s[min(len(s) - 1, int(p / 100.0 * len(s)))]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", default=REPLAY)
    ap.add_argument("--min-score", type=float, default=0.0001,
                    help="rows at/below this are treated as VETOED")
    a = ap.parse_args(argv[1:])

    files = sorted(glob.glob(os.path.expanduser(a.replay)))
    if not files:
        print(f"no replay logs at {a.replay}")
        print("  ABSENT MEASUREMENT, not a null.")
        return 1

    scored = collections.defaultdict(list)      # term -> values, score > 0
    vetoed = collections.defaultdict(list)      # term -> values, score == 0
    n_rows = n_scored = n_vetoed = 0
    veto_hits = collections.Counter()
    peak = 0.0

    for fp in files:
        with open(fp) as fh:
            for line in fh:
                if "SWEEP_REVERSAL" not in line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                bd = (r.get("breakdown") or {}).get("SWEEP_REVERSAL") or {}
                if not bd or not bd.get("named"):
                    continue          # only NAMED pools — the acceptance shape
                n_rows += 1
                sc = float(bd.get("score", 0.0) or 0.0)
                peak = max(peak, sc)
                bucket = scored if sc > a.min_score else vetoed
                if sc > a.min_score:
                    n_scored += 1
                else:
                    n_vetoed += 1
                    for v in VETOES:
                        if bd.get(v) in (0, 0.0, False):
                            veto_hits[v] += 1
                for t in DAMPERS + CORROB:
                    val = bd.get(t)
                    if isinstance(val, (int, float)):
                        bucket[t].append(float(val))

    if not n_rows:
        print("no NAMED sweep breakdowns found in the replay logs.")
        print("  ABSENT MEASUREMENT, not a null — check that the logs carry")
        print("  `breakdown.SWEEP_REVERSAL` (replay_confluence writes it).")
        return 1

    print("=" * 82)
    print("SWEEP TERM CENSUS — which term caps the score?")
    print(f"  {n_rows:,} named-pool sweep row(s) across {len(files)} session file(s)")
    print(f"  observed peak score: {peak:.4f}   (TRENDING pins at 1.00, "
          f"RANGING p90 ~0.615)")
    print("=" * 82)

    print(f"\n  TWO POPULATIONS — these must not be averaged together:")
    print(f"    VETOED to ~0 : {n_vetoed:>6}  ({100.0*n_vetoed/n_rows:.1f}%)")
    print(f"    SCORED  > 0  : {n_scored:>6}  ({100.0*n_scored/n_rows:.1f}%)")
    if veto_hits:
        print("\n  WHICH HARD VETO FIRED (on the vetoed population)")
        for v, c in veto_hits.most_common():
            print(f"    {v:16}{c:>7}  ({100.0*c/max(1,n_vetoed):.1f}% of vetoed)")
        print("    ⚠️ `veto_accept` is the `closes_beyond >= 2` rule. Measured")
        print("       2026-08-15: it blocks 64.5% of named-pool ticks, and of")
        print("       25,792 vetoed ticks post-08-11, **100% were reclaimed and")
        print("       0% were genuine acceptance** — it reads bodies inside the")
        print("       rejection sequence as acceptance.")

    print(f"\n  TERM DISTRIBUTION ON THE SCORED POPULATION (n={n_scored})")
    print(f"    {'term':14}{'role':12}{'n':>6}{'p10':>8}{'p50':>8}{'p90':>8}{'max':>8}")
    print("    " + "-" * 64)
    for t in DAMPERS + CORROB:
        v = scored.get(t, [])
        if not v:
            continue
        role = "DAMPER (x)" if t in DAMPERS else "corrob (+)"
        print(f"    {t:14}{role:12}{len(v):>6}{_pct(v,10):>8.3f}"
              f"{_pct(v,50):>8.3f}{_pct(v,90):>8.3f}{max(v):>8.3f}")

    d = [scored.get(t, []) for t in DAMPERS]
    if all(d):
        prod50 = 1.0
        for t in DAMPERS:
            prod50 *= _pct(scored[t], 50)
        print(f"\n  THE MULTIPLICATIVE CEILING")
        print(f"    dampers at their medians multiply to {prod50:.3f}")
        print(f"    so even PERFECT corroborators (1.0) cap the score at {prod50:.3f}")
        print(f"    -> observed peak {peak:.3f}")
        print("    ⚠️ A regime with TWO necessary conditions is structurally")
        print("       handicapped in an argmax against TRENDING's ONE (adx_s).")
        print("       But RANGING also has two and reaches 0.615 — so the")
        print("       binding constraint is the VALUES above, not the count.")

    print("\n  ⚠️ NOTHING IS PROPOSED HERE. This says which term is smallest, not")
    print("     what it should be. Re-fitting a damper to lift SWEEP into the")
    print("     argmax would be fitting the score to the outcome we want — the")
    print("     grade-inversion error at a different layer.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
