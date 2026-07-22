"""
execution/limit_ladder.py — Mid-anchored limit pricing for entries and exits.
v1.2 — 2026-07-22 — hard-close escalation: 15:40 mark-limits -> 15:45 MARKET.
v1.1 — 2026-07-22 — simplified to MARK-REPRICING (no synthetic tick-walk).

WHY THIS EXISTS
---------------
Before this, single-leg entries AND single-leg exits were MARKET orders, and
spread closes used a fixed $0.10 buffer past mark. On a $0.20 0DTE contract
with a $0.05 spread that is ~25% of premium round-trip — larger than any edge
the strategies are trying to capture. Every price in this system is derived
from mark ((bid+ask)/2), so the DECISION was made at mid while the FILL paid
the touch on both sides.

THE POLICY
----------
We never cross the spread. We post AT THE MARK and re-post at the NEW mark
every tick (~15s) until filled.

  OPENS   Post at mark and let it sit. Re-priced to the current mark each tick.
          An entry that never fills costs nothing — the trade simply is not
          taken and the strategy re-signals next tick.

  CLOSES  Post at mark, and RE-PRICE to the current mark every tick until it
          fills. This is the important property: because the limit re-anchors
          to the live mark on every retry, it CHASES a falling market down
          instead of parking at a stale price. A stop triggered at 0.60 does
          not sit at 0.60 while the contract prints 0.40 — the next tick posts
          at the new mark, and the next, until it fills.

  The exit TRIGGER (e.g. -40%) decides WHEN to start closing. It NEVER anchors
  WHERE the limit sits. That separation is the whole point.

  THE ONE EXCEPTION — end-of-day flatten. 15:40 ET starts mark-limit reposts;
  15:45 ET sends a MARKET order, no exceptions, because an unfilled 0DTE at the
  bell is an expiry (and an assignment on a short leg), not an overnight hold.
  See hard_close_order_mode().

v1.1 NOTE: v1.0 shaded the limit one tick further past the mark on each urgent
attempt to synthesise a walk toward the touch. That was dropped — bid/ask are
not plumbed through to the exit path (only a combined mark is), so the shade
was guesswork about a spread we cannot see. Re-pricing at a live mark achieves
the same "follow the market" behaviour honestly and never pays a spread we
have not measured.
"""
from __future__ import annotations

from datetime import time as _time
from typing import Optional

# ── HARD-CLOSE ESCALATION — the ONE exception to "never cross" ────────────────
# Everything else in this module posts at the mark and waits. The end-of-day
# flatten cannot wait: an unfilled 0DTE at the bell does not become an
# overnight hold, it becomes an EXPIRY (and, for a short leg, an assignment).
# So the flatten gets a five-minute mark-limit window and then a market order.
#
#   15:40 ET  begin posting mark-limits, re-priced every tick (~15s)
#   15:45 ET  MARKET order. No exceptions. The position closes.
#
# NB this MOVES the start of the flatten sweep earlier (it was a single 15:45
# market sweep). The extra five minutes is what buys the chance of a mark fill.
HARD_CLOSE_LIMIT_START_ET = _time(15, 40)
HARD_CLOSE_MARKET_AT_ET   = _time(15, 45)


def hard_close_order_mode(now_et) -> str:
    """'limit' | 'market' | 'none' for the end-of-day flatten.

    now_et : timezone-aware ET datetime (or a datetime.time)

    'none'   before 15:40 — the flatten window has not opened.
    'limit'  15:40-15:44  — post at the mark, re-price each tick, try to fill
                            without paying the spread.
    'market' 15:45 onward — the position MUST close; cross and be done.
    """
    t = now_et.time() if hasattr(now_et, "time") else now_et
    if t >= HARD_CLOSE_MARKET_AT_ET:
        return "market"
    if t >= HARD_CLOSE_LIMIT_START_ET:
        return "limit"
    return "none"


def limit_at_mark(mark: float,
                  cap: Optional[float] = None,
                  floor: Optional[float] = None) -> float:
    """The limit price to post this attempt: the CURRENT mark, always.

    mark  : live mark ((bid+ask)/2, or the combined mark for a spread)
    cap   : optional hard ceiling — a vertical can never be worth more than its
            width, so a close is bounded even if the mark is garbage
    floor : optional hard floor — never post below one tick

    Callers re-invoke this every retry tick with a FRESH mark; that re-anchoring
    is what makes the order track the market instead of going stale.
    """
    if mark is None or mark < 0:
        raise ValueError("limit_at_mark: mark must be a non-negative number")
    px = float(mark)
    if cap is not None:
        px = min(px, float(cap))
    if floor is not None:
        px = max(px, float(floor))
    return round(px, 2)


def paper_fill_price(mark: float,
                     cap: Optional[float] = None,
                     floor: Optional[float] = None) -> float:
    """The price PAPER books — the same mark-limit live would have posted.

    Paper previously filled exits at exact mark with ZERO friction while live
    sent MARKET orders, so paper P&L was optimistic by roughly half the spread
    on every exit. Under the mark-limit policy live also targets the mark, so
    paper and live now trade on the same principle.

    LIMITATION, stated plainly: paper assumes the mark-limit FILLS on the
    attempt it is posted. Live may sit unfilled for several ticks, or never
    fill if the mark keeps running away. So paper is now honest about PRICE but
    still optimistic about FILL RATE — the residual gap to model later is
    no-fill risk, not slippage.
    """
    return limit_at_mark(mark, cap=cap, floor=floor)
