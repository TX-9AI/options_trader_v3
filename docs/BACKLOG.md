# docs/BACKLOG.md — v3.10

**CHANGELOG**
- **v3.10 — 2026-07-30 — THURSDAY CLOSED. L2.5 committed a regime label in
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

## PART 0 — THE CLOCK

| Anchor | Date | What |
|---|---|---|
| Today | **Wed Jul 29** | Epoch 1 begins immediately |
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

### EPOCH 1 — SCRUB & INSTRUMENT — Wed Jul 29 → Sun Aug 9

*Goal: suite green, canaries current, time-critical data harvested, the two
never-built gates built and proven, the bookmark live, mapper hierarchy proven on
the tester. Nothing behavior-changing deploys except on Mon Aug 3.*

**✅ Wed Jul 29 — day closed at v3.1. All three items resolved (see Part 3).**
- **T.1 ✅** — already resolved at HEAD (07-22 defect-T pass); suite verified
  **37/37 green** today on a fresh clone. No change shipped; register entry
  carries the evidence.
- **T.3 ✅** — already resolved at HEAD (position_manager v3.9, 07-22). No
  change shipped.
- **U ✅** — canary set was already current (check_versions v3.1→v4.2, 125
  checks); the missing parity-invariant check shipped today as
  **check_versions v4.3** (+ failure-count DONE banner). Deliberate-failure
  test passed. **Sync after RTH close (~16:30 ET) with today's other deploys.**

**✅ Thu Jul 30 — DAY CLOSED at v3.10. L2.5 ran in production for the first
time in the project's history.** Every item below is resolved; the day's own
work is recorded in the changelog and the Part 3 register.
- **W.0 — 🔴🔴 BEFORE THE OPEN: deploy main v4.7.** The fleet is currently
  stopped on v4.6, in which L2.5 is still unreachable. Until v4.7 is on the
  boxes, Thursday runs the v1.3 classifier exactly like every session before
  it. Push tonight so the morning wake pulls it, then verify from the log's
  first lines rather than by inference: `REGIME ENGINE: l2 (L2 import OK)` at
  start-up, and `[L2 c=...]` on the first regime change after the open. If the
  regime lines still read `[v13]` with v4.7 live, v4.6's new warning will now
  name the exact evidence dimensions starving the book — which is the one
  question left that the probe could not answer offline.
  **VALIDATE:** `echo "L2=$(grep -c "\[L2" ~/options-trader/bot.log)"` on the
  fleet after the first hour of RTH. Any box still at 0 is a box where L2.5 is
  loading but not committing, and its own log now says why.
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
- **W.1 — 🔴 QUARANTINE ALL PRE-2026-07-30 L2 DATA. The scope is the entire
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

- **W.2 — Ask the harder question the incident raises: what else fails
  silently?** Two silent-degradation faults surfaced in one morning. Both were
  invisible because the bot kept trading. Before go-live (Aug 31) the guards
  that can swallow a contract break should be inventoried — every
  `except Exception` that sets a `_OK = False` flag and continues.
  **HOW:** grep the repo for the pattern, list each one, and classify: may
  degrade silently / must page / must refuse to trade. This is a scoping pass
  producing a list, not a rewrite.
  **VALIDATE:** the list itself is the deliverable; each entry that lands on
  "must page" gets an alert like v1.7's and a canary. Schedule the resulting
  work in Epoch 2, not tomorrow.
- **V — NEW: `push.sh` finds its target by guessing (control-server hazard).**
  Found 2026-07-29 when `push.sh` run *from* `~/options-trader-v3` reported the
  remote as `futures_trader_v1.git` and refused. Cause is structural, not a
  mispointed remote (both remotes were correct): push.sh ignores the caller's
  cwd and scans `$HOME`  alphabetically for the first directory containing both
  `main.py` and `config.py`, then cd's there. On a bot box `$HOME` holds one bot
  so it is invisible; on control it silently selects the wrong project.
  Currently DORMANT — the futures checkout was deleted the same day, so the scan
  now lands on the right directory and the tool appears healthy. It returns the
  next time any second project is unpacked on control. Note the same file (same
  trap) ships in **futures_trader_v1**; fix both or the borrowed-box case
  re-bites from the other side.
  **HOW:** v1.7 — prefer `$PWD` when it is a git work tree containing
  `main.py` + `config.py`; fall back to the `$HOME` scan only when invoked from
  outside a bot checkout, and PRINT the resolved directory and remote before
  acting so a wrong pick is visible rather than silent. Keep the refusal
  behaviour (it is what saved us here) but make the message name the resolved
  path, not just the remote.
  **VALIDATE:** self-validating by construction test — recreate the failure in
  a scratch `$HOME` holding two bot-shaped directories, confirm v1.6 picks the
  alphabetically-first one and v1.7 picks the cwd; then confirm the fallback
  still works when invoked from `~`. No dataset needed. Deploy-truth is covered
  by the v4.3 parity invariant on the next fleet pass.
- **P5.1 — Chain-snapshot harvest (TIME-CRITICAL — re-scoped at v3.0).** Verified
  at HEAD: `harvest.py` is already **v0.5.1** (07-27) and pulls
  `data/chain_snapshots/<date>/<SYM>.jsonl.gz` + `signal_journal` — the build is
  done; what remains is confirming it's deployed on control and that the first
  harvested night actually landed.
  **HOW:** commit/push v0.5.1 from control if not already at origin (execute-bit
  convention), run one manual harvest, `ls chain_snapshots/<date>/ | wc -l` vs
  boxes-run; then add a **completeness manifest** — harvest emits one line per
  root (`ohlc/trades/journal/chains: N files, M bytes`) into the conductor
  headline, so the standing daily habit is a glance at the Telegram, not an ssh.
  **VALIDATE:** the manifest is the framework; downstream,
  `chain_reconstruction_check.py` (Aug 14) only runs if this landed — its input
  count IS the audit. Every day this slips is a permanent hole (a strike's quote
  is unrecoverable at 16:00).
- **N.1 — NEW: harvest `regime_log` off-box (instrumentation for L1.9, Aug 5, and
  the Aug 10 churn watch).** Verified at HEAD: harvest pulls OHLC, trades.db,
  journal, chains — **not** the per-box regime timeline. Three scheduled
  validations need it: (a) L1.9's proof metric is *offline-diary vs live-label
  agreement*, which requires the live labels on control; (b) the Aug 5 ADX
  reconstruction timestamp-joins regime_log → trades and shouldn't need 15 ad-hoc
  box pulls; (c) the Aug 10 calibration deploy's "watch churn live" is only
  checkable if the live committed-label timeline is on control nightly.
  **HOW:** harvest v0.6.0 — same best-effort scp pattern as the journal/chain
  pulls, `data/regime_log*` → `BASE_DIR/regime_log/<date>/<SYM>.*`; one file
  touched, rides the same deploy as the P5.1 verification.
  **VALIDATE:** self-validating via the completeness manifest; first consumer is
  the Aug 4 L1.9 agreement metric.
- **Z — `consolidate_trades.py` date filter (day_trader_pro side).** Rollups are
  not date-clean (61% of condor legs sat in a wrong-dated file;
  `fleet_trades_2026-07-13.json` holds only 07-07→07-10 trades). Fix: filter by
  `entry_time[:10]`, dedupe by `trade_id`; regenerate the rollups from the per-box
  DBs. DONE = every row's entry date matches its filename.
  **HOW:** as stated — filter + dedupe in `consolidate_trades.py`, bump to v1.2,
  then regenerate every dated rollup from `trades/<date>/` (the DBs are ground
  truth and are already clean; only the JSON/CSV view was contaminated —
  `conditional_tables` reads the DBs directly, so the L3.4 substrate was never
  polluted).
  **VALIDATE:** existing data closes this loop exactly: a one-shot audit script
  compares each regenerated rollup to its source DBs — row count and P&L sum must
  match per date, and `min/max(entry_time[:10]) == filename date`. Run it over
  every date on disk; zero mismatches = DONE. No new collection needed.
- **T.2 — Decide the condor paper-friction split** (code today, deploys Mon Aug 3).
  Condor paper credits still take the `PAPER_FILL_SLIPPAGE_PCT` haircut while
  singles/butterflies book the raw mark. Live condor entries are already mid-credit
  limits, so the mark-limit rationale applies: unify (or write down, in MECHANICS,
  exactly why condors keep the haircut). One model, documented.
  **HOW:** unify — paper condor books the **limit credit it actually placed**
  (mid-credit, same number the live path submits), no second haircut; the 20s
  cancel-window fill-or-kill is the realism knob, not a synthetic shave. Document
  the model in MECHANICS in the same edit.
  **VALIDATE:** the honest validator is *live* condor fills, which don't exist
  until Aug 31 — so **N.4 (Aug 14)** is the bridge: the chain archive holds real
  bid/ask at the condor's strikes at entry timestamps; reprice every post-Aug-3
  paper condor's credit against the archived NBBO and measure booked-vs-achievable.
  If paper credits sit systematically rich vs the archived quotes, the unification
  overstated fills and the haircut returns with a measured value, not a guess.
  From Sep 1, the live fill-quality audit takes over as the permanent validator.

**⬜ Thu Jul 30 — AFTER THE CLOSE**
- **Y — 🔴 LAND THE DURABLE FIX (3 parts, 2 repos, all committed code).** The
  env-var-only version of this item was WRONG and is withdrawn: `install.sh`
  overwrites `~/market-brief/.env` wholesale from a heredoc, so a hand-edit dies
  at the next reinstall or on any new instance. Nothing load-bearing lives in a
  gitignored file.
  **Y-a — `day_trader_pro/orchestrator.py` v0.3.0 (BUILT + TESTED).** Freshness
  guard: audits the report's `date` against today ET and the presence of the
  `move_ranked` sidecar, Telegrams on either problem, and stamps
  `report_path / report_date / report_stale / report_move_ranked` onto the
  selection so provenance is visible rather than inferred. Proceeds by default —
  a stale cohort of liquid names is a lesser harm than refusing to wake 13 boxes
  — with `DTP_REPORT_STALE_STRICT=1` to fail closed to `ALWAYS_ON`. Also repoints
  the fallback from `~/market_brief/out/report.json` (misspelled AND a
  non-existent `out/`, so it never once resolved) to the reporter's real default
  drop, `~/market-brief/report.json`. **This is the half that makes the fix
  durable**: with the fallback correct, the wake finds today's report even with
  `$DTP_REPORT_JSON` unset. **VALIDATE:** deliberate-failure test PASSED against
  the actual 2026-07-06 payload — frozen+no-sidecar raises 2 problems and one
  alert, healthy today+sidecar is silent, yesterday's file is caught (the race
  below), STRICT degrades to `ALWAYS_ON` only.
  **Y-b — `market_brief_v1/install.sh`: morning timer 09:15 → 09:00 ET (BUILT).**
  day_trader_pro's wake fires at 09:15:00 — the same minute the brief started —
  so the wake could read a report the brief had not finished writing. Measured
  runtime is ~75s (timer 09:15:00 → `generated_at_utc` 09:16:15 on 2026-07-29),
  so 09:00 gives a ~15 minute margin instead of a race. Live effect needs the
  unit rewritten on the box; the installer change is what survives a rebuild.
  **Y-c — `DTP_REPORT_JSON` into install.sh's `.env` heredoc (BUILT).**
  Defaulted to `$HOME/day_trader_pro/data/report.json`, overridable. Belt to
  Y-a's braces: even if the fallback path is wrong someday, the variable is set
  by provisioning rather than by memory.
  **DEPLOY ORDER:** Y-a and Y-c are safe any time. **Y-b's live timer change and
  the first brief-driven wake should NOT land on Thu Jul 30** — that is the first
  session L2.5 has ever run (W.0), and changing the wake cohort the same day
  makes a strange session unattributable. One variable at a time: L2.5 owns
  Thursday, this owns Friday.
  **EXPECT THE COHORT TO CHANGE** once a fresh report is being read — LLY and UNH
  may wake in place of MU or AMD. That is the fix working. Watch two things: the
  `scores` payload changes scale (frozen file 0–8, e.g. MU 7.7852; live brief
  0–1, e.g. LLY 0.7684 — ordering is scale-invariant and `move_ranked` drives the
  first pass once present, so selector should be unaffected), and the universe
  went 29 tickers → 28, so confirm nothing downstream assumes 29.
- **Y.1 — ✅ folded into Y-a.** The unreachable fallback is fixed in the same
  patch rather than as a separate change.
- **Y.2 — Optional hygiene in `market_brief_v1/report/emit.py`, whenever that
  repo is next open.** `_default_path()` falls back to
  `os.getcwd()/report.json`. A producer defaulting to its own working directory
  is precisely how three weeks of reports went somewhere nothing read. Point the
  default at the real consumer so the env var is an override, not a requirement.
  Not needed for durability once Y-a and Y-c are in — which is why it is
  optional rather than scheduled.

**⬜ Fri Jul 31**
- **X — ✅ SOLVED 2026-07-29 (same evening it was filed). See Part 3. Superseded
  by item Y below, which lands the fix.**

- **D (service half) — Templatize `shadow-observer.service`.** The unit hardcodes
  `/home/ubuntu/options-trader`; sed the path at install time like `setup_ec2.sh`
  does for `optionsbot.service`. Zero behavior change on the fleet (canonical path
  matches); closes the last half of defect D before any non-standard-path deploy.
  **HOW:** as stated — install-time sed of `WorkingDirectory`/`ExecStart` from the
  install target, mirroring the optionsbot unit's pattern; shadow_devtools bump.
  **VALIDATE:** tester install at a non-standard path runs; fleet no-op proven
  with existing tooling — option 14 `systemctl cat shadow-observer | grep
  WorkingDirectory` fleet-wide, all 29 identical before and after. No dataset
  needed beyond the fleet's own units.
- **E (build) — `VWAP_FILTER_ACTIVE` hard gate, on the TESTER.** The genesis
  constant that was never wired: VWAP misalignment today costs 11 points against a
  55 bar and cannot veto (a short into strength still fires at Grade B).
  `crypto_trader` learned this the hard way — shorts above VWAP / longs below VWAP
  became hard blocks after a relaxed validator produced consecutive losses. Port the
  lesson: hard block, env-tunable, **ORB exempted** (defect V made the ORB
  deliberately regime/VWAP-agnostic — the gate applies to the scored strategies).
  **HOW:** hard block in the scored-strategy path (setup_scorer/dispatch): short
  requires price ≤ VWAP, long requires price ≥ VWAP; `OT_VWAP_FILTER_ACTIVE`
  env-tunable, default ON only if the Aug 1 ledger convicts; ORB exempt (defect V);
  **index guard** — when `price_vs_vwap == "NONE"` (the 07-17 zero-volume fix:
  SPX cash volume=0) the gate is inert, never a false veto.
  **VALIDATE:** two-stage, both on data we already hold. *Retro (Aug 1):*
  `signal_journal` `scored` events have carried `vwap` + `price_vs_vwap` since
  07-18 (verified at HEAD) — join scored-and-fired signals to trades.db outcomes
  and split by alignment; the would-have-blocked ledger is a query, not a replay.
  *Forward (live proof):* N.2's `gate_block:vwap` disposition rows + the L3.2
  rejection ledger's forward outcomes label every block dodged-a-loss vs
  missed-a-winner. If blocked trades aren't net-negative on the holdout, the gate
  ships OFF as a log-only counter — evidence decides, per house rule.
- **F (build) — `MIN_RRR` floor, on the TESTER.** Second genesis constant, same
  story. The ORB's RRR is structural and varies per setup, currently ungated. Build
  the floor env-tunable, applied at scoring for non-ORB paths; log-only counter for
  the ORB first (measure how often a structural ORB would fail it before gating a
  mechanical trade).
  **HOW:** compute RRR at scoring time from the setup's planned stop and target
  (both known at decision for every scored strategy), floor at `OT_MIN_RRR`
  (default from the Aug 1 fit, not a guess); non-ORB hard, ORB counter-only.
  **VALIDATE:** here the framework was MISSING — nothing journals the computed
  RRR, so the floor could never be fitted or audited from collected data. Closed
  by **N.2** (below): once `rrr` is on every `scored` event, the floor's placement
  is a distribution + outcome question `conditional_tables` can answer (RRR decile
  × win rate × expectancy), and the Aug 1 retro ledger reconstructs RRR for
  historical trades via the replay harness (real engines, as-of stops/targets).
- **N.2 — NEW: journal `rrr` + gate-block dispositions (instrumentation for E + F,
  built with them, deploys Mon Aug 3).** Verified at HEAD: `scored` events carry
  quote context and vwap but **no risk-reward number**, and `disposition` has no
  gate-block reason vocabulary — so E and F would fire (or not) invisibly, and
  L3.2 could not consolidate their rejections.
  **HOW:** signal_journal +2 fields: `rrr` (float, every scored event) and
  disposition reasons `gate_block:vwap` / `gate_block:rrr` emitted whenever either
  gate vetoes. Log-only, freeze-safe, ~10 lines across setup_scorer/main; ships in
  the same Aug 3 pass so the distribution accumulates from day one.
  **VALIDATE:** self-validating on day one (fields present in the harvested
  jsonl); becomes the substrate for the Aug 18 / L3.2 / L3.4 gate audits.
- **N.3 — NEW: capture `closes_beyond` at entry on sweep trade rows
  (instrumentation for the Aug 18 evidence day, built today, deploys Mon Aug 3).**
  Verified at HEAD: trades.db carries adx/conviction/flat-angle/level_strength but
  **not** the reclaim's `closes_beyond` count — yet the Aug 18 "reclaim looseness"
  question is *do losing sweeps carry higher closes_beyond than winners*, which is
  unanswerable from collected data as-is (only reconstructable by replay,
  approximately).
  **HOW:** the proven v-obs pattern — one ALTER-TABLE auto-migrated column
  (`closes_beyond_at_entry INT`), threaded from the sweep confirmation object at
  entry exactly like `level_strength` was on 07-24. Observability only.
  **VALIDATE:** self-validating; by Aug 18 there are ~2 weeks of exact values, and
  the retro replay (approximate) cross-checks the capture on the overlap.

**⬜ Sat Aug 1**
- **E + F tester proof.** Replay both gates over the banked 07-13→07-31 tape:
  enumerate every historical trade each gate would have blocked, with outcomes.
  DONE = a would-have-blocked ledger showing the gates remove net-negative trades
  (if they don't, the defaults ship OFF and the gates ship as log-only counters —
  evidence decides, per house rule).
  **HOW:** E's ledger is a journal+trades join (vwap alignment is already on every
  scored event — no replay needed for the journaled window); pre-07-18 trades and
  all RRR values come from the replay harness driving the real engines as-of.
  Split the verdict by the rotating 30% session holdout so the gate defaults are
  fit on one set and accepted on another (L3.5 discipline applies to gates too).
  **VALIDATE:** the ledger IS the validation artifact — per gate: n blocked, net
  P&L of blocked, win rate of blocked vs admitted, on fit and holdout separately.
  Ship-ON bar: blocked population net-negative on the HOLDOUT, not just the fit.
- **S / L1.9 — BOOKMARK build starts, on the TESTER.** Rolling ~15-session window
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

**⬜ Sun Aug 2**
- **L1.9 bookmark tester proof.** Run against copies of real `ohlc/<date>/`
  folders; prove byte-inert on the diary for warm-irrelevant days and prove the
  EOD conductor chain is untouched. The conductor is finally flawless — it stays
  that way.
  **HOW/VALIDATE:** as L1.9 above — inertness fixture + N.1 agreement metric;
  conductor untouched proven by a full dry-run of the chain on the tester with the
  bookmark grafted onto a *copy* of validate_regime.sh, diffing every artifact
  path it writes.
- **M.3 — Dedicated Telegram bot for options-trader notifications.** Promoted from
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
- **TC.4 (T+1wk) — readiness digest check.** `_trend_credit_spread` journal has
  been accumulating since 07-28; confirm fleet-wide capture is clean.
  **HOW/VALIDATE:** run `readiness_digest` over the harvested journal; per-symbol
  row counts > 0 on every traded box, impulse-SD distribution non-degenerate.
  Existing data; this IS the validation framework TC.4's bounds fit rides on.

**⬜ Tue Aug 4**
- **L1.9 — Graft the proven bookmark onto `validate_regime.sh`**, then run
  `regime_backfill --rebuild` to re-score all dated diary rows warm. DONE = the
  diary reads TRENDING honestly on the days live boxes did.
  **HOW:** graft = the proven copy from Aug 2 replaces the live script (full-file,
  version-bumped); rebuild re-scores every dated folder with warm depth.
  **VALIDATE:** the N.1 agreement metric, now on the full archive: per session,
  offline TRENDING share vs live regime_log TRENDING share — DONE means the known
  under-report signature is gone on the days the live boxes trended (e.g. the
  07-17+ AVGO sessions), with chop days unchanged. Both series are on control;
  the check is a query.
- **TC.4 — SD-bounds fit PR.** Run `readiness_digest`, fit
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
- **Historical ADX reconstruction.** Timestamp-join `regime_log` → trades to
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
- **L1.6 (first pass) — flat-angle sweep.** 16–26° against the rebuilt multi-day
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
- **Level hierarchy + Overnight High/Low — build on the TESTER** (queued 07-24).
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
- **N.6 — NEW: extended-hours-bars audit (gates the ON H/L source).** Verified at
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
- **Sweep level_strength — first look.** 07-27→08-06 sweeps bucketed by
  `level_strength` (the capture shipped 07-24). Observation checkpoint only; n is
  still small. No action.
  **VALIDATE:** existing capture + conditional_tables; checkpoint records n per
  bucket so Aug 18's power is known in advance.

**⬜ Fri Aug 7**
- **Level hierarchy tester proof complete.** Inert where it should be; the
  postmortem buckets become meaningful only once the tiered value flows.
  **HOW/VALIDATE:** replay banked sessions through the tester mapper — every
  sweep that fired at HEAD still fires with the graded value, `is_named`-shim
  parity 100% (byte-inert on decisions, richer on capture). Fixture = the banked
  07-24→08-06 sweep set with recorded level_strength; the graded scorer must
  reproduce the recorded coarse values on the overlap.
- **L1.7 Tier-B ledger check.** With the warm rebuild + three weeks of labels:
  which rows close? TRENDING should now be closable if any labeled trend day
  exists 07-14→08-07; SWEEP needs one mapper-confirmed named-zone reclaim;
  COMPRESSION needs a coil-into-pin session; BREAKOUT needs one more clean hold
  through the BB re-entry flicker. Close what the tape supports; the rest is
  calendar, not code.
  **HOW/VALIDATE:** pure evidence review over collected artifacts — warm diary ×
  auto_label labels; each Tier-B row's bar is stated in VALIDATION.md §2 and the
  diary prints the numbers. No new framework; the framework is why these close.
- **G (data checkpoint).** Snapshot the `retest_depth` distribution (3 weeks
  accumulated). No decision yet — that's Aug 22.
  **VALIDATE:** existing `retest_check` journal events since 07-18; snapshot =
  histogram + n, so the Aug 22 decision knows its power.

**⬜ Sat Aug 8 – Sun Aug 9 (weekend calibration fit)**
- **L2.4 — Fit the integrator priors offline.** θ_commit/θ_hold/δ_displace,
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
- **L1.11 — Fit the remaining ramps** (`flat_s` on its conditional population;
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
- **L3.1 close-out.** Confirm `signal_journal` jsonl captures full fleet sessions;
  the harvest pull landed 07-27 (v0.5.0) — verify the conductor phase reports it
  and the manifest counts match boxes-run. Log-only; freeze-safe.
  **HOW/VALIDATE:** per-box event counts × session from the harvested jsonl;
  every traded box > 0 scored events, dispositions present for every fired trade
  (join journal → trades.db by symbol+timestamp, orphan count = 0). Existing data
  end-to-end.

**⬜ Wed Aug 12**
- **P3 phase 1 — index-context broadcast, log-only.** Control-side writer pushes
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
- **L3.2 — rejection ledger build starts.** `analysis/rejection_ledger.py` +
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
- **P5.3 — run `chain_reconstruction_check`** on ~3 weeks of archive. PASS → build
  ChainReplay (post-freeze); PARTIAL → grid restricted to the validated moneyness
  band, stated in the header; FAIL → the missing piece is named by the `+vega·ΔIV`
  column (IV-path model vs cadence) and gets a date before any harness work.
  **HOW/VALIDATE:** the tool IS the validator (built 07-23, proven on synthetic);
  its inside-spread rate, stratified by moneyness/hour/|ΔS|, is the verdict — and
  it only runs because P5.1/N.1's harvest landed Jul 30. Whatever the verdict, it
  is written into the ROADMAP P5 header the same day.
- **N.4 — NEW: paper-fill realism audit (validates T.2 + the R slippage default,
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
- **L3.2 finish.** Class (b) coverage-gap scan (per strategy: was a live setup
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
- **K — re-arm decision, on paper.** Decide between the current deliberate
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
- **I — butterfly cutoff branch decision.** `can_enter(is_butterfly=...)` is
  unreachable; either fix the `main.py` call site (if a 15:00 butterfly cutoff is
  ever wanted) or delete the branch so config and code stop disagreeing. Decision
  today; code post-freeze.
  **HOW/VALIDATE:** one query on collected trades — the butterfly entry-time
  distribution (trades.db). If no fill has ever wanted the 15:00 window, delete
  the branch (loose-code principle); if late entries exist and lost, wire the call
  site. Data decides a two-line decision.
- **AA checkpoint.** Any two-sided condor with both legs near-simultaneous since
  07-17? Post-fix sample was 7 legs at last count. If clean through ~4 weeks,
  close AA as superseded-by-Y+rich-triggers; if recurred, it gets a forensic slot
  Aug 22.
  **HOW/VALIDATE:** the Z-cleaned rollups make this a one-liner — per condor pair,
  |leg entry gap| distribution; the 07-17 defect signature was gap = 0 min at
  identical underlying_entry. Existing data (and now date-clean).

**⬜ Tue Aug 18 — sweep evidence day (the decision the whole sweep track waits on)**
- **Level-conviction lead:** win-rate/expectancy by `level_strength` bucket at
  ~3 weeks of current-engine data. If equal-H/L sweeps are the losers → a
  level_strength floor on the sweep gate is confirmed.
  **VALIDATE:** existing capture (07-24) × conditional_tables cells with Wilson
  intervals; the Aug 6 checkpoint already told us the per-bucket n, so today's
  verdict is stated with its power, not just its point estimate.
- **Reclaim looseness:** do losing sweeps carry higher `closes_beyond` than
  winners? If yes → require `closes_beyond == 0` post-reclaim (or hold-N-candles).
  **VALIDATE:** **N.3's exact per-trade capture** (live since Aug 3, ~2 weeks) +
  the replay-reconstructed values for older trades on the overlap. This question
  was unanswerable from collected data before N.3 — that was the point of N.3.
- **Exit asymmetry / washout fingerprint:** does 75%-win/negative-net hold on the
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
- **Build the confirmed sweep changes on the TESTER** (level_strength floor and/or
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
- **L3.3 — gate matrix behind a flag, built + tester.** `fires iff regime ∈
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
- **N.5 — NEW: fill-latency telemetry (the TC.2 stop-trigger dataset — must exist
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
- **G — decision.** Feed `retest_depth` into `orb_quality` or drop it: 5 weeks of
  distribution + the Phase-3 ROI buckets now exist to answer it. Decide from the
  data; the measurement gates nothing until then.
  **HOW/VALIDATE:** join `retest_check`/`retest_depth_px` (journal, since 07-18)
  to ORB outcomes (trades.db) by symbol+timestamp; bucket outcome by depth in ATR
  units. Monotone edge with n per bucket ≥ the min-n bar → feed into the A/B
  grade; flat → drop the field from scoring (keep the capture). The join is the
  framework and both sides are already collected.
- **L3.5 — enforce the holdout in the bucketer.** Fit sessions ≠ acceptance
  sessions inside `conditional_tables.py`; slippage-haircut P&L only. The Aug 31
  descent bars come from held-out cells or they don't come.
  **HOW:** session-hash split inside the tool (deterministic, seeded), every
  emitted cell labeled fit/holdout; N.4's measured slippage replaces the flat
  haircut if it landed.
  **VALIDATE:** self-demonstrating — the tool's own report shows the same cell on
  both splits; a cell that collapses on holdout is the guard working.
- **Live shakedown prep:** broker account funded · `configure.sh` mode-switch
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
- **Mode-isolation live-switch rehearsal on ONE box.** Switch paper→live→paper;
  verify defect-Q end-to-end: archives created, mode-scoped queries return zero
  cross-mode rows, no paper row visible to the live loop, breaker reads only live
  P&L.
  **HOW/VALIDATE:** scripted rehearsal with assertions, not eyeballs — after each
  switch: archived DB exists with the mode+stamp name; `realized_pnl_today()` and
  `get_open_trades()` return only current-mode rows (seed one paper row first so
  the negative case is actually exercised); breaker state re-derives clean.
  Existing machinery under test; the seeded-row check is the addition.

**⬜ Wed Aug 26**
- **Entry/exit path shakedown vs the resolved audit (N/O/P).** Re-run
  `test_entry_fill_confirmation`, `test_roll_is_real`, `test_mode_isolation` at
  HEAD; walk the order_confirm deadlines, cancel-and-walk-away, partial booking,
  and paging paths against the tiny-account config on paper.
  **VALIDATE:** the suite + a forced-partial drill (limit far from mark on the
  tiny account's paper twin so the bounded poll and partial-stash paths actually
  execute); N.5 columns populate during the drill — proving the latency capture
  before it matters.

**⬜ Thu Aug 27**
- **M.3 — Telegram bot live test** (built Aug 2): pages route to the dedicated
  options-trader channel; half-complete-roll and phantom-P&L pages verified.
  **VALIDATE:** the Aug 2 drill plan executed — induced half-complete roll page,
  induced phantom-P&L page, fallback-channel test. Transcript archived in the
  runbook.
- **M.1/M.2 — Windows residue documented.** Ghost folder on tarball extraction +
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
- **L3.6 descent, step 0:** live, minimum size, SPX + QQQ, bars one bucket above
  the paper crossing. This is the tiny-account live shakedown that has gated the
  fill-confirmation work since 07-15 — now with the whole scrub list behind it.

**⬜ Tue Sep 1 – Fri Sep 4 — LIVE, first week of September** ✅
- Daily: fill-quality audit (live fill vs mark, per the 07-15 divergence-audit
  template — now sharing N.4's comparison schema so paper-vs-live divergence is
  one diff) · phantom-P&L reconcile check at each close · ladder fill-latency
  read from the **N.5 columns** (this is the TC.2 stop-trigger dataset — the −40%
  trigger vs 35%/25% question gets answered by these numbers, not by guessing).
- **Fri Sep 4:** week-1 live review — divergence report, latency distribution,
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
- **⬜ P4 — HTF zone memory + rejection counts / pitchfork** (rides the tester
  fork, post-L2.6; the pitchfork's own gate has been L2.6 all along — Aug 21 opens
  it). Rejection-count validation consumes the same level_strength/sweep capture
  lineage started 07-24.
- **⬜ P5.4/P5.5 — ChainReplay + exit replay** (post-L2.6, scope set by the Aug 14
  validator verdict; holdout discipline per L3.5).

---

## PART 3 — RESOLVED REGISTER (condensed; kept so fixes don't get quietly reverted)

*Full forensic text: git history of this file at the pre-v2.0 commit, plus
`docs/HISTORY.md` and the audits. Resolution date + fixing versions + the why.*

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
