# docs/BACKLOG.md — v2.0

**CHANGELOG**
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

---

## PART 0 — THE CLOCK

| Anchor | Date | What |
|---|---|---|
| Today | **Wed Jul 29** | Epoch 1 begins immediately |
| Deploy Monday 1 | **Mon Aug 3** | Hard gates (E, F) + friction unification (T.2) go live on the fleet, RTH |
| Deploy Monday 2 | **Mon Aug 10** | THE calibration deploy (level hierarchy, L2.4 priors, L1.6 flat cut, L1.11 ramps) — **L2.6 freeze-candidate window opens** |
| Freeze declared | **Fri Aug 21 EOD** | L2.6 frozen baseline, if the window ran clean |
| Deploy Monday 3 | **Mon Aug 24** | L3.3 gate matrix (flagged, paper) + evidence-confirmed sweep changes |
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

**Standing daily habits (every session, all epochs):** `label_day.sh` at EOD
(feeds L1.6/L1.7 — habit, not code, is the remaining work) · AA-watch: check for
any two-sided condor firing both legs near-simultaneously · verify the chain-snapshot
harvest landed (once shipped Jul 30).

---

## PART 1 — THE SCHEDULE (open items, in accomplishment order)

### EPOCH 1 — SCRUB & INSTRUMENT — Wed Jul 29 → Sun Aug 9

*Goal: suite green, canaries current, time-critical data harvested, the two
never-built gates built and proven, the bookmark live, mapper hierarchy proven on
the tester. Nothing behavior-changing deploys except on Mon Aug 3.*

**⬜ Wed Jul 29**
- **T.1 — Fix the red suite at HEAD.** `test_entry_fill_confirmation.py::test_paper_entries_mirror_live_friction`
  still asserts defect-R behavior (paper single fills at mark×1.01); `entry_engine`
  v3.8 deliberately books the bare mark. Update the test to the mark-limit contract.
  DONE = 36/36 green at HEAD.
- **T.3 — Delete the dead import.** `position_manager.py` imports
  `PAPER_FILL_SLIPPAGE_PCT` and never uses it. Remove; bump header + changelog.
- **U — Canary refresh.** `check_versions.sh` has no canaries for anything after
  07-18: sweep v3.2 ORB-ownership, main v4.0 L2 wiring / v4.2 chain_snapshot,
  regime_confluence v1.2 bounds, orb_engine v3.9 timeout, `limit_ladder.py`,
  `FLATTEN_WINDOW_OPEN_ET`, status v1.13. Add them all. DONE = a stale sync of any
  07-20→07-28 file fails the check.

**⬜ Thu Jul 30**
- **P5.1 — Chain-snapshot harvest (TIME-CRITICAL).** `harvest.py` pulls OHLC +
  `trades.db` only; `data/chain_snapshots/` accumulates on 29 boxes with **no copy
  on control** — an unselected strike's quote is gone permanently at 16:00, and any
  box rebuild takes that symbol's archive with it (~1.4 MB/box/day gz). Add the
  harvest step to the EOD pull. Every day this slips is a permanent hole.
- **Z — `consolidate_trades.py` date filter (day_trader_pro side).** Rollups are
  not date-clean (61% of condor legs sat in a wrong-dated file;
  `fleet_trades_2026-07-13.json` holds only 07-07→07-10 trades). Fix: filter by
  `entry_time[:10]`, dedupe by `trade_id`; regenerate the rollups from the per-box
  DBs. DONE = every row's entry date matches its filename.
- **T.2 — Decide the condor paper-friction split** (code today, deploys Mon Aug 3).
  Condor paper credits still take the `PAPER_FILL_SLIPPAGE_PCT` haircut while
  singles/butterflies book the raw mark. Live condor entries are already mid-credit
  limits, so the mark-limit rationale applies: unify (or write down, in MECHANICS,
  exactly why condors keep the haircut). One model, documented.

**⬜ Fri Jul 31**
- **D (service half) — Templatize `shadow-observer.service`.** The unit hardcodes
  `/home/ubuntu/options-trader`; sed the path at install time like `setup_ec2.sh`
  does for `optionsbot.service`. Zero behavior change on the fleet (canonical path
  matches); closes the last half of defect D before any non-standard-path deploy.
- **E (build) — `VWAP_FILTER_ACTIVE` hard gate, on the TESTER.** The genesis
  constant that was never wired: VWAP misalignment today costs 11 points against a
  55 bar and cannot veto (a short into strength still fires at Grade B).
  `crypto_trader` learned this the hard way — shorts above VWAP / longs below VWAP
  became hard blocks after a relaxed validator produced consecutive losses. Port the
  lesson: hard block, env-tunable, **ORB exempted** (defect V made the ORB
  deliberately regime/VWAP-agnostic — the gate applies to the scored strategies).
- **F (build) — `MIN_RRR` floor, on the TESTER.** Second genesis constant, same
  story. The ORB's RRR is structural and varies per setup, currently ungated. Build
  the floor env-tunable, applied at scoring for non-ORB paths; log-only counter for
  the ORB first (measure how often a structural ORB would fail it before gating a
  mechanical trade).

**⬜ Sat Aug 1**
- **E + F tester proof.** Replay both gates over the banked 07-13→07-31 tape:
  enumerate every historical trade each gate would have blocked, with outcomes.
  DONE = a would-have-blocked ledger showing the gates remove net-negative trades
  (if they don't, the defaults ship OFF and the gates ship as log-only counters —
  evidence decides, per house rule).
- **S / L1.9 — BOOKMARK build starts, on the TESTER.** Rolling ~15-session window
  of **bars** per symbol (bars, not engine state — the engines are stateless),
  load+append+roll each EOD, score today warm. This unblocks honest offline
  TRENDING and everything L1.6/L1.11 need.

**⬜ Sun Aug 2**
- **L1.9 bookmark tester proof.** Run against copies of real `ohlc/<date>/`
  folders; prove byte-inert on the diary for warm-irrelevant days and prove the
  EOD conductor chain is untouched. The conductor is finally flawless — it stays
  that way.
- **M.3 — Dedicated Telegram bot for options-trader notifications.** Promoted from
  nice-to-have to **go-live requirement**: live trading needs its own paging channel
  before Aug 31. Build today, live-test Thu Aug 27.

**⬜ Mon Aug 3 — DEPLOY MONDAY 1 (fresh RTH rollout)**
- Deploy **E** (VWAP hard gate) + **F** (MIN_RRR floor) + **T.2** (condor paper
  friction unification) to the fleet in one option-23 pass; verify canaries before
  restart. Fire-rate watch all session — these are the epoch's behavior changes,
  and the clean-baseline note resets here.
- **TC.4 (T+1wk) — readiness digest check.** `_trend_credit_spread` journal has
  been accumulating since 07-28; confirm fleet-wide capture is clean.

**⬜ Tue Aug 4**
- **L1.9 — Graft the proven bookmark onto `validate_regime.sh`**, then run
  `regime_backfill --rebuild` to re-score all dated diary rows warm. DONE = the
  diary reads TRENDING honestly on the days live boxes did.
- **TC.4 — SD-bounds fit PR.** Run `readiness_digest`, fit
  aware/established/screaming SD bounds + room/extension bounds + corroborator
  weights from the observed distribution. Priors → calibrated knobs (env flips, no
  bake). The firing engine stays unbuilt — gated on the L1 excavation and the
  freeze, per the roadmap's three gates.

**⬜ Wed Aug 5**
- **Historical ADX reconstruction.** Timestamp-join `regime_log` → trades to
  backfill `adx_at_entry` on pre-07-27 rows (deferred at the 07-24 fix; the warm
  rebuild makes it worth doing now). Offline, control-side.
- **L1.6 (first pass) — flat-angle sweep.** 16–26° against the rebuilt multi-day
  diary (07-14 → 08-04) with the rotating 30% holdout — never off one day. Output:
  the candidate frozen cut, staged for the Aug 10 deploy.

**⬜ Thu Aug 6**
- **Level hierarchy + Overnight High/Low — build on the TESTER** (queued 07-24).
  Add `overnight_high`/`overnight_low` (extremes across the Asia+London span) to
  LiquidityMap as a named tier; replace the flat `is_named` bool with graded
  `level_strength` per the stated hierarchy: **ON H/L ≈ PDH/PDL (top) > historic
  multi-day S/R (mid) > individual session H/L > equal-H/L (lowest)**. Mapper logic
  touches what sweeps fire against — tester-first, no exceptions.
- **Sweep level_strength — first look.** 07-27→08-06 sweeps bucketed by
  `level_strength` (the capture shipped 07-24). Observation checkpoint only; n is
  still small. No action.

**⬜ Fri Aug 7**
- **Level hierarchy tester proof complete.** Inert where it should be; the
  postmortem buckets become meaningful only once the tiered value flows.
- **L1.7 Tier-B ledger check.** With the warm rebuild + three weeks of labels:
  which rows close? TRENDING should now be closable if any labeled trend day
  exists 07-14→08-07; SWEEP needs one mapper-confirmed named-zone reclaim;
  COMPRESSION needs a coil-into-pin session; BREAKOUT needs one more clean hold
  through the BB re-entry flicker. Close what the tape supports; the rest is
  calendar, not code.
- **G (data checkpoint).** Snapshot the `retest_depth` distribution (3 weeks
  accumulated). No decision yet — that's Aug 22.

**⬜ Sat Aug 8 – Sun Aug 9 (weekend calibration fit)**
- **L2.4 — Fit the integrator priors offline.** θ_commit/θ_hold/δ_displace,
  dt_max/τ_stale, per-regime τ_up/τ_dn0/λ — recomputed from the labeled-tape
  bar-count distributions (the RANGING τ_up=780 template), judged on the churn
  metric, never P&L. This closes the L2.5-shipped-ahead-of-L2.4 inversion the
  roadmap flags as the priority.
- **L1.11 — Fit the remaining ramps** (`flat_s` on its conditional population;
  `adx_s`/`align_val` from warm-bookmark or live `feed_store.db` depth — the L1.9
  gate is now open). Stage into the same calibration PR.
- **Epoch-1 exit review:** suite green ✅ · canaries current ✅ · chain harvest
  running ✅ · bookmark live ✅ · hierarchy proven ✅ · E/F live with a
  would-have-blocked ledger ✅ · calibration PR staged ✅.

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

**⬜ Tue Aug 11**
- **L3.1 close-out.** Confirm `signal_journal` jsonl captures full fleet sessions;
  wire the EOD-conductor collection phase (harvest the jsonl off-box — deliberately
  unwired until now, volume justifies it). Log-only; freeze-safe.

**⬜ Wed Aug 12**
- **P3 phase 1 — index-context broadcast, log-only.** Control-side writer pushes
  SPX/QQQ regime+conviction via the existing `brief_flags.json` pattern; one
  journaled field on every `scored` event. `conditional_tables.py` grows the
  index-confluence dimension for free. Ungated, freeze-safe.

**⬜ Thu Aug 13**
- **L3.2 — rejection ledger build starts.** `analysis/rejection_ledger.py` +
  `reports/rejection_summary_<date>.jsonl` + digest. Class (a) threshold near-miss
  consolidation from L3.1 events; prove the forward-outcome join leak-free on a
  known session (outcomes only from post-decision bars). Version-hash every row.

**⬜ Fri Aug 14**
- **P5.3 — run `chain_reconstruction_check`** on ~3 weeks of archive. PASS → build
  ChainReplay (post-freeze); PARTIAL → grid restricted to the validated moneyness
  band, stated in the header; FAIL → the missing piece is named by the `+vega·ΔIV`
  column (IV-path model vs cadence) and gets a date before any harness work.

**⬜ Sat Aug 15 – Sun Aug 16**
- **L3.2 finish.** Class (b) coverage-gap scan (per strategy: was a live setup
  present during its target condition with no signal formed?); both classes
  populating across a fleet session. Pre-freeze rows tagged gap-finder grade;
  post-freeze rows will be calibration grade.

**⬜ Mon Aug 17** *(no deploy — freeze holds)*
- **K — re-arm decision, on paper.** Decide between the current deliberate
  hand-off-to-sweep and the unified rule ("re-arm on any invalidation before
  11:00; the origin gate decides whether a break is real" — the v3.5 origin gate
  makes runaway re-arm safe by construction). Write the decision here; any code is
  a post-freeze item (Aug 24 if changed).
- **I — butterfly cutoff branch decision.** `can_enter(is_butterfly=...)` is
  unreachable; either fix the `main.py` call site (if a 15:00 butterfly cutoff is
  ever wanted) or delete the branch so config and code stop disagreeing. Decision
  today; code post-freeze.
- **AA checkpoint.** Any two-sided condor with both legs near-simultaneous since
  07-17? Post-fix sample was 7 legs at last count. If clean through ~4 weeks,
  close AA as superseded-by-Y+rich-triggers; if recurred, it gets a forensic slot
  Aug 22.

**⬜ Tue Aug 18 — sweep evidence day (the decision the whole sweep track waits on)**
- **Level-conviction lead:** win-rate/expectancy by `level_strength` bucket at
  ~3 weeks of current-engine data. If equal-H/L sweeps are the losers → a
  level_strength floor on the sweep gate is confirmed.
- **Reclaim looseness:** do losing sweeps carry higher `closes_beyond` than
  winners? If yes → require `closes_beyond == 0` post-reclaim (or hold-N-candles).
- **Exit asymmetry / washout fingerprint:** does 75%-win/negative-net hold on the
  current engine? Stop-width vs winners' realized magnitude; washout-day regime
  tags.
- Output: the exact list of sweep changes that are **evidence-confirmed** for the
  Aug 24 deploy. Anything unconfirmed stays OBSERVING — do not fix what the data
  hasn't convicted.

**⬜ Wed Aug 19**
- **Build the confirmed sweep changes on the TESTER** (level_strength floor and/or
  reclaim tightening and/or stop tightening — only what Aug 18 convicted). Mapper/
  strategy logic → tester-first, deploy Mon Aug 24.

**⬜ Thu Aug 20**
- **L3.3 — gate matrix behind a flag, built + tester.** `fires iff regime ∈
  permissive AND C ≥ bar(trade_type)` in dispatch; provisional bars ORB/sweep
  ~0.40, condor ~0.65, butterfly ~0.70; flag-off byte-identical to today. Deploys
  Mon Aug 24, paper.

**⬜ Fri Aug 21 — FREEZE DECLARED (EOD)**
- **L2.6 ✅ if the window ran clean** (no L1/L2/entry deploys since Aug 10, churn
  nominal). This is the real gate for everything downstream — pitchfork, P1/P2/P4
  conviction dimensions, ChainReplay, TC.4 firing engine all key off this date.
  If the window broke, the clock restarts and every date below slides by the same
  amount: say so here, don't pretend.
- Epoch-2 exit review; `conditional_tables.py` begins pooling post-freeze rows
  (the only rows that are decision-grade).

**⬜ Sat Aug 22 – Sun Aug 23**
- **G — decision.** Feed `retest_depth` into `orb_quality` or drop it: 5 weeks of
  distribution + the Phase-3 ROI buckets now exist to answer it. Decide from the
  data; the measurement gates nothing until then.
- **L3.5 — enforce the holdout in the bucketer.** Fit sessions ≠ acceptance
  sessions inside `conditional_tables.py`; slippage-haircut P&L only. The Aug 31
  descent bars come from held-out cells or they don't come.
- **Live shakedown prep:** broker account funded · `configure.sh` mode-switch
  dry-run (defect-Q archive machinery fires, `trades_<mode>_<stamp>.db` lands) ·
  tiny-size live config staged (1-contract sizing, SPX + QQQ only) · **J
  (disposition):** the 07-23 header audit restored title/changelog sync; accept
  the v3.0-era legibility loss as historical, keep `check_versions.sh` as the
  deploy-truth tool, and close J as WONTFIX-by-policy unless someone objects here.

---

### EPOCH 3 — GATES ON & GO LIVE — Mon Aug 24 → Fri Sep 4

**⬜ Mon Aug 24 — DEPLOY MONDAY 3 (fresh RTH rollout)**
- Deploy: **L3.3 gate matrix** (flag on, paper, bars provisional/wide) + the
  **Aug-18-confirmed sweep changes** + any K/I code decided Aug 17. Fire-rate
  watch all week. **L3.4 campaign formally starts** on post-freeze data and runs
  underneath everything from here on.

**⬜ Tue Aug 25**
- **Mode-isolation live-switch rehearsal on ONE box.** Switch paper→live→paper;
  verify defect-Q end-to-end: archives created, mode-scoped queries return zero
  cross-mode rows, no paper row visible to the live loop, breaker reads only live
  P&L.

**⬜ Wed Aug 26**
- **Entry/exit path shakedown vs the resolved audit (N/O/P).** Re-run
  `test_entry_fill_confirmation`, `test_roll_is_real`, `test_mode_isolation` at
  HEAD; walk the order_confirm deadlines, cancel-and-walk-away, partial booking,
  and paging paths against the tiny-account config on paper.

**⬜ Thu Aug 27**
- **M.3 — Telegram bot live test** (built Aug 2): pages route to the dedicated
  options-trader channel; half-complete-roll and phantom-P&L pages verified.
- **M.1/M.2 — Windows residue documented.** Ghost folder on tarball extraction +
  `setup_ec2.bat` security warning: fix if trivial, else document the workaround
  in the deploy README and close as documented-known.

**⬜ Fri Aug 28 — GO/NO-GO REVIEW**
- Gate checklist, every box or no-go: suite green at HEAD · canaries pass fleet-
  wide · freeze intact since Aug 10 · gate matrix behaving across 4 paper
  sessions · mode-isolation rehearsal clean · fill-confirmation shakedown clean ·
  paging live · live config staged (1 contract, SPX+QQQ, bars one bucket above the
  paper crossing per L3.6).

**⬜ Sat Aug 29 – Sun Aug 30**
- Live-day runbook written (who watches what, the raise-back trigger, the
  kill-switch: `OT_REGIME_ENGINE=v13` rollback path re-verified, configure.sh
  back-to-paper path re-verified). Final rehearsal.

**⬜ Mon Aug 31 — GO LIVE, RTH (tiny size)** 🎯
- **L3.6 descent, step 0:** live, minimum size, SPX + QQQ, bars one bucket above
  the paper crossing. This is the tiny-account live shakedown that has gated the
  fill-confirmation work since 07-15 — now with the whole scrub list behind it.

**⬜ Tue Sep 1 – Fri Sep 4 — LIVE, first week of September** ✅
- Daily: fill-quality audit (live fill vs mark, per the 07-15 divergence-audit
  template) · phantom-P&L reconcile check at each close · ladder fill-latency
  logged (this is the TC.2 stop-trigger dataset — the −40% trigger vs 35%/25%
  question gets answered by these numbers, not by guessing).
- **Fri Sep 4:** week-1 live review — divergence report, latency distribution,
  descent decision drafted.

---

### RAMP — Mon Sep 7 → Fri Sep 18

**⬜ Mon Sep 7 — Labor Day, markets closed.** Analysis day: first live-week
conditional tables; confirm the newly-admitted buckets' realized expectancy;
finalize the descent decision.

**⬜ Tue Sep 8 — descend one notch.** Half size and/or widen the symbol set —
only if week 1 was clean. Raise-back trigger stays armed: first negative read on
a newly-admitted bucket → back up a notch, no debate.

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
- **⬜ TC.1 — gamma-led strike selection** and **⬜ TC.2 — exit-mechanism bake-off
  (BoS vs trail vs 5-min FVG, counterfactual on identical entries)** — the
  construction season opens against the frozen L3 baseline (late Sep). TC.2's
  observability precursor (log FVG zones + BoS swing points on the trade at entry)
  is log-only and may be scheduled into any free pre-freeze slot if capacity
  appears — same capture pattern as the ADX/level-strength additions.
- **⬜ TC.4 — `vertical_spread_strategy.py` firing engine.** Three gates unchanged:
  calibrated bounds (PR lands Aug 4) + honest-TRENDING L1 excavation + the freeze.
  Earliest sensible build: September, canary on one box, paper.
- **⬜ P1 — consume the chain archive dynamically** (offline report ~Aug 10+ when
  2 weeks of archive exist; any live dimension weight-0, post-L2.6).
- **⬜ P2 — shadow observer stage 2 scorers** (observe-only; graduation post-L2.6).
- **⬜ P4 — HTF zone memory + rejection counts / pitchfork** (rides the tester
  fork, post-L2.6; the pitchfork's own gate has been L2.6 all along — Aug 21 opens
  it).
- **⬜ P5.4/P5.5 — ChainReplay + exit replay** (post-L2.6, scope set by the Aug 14
  validator verdict; holdout discipline per L3.5).

---

## PART 3 — RESOLVED REGISTER (condensed; kept so fixes don't get quietly reverted)

*Full forensic text: git history of this file at the pre-v2.0 commit, plus
`docs/HISTORY.md` and the audits. Resolution date + fixing versions + the why.*

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
  mark-limit policy split it. *(Unified via T.2 → Mon Aug 3.)*
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
  *(Historical backfill → Wed Aug 5.)* Field reference:
  `docs/TRADE_RECORD_FIELDS.md`.
- **Obs ✅ 2026-07-24 — sweep confirmation is real, not anticipatory** —
  hard-gated on `sweep.confirmed`; the loose reclaim inside it is scheduled
  (Aug 18/19), the confirmation architecture itself is correct.
- **Obs ✅ 2026-07-24 (late) — tape/regime washout fingerprint CONFIRMED-NEGATIVE.**
  Flat-angle/trend/chop do not separate good from washout sweep days (all cluster
  26–29°); the discriminator lives in WHAT the sweep reached for — which is
  exactly the level_strength track scheduled Aug 18. Lesson kept: read logged
  angle from replay jsonl, never reconstruct from candles.

---

*Rules carried forward from v1.0: nothing enters without evidence and a stated
sample size; deferred means deferred; resolved items are kept, not deleted; when
an OBSERVING item earns action it gets a date in PART 1, not a silent fix.*
