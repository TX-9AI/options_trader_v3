# docs/BACKLOG.md — v3.81


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

## PART 0.5 — DELIVERY LEDGER (added v3.56, 2026-08-04)

**One thread now owns build → test → deploy.** Every archive delivered from it
ships this file, so the ledger below is the running record of what has actually
moved and what has not. It exists because EV moves only when the backlog records
it, and this is now the sole place that record is produced.

**STATUS VOCABULARY — these are three different things and get named separately:**
`BUILT` = written and proven on the desk · `PUSHED` = on origin, control checkout
in parity · `BAKED` = live on the fleet boxes. A change that is PUSHED but not
BAKED is changing nothing about today's data.

| item | built | pushed | baked | evidence |
|---|---|---|---|---|
| **N.7 — entry snapshot capture** | ✅ 08-04 | ✅ 08-04 `0f78329` | ⬜ **Mon Aug 10** | control suite **146 passed / 1 skipped, rc=0** (read 08-04); ALL CANARIES GREEN; PARITY == origin; tree clean |
| **N.5 — exit ladder latency** | ✅ 08-04 | ✅ 08-04 | ⬜ **Mon Aug 10** | control suite **158 passed / 1 skipped, rc=0**; ALL CANARIES GREEN |
| **N.8 — no regime-flip exit on a stale book** | ✅ 08-04 | ✅ 08-04 | ⬜ **Mon Aug 10** | control suite green, ALL CANARIES GREEN |
| **W.2a — today's own swallows made audible + the alarm made specific** | ✅ 08-04 | ✅ 08-04 | ⬜ **Mon Aug 10** | silent count back to the 08-03 baseline of **87**; `--since` proven on three cases |
| **D.1 — bull/bear were the same token in THREE renderers** | ✅ 08-04 | ✅ 08-04 | n/a (report-only) | 16 rows re-rendered on control; ALL CANARIES GREEN |
| **AV.1 — the pooled gap read, with a legitimacy guard** | ✅ 08-04 | ✅ 08-04 | n/a (offline) | ALL CANARIES GREEN on control |
| **TC.4b-pre — does the impulse floor hold?** | ✅ v1.3 08-04 | ✅ 08-04 | n/a (offline) | **CONTROL RUN: impulse − control TERMINAL = −0.3% ±2.3%. Dead null.** See below |
| **PF.V — pitchfork variant sweep (§12 Q2)** | ✅ 08-04 | ✅ 08-04 | n/a (offline) | Answered: no-change. ACCEL/birth andrews 0.22 · mod_schiff 0.67 · schiff 3.61; adverse tine kills 81-97% in ALL THREE |
| **ORB.1 — ORB was gated by the stale entry block** | ✅ 08-04 | ✅ 08-04 | ⬜ **fleet reflash tonight** | control suite 216 passed, ALL CANARIES GREEN |
| **RPT.1 — report rollup (5 fixes, 2 repos)** | ✅ 08-04 | ⬜ | n/a (offline) | otv3 suite **223 passed / 1 skipped**; behavioural proof on all five |
| **BF.1 — the RTH guard was eating the backfill** | ✅ 08-04 | ⬜ | ⬜ **tonight's reflash** | 8/8 guard states proven; 2 sessions of sat-out tape at stake |
| **BF.2 — guard OFF by default (operator directive)** | ✅ 08-04 | ⬜ | ⬜ **tonight's reflash** | v1.4, both modes proven |
| **BF.3 — THE REAL CAUSE: `--once` hung on the v3.9 RTH gate** | ✅ 08-04 | ✅ 08-04 | ✅ baked | **CONFIRMED WORKING on the box** |
| **BF.4 — session guard reconfigured: one predicate, guard back ON** | ✅ 08-04 | ⬜ | ⬜ **next bake** | suite 229 passed; 8/8 pull states |
| **AI.1 — condor approach telemetry on every plan death** | ✅ 08-04 | ✅ 08-04 | ⬜ **next bake** | 10 tests; item AI becomes answerable |
| **N.9 — contract telemetry (premium decomposition)** | ✅ 08-04 | ⬜ | ⬜ **Mon Aug 10** | suite **247 passed / 1 skipped**; 8 tests; log-only |

**⚠️ TWO READINGS I GOT WRONG ON 2026-08-04, recorded so they are not repeated:**
1. **The `[L2 c=` vs `[v13]` counts are NOT a same-day measurement.** `bot.log`
   accumulates across sessions — TSLA's most recent `NOT committing` line was
   dated **08-03** — so the 11-vs-4 "bimodal split" I read off those counts is
   an artifact of differing log ages and restart times, not of today's engine
   mix. **The correct instrument is the `engine` column on `regime_log` inside
   each box's trades.db** (main v4.8 stamps it; harvest already pulls the DB),
   scoped by date. That is exactly the filter **W.1** defines, and it is a
   query, not a grep.
2. **The stale-block counts alone read as a live counter.** Timestamps showed
   every block fell in **09:35-09:41 ET** and nothing since. Read timestamps
   before reading a trend into counts.

**⬜ NEW, SMALL, NOT YET BUILT — the `NOT committing` warning asserts more than
it checks.** It prints *"This is NOT the designed opening warm-up"* on the
strength of `df_1m` alone. But the designed opening warm-up has more dimensions
than the 1-minute frame: `_ranging` returns None until ATR exists, which needs
`ATR_PERIOD` 5m bars (~75 minutes of session — the 2026-07-25 finding). So at
09:30:02 with `df_1m=60` the message rules out one cause and announces the
conclusion for all of them. Every episode this session sat at the bell, counts
were 0-6 per box, and RECOVER followed — i.e. it IS the open warm-up, via a
dimension the message does not test. **Reword to name the missing dimensions it
actually observed rather than asserting a category.** Log-only, one string.

**⬜ N.7's OWN REMAINING STEPS, in order:**
1. ✅ **Suite result read 2026-08-04: `146 passed, 1 skipped, rc=0`.** Worth
   keeping the note: the `tail -20` had caught only the `check_versions` tail,
   and the grep that recovered it ALSO matched the word `failed` inside file
   headers and changelog prose in the same log — output that renders like a
   failure while meaning nothing of the kind. `rc=` is the load-bearing token;
   anchor future greps to the summary line, not to bare words.
2. **Bake Mon Aug 10** with the calibration deploy (devtools 25 bake-only or 23),
   verifying commit parity BEFORE restart.
3. **Verify capture on the first baked session** with the option-14 count — read
   the PER-BOX line, not the tally. Directional captured with `legs_captured=0`
   is the ctx regression the absence canary exists for.
4. **Nothing consumes the column yet.** The bake-off harness is TC.2 work and
   stays where the roadmap puts it. Do not read the first payloads as a result.

**✅ THE CONDUCTOR TELEGRAM GAP — CLOSED 2026-08-04, VERIFIED ON THE BOX.**
`UNIT_ENVFILE=1 · ENV_TOKEN=1 · ENV_CHAT=1 · TOKEN_LEN=47 · CHAT_LEN=11`, the
last `cannot send` in the journal is **Aug 03 20:29:34** (before the AX
installer was re-run), and the 08-03 conductor's warnings — backfill, swallow
audit, VWAP ledger, EVM, readiness — all arrived in Telegram at 16:59. Item AX
worked. Two corrections to my own account of it: it was **fixed in source on
08-03**, not open, and `grep -c` on the `.env` could not have told a present
variable from an empty one — the LENGTHS did.

---

## PART 1 — THE SCHEDULE (open items, in accomplishment order)

> **ID SPLIT 2026-08-04 (v3.52).** `A2.6` and `L1.9` were each TWO DIFFERENT
> ITEMS sharing one ID. `evm_status` keys on the ID token, so each pair counted
> twice in BAC/PV/overdue AND — the reason this is a defect and not untidiness —
> marking either one ✅ would have satisfied the parser for BOTH, showing work
> resolved that nobody did. Split to `A2.6a`/`A2.6b` and `L1.9a`/`L1.9b`.
> **NOT YET DISAMBIGUATED:** bare `A2.6` and `L1.9` references elsewhere in this
> file (around lines 331, 391, 2808, 2836) predate the split and have not been
> re-pointed — they are flagged rather than guessed at, because the surrounding
> text does not say which member of the pair it means. Resolve them the next
> time either item is worked, and treat the two as separate until verified.


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

- `[DESK·DATA]` **AP — ◐ SOURCE BUILT 2026-08-01; the fork itself ripens on its own.
  The daily series now comes from OUR OWN TAPE, not a second feed.**
  §4.2 wants a daily fork at k=2 with R=40. `TIMEFRAMES["1d"]["candles"] = 10`,
  and ten daily bars cannot yield a k=2 triple with 5-bar separation. Worse than
  a missing fork: §6 names a daily rail within C*ATR of an hourly rail —
  CONFLUENCE — as the highest-value signal the overlay produces, so with one fork
  the paper's headline application could not be measured at all.
  **BUILT:** `day_trader_pro/daily_bars.py` v1.0 + `eod_conductor` **v1.11.0
  phase 5b** + 14 tests. Rebuilds `daily/<SYM>.csv` from the 1-minute tape
  `phase_harvest` already lands.
  **WHY NOT YFINANCE — the operator's objection is the decisive one.** It was
  purged for a large disparity against TastyTrade on low timeframes; it
  normalises on the highest, but a fractal pivot anchors on HIGHS AND LOWS, and
  daily H/L is exactly where a differing consolidated tape or pre/post-market
  inclusion shows up. Its "30 day" 1m pull caps at **21 sessions**. And the
  killer: **what happens when a fork INVALIDATES.** Re-anchoring selects a NEW
  triple and needs bars current AT THAT MOMENT — a manual pull is stale the next
  day, and a recurring one re-introduces the dependency the purge removed. Any
  yfinance arrangement here is a band-aid. Aggregating our own tape extends
  itself every night and keeps the fork reconstructible from tape, which is what
  its determinism rests on.
  **The agreement-check script was proposed and then DROPPED** — once the series
  comes from our own tape, that test's result changes no decision either way, and
  building it would put `import yfinance` back in the repo for no operational
  purpose. A check that cannot change a decision is not worth running.
  **DESIGN CALLS worth knowing before reading the series:** it REBUILDS rather
  than appends (idempotent, and self-heals when a session is backfilled late,
  which an append gets silently wrong forever); it runs **after phase_backfill**,
  not after harvest, because backfill fetches candles for days the boxes never
  handed over; sessions under 300 of ~390 minutes are marked `partial=1` rather
  than dropped, because a short session's high/low are not the session's and a
  pivot anchored on one is an artifact — but a dropped session is a hole nobody
  can see.
  **⬜ WHAT IS STILL OPEN.** (1) HISTORY: tape starts ~07-13, so ~15 sessions —
  the floor for a k=2 triple (P2 confirmed at index 14) with ZERO margin.
  Comfortable (~29) by the Aug 21 freeze, which is when PF.4 wiring happens
  anyway, so the fork ripens on the schedule the overlay needs it. The phase
  emits a conductor WARNING every night until it clears. Do not "fix" the short
  history by reaching back to a second feed. (2) DISTRIBUTION: the series is
  built on CONTROL. PF.1/PF.2/PF.3 are offline work that runs there, so that is
  sufficient today — getting it onto the bot boxes is a **PF.4** problem and is
  NOT solved.

- `[DESK]` **AQ — THE FLEET MAY BE DISPATCHING THE WRONG THETA SIGN INTO THE
  PAUSED-TREND STATE, and no strategy exists that wants it.** Opened 2026-08-01
  from the A2 partition result. `tests/a2_excursion.py` v1.0 built to settle it.
  **✅ RE-RUN ON THE CLEAN CORPUS 2026-08-01 (AT cleared). These numbers are
  final; the provisional set is superseded.** Headline **3.98%** (5,985 / 150,517).
  Grid, violation rate ±95%:
  `OPEN   CONT 9.89±0.59   FLAT  3.60±0.91   REV 9.55±0.49`
  `DECAY  CONT 5.91±0.43   FLAT 13.78±1.53   REV 5.98±0.37`
  `CLEAN  CONT 1.46±0.12   FLAT  3.55±0.45   REV 1.83±0.12`
  **ONLY THE OPEN ROW MOVED** against the contaminated run (CONT 10.62→9.89,
  FLAT 5.41→3.60); DECAY and CLEAN barely shifted. v2.1 altered only the opening
  24 ticks per symbol-session, so that is the fix doing exactly what it claimed
  and nothing more — independent confirmation it was correctly scoped.
  **THE DECAY×FLAT HUMP SURVIVED AND SHARPENED: 13.78%**, still the highest cell
  in the grid, now with BASELINE SHOULDERS ON BOTH SIDES (3.60 → 13.78 → 3.55).
  **H2 FLIPPED TO NOT SUPPORTED** — flat-open mornings 3.60% vs 3.55% midday, so
  there is NO morning excess at all on gapless days and no "opening drive" in the
  plain sense. Which makes the hump unambiguous: **on a flat-open day nothing
  happens at 09:30; the first real move arrives mid-morning and A2 spikes with it.
  The tradeable window on those days is ~10:40-12:00, not the open.**
  **H3 IS PARTIAL, NOT DEAD — correcting my own earlier call.** I claimed it was
  dead on two grounds, the second being that the ADX medians pointed the wrong
  way. On the clean corpus they point the RIGHT way: OPEN row CONT 52.4 > FLAT
  50.2 > REV 46.6, monotone, exactly what the ablation predicted for
  continuation-inflation and reversal-suppression. The reversal RATE deficit still
  does not appear, so PARTIAL stands — but "dead" was a contaminated number read
  confidently.
  *Superseded provisional text follows.* 150,517 ticks joined, 4.14%
  violations (supersedes 4.02%). H1 horizon SUPPORTED, H2 drive SUPPORTED, H3 gap
  **dead as a cause** — the reversal-gap deficit never appeared, and the ADX
  medians point the wrong way (CONT 52.0 < FLAT 53.5, when a continuation-gap
  inflation would need CONT highest). A2 names a real state. **Gap class proxies
  for DAY TYPE, not for an ADX perturbation** — gap days are trend days,
  flat-open days are range-ish.
  **THE UNFLAGGED FINDING, and it is the strongest evidence for H2:**
  DECAY×FLAT **13.88%** is the highest cell in the grid, ~6σ above OPEN×FLAT.
  FLAT is the ONLY class that HUMPS (5.41 → 13.88 → 3.65); CONT and REV both
  decay monotonically. On a flat open there is no overnight repricing, so the
  day's first directional move is DISPLACED to ~10:40-12:00 and the violations
  follow it. Move the drive in time and the violations move with it — nothing
  else predicts a displaced hump.
  **THE OPERATOR'S FRAMING, which is what the new tool measures:** *"If price is
  going NOWHERE in that environment, that should be worked into our STOP logic.
  If price is expected to go SOMEWHERE, let's guess WHERE and trade it."* And:
  *"It should be relevant to whether we are long or short theta."*
  **ONE NUMBER CANNOT ANSWER BOTH.** Signed drift answers the long-theta question
  and tells a condor NOTHING — a session that runs +2% then -2% has zero drift and
  would have blown through both wings. So:
  theta NEGATIVE (continuation debit-directional, sweep naked OTM ~0.20d, orb) →
  SIGNED return in the TRENDING direction plus time-to-arrive, because decay is
  the clock it races. theta POSITIVE (iron_condor, butterfly) → MAX ABSOLUTE
  EXCURSION and its DISTRIBUTION. **The butterfly is why THETA SIGN and not
  credit/debit is the correct axis** — it is a debit structure that is
  theta-positive near the body.
  **THE HYPOTHESIS:** if paused_trend predicts LOW excursion, the fleet sends the
  WRONG theta sign into it. A2 ticks have TRENDING > 0.5, so argmax tends TRENDING
  → **continuation fires and pays decay to sit in tape that is not moving**, while
  condor and butterfly are gated to RANGING/COMPRESSION and locked out of exactly
  the state they would want. A mechanism-level candidate for continuation
  standalone's -$2,024 at 46% WR that has nothing to do with its entry conditions.
  **THE DISTRIBUTION IS A STRIKE RULE**, not just a verdict: p90 of |excursion|
  says where a short strike belongs, priced from the state's own behaviour rather
  than a fixed delta or a BB anchor — the pitchfork paper's rail-anchored-strike
  argument arriving from a different direction and available sooner. And mean
  ADVERSE excursion is the floor under a non-noise stop, which bears directly on
  the premium-relative stop defect (25% of a $0.70 credit is 17.6c, inside the
  0DTE bid/ask band).
  **CONDITIONING — corrects a2_partition's own closing line.** It says evaluate on
  CLEAN×FLAT as "uncontaminated". That cell is uncontaminated by GAP but SELECTED
  ON DAY TYPE, and FLAT runs hotter in every window (CLEAN 3.65% vs 1.49/1.91).
  Judging the state only there measures it on the least-trending days in the
  corpus, exactly where a paused trend is least likely to resume. Use CLEAN across
  ALL THREE classes with gap_class as a COVARIATE — n~95k, not ~6.5k.
  **EPISODE DURATION IS A PREREQUISITE, found by running the tool rather than
  reasoning about it.** The forward window spans N bars but nothing guarantees the
  STATE persists across them; on a planted corpus, violations at HALF the control
  volatility came back as p90 0.248% vs 0.245% — no signal — because the windows
  overlapped non-violating tape. The tool now reports the duration distribution
  FIRST and warns when a horizon exceeds the median episode. `--persistent-only`
  is the clean version at the cost of sample. **Do not read any horizon longer
  than the median episode as an edge.**
  **⬜ THREE OUTCOMES, ALL USEFUL.** Resumes → long-theta entries have a target.
  Flat → A2 is honest, correctly identified, and worth nothing; A2.5 becomes a
  logging nicety and the invariant gets restated rather than acted on. **Negative
  → the "pause" is EXHAUSTION**, a top/bottom, which inverts the item's assumption
  and is worth more than a resume.
  **⬜ THE DESIGN GAP.** If excursion is HIGH but drift is ~zero, that is a LONG
  GAMMA / direction-agnostic environment and **nothing in the fleet trades it** —
  all five strategies are directional or short-vol. If excursion is LOW, the
  expression is a **DEFINED-RISK WIDE IRON CONDOR**, where spread width is the
  sizing dial and `compute_condor_leg_size` already yields a real max_loss so the
  session caps and session_guard keep their denominator.
  **⬜ UNDEFINED-RISK STRUCTURES ARE OUT OF SCOPE — DECIDED, not deferred.** The
  margin account permits selling strangles, but SPX's nominal size (~$640k per
  contract at a 6,400 index) makes a naked strangle one indivisible bite far
  larger than the per-trade risk budget. The operator's call: that constraint is
  PROTECTIVE and is not to be engineered around. **Do NOT build the broker-margin
  denominator into the risk layer** — it existed only to make undefined risk
  sizeable, and the risk layer being unable to size a naked short is a FEATURE.
  The risk layer has exactly two sizing paths and both assume defined risk
  (`compute_size`: max_loss = premium paid; `compute_condor_leg_size`: max_loss =
  (width - credit) × multiplier); a naked short has neither a debit nor a spread
  width, so `max_loss` — which feeds the session caps and session_guard — would be
  wrong or zero and break the whole downstream chain silently.
  **SEQUENCING: this goes BEFORE A2.5.** Building a live factor column for a state
  with no forward edge is work spent to confirm nothing.

- `[DESK]` **AR — THE POOLED MEAN WAS THE WRONG STATISTIC, AND THE FORK IS THE
  RIGHT PREDICTOR. `tests/a2_rail_drift.py` v1.0.** Opened 2026-08-01 from the
  excursion result.
  **✅ RE-RUN ON THE CLEAN CORPUS 2026-08-01 (AT cleared).** Episode duration and
  Predictor 1's negative both HELD — drift shows NO EDGE at every horizon and
  every elapsed bucket, so **A2.5 as a live drift factor remains unsupported.**
  Excursion FIRMED UP: violation p90 sits below control at ALL THREE horizons
  (0.166/0.172, 0.215/0.220, 0.285/0.296), consistent and monotone where the
  contaminated run flip-flopped. Small (~3%) but no longer noise — though the
  missing confidence band on that verdict is still a real defect (below).
  **USABLE NUMBERS, clean:** stop floor (mean adverse excursion) **0.027% /
  0.046% / 0.075%** at 2/3/5 bars; strike distance p90 **0.166% / 0.215% /
  0.285%**. A 17.6c stop on a $0.70 credit still fires far inside the floor.
  **RAIL DRIFT UNCHANGED** — 1,013 ticks with no usable fork, Predictor 2 REFUSED
  at n=78. It reads the 1m tape, not the corpus, so the regen could not touch it.
  **AS is the blocker there, not data.**
  *Original text follows.*
  **WHAT THE EXCURSION RUN ACTUALLY SAID.** Median paused-trend episode is **2
  bars** (p50 2 / p75 6 / p90 12 / p95 17 / max 48, n=1309) — a flicker, not a
  regime. Diluted horizons showed nothing. `--persistent-only` at 2/3/5 showed
  BOTH statistics moving monotonically in the same direction: excursion p90 vs
  control 0.151/0.172, 0.190/0.220, 0.231/0.296 (−12%, −14%, −22%) and drift
  +0.0047 / +0.0080 / **+0.0184 (clears)**. Two independent measures moving
  together across three horizons is not noise.
  **BUT `--persistent-only` CONDITIONS ON THE FUTURE.** To know the state holds
  for the whole window you must know bars t+1..t+h are also violations, which is
  not knowable at t. It says "episodes that LASTED >= h bars behaved this way",
  NOT "when you see a violation, expect this" — the same class of error as
  anchoring a fork at P2's own timestamp (§4.4). **Do not build a gate on that
  number.**
  **WHY THE POOLED DRIFT WAS SO SMALL — my error, not the data's.** a2_excursion
  averaged one scalar across every instance, but those instances sit in trends of
  DIFFERENT SLOPES POINTING IN OPPOSITE DIRECTIONS. A +0.4%/hr uptrend averaged
  against a −0.4%/hr downtrend gives zero. The +0.0184% is the RESIDUE of that
  cancellation, not what any instance did. Stop averaging across trends; predict
  per instance.
  **THE OPERATOR'S POINT, and it closes a loop:** a trend line taken out to a
  moment in time IS a drift prediction. `rail_price(t) = anchor + slope*(t −
  anchor_time)` — **PF.1 already computes it.**
  **TWO PREDICTORS, one tool, both knowable at the tick:**
  **(1) ELAPSED PERSISTENCE** — how long the state has ALREADY run. Zero forward
  conditioning, so a live gate could use it, and it maps onto the existing arming
  state machine. Buckets 1 / 2-3 / 4-7 / 8+ against a no-violation control.
  **(2) MEDIAN-LINE DISPLACEMENT** — split in two because they can disagree:
  **2a SLOPE** (does price move at the rate the ML predicts?) and **2b REVERSION**
  (Andrews' actual teaching is that price RETURNS to the ML, so the signed target
  is `ML(t) − price(t)` — a PER-INSTANCE number, which is what "guess WHERE" asks
  for). Reported as regressions with coefficient + r2 + magnitudes, not means.
  **FORK CONSTRUCTION IS HONEST:** hourly (k=3) from 1m tape resampled and
  concatenated ACROSS SESSIONS (§4.3's R=40 is ~6 sessions at ~7 bars/session),
  rebuilt only when an hourly bar closes, and `build_fork` is called with
  `now_idx` = the last COMPLETED hourly bar so the confirmation lag holds.
  **A SELF-CORRECTION WORTH KEEPING:** the smoke run returned a 2a coefficient of
  +41 and I called it a scaling bug. It is not — checked directly, the fork's
  median line was nearly flat (−0.0023 price/hour) while the tape moved ~93x
  faster, so the prediction sits far under the noise. The formula was right. The
  tool now prints median |predicted| vs |realized| alongside every regression, so
  a SCALE MISMATCH cannot be misread as a broken formula the way I misread it.
  **KNOWN WEAKNESS:** the hourly ML barely moves across a few 1-minute bars, so
  2a has little to work with — **2b is the load-bearing test at these horizons.**
  Re-run 2a when the DAILY fork ripens (AP / daily_bars.py, ~Aug 21), since a
  daily fork carries far more slope per window.
  **SCOPE:** this tests whether the fork PREDICTS anything. It is UPSTREAM of the
  §9/PF.3 condor-strike head-to-head, not a second consumer competing with it —
  rail-anchored strikes only make sense if the rail says something true about
  future price, and testing that directly is cheaper than a credit differential.
  Builds no consumer, gates nothing.
  **⬜ ALSO OPEN, from the excursion run:** a2_excursion's excursion verdict
  compares p90 POINT ESTIMATES with no confidence band, which is why it flipped
  sign across horizons on the diluted run — it needs a bootstrap CI before its
  STILLER/NOT-STILLER language means anything. And favorable/adverse is reported
  for violations only with no control, so the STOP LOGIC number is not yet shown
  to be state-specific. The max-excursion gap (0.870 vs 2.479) is a SAMPLE-SIZE
  artifact — 53x more control ticks — and p95 is nearly identical (0.394/0.396).
  **⬜ USABLE NOW REGARDLESS of how the drift question resolves:** mean adverse
  excursion 0.019% / 0.033% / 0.049% at 2/3/5 bars (~1.2 / 2.1 / 3.1 SPX points)
  is the structural floor under a non-noise stop — a 17.6c stop on a $0.70 credit
  fires far inside it. And p90 excursion 0.231% over 5 bars (~14.8 SPX points) is
  a strike distance derived from the state's own behaviour.
  **⬜ NOT SUPPORTED:** the wrong-theta-sign hypothesis for continuation's
  −$2,024. Excursion is not materially lower on the diluted (real-time-knowable)
  measurement, so continuation is not being handed unusually still tape.

- `[DESK]` **AS — ✅ RESOLVED 2026-08-03. PF.1 HAD NO LIFECYCLE, SO I USED THE FORK AS A PER-BAR
  INDICATOR — the one thing the persistence mandate says it is not. My bug, and
  it is upstream of every pitchfork number taken so far.** Opened 2026-08-01.
  **WHAT THE AUDIT ACTUALLY SHOWED.** 29 symbols, 95-111 hourly bars each, 2,297
  build attempts, **156 forks built (6.8%)**. Rejections: SEPARATION 915 (39.8%),
  STRUCTURAL_bull 637 (27.7%), STRUCTURAL_bear 491 (21.4%),
  FEWER_THAN_3_ALTERNATING 77 (3.4%), SIGNIFICANCE 21 (0.9%).
  **6.8% IS THE BIRTH RATE, NOT THE COVERAGE RATE.** `build_fork` is STATELESS —
  it recomputes from scratch at every index. But **§5.2 says a fork HOLDS UNTIL
  INVALIDATED**; that is the entire reason it is a persistent object rather than
  an indicator. PF.1 deliberately deferred lifecycle ("this file computes geometry
  and stops"), and then `a2_rail_drift` called build_fork per hourly bar and used
  the result only when it returned non-None. **156 births across 29 symbols is ~5
  anchor events per symbol in three weeks — entirely reasonable for a persistent
  object.** With lifecycle, one fork born at hour 20 covers hours 20 → invalidation,
  which can be days. Coverage should go from 6.8% to near-continuous and
  **AR's Predictor 2 starvation (n=78, REFUSED at every horizon) likely
  disappears without touching a single threshold.**
  **MY AUDIT'S VERDICT WAS ALSO MIS-BINNED, corrected in v1.1.** It swept
  STRUCTURAL_* into "filter tightness" and printed "FILTER TIGHTNESS (2064 vs
  77)". `P2_not_above_P0` does NOT mean a threshold is too tight — it means the
  last three pivots are not a directional structure, a CORRECT rejection of chop
  with no parameter behind it. Honestly re-binned: **~52% no qualifying structure
  exists** (STRUCTURAL 1,128 + fewer-than-3 77), **~41% parameter-sensitive**
  (SEPARATION 915 + SIGNIFICANCE 21), 6.8% built. Three bins now, and the tool
  prints the birth-vs-coverage caveat every run.
  **WHAT IS GENUINELY WORTH EXAMINING AFTER LIFECYCLE — and it may not be a
  parameter either.** SEPARATION at 39.8% interacts with the UNIQUENESS rule: the
  implementation takes the three MOST RECENT alternating pivots and tests them, so
  one close pair kills the fork outright rather than falling back to an older
  qualifying triple. §4.3.5 reads *"the three most recent confirmed alternating
  pivots SATISFYING 1-4"* — which arguably means scan back for the most recent
  triple that satisfies the filters, not take-the-last-three-and-test. That is an
  IMPLEMENTATION READING, not a threshold change, and it stays a deterministic
  pure function with no search or best-fit. It could account for most of the 39.8%.
  **ORDER OF OPERATIONS, and the middle step is the point:**
  1. Build **§5 LIFECYCLE** — hold-until-invalidated, with the four invalidation
     conditions (structural break beyond P0; adverse tine break N=2 closes past
     the COUNTER-trend tine by >= 0.25 ATR; supersession by a newer qualifying
     triple with materially different geometry; staleness OFF by default). Note
     §5's key asymmetry: **breaking the TREND-SIDE tine is ACCELERATION, not
     invalidation** — never kill a fork on strength.
  2. **Re-run this audit and a2_rail_drift.** Coverage, not birth rate.
  3. **ONLY THEN** look at separation/uniqueness. Loosening anything before step 2
     would be tuning around a bug I introduced.
  **DO NOT loosen any §4.3 prior yet.** §10 names the ten-parameter surface as a
  headline overfitting risk, and right now we would be fitting to compensate for
  missing lifecycle rather than to anything in the tape.
  **CONSEQUENCE FOR AR:** its Predictor 2 result is a NON-RESULT, not a negative.
  The median-line question has never been measured. Predictor 1 (elapsed
  persistence) IS a real negative and stands — 12 cells, n 376-462 each against
  ~98k control, no edge anywhere — which means **the `--persistent-only` edge was
  look-ahead exactly as suspected, and A2.5 as a live drift factor is not
  supported.**

- `[DESK]` **AU — ✅ THE BLIND ALERT WAS UNSENDABLE IN PRODUCTION, AND THE DRILL
  BUILT TO CATCH THAT LIED FOUR TIMES BEFORE THE TRUTH GOT OUT.** 2026-08-01,
  amends **AL**. Now verified end to end on 29/29 boxes: both the blind alert and
  the recovery notice reach Telegram, and the drill asserts it rather than
  asserting itself.
  **THE PRODUCTION DEFECT, which is the part that mattered.** `TelegramSender`
  posts with `parse_mode="HTML"`, so ANY unescaped `<`, `>` or `&` makes Telegram
  reject the whole message with a 400. The blind alert interpolates forensic
  fields from `record_blindness` AND live position descriptions from trades.db —
  either can contain those characters. **Worse, main.py's own fallback string was
  `"<position read FAILED — check manually>"`**, so a DB failure DURING a blind
  alert produced an unsendable alert: the page died exactly when two things had
  gone wrong at once, which is when it matters most. `alert_manager` **v1.10**
  escapes in `_send`, so every alert is covered rather than the two that happened
  to be under inspection. Verified first that nothing in notifications/ uses
  intentional HTML markup, so no existing message changes appearance.
  **THE FOUR LAYERS THAT HID IT.** Every one reported success:
  1. **devtools 56 ran bare `python3`** — system python on the boxes has no
     pandas, so the drill died at IMPORT on all 29. Third interpreter mismatch of
     the day (day_trader_pro pytest, this, and the 07-31 saga).
  2. **`; true` laundered the exit code.** Added to satisfy the exit-0 fan-out
     convention, it discarded the drill's real return, so the menu printed
     "29/29 succeeded" while nothing ran. stderr was not captured, so the
     traceback vanished and every box showed "(no output)".
  3. **`AlertManager._send` discarded a boolean that already existed.**
     `TelegramSender.send()` has returned success/failure since v3.0; `_send`
     threw it away, so no caller could distinguish "sent" from "silently
     disabled". **Had that one boolean simply been returned, this would have been
     one step instead of five.**
  4. **The drill hardcoded `check("sent the DRILL blind alert", True)`.** My line.
  **AND A FIFTH, environmental:** `setup_ec2.sh` bakes TELEGRAM_TOKEN /
  TELEGRAM_CHAT_ID into the systemd unit as `Environment=` lines. systemd hands
  them to the SERVICE; a non-interactive SSH command inherits none, so
  `telegram_configured()` was False and `send()` returned False logging at DEBUG.
  `blind_alert_selftest` **v1.2** now hydrates from the unit using the SAME
  fallback `day_trader_pro/verify_creds_remote.py::_env()` already uses — which is
  precisely why option 54 worked and this did not — and PRINTS that it recovered
  them, so a real environment difference is stated rather than papered over.
  **FIXES SHIPPED:** devtools **v1.26** (venv interpreter, `2>&1`, per-box verdict,
  and the menu now says READ THE PER-BOX LINE NOT THE TALLY); `alert_manager`
  **v1.9** (return delivery) then **v1.10** (escape); `blind_alert_selftest`
  **v1.1** (assert the real return, ask `telegram_configured()` BEFORE claiming
  anything sent) then **v1.2**; `main.py` fallback string; `check_versions.sh` gains
  `def _send(self, msg: str) -> bool` so a revert to the discarding form fails the
  version audit.
  **THE RULE THIS EARNS, and it generalises past Telegram:** *a green produced by
  a laundered exit code is worse than a red.* `; true` may stop a fan-out
  discarding output, but it must never be the only thing reporting success — the
  command has to print its own PASS/FAIL and stderr must be captured. And an
  alarm-tester that cannot observe its own failure is worse than no tester: it
  converts an unknown into a false assurance.
  **HONEST NOTE ON HOW THIS WAS FOUND.** Not by inspection — by the operator
  saying "I still did not get any telegram notifications" three separate times
  while the tooling insisted everything passed. Each fix revealed the next layer.
  The tooling was never going to surface it alone.

- `[DESK]` **AW — THE HOURLY FORK IS NOT A LEVEL. RE-SCOPE PF.3, THE v4.0 GATE,
  AND THE L1 CORROBORATOR ON MEASURED COVERAGE.** 2026-08-03, from the first run
  of `pitchfork_filter_audit` v1.2 and `a2_rail_drift` v1.1 through **AS**'s
  lifecycle.
  **WHAT THE LIFECYCLE FIXED.** Predictor 2 went from REFUSED at n=78 to
  reporting at **n≈210**; no-fork ticks fell 1,030 → 878. So the per-bar
  `build_fork` rebuild WAS suppressing it, exactly as AS diagnosed.
  **WHAT IT DID NOT FIX — coverage is 10.1% mean, 5.3% MEDIAN, 0.0% min** across
  29 symbols, against a 6.8% birth rate. Only ~1.5x, not the 33x a synthetic
  fixture suggested. **Half the symbols carry a fork under 5% of the time and
  some never have one.** The answer to "my bug or the data" is BOTH.
  **⛔ THIS KILLS THE L1 CORROBORATOR at the hourly timeframe.** An input absent
  ~90% of the time makes a two-mode classifier whose behaviour depends on fork
  AVAILABILITY rather than on the market. §7 wave 4 (`setup_scorer`, L1
  corroborator, L2 weight) stays post-freeze, but the L1 half is now blocked on
  coverage, not on calibration. NOTE the distinction that matters: `setup_scorer`
  grades a setup ALREADY selected, so it changes grade and size but NOT which
  trades exist — comparable before/after. Anything feeding `regime_confluence`
  changes argmax, hence which strategy fires, hence the trade population, and
  every counterfactual (A2's 3.98% baseline, PF.3's credit) loses its control.
  **"Corroborates, never labels" is softer than it reads: a score that feeds
  argmax defines the regime in the only sense that is operationally real.**
  **⛔ 2b REVERSION IS A CLEAN NULL.** Coefficients +0.002 / +0.001 / -0.004,
  r² ≈ 0.001 at every horizon. **Price does not return to the median line.** That
  was the load-bearing test and Andrews' central claim, and on this corpus it is
  not there.
  **⛔ 2a SLOPE IS DEAD AT MINUTE HORIZONS FOR ANY TIMEFRAME.** The prediction is
  4-9x smaller than the noise it sits in. And the reasoning generalises: a DAILY
  median line moves even less per minute, so this is not "the hourly fork failed",
  it is "slope prediction over 3-10 minute horizons is the wrong question for a
  structural object".
  **⬜ EXHAUSTION IS NOW THREE INDEPENDENT MEASUREMENTS, SAME SIGN**, and deserves
  a directed test rather than another footnote: Predictor 1 drift negative in
  EVERY elapsed bucket at all three horizons; 2a slope coefficient NEGATIVE at all
  three (-1.09 / -2.18 / -1.56) with r² RISING with horizon (0.005 → 0.030); and
  the earlier `--persistent-only` run negative before conditioning. None clears
  its bands alone. Three weak signals sharing a sign with a horizon-increasing r²
  is a different object from one. **It inverts A2.5's premise — if a paused trend
  EXHAUSTS rather than resumes, the trade is to FADE it.**
  **⬜ THE SPLIT THAT FOLLOWS — §6 already says it, the data now says why.**
  "Higher timeframe governs zone strength; lower timeframe governs entry timing."
  Measured, the hourly fork is SHORT-LIVED AND REACTIVE: ~9-bar median life,
  exceeded on the trend side in 22 of 33 births, no reversion, sub-noise slope.
  **DAILY → levels** (condor strikes, structural stops, opposite-tine targets) —
  a strike wants a level that does NOT move during the trade, so slow and stable
  is the feature. **HOURLY → touch events and entry timing** — short-lived and
  current is right for "price just tagged a rail", and **162 TOUCH events** is the
  one thing the hourly fork produced in quantity.
  **⬜ PF.3 MOVES BEHIND AP.** Condor strikes are a LEVEL question. Anchoring them
  on an object exceeded two-thirds of the time and dying every ~1.3 sessions would
  burn the measurement, not just the time — and §9 chose strikes precisely because
  a credit is one clean number. Wait for the daily series (~2026-08-21).
  **⬜ AND THE v4.0 GATE MOVES WITH IT.** The paper tags v4.0 at ">=2 consumers
  independently proven". With reversion and slope dead, EVERY surviving consumer
  is level-based and all of them want the slow fork. **The critical path to v4.0
  now runs through AP, not through more hourly work.**
  **✅ ALL THREE OF THE BELOW ARE NOW SPENT (2026-08-04). Results, in the order
  they are listed: (1) cause-of-death ANSWERED — 24 adverse tine (88.9%) vs 3
  structural (11.1%), lifetime p50 5 bars, so by this item's own pre-registered
  reading the N=2/D=0.25 priors are strangling a persistent object and the tape
  is not what is killing it. (2) TOUCH-OUTCOME STUDY run at 180 events — NOT A
  NULL, an ABSENT MEASUREMENT: zero of eighteen cells clears its own MDE and six
  are REFUSED at n=18. Reaching the largest h<=2 effect needs n~600, ~17x what is
  banked, so the hourly fork cannot answer the touch question at any sample
  reachable before the freeze — retired on POWER grounds, not evidence grounds.
  Its one real yield: the signed control REPRODUCES the monotone negative, so the
  original "the rail did not hold" was manufactured by the approach-side sign
  rule, confirming v1.1's hypothesis. (3) §4.3.5 UNIQUENESS READING built as
  pitchfork v1.2 and measured NEGATIVE on coverage — births 6.9%->35.7% and 163
  ->850 built, while lifecycle events were BYTE-IDENTICAL across both arms
  (BORN 34/TOUCH 180/INVALIDATED 27/ACCELERATION 22/SUPERSEDED 2). Cause: the
  scan reaches BACKWARD to older triples and `pitchfork_lifecycle.py:399` refuses
  any candidate whose p2.idx <= the spent-P2 running max, so the scan is
  structurally inert on the lifecycle path. Ships OFF. Whether that guard is
  right under the scan reading is a §5 lifecycle question, now open.
  ALL THREE POINT THE SAME WAY: AP AND THE DAILY SERIES.**

  **⬜ CHEAPEST NEXT ANSWERS, all available without waiting for AP:**
  (1) `pitchfork_filter_audit` **v1.3** now bins CAUSE OF DEATH and prints the
  lifetime distribution — 27 INVALIDATED on 33 BORN is fast for a persistent
  object, and mostly-adverse-tine means the N=2/D=0.25 priors are strangling it
  (revisit them) while mostly-structural means the tape genuinely broke it (priors
  fine). Opposite responses, so measure before touching anything.
  (2) **TOUCH-OUTCOME STUDY** — 162 events, joins with machinery we already have,
  and touches are what §5.2 calls the tradeable event. Highest yield available now.
  (3) **§4.3.5's UNIQUENESS READING** (from AS): scan back for the most recent
  triple SATISFYING the filters rather than take-the-last-three-and-test.
  SEPARATION is 39.8% of rejections. It is an IMPLEMENTATION READING, not a
  threshold change, so it does not touch §10's overfitting surface.
  **⬜ WATCH, not yet a finding: 22 ACCELERATION on 33 births.** Forks exceeded on
  the trend side two-thirds of the time suggests the channel is too NARROW for the
  move it describes — plausibly a Modified Schiff artifact, since §3.2 chose it
  precisely because Andrews runs steep. That is a VARIANT question (§12 open
  question 2), not a threshold one, and `build_all_variants` already computes all
  three in parallel so it is measurable whenever we want it.

- `[DESK]` **AY — THE GAP-DAY MISREAD: continuation fires into post-gap chop on a
  trend that already finished. Plus a SELECTION miss and an EXIT miss that the
  same session exposed.** Filed 2026-08-03 from the −$3,149.50 session and the
  operator's chart review.
  **WHAT THE TAPE ACTUALLY DID.** MSFT +4.93%, AMZN +4.58%, NFLX +2.26% — the
  ENTIRE move happened in the opening bar, then all three chopped sideways in a
  tight range for the rest of the morning. **The trend was complete before the
  first candle closed.**
  **WHY THE CLASSIFIER CALLS THAT TRENDING.** A 5% opening 5m bar spikes ADX, and
  TRENDING is measured on ADX-14 over 5m ≈ a 70-MINUTE window, so the gap DOMINATES
  the window for over an hour after the move is over. Result: **TRENDING_BULL
  labelled 30 times, −$2,943**, and continuation fired into chop repeatedly.
  **THIS IS NOT A NEW FINDING — IT IS THE CELL A2 ALREADY FLAGGED.** The clean
  partition put **CONT × OPEN at 9.89%**, the second-hottest cell in the grid
  outside the DECAY×FLAT hump. We measured the ambiguity weeks ago; today priced it.
  **AND IT IS NOT AN ODD DAY.** gap_backfill over 15 sessions: **CONT 40.4%, REV
  52.7%, FLAT 6.9% — gap days are 93% of session-symbols.** What was unusual today
  was the SIZE of the gaps, not the fact of them. This is the MODAL environment and
  the misread recurs constantly; today merely made it legible.
  **⬜ THE PLAN — measure the specific cell, gate nothing yet.** The fleet is
  deliberately permissive to collect a broad sample (see POSTMORTEM 2026-08-03),
  so the output here is a sharper QUESTION, not a tightening.
  **AV's 2026-08-13 revisit is re-aimed:** it was "does gap class separate
  outcomes"; it is now **"does ContinuationStrategy lose on CONT gap days in the
  OPEN window?"** — a single named cell with a mechanism behind it.
  `tests/gap_outcome_join.py --by strategy --window OPEN` already does exactly this
  join; the `--window` flag exists and matches a2_partition's buckets. **No new
  tool.** If the cell separates, the gate writes itself: continuation should not
  fire in the open window on a CONT gap day. If it does not separate, today was
  variance and we will have learned that cheaply.
  **⬜ SECOND MISS — SELECTION, not strategy. TSLA was never woken.** It ranked
  **#18 at sc 0.0704**, below the 13-symbol discretionary cutoff, and then produced
  a clean +3.49% leg (318 → 324, 10:30–11:15). **No exit or strategy fix reaches a
  symbol that never woke.** New question: how often does a JUST-MISSED symbol
  (ranks ~14–20) produce the session's best move? The tape exists for all 29
  symbols regardless of whether they woke, so the price side is historical — but
  the RANK is only archived from 2026-08-03 (conductor phase 5c). **Revisit
  ~2026-09-05**, same accumulation window as the sentiment study, and read them
  together since both come from the same archived report.
  **⬜ THIRD MISS — THE EXIT, and this is the one real defect.** MU WAS woken, the
  breakout through ~803 at 10:00 ran to ~830 by 11:00 — a **60-minute leg** — and
  the fleet took **6 trades at 2.8 min average hold for −$377.** It was in and out
  repeatedly during a move it had correctly identified.
  That is `bos_exit`'s signature: today n=21, realized **−9%**, MFE **+2%**,
  **giveback +11%**, −$2,757.50 = **88% of the day's loss.** Note the cumulative
  contrast — bos_exit over 40 trades is **57% win, +$477.55**, so it is NOT a
  broken exit; it inverted on one session. **THE TEST: after a bos_exit fires, does
  price CONTINUE in the trade's direction?** If it systematically does, BOS is
  cutting live moves rather than reading structure. Buildable now from tape +
  fleet_trades; no waiting.
  **✅ MEASURED 2026-08-03 — AND THE READING ABOVE IS WRONG. BOS IS NOT CUTTING
  LIVE MOVES.** `tests/post_exit_continuation.py` v1.0 asks the question giveback
  cannot: after an exit fires, does price keep going the trade's way? Signed by
  direction, `bos_exit` against EVERY other exit on the same tape, comparing
  absolute instants (exit_time is UTC, the tape is ET-offset).
  `  h= 5   bos +0.034% ±0.089 (n=17)   other +0.006% ±0.039 (n=167)`
  `  h=15   bos +0.117% ±0.202          other -0.042% ±0.066`
  `  h=30   bos +0.005% ±0.179          other -0.045% ±0.095`
  **No separation at any horizon.** So the -$2,757.50 was **GIVEBACK** (MFE +2%
  -> realized -9%), not early exit. **The candidate is the TRAIL, not the BOS
  trigger** — the opposite of what MU's six 2.8-minute trades suggested, and I
  filed that suggestion as the reading before measuring it.
  **⬜ UNDERPOWERED, NOT NULL — the distinction this week keeps earning.** Every
  bos_exit cell is smaller than its own minimum detectable effect (n=17, MDE
  0.18-0.41%). The h=15 gap of +0.159% would need roughly **n≈113** to resolve —
  about 5-10 more sessions at recent rates. What this says is "no effect larger
  than ~0.4%"; it cannot rule out something smaller. Re-run when bos_exit clears
  n≈100.
  **⬜ AND 41% OF ROWS WERE DROPPED: 157 of 379 had no tape at the exit instant.**
  Partly trades from 07-07..07-10 that predate the tape harvest, partly hard_close
  exits landing after the tape ends, partly the five sat-out symbols. That is a
  large enough hole that selection bias is possible, and it should be closed or
  characterised before this result is leaned on.
  **⬜ THE STRONGEST SIGNAL IN THE TABLE IS NOT BOS.** `max_loss` post-exit
  continuation runs **-0.065% -> -0.205% -> -0.341%** across 5/15/30 minutes on
  n=18 — monotonically negative, the only cell where the effect grows cleanly with
  horizon. **Price keeps moving AGAINST the trade after a max-loss exit**, i.e.
  the disaster stop is doing its job and getting out of positions that continue
  to deteriorate. Worth stating because the day's second-largest line item
  (-$1,958.50) is that exit, and this says it was right.

  **⬜ WHAT IS DELIBERATELY NOT ACTIONED:** the chop losses on the MSFT/AMZN/NFLX-
  shaped names (~$2,000 of the day). We let continuation fire into that on purpose.
  Recording it as a defect would delete the observation we paid for. **Today is a
  dense, clean sample of ONE environment — 78 continuation trades in post-gap chop
  — which is exactly what the permissive posture exists to collect.**
  **⬜ A PROCESS LESSON, recorded because it cost a day of attention.** The flicker
  was found first and four tools were built around it. It was worth **−$234**.
  `bos_exit` sat at **−$2,757** the entire time and was only weighed when the
  excursion report forced the comparison. **The postmortem's own two-bucket test
  should be applied BEFORE building, not after** — "how much did this cost?" is a
  cheaper question than any tool.

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
- `[DESK]` **A2.6a — ⬆️ PROMOTED 2026-08-01: BOTH TOOLS ARE BUILT, TESTED AND
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
- `[DESK]` **A2.6b — `gap_pct`: the overnight gap is never MEASURED, and
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
- `[DESK]` **L1.9a — bookmark tester proof.** Run against copies of real `ohlc/<date>/`
  folders; prove byte-inert on the diary for warm-irrelevant days and prove the
  EOD conductor chain is untouched. The conductor is finally flawless — it stays
  that way.
  **HOW/VALIDATE:** as L1.9 above — inertness fixture + N.1 agreement metric;
  conductor untouched proven by a full dry-run of the chain on the tester with the
  bookmark grafted onto a *copy* of validate_regime.sh, diffing every artifact
  path it writes.
- `[DESK→DEPLOY]` **M.3a — Dedicated Telegram bot for options-trader notifications.** Promoted from
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
- `[DESK·DATA]` **TC.4a (T+1wk) — readiness digest check.** `_trend_credit_spread` journal has
  been accumulating since 07-28; confirm fleet-wide capture is clean.
  **HOW/VALIDATE:** run `readiness_digest` over the harvested journal; per-symbol
  row counts > 0 on every traded box, impulse-SD distribution non-degenerate.
  Existing data; this IS the validation framework TC.4's bounds fit rides on.

**⬜ Tue Aug 4**
- `[DESK→DEPLOY]` **N.9 — ✅ 2026-08-04. CONTRACT TELEMETRY: the repo could say
  WHAT the premium did and never WHY. Log-only, bakes Mon Aug 10.**
  **THE GAP.** MFE, MAE, giveback, capture ratio and the floor sweep are all
  correctly denominated in PREMIUM — that part was right and an earlier read of
  mine calling them underlying-denominated was WRONG. What none of them carries
  is a CAUSE. A -27% floor stop is indistinguishable between *the underlying went
  against us*, *the underlying went nowhere and theta ate it*, and *we were right
  and IV collapsed*. Three causes, three fixes, one number — and on 0DTE a
  correct thesis that resolves slowly is a dud, which makes "was I right?" the
  wrong question and "was I right FAST ENOUGH?" the right one.
  **NOTHING NEW IS FETCHED.** `OptionContract` already carries bid/ask/mark/
  delta/gamma/theta/vega/iv; `OptionsChain` carries spot_price/iv_rank. The chain
  is polled every tick and these were read for strike selection and DISCARDED.
  **TEN COLUMNS, NOT TWELVE.** `entry_mark` and `chain_spot_at_entry` were cut
  from the first cut because **`entry_premium` and `underlying_entry` already
  hold those facts**. Two names for one value is how a report ends up quietly
  reading the stale one. Caught by reading the schema instead of assuming it.
  **NULL = NOT CAPTURED, and there are no defaults.** A `0.0` default would make
  every pre-v3.12 row look like a zero-delta entry.
  **CAPTURED AT BOTH FILL SEAMS** — directional entry AND condor leg — matched on
  the **OCC symbol**, not strike, because a condor's two legs share an underlying
  and a session. Both pinned by canary; a strike match turns a test red.
  **📊 AVAILABLE FOR REPORTING IMMEDIATELY.** Ordinary columns on `trades`, so
  every existing consumer can read them with no plumbing: `excursion_report`
  (40), `trade_report` (41), fleet consolidation (39), any pulled `trades.db`
  (16). They are queryable the moment the first baked session lands — the reports
  simply do not GROUP by them yet, which is a reporting choice and not a data
  gap. Documented in **MECHANICS "Contract telemetry"** with the column table and
  the four questions it opens.
  **⬜ WHAT IT UNLOCKS ONCE SESSIONS ACCRUE:** (a) per-trade attribution —
  `entry_theta` x hold gives decay in dollars, `underlying_entry` vs exit spot
  gives direction, residual is IV+gamma; (b) **A TIME STOP** — bucket that
  attribution by hold time and the crossover is where a correct thesis stops
  paying for itself; this system has no such exit today (`hard_close_15:45` is a
  session boundary, not a decay boundary); (c) the floor sweep's declared
  *"ASSUMES: no slippage"* becomes MEASURED via `entry_ask - entry_bid`, and is
  the basis for the paper-vs-live fill comparison from Aug 31; (d) whether the
  10:00-11:00 hole (-$319 on n=120, the worst phase, against the open's +$9,761)
  is post-open IV crush.
  **⚠️ ONE READING CAUTION, recorded at build time rather than discovered later:**
  `entry_delta` is a SELECTOR OUTPUT, not a market observation — the strike
  chooser picked it. "0.30-delta does worse" is partly a statement about the
  selector.
  **⬜ OPEN — EXIT-SIDE CAPTURE IS NOT WIRED.** `place_exit_order(record, reason,
  mark_price)` has **no chain in scope**, and plumbing one through a signature
  used everywhere was not worth doing days before the freeze. Columns exist and
  stay NULL. **Consequence for the first read: DIRECTION and THETA separate
  cleanly; IV and gamma stay merged in the residual.** Say "residual", not "IV
  crush", until it lands. Do it post-freeze, either by passing the chain or by
  capturing at the main-loop level where `ctx["chain"]` already exists.

- `[DESK→DEPLOY]` **AI.1 — ✅ 2026-08-04. WHY THE CONDOR TOOK NOTHING: 23 PLANS,
  23 DEATHS, 0 LEGS — AND THE ONE INSTRUMENT THAT EXPLAINS IT WAS UNREACHABLE.**
  **THE MEASUREMENT (fleet-wide, date-scoped):** plans **23** across 11 symbols ·
  `nofloor=0` · `vix_blk=0` · **cutoff fired 0 times** · every death on
  `CANCELLED before Leg 1`.
  **AND THE LIFETIMES KILL THE OBVIOUS EXPLANATION.** 1-94 minutes, **median
  ~30**, several 88-94. My first read — plans dying to one-tick label churn —
  is WRONG. These plans were alive across most of the 11:11-14:00 window and
  **price never came within the trigger distance once, on any of them.** The
  cancel is incidental; the plan was never going to fire before it.
  **THAT IS ITEM AI, now with a number behind the mechanism:** *"0.65 of that
  distance lands well OUTSIDE the band. So the plan needed a breakout-sized move
  during RANGING, a regime defined by the absence of one."*
  **THE INSTRUMENT EXISTED AND WAS BEHIND THE WRONG DOOR.**
  `max_price_seen` / `min_price_seen` are tracked from a plan's first tick and
  `_abandon_past_cutoff` reported the approach fractions — **only on the cutoff
  path, which fires zero times.** So the fleet's actual behaviour was
  unmeasurable while the code to measure it sat two branches away.
  **BUILT:** `iron_condor_strategy` **v-approachalways** — `_approach()` /
  `_approach_text()` / `_journal_abandon()`; BOTH death paths now log the same
  line and emit a `condor_abandon` journal row (one per dead plan, joinable
  offline instead of grepped). `tests/condor_approach.py` **v1.0** reads them.
  **THE VERDICT IS PRE-REGISTERED IN THE TOOL, not chosen after the data:**
  `p90 approach < 40%  -> GEOMETRY` (no value of CONDOR_TRIGGER_APPROACH reaches
  it; the ANCHOR is wrong — AI's midpoint, the pitchfork/VWAP work).
  `p90 >= 60%          -> PARAMETER` (fit 0.65 from the distribution).
  `in between          -> NEITHER ESTABLISHED` — say so rather than pick.
  It takes the **closer** side, because a plan needs only ONE leg to fire;
  averaging both would report 45% for a plan whose call side reached 80%.
  **⚠️ A LOW NUMBER WOULD NOT MEAN "LOWER THE TRIGGER".** The un-floored version
  sold with no minimum distance and **bled P&L for ~3 weeks**. Reaching more
  triggers by selling nearer the middle re-runs a known-losing experiment. That
  is exactly why the verdict says ANCHOR rather than parameter below 40%.
  **⬜ SECONDARY, and it is a real asymmetry:** Leg 2 **pauses** on a directional
  tick; Leg 1 **destroys the plan** (`self._plan = None`). v3.2 fixed precisely
  this for Leg 2 on 2026-07-23 and its own comment says *"Leg 1 never got the
  same treatment."* Worth revisiting — but **not on this evidence**, since the
  measurement now says the cancel is not what cost the fires.
  **⬜ ALSO OPEN:** `cutoff=0` fleet-wide while MU held a plan past 13:50 ET. The
  cutoff branch lives inside `check_leg_triggers()`, which only runs when the box
  is FLAT — so a plan held behind an open directional position never formally
  expires and just persists to the next-day reset. Plan-expiry accounting is
  unreliable; do not read `cutoff` counts as plan lifetimes.
  **⬜ NEXT:** run `python3 tests/condor_approach.py` after a session with the
  new rows. Nothing to read before the bake — earlier sessions reported only the
  regime, which IS the gap.
  **CORRECTED IN THE SAME PASS:** `main.py`'s condor comment claimed the plan is
  *"Skipped for directional-only instruments (single names)"*. **False since the
  2026-07-14 directive** set `FULL_STRATEGY_INSTRUMENTS = set(STRIKE_INCREMENTS)`
  — every box is eligible. That stale comment sent this investigation down the
  wrong path for a turn.

- `[DESK→DEPLOY]` **BF.4 — ✅ 2026-08-04. THE SESSION GUARD, RECONFIGURED THE WAY
  THE OPERATOR ASKED: reports and backfills pull outside RTH; fleet maintenance
  still cannot bombard the feed.**
  **THE RULE, and it is the whole lesson of 08-01 → 08-04: a guard must test the
  thing it protects, not a proxy for it.** Three guards sat in one chain and all
  three keyed on the CLOCK — two of them independently blocked the same
  operation, and neither raised anything. Rewritten against purpose, each one
  becomes obvious:
  `candle_feed   protects: HOLDING a live subscription   ->  is this a one-shot?`
  `pull_today    protects: a LIVE BOT on this box        ->  is optionsbot up?`
  **`candle_feed` v3.11 — ONE PREDICATE, `_idle_outside_session(once)`, called
  from both sites.** v3.9 wrote the condition inline twice; v3.10 had to patch
  both; a fourth caller would have had to remember a fourth time. Pure refactor —
  service mode is byte-equivalent to v3.10. The canary counts CALLS to the
  predicate rather than matching a condition, so a hand-written clock check
  anywhere in `run()` fails the audit.
  **`pull_today_ohlc` v1.5 — GUARD BACK ON BY DEFAULT.** v1.4 disabled it at
  operator direction while the failure was being diagnosed, and **the diagnosis
  proved this guard was never the cause** — the 16:28 run was post-close with no
  bot running, a state where it cannot fire. Leaving it off would have removed a
  correct protection to pay for a bug elsewhere. `OT_PULL_RTH_GUARD=0` remains
  the escape hatch and **should sit unused — a knob you HAVE to set is a design
  smell.**
  **WHAT EACH CALLER NOW GETS, which is the operator's requirement stated as
  behaviour:**
  `EOD report / backfill, post-close        -> runs (no bot, or postclose)`
  `Backfill of a SAT-OUT box, mid-session   -> runs (no bot on that box)`
  `Pull at a TRADING box, mid-session       -> REFUSED (would freeze its store ~200s)`
  `candle-feed SERVICE, outside RTH         -> idles (the v3.9 maintenance-wake fix, intact)`
  **WHY NOT DISABLE IT FROM THE CONDUCTOR** — the alternative considered and
  rejected. It inverts this project's own standing rule (things go INTO the
  conductor because a step someone must remember never happens; caller-side
  disabling means every OTHER caller must remember). It makes identical code
  behave differently by caller with nothing in the log saying which. And it
  routes around a wrong condition instead of fixing it — which is what produced
  the 14 phantom files in the first place.
  **⬜ FOLLOW-ON, small:** `pull_today_ohlc`'s own RTH check could route through
  the same helper rather than duplicating the shape in bash. Two languages, one
  rule — worth doing when something else touches that file.

- `[DESK→DEPLOY]` **BF.3 — 🔴 ✅ FOUND AND FIXED 2026-08-04. THE EOD CANDLE
  RETRIEVAL HAS BEEN DEAD SINCE 08-03 AND NOTHING RAISED. `candle_feed` v3.10.
  Ships on tonight's reflash — it is box-side.**
  **THE BOX LOG SETTLED IT** (AAPL, 21:13 UTC, post-close):
  `post-close: safe to rebuild` — the pull guard did NOT block, confirming BF.2's
  read. `TastyTrade session established` — creds fine. Then, four times:
  `Feed idle — outside RTH, no subscriptions held. Open in 976 min. Sleeping 60s.`
  and finally `AAPL → 0 bars`.
  **THE CAUSE: `candle_feed --once` NEVER BACKFILLS OUTSIDE RTH.** v3.9's RTH
  gate (landed **2026-08-01**) idles the reconnect loop whenever `not is_rth()`
  — and **never asks whether the run is a one-shot backfill**. A `--once` run
  therefore sleeps 60s at a time until `timeout 200` kills it, having subscribed
  to nothing. `pull_today_ohlc.sh` calls exactly `candle_feed --once`, and it is
  **the only path the EOD candle retrieval has**.
  **THE DATE MATH IS THE CONFIRMATION.** The gate landed Sat 08-01; the first
  affected trading sessions are **08-03 and 08-04**. That is precisely the two
  days of missing sat-out candles, and it explains why boxes that ran THROUGH a
  session are fine (warm store) while every box woken AFTER it produces nothing.
  **BOTH GATES HAD TO MOVE, and this is the part a naive fix misses.** The
  RTH-over `break` inside the stream loop sits **above** the `--once` drain-exit.
  Exempting only the outer gate reproduces the identical hang one layer down —
  connect, break on the first flush cycle, back to the outer gate, sleep — with
  the backfill still undrained. **Proven: reverting only the inner gate turns 3
  of 5 tests red.**
  **THE EXEMPTION IS RIGHT, NOT A LOOPHOLE.** v3.9 exists so a box does not HOLD
  a live socket when no session needs one — its own header says the problem was
  maintenance wakes putting 29 boxes on the wire. `--once` connects, pulls
  HISTORY from 09:30, flushes and exits; it holds nothing. **The service path is
  untouched**, so v3.9's fix stays intact — verified across all four
  (is_rth × once) states.
  **⛔ THE COST IS PERMANENT AND SHOULD BE STATED PLAINLY.** DXFeed history is
  same-evening only. **08-03's sat-out symbols are gone.** 08-04's are gone too
  unless the reflash lands and the backfill re-runs before midnight ET. Every
  analysis reading the replay corpus inherits two sessions at ~15 symbols ×
  ~243 ticks against a normal 29 × ~389 — including **AV**'s Aug 13 revisit.
  **WHY IT SURVIVED TWO SESSIONS:** no exception, no non-zero exit, an INFO-level
  line, and a 38-byte file where a 16 KB one belongs. The conductor's
  `7 symbol(s) still without candles` warning fired and was the only signal.
  **⬜ IMMEDIATELY AFTER THE REFLASH, while it is still 2026-08-04 ET:**
  `cd ~/day_trader_pro && venv/bin/python eod_backfill.py --date 2026-08-04`
  then `--date 2026-08-03` as a long shot. Confirm by file SIZE, not by the
  summary line: any 38-byte file left in `ohlc/<date>/` is still a failure.

- `[DESK→DEPLOY]` **BF.2 — RTH GUARD DISABLED BY DEFAULT, 2026-08-04, OPERATOR
  DIRECTIVE. `pull_today_ohlc` v1.4, gated on `OT_PULL_RTH_GUARD` (set to 1 to
  restore). Ships on tonight's reflash.**
  **⚠️ RECORDED BECAUSE IT CHANGES WHAT THE DIRECTIVE WILL AND WILL NOT FIX: the
  16:28 backfill that prompted this was NOT blocked by the guard.** Its own
  output reads `0 bot box(es) currently running` and it ran POST-CLOSE, so
  `POSTCLOSE=1` and `BOT != active` — a state where **neither v1.1's guard nor
  v1.3's can fire**. It returned `0 full, 0 short, 14 still missing`. Whatever
  stopped that run is downstream of the guard entirely, and **disabling the
  guard will not address it.** The cause is in the box-side
  `pull_today_ohlc.log`, which records the exact branch taken and whether the
  `--once` refill ran, found creds, or returned no bars.
  **WHAT THE DIRECTIVE DOES BUY:** it removes the guard as a variable while the
  real cause is found, and it permanently unblocks the mid-session sat-out path
  that BF.1 diagnosed. Both are legitimate; neither is the 16:28 failure.
  **WHAT IS BEING GIVEN UP, so the re-enable conversation is informed.** With the
  guard off, a pull fired at a TRADING box during RTH stops its candle-feed for
  the ~200s producer pass. The bot keeps running but reads a FROZEN store for
  that window: every engine consuming 1m/5m frames sees stale bars, and
  `market_data` v3.3's bar-recency guard will begin recording BLINDNESS. **The
  script now warns loudly on exactly that combination.** Mandate 2 is untouched —
  the feed is still stopped before the pass and restarted after — so this is a
  starvation risk, never a double-producer one. On a box with NO bot, which is
  the population backfill wakes, there is no risk at all.
  **THE REFUSAL PATH IS PARKED, NOT DELETED.** One env var reverses it, and
  `tests/test_pull_ohlc_guard.sh` v1.1 drives BOTH modes — the `=1` arm still
  asserts v1.3's table exactly, so the guard cannot rot while switched off and
  come back wrong.
  **⬜ THE OPEN QUESTION FOR THE LATER DISCUSSION, one command:**
  `cd ~/options-trader && tail -25 pull_today_ohlc.log; true`
  on any of the 14. It will name the branch and the outcome — "cannot refill:
  TT_* creds not present" and "0 bars (store empty / entitlement)" are different
  faults with different fixes, and neither is the guard.

- `[DESK→DEPLOY]` **BF.1 — 🔴 ✅ FIXED 2026-08-04. THE RTH GUARD WAS BLOCKING THE
  BACKFILL IT WAS NEVER MEANT TO BLOCK, AND IT HAS COST TWO SESSIONS OF SAT-OUT
  TAPE. Ships on tonight's reflash — the boxes need it.**
  **THE EVIDENCE.** `ohlc/2026-08-04/` holds two classes of file: fifteen at
  15-16 KB written 15:05 UTC, and **fourteen at 38 BYTES** — a bare CSV header —
  written 15:11 / 15:18 / 15:23 UTC. Control runs UTC, so those are **11:11,
  11:18 and 11:23 ET: mid-session**, in three waves matching
  `PRODUCE_TIMEOUT=210s` plus wake overhead at batches of five.
  **THE CAUSE.** `pull_today_ohlc.sh` v1.1's guard is *"candle-feed live AND
  before 16:00 ET → do NOT stop the feed"* — a pure CLOCK test. `eod_backfill`
  wakes SAT-OUT boxes to fetch their candles; those boxes have a **cold store**
  (candle-feed started seconds earlier) and **no trading bot**. The guard refused
  the one thing that would have produced bars — the synchronous
  `candle_feed --once` rebuild — so the script read an empty store and wrote a
  header-only file. It was correct for every state EXCEPT the one backfill
  actually uses.
  **THE FIX — the guard now asks the right question.** It additionally requires
  **`optionsbot` to be ACTIVE**. That bot is the consumer a feed stop would
  starve, and protecting it is what the guard was for. A box with no bot running
  starves nobody. Post-close behaviour is unchanged. **Mandate 2 is unchanged** —
  the feed is still stopped before the `--once` pass and restarted after, so
  there is never a second live producer.
  **PROVEN ACROSS ALL EIGHT STATES** (`tests/test_pull_ohlc_guard.sh`): the
  broken case (sat-out, mid-session, no bot) now REBUILDS; the case the guard
  exists for (trading box, mid-session) still SKIPS; post-close and feed-down
  both rebuild as before.
  **WHY IT WENT UNSEEN FOR TWO SESSIONS.** No error, no exception, no alert — a
  38-byte file where a 16 KB one belongs. It surfaced only as a thin replay
  corpus (**3,652 ticks / 15 symbol-sessions on 08-04, 3,645 / 15 on 08-03**,
  against a normal 29 × ~389) and as the conductor's *"7 symbol(s) still without
  candles"* line. The 08-04 01:51 `MIN_REAL_BARS=10` phantom floor is what makes
  the files visible as missing at all — without it they would have counted as
  harvested and backfill would skip them forever.
  **⏱ THE CLOCK ON RECOVERY. DXFeed history is SAME-EVENING ONLY.** 2026-08-04 is
  recoverable **tonight** and not tomorrow. 2026-08-03 is very likely already
  gone — worth one attempt because it is free, but do not expect it.
  **⬜ RECOVER 08-04 AFTER THE REFLASH (post-16:00 ET, so the old guard would
  allow it too — the fix is what protects every FUTURE mid-session run):**
  `cd ~/day_trader_pro && venv/bin/python eod_backfill.py --date 2026-08-04`
  then the same with `--date 2026-08-03` as a long shot.
  **⬜ COMPANION, control-side:** `eod_backfill` now names the phantom's CAUSE.
  A header-only file written during RTH and one from a dead DXFeed fetch look
  identical in the report and have opposite responses — re-run after the close
  versus investigate entitlement.

- `[DESK]` **RPT.1 — ✅ 2026-08-04. FIVE REPORTING FIXES, ALL OF THEM CASES
  WHERE THE OUTPUT LOOKED RIGHT AND WAS NOT.**
  **(1) devtools 47 was OOM-KILLED, not broken.** `line 341: 126055 Killed` is
  SIGKILL (rc 137) — no traceback, no output. `a2_cooccurrence.load()` held
  EVERY field of every tick across the whole corpus (now 17 sessions) and
  `segments()` then copied them again per symbol. **Identical to
  ramp_calibration v1.2**, which died producing no output on 13 sessions for the
  same reason. **v1.2 slims at parse time** to the five keys the file actually
  reads — measured 30,221 → 154 bytes on a representative record. No analysis
  changes; the dropped fields were never read.
  **THE GUARD SCANS THE SOURCE, NOT A LIST.** A future analysis reading a
  dropped field would not crash — `.get()` returns None, arithmetic degrades to
  zero, and the tool prints a clean table describing nothing. So the test greps
  every `.get("…")` in the file and asserts `_KEEP` covers it. **My first draft
  of that test matched only `r|rec|row.get(...)` and MISSED
  `seg[i].get("price")`** — caught by the deliberate-failure run, and the regex
  is now unqualified.
  **(2) `excursion_report` was asking for a column it already had.** The
  winner-giveback block printed *"add the extreme timestamps to telemetry before
  the freeze"* — `trade_logger` **v3.9 shipped them on 2026-08-03**. v2.6 reads
  them: **PEAK TIMING**, the fraction of the hold at which MFE landed, with
  early/late shares. A high EARLY share is a loose trail; a high LATE share is a
  move that ran to the exit and turned. **Opposite fixes, and giveback alone
  cannot tell them apart** — which is the trail-vs-BOS question sitting under
  today's 33% giveback. NULL on pre-deploy rows is REPORTED, never imputed: a
  missing peak time is not a peak at time zero, and treating it as one would
  manufacture the exact signal the measure exists to detect.
  **(3) EXIT-REASON FAMILIES WERE FRAGMENTING THE SAMPLE.**
  `regime_flip (LABEL)` carries the label in PARENTHESES, which survived the old
  strip: 2026-08-04's twelve regime_flips became four cells of **6/4/1/1**,
  every one REFUSED. `max_loss_floor_25pct` / `_24pct` split 2 and 1 by their own
  config setting. Each fragment then honestly reported itself UNDERPOWERED —
  **correct-looking output that can never reach a verdict.** Pooled, regime_flip
  is one cell of 12 and reaches n=40 in ~4 sessions. `reason_detail()` preserves
  the label, so pooling DEFERS the split rather than destroying it — the same
  principle as `gap_outcome_join --pool`.
  **(4) HEADLINE was printing false sentences.** 2026-08-04 announced
  *"worst regime BREAKOUT_VOLATILE net +1041.50"* — the SECOND-BEST bucket, on a
  profit, because only two cleared the n>=8 floor and both were positive. And
  *"best day_of_week Tuesday"* / *"worst day_of_week Tuesday"* on a
  single-session report. Arithmetically correct, semantically false, in the
  section people skim. **v1.5** refuses the word with one eligible bucket and
  tags it `LOWEST of N, not a loss` when every eligible bucket is positive.
  **(5) ACCEL/birth was CONFOUNDED BY LIFETIME.** The 29-symbol sweep printed
  andrews 0.22 against modified_schiff 0.67 — a 3x gap reading as "andrews
  contains the move far better". But andrews has the SHORTEST median life (3 vs
  6): a fork that dies at bar 3 has less time to be exceeded. **Per HELD BAR
  it is ~0.073 / 0.112 / 0.516** — schiff stays disqualified and the
  andrews-vs-modified gap falls to ~1.5x. Both printed; per held bar is the only
  denominator comparable across variants with different lifetimes.
  **⬜ STILL OPEN from the same review, deliberately not actioned:** the 27
  sub-minute `trend_continuation_handoff` trades (0.5 min hold, 56%
  never-favorable, lift 1.52) are a MECHANISM to find, not a strategy verdict to
  file — and **AJ.2 on Aug 14 would otherwise read an execution artifact as
  strategy quality.** And the sentiment join reads 0/85 with a fallback chain
  (`strength_by_sym or strength or scores`) that cannot tell which quantity it
  loaded; `scores` in `data/report.json` are the selector's COMPOSITE values on a
  different scale entirely.

- `[DESK→DEPLOY]` **ORB.1 — 🔴 ✅ FIXED 2026-08-04, GOING OUT ON TONIGHT'S
  RELOAD. THE FLAGSHIP HAS BEEN GATED OUT OF THE FIRST SIX MINUTES OF ITS OWN
  ENTRY WINDOW SINCE v5.0 DEPLOYED.**
  **Operator's instinct, confirmed by reading HEAD rather than inferring:**
  `main.py:1081` (v5.0) returns on a stale regime book BEFORE the chain fetch and
  BEFORE `orb_regime_bypass` at ~1111. So `ORB_FIRES_REGARDLESS_OF_REGIME` — the
  constant **defect V** created for exactly this purpose — was unreachable on any
  stale tick. v5.0 re-gated the flagship through the back door.
  **THE TIMING IS THE WHOLE POINT, and it is measured.** Fleet grep 2026-08-04:
  `FIRST=09:35:01` on ALL 15 boxes, `LAST=09:39-09:41`. ORB entries open at
  **09:35:00 sharp**. The block IS the cold-book warm-up, and it lands exactly on
  the flagship's opening window. Operator: *"our morning open used to be our
  strongest time of the day, especially with ORB."* Today the open was the only
  losing phase — n=24, 42%, **-$225.50** — against midday +$2,244.
  **THE OPERATOR NAMED THE CAUSE FAMILY AND WAS RIGHT ABOUT THE MECHANISM.**
  Their guess was the bookmark; the bookmark is offline-replay only and cannot
  touch the live path. But the WARM-UP was the right answer — v5.0 converted the
  cold-book warm-up into an entry block, and ORB inherited it.
  **THE FIX — a branch, not a deletion.** A CONFIRMED ORB (OPEN_LONG /
  OPEN_SHORT) is exempt. Nothing else is: continuation, condor, butterfly and
  sweep all condition on the label and stay blocked, so v5.0's real protection is
  intact.
  **WHY THE EXEMPTION IS PRINCIPLED.** v5.0's rule is *"opening a position is a
  DECISION against a classification the engine cannot confirm."* ORB reads no
  classification — break, retest, close back outside, graded on liquidity alone
  since setup_scorer v1.4. There is no label for a stale label to invalidate.
  **AND `stale` IS NOT `blind`.** It is the regime BOOK (a tick gap past
  dt_max=90s); the FEED has its own guard, latch and pager (market_data v3.3 /
  blindness_latch). A confirmed ORB break on a stale book reads FRESH PRICE and
  no label. **Do not widen this to "ignore stale"** — that would delete a
  protection that is real for every other strategy.
  **MEASURED, NOT ASSERTED: `tests/orb_stale_block_audit.py` v1.0.** A blocked
  entry leaves NO trade row — the refusal exists only as a log line, so bot.log
  is the only place the counterfactual survives (`orb_state.json` is overwritten
  every tick and cannot answer a question about 09:35 afterwards). It reports the
  block window per session and how many minutes inside it had a CONFIRMED ORB.
  **That count is an UPPER BOUND on opportunities refused** — sizing, grade,
  liquidity-in-path and the daily-loss halt all sit downstream and none are
  logged — and it is **not forgone P&L**. After the bake, the `exempt` column
  appears where `blocked` used to and the two are the direct before/after.
  **⬜ RUN IT ACROSS THE FLEET (option 14) once the reflash lands:**
  `cd ~/options-trader && python3 tests/orb_stale_block_audit.py 2>&1 | tail -6; true`
  A single box reading zero does not clear the gate — ORB confirms on a break AND
  retest inside a four-to-six-minute window, so most boxes most days will be zero.
  **The fleet total is the number.**
  **⚠️ BOUNDARY FOR EVERY MORNING COMPARISON:** 2026-08-03 and 08-04 are the only
  sessions with the block live. Any open-window fire-rate or ORB statistic that
  spans this deploy is comparing two different machines.

- `[DESK]` **PF.V — ✅ 2026-08-04. THE VARIANT SWEEP: `pitchfork_filter_audit`
  v1.4 `--variant-sweep`. The one pitchfork question that was not blocked on the
  calendar.**
  v1.3 flagged **22 ACCELERATION events against 33 births** and said, correctly,
  that forks exceeded on the TREND side two-thirds of the time look like a
  channel too NARROW for the move — plausibly a Modified Schiff artifact, since
  §3.2 chose that variant precisely because Andrews runs steep. It reported the
  count "so it can be watched rather than assumed" — and then nothing could act
  on it, because watching ONE variant says nothing about the other two.
  **PLUMBING, NOT NEW GEOMETRY.** `build_all_variants` has computed all three
  since PF.1 and `ForkTracker` already threads `variant`. The sweep runs the SAME
  lifecycle over the SAME tape three times and prints births, MEDIAN coverage,
  **ACCELERATION per birth**, touch per birth, cause-of-death split and median
  lifetime side by side.
  **TWO DELIBERATE CHOICES.** Rates are PER BIRTH, or a variant that simply
  builds more forks looks worse for being more productive. Coverage is MEDIAN,
  not mean — AW measured mean 10.1% against median 5.3% with half the symbols
  under 5%, so the mean describes a fleet nobody has.
  **IT DECIDES NO DEFAULT, and says so in its own output.** §10 names the
  ten-parameter surface as the headline overfitting risk and §12 names consumer
  sprawl; a table that invited picking the prettiest coverage would be exactly
  that. A variant exceeded less often describes the move better — a NECESSARY
  property, never a profitable one. **PF.3's condor-credit head-to-head remains
  the only thing that can convict a consumer.**
  **THE FIXTURE TAUGHT ME SOMETHING WORTH RECORDING.** The first planted tape
  reported ZERO births on all three variants — which reads exactly like the
  variant being swallowed. It was not: the legs were ~4 hourly bars long and
  every fork was rejected **SEPARATION**. §4.3's separation prior is doing real
  work, and a tape has to carry ~10-15 hourly bars per leg before a fork can
  exist at all. That is a fact about the filter, not about the fixture, and it
  bears on AW's 39.8%-SEPARATION rejection finding.
  **⬜ RUN IT:** `python3 tests/pitchfork_filter_audit.py --variant-sweep`
  (add `--uniqueness-scan` to see it under the §4.3.5 second reading). ACCEL/birth
  near or above 1.0 is the signal v1.3 was worried about; a markedly lower variant
  makes §3.2's choice the thing to revisit — a VARIANT question with no parameter
  attached, which is why it is safe to ask before the freeze.

- `[DESK·DATA]` **TC.4 — ✅ ANSWERED AND RE-SCOPED 2026-08-04. KEEP THE TREND
  LABEL, DELETE THE SCORING. Operator's decision, on the control run.**
  `ARMED   n=2,812   intraday 17.9%   terminal 62.6%`
  `CONTROL n=5,129   intraday 14.6%   terminal 60.9%`
  `strike curve, failure at +1.00%: armed 15.5% vs control 16.7%; at +2.00%: 6.4% vs 6.2%`
  **⛔ THE MATCHED CONTROL RUN, 2026-08-04 — THE VERDICT, AND IT IS WORSE THAN
  "NO EDGE".** `n=3,534 control  intraday 14.3%  terminal 61.5%`
  `impulse − control, TERMINAL: −0.3% ±2.3%` — a dead null, and **the impulse
  side is the lower of the two.**
  And the strike curve is not a tie, it is an INVERSION: at every offset beyond
  zero the arbitrary extreme is SAFER.
  `+0.25%  28.6% vs control 26.2%   +1.00%  13.1% vs 8.2%`
  `+2.00%   5.1% vs control  1.7%   +3.00%   2.2% vs 0.6%`
  **MECHANISM, and it is coherent:** an impulse candle is by construction a
  large-range bar, so it SELECTS FOR VOLATILITY — and volatility is exactly what
  breaches a strike placed a fixed percentage away. The state does not merely
  fail to protect the floor; **it preferentially picks the conditions that
  breach it.**
  **THE ONE BIAS I CAN IDENTIFY RUNS AGAINST THE FINDING**, which makes it
  conservative: control anchors are drawn uniformly over eligible bars, so they
  sit EARLIER on average and get a LONGER forward window in which to be breached.
  They should have failed more. They failed less.
  **Arming buys 1.7 points, and at the wider strikes the unarmed population is
  marginally BETTER.** Terminal survival is FLAT across every SD bucket in both
  populations (59-64%, all bands overlapping). Two independent measurements
  agreeing: **`impulse_val` does not discriminate on the outcome the trade
  depends on.** Category 2 by the operator's own split — a contributor not doing
  its job is a DEFECT, not a preference.
  **DELETED:** the readiness gate as TC.4's trigger, and TC.4b's plan to fit
  `TR_TCS_IMPULSE_SD_LO/HI` from a durability curve. **There is no curve to fit**
  — re-aim TC.4b's Aug 8-9 slot accordingly rather than running it as written.
  **SURVIVES:** the trend label as the condition, plus a strike distance read off
  the terminal-survival curve. TC.4 becomes *in a confirmed trend, sell N% beyond
  a recent extreme*.
  **NOT DELETED, deliberately:** the log-only readiness track keeps emitting. It
  gates nothing, costs nothing, is the only source of the impulse-floor record
  this analysis ran on, and shares `_extension_from_arm` with the condor sides.
  Removing the emitter destroys the input to every re-examination and changes no
  behaviour. Flagged here so "delete the scoring" is not later read as "delete
  the track".
  **⛔ THE RANGING CONTROL IS IMPOSSIBLE — recorded so nobody plans it again.**
  `_trend_credit_spread` sets `direction = ""` on any non-TRENDING label, so
  `_impulse_sd` is never called and `floor_px` is None. **No ranging floor exists
  anywhere in the journal.** `--control matched` replaced it: a pseudo-impulse at
  a random earlier minute on the same symbol-day, same direction and
  construction — a sharper question, and buildable from tape alone.
  **⬜ WHAT IS STILL UNMEASURED AND STILL DECIDES WHETHER IT EARNS: THE CREDIT.**
  The curve bounds RISK only. A 5-wide taking $1.00 risks 4 to make 1 and needs
  ~80% terminal survival to break even before fees; 62% at the floor is far
  under, and 94% at +2% is only useful if premium survives that far out. **Do not
  build the engine on the strike curve alone** — it can say where the trade stops
  bleeding, never that it pays.
  **⬜ REUSABLE BEYOND TC.4:** terminal survival vs distance beyond a recent
  intraday extreme is a fact about the TAPE, not about this strategy. It is
  directly a prior for any short-premium strike placement — including **AI**'s
  hunt for a condor midpoint that is not the Bollinger.
  **⚠️ TWO FLAKY TESTS OF MINE, CAUGHT BY THE CLOCK — same defect class, both
  shipped today, both found by one suite run that happened to land at 15:58 ET.**
  `tests/test_exit_latency.py` (N.5) asserted `exit_escalated == 0`, but the flag
  is set from 15:45 ET by the hard-close ladder. Both files now pin the clock with
  an autouse fixture. **Neither had ever been correct — only untested at that
  hour**, and both would have gone red on control during exactly the post-close
  window someone runs the suite in. Generalisable: any test that reasons about a
  branch sitting BELOW a time gate must pin the gate, or it is asserting the hour.
  `tests/test_stale_no_regime_flip.py`
  (shipped this morning with N.8) was TIME-OF-DAY DEPENDENT: the 15:45 hard close
  short-circuits ahead of every regime branch it exercises, so the file was green
  all day and went red at 15:58 ET when a suite run happened to land in that
  window. It had never been correct — only untested at that hour. **v1.1 pins the
  clock with an autouse fixture**; the one test that wants the hard close
  overrides it. A suite that passes depending on when you run it is worse than
  one that fails, and this one would have gone red on control during exactly the
  post-close window someone would use.

  **⬜ A PROCESS NOTE WORTH THE LINE.** A strategy that would have cost a build,
  a deploy slot and weeks of paper data was taken to a near-negative for one
  offline tool and an afternoon — and the thing that killed it was not the P&L,
  it was the CONTROL. Every absolute rate before v1.3 looked like a result.

- `[DESK·DATA]` **TC.4b-pre — ARMED RESULT IS IN, AND IT IS NOT GOOD FOR THE
  PREMISE AS STATED. v1.2 built to settle whether that is fatal.**
  **THE NUMBERS (2026-07-28 → 08-04, `--machine ARMED`, n=2,812 distinct
  impulses from 17,177 scored rows):**
  `intraday floor held  17.9%`  ·  `time-to-failure  p10 1min / p50 6min / p90 68min`
  `penetration on failures  p50 0.862% / p90 3.001% / p95 3.756% / max 6.597%`
  `SD buckets: sub-aware n=0 · aware n=5 · establish n=987 (15%) · screaming n=1820 (19%), MDE 4%`
  **THE PRE-REGISTRATION FIRED AND IT GETS HONOURED.** The tool's own text says a
  single-digit p50 means *the thesis was wrong*, not *the 0DTE ran out of clock*.
  p50 is **6 minutes**. Half of all violations happen within six minutes of the
  impulse. That is the strategy's core claim failing on its own terms.
  **BUT THE MEASURE DOES NOT MATCH HOW THE TRADE PAYS — stated plainly rather
  than used quietly to rescue the strategy.** "Was the floor ever violated
  intraday" is not a defined-risk spread's loss condition; **where price sits at
  the bell is.** A floor breached at 10:04 and reclaimed by 15:00 expires fine and
  v1.1 counted it a failure. So an 82% violation rate is NOT an 82% loss rate, and
  the number that actually decides TC.4 had not been computed.
  **v1.2 COMPUTES IT.** INTRADAY, TERMINAL and RECOVERY reported separately and
  never merged, plus a **STRIKE CURVE** — terminal failure rate as a function of
  distance beyond the floor. The offset where it crosses a tolerance stated in
  advance IS the short-strike rule, priced from behaviour rather than a delta.
  Same journal, same tape, no new collection.
  **⬜ A SECOND FINDING, and it breaks TC.4b's stated METHOD.** TC.4b plans to fit
  `TR_TCS_IMPULSE_SD_LO/HI` from this curve. On the ARMED population the curve
  does not exist: `sub-aware n=0`, `aware n=5`. **Arming already requires
  magnitude**, so there is no low-SD variance to fit against — the tool now says
  so in its own output. The two populated buckets differ 15% vs 19% against an
  MDE of 4%, i.e. exactly on the detection limit, so "durability rises with
  magnitude" is **not established, only not-refuted**. The fit must come from
  `--machine STAGING+` or it does not come at all. Re-aim TC.4b accordingly.
  **⬜ NEXT, in order, both one command:**
  (1) `python3 tests/tcs_floor_durability.py` — read TERMINAL, RECOVERY and the
      strike curve. **Decide the tolerance BEFORE reading the curve**, or the
      offset gets chosen to fit the answer.
  (2) `python3 tests/tcs_floor_durability.py --machine STAGING+` — the only
      population with low-SD mass, for the ramp fit.
  **⬜ WHAT WOULD STILL BE MISSING even on a good terminal number:** this prices
  no credit. Further OTM bounds risk and shrinks the premium, and the whole trade
  is that trade-off. A terminal failure rate alone cannot say the strategy earns —
  it can only say the strike distance where it stops bleeding.
  **DECISION POSTURE UNCHANGED: the engine stays unbuilt.** Not on schedule
  grounds — on the grounds that a premise which fails its own pre-registered test
  does not get a firing engine until the terminal measure says whether the failure
  is the thesis or the strike.

- `[DESK·DATA]` **TC.4b-pre RESULT — ⚠️ FIRST RUN IS SUPERSEDED, AND THE
  CORRECTION IS THE FINDING. v1.1 ships the population filter.**
  **WHAT v1.0 REPORTED (2026-08-04, 5,129 "impulses" from 17,177 scored rows):**
  floor held **14.6%**; durability by SD **12% / 13% / 15% / 18%** across
  sub-aware → screaming; penetration on failures p50 0.799% / p90 2.868%;
  time-to-failure **p10 1 min, p50 4 min**, p90 61 min. Largest bucket n=1907,
  MDE 3%.
  **WHY IT IS NOT THE ANSWER.** The impulse lookback recomputes on EVERY TICK, so
  a `floor_px` exists on every scored row whether or not the track was anywhere
  near arming. v1.0 filtered on nothing, so **most of those 5,129 floors belong to
  DORMANT moments the strategy would never have sold beyond.** It is not a
  measurement of the trade; it is a measurement of a rolling minimum. It did not
  error and the output did not look wrong — which is exactly the class of failure
  this thread keeps finding, this time in my own tool, one turn after shipping it.
  **v1.1 — `--machine ARMED` IS NOW THE DEFAULT.** The journal already carried
  `machine` (DORMANT/STAGING/ARMED) and `r`, so the filter cost nothing and should
  have been there from the start. `--machine ANY` is retained ONLY so the two
  populations can be compared, and the header now says on its face which one is
  being shown. `--min-r` added for a tighter cut.
  **DO NOT COMPARE THE TWO RUNS AS IF THEY REFINED EACH OTHER** — they are
  different populations, not different precisions.
  **⬜ WHAT THE v1.0 NUMBERS DO STILL SUGGEST, held loosely and pending the
  ARMED re-run:** the SD curve rises monotonically 12→18% and the 6pp spread
  clears the 3% MDE, so impulse magnitude does appear to protect the floor — the
  direction the strategy assumes. But **p50 time-to-failure of 4 minutes** is the
  number to watch: my own tool's text pre-registered that a single-digit p50
  means *the thesis was wrong*, not *the clock ran out*. If that survives the
  ARMED filter, the premise is in serious trouble and TC.4 should be reconsidered
  rather than built. If it does not survive, the whole first run was noise from
  DORMANT floors and the real curve starts here.
  **⬜ NEXT, one command:** `python3 tests/tcs_floor_durability.py` (now ARMED by
  default), then the same with `--machine ANY` for the contrast.

- `[DESK·DATA]` **TC.4b-pre — ✅ TOOL BUILT 2026-08-04. DOES THE IMPULSE FLOOR
  HOLD? `tests/tcs_floor_durability.py` v1.0. The credit spread's premise, tested
  BEFORE the engine exists.**
  **THE DECISION THIS RECORDS, because it was asked directly:** *should we build
  `vertical_spread_strategy.py` now?* **No — and not for schedule reasons.** The
  strategy rests on one claim: committed order flow will not fully retrace, so a
  spread sold BEYOND the impulse candle is safe. **That claim has never been
  measured.** TC.4b already says this table runs first. Building the firing
  engine ahead of it is the inversion the 08-03 postmortem names in its own
  process lesson — four tools built around a -$234 line item while bos_exit sat
  at -$2,757. Build the measurement, then the fix.
  Three supporting reasons, in descending order: the SD bounds are unfitted
  until TC.4b (Aug 8-9); a new firing strategy moves fire-rate, which is one of
  the four numbers the **Aug 21 freeze verdict** is written from, so it would
  break its own baseline; and it changes the trade population **AV**'s Aug 13
  read and `conditional_tables` are measured on.
  **BUILDABLE TODAY, verified rather than assumed:** every scored readiness
  event since 07-28 journals `floor_px`, `sd_ratio`, `dir` and `ts_et`, and the
  tape sits in `ohlc/<date>/<SYM>_ohlc_<date>.csv`. No new collection. The
  digest already reports `trend_credit_spread wf=802 arm=652`, so the sample is
  banked.
  **THREE OUTPUTS, EACH ANSWERING A DIFFERENT OPEN QUESTION:**
  (1) **Durability by SD bucket** — this IS the fit for
  `TR_TCS_IMPULSE_SD_LO/HI`. The bound belongs where durability starts clearing,
  not where a prior guessed. Feeds TC.4b directly. Bucket edges are printed as
  PRIORS; a flat curve says impulse magnitude is not what protects the floor and
  the ramp is measuring nothing.
  (2) **Penetration on failures** — p90 is a strike distance priced from the
  state's own behaviour, the same argument AQ made for the condor, on a strategy
  that actually wants it.
  (3) **Time to failure** — a floor broken at 15:55 is a 0DTE that ran out of
  clock; one broken in four minutes is a wrong thesis. Only the second
  invalidates the trade.
  **TWO DESIGN CALLS WORTH KNOWING BEFORE READING THE OUTPUT.**
  *CLOSE, not wick.* A short strike is threatened by ACCEPTANCE beyond a level,
  not by a touch. The wick is reported separately so the two are never
  conflated — merge them and durability silently becomes a stop-out statistic.
  *DEDUP on the floor.* The track scores every tick, so ONE impulse appears on
  hundreds of consecutive rows; counting them would report a sample size that
  does not exist. Both are guarded by tests and by absence canaries, because
  either failure produces a confidently WRONG number rather than a missing one.
  **⬜ WHAT IT DOES NOT ESTABLISH, stated in the tool's own output:** no spread
  is priced, no credit assumed, no fill modelled. A held floor is a NECESSARY
  condition for the trade, not a profitable one. If the floor holds, the engine
  build is fast and well-specified with fitted bounds and its slot is the
  **Aug 24 paper deploy** — post-freeze, four weeks before full size. If it does
  not hold, TC.4 is answered for the price of one offline run.
- `[DESK]` **AV.1 — ✅ 2026-08-04. THE POOLING LEVER, BUILT WITH ITS OWN
  LEGITIMACY TEST ATTACHED. `gap_outcome_join` v1.5 `--pool gapflat`.**
  **AV** names this as the ONE lever that moves the answerable date: not waiting
  and not re-slicing, but **not splitting three ways**. n per cell roughly
  triples, which takes a **0.10 R** read from ~2026-09-15 — after go-live — to
  inside the **Aug 10-21 freeze window**. AV also says, correctly, that whether
  the pooling is LEGITIMATE is a judgement rather than a given.
  **SO THE FLAG DOES NOT JUST MERGE THE COLUMNS.** Cells stay keyed on the
  ORIGINAL class and the merge happens at print time, which makes the
  homogeneity check free: every row reports CONT vs REV with a band and a
  verdict — **POOLABLE / NOT POOLABLE / UNDERPOWERED**.
  **WHY THAT GUARD IS THE POINT.** Pooling two arms that disagree averages a
  real positive against a real negative and reports a null. That is the one way
  a LARGER n is WORSE than a smaller one, and in the pooled table it is
  completely invisible. The planted-world test makes it concrete: CONT +0.60 /
  REV -0.60 prints a GAP cell of **+0.0 ± 0.1 at n=80** — a manufactured null —
  beside a verdict reading NOT POOLABLE. A refused row still prints its cell,
  flagged, because silently withholding a number is its own failure.
  **UNDERPOWERED IS NOT PERMISSION.** A row whose arms are each under n=30
  reports that the question is open, not that pooling is fine.
  **⬜ HOW TO USE IT ON AUG 13:** run `--by strategy` BOTH ways. If the verdicts
  say poolable, the pooled cells are the read and 0.10 R is reachable inside the
  freeze. If any row says NOT POOLABLE, that row keeps the three-way table and
  its own slower clock — and the disagreement is itself the finding, since it
  means gap DIRECTION matters for that strategy and nothing in the fleet keys on
  it.
  **A TEST THAT LIED, caught by the deliberate-failure run.** My first
  assertions grepped the section for the bare phrase `NOT POOLABLE`, which also
  appears in the section's own closing explanation — so forcing every verdict to
  "poolable" left the test GREEN. Anchored on the verdict arrow now. Same
  assert-your-own-boilerplate trap as the changelog-prose canaries, three hours
  apart, in a different file.
- `[DESK]` **D.1 — ✅ 2026-08-04. THE DIARY HAS PRINTED THE SAME TOKEN FOR
  TRENDING_BULL AND TRENDING_BEAR SINCE v1.0, IN EVERY ROW OF EVERY SESSION.**
  Found by reading the 16-session scroll rather than by any check.
  `_md_block` built its label as `k.split('_')[0][:4]`, so both directional
  regimes render as **`TREN`** — in the dominance row AND the L2 row. Nothing
  errored, no test failed, and the report simply could not express the
  distinction. **That is not cosmetic:** bull-vs-bear asymmetry is an open
  question in this very workstream (bull-labelled buckets drift WITH thesis,
  bear-labelled AGAINST — replicated on two pools), and the instrument meant to
  show it was blind to it. `regime_diary` **v1.3** ships an explicit LABEL map:
  a sign-suffixed pair plus `RANG / BREA / COMP / SWEE`, four characters so the
  columns still scan. *(Superseded same day — see v1.4 below. The old tokens are
  not spelled anywhere in the tree: an absence canary pins them and greps whole
  files, which is the changelog-prose trap check_versions.sh documents.)*
  **THREE MORE, ALL FROM THE SAME READ.**
  *(a) Acceptance has read `4/5` on all sixteen sessions.* A number that has
  never varied is wallpaper — a genuine 3/5 would have looked identical at a
  glance. It now names them: `acceptance 4/5 (A2)`. A2's residual is definitional
  cross-horizon co-occurrence (A2.4), so naming it also stops it reading as a
  mystery failure every night.
  *(b) CHURN-CUT is now on the L2 line.* L1 argmax flips per committed L2 switch
  — 1.45-1.79 across sixteen sessions, clustering ~1.55. It is the envelope the
  **L2.4** prior fit is judged against and the number the **Aug 10-21 freeze
  watch** keys on, it was computable from the two values printed beside it, and
  it was never shown.
  *(c) TICKS PER SYMBOL on the header.* 2026-08-03 ran **15 symbols x 243/sym**
  against a normal 29 x ~389 — degraded on BOTH axes, and the row said neither.
  That is the corpus the -$3,149 postmortem's regime context came from and the
  one **AV**'s Aug 13 revisit will inherit. Now self-evident on the line.
  **RETROACTIVE BY CONSTRUCTION:** `upsert()` rebuilds the whole `.md` from the
  `.jsonl` every run and every field these lines need is already stored on old
  rows, so re-diarying ONE date re-renders all sixteen. `--rerender` does it with
  no replay at all — worth running before the Aug 10 bake so the freeze window is
  watched on a legible scroll rather than half-and-half.
  **MY OWN ERROR, caught by the test failing on first run:** I wrote churn as
  switches/flips, which prints 0.60 and silently INVERTS the sentence this repo
  reads it with ("churn crushed 1.6x"). Direction mattered more than digits.
  **⬜ STILL OPEN from the same read, NOT actioned here:** why 08-03 ran 15
  symbols when every other session ran 29 — the 7 backfill-missing symbols do
  not account for the gap. And `stale%` tracks TAPE SHORTNESS, not the feed
  (6.3-6.7% on every full day; 10.5 / 8.6 / 10.1 on the three short ones), so
  08-03's 10.1% is a replay artifact of gaps exceeding `dt_max` and must not be
  read as a live problem.
- `[DESK→DEPLOY]` **W.2a — ✅ 2026-08-04. THE NIGHTLY SWALLOW CENSUS FLAGGED MY
  OWN CODE, AND IT WAS RIGHT. Plus: the alarm now NAMES what it found.**
  The 08-03 conductor warned *"silent handlers ROSE 83 → 87 — a new swallow was
  added"*. Running the census against today's HEAD returned **94**: N.7/N.5/N.8
  had added **seven** silent handlers, one of them a bare `except: pass` in
  TIER 1 (risk/orders/record) inside `place_exit_order` — the exact pattern the
  operator named as the go-live risk, added hours after saying so.
  **ALL SEVEN ARE NOW `logs only`, DEBUG, once per site per process.** Loud
  enough that a broken capture is findable; quiet enough that it can never spam
  a session or become the reason a fill goes unrecorded. Behaviour is otherwise
  byte-identical — every handler still returns exactly what it returned.
  Silent count is back to **87**, the 08-03 baseline, so the next rise means
  something again.
  **TWO SELF-INFLICTED LESSONS, both caught by re-running the census rather than
  by reasoning:**
  (1) My first fix routed every log through a `_quiet()` helper. The census still
  counted all five SILENT, because **it reads the HANDLER BODY** — a log behind
  an indirection is invisible to it. Logger calls are now inline and the helper
  only throttles. *Hiding a log from the census would defeat the census.*
  (2) My throttle for the exit-engine handler reused `self._live_exit_alerted`,
  and the classifier promptly read that debug-only handler as **"pages"**. A
  census you can mislead by choosing a variable name is not a census. Own set
  now (`_telemetry_logged`).
  **AND THE ALARM ITSELF WAS INCOMPLETE.** It counted the rise and stopped, so
  every firing cost a manual census to find out WHICH. `swallow_audit` **v1.1**
  gains `--since <snapshot.json>`, and `eod_conductor` **v1.13.0** names up to
  five additions inline in the warning (tier-1 first) — the conductor already
  had both snapshots loaded, so the diff was free.
  **IDENTITY IS (file, func, guards), NOT THE LINE NUMBER.** A line moves
  whenever anything above it changes, so a line-keyed diff would report an
  entire file as new after a one-line edit — the same false-alarm class the
  tool exists to prevent. Proven on three cases: identical snapshot → 0 new,
  rc 0; a planted `except: pass` → named with its tier and guard, rc 1; a
  comment inserted at the top of a file → still 0 new.
  **⬜ NOT DONE, deliberately:** the other 87 are NOT triaged here. Most are
  correctly silent (guarded optional imports, journal emits that must never kill
  a trade). Triaging them is W.2 proper and stays scheduled where it is — this
  item only covers the ones this thread created and the alarm that reports them.
- `[DESK→DEPLOY]` **N.8 — ✅ BUILT 2026-08-04. NO REGIME-FLIP EXIT ON A STALE
  BOOK. Operator directive; bakes Mon Aug 10.** *"Do not execute a regime flip
  exit on stale... wait for the next non-stale tick to decide if it's going to
  make a trade decision."*
  **WHAT v5.1 LEFT OPEN.** It blocked ENTRIES on stale and held the committed
  label — but a HELD label is still a label, and `_evaluate_continuation` fires
  `regime_flip` on any label that is not TRENDING in the trade's direction. On a
  COLD book (stale, nothing committed) main fell back to v1.3 raw argmax and fed
  it to the exit that checks regime **second, before any price stop**. That is
  the 07-23..08-03 flicker mechanism with one branch still open.
  **THE FIX IS ONE ARGUMENT, NOT A NEW GATE.** `regime=None` into the exit path
  while the book is stale. All three regime-driven exits already guard on the
  label being present — `regime_flip`, condor `regime_flip_adverse`, butterfly
  `regime_flip_exit` — so None disables exactly those three and nothing else.
  Verified by reading every use of `regime` in `exit_engine`: it is passed down
  and used nowhere else.
  **SCOPE HELD DELIBERATELY NARROW, and the operator drew the line.** The wider
  reading — *no exit at all on stale* — was raised and NOT taken. Stale means the
  regime BOOK has not resolved; it is not evidence the price feed is down.
  15:45 hard close, stop, max_loss, trail, FVG trail, break-of-structure, condor
  ratchet, nickel close and theta all still fire. A 0DTE position that skips its
  flatten becomes an overnight orphan on an expiring contract.
  **THE TEST ASSERTS BOTH HALVES**, because the second is the one that can be got
  wrong: a live adverse label DOES flip the trade out (so the None case is not
  passing vacuously), and with the label withheld the max-loss floor and the hard
  close still fire on the same record. Plus a source-level assert on main.py,
  since the gate is one argument and a silent revert would raise nothing.
  **⬜ VERIFY AFTER THE BAKE:** `regime_flip` exits should no longer appear in
  the 09:35-09:41 window at all. Re-run `flicker_audit` after a few sessions —
  regime_flip hold-times are the direct before/after, the same instrument the
  08-03 postmortem used.
- `[DESK→DEPLOY]` **N.7 — ◐ BUILT AND PUSHED 2026-08-04 (origin `0f78329`);
  ⬜ NOT YET BAKED — Mon Aug 10. THE TC.2 EXIT BAKE-OFF HAD NO CAPTURE, AND ITS
  DATA WINDOW WAS ALREADY OPEN.**
  **LANDED, WITH THE LIMIT OF THAT WORD STATED:** the deploy line's supersession
  gate passed every content check, `check_versions` v4.9 reported ALL CANARIES
  GREEN, the parity invariant reads checkout == origin HEAD, and the working tree
  is clean. **The FLEET is still running the prior code** — nothing about today's
  or next week's rows changes until the Aug 10 bake, so the capture's clock has
  not started yet. It is NOT ✅; see PART 0.5 for the remaining steps.
  ROADMAP TC.2 states the counterfactual "LIKELY NEEDS AN OBSERVABILITY
  PRECURSOR (log-only, can start pre-freeze like L3.1/L3.2)" and that precursor
  appeared on no date in this file. Verified at HEAD before building
  (`PRAGMA table_info(trades)` and the schema block): no FVG zones, no frame
  identity, no per-timeframe depth on any trade row.
  **WHY IT IS URGENT WHEN THE LOSSES ARE NOT.** The permissive posture is
  deliberate and its P&L is not a finding (POSTMORTEM 2026-08-03, two-bucket
  rule). But the loose stops only pay off if the calibration can later ask
  *"would a different exit have done better on THIS entry?"* — and that question
  is answered from rows, not from money. Every session that closes without the
  capture is a session permanently outside the bake-off. Same shape as v3.9's
  MFE/MAE timestamps: **value strictly decreasing until the Aug 21 freeze**, and
  zero of it recoverable afterwards.
  **WHAT WAS BUILT.** `analysis/entry_snapshot.py` **v1.0** (never raises;
  build/to_json) · `trade_logger` **v3.10** (`entry_snapshot` TEXT, auto-migrated,
  no DEFAULT so NULL keeps meaning *not captured*; `set_entry_snapshot()` RETURNS
  a bool) · `main.py` **v5.1** (hook on the directional path and on BOTH condor
  legs; `_execute_condor_leg` gains an optional `ctx`) · `check_versions` **v4.9**
  (+7 canaries) · `tests/test_entry_snapshot.py` (17 tests).
  **BoS IS DELIBERATELY NOT CAPTURED — correcting my own earlier claim in this
  thread that it was missing.** `BOSTracker` seeds from entry price and direction,
  both already columns, and ratchets on closed 1m candles: the BoS counterfactual
  is a pure function of the post-entry tape. Reading HEAD, not reasoning, is what
  changed that answer.
  **WHAT IS GENUINELY IRRECOVERABLE, which is the whole justification:** the live
  5m frame is CONTINUOUS across sessions while the banked tape is session-scoped
  RTH, so a gap formed over the overnight boundary exists live and cannot exist in
  any offline resample (defect S's divergence class); and frame DEPTH — AK's
  finding — is gone when the tick ends.
  **THE LOAD-BEARING CANARY IS THE ABSENCE ONE.** A log-only capture fails
  silently by construction: if a stale sync drops `ctx` from a condor call site,
  the legs stop being captured, no error is raised, and the column keeps filling
  from the directional path — indistinguishable from working. `check_versions`
  v4.9 greps for the ctx-less call form.
  **VALIDATE — ONE FLEET COMMAND ON THE FIRST BAKED SESSION, no new tool:**
  count non-NULL `entry_snapshot` against today's entered rows per box and read
  the PER-BOX LINE, not the tally (option 56's lesson). Both numbers equal and
  non-zero = capture alive on every path; non-zero directional with zero condor
  legs = the ctx regression the absence canary exists to catch; zero everywhere on
  a box that traded = the hook is not being reached. Then grep bot.log for
  `entry_snapshot NOT captured` — once per reason per process, so ONE line can
  stand for a whole session of misses.
  **⬜ OPEN, deliberately not done here:** nothing CONSUMES the column yet. The
  bake-off harness is TC.2 work and stays gated where the roadmap puts it — this
  item exists so that when the season opens, the rows are already there. Do not
  read the first days' payloads as a result; they are a sample being collected.
- `[DESK]` **L1.9b — Graft the proven bookmark onto `validate_regime.sh`**, then run
  `regime_backfill --rebuild` to re-score all dated diary rows warm. DONE = the
  diary reads TRENDING honestly on the days live boxes did.
  **HOW:** graft = the proven copy from Aug 2 replaces the live script (full-file,
  version-bumped); rebuild re-scores every dated folder with warm depth.
  **VALIDATE:** the N.1 agreement metric, now on the full archive: per session,
  offline TRENDING share vs live regime_log TRENDING share — DONE means the known
  under-report signature is gone on the days the live boxes trended (e.g. the
  07-17+ AVGO sessions), with chop days unchanged. Both series are on control;
  the check is a query.
- `[DESK·DATA]` **TC.4b — SD-bounds fit PR.** Run `readiness_digest`, fit
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
- `[DESK]` **Level.1 — hierarchy + Overnight High/Low, build on the TESTER** (queued 07-24).
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
- `[DESK]` **Level.2 — hierarchy tester proof complete.** Inert where it should be; the
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
- `[DESK·DATA]` **G.1 (data checkpoint).** Snapshot the `retest_depth` distribution (3 weeks
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

- `[DESK·DATA]` **AV — GAP CLASS x TIME OF DAY IS A CONDITIONING VARIABLE AND NOTHING
  **⏱ RE-DATED 2026-08-04 from Sat Aug 1 to Thu Aug 13, and RE-TAGGED `[DESK·DATA]`.** It was dated due 08-01 while its own text records it OPENED 08-02 — due before it existed. And it waits on ~40 trades per cell to read a 0.20 R effect, a DC&A dependency rather than effort: it was counted against execution for sessions that had not happened yet.
  IN THE FLEET KEYS ON IT. `tests/gap_outcome_join.py` v1.0.** Opened 2026-08-02
  out of AQ's clean-corpus result. **This is what survived; read it with the list
  of what did not.**
  **WHAT DIED IN AQ/AR ON CLEAN DATA:** drift shows NO EDGE at any horizon or
  elapsed bucket, so **A2.5 as a live drift factor should be DROPPED, not
  deferred**; the wrong-theta-sign hypothesis for continuation's -$2,024 is NOT
  supported; and the excursion difference is real but ~3% at p90, which does not
  move a condor's economics.
  **WHAT SURVIVED, and it is not A2 at all:**
  `             OPEN         DECAY        CLEAN`
  `FLAT          3.60   →    13.78   →     3.55`
  `CONT          9.89   →     5.91   →     1.46`
  `REV           9.55   →     5.98   →     1.83`
  On a flat open the first 70 minutes are statistically indistinguishable from
  midday, then 10:40-12:00 runs ~4x hotter. On gap days the open is hot and
  decays monotonically. **Two completely different day shapes, and every strategy
  currently treats them identically.**
  **SO A2 WAS NEVER THE TRADEABLE SIGNAL — it was the INSTRUMENT.** A sensitive
  proxy for regime ambiguity that made day type visible when we had no other way
  to measure it. That is a legitimate outcome for a diagnostic, and it is worth
  recording as such rather than pretending the state itself pays.
  **THE SHARPEST TEST, and why ORB is first:** ORB forms its opening range
  09:30-10:00 — PRECISELY the window the clean grid shows is dead on flat opens
  and hot on gap days. **AH** has ORB at **-0.24R over 252 trades** with no
  explanation offered. If that decomposes into something like "+0.3R on gap days,
  -0.8R on flat opens", it is a gate with a real sample behind it, **no new
  collection**, landing well before the freeze. Same split applies to the 362
  condors and to continuation's handoff-vs-standalone problem.
  **THE TOOL:** joins `reports/gap_pct.json` to `reports/fleet_trades_<date>.json`
  by (date, symbol). Rows by strategy / setup_grade / regime / box, columns by gap
  class, optional entry-time window matching a2_partition's buckets. Mean ±95%,
  win rate and MEDIAN per cell — median because one large loser can dominate a
  small cell. Cells under n=30 are REFUSED. Verified on a fixture with a planted
  ORB split (+42.5 CONT / -50.5 FLAT) which it recovered exactly while showing no
  split on the other two strategies.
  **⬜ REVISIT TRIGGER — 2026-08-13, and this is a DATE not an intention.** The
  first real runs settled that the question is not yet answerable and, more
  usefully, exactly WHEN it becomes answerable.
  **WHAT THE RUNS SHOWED.** Clean window (--since 2026-07-23) gives 215 trades,
  116 of them from 07-31 alone. Of 15 cells only continuation cleared n=30:
  CONT -12.3 ±90.1, REV -1.4 ±100.5 — a band 7-8x the point estimate, which is
  no measurement. It also ERASED the condor CONT/REV split that looked like the
  one real signal at n=30/30 pooled (clean: n=10/11) — an artifact of the
  confounded window, exactly as HISTORY.md predicted.
  **BOTH LOWER-VARIANCE ALTERNATIVES FAILED, and how R failed is the finding.**
  `--metric r` did NOT reduce variance, it RESCALED it: sd 340/0.318 = $1,069 and
  detectable 188.5/0.176 = $1,071 — identical to four digits. **`max_loss` is
  near-constant at ~$1,070**, so dividing by it only changes the axis units.
  Which means **the risk manager is sizing consistently** (good, found by
  accident) and **the $340 sigma is OUTCOME dispersion, not position-size
  dispersion** — there was no size variance to remove. `--metric winrate` is
  worse: sd 0.501 at n=51 detects only a **27.8 percentage-point** difference.
  **SO THE BOTTLENECK WAS NEVER THE METRIC — IT IS n**, and n is capped by the
  fleet's trade rate (~31/day in the clean window, continuation 46% of that, split
  three ways = ~4.8 per cell per day):
  `  detect 0.20 R  ->  n=  40/cell  ->   ~8 trading days`
  `  detect 0.10 R  ->  n= 159/cell  ->  ~33 trading days`
  `  detect 0.05 R  ->  n= 634/cell  -> ~133 trading days`
  **THE TRIGGER: re-run `--by strategy` when continuation clears n≈40 per cell,
  expected ~2026-08-13** (8 trading sessions past 2026-08-02). That reads a
  **0.20 R** effect and nothing smaller. 0.10 R lands ~2026-09-15, after go-live.
  **DECIDE NOW WHICH YOU WOULD ACT ON**, because the answer at 0.20 R and at
  0.10 R may differ and committing in advance is the difference between a test and
  a search. 0.20 R is a fifth of risk per trade — a large effect; absence of one
  is NOT evidence of no effect at all.
  **THE ONE LEVER THAT MOVES THE DATE** is not waiting or re-slicing but **not
  splitting three ways**: collapse to gap-vs-flat, or pool strategies sharing a
  mechanism, and n per cell roughly triples — putting 0.10 R inside ~11 days.
  Whether that pooling is legitimate is a judgement about whether ORB and
  continuation respond to gaps the same way, which is exactly the kind of question
  **the tick corpus CAN answer and the trade log cannot** (150,517 ticks vs 215
  trades — three orders of magnitude).
  **NOT BLOCKED, DELIBERATELY PARKED.** Operator's call 2026-08-02: let it
  accumulate. Several sessions of positive expectancy on the CURRENT engine —
  post-07-22, post-L2.5, at the ~15-31 trades/day rate rather than the un-gated
  ~120/day that produced the early sample. That is the configuration going live.
  **⬜ LIMITS WRITTEN INTO THE TOOL, not discovered later:** fills are PAPER, so a
  split depending on fill quality will not show; 252 ORB trades over 15 sessions
  across 3 classes is ~84/class BEFORE any further split, so n is thin; gap class
  is per (date, symbol) so every trade on a symbol-day inherits one class — correct,
  since the gap is a property of the session, but it means cells are not
  independent samples; and pnl_usd is used rather than R, so position size varies.
  **It is not a backtest.** It reports realised outcomes partitioned by a variable
  that was always computable and never computed. Any gate that follows needs its
  own pre-registered validation.

- `[DESK]` **L3.2a — rejection ledger build starts.** `analysis/rejection_ledger.py` +
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
- `[DESK·DATA]` **L3.2b — finish.** Class (b) coverage-gap scan (per strategy: was a live setup
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
- `[DESK·DATA]` **Level.3 — conviction lead:** win-rate/expectancy by `level_strength` bucket at
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
- `[DESK→DEPLOY]` **N.5 — ✅ BUILT 2026-08-04, ⏱ PULLED FORWARD from Thu Aug 20
  build / Mon Aug 24 deploy to the **Mon Aug 10** bake. ⬜ NOT YET PUSHED.**
  **WHY IT MOVED, and it is N.7's argument exactly:** this dataset only accrues
  in sessions recorded AFTER it deploys. Deploying Aug 24 leaves ~5 paper
  sessions before live capital; Aug 10 leaves ~15. It is log-only and touches no
  entry logic, so the Aug 10-21 freeze does not bar it — the roadmap explicitly
  permits log-only work inside the window.
  **WHAT WAS BUILT.** `exit_engine` **v4.11** — instrumented at
  `place_exit_order()`, the ONE seam every close routes through in both modes;
  `trade_logger` **v3.11** — six auto-migrated columns + `set_exit_latency()`
  returning a bool; `check_versions` **v4.10** (+6 canaries);
  `tests/test_exit_latency.py` (12 tests). Desk suite 158 passed / 1 skipped.
  **A SIXTH FIELD BEYOND THE FOUR THIS ITEM NAMED — `exit_mark_at_trigger`, and
  it is the measurement.** Milliseconds are not a cost until they are priced;
  the cost is (mark when the exit fired) − (price it actually filled at). In
  PAPER those are equal by construction, and that equality is the plumbing proof
  this item already predicted — not a result.
  **STATE LIVES ON THE RECORD, NOT THE ENGINE**, because a live close is
  MULTI-TICK: the deadline expires and the next tick resumes the same broker
  order. So `exit_submit_ts` is the FIRST submit of the attempt and
  `exit_ladder_steps` spans the whole sequence. An engine-level counter would
  reset on restart and undercount precisely the slow closes the study is about.
  **THE DELIBERATE-FAILURE CHECK EARNED ITS KEEP.** Breaking the
  confirmed-guard left the paper test green — the paper path returns its
  unconfirmed result BEFORE the stamp, so only the live path exercises that
  guard. A test was added for it. Writing on an unconfirmed pass would book the
  fast final leg of every slow close: not a missing column but a silently biased
  answer, inside the exact population the trigger decision reads. That is the
  absence canary in `check_versions` v4.10.
  **⬜ REMAINING:** push → bake Mon Aug 10 → confirm paper rows populate with
  `exit_latency_ms` ≈ the ladder cadence and `exit_mark_at_trigger` ==
  `exit_premium` (the paper identity); the REAL distribution only exists in the
  Sep 1-4 live week, which is what TC.2 reads.
  *Original item text follows.*
  **N.5 — fill-latency telemetry (the TC.2 stop-trigger dataset — must exist
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

- `[DESK·DATA]` **G.2 — decision.** Feed `retest_depth` into `orb_quality` or drop it: 5 weeks of
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
- `[FLEET]` **M.3b — Telegram bot live test** (built Aug 2): pages route to the dedicated
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

- `[DESK]` **A2.3 — THE LOG-ODDS REFORMULATION. The correct endpoint. HOLD UNTIL
  **⏱ RE-DATED 2026-08-04 from Sun Aug 2 to Mon Sep 7 (post-go-live analysis day).** This item's own first line says HOLD UNTIL AFTER GO-LIVE (Aug 31), and it was nonetheless dated 08-02 and counted overdue against execution. The schedule now matches the item.
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

- **⬜ NICE-TO-HAVE, OUTSIDE THE EVM PLAN — does the morning sentiment score
  predict trade outcomes?** Operator's idea 2026-08-03: let a bullish score
  magnify long directional trades and penalise shorts — *"I didn't think it would
  be wise to short into positive tailwinds or fire longs into headwinds."*
  Operator's own call, and the right one: **measure the correlation first, build
  nothing.** Filed here deliberately so it does not count against the schedule.
  **THE NUDGE ALREADY EXISTS AND DOES SOMETHING ELSE.** `setup_scorer` v1.2 has a
  signed brief nudge at `BRIEF_CONVICTION_WEIGHT = 0.05`, but `brief_sign` keys on
  STRATEGY TYPE, not trade direction: ORB +1.0, Butterfly -1.0, IronCondor -1.0,
  SweepReversal 0.0, and **Continuation is absent so it gets nothing.** A high
  score boosts an ORB whether that ORB is long or short. What the operator
  described needs the sign to come from the trade's DIRECTION — nobody built that.
  **AND IT HAS ONLY JUST STARTED WORKING.** Per the 07-29 diagnosis,
  `brief_strength` was a hardcoded **0.30 for every name every day** until the
  `DTP_REPORT_JSON` fix landed after the close on 07-30. The 08-03 wake shows
  `str` finally VARYING (+1.00 MSFT → +0.42 MU), so there are ~2 sessions of real
  sentiment in the trade history. A month of accumulation is exactly right.
  **⬜ WATCH: XOM printed `+0.30` on 08-03 — exactly the old
  `strength_by_sym.get(s, 0.3)` fallback** while every other name varied. Likely a
  missing entry defaulting silently, which would quietly poison any correlation.
  Check before trusting the series.
  **RECORDING IS ALREADY IN PLACE (eod_conductor v1.12.0, phase 5c).**
  `data/report.json` is overwritten every 09:15, so the day's scores were being
  destroyed before they could be joined. Phase 5c archives it to
  `reports/morning_report_<date>.json` with a freshness check — a stale file is
  worse than none, since it would attribute an old day's sentiment to today's
  trades, which is precisely the 07-29 failure mode. Chosen over a trade-row
  column because the score is per SYMBOL PER DAY, not per trade: no sqlite
  migration, nothing box-side, no freeze exposure.
  **HOW TO ANALYSE IT, and the one correction to "per symbol":** at ~31 trades/day
  fleet-wide a month gives ~20 trades PER SYMBOL — hopeless, the same wall **AV**
  hit. **POOL ACROSS SYMBOLS** (the score is a cross-symbol ranking, so pooling is
  legitimate) and a month is ~650 trades, which resolves a correlation down to
  r≈0.11. `tests/gap_outcome_join.py` already does this join shape — swap the
  conditioning column from gap class to score bucket.
  **⬜ REVISIT ~2026-09-05**, roughly a month of archived reports. Same
  accumulation window as **AV** (2026-08-13), so they can be read together.
  **IF IT CORRELATES**, the change is to make `brief_sign` directional rather than
  strategy-keyed — a behaviour change, so post-freeze, and it needs its own
  pre-registered validation. **NEVER A VETO**, per the operator: influence only.
  Note that "influence, not veto" is harder to guarantee than it sounds — anything
  upstream of a grade threshold can veto in effect, so the weight belongs where it
  cannot cross a gate.

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

**⬜ Wed Aug 5**
- `[DESK]` **RD.1 — ✅ 2026-08-05. THE READINESS HEADLINE COUNTED A DIFFERENT
  THING FROM THE LIST IT POINTS AT.**
  `npeg` measured peg rates on the RAW `_val` series; **FIT SUGGESTIONS measure
  the RAMPED output.** So the Telegram number could disagree with the list it
  sends you to — and the headline is what gets acted on. 2026-08-05 reported
  **"9 pegged factor(s)"** on the raw definition.
  **THE RAMPED OUTPUT IS THE RIGHT ONE**, and it is this section's own premise:
  *"a corroborator pegged at its bound is a constant wearing new clothes."* A RAW
  value at its bound is frequently just what that factor IS — a binary
  corroborator is 0 or 1 by construction and flagging it says nothing. A RAMPED
  output at its bound is the term contributing nothing that varies.
  `npeg = len(fits)` — one definition, and the wording now says **"pegged
  ramp(s)"**.
  **⬜ CONSEQUENCE FOR AUG 8-9:** the real count is whatever FIT SUGGESTIONS
  lists, not 9. Size the calibration slot against that number after the next
  digest, not against the headline that has been running.

- `[DESK]` **A2.W — ✅ 2026-08-05. A2 STOPS BEING A CHECK THAT ALWAYS FAILS.**
  Sixteen diary sessions, every one 4/5, every one the same check. The
  excavation already settled the cause and it is the INVARIANT that is wrong:
  TRENDING reads a ~70-minute lookback and RANGING a ~25-minute one, so a tick
  scoring both high is a slow uptrend containing a tight recent range — a real,
  tradeable state. The two labels answer DIFFERENT QUESTIONS and cannot be held
  mutually exclusive.
  **WHY IT HAD TO CHANGE BEFORE THE FREEZE:** a permanent standing FAIL makes a
  NEW A2 failure invisible. At 224 ticks and at 900 the line reads identically,
  and sixteen sessions of "4/5" trained everyone to skip it. **A check that
  always fails is not a check.**
  **NOW A BANDED METRIC.** Passes at or under `A2_BAND_HI = 8%`, fails above.
  Observed range since the tuned pool is 3.0-5.3%; today was 6.1%. The band is
  widened to 8% because A2 is a REPORTED CHARACTERISTIC — the alarm should mean
  *the tape changed*, not *it moved a bit*.
  **THE RAW COUNT STAYS VISIBLE** and the passing line says why a non-zero
  number is not a contradiction. Turning a failing check into a silent pass
  would have been worse than leaving it failing.
  **Acceptance now reads 5/5 honestly**, and an above-band reading is a real
  alarm for the first time.

- `[DESK→DEPLOY]` **CT.3 — ✅ CONSUMER GUARD 2026-08-05; ⬜ SOURCE FIX PENDING.
  THE APPENDING TRADE LOGS ARE POLLUTING EVERY READ.**
  Each box's `trades.db` is **CUMULATIVE**, and the harvest copies the whole file
  into every dated folder — so a trade from 07-23 appears in all 22 subsequent
  folders. `conditional_tables` de-duplicated NOTHING; **`trade_id` was not even
  in the SELECT**. `trade_report` has collapsed 1112 rows to 388 unique for
  weeks; this tool was reading the 1112.
  **WORSE THAN INFLATED TOTALS: n DRIVES THE WILSON INTERVAL.** At 3x
  duplication every interval is ~1.7x too NARROW. The 2026-08-05 read of
  `ORB x A [53%,61%]` vs `ORB x B [37%,45%]` as NON-OVERLAPPING was made on
  inflated n and **must be re-run before it justifies anything.**
  **v1.6 de-duplicates** on `trade_id`, falls back to a composite key rather
  than dropping id-less rows (a systematically id-less strategy would vanish
  entirely), and **prints the duplication share, naming the SOURCE above 25%** —
  a consumer guard that hid the problem would be worse than none.
  **⬜ SOURCE FIX — operator directive 2026-08-05: "each day's report should
  reflect 1 trading day on the bot boxes." Two routes:**
  **(A)** date-stamp `DB_PATH` (`trades_<date>.db`) — cleanest shape, the file
  IS the day; but it moves the LIVE WRITE PATH and every literal `trades.db`
  reference (configure.sh archive, devtools 16, harvest globs) must move with
  it. A missed one reads empty or stale, silently.
  **(B)** filter at harvest — box keeps its cumulative DB for its own
  reconciliation, the harvest exports only that date's rows into the dated
  artifact. Satisfies the requirement exactly, cannot break trading.
  **RECOMMENDED: B now, A post-freeze.**

- `[DESK]` **CT.2 — ✅ 2026-08-05. THE CONDITIONAL TABLE HAD NEVER READ A TRADE
  DB, AND SAID "NO CELL SEPARATED FROM CHANCE" ANYWAY.**
  **(a) THE GLOB NEVER MATCHED.** Harvested files are `<SYM>_trades_<date>.db`;
  the tool globbed `*_trades.db`, which requires the name to END in
  `_trades.db`. **`excursion_report` hit the IDENTICAL bug and documented it** —
  *"every consumer that globbed `*_trades_<date>.db` correctly; this file was
  the outlier"* — and the fix was never carried across. Now `*_trades*.db`, so a
  rename in either direction cannot empty the corpus again.
  **(b) AN EMPTY LOAD REPORTED A VERDICT.** A manual run printed
  `CT: 0 closed trades / 10 session(s) · no cell separated from chance yet`
  while the conductor's run of the SAME tool that afternoon found **717**. A
  null result and a failed load shared one sentence — **in the tool the Aug 8-9
  calibration fits are read from.** Now exits **rc=2**, names the cause, and
  states "This is NOT a null result".
  **DELIBERATELY PRESERVED:** an empty root with no dated folders is still
  rc=0 — the conductor must never be marked failed by a quiet night. The new
  refusal fires only when folders exist and nothing matched, which is a PATH or
  NAMING fault.
  **THE PATTERN WORTH NAMING:** a tool that runs clean, exits 0 and reports a
  null on a corpus it never read. That is the third instance this week
  (candle_feed `--once` sleeping to its timeout; the RTH guard writing
  header-only CSVs; this). All three were invisible because the OUTPUT LOOKED
  NORMAL.

- `[DESK]` **CT.1 — ✅ 2026-08-05. THE CONDITIONAL TABLE COULD NOT SEE SESSION
  SPREAD, AND IT IS THE TOOL A DISABLE DECISION GETS READ FROM.**
  **THE TRIGGER:** the 08-05 headline named
  `BREAKOUT_VOLATILE x ORBStrategy x B  n=48  P(win)=25%  [15%,39%]  E=-$32.03`.
  The Wilson interval excludes 50%, so on its face that is the **first genuine
  starve candidate** the project has produced. And the tool could not say
  whether the 48 trades came from eight sessions or two bad days.
  **THE DISTINCTION MATTERS BECAUSE THEY ARE DIFFERENT QUESTIONS.** Wilson
  answers *"is this distinguishable from chance"* — a question about n. It is
  SILENT on whether the n is a standing pattern. `trade_report` and
  `excursion_report` both carry a SESSION SPREAD block for exactly this;
  `conditional_tables` did not, and it is the one a starve decision reads.
  **v1.4:** every `Cell` tracks its dates. Rows and the headline now carry
  `sess=N` plus a flag — `<3 SESSION(S), not a standing pattern` or
  `SINGLE-SESSION (X% on one date)`. **The flag WARNS, it does not filter**: a
  flagged cell still reports its real n, win rate and expectancy, because
  suppressing it would hide a finding rather than qualify it.
  **THE TEST I DIDN'T WRITE FIRST, caught by the deliberate-failure run:** every
  assertion built a `Cell` by hand, so removing the date at the
  `build_trade_tables` call site left the whole file GREEN — the exact
  regression the guard exists to catch, invisible to the guard. There is now a
  wiring test that goes trade-row -> table -> cell, and the canary pins the call
  site rather than the flag.
  **⬜ NEXT, before the ORBxB cell can justify anything:** re-run
  `conditional_tables` and read `sess=` on that row. Fewer than three sessions,
  or 80%+ on one date, and it is a bad-day record rather than a combination to
  starve.

- `[DESK]` **W.2b — ✅ 2026-08-05. THE CENSUS CAUGHT ME IN ONE CYCLE, AND IT WAS
  RIGHT ALL THREE TIMES.** Silent handlers 87 -> 89 overnight, all three new
  ones **TIER 1** and all three mine from the previous evening:
  `trade_logger:513 set_entry_contract` · `trade_logger:537 set_exit_contract` ·
  `iron_condor_strategy:554 _journal_abandon`.
  **THE UNCOMFORTABLE PART:** I wrote W.2a's lesson — *"log calls routed through
  a helper are invisible to the census; inline only"* — and then shipped three
  bare handlers hours later. One of them (`_journal_abandon`) I explicitly
  described as deliberately swallowed. **The census cannot tell "deliberate"
  from "accidental" — that is precisely why it reads the handler body.**
  **THE SWALLOWS ARE ALL STILL CORRECT.** A journal failure must never reach the
  trading loop; a setter that cannot write must not raise into a fill path.
  Nothing about the control flow changed. What changed is that each now logs
  INLINE at debug, so the census sees a handler that speaks and a real DB
  failure is distinguishable from "the row was not there".
  **Result: 89 -> 86**, one below the 08-04 baseline (another thread made a
  fourth handler audible in the same window).
  **THE GENERALISABLE BIT:** "correctly silent" is not a property a static audit
  can verify, so it is not a defence. If a handler is right to swallow, it still
  has to say so out loud — the alternative is that every future silent TIER-1
  handler gets waved through on the same reasoning.

## PART 3 — RESOLVED REGISTER (condensed; kept so fixes don't get quietly reverted)

*Full forensic text: git history of this file at the pre-v2.0 commit, plus
`docs/HISTORY.md` and the audits. Resolution date + fixing versions + the why.*

- **AX ✅ 2026-08-03 — RESOLVED, and verified the only way this item allowed:
  by a real warning ARRIVING in Telegram, not by the code path running.** The
  control conductor read `DTP_`-prefixed variables that were never set anywhere,
  while the bot boxes carry un-prefixed ones baked in by setup_ec2.sh — two
  namespaces, one of them wired. Fixed with `EnvironmentFile` on the conductor
  unit, the same file the other two timers already loaded. Operator confirmed
  delivery 2026-08-03. The lesson is the one `alert_manager` v1.10 already
  taught and this item restates at a second layer: an alert that has never
  fired is indistinguishable from an alert with nothing to say, so the proof of
  a notification path is the notification, never the exit code.
- **AZ ✅ 2026-08-03 — RESOLVED. THE EXCURSION CUMULATIVE HAD NEVER WORKED,
  on any run ever made.** `excursion_report._rows_from_dbs` globbed the UNDATED
  filename form while harvest.py:166 writes `<SYM>_trades_<date>.db`, so it
  matched zero files since v2.0 (2026-07-15) and every run silently fell back to
  the single-day consolidated JSON — including the nightly automatic run as EOD
  conductor phase 7, whose docstring says it reads the DBs.
  `consolidate_trades.py:178` and `tests/gate_ledger.py:139` both glob the dated
  form; this file was the lone outlier. **Scope is narrow and worth stating: no
  single-day number was ever wrong** (the fallback is consolidated from the same
  DBs) — only cumulative was impossible. Fixed in v2.3 along with three
  same-class defects found in the same read: the fallback only announced itself
  when the report was EMPTY; LEASH VERDICT iterated a hardcoded flavor tuple and
  silently skipped every trail the fleet actually fires; FLOOR VERDICT matched
  `hard_stop` but not `max_loss_floor`, reporting 1 floor stop on a day with 6.
  `--since` over the fallback now REFUSES with rc=2 rather than labelling one
  session cumulative. 12 tests, deliberate-failure verified.
- **BA ✅ 2026-08-03 — RESOLVED. MENU 41 COULD NOT SEE CONCENTRATION.** `trade_report` carried
  `by_exit_reason` and `by_session_date` as separate MARGINALS with no cross, so
  it structurally could not answer whether an exit was a standing pattern or one
  session — the question raised by `bos_exit` showing n=21 cumulative, identical
  to its single-day n, while every other exit grew 3-6x. v1.4 adds EXIT REASON x
  SESSION SPREAD (distinct sessions, heaviest date, its share, SINGLE-SESSION at
  >=80% AND n >= min_n so a thin reason is never called a finding). It
  immediately paid: the 07-23..08-03 "cumulative" is **67% two sessions** (07-31
  n=116, 08-03 n=88 of 303). Same version fenced off `flag_runners_cut_early`,
  which was computed over the pre-v5.0 flicker whose sub-minute holds drag both
  medians to zero — the ratio is now reported both ways and the verdict is
  WITHHELD above 10% sub-minute. On first contact: 23% sub-minute, correctly
  withheld. 7 tests.
- **BB ✅ 2026-08-03 — RESOLVED. consolidate_trades DOC DRIFT (v1.3, doc only).** Its
  source line put the date before the `_trades` token — a THIRD field ordering,
  disagreeing with its own `_DB_RE` nine lines below and with what harvest
  writes — and its outputs were documented as landing in the day folder when they
  go to `reports/` FLAT. v1.1.1 corrected the other path references and missed
  these two. Filed as its own item because a stale filename in a docstring is
  exactly what produced the excursion defect above.
- **BC ✅ 2026-08-03 — RESOLVED. MFE/MAE TIMESTAMPS (trade_logger v3.9).** v3.8
  stored the excursion extremes as VALUES with no time attached, which measures
  how much a winner gave back and cannot ask whether it could have been
  EXTENDED: a trade that peaked at minute 2 and bled for twenty minutes and one
  that reversed on the last tick produce the identical (MFE, realized) pair and
  call for opposite fixes. Added `max_premium_seen_at` / `min_premium_seen_at`
  (UTC ISO via `ts_for_db`, the same base as entry_time — deliberately, since a
  UTC-vs-ET comparison already inverted one verdict here). The stamp advances
  only when the extreme advances; SQLite evaluates every SET right-hand side
  against the ORIGINAL row, proven by ticking a real path through a real file
  rather than by reading the SQL and agreeing with it. 6 tests,
  deliberate-failure verified. Pre-existing rows read NULL — **consumers must
  treat that as "not recorded", never as zero or as entry time.**
- **AT ✅ 2026-08-01 — RESOLVED. The regen finished (15/15 dates, rc=0, ~5h50m)
  and all four tools were re-run on the clean corpus.** The contamination is
  cleared and the numbers in **AQ** and **AR** are no longer provisional.
  The lesson stands and is the reason this item exists: *"the artifacts exist" is
  not "the job finished"* — I inferred completion from a file COUNT that was
  invariant to progress (the regen overwrites in place), and stated it as fact.
  Check the PROCESS, not the output files. A rebuild-in-place job is invisible to
  every file-level check there is. Also recorded: a full regen is a ~5 hour job on
  control, and a test suite queued against the same box will stall on CPU
  contention rather than hang.
- **Historical ADX reconstruction ❌ 2026-08-03 — CLOSED AS NOT SUPPORTABLE ON
  THIS DATA, which is a result rather than a failure to build.** The item assumed
  a `regime_log` → trades timestamp join at tolerance <= 60s would recover
  `adx_at_entry` on pre-07-27 rows. `tests/adx_reconstruct.py` v1.2 was built,
  and its held-out check — reconstruct rows that ALREADY carry a real value since
  2026-07-27 and compare — says the join does not work at any tolerance:
  `  tol   60s  overlap n=4    REFUSED (below the n>=8 floor)`
  `  tol  600s  overlap n=7    REFUSED`
  `  tol  900s  overlap n=8    med|err| 1.90   within5 62%   FAIL`
  `  tol 1800s  overlap n=15   med|err| 6.28   within5 40%   FAIL`
  `  tol 3600s  overlap n=17   med|err| 7.88   within5 35%   FAIL`
  **Accuracy collapses exactly as the sample grows large enough to measure it.**
  CAUSE: `regime_log` writes on regime CHANGES, not on ticks — 457 rows across a
  month. Measured against real entries, the gap back to the nearest preceding row
  is p50 600s, p90 1740s, max 4770s; only 13/42 land within 60s. A row ten minutes
  old genuinely does not describe ADX at entry, and `adx_at_entry` means what was
  true AT THAT MOMENT.
  **Widening the tolerance until something writes would have produced
  plausible-looking wrong numbers** — worse than the 0.0 default, because a zero
  is obviously missing and a wrong ADX is not. The tool refuses on both grounds
  and prints why, so this closes with evidence rather than a shrug.
  **KEPT:** the `staleness_s` column the tool adds, so any FUTURE join to
  regime_log records how old its source was and the caveat travels with the row
  instead of living in one decision. And the tool itself, as the proof.
  **PROCESS NOTE:** the first fleet run reported "8 passed, 2 failed" on overlaps
  of n=1..4 — one symbol "FAILED" on a single row. Every other tool this week
  carries a refusal floor and this one did not; v1.2 adds MIN_OVERLAP=8. A bar a
  single row can clear is not a bar.

- **I ✅ 2026-08-03 — butterfly cutoff RESOLVED: the branch guards nothing,
  DELETE it** (code post-freeze, per the item). `tests/butterfly_cutoff_query.py`
  v1.1 over 379 trade rows across 15 dbs found **3 butterfly trades, all entered
  before 15:00 ET** — 12:35, 12:41, 13:40, latest 13:40. No fill has ever wanted
  the 15:00 window, so per the item's loose-code principle the unreachable
  `can_enter(is_butterfly=...)` branch goes and config stops disagreeing with code.
  **THE FIRST RUN SAID THE OPPOSITE, and the correction matters more than the
  answer.** v1.0 compared the raw `HH:MM` from `entry_time` to a 15:00 ET cutoff —
  but entry_time is stored in **UTC** (`...T17:38:45+00:00`). Every entry read four
  hours late, so the same three trades appeared at 16:35 / 16:41 / 17:40 and the
  verdict came back "late entries exist and WON, so the cutoff would have COST
  money — delete the branch AND correct the config." **The action was right by
  luck; the reasoning was backwards**, and it would have entered the record as
  evidence that a 15:00 butterfly cutoff is harmful — a claim the tape does not
  make. v1.1 parses the offset, converts properly, and prints BOTH the ET and raw
  UTC times so the conversion is visible rather than trusted.

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

- **v3.81 — 2026-08-05 — RD.1: readiness_digest's headline and its fit
  suggestions measured different things.** The pegged count read RAW factor
  values while the suggestions read the RAMPED output — and the headline is what
  people act on. One definition now; the real pegged-ramp count is whatever FIT
  SUGGESTIONS lists, which is what the Aug 8-9 slot should be sized against.
- **v3.80 — 2026-08-05 — A2.W: A2 becomes a banded metric.** It had failed every
  session since the harness existed because the invariant was wrong, not the
  engine — different lookbacks, so co-occurrence is a real state. A permanently
  failing check hides a new failure; A2 now passes within an 8% band, still
  reports the raw count, and can finally raise a genuine alarm. Acceptance reads
  5/5 honestly.
- **v3.79 — 2026-08-05 — CT.3: conditional_tables v1.6 de-duplicates.** The box
  DBs are cumulative and the harvest copies them into every dated folder, so the
  same trade counted once per subsequent day; trade_id was not even SELECTed.
  Inflated n makes Wilson intervals too narrow, so the 08-05 ORB grade-A/B split
  must be re-read before it justifies anything. Source fix pending: harvest-side
  date filter now, date-stamped DB post-freeze.
- **v3.78 — 2026-08-05 — CT.2: conditional_tables had never loaded a trade DB.**
  The glob required the filename to END in `_trades.db`; the fleet writes
  `<SYM>_trades_<date>.db`. excursion_report hit and documented the same bug and
  the fix was never carried across. Also: an empty load now refuses rc=2 instead
  of printing "no cell separated from chance yet" — a verdict on a corpus it
  never read, in the tool the Aug 8-9 fits are read from.
- **v3.77 — 2026-08-05 — CT.1: conditional_tables v1.4 reports session spread.**
  The 08-05 headline produced the project's first credible starve candidate
  (BREAKOUT_VOLATILE x ORB x B, n=48, interval excluding 50%) and the tool could
  not say whether it was a standing pattern or two bad days. Cells now carry
  sess=N and a concentration flag that warns without filtering. The wiring test
  was missing from the first draft and the deliberate-failure run found it.
- **v3.76 — 2026-08-05 — W.2b: the swallow census flagged three new TIER-1
  handlers overnight and was right about all of them.** All three were mine from
  the previous evening, shipped hours after W.2a's lesson was recorded; one I had
  called deliberately silent. The swallows are correct and unchanged — each now
  logs inline so the census can see it. 89 -> 86.
- **v3.75 — 2026-08-04 — N.9 CONTRACT TELEMETRY.** trade_logger v3.12 + main v5.5
  persist the contract's own state at fill (delta/gamma/theta/iv, bid/ask,
  iv_rank) from values already in memory and previously discarded. Closes the
  gap between "what the premium did" and "why": direction vs decay vs crush were
  one number. Ten columns, not twelve — entry_premium and underlying_entry
  already held the mark and the spot. Available to every existing report
  immediately; documented in MECHANICS. Exit-side capture deferred with reason.
- **v3.74 — 2026-08-04 — AI.1: THE CONDOR'S APPROACH TELEMETRY WAS BEHIND A DOOR
  THAT NEVER OPENS.** 23 plans, 23 deaths, 0 legs fleet-wide — and the approach
  measurement existed only on the cutoff path, which fired zero times. Plan
  lifetimes of 1-94 minutes (median ~30) rule out label churn: price never
  reached a trigger on any plan. Both death paths now report approach and emit a
  `condor_abandon` row; `tests/condor_approach.py` returns a pre-registered
  GEOMETRY/PARAMETER verdict for item AI. Also corrected main.py's stale
  directional-only comment, which misdirected the investigation.
- **v3.73 — 2026-08-04 — BF.4: THE SESSION GUARD RECONFIGURED AGAINST PURPOSE.**
  candle_feed v3.11 collapses both RTH checks into one predicate named for what
  it protects; pull_today_ohlc v1.5 restores its guard to ON now that v3.10 fixed
  the real cause. Reports and backfills run outside RTH, a pull at a live trading
  box is still refused, and the v3.9 maintenance-wake protection is intact.
  Rejected: disabling the guard from the conductor — it inverts the
  build-it-into-the-conductor rule and routes around a wrong condition instead of
  fixing it.
- **v3.72 — 2026-08-04 — BF.3: THE REAL CAUSE. `candle_feed --once` has been
  unable to backfill outside RTH since v3.9's gate landed 2026-08-01.** The gate
  never checked `once`, so every EOD candle pull slept to its timeout and wrote a
  header-only csv — first affected sessions 08-03 and 08-04, exactly the two days
  of missing sat-out tape. Both gates needed the exemption; the inner one sits
  above the drain-exit and a one-gate fix hangs identically. Service behaviour
  unchanged. The loss is permanent: DXFeed history is same-evening only.
- **v3.71 — 2026-08-04 — BF.2: RTH GUARD OFF BY DEFAULT (operator directive),
  behind OT_PULL_RTH_GUARD.** Recorded alongside it: the 16:28 backfill that
  prompted the directive ran POST-CLOSE with zero bot boxes running, a state
  where neither version of the guard can fire — so the guard was not what
  blocked it and disabling it will not fix that run. The refusal path is parked
  rather than deleted and both modes stay under test.
- **v3.70 — 2026-08-04 — BF.1: THE RTH GUARD WAS EATING THE BACKFILL.**
  `pull_today_ohlc` v1.1 refused the full-session rebuild on any live feed before
  16:00 ET — a clock test — so every SAT-OUT box that eod_backfill woke read a
  cold store and wrote a 38-byte header-only csv. Fourteen of them on 08-04, and
  the same signature on 08-03. The guard now also requires a live optionsbot,
  which is the consumer it was protecting; all eight states proven. DXFeed
  history is same-evening only, so 08-04 is recoverable tonight and 08-03
  probably is not.
- **v3.69 — 2026-08-04 — RPT.1: FIVE REPORTING FIXES ACROSS BOTH REPOS.**
  devtools 47 was OOM-killed rather than broken (a2_cooccurrence v1.2 slims at
  parse time, same failure and fix as ramp_calibration v1.2); excursion_report
  v2.6 reads v3.9's peak timestamps it had been asking for and pools the
  regime_flip / max_loss_floor families that were fragmenting every cell into
  permanent REFUSAL; trade_report v1.5 stops calling a +$1,041 bucket "worst";
  pitchfork audit v1.5 adds ACCEL per HELD BAR because per-birth rewarded the
  most fragile variant. Every one is output that looked right and was not.
- **v3.68 — 2026-08-04 — ORB.1: THE FLAGSHIP WAS GATED OUT OF ITS OWN OPENING
  WINDOW.** v5.0's stale-book entry block sits above the dispatch, so
  ORB_FIRES_REGARDLESS_OF_REGIME was unreachable on a stale tick and the fleet
  lost 09:35:01-09:41 every session since it deployed — measured on all 15 boxes,
  and the open was today's only losing phase. main v5.4 exempts a CONFIRMED ORB
  and nothing else. Ships on tonight's reflash rather than the Aug 10 bake.
  `orb_stale_block_audit` v1.0 turns the cost into an upper-bound count instead of
  a claim. Also: PF.V answered as a no-change, with the real finding being that
  adverse-tine kills 81-97% of forks in ALL THREE variants — a §5.3 prior
  question, not a variant one.
- **v3.67 — 2026-08-04 — TC.4's CONTROL VERDICT (−0.3% ±2.3%, and the strike
  curve INVERTS) + PF.V the pitchfork variant sweep.** The impulse origin survives
  no better than an arbitrary recent extreme, and is strictly worse at every
  offset beyond zero — coherently, because an impulse candle selects for
  volatility and volatility is what breaches strikes. The identifiable bias runs
  against the finding. PF.V adds `--variant-sweep` to the filter audit: §12 open
  question 2, geometry only, decides no default. Also recorded: the planted tape's
  zero-birth first run was SEPARATION, not a variant bug — §4.3's separation prior
  needs ~10-15 hourly bars per leg before a fork can exist.
- **v3.66 — 2026-08-04 — TC.4 ANSWERED: KEEP THE TREND LABEL, DELETE THE
  SCORING.** The matched control settled it — arming buys 1.7pp of terminal
  survival and is marginally worse at wide strikes, and the SD curve is flat in
  both populations. `impulse_val` is a category-2 defect, not a tuning question,
  and TC.4b's fit has no curve to fit. The log-only track stays (it is the data
  source, and it gates nothing). Also recorded: the ranging control is impossible
  by construction — no ranging floor is ever journaled — and the credit remains
  the unmeasured half that decides whether the trade earns at all.
- **v3.65 — 2026-08-04 — TC.4b-pre v1.2: THE ARMED RESULT, AND THE MEASURE IT
  EXPOSED AS WRONG-SHAPED.** ARMED run: intraday floor held 17.9% on n=2,812, p50
  time-to-failure 6 minutes — the tool's own pre-registration says that means the
  thesis, not the clock. But intraday violation is not a defined-risk 0DTE's loss
  condition, so v1.2 splits INTRADAY / TERMINAL / RECOVERY and adds a strike curve
  that prices the offset directly. Second finding: the SD ramp cannot be fitted on
  the ARMED population at all (arming already requires magnitude; sub-aware n=0),
  which re-aims TC.4b's method at STAGING+. TC.4's status written into MECHANICS
  and the README with the measured numbers, and VALIDATION updated with the
  terminal/strike-curve semantics.
- **v3.64 — 2026-08-04 — TC.4b-pre v1.1: THE FIRST RUN MEASURED THE WRONG
  POPULATION.** v1.0 scored every floor the impulse lookback ever computed rather
  than the ARMED ones the strategy would have traded — 5,129 "impulses" that were
  largely arithmetic. No error, no odd-looking output, just an answer to a
  question nobody asked. v1.1 defaults to `--machine ARMED`; the v1.0 numbers are
  superseded rather than refined. Also: TC.4's description expanded in MECHANICS
  and the README (what exists today, the trade, its premise, why the engine is not
  built), and VALIDATION gains a catalogue of the offline measurement tools and
  what each one answers.
- **v3.63 — 2026-08-04 — TC.4b-pre: THE CREDIT SPREAD'S PREMISE, TESTED BEFORE
  THE ENGINE.** Asked whether to build `vertical_spread_strategy.py` now; answered
  no, and built the floor-durability table instead — the thing TC.4b already says
  runs first. Every input was already being journaled, so it needed no new
  collection. Its SD curve is the ramp fit, its penetration p90 is a strike rule,
  and a flat curve would kill the strategy for the price of one offline run.
- **v3.62 — 2026-08-04 — AV.1: THE POOLED GAP READ.** `--pool gapflat` collapses
  CONT+REV into GAP (n per cell roughly triples, putting a 0.10 R read inside the
  freeze instead of after go-live) and prints a per-row CONT-vs-REV verdict, so
  an illegitimate pool is visible rather than averaged into a manufactured null.
  Seven planted-world tests. A first draft of two of those tests asserted against
  the tool's own explanatory prose and passed on a broken tool — found by the
  deliberate-failure run and re-anchored.
- **v3.61 — 2026-08-04 — D.1 EXTENDED: BULL/BEAR, AND THE DEFECT WAS IN THREE
  RENDERERS NOT ONE.** Operator's labels replace my sign-suffixed pair. Grepping the
  truncation idiom instead of fixing the row in front of me found the same bug in
  `replay_confluence`'s nightly emitted-distribution line — the one the freeze
  watch reads — and in `regime_confluence`'s self-test. New `utils/regime_labels.py`
  is the single map all three import; canaries pin the map AND each consumer,
  because fixing one renderer leaves the next free to invent its own.
- **v3.60 — 2026-08-04 — D.1: THE DIARY COULD NOT TELL BULL FROM BEAR.** Sixteen
  sessions of rows in which TRENDING_BULL and TRENDING_BEAR both printed `TREN`,
  found by reading the scroll rather than by any check. Fixed with an explicit
  label map, plus three things the same read exposed: acceptance now names the
  failing invariant instead of printing an unvarying 4/5, the L2 line carries
  churn-cut (the number L2.4 and the freeze watch actually key on), and the
  header carries ticks/symbol so 08-03's 15 x 243 corpus is visible. All
  retroactive — `--rerender` rebuilds the whole scroll from the stored jsonl.
- **v3.59 — 2026-08-04 — W.2a: MY OWN SWALLOWS, AND AN ALARM THAT NAMES THEM.**
  The nightly census caught seven silent handlers added by N.7/N.5/N.8 today,
  including a bare `except: pass` in tier 1. All seven now log at DEBUG once per
  site; silent count is back to the 08-03 baseline of 87. Two fixes to my own
  fix, both found by re-running the census: a log behind a helper is invisible to
  it, and reusing the alert set made a debug handler read as "pages". Also
  `swallow_audit` v1.1 `--since` + `eod_conductor` v1.13.0 so the warning names
  the additions instead of only counting them.
- **v3.58 — 2026-08-04 — N.8 BUILT (no regime-flip exit on a stale book); THE
  CONDUCTOR TELEGRAM GAP CLOSED AND VERIFIED; TWO OF MY OWN READINGS RETRACTED.**
  N.8 closes the branch v5.1 left open — a held or fallen-back label could still
  drive `regime_flip` on a tick the engine could not confirm. Scope held narrow
  on the operator's line: regime-driven exits only, every price exit untouched.
  Telegram: verified working on the box, item AX did the job, and it was fixed in
  source on 08-03 rather than open as I had it. RETRACTED: the `[L2`/`[v13]` log
  counts are cross-session and cannot measure today's engine mix (use
  `regime_log.engine`, per W.1); and the stale-block counts needed timestamps
  before a trend was read into them. New open item: the `NOT committing` warning
  asserts a category from one dimension.
- **v3.57 — 2026-08-04 — N.5 BUILT AND PULLED FORWARD TO THE AUG 10 BAKE; N.7's
  SUITE STEP CLOSED; THE CONDUCTOR TELEGRAM STATUS CORRECTED.** N.5 moves from
  Thu Aug 20 build / Mon Aug 24 deploy to built-now / bakes Aug 10 on the same
  argument N.7 won: the dataset only accrues in sessions recorded after it
  deploys, and Aug 24 leaves ~5 paper sessions before live capital where Aug 10
  leaves ~15. Log-only, freeze-permitted. Adds a sixth field beyond the four this
  item named — `exit_mark_at_trigger`, which is the actual measurement.
  **N.7 step 1 closed:** control suite read, `146 passed, 1 skipped, rc=0`; the
  recovery grep also matched `failed` inside changelog prose in the same log, so
  the note about anchoring to the summary line stays. **CORRECTION on my own
  08-04 claim:** the conductor Telegram gap is FIXED IN SOURCE (day_trader_pro
  item AX, 08-03, `EnvironmentFile` in the unit) and only its DEPLOYMENT is
  unverified — restated as ◐ with the one command that settles it, rather than
  left as an open defect it is not.
- **v3.56 — 2026-08-04 — N.7 PUSHED, AND THE LEDGER THAT NOW TRAVELS WITH EVERY
  DELIVERY.** New **PART 0.5 — DELIVERY LEDGER**, because one thread now owns
  build → test → deploy and this file is the only durable record it produces:
  every archive from here ships `docs/BACKLOG.md` with the progress of that
  delivery, the remaining deliverables, a title-line bump and this changelog
  entry (WORKING_AGREEMENT §18). N.7 re-stated ✅ BUILT → ◐ BUILT AND PUSHED,
  because BUILT / PUSHED / BAKED are three different claims and only the third
  changes any data — the fleet runs the prior code until Aug 10. Two gaps
  recorded rather than glossed: the control suite's own result was never read
  (the `tail -20` caught only the canary tail, and canaries green is not the
  suite passing), and the EOD conductor's Telegram credentials are still the
  open Bucket-1 defect from the 08-03 postmortem — the alarm on tape coverage
  that is use-it-or-lose-it.
- **v3.55 — 2026-08-04 — N.7 FILED AND BUILT: the entry-snapshot capture.**
  New item on Tue Aug 4, ✅ built same day, bakes Mon Aug 10. It closes a hole
  that was invisible because it was in the ROADMAP rather than here: TC.2's
  counterfactual names an observability precursor and the precursor had no date,
  no owner and no code. Filed as scope DISCOVERED, not slippage — it adds to BAC
  and EV together. Also corrects a claim made earlier in the same session that
  BoS levels needed capturing: they do not, and reading HEAD is what settled it.
- **v3.54 — 2026-08-04 — TWO DATES CORRECTED TO MATCH WHAT THE ITEMS SAY ABOUT
  THEMSELVES.** **AV** moved Sat Aug 1 → Thu Aug 13 and re-tagged `[DESK·DATA]`:
  dated due 08-01 while its own text records it OPENED 08-02 — due before it
  existed — and it waits on ~40 trades per cell for a 0.20 R read, a DC&A
  dependency rather than effort. **A2.3** moved Sun Aug 2 → Mon Sep 7: its own
  first line reads HOLD UNTIL AFTER GO-LIVE (Aug 31) while it was counted overdue
  against execution. Neither is slippage recovered; both are schedule errors that
  were inflating the accountability number.
- **v3.53 — 2026-08-04 — STATUS SCRUB. FIVE MORE DUPLICATE IDs, AS RESOLVED,
  AW's THREE NEXT-ANSWERS ALL SPENT.** The A2.6/L1.9 split in v3.52 was not the
  whole problem: `M.3`, `TC.4`, `G`, `L3.2` each named two different items and
  `Level` named three — 66 item lines carrying 60 unique IDs, so six items were
  invisible to the register and any one ✅ would have closed its twin. Now
  M.3a/b, TC.4a/b, G.1/G.2, L3.2a/b, Level.1/2/3. **AS ✅** — its lifecycle
  deliverable exists (`analysis/pitchfork_lifecycle.py`, now v1.4) and AW's own
  text records having run through it. AW updated with all three of its named
  cheapest-next-answers and their results; every one points at AP.
  FLAGGED, NOT APPLIED, because both need the item moved under a different date
  header rather than an edit in place: **AV** is dated due 08-01 but was OPENED
  08-02 and waits on ~40/cell for a 0.20 R read with an 08-13 review — mis-dated
  and mis-tagged `[DESK]` when it is `[DESK·DATA]`. **A2.3**'s own first line
  says HOLD UNTIL AFTER GO-LIVE (Aug 31) while it sits dated 08-02 and counted
  against execution. Together worth about -2 on DESK overdue, and neither is
  slippage.
- **v3.52 — 2026-08-04 — DUPLICATE IDs SPLIT.** `A2.6` and `L1.9` were each two
  distinct items under one ID — a register defect, not a formatting one: the EVM
  parser keys on the token, so a single ✅ would have closed both and credited
  work nobody did. Now `A2.6a`/`A2.6b` and `L1.9a`/`L1.9b`. Bare cross-references
  elsewhere in the file are flagged unresolved rather than guessed; the pairs are
  treated as separate items until verified.
- **v3.51 — 2026-08-04 — THE TWO-POPULATION SPLIT, AND FIVE MEASUREMENT
  DEFECTS CLEARED.** The operator's reframing governs the pre-go-live work from
  here: separate trades that were NEVER favorable — not for one tick, so there
  was never anything to manage — from winners that gave gains back. The first is
  a SELECTION problem, the second an EXTENSION problem, and pooling them is why
  "which exit is losing money" kept returning the wrong answer. Standing
  evidence: every losing exit has MFE ~ 0 (max_loss_floor_25pct -0%,
  max_loss_floor_24pct 0%, orb_structure_stop +1%, bos_exit +2%, stop_hit +6%),
  uniform across four exits and three strategies. Leading candidate cell
  TRENDING_BEAR / ContinuationStrategy: n=30, 27% win, -$2,852.50, avg -$95.08 —
  65% of continuation's whole loss in 17% of its trades. **bos_exit is NOT a
  standing loser**: n=34 cumulative, net -$298; the -$2,757 was one session.
  **The trail is not the candidate either** — trails hand back ~22% of peak and
  still realize +15% to +30% on winners; that giveback IS the leash distance.
  Tooling: excursion_report v2.3/v2.4/v2.5, trade_report v1.4,
  consolidate_trades v1.3, trade_logger v3.9. AX resolved. AP re-tagged
  `[DESK·DATA]` — it was counted against execution while waiting on ripening.
- **v3.50 — 2026-08-03 — BOS IS NOT CUTTING LIVE MOVES; AY's THIRD ITEM
  CORRECTED.** `post_exit_continuation` v1.0 measured what giveback cannot — does
  price keep running after an exit fires — and `bos_exit` shows **no separation
  from other exits at 5, 15 or 30 minutes**. So today's -$2,757.50 was GIVEBACK,
  not early exit, and **the trail is the candidate rather than the BOS trigger**.
  I had filed the opposite reading off MU's six 2.8-minute trades before measuring
  it. Three caveats recorded with it: every bos cell is UNDERPOWERED (n=17 vs MDE
  0.18-0.41%, needs n≈113); **41% of rows dropped** for no tape at the exit
  instant, so selection bias is possible; and the clearest signal in the table is
  `max_loss` running -0.065 → -0.205 → -0.341% — price continues AGAINST the trade
  after a max-loss exit, so the day's second-largest line item was the stop
  working.
- **v3.49 — 2026-08-03 — TWO SOLO DESK ITEMS CLOSED, ONE AS A NEGATIVE.**
  **Historical ADX reconstruction ❌ closes as NOT SUPPORTABLE**: the held-out
  check (reconstruct rows that already have a real value, compare) fails at every
  tolerance — below 900s the overlap is too thin to judge, at 900s+ median error
  runs 1.90 → 6.28 → 7.88 ADX points. `regime_log` writes on regime CHANGES, not
  ticks (457 rows/month, p50 gap 600s), so a preceding row minutes old does not
  describe ADX at entry. Widening until something writes would have produced
  plausible wrong numbers, which is worse than a 0.0. Kept: the `staleness_s`
  column, so future joins carry their own caveat.
  **Item I ✅ RESOLVED — delete the branch**: 3 butterfly trades ever, all before
  15:00 ET. The FIRST run said the opposite because `entry_time` is stored in UTC
  and v1.0 compared the raw clock to an ET cutoff — right action, backwards
  reasoning, corrected in v1.1 which now prints ET and UTC side by side.
  Also recorded: adx_reconstruct v1.2 gains MIN_OVERLAP=8 after the first fleet
  run reported PASS/FAIL verdicts on overlaps of n=1.
- **v3.48 — 2026-08-03 — THE GAP-DAY MISREAD, AND TWO MISSES THE SAME SESSION
  EXPOSED.** New **AY**. The tape: MSFT +4.93%, AMZN +4.58%, NFLX +2.26% with the
  ENTIRE move in the opening bar, then hours of chop. TRENDING is ADX-14 on 5m ≈ a
  70-minute window, so a 5% opening bar keeps the label TRENDING_BULL for an hour
  after the move ends — **30 trades, −$2,943.** Exactly the **CONT × OPEN 9.89%**
  cell the clean A2 partition already flagged, and **not** an odd day: gap days are
  **93% of session-symbols** (CONT 40.4% / REV 52.7% / FLAT 6.9%). **AV's Aug 13
  revisit is re-aimed at that one named cell** using `gap_outcome_join --window
  OPEN` — no new tool. Also filed: **TSLA never woke** (#18, sc 0.0704) then gave a
  clean +3.49% leg — a SELECTION miss no exit fix reaches, revisit ~09-05 once ranks
  accumulate; and **MU**, woken, 60-minute move, **6 trades at 2.8 min for −$377** —
  the `bos_exit` giveback (+11%) that is 88% of the day's loss. Process lesson
  recorded: the flicker cost −$234 and got four tools; bos_exit cost −$2,757 and got
  attention only after the excursion report forced the comparison.
- **v3.47 — 2026-08-03 — POSTMORTEM FILED; +AX (conductor cannot send Telegram).**
  `docs/POSTMORTEM_2026-08-03.md` sorts the day into DEFECTS (wrong regardless of
  how permissive the fleet is — and corrupting the sample we are collecting) and
  PERMISSIVENESS COSTS (the system took the trade it was designed to take and the
  environment did not cooperate — **this is the data**). The flicker is bucket 1:
  regime_flip exits have median hold **0.8 min, p25 12 SECONDS** against 5-12 min
  for every other exit reason, and each one writes a row that will later be
  miscounted as evidence about continuation in a trending regime. Fixed same day
  by **main v5.0**, live on 29/29. MSFT −$1,169 and QQQ −$1,327 are bucket 2 —
  good setups, price chopped, and deleting that observation would be the error.
  New **AX**: the conductor's Telegram was never wired, so every EOD warning it
  has raised has gone unread — including tonight's 7 permanently-missing symbols.
- **v3.46 — 2026-08-03 — THE HOURLY FORK IS NOT A LEVEL, AND THAT RE-SCOPES v4.0.**
  New **AW**. AS's lifecycle worked — Predictor 2 went REFUSED-at-78 to n≈210 —
  but coverage came in at **10.1% mean / 5.3% median / 0.0% min**, so the fork is
  genuinely rare on real tape as well. That **kills the L1 corroborator at hourly**
  (an input absent 90% of the time is a two-mode classifier). **2b reversion is a
  clean null** (r²≈0.001) — price does not return to the median line, which was
  Andrews' central claim and the load-bearing test. **2a slope is dead at minute
  horizons for ANY timeframe**, daily included, since a daily ML moves even less
  per minute. What survives is §6's split, now with a reason: **daily → levels,
  hourly → touch events.** **PF.3 moves behind AP** because strikes are a level
  question, and **the v4.0 gate moves with it** — every surviving consumer is
  level-based. Exhaustion is now three independent measurements sharing a sign and
  gets promoted from footnote to directed test. `pitchfork_filter_audit` **v1.3**
  adds cause-of-death and lifetime bins to settle whether the §5.3 priors are
  strangling the object or the tape genuinely breaks it.
- **v3.45 — 2026-08-03 — SENTIMENT SCORE RECORDING STARTS; THE ANALYSIS IS FILED
  OUTSIDE THE PLAN.** Operator's idea: weight directional trades by the morning
  sentiment score, never veto. Turns out `setup_scorer` v1.2 ALREADY has a signed
  brief nudge — but it keys on STRATEGY TYPE (ORB +1, condor/butterfly -1,
  continuation absent), not trade direction, so it does not do what was described.
  It also only started working at all after the 07-30 DTP_REPORT_JSON fix; the
  08-03 wake is the first with `str` actually varying per symbol. `eod_conductor`
  **v1.12.0 phase 5c** archives `report.json` daily with a freshness check, since
  it was being overwritten every morning and the scores destroyed. Analysis filed
  in **PART 2, outside the EVM plan**, to revisit ~09-05. Watch: XOM printed the
  old 0.30 fallback exactly while every other name varied.
- **v3.44 — 2026-08-02 — THE BOTTLENECK IS n, NOT THE METRIC. AV GETS A DATED
  REVISIT TRIGGER.** `gap_outcome_join` v1.4 added `--metric r|winrate|pnl` and a
  power line. **R did not reduce variance, it rescaled it** — sd 340/0.318 and
  detectable 188.5/0.176 both give $1,070, so `max_loss` is near-constant and the
  risk manager is sizing consistently; the $340 sigma is OUTCOME dispersion with
  no size component to strip. Win rate is worse (27.8 pp detectable at n=51).
  The clean window also **erased the condor CONT/REV split** that looked like the
  one real signal — it was a confounded-window artifact. **Trigger set: re-run
  ~2026-08-13** when continuation clears n≈40/cell, which reads a 0.20 R effect;
  0.10 R lands ~09-15, after go-live. Parked deliberately, not blocked — the
  operator's call is to let it accumulate on the current engine, which is running
  several sessions of positive expectancy at the post-fix trade rate.
- **v3.43 — 2026-08-02 — A2 WAS THE INSTRUMENT, NOT THE SIGNAL.** New **AV** +
  `tests/gap_outcome_join.py` v1.0. The clean corpus killed the tradeable reading
  of A2 — no drift edge at any horizon or elapsed bucket (so A2.5 as a live drift
  factor should be DROPPED), the wrong-theta-sign hypothesis unsupported, and a
  ~3% excursion difference that does not move a condor. What survived is
  **gap class x time of day**: flat opens are dead for 70 minutes then run ~4x hot
  at 10:40-12:00, gap days are hot at the open and decay. Nothing in the fleet
  keys on that. The tool joins banked trade outcomes to gap class — **ORB first**,
  since it forms its range in exactly that window and AH has it at -0.24R over 252
  trades with no explanation. No new collection required.
- **v3.42 — 2026-08-01 — CLEAN CORPUS. AT RESOLVED, AQ AND AR FINAL, AND ONE OF
  MY VERDICTS WAS WRONG.** Regen finished 15/15 (~5h50m); all four tools re-run.
  Headline **3.98%**. **Only the OPEN row moved** — v2.1 touched only the opening
  24 ticks per symbol-session, and the grid shows exactly that and nothing else.
  **The DECAY×FLAT hump survived and sharpened to 13.78%** with baseline shoulders
  either side, while **H2 flipped to NOT SUPPORTED** (flat-open mornings 3.60% vs
  3.55% midday) — so there is no opening drive, and on a flat-open day the
  tradeable window is **~10:40-12:00, not the open**. **H3 is PARTIAL, not dead:**
  I called it dead partly because the ADX medians pointed the wrong way; clean,
  they point the RIGHT way (CONT 52.4 > FLAT 50.2 > REV 46.6, monotone, as the
  ablation predicted). Excursion firmed up and now reads consistently across
  horizons. Predictor 1's negative held, so A2.5 as a live drift factor stays
  unsupported. Rail drift unchanged — **AS is its blocker, not data.**
- **v3.41 — 2026-08-01 — THE BLIND ALERT COULD NOT BE SENT, AND FOUR LAYERS OF
  TOOLING SAID IT COULD.** Filed as **AU**, amending AL. `parse_mode="HTML"` means
  any unescaped `<`, `>` or `&` gets the whole message rejected with a 400 — and
  the blind alert interpolates forensic fields and live position descriptions,
  with main.py's own fallback being `"<position read FAILED>"`. So the page died
  exactly in the compound failure it exists for. `alert_manager` **v1.10** escapes
  in `_send`. Underneath it: bare `python3` on the boxes (no pandas), `; true`
  laundering the exit code into "29/29 succeeded", `_send` discarding a boolean
  TelegramSender has always returned, a hardcoded `check(..., True)`, and
  credentials living in the systemd unit where an SSH run cannot see them.
  Now verified on 29/29 with both messages arriving. Rule earned: **a green from a
  laundered exit code is worse than a red**, and an alarm-tester that cannot
  observe its own failure converts an unknown into a false assurance.
- **v3.40 — 2026-08-01 — THE REGEN WAS STILL RUNNING WHILE WE MEASURED.** Filed
  as **AT**. `--backfill --rebuild` started 16:54 and was still on the last date
  at 21:31 — 4h37m. I called it finished because a2_partition reported "corpus
  files: 15", but all 15 files existed throughout; the regen overwrites in place,
  so file count cannot distinguish done from running. Every A2 number from
  2026-08-01 therefore came off a mostly-stale corpus with a few v2.2 dates mixed
  in: **the 4.14% baseline, the whole partition grid, the DECAY×FLAT hump, the
  excursion distributions, the strike and stop numbers, the episode durations,
  and Predictor 1's negative are all PROVISIONAL.** AS and the pitchfork audit are
  unaffected — that tool reads the 1m tape, not the corpus. Rule earned: *"the
  artifacts exist" is not "the job finished"* — check the process, not the files.
  And a full regen is a ~5 hour job; do not run a suite against the same box.
- **v3.39 — 2026-08-01 — THE FORK HAS NO LIFECYCLE, SO I MEASURED ITS BIRTH RATE
  AND CALLED IT COVERAGE.** The filter audit ran: 2,297 attempts, 156 forks built
  (6.8%). But `build_fork` is stateless and §5.2 says a fork HOLDS UNTIL
  INVALIDATED — 156 births across 29 symbols is ~5 anchor events per symbol in
  three weeks, which is right for a persistent object. `a2_rail_drift` used the
  fork as a per-bar indicator, the one thing the persistence mandate says it is
  not, so **AR's Predictor 2 is a NON-RESULT rather than a negative.** New **AS**:
  build §5 lifecycle first, re-run, and only then look at SEPARATION (39.8% of
  rejections) — which may be an implementation reading of §4.3.5's uniqueness rule
  rather than a threshold at all. The audit's own verdict was mis-binned and is
  corrected in v1.1: STRUCTURAL_* is the engine correctly refusing chop, not a
  tight filter, so the honest split is ~52% no-structure / ~41% parameter-
  sensitive / 6.8% built. **Predictor 1 stands as a real negative** — elapsed
  persistence does not predict drift, so A2.5 as a live drift factor is not
  supported and the --persistent-only edge was look-ahead.
- **v3.38 — 2026-08-01 — THE STATE IS A 2-BAR FLICKER, THE POOLED MEAN WAS THE
  WRONG STATISTIC, AND THE FORK IS THE PREDICTOR.** Median paused-trend episode is
  2 bars. `--persistent-only` showed drift AND stillness moving monotonically
  together across 2/3/5 bars (drift +0.0047/+0.0080/+0.0184, excursion p90 −12%/
  −14%/−22% vs control) — but that mode CONDITIONS ON THE FUTURE and cannot drive
  a gate. New **AR** + `tests/a2_rail_drift.py` v1.0 replaces the pooled mean with
  two tick-knowable predictors: ELAPSED persistence (no forward conditioning) and
  MEDIAN-LINE displacement from PF.1's fork, split into slope vs reversion and
  reported as regressions so opposite-signed trends stop cancelling each other
  out. Confirmation lag preserved via `now_idx` = last completed hourly bar.
  Self-correction kept on the record: I called a +41 coefficient a scaling bug; it
  was a real 93x scale mismatch and the formula was right — the tool now prints
  predicted-vs-realized magnitudes so nobody repeats that read. Also filed: two
  a2_excursion defects (no CI on the excursion verdict; no control on
  favorable/adverse), and the wrong-theta-sign hypothesis for continuation is NOT
  supported.
- **v3.37 — 2026-08-01 — A2 IS A REAL STATE. THE QUESTION IS NOW WHETHER IT PAYS,
  AND TO WHICH SIDE OF THETA.** The partition ran on the regenerated corpus:
  150,517 ticks, 4.14% violations. H1 horizon and H2 drive SUPPORTED, **H3 gap
  dead as a cause** — no reversal-gap deficit, and the ADX medians point the wrong
  way. Gap class proxies for DAY TYPE. Strongest single finding, which the tool
  did not flag: **DECAY×FLAT 13.88% is the highest cell in the grid**, and FLAT is
  the only class that humps instead of decaying — on a flat open the drive is
  displaced to ~10:40-12:00 and the violations follow it.
  New **AQ** + `tests/a2_excursion.py` v1.0. Theta sign is the axis (the butterfly
  is a debit structure that is theta-POSITIVE, which is why credit/debit is the
  wrong split): signed drift for the long-theta book, max |excursion| and its
  DISTRIBUTION for the short-theta book — the distribution IS a strike rule, and
  mean adverse excursion is the floor under a non-noise stop. Corrects
  a2_partition's own closing line: CLEAN×FLAT is gap-clean but DAY-TYPE-SELECTED.
  **Episode duration is now reported first** — a horizon longer than the median
  episode measures mostly out-of-state tape, found by running the tool rather than
  reasoning about it. **Undefined-risk structures ruled OUT OF SCOPE**: SPX
  nominal size makes a naked strangle unaffordable, the constraint is protective,
  and the risk layer's inability to size one is a feature to preserve.
- **v3.36 — 2026-08-01 — THE DAILY FORK GETS A SOURCE, AND IT IS OUR OWN TAPE.**
  `daily_bars.py` v1.0 + `eod_conductor` v1.11.0 phase 5b + 14 tests rebuild
  `daily/<SYM>.csv` nightly from the 1-minute tape harvest already lands. yfinance
  was the obvious candidate and is the wrong one — purged for low-timeframe
  disparity, capped at 21 sessions on 1m, and fatally: **re-anchoring an
  invalidated fork needs bars current at that moment**, so a manual pull is stale
  the next day and a recurring one restores the dependency the purge removed. The
  agreement-check script was proposed and dropped: with the series coming from our
  own tape its result changes no decision. Rebuild-not-append so late backfills
  self-heal; after phase_backfill so the tape is complete; partial sessions
  flagged rather than dropped. **AP is ◐ not ✅** — ~15 sessions is the floor with
  zero margin, and distribution to the boxes is a PF.4 problem.
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
