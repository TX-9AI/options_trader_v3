# Options Trader v3 — Vertigo Capital

**Intraday options day-trading suite · 29-box fleet · TastyTrade/DXFeed · single shared candle store per box · paper-first**

---

## ⚠️ READ THIS FIRST — the entry logic is v2.5, and that is deliberate

The regime architecture is mid-migration. Three eras coexist in this tree, and the honest
label for what is *running today* is neither v2 nor v3:

| | Gating model | Result |
|---|---|---|
| **v1** | Boolean gates, permissive | Fired into hostile tape. Sold into uptrends. Got faked out. |
| **v2** | Boolean gates + an `UNKNOWN` regime with **hard veto** | Over-corrected. Most of RTH classified `UNKNOWN`; the veto skipped clean trending setups; **the trade sample starved the very analysis loop meant to fix it.** |
| **v2.5 — RUNNING NOW** | v2's cascade, but `UNKNOWN`'s **veto power removed for the ORB** | Sample restored. **The safety was removed before the replacement was built.** |
| **v3 — TARGET** | Weighted confluence → per-regime conviction → `fires iff regime ∈ permissive AND C ≥ bar(trade_type)` | Bars placed empirically at the marginal fee-adjusted-ROI zero crossing. |

**State it plainly:** v3.2 shipped ROADMAP **Phase 2's permissive set** for the ORB
(`_orb_ok_regimes` in `main.py` is the ROADMAP Phase-2 table verbatim, plus `UNKNOWN` and
`SWEEP_REVERSAL` under the switch) **without Phase 2's conviction bar.** The gate opened; the
thing meant to replace it has not landed.

Consequently, **a confirmed ORB break+retest fires in every regime the classifier can emit,
including `UNKNOWN`.** The only thing between a confirmed setup and an order is
`setup_scorer`'s B-threshold (0.55), inside which `regime_conviction` is a 20%-weighted
dimension that contributes **exactly 0.0 under `UNKNOWN`**.

This is intentional — it is how labeled tape gets generated for the Phase-3 calibration.
**It is also why the fleet stays in paper.** `PAPER_TRADING` defaults to `True` and must not
be flipped on any box until the conviction bars exist. See `ROADMAP.md` §Risks.

Sweep, butterfly, condor, and trend continuation are **untouched** by this: they still
self-gate and still do not fire under `UNKNOWN` (continuation hard-requires a *trending*
regime, a strictly higher bar). Set `ORB_FIRES_REGARDLESS_OF_REGIME = False` to restore strict
v2 gating.

---

## 📦 DAY-ZERO ROLLOUT — 2026-07-18 build (deploy state)

Monday 2026-07-18 is **day zero** on a materially changed engine, and the start of the
~2-week hands-off baseline window (regime labels trusted, L2 weights frozen, condor behavior
confirmed) that gates the pitchfork. What lands and how:

**Already live on the fleet (Fri 2026-07-17):**
- `trend_engine` v3.1 — intraday-primary tf_weights, the dead-4h TRENDING fix (confirmed via
  journal: AVGO threw TRENDING_BEAR conviction 0.52).

**Landing this deploy pass (fleet flat, one `devtools` option-23 FULL wake→bake→restart→STOP,
catching the 19 asleep boxes):**
- `volatility_engine` VWAP zero-volume guard — SPX NaN→"BELOW" false-signal fix (commit `cf5def8`).
- Iron condor premium-rich band-approach triggers + roll-gets-first-refusal (commit `792d802`).
- Trend Continuation strategy — NEW, paper-first on all boxes from Monday (the 2-week baseline is
  its proving ground).
- Signal journal instrumentation (v1.0 module + `setup_scorer` v1.3 + `main.py` v3.9 +
  `orb_engine` v3.7) — **log-only, zero behavior change.**

**Deploy discipline:** full-file drop-ins, never `git apply` patches (patch desyncs against
uncertain server versions burned ~a dozen turns). **The deploy gate is
`python3 -c "import ast; ast.parse(open('<f>').read())"` on the box** — NOT pytest (wrong-venv /
no-pytest on boxes burned this repeatedly). After the pull, `bash check_versions.sh | grep
MISSING` must print nothing; the canary set now fingerprints every day-zero change plus the
instrumentation, so a stale sync surfaces immediately. **Parity invariant:** the same engines
must reach the control checkout (`~/options-trader-v3`) so the replay harness scores Monday's
tape with the bot that traded it — pull + `check_versions.sh` on control right after the fleet.

**Path note:** the 29 boxes deploy to `~/options-trader` (no `-v3`); the control server checkout
is `~/options-trader-v3`.

**Deliberately NOT in this pass:** the offline-replay bookmark (defect S — build and prove inert
on the tester first); observer fleet deployment (one QQQ-TEST box at stage 1 is the whole ask);
shadow-observer service-unit templatizing (defect D service-half); any gate change. Monday's
engine *decisions* are exactly what was approved Friday.

**The Monday habit:** after the EOD conductor runs on control, `cd ~/day_trader_pro &&
./label_day.sh` to tag the session's trend/sweep/pin/breakout symbols — this is what fills the
Layer-1 Tier-B tape gaps (see `docs/REPLAY_VALIDATION.md` and `ROADMAP.md` L1.7).

---

## Architecture

### Fleet topology — and the parity invariant

**This repo is one artifact deployed into two different roles.**

- **29 trading boxes** (EC2, one symbol each) run `main.py` under `optionsbot.service`, plus
  `candle-feed.service`. 29, not 30: `STRIKE_INCREMENTS` is a strike-increment *lookup table*
  (a superset, 30 entries); SPY is defined but not deployed, because SPX covers it.
- **1 control server** runs `fleet.py`. **`fleet.py` lives in `day_trader_pro`, not here** —
  which is why `harden_hosts.sh` and `pull_today_ohlc.sh` reference a file that isn't in this
  tree: they are *invoked by* control, they do not invoke it.

`tests/` ships to all 29 boxes but is *exercised* on control, against harvested,
fleet-aggregated tape. That is deliberate: the harnesses **import the live engines**
(`orb_engine`, `regime_classifier`, `regime_confluence`, `exit_engine`) rather than
re-implementing them, so a backtest always runs the *same execution model the fleet is
running*.

> **INVARIANT — any engine patch deployed to the fleet must also be deployed to control.**
> Otherwise the backtest silently stops being apples-to-apples. It will still run, still
> produce numbers, and those numbers will be measuring a bot that no longer exists.
> **Nothing currently enforces this.** It belongs in `check_versions.sh`.

### Data — one producer, many readers (shipped, v3.0)

Every process on a box — bot, engines, ORB range, candle logger, shadow observer, VIX —
reads **one** SQLite (WAL) store, written by **one** DXFeed subscription held exclusively by
`data/candle_feed.py` (`candle-feed.service`). No consumer may open its own stream.

`data/market_data.py` is a pure store *reader* preserving the exact v2 contract
(`fetch_candles` / `fetch_quote` / `fetch_all_candles`), which is why every downstream engine
required zero changes. Readers **fail loud**: `None` + `WARNING` when the store is missing or
the heartbeat exceeds `OT_FEED_STALE_S` (120s). A dead feed surfaces as "no data," never as
stale numbers driving a decision.

The purge is real and verified: **zero `yfinance` imports repo-wide.** It is the load-bearing
prerequisite for everything else — calibrating conviction against ROI on a feed the bot
doesn't trade is calibrating a board it never plays on.

### Signal journal — Phase-3.1 instrumentation (shipped, v1.0, 2026-07-18)

`analysis/signal_journal.py` is a **log-only** subsystem that makes the *perishable* part of
every trading decision durable. The 1-min OHLC tape can be replayed forever; what evaporates at
16:00 is what the option chain looked like at signal time — premium, bid/ask spread, IV, greeks
— and which gate disposed of each signal. Without it, every session between now and the Phase-3
calibration campaign is tape that can never *become* calibration data. ROADMAP Phase 3.1 states
the rule: *"a gate you can't counterfactual is a gate you can't calibrate."*

It writes append-only JSONL to `data/signal_journal/<YYYY-MM-DD>/<SYMBOL>.jsonl` (gitignored,
self-locating repo root like the shadow observer). Event vocabulary:

| event | emitted by | carries |
|---|---|---|
| `scored` | `setup_scorer` v1.3 | every scored signal **including below-B REJECTs** — grade, total, both thresholds, full breakdown, regime conviction, and the signal's quote context (bid/ask/mark/spread/IV/greeks) |
| `disposition` | `main.py` v3.9 | what happened after scoring: `fired` / `sizing_rejected` / `invalid_signal`; ORB dispositions carry `retest_depth_px` + its ATR-relative form |
| `retest_check` | `orb_engine` v3.7 | per-armed-candle retest penetration depth in PX (**negative = near-miss**) + `orb_width` — the defect-G distribution |
| `condor_plan` / `condor_leg` | `main.py` v3.9 | regime conviction at condor decision/fire time — the condor bypasses the score path, so without these its Phase-3 bar could never be calibrated |

**Design guarantee:** every emission is wrapped so any failure (full disk, bad payload,
permissions) degrades to a missing log line, never a raised exception. The trading loop is
byte-identical whether the journal is present, absent, or broken. It imports nothing from
`execution/`, `risk/`, `strategy/`, or `notifications/`, never opens `trades.db`, and places no
orders. Join key across events: `ts_et` + symbol (one signal per tick, single-threaded per box).

Collection: journal files ride `snapshot.sh` today; an EOD-conductor collection phase will be
added when volume justifies it — **deliberately not wired into the conductor chain yet**, which
is finally flawless and stays untouched until any addition is proven inert on the tester.

---

## Regime classification (running: `regime_classifier.py` v1.3)

Memoryless boolean cascade, re-run from scratch every 15s. First match wins:

**SWEEP_REVERSAL → BREAKOUT_VOLATILE → COMPRESSION → TRENDING_BULL/BEAR → RANGING → UNKNOWN**

ADX comes from the **5-minute** timeframe, matching the trading horizon. `UNKNOWN` is a
genuine abstention (v1.2), not a catch-all — and it remains a **hard no-trade gate for every
strategy except the ORB**.

| Regime | Strategies permitted to fire |
|---|---|
| TRENDING_BULL / TRENDING_BEAR | **ORB · Trend Continuation** |
| BREAKOUT_VOLATILE | **ORB** |
| SWEEP_REVERSAL | Sweep Reversal · **ORB (v3.2 — ORB wins)** |
| RANGING | Iron Condor · Butterfly (if GEX PINNING) · **ORB** |
| COMPRESSION | Butterfly (if GEX PINNING) · **ORB** |
| UNKNOWN | **ORB only** (v3.2 un-gate). Everything else: no trade. |

The ORB appears in every row because the break+retest is **self-validating** — the classifier
does not even test for it, so the label is a scoring input, not a veto.

---

## The ORB — the flagship, and it is now definitional

The setup is mechanical. As of **v3.5 there are no tolerances anywhere in it.**

```
BREAK  = a 1m candle that OPENS INSIDE the opening range and CLOSES OUTSIDE it.
RETEST = a SUBSEQUENT 1m candle — any bar within ORB_MAX_RETEST_BARS (12) of the
         break, NOT only the very next one — whose WICK enters the range and
         whose BODY stays entirely OUTSIDE it. Bars in between that neither
         retest, close back inside, nor reach the 50% TP simply pass; the
         engine stays ARMED and keeps waiting.
STOP   = a 1m CLOSE beyond the impulsive (break) candle's WICK.
```

**Opening range** = the 9:30–9:35 ET 5-minute candle, sourced through the bot's own data
layer (`market_data.fetch_candles`) so it always agrees with the tape the bot trades. Written
to `orb_range.json` as a three-state model — `ESTABLISHED` / `IN_PROGRESS` / `EXPIRED` — and
the engine **arms only on `ESTABLISHED`/today**, so a carried prior-day range can never be
traded.

**State machine** (`ORBState`, renamed in v3.4 to the operator's vocabulary):

```
NO_RANGE → WAITING_FOR_BREAK → ARMED_LONG / ARMED_SHORT → OPEN_LONG / OPEN_SHORT
                  ↑                       ↓
                  └───── INVALIDATED ─────┘        (re-arm rules below)
```

**ARMED means a break has occurred and the next event is FIRE or INVALIDATE.** Before a break
there is nothing armed — the engine is merely waiting.

**Why "opens inside" is definitional (v3.5).** It is an *opening-range* break. A candle that
began life outside the range never broke out of it — it was already out. That is late
continuation. (v3.1 approximated origin as `low < orb_high` — the wick merely reaching back in
— which still admitted candles that opened *above* the range, dipped, and closed higher.)

**Why there is no buffer (v3.5).** The retest **is** the noise filter — a marginal break that
means nothing simply fails its retest. The old `ORB_BREAK_BUFFER` (0.05% *of price*) required
the close to clear the range by **$0.49 on MU, ~$3.00 on SPX**, so price could close three
full points beyond the opening range and not register a break.

**Why there is no grace band (v3.3).** The retest is the **falsification step** of the break
hypothesis ("this level is now support"). A level that was not tested produced *no evidence*;
a level whose retest closed back inside was tested and **failed**. Neither is a graded setup.
The old `body_low >= orb_high * 0.999` admitted a candle whose body **closed back inside the
range** — the disarm condition — as a *confirmed retest*, and bought it. On SPX that window
was ~6 points deep.

**Three invalidations:**

| Reason | Trigger | Re-arms? |
|---|---|---|
| `close_inside` | 1m close back inside the range — the hypothesis failed | ✅ **Yes**, if before 11:00. The second attempt is often the cleaner one; the first is often the fake-out. |
| `runaway` | Ran to the 50% TP with **no retest** | ❌ No. Hands off to Sweep Reversal — the setup a failed runaway most favors. |
| `timeout` | 12 bars without a retest (`ORB_MAX_RETEST_BARS`) | ❌ No. The setup has gone stale. |

**Break latches** (`broke_high`/`broke_low`) are maintained **unconditionally every tick, in
every state**. They are a session-level fact ("a 1m candle closed beyond this boundary"),
independent of the ORB entry state machine, because the sweep gate needs them even while the
ORB is dormant. They are **close-based** (a wick that pokes and closes back inside does not
arm a sweep) and take **no origin gate** — they record a fact, not a setup.

**Entry:** single-leg long call/put, strike near the ORB-projected 100% target.
**Hard cutoff 11:00 ET** — the engine EXPIRES from any state. This expires the *engine*, not
an open position: a fill at 10:58 runs to its own exits.

---

## Strategies

### Sweep Reversal
Detects liquidity sweeps at **mapped** zones (PDH/PDL, equal highs/lows, session H/L). A sweep
requires all three: **location** (at a named pool), **penetration**, and **rejection**
(reclaimed and held). Acceptance *through* a level is a breakout, not a sweep. OTM strikes by
delta targeting, scaled inversely to reversal strength (strong snap → far-OTM; weak →
near-ATM). **BOS exit** on the 1m chart — closes only, no wicks.

### Trend Continuation (NEW 2026-07-18 — paper-first, the trend-native trade)
The trade the `trend_engine v3.1` fix exists to enable. Fires **only in a trending regime** —
and because the classifier is *stingy* about calling trend (it is a high bar to clear), a
trending label is itself the high-conviction signal. Debit directional (long call in
`TRENDING_BULL`, long put in `TRENDING_BEAR`).

**Philosophy: make entry easy, make exit smart.** Entry is a deliberately *low* bar — the
protection lives in the exit, not the entry. Price pulls back to the **BB midline**
(`bb_middle`, the same anchor the condor uses), momentum flips back toward the trend, and it
enters. Two entry paths, both trend-gated:

- **Handoff (looser).** A **runaway ORB** — a break that ran to the 50% TP with no retest —
  is one of the *strongest* trend confirmations there is (strong push → pullback → next leg is
  textbook trend behaviour). So when a runaway ORB invalidates in a trending regime, it now
  **hands off to continuation first** (`main.py` Priority 2.5, `is_handoff=True`): conviction
  floor relaxed 0.45→0.35, `STEADY` momentum accepted. This replaces the old hardcoded
  runaway→sweep chain. Sweep still owns a runaway heading into a near/strong mapped zone when
  *not* trending.
- **Standalone (stricter).** No runaway vouching for it, so it must self-source the setup:
  conviction ≥ 0.45 and `ACCELERATING` momentum required.

**Downside = regime-change OR 40%, whichever first.** Regime-invalidation *is* the smart
stop — the trade is *defined* by the trend, so a flip out of trending kills the thesis
regardless of P&L (this mirrors how the condor self-gates on RANGING). The 40% floor is the
disaster backstop beneath it. No separate structural stop.

All thresholds env-tunable (`OT_CONT_*`). The `MIDLINE_ATR` band (how close to the midline
counts as "at" it, default 0.35·ATR) is the primary knob — it controls how *often* the trade
fires — and is the first thing to calibrate off the paper baseline.

### Iron Condor (legged, tracked)
RANGING fallback when no GEX pin is available. **Strike SELECTION is Bollinger-Band anchored —
no delta enters the strike-picking path.** Short call = lowest liquid strike at/above the BB
upper band; short put = highest at/below the BB lower band. Delta is deliberately excluded
*from selection*: it is relative to where price *sits*, not to the actual range boundary.

**Delta as a calibration street-sign (v3.4).** Distinct from selection: after the BB selector
has picked the short strike, the leg **records `abs(short-strike delta)` as its `setup_score`** —
read-only, purely as a logged waypoint. It does not influence which strike is chosen, how the
leg is sized, or whether it fires; it is written *after* the pick is final. Condor legs
otherwise carry no conviction score (they hardcode Grade B), so this is the axis condor
threshold-calibration will bin fee-adjusted ROI against later. `NULL` when the Greeks feed did
not populate delta — a real short strike is never exactly 0.0 delta, so a stored value is
always a genuine delta. This is the *only* delta anywhere near the condor, and it decides
nothing.

The condor is **the only strategy allowed two concurrent positions** (its two verticals). Each
vertical is a fully tracked position — managed, exited, and P&L'd independently with
credit-spread math — and each is sized at **half the grade budget**. Wings are narrow (5 points
SPX / $5 QQQ), which is what makes half-budget sizing affordable. Legged entry:
`DECIDED → LEG1_FILLED → COMPLETE`; a pending leg is cancelled if the regime flips away from
RANGING, but a filled leg is never cancelled. Exit per leg: 25% stop (spread value at 125% of
credit) or a $0.05 nickel close. Regime-flip exit is **direction-aware** — a call spread only
exits on a bullish flip; a bearish flip is favorable, so it holds.

### Broken-Wing Roll
When both verticals are open and price tests one side, rolls the **untested** side toward
price — **only if the math makes the tested side risk-free**
(`banked_credit + roll_credit − close_cost ≥ tested_side_width`). Smallest qualifying roll
wins. **One-time and final**: once rolled, every leg is flagged `is_broken_wing` and never
adjusted again. Roll once, stand it, defend it.

### Debit Butterfly
RANGING or COMPRESSION **with a PINNING GEX environment**. Center strike = the **GEX pin**, not
ATM. Gated on proximity (price within 1× the session expected move of the pin). Fixed wings
(25pt SPX / $5 QQQ). One per session. Exits immediately on a flip to trending.

**GEX is computed live from the TastyTrade chain every 15s. No scraping, no external API.**
Derived: call wall, put wall, pin strike, flip strike, environment. The condor is intentionally
*not* GEX-dependent — it fires precisely when GEX is **not** pinning.

---

## Exits

### ORB — evaluated every tick, first match wins

| # | Trigger | Condition | Purpose |
|---|---|---|---|
| 1 | Hard close | 15:45 ET | Time |
| 2 | **−25% premium floor** | `premium ≤ entry × 0.75` — **unconditional, every tick**, independent of trail state | **Minimize loss** |
| 3 | **Structure stop** | Last *closed* 1m candle closes **beyond the impulsive candle's wick** (`underlying_stop`). **NOT** the range boundary — closing back inside the range does **not** stop the trade | **Thesis death** |
| 4 | Theta bleed | **All four:** held ≥ 20 min · gain ≥ 10% · gain **< 20%** · projected decay (`theta × 20/1440`) ≥ current gain | **Protect profit** |
| 5 | Past 100% TP | **No hard exit.** Trail tightens to the nearest unfilled in-favor 1m FVG, floored at 85% of current premium | **Let it run** |
| 6 | Below 100% TP | FVG trail arms at **+20%**; % trail arms at **+50%** and ratchets to 75% of current. Higher governs | **Protect profit** |

**#2 and #3 are an AND, not an OR.** They catch different deaths: premium death (theta,
retracement, or the mix) and thesis death (structure). Whichever fires first.

**Exit-reason integrity (v3.3, 2026-07-12):** `stop_premium` is **immutable** — set once at
entry, forever the true −25% floor. Trails persist in their own `trail_stop` column (schema
migration is automatic), and the exit engine re-arms its in-memory trail from it on restart.
Before this, every trail update overwrote `stop_premium`, so every trail-armed exit — including
post-target exits at +100%+ — was logged `hard_stop_25pct`/`stop_hit`, poisoning the
`exit_reason` distributions Phase-3 calibration reads. Same exit ticks, same prices; the labels
now tell the truth.

**The trail and the structure stop are both necessary and serve opposite jobs** — one protects
gains, one minimizes losses. Neither supersedes the other.

**Not present on the ORB:** no BOS exit (that is sweep-only) · no max-hold · no 11:00 exit.

### Trend Continuation — EXHAUSTION-based (NEW 2026-07-18)

The continuation exit is where the trade lives or dies, so it is the deliberately intelligent
half. Evaluated every tick, first match wins:

| # | Trigger | Condition | Purpose |
|---|---|---|---|
| 1 | Hard close | 15:45 ET | Time |
| 2 | **Regime flip** | Regime no longer trending **in our direction** | **Thesis death — the primary stop** |
| 3 | **−40% floor** | `premium ≤ entry × 0.60` (`MAX_LOSS_PCT`) | Disaster backstop |
| 4 | **Exhaustion (two-stage)** | *Only past +15% gain.* **Extension:** price ≥ 2·ATR from the midline → **tighten trail to 85%** (does *not* exit — a strong trend can stay stretched). **Divergence:** new favourable price extreme on **weaker** 5-bar momentum → **exit** | **Detect a spent move** |
| 5 | Runner trail | Standard FVG trail; once armed it owns the trade (and silences theta via the v1.5 trail ceiling) | Let it run |

The distinction from a normal stop: a stop asks *"was I proven wrong?"* (that is #2/#3).
Exhaustion asks *"is the move **tired**, even while still technically going my way?"* — which is
what stops a continuation trade from handing back its gains at the turn. **Extension tightens,
divergence exits** (v1 two-stage). A stricter "both must agree" mode is noted in-code for
future reconsideration; it maps closer to how the operator trades but is intentionally not a
live flag.

**Engine-state exactness with a safety net.** The exit prefers the *live* `vol_state`/`trend`
threaded down from `main.py` (so it judges exhaustion against the same midline/momentum the
entry used), but **falls back to recomputing midline and ROC from `df_5m`** when that state is
absent (restart recovery, adopted positions). It therefore *cannot* raise on a missing engine
snapshot — it only degrades precision. The `vol_state`/`trend` kwargs were added
**optional-with-defaults** through `manage_open_position → _manage_one → evaluate()`
specifically to avoid the 2026-07-16 signature-mismatch crash-loop; every existing strategy
routes byte-identically with them present (regression-checked).

### Fill-confirmed exits (v3.4/v3.5, 2026-07-15) — a close is only real when the broker says so

The 2026-07-15 hard close booked ~8 condor legs at `pnl=+$0.00` because
`flatten_all` treated order *submission* as a fill and booked at a fallback
price. That entire class of bug is now closed:

- **The shared contract:** `place_exit_order()` returns a `FillResult`
  (`confirmed / fill_price / order_id / partial`). `_execute_exit()` books P&L
  **only** when `confirmed=True` with a real price. Unconfirmed → the row
  stays OPEN and the 15:45→16:00 retry loop re-attempts and pages.
- **PAPER:** simulates the fill at the last-known mark in one pass; no mark →
  declines and retries next tick rather than inventing a price. Unchanged
  behavior, now formalized.
- **LIVE (`_confirm_and_book_live_exit`, v3.5):** submit → capture the broker
  order id → poll to a bounded deadline (`LIVE_FILL_POLL_SECONDS` /
  `LIVE_FILL_DEADLINE_SECONDS`) → book **only** the broker's net fill price
  read from per-leg fills. Never the mark, never entry, never $0.00.
  Unfilled at deadline → cancel, resolve the cancel/fill race, stay open,
  page once. **Partials:** filled portion stashed, remainder resubmitted next
  tick at a fresh mark, booked once at the quantity-weighted net price. A
  working order id is resumed on re-entry — retry ticks can never
  double-submit. Verticals close as one 2-leg spread order (previously the
  long leg was orphaned); spread closes are marketable **limits** (tastytrade
  rejects MARKET on spreads) with the vertical debit capped at spread width;
  limit prices follow the SDK's **signed** convention (negative=debit).
  Acceptance tests: `tests/test_live_fill_confirmation.py` (A–E per
  `FABLE_SPEC_live_exit_fill_confirmation.md`) — all pass; tiny-account live
  validation still required before cash.

Theta protection is deliberately narrow (v1.5). The v1.3 check fired on the first green tick —
58 of 77 exits were theta-bleed at a **median 60-second hold**, capping trends while the day's
P&L came from the few trades that reached the trail. Decay is projected per **calendar** day
(1440 min); v1.3 divided by the 390-minute RTH day and overstated decay ~3.7×.

---

## Risk

- **Grade A = 1.5× base risk · Grade B = 1.0×. There is no Grade C** — below-threshold setups
  return `None` and never fire.
- **Regime reassessment after *every* losing trade.** A loss is fresh information about whether
  the regime read still holds.
- **The only circuit breaker is `DAILY_LOSS_LIMIT_USD`** (default = one trade's risk). It halts
  **new entries** when the day's **NET realized P&L** is down by that amount. Wins offset
  losses — a green day keeps trading no matter how many individual losses stack up; only a
  genuinely red day halts. Seeded from the DB on startup, so it survives restarts within the
  session. Open positions keep being managed to their exits. Override via `configure.sh` →
  option 6.
  > The old count-based breaker (`SESSION_LOSS_LIMIT = 2`) was **deleted in config v3.2.** It
  > had gated nothing since risk_manager v1.4 — which requests a reassessment after *every*
  > loss — yet four dashboards still printed *"Session CB: 2 losses → halt"*, a halt that could
  > never occur. `session_losses` survives as a statistic only.
- **Broker reconciliation** (`execution/broker_reconcile.py`, v3.6): **auto-follows the
  trading mode** — flipping to LIVE via `configure.sh` enables it, PAPER keeps it off, and an
  explicit `OT_BROKER_RECONCILE=True/False` pins it either way (configure.sh warns loudly on
  go-live if it's pinned off). Runs at startup and intraday every
  `BROKER_RECONCILE_INTERVAL_MIN` minutes (default **10**), plus wind-down sweeps at
  **15:45, 15:50, and 15:57** — the last guaranteed look before the loop goes dormant at 16:00.
  A broker position with no DB plan is *adopted* (sign-correct `ADOPTED_STOP_PCT` stop);
  a DB row absent at the broker is a *phantom* and is closed — **v3.6: at its REAL fill,
  recovered from broker order history** (`match_closing_fills` — closing actions only, manual
  closes split across multiple orders are quantity-weighted, history reaches back to the
  phantom's entry date on restart). Only when no closing order exists (expiry, assignment)
  does it fall back to the flagged `$0.00` booking. Recovered P&L is written to the DB, so
  `DAILY_LOSS_LIMIT` gates on truth even for positions you closed by hand. Phantom Telegram
  alerts carry the recovered P&L. Paper never reconciles.

## Session windows

| Gate | Window |
|---|---|
| **Opening-range lockout** | **No entries for any strategy before 9:35 ET.** Universal floor at `can_enter`; opens at 9:35:00 sharp. |
| ORB | 9:35 – **11:00** ET (hard cutoff) |
| Trend Continuation | 9:35 – 14:00 ET (trending regime only; runaway-ORB handoff + standalone) |
| Iron Condor | 11:00 – 14:00 ET |
| Butterfly | 12:00 – 14:00 ET (requires GEX PINNING) |
| Sweep Reversal | 9:35 – 14:00 ET |
| Global entry cutoff | **14:00 ET** — past this the tape turns erratic on dealer hedging |
| Hard close | 15:45 ET, all positions |
| VIX > 20 | Blocks butterflies (halved size in the 15–20 zone) |
| VIX > 30 | Blocks all new entries |
| Fed day | **The bot trades Fed days.** `is_fed_day` only boosts ORB conviction. |

---

# 🔱 PLANNED — Pitchfork sloped S/R (designed, NOT built, gated on Layer 2)

**Status: design-complete, deliberately unbuilt. Do not deploy before Layer 2 is ready.**
This section is the build brief so the next hands (or the next thread) inherit the full
requirement, not a hunch.

## What it is

An Andrews-style **median-line pitchfork** used as *sloped* support/resistance — the tilted
cousin of the Bollinger Band (BB is `mean ± σ` around a **horizontal** MA; a pitchfork is the
median line ± tines around a **sloped** axis anchored to three swing pivots). It is folded
**into `LiquidityMapper` as a long-lived sloped-zone object**, not a separate module — because
an S/R level and a liquidity pool are frequently the *same* price described twice, and unifying
them lets one zone carry both its S/R character and its liquidity character.

## Hard requirements (these are the spec, not suggestions)

- **HTF-anchored.** Pivots come from **daily/hourly** swings, computed on HTF data — never by
  zooming out an intraday calc. An LTF-anchored fork redraws every 20 minutes and means nothing.
- **Placed once, persists until invalidated.** A fork is not re-anchored on every wiggle. It
  stands until price *earns* its death: a **decisive close beyond the outer tine** on the wrong
  side, **or** the anchoring swing structure itself is broken. It is **NOT** invalidated by
  price merely tagging the median or a tine — those are *reactions*, the fork working as
  designed. (Naive implementations kill the fork on first touch; do not.)
- **Deterministic placement off `LiquidityMapper` swing pivots.** A pitchfork is pure
  coordinate geometry once the three pivots are chosen; the only hard problem is *anchor
  selection*, solved with a scoring rule (pick the anchoring price has reacted to most),
  validated offline. **NOT the vision API** — non-deterministic, un-backtestable, opaque in the
  live loop; that violates the "regime shapes the trade, outcomes never feed classification"
  discipline. The API's only legitimate role here is **offline anchor-quality validation**
  (batch-check that the deterministic anchors look sane across many tapes), never the live call.
- **Bands, not lines.** Zones are ranges (the tines are ranges by construction), which composes
  with liquidity pools and the BB/ORB ranges already in use.

## Where it contributes (ranked by whether it moves P&L)

1. **Conviction scoring** — rail-distance + confluence as new dimensions. A setup entering *at*
   a strong confluence zone is objectively higher-probability. This is the real payoff.
2. **The continuation trade's exit** — structural-level proximity is the **highest-confidence
   exhaustion signal** (a spent move *at a level* beats a spent move in open air). This is the
   `_evaluate_continuation` "ADD structural-level proximity" hook, already flagged in-code.
3. **Exit/target anchors** — the opposite rail is a natural target / trail-tighten point.
4. **NOT regime definition.** A fork tells you *where* a trend pauses, not *whether* you are
   trending. Regime stays ADX/structure/BB-driven. Do not wire it into the classifier.

## Empirical weight — ship at zero

The pitchfork conviction dimension **ships at weight 0 (shadow)** and is calibrated to
*realized edge* from paper data — exactly as `conviction_integrator` was deployed to observe
before it gated. The weight is a function of `(rail strength × timeframe × confluence)` and is
**allowed to stay 0** if the tape shows no edge. Do not hand-tune a weight; discover it.

## What we are WAITING FOR — the gate

**Build it when ready; do NOT deploy it until Layer 2 is set.** "Set" means:

1. **Trend labels trusted in production** — the `trend_engine v3.1` fix has weeks of live
   confirmation, not one afternoon.
2. **Conviction weights frozen** — the pitchfork enters as a *new* conviction dimension, and
   that is only measurable if the *existing* Layer-2 weights are a stable baseline. Calibrating
   a new dimension against a moving target is impossible. **This is the real gate.**
3. **A clean baseline logged** — a stretch of untouched production performance to compare the
   pitchfork twin against.

Concretely: **~2-week hands-off window from the 2026-07-XX day-zero** (materially changed
engine: trend v3.1 + VWAP + condor triggers + continuation), *then* the pitchfork build spins
up against a frozen Layer-2.

## How it gets built (isolation plan)

- An **ironically-named git fork** of this repo (keeps the production fleet's `git pull` safe).
  Pitchfork lives in **additive, separate modules** so upstream merges stay clean.
- Its own **isolated yfinance HTF feed** (cannibalized from v1/v2) — *not* the broker DXFeed
  stream. Adequate because the fork is HTF *context*, never execution; the entry fill still
  happens on real DXFeed price. Keep the two feeds strictly separated — yfinance HTF in, fork
  geometry out, **no yfinance price ever touches an entry/exit decision.**
- Backtest/replay harness **resident on the tester**.
- Proven via a **QQQ twin A/B**: the pitchfork-weighted tester vs a production QQQ twin on the
  current engine — same execution data, one variable (pitchfork conviction).
- **First concrete deliverable when the build starts:** the swing-pivot rule that anchors the
  fork + the invalidation condition. Everything else is geometry that follows from those two.

## Related future trade (prelude only, not scheduled)

**Rejection-fade** — the near-opposite of continuation. Sell a **premium-rich credit spread**
at a level that has been **firmly rejected**, with conviction **scaling up by HTF rejection
count** (a level rejected three times on the daily >> a one-touch). Continuation trades *with*
momentum into a level expecting breakthrough (debit); rejection-fade sells *against* momentum
into a level expecting it to hold (credit). This trade *wants* the pitchfork/LiquidityMapper
multi-touch HTF zone with a rejection-count attribute — it is the pitchfork's natural partner.

---

# 🔧 OPEN DEFECTS AND UNRESOLVED DECISIONS

**This section is the scrub list. Everything here is known. Items marked ✅ RESOLVED
carry the resolution date and the fixing file versions; everything else remains open.**

### A. ✅ RESOLVED 2026-07-12 — Two Layer-1 implementations
There WERE two: `analysis/regime_confluence.py` and `conviction_integrator.EvidenceAdapter`,
both producing an evidence vector with divergent per-regime math — the circularity failure
`ROADMAP.md` §Risks names. **Resolved by `conviction_integrator.py` v2.0:** `EvidenceAdapter`
and its duplicated `ramp()`/`flat_angle_deg()`/`midline_crossings()` are **deleted**.
`RegimeConfluenceScorer` is the sole Layer 1; the integrator consumes its
`.evidence()` vector and imports the regime labels from it (guarded, with string fallbacks
for isolation).

### B. ✅ RESOLVED 2026-07-12 — Layer 2 ported in-repo (Phase 0.1 done)
`analysis/conviction_integrator.py` **v2.0** is in-tree with the v3 emission law: **always
argmax** — the `UNKNOWN` fallback is deleted from emission; indecision is a low conviction
number on a best-fit label, never a seventh label. The θ_hold/θ_commit/δ hysteresis band is
kept for label stability, and the **STALE/gap state survives** (data faults still block;
indecision does not). Priors untouched — they await tape calibration.
`regime_confluence.py` (v1.1: fixed a silent config-import failure that ran every constant
on fallbacks) now feeds both the Layer-1 replay AND the integrator's Layer-2 tracks in
`tests/replay_confluence.py` v2.0. **Still shadow-only:** no live-loop path touches either —
that is ROADMAP Phase 0.2, deliberately not yet wired.

### C. ✅ RESOLVED 2026-07-13 — `docs/REPLAY_VALIDATION.md` false premise
It justified replaying over the DXFeed CSVs on the claim that the shadow observer *"scores off
yfinance"* and was therefore a divergent feed. **The claim was false.** Read straight from the
now-extracted source: `shadow/observer.py` acquires data through exactly one call —
`get_cache(symbol)` → `data/data_cache.py` → `data/market_data.py` — and since the v3.0 purge
`market_data` reads the on-box shared SQLite store written by `candle_feed.py`
(TastyTrade/DXFeed), read-only, heartbeat-guarded. No yfinance in the repo; none in
`requirements.txt`. **The observer scores off the same DXFeed tape the CSVs are cut from.**

**Resolved by `REPLAY_VALIDATION.md` v1.1:** the conclusion stands, on a true premise. The reason
to calibrate on the CSVs is **sampling, not source** — the observer's jsonl is tick-cadenced and
staleness-gated (a frame may repeat across ticks, or serve `None` past the hard-stale ceiling),
while the CSVs are deterministic, evenly-spaced 1-min bars. Same tape, different sampling;
calibration needs the deterministic one. The identical false claim in
`tests/replay_confluence.py`'s header comment was corrected in the same pass.

### D. ✅ RESOLVED 2026-07-13 — Shadow observer extracted from its tarballs
`observer/shadow_ops_v1.0.tar` and `observer/shadow_subsystem_v1.0.tar` are **extracted and
deleted**; the `observer/` directory is gone. All 13 members landed and were diffed
byte-for-byte against the archives.

**Correction to this defect's own instruction.** It said *"extract to `observer/shadow/`"*. **That
was wrong** — the package belongs at **repo root `shadow/`**, and that is where it now lives.
Three independent reasons: `shadow-observer.service` runs `python -m shadow.observer`; the modules
import each other as `from shadow.primitives import ...`; and `observer.py` derives `REPO_ROOT` as
two levels up from itself, so nested under `observer/` its output would land in
`observer/data/shadow/`. Non-code members go to root (`shadow_devtools.sh`) and `deploy/`
(5 unit/timer files).

**Extraction immediately paid for itself:** with the code greppable, `observer.py`'s docstring was
found still describing a yfinance feed — the exact rot this defect predicted, and the thing that
made defect C's false premise plausible. Fixed in `observer.py` **v1.1** (docstring only, zero
code change).

**Two traps caught in the same pass:**
- `shadow_devtools.sh` uploaded through the GitHub web UI landed at mode `100644`. The browser
  uploader **cannot** set the exec bit — it writes every blob `100644`. `./shadow_devtools.sh`
  fails with permission denied until the mode is committed from a clone. **Anything executable must
  be pushed from a shell, never the web UI.**
- `.gitignore` had no `data/shadow/` rule (the archived copy did). Added — without it the
  observer's runtime jsonl shows as untracked on every box.

**⚠️ Half resolved 2026-07-18 — script fixed, service half still open.**
`shadow_devtools.sh` **v1.1** now self-locates (`REPO="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"`, mirroring `observer.py:61`) — it runs from any checkout,
including the control box's `~/options-trader-v3`. **Still open:**
`deploy/shadow-observer.service` hardcodes `WorkingDirectory`/`ExecStart` to
`/home/ubuntu/options-trader`. That matches the 29 boxes' canonical path, so a QQQ-TEST
deployment works today as-is; templatizing the unit (sed the path at install time, like
`setup_ec2.sh` does for `optionsbot.service`) remains the durable fix before any
non-standard-path deployment. Same class as the installer repo-pointer bug.

### E. `VWAP_FILTER_ACTIVE` — a hard gate that was never built
Marked `UNWIRED`. Genesis constant: present at the initial commit, never referenced, **mentioned
in zero changelog entries.** What exists is a *soft* score in `setup_scorer` (weight 0.15;
misaligned = 0.25 on that dimension). It **cannot veto anything**:

```
Short ORB · UNKNOWN regime · price ABOVE VWAP  (i.e. shorting into strength)
  regime_conviction  0.20 × 0.00 = 0.000
  orb_quality        0.30 × 1.00 = 0.300
  vwap_alignment     0.15 × 0.25 = 0.0375   ← the "filter"
  liquidity_clear    0.20 × 1.00 = 0.200
  macro_context      0.15 × 0.50 = 0.075
                                 = 0.6125  →  Grade B  →  FIRES
```

VWAP misalignment costs **11 points on a 100-point scale, against a 55 threshold.**
**`crypto_trader` learned the opposite lesson the hard way** — shorts above VWAP and longs below
VWAP had to become **hard blocks**, because a relaxed validator let shorts into a strong uptrend
and produced consecutive losses. **That lesson is not ported here.**

### F. `MIN_RRR` — a risk/reward floor that was never built
Marked `UNWIRED`. Same genesis story, same changelog silence. No RRR floor exists anywhere. The
ORB's RRR is *structural* (stop = impulsive origin, target = 100% of range width), so it varies
per setup and is currently **ungated**.

### G. 🔄 MEASUREMENT SHIPPED 2026-07-18 — the near-miss retest is now logged (not yet graded)
The removed grace band was *intended* to admit a "B-grade almost-retest" (the wick approaches the
range but doesn't enter). **The code never did that** — the same condition's first clause already
required the wick to enter, so the near-miss never fired. The defect prescribed: if it is worth
grading, **measure it, don't gate it.** Done as of `orb_engine` v3.7 — every armed 1-min candle
emits a `retest_check` event to `analysis/signal_journal` carrying the penetration depth in PX
(**negative = near-miss**, wick approached but never entered) plus `orb_width`, and the confirming
candle records `ORBData.retest_depth_px`. Depth is logged in PX and divided by tape ATR **offline**
(ATR-relative per this defect — never a percentage; percentages scale into holes on high-priced
instruments, the root cause of every tolerance bug this file has had). **Still open:** whether to
feed `retest_depth` into `orb_quality` at all — that decision belongs to the Phase-3 ROI buckets
once the depth distribution has accumulated. The measurement gates nothing today.

### H. ✅ RESOLVED 2026-07-13 — Two "no entry after" times in two files
`config.NO_ENTRY_AFTER_ET = (11, 0)` (ORB-only) vs `time_utils.NO_ENTRY = dtime(14, 0)`
**hardcoded**, so editing config could not move the global cutoff.

**Resolved by `config.py` v3.3 + `utils/time_utils.py` v3.1**, with the call sites renamed in
`main.py` v3.3, `analysis/orb_engine.py` v3.6, `strategy/sweep_reversal_strategy.py` v3.1:

| constant | value | scope |
|---|---|---|
| `ORB_NO_ENTRY_AFTER_ET` | `(11, 0)` | **ORB-scoped.** The ORB entry cutoff — *and* the arm condition for sweep reversal. |
| `GLOBAL_NO_ENTRY_ET` | `(14, 0)` | **Global.** No new 0DTE entries after 14:00, any strategy. `time_utils.NO_ENTRY` now reads it. |

**Not a behaviour change** — both cutoffs keep their exact prior values (asserted at runtime:
`NO_ENTRY == 14:00`, `ORB_NO_ENTRY_AFTER_ET == (11, 0)`).

**The trap this defect was hiding.** The obvious fix — point `time_utils.NO_ENTRY` at the existing
`NO_ENTRY_AFTER_ET` — would have **silently moved the global 0DTE cutoff from 14:00 to 11:00**,
because the two names describe *different rules*, not one rule written twice. The rename exists so
that can never be misread again. `orb_engine.py` is where it matters most: `past_orb_cutoff` uses
the 11:00 constant while `is_past_entry_cutoff()` (deciding EXPIRED vs re-arm) uses the 14:00 one —
two cutoffs, one file, previously near-indistinguishable by name.

### I. `session_guard.can_enter(is_butterfly=...)` is an inert branch
`main.py` never passes `is_butterfly=True`, so the butterfly-specific cutoff path is unreachable.
Config v3.1 set `BUTTERFLY_ENTRY_CUTOFF_ET = (14, 0)` so that config agrees with live behavior.
**If 15:00 is ever wanted, the call site must be fixed too.**

### J. The repo-wide v3.0 bump destroyed version legibility
Every file's title reads `v3.0` regardless of actual maturity, so version headers no longer carry
information. `check_versions.sh` can confirm a deploy landed; it can no longer tell you what is
*mature*.

### K. Re-arm: unresolved
`runaway` and `timeout` never re-arm. Note the v3.5 origin gate makes this partly redundant —
after a runaway, price is extended and **cannot produce a valid break candle** until it returns to
the range anyway. A unified rule (*"re-arm on any invalidation before 11:00; the origin gate
decides whether a break is real"*) would be simpler and could not fire an extended breakout.
**Counter-argument:** current behavior is a deliberate hand-off to Sweep Reversal. Unchanged
pending a decision.

### L. ✅ RESOLVED 2026-07-13 — `fix_structure_analyzer.sh` deleted
A dead one-off patching a `None`-format crash already fixed in-tree by `structure_analyzer.py`
v1.1 (2026-06-30). Nothing referenced it. **Deleted.**

### M. Known pending, not addressed
Ghost folder on Windows tarball extraction · `setup_ec2.bat` security warning on double-click ·
dedicated Telegram bot for options-trader notifications.

### N. ✅ RESOLVED 2026-07-15 — Exits booked on submission at fabricated prices
The 15:45 hard close booked ~8 condor legs at `pnl=+$0.00` (order *submission*
treated as a fill, price fell back to entry premium). Fixed by the FillResult
contract (exit_engine/position_manager v3.4) + live fill-confirmation
(exit_engine v3.5) + phantom P&L recovery and denser reconcile cadence
(main/broker_reconcile/trade_logger v3.6). See "Fill-confirmed exits" above
and `docs/AUDIT_paper_live_divergence_2026-07-15.md`.

### O. ✅ RESOLVED 2026-07-15 — LIVE ENTRIES book on submission, not on broker fill
All three entry paths now record ONLY broker-confirmed fills at the broker's
per-leg net price, sized to the CONFIRMED quantity, via
`execution/order_confirm.confirm_order_fill` (bounded by
`LIVE_ENTRY_DEADLINE_SECONDS`; unfilled → cancel and walk away; partial →
book the filled size; uncancellable → page + reconcile adopts).
**Condor legs** (main v3.7): signed-credit limit at mid; `notify_leg_filled()`
advances only on real fills. **Single legs** (entry_engine v3.7): MARKET, fill
price read back from fills — never the signal mark. **Butterfly**
(entry_engine v3.7): debit priced NEGATIVE (signed convention — the old
positive price could never fill); attempt 2 (mid + `LIMIT_IMPROVE_TICKS`)
placed ONLY after attempt 1 is confirmed dead with zero fills, closing the
double-position race; butterfly records now persist lower/center/upper leg
SYMBOLS (the v3.5 live close and reconcile both require them). Paper mirrors
live friction via `PAPER_FILL_SLIPPAGE_PCT` (env-tunable `OT_PAPER_SLIPPAGE_PCT`,
default 1% against the trade — defect R) and returns the requested quantity in
one pass. Tests 1–14: `tests/test_entry_fill_confirmation.py`. Original finding:
The entry-side twin of defect N, found in the 2026-07-15 paper→live audit —
**NOT yet fixed**. (a) Condor legs book `response.order.price or net_credit`
the instant the mid-credit LIMIT is accepted — a never-filled entry becomes a
managed ghost, and `notify_leg_filled()` advances the legging state machine on
it. (b) Single-leg MARKET entries book `placed.price or signal.entry_premium`;
a market order has no `.price`, so the recorded entry is ALWAYS the signal
mark, never the fill. (c) Butterfly entries are broken three ways: debit sent
as a POSITIVE price (the SDK's signed convention reads that as demanding a
CREDIT — can never fill); fill detection reads `status` immediately after
submission (always Received/Routed → place/cancel churn); a fill during the
retry sleep plus a swallowed cancel failure can open a DOUBLE position.
**Fix shape:** entry mirror of exit v3.5 (bounded poll, record only confirmed
per-leg net fills, signed limits). Until built, live entries are unvalidated
regardless of how good paper looks. Full detail:
`docs/AUDIT_paper_live_divergence_2026-07-15.md` §L1.

### P. ✅ RESOLVED 2026-07-15 — Broken-wing roll opens a FICTIONAL vertical in live
Fixed (condor_roll v3.7): the rolled vertical is now a REAL signed-credit
limit order, fill-confirmed via `execution/order_confirm` — the record books
only confirmed contracts at the broker's net credit. The close of the old
untested vertical books the ACTUAL `fill.fill_price` (both modes route through
`place_exit_order`; paper mirrors live friction on the rolled credit). If the
open fails after the close succeeded, position-truth is preserved, a
HALF-COMPLETE page fires, and the roll re-evaluates next tick. The risk-free
claim is re-checked against the ACTUAL fill credit and pages if it came in
light. Tests: `tests/test_roll_is_real.py`. Original finding:
`condor_roll._execute_roll` step 2 claims "live order placement mirrors
_execute_condor_leg" — **no order is placed**; the rolled vertical is written
to the DB only. Live: the real untested vertical closes (fill-confirmed),
then a position that never existed is booked and managed. Secondary: step 1
books the close at `plan.close_cost` instead of the confirmed
`fill.fill_price` it just received. **NOT yet fixed** — either place a real
signed-credit order with fill confirmation, or gate the roll to paper. Audit
§L2.

### Q. ✅ RESOLVED 2026-07-15 — One `trades.db`, no mode filter (mode isolation shipped)
Fixed by trade_logger v3.7 (every decision/session query — `get_open_trades`,
`realized_pnl_today`, session losses, expired autoclose — is scoped to the
current mode via `COALESCE(paper_trade,1)`; legacy NULL rows count as paper,
the safe direction) + configure.sh v2.0 (trades.db and WAL sidecars archived
as `trades_<mode>_<stamp>.db` on EVERY mode switch, so histories never share a
file to begin with). Tests: `tests/test_mode_isolation.py`. Original finding:
`realized_pnl_today()` (the DAILY_LOSS_LIMIT source of truth) and
`get_open_trades()`/`get_open_trades_live()` (startup recovery, position
manager) ignore the `paper_trade` column. Switching to live after weeks of
paper: paper P&L closed the same ET day gates the LIVE breaker, and any
still-open paper rows are handed to the live bot, which submits real close
orders for them until reconcile phantoms them — polluting live realized P&L
again. Only *instrument* changes wipe the DB (paper mode only); *mode* changes
wipe nothing. **NOT yet fixed** — mode-filter both queries + archive
`trades.db` on switching to LIVE in configure.sh. Audit §L3. **Do this one
first: smallest change, blocks day-one contamination.**

### R. ✅ RESOLVED 2026-07-15 — Paper fills are perfect (was `PAPER_FILL_SLIPPAGE_PCT = 0.0`)
Now env-tunable (`OT_PAPER_SLIPPAGE_PCT`), default **1% against the trade**
(debits pay more, credits receive less), applied uniformly — condor legs
included, which previously ignored the knob. Set `0.0` for apples-to-apples
comparison with pre-change paper history. Original finding:
Paper enters and exits at the exact mid, both sides, every trade; live pays
spread crossing on entry and buys through the mark by
`LIVE_CLOSE_LIMIT_BUFFER` on exit. Paper P&L is therefore a structurally
optimistic estimate of live — materially so on wide SPX spreads. Consider
nonzero paper slippage so the next stretch of paper predicts live. Audit §M1.

### S. Offline replay is HTF-starved — the diary under-reports TRENDING by construction
The daily regime replay (`validate_regime.sh run_date` → `tests/replay_confluence.py`)
feeds the harness **one day-folder at a time**, so the 1h/1d timeframes never accumulate
enough bars to clear their EMA warmups: `trend_engine` returns NEUTRAL on the starved
timeframes and the vote dilutes — the exact mechanism behind the 0-TRENDING-in-34,925-ticks
finding (2026-07-16), *partially* addressed by trend v3.1's reweighting but structurally
present in every diary row scored on single-day tape. **Live boxes are unaffected**
(feed_store.db carries weeks of depth — why live trend detection works). Consequence:
diary baseline rows are trend-blind until fixed, and the Tier-B TRENDING acceptance row
cannot be honestly closed through the daily replay even once a real trend day is on tape.
**Fix = the BOOKMARK:** persist a rolling ~15-session window of **bars** per symbol
(bars, not engine state — the engines are stateless pure functions of the dataframes
passed in, so no serialization/drift risk), load+append+roll each EOD run, score today
with warm depth. Scores only ONE day per run (avoids the abandoned seed-builder's
per-bar full-stack slowness). Build and prove on the TESTER against copies of real
`ohlc/<date>/` folders **before** grafting onto `validate_regime.sh` — the EOD conductor
chain is finally flawless and stays untouched until the bookmark is proven inert.
Mitigation meanwhile: `regime_backfill --rebuild` re-scores all dated tape once the
bookmark lands, so no diary row is permanently lost — they are just wrong until rebuilt.

---

## File structure — every file, and what it currently does

**Legend:** ✅ live in the trading loop · 🧪 dev/analysis only · ⚙️ ops/deploy · 📄 docs · ⚠️ defective or unwired

### Root

| File | Purpose |
|---|---|
| `main.py` ✅ | **v3.9.** The bot. 15s loop: analyze → classify regime → dispatch strategy → score → size → enter; manages open positions, runs the BWB roll check, enforces the daily-loss halt, writes `orb_state.json` each tick. Holds the `UNKNOWN` hard gate and the ORB un-gate exception. Condor legs log `abs(short-strike delta)` as `setup_score` (calibration waypoint; see Iron Condor). **v3.7: live condor legs book ONLY broker-confirmed fills (`order_confirm`); v3.6: phantom P&L recovery + 10-min reconcile cadence with 15:45/15:50/15:57 wind-down sweeps; v3.8: threads `df_5m` into position management for the 5m FVG trail anchor; v3.9: signal-journal dispositions (fired/sizing_rejected/invalid) + condor plan/leg conviction events — log-only, Phase 3.1.** |
| `config.py` ✅ | **v3.3.** Every tunable parameter + credential accessors (env-only, never in source). `PAPER_TRADING` defaults `True`. |
| `README.md` 📄 | This file. Current state, not aspiration. |
| `ROADMAP.md` 📄 | **Build status lives here.** v2→v3 reconciliation, honest distance-to-vision, Phases 0–4, and the named risks. |
| `CHANGELOG.md` 📄 | v3.0 purge changelog (fork point, changed-file table, verification status). |
| `requirements.txt` ⚙️ | tastytrade, httpx, anyio, pandas, numpy, pytz. **No market-data dependency** — sqlite3 is stdlib. |
| `status.py` 🧪 | Live snapshot: ORB state/range/latches, regime, GEX pin, open position, daily-loss banner. Reads `orb_state.json` as authoritative. |
| `query.py` 🧪 | **v3.4.** Performance dashboard against `trades.db` — W/L, R, grades, exit reasons. None-guards a NULL `setup_score` (condor legs) so the open-position view can't crash on `:.2f`. |
| `debug_status.py` 🧪 | Verbose diagnostic for `status.py` instrument/env resolution. |
| `eod_summary.py` ⚙️ | Per-box EOD P&L writer (~15:50 ET, own timer). Emits `pnl_today.json` for control-side harvest. |
| `stress_theta_bleed.py` 🧪 | Offline stress test for the four theta gates. Patches `minutes_since`; no network. **Lives at root, not `tests/`.** |
| `test_candle_logger.py` 🧪 | Offline self-test: builds a synthetic feed store, verifies the logger's CSV output. **Root, not `tests/`.** |

### Shell / ops

| File | Purpose |
|---|---|
| `install.sh` ⚙️ | Web installer — the one-liner entry point. Pulls and runs `setup_ec2.sh`. |
| `setup_ec2.sh` ⚙️ | **v3.2.** Full box build: venv, deps, systemd units for `optionsbot` + `candle-feed` (bot ordered `After=`/`Wants=` the feed), credentials into the unit env, cleanup, drops to shell with venv active. |
| `bootstrap.example.sh` ⚙️ | Template for unattended deploy. Copy to `bootstrap.sh` (gitignored) and put secrets *there*. Shredded by `setup_ec2.sh` on completion. |
| `configure.sh` ⚙️ | Runtime settings menu: instrument, risk, paper/live, Telegram, TT creds, **daily-loss-cap override (option 6)**. |
| `check_versions.sh` ⚙️ | Recursive version-header + critical-string verification after a deploy. **Should also enforce the fleet↔control parity invariant. It does not.** |
| `push.sh` ⚙️ | Git push/deploy wrapper — self-healing, optional restart, verifies the push landed. |
| `snapshot.sh` ⚙️ | Bot state backup; **redacts secrets** before archiving. |
| `shadow_devtools.sh` ⚙️ | **v1.1.** Operator menu for the shadow subsystem: start/stop/restart the observer, toggle stage 1↔2, tail the journal, would-fire summary, EOD compare, isolation re-check. Observe-only — nothing here can place a trade. **v1.1: self-locates its repo (defect D script-half resolved); the service unit's hardcoded path remains — see defect D.** |
| `harden_hosts.sh` ⚙️ | Host hardening for a trading box (guards against unattended-upgrade restarts mid-session). Invoked from control. |
| `pull_today_ohlc.sh` ⚙️ | Background-detached EOD retrieval of today's full 1-min session on a box (works around `fleet.py`'s ~22s SSH ceiling). **Invoked by `fleet.py`.** |
| `install_candle_feed.sh` ⚙️ | Installs `candle-feed.service` on a box provisioned before v3.0. |
| `install_candle_logger_timer.sh` ⚙️ | Installs the 16:05 ET EOD candle-logger timer. |
| `install_eod_timer.sh` ⚙️ | Installs the 15:50 ET EOD P&L-writer timer. |

### `analysis/` — the reading of the tape

| File | Purpose |
|---|---|
| `orb_engine.py` ✅ | **v3.7.** The ORB state machine. Break → armed → retest → open, plus the three invalidations, the re-arm rule, the session break latches, and the impulsive-candle stop level. **No tolerances anywhere. v3.7: defect-G measurement — `retest_depth_px` recorded on confirm + per-candle `retest_check` journal events (near-misses included); gates nothing.** |
| `signal_journal.py` 🧪 | **v1.0 — Phase-3.1 instrumentation (log-only, never trades).** Append-only JSONL at `data/signal_journal/<date>/<SYMBOL>.jsonl`: `scored` (every scored signal incl. REJECTs, with bid/ask/IV quote context — the perishable data), `disposition` (fired/sizing_rejected/invalid), `retest_check` (defect-G depth distribution), `condor_plan`/`condor_leg` (conviction at decision time). Every emission swallowed on failure — the loop is byte-identical without it. Gitignored runtime output. |
| `get_orb_range.py` ✅ | Resolves the 9:30–9:35 range through `market_data.fetch_candles` (same feed the bot trades) → `orb_range.json` with `ESTABLISHED`/`IN_PROGRESS`/`EXPIRED`. |
| `regime_classifier.py` ✅ | **v1.3 — the LIVE classifier.** Memoryless boolean cascade, first-match-wins. Emits one label + a post-hoc conviction number that currently gates nothing. |
| `regime_confluence.py` ✅ | **v1.1 — LAYER 1 of v3 (canonical, sole).** Instantaneous graded per-regime evidence (`hard_veto × soft_necessary × Σ corroborators`), implementing `REGIME_TRUTHS.md` v0.2. v1.1 fixed a silent config-import failure (a wrong-home constant threw the whole guarded block; every constant ran on fallbacks). Feeds the L1 replay and the L2 integrator via `tests/replay_confluence.py` v2.0. **No live-loop path yet — Phase 0.2.** |
| `conviction_integrator.py` ✅ | **v2.0 — LAYER 2 (shadow-only; drives nothing).** Leaky per-regime conviction: rises on agreement, decays on disagreement with decay resistance scaled by banked conviction; **always-argmax emission** with θ_hold/displacement hysteresis — no `UNKNOWN`; `stale` (data gap/unwarmed) is the only hard no-trade marker. dt-aware, snapshot/replay warm start, embedded validation suite. **All thresholds are PRIORS pending tape calibration.** |
| `trend_engine.py` ✅ | EMA stacks, **ADX from the 5m timeframe**, momentum, timeframe alignment count. |
| `volatility_engine.py` ✅ | Bollinger Bands, VWAP, ATR, expansion/contraction state. Feeds condor strikes and regime evidence. |
| `structure_analyzer.py` ✅ | Swings, HH/HL/LH/LL sequence, S/R zones, **FVGs** (which the trail parks against). |
| `liquidity_mapper.py` ✅ | Maps named pools (PDH/PDL, equal highs/lows, session H/L). Feeds the sweep definition and the ORB's `liquidity_clear` score. |

### `strategy/` — what to trade when

| File | Purpose |
|---|---|
| `base_strategy.py` ✅ | `OptionsSignal` + the premium-level math every strategy inherits (`stop_premium`, `target_premium`, `trail_activation_premium`). |
| `orb_strategy.py` ✅ | Turns a confirmed ORB engine state into a signal: strike selection, liquidity-path check (**blocks on a named pool in the path with no extra confluence**), target adjustment, confluence notes. |
| `sweep_reversal_strategy.py` ✅ | Post-sweep reversal. Delta-band strike selection scaled inversely to reversal strength. ATR-aware recovery window. |
| `continuation_strategy.py` ✅ | **NEW 2026-07-18.** Trend-continuation on pullback to the BB midline. Trending-regime-gated (a stingy label is the signal). Low-bar entry (momentum resumption); exhaustion-based exit owns the risk. Two paths: runaway-ORB **handoff** (looser) + **standalone** (stricter). Debit directional. Paper-first. |
| `iron_condor_strategy.py` ✅ | **v3.1.** Legged condor, **BB-anchored strikes, zero delta**. Plan state machine + per-leg price triggers. **v3.1 restored an import missing since the file's first commit** — masked on the fleet by Python 3.14's lazy annotations (PEP 649); on any ≤3.13 interpreter the module raised `NameError` at import and killed `main.py`. Verified 3.12 vs 3.14 A/B. |
| `condor_roll.py` ✅ | **v3.7.** Broken-wing roll. Close of the old untested vertical books the CONFIRMED fill; the rolled vertical is a REAL fill-confirmed signed-credit order (was a DB-only fiction in live); risk-free re-checked against actual fills. |
| `butterfly_strategy.py` ✅ | **v3.1.** Debit butterfly centered on the **GEX pin**. Gated on PINNING + proximity + noon–14:00 + one-per-session. |

### `execution/` — orders and exits

| File | Purpose |
|---|---|
| `entry_engine.py` ✅ | Places the opening order (paper fills at the mark). Writes the `TradeRecord`, including `underlying_stop` — **the impulsive candle's wick, which the exit engine reads back.** |
| `exit_engine.py` ✅ | **v3.8.** All exits, routed per strategy (ORB floor/structure/theta/trails · Sweep BOS · butterfly/condor premium + regime-flip · adopted generic). **v3.4/v3.5: FillResult contract — paper simulates at the mark in one pass; live books only broker-confirmed fills at the real net fill price, with bounded polling, partial-fill weighting, idempotent order resume, 2-leg vertical closes, and signed marketable-limit pricing. v3.8: runner refinements — 40% premium floor (butterfly stays 25%), 5m-anchored FVG trails, 0.75 post-target fallback, sweep post-target trail replaces the +100% hard TP, MFE/MAE telemetry (see `docs/EXIT_RULES.md`). NEW 2026-07-18: `_evaluate_continuation` — exhaustion exit (regime-flip primary · 40% floor · extension-from-midline tightens trail · momentum divergence exits), prefers live `vol_state`/`trend` with `df_5m` fallback so it never raises on a missing snapshot.** |
| `position_manager.py` ✅ | **v3.8.** Owns the single open position (the condor's two verticals are the sole exception). **`_execute_exit` books ONLY on `FillResult.confirmed` at the actual fill price — an unconfirmed close leaves the row OPEN for the 15:45→16:00 retry loop (anti-orphan invariant).** Trail updates write `trail_stop`, never `stop_premium`. **v3.8: threads `df_5m` through to `exit_engine.evaluate()` (5m FVG trail anchor). NEW 2026-07-18: also threads optional `vol_state`/`trend` (defaults preserve every existing caller — avoids the 2026-07-16 signature-mismatch crash) for the continuation exhaustion exit.** |
| `broker_reconcile.py` ✅ | **v3.6, LIVE-only, auto-enables with LIVE mode.** Adopt / keep / phantom-close against the broker at startup + intraday (10-min cadence + 15:45/15:50/15:57 wind-down sweeps). **Phantom P&L recovery: a manually-closed position books its real fill from order history instead of a flagged $0.00.** Paper never reconciles. |

### `risk/` — sizing and gates

| File | Purpose |
|---|---|
| `setup_scorer.py` ✅ | **v1.3.** Scores a signal across 5 weighted dimensions per strategy → **Grade A (1.5×) / B (1.0×) / no trade.** There is no Grade C. **v1.3: emits a `scored` journal event for every scored signal, below-B REJECTs included (Phase 3.1 counterfactual capture).** |
| `risk_manager.py` ✅ | **v3.1.** Contract sizing, half-budget condor legs, reassess-after-every-loss, and the **net daily-loss halt** (DB-seeded, restart-proof). |
| `session_guard.py` ✅ | **v3.1.** RTH · **9:35 opening-range lockout (universal floor)** · 15:45 hard close · 14:00 entry cutoff · VIX-crisis lockout. |

### `data/` — one producer, many readers

| File | Purpose |
|---|---|
| `candle_feed.py` ✅ | **v3.8. THE single DXFeed producer per box.** Owns the box's only `DXLinkStreamer` subscription (its symbol across 1m/5m/15m/1h/1d + VIX) → SQLite (WAL) + heartbeat. **No other process may open a stream.** |
| `market_data.py` ✅ | Pure store **reader**. `fetch_candles`/`fetch_quote`/`fetch_all_candles` keep the v2 contract byte-for-byte, which is why nothing downstream changed. Fails loud on a stale heartbeat. |
| `data_cache.py` ✅ | Per-timeframe cache over the reader. A refresh failing past 3× the staleness ceiling returns `None` — a dead feed can't hide behind an aging frame. |
| `options_chain.py` ✅ | 0DTE chain from the TastyTrade SDK: strikes, greeks, marks, delta-band selection. |
| `gex_data.py` ✅ | **GEX computed live from that chain** (gamma × OI × 100 × spot, puts negated). Derives call wall, put wall, pin, flip, environment, ORB bias. No scraping. |
| `macro_data.py` ✅ | VIX (via `fetch_quote("VIX")` — same store), IV rank, Fed/FOMC calendar detection. |
| `tasty_client.py` ✅ | TastyTrade session/account (OAuth refresh, shared event loop). |
| `candle_logger.py` ⚙️ | **v3.1.** EOD store consumer → `data/OHLC/<date>/<SYMBOL>.csv`. **This CSV is the calibration substrate for the whole v3 campaign.** |

### `database/`, `notifications/`, `utils/`

| File | Purpose |
|---|---|
| `database/trade_logger.py` ✅ | **v3.8.** SQLite trade log. Spread columns for condor legs, `get_open_trades()`, `realized_pnl_today()` (which seeds the daily halt), `update_fields()`. **`trail_stop` column (auto-migrated) + `update_trail_stop()`; `update_stop()` removed — its only caller was the floor-overwrite bug. v3.7: every read is mode-scoped via `COALESCE(paper_trade,1)` (defect Q — paper history can never feed the live loss breaker). v3.8: `max/min_premium_seen` MFE/MAE columns, updated every tick.** |
| `notifications/alert_manager.py` ✅ | The 4 core Telegram events (start, stop, entry, exit) + BWB roll + daily-loss-limit. |
| `notifications/telegram_sender.py` ✅ | Bot API transport. |
| `notifications/test_telegram.py` 🧪 | Connectivity check. |
| `utils/time_utils.py` ✅ | **v3.1.** ET/RTH helpers. `NO_ENTRY` now reads `config.GLOBAL_NO_ENTRY_ET` (14:00) — **defect H resolved.** |
| `utils/math_utils.py` ✅ | Strike snapping, ORB strike selection, expected move, rounding. |
| `utils/check_sdk.py` 🧪 | TastyTrade SDK diagnostic. |

### `shadow/` — the shadow subsystem (observe-only, never trades)

Extracted from its tarballs 2026-07-13 (**defect D resolved**); `observer/` is gone.

| File | Purpose |
|---|---|
| `shadow/observer.py` 🧪 | **v1.1.** The observer service. Own systemd unit, own process, zero shared memory with `optionsbot.service`. Per RTH tick: reads the **same TastyTrade/DXFeed store the bot reads** via its own `DataCache`, runs the same engines, computes primitives, and appends one JSON line to `data/shadow/<date>/<SYMBOL>.jsonl`. Imports nothing from `execution/`, `risk/`, `strategy/`, `notifications/`. **Never trades.** |
| `shadow/primitives.py` 🧪 | Velocity / magnitude / position accumulator — the shared measurement layer beneath the scorers. |
| `shadow/scorers.py` 🧪 | Per-pattern precursor scorers (stage 2 only). |
| `shadow/registry.py` 🧪 | Level registry consumed by the scorers. |
| `shadow/eod_compare.py` 🧪 | EOD comparator: shadow log vs `trades.db` (**read-only**, `mode=ro`) + `data/OHLC/`. Reads each candidate threshold's base rate off the logs — **thresholds are the LAST parameter, set from data.** |
| `shadow/trading_day.py` 🧪 | Weekend/holiday check. |

**Staging (`OT_SHADOW_STAGE`):** `1` = primitives measure-only (default — verify velocity against `data/OHLC/` for a few sessions before any scorer consumes it); `2` = scorers + would-fire flags logged across a **range** of candidate thresholds (0.50–0.95). **Zero firing at either stage.**

### `deploy/` — systemd units (never imported by the bot)

| File | Purpose |
|---|---|
| `candle-feed.service` ⚙️ | Reference unit for the feed producer (`setup_ec2.sh` generates the real one). |
| `candle-logger.service` ⚙️ | EOD 1-min OHLC export unit (store consumer; needs no credentials). |
| `candle-logger.timer` ⚙️ | Fires the logger weekdays at 16:05 ET, shortly after the close. |
| `README_candle_logger.md` 📄 | Operator notes for the logger. |

### `docs/`

| File | Purpose |
|---|---|
| `REGIME_TRUTHS.md` 📄 | **v0.2.** The Layer-1 definitional audit: per-regime hard vetoes + graded confluence, the three-tier factor grammar, the discriminator matrix. `regime_confluence.py` is its implementation. |
| `REPLAY_VALIDATION.md` 📄 | **v1.1.** The Layer-1 validation/calibration plan. Premise corrected — the CSVs are the calibration substrate because their **sampling** is deterministic, not because the observer is a different feed (it is not). **Defect C resolved.** |
| `README_orb_stop_rework_v3_1.md` 📄 | The impulsive-wick stop fix, with the MU 07-10 reference. |
| `README_orb_regime_ungate_v3_2.md` 📄 | The `UNKNOWN` un-gate rationale. |

### `tests/` — ships to the fleet, **runs on control**

| File | Purpose |
|---|---|
| `replay_confluence.py` 🧪 | **v2.0 — the v3 workhorse.** Replays `regime_confluence` over harvested DXFeed 1-min tape — AND feeds each symbol-session's evidence through a fresh `ConvictionIntegrator`: every JSONL tick carries an `l2` object, the report gains a LAYER-2 section (emitted distribution, **label switches vs L1-argmax flips** — the churn metric — stale%). `--report-only <jsonl>` reprints a saved run without re-scoring (merged from the control-box local mod that never reached GitHub). CLI/exit codes unchanged; L1 acceptance remains the sole exit-code authority. |
| `regime_diary.py` 🧪 | **v1.1.** Rolling one-entry-per-date diary (upsert by date, JSONL + md). v1.1 adds an L2 line — emitted dominance, switches vs L1 flips, stale% — when the day's log carries `l2`; pre-v2.0 logs digest unchanged. Tape-only, never reads trades. |
| `regime_backfill.py` 🧪 | **v1.0.** Disk-driven catch-up: replays + diaries every harvest date that has `*_OHLC_*.csv` tape but no diary row. `--rebuild` re-scores all dated tape (retro-fills L2 after a threshold change). |
| `validate_regime.sh` ⚙️ | **v2.0 — the single entrypoint** for the manual regime workflow on 1-REPORTER (devtools 40–44 are thin wrappers): run today / a date / `--report` / `--diary` / `--backfill [--rebuild]`. Auto-bootstraps checkout + venv; `git pull --ff-only` per run. The executing copy lives at `~/validate_regime.sh` on control — sync it manually when this file changes. |
| `replay_classifier.py` 🧪 | Replays the live v1.3 classifier over logged tape (built for the sweep-definition correction). |
| `test_orb_retest_v33.py` 🧪 | **NEW.** Locks the MU 2026-07-10 reference: 09:48 is not a break · 09:49 is · stop = impulsive wick low · 09:50 retest fires · a body closing inside disarms · runaway doesn't re-arm. 10/10. |
| `test_regime_gate.py` 🧪 | State-transition pressure test on the `UNKNOWN` gate + reassessment throttle. |
| `test_market_data_contract.py` 🧪 | Locks the v3.0 reader contract (17 assertions). Run this before any change near `market_data.py`. |
| `verify_feed_v3.sh` ⚙️ | **ON-BOX acceptance gate.** Proves single-subscription, store health, ORB equivalence. Run during RTH on one paper box before a fleet deploy. |

### Runtime artifacts (gitignored, never committed)
`trades.db` · `bot.log` · `orb_range.json` · `orb_state.json` · `pnl_today.json` · `credentials.py` · `bootstrap.sh` · `*.pem` · `data/OHLC/` · `data/shadow/`

**Referenced but not in this repo — by design:** `fleet.py` (control plane, lives in `day_trader_pro`).
**Formerly referenced, genuinely missing:** `docs/persistence_integrator_design.md` — the citation was removed in `conviction_integrator.py` v2.0; the design contract now lives in that file's own header.
**Gone, and it was never a runtime dependency:** `timing_analysis.py`.

---

## Deployment

```bash
curl -fsSL https://raw.githubusercontent.com/TX-9AI/options_trader_v3/main/install.sh -o install.sh && bash install.sh
```

**Always purge the bytecode cache before restarting.** This is the single most common cause of "I
pushed the fix but it's still broken" — and it matters more than usual right now, because v3.4
renamed the `ORBState` strings.

```bash
cd ~/options-trader
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
sudo systemctl restart optionsbot
bash check_versions.sh
```

Monitoring: `python status.py` · `python query.py` · `bash configure.sh` (risk, mode, daily-loss
cap override).

**`config.py` must always default to `PAPER_TRADING = True`.**

---

## Changelog

### 2026-07-12 (late) — audit remediation batch
- **`iron_condor_strategy` v3.1** — restored the `OptionContract`/`OptionsChain` import missing
  since the file's first commit (v2, 06-30). Masked fleet-wide by Python 3.14's lazy annotation
  evaluation; fatal `NameError` at import on ≤3.13. Repo-wide AST sweep: sole instance.
- **Exit-reason integrity (F5)** — `trade_logger` v3.1 (new `trail_stop` column + migration,
  `update_trail_stop()`, `update_stop()` removed) · `position_manager` v3.1 (trail writes go to
  `trail_stop`) · `exit_engine` v3.3 (floor checks read the now-immutable `stop_premium`; trails
  seed from `trail_stop` on restart). Behaviorally neutral — same exit ticks and prices — but
  `exit_reason` stops labeling trail exits as hard stops. Deploy the three files together.
- **`regime_confluence` v1.1** — the guarded config import silently failed (one wrong-home
  constant threw the whole block; `_HAVE_CONFIG=False` on every box). Split into independent
  guards; config tunes now reach the Layer-1 scorer.
- **`conviction_integrator` v2.0** — ROADMAP Phase 0.1 port: always-argmax emission (`UNKNOWN`
  deleted), hysteresis/displacement kept, STALE kept, `EvidenceAdapter` + duplicated helpers
  deleted. **Defects A and B resolved.** Shadow-only; priors uncalibrated.
- **Installer repo pointers (v3.1)** — `install.sh` cloned `options_trader_v2.git`, so every
  fresh install deployed v2 (caught on the QQQ-TEST rebuild: v2.5 banner, 542-object clone).
  `install.sh`/`bootstrap.example.sh`/`setup_ec2.sh` prompts fixed; verified end-to-end on a
  fresh EC2 (231 objects, dual candle-feed + bot services, v3 banners).
- **`replay_confluence` v2.0 / `regime_diary` v1.1 / `regime_backfill` v1.0 /
  `validate_regime.sh` v2.0** — Layer-2 tracks in the daily manual replay (zero live-loop
  changes), `--report-only` drift-merged, diary/backfill/entrypoint landed in the repo for the
  first time (they lived only on the control box). Control's silent `git pull --ff-only`
  failure (dirty local `replay_confluence.py`) diagnosed and healed.

### v3.5 / v3.4 / v3.3 — 2026-07-12 (the ORB made definitional + doc scrub)
- **`orb_engine` v3.5** — the origin gate now keys on the **open** (`orb_low ≤ open ≤ orb_high`),
  not the wick. `ORB_BREAK_BUFFER` **removed** from the break test *and* the session latch, which
  preserves the latch's documented invariant that it uses the same threshold as
  `_check_for_break()`. Net effect: **fewer** breaks (the origin gate is strictly tighter) and
  **earlier** breaks (no buffer to clear). Side effect: marginally more breaks latch the sweep
  gate.
- **`orb_engine` v3.4** — state vocabulary corrected. `ORBState.RANGING` and `Regime.RANGING`
  shared a string while meaning unrelated things. Now `NO_RANGE` / `WAITING_FOR_BREAK` /
  `ARMED_LONG` / `ARMED_SHORT` / `OPEN_*`.
- **`orb_engine` v3.3** — **retest grace band removed.** `body_low >= orb_high * 0.999` admitted a
  candle whose body **closed back inside the range** as a confirmed retest, and bought it (~$0.97
  inside on MU; **~6 points on SPX**). That is the disarm condition. The near-miss it was
  *intended* to admit was never reachable.
- **`exit_engine` v3.2** — doc sync, **zero executable lines changed.** `_evaluate_orb`'s docstring
  still described the pre-v3.1 range-boundary stop — the exact bug v3.1 fixed, and a trap for
  anyone "correcting" the code back toward it. Now marked `[HISTORICAL — do not restore]`.
  Butterfly TP corrected (20%, not 25%).
- **`config` v3.2 / v3.1** — deleted (all verified unimported): `SESSION_LOSS_LIMIT`,
  `ORB_BREAK_BUFFER`, `ORB_TRAIL_ACTIVATION`, `CONDOR_SHORT_DELTA`, `CONDOR_DELTA_TOLERANCE`,
  `MIN_TF_CONFLUENCE`, `ENTRY_COOLDOWN_MINUTES`. Retained and explicitly marked **UNWIRED**:
  `MIN_RRR`, `VWAP_FILTER_ACTIVE`. The condor "delta-primary" comment was corrected — strikes have
  been BB-anchored since v1.1. Butterfly cutoff 15:00 → 14:00 (the 15:00 was unreachable; **not**
  a behavior change).
- Twilio dependency removed from `requirements.txt` (Telegram replaced it in v2.0; the dep
  lingered for six weeks).
- **Verified:** `test_orb_retest_v33` (10/10) · `test_market_data_contract` (17/17) ·
  `stress_theta_bleed` (7/7) · `test_regime_gate` — all pass.

### v3.2 / v3.1 — 2026-07-11 (ORB stop rework + regime un-gate)
- Stop anchors to the impulsive candle's **wick**, not its body. Inverted-risk entries
  **28% → 0%** across 44 symbol-sessions; median entry risk 0.089% → 0.201%; setup count unchanged
  (92 → 96).
- Structure exit fires on a close **beyond the impulsive origin**, not the range boundary. Runs
  beside the unconditional −25% floor as an **AND**.
- `ORB_FIRES_REGARDLESS_OF_REGIME` (default on) — see the v2.5 note at the top of this file.
- **Not P&L-validated.** Stop geometry and gate placement only; option-premium P&L cannot be
  reconstructed from underlying OHLC. That is a paper-forward question.

### v3.0 — 2026-07-10 (Yahoo-Finance purge)
Single shared TastyTrade/DXFeed store per box. `market_data.py` rewritten as a pure reader with a
byte-identical contract, so every downstream consumer needed zero changes. Readers fail loud on a
stale heartbeat. **No trading logic touched.**

*Earlier: v2.4 (theta rework, 9:35 lockout, break-latch fix, candle logger) · v2.3 (tracked condor
legs, BWB roll, narrow wings, three-state ORB range, net daily-loss halt) · v2.2 (iron condor) ·
v2.1 (ADX from 5m, Grade C eliminated) · v2.0 (live GEX, Telegram) · v1.0.*

---

## Security
Credentials live in the systemd environment only — never in source. `.gitignore` excludes
`credentials.py`, `*.pem`, `orb_range.json`, `orb_state.json`. `snapshot.sh` redacts secrets before
archiving.
