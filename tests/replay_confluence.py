#!/usr/bin/env python3
# tests/replay_confluence.py — options_trader_v3
# v2.0 — 2026-07-12 — LAYER-2 TRACKS + drift merge.
#   (a) MERGE: absorbs the control-box local mod (--report-only: rebuild + reprint
#       the full report from a saved tick-log JSONL; no engines, no re-scoring)
#       that never reached GitHub — ends the two-way drift where the repo had
#       v1.1's sibling-skip and control had report-only, neither had both.
#   (b) LAYER-2: each symbol-session's per-tick evidence vector is now ALSO fed,
#       in time order, through a fresh ConvictionIntegrator (v2.0, always-argmax).
#       Every JSONL record gains an "l2" object {regime, c, stale, cv[, trigger]}
#       and the report gains a LAYER-2 section: emitted-label distribution,
#       label SWITCHES per symbol-session vs L1-argmax flips (the churn metric
#       the integrator exists to crush), and stale%. Purely additive: CLI args,
#       exit codes (0 pass / 2 acceptance-fail), and every existing JSONL field
#       are unchanged — regime_diary/regime_backfill/validate_regime.sh work
#       as-is; L2 report prints only when l2 fields are present (old logs
#       reprint cleanly under --report-only). Layer-1 acceptance checks remain
#       the sole exit-code authority; L2 is observational until L2 targets land.
# v1.1 — 2026-07-11 — skip non-OHLC siblings in harvest folders (fleet_trades_*.csv,
#         *_trades_*.db, daily_trades_*.json) that share data/harvest/<date>/ with the
#         tape; load_ohlc returns None on a missing timestamp column. v1.0 crashed at
#         the report step on the consolidated fleet_trades CSV. No scoring-logic change.
#   Layer-1 VALIDATION + CALIBRATION harness. Replays analysis/regime_confluence.py
#   over the candle logger's DXFeed 1-min OHLC (data/OHLC/<date>/<SYMBOL>.csv) — the
#   traded tape, store-consistent per ROADMAP (NOT the live yfinance observer feed).
#
#   Method: AS-OF replay. For each 1-min bar t of the session, slice every timeframe
#   frame to bars ≤ t, run the REAL engines (volatility/trend/structure/liquidity —
#   the same code the live bot runs), then score the resulting states with the real
#   RegimeConfluenceScorer. Optionally logs the v1.3 boolean regime for comparison.
#
#   Emits: (1) per-regime score distributions, (2) per-FACTOR distributions split by
#   the v1.3 label (the calibration gold — e.g. flat-angle on RANGING vs TRENDING
#   ticks), (3) the Layer-1 acceptance checks (see REPLAY_VALIDATION.md). No Layer-2
#   behavior is invoked — this validates instantaneous scores only.
#
#   Run (on-box, repo root):  python -m tests.replay_confluence data/OHLC/2026-07-13
#         or specific files:   python -m tests.replay_confluence path/to/SPX.csv ...
#         options:  --jsonl out.jsonl   --warmup 20   --no-v13
#
#   Isolation: reads OHLC + runs engines only. Places no orders, opens no trades.db,
#   writes only the report (+ optional --jsonl). Safe to run anytime.

from __future__ import annotations
import argparse, os, re, sys, json, math, warnings
from typing import Dict, List, Optional, Tuple
import pandas as pd
# volume-less index tape (e.g. cash SPX logs volume=0) makes the engine VWAP a 0/0;
# our scorer reads price_vs_bb, not VWAP, so it does not affect scores — quiet the noise.
warnings.filterwarnings("ignore", category=RuntimeWarning)

# --- repo engines (this harness is repo-bound by design; regime_confluence is not) --
from analysis.volatility_engine import get_volatility_engine
from analysis.trend_engine import get_trend_engine
from analysis.structure_analyzer import get_structure_analyzer
from analysis.liquidity_mapper import get_liquidity_mapper
from analysis.regime_confluence import (
    RegimeConfluenceScorer, REGIMES, RANGE_WINDOW_BARS,
    TRENDING_BULL, TRENDING_BEAR, RANGING, BREAKOUT_VOLATILE, COMPRESSION, SWEEP_REVERSAL,
)

try:
    from analysis.regime_classifier import get_regime_classifier
    _HAVE_V13 = True
except Exception:
    _HAVE_V13 = False

# Layer 2 (v2.0): optional so a mid-sync checkout without the ported integrator
# still replays Layer 1 — the L2 fields/report simply don't appear.
try:
    from analysis.conviction_integrator import ConvictionIntegrator
    _HAVE_L2 = True
except Exception:
    _HAVE_L2 = False


# ── CSV load (candle-logger tape: footer junk, zero-range pads, CRLF, ISO8601 tz) ──
def load_ohlc(path: str) -> Optional[pd.DataFrame]:
    raw = pd.read_csv(path, header=0, dtype=str)
    raw.columns = [c.strip().lower() for c in raw.columns]
    # Not an OHLC tape file (e.g. harvest's fleet_trades_<date>.csv sits in the same
    # folder): no timestamp column → skip gracefully rather than crash the run.
    if "timestamp" not in raw.columns:
        return None
    ts = pd.to_datetime(raw["timestamp"], format="ISO8601", errors="coerce")
    ok = ts.notna()
    df = raw[ok].copy()
    df.index = ts[ok]
    for c in ["open", "high", "low", "close", "volume"]:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"])
    zr = (df.high == df.low) & (df.open == df.close) & (df.high == df.close)
    return df[~zr][["open", "high", "low", "close", "volume"]]


_AGG = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}


def resample(df1m: pd.DataFrame, rule: str) -> pd.DataFrame:
    return df1m.resample(rule, label="right", closed="right").agg(_AGG).dropna(subset=["close"])


def sym_of(path: str) -> str:
    return re.split(r"[_.]", os.path.basename(path))[0].upper()


# ── distribution helper ───────────────────────────────────────────────────────
def dist(xs: List[float]) -> dict:
    xs = sorted(v for v in xs if v is not None)
    if not xs:
        return {"n": 0}
    n = len(xs)
    q = lambda p: xs[min(n - 1, int(p * n))]
    return {"n": n, "min": round(xs[0], 3), "p10": round(q(.10), 3),
            "p50": round(q(.50), 3), "p90": round(q(.90), 3), "max": round(xs[-1], 3)}


# ── one symbol replay ─────────────────────────────────────────────────────────
def replay_symbol(path: str, warmup: int, use_v13: bool) -> Tuple[List[dict], str]:
    sym = sym_of(path)
    df1m = load_ohlc(path)
    if df1m is None or len(df1m) < warmup + 5:
        return [], sym
    d5, d15, d1h = resample(df1m, "5min"), resample(df1m, "15min"), resample(df1m, "1h")

    volE, trE, stE, lqE = (get_volatility_engine(), get_trend_engine(),
                           get_structure_analyzer(), get_liquidity_mapper())
    scorer = RegimeConfluenceScorer()
    clf = get_regime_classifier() if (use_v13 and _HAVE_V13) else None
    integ = ConvictionIntegrator() if _HAVE_L2 else None   # fresh book per symbol-session

    recs: List[dict] = []
    idx1m = df1m.index
    for i in range(warmup, len(df1m)):
        t = idx1m[i]
        price = float(df1m["close"].iloc[i])
        # as-of slices (only bars that had closed by t)
        s5  = d5[d5.index <= t]
        s15 = d15[d15.index <= t]
        s1h = d1h[d1h.index <= t]
        s1m = df1m.iloc[: i + 1]
        if s5.empty:
            continue
        s1h_safe = s1h if not s1h.empty else s5
        try:
            vol = volE.analyze(s5, s1h_safe, price)
            trend = trE.analyze({"1m": s1m, "5m": s5, "15m": s15, "1h": s1h})
            structure = stE.analyze(s5, s15, s1h if not s1h.empty else None, price)
            liq = lqE.analyze(s5, s15, price)
        except Exception as e:            # engine hiccup on thin early tape — skip bar
            continue

        closes = s1m["close"].tolist()[-RANGE_WINDOW_BARS:]
        atr = getattr(vol, "atr_current", None)
        res = scorer.score(vol, trend, structure, liq, closes=closes, atr=atr)

        rec = {"ts": t.strftime("%H:%M"), "sym": sym, "price": price,
               "scores": res.scores, "breakdown": res.breakdown}
        if integ is not None:
            st = integ.update(t.timestamp(), res.evidence())
            l2 = {"regime": st.regime, "c": round(st.conviction, 3),
                  "stale": bool(st.stale),
                  "cv": {k: round(v, 3) for k, v in st.convictions.items()}}
            if st.trigger:
                l2["trigger"] = st.trigger
            rec["l2"] = l2
        if clf is not None:
            try:
                rc = clf.classify(vol, trend, structure, liq, macro=None, trigger="replay")
                rec["v13"] = rc.primary_regime
            except Exception:
                rec["v13"] = "ERR"
        recs.append(rec)
    return recs, sym


# ── acceptance checks (Layer-1 only — instantaneous scores, no L2) ────────────
def acceptance(recs: List[dict]) -> List[Tuple[str, bool, str]]:
    out = []
    if not recs:
        return [("has ticks", False, "no replayed ticks")]

    def sc(r, k): 
        v = r["scores"].get(k); return v if v is not None else 0.0

    n = len(recs)
    # A1 — score bounds: every score is None or ∈ [0,1]
    bad = [k for r in recs for k, v in r["scores"].items() if v is not None and not (0.0 <= v <= 1.0)]
    out.append(("A1 scores in [0,1] or None", not bad, f"{len(bad)} out-of-range" if bad else "ok"))

    # A2 — flat-veto mutual exclusion: TRENDING and RANGING never BOTH strong (>0.5)
    both = sum(1 for r in recs if (sc(r, TRENDING_BULL) > .5 or sc(r, TRENDING_BEAR) > .5) and sc(r, RANGING) > .5)
    out.append(("A2 TREND & RANGE not both >0.5 (flat veto)", both == 0, f"{both} violating ticks"))

    # A3 — BREAKOUT and COMPRESSION never both strong (opposite width axis)
    both_bc = sum(1 for r in recs if sc(r, BREAKOUT_VOLATILE) > .5 and sc(r, COMPRESSION) > .5)
    out.append(("A3 BREAKOUT & COMPRESSION not both >0.5", both_bc == 0, f"{both_bc} violating ticks"))

    # A4 — structure-contradiction veto: no tick has TRENDING_BULL>0 with LH_LL structure
    viol = sum(1 for r in recs
               if sc(r, TRENDING_BULL) > 0 and r["breakdown"].get("TRENDING", {}).get("structure_sequence") == "LH_LL")
    out.append(("A4 no TREND_BULL under LH_LL structure", viol == 0, f"{viol} violating ticks"))

    # A5 — no global abstention: every tick has at least one regime scoring >0
    silent = sum(1 for r in recs if all(sc(r, k) == 0.0 for k in REGIMES))
    out.append(("A5 no all-zero ticks (UNKNOWN eliminated)", silent / n < 0.15,
                f"{silent}/{n} ({100*silent/n:.0f}%) all-zero — target <15%"))
    return out


# ── report ────────────────────────────────────────────────────────────────────
def report(all_recs: List[dict], jsonl: Optional[str]):
    if jsonl:
        with open(jsonl, "w") as f:
            for r in all_recs:
                f.write(json.dumps(r) + "\n")

    n = len(all_recs)
    print(f"\n{'='*70}\nLAYER-1 REPLAY — {n} ticks across "
          f"{len(set(r['sym'] for r in all_recs))} symbol-sessions\n{'='*70}")

    # 1) per-regime score distribution + share of ticks scoring dominant
    print("\n── per-regime instantaneous score distribution ──")
    print(f"{'regime':18}{'>0%':>6}{'p50':>7}{'p90':>7}{'max':>7}{'dom%':>7}")
    for k in REGIMES:
        vals = [r["scores"].get(k) for r in all_recs]
        nz = [v for v in vals if v is not None and v > 0]
        dom = sum(1 for r in all_recs
                  if (r["scores"].get(k) or 0) == max((r["scores"].get(x) or 0) for x in REGIMES)
                  and (r["scores"].get(k) or 0) > 0)
        d = dist([v for v in vals if v is not None])
        print(f"{k:18}{100*len(nz)/n:5.0f}%{d.get('p50',0):7}{d.get('p90',0):7}"
              f"{d.get('max',0):7}{100*dom/n:6.0f}%")

    # 2) CALIBRATION: flat-angle distribution split by v1.3 label (top priority knob)
    have_v13 = any("v13" in r for r in all_recs)
    if have_v13:
        print("\n── CALIBRATION: flat-angle° by v1.3 label (sets FLAT_ANGLE_CUT_DEG) ──")
        by = {}
        for r in all_recs:
            ang = r["breakdown"].get("RANGING", {}).get("angle")
            if ang is None:
                ang = r["breakdown"].get("COMPRESSION", {}).get("angle")
            if ang is not None:
                by.setdefault(r.get("v13", "?"), []).append(ang)
        print(f"{'v1.3 label':20}{'n':>6}{'min':>7}{'p10':>7}{'p50':>7}{'p90':>7}{'max':>7}")
        for lbl, xs in sorted(by.items(), key=lambda kv: -len(kv[1])):
            d = dist(xs)
            print(f"{lbl:20}{d['n']:6}{d.get('min',0):7}{d.get('p10',0):7}"
                  f"{d.get('p50',0):7}{d.get('p90',0):7}{d.get('max',0):7}")
        print("  → calibration read: the cut belongs between the RANGING p90 and the")
        print("    TRENDING p10 of this column, swept 16–26° on multi-day tape.")

    # 3) label agreement (context only — NOT a Layer-1 acceptance metric)
    if have_v13:
        def top(r):
            best = max(REGIMES, key=lambda k: (r["scores"].get(k) or 0))
            return best if (r["scores"].get(best) or 0) > 0 else "NONE"
        agree = sum(1 for r in all_recs if r.get("v13") == top(r))
        print(f"\n── L1-argmax vs v1.3 label agreement: {100*agree/n:.0f}%  "
              f"(context only; L1 argmax ≠ L2 committed label)")

    # 3b) LAYER-2 tracks (v2.0) — printed only when the log carries l2 fields
    l2recs = [r for r in all_recs if r.get("l2")]
    if l2recs:
        print("\n── LAYER-2 (conviction integrator, always-argmax) ──")
        m = len(l2recs)
        emitted = {}
        for r in l2recs:
            emitted[r["l2"]["regime"]] = emitted.get(r["l2"]["regime"], 0) + 1
        dist_line = "  ".join(f"{k.split('_')[0][:5]} {100*v/m:.0f}%"
                              for k, v in sorted(emitted.items(), key=lambda kv: -kv[1]))
        stale_n = sum(1 for r in l2recs if r["l2"].get("stale"))
        print(f"  emitted: {dist_line}")
        # churn: L2 label switches vs L1 argmax flips, per symbol-session
        def _top1(r):
            return max(REGIMES, key=lambda k: (r["scores"].get(k) or 0))
        sw_tot = fl_tot = 0
        per_sym = []
        by_sym: Dict[str, List[dict]] = {}
        for r in l2recs:
            by_sym.setdefault(r["sym"], []).append(r)
        for s, rs in sorted(by_sym.items()):
            sw = sum(1 for a, b in zip(rs, rs[1:]) if a["l2"]["regime"] != b["l2"]["regime"])
            fl = sum(1 for a, b in zip(rs, rs[1:]) if _top1(a) != _top1(b))
            sw_tot += sw; fl_tot += fl
            per_sym.append((s, sw, fl))
        ratio = f"{fl_tot/max(sw_tot,1):.1f}x" if sw_tot else "∞"
        print(f"  label switches: {sw_tot} vs L1-argmax flips: {fl_tot}  "
              f"(churn crushed {ratio})   stale ticks: {100*stale_n/m:.0f}%")
        worst = sorted(per_sym, key=lambda x: -x[1])[:5]
        if worst and worst[0][1] > 0:
            print("  switchiest: " + "  ".join(f"{s}:{sw}" for s, sw, _ in worst if sw > 0))

    # 4) acceptance checks
    print("\n── LAYER-1 ACCEPTANCE ──")
    checks = acceptance(all_recs)
    for name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}  — {detail}")
    n_pass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n{n_pass}/{len(checks)} acceptance checks passed")
    return n_pass == len(checks)


def gather_paths(args_paths: List[str]) -> List[str]:
    out = []
    for p in args_paths:
        if os.path.isdir(p):
            # only OHLC tape files — harvest folders also hold fleet_trades_<date>.csv,
            # daily_trades_<date>.json, and per-box *_trades_<date>.db siblings.
            names = sorted(os.listdir(p))
            ohlc = [f for f in names if "_ohlc_" in f.lower() and f.lower().endswith((".csv", ".csv.gz"))]
            # fall back to any .csv only if no OHLC-named files exist (e.g. a bare dir)
            picked = ohlc if ohlc else [f for f in names if f.lower().endswith((".csv", ".csv.gz"))]
            out += [os.path.join(p, f) for f in picked]
        else:
            out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser(description="Layer-1 confluence replay over DXFeed OHLC")
    ap.add_argument("paths", nargs="*", help="CSV files or a data/OHLC/<date>/ directory")
    ap.add_argument("--warmup", type=int, default=20, help="skip first N 1-min bars")
    ap.add_argument("--jsonl", default=None, help="dump per-tick records to this JSONL")
    ap.add_argument("--no-v13", action="store_true", help="skip the v1.3 comparison label")
    ap.add_argument("--report-only", default=None, metavar="JSONL",
                    help="rebuild + reprint the full report from a saved tick-log JSONL "
                         "(no engines, no re-scoring — the report is deterministic from the log)")
    args = ap.parse_args()

    # --report-only: reload a saved per-tick log and reprint the identical report.
    if args.report_only:
        if not os.path.isfile(args.report_only):
            print(f"no tick log at {args.report_only}"); sys.exit(1)
        all_recs = []
        with open(args.report_only) as f:
            for line in f:
                line = line.strip()
                if line:
                    all_recs.append(json.loads(line))
        if not all_recs:
            print(f"tick log is empty: {args.report_only}"); sys.exit(1)
        print(f"[report-only] rebuilt from {len(all_recs)} saved ticks — {args.report_only}")
        ok = report(all_recs, jsonl=None)   # jsonl=None: don't re-dump, just print
        sys.exit(0 if ok else 2)

    if not args.paths:
        ap.error("provide OHLC paths to replay, or --report-only <jsonl> to reprint a saved run")

    paths = gather_paths(args.paths)
    all_recs: List[dict] = []
    for p in paths:
        recs, sym = replay_symbol(p, args.warmup, use_v13=not args.no_v13)
        print(f"  replayed {sym:6} {len(recs):4d} ticks  ({os.path.basename(p)})")
        all_recs += recs

    if not all_recs:
        print("no ticks replayed — check paths / warmup")
        sys.exit(1)
    ok = report(all_recs, args.jsonl)
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
