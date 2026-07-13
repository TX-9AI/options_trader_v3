# Backtest Harness — v1.0

`tests/backtest_harness.py` — drops next to `replay_confluence.py`, reads-only,
drives the **real deployed engines** over a spliced multi-day 1-minute file per
symbol. It answers "how would my bots have traded this tape" faithfully for the
signal layer, and *approximately* for dollars.

## Run

```
python tests/backtest_harness.py --symbol CVX_1m_30d.csv --vix VIX_1m_30d.csv
python tests/backtest_harness.py --symbol CVX_1m_30d.csv --vix VIX_1m_30d.csv --model-premium --dte 0
```

- `--model-premium` adds Black-Scholes dollar P&L off the VIX level (off by default)
- `--dte N` expiry for the premium model: `0` = 0DTE (default), `5` ≈ weekly
- `--fed-days 2026-06-17,2026-07-29` marks FOMC dates for the macro dimension

Files are `timestamp,open,high,low,close,volume`, ET, RTH; one file per symbol.
VIX same format/window. It runs in the repo, so it always drives whatever version
of the engines is currently deployed.

## What is exact vs modeled

**Exact — drives the actual modules, no reimplementation:**
regime labels (`regime_classifier` + the four engines), v3 confluence scores
(`regime_confluence`, uncalibrated), ORB setups & stops (`orb_engine` v3.2), the
entry gate (`main.py` v3.2 `ORB_FIRES_REGARDLESS_OF_REGIME`), the structure stop
(`exit_engine` v3.1, on the underlying), and the VIX no-entry gate.

**Modeled — not exact (no option chain in an OHLC file):**
option premium and dollar P&L via Black-Scholes off VIX. The exit path runs the
real two-stop **AND** — structure stop (underlying close beyond the impulsive
origin), the **−25% premium floor**, and the target, whichever fires first — with
the floor modeled to fill at −25% (so no modeled loss is ever worse). Caveats:
0DTE by default; `vol = VIX/100` (apt for index ORBs, a rough proxy for single
names whose IV ≠ VIX); European BS, no smirk, no bid/ask, no slippage. Treat
dollar figures as **relative**, not a fill-accurate statement.

## Fidelity notes (why multi-day tape is required)

- Intraday timeframes (1m/5m/15m) are **session-scoped** (reset each session),
  matching the live feed's "never padded across the overnight gap." Higher
  timeframes (1h/4h/1d) use full continuous history. On a single session 1h is
  starved and direction collapses to NEUTRAL — ~15+ sessions gives it real depth.
  This is faithful to the live feed and is *why* the ORB window often reads
  UNKNOWN/RANGING (the 5m ADX is short all morning).
- 1d/4h are synthesized from the tape; over ~a month they're short (<55 bars) and
  contribute NEUTRAL, same as the feed's thin daily backfill.

## Reading the output — worked example (CVX, 19 sessions, 2026-06-12→07-10)

```
REGIME: RANGING 50% · COMPRESSION 31% · UNKNOWN 13% · TREND_BEAR 3% · TREND_BULL 2%
ORB: 29 setups, 29 fired, 0 gate-blocked (11 long / 18 short — short-lean = bearish drift)
  exact underlying:  TARGET 5 · STRUCTURE_STOP 24 · −0.54R expectancy
  modeled 0DTE:      TARGET 5 · STRUCTURE_STOP 4 · PREMIUM_FLOOR 20 · mean −5% / median −25%
```

What it tells you:

- **CVX was a chop/range month** (50% RANGING) — ORB break-and-retests mostly
  faked out (24/29 structure-stop on the underlying, −0.54R). That's the tape, not
  a bug: the un-gate deliberately trades this population.
- **On 0DTE the −25% floor is the binding stop, not the structure stop** (20 vs 4).
  Theta + a small retrace burns 25% of premium before price ever closes beyond the
  impulsive origin. This is exactly the "is the impulsive-low too loose in practice"
  question from the shadow plan — on 0DTE, yes. On `--dte 5` it shifts back toward
  the structure stop. **The ORB expiry choice per symbol changes the answer**, so
  run both.
- The 5 directional winners (+67% etc.) nearly offset the −25% losses → modeled
  mean −5%. A low-edge month, honestly rendered.

## Two honest limits

- **One symbol, single-stock, VIX-vol proxy.** CVX's real IV isn't VIX; the dollar
  layer is roughest for single names. It's most faithful for the index ORBs
  (SPX/QQQ/DIA) the strategy is actually built around.
- **It does not validate the strategy.** It shows what *would have fired* and how it
  *would have resolved* on this tape, on a sound risk model. Edge is a
  many-symbol, many-month question — which is what the diary + shadow corpus are
  for. This harness is the offline complement to that, not a substitute.
