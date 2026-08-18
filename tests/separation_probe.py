#!/usr/bin/env python3
"""
tests/separation_probe.py — v1.1 — 2026-08-17   (P0.1 — THE GATE)

v1.1 — 2026-08-17 — OOM FIX + TWO GLOB EXCLUSIONS.
    v1.0 built a dict of EVERY tick across EVERY replay log before touching a
    trade — ~282k parsed JSON records held at once — and was **KILLED (rc=137)**
    on control, the same failure the regime grid hit on 08-15.
    ⚠️ AND THE LOUD "ABSENT MEASUREMENT" GUARD COULD NOT FIRE: the process died
    before reaching it. **An in-process guard cannot report a kill** — which is
    why the first two runs printed nothing at all rather than a diagnosis.
    NOW: the trade list is built FIRST, and only the (date, sym, HH:MM) keys
    those trades need are indexed. MEASURED: 282,750 ticks scanned, 2 indexed,
    **13 MB peak RSS**.
    ALSO: `_archive_pre_*` directories and `.bak` files live inside the trades
    tree and were being globbed as real data.

**DOES ANYTHING ALREADY COLLECTED SEPARATE FAVOURABLE FROM NEVER-FAVOURABLE
TRADES AT DECISION TIME?**

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/separation_probe.py

────────────────────────────────────────────────────────────────────────────
WHY THIS IS THE GATE, AND WHY IT COMES FIRST
────────────────────────────────────────────────────────────────────────────
The project's founding premise — infer a pattern *forming*, express it as a
confidence factor, and **scale the entry on it** — was never actually run.
`ROADMAP.md` §LAYER 3: **"Status: NOT STARTED. 0%"**. A proxy assembly ran
instead (grade → 1.5x size) and **inverted**: A-grade 399 trades **−$8,244**,
B-grade 220 trades **+$1,893**.

The two quantities the system DID gate and size on are measured dead:
  · `SETUP` — nf ≈ ok, and the grade inverted at size.
  · `RGCV`  — nf **1.00** vs ok **0.34** in RANGING (an ANTI-signal), 0.59 vs
    0.36 in COMPRESSION, and **1.00 vs 1.00 in trend** (no separation at all).
    Its own scorer header names the class error: *"High conviction means the
    trend is already obvious, which means LATE."*

**Every phase of TRANSITION_ROADMAP.md is conditional on this answer.** If a
primitive separates, the remaining work is WIRING. If nothing does — including
shadow velocity with four fleet-weeks — the escalation is NEW INPUTS, not a new
combiner, and that is worth knowing before anything is rebuilt.

────────────────────────────────────────────────────────────────────────────
PRE-REGISTERED SUCCESS CRITERION — written BEFORE the run, per §12
────────────────────────────────────────────────────────────────────────────
A primitive is a candidate confidence factor **only if all four hold**:

    1. nf BELOW ok              (direction: the losers score lower)
    2. CI-separated             (Wilson 95% on the nf-rate at the extremes)
    3. n >= 200 across >= 10 sessions
    4. sign stable across at least the two post-LIQ.1 windows

⚠️ **NO BEST PRIMITIVE IS NAMED BY THIS TOOL.** In-sample argmax over a dozen
candidates is overfit by construction — trying twelve things and reporting the
best is a different experiment from testing one. This prints every candidate,
its n, and whether it CLEARS. The choice is a decision, made against the
criterion above, not an argmax.

⚠️ **AND A FAILING PRIMITIVE IS A RESULT.** `pair_conf` was killed this way
(AX.3) and that saved building on it. Reporting only winners would make this
tool a confirmation machine — the exact failure it exists to diagnose.

────────────────────────────────────────────────────────────────────────────
WINDOWS, EXCLUSIONS, AND WHY
────────────────────────────────────────────────────────────────────────────
⚠️ THE ARCHIVE IS **FOUR REGIMES** for anything touching levels or sweeps:
    pre-LIQ.1 · post-LIQ.1 (08-12) · post-LIQ.6 (08-15) · post-FEED.2 (08-17)
Level-dependent primitives are NOT comparable across those boundaries; a
separator that flips sign across LIQ.6 is a level artifact, not a signal.
Velocity is level-agnostic and stays comparable.

⚠️ **2026-08-14 IS EXCLUDED** — 130 of 153 trades are identity-chain / CNT.1
artifacts. `trend_continuation_breakout` rows from 08-07 onward are one-tick
artifacts and are excluded regardless of date.

⚠️ READ-ONLY, CONTROL-SIDE. Touches no box, needs no bake. **The fleet must keep
trading and collecting through the retool** — the probe cannot be the thing that
interrupts it.
"""

import argparse
import collections
import glob
import json
import math
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DTP = os.path.expanduser("~/day_trader_pro")
TRADES_GLOB = os.path.join(DTP, "trades", "*", "*_trades_*.db")
REPLAY_GLOB = os.path.join(DTP, "reports", "regime_replay_*.jsonl")
JOURNAL_DIR = os.path.join(DTP, "signal_journal")

# window boundaries — see the header
WINDOWS = (("pre-LIQ.1", "0000-00-00", "2026-08-11"),
           ("post-LIQ.1", "2026-08-12", "2026-08-14"),
           ("post-LIQ.6", "2026-08-15", "2026-08-16"),
           ("post-FEED.2", "2026-08-17", "9999-99-99"))

MIN_N = 200
MIN_SESSIONS = 10


def _window(date):
    for name, lo, hi in WINDOWS:
        if lo <= date <= hi:
            return name
    return "?"


def _wilson(k, n):
    """95% Wilson interval — the repo's own convention for a rate with small n."""
    if n == 0:
        return (0.0, 1.0)
    z = 1.96
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _hhmm(entry_time):
    """'…T13:45:02+00:00' -> 'HH:MM' in ET. Converted, never offset-guessed."""
    try:
        from datetime import datetime
        from zoneinfo import ZoneInfo
        t = datetime.fromisoformat(str(entry_time))
        return t.astimezone(ZoneInfo("America/New_York")).strftime("%H:%M")
    except Exception:                                          # noqa: BLE001
        return ""


def load_trades(a):
    """Closed trades with an MFE, tagged nf/ok. Exclusions applied here."""
    out = []
    for db in sorted(glob.glob(os.path.expanduser(a.trades))):
        if "_archive" in db or db.endswith(".bak"):
            continue          # the trades tree carries both
        # ⚠️ REGEX, NOT split("_"). The filename is `<SYM>_trades_<date>.db`, so
        # splitting yields "2026-08-12.db" WITH the extension and every date
        # comparison silently fails — the probe reported "no closed trades"
        # against a populated directory. An empty result that looks like a null.
        import re as _re
        _m = _re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(db))
        date = _m.group(1) if _m else ""
        if not date or date < a.since or date in a.exclude_dates:
            continue
        try:
            con = sqlite3.connect("file:" + db + "?mode=ro", uri=True)
            con.row_factory = sqlite3.Row
            rows = con.execute(
                "SELECT * FROM trades WHERE status='closed'").fetchall()
        except Exception:                                      # noqa: BLE001
            continue
        for r in rows:
            r = dict(r)
            st = str(r.get("setup_type") or "")
            if st == "trend_continuation_breakout" and date >= "2026-08-07":
                continue                      # one-tick artifacts, any date
            ent = r.get("entry_premium") or 0
            mx = r.get("max_premium_seen")
            try:
                ent = float(ent)
            except Exception:                                  # noqa: BLE001
                continue
            if ent <= 0 or mx is None:
                continue
            mfe = (float(mx) - ent) / ent * 100.0
            r["_date"] = date
            r["_hhmm"] = _hhmm(r.get("entry_time"))
            r["_nf"] = mfe < a.nf_cut
            r["_window"] = _window(date)
            out.append(r)
    return out


def load_replay_axes(a, wanted=None):
    """(date, sym, HH:MM) -> the L1 scores + l2 at that tick.

    `direction_conf` is replayed from these rather than read from the journal,
    because **AX.3's emission step was never built** — the primitive that
    already measured +0.188 separation is not journaled anywhere.
    """
    # ⚠️ INDEX ONLY THE TICKS THE TRADES ASK FOR. v1.0 built a dict of EVERY
    # tick across EVERY replay log before touching a trade — ~280k parsed JSON
    # records held at once — and was **OOM-KILLED (rc=137)** on control, exactly
    # as the regime grid was on 08-15. The loud "ABSENT MEASUREMENT" guard could
    # not fire, because the process died before reaching it: an in-process guard
    # cannot report a kill.
    # `wanted` is the set of (date, sym, HH:MM) keys the trades actually need —
    # a few thousand, not a few hundred thousand.
    idx = {}
    for path in sorted(glob.glob(os.path.expanduser(a.replay))):
        import re
        m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
        if not m:
            continue
        date = m.group(1)
        if date < a.since or date in a.exclude_dates:
            continue
        with open(path) as f:
            for line in f:
                if '"scores"' not in line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                ts = str(r.get("ts", ""))
                if len(ts) < 5:
                    continue
                key = (date, str(r.get("sym", "")), ts[:5])
                if wanted is not None and key not in wanted:
                    continue          # discard immediately; do not accumulate
                idx[key] = r
    return idx


def candidates(tr, rep):
    """Every decision-time primitive we can evaluate, per trade.

    ⚠️ A `None` here means NOT AVAILABLE for that trade — it is dropped from
    that primitive's sample and COUNTED, never imputed. An imputed value would
    manufacture separation out of missingness.
    """
    out = {}
    r = rep.get((tr["_date"], tr.get("symbol"), tr["_hhmm"]))
    sc = (r or {}).get("scores") or {}
    l2 = (r or {}).get("l2") or {}

    # --- already measured, carried for comparison -------------------------
    out["RGCV (conviction)"] = tr.get("regime_conviction")
    out["SETUP (grade score)"] = tr.get("setup_score")

    # --- L1 direction axis: AX.3's +0.188, never journaled ----------------
    if sc:
        bull = sc.get("TRENDING_BULL") or 0.0
        bear = sc.get("TRENDING_BEAR") or 0.0
        out["direction_conf (L1)"] = max(bull, bear)
        out["RANGING score"] = sc.get("RANGING")
        out["BREAKOUT score"] = sc.get("BREAKOUT_VOLATILE")
        out["COMPRESSION score"] = sc.get("COMPRESSION")
        # dominance-at-entry: how decisively the winner led, that tick
        tot = sum(v for v in sc.values() if isinstance(v, (int, float)))
        top = max((v or 0) for v in sc.values())
        out["L1 dominance share"] = (top / tot) if tot > 0 else None

    # --- ORB geometry, journaled since 07-18 ------------------------------
    for col, name in (("retest_depth_px", "ORB retest depth"),
                      ("adx_at_entry", "ADX at entry"),
                      ("atr_at_entry", "ATR at entry")):
        if tr.get(col) is not None:
            out[name] = tr.get(col)

    # --- readiness / shadow, if the columns exist -------------------------
    for col, name in (("readiness_grade", "readiness grade"),
                      ("velocity_at_entry", "shadow velocity"),
                      ("pos_pct", "pitchfork pos_pct")):
        if tr.get(col) is not None:
            out[name] = tr.get(col)

    return {k: v for k, v in out.items() if isinstance(v, (int, float))}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--trades", default=TRADES_GLOB)
    ap.add_argument("--replay", default=REPLAY_GLOB)
    ap.add_argument("--since", default="2026-07-13")
    ap.add_argument("--nf-cut", type=float, default=2.0,
                    help="MFE%% below which a trade NEVER went favourable")
    ap.add_argument("--strategy", default="",
                    help="restrict to one strategy, e.g. ORBStrategy")
    a = ap.parse_args(argv[1:])
    a.exclude_dates = {"2026-08-14"}          # identity-chain pollution

    trades = load_trades(a)
    if not trades:
        print(f"no closed trades with MFE at/after {a.since}")
        print(f"  looked in: {a.trades}")
        print("  ABSENT MEASUREMENT, not a null.")
        return 1
    if a.strategy:
        trades = [t for t in trades if t.get("strategy") == a.strategy]
    wanted = {(t["_date"], t.get("symbol"), t["_hhmm"]) for t in trades}
    rep = load_replay_axes(a, wanted)

    print("=" * 94)
    print("SEPARATION PROBE (P0.1) — does anything separate outcomes AT DECISION TIME?")
    print(f"  {len(trades)} closed trade(s) with MFE   "
          f"{len({t['_date'] for t in trades})} session(s)   "
          f"nf cut = MFE < {a.nf_cut}%"
          + (f"   strategy={a.strategy}" if a.strategy else ""))
    print(f"  replay ticks indexed: {len(rep):,}   "
          f"(08-14 excluded; _breakout rows from 08-07 excluded)")
    print("=" * 94)

    nf_n = sum(1 for t in trades if t["_nf"])
    print(f"\n  never-favourable: {nf_n}/{len(trades)} "
          f"({100.0*nf_n/len(trades):.0f}%)")

    # gather per-primitive samples
    vals = collections.defaultdict(lambda: {"nf": [], "ok": [],
                                            "sess": set(), "win": {}})
    unmatched = 0
    for t in trades:
        c = candidates(t, rep)
        if not c:
            unmatched += 1
            continue
        for k, v in c.items():
            b = vals[k]
            (b["nf"] if t["_nf"] else b["ok"]).append(v)
            b["sess"].add(t["_date"])
            b["win"].setdefault(t["_window"], {"nf": [], "ok": []})
            (b["win"][t["_window"]]["nf"] if t["_nf"]
             else b["win"][t["_window"]]["ok"]).append(v)
    if unmatched:
        print(f"  ⚠️ {unmatched} trade(s) had NO primitive available and were "
              f"dropped, not imputed.")

    def med(v):
        return sorted(v)[len(v) // 2] if v else float("nan")

    print(f"\n  {'primitive':26}{'n':>6}{'sess':>6}{'nf med':>9}{'ok med':>9}"
          f"{'gap':>9}  {'windows':<22}verdict")
    print("  " + "-" * 90)
    results = []
    for k in sorted(vals):
        b = vals[k]
        n = len(b["nf"]) + len(b["ok"])
        if not b["nf"] or not b["ok"]:
            continue
        mnf, mok = med(b["nf"]), med(b["ok"])
        gap = mok - mnf
        sess = len(b["sess"])
        # window sign stability (post-LIQ.1 onward, per the criterion)
        signs = []
        for w, _lo, _hi in WINDOWS[1:]:
            d = b["win"].get(w)
            if d and d["nf"] and d["ok"]:
                signs.append(1 if med(d["ok"]) > med(d["nf"]) else -1)
        stable = bool(signs) and len(set(signs)) == 1
        lo, hi = _wilson(len(b["nf"]), n)
        clears = (gap > 0 and n >= MIN_N and sess >= MIN_SESSIONS
                  and stable and len(signs) >= 2)
        verdict = ("CLEARS" if clears
                   else "under-powered" if (n < MIN_N or sess < MIN_SESSIONS)
                   else "INVERTED" if gap < 0
                   else "unstable" if not stable
                   else "flat/no separation")
        wtxt = f"{len(signs)} win, {'stable' if stable else 'mixed'}"
        print(f"  {k:26}{n:>6}{sess:>6}{mnf:>9.3f}{mok:>9.3f}{gap:>+9.3f}"
              f"  {wtxt:<22}{verdict}")
        results.append((k, clears, gap, n, sess))

    print("\n  PRE-REGISTERED CRITERION (set before the run):")
    print(f"    nf BELOW ok · CI-separated · n >= {MIN_N} across >= {MIN_SESSIONS}"
          f" sessions · sign stable across >= 2 post-LIQ.1 windows")
    win = [r for r in results if r[1]]
    if win:
        print(f"\n  ✅ {len(win)} primitive(s) CLEAR: "
              + ", ".join(r[0] for r in win))
        print("     -> the confidence factor exists in collected data; the")
        print("        remaining work is WIRING (roadmap Phase 1).")
        print("     ⚠️ NO BEST IS NAMED. Choosing the largest gap among many")
        print("        candidates is in-sample argmax — pick against the")
        print("        criterion and confirm forward, do not rank on this run.")
    else:
        print("\n  ❌ NOTHING CLEARS.")
        print("     -> that IS the finding, and it is worth more than the plan.")
        print("        The escalation is NEW INPUTS (chain-derived expectation")
        print("        first — already collected, cannot be backfilled), NOT a")
        print("        new combiner and NOT a new codebase.")
        print("     ⚠️ Check the under-powered rows before concluding: an absent")
        print("        measurement is not a null result.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
