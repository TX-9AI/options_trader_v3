#!/usr/bin/env python3
# tests/readiness_digest.py — options_trader_v3
# v1.0 — 2026-07-27 — NEW. Nightly readiness digest (ROADMAP readiness track).
#
#   Offline control-server tool, stdlib-only, read-only. Reads the harvested
#   signal-journal jsonl for a date and digests the trade_readiness v1.1
#   events (`readiness`, `readiness_would_fire`, `readiness_staged_pick`) into
#   the DIAL-TUNING report: per strategy — time in each machine state, R
#   distribution, arm episodes and their durations, would-fire count,
#   staged-pick stats (target-delta and spread distributions, conv_ema vs the
#   bars), and — when `disposition` events exist in the same file — the
#   ANTICIPATION metric: for each fired trade, how long its strategy had been
#   ARMED beforehand (the lead-time the readiness engine exists to create).
#
#   Runs unattended as EOD-conductor phase 9 (--quiet prints ONE headline and
#   returns 0 even on empty nights so it can never mark the chain failed —
#   conditional_tables.py precedent). Writes:
#       reports/readiness_digest_<date>.txt
#       reports/readiness_digest_<date>.jsonl   (machine-readable, for tuning)
#
#   The bars it reports against are read FROM THE ROWS (each readiness row
#   embeds its bars), so a knob change on the boxes shows up here without
#   touching this tool.

from __future__ import annotations
import argparse, json, os, sys, glob
from collections import defaultdict


def _pct(vals, q):
    if not vals:
        return 0.0
    s = sorted(vals)
    return s[min(int(q * len(s)), len(s) - 1)]


def _load_day(day_dir):
    rows = []
    for f in sorted(glob.glob(os.path.join(day_dir, "*.jsonl"))):
        sym = os.path.basename(f).split(".")[0].split("_")[0]
        try:
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    r["_sym"] = sym
                    rows.append(r)
        except Exception:
            continue
    return rows


def digest(day_dir, date):
    rows = _load_day(day_dir)
    ready = [r for r in rows if r.get("event") in
             ("readiness", "readiness_would_fire") and "readiness" in r]
    picks = [r for r in rows if r.get("event") == "readiness_staged_pick"]
    disps = [r for r in rows if r.get("event") == "disposition"]

    per = defaultdict(lambda: {"rs": [], "machines": defaultdict(int),
                               "would_fire": 0, "arm_spans": [], "slopes": []})
    # arm episode tracking per (symbol, strategy)
    armed_since = {}
    for r in sorted(ready, key=lambda x: (x.get("_sym", ""), x.get("ts_et", ""))):
        d = r["readiness"]; key = d.get("strategy", "?")
        sym = r.get("_sym", "?"); ts = r.get("ts_et", "")
        p = per[key]
        p["rs"].append(float(d.get("r", 0.0)))
        p["slopes"].append(float(d.get("slope_per_min", 0.0)))
        m = d.get("machine", "?"); p["machines"][m] += 1
        if r.get("event") == "readiness_would_fire":
            p["would_fire"] += 1
        ak = (sym, key)
        if m == "ARMED" and ak not in armed_since:
            armed_since[ak] = ts
        elif m != "ARMED" and ak in armed_since:
            p["arm_spans"].append((sym, armed_since.pop(ak), ts))

    # anticipation: disposition fires vs prior ARMED state of that strategy
    anticipations = []
    for dp in disps:
        strat = str(dp.get("strategy") or dp.get("setup_type") or
                    (dp.get("signal") or {}).get("strategy") or "").lower()
        sym = dp.get("_sym", "?"); ts = dp.get("ts_et", "")
        for key in per:
            if key.split("_")[0] in strat and (sym, key) in armed_since:
                anticipations.append({"sym": sym, "strategy": key,
                                      "armed_since": armed_since[(sym, key)],
                                      "fired_at": ts})

    pick_stats = defaultdict(lambda: {"n": 0, "deltas": [], "spreads": [], "convs": []})
    for r in picks:
        st = r.get("staged", {}); key = st.get("strategy", "?")
        ps = pick_stats[key]; ps["n"] += 1
        ps["deltas"].append(float(st.get("target_delta") or 0))
        ps["convs"].append(float(st.get("conv_ema") or 0))
        c = st.get("contract") or {}
        if c.get("spread_pct_of_mid") is not None:
            ps["spreads"].append(float(c["spread_pct_of_mid"]))

    lines = [f"READINESS DIGEST — {date}",
             f"journal rows: {len(rows)}  readiness: {len(ready)}  "
             f"staged picks: {len(picks)}  dispositions: {len(disps)}", ""]
    out_json = {"date": date, "rows": len(rows), "strategies": {}}
    for key in sorted(per):
        p = per[key]; n = len(p["rs"])
        mline = " ".join(f"{m}:{c}" for m, c in sorted(p["machines"].items()))
        lines.append(f"[{key}] ticks={n}  {mline}")
        lines.append(f"    R p50={_pct(p['rs'],.5):.3f} p90={_pct(p['rs'],.9):.3f} "
                     f"max={max(p['rs']) if p['rs'] else 0:.3f}  "
                     f"slope p90={_pct(p['slopes'],.9):.3f}/min  "
                     f"would_fire={p['would_fire']}  arm_episodes={len(p['arm_spans'])}")
        ps = pick_stats.get(key)
        if ps and ps["n"]:
            lines.append(f"    staged picks n={ps['n']}  target_delta p50="
                         f"{_pct(ps['deltas'],.5):.3f}  conv_ema p50={_pct(ps['convs'],.5):.3f}"
                         + (f"  spread%mid p50={_pct(ps['spreads'],.5):.4f}" if ps["spreads"] else ""))
        out_json["strategies"][key] = {
            "ticks": n, "machines": dict(p["machines"]),
            "r_p50": _pct(p["rs"], .5), "r_p90": _pct(p["rs"], .9),
            "would_fire": p["would_fire"], "arm_episodes": len(p["arm_spans"]),
            "staged_picks": (ps["n"] if ps else 0)}
    if anticipations:
        lines.append("")
        lines.append("ANTICIPATION (strategy was ARMED before its trade fired):")
        for a in anticipations:
            lines.append(f"    {a['sym']} {a['strategy']}: armed {a['armed_since']} -> fired {a['fired_at']}")
    out_json["anticipations"] = anticipations
    headline = (f"🧭 readiness {date}: "
                + (", ".join(f"{k} wf={per[k]['would_fire']} arm={len(per[k]['arm_spans'])}"
                             for k in sorted(per)) if per
                   else "no readiness rows yet (journal not harvested or fleet pre-v4.4)"))
    return lines, out_json, headline


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--journal-root", required=True)
    ap.add_argument("--reports-dir", required=True)
    ap.add_argument("--date", default=None, help="default: latest dated folder present")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    days = sorted(d for d in glob.glob(os.path.join(a.journal_root, "20*-*-*"))
                  if os.path.isdir(d))
    if a.date:
        day_dir = os.path.join(a.journal_root, a.date); date = a.date
    elif days:
        day_dir = days[-1]; date = os.path.basename(day_dir)
    else:
        print("🧭 readiness: no journal folders on disk yet")
        return 0                      # quiet night must never fail the chain
    lines, out_json, headline = digest(day_dir, date)
    os.makedirs(a.reports_dir, exist_ok=True)
    with open(os.path.join(a.reports_dir, f"readiness_digest_{date}.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(a.reports_dir, f"readiness_digest_{date}.jsonl"), "w") as f:
        f.write(json.dumps(out_json) + "\n")
    print(headline if a.quiet else "\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
