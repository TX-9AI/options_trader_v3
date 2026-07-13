"""
data/options_chain.py — Options chain data from TastyTrade SDK.
v3.1 — 2026-07-13 — PERSISTENT CHAIN STREAMER (session-exhaustion fix) + fail-loud.
        The old code opened a NEW DXLinkStreamer websocket on EVERY fetch_chain()
        call — one full REST-token + connect + auth + subscribe + teardown cycle
        per 15 s tick per box. Across the fleet that saturated TastyTrade's
        (unpublished) concurrent-session pool: DXLink returned
        'user sessions has exceeded the configured limit' roughly once per tick
        on 24/29 boxes, quotes/Greeks came back empty, every contract kept
        mark=0.0, the mark>0.05 liquidity filters rejected every strike in every
        regime, and the fleet took ZERO trades on 2026-07-13 while logging a
        plausible-looking "no setup" day. Changes:
        1. ONE long-lived DXLinkStreamer per process (lazy connect on the shared
           tasty_client loop thread, held via AsyncExitStack). Subscriptions are
           RECONCILED (only never-seen symbols subscribed; expiry rollover
           unsubscribes all and resets). Steady state: 2 sessions/box
           (candle-feed + this), ZERO churn.
        2. Reconnect with EXPONENTIAL BACKOFF (5s → 60s cap) on stream failure —
           a saturated pool is never hammered at tick cadence again (the old
           retry-every-15s kept the pool full and made the outage self-sustaining).
        3. Latest-value Greeks/Quote maps persist across ticks (each tick drains
           pending events non-blocking; only never-seen symbols block briefly).
           If the stream is DOWN and the last event is older than
           OT_CHAIN_STALE_S, fetch_chain returns None — stale marks are never
           served as fresh (an open position priced off dead marks would trip
           the -25% floor on garbage).
        4. FAIL-LOUD: a built chain in which NO contract has mark>0 returns None
           with an ERROR log instead of a structurally-valid corpse. Silent
           zero-mark chains are what hid this outage for five hours.
        5. Chain STRUCTURE (REST strike list) is cached OT_CHAIN_STRUCT_REFRESH_S
           (default 30 min) — the 0DTE strike set is static intraday; only
           Greeks/marks need per-tick freshness, and those ride the stream.
        Env knobs: OT_CHAIN_STRUCT_REFRESH_S=1800 · OT_CHAIN_INIT_COLLECT_S=10 ·
        OT_CHAIN_RECONNECT_BASE_S=5 · OT_CHAIN_RECONNECT_MAX_S=60 ·
        OT_CHAIN_STALE_S=120.
v3.0 — 2026-07-03 — delta-band sweep selection (caller passes a strength-scaled
        target delta); ORB nearest-strike snap breaks toward higher/lower delta.
v3.0 — 2026-07-10 — repo-wide v3.0 bump: Yahoo-Finance purge & data stream
        mapping optimization (all market data now flows from the single
        shared TastyTrade candle feed — see data/candle_feed.py). No logic
        change in this file.

Chain fetching:  get_option_chain(session, symbol) → dict[date, list[Option]]
Greeks/marks:    DXLinkStreamer subscription for real-time Greeks and quotes

Workflow:
  1. get_option_chain() returns all Option objects (no pricing)
  2. Filter to today's expiry (0DTE)
  3. Subscribe DXLinkStreamer to get Greeks (delta, IV) and Quote (bid/ask/mark)
  4. Build OptionsChain with fully populated OptionContract objects
"""

import asyncio
import contextlib
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List, Dict
from decimal import Decimal

from tastytrade.instruments import get_option_chain, Option as TTOption, OptionType
from tastytrade.dxfeed import Greeks, Quote
from tastytrade import DXLinkStreamer

from data.tasty_client import get_session, get_loop, run_async, TastyClientError
from config import (
    INSTRUMENT, STRIKE_INCREMENT, CONTRACT_MULTIPLIER,
    SWEEP_DELTA_TOLERANCE, ORB_STRIKE_DELTA_BIAS
)
from utils.math_utils import round_to_strike, floor_to_strike, ceil_to_strike

logger = logging.getLogger(__name__)

# ── v3.1 transport knobs (env-overridable, OT_ convention) ────────────────────
OT_CHAIN_STRUCT_REFRESH_S = float(os.environ.get("OT_CHAIN_STRUCT_REFRESH_S", "1800"))
OT_CHAIN_INIT_COLLECT_S   = float(os.environ.get("OT_CHAIN_INIT_COLLECT_S",   "10"))
OT_CHAIN_RECONNECT_BASE_S = float(os.environ.get("OT_CHAIN_RECONNECT_BASE_S", "5"))
OT_CHAIN_RECONNECT_MAX_S  = float(os.environ.get("OT_CHAIN_RECONNECT_MAX_S",  "60"))
OT_CHAIN_STALE_S          = float(os.environ.get("OT_CHAIN_STALE_S",          "120"))


@dataclass
class OptionContract:
    """A single option contract with pricing and greeks."""
    symbol:         str     = ""    # OCC symbol
    underlying:     str     = ""
    expiry:         str     = ""    # YYYY-MM-DD
    option_type:    str     = ""    # "C" or "P"
    strike:         float   = 0.0
    bid:            float   = 0.0
    ask:            float   = 0.0
    mark:           float   = 0.0
    delta:          float   = 0.0
    gamma:          float   = 0.0
    theta:          float   = 0.0
    vega:           float   = 0.0
    iv:             float   = 0.0
    open_interest:  int     = 0
    volume:         int     = 0
    streamer_symbol: str    = ""    # DXFeed streamer symbol


@dataclass
class OptionsChain:
    """Full 0DTE chain snapshot."""
    underlying:     str = ""
    expiry:         str = ""
    spot_price:     float = 0.0
    iv_rank:        float = 0.0
    calls:          List[OptionContract] = field(default_factory=list)
    puts:           List[OptionContract] = field(default_factory=list)


class OptionsChainFetcher:
    """
    Fetches the 0DTE options chain from TastyTrade and populates
    Greeks/marks via DXLinkStreamer.

    v3.1: ONE persistent streamer per process. All streamer state below is
    touched ONLY on the shared tasty_client loop thread (get_loop()).
    """

    def __init__(self):
        # persistent stream (held open across ticks via AsyncExitStack)
        self._stack:     Optional[contextlib.AsyncExitStack] = None
        self._streamer   = None
        self._subscribed: set = set()
        self._sub_expiry: str = ""            # expiry the subscriptions belong to
        # latest-value event maps (survive ticks; cleared on expiry rollover)
        self._greeks_latest: Dict[str, Greeks] = {}
        self._quotes_latest: Dict[str, Quote]  = {}
        self._last_event_wall: float = 0.0     # wall time of last drained event
        # reconnect backoff
        self._next_connect_ok: float = 0.0     # monotonic
        self._backoff: float = OT_CHAIN_RECONNECT_BASE_S
        # chain-structure cache: symbol -> (monotonic_fetched, chain_map)
        self._struct_cache: Dict[str, tuple] = {}

    def fetch_chain(self, symbol: str = INSTRUMENT,
                    expiry: Optional[str] = None) -> Optional[OptionsChain]:
        """
        Fetch the 0DTE options chain with Greeks and marks.

        Args:
            symbol: Underlying symbol (QQQ, SPY, SPX)
            expiry: YYYY-MM-DD — defaults to today (0DTE)

        Returns:
            OptionsChain or None on failure
        """
        today      = date.today()
        target_date = date.fromisoformat(expiry) if expiry else today
        today_str  = target_date.isoformat()

        try:
            session = get_session()

            # Step 1: chain STRUCTURE (REST) — cached; the 0DTE strike set is
            # static intraday. v3.1: was fetched every tick for no benefit.
            chain_map = self._get_chain_structure(session, symbol)

            if not chain_map:
                logger.warning(f"Empty option chain for {symbol}")
                return None

            # Step 2: Find today's expiration
            options_today: List[TTOption] = chain_map.get(target_date, [])

            if not options_today:
                # Try to find the nearest available expiry
                available = sorted(chain_map.keys())
                future    = [d for d in available if d >= target_date]
                if future:
                    target_date   = future[0]
                    today_str     = target_date.isoformat()
                    options_today = chain_map[target_date]
                    logger.info(f"No 0DTE for {today}, using nearest: {today_str}")
                else:
                    logger.warning(f"No options expiring on or after {today_str}")
                    return None

            logger.info(f"Found {len(options_today)} options for {symbol} {today_str}")

            # Step 3: Build OptionContract list (no pricing yet)
            calls_raw: List[OptionContract] = []
            puts_raw:  List[OptionContract] = []

            for opt in options_today:
                oc = OptionContract(
                    symbol       = opt.symbol,
                    underlying   = symbol,
                    expiry       = today_str,
                    option_type  = "C" if opt.option_type == OptionType.CALL else "P",
                    strike       = float(opt.strike_price),
                    streamer_symbol = opt.streamer_symbol or "",
                )
                if opt.option_type == OptionType.CALL:
                    calls_raw.append(oc)
                else:
                    puts_raw.append(oc)

            # Step 4: Fetch Greeks and quotes via DXLinkStreamer
            streamer_syms = [
                oc.streamer_symbol for oc in calls_raw + puts_raw
                if oc.streamer_symbol
            ]

            if streamer_syms:
                greeks_map, quote_map = self._fetch_greeks_and_quotes(
                    session, streamer_syms, expiry=today_str
                )
                self._apply_market_data(calls_raw, greeks_map, quote_map)
                self._apply_market_data(puts_raw,  greeks_map, quote_map)

            # Step 5: Sort by strike
            calls_raw.sort(key=lambda c: c.strike)
            puts_raw.sort(key=lambda c: c.strike)

            chain = OptionsChain(
                underlying = symbol,
                expiry     = today_str,
                calls      = calls_raw,
                puts       = puts_raw,
            )

            # Populate spot_price from ATM call (nearest delta to 0.50)
            liquid_calls = [c for c in chain.calls if c.delta > 0 and c.mark > 0]
            if liquid_calls:
                try:
                    atm = min(liquid_calls, key=lambda c: abs(c.delta - 0.50))
                    chain.spot_price = atm.strike
                except Exception:
                    pass

            # v3.1 FAIL-LOUD: a chain with zero live marks is a corpse, not data.
            # Serving it lets every liquidity filter reject every strike while
            # the logs look like a quiet no-setup day (2026-07-13). Callers
            # already handle None correctly; None is also strictly safer for an
            # OPEN position than zero marks (premium=0 would trip the -25%
            # floor on garbage).
            if not any(c.mark > 0 for c in chain.calls + chain.puts):
                logger.error(
                    f"Chain FAIL-LOUD: {symbol} {today_str} built with ZERO live "
                    f"marks ({len(chain.calls)}C/{len(chain.puts)}P) — stream "
                    f"down or unpopulated; returning None instead of a corpse"
                )
                return None

            logger.info(
                f"Chain built: {symbol} {today_str} "
                f"calls={len(chain.calls)} puts={len(chain.puts)} "
                f"spot~=${chain.spot_price:.0f}"
            )
            return chain

        except Exception as e:
            logger.error(f"Failed to fetch chain for {symbol}: {e}")
            return None

    def _get_chain_structure(self, session, symbol: str):
        """v3.1 — REST strike-list, cached OT_CHAIN_STRUCT_REFRESH_S. On a REST
        failure with a warm cache, serve the cache and warn (structure is
        static intraday; marks ride the stream and stay fresh regardless)."""
        now = time.monotonic()
        cached = self._struct_cache.get(symbol)
        if cached and (now - cached[0]) < OT_CHAIN_STRUCT_REFRESH_S:
            return cached[1]
        try:
            chain_map = run_async(get_option_chain(session, symbol))
            if chain_map:
                self._struct_cache[symbol] = (now, chain_map)
            return chain_map
        except Exception as e:
            if cached:
                logger.warning(f"Chain structure refresh failed ({e}) — serving "
                               f"cached structure ({now - cached[0]:.0f}s old)")
                return cached[1]
            raise

    def _fetch_greeks_and_quotes(
        self,
        session,
        streamer_symbols: List[str],
        timeout: float = OT_CHAIN_INIT_COLLECT_S,
        expiry: str = ""
    ) -> tuple:
        """
        v3.1 — read Greeks/Quotes from the ONE persistent streamer.
        Ensures the connection (with reconnect backoff), reconciles
        subscriptions, drains pending events non-blocking, and blocks briefly
        only for symbols never seen since (re)subscribe. Returns latest-value
        maps; on stream failure returns the last-known maps (staleness is
        policed in fetch_chain via OT_CHAIN_STALE_S).
        """
        loop = get_loop()
        try:
            future = asyncio.run_coroutine_threadsafe(
                self._stream_snapshot(session, streamer_symbols, timeout, expiry),
                loop
            )
            return future.result(timeout=timeout + 10)
        except Exception as e:
            logger.warning(f"Streamer fetch failed: {e}")
            return self._maps_if_fresh()

    def _maps_if_fresh(self) -> tuple:
        """Last-known maps, but NEVER stale ones: if the stream is down and the
        last event is older than OT_CHAIN_STALE_S, return empty maps so
        fetch_chain fail-louds instead of pricing off dead marks."""
        age = time.time() - self._last_event_wall
        if self._last_event_wall and age <= OT_CHAIN_STALE_S:
            return dict(self._greeks_latest), dict(self._quotes_latest)
        if self._greeks_latest or self._quotes_latest:
            logger.error(f"Chain marks STALE ({age:.0f}s > {OT_CHAIN_STALE_S:.0f}s "
                         f"ceiling) with stream down — refusing to serve them")
        return {}, {}

    async def _stream_snapshot(self, session, streamer_symbols: List[str],
                               timeout: float, expiry: str) -> tuple:
        """Runs on the shared loop thread. All persistent-stream state lives here."""
        if not await self._ensure_streamer(session):
            return self._maps_if_fresh()
        try:
            # Expiry rollover (bots run continuously): yesterday's 0DTE symbols
            # are dead air — unsubscribe everything, clear maps, start clean.
            if expiry and expiry != self._sub_expiry:
                if self._sub_expiry:
                    logger.info(f"Chain streamer expiry rollover "
                                f"{self._sub_expiry} → {expiry}: resubscribing")
                    await self._streamer.unsubscribe_all(Greeks)
                    await self._streamer.unsubscribe_all(Quote)
                self._subscribed.clear()
                self._greeks_latest.clear()
                self._quotes_latest.clear()
                self._sub_expiry = expiry

            new = [s for s in streamer_symbols if s not in self._subscribed]
            if new:
                await self._streamer.subscribe(Greeks, new)
                await self._streamer.subscribe(Quote,  new)
                self._subscribed.update(new)
                logger.info(f"Chain streamer subscribed {len(new)} new symbols "
                            f"({len(self._subscribed)} total)")

            # Drain everything queued since last tick — non-blocking.
            self._drain_nowait()

            # Block briefly ONLY for symbols never seen (first tick after
            # (re)subscribe); steady-state ticks skip this entirely.
            needed = {s for s in streamer_symbols
                      if s not in self._greeks_latest or s not in self._quotes_latest}
            if needed:
                deadline = asyncio.get_event_loop().time() + timeout
                while needed and asyncio.get_event_loop().time() < deadline:
                    try:
                        g = await asyncio.wait_for(
                            self._streamer.get_event(Greeks), timeout=0.5)
                        if g:
                            self._greeks_latest[g.event_symbol] = g
                            self._last_event_wall = time.time()
                    except asyncio.TimeoutError:
                        pass
                    try:
                        q = await asyncio.wait_for(
                            self._streamer.get_event(Quote), timeout=0.5)
                        if q:
                            self._quotes_latest[q.event_symbol] = q
                            self._last_event_wall = time.time()
                    except asyncio.TimeoutError:
                        pass
                    needed = {s for s in needed
                              if s not in self._greeks_latest
                              or s not in self._quotes_latest}

            self._backoff = OT_CHAIN_RECONNECT_BASE_S   # healthy pass resets it
            return dict(self._greeks_latest), dict(self._quotes_latest)

        except Exception as e:
            await self._teardown_streamer()
            self._note_stream_failure(e)
            return self._maps_if_fresh()

    def _drain_nowait(self):
        """Pull every buffered event into the latest-value maps (no blocking)."""
        while True:
            g = self._streamer.get_event_nowait(Greeks)
            if g is None:
                break
            self._greeks_latest[g.event_symbol] = g
            self._last_event_wall = time.time()
        while True:
            q = self._streamer.get_event_nowait(Quote)
            if q is None:
                break
            self._quotes_latest[q.event_symbol] = q
            self._last_event_wall = time.time()

    async def _ensure_streamer(self, session) -> bool:
        """Connect the persistent streamer if absent, honoring the backoff."""
        if self._streamer is not None:
            return True
        if time.monotonic() < self._next_connect_ok:
            logger.debug("Chain streamer in reconnect backoff "
                         f"({self._next_connect_ok - time.monotonic():.0f}s left)")
            return False
        try:
            stack = contextlib.AsyncExitStack()
            streamer = await stack.enter_async_context(DXLinkStreamer(session))
            self._stack, self._streamer = stack, streamer
            self._subscribed.clear()
            self._sub_expiry = ""             # force clean resubscribe
            logger.info("Chain streamer CONNECTED (persistent, v3.1)")
            return True
        except Exception as e:
            self._note_stream_failure(e)
            return False

    def _note_stream_failure(self, e: Exception):
        self._next_connect_ok = time.monotonic() + self._backoff
        logger.warning(f"Chain streamer failure: {e} — next reconnect attempt "
                       f"in {self._backoff:.0f}s")
        self._backoff = min(self._backoff * 2, OT_CHAIN_RECONNECT_MAX_S)

    async def _teardown_streamer(self):
        stack, self._stack, self._streamer = self._stack, None, None
        self._subscribed.clear()
        if stack is not None:
            try:
                await stack.aclose()
            except Exception:
                pass

    def close(self):
        """Tear down the persistent streamer (tests / clean shutdown)."""
        if self._streamer is None:
            return
        try:
            asyncio.run_coroutine_threadsafe(
                self._teardown_streamer(), get_loop()).result(timeout=10)
        except Exception:
            pass

    def _apply_market_data(
        self,
        contracts: List[OptionContract],
        greeks_map: Dict[str, Greeks],
        quote_map:  Dict[str, Quote]
    ):
        """Apply Greeks and Quote data to OptionContract objects."""
        for oc in contracts:
            sym = oc.streamer_symbol

            greek = greeks_map.get(sym)
            if greek:
                oc.delta = float(greek.delta or 0)
                oc.gamma = float(greek.gamma or 0)
                oc.theta = float(greek.theta or 0)
                oc.vega  = float(greek.vega  or 0)
                oc.iv    = float(greek.volatility or 0)

            quote = quote_map.get(sym)
            if quote:
                bid = float(quote.bid_price or 0)
                ask = float(quote.ask_price or 0)
                oc.bid  = bid
                oc.ask  = ask
                oc.mark = (bid + ask) / 2 if bid > 0 and ask > 0 else (bid or ask)

    # ─── Strike Selection ─────────────────────────────────────────────────────

    def select_orb_strike(self, chain: OptionsChain, direction: str,
                           target_strike: int,
                           delta_bias: str = ORB_STRIKE_DELTA_BIAS
                           ) -> Optional[OptionContract]:
        """Nearest liquid strike to target_strike. When strikes bracket the target
        equally, break toward the higher- (more ITM/participation) or lower-
        (further OTM) |delta| per delta_bias."""
        contracts = chain.calls if direction == "long" else chain.puts
        candidates = [c for c in contracts if c.mark > 0.05]
        if not candidates:
            logger.warning("No liquid contracts in chain")
            return None
        min_dist = min(abs(c.strike - target_strike) for c in candidates)
        nearest = [c for c in candidates
                   if abs(c.strike - target_strike) <= min_dist + 1e-6]
        if len(nearest) == 1:
            best = nearest[0]
        elif delta_bias == "lower":
            best = min(nearest, key=lambda c: abs(c.delta))
        else:  # "higher" — more ITM / more directional participation
            best = max(nearest, key=lambda c: abs(c.delta))
        logger.info(
            f"ORB strike: {best.option_type} {best.strike} "
            f"mark=${best.mark:.2f} delta={best.delta:.3f} (bias={delta_bias})"
        )
        return best

    def select_sweep_strike(self, chain: OptionsChain,
                             direction: str,
                             target_delta: float,
                             tolerance: float = SWEEP_DELTA_TOLERANCE
                             ) -> Optional[OptionContract]:
        """Select the OTM strike whose |delta| is nearest target_delta (the caller
        scales target_delta by reversal strength). Prefers strikes within
        +/- tolerance of the target; falls back to the nearest available."""
        pool = chain.calls if direction == "long" else chain.puts
        liquid = [c for c in pool if c.mark > 0.05 and 0.0 < abs(c.delta) <= 0.55]
        if not liquid:
            return None
        band = [c for c in liquid if abs(abs(c.delta) - target_delta) <= tolerance]
        pick_from = band if band else liquid
        best = min(pick_from, key=lambda c: abs(abs(c.delta) - target_delta))
        logger.info(
            f"Sweep strike: {best.option_type} {best.strike} "
            f"mark=${best.mark:.2f} delta={best.delta:.3f} "
            f"(target={target_delta:.2f}{'' if band else ', band empty->nearest'})"
        )
        return best

    def select_butterfly_strikes(self, chain: OptionsChain,
                                  direction: str,
                                  current_price: float,
                                  wing_width_strikes: int
                                  ) -> Optional[Dict[str, OptionContract]]:
        """Select center (ATM) ± wing_width butterfly strikes."""
        center_strike = round_to_strike(current_price, STRIKE_INCREMENT)
        lower_strike  = center_strike - wing_width_strikes * STRIKE_INCREMENT
        upper_strike  = center_strike + wing_width_strikes * STRIKE_INCREMENT

        contracts = chain.calls if direction == "call" else chain.puts

        def find_strike(target: int) -> Optional[OptionContract]:
            candidates = [c for c in contracts if c.mark > 0 and c.strike == target]
            if candidates:
                return candidates[0]
            liquid = [c for c in contracts if c.mark > 0]
            if not liquid:
                return None
            return min(liquid, key=lambda c: abs(c.strike - target))

        lower  = find_strike(lower_strike)
        center = find_strike(center_strike)
        upper  = find_strike(upper_strike)

        if not all([lower, center, upper]):
            logger.warning(
                f"Butterfly: could not find all strikes "
                f"{lower_strike}/{center_strike}/{upper_strike}"
            )
            return None

        logger.info(
            f"Butterfly: {direction.upper()} "
            f"{lower.strike}/{center.strike}/{upper.strike} "
            f"marks={lower.mark:.2f}/{center.mark:.2f}/{upper.mark:.2f}"
        )
        return {"lower": lower, "center": center, "upper": upper}

    def get_iv_rank(self, chain: OptionsChain) -> float:
        """Estimate IV rank. Falls back to ATM call IV."""
        if chain.iv_rank > 0:
            return chain.iv_rank
        if chain.calls:
            atm = min(chain.calls, key=lambda c: abs(c.delta - 0.5))
            return atm.iv * 100
        return 0.0


# Singleton
_fetcher: Optional[OptionsChainFetcher] = None


def get_chain_fetcher() -> OptionsChainFetcher:
    global _fetcher
    if _fetcher is None:
        _fetcher = OptionsChainFetcher()
    return _fetcher