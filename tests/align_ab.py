#!/usr/bin/env python3
"""
tests/align_ab.py — v1.1 — 2026-08-19   (L1.12 verification)

DID THE FLAG DO ANYTHING, AND WHY IS TRENDING_BEAR SILENT?

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/align_ab.py /tmp/qqq_align.jsonl /tmp/qqq_max.jsonl

────────────────────────────────────────────────────────────────────────────
WHY
────────────────────────────────────────────────────────────────────────────
The `align` and `max` re-scores of QQQ 2026-08-17 produced **byte-identical**
per-regime output — every regime, every percentile. There are two very
different reasons that can happen and they call for opposite conclusions:

  (a) the flag never reached the scorer, so **the A/B never ran**; or
  (b) the flag worked and `align_val` genuinely does not move TRENDING on this
      tape, because ADX and alignment agreed on every tick that mattered.

⚠️ IDENTICAL OUTPUT MUST NOT BE READ AS "NO EFFECT" UNTIL THE FLAG IS PROVEN
LIVE. That is the same error as reading an absent measurement as a null —
committed three times already this week (the ORB-only probe run, the
`label_day` status string, the sub-noise sweep candidates).

────────────────────────────────────────────────────────────────────────────
AND THE SECOND QUESTION, WHICH IS THE BIGGER ONE
────────────────────────────────────────────────────────────────────────────
`TRENDING_BEAR` scored **0% on every measure** — `>0%`, p50, p90, max, dom — on
a session where price rotated enough that the operator called it a range and
RANGING scored 61% of ticks. **A directional pair with one side structurally
silent is a defect shape, not a market read.** It was 0% on the pre-fix run too,
so it is not something L1.12 introduced.

This reports the BEAR-side inputs beside the BULL-side ones, so "bear never
scores" becomes "bear never scores BECAUSE <term> is always zero" — or is ruled
out as a genuine one-directional session.
"""

import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load(path):
    out = []
    try:
        with open(path) as fh:
            for line in fh:
                if '"scores"' not in line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:                              # noqa: BLE001
                    continue
    except Exception:                                          # noqa: BLE001
        return []
    return out


def _pct(v, p):
    if not v:
        return float("nan")
    s = sorted(v)
    return s[min(len(s) - 1, int(p / 100.0 * len(s)))]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", nargs=2, help="the align run and the max run")
    a = ap.parse_args(argv[1:])

    runs = {}
    for path in a.jsonl:
        tag = "align" if "align" in os.path.basename(path) else "max"
        runs[tag] = _load(path)

    for tag, rows in runs.items():
        if not rows:
            print(f"{tag}: NO ROWS at that path — ABSENT MEASUREMENT, not a null.")
            return 1

    print("=" * 78)
    print("A/B — DID THE ALIGN MODE FLAG ACTUALLY CHANGE ANYTHING?")
    print("=" * 78)

    for tag, rows in sorted(runs.items()):
        diff = same = 0
        av, af = [], []
        for r in rows:
            bd = (r.get("breakdown") or {}).get("TRENDING") or {}
            f, v = bd.get("align_frac"), bd.get("align_val")
            if not isinstance(f, (int, float)) or not isinstance(v, (int, float)):
                continue
            af.append(f)
            av.append(v)
            if abs(f - v) > 1e-9:
                diff += 1
            else:
                same += 1
        n = diff + same
        print(f"\n  {tag:6} ticks with TRENDING breakdown: {n}")
        if n:
            print(f"         align_frac != align_val on {diff} ({100.0*diff/n:.1f}%)")
            print(f"         align_frac  p25 {_pct(af,25):.2f}  p50 {_pct(af,50):.2f}"
                  f"  p95 {_pct(af,95):.2f}")
            print(f"         align_val   p25 {_pct(av,25):.2f}  p50 {_pct(av,50):.2f}"
                  f"  p95 {_pct(av,95):.2f}")

    d_align = runs.get("align") or []
    d_max = runs.get("max") or []
    if d_align and d_max:
        def _mask(rows):
            n = 0
            for r in rows:
                bd = (r.get("breakdown") or {}).get("TRENDING") or {}
                f, v = bd.get("align_frac"), bd.get("align_val")
                if isinstance(f, (int, float)) and isinstance(v, (int, float)) \
                        and abs(f - v) > 1e-9:
                    n += 1
            return n
        m_a, m_m = _mask(d_align), _mask(d_max)
        print("\n  VERDICT ON THE FLAG")
        if m_a == 0 and m_m > 0:
            print("    ✅ THE FLAG IS LIVE. Under `max` the ADX branch masked")
            print(f"       alignment on {m_m} tick(s); under `align` it never does.")
            print("    -> identical per-regime output therefore means the")
            print("       corroborator genuinely does not move TRENDING on this")
            print("       tape: ADX and alignment agreed where it counted.")
        elif m_a == 0 and m_m == 0:
            print("    ❌ INCONCLUSIVE — the mask never fired in EITHER run.")
            print("       Either the env var did not reach the scorer, or ADX")
            print("       never exceeded alignment on this session. **Do not")
            print("       read the identical scores as evidence of anything.**")
        else:
            print(f"    ⚠️ UNEXPECTED: align run shows {m_a} masked tick(s).")
            print("       `align` must never mask — re-check the mode plumbing.")

    # ── v1.1 — COUNT SCORE DELTAS, NOT MASKS ────────────────────────────────
    # ⚠️ v1.0 COUNTED THE WRONG THING. It reported how often the ADX branch
    # masked alignment (145 ticks on QQQ 08-17, 110 on AMD 08-13) and then let
    # me reason about whether the SCORE moved. **The mask is the mechanism; the
    # score is the question.** A mask that fires where `align_frac` is already
    # ~1.0, or where the corroborator sum is already saturated by `mom_val`,
    # changes the mask count and nothing else.
    if d_align and d_max and len(d_align) == len(d_max):
        moved = []
        for ra, rm in zip(d_align, d_max):
            sa = (ra.get("scores") or {})
            sm = (rm.get("scores") or {})
            for k in ("TRENDING_BULL", "TRENDING_BEAR"):
                va, vm = sa.get(k) or 0.0, sm.get(k) or 0.0
                if abs(va - vm) > 1e-9:
                    moved.append((k, va, vm))
        print("\n  DID THE SCORE ACTUALLY MOVE?")
        print(f"    ticks compared: {len(d_align)}")
        print(f"    TRENDING score differs on: {len(moved)}")
        if moved:
            deltas = [abs(a - b) for _k, a, b in moved]
            deltas.sort()
            print(f"    |delta|  p50 {deltas[len(deltas)//2]:.4f}   "
                  f"max {deltas[-1]:.4f}")
            print("    -> the duplication was COSTING something on this tape.")
        else:
            print("    ⚠️ ZERO. The mask fires and the SCORE DOES NOT MOVE.")
            print("       The duplication is real in the code and INERT here:")
            print("       either `align_frac` is already ~1.0 where the mask")
            print("       fires, or `mom_val` (p50 1.000) already saturates the")
            print("       corroborator sum so alignment cannot shift it.")
            print("       **That makes L1.12 a correctness cleanup, not a")
            print("       behaviour fix — and it does NOT justify a bake or a")
            print("       27-session re-score on its own.**")
    elif d_align and d_max:
        print(f"\n  ⚠️ CANNOT COMPARE: {len(d_align)} vs {len(d_max)} ticks. The two")
        print("     runs must cover the same tape or the pairing is meaningless.")

    print("\n" + "=" * 78)
    print("TRENDING_BEAR — 0% ON EVERY MEASURE. WHY?")
    print("=" * 78)
    rows = d_align or d_max
    terms = collections.defaultdict(list)
    bull_n = bear_n = 0
    for r in rows:
        sc = r.get("scores") or {}
        if (sc.get("TRENDING_BULL") or 0) > 0:
            bull_n += 1
        if (sc.get("TRENDING_BEAR") or 0) > 0:
            bear_n += 1
        bd = (r.get("breakdown") or {}).get("TRENDING") or {}
        for k, v in bd.items():
            if isinstance(v, (int, float)):
                terms[k].append(float(v))
    print(f"\n  ticks with BULL > 0: {bull_n}     ticks with BEAR > 0: {bear_n}")
    print(f"\n  {'TRENDING term':22}{'n':>6}{'p10':>8}{'p50':>8}{'p90':>8}{'max':>8}")
    print("  " + "-" * 60)
    for k in sorted(terms):
        v = terms[k]
        print(f"  {k:22}{len(v):>6}{_pct(v,10):>8.3f}{_pct(v,50):>8.3f}"
              f"{_pct(v,90):>8.3f}{max(v):>8.3f}")

    print("\n  ⚠️ THE BREAKDOWN IS SHARED BY BOTH DIRECTIONS — `_trending` scores")
    print("     one TREND and the SIDE is assigned from the trend engine's")
    print("     direction vote. So a term pinned at 0 here does not by itself")
    print("     explain a silent BEAR; a DIRECTION that never reads bearish")
    print("     does. Check `veto_dir` and the trend vote before concluding.")
    print("  ⚠️ AND ON A ONE-WAY SESSION A SILENT BEAR IS CORRECT. QQQ 08-17")
    print("     closed near its highs; the question is whether BEAR is silent")
    print("     ACROSS THE POOL, which needs the 27-session run, not this one.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
