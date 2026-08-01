# docs/BACKLOG.md — v3.35


**Read top-down.** The clock sets the dates, PART 1 is the open schedule in
accomplishment order — that trajectory is the plan and does not get reshuffled —
PART 2 is what is parked, PART 3 is what is done, and the document's own history
sits at the bottom where it belongs.

**TAGS on every open item — grep one to fill a session:**
`[DESK]` no fleet, no data wait, workable today · `[DESK→DEPLOY]` build now, bake
Monday · `[DESK·DATA]` blocked only until sessions accrue · `[FLEET]` needs boxes
up or a deploy window. **DESK is the only bucket effort can move**; the rest
unblock on the calendar. Earned value: `python3 tests/evm_status.py`.

## PART 0 — THE CLOCK

| Anchor | Date | What |
|---|---|---|
| Epoch 1 start | **Wed Jul 29** | Epoch 1 began (label was "Today" — stale by 07-30) |
| Deploy Monday 1 | **Mon Aug 3** | Hard gates (E, F) + friction unification (T.2) + N.2/N.3 captures go live on the fleet, RTH |
| Deploy Monday 2 | **Mon Aug 10** | THE calibration deploy (level hierarchy, L2.4 priors, L1.6 flat cut, L1.11 ramps) — **L2.6 freeze-candidate window opens** |
| Freeze declared | **Fri Aug 21 EOD** | L2.6 frozen baseline, if the window ran clean |
| Deploy Monday 3 | **Mon Aug 24** | L3.3 gate matrix (flagged, paper) + evidence-confirmed sweep changes + N.5 latency telemetry |
| **GO LIVE** | **Mon Aug 31, RTH** | Tiny size, subset of symbols — live through **Sep 1–4, the first week of September** ✅ |
| Labor Day | Mon Sep 7 | Markets closed — analysis day |
| Descent notch | Tue Sep 8 | Half size if week 1 was clean |
| **FULL SIZE** | **Mon Sep 14, RTH** | Mid-September ✅ (contingent on two clean live weeks; raise-back trigger stays armed) |

**Honesty note on compression.** ROADMAP L3.4 specifies a 3–6 week bar-placement
campaign; this calendar does not contain one before go-live. The schedule resolves
that the way L3.6 already prescribes: go live with **provisional bars set one bucket
ABOVE the paper crossing, at minimum size**, descend one notch per clean review
window, and **raise back on the first negative read.** The L3.4 campaign keeps
running underneath the ramp — Sep 14 full size is the plan, not a promise the data
can't veto. Any freeze break during Aug 10–21 resets the L2.6 clock and slides
everything downstream of it.

**Standing daily habits (every session, all epochs):** `label_day.sh` at EOD only
when overriding auto_label (feeds L1.6/L1.7) · AA-watch: check for any two-sided
condor firing both legs near-simultaneously · verify the chain-snapshot + journal
+ regime_log harvest landed (one glance at the completeness manifest, once shipped
Jul 30).

---

## PART 1 — THE SCHEDULE (open items, in accomplishment order)

**TAGS — what each open item actually requires.** Grep one to fill a session:
`[DESK]` self-contained, no fleet, no data wait — workable ANY day, today included.
`[DESK→DEPLOY]` build is desk work but needs a bake to take effect → deploy Monday.
`[DESK·DATA]` desk work, blocked only until enough sessions accrue.
`[FLEET]` needs boxes up or a deploy pass — cannot be done from the desk.
The DESK pile is the only part of this list under our direct control; DESK·DATA
unblocks itself on the calendar. Drive DESK to zero and the freeze waits on data
alone, not on us.


### EPOCH 1 — SCRUB & INSTRUMENT — Wed Jul 29 → Sun Aug 9

*Goal: suite green, canaries current, time-critical data harvested, the two
never-built gates built and proven, the bookmark live, mapper hierarchy proven on
the tester. Nothing behavior-changing deploys except on Mon Aug 3.*

**✅ Wed Jul 29 — day closed. T.1 · T.3 · U all resolved — see PART 3.**
**◐ Thu Jul 30 — L2.5 ran in production for the first time in the project's
history.** Seven of eight items resolved and marked ✅ inline below. **W.1 is
NOT resolved and carries forward** — the quarantine cannot complete until
enough real L2 data exists to compare against (re-check at the Aug 10
calibration-epoch start). The day is not "closed"; it is closed *except W.1*.
- `[DESK·DATA]` **W.1 — 🔴 QUARANTINE ALL PRE-2026-07-30 L2 DATA. The scope is the entire
  project history, not one session.** This item was written as "quarantine
  07-29" when we believed the L2.5 outage began with the 07-28 excavation. The
  v4.7 root cause proved otherwise: `_REGIME_ENGINE` was `.lower()`ed to `"l2"`
  and both gates compared it to the literal `"L2"`, so the L2 block was
  unreachable from the moment v4.0 wired it. **No environment variable could
  have matched, because the DEFAULT itself failed the comparison.** Every regime
  label and conviction value this fleet has ever produced came from the v1.3
  classifier alone. Confirmed empirically: `[L2` count ZERO across bot.logs of
  34k–138k lines on all 29 boxes, `integrator_state.json` had never been written
  anywhere, and `FAILED`/`STALE` were also zero — the block never ran, so it
  could not even fail.
  **First real L2.5 data: Thu 2026-07-30, from ~09:55 ET** (the boxes committed
  after the 25-bar 1m warm-up; `RECOVERED=1` on all 15).
  **WHAT IS ACTUALLY AFFECTED — anything conditioned on an L2 label or an L2
  conviction:** `conditional_tables` (regime × strategy × outcome — the
  conditioning variable was v13 throughout), the **L2.4 churn calibration** (it
  has never seen integrator churn), the **L1.11 ramp fits**, and the readiness
  `conv_val` ramp. Note the knock-on: the 07-28 finding that "eight boxes sat at
  conviction 0.679 simultaneously = L2 integrator saturation" was a
  MISATTRIBUTION — that was v1.3's conviction distribution, and the observed
  0.59–0.83 band is v1.3's band. Refit that ramp from L2 data, not from the
  07-28 digest.
  **WHAT IS NOT AFFECTED — assess these on their own merits, this is not an
  if/then cascade:** ORB (regime-agnostic by design, defect V); all fill,
  friction and latency work (T.2, N.4, N.5); harvest/conductor plumbing; the
  morning selection chain (Y); push.sh (V); trade mechanics, exits and risk.
  None of it is conditioned on an L2 label, so none of it waits.
  **HOW (mechanical, not archaeological):** main v4.8 stamps
  `regime_log.engine` and `trades.regime_engine` with `L2`/`v13`, so from today
  the split is a `WHERE engine='L2'` clause. Rows written before v4.8 carry NULL
  — which is honest: provenance for those is genuinely unknown at row level,
  though we now know from the reachability proof that all of them are v13.
  Treat `engine IS NULL OR engine='v13'` as excluded from any L2-conditioned
  fit.
  **VALIDATE:** re-run `conditional_tables` with and without the exclusion and
  confirm the row counts collapse to today-only — if they do not, the filter is
  not being applied. Then re-run once ~10 sessions of real L2 data exist and
  compare the tables; a large divergence quantifies exactly what the v13-fitted
  priors were worth.
  **TIMELINE — TIGHT, NOT DERAILED.** The Aug 21 freeze assumed roughly two
  weeks of L2 baseline. Real L2 data starting 07-30 gives ~16 trading sessions
  by Aug 21 — still inside the original intent. The genuine constraint is
  PER-SYMBOL depth rather than session count: only ~15 of 29 boxes trade daily
  and the cohort now follows the brief, so any per-symbol L2 statistic will be
  thinner than the session count suggests. Re-check sample adequacy at the
  Aug 10 calibration-epoch start rather than assuming it.

**✅ Thu Jul 30 — AFTER THE CLOSE — Y · Y.1 · Y.2 all resolved, see PART 3.**
**⬜ Fri Jul 31**
- `[DESK]` **AI — condor trigger geometry: the midpoint is wrong, and that is
  the real design question.** From the same CVX log: spot ~190, `bb_upper=190.93`,
  and the call trigger sat at **193** — the 0.80xEM dual floor put the short at
  195 and 0.65 of that distance lands well OUTSIDE the band. So the plan needed a
  breakout-sized move during RANGING, a regime defined by the absence of one.
  Operator's read, recorded because it frames the fix: Bollinger boundaries fired
  too often; expected-move-from-spot is too far to reach; what is actually needed
  is expected move measured from a MIDPOINT that has not been identified yet.
  **This is pitchfork work** — a sloped median line gives a midpoint that moves
  with structure, where BB is a lagging envelope and EM-from-spot assumes no
  drift.
  **ANCHOR CANDIDATES CONSIDERED 2026-07-30 (record so they are not re-litigated):**
  *GEX pin* — REJECTED for condor. main.py:1049 assigns condor as the "RANGING
  fallback when no GEX pin"; condor is never even passed a gex object. Anchoring
  to the pin folds condor into butterfly's territory, and butterfly has 27
  lifetime trades against condor's 362 — it would inherit that rarity.
  *VWAP* — LIVE CANDIDATE. Always available (no pin gate), already computed in
  VolatilityState (`vwap`, `price_vs_vwap`), volume-weighted so it marks where
  trade actually happened rather than where price averaged, and in a trending
  session it sits BEHIND price — which skews the structure toward the drift, the
  direction a sloped median would too. Condor references it zero times today.
  **OPERATOR DOCTRINE ON DATA (2026-07-30):** "I'd rather have a pool of some
  data than the damn thing won't fire and we're getting no data." A strategy that
  fires often and loses is worth more right now than one that is theoretically
  correct and silent — collect wide on paper, then place the gate at the
  fee-adjusted-ROI zero crossing, which is exactly the substrate
  conditional_tables.py was built to produce. **Constraint:** the loose version is
  NOT unmeasured — the pre-dualfloor code sold with no minimum distance and "bled
  P&L for ~3 weeks". Widening the floor back out re-runs a known-losing
  experiment. What is unmeasured is the MIDDLE: an anchor where it fires AND
  works. **Calendar:** go-live Aug 31 — collect through August, locate the
  crossing by the third week, leave a week to bake the chosen threshold. **Do NOT re-tune 0.65 or 0.80 in isolation**; that is the category-3
  optimisation the operator does not want. The geometry decides whether the
  strategy is salvageable, and the pitchfork is the instrument.
**⬜ Sat Aug 1**
- `[DESK·DATA]` **AJ — 🔴 THE HANDOFF PATH IS THE CHASE-VS-RETEST ANSWER, and it
  has been collecting data since July under a different name. Candidate outcome:
  retire the standalone path and run handoff-only — NOT before ~2 more weeks.**
  `trend_continuation_handoff     50 trades  56% WR  +$1,333.50  avg +$26.67`
  `trend_continuation_standalone  49 trades  46% WR  -$2,024.00  avg -$41.31`
  **WHAT HANDOFF ACTUALLY IS** (`main.py:980`):
  `_is_runaway = getattr(orb, "invalidation_reason", "") == "runaway"`.
  A handoff fires on exactly the setups **ORB had to discard**: the range broke,
  price ran away, never returned for the retest, and the ORB was invalidated as
  `runaway`. Continuation then picks the move up on a pullback.
  **THIS IS THE COUNTERFACTUAL.** ORB's state machine only promotes ARMED ->
  OPEN when price RETURNS to the broken level; a strong trend is precisely when
  it does not, so the retest requirement systematically discards the breaks that
  worked (see AH). "What would those have returned if taken?" was believed
  unmeasurable — the assistant said so explicitly on 07-30 — and it was wrong:
  the handoff path is that measurement, running since July.
  **THE PRECISE FINDING, which is better than "chasing works":** handoff still
  requires a PULLBACK (1m wick tagging an unfilled 5m FVG). It is not
  entry-at-the-break. It is *runaway confirms the directional force, then enter
  on a SHALLOW pullback rather than a full retest.* That is a third option, not
  either of the two the question was framed around.
  **CONFOUND — state it every time these numbers are cited.** Handoff also runs a
  LOOSER momentum gate (accepts ACCELERATING **or** FLAT; standalone demands
  ACCELERATING). Two variables differ, not one. The direction is what makes it
  interesting: the looser gate is the winning one, which says the prior runaway
  is doing more filtering work than momentum strictness ever did. A clean read
  needs handoff-with-strict-momentum, or standalone-with-loose — neither exists
  in the data yet.
  **SECOND CONFOUND:** `exit_engine` v4.10's BOS stop lands Mon Aug 3 and will
  move standalone's P&L specifically (its losses concentrate in
  `max_loss_floor`, which is the hole BOS fills). **The numbers above are the
  PRE-BOS baseline and are not comparable to post-Aug-3 sessions.**
  **DECISION PATH (operator, 2026-07-31): retire standalone and run handoff-only
  is the candidate outcome — but NOT on one session.** Gate the decision on:
  (1) ~2 more weeks of sessions, i.e. **review ~Aug 14**, after v4.10 has been
  live long enough that standalone is being judged WITH its structural stop, not
  without it; (2) does standalone still lose once `bos_exit` replaces
  `max_loss_floor` on its never-worked trades? If BOS rescues it, the entry was
  never the problem; (3) does standalone account for the TRENDING_BEAR
  concentration (22 trades / 32% / -$1,533.50 fleet-wide on 07-31)? If its losses
  are one-sided, the answer may be a direction gate rather than deletion.
  **DO NOT DELETE A PATH THAT IS STILL THE ONLY SOURCE OF SETUPS IN ITS REGIME.**
  Handoff requires a prior runaway ORB; on days with no runaway there is no
  handoff. Retiring standalone means accepting zero continuation trades on those
  days — quantify that cost before cutting: count sessions in the banked corpus
  with zero runaways.
- `[DESK·DATA]` **AH — ORB in RANGING: is the flagship firing in a regime that
  contradicts its own thesis? (weekend work, deliberately — no trading day is
  spent on this).** First evidence 2026-07-30 from `tests/backtest_harness.py`
  over 14 spliced CVX sessions: **10 setups detected, 10 fired, 0 blocked by the
  regime gate**, exits `TARGET 1 / STRUCTURE_STOP 8 / EOD_FLAT 1`, underlying
  expectancy **-1.56R**, and the regime labels those fired under were
  **RANGING 7, UNKNOWN 2, TRENDING_BEAR 1**.
  **MECHANISM (why this is worth a weekend, not a P&L observation):** an opening
  range BREAKOUT is a directional continuation bet — it wagers price leaving the
  range keeps going. RANGING is definitionally mean-reverting. A breakout inside
  a ranging tape is not a low-quality signal, it is a STRUCTURALLY false one, and
  8-of-10 STRUCTURE_STOP is the fingerprint: the structural stop sits at
  invalidation and a range routinely trades back through it. This reopens defect
  V deliberately — V un-gated ORB on the reasoning that break-and-retest
  confirmation IS the filter; this says confirmation may not be sufficient in a
  range.
  **DO NOT ACT ON THIS YET.** One symbol, ten trades, and CVX was **51% RANGING**
  over the window — unusually range-bound, so "7 of 10 in RANGING" may describe
  CVX more than it describes ORB. ORB is the only strategy currently earning;
  changing its gating on this evidence would be the exact mistake this backlog
  keeps recording.
  **PREREQUISITE ✅ DONE 2026-07-31** — harness **v1.2** gained `--all` (lifts the
  8-trade display cap) and `--json PATH` (appends every fired trade as jsonl:
  symbol, ts, long/short, regime, entry, stop, outcome, under_R). Sweep **v1.3**
  threads them through, so one command pools all 29 symbols:
  `python3 tests/backtest_sweep.py --json /tmp/orb_trades.jsonl`
  Then group by regime and average `under_R`. The cap mattered because the first
  8 fires chronologically is not a random sample — it is the start of the window.
  Still a per-symbol sweep (NOT a cross-symbol
  splice: intraday frames are session-scoped and safe, but HTF is CONTINUOUS by
  design, so splicing CVX at $195 onto QQQ at $560 corrupts exactly the 1h depth
  the multi-day splice exists to build).
  **VALIDATE:** if ORB-in-RANGING is consistently negative across 6+ symbols,
  that is a mechanism finding and a regime gate is justified. If CVX is the
  outlier, it is a symbol characteristic and ORB stays as written.
- `[DESK·DATA]` **S / L1.9 — ◐ PARTLY RESOLVED 2026-08-01. THE BOOKMARK WAS
  ALREADY BUILT (v1.2, 2026-07-21) — this item's premise was stale, the same
  class as T.1/T.3 on Jul 29. What was actually wrong was a DEFECT INSIDE it,
  and that is now fixed and tested (commits 0a0da3b, 380a1bd).**
  **THE DEFECT — the bookmark warmed the 1m frame too, and 1m is the one frame
  live deliberately does NOT warm.** v1.2 prepended prior sessions to `df1m` so
  the RESAMPLED 5m/15m/1h would carry ADX/EMA history — correct, and still the
  point. But `s1m` was then sliced from that same concatenated frame, so the
  25-bar 1-minute close window handed to the scorer STRADDLED THE OVERNIGHT GAP
  for the opening 25 bars of every replayed session. `market_data` v3.1
  session-scopes 1m ONLY, on purpose, and `tests/test_market_data_contract.py`
  already asserts that contract on the LIVE path — the replay violated the
  identical contract. Live has <25 bars until ~09:55 and passes `closes=None`,
  so RANGING and COMPRESSION go UNSCORED; the replay scored both from 09:30 off
  a gap-spanning regression. Proven on a two-session fixture through the real
  code path: **24 of the 25 window bars belonged to the PRIOR session and a
  -1.14 gap sat inside the regression.** Fixed in **replay_confluence v2.1**;
  guarded by `tests/test_replay_1m_session_scope.py` (6 tests, incl. a
  source-level assert and a deliberate-failure check that reverting turns 3 red).
  **WHY IT HID: the bookmark made the replay MORE correct on the frames anyone
  was looking at** (ADX went 0.0 -> warm), so the fix that introduced the 1m
  contamination was validated by the improvement it also delivered.
  **SECOND DEFECT, found the same day — the frames were UNCAPPED.** Every warm
  session added history no live engine ever receives, and the divergence grew
  with `--warm-sessions`. It became load-bearing the moment AK woke the 15m vote
  and left 1h asleep: at warm >= 7 the replay's 1h frame reaches 55+ bars and
  VOTES, while live holds it at 50 and it stays NEUTRAL. **replay_confluence
  v2.2** trims each resampled frame to `TIMEFRAMES[tf]["candles"]` — read from
  config, so it cannot drift from what data_cache requests — and moves the warm
  default 5 -> 8. **regime_backfill v1.2** adds a `--warm-sessions` passthrough,
  because nothing in the chain ever passed one: every diary, backfill and
  a2_characterise run to date used the old default of 5.
  **WHAT REMAINS, and why this is now DESK·DATA not DESK:** validation criterion
  (1) INERTNESS is met — `test_fix_is_inert_when_the_bookmark_is_off` proves the
  change is a no-op at `--warm-sessions 0`. Criterion (2) HONESTY GAIN is NOT
  met and cannot be until **N.1** puts regime_log on control and **AM** rebuilds
  the corpus. Do not mark this ✅ on the strength of the defect fix alone.
  *The original build spec and VALIDATE bar follow — the VALIDATE half is still
  the standard this item is closed against, so it is kept verbatim rather than
  summarised.* Rolling ~15-session window
  of **bars** per symbol (bars, not engine state — the engines are stateless),
  load+append+roll each EOD, score today warm. This unblocks honest offline
  TRENDING and everything L1.6/L1.11 need.
  **HOW:** per-symbol rolling bar store (csv/parquet under the tester's data root,
  keyed by timeframe), EOD job: load window → append today's `ohlc/<date>/` →
  trim to 15 sessions → hand the *combined* frames to the unchanged harness;
  engines stay pure functions of the dataframes passed in — zero serialization of
  state, zero drift risk.
  **VALIDATE:** two metrics, both from data we now collect. (1) *Inertness:* on a
  warm-irrelevant day the diary output is byte-identical with and without the
  bookmark (existing diary artifacts are the fixture). (2) *Honesty gain:* the
  offline diary's TRENDING share converges toward the LIVE boxes' committed-label
  share on the same sessions — computable only because **N.1** puts regime_log on
  control. Agreement% (offline label vs live label, per tick bucket) is the
  number; today's known signature is offline under-reporting TRENDING, so the fix
  is proven when that gap closes without RANGING/COMPRESSION shares moving.

- `[DESK→DEPLOY]` **AK — 🔴 THREE OF FOUR TIMEFRAMES HAVE NEVER VOTED IN
  PRODUCTION, and the 07-16 fix that was supposed to solve this only half
  landed.** Found 2026-08-01 while sizing the replay's warm depth. Shipped in
  380a1bd; **bakes Mon Aug 3**.
  `trend_engine._analyze_single` bails to NEUTRAL below `EMA_SLOW + 5 = 55` bars.
  Measured against live fetch depths — `TIMEFRAMES[tf]["candles"]`:
  `1d=10  1h=50  15m=50  ->  NEUTRAL, DEAD      5m=100 -> the only frame that votes`
  v3.1's reweight on 07-16 diagnosed exactly this for 1d/1h and moved the
  direction weight onto **15m (0.30)** + 5m (0.35) — **but 15m fetches 50 bars
  too**, so 0.30 of the weight it moved TO was already dead on arrival. The
  symptom is a silent NEUTRAL, not an error, so nothing surfaced it for two weeks.
  **WHAT IT DOES TO THE GATE.** NEUTRAL frames still contribute half-weight to
  the denominator, so with only 5m voting `bull_score = 0.35c / 0.675 = 0.519c`
  against a 0.30 gate: **the 5m vote needs conviction > 0.579 or
  `overall_direction` is NEUTRAL — and NEUTRAL is a HARD VETO on TRENDING in
  `_trending`.** Below that line TRENDING is structurally zero and argmax must
  land elsewhere. Waking 15m in agreement drops the requirement to c > 0.381.
  **CONSEQUENCE WORTH TESTING, NOT ASSUMING: the iron condor has been absorbing
  the deficit.** It is the RANGING fallback (main.py:1049), so some share of its
  362 lifetime fires were ticks that were actually trending and could not be
  labelled that way — a mechanism for **AI**'s bleed that is not about strike
  geometry at all. Same for **AH**: ORB's 65%-of-fires-in-RANGING may be partly a
  labelling artifact, which would mean conditional_tables has been pooling trend
  ORBs and range ORBs under one label. Continuation and trend_credit_spread move
  most in fire count; sweep is untouched (SWEEP_REVERSAL does not read direction).
  **THE FIX, and why 150 rather than 60** (config **v4.1**, 15m 50 -> 150):
  clearing 55 wakes the vote but not usefully — the engine re-seeds the EMA on
  whatever tail it is handed, and measured against a fully-warm EMA-50 the error
  is **69% of a 0.30 bar at 55 bars, 49% at 60, 2.5% at 80, 0.3% at 150.** A
  confident vote on a number dominated by its seed is worse than an honest
  NEUTRAL. **Costs nothing in data:** candle_feed already prunes to
  `max(need,60)*4 = 240` 15m bars, so the history was there and only the fetch cap
  hid it.
  **1h DELIBERATELY LEFT ASLEEP — operator's call, 2026-08-01:** *"the markets
  respond more broadly to recent developments SINCE the close than they do to the
  previous session's range — which is a point of reference in my opinion, not
  necessarily a discriminator."* A live 1h vote in the morning is dominated by the
  PRIOR session and would oppose the opening drive, suppressing TRENDING in
  exactly the 09:30-10:40 window **A2.6** is studying. 15m carries more weight and
  has no such lag pathology.
  **WATCH ON THE FIRST BAKE:** TastyTrade's backfill reach is limited and the
  cutoff is unknown, so a cold store may not be served 150 at once. It accrues
  ~26 15m bars/session and the vote stays NEUTRAL until it fills — no worse than
  today. `trend_engine` **v3.3** reports the real per-box depth from the first RTH
  session (see AL for why that warning is throttled and RTH-gated). **Retreat
  value if the store turns out to be wiped often: 80**, which is 2.5% error and
  ~1 session of accrual.
- `[DESK→DEPLOY]` **AL — 🔴 THE BOT COULD BE BLIND AND NOBODY WOULD KNOW.
  Operator requirement, built and shipped the same day (380a1bd); bakes Mon Aug 3.**
  *"If any condition happens where the bot is blinded — whether it's the feed, or
  some other stale data, or the heartbeat, or anything else that is blinding it —
  we need a notification immediately that I need to take a look at it."*
  **THE HOLE.** `fetch_quote` was protected (it re-asserts bar age against
  `QUOTE_MAX_AGE_S`, so a delayed bar is rejected). `fetch_candles` was NOT: it
  gates on `_feed_alive()`, which reads a `__feed__/heartbeat` row — that proves
  the PRODUCER is running, not that the BARS are current. **A feed writing
  15-minute-stale bars has a perfectly fresh heartbeat**, so every engine reading
  5m/15m/1h frames would consume delayed data with no signal anywhere. Not
  sandbox-specific: any fault that keeps the writer alive while data lags (a
  DXLink subscription silently ceasing on one interval, a partial fault after a
  reconnect) produces it.
  **BUILT ON THE SYMPTOM, NOT A CAUSE LIST** — a cause list only ever covers the
  failures already thought of. `market_data` **v3.3** adds a bar-recency guard
  (3x the timeframe's own bar width, RTH only) and funnels all six blind paths
  through `record_blindness()`: `STORE_MISSING`, `HEARTBEAT_STALE`, `NO_BARS`,
  `ALL_NAN`, `EMPTY_SESSION`, `BARS_STALE`. `utils/blindness_latch.py` **v1.0**
  decides when to page (3 consecutive blind ticks AND >= 45s), `alert_manager`
  **v1.8** sends it, `main.py` wires `_check_blindness()` into the RTH tick loop.
  **The snapshot is captured at the FIRST blind tick, not when the latch trips** —
  a feed that reconnects mid-outage would otherwise report healthy fields
  alongside the alert, the worst possible forensic record.
  **COMPLEMENTS the existing bot/service-down notification rather than duplicating
  it:** that one fires when the bot STOPS; this fires when the bot KEEPS RUNNING
  on data it cannot trust. Process alive, service green, trading blind was the
  uncovered middle.
  **TELEGRAM IS AN EMERGENCY SERVICES CHANNEL** (operator's framing, now
  WORKING_AGREEMENT §17). Nothing routine goes there. Warnings and paging are
  RTH-gated while DETECTION and the record stay on, so callers that legitimately
  run outside the session still get a true answer — not fully dark, just not
  paging. The first cut of the starvation warning logged EVERY TICK and buried
  bot.log; it is now once per episode with a recovery notice, the same
  one-time-per-key idiom `candle_feed._log_backfill_depth()` uses.
  **DRILLABLE, because an alarm that has never fired is one nobody knows works.**
  `tests/blind_alert_selftest.py` walks the real path (recorder -> latch ->
  AlertManager -> Telegram) and asserts the things that rot silently: that it does
  NOT page early, pages exactly once, holds the first snapshot, and that recovery
  still carries duration and cause after the reset. **devtools 56** fans it to the
  fleet with a dry-run prompt. Every drill message is prefixed `DRILL — NOT REAL`,
  because a test that looks real IS a false alarm. Alerts also fire in PAPER
  (tagged `[PAPER]`, no manage-manually line) so the path is exercised daily
  before Aug 31. `tests/test_blindness_latch.py` — 10 tests.
  **⬜ OPEN DECISION, deliberately not taken: `OT_BLIND_REFUSE` ships OFF.** A
  stale frame is currently still SERVED with a warning. Refusing it would halt the
  tick loop on a false positive — a trading-behaviour change. For live cash the
  argument to turn it ON is strong (0DTE on 15-minute-old bars is worse than not
  trading), but decide it on a few sessions of observed `BARS_STALE` frequency,
  not before. **Revisit at the Aug 24 gate.**
- `[DESK]` **AM — REBUILD THE REPLAY CORPUS at `--warm-sessions 8`, and retire
  the numbers it supersedes.** Blocks **A2.6** and S's honesty-gain check.
  `devtools 46` -> answer **y** to *"Rebuild ALL dated tapes"* (it is not
  gap-fill-only; `--backfill --rebuild` re-scores every dated tape). Long job —
  **run it in tmux** (WORKING_AGREEMENT §16).
  **TWO CHANGES LAND AT ONCE and the result is not attributable to either alone:**
  v2.1 alters only the opening 24 ticks per symbol-session (~6.7% of the corpus,
  but ALL of it inside 09:30-09:55, exactly where the gap question lives), while
  v2.2's frame caps + warm 8 change the HTF depth for EVERY tick. Isolating them
  would cost a second full pass for a diagnostic we do not need — but it means
  **the 4.02% A2 violation rate and the 45%-in-the-10:00-hour concentration from
  v3.33 are SUPERSEDED and NOT comparable.** State the new baseline as new; do not
  diff it against the old one.
  **EXPECT NOISE ON THE FIRST PASS:** with 15m at 150 the corpus will log 15m
  starvation until the warm depth fills it — the same signal Monday's live boxes
  produce. That is the instrumentation working, not a fault.

- `[DESK]` **AP — THE DAILY FORK HAS NO DATA SOURCE, which also blocks the
  overlay's highest-value signal.** Split out of **AN** 2026-08-01 so a real
  blocker is not buried inside a resolved item.
  §4.2 wants a 1d fork at k=2 with R=40 recency. `TIMEFRAMES["1d"]["candles"] =
  10` — ten daily bars cannot yield a k=2 triple with 5-bar separation, let alone
  40 bars of recency. The HOURLY fork works today; the daily one is unbuildable.
  **CONSEQUENCE BEYOND THE MISSING FORK:** §6 names a daily rail within C*ATR of
  an hourly rail — CONFLUENCE — as the highest-value signal the overlay produces.
  With one fork there is nothing to confluence against, so the paper's headline
  application cannot be measured at PF.3 no matter how well the hourly fork works.
  **CANDIDATE SOURCE:** devtools 51 already fetches 21 days from yfinance, on an
  isolated feed. ~60 daily bars would comfortably serve k=2/R=40. Note this is a
  DIFFERENT feed from the DXLink store — worth confirming the two agree on daily
  OHLC before anchoring a persistent object on it.
  **NOT urgent for PF.3** (condor strikes are the first consumer and the hourly
  fork serves them), but it must land before §6 is claimed as a capability.

**⬜ Sun Aug 2**
- `[DESK]` **A2.4 — 🔴 A2's REAL CAUSE IS A HORIZON MISMATCH, and the state it
  flags may be TRADEABLE rather than defective. Read this before building A2.2.**
  Measured 2026-08-01 over 156,712 ticks / 15 sessions: **6,303 violations
  (4.02%)** — more than double the 1.7% a single session suggested.
  `VIOLATING  adx p50=45.8 mean=48.3   angle p50=6.8  mean=6.9`
  `clean      adx p50=29.6 mean=31.4   angle p50=11.8 mean=13.7`
  `adx direction on violators: falling 52% / rising 48%  <- LAG IS DEAD`
  `by hour: 09:454  10:2853  11:1197  12:721  13:284  14:307  15:487`
  **THE CAUSE — the two scores read different LOOKBACKS:**
  `RANGING angle: df1m["close"][-25:]      -> 25 bars of 1-MINUTE = 25 min`
  `TRENDING adx : primary_adx from 5m TF   -> ADX-14 x 5m         = 70 min`
  TRENDING asks *"was the last 70 minutes directional?"*; RANGING asks *"are the
  last 25 minutes flat?"* **Both can honestly be yes.** ADX 48 beside a 6.9°
  midline stops being paradoxical: the last hour-plus was directional, the last
  25 minutes are not. It also explains the 52/48 direction split (ADX is not
  decaying — its window still CONTAINS the drive) and the **45% concentration in
  the 10:00 hour** (the opening drive stays inside a 70-minute window until
  ~10:40 while the 25-minute angle flattens within minutes of it ending).
  **CONSEQUENCE FOR A2.2:** a shared axis only helps if computed on ONE horizon,
  which silently discards the other. Kaufman ER over 25 bars and over 70 minutes
  would disagree exactly as much as adx and angle do now. **The question is not
  "how do we couple them" but "which horizon should A2 be stated on" — or whether
  the invariant should be PER-HORIZON with cross-horizon disagreement expected
  rather than forbidden.** That is strikingly close to what the pitchfork paper
  already says about daily and hourly forks legitimately disagreeing (§7.3).
  **CHEAP DECISIVE TEST:** recompute the angle on a 70-minute window (or adx on a
  25-minute equivalent) and re-run `tests/a2_characterise.py`. If violations
  collapse, it is horizon and nothing else.
  **OPERATOR'S REFRAME (2026-08-01), and it may invert the whole item:** this
  state — impulse still in ADX, midline gone flat — is a *pause in a live trend*.
  A flag, a pennant, a pullback. It is a regularly-occurring, recognisable
  condition, not a defect. *"That should be something we bank on."* The system
  currently DESTROYS it: L1 scores both high, argmax picks one, and the fact that
  BOTH were true — which is the signal — never reaches a consumer. **A2 has been
  flagging the most informative tick class in the corpus as an error.**
- `[DESK→DEPLOY]` **A2.5 — `paused_trend` as a FACTOR COLUMN, not a strategy
  change.** Emit on every scored event: both TREND and RANGE > 0.5, plus the
  magnitudes. Same shape and freeze-safety as N.2's `rrr` and N.3's
  `closes_beyond`. Then `conditional_tables` answers what it is worth PER
  STRATEGY and any gate is placed at the fee-adjusted ROI crossing rather than
  from a story — the operator's own collect-wide doctrine, on infrastructure
  that shipped 07-31.
  **TESTABLE PRIOR, stated so it can be falsified:** continuation's **handoff**
  path fires on a runaway ORB then enters on a shallow pullback — which IS this
  state (ADX elevated from the runaway, angle flat during the pullback). Handoff
  made **+$1,333.50 / 56%**; standalone lost **$2,024 / 46%**. **If A2-violating
  ticks coincide with handoff entries and not standalone ones, this state is
  already earning money and nobody knew it was measurable.** Join them and see.
  Priors on the rest: continuation should love it, butterfly should love it
  (flat midline = pin conditions), **condor is genuinely ambiguous** — low
  realised vol against still-elevated IV is attractive, but a paused trend
  RESOLVES, and a condor sold into a coiled spring is short the resolution.
- `[DESK]` **A2.6 — ⬆️ PROMOTED 2026-08-01: BOTH TOOLS ARE BUILT, TESTED AND
  SHIPPED (380a1bd). Startable the moment AM rebuilds the corpus — no sessions
  to wait for.** Tag moved DESK·DATA -> DESK: the gap is backfillable, so the
  only remaining dependency is our own regen, not the calendar.
  `tests/gap_backfill.py` **v1.1** — computes gap_pct per (date,symbol) from
  `~/day_trader_pro/ohlc/<date>/`, writes `reports/gap_pct.json`. It classifies
  CONT/REV/FLAT against **the prior session's LAST 70 MINUTES**, not the whole
  session, because 70 min IS the ADX-14-on-5m window the boundary bar perturbs —
  whether the gap's DM reinforces or cancels depends on the accumulated DM in
  *that* window. `prior_dir_day` is emitted alongside so the choice can be
  checked rather than trusted. (v1.0 defaulted to a `data/OHLC` root that does
  not exist; `~/day_trader_pro/data/` holds only instance_map/mock_state/
  report.json and the harvest roots are its SIBLINGS.)
  `tests/a2_partition.py` **v1.0** — the 3x3 grid {OPEN 09:30-10:40, DECAY
  10:40-12:00, CLEAN 12:00-16:00} x {CONT, FLAT, REV}, reporting RATES with 95%
  half-widths and **refusing any verdict on a cell under n=500** (a2_characterise
  v1.0's lesson, asserted rather than remembered).
  **WHY A GRID AND NOT A TIME HISTOGRAM.** Three mechanisms produce A2's 10:00
  signature and time-of-day cannot separate them: **H1 horizon co-truth**
  (structural, all day, genuine), **H2 opening drive** (H1 with a morning
  density, genuine), **H3 gap artifact** (the impulse happened overnight, so a
  pause flagged from it has nothing to resume). MEASURED by ablation on a
  two-session fixture with the real trend_engine, only the boundary changed:
  `zero gap  ADX 46.4 @09:40 -> 16.3 @12:30`
  `gap WITH prior direction  52.0 -> 17.8   (inflated ~+17 at 10:30)`
  `gap COUNTER to prior dir  26.1 -> 14.9   (SUPPRESSED ~20 pts)`
  **A reversal gap DEPRESSES ADX. H1 and H2 can only ADD violations — neither
  can produce a rate BELOW the midday baseline.** That deficit is H3's unique
  fingerprint and is unfakeable by the other two. All three can light up at
  once; that is the expected answer, not a muddle.
  **PROVEN, not asserted:** `tests/test_a2_partition_recovers.py` plants four
  worlds (H1-only, H1+H2, all three, thin cells) and asserts the tool recovers
  each — including that a reversal deficit WITHOUT continuation inflation reads
  **ANOMALOUS**, not CONFIRMED, and that sub-floor cells yield REFUSED with no
  verdict anywhere in the output.
  **WHAT IT DECIDES.** CLEAN x FLAT is an uncontaminated sample of the paused-
  trend state — that is where **A2.5**'s forward edge gets evaluated per
  strategy, before any of it touches a gate. Hold open the outcome that the
  state is real, correctly identified, and still has no edge.
  *Original framing follows.*
- `[DESK]` **A2.6 — `gap_pct`: the overnight gap is never MEASURED, and
  unlike everything else this week it is fully BACKFILLABLE.** Operator's point,
  2026-08-01: *"the gaps you see overnight from previous close to current open
  are big and meaningful, and they have to be reflected somewhere."*
  **WHERE IT IS REFLECTED:** ATR does see it — `atr_series` uses proper true
  range with `prev_close = close.shift(1)` and 5m is CONTINUOUS, so the first 5m
  bar after the open carries `|high - prev_close|` and a large gap spikes ATR
  immediately. The 25-bar angle correctly never sees it (1m is session-scoped;
  a regression must not span a gap). HTF bars carry it too.
  **WHERE IT IS NOT:** nowhere is the gap MEASURED. No `gap_pct`, no `gap_size`,
  nothing conditions on it. It enters as an anonymous ATR spike that decays over
  14 periods, and the magnitude — the part that matters — is discarded.
  **WHY THIS IS THE CHEAPEST FACTOR ON THE BOARD:** prior session close and
  today's open are both already in `ohlc/<date>/` for every session. **Nothing
  needs collecting** — compute it retroactively across the whole corpus. Unlike
  `rrr`, `closes_beyond` or `paused_trend`, no session is lost by waiting.
  **THE HYPOTHESIS, aimed at the flagship:** does gap magnitude predict ORB
  outcome? An opening range forming AFTER a large repricing is a different animal
  from one forming after a flat open — the overnight move already happened, so
  the "breakout" may be continuation of something already spent. **AH** found ORB
  at **-0.24R with 65% of fires in RANGING** across 252 trades; if gap size
  separates the good ORB days from the bad, that is a conditioning variable with
  the sample already banked.
  **Also relates to the torque model:** a gap IS an impulse that occurred while
  the intraday frames were asleep. ADX picks it up ~5 minutes later; the angle
  never does. Likely part of why 45% of A2 violations land in the 10:00 hour.
- `[DESK·DATA]` **A2.1 — CHARACTERISE the A2 violations. Query, not a build. Do
  this before any fix; it can kill the whole plan.** A2 (TREND & RANGE not both
  >0.5) fails on ~196 of 11,299 ticks (1.7%). Dump those ticks with their `adx`
  and `angle` from the replay jsonl.
  **THE HYPOTHESIS TO KILL:** post-move consolidation, where ADX-14 has not yet
  decayed while the midline angle has already flattened. If that is what these
  ticks are, the overlap is a **lag artifact of the measurement** and no
  reformulation fixes it — the answer would be an ADX freshness term, not a
  shared axis. **Evidence pointing at it:** raising `--warm-sessions` 5 -> 15 made
  A2 WORSE (179 -> 196) while TRENDING dom% rose 30% -> 36%. Deeper history makes
  ADX more confidently high; the angle is computed independently, so overlap grew
  exactly as an uncoupled-ADX story predicts.
  **FOURTH HYPOTHESIS, added 2026-08-01 — do not skip it.** The pitchfork paper
  §7.3 notes daily and hourly forks can legitimately slope in OPPOSITE
  directions, which would make some violators genuine **cross-horizon
  disagreement** rather than a scoring defect. If so, A2.2's single-axis fix
  would ERASE that signal rather than repair it. Record whether violators cluster
  on symbols/times where a daily and an hourly fork would plausibly disagree —
  this needs **PF.1** to exist, which is part of why PF.1 starts now.
  **TOOL BUILT 2026-08-01 — just run it:** `python3 tests/a2_characterise.py`
  (options_trader_v3, read-only, auto-discovers the replay corpus, streams it).
  It separates the three stories and states which fix the data supports:
  **(1) ADX LAG** — violators carry HIGH adx that is mostly FALLING while the
  angle has flattened. Verdict: a shared axis papers over a MEASUREMENT problem;
  build an adx freshness/decay term and **do NOT build A2.2 as specified**.
  **(2) GENUINE CO-OCCURRENCE** — violations spread across many symbols.
  Verdict: A2.2's shared axis (Kaufman ER) is the right fix.
  **(3) MIXED/CONCENTRATED** — a few symbols carry most of them, pointing at
  cross-horizon or a symbol artefact, neither of which a single-axis
  reformulation should erase.
  The discriminator is **the DIRECTION of adx on violating ticks**, not its
  level: a decaying adx alongside a flattened angle is the post-move signature.
  Both branches verified against purpose-built fixtures.
  **VALIDATE:** the answer is a scatter of adx vs angle on violating ticks
  against the same on non-violating ticks. If violators cluster at high-adx AND
  low-angle with a recent-large-move signature, it is lag. If they are spread,
  it is genuine co-occurrence and A2.2 is the right fix.
- `[DESK]` **A2.2 — THE SHARED-AXIS FIX. Copy the structure that already makes A3
  pass, rather than inventing one.** 🔴 The root cause is now identified and it is
  structural, not a tuning problem:
  `_breakout:    expand_val       = ramp(atr_ratio, LO, HI)`
  `_compression: atr_contract_val = 1.0 - ramp(atr_ratio_c, LO, HI)`
  **ONE measurement, TWO ends, one inverted** — which is exactly why **A3 passes
  with ZERO violating ticks**. It is not luck; BREAKOUT and COMPRESSION are
  mathematically unable to both be high.
  Now the failing pair:
  `_trending: adx_s  = ramp(adx, adx_trend - 5, ADX_STRONG_SOLO)     <- ADX`
  `_ranging:  flat_s = ramp(FLAT_ANGLE_CUT_DEG - ang, 0, SOFT_DEG)   <- ANGLE`
  **TWO unrelated measurements.** ADX and midline angle are correlated in the
  market but NOTHING IN THE CODE COUPLES THEM, so both can be high on the same
  tick. That is the entirety of A2.
  **FIX:** give TREND/RANGE a shared inverted measurement in the same idiom.
  Leading candidate: **Kaufman's Efficiency Ratio** — net displacement / total
  path length, bounded [0,1]. It IS the trend-vs-chop spectrum as one number, so
  `trend_s = ramp(ER, ...)` and `flat_s = 1 - that` from the SAME ER. Small,
  matches existing style, provably reduces overlap.
  **VALIDATE:** A2 violating-tick count on the same tape, before and after, at
  identical --warm-sessions. Must fall sharply. Also confirm TRENDING dom% does
  NOT collapse — the fix must decouple, not suppress.
- `[DESK]` **A2.3 — THE LOG-ODDS REFORMULATION. The correct endpoint. HOLD UNTIL
  AFTER GO-LIVE (Aug 31).** Operator's instinct, and it is right: treat
  trend-vs-range as ONE latent axis in log-odds rather than two independent
  scores. Each factor contributes a log-likelihood ratio, evidence ADDS in
  log-odds space, then `TREND = sigmoid(L)` and `RANGE = sigmoid(-L) = 1 - TREND`.
  **A2 then becomes IMPOSSIBLE TO VIOLATE rather than tested for** — the
  invariant stops being an acceptance check and becomes a property of the
  construction. Same reasoning generalises: any mutually-exclusive pair belongs
  on one axis, and the current design only accidentally gets that right for
  breakout/compression.
  **WHY NOT NOW:** it is a rewrite of the regime scoring core four weeks before
  live capital. Every ramp bound, every acceptance check and the entire L1.11
  calibration track are fitted against the current formulation. Ship A2.2's
  targeted fix for go-live; take A2.3 in September with time to re-fit.
- `[DESK]` **L1.9 bookmark tester proof.** Run against copies of real `ohlc/<date>/`
  folders; prove byte-inert on the diary for warm-irrelevant days and prove the
  EOD conductor chain is untouched. The conductor is finally flawless — it stays
  that way.
  **HOW/VALIDATE:** as L1.9 above — inertness fixture + N.1 agreement metric;
  conductor untouched proven by a full dry-run of the chain on the tester with the
  bookmark grafted onto a *copy* of validate_regime.sh, diffing every artifact
  path it writes.
- `[DESK→DEPLOY]` **M.3 — Dedicated Telegram bot for options-trader notifications.** Promoted from
  nice-to-have to **go-live requirement**: live trading needs its own paging channel
  before Aug 31. Build today, live-test Thu Aug 27.
  **HOW:** new bot token; fleet-wide .env rotation via the existing
  `rotate_env_remote.sh` v1.3 machinery (adds missing vars); notify path reads the
  dedicated token with fallback to the shared one so a mis-rotation can never
  silence paging.
  **VALIDATE:** existing framework — devtools 36 (test Telegram) per box +
  forced-page drills on Aug 27 (trigger a half-complete-roll page and a
  phantom-P&L page in paper via induced conditions); the drill transcript is the
  evidence. Verify the fallback by removing the token on one box and confirming
  the page still lands on the shared channel.

**⬜ Mon Aug 3 — DEPLOY MONDAY 1 (fresh RTH rollout)**
- Deploy **E** (VWAP hard gate, default per the Aug 1 verdict) + **F** (MIN_RRR
  floor, same) + **T.2** (condor paper friction unification) + **N.2/N.3**
  (captures) to the fleet in one option-23 pass; verify canaries before restart.
  Fire-rate watch all session — these are the epoch's behavior changes, and the
  clean-baseline note resets here.
  **VALIDATE (the watch itself):** same-day fire-rate vs the trailing 2-week mean
  from `conditional_tables` (existing nightly artifact); gate-block dispositions
  visible in that night's harvested journal = the gates are alive; N.3 column
  populating on any sweep = capture alive.
- `[DESK·DATA]` **TC.4 (T+1wk) — readiness digest check.** `_trend_credit_spread` journal has
  been accumulating since 07-28; confirm fleet-wide capture is clean.
  **HOW/VALIDATE:** run `readiness_digest` over the harvested journal; per-symbol
  row counts > 0 on every traded box, impulse-SD distribution non-degenerate.
  Existing data; this IS the validation framework TC.4's bounds fit rides on.

**⬜ Tue Aug 4**
- `[DESK]` **L1.9 — Graft the proven bookmark onto `validate_regime.sh`**, then run
  `regime_backfill --rebuild` to re-score all dated diary rows warm. DONE = the
  diary reads TRENDING honestly on the days live boxes did.
  **HOW:** graft = the proven copy from Aug 2 replaces the live script (full-file,
  version-bumped); rebuild re-scores every dated folder with warm depth.
  **VALIDATE:** the N.1 agreement metric, now on the full archive: per session,
  offline TRENDING share vs live regime_log TRENDING share — DONE means the known
  under-report signature is gone on the days the live boxes trended (e.g. the
  07-17+ AVGO sessions), with chop days unchanged. Both series are on control;
  the check is a query.
- `[DESK·DATA]` **TC.4 — SD-bounds fit PR.** Run `readiness_digest`, fit
  aware/established/screaming SD bounds + room/extension bounds + corroborator
  weights from the observed distribution. Priors → calibrated knobs (env flips, no
  bake). The firing engine stays unbuilt — gated on the L1 excavation and the
  freeze, per the roadmap's three gates.
  **HOW:** fit bounds so tier occupancy matches design intent (screaming rare,
  aware common — target percentiles stated in the PR); add a **floor-durability
  table** to the digest: for every journaled impulse, did price close back through
  the impulse origin intra-session? (join readiness journal → banked OHLC — both
  already collected). That table is the first empirical test of the strategy's
  core premise ("committed order flow won't fully retrace") *before* any engine
  is built.
  **VALIDATE:** the digest + durability table are the framework; the transition-
  gap watch (3.0–4.5 ATR) gets its own row — share of arm-events landing in the
  danger band. All from the existing readiness journal + OHLC; no gap.

**⬜ Wed Aug 5**
- `[DESK]` **L1.CAL.2 — post-graft ramp re-read (verifies the L1.CAL correction
  before L1.11 fits anything).** L1.9 grafts the bookmark onto
  `validate_regime.sh` on Tue Aug 4 and re-scores the diary. The day after,
  re-run `python3 tests/ramp_calibration.py` over the rebuilt corpus and check
  ONE thing: **did `align_frac`'s distribution actually widen?** If p25/p50 lift
  off 0.67, the bookmark did its job and L1.11 can fit `align_val` on Aug 8–9
  against real spread. If they are still pinned at 0.67 with only the p95 tail
  reaching 1.00, the graft did not restore HTF depth and **L1.11 must fit the
  other terms and leave `align_val` alone** rather than fitting a compressed
  input and calling it calibrated.
  **TWO BIRDS:** L1.6's flat-angle sweep (16–26°) is already on this date and
  reads the same rebuilt diary — and `flat_s` is the term with the clearest fit
  (67.6% pegged, `lo=12` at input p52). Do them in one sitting; the L1.6 cut
  sweep and the `flat_s` ramp refit are the hard veto and the soft credit ramp
  of the same angle measurement, and fitting either without the other is how
  you end up with a veto and a ramp that disagree.
  **VALIDATE:** the pull_val rule — accept a bound only where the raw
  distribution spans the behaviour the factor measures. Angle does
  (p5 1.09° → p99 47.14°). `align_frac` currently does not.
- `[DESK]` **Historical ADX reconstruction.** Timestamp-join `regime_log` → trades to
  backfill `adx_at_entry` on pre-07-27 rows (deferred at the 07-24 fix; the warm
  rebuild makes it worth doing now). Offline, control-side.
  **HOW:** nearest-preceding-timestamp join per symbol, tolerance ≤ 60s, off the
  N.1-harvested regime_log archive (no ad-hoc box pulls); write back via an
  UPDATE tagged `source=reconstructed`.
  **VALIDATE:** free overlap check we already collect — rows since 07-27 carry
  BOTH the live-captured `adx_at_entry` and a reconstructable value; the
  reconstruction error distribution on that overlap qualifies (or disqualifies)
  the backfill. |err| p90 < 2 ADX points = trustworthy; worse = tag the backfilled
  rows excluded from calibration queries.
- `[DESK·DATA]` **L1.6 (first pass) — flat-angle sweep.** 16–26° against the rebuilt multi-day
  diary (07-14 → 08-04) with the rotating 30% holdout — never off one day. Output:
  the candidate frozen cut, staged for the Aug 10 deploy.
  **HOW:** sweep the cut over the warm-rebuilt diary, scoring each candidate on
  (a) A5 all-zero residual and (b) label agreement vs `session_labels.jsonl`
  (auto_label's price-action-only ground truth — independent by construction);
  fit on 70%, accept on the rotating 30%.
  **VALIDATE:** all inputs already collected (diary + labels + the
  flat-angle-by-label table `ramp_calibration.py` prints). Acceptance: residual
  falls from ~13% and RANGING agreement rises *on the holdout*; a cut that only
  wins on its fit set is unproven and the 20° default stands.

**⬜ Thu Aug 6**
- `[DESK]` **Level hierarchy + Overnight High/Low — build on the TESTER** (queued 07-24).
  Add `overnight_high`/`overnight_low` (extremes across the Asia+London span) to
  LiquidityMap as a named tier; replace the flat `is_named` bool with graded
  `level_strength` per the stated hierarchy: **ON H/L ≈ PDH/PDL (top) > historic
  multi-day S/R (mid) > individual session H/L > equal-H/L (lowest)**. Mapper logic
  touches what sweeps fire against — tester-first, no exceptions.
  **HOW:** graded `level_strength` float replaces `is_named` throughout the
  mapper (compat shim: `is_named = strength >= session-tier`); ON H/L computed at
  boot from **raw feed_store bars outside RTH** for the prior Asia+London span —
  pending N.6's verdict on whether those bars exist per symbol.
  **VALIDATE (forward-only — stated honestly):** no overnight tape exists
  historically, so the ON tier's *potency claim* (≈ PDH/PDL) cannot be
  retro-validated; it ships as a PRIOR and is judged forward by the existing
  `level_strength` trade capture → `conditional_tables` cells (win/expectancy by
  tier). Expect ON-tier n to be thin by Aug 18 — the tier's *rank* is revisable at
  the Sep 7 analysis day when n supports it. The hierarchy's non-ON tiers ARE
  retro-checkable from banked sweeps (level_strength captured since 07-24).
- `[FLEET]` **N.6 — NEW: extended-hours-bars audit (gates the ON H/L source).** Verified at
  HEAD that nothing asserts the feed_store contains non-RTH bars: candle_feed
  backfills by calendar start-times (so ETH bars for equities likely arrive from
  DXFeed), but `market_data` session-scopes 1m and the OHLC CSVs are RTH-only —
  the raw store is the only candidate source and it is unaudited. SPX cash has no
  overnight session at all.
  **HOW:** one read-only fleet query (option 14): count feed_store 1m rows outside
  09:30–16:00 ET for the prior night, per symbol.
  **VALIDATE:** the audit IS the decision data — ETH bars present → ON H/L
  computes from the store, no new collection; absent (or SPX-style cash symbols) →
  the ON tier degrades to PDH/PDL for those symbols by design, and if the tier is
  wanted fleet-wide a boot-time DXFeed ETH history pull gets scheduled as its own
  post-freeze item rather than silently shipping empty levels.
- `[DESK·DATA]` **Sweep level_strength — first look.** 07-27→08-06 sweeps bucketed by
  `level_strength` (the capture shipped 07-24). Observation checkpoint only; n is
  still small. No action.
  **VALIDATE:** existing capture + conditional_tables; checkpoint records n per
  bucket so Aug 18's power is known in advance.

**⬜ Fri Aug 7**
- `[DESK]` **Level hierarchy tester proof complete.** Inert where it should be; the
  postmortem buckets become meaningful only once the tiered value flows.
  **HOW/VALIDATE:** replay banked sessions through the tester mapper — every
  sweep that fired at HEAD still fires with the graded value, `is_named`-shim
  parity 100% (byte-inert on decisions, richer on capture). Fixture = the banked
  07-24→08-06 sweep set with recorded level_strength; the graded scorer must
  reproduce the recorded coarse values on the overlap.
- `[DESK·DATA]` **L1.7 Tier-B ledger check.** With the warm rebuild + three weeks of labels:
  which rows close? TRENDING should now be closable if any labeled trend day
  exists 07-14→08-07; SWEEP needs one mapper-confirmed named-zone reclaim;
  COMPRESSION needs a coil-into-pin session; BREAKOUT needs one more clean hold
  through the BB re-entry flicker. Close what the tape supports; the rest is
  calendar, not code.
  **HOW/VALIDATE:** pure evidence review over collected artifacts — warm diary ×
  auto_label labels; each Tier-B row's bar is stated in VALIDATION.md §2 and the
  diary prints the numbers. No new framework; the framework is why these close.
- `[DESK·DATA]` **G (data checkpoint).** Snapshot the `retest_depth` distribution (3 weeks
  accumulated). No decision yet — that's Aug 22.
  **VALIDATE:** existing `retest_check` journal events since 07-18; snapshot =
  histogram + n, so the Aug 22 decision knows its power.

**⬜ Sat Aug 8 – Sun Aug 9 (weekend calibration fit)**
- `[DESK·DATA]` **AF — refit continuation's strike-selection CONVICTION bounds
  (`OT_CONT_CONV_LO/HI`). Currently recorded only in the v3.18 changelog and
  scheduled nowhere.** v1.4 places the strike a fraction of the ATM-straddle
  expected move out, the fraction being a confluence of ADX and regime
  conviction. The ADX half is fine — ADX is mechanical and engine-independent.
  **The conviction half is not.** Its bounds (`CONV_LO=0.40 / CONV_HI=0.60`,
  from archive p25 0.396 / p90 0.587) were fitted against a conviction
  distribution that **changed on 2026-07-30**: L2.5 committed its first live
  label at ~09:55 that morning, and every conviction value before it came from
  the v1.3 fallback engine. So the strike distance is calibrated against an
  engine the fleet no longer runs.
  **HOW:** refit `CONV_LO/HI` from L2-engine conviction only —
  `WHERE engine='L2'` on `regime_log` (main v4.8 stamps it), which is exactly
  the filter W.1's quarantine defines. Do it in the same sitting as L1.11 and
  L2.4: same corpus, same question, and all three are meaningless if fitted on
  mixed-engine data.
  **VALIDATE:** compare the refitted bounds against the v1.4 values. A large
  move quantifies what the fallback-engine fit was worth; a small one says the
  two engines' conviction distributions overlap more than expected — itself
  worth knowing before the Aug 21 freeze.
  **DO NOT** refit before there are enough L2 sessions. Per the pull_val rule,
  accept a bound only where the raw distribution spans the behaviour the factor
  measures; at Aug 8 that is ~7 sessions of real L2 conviction. If it looks thin,
  say so and defer rather than fitting thin data and calling it calibrated.
- `[DESK·DATA]` **L2.4 — Fit the integrator priors offline.** θ_commit/θ_hold/δ_displace,
  dt_max/τ_stale, per-regime τ_up/τ_dn0/λ — recomputed from the labeled-tape
  bar-count distributions (the RANGING τ_up=780 template), judged on the churn
  metric, never P&L. This closes the L2.5-shipped-ahead-of-L2.4 inversion the
  roadmap flags as the priority.
  **HOW:** re-derive per-regime commitment-window bar counts from the warm diary ×
  labels (the τ_up=780 template generalized); tune on the replay harness's `l2`
  churn report (label switches vs L1 flips, emitted distribution, stale%) — the
  purpose-built framework that already exists.
  **VALIDATE:** offline — churn on the holdout sessions lands in the labeled
  bar-count windows; **live (post-Aug-10)** — the same churn metric computed from
  the N.1-harvested regime_log, nightly, against the offline prediction. A live
  churn that diverges from the offline fit within 3 sessions = the fit was
  overfit; the freeze-window clean/broken verdict cites this number.
- `[DESK]` **L1.CAL — ramp_calibration fixed, and the L1.9 dependency it exposed
  (NEW 2026-07-30).** First real use of `tests/ramp_calibration.py` produced two
  silent failures and one finding that reorders the calibration track.
  **Fixed as v1.2:** run as a direct script the tool could not import
  `analysis.regime_confluence` (tests/ on sys.path, not the repo root), fell to
  `_RC = None` without a word, and printed HARDCODED FALLBACK bounds as
  "CURRENT" — `room_s` reported lo=0.05/hi=0.20 when the live dials were
  0.17/1.00. It misreported the very constants it exists to calibrate. Repo root
  now on sys.path, and a failed import prints a banner stating the bounds column
  cannot be trusted. Also: `load()` held every record of every session (~300MB
  for a fortnight) and the 13-session auto-discover run died producing NO OUTPUT
  — now streams per line, keeping only sampled floats.
  **CORRECTED against the full corpus — I overstated this from one session.**
  The single-session read (11,295 ticks) showed `align_frac` p25 = p50 = p95 =
  0.67 and I called it a hard constant, concluding L1.11 could not fit
  `align_val` at all until L1.9 landed. **Across all 13 sessions (134,137 ticks)
  p95 = 1.00** — it does reach full alignment, in roughly the top 5% of ticks.
  So `align_val` is SEVERELY COMPRESSED, not structurally dead: its pegged-1.0
  rate is 43.0% with 57.0% graded. The L1.9 bookmark WIDENS that tail rather
  than being a precondition for the factor existing. regime_confluence line 86
  (*"align_frac never exceeds 0.67 in replay"*) is itself a single-window
  observation and should be re-read after the graft.
  **The schedule already handles the dependency** — L1.9 grafts Tue Aug 4,
  L1.11 fits Sat Aug 8–9. No reordering needed; what is needed is a
  VERIFICATION between them, dated below.
  **Full-corpus readings (13 sessions) supersede the single-day numbers:**
  `flat_s` pegs 67.6% — WORSE than the one-day 61.7%, and `lo=12` sits at input
  **p52**, so over half of all ticks already take full flat credit while angle
  spans p5 1.09° → p99 47.14°. Clearest fit on the board.
  `adx_s` pegs 37.6% (was 54.2% on one day) — less urgent than it looked; still
  DERIVED, still needs a hand fit.
  `room_s` 66.2% graded and `osc_s` 59.6% graded — **both healthy, both already
  re-fitted in the v1.3 pass.** They are the control cases proving the tool
  reports honestly and that a refit works.
  **VALIDATE:** re-run over the full corpus once streaming is deployed; a fit is
  only accepted where the raw distribution spans the behaviour the factor
  measures (the pull_val rule), which one session cannot establish.
- `[DESK·DATA]` **L1.11 — Fit the remaining ramps** (`flat_s` on its conditional population;
  `adx_s`/`align_val` from warm-bookmark or live `feed_store.db` depth — the L1.9
  gate is now open). Stage into the same calibration PR.
  **HOW:** `ramp_calibration.py` (existing) over the warm-rebuilt diary — the
  bookmark un-starves `align_frac` (its offline ceiling of 0.67 was the HTF
  signature); fit `flat_s` only on ticks past the flat veto (its true conditional
  population).
  **VALIDATE:** same convergence discipline L1.10 set — the fit must re-derive on
  independent session pools; saturation shares (the `room_s`/`osc_s` template:
  graded% up, p90 off the rail) are the acceptance numbers, printed by the
  existing tool. Watch the OSC_CROSS see-saw finding — COMPRESSION p90 is a
  guarded metric in the same report.
- **Epoch-1 exit review:** suite green ✅ · canaries current ✅ · chain + journal +
  regime_log harvest running ✅ · bookmark live ✅ · hierarchy proven ✅ · E/F live
  with a would-have-blocked ledger ✅ · N.2/N.3 fields populating ✅ · calibration
  PR staged ✅.

---

### EPOCH 2 — CALIBRATE & FREEZE — Mon Aug 10 → Sun Aug 23

*Goal: one consolidated calibration deploy Monday, then hands off L1/L2/entry
logic for two weeks. Everything else this epoch is offline or log-only — which the
roadmap explicitly permits during the freeze (L3.1/L3.2/P3 phase 1 drive nothing).*

**⬜ Mon Aug 10 — DEPLOY MONDAY 2 (the calibration deploy) — FREEZE WINDOW OPENS**
- Deploy in one pass: **level hierarchy + ON H/L** (mapper) · **L2.4 calibrated
  priors** · **L1.6 frozen flat-angle cut** · **L1.11 ramp fits**. Verify canaries,
  restart, watch the emitted distribution and label churn live.
- Declare the **L2.6 freeze-candidate window: Aug 10 → Aug 21.** No L1 truth, L2
  prior, or entry-logic deploy until Fri Aug 21 EOD. Anything discovered goes in
  this file with a post-freeze date.
  **VALIDATE (the watch):** nightly, from harvested artifacts only — regime_log
  churn vs the L2.4 offline prediction (N.1) · emitted-distribution shift vs the
  trailing diary · A5 residual on the nightly replay · fire-rate vs trailing mean
  in conditional_tables. Four numbers, all already landing on control; the freeze
  verdict on Aug 21 is written from them, not from impressions.

**⬜ Tue Aug 11**
- `[FLEET]` **L3.1 close-out.** Confirm `signal_journal` jsonl captures full fleet sessions;
  the harvest pull landed 07-27 (v0.5.0) — verify the conductor phase reports it
  and the manifest counts match boxes-run. Log-only; freeze-safe.
  **HOW/VALIDATE:** per-box event counts × session from the harvested jsonl;
  every traded box > 0 scored events, dispositions present for every fired trade
  (join journal → trades.db by symbol+timestamp, orphan count = 0). Existing data
  end-to-end.

**⬜ Wed Aug 12**
- `[DESK→DEPLOY]` **P3 phase 1 — index-context broadcast, log-only.** Control-side writer pushes
  SPX/QQQ regime+conviction via the existing `brief_flags.json` pattern; one
  journaled field on every `scored` event. `conditional_tables.py` grows the
  index-confluence dimension for free. Ungated, freeze-safe.
  **HOW:** control-side writer (5-min cadence, reads the two ALWAYS_ON boxes'
  regime_log tails via the existing ssh util) → per-box `~/brief_flags.json`
  merge; setup_scorer journals `index_regime`/`index_conviction`/`aligned` on
  every scored event.
  **VALIDATE:** the new field IS the validation framework it exists to feed —
  with-trend vs against-index cells in conditional_tables (Wilson intervals) are
  the evidence that decides if this ever graduates past log-only (post-L2.6 +
  a cell that earns it). Day-one check: field non-null on every journaled event
  of a session.

**⬜ Thu Aug 13**
- `[DESK]` **L3.2 — rejection ledger build starts.** `analysis/rejection_ledger.py` +
  `reports/rejection_summary_<date>.jsonl` + digest. Class (a) threshold near-miss
  consolidation from L3.1 events; prove the forward-outcome join leak-free on a
  known session (outcomes only from post-decision bars). Version-hash every row.
  **HOW:** consolidate `scored` below-B REJECTs, `disposition` rejects, N.2
  `gate_block:*`, and `retest_check` near-misses into one row schema
  {strategy, ts, failing gate/clause, score/conviction, forward outcome to
  would-be stop/target over N bars}; outcomes computed from banked OHLC strictly
  after the decision bar; every row tagged with the ruleset/version hash.
  **VALIDATE:** leak-freedom proven on a known session by shifting the decision
  timestamp +1 bar and confirming outcomes change accordingly (a leak-free join
  is sensitive to the boundary); coverage proven by reconciling ledger n against
  raw journal reject counts. All inputs already harvested nightly.

**⬜ Fri Aug 14**
- `[DESK·DATA]` **AJ.2 — THE DECISION: retire continuation's standalone path, or
  keep it?** Opened 2026-07-31 with a deliberate two-week wait. Baseline that day:
  handoff 50 trades / 56% / +$1,333.50 against standalone 49 / 46% / -$2,024.00.
  **WHY THE WAIT WAS DELIBERATE, not caution for its own sake:** `exit_engine`
  v4.10's BOS structural stop deployed Mon Aug 3, and standalone's losses
  concentrated in `max_loss_floor` — the exact hole BOS fills. Judging standalone
  on pre-BOS data would condemn it for an exit defect that has since been fixed.
  Everything before Aug 3 is a different strategy.
  **THE QUESTION TO ANSWER, in order:**
  (1) Post-Aug-3 only: is standalone still net-negative once its never-worked
      trades exit `bos_exit` instead of riding to the 25% floor? If BOS rescues
      it, the entry path was never the problem and this item closes as "keep".
  (2) Is standalone's loss one-sided by direction? On 07-31 TRENDING_BEAR ran
      22 trades / 32% / -$1,533.50 fleet-wide. If standalone owns most of that,
      the fix is a direction gate, not deletion.
  (3) **THE COST OF DELETION — quantify before cutting.** Handoff requires a
      prior runaway ORB (`orb.invalidation_reason == "runaway"`). On sessions
      with no runaway there is NO handoff, so retiring standalone means accepting
      zero continuation trades that day. Count zero-runaway sessions in the
      banked corpus first: if that is 1 day in 10 the cost is trivial, if it is
      4 in 10 it is not.
  (4) The confound from AJ still stands unless someone has broken it: handoff
      also runs a looser momentum gate (ACCELERATING **or** FLAT vs standalone's
      ACCELERATING-only). Two variables. A clean A/B needs one of the two mixed
      configurations, which does not exist in the data unless built.
  **DECIDE, do not defer again.** By Aug 14 there are ~9 post-BOS sessions; that
  is enough to act or to say explicitly what would change the answer.
- `[DESK·DATA]` **P5.3 — run `chain_reconstruction_check`** on ~3 weeks of archive. PASS → build
  ChainReplay (post-freeze); PARTIAL → grid restricted to the validated moneyness
  band, stated in the header; FAIL → the missing piece is named by the `+vega·ΔIV`
  column (IV-path model vs cadence) and gets a date before any harness work.
  **HOW/VALIDATE:** the tool IS the validator (built 07-23, proven on synthetic);
  its inside-spread rate, stratified by moneyness/hour/|ΔS|, is the verdict — and
  it only runs because P5.1/N.1's harvest landed Jul 30. Whatever the verdict, it
  is written into the ROADMAP P5 header the same day.
- `[DESK·DATA]` **N.4 — NEW: paper-fill realism audit (validates T.2 + the R slippage default,
  before any live fill exists).** The framework to test paper-fill honesty against
  reality was missing until the chain archive reached control; it exists now.
  **HOW:** offline control-side tool (conditional_tables idiom, stdlib): for every
  post-Aug-3 paper entry, look up the archived chain snapshot nearest the entry
  timestamp and compare booked fill vs NBBO — singles vs mark-inside-spread,
  condor credits vs achievable mid-at-limit; emit per-strategy booked-minus-
  achievable distributions.
  **VALIDATE:** the audit output is the evidence — if paper books systematically
  rich (beyond the 5-min snapshot tolerance P5.3 just quantified), T.2's
  unification and/or the 1% `OT_PAPER_SLIPPAGE_PCT` default get corrected with a
  measured number *before* go-live, and the Sep live fill-quality audit inherits
  the same comparison schema so paper-vs-live divergence is one diff.

**⬜ Sat Aug 15 – Sun Aug 16**
- `[DESK·DATA]` **L3.2 finish.** Class (b) coverage-gap scan (per strategy: was a live setup
  present during its target condition with no signal formed?); both classes
  populating across a fleet session. Pre-freeze rows tagged gap-finder grade;
  post-freeze rows will be calibration grade.
  **HOW:** class (b) scans banked OHLC + the nightly diary for each strategy's
  target condition (labeled range with no condor engagement, decisive break with
  no ORB armed, labeled trend with no continuation/TC.4 readiness) and asks the
  journal whether ANY signal formed in the window.
  **VALIDATE:** seeded-truth test — the SPX 07-28 rip is a KNOWN coverage gap
  (fell through every entry; documented in TC.4's origin); the scanner must find
  it unprompted. Finding the known gap = the scanner works; then fleet-wide.

**⬜ Mon Aug 17** *(no deploy — freeze holds)*
- `[DESK·DATA]` **K — re-arm decision, on paper.** Decide between the current deliberate
  hand-off-to-sweep and the unified rule ("re-arm on any invalidation before
  11:00; the origin gate decides whether a break is real" — the v3.5 origin gate
  makes runaway re-arm safe by construction). Write the decision here; any code is
  a post-freeze item (Aug 24 if changed).
  **HOW:** decide from a counterfactual count, not preference: tester run of
  orb_engine with re-arm enabled over the banked tape — how many second-break
  entries appear before 11:00, and what did the tape do to their stop/target?
  **VALIDATE:** banked OHLC + the real engine on the tester (existing harness
  pattern); the decision memo cites n, win share, and net R of the counterfactual
  entries. Thin n → keep the current handoff (rule 12: thin samples find
  mechanisms, not conclusions).
- `[DESK]` **I — butterfly cutoff branch decision.** `can_enter(is_butterfly=...)` is
  unreachable; either fix the `main.py` call site (if a 15:00 butterfly cutoff is
  ever wanted) or delete the branch so config and code stop disagreeing. Decision
  today; code post-freeze.
  **HOW/VALIDATE:** one query on collected trades — the butterfly entry-time
  distribution (trades.db). If no fill has ever wanted the 15:00 window, delete
  the branch (loose-code principle); if late entries exist and lost, wire the call
  site. Data decides a two-line decision.
- `[DESK·DATA]` **AA checkpoint.** Any two-sided condor with both legs near-simultaneous since
  07-17? Post-fix sample was 7 legs at last count. If clean through ~4 weeks,
  close AA as superseded-by-Y+rich-triggers; if recurred, it gets a forensic slot
  Aug 22.
  **HOW/VALIDATE:** the Z-cleaned rollups make this a one-liner — per condor pair,
  |leg entry gap| distribution; the 07-17 defect signature was gap = 0 min at
  identical underlying_entry. Existing data (and now date-clean).

**⬜ Tue Aug 18 — sweep evidence day (the decision the whole sweep track waits on)**
- `[DESK·DATA]` **E + F gate verdict — the single run.** `python3
  tests/gate_ledger.py` on control (day_trader_pro). Read-only; analyses journal
  + trades already harvested, gathers nothing, changes nothing. Both gates ship
  OFF, so the cost of waiting is only that they stay counters — their designed
  state.
  **FIRST READ ALREADY DONE — 2026-07-31, 10 sessions (07-20 → 07-31), 208
  scored events, 194 joined to a trade (93%). START FROM THIS, do not re-derive:**
  `E FIT   SweepReversal          n=27  net=+$1,781.18  wr=78%`
  `E FIT   ContinuationStrategy   n=8   net=-$  928.50  wr=25%`
  `E HOLDOUT (sweep only)         n=6   net=-$  140.58  wr=50%   THIN`
  `F everything                   n=0   (rrr coverage 0/208 — see below)`
  **NO FORMAL VERDICT** — the holdout is n=6 and contains no continuation at all.
  But the shape is unambiguous, and it matches the mechanism reasoned from the
  code BEFORE any data was read: **the trades E would refuse on sweep won 78% of
  the time and made $1,781.** That is the setup working as designed — a low sweep
  produces a LONG while price is still under VWAP, and sweep treats VWAP recovery
  as a confluence BONUS, not a requirement. Blocking them blocks sweep's thesis.
  Continuation points the other way (25%, -$928.50), which is E's premise
  holding, but n=8 is not a finding.
  **SO THE LEADING ANSWER IS THE THIRD BRANCH — EXEMPT SWEEP, then judge
  continuation on its own n.** Arrive expecting that and test it; do not reopen
  ship-or-abandon from zero.
  **WHY F HAS NOTHING:** `rrr` only began being journaled 2026-07-31 (N.2), so
  F's population is empty by construction until sessions accumulate. That is the
  whole reason this run is dated here.
  **SHIP-ON BAR: the HOLDOUT, not the fit.** The tool refuses a verdict below
  n=20 and prints THIN. A thin holdout is a legitimate "no verdict — carry
  forward", never a reason to ship on the fit.
  **F's floor of 1.3 is the genesis GUESS, not a fit.** If F has n by today, set
  it from the rrr-decile / outcome distribution. If not, say so and leave it.
  **A BUG THE FIRST RUN CAUGHT — keep the fix.** gate_ledger v1.0 counted
  ORBStrategy in the blocked population; ORB was +$3,343 of a +$4,196 total,
  dominating a verdict for trades the gate can never refuse (it short-circuits to
  `_grade_orb`). v1.1 excludes it. Any future gate: check its exempt set before
  trusting a ledger number.
- `[DESK·DATA]` **Level-conviction lead:** win-rate/expectancy by `level_strength` bucket at
  ~3 weeks of current-engine data. If equal-H/L sweeps are the losers → a
  level_strength floor on the sweep gate is confirmed.
  **VALIDATE:** existing capture (07-24) × conditional_tables cells with Wilson
  intervals; the Aug 6 checkpoint already told us the per-bucket n, so today's
  verdict is stated with its power, not just its point estimate.
- `[DESK·DATA]` **Reclaim looseness:** do losing sweeps carry higher `closes_beyond` than
  winners? If yes → require `closes_beyond == 0` post-reclaim (or hold-N-candles).
  **VALIDATE:** **N.3's exact per-trade capture** (live since Aug 3, ~2 weeks) +
  the replay-reconstructed values for older trades on the overlap. This question
  was unanswerable from collected data before N.3 — that was the point of N.3.
- `[DESK·DATA]` **Exit asymmetry / washout fingerprint:** does 75%-win/negative-net hold on the
  current engine? Stop-width vs winners' realized magnitude; washout-day regime
  tags.
  **VALIDATE:** existing MFE/MAE telemetry (max/min_premium_seen) + excursion
  reports + the adx/flat-angle/conviction entry context — all on every trade row
  since 07-24. Stop-width question = MAE distribution of winners vs the −40%
  trigger; giveback = MFE-vs-booked.
- Output: the exact list of sweep changes that are **evidence-confirmed** for the
  Aug 24 deploy. Anything unconfirmed stays OBSERVING — do not fix what the data
  hasn't convicted.

**⬜ Wed Aug 19**
- `[DESK→DEPLOY]` **Build the confirmed sweep changes on the TESTER** (level_strength floor and/or
  reclaim tightening and/or stop tightening — only what Aug 18 convicted). Mapper/
  strategy logic → tester-first, deploy Mon Aug 24.
  **HOW:** each convicted change behind its own env knob (`OT_SWEEP_LS_FLOOR`,
  `OT_SWEEP_MAX_CLOSES_BEYOND`, …) so rollback is a config flip.
  **VALIDATE:** tester replay over the banked sweep set — the change must block
  exactly the population Aug 18 convicted (row-level reconciliation, not
  aggregate), and nothing else. Post-deploy, the L3.2 ledger's `gate_block` rows
  carry forward outcomes on everything newly blocked — the standing live
  validator for every gate this file ships.

**⬜ Thu Aug 20**
- `[DESK]` **L3.3 — gate matrix behind a flag, built + tester.** `fires iff regime ∈
  permissive AND C ≥ bar(trade_type)` in dispatch; provisional bars ORB/sweep
  ~0.40, condor ~0.65, butterfly ~0.70; flag-off byte-identical to today. Deploys
  Mon Aug 24, paper.
  **HOW:** the permissive×bar table in dispatch behind `OT_GATE_MATRIX`; flag-off
  path proven byte-identical by replaying a banked session through both and
  diffing decisions.
  **VALIDATE:** conviction is on every trade row and every journaled signal
  (existing since 07-24/07-18), so the matrix's effect is fully auditable:
  flag-on paper week → blocked set enumerated in the L3.2 ledger with forward
  outcomes; bars judged on L3.4's marginal-expectancy curve (conditional_tables,
  holdout enforced Aug 22) on BOTH precision and recall axes.
- `[DESK→DEPLOY]` **N.5 — NEW: fill-latency telemetry (the TC.2 stop-trigger dataset — must exist
  before the live week that is supposed to produce it).** Verified at HEAD:
  FillResult carries confirmation but **no submit→fill timing**, and trades.db has
  no latency columns — yet Sep 1–4's plan says "ladder fill-latency logged" and
  TC.2's stop-trigger decision (−40% vs 35%/25%) is explicitly "calibrate against
  measured ladder fill-latency." Without this, the live week produces no such
  dataset.
  **HOW:** FillResult + trade row gain `submit_ts`, `fill_ts`, `ladder_steps`,
  `escalated` (v-obs pattern, auto-migrated columns); populated by
  order_confirm/exit ladder on both paper and live paths. Log-only telemetry —
  not entry logic, freeze-untouched — deploys with the Aug 24 pass so it has a
  paper week of burn-in before it must be trusted live.
  **VALIDATE:** paper week = plumbing proof (latency ≈ ladder cadence by
  construction); live week = the real dataset. TC.2's trigger decision then reads
  latency-cost per exit (mark at trigger vs realized fill) from collected rows.

**⬜ Fri Aug 21 — FREEZE DECLARED (EOD)**
- **L2.6 ✅ if the window ran clean** (no L1/L2/entry deploys since Aug 10, churn
  nominal). This is the real gate for everything downstream — pitchfork, P1/P2/P4
  conviction dimensions, ChainReplay, TC.4 firing engine all key off this date.
  If the window broke, the clock restarts and every date below slides by the same
  amount: say so here, don't pretend.
  **VALIDATE:** the four nightly watch numbers (Aug 10 entry) over 10 sessions —
  churn within the L2.4 offline envelope, distribution stable, A5 nominal,
  fire-rate unbroken. The freeze declaration quotes them.
- Epoch-2 exit review; `conditional_tables.py` begins pooling post-freeze rows
  (the only rows that are decision-grade).

**⬜ Sat Aug 22 – Sun Aug 23**

- `[DESK]` **AO — 🔴 `find_swing_highs/lows` USES FLOAT EQUALITY, so equal highs
  emit EVERY tied bar as a pivot.** Found 2026-08-01 during PF.1.
  `utils/math_utils.py` tests `prices[i] == max(window)`. On a plateau every bar
  in it is marked a pivot. Reproduction in
  `tests/test_pitchfork_construct.py::test_shared_helper_emits_duplicate_pivots_on_a_plateau`.
  **WHY IT IS NOT FIXED YET, and this is a scheduling call rather than a judgement
  that it does not matter:** the helper feeds `StructureAnalyzer._find_swings` ->
  `structure_sequence` -> a HARD VETO in `regime_confluence._trending` and the A4
  invariant. Changing it changes what gets traded, three weeks before go-live and
  inside the L2.6 behavioural freeze.
  **WHAT IT MAY BE DOING TODAY:** duplicate pivots inflate swing counts, which
  feeds `_find_sr_levels` and `_classify_sequence`. Whether that has been
  distorting HH/HL/LH/LL classification is UNMEASURED — measure it on the
  rebuilt corpus (**AM**) before deciding the fix's shape.
  **POST-FREEZE (after Aug 21).** Do not fold it into an unrelated deploy.

- `[DESK·DATA]` **G — decision.** Feed `retest_depth` into `orb_quality` or drop it: 5 weeks of
  distribution + the Phase-3 ROI buckets now exist to answer it. Decide from the
  data; the measurement gates nothing until then.
  **HOW/VALIDATE:** join `retest_check`/`retest_depth_px` (journal, since 07-18)
  to ORB outcomes (trades.db) by symbol+timestamp; bucket outcome by depth in ATR
  units. Monotone edge with n per bucket ≥ the min-n bar → feed into the A/B
  grade; flat → drop the field from scoring (keep the capture). The join is the
  framework and both sides are already collected.
- `[DESK]` **L3.5 — enforce the holdout in the bucketer.** Fit sessions ≠ acceptance
  sessions inside `conditional_tables.py`; slippage-haircut P&L only. The Aug 31
  descent bars come from held-out cells or they don't come.
  **HOW:** session-hash split inside the tool (deterministic, seeded), every
  emitted cell labeled fit/holdout; N.4's measured slippage replaces the flat
  haircut if it landed.
  **VALIDATE:** self-demonstrating — the tool's own report shows the same cell on
  both splits; a cell that collapses on holdout is the guard working.
- `[FLEET]` **Live shakedown prep:** broker account funded · `configure.sh` mode-switch
  dry-run (defect-Q archive machinery fires, `trades_<mode>_<stamp>.db` lands) ·
  tiny-size live config staged (1-contract sizing, SPX + QQQ only) · **J
  (disposition):** the 07-23 header audit restored title/changelog sync; accept
  the v3.0-era legibility loss as historical, keep `check_versions.sh` as the
  deploy-truth tool, and close J as WONTFIX-by-policy unless someone objects here.
  **VALIDATE:** each prep step has an artifact (archived DB filename, staged
  config diff, funding confirmation in the runbook) — the Aug 28 go/no-go
  checklist consumes artifacts, not recollections.

---

### EPOCH 3 — GATES ON & GO LIVE — Mon Aug 24 → Fri Sep 4

**⬜ Mon Aug 24 — DEPLOY MONDAY 3 (fresh RTH rollout)**
- Deploy: **L3.3 gate matrix** (flag on, paper, bars provisional/wide) + the
  **Aug-18-confirmed sweep changes** + **N.5 latency telemetry** + any K/I code
  decided Aug 17. Fire-rate watch all week. **L3.4 campaign formally starts** on
  post-freeze data and runs underneath everything from here on.
  **VALIDATE:** same four nightly watch numbers + the L3.2 ledger now populating
  gate-matrix blocks with forward outcomes.

**⬜ Tue Aug 25**
- `[FLEET]` **Mode-isolation live-switch rehearsal on ONE box.** Switch paper→live→paper;
  verify defect-Q end-to-end: archives created, mode-scoped queries return zero
  cross-mode rows, no paper row visible to the live loop, breaker reads only live
  P&L.
  **HOW/VALIDATE:** scripted rehearsal with assertions, not eyeballs — after each
  switch: archived DB exists with the mode+stamp name; `realized_pnl_today()` and
  `get_open_trades()` return only current-mode rows (seed one paper row first so
  the negative case is actually exercised); breaker state re-derives clean.
  Existing machinery under test; the seeded-row check is the addition.

**⬜ Wed Aug 26**
- `[DESK]` **Entry/exit path shakedown vs the resolved audit (N/O/P).** Re-run
  `test_entry_fill_confirmation`, `test_roll_is_real`, `test_mode_isolation` at
  HEAD; walk the order_confirm deadlines, cancel-and-walk-away, partial booking,
  and paging paths against the tiny-account config on paper.
  **VALIDATE:** the suite + a forced-partial drill (limit far from mark on the
  tiny account's paper twin so the bounded poll and partial-stash paths actually
  execute); N.5 columns populate during the drill — proving the latency capture
  before it matters.

**⬜ Thu Aug 27**
- `[FLEET]` **M.3 — Telegram bot live test** (built Aug 2): pages route to the dedicated
  options-trader channel; half-complete-roll and phantom-P&L pages verified.
  **VALIDATE:** the Aug 2 drill plan executed — induced half-complete roll page,
  induced phantom-P&L page, fallback-channel test. Transcript archived in the
  runbook.
- `[DESK]` **M.1/M.2 — Windows residue documented.** Ghost folder on tarball extraction +
  `setup_ec2.bat` security warning: fix if trivial, else document the workaround
  in the deploy README and close as documented-known.
  **HOW/VALIDATE:** one clean-Windows extraction attempt decides trivial-vs-not;
  either way the deploy README carries the outcome. Self-contained.

**⬜ Fri Aug 28 — GO/NO-GO REVIEW**
- Gate checklist, every box or no-go: suite green at HEAD · canaries pass fleet-
  wide · freeze intact since Aug 10 · gate matrix behaving across 4 paper
  sessions · mode-isolation rehearsal clean · fill-confirmation shakedown clean ·
  paging live · live config staged (1 contract, SPX+QQQ, bars one bucket above the
  paper crossing per L3.6).
  **VALIDATE:** every checklist line points at an artifact produced above — this
  review reads evidence, it does not generate it.

**⬜ Sat Aug 29 – Sun Aug 30**
- Live-day runbook written (who watches what, the raise-back trigger, the
  kill-switch: `OT_REGIME_ENGINE=v13` rollback path re-verified, configure.sh
  back-to-paper path re-verified). Final rehearsal.
  **VALIDATE:** both rollback paths *executed* on the rehearsal box, not read.

**⬜ Mon Aug 31 — GO LIVE, RTH (tiny size)** 🎯
- `[FLEET]` **L3.6 descent, step 0:** live, minimum size, SPX + QQQ, bars one bucket above
  the paper crossing. This is the tiny-account live shakedown that has gated the
  fill-confirmation work since 07-15 — now with the whole scrub list behind it.

**⬜ Tue Sep 1 – Fri Sep 4 — LIVE, first week of September** ✅
- Daily: fill-quality audit (live fill vs mark, per the 07-15 divergence-audit
  template — now sharing N.4's comparison schema so paper-vs-live divergence is
  one diff) · phantom-P&L reconcile check at each close · ladder fill-latency
  read from the **N.5 columns** (this is the TC.2 stop-trigger dataset — the −40%
  trigger vs 35%/25% question gets answered by these numbers, not by guessing).
- `[DESK·DATA]` **Fri Sep 4:** week-1 live review — divergence report, latency distribution,
  descent decision drafted.
  **VALIDATE:** all three daily checks read collected rows (trades.db + N.5 +
  broker_reconcile records + chain archive); nothing in the review depends on a
  measurement that wasn't scheduled above.

---

### RAMP — Mon Sep 7 → Fri Sep 18

**⬜ Mon Sep 7 — Labor Day, markets closed.** Analysis day: first live-week
conditional tables; confirm the newly-admitted buckets' realized expectancy;
revisit the ON-tier rank with whatever n exists; finalize the descent decision.

**⬜ Tue Sep 8 — descend one notch.** Half size and/or widen the symbol set —
only if week 1 was clean. Raise-back trigger stays armed: first negative read on
a newly-admitted bucket → back up a notch, no debate.
  **VALIDATE:** "clean" is defined by the Sep 4 review's three artifacts; the
  raise-back trigger reads held-out conditional-table cells (L3.5), never the
  fit set.

**⬜ Wed Sep 9 – Fri Sep 11 — hold the notch.** Watch, don't touch.

**⬜ Mon Sep 14 — FULL POSITION SIZES, RTH** 🎯 — mid-September, contingent on two
clean live weeks. The L3.4 campaign keeps placing final bars underneath; a bar
that the marginal-expectancy data moves, moves.

**⬜ Tue Sep 15 – Fri Sep 18 — full-size steady state** + close-out review of this
file: everything above either ✅ or explicitly re-dated below.

---

## PART 2 — DEFERRED PAST THE WINDOW (kept, dated, gated — not forgotten)

- **⬜ L3.7 — wire live + delete UNKNOWN from the enum + recalibration cadence.**
  After the bars are placed (late Sep). Grep status.py/query.py/alerts before the
  enum change; the data-fault no-trade stays forever.
  **VALIDATE (when due):** the grep sweep is the framework; the recalibration
  cadence consumes the same nightly tables/ledger pipeline built above.
- **⬜ TC.1 — gamma-led strike selection** and **⬜ TC.2 — exit-mechanism bake-off
  (BoS vs trail vs 5-min FVG, counterfactual on identical entries)** — the
  construction season opens against the frozen L3 baseline (late Sep). TC.2's
  observability precursor (log FVG zones + BoS swing points on the trade at entry)
  is log-only and may be scheduled into any free pre-freeze slot if capacity
  appears — same capture pattern as the ADX/level-strength/N.3 additions. TC.2's
  *latency* input is covered: **N.5 ships Aug 24** and the live week banks it.
  TC.1's substrate is the chain archive (secured Jul 30) + ChainReplay (P5.4).
- **⬜ TC.4 — `vertical_spread_strategy.py` firing engine.** Three gates unchanged:
  calibrated bounds (PR lands Aug 4, with the floor-durability table as the
  premise test) + honest-TRENDING L1 excavation (validated via the N.1 agreement
  metric) + the freeze. Earliest sensible build: September, canary on one box,
  paper.
- **⬜ P1 — consume the chain archive dynamically** (offline report ~Aug 10+ when
  2 weeks of archive exist; any live dimension weight-0, post-L2.6). Substrate
  secured by the Jul 30 harvest verification.
- **⬜ P2 — shadow observer stage 2 scorers** (observe-only; graduation post-L2.6).
  Stage-1 validation data (shadow jsonl vs data/OHLC) already banking fleet-wide.
- **⬜ P4 — HTF zone memory + rejection counts** (rides the tester fork,
  post-L2.6). Rejection-count validation consumes the same level_strength/sweep
  capture lineage started 07-24.
- **⬜ PITCHFORK — SPLIT INTO FOUR PHASES 2026-08-01. Only the LAST needs L2.6.**
  The whole overlay had been gated behind Aug 21, which meant construction would
  start **ten days before live capital** and the condor — which **AI** names the
  fork as the instrument to fix — would stay broken through go-live. Full
  reasoning in `docs/WHITEPAPER_pitchfork_overlay.md` §13.
  **PF.1 CONSTRUCT — startable NOW.** Geometry engine in a git fork:
  deterministic anchors, three variants in parallel, rails as
  `anchor + slope*(t - anchor_time)`. Consumed by nothing, gates nothing,
  weight 0. **The freeze does not apply** — L2.6 protects L1/L2/entry BEHAVIOUR,
  and an object nothing reads cannot alter behaviour.
  **PF.2 FIT — after Aug 5.** §4.4's confirmation-lag rule made replay validation
  depend on **defect S**, the HTF bookmark. That is now evidenced, not assumed:
  `--warm-sessions` 5 → 15 moved TRENDING dom% **30% → 36%** and TRENDING_BEAR
  p90 **0.439 → 0.65** on identical tape. Starts once L1.CAL.2 confirms it on the
  rebuilt corpus.
  **PF.3 MEASURE — ~Aug 10, CONDOR STRIKES ONLY.** QQQ twin, weight 0, against
  the chain archive (needs ~2 weeks of it). Condor first because a **credit is
  one number**, directly comparable on identical tape, no attribution problem.
  **Resist every other consumer until this one has a number** — §12 names
  consumer sprawl as a headline risk and this project has already paid for it.
  **PF.4 WIRE — post-L2.6 (Aug 21) earliest, realistically September.** Anything
  that changes what gets traded. **v4.0 tags at TWO proven consumers**, not when
  the overlay exists.
  **THE REPLACEMENT MAP — current constants, so the head-to-head is concrete:**
  `#1 condor strikes  bb_upper/lower OR 0.80*EM (farther), guardrail 1.2*EM,`
  `                   trigger 0.65    ->  sell at/outside UML / LML`
  `#7 stops           MAX_LOSS_PCT=0.40 of premium  ->  beyond a rail`
  `#10 exhaustion     ATR-extension from bb_middle (20-SMA 5m,`
  `                   exit_engine:1428)  ->  distance beyond UML / channel width`
  `#9 trailing        FVG trails, HORIZONTAL  ->  slopes with the ML`
  `#15 compression    BB_WIDTH_COMPRESSION_PCT=0.20, RANGE_ROOM_LO/HI=0.17/1.00`
  `                   ->  |UML-LML|, structural width that does not lag a 20-bar BB`
  `#11 condor roll    "tested" premium-derived  ->  price reached that side's rail`
  `#4 ORB grade       liquidity-in-path only  ->  retest occurring AT a rail`
  **STALE TARGET CORRECTED IN THE PAPER:** application **#2** cited
  `CONTINUATION_MIDLINE_ATR = 0.35 * ATR` around `bb_middle`. The 07-28
  `v-fvg-pullback` rewrite removed that trigger; the constant is now an ORPHAN
  referenced only in comments describing its own removal
  (`continuation_strategy.py:10,157`). The application is not dead, but it has no
  current baseline to measure against and must be re-derived. **General lesson
  now written into §7:** the paper enumerates 17 consumers against a codebase
  that moves weekly — **re-read §7 against HEAD before fixing any consumer
  order**, or the head-to-head has nothing on the other side.
  **A2 LINKAGE — §13.5, and it argues for building EARLY.** §7.3 notes daily and
  hourly forks can legitimately slope in OPPOSITE directions, which may give the
  A2 residual a **structural** explanation rather than a statistical one. If some
  of the ~196 violating ticks are genuine cross-horizon disagreement, A2.2's
  single-axis reformulation would **erase** that signal rather than fix it.
  A2.1's characterisation should record whether violators cluster where a daily
  and an hourly fork would plausibly disagree — **which cannot be checked until
  PF.1 exists.**
- **⬜ P5.4/P5.5 — ChainReplay + exit replay** (post-L2.6, scope set by the Aug 14
  validator verdict; holdout discipline per L3.5).

---

## PART 3 — RESOLVED REGISTER (condensed; kept so fixes don't get quietly reverted)

*Full forensic text: git history of this file at the pre-v2.0 commit, plus
`docs/HISTORY.md` and the audits. Resolution date + fixing versions + the why.*

- **AN ✅ 2026-08-01 — PF.1 CONSTRUCT BUILT, and the white paper's §4.1 was
  wrong about its own foundation.** `analysis/pitchfork.py` v1.0 +
  `tests/test_pitchfork_construct.py` (24 tests). Weight 0, consumed by nothing —
  outside L2.6 exactly as §13.1 argues. Deterministic anchors, three variants in
  parallel, rails as `origin + slope*(bars from origin)`, confirmation lag
  enforced structurally (`born_idx` is computed, never supplied, and the
  bar-by-bar replay test asserts no fork appears before it).
  §4.1 claimed LiquidityMapper already computes swing pivots. **It does not** — it
  computes equal-high/low PRICE CLUSTERS, sweeps and named session levels. The
  real fractal is `utils.math_utils.find_swing_highs/lows`, consumed by
  StructureAnalyzer. **The paper is corrected in place with the superseded text
  left visible.** The fork owns its own pivot definition so anchor evolution never
  becomes a diff against the live trading path, and so it can be deleted if the
  overlay does not earn its keep; `pivots_shared()` logs both sets during shadow
  so PF.3 can attribute a credit win to geometry rather than to better pivots.
  §3.2's Modified Schiff default is now MEASURED — andrews +0.70/bar puts its
  median at 119.80 against a ~108 close, modified_schiff +0.26/bar at 111.53.
  Slope is per BAR, not per second, because charts compress non-trading time.
  Spawned **AO** (float-equality defect in the shared helper, post-freeze) and
  **AP** (the daily fork has no 1d source, which blocks §6 confluence).
- **AE ✅ 2026-07-31 — RESOLVED, and the item's premise was WRONG.**
  `futures_trader_v1` does **not** ship `push.sh` — it has no push script at all
  (verified against a fresh clone). So there was no hole of the kind AE
  described. The repo was also already **clean**: 0 undefined names across 63
  tracked files.
  **The underlying concern was still valid**, so the portable half shipped:
  `tests/test_no_undefined_names.py` ported over, plus pyflakes in
  requirements.txt. **It is MORE load-bearing there than here** — options_trader_v3
  runs this gate in two places (suite + push.sh) and futures_trader_v1 has only
  the suite, so there is no second net. Verified: passes clean on the repo as-is,
  and fails with file and line on a deliberately reintroduced orphan.
  **Note for whoever resumes that project:** the gate exists now but nothing
  enforces running it — no push.sh means no chokepoint. If a deploy script is
  ever added there, the pyflakes gate belongs in it (see AB).
- **candle_feed RTH gate ✅ 2026-08-01 (v3.9) — 29 boxes no longer sit on
  DXFeed with no session to serve.** The feed had **no time gate at all** —
  `Restart=always`, no timer, no clock check in the reconnect loop — so while a
  box was up it held a DXLink socket continuously. Invisible on a normal day
  (phase_report stops the instances at EOD, so nothing runs), but every
  MAINTENANCE wake put all 29 back on the wire for work that needs no market
  data. Now sleeps outside RTH holding **zero subscriptions**.
  **WHY THIS LOOKED RISKY AND IS NOT.** Greeks/Quote for the option chain ride
  this SAME socket (v3.1's "one producer, many readers"), so idling the loop also
  stops draining `chain_marks` — and `chain_snapshot` is what P5.3 and N.4 both
  depend on. Resolved by reading rather than assuming:
  `chain_snapshot.snapshot()` takes the chain as an **argument** and is called
  from inside main.py's tick loop, which **already returns early on
  `not is_rth()`** (main.py:1268). Archival therefore only ever happens during
  RTH. The gate cannot cost a snapshot. **The bot has had this exact
  sleep-and-continue since it was written; the feed simply never got it** — the
  same asymmetry as condor Leg 1 vs Leg 2.
  **WARM LEAD-IN, not a hard 09:30.** `fetch_candles` refuses on a stale
  heartbeat, so a feed connecting exactly at the open serves nothing for its
  first cycles. Connects `OT_FEED_WARM_LEAD_S` early — default **1200s (20 min)**,
  which covers the 09:15 fleet wake. Verified across the clock: idle at 03:00 /
  08:00 / 09:05, **CONNECT (warm lead-in)** from 09:10, **CONNECT (in RTH)**
  09:35–15:59, idle again from 16:05.
  **BOTH EDGES, because the point is that a forgotten box is not a problem.**
  The top-of-loop gate only decides whether to CONNECT — on its own the feed
  would stream past 16:00 for as long as the box stayed up, which is exactly the
  evening-maintenance case this exists for. A second check rides the EXISTING
  flush cadence (no new timer, no new mechanism — we are already in that block
  once per cycle) and breaks the socket when the session ends, returning to the
  outer gate which then sleeps. Buffered bars are flushed immediately before the
  break, so nothing is lost.
  **Operator's framing, recorded because it is the general rule:** *"I would like
  to be able to forget that I left them up and it not be a problem."* Same
  principle as the conductor rule — anything that depends on someone remembering
  will eventually not happen.
  **Full cycle verified:** idle 17:00 / 21:00 / 06:00 / 09:05 -> CONNECT 09:12
  (warm lead) -> streaming 09:31–15:58 -> **DISCONNECT 16:01** -> idle 16:30 /
  19:00. Both edges, one day-night cycle.
  **TUNABLE both ways:** `OT_FEED_WARM_LEAD_S=0` makes the gate exact-open; a
  very large value restores the old always-on behaviour without a code change.
- **D ✅ 2026-07-31 — shadow-observer.service templatized (shadow_devtools v1.3),
  closing the last half of defect D.** The unit hardcoded
  `/home/ubuntu/options-trader` in both `WorkingDirectory` and `ExecStart`, so it
  pointed at the canonical path from ANY checkout — a silent no-op on the fleet
  (which uses that path) and a **broken observer anywhere else**, including the
  tester. That is the same shape as defect D's first half, which the v1.2 script
  fixed for itself but not for the unit it manages.
  **HOW:** template now carries `__INSTALL_DIR__`; new **option 11** substitutes
  `$REPO` at install time, mirroring `setup_ec2.sh`'s `${INSTALL_DIR}` pattern
  for optionsbot.service. **Refuses to arm the unit if the placeholder survives
  substitution** — a half-written unit is worse than none, and this is the class
  of failure that shows up as "the service is running" while pointing somewhere
  wrong. Verified at a non-standard path (`/opt/tester/options-trader`), and the
  refusal path verified against an unsubstituted template.
  **FLEET IMPACT: ZERO** — canonical path matches, so nothing changes until the
  unit is reinstalled. Prove with option 14:
  `systemctl cat shadow-observer | grep WorkingDirectory` — all 29 identical
  before and after.
- **E + F tester proof ✅ 2026-07-31 — done the night it was scheduled for,
  ahead of the operator travelling Saturday.** Built `tests/gate_ledger.py`
  (day_trader_pro, read-only) and ran it: 10 sessions, 208 scored events, **194
  joined to a trade (93%)** — the ts_et join works, which was the main
  uncertainty. Verdict and numbers recorded on the **Aug 18** item, which is now
  the single decision point rather than a fresh analysis. Headline: the trades E
  would refuse on SweepReversal won **78%** and made **+$1,781.18** (n=27), so
  the leading answer is exempt-sweep, not ship-or-abandon. F is empty by
  construction (rrr journaled only from 07-31).
- **F ✅ 2026-07-31 — MIN_RRR floor wired (setup_scorer v1.6), SHIPS OFF, ORB
  counter-only.** Same shape as E and the same kind of measured premise: a setup
  with **rrr = 1.00 scores 0.84 and grades A**. A 1:1 risk-reward trade is
  currently a top-grade fire, because the 5-dimension scorer has no RRR input at
  all — it was never one of the dimensions.
  **ORB IS COUNTER-ONLY, NEVER BLOCKED — and that is a design decision, not
  timidity.** The ORB's RRR is structural: stop = range boundary, target =
  measured move. A narrow opening range mechanically produces a low ratio
  without the setup being any worse. Gating the only strategy currently earning
  (10 trades / 80% / +$4,385.50 on 07-31) on a ratio it does not control, with
  zero evidence that low-rrr ORBs actually lose, is exactly the category-3 move
  the house rules forbid. It logs `RRR floor COUNTER (ORB never blocked)` and
  trades anyway. If the Aug 1 ledger shows low-rrr ORBs are net-negative, THEN
  gating it becomes a decision with evidence behind it.
  **rrr of None is INERT.** A signal with no planned stop or target has an
  UNKNOWN ratio, not a bad one; treating it as 0.0 would veto every such signal.
  Verified: no-stop signal passes with the flag ON.
  **Ships DEFAULT OFF** (`OT_MIN_RRR_ACTIVE=0`), floor `OT_MIN_RRR` default 1.3.
  **That 1.3 is the genesis value and is explicitly a PRIOR, not a fit** — the
  Aug 1 ledger sets it from the rrr-decile / outcome distribution that N.2's
  journaling now makes computable. Do not defend 1.3; it was a guess in the
  original config and remains one until fitted.
  **Reuses `_journal._rrr`** rather than re-deriving, so the gate can never
  disagree with its own audit trail.
- **E ✅ 2026-07-31 — VWAP hard gate wired (setup_scorer v1.5), SHIPS OFF.**
  The premise is now measured, not argued: a `ContinuationStrategy` long with
  price **BELOW** VWAP scores **0.73 and grades B** — it fires. `vwap_alignment`
  contributes 0.11 against a 0.55 bar, so misalignment could never veto no matter
  how wrong the side was. The gate makes it a block.
  **PLACED AFTER SCORING, deliberately.** The journal records what the blocked
  setup WOULD have graded (`GATE_BLOCK_VWAP(B)`), which is exactly what the
  retro ledger needs to answer "did this gate block winners?". Blocking earlier
  would save microseconds and destroy the evidence.
  **DEFAULT OFF** (`OT_VWAP_FILTER_ACTIVE=0`) — log-only counter until blocked
  trades are shown net-negative on collected data. House rule: evidence decides.
  **Three deliberate no-fires:** ORB is exempt BY CONSTRUCTION (short-circuits to
  `_grade_orb` before this path — defect V for free, verified: ORB long below
  VWAP with the gate ON still passes grade A); `price_vs_vwap == "NONE"` is
  inert, because VWAP UNDEFINED is not VWAP misaligned (the 07-17 SPX
  zero-volume case, where every index setup would otherwise be vetoed by an
  unmeasurable condition); `direction == "neutral"` has no VWAP side to be on.
  **Also closes N.2's second half:** `_journal_gate_block()` emits
  `gate_block:vwap` dispositions. Without it a gate vetoes invisibly and could
  never be calibrated from its own rejections.
  **A REAL BUG THIS SURFACED — `VWAP_FILTER_ACTIVE` was declared TWICE.** The
  genesis block (config.py:518) had `VWAP_FILTER_ACTIVE = True  # UNWIRED`
  sitting as a hardcoded True that nothing read; a new definition added higher in
  the file was silently overridden by it, since the later assignment wins. The
  gate would have shipped **ON** — the opposite of what this item specifies.
  Caught by a test asserting the default was False when it read True. Now one
  definition only, wired in place, env-tunable. `MIN_RRR` sat in the same block
  with the same problem and is now wired for F.
- **AD ✅ 2026-07-31 — CONTINUATION TRADED. First trades since it was written.**
  v1.4's strike selection works on a real chain, not just a modelled one.
  Fleet-wide **99 trades, 52% WR, -$690.50**, on a day the fleet netted +$3,581
  across 116. Real strikes and fills (CVX C 195, ORCL C 129/132/133). The
  `no strike: no expected move` failure signature did NOT appear.
  **The finding worth more than the P&L — the two entry paths diverge:**
  `trend_continuation_handoff     50 trades  56% WR  +$1,333.50`
  `trend_continuation_standalone  49 trades  47% WR  -$2,024.00`
  Balanced N, opposite signs, split along a DESIGNED boundary. Carried as **AJ**.
  By regime the same session: TRENDING_BULL 75/63%/+$3,440.50 against
  TRENDING_BEAR 22/32%/-$1,533.50 — long-biased, hurt on the short side.
  **METHOD NOTE:** the first read was ORCL alone — 3 trades, 0% WR, -$1,341 —
  and the assistant called it a problem with the strategy. The fleet said 52%
  and roughly flat. Three trades on one symbol is not a result; the operator
  called that correctly.
- **AG.2 ✅ 2026-07-31 — the compression HOLD works.** `COMPCANCEL=0` on both CVX
  and ORCL, against three cancels on CVX alone the day before. A plan survived,
  fired **Leg 1 as a put credit spread**, and carried to `hard_close_15:45`.
  `ABAND=0` follows from that — it did not need abandoning because it entered.
  **Consequence for AI:** the `approach call NN%` figure still has not been
  observed, since no plan has yet reached the cutoff un-filled. AI keeps waiting
  on it, but the urgency drops — a condor DID fire, so the trigger geometry is
  not categorically unreachable. Fleet condor for the day: 6 trades, 33%, -$25.50.
- **AC ✅ 2026-07-31 — the three silent declines now speak.** Of 26 `return None`
  paths in `strategy/`, most are regime-mismatch gates that are correctly silent.
  These three could refuse a QUALIFYING setup and say nothing:
  `butterfly_strategy.find_strike` (v3.4) — no liquid contract, killing a fly
  that had ALREADY cleared the GEX-pin and regime gates. Butterfly has 27
  lifetime trades against sweep's 985; this line shows whether any of that
  scarcity is chain liquidity rather than gate strictness.
  `condor_roll` (v1.1) — no mark for the untested vertical. The most
  consequential: it declines a roll on a LIVE position with one side tested, and
  the roll IS the risk-reduction step. Now names the missing leg.
  `iron_condor_strategy._pick_short` (v-declineloud) — nothing clears the
  0.80*EM/BB dual floor. **This one had already cost a wrong conclusion:** on
  07-30 `grep -c "no liquid strike"` returned 0 across all history and was read
  as "the dual floor never rejects" when it meant "rejects in silence".
  No behaviour change — a setup declined today is still declined, it just says so.
- **N.2 + N.3 ✅ 2026-07-31 — factor columns that cannot be backfilled.**
  `signal_ctx` (signal_journal v1.1) now carries **`rrr`** on every scored,
  disposition and readiness event — reward:risk from the underlying levels,
  returning **None rather than 0.0** when levels are absent, because "no stop"
  and "worst possible trade" must stay distinguishable in any distribution built
  from this. Without it, item F's MIN_RRR floor would veto INVISIBLY: no record
  of what the rrr was on the trades it blocked, so the floor could never be
  calibrated from its own rejections.
  **N.3:** sweep signals carry **`closes_beyond`** and `sweep_age_bars` at ENTRY.
  The liquidity mapper has computed closes_beyond since v1.3 and shadow/registry
  gates on it, but it never reached a trade row. It is the cleanest
  sweep-vs-breakout discriminator available: a level swept and RECLAIMED is a
  sweep; a level closed beyond repeatedly is a breakout wearing a sweep's
  clothes. Captured at entry because the bar window has moved on by exit.
  Both log-only and freeze-safe. **Deploy Mon Aug 3** with E and F.
- **AG ✅ 2026-07-30 — condor cancelled itself on a COMPRESSION flip; Leg 1 now
  HOLDS.** Diagnosed by reading CVX's bot.log directly after three rounds of
  `grep -c` produced two confident wrong answers. Three plans in one session,
  each killed ~19 minutes in by a flip to COMPRESSION, none reaching the cutoff —
  which is also why `NEVER1=0` looked like "no abandonment" when it actually
  meant "the plan never lived long enough to reach that branch". Shipped as
  `v-holdcompression`: only TRENDING_BULL/TRENDING_BEAR/BREAKOUT_VOLATILE cancel
  an un-filled plan; COMPRESSION, SWEEP_REVERSAL and UNKNOWN HOLD, mirroring the
  pause-and-hold Leg 2 has had since v3.2. Verified across all six regimes.
  Shipped WITH `v-selfdiag` (see below) because a longer-lived plan is only
  useful if it reports what happened to it.
  **Live verification is open as AG.2.**
- **v-selfdiag ✅ 2026-07-30 — an abandoned condor plan now reports WHY.** The
  cutoff line carries the excursion toward each trigger as a percentage, the
  high-water marks, and expected move at plan time vs at abandonment. That last
  figure exists because holding through compression means waiting to sell into
  CONTRACTING premium, and strikes are validated against EM exactly once, at plan
  time, then never re-checked — a short at 1.0x EM becomes 1.25x EM if EM decays
  20%, which would fail the 1.2x guardrail if planned fresh. The tension is real
  and is now measured rather than argued.
  **A bug the test caught and reasoning did not:** the first cut put the HOLD
  branch above the cutoff check, so a plan held through COMPRESSION returned
  early every tick and would have sat alive to end of session — producing exactly
  the silence the change exists to remove. Cutoff now sits above the regime block.
- **AB ✅ 2026-07-30 — the deploy gate could not see undefined names.** The
  box-side gate is `python -c "import ast"` (working agreement, after repeated
  wrong-venv/no-pytest burns). `ast.parse` proves a file COMPILES — an undefined
  name compiles fine and raises at RUNTIME — so the deploy path was structurally
  blind to the class that cost two sessions in two days: continuation `mid`
  (07-29; all 15 boxes took zero trades until 10:05, whole ORB window) and
  butterfly `_mult` (07-30; IWM crash-looped an hour, regime-gated so 14 boxes
  ran it clean). Closed in three parts — `tests/test_no_undefined_names.py`
  (suite gate, zero tolerance, deliberate-failure tested and it catches `mid`
  too); **push.sh v1.8** running pyflakes before the commit and REFUSING on any
  hit, with a missing pyflakes also a refusal rather than a skip; and
  **install_tooling.sh** + push.sh v1.9 so a checkout provisions its own
  dependencies with or without a controller — needed because the gate's hard
  dependency was never installed on the control checkout, which no script has
  ever provisioned. A second undefined name in main.py (a quoted forward
  reference, no runtime risk) was fixed with a TYPE_CHECKING import so the gate
  runs at zero tolerance instead of carrying an exception list.
  **Remaining half is open as AE:** futures_trader_v1 ships the same push.sh.
- **W.0 / W.2 / V / T.2 ✅ 2026-07-30 — Thursday's four, with two found already
  shipped.** W.0: main v4.7 deployed fleet-wide, and L2.5 committed its first
  production label at ~09:55 ET after the designed 25-bar warm-up — the first in
  the project's history. W.2: `tests/swallow_audit.py` — 139 swallowing handlers
  in options_trader_v3 (81 silent) and 48 in day_trader_pro (42 silent), tiered
  by consequence so the ~20 that sit in risk/orders/record paths are separable
  from the guarded imports and date parsers that are correctly silent; `--json`
  emits a stable snapshot, and conductor phase 10 now diffs it nightly. V:
  push.sh v1.7, all three resolution paths tested against a scratch $HOME with
  two bot-shaped directories. T.2: the unification shipped in main v4.1 back on
  07-22 — only the documentation was missing, now in MECHANICS with the reason
  recorded so it is not re-litigated (a mid limit is a reasonable expectation;
  the residual is no-fill risk, and no-fill risk cannot be modelled as a price
  haircut).
  **Pattern worth carrying: this is the FOURTH time this week the backlog
  trailed the repo** — T.1, T.3 and U on Wednesday, T.2 today. Every item's
  premise gets re-verified at HEAD on the day it is worked, never trusted from
  this file. It cost nothing on any of the four only because the check happened
  first.
- **X ✅ 2026-07-29 — the morning wake picked the same 13 discretionary names
  every day: the report it ranks on was FROZEN AT 2026-07-06.** Filed and solved
  the same evening. The brief regenerates correctly every morning at 09:15 and
  writes `~/market-brief/report.json`; `orchestrator._load_and_select()` reads
  `config.DATA_DIR/report.json`, a different file, last written **2026-07-06
  10:40 UTC** — 23 days stale. Cause: `report/emit.py` resolves its destination
  as explicit `path=` → `$DTP_REPORT_JSON` → `os.getcwd()/report.json`, and
  `DTP_REPORT_JSON` is set NOWHERE — the variable exists only inside emit.py's
  own docstring instructing that it be set. Emit therefore took the cwd fallback
  from day one.
  **Every symptom follows from that one stale file:** the frozen report has no
  `move_ranked` key (that sidecar shipped in emit v1.3.0 on 2026-07-15, after
  the file was written), so selector's first `ranked` pass yields nothing and the
  whole ranking falls through to the frozen composite `scores` — identical every
  morning, hence the identical cohort. `strength_by_sym` ends up empty, so line
  178's `strength_by_sym.get(s, 0.3)` defaults for every name, which is the
  `str +0.30` printed against all 13 in the wake message. Proof from 07-29: the
  brief's own top picks were discarded — LLY (#1, score +0.77) ranked **#18** and
  missed the cutoff, ORCL (#4) **#19**, UNH (#2) did not place at all.
  **The quiet one:** `brief_strength` feeds the bot's Stage-3 setup nudge, so the
  brief's signed sentiment has been a hardcoded 0.30 constant for every name
  every day. The sentiment pipeline is fully wired and has never influenced a
  single setup — only the wake list, and that from a three-week-old file.
  Diagnosis only; the fix lands as **Y** after Thu Jul 30's close, deliberately
  not stacked on L2.5's first live session. Investigation cost one directory
  scan and four one-line reads — no replay, no new tooling.
- **T.1 ✅ 2026-07-22 (registered 2026-07-29) — red suite at HEAD.** Fixed in
  the defect-T pass: `test_paper_entries_mirror_live_friction` replaced by
  `test_paper_entries_book_the_mark_by_default` +
  `test_paper_friction_knob_applies_to_every_path` (docstring item 14 — uniform
  friction, knob-not-hardcode). Verified 2026-07-29 on a fresh clone: **37/37
  green**. The v3.0 VALIDATE spot-join (paper `entry_price` == journal `scored`
  mark on singles) remains available as an optional live cross-check any day.
- **T.3 ✅ 2026-07-22 (registered 2026-07-29) — dead import.**
  position_manager **v3.9** removed the `PAPER_FILL_SLIPPAGE_PCT` import with a
  changelog entry; verified at HEAD 2026-07-29 — the only remaining grep hit in
  the file is that changelog prose. Import block clean.
- **U ✅ 2026-07-29 — canary refresh + parity invariant.** The fingerprint gap
  was closed 07-22 as check_versions **v3.1** ("audit defect U", 16 canaries)
  and extended v3.2→v4.2 to **125 checks** — every item in U's list confirmed
  present (orb v3.9 `_rearm`/`bars_since_break`, sweep v3.2, main v4.x,
  regime_confluence bounds VALUE-pinned, limit_ladder, `FLATTEN_WINDOW_OPEN_ET`,
  status v1.13). The missing piece shipped as **v4.3** (2026-07-29): PARITY
  INVARIANT section — `git rev-parse HEAD` vs `git ls-remote origin HEAD`, RED
  on mismatch (catches "internally consistent but old", the one staleness no
  fingerprint can see), WARN when origin unreachable or tracked files dirty —
  plus a failure-count DONE banner (exit code unchanged; callers safe).
  Deliberate-failure test passed: token deletion → 2 MISSING, locally-committed
  divergence → PARITY RED, banner "3 FAILURE(S)"; green at clean HEAD.
- **A ✅ 2026-07-12 — Two Layer-1 implementations.** `conviction_integrator` v2.0
  deleted `EvidenceAdapter`; `RegimeConfluenceScorer` is the sole L1. No
  circularity.
- **B ✅ 2026-07-12 — Layer 2 ported in-repo.** Integrator v2.0, always-argmax
  emission, UNKNOWN deleted from emission, STALE survives; hysteresis kept.
- **C ✅ 2026-07-13 — REPLAY_VALIDATION false premise.** Observer scores off the
  same DXFeed tape as the CSVs (no yfinance anywhere). Calibrate on CSVs for
  **sampling**, not source. v1.1.
- **D ✅ 2026-07-13/18 — Shadow observer extracted** to repo-root `shadow/`;
  tarballs deleted; `shadow_devtools.sh` v1.1 self-locates. Lessons kept: web-UI
  uploads can't set the exec bit; `.gitignore` needs runtime-data rules.
  *(Service-unit half → scheduled Fri Jul 31.)*
- **G 🔄 2026-07-18 — near-miss retest measured, not gated.** `orb_engine` v3.7
  logs `retest_check` depth in PX, ATR-relative offline, never percentages.
  *(Feed-or-drop decision → Aug 22.)*
- **H ✅ 2026-07-13 — two "no entry after" times.** `ORB_NO_ENTRY_AFTER_ET` (11:00,
  ORB-scoped) vs `GLOBAL_NO_ENTRY_ET` (14:00, global) — renamed so the two rules
  can never be conflated again; values asserted at runtime.
- **L ✅ 2026-07-13 — dead `fix_structure_analyzer.sh` deleted.**
- **N ✅ 2026-07-15 — exits booked on submission.** FillResult contract + live
  fill-confirmation + phantom-P&L recovery (exit_engine v3.4/v3.5, main/
  broker_reconcile/trade_logger v3.6).
- **O ✅ 2026-07-15 — live entries booked on submission.** All three entry paths
  record only broker-confirmed fills via `order_confirm` (main v3.7, entry_engine
  v3.7; butterfly signed-debit + double-position race closed). Tests 1–14.
- **P ✅ 2026-07-15 — broken-wing roll opened a fictional vertical.** condor_roll
  v3.7: real signed-credit order, fill-confirmed, half-complete pages.
- **Q ✅ 2026-07-15 — mode isolation.** trade_logger v3.7 mode-scoped queries +
  configure.sh v2.0 DB archiving on every mode switch. *(Re-rehearsed live
  Aug 25.)*
- **R ✅ 2026-07-15, ⚠️ partially superseded 07-22** — paper slippage knob;
  mark-limit policy split it. *(Unified via T.2 → Mon Aug 3; realism-audited via
  N.4 → Aug 14.)*
- **V ✅ 2026-07-22 — ORB was scored, not gated.** `setup_scorer` v1.4
  `_grade_orb`: a confirmed ORB always trades; liquidity downgrades A→B, never
  vetoes; regime/VWAP/macro removed from the ORB grade. *(This is why gate E
  exempts the ORB.)*
- **U ✅ (header half) 2026-07-23 — full-repo header audit** re-synced every title
  to its newest changelog entry; check_versions v3.7 records the sweep.
  *(Canary half → Wed Jul 29.)*
- **X ✅ 2026-07-23 — condor legs round-tripped +25%→−25%.** exit_engine v4.1
  ratchet (+20%→BE, +40%→lock +20%) + time-gated TP@25% only after the entry
  cutoff and only with no open sibling (a pre-cutoff TP structurally prevents the
  condor from forming); risk_manager v3.2 full-budget verticals; iron_condor v3.2
  leg-2 pause.
- **Y ✅ 2026-07-23 — condor window opened before BB was computable.** Window
  11:00→11:11; `current_price` fallback removed.
- **Obs ✅ 2026-07-24 — trade record missing regime context.** `adx_at_entry`,
  `regime_conviction`, `flat_angle_deg` on every entry path, live 07-27.
  *(Historical backfill → Wed Aug 5, validated on the post-07-27 overlap.)*
- **Obs ✅ 2026-07-24 — sweep confirmation is real, not anticipatory** —
  hard-gated on `sweep.confirmed`; the loose reclaim inside it is scheduled
  (Aug 18/19, armed by N.3), the confirmation architecture itself is correct.
- **Obs ✅ 2026-07-24 (late) — tape/regime washout fingerprint CONFIRMED-NEGATIVE.**
  Flat-angle/trend/chop do not separate good from washout sweep days (all cluster
  26–29°); the discriminator lives in WHAT the sweep reached for — which is
  exactly the level_strength track scheduled Aug 18. Lesson kept: read logged
  angle from replay jsonl, never reconstruct from candles.

---

*Rules carried forward from v1.0/v2.0: nothing enters without evidence and a
stated sample size; deferred means deferred; resolved items are kept, not
deleted; when an OBSERVING item earns action it gets a date in PART 1, not a
silent fix. Added at v3.0: no fix ships without a VALIDATE clause pointing at
data that exists — or at the dated N-item that creates it first.*


---

### Moved out of the schedule 2026-07-30 — resolved, no longer open work
*These sat in PART 1 carrying ✅. PART 1 is now OPEN ITEMS ONLY.*
*LETTERS ARE REUSED IN THIS FILE: the `V` and `Y` below are the 2026-07-29/30 items
(push.sh target resolution; the report-wiring fix). They are NOT the older
`V ✅ 2026-07-22` (ORB scored, not gated) or `Y ✅ 2026-07-23` (condor window opened
before BB was computable) recorded above. Worth knowing before reading either.*

- **W — ✅ superseded by W.0: the L2.5 restoration (fix built 2026-07-29, awaiting
  the post-close window).** Two defects from the 07-29 incident, one already
  hotfixed on the fleet (continuation v1.3.1 `mid` NameError, `dd0d097`) and
  one still live at the time of writing: **every box is running the v1.3
  classifier, not the L2.5 conviction integrator.**
  **DIAGNOSIS (this is not what the handoff assumed).** `RANGE_WINDOW_BARS` has
  never been defined in `conviction_integrator`. It is owned by
  `regime_confluence` (v1.3, ~line 181, value 25). `conviction_integrator`
  re-exports a tuple of six *regime-label* constants from regime_confluence and
  nothing else; `main.py:275` imported `RANGE_WINDOW_BARS` *through* it, so the
  import only ever worked while that name sat in the re-export list. The 07-28
  excavation (`92c89d7`) trimmed the tuple. The resulting ImportError was
  swallowed by main.py's `except Exception` L2 guard, which downgraded a hard
  contract break to one WARNING per process start.
  **THE REAL DEFECT is the guard, not the import.** The import is a one-line
  fix. What let it cost a full session of calibration data is that the failure
  mode was *silent and non-fatal*: trading continued normally, so nothing in
  P&L, status, or alerts looked wrong. Same shape as the `mid` NameError the
  same morning — a fault that unit tests could not reach because nothing
  asserted the contract that production actually depends on.
  **HOW (built, tested, not yet deployed):** `main.py` **v4.5** imports both
  symbols from the modules that OWN them (a re-export is never a contract) and
  the fallback now logs at ERROR *and* pages via
  `alert_manager` **v1.7** `send_regime_engine_degraded_alert` — the pager is
  itself wrapped so it can never take a box down. `check_versions` **v4.5**
  adds 3 presence canaries + 1 absence canary on the broken import form, and
  fixes a defect in its own v4.3 banner (the regime_confluence ABSENCE loop
  printed ✗ STALE without incrementing MISS, so a restored fabricated fallback
  would still have reported ALL CANARIES GREEN). New
  `tests/test_l2_import_contract.py` (5 assertions) enforces the general rule:
  symbols import from their definer, `conviction_integrator` must NOT re-export
  `RANGE_WINDOW_BARS`, main.py must not use the broken form, and the fallback
  must be loud. Suite **42/42**.
  **VALIDATE:** (a) deliberate-failure test PASSED — reintroducing the old
  import turns the contract suite red; (b) post-deploy, the L2.5-unavailable
  line must be absent from every box's log and `status.py` must show the L2
  engine; (c) the canary set proves it can't return on a stale sync.
  **DEPLOY:** after the close with the day's other syncs — this needs a
  fleet restart and must not happen mid-session.




- **Y.1 — ✅ folded into Y-a.** The unreachable fallback is fixed in the same
  patch rather than as a separate change.


## PART 4 — CHANGELOG (document history, newest first)

*Moved here 2026-07-30. It had grown to ~295 lines sitting ABOVE the work, so
opening the file showed history before it showed anything still to do.*

- **v3.35 — 2026-08-01 — PF.1 CONSTRUCT BUILT, AND THE WHITE PAPER WAS WRONG
  ABOUT ITS OWN FOUNDATION.** `analysis/pitchfork.py` v1.0 + 24 tests. Weight 0,
  outside the freeze. §4.1 claimed LiquidityMapper already computes swing pivots
  — it does not; it computes equal-high/low price clusters. The real fractal is
  in `utils.math_utils`, consumed by StructureAnalyzer. **The paper is corrected
  in place with the superseded text left visible**, per the operator's rule that
  an ugly truth gets adapted to rather than covered up.
  The fork owns its own pivot definition (**AN**), chosen so anchor evolution
  never becomes a diff against the live trading path — and so it can be deleted
  if the overlay does not earn its keep. §3.2's Modified Schiff default is now
  MEASURED rather than reasoned. **New AO: the shared helper's float-equality
  defect**, reproduced in a test, filed for post-freeze because it feeds
  TRENDING's veto. **The daily fork remains unbuildable** — `TIMEFRAMES["1d"]`
  serves 10 bars and §4.2 needs k=2 with R=40, which also blocks §6's
  daily/hourly confluence, the highest-value signal the overlay was to produce.
- **v3.34 — 2026-08-01 — THREE OF FOUR TIMEFRAMES HAVE NEVER VOTED, AND THE BOT
  COULD HAVE GONE BLIND WITHOUT SAYING SO.** Two independent silent-degradation
  faults found in one session, both shipped the same day (0a0da3b, 380a1bd).
  **AK — the trend vote.** `_analyze_single` bails to NEUTRAL below
  `EMA_SLOW+5 = 55` bars; live fetches 1d=10, 1h=50, **15m=50** — only 5m (100)
  can vote. v3.1's 07-16 reweight moved the direction weight onto 15m believing
  it would carry, and **15m was starved too**, so that fix only half landed. With
  one voter the gate needs 5m conviction > 0.579 or direction is NEUTRAL, which
  is a HARD VETO on TRENDING — so TRENDING has been structurally unreachable
  below that line and the **condor, as the RANGING fallback, absorbed the
  deficit.** config **v4.1** raises 15m to **150** (not 60: the EMA-50 is
  re-seeded on the tail and is off by 69% of a bar at 55, 49% at 60, 2.5% at 80,
  0.3% at 150). **1h left asleep on the operator's call** — the market responds
  to developments since the close more than to the prior session's range, and a
  live 1h vote would oppose the opening drive in exactly the window A2.6 studies.
  **AL — the blind alert.** `_feed_alive()` proves the PRODUCER runs, not that
  the BARS are current, so a feed writing 15-minute-stale bars passed every check
  while every engine consumed delayed data. `market_data` **v3.3** adds a recency
  guard and routes six blind paths through `record_blindness()`; `blindness_latch`
  **v1.0** + `alert_manager` **v1.8** + main.py wiring page once per outage with
  the snapshot captured at the FIRST blind tick. Built on the SYMPTOM, not a cause
  list. **Telegram is an emergency-services channel** — RTH-gated, throttled once
  per episode, drillable via devtools **56** with a `DRILL — NOT REAL` prefix.
  `OT_BLIND_REFUSE` ships OFF pending stale-frequency evidence.
  **S was already built, and had a defect inside it.** The bookmark shipped
  2026-07-21; the real fault was that it warmed the **1m** frame too — the one
  frame `market_data` v3.1 deliberately session-scopes — so the 25-bar angle
  window straddled the overnight gap for the opening 25 bars of every replayed
  session, scoring RANGING/COMPRESSION where live scores nothing. **v2.1** scopes
  it; **v2.2** caps every resampled frame at `TIMEFRAMES[tf]["candles"]` (the
  frames were UNCAPPED, and at warm >= 7 the offline 1h would have voted while
  live's stays asleep) and moves the warm default 5 -> 8. **regime_backfill v1.2**
  adds the passthrough — nothing in the chain had ever passed one, so every diary
  and a2_characterise run used the old default of 5.
  **A2.6 promoted to DESK** with both tools built and proven: `gap_backfill` v1.1
  and `a2_partition` v1.0, the latter verified by planting four worlds and
  asserting recovery. The discriminator is the **reversal-gap deficit** — H1 and
  H2 can only ADD violations, so a rate BELOW the midday baseline is the gap
  artifact's unfakeable fingerprint.
  **New AM: rebuild the corpus at warm 8. The 4.02% A2 rate and the 45%-in-the-
  10:00-hour concentration are SUPERSEDED** and must not be diffed against the new
  baseline.
  **WORKING_AGREEMENT gains §15-17:** delivery is a tarball plus one line with a
  CONTENT-keyed supersession gate; long-running work goes in tmux; Telegram is an
  emergency services channel.
  **Two self-inflicted lessons worth the ink:** the starvation warning's first cut
  logged every tick and buried the log — an alarm that spams is an alarm that gets
  filtered, which is how three dead timeframes went unnoticed in the first place.
  And the latch's `_reset()` wiped the outage duration a beat before the recovery
  notice reported it, so the all-clear would have read "was blind 0s" — the one
  number it exists to carry.
- **v3.33 — 2026-08-01 — A2 IS A HORIZON MISMATCH, AND THE STATE IT FLAGS MAY BE
  TRADEABLE.** `a2_characterise` over 156,712 ticks: 6,303 violations (4.02%),
  adx p50 45.8 vs 29.6 clean, angle p50 6.8 vs 11.8 clean, adx direction 52/48
  (**lag hypothesis dead**), 45% of violations in the 10:00 hour. Cause found in
  the code: **RANGING's angle reads 25 bars of 1-MINUTE data (25 min) while
  TRENDING's adx comes from the 5m frame at ADX-14 (70 min)** — the two scores
  answer questions about different lookbacks, so both can honestly be true.
  **This may INVERT A2.2:** a shared axis must pick one horizon and would discard
  the other. New **A2.4** (the finding + the decisive 70-min-window test),
  **A2.5** (`paused_trend` factor column — the operator's reframe: an impulse
  that has paused is a flag/pennant, a recognisable tradeable state, and argmax
  currently destroys the fact that both were true), **A2.6** (`gap_pct` — the
  overnight gap enters ATR via true range but is never MEASURED; uniquely
  BACKFILLABLE from data already on disk, and the first hypothesis is whether gap
  size conditions ORB's -0.24R).
  **The tool caught its own defect first:** v1.0 looked up `TRENDING_BULL` in a
  breakdown keyed `TRENDING`, found zero adx, and printed a verdict anyway. v1.1
  refuses a verdict when the discriminator did not run.
- **v3.32 — 2026-08-01 — PITCHFORK SPLIT INTO FOUR PHASES; only the last needs
  L2.6.** The overlay had been gated whole behind Aug 21, which put construction
  ten days before live capital and left the condor broken through go-live.
  **PF.1 CONSTRUCT is startable now** — a weight-0 object nothing reads cannot
  break a behavioural freeze. **PF.2 FIT's blocker cleared tonight**: defect S,
  the HTF bookmark, is now evidenced (warm-sessions 5 → 15 moved TRENDING dom%
  30% → 36%). **PF.3 MEASURE ~Aug 10, condor strikes ONLY** — a credit is one
  number. **PF.4 WIRE post-L2.6**, v4.0 at two proven consumers.
  **The replacement map is now recorded with the ACTUAL current constants** so
  the head-to-head is concrete: 0.80*EM / 1.2*EM guardrail / 0.65 trigger for
  strikes, MAX_LOSS_PCT=0.40 for stops, bb_middle for exhaustion, horizontal FVG
  trails, BB_WIDTH_COMPRESSION_PCT=0.20 for compression.
  **A STALE TARGET FOUND AND CORRECTED:** the paper's application #2 cited
  `CONTINUATION_MIDLINE_ATR`, removed by the 07-28 FVG-pullback rewrite and now an
  orphan. Eight days old and one of seventeen targets had already moved. §7 now
  carries a standing instruction to re-read against HEAD before ordering
  consumers.
  **And §7.3's A2 note is promoted to a live hypothesis:** daily and hourly forks
  may legitimately disagree, so a single-axis A2 fix could ERASE genuine
  cross-horizon signal. That check needs PF.1 to exist — a further argument for
  constructing early.
- **v3.31 — 2026-08-01 — A2's ROOT CAUSE IDENTIFIED, and the answer was already
  in the codebase.** A3 (BREAKOUT & COMPRESSION not both >0.5) passes with ZERO
  violations because those two read the SAME `atr_ratio` in OPPOSITE directions —
  one measurement, two ends. A2 fails because TRENDING reads **ADX** and RANGING
  reads **midline ANGLE**: two unrelated measurements with nothing coupling them,
  so both can be high on the same tick. That is the whole of A2, and it is
  structural rather than a tuning problem.
  Staged as **A2.1** (characterise the 196 violating ticks first — if they are
  post-move consolidation with undecayed ADX-14, it is a measurement LAG and no
  reformulation helps), **A2.2** (shared inverted axis, Kaufman Efficiency Ratio
  the leading candidate, matching A3's existing idiom — ship for go-live), and
  **A2.3** (log-odds: TREND = sigmoid(L), RANGE = 1 - TREND, making A2 impossible
  to violate rather than tested for — correct endpoint, HOLD until after Aug 31
  since it re-bases every ramp bound and the whole L1.11 track).
  **Corroborating evidence from tonight's warm-sessions experiment:** 5 -> 15
  raised TRENDING dom% 30% -> 36% and made A2 WORSE (179 -> 196). Deeper history
  makes ADX more confidently high while the angle is computed independently —
  exactly what an uncoupled-ADX story predicts.
- **v3.30 — 2026-08-01 — candle_feed gets an RTH gate (v3.9).** No time gate had
  ever existed on the reconnect loop, so a box that was up held a DXLink socket
  regardless of hour — harmless on a normal day, but every maintenance wake put
  29 boxes on the wire for nothing. The blocker was that chain Greeks/Quote share
  that socket; resolved by reading the call path rather than reasoning about it —
  `chain_snapshot.snapshot()` runs inside a tick loop that already gates on
  `is_rth()`, so archival is unaffected. Connects 20 min before the open
  (`OT_FEED_WARM_LEAD_S`) because fetch_candles refuses a stale heartbeat, and
  DISCONNECTS at the close on the existing flush cadence — both edges, so a box
  left up overnight releases its subscriptions instead of streaming until
  something drops it.
- **v3.29 — 2026-07-31 — E's FIRST LEDGER RUN: sweep says do not ship.**
  `gate_ledger.py` over 10 sessions, 194 of 208 scored events joined to trades.
  **The trades E would have refused on SweepReversal won 78% and made $1,781.18
  (n=27)** — the gate is wrong for that strategy, exactly as the mechanism
  predicted before any data was read. Continuation goes the other way (n=8, 25%,
  -$928.50) on a sample too thin to call. Holdout is n=6 and sweep-only, so there
  is NO formal verdict — but the leading answer is now **exempt sweep and judge
  continuation separately**, not ship-or-abandon. Recorded on the Aug 18 item so
  it is not re-derived. F is 0/208 on rrr, as designed.
  **gate_ledger v1.1** — v1.0 counted ORB in the blocked population (+$3,343 of a
  +$4,196 total) for a gate ORB never reaches. Caught on the first real run.
- **v3.28 — 2026-07-31 — FRIDAY IS CLEAR. AE resolved (premise was wrong) and D
  closed.** AE assumed `futures_trader_v1` shipped the same `push.sh`; a fresh
  clone shows it has **no push script at all**, and the repo was already clean —
  0 undefined names across 63 files. Ported the suite gate anyway, where it is
  more load-bearing than here because there is no second net. D templatized
  `shadow-observer.service` with `__INSTALL_DIR__` + option 11 substitution,
  refusing to arm a unit with the placeholder still in it. Zero fleet impact.
- **v3.27 — 2026-07-31 — F WIRED. Both genesis constants are finally read by
  something.** Measured premise, same as E's: **rrr = 1.00 scores 0.84 and grades
  A** — a 1:1 trade is a top-grade fire, because RRR was never one of the five
  scoring dimensions. Hard floor on the scored path, **ORB counter-only** (its
  RRR is structural — narrow range mechanically means low ratio — and gating the
  only earning strategy on a ratio it does not control, with no evidence low-rrr
  ORBs lose, is the category-3 move the house rules forbid). rrr of None is
  inert. Ships OFF; the 1.3 floor is the genesis guess and is explicitly a PRIOR
  awaiting the Aug 1 fit.
  **Saturday is now unblocked** — "E + F tester proof" needed both to exist.
- **v3.26 — 2026-07-31 — the E ledger must be split PER STRATEGY, or it can
  give the wrong verdict in both directions.** E applies to exactly two
  strategies and they relate to VWAP oppositely: continuation is trend-following
  (misalignment = wrong-sided, the case E was reasoned from), while
  **SweepReversal is a FADE** — a low sweep produces a LONG while price is still
  below VWAP, and the strategy treats VWAP recovery as a confluence BONUS, not a
  requirement. So valid sweep longs are misaligned by design and this gate would
  block them. Sweep is the highest-volume strategy in the fleet (985 lifetime)
  and among the best performing. A pooled "ship it" would gut it. Three outcomes
  now written into the Aug 1 tester proof, including "exempt sweep the way ORB is
  exempt", plus a forward path to Aug 18 if tomorrow's holdout n is thin.
- **v3.25 — 2026-07-31 — E WIRED, and it caught a duplicate constant that would
  have shipped it backwards.** The VWAP gate blocks misaligned scored setups —
  measured premise: a long BELOW vwap scores 0.73 and grades B, i.e. fires. Ships
  DEFAULT OFF as a counter until the retro ledger convicts. ORB exempt by
  construction, inert on undefined VWAP, inert on neutral direction. Closes N.2's
  `gate_block` disposition half.
  **The bug worth remembering:** `VWAP_FILTER_ACTIVE = True # UNWIRED` had sat in
  the genesis block since the beginning — a hardcoded True nothing consulted, so
  "the filter is on" was true in config and false in code for months. Adding a
  second definition higher in the file was silently overridden by it. A test that
  asserted the default was False is the only reason it did not ship ON.
- **v3.24 — 2026-07-31 — FRIDAY CLEARED: five items closed, and the entry-side
  twin of v3.23's finding is opened.** **AD** (continuation traded — 99 trades,
  52% WR fleet-wide) and **AG.2** (compression HOLD works, COMPCANCEL=0, a condor
  Leg 1 actually filled) both verified on live tape. **AC** gave the three
  consequential silent declines a voice, including the dual-floor one that had
  already produced a wrong conclusion the day before when a zero grep count was
  read as "never rejects" instead of "rejects silently". **N.2 + N.3** added
  `rrr`, `closes_beyond` and `sweep_age_bars` to the journal — factor columns,
  done today rather than Monday because they cannot be backfilled.
  **New AJ (Sat Aug 1) — and it turned out to be the chase-vs-retest answer.**
  Continuation's handoff path made +$1,333.50 over 50 trades while standalone
  lost $2,024.00 over 49. Then the mechanism: `_is_runaway = orb.invalidation_
  reason == "runaway"`, so **a handoff fires on exactly the setups ORB had to
  discard because price never returned for the retest**. That is the
  counterfactual the assistant declared unmeasurable on 07-30 — it has been
  running since July under a different name. The runaways are the profitable
  half. Precise version: not "chasing works", but *runaway confirms force, then
  enter on a shallow pullback instead of a full retest.* Two confounds recorded
  in the item (handoff also runs a looser momentum gate; v4.10's BOS stop lands
  Aug 3 and will move standalone specifically). **Candidate outcome — retire
  standalone, run handoff-only — reviewed ~Aug 14, not before.**
- **v3.23 — 2026-07-31 — CONTINUATION GAINS A STRUCTURAL STOP (BOS), and the
  excursion LEASH section was silently printing nothing.**
  **(1) BREAK OF STRUCTURE — `exit_engine` v4.10, step 2b, UNGATED.**
  Continuation's ladder was hard-close → regime-flip → −25% floor → theta-bleed →
  trail, and **gates 4 and 5 both require the trade to have worked first**
  (theta needs a gain band; the trail needs a resumption gain to arm). So a trade
  that never worked had *nothing* between entry and the floor. MEASURED
  (excursion 2026-07-31, 116 trades): **31 continuation trades ran from entry
  straight to the −25% floor with MFE of only 2–3%** — `max_loss_floor_25pct`
  n=17, `_24pct` n=11, `_26pct` n=2, `_23pct` n=1, all 0% win. ORB has had a
  structure stop all along; continuation never did.
  `BOSTracker` already existed but was wired **only into the sweep path**. It now
  runs for continuation too: every new closing high promotes that candle's LOW to
  the protected higher-low, and a 1m **close** below it breaks the HH/HL sequence
  (mirrored for shorts on closing lows / protected lower-high). Uses `iloc[-2]`,
  the last fully closed candle. New exit reason on continuation: `bos_exit`.
  **Deliberately UNGATED.** Sweep's copy is gated on `pnl_pct > 0` ("don't BOS
  out of a healthy retest that hasn't moved yet"). That gate is precisely what
  would have MISSED all 31 of these — they never went positive. A third
  must-work-first gate would have left the same hole.
  **WHY BOS AND NOT THE FVG STOP (operator's call).** `underlying_stop` is
  stamped on every continuation record since v1.3.1 (long `gap.bottom − 0.5·atr`)
  and has never been read — but wiring *that* in was rejected on the reasoning
  that **a gap fill is not trend failure**: gaps fill routinely inside healthy
  trends, so the FVG level invalidates the *entry* rather than the *thesis*. It
  is also **static**, fixed at entry, so it protects nothing once the trade
  works. BOS is **dynamic** — the protected level ratchets up as the trend makes
  new highs, so it both invalidates on real structure failure and trails the gain
  structurally. **The FVG remains the ENTRY** (exploited repeatedly and
  profitably on 2026-07-31: `continuation_trail` n=48, 83% win, +15% realized);
  it is simply not the exit. The stop *types* in this system are the operator's
  design; this was a wiring gap, not a new rule.
  **The −25% floor is NOT widened.** Same report's FLOOR VERDICT: **0 of 59
  winners ever breached −25% and recovered**, so a wider floor would have saved
  nothing. The MAE separation also argues BOS will not be over-restrictive —
  winners **−5%**, floor-losers **−29%**, a wide clean gap.
  **(2) LEASH VERDICT was silently empty — `excursion_report` v2.3
  (day_trader_pro).** The section iterated a hardcoded tuple
  `("trail_stop_hit","post_target_trail","bos_exit","theta_bleed")`. On
  2026-07-31 **none of those four occurred** — the day's trail exits were
  `continuation_trail` (n=48), `orb_trail_stop` (n=7), `orb_fvg_trail_stop`
  (n=1) — so every iteration hit `continue` and the block printed nothing, on the
  day it was most needed. Now derived from the data, sorted by giveback
  descending (loosest leash first), with an explicit "nothing to compare" line
  instead of silence. First reading: `continuation_trail` gives back **20% of a
  35% MFE (57% of peak)**, `condor_stop` **31% of 38% (84%)**, while
  `orb_fvg_trail_stop` gave back **47% of 152% (31% — best)**; one trade, but the
  first live datapoint favouring the FVG-anchored trail in the TC.2 bake-off.
  **ALSO ESTABLISHED (no action possible).** MFE/MAE **cannot be recomputed
  retroactively** — `max_premium_seen`/`min_premium_seen` are written tick-by-tick
  while a position is open. `fleet_trades_2026-07-13.json` verified to contain
  **zero** rows with telemetry; that date predates the v3.8 columns entirely.
  Reports that appeared to show 07-13 telemetry were the cumulative-file bug
  surfacing *recent* trades under an old date. Separately,
  `excursion_report.load_day()` prefers `trades/<date>/*.db` whenever the folder
  exists and only falls back to the JSON — so a harvest backfilling an old date
  folder silently switches that date's source to schema-less DBs. Noted, not
  changed.
- **v3.22 — 2026-07-30 — AG SHIPPED THE SAME NIGHT IT WAS FOUND, plus the
  instrumentation that makes it worth shipping.** Condor Leg 1 no longer cancels
  on a COMPRESSION flip — compression is a tightening range and that is where a
  neutral short-premium structure most belongs; only DIRECTIONAL regimes cancel.
  Paired with `v-selfdiag`, so the abandonment line reports excursion toward each
  trigger plus EM decay — because holding longer trades a fast death for a slow
  drift, and the drift needed measuring rather than assuming.
  **Set expectations honestly: this will probably not produce condor TRADES
  tomorrow.** The trigger geometry (AI) is untouched. What it produces is the
  first excursion data this strategy has ever generated, which is what decides
  whether the anchor question is a tweak or a redesign. Live verification is
  **AG.2** (Fri Jul 31).
  **AI now records the anchor candidates** so they are not re-litigated: GEX pin
  REJECTED (condor is architecturally the no-pin fallback; adopting the pin folds
  it into butterfly, which has 27 lifetime trades vs condor's 362), VWAP LIVE
  (always available, already computed, sits behind price in a trend). Plus the
  operator's data doctrine — collect wide on paper, place the gate at the ROI
  crossing — with the standing constraint that the loose version is NOT
  unmeasured: pre-dualfloor sold with no minimum distance and bled for ~3 weeks.
- **v3.21 — 2026-07-30 — CONTINUATION v1.4 PROVEN OFFLINE; condor baseline
  recorded; sweep is genuinely rare.** `backtest_harness` v1.1 added a strategy
  attempt census (continuation / sweep / condor driven over the same tape against
  a modelled chain; butterfly excluded — it needs a GEX pin). Swept across 29
  symbols x 14 sessions = **82,698 strategy evaluations, ZERO raised**, which is
  its own robustness signal after a week that produced two NameErrors.
  **Continuation 158 setups, 158 valid, 0 invalid** — AD downgraded from
  unverified to logic-proven; the remaining gap is fill on a REAL chain, since
  the census chain is Black-Scholes with assumed liquidity.
  **IronCondor 141 plans** — recorded on AG as the baseline the compression-cancel
  fix is protecting; plan creation was never the bottleneck.
  **SweepReversal 26 setups (0.09%)** — genuinely rare offline, and worth a
  flag: CVX ran FOUR profitable sweeps live the same day, so live detection
  finds more than the harness does. Likely because the harness's liquidity
  engine reads resampled 5m/15m rather than live 1m. Not a defect; it means the
  backtest UNDERSTATES sweep and should not be used to judge it.
  **Method note:** the first sweep run silently omitted the whole census section
  because the strategy imports failed under control's venv
  (`ModuleNotFoundError: tastytrade`) — the harness guard correctly said so per
  symbol, but backtest_sweep printed nothing rather than surfacing that 29 runs
  had come back degraded. A missing block looked identical to a block of zeros.
  Same failure class this file has been cataloguing all week, in code written the
  same hour. Fix: the sweep must banner `CENSUS DISABLED on N/29`.
- **v3.20 — 2026-07-30 — THE CONDOR DROUGHT HAS A CAUSE, AND IT IS NOT THE
  TRIGGER.** Reading CVX's bot.log directly — after counting greps produced two
  wrong answers — showed condor plans being **CANCELLED three times by a flip to
  COMPRESSION**, each surviving ~19 minutes. New **AG** (Fri Jul 31): a neutral
  trade belongs most in a tightening range, so cancelling there is a category
  error; treat COMPRESSION as a permitted hold, cancel only on a flip to a
  DIRECTIONAL regime, mirroring Leg 2's existing pause-and-hold behaviour. New
  **AI**: the trigger geometry is the deeper question — spot ~190, bb_upper
  190.93, call trigger at **193**, i.e. a plan needing a breakout-sized move
  during a regime defined by its absence. The missing piece is a MIDPOINT, and
  that is pitchfork work; explicitly NOT a re-tune of 0.65/0.80.
  New **AH** (Sat Aug 1, weekend by operator's choice): first evidence that ORB
  may be firing in a regime contradicting its own thesis — 14 CVX sessions, 10
  fired, 0 gate-blocked, **-1.56R**, 8-of-10 STRUCTURE_STOP, **7 of 10 under
  RANGING**. Recorded with an explicit DO-NOT-ACT: one symbol, ten trades, and
  CVX was 51% RANGING. Needs a harness `--all` flag and a per-symbol sweep first.
  **Method note worth keeping:** three rounds of `grep -c` gave confident wrong
  answers (the dual floor "never rejects" — true but irrelevant; `NEVER1=0`
  read as "no abandonment" when the real meaning was "the plan never lived long
  enough to reach that branch"). Reading twenty log lines settled it in one
  pass. Counts test a hypothesis you already have; the log tells you which
  hypothesis to have.
- **v3.19 — 2026-07-30 — THREE THINGS THAT EXISTED ONLY AS PROSE ARE NOW DATED
  ITEMS, and AB is recorded as resolved.** v3.18 correctly captured the
  continuation finding, but three of its consequences lived only in the
  changelog, where nothing will ever prompt anyone to act on them: the
  **silent-decline punch list** (now **AC**, Fri Jul 31 — three paths that can
  refuse a qualifying setup in silence, named with file and line), **v1.4's
  live-fire verification** (now **AD** — the rejection path is confirmed closed;
  the strategy actually firing is NOT proven, and a `no strike: no expected move`
  line would mean the fix is incomplete), and the **conviction-bound refit** (now
  **AF**, Aug 8–9 alongside L1.11/L2.4 — `OT_CONT_CONV_LO/HI` were fitted against
  fallback-engine conviction, and L2.5 replaced that engine on the morning of
  07-30, so the strike distance is calibrated against an engine the fleet no
  longer runs).
  **AB recorded as resolved** with its open half split out as **AE**
  (futures_trader_v1 ships the same push.sh and still has the hole).
  **PROCESS NOTE, because it nearly cost this file real content:** an earlier
  v3.18 from a parallel thread added AB and was never committed — the tarball was
  delivered, the conversation moved on to the push.sh code, and the backlog edit
  was simply never applied. Nothing was overwritten and no thread did anything
  wrong; the item just evaporated between delivery and landing. **Any backlog
  delivery should lead with `git pull --ff-only && head -1 docs/BACKLOG.md`** so
  a version that is not what the edit expects refuses rather than silently
  diverging — and so an unlanded edit is visible immediately.
- **v3.18 — 2026-07-30 — CONTINUATION HAD NO STRIKE SELECTION. It has never
  taken a trade, on any box, since it was written.** Found by asking why AMZN sat
  out a textbook FVG pullback in a clean uptrend. `generate_signal` built an
  `OptionsSignal` with **no strike and no entry_premium**;
  `base_strategy.is_valid()` requires `strike > 0 and entry_premium > 0`, so main
  rejected it every tick with `Invalid signal from ContinuationStrategy` and the
  strategy re-signalled forever. Confirmed **fleet-wide** — AAPL, UNH, XOM, AMZN
  and the rest all logging the same rejection all day.
  **v1.1's own header predicted this and nobody read it that way:** defect W said
  both paths "dead-ended before ever reaching strike selection." The gates were
  fixed in v1.1; *the strike selection they were supposed to reach was never
  written.* Every entry-trigger change since — the BB-midline logic, the
  2026-07-28 FVG rewire, the 07-29 `mid` hotfix — was tuning a path that could
  not produce a valid signal regardless.
  **FIX (v1.4, `1017f3c`, deployed 15/15):** the strike now sits a fraction of
  the ATM-straddle expected move out in the trend direction, the fraction being a
  confluence of ADX (mechanical travel) and regime conviction (the engine's
  agreement). Disagreement between the two pulls the strike back toward the
  money; only mutual agreement pushes it out. Same EM basis as the condor's
  0.80×EM floor. Bounds fitted from the fleet archive (ADX p25 24.7 / p75 47.3;
  conviction p25 0.396 / p90 0.587) → `OT_CONT_ADX_LO=25 ADX_HI=50
  CONV_LO=0.40 CONV_HI=0.60 W_ADX=0.6 W_CONV=0.4 EM_FRAC_MIN=0.25
  EM_FRAC_MAX=0.75`, all env-overridable. `trend_strike_plan()` is module-level
  **on purpose** so `trade_readiness._staged_pick` can call it while a trade is
  merely STAGING — chain availability and liquidity checked as conviction climbs,
  not at the moment of the trigger. Wiring readiness to it is NOT done.
  **CORRECTS A FIGURE THIS FILE MAY CARRY ELSEWHERE:** conviction is *not*
  ceilinged at 0.582. That was one day on the degraded fallback engine; the
  archive reaches **0.831**.
  **ELEVENTH SILENT FAILURE OF THE WEEK, and the fourth found this way.**
  `is_valid()` returns a bare `False` — it never says which field failed. A
  validator that named the field would have caught this the day it shipped. Same
  class as the butterfly's DEBUG-level gates, ORB's "1 named level(s)", and
  continuation's own three bare `return None` paths (all logged in v1.3.3, folded
  into v1.4). A sweep of `strategy/` found **26 silent `return None` paths**;
  most are regime-mismatch gates that fire every tick and are left silent
  deliberately. The ones that can refuse a QUALIFYING setup and are still silent:
  `butterfly_strategy.py:238` (find_strike, no liquid → butterfly dies with no
  explanation), `condor_roll.py:131`, `iron_condor_strategy.py:288`. **Not fixed —
  open punch list.**
  **STILL UNVERIFIED:** no `[continuation] strike` line has appeared yet. v1.4
  landed ~14:00 ET and the required conjunction (TRENDING + 1m wick tagging an
  unfilled 5m FVG) has not occurred since. Zero `Invalid signal` in the hour
  after deploy confirms the rejection path is closed; the strategy firing at all
  remains **unproven on live tape.** Watch
  `grep -E "\[continuation\]"` — a `no strike: no expected move` line would mean
  the ATM straddle lookup fails and the fix is incomplete.
- **v3.17 — 2026-07-30 — L1.CAL CORRECTED, and a verification dated.** The
  "align_frac is a constant" claim came from ONE session; the full 13-session
  corpus (134,137 ticks) shows p95 = 1.00, so the factor is severely compressed
  rather than dead and L1.9 widens its tail rather than gating its existence.
  The existing schedule already sequences this correctly — L1.9 grafts Aug 4,
  L1.11 fits Aug 8–9 — so nothing moves; instead **L1.CAL.2 lands Wed Aug 5** to
  verify the graft actually widened the distribution before anything is fitted
  to it, paired with L1.6's flat-angle sweep because both read the same rebuilt
  diary and `flat_s` is the same measurement's soft ramp. Full-corpus numbers
  replace the single-day ones throughout: `flat_s` 67.6% pegged with `lo=12` at
  input p52 (worse than the one-day read, and the clearest fit available),
  `adx_s` 37.6% (better), `room_s` and `osc_s` both healthy and both already
  re-fitted — the control cases.
- **v3.16 — 2026-07-30 — L1 RAMP CALIBRATION: tool fixed, and it found that
  L1.11 has an unrecorded dependency on L1.9.** `align_frac` is a CONSTANT 0.67
  across 11,295 ticks, so `align_val` contributes nothing independent and cannot
  be fitted until the bookmark lands. New item **L1.CAL** carries the detail.
  Two more silent failures fixed in the tool itself (misreported bounds via a
  swallowed import; a 300MB load that died producing no output) — that is the
  ninth and tenth of the week, both in a tool built to detect exactly this class.
- **v3.15 — 2026-07-30 — PART 1 IS NOW OPEN ITEMS ONLY.** Fifteen resolved
  items were still sitting in the schedule carrying ✅. Eight were already
  written up in PART 3 and were simply duplicates — dropped, along with the
  "Original text follows" blocks that made some of them a third copy. The other
  seven (W, W.2, P5.1, N.1, Z, T.2, Y.1, Y.2) moved into PART 3 under a dated
  subsection. All 47 open items verified retained.
  **Recorded because it will confuse someone later: THIS FILE REUSES LETTERS.**
  PART 3 already held a `V ✅ 2026-07-22` (ORB scored, not gated) and a
  `Y ✅ 2026-07-23` (condor window opened before BB was computable) — entirely
  different items from the 2026-07-29/30 `V` (push.sh target resolution) and `Y`
  (report wiring). The moved subsection says so inline.
  Two bullets in PART 1 still contain a ✅ glyph and are CORRECTLY left there —
  the Epoch-1 exit review and `L2.6 ✅ if the window ran clean` are future
  conditionals, not resolved work. An automated sweep that keys on the glyph
  alone would delete both.
- **v3.14 — 2026-07-30 — CHANGELOG MOVED TO THE BOTTOM (PART 4).** The open
  schedule is now what the file opens with. Nothing in PART 0–3 was reordered:
  the date trajectory is the plan and it is untouched. Added a short orientation
  header with the tag legend, so a light session starts with a grep rather than
  a read. Also fixed a stale anchor — PART 0's clock still labelled Wed Jul 29
  as "Today".
- **v3.13 — 2026-07-30 — EVM instrumented, and the first reading closed both
  late DESK items.** `tests/evm_status.py` reports earned value against this
  file, with the adaptation that makes it honest here: **schedule variance is
  split by cause.** SPI(all) is calendar truth; **SPI(desk) is accountability**
  — of the work that was ours to move, how much moved. A late `[DESK·DATA]`
  item is a DC&A dependency, not an execution failure, and averaging the two
  produces a number that cannot be acted on.
  First run found two things immediately. It reported **SPI 2.53** — impossible,
  and the cause was that PART 3's resolved register duplicates every item
  already marked ✅ in PART 1, so earned value exceeded the baseline. A metric
  that can exceed its own BAC is measuring the document, not the project; the
  parser now reads the schedule only. **That duplication is real and still
  present in this file** — it is what makes it balloon, and it is worth removing
  in a later pass.
  Corrected reading: **BAC 64 · PV 15 · EV 15 · SV 0 · SPI(all) 1.00** — on
  plan. But **SPI(desk) was 0.00**: both DESK items due were open. **Y** was
  simply never marked (it landed and was verified at the 07-30 wake) and **Y.2**
  was genuinely outstanding — now shipped as emit **v1.5.0**. Both closed, so
  the controllable index is clean.
  Gate pressure, stated plainly: 13 DESK items fall on or before the **Aug 21
  freeze**, 22 days out — **0.59/day, which the tool rates TIGHT.** DESK·DATA
  and FLEET unblock themselves; the DESK pile does not.
- **v3.12 — 2026-07-30 — EVERY OPEN ITEM TAGGED BY WHAT IT REQUIRES. Dates and
  order untouched** — the trajectory is the plan and it stays exactly as it was.
  All 49 open items now carry `[DESK]` / `[DESK→DEPLOY]` / `[DESK·DATA]` /
  `[FLEET]`, so filling a light session is a grep instead of a reading exercise.
  **The split: 16 DESK · 7 DESK→DEPLOY · 20 DESK·DATA · 6 FLEET.**
  The point of the tagging: **DESK is the only bucket under our control.**
  DESK·DATA unblocks itself on the calendar and FLEET waits for a window — so
  the 16 DESK items are the whole of what effort can move. Drive them to zero
  and the Aug 21 freeze waits on data alone rather than on us.
  Flagged while classifying: **item I is an UNREACHABLE BRANCH**
  (`can_enter(is_butterfly=...)` — the main.py call site never passes it),
  scheduled Aug 17 as a tidy-up. That is the same defect class as
  `_REGIME_ENGINE == "L2"`, which cost the entire L2.5 history. Two of these in
  one week is a pattern, and `swallow_audit` does not catch it — it answers
  "does it say so when it fails?", not "does it run at all?"
- **v3.11 — 2026-07-30 — MARKER CORRECTION (caught by the user).** v3.10 wrote
  a day header asserting "every item below is resolved" and left every
  individual bullet unmarked — W.0 still reading 🔴🔴 — while W.1 was in fact
  still open. A summary claim is not a status. Each item now carries its own ✅
  inline with the evidence, the original text is preserved beneath it, and the
  day header says what is true: **closed EXCEPT W.1**, which carries forward to
  the Aug 10 calibration-epoch start because the quarantine cannot complete
  until enough real L2 data exists to compare against. **This is the fifth
  stale-marker instance this week** and the only one I introduced: T.1, T.3, U
  and T.2 were all cases of the file trailing the repo; this one was the file
  contradicting itself. Rule reinforced — mark the ITEM, never the day.
- **v3.10 — 2026-07-30 — THURSDAY'S WORK. L2.5 committed a regime label in
  production for the first time ever.** Verified live: `STATE=yes` on all 15
  woken boxes (that state file had never existed on any box), and
  `RECOVERED=1` fleet-wide — every box warmed through the opening window and
  began committing. XOM led with 7 L2 transitions.
  **Items resolved today:** **W.0** (main v4.7 deployed, L2.5 reachable);
  **W.2** delivered as `tests/swallow_audit.py` AND promoted to a nightly
  conductor phase; **V** as push.sh v1.7 (prefers the caller's directory,
  announces its resolved target and remote before acting — the 07-29 near-miss
  wrote nothing only by luck); **T.2** found already shipped in main v4.1, with
  the missing half — the documented model — added to MECHANICS; **Y** complete
  across all three parts and two repos.
  **Built today beyond the list:** main **v4.8** — the ~25-minute opening
  window where RANGING and COMPRESSION cannot compute now logs INFO as designed
  behaviour instead of a WARNING that fired on 13 of 15 boxes, and
  `regime_log.engine` / `trades.regime_engine` stamp L2-vs-v13 provenance into
  the row rather than leaving it recoverable only from a bot.log tag.
  orchestrator **v0.4.0** — fleet/origin parity reported in the morning ack
  (drift is named, never auto-pulled: a 09:15 pull would deploy unverified code
  fifteen minutes before the open, which is precisely how the 07-28 rewire took
  out the 07-29 session). conductor **v1.8.0** — phases 10 and 11.
  **NEW STANDING RULE, and it changed what shipped today:** anything that must
  happen around the EOD chain belongs IN the conductor, never in a command
  someone has to remember — *including a one-time check* — and every such
  addition is documented in the version header and changelog for posterity. Two
  things I had handed over as manual commands became phases under it: the
  nightly silent-failure census (warns when the swallow count RISES, i.e. when
  a new silent handler is added) and the VWAP orientation ledger, so item E's
  evidence accrues whether or not anyone remembers to gather it.
  **Consequence for Friday:** E is no longer a build. The ledger runs nightly,
  so Friday premarket is a DECISION on evidence — including the open question
  of whether a trend-following filter belongs on a mean-reversion strategy at
  all.
- **v3.9 — 2026-07-30 — W.1 REWRITTEN TO ITS TRUE SCOPE, and W.2 answered.**
  W.1 was scoped as "quarantine 07-29" on the belief that the L2.5 outage began
  with the 07-28 excavation. The v4.7 reachability proof widened it to the whole
  project history: the L2 block was never once executed, so **every regime label
  and conviction value ever logged came from the v1.3 classifier**. First real
  L2.5 data is 2026-07-30 from ~09:55 ET. The item now names exactly what is
  affected (conditional_tables, L2.4 churn, L1.11 ramp, the readiness conv_val
  ramp — plus the correction that 07-28's "L2 integrator saturation" was
  actually v1.3's conviction band) and, deliberately, what is NOT: ORB, all
  fill/friction/latency work, the harvest and conductor plumbing, the morning
  selection chain, push.sh. **These proceed on their own merits — it is not an
  if/then cascade.** Timeline assessed rather than assumed: ~16 trading sessions
  of L2 data exist by the Aug 21 freeze, inside the original two-week intent, so
  the schedule is tight but not derailed; the real constraint is per-symbol
  depth, to be re-checked at the Aug 10 calibration start.
  **W.2 delivered** as `tests/swallow_audit.py` — a repeatable, tiered census of
  every exception handler that swallows without re-raising. 139 in
  options_trader_v3 (81 silent) and 48 in day_trader_pro (42 silent), but tiered
  by consequence only ~20 sit in risk/orders/record paths, and most of those are
  correctly silent guarded imports and date parsers. `--json` emits a stable
  snapshot so "did we add a new silent failure?" becomes a diff instead of a
  memory exercise. The tool's docstring carries all seven of the week's
  silent-failure defects and the line that ties them: every check we had asked
  whether the code WORKS; none asked whether it RUNS, and whether it SAYS SO
  when it does not.
- **v3.8 — 2026-07-29 (late) — Y REWRITTEN: the env-var fix was a band-aid, and
  the user caught it.** `install.sh` overwrites `~/market-brief/.env` from a
  heredoc, so the one-line fix would have died at the next reinstall or on any
  new instance — permanent-looking and not permanent. Y is now three committed
  changes across two repos: **orchestrator v0.3.0** (freshness guard on the
  report's `date` + `move_ranked` shape, Telegram alert, provenance stamped onto
  the selection, and the never-resolving `~/market_brief/out/report.json`
  fallback repointed at the reporter's real drop — this is what makes the fix
  survive a rebuild), **install.sh 09:15 → 09:00** (the wake fired the same
  minute the brief started; measured brief runtime ~75s, so 09:00 turns a race
  into a 15-minute margin), and **`DTP_REPORT_JSON` provisioned in the .env
  heredoc**. Deliberate-failure test passed against the real 2026-07-06 payload.
  Also new: **`day_trader_pro/docs/ARCHITECTURE.md`** records the target layout —
  Day_Trader_Pro as the over-arching project with `market_brief` and
  `options_trader` as nested, independently-installable modules — plus the
  modularity contract, an inventory of all five coupling seams, and the rule this
  day earned: a file seam between two independently-scheduled processes must
  carry a freshness stamp that the consumer checks, because it is the one seam
  class that fails silently. It also flags that **`push.sh` must be fixed
  (item V) BEFORE any migration**, since its `$HOME` scan becomes ambiguous once
  two modules share a parent.
- **v3.7 — 2026-07-29 (late) — ITEM X SOLVED THE SAME EVENING IT WAS FILED, and
  it was neither of the two explanations X proposed.** The morning wake has been
  ranking off a report frozen at **2026-07-06** — 23 days stale. The scorer is
  not broken and there is no silent model fallback: `$DTP_REPORT_JSON` was never
  set, so `report/emit.py` took its `os.getcwd()` fallback and has written
  `~/market-brief/report.json` every morning while orchestrator read a different,
  static file. Full diagnosis in Part 3; the one-line fix is **Y** (Thu Jul 30
  after the close, deliberately NOT stacked on L2.5's first live session), with
  **Y.1** repairing orchestrator's unreachable `~/market_brief/out/report.json`
  fallback (underscore instead of hyphen, plus a non-existent `out/`).
  **Also newly known: the brief's signed sentiment has never reached trading.**
  `brief_strength` feeds the Stage-3 setup nudge and has been a constant 0.30 for
  every name every day, because the frozen report predates the `move_ranked`
  sidecar. Sixth silent-default finding of the day — the tally is now the L2
  import guard, the discarded scp return values, the conductor's OHLC-only
  completeness check, selector's EXACTLY-N backfill, the unreachable
  `_REGIME_ENGINE` gate, and this. Every one of them produced plausible output
  while doing nothing. **W.2 is the most valuable item in this file.**
- **v3.6 — 2026-07-29 (evening) — L2.5 HAS NEVER RUN. NOT ONCE.** The day's
  chase ended somewhere none of the earlier hypotheses reached. A fleet-wide
  grep of `bot.log` on all 29 boxes — 34k to 138k lines each — returned
  **L2=0, FAILED=0, STALE=0**, and `integrator_state.json` had never been
  written on any box. Cause: `_REGIME_ENGINE` is built with `.lower()`, so it is
  always `"l2"`, while **both** gate sites compared it to the uppercase literal
  `"L2"` — the tick override and the startup warm-load that calls
  `_l2_integ.load`/`save`. `"l2" == "L2"` is False, so the entire L2.5 block has
  been unreachable dead code since v4.0 wired it, and **no environment variable
  could ever have helped, because the default itself failed the comparison.**
  Today's earlier fixes were real and both irrelevant to reachability: v4.5
  repaired an import into a block that never executed, and v4.6 added reporting
  to a branch never entered. Fixed as **main v4.7** (lowercase at both gates, a
  start-up assert that refuses to boot on an unrecognised engine value, and a
  start-up line naming the active engine), **check_versions v4.7** (absence
  canary on the uppercase literal), and three reachability tests — suite 45/45,
  deliberate-failure test passed.
  **Why nothing caught it for weeks:** a gate that never opens raises nothing,
  logs nothing, alerts nothing, and breaks no test. Every check we had asked
  "does this code work?" — none asked "does this code run?". That is the fifth
  and worst instance of today's recurring shape, after the L2 import guard, the
  discarded scp return values, the conductor's OHLC-only completeness check and
  the scorer's EXACTLY-N backfill. **W.2 is no longer a scoping pass; it is the
  most valuable item on this backlog.**
  **The calibration consequence is the big one.** Every regime label and every
  conviction value this fleet has ever logged came from the v1.3 classifier. The
  contamination is not 07-29 — it is the **entire history**. W.1's quarantine
  widens accordingly, and any L2-derived prior (L2.4 churn fits,
  `conditional_tables`, the L1.11 ramp) has never had real L2.5 data behind it.
  **Thu Jul 30 will be the first session L2.5 has ever actually run**, which
  makes it Day Zero for the L2 dataset and pushes every L2-dependent freeze date
  out by however long the real baseline takes. Do not re-fit anything L2-derived
  against pre-07-30 data.
- **v3.5 — 2026-07-29 — new item X on Fri Jul 31 (light day): the morning
  scorer looks like it picks the same 15 symbols every session.** Found while
  back-harvesting 07-27/28/29 — all three reported an identical discretionary
  cohort. Either the scorer is working and 14 boxes simply never contribute
  tape (a calibration-breadth problem before the Aug 21 freeze), or the model
  call is failing into `selector`'s EXACTLY-N backfill and selection has
  degraded to reporter rank while still looking normal — the same
  silent-fallback shape as the L2 guard, the discarded scp return values and
  the conductor's OHLC-only completeness check. `selection_log.jsonl` already
  holds the evidence to tell the two apart, so the item is a read, not a
  build. Also recorded here: **07-29 ran the v1.3 fallback classifier for the
  ENTIRE session** — a fleet-wide `bot.log` grep found every REGIME line tagged
  `[v13]` and not one `[L2` line, so L2.5 never produced a committed label that
  day (main v4.5 reached the boxes only at the ~17:05 fan-out, after the
  close). W.1's quarantine therefore covers the whole day with no per-box
  bracketing needed, and the afternoon's P&L recovery cannot be attributed to
  L2.5. The fix remains UNPROVEN in production until `[L2 c=...]` tags appear
  on REGIME lines after an open.
- **v3.4 — 2026-07-29 — 07-29 FLEET INCIDENT: items W, W.1, W.2 at the top of
  Thu Jul 30.** Zero trades fleet-wide until ~10:05 ET (continuation v1.3
  orphaned `mid` → NameError every tick; hotfixed as v1.3.1, `dd0d097`), and a
  second, still-live defect: all 15 boxes running the v1.3 classifier instead
  of L2.5. Root cause diagnosed and **differs from the initial read** —
  `RANGE_WINDOW_BARS` was never in `conviction_integrator`; main.py imported it
  through a re-export tuple that the 07-28 excavation trimmed, and main.py's L2
  guard swallowed the ImportError into a per-start WARNING. Fix built and
  tested (main v4.5, alert_manager v1.7, check_versions v4.5,
  tests/test_l2_import_contract.py — suite 42/42), deploying after the close.
  **W.1 quarantines the day's conviction data** — it is off-engine and must not
  feed any fit until the contaminated window is bounded from the logs. W.2
  opens the systemic question: two silent-degradation faults in one morning,
  both invisible because trading continued. That pattern, not either bug, is
  the go-live risk.
- **v3.3 — 2026-07-29 — new item V on the Thu Jul 30 punch list: `push.sh`
  resolves its target by scanning `$HOME` and ignoring the caller's cwd.**
  Surfaced when a push from the correct directory reported the wrong repo's
  remote. Both remotes were correct — the tool had cd'd elsewhere. Dormant now
  that the borrowed futures checkout is off the box, which is exactly why it is
  written down: nothing will show it is still broken until the next time two
  projects share `$HOME`. Same file ships in futures_trader_v1.
- **v3.2 — 2026-07-29 — check_versions v4.4 (glyph fix) + a path convention
  worth writing down.** First control-side run of v4.3 surfaced an inherited
  defect: status glyphs were emitted as literal `\u2713` / `\u2717` (bash
  `echo` does not interpret `\u`), so they have never rendered. Fixed as
  **v4.4**, literal UTF-8, no logic change — it rides the same commit as v4.3
  since neither has been pushed. Also recorded, because it has now cost one
  failed command: **the control checkout is `~/options-trader-v3`; the bot
  boxes are `~/options-trader`.** Control-side verification commands take the
  suffix, fleet/menu commands do not.
- **v3.1 — 2026-07-29 — JUL 29 DAY CLOSED; T.1/T.3 FOUND ALREADY RESOLVED AT
  HEAD.** Working the day's items against a fresh clone (working-agreement
  rule 8) found T.1 and T.3 were **already shipped in the 07-22 defect-T pass**
  and never registered here: the old `test_paper_entries_mirror_live_friction`
  no longer exists — replaced by `test_paper_entries_book_the_mark_by_default`
  + `test_paper_friction_knob_applies_to_every_path`, which is exactly T.1's
  HOW clause — and the suite runs **37/37 green** at HEAD (the "36/36" target
  was stale; a test was added since). position_manager is at v3.9 (07-22) with
  the import gone and the removal changelogged. **U** was likewise 95% shipped:
  check_versions v3.1 (07-22) closed the fingerprint gap under the name "audit
  defect U" and v3.2–v4.2 extended it to 125 checks covering every item in U's
  list. The one genuinely missing piece — the README **parity invariant**
  (checkout commit vs origin HEAD) — is delivered today as **check_versions
  v4.3**, with a failure-count DONE banner (one greppable line per box on an
  option-23 pass) and a passed deliberate-failure test (token deletion → 2
  MISSING; diverged HEAD → PARITY RED). All three moved to Part 3 with
  evidence. Lesson standing: this file trailed the repo by a week on three
  items — an item's premise is re-verified at HEAD *the day it's worked*, not
  trusted from the file.
- **v3.0 — 2026-07-29 — HOW + VALIDATE AMENDMENT.** Every open item now carries a
  **HOW** (the proposed fix, concretely) and a **VALIDATE** clause naming the exact
  dataset *already collected* that will confirm or disprove the fix — trades.db
  observability columns (adx/conviction/flat-angle/level_strength/MFE-MAE),
  `signal_journal` jsonl (incl. vwap + price_vs_vwap, verified at HEAD),
  `chain_snapshots` (harvest v0.5.1 pulls them since 07-27), `session_labels.jsonl`
  (auto_label), the regime diary/replay, `conditional_tables`, the readiness
  journal, excursion reports, and the shadow corpus. Where the framework to
  validate a fix does **not** exist, a new instrumentation item is scheduled early
  enough to be in place before the fix it validates: **N.1** regime_log harvest
  (Jul 30 → validates L1.9, powers Aug 5 ADX reconstruction and the Aug 10 live
  churn watch) · **N.2** `rrr` + gate-block dispositions in the signal journal
  (Jul 31 build → validates E/F live via L3.2) · **N.3** `closes_beyond` captured
  on sweep trade rows (Jul 31 build → arms the Aug 18 reclaim-looseness verdict)
  · **N.4** paper-fill realism audit off the chain archive (Aug 14 → validates T.2
  and the R slippage default before any live fill exists) · **N.5** fill-latency
  telemetry on FillResult (Aug 20 build → the live-week dataset TC.2's
  stop-trigger decision requires) · **N.6** extended-hours-bars audit
  (Aug 6 → gates whether Overnight H/L is computable from the feed_store or needs
  its own capture). Capture-claims verified against HEAD 2026-07-29, not memory
  (working-agreement rule 8): harvest already at v0.5.1, so P5.1's Jul 30 slot is
  re-scoped from *build* to *deploy-verify + completeness manifest*.
- **v2.0 — 2026-07-29 — SCHEDULED REWRITE.** The whole backlog re-ordered into the
  sequence the work can actually be accomplished, with a target date per item, driven
  by the go-live clock: **live trading by the first week of September, full position
  sizes by mid-September.** Four ~2-week epochs, deliverables checkable daily
  (weekends included for builds/analysis — markets closed is when tester-first work
  is safest), and every trade-behavior-changing deploy lands **fresh on a Monday
  RTH.** Open items carry their original defect/observation IDs. The resolved
  register (A–D, G–H, L, N–R, V–Y and the resolved observations) is preserved in
  PART 3 in condensed form — resolution date + fixing versions + the why — so no fix
  gets quietly reverted; full forensic text lives in git history at the pre-v2.0
  commit of this file. Stale framing removed: the "Part 1 / Part 2 consolidated from
  README + OBSERVATIONS.md" structure is superseded by the schedule.
- v1.0 — 2026-07-28 — Consolidated from `README.md`'s defect register (items A–AA)
  and `docs/OBSERVATIONS.md`, both preserved verbatim.

**Status motif:** `✅ RESOLVED` · `🔄 IN PROGRESS` · `⚠️ OPEN` · `⬜ NOT STARTED / scheduled`

**How to read a v3.0 item:** the v2.0 scheduling text stands; **HOW** = the
proposed mechanism of the fix; **VALIDATE** = the evidence contract — which
*already-collected* dataset confirms or disproves it, and by what metric. A fix
whose VALIDATE clause points at a dataset that doesn't exist yet points instead at
the N-item that creates it, and that N-item is dated *before* the fix's own
decision date. Evidence decides; the schedule just makes sure the evidence is
waiting when the decision arrives.

---
