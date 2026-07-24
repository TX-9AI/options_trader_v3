"""
options_trader_v3/data/market_data.py — Underlying price data (candles + live
quote). v3.2

Candle history:    shared TastyTrade/DXFeed store (written by candle_feed.py —
                   the ONLY DXFeed subscription on the box)
Live quote:        shared store primary (latest 1m close), TastyTrade SDK
                   market-data endpoint secondary

v3.0 — 2026-07-10 — YAHOO-FINANCE PURGE / data stream mapping optimization.
        The legacy Yahoo-Finance client removed entirely (it was a DIFFERENT series than the DXLink/DXFeed tape
        the bot trades and logs on — provably divergent on the 5-minute
        opening range). This module now READS the on-box shared SQLite store
        maintained by data/candle_feed.py (one producer, many readers). No
        network, no DXFeed, no Yahoo anywhere in this module. Public contract of
        fetch_candles / fetch_quote / fetch_all_candles preserved EXACTLY so
        data_cache.py, all four engines, main.py, get_orb_range.py, query.py,
        and the off-repo shadow observer (via get_cache()) need zero changes.
        The legacy Yahoo period map was deleted.

        Failure semantics — fail loud, never silently short:
          * Store missing/empty, or feed heartbeat older than OT_FEED_STALE_S
            (default 120s) => return None + WARNING. A crashed candle-feed
            surfaces as "no data", never as stale numbers driving decisions.
          * A young session with only 6 one-minute bars is REAL data, not
            failure — return the bars we have. A 25-bar window legitimately
            cannot fill until ~25 minutes in; that is arithmetic, not a bug.
          * Intraday windows (1m/5m/15m) are NOT padded across the overnight
            gap with the prior session's bars: they are scoped to the most
            recent session present in the store. (Escape hatch:
            OT_FEED_INTRADAY_SCOPE=continuous restores multi-session windows.)
            1h/1d naturally span sessions.
v3.1 — 2026-07-13 — REGRESSION FIX: session-scoping now applies to 1m ONLY.
        Scoping 5m/15m as well broke the prior-session carry in
        get_orb_range.py (no priors visible ⇒ "no valid opening range found in
        lookback window" every tick, orb_range.json never refreshed — GLD and
        GOOGL, 2026-07-13) and silently forced trend_engine's 5m vote to NEUTRAL
        until ~14:05 ET (EMA_SLOW+5 = 55 bars unreachable in a session-scoped
        window). The no-overnight-padding rule belongs to the 25-bar 1-minute
        RANGING slope window and nothing else. 5m/15m/1h/1d are continuous.
v3.2 — 2026-07-13 — POISON-CANDLE GUARD (consumer side). DXFeed intermittently
        emits a junk candle at the signed-32-bit rollover (ts=2147483648xxx ms =>
        2038) with all prices 0.0 (observed live: GOOGL 1m then 15m, 2026-07-13).
        It sorted to the top of the ts DESC window, computed a NEGATIVE age (thus
        passing the freshness check) and returned close=0.0 — which run_analysis
        reads as falsy => "Could not fetch current price" => the tick loop died
        EVERY TICK while systemd still reported the unit ACTIVE. Silent and total.
        fetch_quote() and fetch_candles() now exclude non-positive prices and
        future-dated bars at the SQL layer, and fetch_quote re-asserts a
        non-negative age before returning. Feed-side fix: data/candle_feed.py v3.2.
"""

import logging
import os
import sqlite3
import time as _time
from datetime import datetime, time as dtime
from typing import Optional, Dict
from zoneinfo import ZoneInfo

import pandas as pd

from data.tasty_client import get_session
from data.candle_feed import feed_db_path, SESSION_OPEN_HM
from config import INSTRUMENT, TIMEFRAMES

logger = logging.getLogger(__name__)
ET = ZoneInfo("America/New_York")

FEED_STALE_S     = float(os.environ.get("OT_FEED_STALE_S", "120"))
INTRADAY_SCOPE   = os.environ.get("OT_FEED_INTRADAY_SCOPE", "session").lower()
# v3.1: ONLY 1m is session-scoped. The no-overnight-padding rule exists for the
# RANGING slope/angle read, which is computed on a 25-bar 1-MINUTE window — a
# window that must never bleed across the overnight gap. It was never meant for
# 5m/15m, and applying it there broke two things:
#   • get_orb_range.py could see NO prior sessions, so its last-valid-prior carry
#     was always empty; if today's 09:30 bar hadn't landed in the store yet it
#     raised "no valid opening range found in lookback window" every tick and
#     never refreshed orb_range.json (GLD/GOOGL, 2026-07-13).
#   • trend_engine needs EMA_SLOW+5 = 55 bars; session-scoped 5m doesn't reach 55
#     until ~14:05 ET, silently forcing the 5m trend vote to NEUTRAL all morning.
# 5m/15m/1h therefore return continuous multi-session history, as in v2.
INTRADAY_TFS     = ("1m",)
QUOTE_MAX_AGE_S  = 180.0     # latest 1m bar older than this => not a live quote


def _connect_ro() -> Optional[sqlite3.Connection]:
    path = feed_db_path()
    if not os.path.exists(path):
        return None
    try:
        return sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5.0)
    except Exception as e:
        logger.warning(f"feed store open failed ({path}): {e}")
        return None


def _feed_alive(conn: sqlite3.Connection) -> bool:
    """True iff candle_feed's heartbeat is fresh. This is the dead-feed guard:
    a crashed producer must surface as None, not stale numbers."""
    try:
        cur = conn.execute(
            "SELECT last_write_epoch FROM feed_meta "
            "WHERE symbol='__feed__' AND interval='heartbeat'")
        row = cur.fetchone()
    except Exception:
        return False
    if not row:
        return False
    return (_time.time() - float(row[0])) <= FEED_STALE_S


def fetch_candles(symbol: str, timeframe: str, count: int) -> Optional[pd.DataFrame]:
    """
    Fetch OHLCV candles from the shared TastyTrade feed store.

    Args:
        symbol:     e.g. "QQQ", "SPY", "SPX", "VIX"
        timeframe:  "1m", "5m", "15m", "1h", "1d"
        count:      Number of most-recent candles to return

    Returns:
        DataFrame with columns [open, high, low, close, volume] (lowercase),
        tz-aware DatetimeIndex in America/New_York, ascending, NaNs dropped,
        at most the last `count` rows. None (never a silent short frame caused
        by feed death) when the store is missing, empty for the symbol, or the
        feed heartbeat is stale.
    """
    conn = _connect_ro()
    if conn is None:
        logger.warning(f"feed store missing — is candle-feed.service running? "
                       f"({symbol} {timeframe})")
        return None
    try:
        if not _feed_alive(conn):
            logger.warning(f"feed STALE (heartbeat > {FEED_STALE_S:.0f}s) — "
                           f"refusing to serve {symbol} {timeframe}")
            return None

        fetch_n = max(count * 3, count + 10)   # margin for NaN drops / scoping
        # Poison filter (v3.1): exclude non-positive prices and future-dated bars
        # (DXFeed 2**31 rollover junk). A 2038-stamped bar would otherwise sort to
        # the top of the DESC window and land at the END of the ascending frame —
        # i.e. it would masquerade as the newest bar to every engine.
        cur = conn.execute(
            "SELECT ts_epoch_ms, open, high, low, close, volume FROM candles "
            "WHERE symbol=? AND interval=? AND close > 0 AND open > 0 "
            "AND ts_epoch_ms <= ? "
            "ORDER BY ts_epoch_ms DESC LIMIT ?",
            (symbol, timeframe, int((_time.time() + 172_800) * 1000), fetch_n))
        rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        logger.warning(f"feed store has no bars for {symbol} {timeframe}")
        return None

    rows.reverse()                              # ascending
    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
    idx = pd.to_datetime(df.pop("ts"), unit="ms", utc=True).dt.tz_convert(ET)
    df.index = pd.DatetimeIndex(idx)
    df = df.dropna(subset=["open", "high", "low", "close"])
    if df.empty:
        logger.warning(f"feed store bars for {symbol} {timeframe} all NaN")
        return None

    # Intraday scope: never pad the window across the overnight gap with the
    # prior session's bars. Scope 1m/5m/15m to the most recent session in the
    # frame. Fewer-than-count early in the session is real data, not failure.
    if timeframe in INTRADAY_TFS and INTRADAY_SCOPE != "continuous":
        last_ts = df.index[-1]
        session_open = datetime.combine(
            last_ts.date(), dtime(*SESSION_OPEN_HM), tzinfo=ET)
        df = df[df.index >= session_open]
        if df.empty:
            logger.warning(f"no bars in latest session for {symbol} {timeframe}")
            return None

    if len(df) > count:
        df = df.iloc[-count:]

    logger.debug(f"{symbol} {timeframe}: {len(df)} candles via feed store")
    return df


def fetch_quote(symbol: str) -> Optional[float]:
    """
    Fetch current price.
    Primary:   shared feed store — latest 1m bar close (fresh, same tape the
               bot trades on)
    Secondary: TastyTrade SDK market-data endpoint (REST, same broker)

    Returns:
        Current price as float, or None on failure.
    """
    # Primary: feed store latest 1m close
    conn = _connect_ro()
    if conn is not None:
        try:
            if _feed_alive(conn):
                cur = conn.execute(
                    "SELECT ts_epoch_ms, close FROM candles "
                    "WHERE symbol=? AND interval='1m' AND close > 0 "
                    "AND ts_epoch_ms <= ? "
                    "ORDER BY ts_epoch_ms DESC LIMIT 1",
                    (symbol, int((_time.time() + 172_800) * 1000)))
                row = cur.fetchone()
                if row and row[1] is not None:
                    age = _time.time() - (float(row[0]) / 1000.0)
                    price = float(row[1])
                    # A quote must be POSITIVE and NOT from the future. A poison
                    # bar (DXFeed 2**31 rollover ts, close=0.0 — GOOGL 2026-07-13)
                    # would otherwise win the ORDER BY, compute a NEGATIVE age
                    # (passing the freshness check) and return 0.0, which
                    # run_analysis reads as falsy => "Could not fetch current
                    # price" => dead tick loop while the unit reports ACTIVE.
                    # The SQL filters it, and 0 <= age re-asserts it here.
                    if price > 0 and 0 <= age <= QUOTE_MAX_AGE_S:
                        return price
                    logger.debug(f"store 1m bar for {symbol} unusable "
                                 f"(price={price} age={age:.0f}s) — "
                                 f"falling back to TastyTrade REST quote")
        except Exception as e:
            logger.debug(f"store quote failed for {symbol}: {e}")
        finally:
            conn.close()

    # Secondary: TastyTrade SDK
    try:
        from tastytrade.market_data import get_market_data
        from tastytrade.order import InstrumentType
        from data.tasty_client import run_async

        session   = get_session()
        inst_type = (InstrumentType.INDEX if symbol in ("SPX", "VIX")
                     else InstrumentType.EQUITY)
        md        = run_async(get_market_data(session, symbol, inst_type))

        if md and md.mark is not None:
            return float(md.mark)
        if md and md.bid is not None and md.ask is not None:
            return float((md.bid + md.ask) / 2)
        if md and md.last is not None:
            return float(md.last)

    except Exception as e:
        logger.debug(f"TastyTrade quote unavailable for {symbol}: {e}")

    return None


def fetch_all_candles(symbol: str = INSTRUMENT) -> Dict[str, Optional[pd.DataFrame]]:
    """Fetch all configured timeframes for the underlying."""
    result = {}
    for tf, cfg in TIMEFRAMES.items():
        df = fetch_candles(symbol, tf, cfg["candles"])
        result[tf] = df
        if df is not None:
            logger.debug(f"{symbol} {tf}: {len(df)} candles")
    return result
