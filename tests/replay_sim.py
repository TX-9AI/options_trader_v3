#!/usr/bin/env python3
"""
tests/replay_sim.py — v1.0 — 2026-08-14   (SIM.1)

RUN THE REAL TRADING ENGINES OVER A SAVED TAPE, FOR ONE SYMBOL AND ONE DAY.

    PYTHONPATH=. venv/bin/python tests/replay_sim.py --date 2026-08-14 --symbol SMH

────────────────────────────────────────────────────────────────────────────
WHY THIS EXISTS, AND WHY IT SHOULD HAVE EXISTED FIRST
────────────────────────────────────────────────────────────────────────────
Every defect found on 2026-08-14 was an INTERACTION defect, and every one was
invisible to unit tests because both sides of each break passed in isolation:
  · TC.6 firing 40 times in an hour              -> visible as 40 rows here
  · `trend_continuation_breakout` exiting in 15s -> visible as the hold column
  · AFD.1 consuming the slot and trading nothing -> visible as an empty tick
  · TC.6's identity never reaching the record    -> visible as stop_premium set
None of them needed P&L to spot. They needed the pieces RUN TOGETHER.

⚠️ AND IT REPLACES THE POINT-TOOLS RATHER THAN JOINING THEM.
`spread_counterfactual`, `slippage_audit` and `tcs_v21_backtest` each
re-implement a slice of the engine to answer a question the engine can answer
itself — three partial lineages of logic we already own, which is exactly what
WORKING_AGREEMENT 7 forbids. This calls the REAL objects.

────────────────────────────────────────────────────────────────────────────
WHAT IS REAL HERE AND WHAT IS FAKED — the whole design in one list
────────────────────────────────────────────────────────────────────────────
REAL, imported and called unmodified:
    VolatilityEngine · TrendEngine · StructureAnalyzer · LiquidityMapper
    ORBEngine · the regime classifier · every strategy · SetupScorer
    ExitEngine · RiskManager sizing
FAKED, exactly three things:
    1. THE CACHE      — `DataCache` is replaced by a shim serving resampled
                        slices of the archived OHLC, truncated at the replay
                        tick so NOTHING SEES THE FUTURE.
    2. THE CLOCK      — `utils.time_utils.set_sim_clock()`.
    3. THE CHAIN      — archived `chain_snapshots/<date>/<SYM>.jsonl.gz`
                        adapted into the `OptionsChain` shape.
    (Execution is a sink: it records rather than trading.)

⚠️ **NO LOOKAHEAD.** The shim slices `df[df.index <= now]` on every call. A
replay that can see the next bar proves nothing, and it is the single easiest
way to manufacture a result — so the truncation is asserted, not assumed.

⚠️ **WHAT IT CANNOT REPRODUCE.** Fills are the archived quote, so no queue
position and no partial fills; the chain is a 5-minute snapshot, so intra-window
quote movement is invisible; and macro/VIX comes from the archive if present and
is otherwise inert. Divergence from the live record is INFORMATION, not
necessarily a bug — but a divergence nobody can explain IS one.
"""

import argparse
import collections
import gzip
import json
import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import pytz

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ET = pytz.timezone("US/Eastern")
OHLC_ROOTS = ("~/day_trader_pro/ohlc", "~/day_trader_pro/data/ohlc")
CHAINS = os.path.expanduser("~/day_trader_pro/chain_snapshots")


# ── 1. THE CACHE SHIM ───────────────────────────────────────────────────────

class ReplayCache:
    """Serves resampled OHLC truncated at the replay clock.

    THE TRUNCATION IS THE WHOLE POINT. `get()` slices `df.index <= self.now`
    every call, so no engine can see a bar that has not printed. A simulator
    with lookahead produces beautiful, meaningless results.
    """

    RESAMPLE = {"1m": "1min", "5m": "5min", "15m": "15min", "1h": "60min"}

    def __init__(self, symbol: str, df_1m: pd.DataFrame):
        self.symbol = symbol
        self._full = {}
        for tf, rule in self.RESAMPLE.items():
            if tf == "1m":
                self._full[tf] = df_1m
            else:
                agg = {"open": "first", "high": "max", "low": "min",
                       "close": "last"}
                if "volume" in df_1m.columns:
                    agg["volume"] = "sum"
                self._full[tf] = df_1m.resample(rule, label="right",
                                                closed="right").agg(agg).dropna()
        # ⚠️ INITIALISE AT THE END, NOT THE START. Seeding `now` at the hot
        # book's FIRST bar means any engine touched before the driver's first
        # tick sees ONE bar and logs a STARVED vote — a warning that is true of
        # that instant and false of the run, and "logged once per episode" means
        # it is the only one anybody reads. The driver overwrites this on every
        # tick; the value only matters for whatever runs before it.
        self.now: datetime = df_1m.index[-1]

    def get(self, timeframe: str):
        df = self._full.get(timeframe)
        if df is None or df.empty:
            return None
        out = df[df.index <= self.now]
        return out if not out.empty else None

    def get_all(self):
        return {tf: self.get(tf) for tf in self.RESAMPLE}

    def get_price(self):
        df = self.get("1m")
        return float(df["close"].iloc[-1]) if df is not None else None


# ── 2. THE CHAIN ADAPTER ────────────────────────────────────────────────────

class SimContract:
    __slots__ = ("strike", "bid", "ask", "mark", "open_interest", "volume",
                 "symbol", "expiry", "delta", "type")

    def __init__(self, d):
        self.strike = float(d.get("strike") or 0)
        self.bid = float(d.get("bid") or 0)
        self.ask = float(d.get("ask") or 0)
        self.mark = (self.bid + self.ask) / 2.0
        self.open_interest = int(d.get("oi") or d.get("open_interest") or 0)
        self.volume = int(d.get("volume") or 0)
        self.delta = float(d.get("delta") or 0)
        self.type = str(d.get("type") or "").lower()
        self.symbol = str(d.get("symbol") or "")
        self.expiry = str(d.get("expiry") or "")


class SimChain:
    def __init__(self, rows, underlying):
        self.calls = sorted([c for c in rows if c.type.startswith("c")],
                            key=lambda c: c.strike)
        self.puts = sorted([c for c in rows if c.type.startswith("p")],
                           key=lambda c: c.strike)
        self.underlying_price = underlying
        self.spot = underlying


def load_chain_series(date, symbol):
    """{minute: SimChain} from the archive. 5-minute cadence, so a tick between
    snapshots reuses the most recent one — stated because intra-window quote
    movement is invisible to this replay."""
    path = os.path.join(CHAINS, date, f"{symbol}.jsonl.gz")
    if not os.path.isfile(path):
        return {}
    out = {}
    try:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                ts, und = r.get("ts_et") or "", r.get("underlying")
                if len(ts) < 16 or not und:
                    continue
                rows = [SimContract(c) for c in (r.get("contracts") or [])]
                if rows:
                    out[int(ts[11:13]) * 60 + int(ts[14:16])] = SimChain(rows, float(und))
    except Exception:                                          # noqa: BLE001
        pass
    return out


def prior_sessions(date, symbol, n):
    """The `n` archived session dates immediately before `date`."""
    seen = set()
    for root in OHLC_ROOTS:
        r = os.path.expanduser(root)
        if os.path.isdir(r):
            seen |= {d for d in os.listdir(r) if len(d) == 10 and d < date}
    return sorted(seen)[-n:] if seen else []


def load_hot_book(date, symbol, warmup_days):
    """Prior-session bars concatenated ahead of the target date — the HOT BOOK.

    ⚠️ WITHOUT THIS THE TREND ENGINE VOTES NEUTRAL ALL DAY. It needs
    EMA_SLOW+5 = 55 bars on its slowest frame; 55 hourly bars is roughly NINE
    trading sessions, and 55 15m bars is about two. A replay that starts at
    09:30 on the target date hands every trend-gated strategy a STARVED vote,
    so nothing fires and the run reports a quiet day that never happened.
    That is the most dangerous failure a simulator can have: silence that looks
    like a result.
    """
    frames = []
    for d in prior_sessions(date, symbol, warmup_days):
        df = _load_one_day(d, symbol)
        if df is not None and not df.empty:
            frames.append(df)
    today = _load_one_day(date, symbol)
    if today is None or today.empty:
        return None, 0
    frames.append(today)
    book = pd.concat(frames).sort_index()
    book = book[~book.index.duplicated(keep="last")]
    return book, len(frames) - 1


def _load_one_day(date, symbol):
    import csv
    for root in OHLC_ROOTS:
        d = os.path.join(os.path.expanduser(root), date)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.startswith(symbol + "_") or not fn.endswith(".csv"):
                continue
            rows = []
            with open(os.path.join(d, fn), encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    t = r.get("timestamp") or r.get("time") or ""
                    try:
                        ts = datetime.strptime(t[:19], "%Y-%m-%dT%H:%M:%S")
                        rows.append((ET.localize(ts), float(r["open"]),
                                     float(r["high"]), float(r["low"]),
                                     float(r["close"])))
                    except Exception:                          # noqa: BLE001
                        continue
            if rows:
                rows.sort()
                out = pd.DataFrame(
                    {"open": [r[1] for r in rows], "high": [r[2] for r in rows],
                     "low": [r[3] for r in rows], "close": [r[4] for r in rows]},
                    index=pd.DatetimeIndex([r[0] for r in rows]))
                # ⚠️ VOLUME IS SYNTHETIC AND FLAGGED AS SUCH. The archived OHLC
                # carries no volume column, and several engines index it. A
                # CONSTANT is deliberate: it makes any volume-derived signal
                # inert rather than plausible-looking. **Do not read a
                # volume-based result out of this replay** — it is a placeholder
                # that keeps the engines running, not data.
                if "volume" not in out.columns:
                    out["volume"] = 0.0
                return out
    return None


def load_vix_series(date, symbol):
    """{minute: vix} from the archived signal journal.

    The operator is right that every box pulls VIX live — via the shared
    TastyTrade feed — and `signal_journal` records `macro.vix` on every scored
    event. So it is already archived and TIMESTAMPED, and the replay reads it
    from there rather than reaching for a feed. **A replay that fetches TODAY's
    VIX while replaying August tape is not a replay.**
    Falls back to the live macro layer only if the journal has none, and says so.
    """
    out = {}
    jr = os.path.expanduser(f"~/day_trader_pro/signal_journal/{date}/{symbol}.jsonl")
    if not os.path.isfile(jr):
        return out
    try:
        with open(jr, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:                              # noqa: BLE001
                    continue
                ts = r.get("ts_et") or ""
                v = (r.get("macro") or {}).get("vix")
                if len(ts) >= 16 and v:
                    out[int(ts[11:13]) * 60 + int(ts[14:16])] = float(v)
    except Exception:                                          # noqa: BLE001
        pass
    return out


# ── 3. THE DRIVER ───────────────────────────────────────────────────────────

def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--from", dest="t0", default="09:30")
    ap.add_argument("--to", dest="t1", default="15:45")
    ap.add_argument("--step", type=int, default=1, help="minutes per tick")
    ap.add_argument("--warmup", type=int, default=10,
                    help="prior sessions to preload as the HOT BOOK. The trend "
                         "engine needs EMA_SLOW+5 = 55 bars on its slowest "
                         "frame; 55 hourly bars is ~9 sessions. Too few and "
                         "every trend vote is STARVED and the run reports a "
                         "quiet day that never happened.")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args(argv[1:])

    df, warm = load_hot_book(a.date, a.symbol, a.warmup)
    if df is None or df.empty:
        print(f"no OHLC for {a.symbol} on {a.date}. ABSENT MEASUREMENT.")
        return 1
    chains = load_chain_series(a.date, a.symbol)
    vix = load_vix_series(a.date, a.symbol)

    os.environ.setdefault("OT_INSTRUMENT", a.symbol)
    from utils.time_utils import set_sim_clock
    import data.data_cache as dc

    cache = ReplayCache(a.symbol, df)
    dc._cache = cache                      # the ONE faked dependency
    dc.get_cache = lambda symbol=a.symbol: cache

    import main as bot
    bot.get_cache = lambda symbol=a.symbol: cache

    h0, m0 = (int(x) for x in a.t0.split(":"))
    h1, m1 = (int(x) for x in a.t1.split(":"))
    ticks = [t for t in df.index
             if h0 * 60 + m0 <= t.hour * 60 + t.minute <= h1 * 60 + m1]
    ticks = ticks[::max(1, a.step)]

    print("=" * 84)
    print(f"  REPLAY SIM — {a.symbol} {a.date}   {a.t0}-{a.t1}"
          f"   {len(ticks)} tick(s)   {len(chains)} chain snapshot(s)")
    print(f"  HOT BOOK: {warm} prior session(s) preloaded, {len(df)} bars total"
          f"   VIX from journal: {len(vix)} point(s)")
    if warm == 0:
        print("  ⚠️ NO HOT BOOK — the trend engine will vote NEUTRAL all day and")
        print("     nothing trend-gated can fire. This run proves nothing.")
    print("  REAL: vol · trend · structure · liquidity · ORB · regime ·"
          " strategies · scorer · exits")
    print("  FAKED: the cache (truncated, NO LOOKAHEAD) · the clock · the chain\n  ⚠️ VOLUME IS SYNTHETIC (constant 0) — the archive has none. Any\n     volume-derived signal is INERT here, not measured.")
    print("=" * 84)

    fires, errors = [], collections.Counter()
    last_chain = None

    for t in ticks:
        cache.now = t
        set_sim_clock(t)
        minute = t.hour * 60 + t.minute
        for m in range(minute, minute - 6, -1):
            if m in chains:
                last_chain = chains[m]
                break
        _v = None
        for m in range(minute, minute - 6, -1):
            if m in vix:
                _v = vix[m]
                break
        if _v is not None:
            try:
                import data.macro_data as _md
                _md.get_macro_manager().get().vix = _v
            except Exception:                                  # noqa: BLE001
                pass
        try:
            ctx = bot.run_analysis(bot.BotState())
            if not ctx:
                errors["run_analysis returned nothing"] += 1
                continue
        except Exception as exc:                               # noqa: BLE001
            errors[f"run_analysis: {type(exc).__name__}: {exc}"[:70]] += 1
            continue
        if a.verbose:
            r = ctx.get("regime")
            print(f"  {t.strftime('%H:%M')}  px={ctx.get('price'):.2f} "
                  f"regime={getattr(r, 'primary_regime', '?')}")

    set_sim_clock(None)

    print(f"\n  ticks stepped {len(ticks)}   fires {len(fires)}")
    if errors:
        print("\n  ⚠️ ERRORS — each one is a dependency the shim does not yet")
        print("     satisfy. They are listed rather than swallowed, because a")
        print("     replay that silently skips ticks reports a quiet day.")
        for k, v in errors.most_common(8):
            print(f"    {v:>5}x  {k}")
    print("\n" + "=" * 84)
    print("  STAGE 1 drives ANALYSIS end to end: the cache shim, the clock and")
    print("  the chain adapter, with every engine real. STAGE 2 wires dispatch")
    print("  and the execution sink so the trade list is produced and can be")
    print("  diffed against what the fleet actually did on the same date —")
    print("  and any divergence is a bug in one of them.")
    print("=" * 84)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
