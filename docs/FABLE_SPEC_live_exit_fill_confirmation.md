# FABLE SPEC — Live exit fill-confirmation (`_confirm_and_book_live_exit`)

**Repo:** `github.com/TX-9AI/options_trader_v3` · **Owner of this file after build:** Fable
**Status:** paper side is DONE and deployed; this is the LIVE half only.
**Hard rule:** do not touch the paper path or the shared contract below — build only
the live method. One owner per file: you own `_confirm_and_book_live_exit` and the
broker-polling helpers; the seam it plugs into is fixed.

---

## The one-sentence problem

When the bot closes a position in **live/cash** mode, it must book P&L **only after the
broker confirms the fill, at the broker's actual fill price** — never at a mark, never at
entry, never a fabricated `$0.00`, and an unconfirmed close must remain an **open
position**, not a booked row.

## Why this exists (the bug that motivated it)

On 2026-07-15 the 15:45 hard-close flattened ~8 condor legs and logged **every one at
`pnl=+$0.00`**. Root cause: `flatten_all` booked P&L on order *submission success*, at a
fallback price (entry premium), with **no fill confirmation**. In paper that's a
reconcilable bookkeeping error. In live it is a position-truth catastrophe: the DB says
flat, the broker may not be, P&L is fiction, and the `DAILY_LOSS_LIMIT` circuit breaker
(which halts on realized P&L) is now reading fabricated numbers. This spec closes that
hole for live trading.

## What is already done (do not redo, do not change)

`execution/exit_engine.py` v3.4 and `execution/position_manager.py` v3.4 now use a shared
result contract. **This is the seam. It is fixed. Build to it.**

```python
@dataclass
class FillResult:
    confirmed:  bool                      # True ONLY on a real, completed close
    fill_price: Optional[float] = None    # ACTUAL close price; None iff not confirmed
    order_id:   Optional[str]   = None    # broker order id (live)
    partial:    bool            = False   # partially filled, remainder still working
    detail:     str             = ""      # human-readable status for logs/alerts
```

- `place_exit_order(record, reason, mark_price=None) -> FillResult`
  - **PAPER (built, frozen):** simulates the fill at `mark_price`, returns
    `FillResult(confirmed=True, fill_price=mark_price)`. One pass — a simulated close
    always succeeds; no polling, no retry, no reuse.
  - **LIVE (your job):** calls `self._confirm_and_book_live_exit(record, reason, mark_price)`.
- `_execute_exit` (position_manager) books **only** when `fill.confirmed and fill.fill_price
  is not None`, using `fill.fill_price`. On `confirmed=False` it books nothing and returns
  `False`, and `flatten_all` retries every tick 15:45→16:00 and escalates. **You do not need
  to touch any of this** — return a correct `FillResult` and the accounting is handled.
- `_submit_live_close(record) -> bool` already exists: it submits the SELL_TO_CLOSE / spread
  order via the tastytrade SDK and returns submit success. **Submission is not a fill** — it
  is provided for you to call as step 1, nothing more.
- Current live stub raises `NotImplementedError` on purpose, so cash cannot be enabled until
  you ship this. That is the safety property; preserve it until the real thing is proven.

## What you must build

Implement `ExitEngine._confirm_and_book_live_exit(self, record, reason, mark_price) ->
FillResult` with this contract:

1. **Submit** the close (use `_submit_live_close(record)` or inline equivalent) and **capture
   the broker order id.** If submission fails → `FillResult(confirmed=False,
   detail="submit failed")`.
2. **Poll** broker order status for that order id on a **bounded** loop:
   - poll interval and total deadline configurable (propose `LIVE_FILL_POLL_SECONDS` and
     `LIVE_FILL_DEADLINE_SECONDS` in `config.py`; sensible defaults e.g. 2s / 30s);
   - terminal states: `filled`, `partially_filled`, `rejected`, `cancelled`, `expired`;
   - respect API rate limits (this runs during the session-limited window).
3. **Book only on a confirmed FULL fill:** return `FillResult(confirmed=True,
   fill_price=<broker fill price>, order_id=...)`. The fill price is the broker's, read back
   from the filled order — **not** `mark_price`, which is context only.
4. **Partial fills:** either (a) track the remainder to completion and return the
   quantity-weighted average fill price once fully closed, or (b) return
   `FillResult(confirmed=False, partial=True, detail=...)` and let the caller retry — pick
   one and document it. Never book a partial as if it were whole.
5. **Not filled by deadline / rejected / error:** return `FillResult(confirmed=False,
   detail=<why>)`. The position **stays open**; the 15:45→16:00 retry loop will re-attempt
   and page. Never fabricate a price, never mark closed.
6. **Spreads (condor legs):** a leg is a two-legged vertical. Confirm the **spread** closed
   (both legs), and return the **net** spread fill price on the same credit basis the P&L
   math expects (`_execute_exit` computes `entry_prem - fill_price` for credit-signed
   positions — so `fill_price` must be the net spread value, matching how the paper mark is
   `short_mark - long_mark`).

## Acceptance tests (must pass before cash)

- **A — happy path:** submitted → filled → `FillResult(confirmed=True)` with the broker fill
  price; DB row closes; P&L matches `(entry - fill) * contracts * 100` for a credit spread.
- **B — the orphan test (the whole point):** submit an order that does **not** fill by the
  deadline → `confirmed=False`, **P&L booked = none**, DB row **still open**, alert fired.
  A submitted-but-unfilled order must **never** produce a `$0.00` (or any) booked close.
- **C — reject:** broker rejects → `confirmed=False`, position open, no booking.
- **D — partial:** partial then complete → single correct net fill price; or documented
  retry. Never books the partial as whole.
- **E — paper untouched:** `PAPER_TRADING=True` still books the simulated mark in one pass;
  no polling path entered.

## What you'll need from Jason

- Live tastytrade **API credentials** for a funded but **tiny** account (test with 1
  contract / minimal width). Jason has offered these — request them for the test account,
  not production size.
- Confirmation of the tastytrade SDK's order-status object shape (fields for state, filled
  quantity, average fill price) — verify against the live SDK, do not assume.

## Guardrails

- Complete files, never patches; bump the header of every file you change with what changed.
- Clone repo HEAD and read before editing — this file's paper seam is v3.4; build on it.
- Do not weaken the fail-loud stub until the acceptance tests pass; a half-built live path
  must still refuse to book rather than book an orphan.
- `PAPER_TRADING` default stays `True`. Nothing you build may change paper behavior.
