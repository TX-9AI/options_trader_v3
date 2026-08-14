#!/usr/bin/env python3
"""
tests/tcs_v21_backtest.py — v1.0 — 2026-08-14   (TC.6 v2.1)

REPLAY THE SHIPPED v2.1 GATE STACK AGAINST ARCHIVED CHAINS AND TAPE.

Sequential, one open position per symbol at a time: enter when every gate
passes, hold until a BREACH of the ORB bound or the 15:45 close, then become
eligible again. That mirrors the live shape — there is no cooldown and no
per-session limit.

────────────────────────────────────────────────────────────────────────────
⚠️ WHAT THIS CANNOT REPLAY, STATED FIRST BECAUSE IT BOUNDS EVERY NUMBER BELOW
────────────────────────────────────────────────────────────────────────────
1. **THE DIRECTION GATE IS A PROXY, NOT THE LIVE RULE.** v2.1 takes direction
   from the TREND VOTE (`overall_direction` + `primary_adx`), and **neither is
   archived** — `signal_journal` carries no trend-vote fields. Reimplementing the
   trend engine here would create a SECOND LINEAGE of it, which is the failure
   WORKING_AGREEMENT 7 forbids and which has already cost this project twice.
   So this uses the journaled REGIME LABEL as a stated proxy: TRENDING_BULL ->
   long/put, TRENDING_BEAR -> short/call.
   **THE LIVE GATE IS STRICTER** (a directional vote AND an ADX floor), so the
   trade count here is an **UPPER BOUND** and the population is contaminated with
   entries the real ADX filter would have refused.

2. **CNT.1's EXIT FIX IS NOT BACKTESTABLE AT ALL.** Every historical
   `trend_continuation_breakout` closed at ONE TICK, so the premium path after
   that exit was never recorded. There is no counterfactual in the data. Any
   number claiming to measure that fix would be fabricated.

3. **AFD.1's PRE-DISPATCH MOVE IS NOT BACKTESTABLE.** Trade records show what
   FIRED, never what would have fired had the slot not been consumed. Simulating
   dispatch means simulating every strategy, which is the live engine, not a test.

So this backtests exactly ONE of the three corrections. That is stated rather
than papered over.

────────────────────────────────────────────────────────────────────────────
THE GATES APPLIED (v2.1, in the shipped order)
────────────────────────────────────────────────────────────────────────────
  11:00-14:00 ET · direction proxy · ORB bound exists (recomputed from the
  09:30-09:35 bars, never from the engine) · **PRICE OUTSIDE THE RANGE** ·
  strike beyond the bound · beyond the session extreme so far · quote width <=
  CONDOR_MAX_QUOTE_WIDTH · POP >= CONDOR_MIN_POP · protective wing exists ·
  joint EV positive · credit >= 4x the nickel close.
  **NO EM floor** (dis-inherited) and **NO cooldown** (removed).

EXIT: a 1-minute CLOSE back through the bound, or 15:45. **No nickel close, no
premium stop** — matching the shipped exit.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python tests/tcs_v21_backtest.py --since 2026-07-23
"""

import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.credit_edge import CHAINS                                       # noqa: E402
from tests.spread_counterfactual import (session_path, ohlc_root,          # noqa: E402
                                         load_group_chain, nearest)
from execution.limit_ladder import price_increment                          # noqa: E402

import config                                                               # noqa: E402
from strategy.iron_condor_strategy import IronCondorStrategy                # noqa: E402

SEL = IronCondorStrategy.__new__(IronCondorStrategy)
OPEN_MIN, OPEN_END = 9 * 60 + 30, 9 * 60 + 30 + config.ORB_WINDOW_MINUTES
CLOSE_MIN = 15 * 60 + 45
CONTRACT_MULT = 100


def opening_range(bars):
    w = [b for b in bars if OPEN_MIN <= b[0] < OPEN_END]
    if not w:
        return None
    return max(b[1] for b in w), min(b[2] for b in w)


def regime_by_minute(journal_dir, date, sym):
    """{minute: label} from the journal — the DIRECTION PROXY, not the live gate."""
    out = {}
    path = os.path.join(journal_dir, date, f"{sym}.jsonl")
    if not os.path.isfile(path):
        return out
    import json
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                ts = r.get("ts_et") or ""
                lab = ((r.get("regime") or {}).get("label")
                       or (r.get("regime") or {}).get("primary_regime"))
                if len(ts) >= 16 and lab:
                    out[int(ts[11:13]) * 60 + int(ts[14:16])] = str(lab).upper()
    except Exception:                                          # noqa: BLE001
        pass
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-07-23")
    ap.add_argument("--journal", default=os.path.expanduser(
        "~/day_trader_pro/signal_journal"))
    ap.add_argument("--start", default="11:00")
    ap.add_argument("--width", type=float, default=0.0,
                    help="wing width; 0 = use the instrument default")
    a = ap.parse_args(argv[1:])

    root = ohlc_root()
    if not root or not os.path.isdir(a.journal):
        print("no OHLC or journal root — ABSENT MEASUREMENT, not a null.")
        return 0
    sh, sm = (int(x) for x in a.start.split(":"))
    start_min = sh * 60 + sm

    dates = sorted(d for d in os.listdir(a.journal)
                   if len(d) == 10 and d >= a.since)

    trades, skips = [], collections.Counter()
    sym_days = 0

    for date in dates:
        paths = session_path(date, root)
        regs_dir = os.path.join(a.journal, date)
        if not os.path.isdir(regs_dir):
            continue
        for fn in sorted(os.listdir(regs_dir)):
            if not fn.endswith(".jsonl"):
                continue
            sym = fn[:-6]
            bars = paths.get(sym) or []
            if not bars:
                continue
            rng = opening_range(bars)
            if rng is None:
                skips["no opening range"] += 1
                continue
            orb_hi, orb_lo = rng
            regs = regime_by_minute(a.journal, date, sym)
            if not regs:
                skips["no regime series"] += 1
                continue
            sym_days += 1

            width = a.width or (config.CONDOR_WING_WIDTH_SPX
                                if sym in ("SPX", "SPXW")
                                else config.CONDOR_WING_WIDTH_QQQ)
            window = [b for b in bars if start_min <= b[0] <= CLOSE_MIN]
            targets = [b[0] for b in window]
            snaps = load_group_chain(date, sym, targets) if targets else []

            open_pos = None
            for (m, hi, lo, close) in window:
                # ── manage an open position first ────────────────────────────
                if open_pos is not None:
                    breached = (close < open_pos["bound"]
                                if open_pos["side"] == "put"
                                else close > open_pos["bound"])
                    if breached or m >= CLOSE_MIN:
                        k_s, k_l = open_pos["ks"], open_pos["kl"]
                        if open_pos["side"] == "put":
                            loss = min(max(0.0, k_s - close), width)
                        else:
                            loss = min(max(0.0, close - k_s), width)
                        open_pos["pnl"] = (open_pos["credit"] - loss) * CONTRACT_MULT
                        open_pos["exit_min"] = m
                        open_pos["exit_reason"] = ("breach" if breached
                                                   else "hard_close_15:45")
                        trades.append(open_pos)
                        open_pos = None
                    else:
                        continue

                if m >= CLOSE_MIN:
                    continue

                # ── DIRECTION PROXY (see the header caveat) ──────────────────
                lab = regs.get(m) or regs.get(m - 1) or regs.get(m - 2) or ""
                if "TRENDING_BULL" in lab:
                    side, bound = "put", orb_hi
                elif "TRENDING_BEAR" in lab:
                    side, bound = "call", orb_lo
                else:
                    skips["not trending (proxy)"] += 1
                    continue

                # ── PRICE MUST BE OUTSIDE THE RANGE ─────────────────────────
                if not (close > bound if side == "put" else close < bound):
                    skips["price back inside the range"] += 1
                    continue

                prior = [b for b in bars if b[0] <= m]
                extreme = (min(b[2] for b in prior) if side == "put"
                           else max(b[1] for b in prior))

                rows = nearest(snaps, m)
                if not rows:
                    skips["no chain within window"] += 1
                    continue

                atrs = [abs(b[1] - b[2]) for b in prior[-14:]]
                sigma = (sum(atrs) / len(atrs)) if atrs else 0.0
                bars_left = max(0.0, (CLOSE_MIN - m) / config.CONDOR_POP_BAR_MIN)

                short = SEL._select_beyond_rail(
                    [type("C", (), {"strike": k, "bid": (c.get("bid") or 0.0),
                                    "ask": (c.get("ask") or 0.0),
                                    "mark": ((c.get("bid") or 0.0) + (c.get("ask") or 0.0)) / 2,
                                    "open_interest": 0, "volume": 0})()
                     for (sd, k), c in rows.items() if sd == side],
                    side, bound,
                    float("inf") if side == "put" else float("-inf"),
                    extreme, spot=close, sigma=sigma, bars_left=bars_left,
                    min_pop=config.CONDOR_MIN_POP,
                    max_width_pct=config.CONDOR_MAX_QUOTE_WIDTH)
                if short is None:
                    skips["no strike clears the stack"] += 1
                    continue

                k_l = short.strike - width if side == "put" else short.strike + width
                lc = rows.get((side, round(k_l, 4)))
                if lc is None:
                    skips["no protective wing"] += 1
                    continue
                credit = max(0.0, (short.bid or 0.0) - (lc.get("ask") or 0.0))
                pop = SEL._pop(abs(short.strike - close), sigma, bars_left)
                if pop <= 0.0:
                    skips["POP unresolvable"] += 1
                    continue
                if credit / width <= config.TCS_LOSS_GIVEN_BREACH * (1 - pop) / pop:
                    skips["negative EV"] += 1
                    continue
                if credit < config.TCS_MIN_CREDIT_NICKEL_MULT * config.CONDOR_NICKEL_CLOSE:
                    skips["credit below nickel floor"] += 1
                    continue

                open_pos = {"date": date, "sym": sym, "side": side, "min": m,
                            "bound": bound, "ks": short.strike, "kl": k_l,
                            "credit": credit, "pop": pop, "width": width}

    print("=" * 84)
    print("  TC.6 v2.1 BACKTEST — the shipped gate stack, replayed")
    print(f"  {len(dates)} session(s) since {a.since}   {sym_days} symbol-days"
          f"   window {a.start}-15:45")
    print("=" * 84)
    print("\n  ⚠️ THE DIRECTION GATE IS A PROXY. v2.1 uses the TREND VOTE")
    print("     (overall_direction + ADX) and NEITHER IS ARCHIVED. This uses the")
    print("     journaled REGIME LABEL instead. The live gate is STRICTER, so")
    print("     the trade count below is an UPPER BOUND.")
    print("  ⚠️ CNT.1's exit fix and AFD.1's pre-dispatch move are NOT")
    print("     backtestable — the counterfactual is not in the data.")

    if not trades:
        print("\n  NO TRADES QUALIFIED. Skip reasons:")
        for k, v in skips.most_common():
            print(f"    {k:34s} {v:,}")
        print("\n  ABSENT MEASUREMENT, not a null.")
        return 0

    n = len(trades)
    net = sum(t["pnl"] for t in trades)
    wins = [t for t in trades if t["pnl"] > 0]
    held = [t for t in trades if t["exit_reason"] != "breach"]
    holds = [t["exit_min"] - t["min"] for t in trades]
    print(f"\n  TRADES {n}   net ${net:,.0f}   ${net/n:+,.2f}/trade"
          f"   win {100.0*len(wins)/n:.0f}%")
    print(f"  held to the close {len(held)} ({100.0*len(held)/n:.0f}%)"
          f"   breached {n-len(held)}")
    print(f"  median hold {sorted(holds)[len(holds)//2]:.0f} min"
          f"   median credit ${sum(t['credit'] for t in trades)/n:.2f}"
          f"   median POP {sorted(t['pop'] for t in trades)[n//2]:.2f}")

    print(f"\n  BY EXIT")
    for reason in ("hard_close_15:45", "breach"):
        g = [t for t in trades if t["exit_reason"] == reason]
        if g:
            print(f"    {reason:20s} {len(g):>4}  ${sum(x['pnl'] for x in g):>10,.0f}"
                  f"  ${sum(x['pnl'] for x in g)/len(g):>8,.2f}/trade")

    print(f"\n  BY SIDE")
    for side in ("put", "call"):
        g = [t for t in trades if t["side"] == side]
        if g:
            print(f"    {side:20s} {len(g):>4}  ${sum(x['pnl'] for x in g):>10,.0f}")

    print(f"\n  SKIPS (why the stack refused)")
    for k, v in skips.most_common(8):
        print(f"    {k:34s} {v:,}")

    print("\n" + "=" * 84)
    print("  HOW TO READ IT. Every trade here passed the SHIPPED gates except")
    print("  the ADX/vote filter, which cannot be replayed. Treat the count as")
    print("  an upper bound and the population as contaminated with entries the")
    print("  real filter would refuse. A NEGATIVE result is therefore stronger")
    print("  evidence than a positive one: the live gate can only remove trades.")
    print("=" * 84)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
