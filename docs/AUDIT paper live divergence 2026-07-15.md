# AUDIT — Paper→Live behavioral divergence · 2026-07-15

**Scope:** every `paper_trading` / `PAPER_TRADING` / `paper_trade` branch in the
repo, plus every live order-placement and P&L-booking path, audited for
behavior that changes — or breaks — when `OT_PAPER_TRADING` flips to `False`.
Prompted by the 15:45 hard-close `$0.00` booking bug (fixed in exit_engine
v3.4/v3.5): the question was *what else is of that species*.

**Verdict in one line:** the EXIT side is now fill-confirmed and safe (v3.5),
the reconcile side recovers truth (v3.6) — but the **ENTRY side has the same
submission-equals-fill disease**, the **broken-wing roll opens a fictional
position in live**, and **paper and live rows share one trades.db with no mode
filter**, so two weeks of paper history will contaminate the live daily-loss
breaker on day one.

Files audited: `main.py`, `execution/entry_engine.py`, `execution/exit_engine.py`,
`execution/position_manager.py`, `execution/broker_reconcile.py`,
`strategy/condor_roll.py`, `database/trade_logger.py`, `risk/risk_manager.py`,
`risk/session_guard.py`, `data/tasty_client.py`, `notifications/alert_manager.py`,
`status.py`, `eod_summary.py`, `query.py`, `config.py`, `configure.sh`.

---

## 🔴 CRITICAL — will misbehave or lose position-truth in live

### L1 — Entries book on SUBMISSION, not on broker fill (all three entry paths)

The entry side never got the FillResult treatment. Every live entry path
records the position as open — at a price that is not the fill — the moment
the order is *accepted*, exactly the class of bug that produced the $0.00
exits.

**L1a · Condor legs** (`main._execute_condor_leg`): places the 2-leg vertical
as a LIMIT at mid-credit, then books
`fill_credit = response.order.price or net_credit` immediately. `.price` on a
just-placed order is the *limit you asked for*, not a fill, and a mid-credit
limit is precisely the kind of order that sits unfilled. Consequences of a
never-filled entry: a DB position that does not exist at the broker, managed
every tick, "closed" at 15:45 with real close orders the broker rejects, and
`notify_leg_filled()` advances the condor legging state machine on a fill that
never happened — Leg 2 can arm off a fictional Leg 1.

**L1b · Single legs** (`entry_engine._place_single_leg`): MARKET order, then
`fill_price = float(placed.price or signal.entry_premium)`. A market order has
no `.price`, so this **always** books the signal-time mark as the entry — the
recorded entry premium in live is never the actual fill. Stops/targets and P&L
all key off a number the broker never printed. (Market orders nearly always
fill, so position existence is usually fine — the *price* is what's wrong.)

**L1c · Butterfly** (`entry_engine._place_butterfly`) — broken three ways:
1. **Wrong price sign.** The debit is sent as a POSITIVE `price` with
   `price_effect=DEBIT`. Verified against the SDK (v8+ through 13.x):
   `NewOrder.price` is **signed** (negative=debit, positive=credit) and
   `price_effect` is silently ignored. A positive-priced opening fly demands a
   *credit* to buy a debit spread — it will never fill.
2. **Fill check that can't succeed.** It reads `placed.status` immediately
   after submission, looking for "Filled" — the status at that instant is
   Received/Routed. So even a correctly priced order goes: place → sleep →
   cancel → re-place → cancel → give up.
3. **Double-position race.** If the first order fills during the sleep, the
   `delete_order` fails (exception swallowed with `pass`) and attempt 2 places
   a **second** butterfly.

**Fix shape:** an entry-side mirror of exit_engine v3.5 —
`_confirm_entry_fill(order_id)` polling to a bounded deadline, record written
ONLY on a confirmed fill at the broker's per-leg net fill price, signed limit
prices, cancel-and-resolve on timeout. Until then the deliberate "entry logic
is v2.5" stance in the README should be read as **live entries are not
validated**.

### L2 — Broken-wing roll opens a FICTIONAL vertical in live

`strategy/condor_roll._execute_roll` step 2 carries the comment "*live order
placement mirrors _execute_condor_leg*" — **but no order is placed**. The code
writes the rolled vertical's DB record and moves on. In live: the real
untested vertical is closed (correctly, fill-confirmed via v3.5), then the bot
books and "manages" a new vertical that was never opened at the broker. The
rolled structure's risk-free math is fiction; reconcile will eventually flag
the ghost. Secondary: step 1 books the close at `plan.close_cost` instead of
the confirmed `fill.fill_price` it *just received* from the v3.5 close.

**Fix shape:** place the rolled vertical as a real signed-credit limit order
with fill confirmation before writing the record; book step 1 at
`fill.fill_price`. Alternatively gate `check_and_execute_roll` behind
`paper_trading` until built — a silent no-roll is strictly safer live than a
ghost position.

### L3 — One trades.db, no mode filter: paper history contaminates live truth

There is **no `paper_trade` filter** in the queries that matter:

- `realized_pnl_today()` — **the DAILY_LOSS_LIMIT source of truth** — sums
  every closed row. On switch day, two weeks of paper habits plus any paper
  rows closed that ET day gate the *live* breaker. A red paper morning can
  halt real-money entries; a green one can mask a real-money halt.
- `get_open_trades()` / `get_open_trades_live()` — startup recovery and the
  position manager hand any still-open paper rows (unexpired weeklies, or
  rows with unknown expiry, which are deliberately kept) to the LIVE bot,
  which manages them, submits real close orders for them, collects broker
  rejects and pages until reconcile phantoms them — and the phantom booking
  then *also* lands in live realized P&L.
- The only DB wipe in the system is on **instrument** change, paper mode only.
  **Mode** change wipes nothing and archives nothing.

**Fix shape (small, do first):** mode-aware queries — filter
`paper_trade = (0 if live else 1)` in `get_open_trades` and
`_closed_today_rows` — plus a `configure.sh` step on switching to LIVE that
archives `trades.db → trades_paper_YYYY-MM-DD.db` (preserving the two weeks of
paper data rather than mixing or deleting it).

---

## 🟡 MODERATE — expectation and hygiene

### M1 — Paper fills are perfect; live fills are not
`PAPER_FILL_SLIPPAGE_PCT = 0.0`: paper enters AND exits at the exact
mid/mark, both sides, every time. Live pays spread crossing on entry, and the
v3.5 close buys through the mark by `LIVE_CLOSE_LIMIT_BUFFER` to get filled.
Two weeks of paper P&L is therefore a structurally *optimistic* estimate —
materially so on wide SPX spreads. Not a bug; a calibration warning. Consider
a nonzero paper slippage (even 1–2%) so paper stats stop flattering.

### M2 — Dashboards report mixed modes
`status.py`, `eod_summary.py`, and the risk manager's session stats aggregate
paper and live rows together (`query.py` at least prints the flag per trade).
After L3's filter lands this mostly resolves itself; until then, switch-day
dashboards lie.

### M3 — Live-only code paths have never executed
`get_open_option_positions()` is written version-robustly (sync on tastytrade
12.x, coroutine on 13.x) but its field access has only been verified against
SDK source, never a live account — same for every live order path. Reconcile
now auto-enables with LIVE (v3.6/config v1.8), which makes the tiny-account
shakedown *more* important, not less: first live session should be 1 contract,
minimal width, watching `journalctl` and Telegram.

---

## ✅ VERIFIED SAFE across the switch (so you don't re-audit them)

- **Exits** — fill-confirmed (v3.5): submit → bounded poll → book only on the
  broker's net fill; partials weighted; idempotent resume; verticals close as
  2-leg spread orders with signed debit limits; butterfly closes are
  marketable limits. Acceptance tests A–E pass.
- **15:45→16:00 flatten retry + paging** — mode-agnostic, books only via
  `_execute_exit`, which refuses unconfirmed fills.
- **Reconcile (v3.6)** — auto-follows mode; interval sweeps
  (`BROKER_RECONCILE_INTERVAL_MIN`, default 10) plus 15:45/15:50/15:57
  wind-down passes; phantom P&L recovered from order history; fail-safe on
  bad/empty broker reads; paper never reconciles.
- **DAILY_LOSS_LIMIT mechanics** — DB-seeded, restart-proof, net-based
  (content is compromised by L3 until filtered, but the mechanism is sound).
- **Regime/conviction/session gates, candle feed, sizing** — mode-agnostic by
  construction; single TastyTrade/DXFeed feed serves both modes identically.

---

## Recommended order of work before cash

1. **L3** — mode-filter the two queries + archive-on-switch in configure.sh.
   Smallest change, prevents day-one contamination no matter what else ships.
2. **L1** — entry-side fill confirmation (mirror of exit v3.5). Condor legs
   first (the strategy you actually run), then single-leg price readback, then
   butterfly (or gate butterflies off in live until rebuilt).
3. **L2** — real order in the roll, or gate the roll to paper.
4. **M1** — nonzero paper slippage so the next two weeks of paper predict live.
5. Tiny-account live shakedown (1 contract) with reconcile auto-on, per the
   v3.5 spec's acceptance criteria.
