# ORB Stop-Placement Rework — v3.1 (2026-07-11)

## Scope

The 5-minute opening-range break-and-retest stop was being placed and enforced
against the wrong price levels. This change corrects **where the stop level is
set** (the engine) and **how it is enforced** (the exit path). Two files change,
both bumped to **v3.1**:

- `analysis/orb_engine.py`
- `execution/exit_engine.py`

No other strategy (sweep, butterfly, condor) is touched. **The regime un-gate
(letting a confirmed ORB fire under an UNKNOWN/sweep label) is NOT part of this
change set** — it remains queued separately.

---

## Root cause

Two distinct defects, both in the ORB stop, discovered by driving the real
engine over candle-logger tape:

1. **Stop LEVEL was anchored to the impulsive candle's body, not its wick.**
   The engine set the stop to `min(open, close)` (long) / `max(open, close)`
   (short) of the break candle. When that candle opened *outside* the range, its
   body edge sat outside the level — so the retest entry (which returns to the
   level) printed a stop on the *wrong side* of the entry. Result: inverted /
   near-zero risk on a meaningful share of trades.

2. **The exit's structure stop fired at the range boundary, not the impulsive
   origin.** `_evaluate_orb` exited on any 1-minute close back inside the ORB
   range (`close < orb_high` for a long). By the strategy's definition that is
   *not* an invalidation — the trade is allowed to breathe inside the range as
   long as it holds the impulsive candle's origin. Stopping at the range edge
   cut trades that were still structurally valid.

A separate, important finding from the same dissection: the corrected
`underlying_stop` is **not** the live executor. Live exits govern off the **−25%
premium floor** (`current_premium <= stop_premium`); the underlying level is a
structure check that runs *beside* it. Both are intentional and both are kept —
see "The stop model now."

---

## What changed

### `analysis/orb_engine.py` (v3.1) — `_check_for_break`

1. **Stop anchors to the impulsive candle's wick**: its `low` for a long, its
   `high` for a short (was the body `min/max(open, close)`). The wick is the true
   origin of the breakout move and sits inside the range where invalidation lives.

2. **A valid impulsive candle must originate inside the range**: `low < orb_high`
   for a long, `high > orb_low` for a short. A candle sitting entirely beyond the
   range is late continuation, not an ORB break; taking its "retest" was the
   source of the remaining inverted stops (fast/gap breaks and re-arms while
   price was already extended). Gating on origin removes them, and — because the
   engine now waits for the valid break instead of firing on the extended one —
   it did not cost setups.

### `execution/exit_engine.py` (v3.1) — `_evaluate_orb`

- The structure stop now keys off `underlying_stop` (the impulsive origin set by
  the engine) instead of `orb_range_high` / `orb_range_low`. A long exits on a
  1-minute close **below the impulsive low**, a short on a close **above the
  impulsive high**. A close back inside the range that still holds the origin now
  **keeps** the trade.
- It remains close-based on the last *closed* candle (`iloc[-2]`), so an intrabar
  wick into the range survives; only a confirmed close beyond the origin exits.
- The **unconditional −25% premium floor (v1.6) is unchanged** and still evaluated
  first, every tick.

---

## The stop model now (the "AND")

Two independent exits protect an ORB position. Whichever trips first closes it —
they are an **AND** (both always armed), not a choice:

| Exit | Level | Fires when | Catches |
|---|---|---|---|
| **Structure stop** | impulsive candle origin (low/high) | 1-min *close* beyond it | thesis is dead, regardless of premium |
| **−25% premium floor** | 75% of entry premium | premium ≤ floor | dollars gone past tolerance — theta, retracement, or the two combined — regardless of structure |

Neither is redundant: a slow bleed or a shallow-but-costly retracement can hit
−25% without ever closing beyond the origin, and a sharp close beyond the origin
can invalidate the thesis while the premium is still above −25%.

---

## Smoke test

**Tape:** candle-logger 1-minute OHLC for 2026-07-09 (15 symbols) and 2026-07-10
(29 symbols) — 44 symbol-sessions. **Method:** the *real* `ORBEngine` is driven
bar-by-bar with the clock and opening range injected (no reimplementation), then
each confirmed entry's stop geometry is measured; the *real* `_evaluate_orb` is
run against the MU reference sequence.

### Expected

- Every confirmed entry carries a stop below entry (long) / above entry (short).
- The MU 2026-07-10 setup reproduces the manual read: impulsive candle 09:49,
  retest 09:50, stop at the impulsive low, 09:54 survives, 09:55 stops.
- The exit's structure stop gives room inside the range that the old
  range-boundary rule did not.

### Realized

| Metric | Before (body stop, range-boundary exit) | After (v3.1) |
|---|---|---|
| Inverted / degenerate-risk entries | **26 / 92 (28%)** | **0 / 96 (0%)** |
| Median entry risk (% of price) | 0.089% (collapsed onto entry) | **0.201%** (sane distance) |
| Confirmed ORB entries | 92 | 96 (fix did not cost setups) |

- **MU reference, through the real exit method:**
  ORB range 971.50 / 958.08; impulsive candle **09:49** (O 971.35, H 975.49,
  **L 971.14**, C 973.83); retest **09:50** doji (L 971.00 wicks in, C 973.99
  closes out) → fires, entry 973.83, **stop = 971.14**.
  `09:54` close 972.15 → **holds**. `09:55` close 970.88 → **exits**:
  `orb_structure_stop: 1m close 970.88 below impulsive-candle low 971.14`. Exact
  match to the manual walkthrough.
- **Extra room from the exit change:** across the entries where the two rules
  differed, the impulsive-origin stop held the trade a **median of +3 bars**
  longer than the old range-boundary stop (~1/3 of entries), i.e. it survived a
  range re-entry the old rule would have cut. The −25% floor still independently
  caps dollar loss on those.

---

## What this does and does not establish

- **Verified:** stop *geometry* (level) and exit *trigger* (level + close-based).
  Every ORB entry in the run now has a correctly-placed, non-inverted stop, and
  the exit fires on the origin, not the range edge.
- **Not established here:** option-premium P&L / win-rate. The bot's real
  outcomes ride on option premium (a 25% premium stop and premium target), which
  cannot be reconstructed from underlying OHLC without the option chain. Whether
  these setups are net-profitable is a **paper-forward** question, not a
  backtest-from-tape one.
- **Data limits:** two single-day sessions; the regime classifier is starved on
  single-day tape and is unaffected by this change regardless.

---

## Deploy

Both files ship together (they are a matched pair — the engine sets the level the
exit reads).

```
scp orb_engine.py  <box>:<repo>/analysis/orb_engine.py ;
scp exit_engine.py <box>:<repo>/execution/exit_engine.py ;
```

No `config.py` changes, no new dependencies, no schema changes. `underlying_stop`
is already carried on the trade record (written by `entry_engine`), so no
migration is required. Restart the bot service to load v3.1.
