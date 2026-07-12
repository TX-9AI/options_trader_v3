# options_trader v3 — Vertigo Capital

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

Sweep, butterfly, and condor are **untouched**: they still self-gate and still do not fire
under `UNKNOWN`. Set `ORB_FIRES_REGARDLESS_OF_REGIME = False` to restore strict v2 gating.

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

---

## Regime classification (running: `regime_classifier.py` v1.3)

Memoryless boolean cascade, re-run from scratch every 15s. First match wins:

**SWEEP_REVERSAL → BREAKOUT_VOLATILE → COMPRESSION → TRENDING_BULL/BEAR → RANGING → UNKNOWN**

ADX comes from the **5-minute** timeframe, matching the trading horizon. `UNKNOWN` is a
genuine abstention (v1.2), not a catch-all — and it remains a **hard no-trade gate for every
strategy except the ORB**.

| Regime | Strategies permitted to fire |
|---|---|
| TRENDING_BULL / TRENDING_BEAR | **ORB** |
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
RETEST = the next 1m candle WICKS INTO the range and CLOSES OUTSIDE it.
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

### Iron Condor (legged, tracked)
RANGING fallback when no GEX pin is available. **Strikes are Bollinger-Band anchored — there
is no delta anywhere in the condor path.** Short call = lowest liquid strike at/above the BB
upper band; short put = highest at/below the BB lower band. Delta is deliberately excluded: it
is relative to where price *sits*, not to the actual range boundary.

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
- **Broker reconciliation** (`execution/broker_reconcile.py`, `BROKER_RECONCILE_ENABLED`,
  default **off**): on a LIVE restart, a position found open at the broker with no DB plan is
  *adopted* and managed by a generic exit path (sign-correct `ADOPTED_STOP_PCT` stop, long-side
  trail, 15:45 close). Paper never reconciles.

## Session windows

| Gate | Window |
|---|---|
| **Opening-range lockout** | **No entries for any strategy before 9:35 ET.** Universal floor at `can_enter`; opens at 9:35:00 sharp. |
| ORB | 9:35 – **11:00** ET (hard cutoff) |
| Iron Condor | 11:00 – 14:00 ET |
| Butterfly | 12:00 – 14:00 ET (requires GEX PINNING) |
| Sweep Reversal | 9:35 – 14:00 ET |
| Global entry cutoff | **14:00 ET** — past this the tape turns erratic on dealer hedging |
| Hard close | 15:45 ET, all positions |
| VIX > 20 | Blocks butterflies (halved size in the 15–20 zone) |
| VIX > 30 | Blocks all new entries |
| Fed day | **The bot trades Fed days.** `is_fed_day` only boosts ORB conviction. |

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

### C. `docs/REPLAY_VALIDATION.md` justifies its method on a **false premise**
It says to calibrate on the DXFeed CSVs *"not the live **yfinance** shadow observer — the
observer scores off yfinance."* **The observer does not score off yfinance.** The v3.0 purge
rewrote `market_data.py` behind the preserved `get_cache()` seam, and the observer was silently
migrated onto the shared store (CHANGELOG: it *"required zero changes"*). The *conclusion* (use
the CSVs) is still right. The *reason* is wrong — and it will send an agent off to "re-purge" a
thing that is already clean.

### D. The shadow observer ships as **unextracted tarballs**
`observer/shadow_ops_v1.0.tar` and `observer/shadow_subsystem_v1.0.tar`. Code that cannot be
grepped, diffed, or version-checked — which is precisely how `observer.py`'s docstring came to
describe a yfinance feed it no longer uses, without anyone noticing.
**Extract to `observer/shadow/` + `deploy/`.**

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

### G. The near-miss retest is unmeasured
The removed grace band was *intended* to admit a "B-grade almost-retest" (the wick approaches the
range but doesn't enter). **The code never did that** — the same condition's first clause already
required the wick to enter, so the near-miss never fired. If it is worth grading, it must be
**measured, not gated**: log `retest_depth = (orb_high − candle_low) / ATR` on every setup
(negative = near-miss), feed it to `orb_quality`, and let the Phase-3 ROI buckets decide.
**ATR-relative, never a percentage** — percentages scale into holes on high-priced instruments,
which is the root cause of every tolerance bug this file has had.

### H. Two "no entry after" times in two files
`config.NO_ENTRY_AFTER_ET = (11, 0)` (ORB-only) vs `time_utils.NO_ENTRY = dtime(14, 0)`
**hardcoded, not read from config.** Edit the config value expecting the global cutoff to move
and it won't. `time_utils` should read from `config`.

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

### L. `fix_structure_analyzer.sh` is a dead one-off
It patches a `None`-formatting crash in `structure_analyzer.py` — **a bug already fixed in-tree by
v1.1 (2026-06-30)**. Running it against current code is at best a no-op and at worst re-applies a
patch to already-patched source. It has no place in a deployed tree. **Delete it.**

### M. Known pending, not addressed
Ghost folder on Windows tarball extraction · `setup_ec2.bat` security warning on double-click ·
dedicated Telegram bot for options-trader notifications.

---

## File structure — every file, and what it currently does

**Legend:** ✅ live in the trading loop · 🧪 dev/analysis only · ⚙️ ops/deploy · 📄 docs · ⚠️ defective or unwired

### Root

| File | Purpose |
|---|---|
| `main.py` ✅ | **v3.2.** The bot. 15s loop: analyze → classify regime → dispatch strategy → score → size → enter; manages open positions, runs the BWB roll check, enforces the daily-loss halt, writes `orb_state.json` each tick. Holds the `UNKNOWN` hard gate and the ORB un-gate exception. |
| `config.py` ✅ | **v3.2.** Every tunable parameter + credential accessors (env-only, never in source). `PAPER_TRADING` defaults `True`. |
| `README.md` 📄 | This file. Current state, not aspiration. |
| `ROADMAP.md` 📄 | **Build status lives here.** v2→v3 reconciliation, honest distance-to-vision, Phases 0–4, and the named risks. |
| `CHANGELOG.md` 📄 | v3.0 purge changelog (fork point, changed-file table, verification status). |
| `requirements.txt` ⚙️ | tastytrade, httpx, anyio, pandas, numpy, pytz. **No market-data dependency** — sqlite3 is stdlib. |
| `status.py` 🧪 | Live snapshot: ORB state/range/latches, regime, GEX pin, open position, daily-loss banner. Reads `orb_state.json` as authoritative. |
| `query.py` 🧪 | Performance dashboard against `trades.db` — W/L, R, grades, exit reasons. |
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
| `harden_hosts.sh` ⚙️ | Host hardening for a trading box (guards against unattended-upgrade restarts mid-session). Invoked from control. |
| `pull_today_ohlc.sh` ⚙️ | Background-detached EOD retrieval of today's full 1-min session on a box (works around `fleet.py`'s ~22s SSH ceiling). **Invoked by `fleet.py`.** |
| `install_candle_feed.sh` ⚙️ | Installs `candle-feed.service` on a box provisioned before v3.0. |
| `install_candle_logger_timer.sh` ⚙️ | Installs the 16:05 ET EOD candle-logger timer. |
| `install_eod_timer.sh` ⚙️ | Installs the 15:50 ET EOD P&L-writer timer. |
| `fix_structure_analyzer.sh` ⚠️ | **DEAD.** A one-off patch for a `None`-format crash in `structure_analyzer.py` — **already fixed in-tree by v1.1 (2026-06-30).** Re-running it against current code is at best a no-op. Delete. |

### `analysis/` — the reading of the tape

| File | Purpose |
|---|---|
| `orb_engine.py` ✅ | **v3.5.** The ORB state machine. Break → armed → retest → open, plus the three invalidations, the re-arm rule, the session break latches, and the impulsive-candle stop level. **No tolerances anywhere.** |
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
| `iron_condor_strategy.py` ✅ | **v3.1.** Legged condor, **BB-anchored strikes, zero delta**. Plan state machine + per-leg price triggers. **v3.1 restored an import missing since the file's first commit** — masked on the fleet by Python 3.14's lazy annotations (PEP 649); on any ≤3.13 interpreter the module raised `NameError` at import and killed `main.py`. Verified 3.12 vs 3.14 A/B. |
| `condor_roll.py` ✅ | Broken-wing roll solver: smallest roll toward price that makes the tested side risk-free. One-time, final. |
| `butterfly_strategy.py` ✅ | **v3.1.** Debit butterfly centered on the **GEX pin**. Gated on PINNING + proximity + noon–14:00 + one-per-session. |

### `execution/` — orders and exits

| File | Purpose |
|---|---|
| `entry_engine.py` ✅ | Places the opening order (paper fills at the mark). Writes the `TradeRecord`, including `underlying_stop` — **the impulsive candle's wick, which the exit engine reads back.** |
| `exit_engine.py` ✅ | **v3.3.** All exits, routed per strategy. ORB: hard close · unconditional −25% floor · impulsive-origin structure stop · gated theta bleed · FVG/% trails. Sweep: BOS. Butterfly/condor: premium + regime-flip. Adopted: generic. **v3.3: floor checks read the immutable `stop_premium` only; trails seed from the persisted `trail_stop` on restart — exit_reason labels are truthful.** |
| `position_manager.py` ✅ | **v3.1.** Owns the single open position (the condor's two verticals are the sole exception). Live chain marks for P&L in paper. **Trail updates write `trail_stop`, never `stop_premium`.** |
| `broker_reconcile.py` ⚙️ | **LIVE-only, default OFF.** Adopt / keep / phantom-close reconciliation against the broker on restart. Paper never reconciles. |

### `risk/` — sizing and gates

| File | Purpose |
|---|---|
| `setup_scorer.py` ✅ | Scores a signal across 5 weighted dimensions per strategy → **Grade A (1.5×) / B (1.0×) / no trade.** There is no Grade C. |
| `risk_manager.py` ✅ | **v3.1.** Contract sizing, half-budget condor legs, reassess-after-every-loss, and the **net daily-loss halt** (DB-seeded, restart-proof). |
| `session_guard.py` ✅ | **v3.1.** RTH · **9:35 opening-range lockout (universal floor)** · 15:45 hard close · 14:00 entry cutoff · VIX-crisis lockout. |

### `data/` — one producer, many readers

| File | Purpose |
|---|---|
| `candle_feed.py` ✅ | **v3.2. THE single DXFeed producer per box.** Owns the box's only `DXLinkStreamer` subscription (its symbol across 1m/5m/15m/1h/1d + VIX) → SQLite (WAL) + heartbeat. **No other process may open a stream.** |
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
| `database/trade_logger.py` ✅ | **v3.1.** SQLite trade log. Spread columns for condor legs, `get_open_trades()`, `realized_pnl_today()` (which seeds the daily halt), `update_fields()`. **New `trail_stop` column (auto-migrated) + `update_trail_stop()`; `update_stop()` removed — its only caller was the floor-overwrite bug.** |
| `notifications/alert_manager.py` ✅ | The 4 core Telegram events (start, stop, entry, exit) + BWB roll + daily-loss-limit. |
| `notifications/telegram_sender.py` ✅ | Bot API transport. |
| `notifications/test_telegram.py` 🧪 | Connectivity check. |
| `utils/time_utils.py` ✅ | ET/RTH helpers. **⚠️ Hardcodes `NO_ENTRY = 14:00` instead of reading config — see defect H.** |
| `utils/math_utils.py` ✅ | Strike snapping, ORB strike selection, expected move, rounding. |
| `utils/check_sdk.py` 🧪 | TastyTrade SDK diagnostic. |

### `observer/` — the shadow subsystem ⚠️

| File | Purpose |
|---|---|
| `shadow_subsystem_v1.0.tar` ⚠️ | **UNEXTRACTED.** Contains `shadow/observer.py`, `scorers.py`, `primitives.py`, `registry.py`, `eod_compare.py`, `deploy/shadow-observer.service`. Observe-only: runs the same engines in its own process and appends one JSON line per tick to `data/shadow/<date>/<SYMBOL>.jsonl`. **Never trades.** |
| `shadow_ops_v1.0.tar` ⚠️ | **UNEXTRACTED.** `shadow/trading_day.py`, `shadow_devtools.sh`, start/stop service+timer units. |

> Both are **opaque blobs** — un-greppable, un-diffable, un-version-checkable. This is exactly how `observer.py`'s docstring came to describe a yfinance feed it no longer uses. **See defect D.**

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
| `REPLAY_VALIDATION.md` ⚠️ | **v1.0.** The Layer-1 validation/calibration plan. **Its stated premise is false — see defect C.** |
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
