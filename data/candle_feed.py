"""
options_trader_v3/data/candle_feed.py — THE single candle-feed producer. v3.0
v3.0 — 2026-07-10 — initial release (Yahoo-Finance purge; single shared TastyTrade
        candle feed / data stream mapping optimization). This service owns the
        ONLY DXLinkStreamer subscription on the box. Every other process (the
        trading bot, the shadow observer, the candle logger, query tools) reads
        the shared SQLite store this service maintains. One producer, many
        readers — it is FORBIDDEN for any consumer to open its own DXFeed
        stream.
v3.2 — 2026-07-13 — POISON-CANDLE GUARD (producer side). Reject at ingest any
        candle whose timestamp falls outside a sane window (kills the DXFeed
        signed-32-bit rollover bar: ts=2147483648xxx ms => year 2038) or whose
        OHLC contains a non-positive price. Observed live on GOOGL 2026-07-13:
        the junk bar entered the store, won the "latest bar" query in
        fetch_quote(), returned 0.0, and killed the bot's tick loop every tick
        while the unit still reported ACTIVE. Also adds FeedStore.purge_poison(),
        run at startup, so a box whose store was already poisoned self-heals on
        restart with no manual sqlite surgery across the fleet.
v3.3 — 2026-07-13 — CROSS-THREAD SQLITE FIX. FeedStore's connection is built on
        the MAIN thread but every write (_flush -> upsert_candles / heartbeat /
        commit / prune) is driven from the asyncio event-loop thread created by
        get_loop(). Python's sqlite3 rejects that by default, so candle-feed
        died on its FIRST flush on every start ("SQLite objects created in a
        thread can only be used in that same thread") and systemd's
        Restart=on-failure turned it into a crash-loop — which in turn piled up
        DXLink sessions until TastyTrade returned "The number of user sessions
        has exceeded the configured limit" (GOOGL, 2026-07-13). Connection now
        uses check_same_thread=False with an explicit threading.Lock
        serializing every write; still a single writer, so WAL semantics are
        unchanged.

Architecture (Mandate 2 of the Yahoo-Finance purge):
  - Runs as its own systemd unit: candle-feed.service (Before=optionsbot).
  - Reuses data.tasty_client.get_session() and get_loop() — one login, one
    background event loop, no duplication.
  - Subscribes ONCE to this box's symbol (config.INSTRUMENT) across every
    interval in config.TIMEFRAMES (1m, 5m, 15m, 1h, 1d) plus VIX (1m + 1d),
    with per-interval backfill start times deep enough to satisfy
    TIMEFRAMES[tf]["candles"] with margin (entitlement permitting — see
    FIRST-RUN CHECKLIST below).
  - Maintains a rolling in-memory buffer, last-write-wins per int(candle.time)
    (DXFeed re-sends/corrects bars — same mechanics proven in
    candle_logger._collect v1.x, consolidated here as a PERSISTENT
    subscription instead of a one-shot drain).
  - Flushes the buffer to an on-box SQLite store in WAL mode (one writer, many
    concurrent readers, atomic, survives consumer restarts):
        candles(symbol, interval, ts_epoch_ms, open, high, low, close, volume)
        feed_meta(symbol, interval, last_write_epoch)   -- staleness detection
    plus a global heartbeat row feed_meta('__feed__','heartbeat') updated on
    every flush cycle so readers can detect a dead feed even when no new bars
    are arriving (e.g. the forming 1d bar).
  - Keeps a bounded history per (symbol, interval): PRUNE_FACTOR x the largest
    configured count, pruned periodically.
  - Reconnects with backoff if the streamer drops; re-backfills from session
    open so corrected bars are re-applied.

Store location (producer and every consumer must resolve identically):
  $OT_FEED_DB if set, else <repo>/data/feed_store.db  (self-locating, same
  pattern as candle_logger's OHLC dir — no /var/lib permission trap).

DXFeed symbology:
  Equities/ETFs use the plain ticker. Index boxes may need a DXFeed-specific
  symbol — set OT_DXFEED_SYMBOL to override (e.g. OT_DXFEED_SYMBOL=SPX).
  VIX subscribes as $OT_DXFEED_VIX (default "VIX").
  Candle events arrive as 'QQQ{=1m}' — base symbol = split on '{'. Bars are
  stored under the BOT's symbol name (config.INSTRUMENT / "VIX"), not the
  DXFeed alias, so readers never need the mapping.

FIRST-RUN CHECKLIST (one box, before fleet deploy — mirrors candle_logger v1.x):
  1. History depth / entitlement: journalctl -u candle-feed | grep "backfill"
     — every interval must report >= its configured count (1h needs ~10
     trading days, 1d needs ~3 weeks). Thin entitlement on 1h/1d will surface
     here, NOT as a silent short window downstream. The persistent buffer
     accumulates over the session, so intraday depth grows on its own.
  2. VIX entitlement: grep "VIX" — if DXFeed lacks VIX on your entitlement,
     macro falls back stale->default-20 (fail-loud WARNING). See
     data/macro_data.py v3.0 header for the flagged alternative.
  3. Index symbology: SPX box — set OT_DXFEED_SYMBOL and confirm bars land.

Usage:
    python -m data.candle_feed                 # foreground (systemd runs this)
    python -m data.candle_feed --once          # single backfill+flush, then exit
                                               # (smoke test / pre-open warm)
"""
import argparse
import asyncio
import logging
import os
import sqlite3
import threading
import time as _time
from datetime import datetime, time as dtime, timedelta
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

from tastytrade import DXLinkStreamer           # module-level so tests can patch
from tastytrade.dxfeed import Candle

from config import INSTRUMENT, TIMEFRAMES
from data.tasty_client import get_session, get_loop

logger = logging.getLogger(__name__)

# ── Poison-candle sanity window (v3.2) ────────────────────────────────────────
# Any candle timestamp outside this window is junk. The observed failure is the
# signed-32-bit rollover (2**31 * 1000 = 2147483648000 ms => 2038-01-19), which
# is far in the future; a 0 / negative ts is equally invalid. Upper bound is
# computed at call time (now + 2 days) so a legitimately-fresh bar is never
# rejected for clock skew, while a 2038 bar always is.
TS_MS_MIN = 1_262_304_000_000        # 2010-01-01 — older than any bar we'd want


def _ts_ms_max() -> int:
    """Newest acceptable candle ts: now + 2 days (tolerates clock skew, kills 2038)."""
    return int((_time.time() + 172_800) * 1000)
ET = ZoneInfo("America/New_York")

# ─── Store location — single definition, imported by every reader ─────────────

def feed_db_path() -> str:
    """Resolve the shared store path. $OT_FEED_DB overrides; default is
    self-locating inside the repo's data/ dir so producer and consumers on the
    same checkout always agree."""
    env = os.environ.get("OT_FEED_DB", "").strip()
    if env:
        return env
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "feed_store.db")


# ─── Tunables ──────────────────────────────────────────────────────────────────

SESSION_OPEN_HM   = (9, 30)          # ET
FLUSH_INTERVAL_S  = 2.0              # buffer -> SQLite cadence (also heartbeat)
PRUNE_FACTOR      = 4                # keep count*FACTOR rows per interval
PRUNE_EVERY_S     = 300
RECONNECT_MIN_S   = 3
RECONNECT_MAX_S   = 60
VIX_SYMBOL        = os.environ.get("OT_DXFEED_VIX", "VIX")
VIX_INTERVALS     = ("1m", "1d")

# Backfill depth per interval: calendar days back from now that comfortably
# cover TIMEFRAMES count (RTH ~6.5h/day, ~78 5m bars, ~26 15m bars, ~7 1h bars).
BACKFILL_DAYS = {
    "1m":  1,      # today's session (plus yesterday if pre-open)
    "5m":  4,      # 100 bars ≈ 1.3 sessions -> 4 cal days covers weekends
    "15m": 6,      # 50 bars ≈ 2 sessions
    "1h":  16,     # 50 bars ≈ 8 sessions
    "1d":  30,     # 10 bars ≈ 2 weeks + margin
}


def _dxfeed_symbol() -> str:
    return os.environ.get("OT_DXFEED_SYMBOL", "").strip() or INSTRUMENT


def _base_symbol(event_symbol: str) -> str:
    """'QQQ{=5m}' -> 'QQQ'."""
    return (event_symbol or "").split("{")[0]


def _backfill_start(interval: str, now_et: Optional[datetime] = None) -> datetime:
    now_et = now_et or datetime.now(ET)
    days = BACKFILL_DAYS.get(interval, 4)
    if interval == "1m":
        # Today's session open; if pre-open, previous calendar day's open so the
        # most recent session is available (readers scope to one session).
        d = now_et.date()
        if now_et.time() < dtime(*SESSION_OPEN_HM):
            d = d - timedelta(days=1)
        return datetime.combine(d, dtime(*SESSION_OPEN_HM), tzinfo=ET)
    return now_et - timedelta(days=days)


# ─── SQLite store (WAL, one writer — this process) ────────────────────────────

class FeedStore:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # check_same_thread=False + an explicit lock (v3.3).
        # The store is constructed on the MAIN thread but every write
        # (_flush -> upsert_candles/heartbeat/commit) is driven from the asyncio
        # event-loop thread created by get_loop(). Python's sqlite3 rejects that
        # by default:
        #   ProgrammingError: SQLite objects created in a thread can only be
        #   used in that same thread.
        # which killed candle-feed on its first flush, every start (GOOGL,
        # 2026-07-13). We remain a SINGLE writer — the lock serializes access so
        # allowing cross-thread use is safe.
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS candles (
                symbol      TEXT NOT NULL,
                interval    TEXT NOT NULL,
                ts_epoch_ms INTEGER NOT NULL,
                open REAL, high REAL, low REAL, close REAL, volume REAL,
                PRIMARY KEY (symbol, interval, ts_epoch_ms)
            );""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS feed_meta (
                symbol   TEXT NOT NULL,
                interval TEXT NOT NULL,
                last_write_epoch REAL NOT NULL,
                PRIMARY KEY (symbol, interval)
            );""")
        self.conn.commit()

    def upsert_candles(self, rows: List[Tuple]):
        """rows: (symbol, interval, ts_ms, o, h, l, c, v). Last write wins."""
        if not rows:
            return
        with self._lock:
            self._upsert_candles_locked(rows)

    def _upsert_candles_locked(self, rows: List[Tuple]):
        self.conn.executemany(
            "INSERT OR REPLACE INTO candles "
            "(symbol, interval, ts_epoch_ms, open, high, low, close, volume) "
            "VALUES (?,?,?,?,?,?,?,?)", rows)
        now = _time.time()
        touched = {(r[0], r[1]) for r in rows}
        self.conn.executemany(
            "INSERT OR REPLACE INTO feed_meta (symbol, interval, last_write_epoch) "
            "VALUES (?,?,?)", [(s, i, now) for (s, i) in touched])

    def purge_poison(self) -> int:
        """Delete any poison rows already in the store (v3.2). Runs at feed
        startup so a box whose DB was poisoned before this guard existed
        self-heals on restart — no manual sqlite surgery across the fleet."""
        with self._lock:
            cur = self.conn.execute(
                "DELETE FROM candles WHERE open <= 0 OR high <= 0 OR low <= 0 "
                "OR close <= 0 OR ts_epoch_ms < ? OR ts_epoch_ms > ?",
                (TS_MS_MIN, _ts_ms_max()))
            self.conn.commit()
            n = cur.rowcount or 0
        if n:
            logger.warning("purged %d poison candle row(s) from the store", n)
        return n

    def heartbeat(self):
        with self._lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO feed_meta (symbol, interval, last_write_epoch) "
                "VALUES ('__feed__','heartbeat',?)", (_time.time(),))

    def commit(self):
        with self._lock:
            self.conn.commit()

    def prune(self, symbol: str, interval: str, keep: int):
        with self._lock:
            self._prune_locked(symbol, interval, keep)

    def _prune_locked(self, symbol: str, interval: str, keep: int):
        self.conn.execute("""
            DELETE FROM candles WHERE symbol=? AND interval=? AND ts_epoch_ms NOT IN
            (SELECT ts_epoch_ms FROM candles WHERE symbol=? AND interval=?
             ORDER BY ts_epoch_ms DESC LIMIT ?)""",
            (symbol, interval, symbol, interval, keep))

    def bar_count(self, symbol: str, interval: str) -> int:
        with self._lock:
            cur = self.conn.execute(
                "SELECT COUNT(*) FROM candles WHERE symbol=? AND interval=?",
                (symbol, interval))
            return int(cur.fetchone()[0])

    def close(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception:
            pass


# ─── The producer ──────────────────────────────────────────────────────────────

class CandleFeed:
    """Persistent single subscription -> in-memory last-write-wins buffer ->
    periodic flush to the shared store."""

    def __init__(self, store: FeedStore):
        self.store = store
        self.dx_symbol = _dxfeed_symbol()
        # (dxfeed_symbol, interval) -> store symbol name
        self.symbol_map: Dict[Tuple[str, str], str] = {}
        self.subs: List[Tuple[str, str, datetime]] = []   # (dx_sym, interval, start)
        for tf in TIMEFRAMES.keys():
            self.subs.append((self.dx_symbol, tf, _backfill_start(tf)))
            self.symbol_map[(self.dx_symbol, tf)] = INSTRUMENT
        for tf in VIX_INTERVALS:
            self.subs.append((VIX_SYMBOL, tf, _backfill_start(tf)))
            self.symbol_map[(VIX_SYMBOL, tf)] = "VIX"
        # buffer[(store_symbol, interval)][ts_ms] = row tuple
        self.buffer: Dict[Tuple[str, str], Dict[int, Tuple]] = {}
        self.backfill_logged: Dict[Tuple[str, str], bool] = {}
        self._unmapped_seen: set = set()   # v3.5: warn-once on unmapped candles

    def _interval_of(self, event_symbol: str) -> Optional[str]:
        """Map DXFeed's echoed candle symbol back to OUR config timeframe key.

        'AAPL{=5m}'            -> '5m'
        'AAPL{=5m,tho=true}'   -> '5m'    (attributes stripped)
        'AAPL{=m,tho=true}'    -> '1m'    (DXFeed canonicalizes 1m -> m)
        'AAPL{=h,tho=true}'    -> '1h'
        'AAPL{=d,tho=true}'    -> '1d'

        v3.5 — TWO bugs fixed here, both of which SILENTLY DROPPED EVERY CANDLE:
        (1) DXFeed echoes the symbol back with its ATTRIBUTES attached (the
            trading-hours flag, ',tho=true'); the old parser returned
            '5m,tho=true' and never matched symbol_map.
        (2) DXFeed CANONICALIZES a leading 1: we subscribe '1m'/'1h'/'1d' and it
            echoes 'm'/'h'/'d'. Even with (1) fixed, those three would still miss
            the map — and 1m is what fetch_quote() reads, i.e. the bot's price.
        Result on 2026-07-14: feeds 'active', authenticated and streaming, store
        taking ZERO writes; bots read yesterday's bars, no ORB range for today,
        fleet-wide EXPIRED/UNKNOWN, and not one error logged anywhere.
        """
        if "{=" not in (event_symbol or ""):
            return None
        token = event_symbol.split("{=", 1)[1].rstrip("}")
        token = token.split(",", 1)[0].strip()      # drop ',tho=true' etc.
        # Re-expand DXFeed's canonical bare units back to our config keys.
        return {"m": "1m", "h": "1h", "d": "1d", "s": "1s"}.get(token, token)

    def _on_candle(self, c: Candle):
        ev_sym = getattr(c, "event_symbol", "")
        base = _base_symbol(ev_sym)
        interval = self._interval_of(ev_sym) or ""
        key_sym = self.symbol_map.get((base, interval))
        if key_sym is None:
            # v3.5: NEVER drop a candle silently. This branch swallowed the
            # entire feed on 2026-07-14 (unparsed 'tho=true' attribute) with no
            # log line anywhere. Warn once per distinct unmapped key.
            if ev_sym and (base, interval) not in self._unmapped_seen:
                self._unmapped_seen.add((base, interval))
                logger.warning(
                    "DROPPING candles: event_symbol=%r parsed to (base=%r, interval=%r) "
                    "which is NOT in symbol_map %r — nothing will be stored for it",
                    ev_sym, base, interval, sorted(self.symbol_map.keys()))
            return
        if c.time is None or c.open is None:
            return

        # ── POISON GUARD (v3.2) ───────────────────────────────────────────────
        # DXFeed intermittently emits a junk candle: timestamp at the signed
        # 32-bit rollover (2147483648xxx ms => year 2038) with all prices 0.0.
        # Observed live on GOOGL 2026-07-13 (1m, then 15m). It is fatal
        # downstream: fetch_quote() sorts by ts DESC, so the 2038 row wins, its
        # age computes NEGATIVE (passes the freshness check), and it returns
        # close=0.0. run_analysis() treats 0.0 as falsy -> "Could not fetch
        # current price" -> the tick loop dies EVERY TICK while the unit still
        # reports ACTIVE. Silent, total. Reject it at the door: bad data must
        # never enter the store.
        try:
            ts_ms = int(c.time)
            o, h, l, cl = float(c.open), float(c.high), float(c.low), float(c.close)
        except (TypeError, ValueError):
            return

        if not (TS_MS_MIN <= ts_ms <= _ts_ms_max()):
            logger.warning(
                "REJECTED poison candle %s %s: insane ts=%d (%.1f) — outside sane window",
                key_sym, interval, ts_ms, ts_ms / 1000.0)
            return
        if o <= 0 or h <= 0 or l <= 0 or cl <= 0:
            logger.warning(
                "REJECTED poison candle %s %s ts=%d: non-positive price "
                "(o=%.4f h=%.4f l=%.4f c=%.4f)", key_sym, interval, ts_ms, o, h, l, cl)
            return

        row = (key_sym, interval, ts_ms, o, h, l, cl,
               float(getattr(c, "volume", 0) or 0))
        self.buffer[(key_sym, interval)] = self.buffer.get((key_sym, interval), {})
        self.buffer[(key_sym, interval)][ts_ms] = row

    def _flush(self):
        rows: List[Tuple] = []
        for bucket in self.buffer.values():
            rows.extend(bucket.values())
        self.buffer = {}
        self.store.upsert_candles(rows)
        self.store.heartbeat()
        self.store.commit()
        return len(rows)

    def _log_backfill_depth(self):
        """One-time per (symbol, interval): report depth vs required count so
        entitlement gaps surface in the journal (FIRST-RUN CHECKLIST #1)."""
        for (dx_sym, tf, _start) in self.subs:
            sym = self.symbol_map[(dx_sym, tf)]
            if self.backfill_logged.get((sym, tf)):
                continue
            n = self.store.bar_count(sym, tf)
            need = TIMEFRAMES.get(tf, {}).get("candles", 0) if sym == INSTRUMENT else 1
            level = logging.INFO if n >= need else logging.WARNING
            logger.log(level, "backfill %s %s: %d bars in store (need %d)%s",
                       sym, tf, n, need, "" if n >= need else "  << SHORT — check entitlement")
            self.backfill_logged[(sym, tf)] = True

    async def run(self, once: bool = False):
        session = get_session()
        backoff = RECONNECT_MIN_S
        while True:
            try:
                async with DXLinkStreamer(session) as streamer:
                    for (dx_sym, tf, start) in self.subs:
                        await streamer.subscribe_candle([dx_sym], tf, start_time=start)
                        logger.info("subscribed %s %s from %s", dx_sym, tf, start.isoformat())
                    backoff = RECONNECT_MIN_S
                    last_flush = 0.0
                    last_prune = _time.time()
                    quiet_since: Optional[float] = None
                    while True:
                        try:
                            c = await asyncio.wait_for(streamer.get_event(Candle), timeout=1.0)
                            self._on_candle(c)
                            quiet_since = None
                        except asyncio.TimeoutError:
                            if quiet_since is None:
                                quiet_since = _time.monotonic()
                        now = _time.monotonic()
                        if now - last_flush >= FLUSH_INTERVAL_S:
                            n = self._flush()
                            last_flush = now
                            if n:
                                logger.debug("flushed %d bars", n)
                            self._log_backfill_depth()
                            if once and quiet_since is not None and (now - quiet_since) > 8.0:
                                logger.info("--once: backfill drained, exiting")
                                return
                        if _time.time() - last_prune >= PRUNE_EVERY_S:
                            for (dx_sym, tf, _s) in self.subs:
                                sym = self.symbol_map[(dx_sym, tf)]
                                need = TIMEFRAMES.get(tf, {}).get("candles", 60)
                                self.store.prune(sym, tf, max(need, 60) * PRUNE_FACTOR)
                            self.store.commit()
                            last_prune = _time.time()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self._flush()
                logger.error("feed stream error: %s — reconnecting in %ds", e, backoff)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, RECONNECT_MAX_S)


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true",
                    help="backfill, flush, exit (smoke test)")
    ap.add_argument("--db", default=None, help="override store path")
    args = ap.parse_args()

    if args.db:
        os.environ["OT_FEED_DB"] = args.db
    store = FeedStore(feed_db_path())
    logger.info("candle_feed v3.5 — store=%s symbol=%s (dxfeed=%s) vix=%s",
                feed_db_path(), INSTRUMENT, _dxfeed_symbol(), VIX_SYMBOL)
    store.purge_poison()   # v3.2: self-heal any pre-existing poison rows

    feed = CandleFeed(store)
    loop = get_loop()
    fut = asyncio.run_coroutine_threadsafe(feed.run(once=args.once), loop)
    try:
        fut.result()          # blocks for service lifetime
    except KeyboardInterrupt:
        fut.cancel()
    finally:
        store.close()


if __name__ == "__main__":
    main()
