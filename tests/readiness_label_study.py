#!/usr/bin/env python3
"""
tests/readiness_label_study.py — v1.0 — 2026-08-12  (ANT.1)

DOES THE ANTICIPATION LAYER PREDICT? — the test of the project's own premise.

Operator, 2026-08-12: *"This entire project has been building on the premise
that we could assemble a picture from pieces and form our best guess before the
last piece is in place. It's supposed to be our best guess where things are
headed with 80% of the evidence in front of us and relying on conviction that
the other 20% will fill in."*

⚠️ **THAT PREMISE HAS NEVER BEEN TESTED.** What has been tested, and found
wanting, is the CONFLUENCE SCORER — which grades whether the last piece has
ALREADY LANDED. `scorer_backtest` v1.0 measured it across 805 trades and every
continuation dimension came back sep = 0.000, with the A grade INVERTED
(A −$8,244, B +$1,893). Confluence is a lagging indicator by construction: things
agree only after a move is underway, and on a decaying instrument a high score
means you are late.

The readiness layer is the machinery the premise actually describes. It arms
AHEAD of events, holds graded state, and `readiness_digest` v1.4 measured a
**median 7.8-minute lead** from arm to fire with no negative leads. **It is
log-only. Nothing gates on it.** So the project built the anticipation layer and
then gated entries on a lagging one running in parallel.

────────────────────────────────────────────────────────────────────────────
WHAT THIS MEASURES
────────────────────────────────────────────────────────────────────────────
Every readiness row carries `r` (the graded score), `machine` (DORMANT/STAGING/
ARMED), `slope_per_min`, `peak_r` and the per-factor breakdown. This joins each
row to the FORWARD MOVE of the underlying from the harvested tape and asks the
only question that matters:

    when readiness looked like THIS, what happened next?

Reported in the cut-table form used all week: **the threshold that captures the
movement while cutting the fewest quiet ticks.** A floor at winners-p10 that
sits above the losers' p50 is the shape that worked for velocity at 20 minutes
and failed for progress-to-target.

⚠️ **THE SAMPLE IS THE POINT, AND IT IS NOT THE TRADE COUNT.** 805 trade outcomes
is far too few to fit anything — a model built on it memorises 2026. The
readiness layer writes **~8,725 rows per session**; joined to the tape, every one
gets a forward outcome. That is the sample intuition cannot reach, and it is
already being written. **This tool requires NO new collection.**

⚠️ **READINESS IS SPARSE AND THAT LIMITS THE CLAIM.** It journals on state
CHANGE, heartbeat and would-fire — not every tick (`[continuation] ticks=2242`
against ~23,000 actual ticks). So this measures the moments readiness CHOSE to
record, which is a biased sample of the session by construction. A positive
result therefore says "the recorded states predict", not "readiness predicts at
every instant". Denser journaling is a Phase-2 decision, and only worth making
if this comes back positive.

⚠️ FORWARD MOVE IS DIRECTIONLESS (the larger of up and down), matching PRE.1.
Readiness tracks are directional, so availability is necessary and not
sufficient — but a track that cannot even predict AVAILABLE movement cannot
predict a directional outcome either. This is the weaker test, deliberately: if
it fails here it fails everywhere.

READ-ONLY. stdlib only. Reads the signal journal + harvested OHLC.
Touches no fleet, no live path, writes nothing.

USAGE (control)
    python3 tests/readiness_label_study.py --since 2026-07-20
    python3 tests/readiness_label_study.py --since 2026-08-01 --track continuation
"""

import argparse
import collections
import csv
import datetime as dt
import glob
import json
import os
import sys

DTP = os.path.expanduser("~/day_trader_pro")
JOURNAL = os.path.join(DTP, "signal_journal")
OHLC = os.path.join(DTP, "ohlc")
MARKS = (5, 10, 20)


def pctile(v, q):
    v = sorted(v)
    return v[min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))] if v else None


def load_tape(sym, date):
    p = os.path.join(OHLC, date, f"{sym}_ohlc_{date}.csv")
    if not os.path.isfile(p):
        return None, None
    bars = []
    with open(p, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            t = r.get("timestamp") or r.get("time")
            try:
                d = dt.datetime.fromisoformat(t)
                bars.append((d.strftime("%H:%M"), float(r["high"]),
                             float(r["low"]), float(r["close"])))
            except Exception:                                  # noqa: BLE001
                continue
    if not bars:
        return None, None
    return bars, {t: i for i, (t, *_x) in enumerate(bars)}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-07-20")
    ap.add_argument("--track", default="")
    ap.add_argument("--min-n", type=int, default=200)
    a = ap.parse_args(argv[1:])

    dates = sorted(d for d in os.listdir(JOURNAL) if len(d) == 10 and d >= a.since)
    if not dates:
        print(f"no journal folders at/after {a.since}")
        return 1

    rows = []
    nojoin = 0
    for date in dates:
        tapes = {}
        for path in sorted(glob.glob(os.path.join(JOURNAL, date, "*.jsonl"))):
            sym = os.path.basename(path).split(".")[0]
            if sym not in tapes:
                tapes[sym] = load_tape(sym, date)
            bars, imap = tapes[sym]
            if not bars:
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if '"readiness"' not in line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:                          # noqa: BLE001
                        continue
                    if not str(r.get("event", "")).startswith("readiness"):
                        continue
                    strat = r.get("strategy")
                    if a.track and strat != a.track:
                        continue
                    ts = str(r.get("ts_et") or "")[11:16]
                    if ts not in imap:
                        nojoin += 1
                        continue
                    i0 = imap[ts]
                    px = bars[i0][3]
                    if px <= 0:
                        continue
                    fwd = {}
                    for m in MARKS:
                        w = bars[i0:i0 + m + 1]
                        if len(w) < 2:
                            continue
                        hi = max(b[1] for b in w)
                        lo = min(b[2] for b in w)
                        fwd[m] = max((hi - px) / px, (px - lo) / px) * 100.0
                    if not fwd:
                        continue
                    rows.append({
                        "strat": strat, "sym": sym,
                        "r": r.get("r"), "machine": r.get("machine"),
                        "slope": r.get("slope_per_min"), "peak": r.get("peak_r"),
                        "factors": r.get("factors") or {},
                        "fwd": fwd, "hour": int(ts[:2]),
                    })

    if not rows:
        print("no readiness rows joined to tape")
        return 1

    print("=" * 78)
    print(f"  READINESS LABEL STUDY (ANT.1) — {len(dates)} session(s),"
          f" {len(rows):,} labelled readiness rows")
    if nojoin:
        print(f"  ⚠️ {nojoin:,} rows dropped — no tape bar at that minute")
    print(f"  forward move is DIRECTIONLESS; this is the WEAK test on purpose")
    print("=" * 78)

    by = collections.defaultdict(list)
    for x in rows:
        by[x["strat"]].append(x)

    for strat, g in sorted(by.items(), key=lambda kv: -len(kv[1])):
        if len(g) < a.min_n:
            continue
        print(f"\n{'='*78}\n  {strat}   n={len(g):,}")

        # ── does r predict? ────────────────────────────────────────────────
        print(f"\n  FORWARD MOVE BY READINESS SCORE r")
        print(f"    {'r band':14}{'n':>8}" +
              "".join(f"{'p50@'+str(m):>10}" for m in MARKS) +
              "".join(f"{'p90@'+str(m):>10}" for m in MARKS))
        bands = [(0, .2, "0.0-0.2"), (.2, .4, "0.2-0.4"), (.4, .6, "0.4-0.6"),
                 (.6, .8, "0.6-0.8"), (.8, 1.01, "0.8-1.0")]
        seps = {}
        for lo, hi, lab in bands:
            sub = [x for x in g if isinstance(x["r"], (int, float))
                   and lo <= x["r"] < hi]
            if len(sub) < 50:
                continue
            p50 = [pctile([x["fwd"][m] for x in sub if m in x["fwd"]], .5)
                   for m in MARKS]
            p90 = [pctile([x["fwd"][m] for x in sub if m in x["fwd"]], .9)
                   for m in MARKS]
            seps[lab] = p50[1] if len(p50) > 1 else None
            print(f"    {lab:14}{len(sub):>8,}" +
                  "".join(f"{(v if v is not None else 0):>10.3f}" for v in p50) +
                  "".join(f"{(v if v is not None else 0):>10.3f}" for v in p90))
        vals = [v for v in seps.values() if v is not None]
        if len(vals) >= 2:
            lift = (max(vals) - min(vals)) / max(min(vals), 1e-9) * 100
            verdict = ("SEPARATES" if lift >= 25 else
                       ("weak" if lift >= 10 else "FLAT — r does not predict"))
            print(f"    ⇒ spread across r bands at 10 bars: {lift:.0f}%  {verdict}")
            print(f"      ⚠️ a MONOTONE rise is the claim, not merely a spread —")
            print(f"      check the column reads in order before believing it.")

        # ── does the state machine predict? ────────────────────────────────
        print(f"\n  FORWARD MOVE BY MACHINE STATE")
        print(f"    {'machine':14}{'n':>8}" +
              "".join(f"{'p50@'+str(m):>10}" for m in MARKS))
        for st in ("DORMANT", "STAGING", "ARMED"):
            sub = [x for x in g if x["machine"] == st]
            if len(sub) < 50:
                continue
            print(f"    {st:14}{len(sub):>8,}" +
                  "".join(f"{(pctile([x['fwd'][m] for x in sub if m in x['fwd']],.5) or 0):>10.3f}"
                          for m in MARKS))

        # ── does SLOPE predict? the "picture assembling" claim ─────────────
        print(f"\n  FORWARD MOVE BY SLOPE (r per minute) — the 80%%-picture claim")
        print(f"    {'slope band':14}{'n':>8}" +
              "".join(f"{'p50@'+str(m):>10}" for m in MARKS))
        sl = [x for x in g if isinstance(x["slope"], (int, float))]
        if sl:
            qs = sorted(x["slope"] for x in sl)
            cuts = [qs[len(qs)//4], qs[len(qs)//2], qs[3*len(qs)//4]]
            for lo, hi, lab in ((-9e9, cuts[0], "Q1 falling"),
                                (cuts[0], cuts[1], "Q2"),
                                (cuts[1], cuts[2], "Q3"),
                                (cuts[2], 9e9, "Q4 rising")):
                sub = [x for x in sl if lo <= x["slope"] < hi]
                if len(sub) < 50:
                    continue
                print(f"    {lab:14}{len(sub):>8,}" +
                      "".join(f"{(pctile([x['fwd'][m] for x in sub if m in x['fwd']],.5) or 0):>10.3f}"
                              for m in MARKS))
            print(f"    ⚠️ SLOPE IS THE PREMISE'S SHARPEST FORM: a picture ASSEMBLING")
            print(f"       should beat a picture merely HIGH. If Q4 beats the top r")
            print(f"       band, gate on slope; if not, the premise loses its")
            print(f"       distinctive claim even where the level survives.")

    print(f"\n  ── HOW TO READ THIS ──")
    print(f"    A band table that rises MONOTONELY with r is the premise working.")
    print(f"    A flat table is the premise failing on the SAME test the")
    print(f"    confluence scorer failed — and would mean the anticipation layer")
    print(f"    is not merely ungated but not predictive either. That is a real")
    print(f"    answer and it redirects the whole roadmap, so do not soften it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
