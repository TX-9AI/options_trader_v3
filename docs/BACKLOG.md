# docs/BACKLOG.md — v5.07


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

> **🔴 SUSPENDED 2026-08-13, RESET SAME DAY.** The Sep 8 go-live and the Aug 17
> deploy Monday below were PAUSED INDEFINITELY on 2026-08-13 pending P&L
> recovery. The operator then set a NEW anchor the same evening, after the
> largest single-day behavioural change in the project's history baked to 29/29
> boxes. **The row that is live is FRI 2026-08-28.** Everything dated Aug 17 or
> Sep 8 below is HISTORICAL — do not act on it.
>
> ⬜ **REBASED 2026-08-15:** the anchor's BASIS is now the 08-15 bake, not
> 08-13. The DATE is unchanged — Mon 08-17 through Fri 08-28 is ten sessions,
> exactly two trading weeks, all on the current fleet. Aug 28 evaluates **the
> 08-15 fleet**; it is not an isolation test of the 08-13 changes.
>
> **THE SEQUENCE (operator, 2026-08-13; basis rebased 2026-08-15):**
> 1. **Fri Aug 28** — evaluate the paper-P&L impact of the 08-13 changes, once
>    the bugs are worked out. **The two weeks to that date are a MEASUREMENT
>    WINDOW, not a tuning window.**
> 2. **Resume freezing the L1 dials.** L2 is mostly complete — a few
>    verifications remain; chatter is nearly eliminated.
> 3. **Then L3.**
> 4. **Then final trade adjustments + stop-quality evaluation.**
> 5. **Then live cash, REDUCED SIZE for the first week.**
>
> ⚠️ **RESIST RE-TUNING ON THE FIRST BAD SESSION.** Most of the 08-13 thresholds
> are STATED PRIORS, not fits — the 0.70 POP floor, the 0.25 quote width, the
> 11:00 cutoff. Re-fitting them on the data that motivated them turns an
> out-of-sample validation into an in-sample one. **The full account of what
> changed, why, the expected benefit and every tuning knob is in
> **`docs/HISTORY.md`** (2026-08-13 section).
> ⬜ POINTER CORRECTED 2026-08-15: this read `docs/FLEET_STATE_2026-08-13.md`,
> which was DELETED on 08-14 — it violated `docs/README.md`'s rule against
> per-date state files and its content was folded into HISTORY.md. The clock has
> been directing readers at a missing file since then.


| Anchor | Date | What |
|---|---|---|
| Epoch 1 start | **Wed Jul 29** | Epoch 1 began (label was "Today" — stale by 07-30) |
| Deploy Monday 1 | **Mon Aug 3** | Hard gates (E, F) + friction unification (T.2) + N.2/N.3 captures go live on the fleet, RTH |
| Deploy Monday 2 | **Mon Aug 17** | THE calibration deploy (level hierarchy, L2.4 priors, L1.6 flat cut, L1.11 ramps) — **L2.6 freeze-candidate window opens** |
| Freeze declared | **Fri Aug 28 EOD** | L2.6 frozen baseline, if the window ran clean |
| Deploy Monday 3 | **Mon Aug 31** | L3.3 gate matrix (flagged, paper) + evidence-confirmed sweep changes + N.5 latency telemetry |
| **GO LIVE** | **Tue Sep 8, RTH** | Tiny size, subset of symbols — live through **Sep 9–11**. TUESDAY, not Monday: the one-week slip lands on Labor Day |
| Labor Day | Mon Sep 7 | Markets closed — analysis day |
| Descent notch | Tue Sep 15 | Half size if week 1 was clean |
| **FULL SIZE** | **Mon Sep 21, RTH** | Late September (contingent on two clean live weeks; raise-back trigger stays armed) |

**⚠️ SLIPPED ONE WEEK, 2026-08-07.** Every anchor from Deploy Monday 2 onward
moved right by seven days; Epoch 1's past dates did NOT move, so anything already
overdue stays overdue and the DESK-overdue count keeps its sting. Labor Day is a
fixed holiday and did not slip — which is why **GO LIVE is TUESDAY Sep 8**, not
the Monday the arithmetic produced.
**READ THE NEXT EVM RUN AS A RE-BASELINE, NOT AS RECOVERED SCHEDULE.** PV
recomputes against these dates, so SPI will jump on the first run after this
edit. That jump is the plan moving, not work getting done. Pass `--asof`
explicitly: control is UTC, the desk is Central, so after ~19:00 Central an
unqualified run briefs tomorrow's PV.

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
| **WH.11 — report parity** | ✅ 08-16 | ✅ 08-16 | n/a (control-only) | **40 and 41 both MATCH from the warehouse on 2026-08-14.** Three rounds of instrumentation defects first, none in the warehouse. ⚠️ ONE DATE — run `--since 2026-08-13` before severing; `OT_EOD_PULL=0` defensible, not justified |
| **Menu is data — devtools.sh v1.32** | ✅ 08-16 | ✅ 08-16 | n/a (control-only) | 541→184 lines. Numbers generated at render; registry + functions hold no numbers. `--diff` across the swap: **all labels survive with identical commands.** 16 numbers moved (FIT REPORT 57→42); EMERGENCY STOP still 27. Renumbering is now structurally impossible |
| **WH.9a — warehouse cost/inventory script** | ✅ 08-16 | ⬜ | n/a (control, read-only) | `warehouse_cost.py` v1.0, 15 checks. **Recommendation: AGAINST compaction (est. <$2/mo total), AGAINST a Glue crawler, Athena gated behind a workgroup scan limit.** ⚠️ versioning with no lifecycle rule is the one line item that grows unbidden |
| **WH.8 — warehouse reader + the two missing tables** | ✅ 08-16 | ⬜ | ⬜ **s3_push v1.7 needs option 25** | `warehouse_reader.py` v1.0 (23 checks) reproduces the fleet_trades bundle from S3, reusing consolidate_trades' own stats code; **found regime_log + circuit_breaker_events were never pushed**; `--compare` is WH.11's gate. NOT yet run against the real bucket |
| **WH.14 eval — first EOD assessment** | n/a | n/a | 🗓️ **DUE TUE 08-18** | liquidity_ledger objects landed? `sym=<SYM>_EXT` present under raw/candles/? SHORT boxes repeat night-over-night? is 5s spacing right? **Tuesday not Monday: 08-17 belongs to v4.94 Tier-1, and a backfill anomaly in that window could be the conductor OR any of the eleven unvalidated changes — indistinguishable.** ⬜ DO NOT SEVER (gated on WH.11) |
| **WH.14 — EOD fills the bucket + liquidity ledger** | ✅ 08-16 | ✅ 08-16 `e98aad8` / `901257e` | ⬜ **s3_push needs option 25** | s3_push v1.6 (88 checks) · eod_backfill v1.3 + suite (17 checks); Telegram on SHORT via existing notify; `OT_EOD_PULL` severable; batches stay sequential |
| **WH.7 — devtools EMERGENCY STOP fixed** | ✅ 08-16 | ✅ 08-16 `6e4941d` | n/a (control-only) | **PROVEN LIVE 10:53 ET with 2/29 up: HALT → 29/29 stopped in seconds.** Was pinging 29 boxes over SSH first (~5 silent min). 15 checks, safety props pinned BY NAME |
| **N.7 — entry snapshot capture** | ✅ 08-04 | ✅ 08-04 `0f78329` | ⬜ **Mon Aug 17** | control suite **146 passed / 1 skipped, rc=0** (read 08-04); ALL CANARIES GREEN; PARITY == origin; tree clean |
| **N.5 — exit ladder latency** | ✅ 08-04 | ✅ 08-04 | ⬜ **Mon Aug 17** | control suite **158 passed / 1 skipped, rc=0**; ALL CANARIES GREEN |
| **N.8 — no regime-flip exit on a stale book** | ✅ 08-04 | ✅ 08-04 | ⬜ **Mon Aug 17** | control suite green, ALL CANARIES GREEN |
| **W.2a — today's own swallows made audible + the alarm made specific** | ✅ 08-04 | ✅ 08-04 | ⬜ **Mon Aug 17** | silent count back to the 08-03 baseline of **87**; `--since` proven on three cases |
| **D.1 — bull/bear were the same token in THREE renderers** | ✅ 08-04 | ✅ 08-04 | n/a (report-only) | 16 rows re-rendered on control; ALL CANARIES GREEN |
| **AV.1 — the pooled gap read, with a legitimacy guard** | ✅ 08-04 | ✅ 08-04 | n/a (offline) | ALL CANARIES GREEN on control |
| **TC.4b-pre — does the impulse floor hold?** | ✅ v1.3 08-04 | ✅ 08-04 | n/a (offline) | **CONTROL RUN: impulse − control TERMINAL = −0.3% ±2.3%. Dead null.** See below |
| **PF.V — pitchfork variant sweep (§12 Q2)** | ✅ 08-04 | ✅ 08-04 | n/a (offline) | Answered: no-change. ACCEL/birth andrews 0.22 · mod_schiff 0.67 · schiff 3.61; adverse tine kills 81-97% in ALL THREE |
| **ORB.1 — ORB was gated by the stale entry block** | ✅ 08-04 | ✅ 08-04 | ✅ **BAKED 08-08** | control suite 216 passed, ALL CANARIES GREEN |
| **RPT.1 — report rollup (5 fixes, 2 repos)** | ✅ 08-04 | ⬜ | n/a (offline) | otv3 suite **223 passed / 1 skipped**; behavioural proof on all five |
| **BF.1 — the RTH guard was eating the backfill** | ✅ 08-04 | ✅ | ✅ **BAKED 08-08** | 8/8 guard states proven; 2 sessions of sat-out tape at stake |
| **BF.2 — guard OFF by default (operator directive)** | ✅ 08-04 | ✅ | ✅ **BAKED 08-08** | v1.4, both modes proven |
| **BF.3 — THE REAL CAUSE: `--once` hung on the v3.9 RTH gate** | ✅ 08-04 | ✅ 08-04 | ✅ baked | **CONFIRMED WORKING on the box** |
| **BF.4 — session guard reconfigured: one predicate, guard back ON** | ✅ 08-04 | ✅ | ✅ **BAKED 08-08** | suite 229 passed; 8/8 pull states |
| **AI.1 — condor approach telemetry on every plan death** | ✅ 08-04 | ✅ 08-04 | ✅ **BAKED 08-08** | 10 tests; item AI becomes answerable |
| **N.9 — contract telemetry (premium decomposition)** | ✅ 08-04 | ✅ | ✅ **code BAKED 08-08** (was scheduled Mon Aug 17) | suite **247 passed / 1 skipped**; 8 tests; log-only |
| **RGM.1 probe — RANGING fallback run lengths** | ✅ 08-06 | ⬜ | n/a (offline, read-only) | `tests/rng_probe.py` v1.0; proven on a planted corpus with known run lengths (5/5 runs, histogram, warm-up/mid split, gap classification, implied crossings) before issue. **NOT YET RUN on the real corpus — that run is the deliverable, not this file.** |
| **RGM.1 — emission-law attribution + counterfactual** | ✅ 08-06 | ⬜ | n/a (offline, read-only) | `tests/emission_law_sweep.py` v1.0; harness **99.9%** faithful against the REAL integrator on a planted one-change world, where the current law gives **141.5 switches/symbol-day** and protect-below-hold gives **1.0** — a cliff, not the delta sweep's slope. **NOT YET RUN on the real corpus.** |
| **RGM.1 F7 — the emission fix + live A/B** | ✅ 08-06 | ✅ | ✅ **BAKED 08-08** | conviction_integrator **v2.1**, main **v5.5**, `tests/test_emission_protection.py` (7 pass, incl. a v2.0 control that MUST flip), `tests/label_agreement.py` v1.0. Sandbox suite **224 passed / 1 skipped**; 8 collection failures are the missing `tastytrade` SDK and are IDENTICAL at origin HEAD. **Authoritative suite run happens on control as part of the deploy — not yet read.** |
| **RGM.2 — Layer-1 discrimination census** | ✅ 08-07 | ⬜ | n/a (offline, read-only) | `tests/discrimination_census.py` v1.0; every planted count recovered exactly (101 dead / 50 one-live / 30 tight-gap / 20 wide-gap). **NOT YET RUN on the corpus.** |
| **RGM.1 F7 — MEASURED END TO END** | ✅ 08-07 | ✅ 08-07 | ✅ **BAKED 08-08** | real-tape A/B on 08-06: **20.8 → 4.2 switches/symbol-day**, `L1 IDENTICAL`, re-emitted baseline 661 on BOTH files (conviction dynamics unchanged). Agreement gate over 19 sessions: TREND modal **63.4→69.1%**, in-family **47.5→57.8%**. Suite 287/rc=0. Evidence archived to `~/evidence_rgm1_20260806/` |
| **MEM.1 — SPX leak: confirmed and traced** | ✅ 08-07 | ⬜ | ⬜ **needs an RTH run** | two-sample fleet RSS: 14 boxes flat (MU −1.9 MB, NVDA −4.5 MB), **SPX +93.5 MB in 16.4 min = 5.7 MB/min**; QQQ control **+8 KB**. `tests/mem_tracer.py` v1.0 built; diff machinery proven on a planted 10 MB leak. |
| **SWP.1 — ungate sweep from regime** | ✅ 08-07 tool | ⬜ | ⬜ **needs the floor + a bake** | operator ruling: sweep is an EVENT, not a regime. Fleet log grep confirmed **zero sweep activity 08-07** — every `Sweep strike:` line was CONTINUATION readiness (`target=0.45` = `TR_CONT_TARGET_DELTA`). `tests/sweep_score_dist.py` v1.0 sets the gate floor from the corpus; proven on planted data. |
| **SWP.1 — THE UNGATING, BUILT** | ✅ 08-07 | ✅ | ✅ **BAKED 08-08** | config **v4.2** (`SWEEP_SETUP_FLOOR` 0.05, `OT_SWEEP_SETUP_FLOOR`), main **v5.6**, sweep_reversal_strategy **v3.3**, `tests/test_sweep_ungated.py` 6 pass incl. a PLTR-guard canary. Deliberate-failure test passed. Sandbox suite 231 passed / 1 skipped (7 failures = missing tastytrade SDK, identical at origin HEAD). **Authoritative suite run on control NOT yet read.** |
| **CNT.1 — continuation under BREAKOUT** | ✅ 08-07 | ✅ | ✅ **BAKED 08-08** | config **v4.3** (`CONT_BREAKOUT_DIRECTION`, `CONT_BREAKOUT_MIN_ADX` 25), main **v5.7**, continuation_strategy direction branch, `tests/test_continuation_breakout.py` 6 pass, deliberate-failure test passed. Tagged `trend_continuation_breakout` so it scores separately. Sandbox 237 passed / 1 skipped. |
| **CNT.2 — insurance gate (BOS blind window)** | ✅ 08-07 | ✅ | ✅ **BAKED 08-08** | config **v4.4** (`CONT_INSURANCE_STOP`), exit_engine **v4.14** (gate 2c), `tests/test_insurance_stop.py` 7 pass, deliberate-failure test passed. Sandbox 244 passed / 1 skipped. Arms the already-stamped `underlying_stop` ONLY while `BOSTracker.protected_level is None`. |
| **RGM.3 — sweep leaves the regime set** | ✅ 08-07 | ✅ | ✅ **BAKED 08-08** | conviction_integrator **v2.2**; `INTEGRATED_REGIMES` 6→5, tie-break head SWEEP→BREAKOUT_VOLATILE, RegimeParams row removed. Scorer UNTOUCHED (SWP.1 depends on it). `tests/test_sweep_not_a_regime.py` 6 pass, deliberate-failure verified. Sandbox 250 passed / 1 skipped. |
| **DRF.1 — trigger-conditioned drift + ORB positive control** | ✅ 08-07 | ⬜ | n/a (offline) | `tests/trigger_drift.py` v1.0; planted proof separated a +0.02%/bar window (ORB Long median +0.200%, 100% positive) from noise (−0.010%) against a null arm at 0.000%, 40/40 triggers matched through the UTC→ET conversion. **NOT YET RUN on the real corpus.** |
| **SWP.2 + CNT.3 — the two Tier-1 priors** | ✅ 08-07 | ✅ | ✅ **BAKED 08-08** | config **v4.5**, sweep_reversal_strategy **v3.4**, continuation branch. `tests/test_tier1_priors.py` 6 pass, deliberate-failure verified. Sandbox 256 passed / 1 skipped. Both are PRIORS carried by mechanism, not fits. |
| **MEM.2 — in-process tracemalloc** | ✅ 08-07 | ✅ | ✅ **BAKED 08-08** (SPX is the only box with OT_MEM_TRACE=1) | `utils/mem_trace.py` v1.0 + main **v5.8**; env-gated `OT_MEM_TRACE`, one bool test per tick when off. mem_tracer v1.1 gets the symbol banner + empty-fetch abort. Sandbox 256 passed / 1 skipped. |
| **GATE.1 — label_agreement v1.1** | ✅ 08-07 | ⬜ | n/a (offline) | each tag scored over ITS OWN timeframe: TREND whole-session, PIN last hour, BREAKOUT/SWEEP **NOT SCORED** (single-event tags, no breach timestamp). v1.0's PIN 8.9% / BREAKOUT 2.8% / SWEEP 0.0% are RETRACTED. |
| **L3.2a — rejection ledger** | ✅ 08-07 build | ⬜ | n/a (offline) | `analysis/rejection_ledger.py` v1.0 + 3 tests, deliberate-failure verified. Planted proof: vwap blocking longs into a falling tape → 100% DODGED; rrr blocking shorts → 100% MISSED. **NOT YET RUN on the real journals.** |
| **SHD.1 — shadow observer data OFF the fleet** | ✅ 08-07 | ⬜ | n/a (offline) | **282,350 records / 188 files / 238 MB / 29 boxes**, pulled for the first time ever (`harvest.py` has no shadow class). `tests/shadow_summary.py` v1.0 built + proven on planted data. **NOT YET RUN on the real pull.** |
| **AX.1 — the conjunction, codified** | ✅ 08-07 | ⬜ | n/a (pure, gates nothing) | `analysis/regime_axes.py` v1.0 — two-axis decomposition + `pair_conf = min(dir, vol)`. 6 tests, deliberate-failure verified (a mean turns it red). **NOT wired to anything yet — by design.** |
| **AX.2 — the 3x3 cross-tab + separation test** | ✅ 08-07 | ⬜ | n/a (offline) | `tests/axis_crosstab.py` v1.0. Planted proof: `direction_conf` gap **+0.000** (does not separate) while `pair_conf` gap **+0.800** — the conjunction succeeding where a component fails, detected. **NOT YET RUN on the real book.** |
| **AX.3 — keep what separated, kill what did not** | ✅ 08-07 | ✅ | ⬜ **NOT the bake — emission was never BUILT** | regime_axes **v1.1** — `pair_conf` marked DEAD in the payload itself (`pair_conf_status`), `direction_conf` (+0.188, n=571) carried forward. 7 tests. **Emission onto the journal is the next step and is NOT built.** |
| **VW.1 — vwap_orientation reads the journal at last** | ✅ 08-07 | ⬜ | n/a (offline) | **v1.1 path-aware discovery.** The "three renames" diagnosis was WRONG — `_first_key` tested top-level keys only while the journal nests under `readiness.` and `factors.`. Proven on a realistic nested record. |
| **VW.1b — paths verified against the emitter** | ✅ 08-08 | ⬜ | n/a (offline) | v1.1's path-awareness was necessary but I then GUESSED the paths and found NONE across 39,344 records. Reading `trade_readiness._journal()`: everything is TWO levels deep — `readiness.market.vwap`, `readiness.factors.dir`. |
| **VW.1c — the event filter, the fourth layer** | ✅ 08-08 | ⬜ | n/a (offline) | v1.3. The whitelist accepted only `scored/fired/entry/entered` — pre-v1.5 names — while the records carrying `readiness.market` are `readiness*`. **11,584 records skipped on 08-06 alone.** Now prefix-matched. |
| **VW.1d — the join layer, the fifth and final one** | ✅ 08-08 | ⬜ | n/a (offline) | v1.4 — and this time the WHOLE remaining path was traced before patching. v1.3's real run (30,565 undecidable, only TREND_CREDIT_SPREAD in the table, 304 trade rows joined to ZERO) had THREE stacked causes, none of them the filter: (1) `factors.dir` exists on exactly ONE track — TCS (trade_readiness.py:569); the other five journal no direction, so `aligned()` dumped them all into a counter mislabeled "index/NONE side". (2) The trade join compared track slugs (`SWEEP`) to class names (`SweepReversal`) — no key could ever match. (3) TCS, the one decidable strategy, has NO firing engine yet (TC.4), so its 0 trades were arithmetically forced. Fix: per-strategy direction resolver (continuation from label exactly as the emitter's own staged-pick path; condor sides mapped ON MECHANISM — call credit = SHORT exposure, the inverse of the buyer's-eye reading; sweep via `staged.direction` paired to the symbol's last market snapshot ≤120s; butterfly undecidable BY DESIGN), family-normalized trade join with condor legs attributed via setup_type, and undecidable/unjoinable REPORTED BY CAUSE so the counter can never lie again. Reproduced the exact v1.3 symptom on planted data, then proved v1.4 resolves all five families and joins trades. |
| **VW.1e / RDY.1 — `dir` on every track, at the source** | ✅ 08-08 | ✅ | ✅ **BAKED 08-08** — earlier than planned | **trade_readiness v1.6 — the emitter side of VW.1d, and the reason the ledger needed five versions.** ONE track (`_trend_credit_spread`) journaled a direction and five journaled none; a field with a single writer is indistinguishable from a field nobody needs until a reader depends on it. Each track now stamps `dir` from the source that actually knows: continuation from the trending label (identical to `_staged_pick`'s derivation, so journal and picker cannot drift); **sweep from the LIVE `liq_map.recent_sweep.kind` — the field no offline tool could ever recover**, which is why v1.4 had to pair against staged picks; condor sides from EXPOSURE (**call credit = SHORT**, inverse of the buyer's-eye reading); butterfly explicit `"neutral"`. `""` = no intended side this tick, an honest absence now distinguishable from a missing field. **LOG-ONLY, freeze-safe, no trading-behaviour change.** Ledger **v1.5** PREFERS the emitted field and KEEPS the v1.4 derivation, because no fleet-side change can reach already-banked history. 7 new tests + 4 canaries; deliberate-failure verified (inverting the condor mapping turns the suite red). Suite 339 passed / 1 skipped. **⚠️ FORWARD-ONLY — reaches only sessions after Monday's restart.** |
| **RGM.5 — the v13 classifier still emits SWEEP_REVERSAL** | ⬜ **OPEN** | ⬜ | n/a | RGM.3 took SWEEP out of the **L2 integrator's** argmax and stopped there. `regime_classifier.py:171` still assigns `SWEEP_REVERSAL` at HIGHEST priority, and `main` falls back to the v13 classifier whenever L2 is not committing — so on fallback ticks the label reappears and the readiness sweep track scores off it (R p50 0.525 on 65 of 11,136 ticks, 2026-08-10). Found while resolving a contradiction between `COMMITTED_SWEEP=0` fleet-wide and a readiness digest showing the track alive: **both were true.** The category error RGM.3 was meant to end survives in a second place. Behavioural for the label, not for dispatch (SWP.1 gates on the setup score). Decide whether the classifier should emit it at all, or whether the fallback path should be narrowed. |
| **VW.1f — three defects in the ledger, found by reading its own first output** | ⬜ **OPEN** | ⬜ | n/a (offline) | **NEW SCOPE, discovered 08-08 from the first real run — filed rather than fixed on the spot, because the fleet does not depend on it.** (1) **~29 TRADES VANISH SILENTLY:** 304 rows − 40 reported unjoinable (37 ORB, 3 butterfly) = 264 mappable, but only **235 joined** (233 continuation + 2 condor). A trade that maps to a family fine but whose `(symbol, family, direction)` key never matches a signal group is dropped with NO line in "not joinable BY CAUSE" — the exact gap by-cause reporting was built to close. Fix: a MAPPED-BUT-UNMATCHED count. (2) **THE MIXED-ERAS WARNING CRIED WOLF ON ITS FIRST OUTING:** all three dates were pre-bake, and `[era] emitted 9,596` is EXACTLY TCS's own total (7,201 + 2,395) — the split was BY TRACK, not by date, so it told the operator to "split the dates at the bake" when no bake was in range. Fix: warn only when a SINGLE track shows both emitted and derived rows. (3) **THE VERDICT FLOOR TESTS THE WRONG THING:** `tr < 3` on TOTAL trades let a verdict print off a 5-trade arm. Fix: a floor on BOTH arms. Compounding it, the per-group MAJORITY-ALIGNMENT collapse systematically SHRINKS the minority arm — the method minimises the very population the verdict rests on, which belongs in the printed caveat. |
| **CV.1 — two canary reds at clean HEAD** | ⬜ **OPEN** | ⬜ | n/a (offline) | **Confirmed present on a PRISTINE clone, NOT introduced by any 08-08 delivery.** `check_versions.sh` pins `v5.4 main header current` while `main.py` is at **v5.8**, and one canary expects `tests/condor_plan_lifetime.py`, which **does not exist in the repo**. Consequence is the reason this is an item and not a footnote: the sweep now ends `DONE — 2 CANARY/PARITY FAILURE(S)` on a perfectly clean checkout, so **its own DONE banner has stopped being usable as a gate** — the cried-wolf failure this repo has already paid for once (WORKING_AGREEMENT §17: an alarm that spams is an alarm that gets filtered). Either update the pin to v5.8 and re-point or delete the orphaned canary; both are one-line edits. Left for the operator's call rather than folded silently into another delivery. |
| **N.7 — ruleset stamp on journal rows** | ✅ 08-07 | ✅ | ✅ **BAKED 08-08** | signal_journal **v1.2**; resolved once at import, `"unknown"` fallback, never a partial hash. 4 tests, deliberate-failure verified. Closes L3.2a's `decision_hash: null` and the 07-29 engine-identity gap. Log-only. |
| **SLIP — one week right** | ✅ 08-07 | n/a | n/a | FREEZE 08-21→**08-28**, GO-LIVE 08-31→**Tue 09-08** (09-07 is Labor Day), FULL SIZE 09-14→**09-21**. |
| **RGM.2 census — RUN** | ✅ 08-07 | ✅ 08-07 | n/a (offline) | dead ticks only 4.2% (my tiebreak worry REFUTED); the finding is **41.9% of ticks carry ≤1 live regime** |

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
2. **Bake Mon Aug 17** with the calibration deploy (devtools 25 bake-only or 23),
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

## PART 0.9 — SATURDAY 2026-08-08 EOD: THE BAKE MOVED, AND THE LEDGER SPOKE (added v4.17)

**THE FLEET WAS BAKED AND RESTARTED ON SATURDAY, NOT MONDAY.** `wake_and_bake
[full]`: **232 files (8 x 29) synced, `[VERIFY] all 29/29 boxes on 43911e9a3d
(== origin/main)`, pycache cleared, optionsbot active on all 29**, boxes left
running by choice. Confirmed independently by an option-14 fan-out: every box
reports `COMMIT=43911e9 SVC=active/active` and a startup line reading
`REGIME ENGINE: l2 (L2 import OK) — OT_REGIME_ENGINE=(unset, default L2)`,
timestamped 20:28-20:30 UTC — i.e. produced BY THIS RESTART, not carried over
from an earlier boot. That timestamp is the check that matters: a stale line
would have proven nothing, which is exactly how a green launders itself here.

**`(unset, default L2)` is correct, not a gap.** main v4.7's startup assert
refuses to boot on an unrecognised engine value, so 29/29 reaching `active`
already proves the resolved value is legal. And `L2 import OK` proves the module
LOADS — never that it COMMITS labels. That still needs `[L2 c=...]` tags on
REGIME lines after Monday's open, the same distinction that hid the dead
uppercase gate for weeks.

**⇒ CONSEQUENCE FOR EVERY STATISTIC: the basis change is 08-08 EOD.** Monday
08-10 is simply the first SESSION on the new engine. The check-in list in PART
0.6 is unchanged; only its premise moved.

### ⚠️ 29 BOXES ARE RUNNING OVER THE WEEKEND — WHAT THAT CHANGES
Deliberate, and the operator's call. Recorded because it has consequences that
would otherwise surface as unexplained numbers on Monday.
- **v5.07 — 2026-08-17 — THE FRAME-REACH CENSUS RAN. NO FOURTH INSTANCE.**
  Read-only; closes the ⬜ candidate TCS.3 raised rather than leaving it open.

  **THE PATTERN IT WAS HUNTING:** three times in a week a lookback was written
  against history its frame does not carry — LIQ.6's 10-day section lookback on
  a 100-bar 5m frame (0.35 days), the ledger's premise, and now TCS.3's bound on
  a 60-bar 1m frame (1.0h) when it was needed at 11:00.

  **WHAT EACH FRAME ACTUALLY REACHES** (cap x bar width, from `TIMEFRAMES`):
  `df_1m` **1.0h** · `df_5m` **8.3h** · `df_15m` **1.56d** · `df_1h` **2.08d** ·
  `df_1d` **60d**. ⚠️ The two frames most engines read are the two that reach
  back least — 1m does not survive one hour, 5m does not survive one session.

  **METHOD:** every `ctx.get("<tf>")` / `ctx["df_*"]` read in non-test code,
  cross-checked against a 20-line window for a session or lookback anchor
  (`09:30`, `session_open`, `prev_day`, `days=`, `LOOKBACK`, `since`).

  **RESULT — 3 sites, 0 undiscovered defects:**
  · `main.py:1645` `_opening_range` — **the TCS.3 case, already fixed.**
  · `main.py:1678` `_session_extremes` df_5m — already carries the correct
    caveat in its own docstring (*"each is a rolling window and neither is
    guaranteed to reach 09:30"*), which is the line that would have prevented
    TCS.3 had it been read.
  · `analysis/trade_readiness.py:863` df_1m — **CLEAN.** `TR_TCS_SD_LOOKBACK`
    is 20 bars against a 60-bar frame: 3x margin.

  ⚠️ **A CLEAN CENSUS IS A RESULT, NOT A NULL.** The question "is there a
  fourth?" is now answered rather than carried. It cost one pass and it is
  re-runnable whenever a new frame consumer lands — which is the cheap moment to
  run it, not after a fleet verification.
  ⬜ THE STANDING RULE THIS ARGUES FOR: a lookback expressed in TIME must state
  the frame it reads and that frame's reach, in the same place. All three
  failures shared one shape — the reach was knowable from `TIMEFRAMES` and
  nobody multiplied it out.

- **🔴 v5.06 — 2026-08-17 — TCS.3: TREND PARTICIPATION NEVER HAD A BOUND.
  FOUND AT NOON, FLEET-VERIFIED, FIXED FOR THE AFTER-CLOSE BAKE.** `main`
  v6.12 · `check_versions` v4.54 · tests/test_opening_range.py v1.0 (6
  executing; born-red 2 vs `b672ae6`).

  **THE OPERATOR'S QUESTION:** no credit-spread trades by Monday noon. The
  code answered it in one arithmetic step: `_opening_range` (v6.7, baked
  Fri 08-14 in `d12ee3e`) read the bound from `ctx["df_1m"]`, which the
  cache caps at **60 bars** — so the 09:30-09:35 bars leave the frame at
  **~10:35 ET, 25 minutes before `TCS_START_ET` (11:00)**. The bound was
  `(None, None)` for every minute of the credit window, on every box, since
  the day it shipped. Trend participation — the trade the 11:00 debit
  cutoff exists to hand the afternoon TO — was structurally off while the
  docstring asserted "the bars do not go anywhere." Its own sibling
  `_session_extremes` already said the true thing: "each is a rolling
  window and neither is guaranteed to reach 09:30."

  **FLEET VERIFICATION BEFORE FIXING (option 14, 15 boxes, 2026-08-17
  ~12:15 ET):** `[tcs] no opening-range` on 13/15 boxes — GLD 289, TLT 290,
  MU 289, SMH 289, NFLX 262, GS 238, SPX 222 with VOTE=0/ADX=0, i.e. the
  direction and ADX gates passed on essentially EVERY evaluated tick and
  every one died at the bound. **Those seven boxes spent the whole morning
  in exactly the conditions this trade was designed for.** AMZN/TSLA also
  showed the condor's PF.5 fork gate refusing as designed (FORK 245/246) —
  the CONDOR's zero today is the operator's guardrail working plus RANGING
  scarcity (PLAN=0 fleet-wide), not a defect. DEFER=0 and F5ERR=0: the F5
  occupancy path is clean.

  **THE FIX (main v6.12):** the bound now reads **TODAY'S 09:30 5m bar** —
  exact for a 5-minute window (`ORB_WINDOW_MINUTES=5`, bars align to :30),
  and present all session on every tape (RTH-only frames span the day;
  SPX's 24h tape reaches ~8.3h back). The 1m window stays as the
  early-session supplement and the general path for window sizes not
  divisible by 5. **Both paths date-filter** — an RTH-only 5m frame carries
  ~1.3 sessions, so Friday's 09:30 bar is in-frame Monday afternoon and
  must never become today's bound (a defect the fix would have introduced
  without the filter; test pins it). v6.7's reasons for not reading the ORB
  engine all stand — only the frame was wrong.

  **SAME FAILURE CLASS AS A2.1, ONE FUNCTION OVER, THREE DAYS LATER:** a
  lookback written against history the frame does not carry. That is now
  three instances in one week (LIQ.6 sections / the ledger's premise /
  this). ⬜ CANDIDATE STANDING ITEM: a one-page census of every
  `ctx["df_*"]` read that assumes reach-back beyond the frame's cap —
  cheaper than finding the fourth one live.

  **TESTS:** first suite in the repo that imports `main` (broker-SDK stub
  pattern from test_audit2_fixes, no-op on boxes). The defining test —
  bound survives a 13:00 frame with 09:30 long gone — is born-red at
  `b672ae6`, as is the date-filter test; the early-session 1m semantics,
  the non-5m fallback and the no-frames case pin unchanged behaviour and
  say so.

  **DEPLOY:** extract + push safe now (boxes pull only at a bake); **BAKE
  AFTER CLOSE** with the rest of Monday's queue. Nothing about this fix is
  freeze-relevant — it makes an already-shipped strategy able to run at
  all. ⚠️ MEASUREMENT NOTE: TC.6's live sample is ZERO trades to date —
  Friday afternoon and Monday morning were not "quiet", they were
  structurally off. The first real TC.6 data begins at tomorrow's open;
  nothing before it belongs in any TC.6 read.

- **v5.05 — 2026-08-16 — WAREHOUSE THREAD: FULL ACCOUNTING, THE WEEK'S DUE DATES, AND WHAT THE MISTAKES TAUGHT.**

  ## PART A — DUE THIS WEEK, EXPLICITLY

  | when | item | gate / why that day |
  |---|---|---|
  | **Mon 08-17** | ⬜ **BAKE `s3_push` v1.8** (option 25) — the ORB removal | Pusher runs on its own timer, so it is **freeze-exempt**. Until it bakes, the fleet still pushes two dead streams |
  | **Mon 08-17, after RTH** | ⬜ **v4.94 Tier-1 verification** — NOT warehouse work | Eleven behavioural changes baked 08-15 have zero live proof. **FEED.2's overnight tape check is the only item that gets worse by waiting** (DXFeed history is same-evening only) |
  | **Tue 08-18** | ⬜ **WH.14 first evaluation** (registered v4.97) | Did `liquidity_ledger` objects land · did `sym=<SYM>_EXT` appear under `raw/candles/` (reasoned, never observed) · did the same boxes report SHORT twice · is 5s spacing right |
  | **Wed 08-19** | ⬜ **THE SEVER.** `OT_EOD_PULL=0`, and point report 41 at `reports/fleet_trades/` | **Run `tools/report_parity.py --since 2026-08-13` FIRST — it must be green.** Wednesday because Mon/Tue are measurement windows and severing inside one makes any anomaly unattributable |
  | **Wed 08-19** | ⬜ **Remove report 41's dedup shim** | Falls out of the repoint: every file in `reports/fleet_trades/` is exactly one day, so the pre-07-28 cumulative-bundle shim becomes dead code |
  | **Thu 08-20** | ⬜ **Delete the root `fleet_trades_*.json`** — only after 41 is repointed and has run clean once | Deleting them earlier silently shortens 41's cumulative window. **This is the one irreversible step in the sequence** |
  | **Fri 08-21** | ⬜ **Lifecycle rule for noncurrent versions + a billing alarm** | Versioning is ON with no lifecycle rule — the only line item that grows with nobody deciding. The alarm is the real protection and is independent of every design choice |
  | **Fri 08-21** | ⬜ **Design (not build) the box-side scrub** | Gated on confirmed-in-S3. The last piece of "push INSTEAD of pull" |

  ## PART B — WHAT WAS ACCOMPLISHED

  **Against the stated goal — bucket, boxes push, conductor wakes-and-verifies,
  devtools repointed, `/reports` cleaned, devtools fortified, redundancy
  severed, audits pass — six of eight are done and the seventh is a decision
  rather than a build.**

  - **Bucket.** `vertigo-warehouse-tx9ai`, us-east-2, instance roles only, no
    access keys, versioning on, SSE-S3. **No Delete permission anywhere in the
    system** — cleanup requires the console, by design.
  - **Boxes push.** Ten stages live on all 29: trades · regime_log ·
    circuit_breaker · eod · ohlc · candles · liquidity_ledger · chains · shadow ·
    signal_journal. **712,501 objects, 1.392 GB, ~$2.82/month.** Content-hash
    keys and read-back-and-compare on every write.
  - **Conductor.** WH.14 — per-box drain-verify, named Telegram alert on
    failure, skip on, batches sequential, scp pull behind a flag.
  - **Devtools fortified.** `devtools.sh` v1.35 is **declarative**: 541 → 184
    lines, numbers generated at render time. **Renumbering is structurally
    impossible rather than watched for.** The EMERGENCY STOP is fixed and
    proven live — it had been pinging 29 boxes over SSH before stopping any of
    them, ~5 silent minutes exactly when the fleet is partially up.
  - **`/reports` cleaned.** 12 type folders, one-offs named rather than counted,
    `fleet_trades/` rebuilt from S3.
  - **Audits pass.** `tools/report_parity.py` — reports 40 and 41 both reproduce
    exactly from the warehouse across the full collection window.
  - **NOT DONE: the sever.** Everything shipped is ADDITIVE. `OT_EOD_PULL`
    still defaults to 1, the S3 menu items sit alongside the local reports, and
    41 still reads the root bundles. Evidence is sufficient; timing is not.

  **TWO FINDINGS THAT WERE NOT ON THE LIST AND MATTER MORE THAN SOME THAT WERE:**

  1. **🔴 THE WAREHOUSE HAS ALREADY PAID FOR ITSELF. 2026-07-15 holds 45 closed
     trades in S3 — 20 boxes, net -722.50 — and control's own bundle for that
     day holds ZERO.** Control can scavenge 12 from other cumulative bundles;
     **33 closed trades exist nowhere else.** They survived only because a box
     still had them in `trades.db` on 08-13 when the first push ran. Every
     cumulative analysis has been seeing 12 of 45 for that day — a ~73%
     understatement, silently biasing any per-day comparison that includes it.
  2. **⚠️ CONTROL HAS NEVER HELD SHADOW DATA.** 18 dates, all S3-only, because
     `backharvest()` pulls `artifacts=("ohlc","journal","chains")` and shadow is
     not in the list. Not a failure — a scope decision nobody had written down.
     **The warehouse is the only route to fleet-wide shadow analysis on control,
     and the Layer-1 freeze that shadow exists to feed is imminent.**

  ## PART C — WHY WE DID IT THIS WAY

  - **Dual-write then sever, never sever on faith.** Bundle equivalence was
    necessary and never sufficient: report 40 normally reads per-box DBs and had
    never been exercised against the warehouse at all, and report 41's answer
    depends on the SET of bundles present, not just their contents. So the gate
    is **output parity**, not input parity.
  - **S3 stays dumb storage. No compute, ever.** A Lambda or Glue job would be
    code with no tests, no version control and no changelog — every discipline
    this repo runs on would stop applying to it. Control pulls raw, aggregates
    in memory, writes the report. Two files produced, both local, both
    regenerable.
  - **Content-hash keys, not uuid4.** A uuid duplicates on every retry. The hash
    covers the RECORD ONLY — v1.0 hashed the envelope, which carries
    `pushed_at_utc`, making the key a function of WHEN rather than WHAT.
  - **One object per state, not per trade.** Rows mutate, so the warehouse holds
    change-data-capture the box itself does not keep — 178 objects for 08-14's
    153 trades. Collapsing at write time would discard history the box
    overwrote.
  - **The menu is data because the number is arbitrary.** Operator: *"as long as
    it calls the correct script, it doesn't really matter what number you call
    it."* So don't test that a renumber was safe — make renumbering a non-event.
    The July 22 incident happened because numbers were hand-maintained in two
    places that had to agree.
  - **COPY, never move, in `/reports`.** It is BOTH an output directory and an
    input directory; a move is a live edit to three readers' data sources.
  - **Against Parquet compaction, against a Glue crawler, for Athena but gated.**
    Compaction would save money that does not exist and **cannot refund PUTs
    already made**; the real argument is query latency and no report has shown
    that pain. Athena gets a workgroup scan limit and partition projection.
  - **Two streams were REMOVED rather than fixed.** `orb_state` captured zero
    objects in thirty days and nothing consumed it. **A stream nobody consumes
    that captured nothing is not a capture bug to diagnose; it is a stream to
    stop collecting.**

  ## PART D — LESSONS FROM THE MISTAKES

  **Every one of these was mine, and none was in the warehouse.**

  - **🔴 FIVE COMPARISON-DESIGN ERRORS, ONE ROOT CAUSE: the two sides were not
    asked the same question.** (a) The parity tool compared 25 local sessions
    against 1 warehouse date. (b) It changed two variables at once —
    DBs-vs-bundle *and* local-vs-warehouse — so no difference could be
    attributed. (c) It picked a file **by mtime** and read a stale full-fleet
    run. (d) A noise filter popped `generated` when the key is `generated_utc`.
    (e) `--all` compared a pre-07-28 CUMULATIVE bundle date-for-date against
    date-partitioned storage and reported six "divergent" dates that were never
    gaps. **Before believing a red result, check whether both sides were asked
    the same question.**
  - **🔴 A TEST THAT MANUFACTURES ITS OWN FAILURE IS WORSE THAN NO TEST.** It
    burns attention and makes a real divergence indistinguishable from noise —
    the CV.1 lesson restated. I deleted a menu-integrity test of mine rather
    than fix it: it produced eleven failures of which nearly all were its own
    bugs, reporting four live menu items as missing and inventing a phantom one.
  - **🔴 A "VALUE" DIFFERENCE THAT IS REALLY AN ORDERING DIFFERENCE GETS
    MISDIAGNOSED AS DATA CORRUPTION.** Report 40 diverged at one figure in 421;
    the located lines held the same rows in a different order.
    `consolidate_trades:239` sorts by (box, entry_time), the reader sorted by
    (entry_time, box). Trade-level equality was never affected — which is why
    `--compare` always said 153/153.
  - **🔴 CHECK WHAT AN ASSERTION ACTUALLY READS.** Four of my own tests passed or
    failed for the wrong reason: a `_stop` match hitting the `def` not the call
    site · a rounded value compared at 1e-6 · a stub too small for its cost to
    register at printed precision · a fixture that fell out of coverage when a
    filter landed and silently stopped testing anything.
  - **🔴 THE TOOL BUILT TO COMPARE TWO SOURCES WAS QUIETLY MERGING THEM.** The
    reader's default output path sat inside report 41's input glob. Caught
    before a single file was written. Output now goes elsewhere and a write into
    the glob namespace is **refused, not warned about**.
  - **🔴 A PREVIEW THAT NAMES THE WRONG ACTION IS WORSE THAN NO PREVIEW.** The
    organiser's dry run said "13 files copied" for a type where nothing gets
    copied.
  - **🔴 A TOOL MUST NOT THROW WHEN THE THING IT MEASURES HAS BEEN FIXED.**
    `menu_extract.parse()` raised `StopIteration` the moment the heredoc it
    parsed was replaced by the declarative registry — the proof tool broke at
    exactly the moment it was needed.
  - **🔴 IT COULD NOT TELL "DIVERGED" FROM "DID NOT RUN".** With no credentials
    every step errored and it still printed "NOT AT PARITY — investigate the
    diffs above" when there were no diffs. Three verdict states now, and **an
    unrun date is not a passing date**.
  - **⚠️ VERIFY A MENU ITEM BY DRIVING THE MENU.** The operator's call. It caught
    three things the shell path could not: relative `--bundles-dir` paths, an
    11-line botocore traceback where one sentence belonged, and the verdict
    defect above.
  - **⚠️ ANY MULTI-MINUTE OPERATION SHIPS WRAPPED IN `tmux`.** The fleet is run
    from mobile; the session is the fragile part, not the tool. The `--apply`
    that survived a dropped connection did so because it was **idempotent by
    design** — copies skip identical files, rebuilds overwrite deterministically,
    nothing moves or deletes.
  - **⚠️ REFRESHING A BASELINE IS ONLY LEGITIMATE AFTER READING WHAT CHANGED.**
    Doing it reflexively turns a proof tool into a rubber stamp.
  - **⚠️ AND TWO PLAIN ERRORS OF FACT I HAD TO WITHDRAW:** I argued the ORB
    attempt counter was not derivable (it rides on every journal event), and I
    recorded that the L1 analysis reads local shadow files (control holds none).
    **Both were stated confidently and both were wrong; the operator's question
    was what surfaced each one.**

- **v5.04 — 2026-08-16 — THE RECURRING REPORT REGISTER. EVERY NIGHTLY ARTIFACT NOW STATES WHY IT EXISTS.**
  Operator, on two report types found in `reports/`: *"They are recurring but I
  don't know why we are collecting them. It should state the reason in
  BACKLOG."* Both were in fact documented — **in their producers' header
  comments, which is not somewhere anyone looks when asking "can I delete
  this?"** A purpose recorded only in the code that writes the file is a
  purpose that disappears the moment someone reads the directory instead.

  | report | producer | why it exists | consumed by |
  |---|---|---|---|
  | `fleet_trades_<date>.json/.csv` | `consolidate_trades.py` (39) | full-fidelity per-day fleet trade bundle | reports 40 (fallback) and 41 (glob); **now rebuilt from S3** |
  | `excursions_<date>.txt` | `excursion_report.py` (40) | MFE/MAE distributions | read by hand; the fitting thread |
  | `trade_report_<date>.json` | `trade_report.py` (41) | cross-day regime/strategy/grade breakdown | read by hand; `fit_report` |
  | `regime_replay_<date>.jsonl` | `validate_regime.sh` (42–46) | tape-only Layer-1 confluence replay | **report 47 auto-discovers these** |
  | `conditional_tables_<first>_<last>` | otv3 `tests/conditional_tables.py` | **ROADMAP L3.4 conviction-bar substrate**, built nightly so it does not depend on a manual run. **Cumulative BY DESIGN** — a conditional cell only becomes decision-grade as sample accrues | the L3.4 conviction work |
  | `readiness_digest_<date>` | otv3 `tests/readiness_digest.py` | machine states, R distribution, would-fire counts, arm episodes, staged picks, anticipation lead-times | **the file the readiness bars (`OT_TR_*`) get tuned from** |
  | `swallow_audit_<date>.json` | otv3 `tests/swallow_audit.py` (backlog W.2) | nightly silent-failure census; **WARNS when the silent-handler count rises**, i.e. when someone adds an exception handler that swallows without logging | the week of 2026-07-27 produced **eight defects of exactly that shape** — a census nobody runs would have caught none |
  | `vwap_orientation_<date>.txt` | otv3 `tests/vwap_orientation_ledger.py` | **evidence for backlog item E**, which must NOT be built until the evidence says which direction the gate belongs in | item E's decision |
  | `morning_report_<date>.json` | the morning brief chain | AM selection + sentiment | report 41's sentiment join |
  | `daily_trades_<date>.json` | `harvest.py` | trade-anatomy aggregation, the original v0.1.0 product | the trades-analysis thread |
  | `backharvest_<date>.json` | `harvest.py backharvest()` | **a RECEIPT, not an analysis** — records that a past session's date-addressed artifacts (OHLC, journal, chains) were recovered | forensic record of what was pulled and when |
  | `fit_report_<date>.txt` | `fit_report.py` | everything for fitting in one file | the fitting thread |

  - **THE STANDING PRINCIPLE THIS ENCODES:** every recurring artifact names a
    consumer. Two of the strongest entries — swallow_audit and vwap_orientation
    — exist precisely because *"evidence that accrues only when someone
    remembers to run a script will not exist on decision day."* That is the
    same argument as the warehouse itself, applied to reports.
  - **🔑 AND IT EXPLAINS THE SHADOW GAP.** `backharvest()` pulls
    `artifacts=("ohlc", "journal", "chains")` — **shadow is not in the list**,
    which is why control holds ZERO shadow dates while S3 holds 18. Not a
    failure; a scope decision nobody had written down. **The warehouse is
    therefore the only route to fleet-wide shadow analysis on control, and the
    Layer-1 freeze that shadow exists to feed is imminent.**
  - **`tools/reports_organize.py` v1.2 — one-offs are NAMED, not counted.**
    `sweep` tripped the 3-file threshold and would have been given a folder.
    Raising the threshold to 4 would not fix the class: the next diagnostic run
    three times gets a folder too, and `fit_report` (5) sits close to the edge.
    A count is a proxy for "is this automated"; the answer is knowable, so it is
    declared.

- **v5.03 — 2026-08-16 — ORB REMOVED FROM THE WAREHOUSE. A STREAM NOBODY CONSUMES THAT CAPTURED NOTHING IS NOT A CAPTURE BUG.**
  `warehouse/s3_push.py` v1.8 · suite v1.8 (92 checks). Eleven stages → **ten**.
  - **THE OPERATOR ASKED THE QUESTION THAT SETTLED IT:** *"Do we even need it?
    The orb state could be derived by the first 5-minute candle of the RTH."*
    `raw/orb_state` had captured **ZERO objects in thirty days** and
    `raw/orb_range` 81, and nothing read either.
  - **EVERYTHING IT HELD IS ALREADY AVAILABLE.** The RANGE recomputes from
    candles, warehoused at 1m and 5m. The ATTEMPTS are logged individually in
    the signal journal with price and timestamp — **`tests/orb_conversion.py`
    already derives break-attempts from `retest_check` events keyed on
    (symbol, date, direction, attempt) and never opens `orb_state.json`.** The
    state machine is the only unique part and nothing has ever asked for it.
  - **⚠️ I HAD ARGUED THE ATTEMPT COUNTER WAS NOT DERIVABLE. THAT WAS WRONG** —
    the attempt number rides on every journal event. I was also treating "zero
    objects in thirty days" as a defect to diagnose, when the correct reading
    was the operator's: stop collecting it.
  - **The 81 existing `orb_range` objects stay in `raw/`**, which never deletes.
    They simply stop growing.
  - **THE TESTS WERE DELETED, NOT FIXED.** They asserted real behaviour and
    passed; the FEATURE went. The three stage-order assertions drop from
    eleven/nine/eight names to ten/eight/seven — **an order test is only worth
    having if it covers the stages that actually exist.**
  - ⚠️ Also caught: I wrote "eleven stages become nine" in my own changelog. ORB
    was ONE stage covering both files, so it is **ten**. Corrected in place.
  - **⚠️ NEEDS A BAKE (option 25).** Removal only; no trading-loop effect.

- **v5.02 — 2026-08-16 — 🎯 WH.11 GATE MET: A REPORT NOW RUNS FROM THE WAREHOUSE AND REPRODUCES THE LOCAL PIPELINE EXACTLY.**
  `tools/report_parity.py` v1.3 · `warehouse_reader.py` v1.6 ·
  `trade_report.py` v1.8 · `excursion_report.py` v3.4 · devtools item 67.
  - **RESULT on 2026-08-14:** `40: DB-vs-localbundle same | localbundle-vs-WAREHOUSE MATCH` · `41: MATCH`.
    **The 07-23 chain-archive trap is broken.** Since that date the standing
    caution has been that a store makes collection cheap and analysis merely
    *feel* imminent. Two reports now run end-to-end off S3 and produce output
    identical to the local pipeline's.
  - **⚠️ SCOPE: ONE DATE.** Parity is proven for 2026-08-14 only. `--since
    2026-08-13` covers the whole collection window and must be clean before
    anything is severed. Pre-08-13 dates are partial by construction (§6a) and
    cannot pass. **`OT_EOD_PULL=0` is now DEFENSIBLE, not JUSTIFIED.**
  - **IT TOOK THREE ROUNDS OF TOOL DEFECTS TO GET A TRUSTWORTHY RESULT, AND ALL
    THREE WERE IN THE INSTRUMENTATION, NOT THE WAREHOUSE:**
    1. **The tool manufactured its own failure.** Report 41 is cross-day; the
       local side globbed ~25 bundles while the warehouse side had ONE rebuilt
       date, so it compared 25 sessions against 1. Report 40 changed two
       variables at once (DBs-vs-bundle *and* local-vs-warehouse), so no
       difference could be attributed. And the noise filter popped `generated`
       when the key is `generated_utc`.
    2. **It read the wrong file.** `newest()` chose a `trade_report_<stamp>.json`
       **by mtime** — a guess — and returned a stale full-fleet run (1,742 raw
       rows, 1,315 trades) instead of the restricted run it had just produced.
       **Identifying a file by "probably the newest" is not identifying it.**
       Fixed with an explicit `--out`.
    3. **The last "value" difference was an ORDERING difference.** Report 40
       diverged at one figure in 421 — but the located lines held the same rows
       in a different order (`max_loss_floor/Continuation` vs
       `orb_structure_stop/ORBStrategy`). `consolidate_trades:239` sorts by
       **(box, entry_time)**; the reader sorted by **(entry_time, box)**.
       Trade-level equality was never affected — which is why `--compare` had
       always said 153/153 — but downstream grouping breaks ties by input order.
       **A value difference that is really an ordering difference is the kind of
       thing that gets misdiagnosed as data corruption.**
  - **WHAT MADE THE DIAGNOSIS POSSIBLE** was v1.2 printing the differing VALUES
    and the source LINE holding the divergent figure, instead of naming the
    section and leaving it there. A difference you cannot act on is half an
    answer.
  - **⚠️ DO NOT SEVER ON MON 08-17 OR AHEAD OF THE TUE 08-18 WH.14 EVALUATION.**
    Monday is v4.94's Tier-1 verification session for eleven unvalidated
    changes. The dual write costs almost nothing; severing inside a measurement
    window would make any anomaly unattributable.

- **v5.01 — 2026-08-16 — `docs/WAREHOUSE_LAYOUT.md` v2.0: THE SPEC CATCHES UP WITH WHAT IS ACTUALLY RUNNING.**
  v1.0 was written on 08-13 when one stream was migrated and nine were
  "planned". Every one is now migrated, three streams exist that v1.0 never
  mentioned, and the handback document was the furthest-drifted artifact in the
  project.
  - **⚠️ THE DRIFT INCLUDED TWO STREAMS v1.0 SPECIFIED AND NOBODY BUILT** —
    `regime_log` and `circuit_breaker_events` sat in the register as "planned"
    for three days while six *other* streams were built around them. A
    specification that lists something is not evidence it exists.
  - **NEW §4a — MEASURED VOLUME AND COST**, read off the bucket rather than
    estimated: 712,501 objects, 1.392 GB, ~23,750/day, **~$2.82/month, 88% of
    it PUT requests and 5% storage.** Records which column answers which
    question — journal and shadow dominate OBJECT COUNT, chains dominate BYTES;
    a compaction candidate is chosen by bytes, a latency problem is caused by
    count. Carries the standing decision: **against compaction, against a Glue
    crawler, for Athena but gated behind a workgroup scan limit and partition
    projection**, plus the one real billing-surprise vector (versioning with no
    lifecycle rule).
  - **NEW §5a — WHERE PROCESSING HAPPENS.** Append on the box, dedup in the
    reader, aggregation in reports, **S3 as storage with no compute ever.** Two
    warnings recorded rather than left implicit: **dedup currently happens TWICE
    with different tie-breakers** (reader keeps newest `pushed_at_utc`, report
    41 keeps the most-filled row), and **poison cannot be deleted once pushed** —
    `raw/` has no Delete permission, and the box purge runs on a different
    cadence than the pusher, so a bad bar can land permanently. The read-side
    filter is an open decision, not a bug.
  - **NEW §6a — COLLECTION COVERAGE IS NOT `dt=` COVERAGE.** The bucket holds
    partitions back to 07-06 but began collecting 08-13; the first push shipped
    whatever history survived on each box, and `trim_trade_dbs` had already
    pruned the rest. Confusing the two produces false alarms.
  - **§11 IS NO LONGER HYPOTHETICAL.** The read path exists and **19 of 25 dates
    reproduce the control bundle exactly** — every date from 07-22 onward. But
    the section now says plainly what that does NOT establish: report 40 reads
    per-box DBs rather than the bundle, report 41 globs every bundle, and **no
    report has been run from the warehouse yet.** The pile is now well-organised
    AND readable — and still unread.
  - **⚠️ DOC ONLY. No code, no bake, freeze-irrelevant.**

- **v5.00 — 2026-08-16 — THE DEVTOOLS MENU IS DATA. RENUMBERING IS NOW STRUCTURALLY IMPOSSIBLE, NOT MERELY WATCHED FOR. PLUS THE READER'S COVERAGE FLOOR AND `--explain`.**
  `day_trader_pro/devtools.sh` **v1.32** (541 → 184 lines) · `menu_registry.sh` ·
  `menu_functions.sh` · `tools/menu_extract.py` v1.3 ·
  `tests/test_menu_extract.py` (21 checks) · `docs/MENU_INVENTORY.tsv` ·
  `warehouse_reader.py` v1.3 (43 checks).
  - **THE OPERATOR'S FRAMING, WHICH IS THE WHOLE DESIGN:** *"What number the
    action is is irrelevant. You could scramble the order or scramble the
    numbers. And as long as it calls the correct script, it doesn't really
    matter what number you call it."* Then: *"I don't want anything tied to the
    number. The number should be able to be completely arbitrary."*
  - **SO NUMBERS APPEAR IN NEITHER FILE.** `menu_registry.sh` lists
    (SECTION, LABEL, FUNCTION) in display order; `menu_functions.sh` holds one
    function per item with the body copied VERBATIM from the old case block —
    option 58's 26 lines of prompts and nested conditionals stay 26 lines rather
    than being flattened into a delimited string, which would have meant hand-
    rewriting a destructive handler. `menu_render` assigns numbers from a loop
    counter; `menu_dispatch` matches the same counter. **The July 22 v1.18
    incident happened because numbers were maintained by hand in two places that
    had to agree. That class of failure is now impossible by construction.**
  - **EQUIVALENCE PROVEN, NOT ASSUMED.** `--roundtrip` before the swap: 58 vs 58,
    zero label differences, zero command differences. `--diff` across the swap:
    **every label survives with an identical command.** The diff tool is proven
    in BOTH directions — a randomly scrambled order passes clean, while removing
    the EMERGENCY STOP label or repointing a script is caught and named.
  - **⚠️ SIXTEEN NUMBERS MOVED.** Identity is the label; muscle memory is not.
    **FIT REPORT 57 → 42** (it always displayed inside TRADES DATA, out of
    numeric order) and everything 42–56 shifts up by one. **1–41 and 58 are
    unchanged. EMERGENCY STOP is still 27.**
  - **AND IT FIXED A PRE-EXISTING DRIFT:** the file header read v1.31 while the
    rendered menu still said "v1.26 Service Menu" — the same class as the
    title-vs-changelog rule. Both v1.32, and the version now lives in ONE place.
  - **THREE OF MY OWN BUGS, ALL FOUND BY RUNNING IT RATHER THAN READING IT:**
    (1) `0` did `return 9`, but the caller is `while true; do menu; done`, so
    Exit looped forever — now `exit 0`; (2) a splice left an orphaned `}` and my
    version helper deleted the title line; (3) **`menu_extract.parse()` threw
    `StopIteration` once the heredoc vanished — the proof tool broke because the
    thing it measured had been fixed.** It now degrades: `--check` reads
    whichever source is live, `--roundtrip` says plainly there is nothing left
    to compare. A tool that throws when its subject improves is a tool you stop
    running.
  - **AN EARLIER MENU TEST OF MINE WAS DELETED, NOT FIXED.** A regex over the
    whole of `devtools.sh` produced ELEVEN failures, of which nearly all were its
    own bugs — it reported four live items as missing and invented a phantom
    entry. **A check that cries wolf trains you to ignore red runs** (the CV.1
    lesson). The bounded marker-based parser reconciles exactly instead.
  - **WAREHOUSE READER v1.3:** the coverage floor was the WRONG QUANTITY — it
    read the earliest `dt=` partition (2026-07-06) and excluded nothing, because
    **`dt=` coverage is not COLLECTION coverage**: the first push shipped
    whatever history survived on each box. Floor is now the collection start
    (2026-08-13). `--explain <date>` lists the differing trade_ids per side so a
    divergence is READ rather than inferred.
  - **⚠️ CONTROL-SIDE ONLY. No bake, no fleet change, freeze-irrelevant.**

- **v4.99 — 2026-08-16 — WH.9a: MEASURE THE BILL BEFORE DECIDING ABOUT COMPACTION. RECOMMENDATION: DON'T — YET.**
  `day_trader_pro/warehouse_cost.py` v1.0 + suite (15 checks). Read-only: LIST
  only, no GET, no write, no delete.
  - **THE RECOMMENDATION, STATED PLAINLY: AGAINST Parquet compaction for now,
    and AGAINST a Glue crawler ever.** On estimated volumes the entire warehouse
    runs **under ~$2/month** — ~14.6k objects/day, ~0.11 GB/day, ~28 GB/year;
    PUT ~$1.53/mo, verify-GET ~$0.12, storage cents. **Compaction would save
    money that does not exist.**
  - **THE REAL ARGUMENT FOR COMPACTION IS LATENCY, NOT DOLLARS.** An Athena
    query over a month of `signal_journal` reads ~230,000 objects and per-file
    overhead dominates. No report has demonstrated that pain yet, and building
    the tier before a consumer complains is the 07-23 chain-archive trap in a
    new costume. **Trigger to revisit: a report that must scan >1 month of
    journal or chains AND is measurably too slow.**
  - **ATHENA: YES, BUT GATED.** Enable it when a specific report needs SQL;
    create the workgroup with a **per-query data-scan limit** so a runaway query
    cannot surprise the bill; use **partition projection, not a crawler** —
    crawlers cost money on a schedule and add a moving part. The
    sequential/stateful reports (replay integrator, MFE/MAE, run lengths,
    pitchfork geometry) stay Python; forcing them into SQL is a downgrade.
  - **⚠️ THE ONE REAL BILLING-SURPRISE VECTOR IS VERSIONING WITH NO LIFECYCLE
    RULE.** Noncurrent versions accumulate with nobody deciding — it is the only
    line item here that grows unbidden. Content-hash keys make overwrites rare
    so it is slow, but it is unbounded. `--versions` accounts it separately and
    warns. A billing alarm is the real protection and is independent of every
    design choice above.
  - **WHY A SCRIPT AND NOT A ONE-LINER:** the recommendation above rests on
    ESTIMATES — object counts times typical sizes. Estimates are fine for a
    recommendation and useless for a billing decision. This reads the real
    bucket, splits BYTES from OBJECTS per prefix (they point at different
    streams — journal dominates objects, chains dominate bytes), derives the
    per-day rate from the distinct `dt=` partitions actually present, and
    reports year-1 storage as the AVERAGE balance rather than the peak, because
    that is how it is billed.
  - **A TEST THAT FAILED FOR THE WRONG REASON, AGAIN CAUGHT:** the byte-total
    assertion compared a 4-decimal ROUNDED figure at 1e-6 tolerance, and the
    noncurrent-cost assertion used a 1 MB stub whose cost rounds to $0.000 — it
    would have "passed" only by luck. Both fixed; the second stub is now sized
    so the line item is visible at the printed precision, which is the point of
    testing it at all.
  - **⚠️ CONTROL-SIDE ONLY, read-only. No bake, no fleet change.**

- **v4.98 — 2026-08-16 — WH.8: THE WAREHOUSE HAS A READER. AND TWO STREAMS WERE MISSING THAT NOBODY WOULD HAVE NOTICED UNTIL THE DIFF.**
  `day_trader_pro/warehouse_reader.py` v1.0 + suite (23 checks) ·
  `warehouse/s3_push.py` v1.7 (97 checks).
  - **🔴 `regime_log` AND `circuit_breaker_events` WERE NEVER BEING PUSHED.**
    The bundle has a `regime_timeline` and a `breaker_events` section, both
    sourced from those tables inside trades.db. WH.2 scoped itself to the
    `trades` table and said the other two would follow; WH.3 covered six OTHER
    streams and they were never picked up. **Found by building the reader, not
    by looking** — and a reader built on top would have produced two
    permanently empty sections, with the WH.11 diff showing a gap forever and
    the reader taking the blame for a missing push. Both are append-only, so
    they use a stable per-row content hash with no CDC semantics.
  - **THE READER IMPORTS `_stats` AND `_load_selection` FROM
    `consolidate_trades` RATHER THAN REIMPLEMENTING THEM.** If it computed its
    own win-rate the WH.11 diff would compare two ARITHMETICS as well as two
    SOURCES and a mismatch would be ambiguous. The only thing allowed to differ
    between the bundles is where the rows came from.
  - **LATEST-STATE-PER-TRADE, AND THE ORDER IS LOAD-BEARING.** The warehouse
    holds every state a row passed through — more than the local bundle keeps —
    so the reader groups by `trade_id` and keeps the newest `pushed_at_utc`.
    **Collapse BEFORE filtering `status='closed'`, never after:** a trade open
    at 10:00 and closed at 15:00 has objects in both states, and filter-first
    would keep whichever survived the filter and could drop the trade entirely.
    A test asserts the ordering rather than trusting the comment beside it.
  - **`box` COMES FROM THE `sym=` PARTITION** — the warehouse's equivalent of
    consolidate_trades' authoritative filename tag. The row's own `symbol` is
    left untouched, so a mislabeled row keeps both values for audit. Same
    contract, different source; proven with a deliberately mislabeled row.
  - **`--compare` IS WH.11's GATE, SHIPPED EARLY.** It diffs the two bundles on
    what matters — trade counts, the closed set, per-trade P&L and status — and
    ignores cosmetic differences like `generated_utc`. It prints **MATCH** or
    **DIVERGENCE — do NOT sever**.
  - **⚠️ NOTHING IS SEVERED AND NOTHING IS PROVEN YET.** The reader has been
    exercised against a stub, not against the real bucket. First real run needs
    a date whose trades are fully drained. **`OT_EOD_PULL=0` stays gated on a
    clean `--compare`.**
  - **⚠️ s3_push v1.7 NEEDS A BAKE (option 25)** or the two new tables never push.

- **v4.97 — 2026-08-16 — 🗓️ DUE TUE 08-18: WH.14's FIRST EVALUATION. AND A CORRECTION TO MY OWN SEQUENCING.**

  **⚠️ FIRST, THE CORRECTION.** I recommended *"Monday runs the CURRENT
  conductor, WH.14's first live EOD is Tuesday"* — and then WH.14 was landed on
  control the same evening. **Monday 08-17 will therefore run `eod_backfill`
  v1.3, not v1.2.** The recommendation was overtaken by the landing and saying
  otherwise would be false.

  **WHY THAT IS ACCEPTABLE, MEASURED BY DIFF RATHER THAN ASSUMED.** At DEFAULT
  config the v1.2→v1.3 behavioural delta is exactly two things:
  1. **~20s of added spacing per batch** (`OT_EOD_DRAIN_SPACING=5`, four gaps
     across five boxes). The drain loop was already serial.
  2. **A Telegram alert when a box reports SHORT.** New output, not new
     behaviour — `_drain_verify` already ran in v1.2 and already did not block.

  The scp pull is UNCHANGED: `OT_EOD_PULL` defaults to 1. **The one genuinely
  behavioural change — severing the pull — is opt-in and stays gated on WH.11
  regardless.** So Monday inherits an alert and twenty seconds, not a rework.

  **🗓️ MONDAY 08-17, WATCH ITEM (not an action):** expect Telegram alerts naming
  any box that reports SHORT. **That is the instrument working, not a fault** —
  boxes with journal backlog have been reporting SHORT by design since WH.4.
  Do not read a first-night alert as a conductor regression, and do not let it
  displace v4.94's Tier-1 list, which owns that session. **FEED.2's overnight
  tape check remains the only item that gets worse by waiting** (DXFeed history
  is same-evening only).

  **🗓️ TUESDAY 08-18, DUE — WH.14's FIRST EVALUATION.** Tuesday rather than
  Monday because Monday's session belongs to validating eleven behavioural
  changes baked 08-15 with zero live proof, and reading a reworked conductor's
  first results in the same window confounds the two: a backfill anomaly could
  be the conductor or any of the eleven, and you would not be able to tell which.
  1. **Did `liquidity_ledger` objects land?** Count `raw/liquidity_ledger/` —
     it should be non-zero for every box that traded. This stream did not exist
     in the warehouse before today and the mapper is what it feeds.
  2. **Did `sym=<SYM>_EXT` partitions appear under `raw/candles/`?** FEED.2's
     overnight tape reaching the warehouse is unverified — reasoned from
     `SELECT DISTINCT symbol`, never observed.
  3. **How many boxes reported SHORT, and were they the same ones twice?** A
     box short on two consecutive nights is a real problem; a different box each
     night is backlog draining normally.
  4. **Is 5s the right spacing?** It cost ~20s per batch. Raise it only if
     something measurably contended; lower it to 0 if nothing did.
  5. **⬜ DO NOT SEVER.** `OT_EOD_PULL=0` stays gated on WH.11 comparing report
     outputs from both sources. Nothing on Tuesday unlocks it.

- **v4.96 — 2026-08-16 — WH.14: THE EOD PASS FILLS THE BUCKET, FAILS LOUDLY, AND THE PULL BECOMES SEVERABLE. PLUS THE LIQUIDITY LEDGER JOINS THE WAREHOUSE.**
  `warehouse/s3_push.py` v1.6 (88 checks) · `day_trader_pro/eod_backfill.py` v1.3
  + `tests/test_eod_backfill_wh14.py` v1.0 (17 checks).
  - **🔴 THE LIQUIDITY LEDGER WAS NOT BEING PUSHED.** LIQ.4 wired
    `data/liquidity_ledger/<date>/<SYMBOL>.json` on 08-15 — the level book the
    mapper builds from — and no warehouse stream covered it. Now a whole-file
    stream like OHLC. It is rewritten on EVERY closed bar, but the pusher
    samples every 5 minutes, so the object count lands near the chain archive's
    rather than near 390/box/day, and each sampled state is its own object —
    **the intraday EVOLUTION of the level book survives, not just its closing
    shape.**
  - **FEED.2 NEEDS NOTHING HERE.** Extended-hours tape lands in feed_store as
    its own store symbol `<SYM>_EXT`, and `push_candles` does
    `SELECT DISTINCT symbol`, so it already partitions as `sym=<SYM>_EXT`.
    Verified by reading, not assumed.
  - **FAIL LOUDLY, SKIP ON** (operator). A box that cannot confirm now fires a
    REAL Telegram alert through the conductor's EXISTING notify path — named,
    counted, and saying the data is stranded until the next wake rather than
    lost. It does not hold the pipeline: holding would strand the whole backfill
    against the stream cap. A Telegram failure cannot stop the pass either.
  - **THE SCP PULL IS NOW SEVERABLE BY CONFIG** — `OT_EOD_PULL`, default ON.
    Ending the dual write becomes a flag flip rather than a code change, and it
    is reversible, which is the point of dual-write-then-sever (decision #5).
  - **⚠️ BATCHES REMAIN SEQUENTIAL — group A stops before group B wakes.** An
    earlier cross-batch pipeline idea of mine was wrong; the operator corrected
    it and it is not built. A test asserts no threading crept in.
  - **AN HONEST NOTE ON THE STAGGER.** The drain loop was ALREADY serial, so the
    five boxes in a batch never drained simultaneously — the new spacing knob
    makes that deliberate and tunable rather than incidental. The real
    concurrency is each box's own 5-minute timer, which no conductor setting can
    reach; that is handled on the box by `Nice=15` / idle IO. **Also worth
    stating plainly: five boxes pushing to S3 at once was never a problem for
    S3** — one object per event exists precisely so concurrent writers cannot
    collide, and each box writes only its own `sym=` prefixes.
  - **A TEST THAT FAILED FOR THE WRONG REASON, CAUGHT.** The `_stop` ordering
    assertion matched `def _stop(recs, dry):` as well as the call site, so it
    was reading the function definition's position. Fixed to match the indented
    call. **An assertion that passes for the wrong reason is worse than none.**
  - **⚠️ CONTROL-SIDE + BOX-SIDE.** s3_push needs a bake (option 25); the
    conductor files are control-only. **Recommend Monday runs the CURRENT
    conductor** — v4.94 makes 08-17 after RTH a verification session for eleven
    unvalidated changes, and the reworked conductor's first live EOD should not
    muddy that signal. First real run **Tuesday**.

- **v4.95 — 2026-08-16 — WH.7: THE EMERGENCY STOP WAS PINGING 29 BOXES OVER SSH BEFORE STOPPING ANY OF THEM.**
  `day_trader_pro/wake_and_bake.py` v1.3 · `tests/test_emergency_stop.py` v1.0.
  Operator: *"presently it just hangs & gives no warning."*
  - **THE MECHANISM, READ FROM SOURCE.** Option 27 runs `--shutdown-only`, whose
    path was HALT gate → notify → discover → **`stage_ping` over ALL 29** →
    stop. Discovery returns STOPPED instances too, and a stopped box keeps a
    stale `private_ip`, so the ping SSHed machines that cannot answer and paid
    `SSH_CONNECT_TIMEOUT=12s` each. The loop is SEQUENTIAL: ~27 down = **~5.4
    minutes for a single pass**, longer than `SSH_READY_TIMEOUT=180s` — which is
    only checked BETWEEN passes — and the first `…waiting for SSH` line prints
    only AFTER a full pass. **~5 silent minutes before the stop was attempted,
    and worst precisely when the fleet is partially up, which is when you reach
    for a kill switch.**
  - **THE FIX IS A DELETION.** Stopping needs an instance ID, not an IP and not
    a reachable host: `_ids()` reads `instance_id`, `ec2ops.stop()` takes ids,
    and `wait_state("stopped")` already returns True for a box that is stopped.
    The operator made the same point independently — *"the instance map does not
    even require any IP addresses."* Shutdown now skips the ping entirely.
    Reachability is irrelevant to the one job this mode has.
  - **SCOPED, NOT BLANKET.** `stage_ping` is still correct for `full`/`bake`,
    which must know what they are syncing. Only the shutdown branch skips it.
  - **IT CAN NEVER LOOK SILENT AGAIN** — it now announces that it is skipping
    reachability, and announces the stop request BEFORE the poll begins.
  - **⚠️ SAFETY PROPERTIES PINNED BY NAME, NOT BY POSITION** — the July 22 rule
    applied to code rather than to a menu. The suite asserts the HALT gate
    string, its exact comparison, the position-abandonment warning, the
    live-fleet in-RTH escalation, the RTH exemption, and "no EOD, no pycache".
    **This item has now been damaged silently twice** — the v1.18 renumber took
    its label, the pre-ping took its responsiveness — so it gets a test that
    fails loudly instead of a comment asking for care.
  - **DELIBERATE-FAILURE GATE:** the suite patches `_exec` to RAISE, so any SSH
    in the shutdown path is an instant error rather than a five-minute wait.
    **Verified rc=1 against v1.2 and rc=0 against v1.3** — the bug made visible
    in milliseconds. 15 checks.
  - **⚠️ CONTROL-SIDE ONLY. No bake, no fleet change, freeze-irrelevant.**

- **v4.94 — 2026-08-15 — MONDAY 08-17 AFTER RTH: THE ORDER OF WORK.**
  Eleven behavioural changes baked to 29/29 with **zero live validation**. The
  first session is a verification session, not a development one.

  **TIER 1 — DID THE BAKE WORK? (do these before anything else, in order)**
  1. **⚠️ FEED.2 — is overnight tape actually arriving?** One fleet command:
     count `<SYM>_EXT` rows and their earliest ET hour. **If `ext` bars are
     absent, LIQ.6's sections are still inert and everything downstream of them
     is unchanged** — and a lost night is unrecoverable (DXFeed history is
     same-evening only), so this is the ONLY item that gets worse by waiting.
  2. **TC.6's first clean execution.** It has NEVER traded correctly — the
     identity chain, the dispatch routing and the exit branch were each broken
     in sequence. Check it fired, was labelled `TrendCreditSpread`, and exited
     on breach or 15:45 rather than a condor ladder.
  3. **BFLY.3 volume.** SMH went from 3 fires to a possible 46 on the 08-15
     read. **A large jump on one symbol from one day's data is exactly what a
     flat ceiling could get wrong** — count fires per symbol and check the
     realized ratios sit under 0.50.
  4. **F7/F5/F8 fired at all?** Each is a defect fix with no live proof yet.
     Grep for `regime_flip` on continuations (F7's new vote gate), the F5 orphan
     warning, and `gate_block:afternoon_debit` dispositions (F8's journal).
  5. **LIQ.4 — is the ledger writing?** `data/liquidity_ledger/<date>/` should
     exist with non-zero touch counts. It has collected nothing since 08-13.

  **TIER 2 — CHEAP, NO MARKET NEEDED (any evening this week)**
  6. **L1.7 TRENDING: LABEL IT.** 251 symbol-sessions already clear the bar;
     TSLA 08-04 at 99% is the strongest. **This is the only item on the critical
     path to the L2.6 freeze that needs no new data at all.**
  7. **Re-run LIQ.5's retreat probe** once a few post-LIQ.6 sessions exist — its
     NY figures measured a moving target and rungs 2-3 did not previously exist.

  **TIER 3 — REAL DEFECTS, BUT THEY CAN WAIT A SESSION**
  8. **F3** — live-only double-close on a mid-ladder restart. Must close before
     cash; harmless on paper.
  9. **A2.10** — today's tape cannot break a ladder rung.
  10. **CND.8** — the condor has no structural exit. ⚠️ **BLOCKED until enough
      post-LIQ.6 sessions exist**: the 5-of-14 double-stop rate predates condor
      v2 and must be re-measured before anything is designed.

  **⚠️ WHAT NOT TO DO MONDAY: re-tune on the first session.** PART 0's warning
  applies with more force now, not less — most thresholds that shipped today are
  STATED PRIORS (0.50 debit ceiling = the structure's break-even, 0.002 zone =
  the mapper's own dedupe tolerance, 3-deep ladder). **Re-fitting them on the
  first data they produce turns an out-of-sample test into an in-sample one**,
  and restarts the two-week clock a third time.

- **🔴 v4.92 — 2026-08-15 — TODAY'S BAKE RESETS THE MEASUREMENT WINDOW. THE
  AUG 28 EVALUATION NEEDS A DECISION.**

  **THE CONFLICT, STATED PLAINLY.** PART 0 says the two weeks to **Fri Aug 28**
  are *"a MEASUREMENT WINDOW, not a tuning window"* — the point being to judge
  the 08-13 changes on out-of-sample sessions. **Today baked eleven behavioural
  changes to 29/29 boxes** (LIQ.6, SWP.8, F7, F8, F5, LIQ.4+LIQ.7, the audit-2
  fix set, FEED.1/2/3, BFLY.3). Some are defect fixes that had to ship; some —
  BFLY.3's flat ceiling, LIQ.6's pool redefinition, FEED.2's extended hours —
  **change what the fleet trades and what it sees.**

  **✅ RESOLVED SAME DAY — REBASED, NOT MOVED (operator, 2026-08-15):**
  *"8/13 and 8/15 moot, just normalize the marker to 8/15 — 2 weeks is still 2
  weeks."*
  **THE DATE DOES NOT CHANGE.** 2026-08-15 is a Saturday, so the first
  post-bake session is **Mon 08-17** and ten sessions later is **Fri 08-28** —
  exactly two clean trading weeks, entirely on the 08-15 fleet. The anchor was
  already right; only its BASIS was wrong.
  ⚠️ **THE LABEL IS WHAT CHANGES.** Aug 28 evaluates **the 08-15 fleet**, not
  the 08-13 changes in isolation — reporting it as "the 08-13 evaluation" would
  be false, and the two-week discipline exists precisely so a number means what
  its label says.
  ⚠️ AND SESSIONS BEFORE 08-17 ARE A DIFFERENT POPULATION. Do not pool them.

  **WHY THE RESET IS ACCEPTABLE RATHER THAN A SETBACK** (operator): most of what
  shipped were **structural limitations that were not to spec** — a pool
  definition that named a still-forming extreme, an exemption that held a long
  through a bear breakout, a refusal journal that had gone silent, a feed asking
  DXFeed to exclude the tape it needed. Measuring a fleet that was not to spec
  would have measured the defects.

  ⚠️ **AND THE ARCHIVE IS NOW FOUR REGIMES** for anything touching levels or
  sweeps: pre-LIQ.1 · post-LIQ.1 (08-12+) · post-LIQ.6 (08-15 bake) ·
  post-FEED.2 (same bake, but the first session with overnight bars is Mon
  08-17). **Name the window or the numbers are not comparable.**

  ⬜ POINTER CORRECTED: PART 0 directed readers to
  `docs/FLEET_STATE_2026-08-13.md` for "the full account of what changed" — that
  file was DELETED on 08-14 (it violated `docs/README.md`) and folded into
  `docs/HISTORY.md`. **The clock has been pointing at a missing file for two
  days.** Found during the 08-15 scrub, not by anyone following the link.

- **v4.91 — 2026-08-15 — THE DAY'S ACCOUNTING, AND A SCRUB OF WHAT IT CLAIMS.**
  Operator: *"I shouldn't be able to go behind you and find something you missed
  because you just glossed over it."* Every entry from v4.76-v4.90 was re-read
  against the code rather than against memory. **Three superseded claims and one
  misleading convention were found and corrected in place.**

  **🔴 CORRECTION 1 — v4.87's CENTRAL CONCLUSION WAS WRONG.** It states *"there
  is no overnight tape, so Asia and London sections can never build"* and *"the
  data simply does not exist."* FEED.2 proved the opposite hours later: the data
  was always there and the feed was asking DXFeed to exclude it. The entry is
  kept VERBATIM with a correction block, because the reasoning error is the
  lesson — **`ext=0` was read as a property of the DATA when it was a property
  of the REQUEST**, and two further wrong diagnoses followed from it before the
  SDK signature was read.

  **🔴 CORRECTION 2 — v4.88's SCHEDULE WAS CANCELLED, NOT DEFERRED.** The 08:15
  wake / groups-of-five / verify / stop plan is unnecessary: DXFeed streams
  history from `fromTime`, so overnight bars arrive on the 09:10 warm-lead
  connection that already happens. Marked superseded rather than left as
  planned work someone would later try to build.

  **🔴 CORRECTION 3 — the ON-tier item's PREMISE.** *"No overnight tape exists
  historically"* was true only because of `tho=true`. Forward of the FEED.2 bake
  it exists and the tier can be validated on collected data; **nothing before
  that bake can be retro-validated**, since DXFeed history is same-evening only.

  **⚠️ CONVENTION FIXED — THE TEST COUNTS IN TODAY'S ENTRIES ARE NOT
  COMPARABLE.** BFLY.3 records "177 total" and FEED.3 records "141 total" — a
  LATER, SMALLER number, which reads as tests having been lost. They were not:
  each entry counted whatever file subset was run at that moment, and the
  subsets differed. **Verified now on the full named suite: 175 passing.**
  Going forward an entry states the count AND the scope, or states neither.

  **WHAT LANDED TODAY — 24 commits, nothing baked.** Grouped by what it does:
  · **Reporting/tooling (read-only):** `replay_confluence` v2.3→v2.7 (per-symbol
    view, regime grid, named-pool sweeps, streaming, date-range file selection),
    `butterfly_wing_sweep`, `sweep_veto_probe`, `sweep_accept_probe`,
    `retreat_probe`.
  · **Live behaviour:** BFLY.3 flat 0.50 ceiling · LIQ.6 pool redefinition ·
    SWP.8 refusal logs to INFO · F7 breakout exemption · F8 refusal journal ·
    F5 orphan occupancy · LIQ.4 wiring + LIQ.7 zone · the audit-2 fix set
    (mapper v4.1, ledger v1.1, main v6.11, pm v3.3) · FEED.1 maintenance mode ·
    FEED.2 extended hours · FEED.3 pruning off.
  · **`day_trader_pro`:** devtools v1.31 (option 58).

  **THE THREE FINDINGS THAT MATTER MOST, IN ORDER:**
  **1.** L1.7's "tape gaps" were REPORTING gaps — 251 symbol-sessions already
  cleared the TRENDING bar; the row needs LABELING, not calendar time.
  **2.** The overnight tape was excluded by one SDK default (`tho=true`), which
  is why the sections were inert. One parameter closed a question that consumed
  the afternoon.
  **3.** Pruning was never buying anything — a full year is 54 MB per box — and
  it had silently capped an analytical consumer TWICE (PF.2, then LIQ.6).

  **⬜ STILL OPEN, NOT GLOSSED:** A2.10 (today's tape cannot break a ladder
  rung) · CND.8 (the condor has no structural exit; needs the double-stop rate
  re-measured under condor v2 AFTER collection under LIQ.6) · F3 (live-only
  double-close on mid-ladder restart) · the winter section gap at UTC hour 13 ·
  boxes still PULL-only, conductor still requests their data until the S3 PUSH
  and the non-trader wake are automated · retention now unbounded, so disk
  should be watched even though a year is 54 MB.

- **v4.90 — 2026-08-15 — FEED.3: PRUNING IS OFF, AND THE LOCAL STORE STOPS
  PRETENDING TO BE AN ARCHIVE.** `candle_feed` v3.14 · `check_versions` · 4 tests
  (141 total).

  **THE BOUND WAS SIZED FOR THE LIVE LOOP AND KEPT SILENTLY CONSTRAINING
  ANALYTICAL CONSUMERS THAT ARRIVED LATER — twice now.** PF.2 found the boxes
  held 84 daily bars while the engine was handed 10 (*"the history was never
  missing — the frame was"*), and LIQ.6's 10-day section lookback landed on
  **exactly** the 240-row 1h ceiling with zero margin.

  **AND IT WAS NEVER BUYING ANYTHING.** Measured: a FULL YEAR of every interval
  with extended hours is **54 MB per box**, on an 8 GB root. Ten days is 1.5 MB.
  **The pruner was tidiness, not capacity.**

  **THE DIVISION OF LABOUR (operator's):** boxes retain what they collect —
  enough to keep the engines warm — **S3 is the archive**, the conductor fans
  out in groups of 5, and **weekend reporting reads the bucket** rather than
  requiring any box to be awake. That is strictly better than today, where
  reports depend on the fleet having pushed to control first.
  ⚠️ RECOMMENDATION HELD: keep the CONTINUOUS push and make the Friday fan-out a
  VERIFY-AND-BACKFILL sweep. If the push moves to Friday-only, a box that dies
  on Wednesday takes the week with it and the local store is the only copy.

  ⚠️ `OT_PRUNE_KEEP_ROWS=<n>` re-enables a flat cap — kept as a mechanism rather
  than deleted so reversing it is one env var, not a code change.
  ⚠️ **THE POISON PURGE IS UNTOUCHED.** It deletes BAD rows (non-positive
  prices, 2038-stamped DXFeed rollover junk that would sort to the top of a DESC
  window and masquerade as the newest bar), not OLD ones.

  **🔴 AND IT CAUGHT A LIVE BUG IN FEED.2.** The prune loop still unpacked a
  **3-tuple** after `self.subs` widened to four. It would have raised at runtime
  after `PRUNE_EVERY_S` inside the flush path, **on a box in production** —
  `--once` exits before the first prune and no test touched it. **Found by
  accident while reading the call site, not by looking.** A test now asserts
  every consumer matches the declared arity, so widening it again cannot leave a
  straggler.

  ⬜ CV.1 PRECEDENT APPLIED: `check_versions` pinned the literal string
  `addendum v3.11`, which went red on a legitimate bump. **A canary that fails on
  every version change teaches the operator to ignore a red run.** Replaced with
  BEHAVIOUR canaries on the extended-hours sub and the maintenance gate.

- **🔴 v4.89 — 2026-08-15 — FEED.2: THE OVERNIGHT TAPE WAS NEVER UNAVAILABLE.
  WE WERE ASKING DXFEED TO EXCLUDE IT.** `candle_feed` v3.13 · `main` · 7 tests.
  **THIS CLOSES THE OFF-HOURS LIQUIDITY QUESTION.**

  `TastytradeStreamer.subscribe_candle` takes **`extended_trading_hours: bool =
  False`**, and when it is False the SDK appends **`tho=true`** —
  trading-hours-only — to the DXFeed symbol: `QQQ{=1h,tho=true}`. **Every
  subscription this feed has ever made carried it, by taking the default.**

  **⚠️ ONE DEFAULT PRODUCED EVERY SYMPTOM CHASED TODAY:** `ext=0` on 28 of 29
  boxes · a 1h store of 252 bars (36 sessions x 7 = RTH only) · LIQ.6's Asia and
  London sections with nothing to build from · and three successive wrong
  diagnoses of mine — that it was the session guard, then that it was a
  warehouse gap, then that it was a feed-subscription tier. **It was none of
  them.** A test now asserts the SDK's own default so a future version change
  surfaces here rather than silently reshaping the fleet.

  **A SEPARATE STREAM, NOT A FLAG ON `1h`.** Plain 1h is read by
  `structure_analyzer` (swings + S/R), by `pitchfork` and its observer, and by
  `entry_snapshot`. Flipping it in place would have rebuilt all of them on 24h
  bars with nothing announcing it — **the pitchfork is a v4.0 milestone and its
  forks would have changed shape overnight.** The extended stream lands under
  its own store symbol `<SYM>_EXT`; no existing consumer moves.
  The named-level frame prefers `_EXT` and **falls back LOUDLY** to RTH-only 1h
  on a box that has not collected yet — which is exactly today's behaviour, not
  a regression, but it says so rather than leaving "the sections are inert here"
  invisible again.

  **🔵 NO AM/PM COLLECTOR IS NEEDED — the 08:15 pass is cancelled.**
  `fromTime` is `now - 16 days` and DXFeed streams HISTORY from there, so
  without `tho=true` **last night's Asia and London arrive on the 09:10
  warm-lead connection that already happens.** No wake in fives, no batches, no
  conductor change, no extra instance-hours. The whole schedule designed earlier
  today is unnecessary.

  **⚠️ RETENTION IS EXACTLY AT THE EDGE.** The pruner keeps 240 1h rows =
  **10.0 days** of 24h tape against `SECTION_LOOKBACK_DAYS = 10`. It fits with
  **zero margin** — a missed night eats straight into the ladder's depth. Raise
  the 1h prune ceiling before relying on the full lookback.

  ⬜ FEED.1's maintenance flag (option 58) is **inert** given this: it guards
  against `--once` at an awkward hour, and with no capture pass there is no such
  caller. Kept for possible repurposing, per operator.

- **v4.88 — 2026-08-15 — FEED.1: A MAINTENANCE WINDOW. `candle_feed` v3.12 ·
  10 tests (138 total).** Operator's requirement: *"a dedicated maintenance
  window where I can bring up all 29 and make fleet updates without involving
  the feed or using api resources."*

  **WHY IT COULD NOT BE A CLOCK RULE.** `_idle_outside_session` already said the
  right thing — *"THE DISTINCTION IS PURPOSE, NOT TIME"* — but had only TWO
  purposes: service and one-shot. `--once` was therefore allowed at ANY hour,
  which is correct for the EOD pull and wrong for exactly what v3.9 protects
  against. **And the 08:15 overnight capture pass falls on the same hours as a
  maintenance window and wants the opposite behaviour**, so no time-based gate
  can separate them.

  **MODES:** `service` (default, byte-for-byte the old behaviour) · `capture`
  (gates as service; the name makes a capture wake distinguishable in the logs
  and gives a future window argument somewhere to live) · `maintenance` (HARD
  OFF, `--once` included).

  **⚠️ A SENTINEL FILE, NOT ONLY ENV.** `Environment=` in the unit is read ONCE
  AT IMPORT, so flipping a RUNNING feed would need a restart — **and that
  restart window is precisely when the box is on the wire during the
  maintenance it should be excused from.** `data/FEED_MAINTENANCE` is checked on
  every gate evaluation: touch to enter, rm to leave, nothing restarts, no race.

  **⚠️ IT FAILS *OPEN* TO service — the one place in this repo that
  deliberately does.** A box that cannot stat the flag keeps FEEDING, because
  the costs are not symmetric: a stray socket during maintenance is recoverable
  in seconds, while a missed session is **PERMANENT** (DXFeed history is
  same-evening only — that is how 2026-08-03 and 08-04 were lost for good).

  **⚠️ AND IT ANNOUNCES ITSELF AT WARNING**, naming the mode and stating the
  tape is NOT being collected. The 08-03 loss was this same gate firing
  SILENTLY at INFO — `Feed idle - outside RTH`, four times, then `0 bars`, then
  fourteen 38-byte header-only CSVs, and nothing raised.

  🔴 **THE SCHEDULE BELOW WAS CANCELLED BY FEED.2 (v4.89) HOURS AFTER IT WAS
  AGREED.** DXFeed streams HISTORY from `fromTime`, so with `tho=true` removed
  the overnight bars arrive on the 09:10 warm-lead connection that already
  happens — **no wake, no batches, no conductor change.** Kept for the record
  because the reasoning about session boundaries stands and would apply again if
  a capture pass is ever needed for another reason.
  ⚠️ AND IT LEAVES FEED.1 (the maintenance flag, devtools 58) INERT: it guards
  against `--once` firing at an awkward hour, and with no capture pass there is
  no such caller. Operator's call: kept for possible repurposing.

  **⬜ THE SCHEDULE THIS SERVES (SUPERSEDED — see above).** 08:15 wake in groups
  of 5 → pull overnight → verify → stop, capturing **Asia complete** (closed by
  08:15) and London through 08:15; **09:15** the 15 traders wake into the warm
  lead and cover 08:15-09:30 as ordinary history; **EOD** the existing pass.
  ⚠️ **BLOCKER FOR THE 08:15 PASS:** `pull_today_ohlc.sh` calls `candle_feed
  --once`, which pulls history **from 09:30** by construction — a pre-open run
  would ask for a window that has not started and return the same 38-byte
  header-only files. `--once` must take an explicit window first.
  ⚠️ AND `eod_backfill` v1.2 ALREADY IMPLEMENTS the wake→pull→verify→stop loop
  at batch 5 with a capacity guard and `_drain_verify()` over SSH. **Do not
  build a second one.** Note its deliberate choice: `_drain_verify` is
  WARN-NEVER-STOP (a box left up blocks the batch loop against the stream cap),
  so verification currently REPORTS rather than GATES — a decision to revisit
  against the operator's "verified, then next box starts".

- **v4.87 — 2026-08-15 — THE THREE AUDIT-2 UNKNOWNS, MEASURED ON 29/29 BOXES.**
  Read-only, via the two instruments from the audit handoff.

  **🔴 `ext=0` ON 28 OF 29 SYMBOLS — THERE IS NO OVERNIGHT TAPE, SO ASIA AND
  LONDON SECTIONS CAN NEVER BUILD.** Only SPX carries extended-hours 5m bars
  (21 of 401). The 1h store is RTH-only too: **252 bars over a 50.2-day span =
  36 trading days x 7 bars/day.**
  **LIQ.6's London restoration is INERT everywhere except SPX.** Rule 1 said
  *"only the overlapping tail was ever the problem; the pre-RTH London extreme
  is a real level and is back"* — there are no pre-RTH bars to build it from.
  **In practice the ladder is three prior NY sessions**, and the section
  machinery reduces to one section on 28 boxes.
  🔴 **SUPERSEDED THE SAME EVENING BY FEED.2 (v4.89) — THIS DIAGNOSIS WAS
  WRONG.** The measurement above is accurate; the CONCLUSION drawn from it was
  not. "The data simply does not exist" is false: `subscribe_candle` takes
  `extended_trading_hours=False` by DEFAULT and the SDK then appends `tho=true`
  to the symbol, so **the feed was explicitly asking DXFeed to exclude the
  overnight bars.** They were always available.
  ⚠️ KEPT VERBATIM RATHER THAN REWRITTEN, because the reasoning error is the
  lesson: `ext=0` was read as a property of the DATA when it was a property of
  the REQUEST. Two further wrong diagnoses followed the same evening — that the
  session guard was responsible, then that it was a warehouse gap — before the
  SDK signature was actually read. **Measure, then check what you are measuring,
  before concluding what it means.**
  ⬜ The "source overnight tape or declare sections SPX-only" decision it poses
  is therefore MOOT — FEED.2 sources it with one parameter.

  **🔵 DEPTH CONFIRMED — A2.1'S FIX IS SUFFICIENT.** 1h reads 238-252 rows
  across ~49-50 days (XOM 238, SPX 241 sit right on the 240 prune ceiling,
  confirming the r2 correction). **~34-36 RTH sessions against a 10-day
  lookback** — the truncation that made LIQ.6's ladder read a rolling 8.3-hour
  window is genuinely gone.

  **🔵 A2.4'S LEAK IS NOT CURRENTLY OCCURRING. `gt75=0` on all 29 boxes**,
  `winmax` 15.0-17.1s (SPX worst). The mechanism needed ticks over ~75s so two
  1m bars close between feeds; at a 15s cadence **four ticks fit inside every 1m
  bar.** The gap-safe `feed_frame` fix is still correct and stays — it makes the
  ledger robust to a stall — but **nothing should read its presence as evidence
  of a problem.**
  ⚠️ HONEST LIMIT, from the instrument's own author: heartbeats land every 20
  ticks, so these are WINDOW MEANS and `gt75` is a LOWER BOUND. A single 75s
  tick would still lift its window to ~18s, and nothing exceeds 17.1 — so the
  bound is tight here, but per-tick precision only arrives after the bake, from
  the ledger's own `last_bar_ts` against write cadence.

  **🔵 `late16ET=0` EVERYWHERE — no box ticks past 16:00 ET.** So A2.5's
  secondary finding (winter bars 20:00-21:00 UTC belonging to no section) has no
  bars to lose. The winter gap at UTC hour 13 recorded in v4.86 is likewise
  pre-market on tape that does not exist. **Both are latent, not live.**

- **v4.86 — 2026-08-15 — THE A2.3 HYDRATE MADE THE LEDGER TESTS STATEFUL, AND
  THE LEDGER WAS WRITING INTO THE REPO.** Caught reviewing the audit-2 fix set
  before landing it; the fix set itself is otherwise verified and taken as-is.

  **🔴 `data/liquidity_ledger/` WAS NOT IN `.gitignore`.** The ledger writes
  `<root>/<date>/<sym>.json` on **every closed bar** once live, and the delivery's
  own deploy line runs `git add -A`. **Live fleet output would have been
  committed into the repo** — the MANIFEST.txt / trades.db precedent exactly,
  and the standing rule that delivery scaffolding must clean itself up. Now
  ignored.

  **🔴 AND THE TESTS SHARED STATE WITH THEIR OWN HISTORY.** A2.3's fix makes
  `reset_for_session` READ BACK that file — correct in production, that is the
  whole point of the restart fix — but the tests wrote to the real path, so runs
  ACCUMULATED: `test_the_zone_cuts_BOTH_ways` reported **`holds == 3` from a
  single bar** after three invocations stacked up. A test that inherits its own
  previous run proves nothing.
  **FIX:** `_OUT_ROOT` is now env-overridable (`OT_LEDGER_ROOT`), and an autouse
  fixture points every ledger test at a FRESH `tmp_path`. Production path
  unchanged. Verified: the suite passes twice consecutively with identical
  counts, and a clean run writes nothing under `data/`.

  ⚠️ **DESIGN NOTE, HELD NOT BLOCKED — a winter coverage gap.** A2.5's DST fix
  derives NY hours per date (EDT 13-20, EST 14-21) and is correct. But
  `SECTIONS_FIXED` keeps London at 8-13, so in EST **UTC hour 13 (08:00-09:00
  ET) belongs to NO section** — the "contiguous" property in LIQ.6 rule 1 holds
  in summer only. No pool is lost (that hour is pre-market and is not a session
  extreme by any definition), but a bar in an unassigned hour **cannot
  contribute to the ladder's break-exclusion**, so price trading through a rung
  during it cannot invalidate that rung. Related to A2.10, already parked.
  Recorded so it is a decision rather than a discovery in November.

  ⬜ r1 of the fix set was WITHDRAWN by its author and must never be extracted;
  r2 differs only in a `main.py` comment and a BACKLOG depth claim. The
  correction: `BACKFILL_DAYS` requests 16 days of 1h ONCE, but `candle_feed`'s
  pruner trims 1h to `max(50,60)*PRUNE_FACTOR = 240` rows every 300s, so steady
  state is ~240h — **~10 days of 24h tape.** The lookback is satisfied, for a
  different reason than r1 stated.

- **🔴 v4.85 — 2026-08-15 — ADVERSARIAL AUDIT #2: THE UNBAKED QUEUE, AUDITED
  AND FIXED BEFORE IT COULD BAKE.** `liquidity_mapper` v4.1 · `liquidity_ledger`
  v1.1 · `main` v6.11 · `position_manager` v3.3 · `iron_condor_strategy` v-a2 ·
  `check_versions` v4.53 · 17 executing tests (suite 625 green).

  Same treatment as audit #1, applied to `dad8662..89cbaf6` before Monday's
  bake. Full report + repros shipped separately
  (`ADVERSARIAL_AUDIT_2_FINDINGS_2026-08-15.md`, `repro_liq.py`). Verdicts:
  **LIQ.6 and LIQ.4 carried the serious defects; one of the three audit fixes
  (F5) never reached runtime; F7, F8, SWP.8 clean, traced end to end.**

  **🔴 A2.1 — LIQ.6's 10-DAY LOOKBACK RAN ON AN 8-HOUR FRAME (reproduced).**
  `df_5m` is capped at 100 bars; truncated sections were admitted as closed
  pools at WRONG prices (true Asia High 101.10 emitted as 97.10) and rung
  prices MUTATED intraday as the window slid — the self-rewriting level, back
  through the input. **Fix, two independent layers:** (a) `analyze()` takes
  `named_df` — a deep 1h store frame `main._named_level_frame()` supplies
  (300s TTL, PF.2 precedent: the history was never missing, the frame was;
  fails soft to the live frame). **DEPTH TRUTH, corrected in r2 while
  building the census command:** BACKFILL_DAYS requests 16 days of 1h ONCE,
  but candle_feed's pruner trims 1h to max(50,60)×PRUNE_FACTOR = **240 rows
  every 300s** — steady state is ~10 days of 24h tape / ~34 RTH sessions, so
  the 16-day backfill is deleted down to 240 within five minutes of arriving
  (⬜ operator call whether to align BACKFILL_DAYS or raise the prune
  ceiling; the lookback itself is satisfied). The constant asks for 264 —
  harmless headroom, fetch returns what exists — and with the earliest
  partial day skipped by the truncation guard the ladder effectively sees
  ~9 complete days + today; (b) a section
  whose START the frame does not reach is **LEFT-TRUNCATED and skipped** — on
  ANY input depth, so replay/tests passing their own tape are equally honest.

  **🔴 A2.2 — THE F5 FIX WAS DEAD CODE.** Its only call site sits inside
  `attempt_new_entry`, which only runs when `has_open_position()` is False —
  and that falls back to the SAME `get_open_trades()`. With a leg open the
  site was unreachable; when reached, the count was by construction zero, so
  the occupancy OR could never fire and **the orphan WARNING could never
  fire.** The v4.83 danger model (TC.6 second spread) was impossible for the
  same reason — corrected in place above. **Fix: the announcement moved to the
  manage branch** — the only code that RUNS with a leg open — via
  `pos_mgr.open_condor_leg_count()` (new, counts records already in hand);
  the checker is now side-effect-free belt-and-braces; the once-latch re-arms
  daily. **§21 hop-0, repeated within 24h of being written: the F5 tests
  asserted source text and called the announcer directly — reachability was
  never executed. The new suite executes it.**

  **🔴 A2.3 — EVERY BAKE WIPED THE LEDGER'S DAY (reproduced).** `write()` had
  NO READER: a restart reseeded the same date from zero and the next write
  overwrote the good file with zeros — §22 verbatim, in the commit whose
  purpose is "the running record cannot be recovered later." **Fix:
  `reset_for_session` hydrates the same-date JSON first** (schema and
  touch-tol guarded — counts taken under a different zone start clean,
  loudly), then merges seeds through `add_level`.

  **🔴 A2.4 — THE LEDGER SILENTLY SKIPPED BARS (reproduced).** `iloc[-2]`
  behind a one-stamp guard drops closed bars on any tick slower than ~75s —
  and slow ticks correlate with busy tape, so the undercount landed on the
  bars most likely to test levels. **Fix: bar selection moved INTO the ledger
  — `feed_frame(df_1m)`** walks every closed session bar (≥09:30 ET, session
  date) newer than `last_bar_ts`, which is persisted, so the A2.3 hydrate
  also recovers the bake gap from the 60-bar frame.

  **🟠 A2.5 — WINTER DST (reproduced):** fixed 13-20 UTC NY section would have
  admitted TODAY'S FORMING RTH extreme as a pool from 3:00pm ET every EST day
  starting 2026-11-01, and left 20-21 UTC winter bars in no section. NY hours
  now derive from the date's ET offset via ZoneInfo (13-20 EDT / 14-21 EST) —
  same lesson as the hardcoded −4 offset, caught before Nov 1 this time.
  Still-forming is now an instant test (tape must reach the section's end).

  **🟠 A2.6:** `NAMED_POOLS_INCLUDE_SESSIONS` was a DEAD KNOB — the ladder
  never read it, while `test_session_pools_are_off_by_default` stayed green
  asserting the opposite of production. Removed; the two flag tests replaced
  by behavior asserts (rungs on by doctrine; the LIQ.1 protection — no
  still-forming section is ever a pool — is executed against the real mapper).
  **🟠 A2.7 (reproduced):** more-extreme-wins REPLACED the colliding name, so
  PDH could vanish when a rung inside the 0.2% zone out-priced it. The merge
  is now symmetric: a collision never deletes a fact in either direction.
  **🟡 A2.8:** the candle-count fallback built OLD-definition session pools and
  exceptions routed to it at debug — a per-tick regime coin toss. Fallback is
  PDH/PDL-only now; the exception warns once per process.
  **🟡 A2.9:** an empty first-tick seed latched a zero-level ledger all day —
  seeding now retries until the mapper produces named pools; wiring routes
  through `get_ledger()` (one singleton, not two).

  **BORN-RED, VERIFIED:** the new suite `tests/test_audit2_fixes.py` runs
  **17/17 on the fixed tree and 12-failed against pristine `89cbaf6`** (the 5
  HEAD-passes are deliberate pins of unchanged behavior and say so). Full
  suite: **625 passed** on every collecting test file, failures identical to
  HEAD's pre-existing sandbox-env set; `test_no_undefined_names` green with
  real pyflakes.

  **HYGIENE FOUND WHILE PACKAGING, fixed in this delivery:**
  · **committed merge-conflict markers in THIS FILE** (`<<<<<<<`/`>>>>>>>`
    around v4.84-v4.82, the collision v4.83 itself describes) — resolved,
    upstream side kept, the stashed duplicate F5 entry dropped;
  · **CV.2**: check_versions' "v1.6 header current" canary pinned a VERSION
    STRING and went red at HEAD when continuation_strategy legitimately moved
    to v1.7 — removed, not silently (CV.1 precedent); its behavior canaries
    remain;
  · mapper title had drifted (v3.3 while LIQ.6-era) — the exact failure class
    of the 07-23 sweep; now v4.1 with both entries;
  · new A2 canaries are BEHAVIOR greps incl. an ABSENCE check on the dead
    knob (assignment pattern, so changelog mentions stay legal — SWP.1).

  **⬜ OPERATOR CALLS, deliberately NOT fixed:** A2.10 — today's tape cannot
  BREAK a ladder rung (forming sections are excluded from break detection),
  so an accepted-through level stays named all day; interacts with "an
  untouched extreme is where the stops are." UNKNOWNS worth one option-14
  each: per-symbol overnight-bar presence (sets the old frame's wall-clock
  reach; mechanism unaffected), live tick-latency distribution (A2.4's real
  leak rate), whether any box ticks past 20:00 UTC in summer.

  **ARCHIVE REGIME:** A2.1/A2.5 change what a pool IS **again** — shipped in
  the SAME pre-collection window as LIQ.6, so the archive gains ONE new
  regime, not two. A2.3/A2.4 land before the ledger's first collecting
  session, so week one is not restart-truncated in ways indistinguishable
  from market structure. Boxes need nothing installed: stdlib `zoneinfo`
  reads the system tz database (sandbox needed `tzdata` from pip; Ubuntu
  boxes carry `/usr/share/zoneinfo`).

- **v4.84 — 2026-08-15 — LIQ.4 WIRED AT LAST, AND LIQ.7 ALIGNS ITS ZONE.**
  `main` · `analysis/liquidity_ledger.py` · 5 tests.

  **THE LEDGER HAS BEEN BUILT, TESTED AND COLLECTING NOTHING SINCE 08-13.**
  Every unwired session is level history that CANNOT be recovered — the tape
  survives, but the running touch/hold/breach record does not, and rebuilding it
  later means re-deriving levels the mapper found live.

  **🔵 AND IT ALREADY IMPLEMENTS THIS MORNING'S RETREAT RULE, VERBATIM** — wick
  reaches = touch, close beyond = breach, close back on the origin side = hold,
  a bar that never reaches does nothing. Written 08-13, before the conversation
  that re-derived it. **Checking before building saved writing it twice.**

  **🔴 LIQ.7 — THE TOLERANCE WAS OFF BY 10x.** The ledger shipped at **0.0002
  (2bp)** while `liquidity_mapper._add_named_pool` uses **`within_pct(...,
  0.002)` (20bp)** to decide two prices are the SAME LEVEL. On a $580
  underlying 2bp is **12 CENTS** — a clean approach that reversed just short of
  the level did not register as a test at all, so **the most-defended levels
  looked untested**, which is exactly what the sizing rule exists to reward.
  Operator: *"Reach within a small margin of error is good enough. A level is a
  ZONE, not a fixed number."* Now 0.002 — **one definition of a zone.**
  ⚠️ THE ZONE CUTS BOTH WAYS: a close slightly beyond the nominal price is still
  INSIDE the band and counts as a HOLD. Widening only the touch test would have
  counted defended levels as broken.

  **WIRING DETAILS THAT MATTER:**
  · **CLOSED BARS ONLY, ONCE EACH.** `df_1m`'s last row is the FORMING bar on
    most ticks — feeding it counts a wick that has not finished printing and a
    close that is not a close, and re-counts the same bar on every tick as it
    forms. `df_1m.iloc[-2]` plus a `_LEDGER_LAST_BAR` guard.
  · **SEEDS COME FROM THE MAPPER, never re-derived.** LIQ.6 changed what a named
    pool IS (sections, closed-only, a 3-deep ladder), so the ledger takes
    whatever the mapper currently names — rung suffixes included — rather than
    holding a second opinion about levels (WORKING_AGREEMENT 7). A test asserts
    it contains no level names of its own.
  · Re-seeds per session date; fails silently to a debug line so a ledger fault
    can never stop a tick.

- **🔴 v4.83 — 2026-08-15 — AUDIT F5 FIXED: A RESTART ORPHANS THE CONDOR
  STRUCTURE.** `main` v6.10 · `iron_condor_strategy` · 3 tests (126 total).

  **`IronCondorStrategy._plan` IS PROCESS-LOCAL.** Restart with leg 1 filled and
  leg 2 pending and the plan is GONE — **and with it leg 2's TRIGGER PRICE,
  which is in no column.** The structure can never complete. **A restart happens
  on every bake**, so this is not an edge case.

  **WHAT IS *NOT* BROKEN, and it shapes the fix:** the orphaned leg itself is
  fine. `_condor_sibling_open()` reads the DB, returns False, and CND.7 manages
  it correctly as a STANDALONE vertical with the ratchet it earns.

  **WHAT WAS BROKEN IS DEFERRAL.** `has_active_plan` goes False, so **TC.6 stops
  standing down and can open a SECOND credit spread on the same underlying**
  while the orphan is open — two credit verticals on one symbol, sized and
  managed as neither.
  **⚠️ CORRECTED v4.85 (audit A2.2): this scenario was ALREADY IMPOSSIBLE** —
  TC.6 only dispatches inside `attempt_new_entry`, which only runs when
  `has_open_position()` is False, and that reads the SAME `get_open_trades()`.
  The guard below is retained as belt-and-braces but it guarded a closed door,
  and the orphan WARNING wired here could never fire. See v4.85.
  **FIX: the symbol stays OCCUPIED while any condor leg is open**, derived from
  the persisted fields `_condor_sibling_open` already trusts (`is_condor_leg`,
  `status='open'`) rather than from a plan that did not survive. **Same
  principle as `structure.py`: derive from what persists.**
  ⚠️ FAILS CLOSED — any error treats the symbol as occupied. A missed trade
  costs less than an unmanaged pair.

  **AND THE ORPHAN ANNOUNCES ITSELF, ONCE.** Previously it sat there looking
  like a standalone vertical and the only signal was a condor that never got its
  second side. **Silence here is the same failure as VEL.1 and the AFD.1 slot
  bug — a state nobody could distinguish from normal.**

  ⚠️ TWO PROCESS CATCHES. A test of mine targeted the WRONG `except` — the
  function has an inner guard around the warning and an outer one that decides
  the return; a substring search found the inner one and proved nothing. Now
  walks the AST. **And this delivery nearly overwrote F8**: my sandbox pulled
  BEFORE F8 landed, so restoring stashed work wiped the pre-dispatch journal
  from `main.py` and the BACKLOG collided on v4.82. Caught by checking both
  markers were present before packaging — **WORKING_AGREEMENT 24, verify the
  edit landed, applied to a MERGE rather than an edit.**

- **v4.82 — 2026-08-15 — AUDIT F8 FIXED: THE REFUSAL JOURNAL MOVED WITH THE
  GATE.** `main` v6.10 · 3 tests (126 total).

  **FIXING THE SLOT BUG KILLED THE CUTOFF'S OWN TELEMETRY.** Moving AFD.1 to
  PRE-DISPATCH — so a blocked debit strategy could no longer consume the
  afternoon slot — made the POST-SELECTION journal structurally unreachable for
  ORB/Continuation/Sweep. They are SKIPPED, so no signal is ever formed to carry
  a `gate_block:afternoon_debit` disposition. **The telemetry went to zero the
  moment the bug was fixed**, silently, and that is exactly the class the repo's
  own gate-ordering reasoning warns about.

  Now journaled PER STRATEGY at the pre-dispatch gate.
  **⚠️ HONEST TRADEOFF, RECORDED RATHER THAN BURIED:** there is no SIGNAL at
  pre-dispatch, so the record carries **no contract, strike or score**. It
  answers *"the cutoff fired and for whom"*, not *"what would have traded"* —
  and marks itself `stage=pre_dispatch` so nobody reads it as the richer thing.
  A test asserts it does NOT call `signal_ctx()`, because fabricating signal
  context it does not have would be worse than the gap.
  The post-selection journal is **RETAINED as defence in depth** for any future
  strategy added to `DEBIT_DIRECTIONAL_STRATEGIES` without a pre-gate — that one
  still gets the full record.

- **🔴 v4.81 — 2026-08-15 — AUDIT F7 FIXED: THE BREAKOUT EXEMPTION WAS
  ASYMMETRIC AND DIRECTION-BLIND.** `exit_engine` v4.22 · 6 tests (112 total).

  **v4.19 SCOPED THE EXEMPTION TO `_breakout` RECORDS TO AVOID OVER-REACHING,
  AND CREATED A WORSE PROBLEM.** A STANDALONE or HANDOFF continuation riding
  TRENDING_BULL that **accelerated into BREAKOUT_VOLATILE — the strongest tape
  in its own direction — was closed as a `regime_flip`**, while a breakout
  record survived the IDENTICAL TAPE. Same market, opposite decision, decided by
  setup_type alone.

  **⚠️ AND THE OTHER HALF IS WORSE: BREAKOUT_VOLATILE CARRIES NO DIRECTION.**
  The label-only test meant **a LONG survived a violent move DOWN** as long as
  the record was `_breakout`. v4.19's own comment already said a breakout
  continuation must live or die on the TREND VOTE — but the code tested the
  LABEL, which cannot supply direction.

  **FIX: ANY continuation survives BREAKOUT_VOLATILE when the TREND VOTE
  AGREES; none survives when it does not.** `trend` was already a parameter on
  `_evaluate_continuation`. setup_type no longer gates anything here.
  ⚠️ FAILS CLOSED: an absent vote yields `""`, which agrees with no direction,
  so the trade exits. **A missing input is never evidence the thesis survives.**

  ⚠️ THREE EXISTING TESTS ASSERTED THE DEFECT and had to be rewritten — they
  pinned "only `_breakout` gains the exemption", which WAS the bug rather than
  the contract. **And the rewritten mirror was caught being MORE PERMISSIVE than
  the engine**: it defaulted an EMPTY vote to the trade's own direction, where
  the engine leaves it empty and fails closed. Only `None` defaults now.

- **v4.80 — 2026-08-15 — SWP.8: SWEEP REFUSAL PATHS PROMOTED TO INFO.**
  `strategy/sweep_reversal_strategy.py`. Log-only, no gate or threshold change,
  freeze-safe. Closes a `[DESK]` item that had been open since 08-11.

  **ALL 10 `logger.debug` CALLS WERE REASONS A TRADE DID NOT HAPPEN**, and the
  fleet runs at `LOG_LEVEL="INFO"` — so **none of them existed in any log anyone
  could read.** Verified by AST after the change: debug=0, info=15, warning=2.

  **⚠️ IT COST A WHOLE MORNING TO PROVE THE POINT.** The 2026-08-15 sweep
  investigation had to proceed by ELIMINATION-BY-READING THE SOURCE, because the
  strategy never said why it declined. The BUTTERFLY logs its gates at INFO, and
  that same morning its blocker was found in ONE GREP — `GEX not PINNING`
  dominating 20-50x, then the discount gate rejecting 39/26. **Same class of
  question, two very different costs.**

  ⚠️ VOLUME IS THE POINT, NOT A SIDE EFFECT: these fire per-tick on a refused
  sweep, so a symbol that never qualifies prints steadily. **A silent refusal is
  indistinguishable from a strategy that was never evaluated** — the exact
  ambiguity that made VEL.1 (a mechanism inert for five weeks), the AFD.1 slot
  bug (a gate consuming a slot it could not use) and this one all cost hours.

- **🔴 v4.79 — 2026-08-15 — LIQ.6: A WHOLESALE CHANGE TO WHAT A NAMED POOL IS.**
  `analysis/liquidity_mapper.py`. **Everything prior was correct FOR ITS TIME
  and is incorrect under the clearer rules** (operator).

  **1. SECTIONS ARE NON-OVERLAPPING AND CONTIGUOUS** in UTC — Asia 00-08,
  London 08-13, NY 13-20. A bar belongs to exactly one. The old windows
  OVERLAPPED (Asia 00-08, London 07-16, NY 13-22), which is how "London High"
  could be set by a price RTH traded seconds ago — and why LIQ.1 removed London
  wholesale. **Only the overlapping TAIL was ever the problem**, so the pre-RTH
  London extreme is a real level and is back.

  **2. A SECTION IS A POOL ONCE IT IS CLOSED.** Operator: *"The current day's
  levels must be excluded BY DEFINITION because they are still forming.
  Exception: overnight low/high are still today, but an EARLIER session &
  therefore valid."* The test is COMPLETED vs STILL FORMING, never the calendar
  date. **Today's RTH is never a pool** — it is `session_high`/`session_low`,
  already tracked by the not-exceeded filter. The old code named today's forming
  RTH extreme "NY High": a level that rewrote itself on every print.

  **3. `NY High/Low` IS SESSION-TYPE, NOT DATE-RELATIVE.** Operator: *"If one of
  the last extremes was NY H/L but it was 5 days ago, then it's not PDH/PDL — it
  accurately IS NY H/L."* PDH/PDL means literally yesterday; an untouched RTH
  extreme is where the stops are regardless of when it formed.

  **4. A LADDER THREE DEEP, AND A BROKEN LEVEL IS NOT A POOL.** Operator: *"More
  extreme means the less extreme level was already invalidated"* and *"the
  mapper should run 3 levels deep: most recent h/l, next most, 3rd most."* If a
  later section printed a higher high, price went THROUGH the earlier one and
  those stops are gone. Rung 1 is the next liquidity; rungs 2-3 are where price
  runs if it takes rung 1.
  ⚠️ THE RUNG IS ALWAYS IN THE NAME, and a collision MERGES it rather than
  discarding it. PDH/PDL is added before the ladder and yesterday's full-day
  extreme is usually the SAME PRINT as yesterday's RTH extreme, so the collision
  is the norm — it now reads **`PDH (R2)`**, keeping both facts. Without the
  merge the ladder read `London High (R1) / PDH / NY High (R3)` with rung 2
  invisible.
  Verified on planted tape: highs **105 (R1) -> 108 (R2) -> 110 (R3)**, lows
  **95 -> 92 -> 90**, today's forming RTH excluded, and 08-13's broken Asia/
  London extremes correctly absent.

  **⚠️ THIS INVALIDATES TODAY'S EARLIER READS AS BASELINES.** Every sweep in the
  archive was scored against the OLD pool definition, so the accept-veto rate
  (64.5%), the retreat distribution and the SWEEP tape-gap conclusions describe
  a mapper that no longer exists. **The archive is now a THIRD regime** (pre-
  LIQ.1, post-LIQ.1, post-LIQ.6).
  **SEQUENCING, agreed: ship the mapper, COLLECT, then revisit the sweep setup
  for edge.** Changing what a level IS and when a sweep FIRES in the same window
  would make neither attributable. The retreat probe (LIQ.5) must be re-run
  after collection — its NY figures measured a moving target, and rungs 2-3 did
  not previously exist.

- **v4.78 — 2026-08-15 (Sat) — L1.7's "TAPE GAPS" WERE REPORTING GAPS, AND THE
  SWEEP SETUP IS CONFIRMED TOO LATE TO TRADE.** `replay_confluence` v2.7 ·
  `sweep_veto_probe` · `sweep_accept_probe`.

  **🔵 TRENDING IS CLOSEABLE AND HAS BEEN ALL ALONG — 251 SYMBOL-SESSIONS
  CLEARED THE BAR.** Every regime-validation report (42-47) aggregates ~29
  symbol-sessions, but L1.7's acceptance is written PER SYMBOL-DAY — and
  blending symbols GUARANTEES no regime dominates, because different symbols are
  in different regimes on the same day. A perfect trend day on QQQ was averaged
  against 28 others. **The qualifying days were on disk the whole time.**
  Strongest: TSLA 08-04 **99%**, AVGO 08-14 97%, SPX 08-04 97%, ORCL 08-10 97%,
  GLD 07-21 97%. **What remains is LABELING, not calendar time.**
  Operator's simplification made it cheap: `gather_paths` already returns ONE
  FILE PER SYMBOL, so `--symbol` filters the PATH LIST (~29x faster) instead of
  post-filtering records.
  ⚠️ SIDE FINDING: QQQ and SPX sit in RANG far more than the single names —
  **the indices chop while individual stocks trend.** Bears on symbol selection
  and was structurally invisible in an aggregate.

  **🔴 THE SWEEP SETUP IS CONFIRMED 5-20 MINUTES AFTER THE MOVE.** The mapper
  runs on **5m/15m — never 1m** (`main.py:781`). `SWEEP_REJECTION_CANDLES=3` on
  5m is a **15-MINUTE** window, so a sweep at bar `i` cannot be confirmed until
  `i+3` closes. The reversal has typically already travelled. Operator: *"After
  the move is completely done??"* — effectively yes.
  ⚠️ **AND THE CONFIRMATION WINDOW IS THE DISQUALIFICATION WINDOW.**
  `closes_beyond` is counted over that SAME `i..i+3` span, and `veto_accept`
  (`closes_beyond >= 2`) is a HARD veto. **Waiting for evidence actively
  manufactures the acceptance count that then refuses the trade.** Measured: the
  accept veto closes **64.5%** of all named-pool ticks.
  **ONE CAUSE FOR THREE SYMPTOMS** previously investigated separately — 2%
  fleet-wide SWEEP dominance, L1.7's "SWEEP tape gap", and SweepReversal's 0.4%
  live win rate.

  **⚠️ WICKS AND BODIES APPLY HERE TOO (operator's standing rule).** A wick is a
  touch; a close is a decision. The mapper's DETECTION already honours it
  (`highs[i] > pool.price` is the wick, `closes[k] <= pool.price` the body back
  in). The VETO does not: it counts bodies **inside the rejection sequence the
  mapper is still evaluating** and reads them as acceptance. Acceptance is a
  RUNNING condition, and LIQ.3 already built `closes_beyond_live` and
  `invalidated` for it — **the veto uses neither.**

  **THE PROPOSED RULE (operator's, not fitted):** fire on the **first 15s tick
  after the 5m candle that closes back inside the level.** At that instant the
  wick beyond and the body back in both exist, on a frame where a body is a real
  decision. Confirmation drops from 5-20 min to ~15 seconds, and **the veto
  problem dissolves structurally** — with no forward window there is nothing to
  accumulate closes in. Cost accepted: occasional re-breaches, caught by LIQ.3's
  running invalidation instead of by waiting.
  ⚠️ FRAME: **1m for the wick, 5m for the body** — *"the lowest timeframe that
  isn't noise or a rounding error."* On 5m a fast raid-and-reclaim prints as ONE
  candle with a wick and is invisible. Any threshold must move WITH the frame:
  `closes_beyond >= 2` is 10 minutes on 5m and 2 minutes on 1m, and only one of
  those is acceptance.

  **🔴 `touch_count` IS A CONSTANT — 44,450 of 44,890 ticks read 1 (99%).** It
  is NEVER INCREMENTED. Named pools hardcode `touch_count=1`
  (`liquidity_mapper:461`); only equal-high/low CLUSTERS carry a real count
  (`len(cluster)`, lines 489/508). A PDH reads 1 forever regardless of how many
  times price returned to it. **Same failure shape as the condor's constant
  conviction and SWP.3's approach weight: a score with no variation cannot drive
  anything.**
  **THE OPERATOR'S SIZING RULE — size scales with previous touches by a
  consistent multiple — IS SOUND AND CANNOT RUN ON THIS FIELD.** It would be 1x
  on every trade.
  **DECISION: do NOT change the mapper.** It stays the level-finder; the RETREAT
  COUNT is computed alongside it. *"A level is a zone, not a fixed number"* — a
  retreat is a wick reaching **within 0.2%** (the tolerance the mapper's own
  dedupe already uses, so there is ONE definition of a zone) with a body closing
  back inside. **A retreat and a sweep are the same event at different depths** —
  reach-and-reject vs breach-and-reject — so the count is the level's defence
  record and the sweep inherits it as size.
  ⚠️ On a 0.2% band the count runs HIGHER than intuition because near-misses
  count. **The multiple must be modest** — six defences must not mean six times
  the risk.

  **🔵 LONDON IS CLEAN — LIQ.1 WORKED.** London-named sweeps: 08-11 **3,013**,
  then **0 / 0 / 0** on 08-12/13/14. The gate (`NAMED_POOLS_INCLUDE_SESSIONS`,
  default off) is correct and covers both the Asia and London sites; the FIELDS
  stay populated by design because `shadow/primitives.py` reads them.
  **SWP.7's 2,009 London ticks came entirely from 08-11** — the `--since` was
  one day early.
  ⚠️ **POST-LIQ.1 ANALYSIS STARTS 2026-08-12, NOT 08-11.** The archive is TWO
  REGIMES: before 08-12 London/Asia were sweepable pools, after they were not.
  **Mixing them makes sweep numbers incomparable.**

  ⚠️ TOOLING: the grid and sweeps reports STREAM (constant memory) because the
  first version loaded every log and was **silently OOM-killed, rc=137, on five
  sessions** — printing nothing at all. Measured after: 282,750 records at
  **77 MB** peak. Both write report files rather than relying on scrollback.

- **v4.77 — 2026-08-15 — BFLY.3: THE BUTTERFLY DEBIT CEILING IS FLAT AT 0.50.
  CONVICTION NO LONGER GATES IT.** `butterfly_strategy` v3.5 · `config` ·
  6 tests (177 total).

  **THE MEASUREMENT REFUTED BOTH CANDIDATE DESIGNS.** The ceiling scaled with
  `regime.conviction` (0.33 at conv<=0.30 rising to 0.50 at conv>=0.55). The
  operator proposed INVERTING it, reasoning that low conviction should mean the
  best payoff asymmetry. Fleet-wide across 29 boxes:
  **THE conv->ratio SLOPE IS POSITIVE ON 5 OF 7 SAMPLED SYMBOLS** — AVGO +0.103,
  GS +2.550, NVDA +0.109, PLTR +0.038, QQQ +0.211; only SMH −0.048 and
  TLT −0.031 negative. **Higher conviction travels with MORE EXPENSIVE tents.**
  So the original design paid more exactly where the trade was worse, and
  inverting would have been worse still. Likely mechanism: a strong pin CREATES
  the low-ADX tight-range state L2 reads as high-conviction RANGING, so
  conviction and tent price move together — conviction is a weak proxy for pin
  quality, not an inverse of it.

  **AND IT COST REAL TRADES. SMH: 46 setups at a mean ratio of 0.379 —
  comfortably positive asymmetry — and only 3 fired**, because conviction
  averaged 0.033 so the ceiling sat on its 0.33 floor. **43 cheap tents refused
  by a score that does not measure the thesis.** AVGO 1 of 5, QQQ 1 of 27,
  MSFT 1 of 2.

  **WHY 0.50 AND WHY IT NEEDS NO HOLDOUT.** Max profit is `wing − debit`, so at
  ratio 0.50 you risk exactly what you can win. **0.50 IS THE STRUCTURE'S OWN
  BREAK-EVEN** — it is arithmetic, not an argmax, and cannot be overfit. Above
  it a butterfly pays less than it costs.

  **THE REJECTS STILL DO THE HEAVY LIFTING**, which is what makes a flat ceiling
  safe (operator: *"the rejects are already doing the heavy lifting for us"*):
  NVDA 0.718, PLTR 0.799, NFLX 0.941 and TLT 1.029 stay refused **on PRICE**.
  `_conv` is still journaled so the relationship remains measurable and this is
  revisitable; the old constants stay in config unread, so a revert is one line.

  ⚠️ **BFLY.2's WING SWEEP CAME BACK AGAINST THE THEORY AND WAS NOT ACTED ON.**
  On real chains the ratio rises MONOTONICALLY with width — 0.33 / 0.52 / 0.69 /
  0.79 / 0.86 / 0.89 at 2x-16x — the opposite of the U-curve a synthetic convex
  chain predicted. Only 2x clears 0.50. **But n=15 pin observations across 5
  sessions**, every cell under the n>=40 floor, and there is a known measurement
  gap: far wings may be priced off wide or stale quotes, which would produce
  exactly this inversion. **No wing change shipped.** The bid/ask-width-by-wing
  column has to be added before that curve is trusted.

- **v4.76 — 2026-08-15 — OBSERVER DEBT CLOSED: ALL THREE READS ANSWERED, NONE
  DELETED.** Every criterion was written to force a delete decision; none was met
  for the reason the criterion anticipated.

  **VEL.1 — PARKED, CAUSE IDENTIFIED. Not deleted (operator's call: "I'm not
  gonna delete anything").** Zero firings in FIVE WEEKS of logs (Jul 10 -> Aug 15,
  47MB) — zero occurrences of the string VELOCITY at all, on SPX and QQQ.
  Verified the grep matched the code's actual emission and that
  `VELOCITY_STALL_ENABLED` defaults ON, so the null is real.
  **THE CAUSE IS A HORIZON MISMATCH, NOT BROKEN LOGIC.** `VELOCITY_GRACE_MIN=10`
  plus 3 confirm ticks means a position must live ~10.75 min before the check can
  emit. **ORB's killers die at 3.0 min** (`orb_structure_stop`, n=93, 23 sessions)
  **while its winners live 7.2 and 13.3 min.** So hold duration is nearly an
  INVERSE discriminator: any grace short enough to catch a staller sits inside the
  window where a winner is still developing. **No grace value separates them.**
  Greeks were NOT the blocker (`chain_marks` shows theta 100%% populated, delta
  60-83%%), and the floor curve `{10: 3.9, 15: 18.0, 20: 29.8}` was fitted at
  n=22 on 10-20 minute horizons ORB never reaches.
  ⚠️ Also banked: `theta_bleed` IS live and firing — **107 trades, 100%% win,
  +$2,159** — it protects gains rather than cutting stallers, exactly as its
  docstring says. And `orb_structure_stop` at **−$21,958 / 93 trades** is the
  PRICE OF A CORRECT INVALIDATION RULE, not a defect: ORB is **+$25,081 net
  including it**. Whether some of those were dead before structure confirmed is
  a real question, TABLED at the operator's direction.

  **PF.2 — CONTINUE. Criterion not met.** 15/15 boxes, three sessions, ~22.1k
  fork records each. Real geometry: AMD daily `modified_schiff`, 45 bars,
  511.93/454.33/396.73, `pos_pct` 79.84.
  **⚠️ AND THE OBJECT IS A CONTAINMENT ENVELOPE, NOT AN ANDREWS PITCHFORK.**
  `pivot_built {"1d": false}` on **22,159 of 22,159** records — the §4.3 pivot
  arm has NEVER built on a real frame. Every daily fork in the system is a
  containment fit (spans 0.95-1.00). Operator: that is still useful, and for
  anchoring a credit spread it is arguably BETTER — a rail price has
  demonstrably respected beats a three-pivot construction.
  ⚠️ Anything reasoning about *pitchfork* mechanics (median-line reversion, tine
  touch) is reasoning about geometry we do not have — the whitepaper's 17
  applications need re-reading with that in mind. §4.3 to be parked with a
  one-line report if it ever fires, so it cannot stay silently false for another
  month. The `pos_pct` × continuation join waits for a clean session (22 of
  08-14's continuation fires are one-tick CNT.1 artifacts).

  **BFLY.1 — DO NOT MOVE THE WINDOW YET. The blocker is the DISCOUNT GATE, and
  the gate is right.** Fleet logs: `GEX not PINNING` dominates 20-50x, but after
  a pin is found the rejections are `tent too expensive for this conviction`
  (39 NVDA / 26 QQQ) and `discount gate REJECT` — with exactly **one PASS** on
  QQQ, which closed **two butterflies, both winners**.
  **⚠️ QQQ's CONVICTION IS ALREADY MAXED AND IT STILL REJECTS:** p50 conviction
  **0.647** (above `DISC_CONV_HI` 0.55, so the ceiling is pinned at 0.50) while
  tents cost p50 **0.54**, closest miss **0.01**. NVDA is the opposite: conviction
  p50 **0.014** (gate stuck at the 0.33 floor), tents **0.62-0.82**.
  **AND 0.50 IS EXACTLY WHERE THE ASYMMETRY INVERTS** — max profit is
  `wing − debit`, so at ratio 0.54 you risk 0.54 to win 0.46. Those rejections
  are CORRECT. Raising the ceiling would buy trades whose payoff is upside-down.
  ⚠️ The code comment claiming gate 6 is *"MEASURED never-binding: zero 'too far
  from pin' rejections in the entire QQQ log"* is **FALSE** — it fires **91 times
  on NVDA**. Measured on one symbol, generalised to all.

- **v4.76 (cont) — BFLY.2: THE WING IS FIXED, AND THAT IS THE REAL CONSTRAINT.**
  `tests/butterfly_wing_sweep.py` v1.0.
  `config` defines only `BUTTERFLY_WING_SPX = 25` and `BUTTERFLY_WING_QQQ = 5`;
  **every other symbol takes the QQQ default of 5 STRIKE INCREMENTS** regardless
  of price, expected move or volatility. A pin on a quiet day and a violent day
  get identical wings — when the question is how much of the distribution lands
  inside them. That plausibly explains NVDA at 0.62-0.82 vs QQQ at 0.41-0.57 for
  the same thesis.
  **THE RATIO IS A U-CURVE, NOT MONOTONE.** Verified on a convex synthetic chain:
  0.76 at 2x, **0.64 at 5x**, then RISING to 0.71 / 0.80 / 0.85 at 8x/12x/16x,
  with max profit and zone width plateauing after 8x. **So there IS a sweet spot
  and widening past it is strictly worse** — more capital at risk for the same
  payoff. Today's default of 5x sits at the minimum on the idealised curve;
  whether it does on real chains, and whether the minimum SHIFTS PER SYMBOL, is
  what the tool answers.
  Measures per width: debit/wing (what the gate reads), max profit in dollars,
  **zone/EM** (the honest POP stand-in — a butterfly wins anywhere between its
  breakevens), and **REALIZED** settled on the tape.
  ⚠️ Priced at MID, no slippage (FRC.1 says the real spread is material, so
  dollars are OPTIMISTIC — the RANKING survives, the magnitudes do not); 5-minute
  chain cadence; held to 15:45. **NO BEST WIDTH IS NAMED** — the in-sample argmax
  is overfit by construction, same discipline as the floor sweep.
  Reads the PIN the engine identified rather than re-deriving GEX, so there is no
  second lineage of that logic (§7).

- **v4.75 — 2026-08-14 — WORKING_AGREEMENT 21-25: THE FIVE FAILURE MODES OF
  2026-08-14, WRITTEN DOWN.** At the operator's instruction, so a future thread
  inherits the lessons rather than the mistakes.

  **21 — A TEST THAT READS SOURCE TEXT PROVES NOTHING ABOUT RUNTIME.** 162 tests
  passed over a `NameError` that crash-looped every box opening a condor leg
  ~7.5 min later. Twelve tests covered that path; every one asserted the SOURCE
  contained `is_trend_participation(record)` — which it did. **The name was never
  bound.** Rule 20 one level up. Now: at least one test per exit path CALLS
  `evaluate()` with a real record, in BOTH fresh and rehydrated shape, and a
  chain test must include HOP 0 — the dispatch. **The proof a test is real is
  that it FAILS against the broken version.**

  **22 — A FIELD READ OFF `record` MUST BE A COLUMN.** `is_trend_credit` is not
  one of the 69; `SELECT *` dropped it on every restart, and a restart happens on
  every bake. **Prefer DERIVING over adding a column** — a column fixes tomorrow
  and leaves today's open rows reading `None` as `False`. Derivation must FAIL
  CLOSED. Same rule for in-memory engine state: the condor ratchet's earned tier
  was reset by every bake.

  **23 — FIX THE HOP UPSTREAM.** Five of the nine audit findings were introduced
  the same day, each while fixing the previous one, and the pattern was identical
  every time: repaired where found, feeding hop never checked. Changed the
  record's `strategy` field without checking what DISPATCHES on it; added a call
  without checking the IMPORT. **grep every READER, not just the writer. Ship
  coupled changes in ONE commit.**

  **24 — VERIFY THE EDIT LANDED.** The `NameError` came from a scripted
  `.replace()` whose anchor appears ZERO times in the target — it succeeded,
  changed nothing, reported nothing. Assert the anchor matched; read back the
  result; `python -c "import <module>"` catches an unbound name in one second and
  was not run. **Canaries check BEHAVIOUR, never a version string** — four were
  failing at HEAD purely because those files legitimately advanced, training the
  reader to skim past failures while a real one looks identical.

  **25 — READ EVERY `.md` BEFORE WRITING CODE.** The thread's opening instruction.
  Reading on demand instead cost a **774-line duplicate** of
  `tests/replay_confluence.py` (which has done as-of replay since 2026-07-21) that
  **reintroduced the exact bug its v2.2 prevents**, a live module modified for a
  test artifact without consulting `FILE_MAP.md`, a doc file created against
  `docs/README.md`, and two days of priority ranking done without `ROADMAP.md`.
  All reverted.

- **ALL 29 WILL TRADE MONDAY, NOT THE USUAL ~15.** Read from source rather than
  assumed: `orchestrator.run()` starts only its `wake_list` and never STOPS a
  box outside it, and `main.py` has NO selection gate — a running bot trades
  whenever `is_rth()`. So the cohort is normally ~15 only because the other
  boxes are STOPPED instances. **Monday's sample composition therefore changes
  at the same moment the engine does — two basis changes at once.** Not
  necessarily bad (14 symbols that have never traded would finally produce
  rows), but it must not be discovered retrospectively in the numbers
- **A SMALL CONFOUND ON TOP:** `_push_brief_flags` writes `~/brief_flags.json`
  only to boxes in the wake list, and `setup_scorer._brief_strength()` yields
  **0.0** on a missing or stale-dated file. Selected boxes carry the brief nudge
  (a flat 0.30 for every name, per item X), non-selected boxes carry 0.0. The
  two cohorts are scored on slightly different inputs — benign, documented, and
  a reason not to pool them without noting it
- **THE DAY ROLLOVER IS SAFE — CHECKED, NOT ASSUMED.** A process running from
  Saturday through Monday could have carried stale daily state. It does not:
  `main_loop` clears `session_reset_done` on any non-RTH tick, so
  `handle_session_reset()` fires fresh at Monday's open — risk manager session
  reset, ORB engine reset, `orb_range_established_today` cleared and re-fetched
  after 9:35. No carried-over ORB range, no stale daily counter
- **WATCH ITEM — SPX MEMORY.** The known OOM peaks at 419M, and these processes
  will have run ~65 hours by Monday's close instead of ~7. `OT_MEM_TRACE=1` is
  armed on SPX, so this is unusually GOOD conditions for MEM.2 — a longer
  runway makes a real leak easier to see. It is also the most likely session for
  an OOM kill. Both are true; read MEM_TRACE early rather than at the close

### 🔑 THE VWAP LEDGER'S FIRST REAL VERDICT — AND WHY IT DOES NOT SHIP ITEM E
Run over 08-05/06/07: 39,344 journal records, 304 trade rows, six tracks in
coverage where v1.3 showed one.
- **CONTINUATION is the only strategy with a real sample: 233 trades joined.**
  LONG ALIGNED **-$3,773.50** (156 tr, 72 W) - SHORT ALIGNED **-$1,276.00**
  (72 tr, 29 W) - SHORT MISALIGNED **-$858.00** (5 tr, 0 W)
- **DISPOSITION: item E's HARD GATE DOES NOT SHIP ON THIS EVIDENCE.** The gate
  would block 5 trades losing $858 while KEEPING 228 aligned trades losing
  $5,049.50. VWAP alignment does not reach continuation's problem. That is the
  same answer `trigger_drift` gave from the other direction — continuation
  drifts AGAINST itself at 37% positive over 30 bars — and **an entry filter
  cannot repair a trigger with negative drift.** Trigger, not filter
- **DO NOT READ THE PRINTED VERDICT AS SUPPORT.** The tool printed "orientation
  looks right" off a MISALIGNED arm of **5 trades**, because the verdict gate
  tests TOTAL trades >= 3 rather than a floor on both arms. That is a defect in
  the instrument (VW.1f), not a finding about VWAP
- **SWEEP is effectively unmeasured pre-bake:** 3 decided / 157 undecided (132
  "dir not on readiness rows", 25 "no fresh snapshot"). VW.1e's stamp is exactly
  what fixes this, and only forward — from 08-10 the sweep rows carry their own
  direction

## PART 0.8 — THREAD HANDOFF, 2026-08-08 (added v4.14)

Thread hit its attachment limit. This is the state of play, written so the next
thread starts from fact rather than from a summary of a summary.

**~~WHERE WE ARE RIGHT NOW.~~ ⚠️ SUPERSEDED 2026-08-08 EOD — READ PART 0.9.**
This paragraph said 30 deliveries were PUSHED and none BAKED, with the fleet on
pre-RGM.3 code until Monday. **That is no longer true.** The operator baked and
restarted the fleet on SATURDAY 08-08 ~16:30 ET. All 29 boxes are on
`43911e9a3d` == origin/main. Left here struck rather than deleted, because the
next reader needs to see that the plan changed, not a clean sheet that hides it.

**~~THE ONE THING STILL OPEN AND MID-FLIGHT: `vwap_orientation_ledger` v1.3.~~
✅ CLOSED 08-08 — v1.4 (VW.1d) then v1.5 + trade_readiness v1.6 (VW.1e): the remaining defect was the JOIN layer —
direction journaled on only one track, plus a strategy-vocabulary mismatch that
made the trade join structurally unable to match. Traced emitter → event →
section → field end to end before patching, as instructed below.**
Four layers were wrong and each fix was one layer short — field names, then
depth, then paths, then the event whitelist. v1.3 prefix-matches `readiness*`,
which admits the 11,584 records/day that were being skipped. **The operator ran
it and reports a REMAINING PROBLEM that could not be shared before the thread
limit.** So: v1.3 is correct as far as it goes, the payload is confirmed present
(08-06: BELOW 5,058 / ABOVE 3,912), and there is a further defect to diagnose
from output the next thread has not seen. **Do not assume it is the event filter
again — trace emitter → event → section → field before patching anything.**

**~~BAKE STATE~~ — SUPERSEDED, see PART 0.9.** Everything this paragraph listed
as "on disk but NOT running" — RGM.3, SWP.1/SWP.2, CNT.1/CNT.2/CNT.3, MEM.2,
N.7 — went LIVE on 2026-08-08 at ~16:30 ET, along with AX.3's files and VW.1e.
`OT_MEM_TRACE=1` remains armed in the SPX unit.
**⇒ THE BASIS CHANGE IS SATURDAY 08-08 EOD, NOT MONDAY'S RESTART. Do not pool
across 08-08.**

**THE THREE FINDINGS THAT SHOULD GOVERN NEXT WEEK'S WORK.**
1. The edge is in the TRIGGER, not the LABEL — label states carry no forward
   drift, trigger events do, and continuation drifts AGAINST itself (standalone
   37% positive at 30 bars, n=136).
2. `direction_conf` separates favourable from never-favourable at **+0.188**
   (n=571) where `setup_score` and `regime_conviction` are flat. It is the RAW
   L1 score. Needs OUT-OF-SAMPLE confirmation before anything gates on it.
3. The fused label was burying **BEAR/EXPANDING (+$5,059)** inside
   TRENDING_BEAR (−$6,137), and RANGING splits +$1,619 expanding vs −$2,752
   neutral.

**SELECTION IS THE LARGEST NUMBER ON THE BOARD:** 40% of trades never went 2%
favourable, −$34,411 over 12 sessions. No exit work reaches it.

---

## PART 0.7 — SATURDAY 2026-08-08: WHAT LANDED AND WHAT IT COST (added v4.10)

**26 deliveries in one working day.** Recorded here because the delivery ledger
counts artifacts and this counts CONSEQUENCES — and because the next person to
open this file (including me) needs the shape of the day, not just its commits.

**THE ENGINE CHANGED FIVE TIMES.** conviction_integrator v2.1 (F7 emission,
churn 20.8 → 4.2/symbol-day, confirmed live at 7.6x damping) then v2.2 (RGM.3,
sweep leaves the argmax). main v5.5 → v5.8. Sweep ungated from the label
(SWP.1) then given a separate short floor (SWP.2). Continuation opened to
BREAKOUT tape (CNT.1), given an insurance gate for BOS's blind window (CNT.2),
and blocked from the runaway handoff under COMPRESSION (CNT.3).
**⇒ EVERY PER-REGIME STATISTIC IS NOW ON A DIFFERENT BASIS than the 12-session
history. Do not pool across the Monday bake.**

**FOUR INSTRUMENTS BUILT, AND THE POINT OF EACH IS A CONTROL.**
`trigger_drift` (DRF.1) put a POSITIVE CONTROL under a measurement that had only
ever had a null one — ORB Short cleared the random arm at every horizon, which
is what made `a2_cooccurrence`'s "no directional edge in any label state" a
finding rather than a possible artefact. `rejection_ledger` (L3.2a) looks at
what was DECLINED for the first time. `axis_crosstab` (AX.2) was built able to
kill its own hypothesis, and did. `shadow_summary` (SHD.1) read 282,350 records
that had never been read.

**THE THREE FINDINGS THAT SHOULD OUTLIVE THE DAY.**
1. **THE EDGE IS IN THE TRIGGER, NOT THE LABEL.** Label states carry no forward
   directional drift; trigger events do. Continuation drifts AGAINST itself —
   standalone 37% positive at 30 bars over 136 trades. That is negative edge, not
   absent edge, and no stop or trail reaches it.
2. **`direction_conf` SEPARATES AT +0.188** (n=571) where `setup_score` and
   `regime_conviction` do not. It is the RAW Layer-1 score; the INTEGRATED one is
   flat. Needs out-of-sample confirmation before anything gates on it.
3. **THE FUSED LABEL WAS BURYING TWO CELLS.** TRENDING_BEAR is the worst regime
   in the book (−$6,137) while the BEAR AXIS is +$4,391, driven by
   BEAR/EXPANDING at +$5,059. RANGING splits into +$1,619 expanding vs −$2,752
   neutral.

**WHAT WAS KILLED, ON PURPOSE.** `pair_conf` (gap +0.001) — stamped DEAD in its
own payload with a test pinning the marker. The floor stays at 25%/40%: 308
winners, still exactly 5 ever recovered from −25%, zero from −40%.

**WHAT I GOT WRONG, kept because the corrections are the useful part.**
Claimed a sweep fired today off an unscoped aggregate — it had not. Claimed the
fleet was behind HEAD when it was not. Read six thin shadow boxes as an
enable-at-boot failure when the operator's plainer explanation (never selected,
so never woken) fit without requiring six identical faults. Carried "three field
renames" for the VWAP ledger for two nights when the accessor was reading
top-level keys only. **The pattern: a diagnosis that survives unexamined becomes
a fact, and an aggregate quoted without its date range is not evidence.**

**AND THE TOOLS KEPT CATCHING THEMSELVES.** A canary that fired on a CHANGELOG
quoting the line it removed. A leak test that passed on a deliberately leaking
build. A separation verdict printed from an EMPTY arm. Each is the same family
as the laundered green this repo exists to prevent — and each was found by
running the tool against planted data before real data.

---

## PART 0.6 — 2026-08-07 SHIPMENTS: DATED CHECK-INS (added v4.03)

Nineteen deliveries landed on 2026-08-07 and **every one of them is
SHIPPED-NOT-VERIFIED**. Code that is pushed has changed nothing until its effect
is read back, and an unverified change is indistinguishable from a broken one
until someone looks. Each row below names the DATE and the SPECIFIC QUESTION —
not "review", which is how a check-in becomes a formality.

| ⬜ | Check date | Item | The question, and what would falsify it |
|---|---|---|---|
| ⬜ | **Mon Aug 10** | MEM.2 | Does `grep MEM_TRACE ~/options-trader/bot.log` on SPX name a growing allocation site? **If RSS climbs while traced growth stays flat, the leak is NOT in Python objects** and tracemalloc is the wrong tool — the tool says so itself. |
| ⬜ | **Mon Aug 10** | SWP.1 + SWP.2 | Did sweep fire at all under the score gate, and did SHORTS stop? A 0.20 floor against a ~0.265 ceiling is a NEAR-DISABLE. Zero longs would mean the 0.05 floor is also too high. |
| ⬜ | **Mon Aug 10** | CNT.2 | Do `insurance_stop` rows appear? Zero in a full session means `underlying_stop` is never breached before BOS arms, and the gate is inert rather than protective. |
| ⬜ | **Mon Aug 10** | CNT.3 | `COMPRESSION / Continuation` trade count must be **ZERO**. Anything above zero means the block is not reached. |
| ⬜ | **Mon Aug 10** | RGM.3 | Confirm no `SWEEP_REVERSAL` label is emitted, and that the tie-break head is BREAKOUT_VOLATILE on dead ticks. **Per-regime stats are now on a different basis — do not compare to the 12-session history.** |
| ✅ | **CLOSED 08-08** | ~~SHD.2a — revive the dead observers~~ | **NOT A FAULT.** All 29 boxes read `enabled` + `active`; GS simply has zero sessions because it has barely been SELECTED to trade, and the observer only runs on a WOKEN box. The operator's explanation fit without requiring six identical failures; mine required six. Coverage maps onto the trading cohort. **Nothing to revive, nothing being lost.** |
| ⬜ | **Mon Aug 10** | SHD.2a-remnant — SMCI's truncated session | The ONE box that fits neither story: `SESS=1` with **11 RECORDS** ≈ 2.75 minutes. Never-woken gives 0; woken gives ~1,560. Eleven is a start that died almost immediately. One box, one date — small, but it is a real anomaly rather than a selection artefact. |
| ✅ | **CLOSED 08-08** | ~~VW.2 — is the VWAP payload populated?~~ | **YES, IT ALWAYS WAS.** 2026-08-06: `price_vs_vwap` BELOW **5,058** / ABOVE **3,912**, only 554 NONE. My "the pipe may be empty" hypothesis was wrong. The tool's EVENT WHITELIST was rejecting every record that carried the data — see VW.1c. |
| ⬜ | **Mon Aug 10** | **VW.2 — is the VWAP payload actually POPULATED?** | VW.1b fixed the SCHEMA (all five fields resolve) but the first real run returned **419 undecidable, ZERO decidable** — every row "index/NONE side, gate inert by spec". `_market_snapshot` emits `{vwap: None, price_vs_vwap: "NONE"}` whenever `vw <= 0 or px <= 0`. **So the pipe is open and the payload may still be empty.** Check `price_vs_vwap` on NON-index symbols: if it is NONE there too, `volatility_engine.vwap` is not reaching the snapshot and item AI's VWAP-anchored condor midpoint STILL has no data accumulating — which was the whole deadline. A fixed schema over a null payload is not a fixed pipeline. |
| ⬜ | **Mon Aug 10** | SHD.2a — REVIVE THE DEAD OBSERVERS **FIRST** | `systemctl is-enabled shadow-observer` on **GS (0 sessions), SMCI (11 RECORDS), DIA/GLD/IWM/TLT (exactly 1 session each)**. One 1,560-line session then silence is the ORIGINAL 07-22 signature, so the enable-at-boot fix did not take there. **Do this Monday or the Aug 14 pull inherits the same six holes** — every session between now and then is unrecoverable once missed. Disabled vs enabled-but-crashing are different problems; `is-enabled` separates them in one line. |
| ⬜ | **Tue Aug 11** | EVM re-baseline | First `evm_status.py --asof` run after the slip. **SPI will JUMP; that is the plan moving, not work done.** Brief it as a re-baseline or the number lies. |
| ⬜ | **Fri Aug 14** | CNT.1 | One week of `trend_continuation_breakout`. Compare its drift and never-favourable rate to `_standalone`. **This is the only live test of whether direction from the trend VOTE beats direction from the LABEL** — and the vote-derived buckets showed the same nothing, so do not assume it wins. |
| ⬜ | **Fri Aug 14** | DRF.1 | Re-run `trigger_drift` with the post-bake sessions. **ORB Short must still clear the null arm** — if the positive control stops passing, every conclusion drawn from it is withdrawn, not adjusted. |
| ⬜ | **Fri Aug 14** | N.7 | Are rows carrying `ruleset`? Then re-run L3.2a and confirm cross-date pooling can finally be split by engine. |
| ⬜ | **Fri Aug 14** | L3.2a v1.1 | Add the seeded NULL ARM and make the MFE/MAE **ratio** the headline. Until then the MISSED column must not be quoted — MFE ≥ 0.10% over 20 bars is a bar ordinary range clears. |
| ⬜ | **Fri Aug 14** | GATE.1 follow-on | Add a BREACH TIMESTAMP to `auto_label` so BREAKOUT (141) and SWEEP (63) symbol-days become gradeable. 204 symbol-days of ground truth currently unscoreable. |
| ⬜ | **Fri Aug 14** | **SHD.2 — RE-PULL THE SHADOW DATA AND CALIBRATE OFF IT** | The calibration deploy is **Mon Aug 17** and this is the last working day before it, so this is the pull that can actually SET DIALS rather than describe them after the fact. Expect ~19 sessions (13 banked + Aug 10-14). Three questions it is being run to answer, each already framed by the 08-07 read: **(a)** does `dist_atr` still put the median >2 ATR from a named level and only ~14% within 0.5 ATR — if so the sweep floor stays permissive and "it barely fires" is NOT an argument to tighten it; **(b)** do London High/Low still carry ~61% of nearest-level observations — that decides whether Level.1/2/3 work is really London-levels work; **(c)** is `UNKNOWN` still ~18% of live ticks against the offline harness's 4% — a 4x divergence in the same quantity, and the same class that hid the dead L2 gate. **⚠️ THE PULL WILL SPAN TWO ENGINES**: RGM.3 bakes Monday, so `regime` values before and after must be split at the bake date, never pooled. |
| ⬜ | **Wed Aug 26** | SHD.3 — confirmation pull, 2 days before FREEZE | Re-run the summariser one last time before **Fri Aug 28**. Not to set dials — those were set on the 17th — but to confirm the distributions the dials were fitted to have not drifted underneath them. **A freeze declares a baseline; declaring one on a distribution that moved after calibration is how a frozen baseline becomes a frozen mistake.** If (a), (b) or (c) has shifted materially, the freeze is the thing to reconsider, not the dial. |
| ⬜ | **Fri Aug 21** | AJ.2 | The continuation decision, with a week of CNT.1 behind it. Standing evidence: standalone drifts **−0.106% at 30 bars, 37% positive over 136 trades** — negative edge, not absent edge. |
| ⬜ | **Fri Aug 28** | Floor re-test | Only if new evidence appears. **DECIDED 08-07: the 25%/40% floor STAYS.** 308 winners, still exactly 5 ever recovered from −25%, zero from −40%. Do not reopen on a whim. |

**⚠️ TWO CAVEATS THAT OUTLIVE THIS TABLE.**
**(1)** 2026-08-03 and 2026-08-04 carry ~3,650 ticks each against ~11,280
elsewhere — the session guard blocked collection on 14 boxes two days running and
the tape is NOT recoverable. Mark both PARTIAL wherever they are pooled; every
statistic computed on the 12-session corpus inherits it.
**(2)** Rows banked before N.7 carry no `ruleset`, so the whole 12-session
history is un-attributable to an engine. It only applies forward.

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
`[DESK→DEPLOY]` build is desk work but needs a bake to take effect. **⚠️ The
bake happened SAT 2026-08-08, not Monday** — all 29 boxes are at `43911e9a3d`
== origin/main, so anything at HEAD is already live and this tag now means the
NEXT bake, not the Aug 10 one.
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
  before Aug 31. Build today, live-test Thu Sep 3.
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
  WHAT the premium did and never WHY. Log-only, bakes Mon Aug 17.**
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
  BOOK. Operator directive; bakes Mon Aug 17.** *"Do not execute a regime flip
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
  ⬜ NOT YET BAKED — Mon Aug 17. THE TC.2 EXIT BAKE-OFF HAD NO CAPTURE, AND ITS
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
- `[DESK→DEPLOY]` **VW.1 — ✅ 2026-08-05. VWAP WAS COMPUTED EVERY TICK AND NEVER
  WRITTEN DOWN. Log-only; bakes with the next fleet cycle.**
  **THE FINDING.** `vwap_orientation` has been exiting **rc=1** for at least two
  nights. It is not a broken tool — a key scan of 2026-08-05's journal (11,138
  records, EVERY event type) found **no VWAP-shaped field anywhere**:
  `hits: ['fa.floor_px', 'fa.origin_px']`, which are the condor's impulse
  fields. The tool was built against a schema that never landed, so it has
  **never once run.**
  **AND THE VALUE EXISTED THE WHOLE TIME.** `volatility_engine` carries `vwap`
  and `price_vs_vwap` on its state and has since well before this. Nothing
  persisted them.
  **WHY IT COULD NOT WAIT FOR THE FREEZE.** Item **AI**'s candidate fix for the
  condor is a **VWAP-ANCHORED midpoint** instead of the flat Bollinger midline —
  the leading option if `condor_approach` returns GEOMETRY next week. It cannot
  be evaluated on data that does not exist, so every session from here is history
  we either have or do not. Same use-it-or-lose-it logic as the candle tape.
  **BUILT:** `trade_readiness` v1.5 — `_market_snapshot(ctx)` emits
  `{vwap, price_vs_vwap, dist_pct}` on EVERY readiness record, one snapshot per
  tick shared by all six tracks. `dist_pct` is SIGNED and a percentage of VWAP,
  so a $30 symbol and a $900 one are comparable; a dollar gap would let the
  expensive names dominate every pooled read.
  **`price_vs_vwap` IS READ FROM THE ENGINE, NEVER DERIVED FROM THE SIGN.** The
  engine sets NONE when there is no volume, and a computed sign would always have
  an opinion exactly where the engine deliberately has none. Behavioural tests
  could NOT tell the two apart (the no-volume path returns early), so the guard
  is source-level — found by the deliberate-failure run.
  **⬜ WHY THE PITCHFORK DOES NOT REPLACE THIS:** the fork exists on ~5% of bars
  (median coverage 5.3%, half the symbols under 5%). A fork-anchored midpoint is
  available one tick in twenty; VWAP is available on every tick of every session.
  They are also different objects — VWAP is a volume-weighted centre of gravity,
  the median line is a geometric trend projection. Keep both journaled and the
  comparison stays possible.
  **⬜ STILL BROKEN: `vwap_orientation`'s OTHER lookups.** Even with VWAP
  present, its `CAND` map wants `strategy` and `direction` at the TOP level; the
  journal has `readiness.strategy` and `factors.dir`. Three renames, and it
  cannot run until they land.
  **NOTED IN PASSING:** today's journal already carries `condor_plan: 49`,
  `condor_abandon: 43`, `condor_leg: 2` — AI.1's telemetry is live, and **two
  condor legs actually fired**, the first all week.

- `[DESK]` **A2.R — ✅ CLOSED AS RESEARCH 2026-08-05, plus one candidate and one
  warning. Full write-up in MECHANICS "A2 — TREND and RANGE co-occurrence".**
  **THE DRIFT STUDY CAME BACK NULL, and that is a result.** 175,302 ticks, 6,860
  co-occurring (3.9%), RANGE_ONLY as the control:
  `+10 bars -0.001%  ·  +20 bars +0.003%  ·  +30 bars +0.011%` median drift for
  range-in-bull-trend versus a plain range, n≈3,500 per bucket. The tool's
  PRE-REGISTERED criterion was "a materially positive lift supports treating HTF
  direction as a drift/bias term on the LTF range". **+0.011% at thirty minutes
  is a rounding error on a 0DTE contract.** HTF direction is not a usable drift
  term inside a range — measured and rejected, not untested. **Do not re-open
  it.**
  **WHAT THE CO-OCCURRENCE ACTUALLY COSTS.** L2 commits to a TREND label on
  **98%** of those ticks (BULL 50.6%, BEAR 47.8%, RANGING **1.5%**) because
  argmax makes the labels compete. So on 3.9% of all ticks a genuine range state
  is INVISIBLE to every RANGING-gated strategy — the condor and the butterfly,
  and the condor is the one that has been starving all week. The loss is not a
  worse forecast; **it is a co-truth suppressing half of itself.**
  **⚠️ THE FINDING I WOULD CARRY INTO THE L1 FREEZE:** median conviction on those
  commits is **1.00** for both BULL and BEAR — the integrator is MAXIMALLY
  CONFIDENT on precisely the ticks where the drift study says the direction has
  no forward content. **Confidence and predictive value have come apart.** That
  is about L2's conviction scale, not about A2, and it means a label can be
  certain and uninformative at once. Worth stating before anything downstream
  treats conviction 1.00 as evidence.
  **⬜ CANDIDATE (POST-FREEZE): split A2 into two independently weighted axes**
  so a range inside a trend is BOTH, instead of one losing argmax. It would NOT
  improve prediction — settled above. It would stop RANGING losing on ticks where
  it is true.
  **⬜ GATE IT ON A MEASUREMENT, NOT THE ARGUMENT — Aug 8-9, offline, changes
  nothing:** the replay corpus already holds all 6,860 ticks with both scores, so
  one pass answers *if RANGING had won there, how many condor plans would have
  existed, and in which regimes?* A handful means the change buys little; the
  condor's missing population means it has its justification with a number.
  **SCOPE WARNING:** this makes regimes AXES rather than mutually exclusive
  competitors, so every consumer of `primary_regime` is affected — the condor's
  RANGING gate, continuation's TRENDING gate, the exit-side regime flip. Post
  Aug 21 only.
  **ALSO TODAY: 5/5 ACCEPTANCE FOR THE FIRST TIME**, and the tape is fully
  recovered — 11,293 ticks across 29 symbol-sessions against 08-03/08-04's
  degraded ~3,650 across 15.

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
- `[DESK·DATA]` **RGM.1 — 🔴 OPEN. THE FLEET IS CHURNING, NOT TRADING. Layer-2
  label instability is the largest single problem on the board, and three
  offline tools have narrowed it without closing it.**

  **THE SYMPTOM.** 2026-08-06: 95 trades, **-$3,129**, 40% win, **median hold
  0.3 min**, 68% sub-minute. `regime_flip` exits grew **12 -> 43 -> 59** across
  08-04/05/06 and are now the fleet's dominant behaviour. RANGING was 56 of 95
  entries and `regime_flip (RANGING)` closed **54** of them at ~0% excursion in
  either direction. Never-favorable hit 65% at the 2% cut against 35%
  cumulative.

  **THE SCALE.** L2 is `always-argmax` (its own log line). It commits **~20
  label switches per symbol per session** — 586 across 29 symbols on 08-05,
  against 961 raw L1 flips, so it does damp 1.6x. **Operator prior, from
  discretionary experience: a real session contains ONE OR TWO regime changes.**
  A tape that starts trending and goes sideways; a muted open that catches a
  move late. Not dozens. **That is a 10-20x discrepancy between what the engine
  reports and what the market does**, and the prior is the more credible of the
  two.

  **TOOLS BUILT (all pushed, all offline, all read-only):**
  `tests/regime_switch_cost.py` **v1.1** — sweeps a switching cost over the
  replay corpus. Streams one file at a time and keeps only the scores; v1.0 was
  **OOM-killed**, the THIRD tool in this repo to die of load-everything-then-
  filter (after ramp_calibration and a2_cooccurrence).
  `tests/score_series.py` **v1.0** — sparkline dump of one symbol-day's
  per-regime scores, so the question can be answered by looking rather than by
  another summary statistic.
  `tests/veto_attribution.py` **v1.1** — attributes zero<->nonzero transitions
  to the hard veto that flipped, and separates BRANCH CHANGES (a veto key
  appearing or disappearing) from true veto flips.

  **FINDING 1 — A SWITCHING COST DOES NOT FIX IT.** `delta=0` gives **25.1
  switches/sym/day**, which matches L2's own ~20 and validates the harness.
  `delta=0.30` — a third of the entire score range — only reaches **8.2**, with
  median hold 23 ticks (~6 minutes). **Gradual decay, no cliff.** On a planted
  world with two real regime changes buried in noise, `delta=0.10` collapsed
  churn from 104 to 2.5. Real tape does not behave that way, so the churn is
  **not** argmax tying on a margin.

  **FINDING 2 — WHY. THE GRAMMAR IS MULTIPLICATIVE** (regime_confluence's own
  header): `score_R = (∏ hard_veto ∈{0,1}) · (∏ soft_necessary ∈[0,1]) ·
  (Σ w·corroborator)`. **A single hard veto at 0 annihilates the score**,
  however strong every corroborator is. So a regime transition is a BOOLEAN
  FLIPPING, not a score crossing — and **hysteresis cannot fight a boolean**.
  The same fact means **re-weighting corroborators would change little**: the
  weights live in the LAST term, which is multiplied by zero on most ticks.

  **FINDING 3 — THE SCORES ARE SPARSE, NOT BINARY.** Fleet-wide, share of ticks
  at exactly 0 / exactly 1 / in between:
  `SWEEP_REVERSAL 96.0/0.0/4.0 · COMPRESSION 79.5/0.0/20.5 ·`
  `TRENDING_BEAR 73.0/10.9/16.1 · TRENDING_BULL 71.2/11.9/16.9 ·`
  `BREAKOUT_VOLATILE 63.8/0.1/36.0 · RANGING 45.7/0.0/54.3`
  Only the trend regimes ever peg at 1.0. **SWEEP_REVERSAL is effectively not
  participating** — above zero on 4% of ticks across 19 sessions.

  **FINDING 4 — VETO ATTRIBUTION, 19 sessions (07-13..08-06):**
  `RANGING (branch change: veto_flat) 13,860 = 70%`
  `BREAKOUT (no veto changed — soft)   8,325 = 100%`
  `RANGING veto_flat                   4,261 = 21%`
  `COMPRESSION veto_inside             1,834 = 44%`
  `COMPRESSION veto_flat               1,199 = 29%`
  `TRENDING_BULL veto_dir  874 = 48% · TRENDING_BEAR veto_dir 841 = 49%`
  `TRENDING_BULL veto_struct 566 = 31%`
  totals: RANGING 19,837 · BREAKOUT 8,325 · COMPRESSION 4,198 ·
  TRENDING_BULL 1,806 · TRENDING_BEAR 1,701 · SWEEP 271.

  **FINDING 5 — BREAKOUT_VOLATILE HAS `hard_vetoes=[]`.** No hard gates at all,
  so its 8,325 transitions are pure soft crossings. **A switching cost WOULD
  help BREAKOUT specifically**, which partly rehabilitates
  `regime_switch_cost` — right fix, wrong regime.

  **FINDING 6 — RANGING's `veto_flat` IS COSMETIC.** Its full path passes
  `hard_vetoes=[1.0]` (hardcoded) while publishing `"veto_flat": 1.0`. The LIVE
  `veto_flat` belongs to COMPRESSION. RANGING emits THREE breakdown shapes
  (last 3 sessions): `20,249` full path (11 keys, veto_flat=1.0) · `4,224`
  angle >= FLAT_ANGLE_CUT_DEG early return (3 keys, veto_flat=0.0) · `1,752`
  **no bar window** (adx, is_expanding, path, price_vs_bb, reason — NO veto
  key). Over all 19 sessions the reason split is `(evaluated) 174,610 = 93.6%`
  vs `no bar window 11,972 = 6.4%`.

  **⬜ CURRENT HYPOTHESIS, HELD LOOSELY.** RANGING drops into its
  no-bar-window fallback on 6.4% of ticks **in short isolated bursts** rather
  than one contiguous warm-up block. Each isolated burst produces TWO
  zero-crossings (in and out), which is how ~11,972 fallback ticks generate
  ~13,860 branch-change transitions. **If so this is a BAR-AVAILABILITY problem
  wearing a classification costume** — the same family as the
  `trend vote STARVED 1d: 10 bars, need 55` warnings and the thin tape
  (MSFT 390 ticks on 08-06 against ~750 for a full session).

  **⬜ THE VERY NEXT STEP — probe SHIPPED as `tests/rng_probe.py` v1.0 (08-06),
  NOT YET RUN on the corpus.** Measures the RUN LENGTHS of RANGING's fallback
  and the session index where it first appears. Mostly **1-tick runs** => the
  input flaps on individual ticks, a plumbing bug and the most fixable version.
  **Long runs** => genuine warm-up or outage. First-fallback p50 near 0 =>
  benign warm-up; p50 mid-session (300+) => the window is LOST after being
  established, which is worse.

  **TWO DISCRIMINATORS ADDED BEYOND THE ORIGINAL SPEC**, both free from the
  tape. (a) **The ts gap ENTERING each mid-session run.** A gap of 1 minute
  means the tape was contiguous and the INPUT flapped; a gap > 1 minute means
  bars were missing. This matters because of a source fact verified at HEAD:
  `replay_confluence` v2.1 builds `closes` as the last-25 slice of a GROWING
  frame, so in this corpus **`closes` can never revert to None after bar 25** —
  a mid-session fallback here can only be `atr_current` going None, or a run
  sitting after a tape gap. The probe separates those two rather than leaving
  the answer to inference, which is how the last two wrong turns happened.
  (b) **Implied crossings counted with `veto_attribution` v1.1's own semantics**
  (a crossing exists only where the ADJACENT EVALUATED tick scored non-zero;
  session edges and zero-to-zero neighbours contribute none) instead of a flat
  2-per-burst, so the comparison against 13,860 is apples-to-apples. If implied
  ≈ 13,860 the burst arithmetic holds and the fallback explains the branch
  changes; materially short and something ELSE is toggling RANGING's key set.

  Proven on a planted corpus with known run lengths before issue (5 planted runs
  recovered as 5, with the exact histogram, warm-up/mid split, gap
  classification and crossing count). Read-only, stdlib-only, streams one file
  at a time — the fourth tool in this repo would otherwise have been the fourth
  to die of load-everything-then-filter. **The RUN is the deliverable; this file
  is not a finding.**

  **⚠️ THREE WRONG TURNS ON THIS THREAD, recorded so they are not repeated:**
  (1) assumed hysteresis was the fix — the sweep refuted it; (2) read one MSFT
  chart as "binary switches" — the fleet table showed sparse-zero instead;
  (3) called BREAKOUT's 100%-no-veto a tool bug — it is correct. Plus two tool
  bugs of my own: v1.0 credited RANGING with 4,929 `veto_flat` flips that were
  branch-change artifacts, and I argued "you cannot have more crossings than
  states" when an isolated 1-tick run yields two. **I inferred from source twice
  and was wrong twice. Measure first.**

  **⬜ FINDING 7 — THE EMISSION LAW HAS AN UNPROTECTED BRANCH** (read directly
  from `conviction_integrator` v2.0 `_emit` at HEAD, 08-06). While the
  incumbent's conviction is **>= theta_hold (0.45)** a challenger displaces it
  only by clearing **theta_commit (0.65)** AND beating it by
  **delta_displace (0.12)**. The moment the incumbent falls **below 0.45** the
  code executes `self.incumbent = top_r` **unconditionally, every tick** — no
  commit bar, no margin, no dwell. A challenger at conviction 0.05 takes the
  label and can lose it again on the next tick.

  **This contradicts the module's own stated design contract**, in its header:
  *"Fast to recognize, slow to abandon… A single-tick flicker can never move the
  emitted label off a held regime."* Below theta_hold that is not what the code
  does. By the operator's three-way split this is **CATEGORY 2 —
  CORRECTNESS**, a contributor not doing the job it was designed for, not a
  category-3 tuning preference.

  **IT ALSO EXPLAINS FINDING 1.** `regime_switch_cost`'s delta models
  `delta_displace`, which exists ONLY in the protected branch. If the churn
  lives below theta_hold, that sweep was tuning a knob that is not in the path
  where the churn happens — **right knob, wrong branch**, the same shape as
  F5's right-fix-wrong-regime. It accounts for the gradual-decay-no-cliff
  signature that never made sense for a real hysteresis knob.

  **AND IT SINGLES OUT RANGING.** Its params are `tau_up=780s` (~13 min to
  build) against `tau_dn0=60s` at low conviction — slow to rise, fast to fade,
  so RANGING spends disproportionate time below 0.45, inside the unprotected
  branch. RANGING is 56 of 95 entries and 54 of the regime_flip exits.
  Consistent; **not yet proven.**

  **⬜ THE MEASUREMENT — `tests/emission_law_sweep.py` v1.0, BUILT 08-06, NOT
  YET RUN on the corpus.** The replay records carry `l2.cv`, the full
  post-update conviction vector, so candidate emission laws can be re-decided
  over convictions that were actually observed — no engine run, no tape, no
  re-integration. It reports three things: the share of ticks the incumbent
  spends below theta_hold (is the unprotected branch the NORMAL operating mode
  or an edge case?); every observed switch attributed to its branch by the
  engine's OWN recorded trigger string rather than by my reading; and
  counterfactual switches per symbol-day under protect-below-hold and under
  added dwell, against the operator's 2-4 prior.
  **Harness validation is output #0 and gates the rest** — the baseline variant
  must reproduce the recorded label sequence, exactly as delta=0 had to
  reproduce the engine's ~20 switches before the delta sweep meant anything.
  On a planted one-change world driven through the REAL integrator it agrees
  **99.9%**, and there the current law yields **141.5 switches/symbol-day**
  against protect-below-hold's **1.0** — a CLIFF, which is the signature the
  delta sweep never produced. Dwell 12 over-damps to 0.0 and misses the real
  change, so the tool can detect over-correction as well as churn.

  **⬜ THE FIX, BUILT 08-06 — `conviction_integrator` v2.1.**
  `protect_below_hold` (default ON; **`OT_L2_PROTECT_BELOW_HOLD=0` restores the
  v2.0 law exactly** and is both the kill switch and the A/B control) applies
  commit+margin in BOTH branches and **HOLDS the incumbent when no challenger
  qualifies**. A fading belief is still the best available belief, and its
  conviction — which Layer 3 gates on — reports the weakness honestly either
  way. Declining to switch is not asserting the old label is strong.

  **COLD START IS CARVED OUT.** Protection ARMS only once some regime has
  reached theta_commit at least once. Before that the convictions are near zero
  and the argmax is the deterministic tiebreak head, SWEEP_REVERSAL — above
  zero on 4% of ticks — so protecting from tick 1 would pin the session to it.
  Verified on the planted world: 13 of 20 symbol-days open TRENDING_BULL and
  only 2 on SWEEP. `main.py` independently gates on `not st.stale`, and the
  ORB owns the open and is regime-immune at BOTH dispatch and exit (bare
  `regime_flip` exists only in `_evaluate_continuation`) — three layers of
  cover on the same edge.

  **THE LIVE A/B COSTS NOTHING AND ANSWERS TOMORROW.** v2.1 runs BOTH laws off
  the same conviction vector every tick and reports the other one's label as
  `shadow_regime`, with cumulative `switches` / `shadow_switches`. main v5.5
  logs the pair whenever the divergence CHANGES — never per tick, per
  WORKING_AGREEMENT §17. Nothing reads the shadow to trade. The A/B reads the
  same in either direction, so the control is one env var.

  **⬜ THE GATE — `tests/label_agreement.py` v1.0, BUILT 08-06, NOT YET RUN.**
  Scores both laws against `session_labels.jsonl`, which `auto_label.py`
  derives from PRICE ACTION ONLY (body fraction, close position, prior-session
  extremes) and which has never seen a score, a conviction or a label — so it
  cannot agree with the engine by construction. **PRE-REGISTERED, stated before
  any number was read: H1 — on TREND-tagged symbol-days the protected law
  spends a HIGHER share of ticks in the trending family and its modal label
  agrees with the tag more often. H0 — agreement is unchanged or FALLS, which
  would mean stability was bought by locking in whichever label happened to be
  held. A FALL KILLS THE DEPLOY.** Untagged symbol-days are excluded rather
  than scored as RANGING; absence of a tag is not evidence of a range.

  **✅ RESULT 2026-08-07 — F7 IS MEASURED, NOT ARGUED. Five independent checks,
  every one of which could have killed it.**

  **1. MECHANISM.** `emission_law_sweep` over 19 sessions / 523 symbol-days /
  186,582 ticks: **8,083 of 8,345 label switches — 96.9% — came from the
  unprotected branch.** Commit threshold and displacement margin governed 3.1%.
  Median incumbent conviction at the moment of a switch: **0.08**. The typical
  label change handed off between two near-zero beliefs. The incumbent sat
  below `theta_hold` on 50.3% of ticks, so this was half the session, not an
  edge case. Harness validated first at **98.4%** label reproduction.

  **2. STABILITY, REAL ENGINE, REAL TAPE.** The 08-06 session replayed twice
  through the actual integrator, one variable (`OT_L2_PROTECT_BELOW_HOLD`):
  **v2.0 = 604 switches (20.8/symbol-day) → v2.1 = 121 (4.2/symbol-day).**
  Roughly 5x. The offline counterfactual had predicted 3.3 against a 17.6
  baseline; 08-06 ran churnier than average (20.8), and 3.3 × (20.8/17.6) = 3.9
  plus the arming carve-out — so the model predicted the end-to-end result
  within noise, which validates the modelling chain independently.
  **Stated honestly: 4.2 is slightly ABOVE the operator's "three or four at the
  most", and it is ONE session.**

  **3. CORRECTNESS — the gate, pre-registered before any number was read.**
  `label_agreement` over 19 sessions, 361 tagged symbol-days, scored against
  `auto_label`'s price-action-only ground truth which has never seen a score, a
  conviction or a label: **TREND modal agreement 63.4% → 69.1%, in-family
  47.5% → 57.8%.** The protected law is not merely steadier, it is **more
  right**. H1 confirmed on its registered terms.

  **4. SCOPE.** `L1 IDENTICAL` — the A1–A5 acceptance blocks diff clean across
  the A/B, so the change stayed inside Layer 2. And a free stronger proof: the
  sweep's re-emitted baseline is **661 on BOTH files, byte-identical**. That
  figure derives from each run's recorded conviction vectors, so identical
  baselines prove the **conviction dynamics are unchanged** — v2.1 altered only
  which label is chosen, never how belief accumulates.

  **5. SUITE.** 287 passed / 1 skipped / rc=0 on control, with all 7 emission
  tests confirmed **by name** — including `test_v2_0_control_does_hand_it_over`,
  which must FAIL to flip if the protection assertion is passing for an
  unrelated reason.

  **⚠️ THE ONE DEBIT, NAMED NOT BURIED.** SWEEP in-family FELL 3.5% → 1.3%. The
  registered H1 was TREND-specific while the tool header said "a fall kills the
  deploy" — that ambiguity is mine and is not resolved silently in favour of the
  wanted result. Read straight: SWEEP was ALREADY a dead regime (0.4% of live
  wins, 96% zero), so 3.5% was noise and 1.3% is less noise. It does not
  overturn the gate; it is still a debit.

  **⚠️ WHAT THIS DOES **NOT** FIX, so nobody reads it as more than it is.**
  Layer 1 is untouched — RGM.2 below. Even on TREND-tagged days the protected
  label spends only **57.8%** of ticks in the trending family. The label is
  steadier and more right; it is not right. And **the failure mode CHANGES
  shape**: strategy dispatch gates on the label, so a HELD label runs its
  strategy for ~50 ticks instead of ~8. Thrashing between strategies becomes
  commitment to possibly the wrong one. The agreement lift is the evidence that
  trade is worth taking; it is not proof it always is.

  **⚠️ WHAT A STEADIER LABEL DOES NOT PROVE.** A law emitting one regime all
  day scores zero switches and is worthless. Stability is necessary, not
  sufficient; whether the steadier label is the CORRECT label is the
  `session_labels.jsonl` agreement question and neither tool touches it.

  **⬜ REMAINING UNRESOLVED, carried forward — none of these is closed:**
  1. **The live bake.** BUILT and PUSHED; **NOT BAKED.** Until the fleet runs
     it, today's data is still being generated by the old law.
  2. **Offline ≠ live.** The replay steps bar-to-bar on 1m tape; the fleet ticks
     every 15s. Tomorrow's `L2 A/B DIVERGE` log is the first live evidence.
  3. **The 355-vs-13,860 contradiction (F6/probe).** The RANGING fallback can
     explain at most ~2.6% of the branch changes `veto_attribution` counted.
     Either that row is a THIRD bug in that file's lineage or a fourth RANGING
     breakdown shape exists. Unresolved; needs a direct key-set census.
  4. **`regime_flip` bucketing.** 54 RANGING entries reported closed by an exit
     that exists only in `_evaluate_continuation`, which cannot enter on
     RANGING. Either the report buckets all three variants under one name or the
     entry-regime field means something else. **This changes which strategy the
     churn was actually killing.**
  5. **Cold start unverified.** Protection arms on first commit and `main.py`
     gates on `not st.stale`, and ORB owns the open regime-immune at both
     dispatch and exit — three layers of cover, none of them measured. Wanted:
     first committed label per symbol-day and how long it lasts.
  6. **SWEEP_REVERSAL is a dead regime.** 0.4% of live wins, 96% zero, 0.0%
     modal agreement. A whole regime carrying no weight. Own workstream.
  7. **Two under-sampled dates.** 08-03 and 08-04 carry ~3,650 ticks against
     ~11,280 elsewhere — about 9 symbols instead of 29. They are underweight in
     EVERY pooled statistic on this corpus, including the 96.9% attribution.
     Cause unknown; check the harvest.
  8. **`label_agreement` v1.1.** PIN/BREAKOUT/SWEEP rows are a granularity
     mismatch and are NOT evidence about the engine — window each tag to its own
     timeframe before quoting them.
  9. **`discrimination_census` v1.1.** Separation must be conditioned on ≥2 live
     regimes; the 0.347 median is inflated by uncontested ticks.

  **⚠️ SCOPE + TIMING.** Everything above is read-only analysis. But F7 is a
  contract defect whose output CORRUPTS THE SAMPLE — every `regime_flip
  (RANGING)` row banked at ~0% excursion will later be counted as evidence
  about ranging regimes and it is not — which is Bucket 1 under the two-bucket
  frame, fix-on-sight. The natural slot is therefore the **Mon Aug 17
  calibration deploy, BEFORE the L2.6 freeze window opens**, not post-freeze.
  It changes what gets traded (the label drives dispatch AND the regime_flip
  exit), so it is the operator's call under the standing division of labour.

- `[DESK]` **SWP.2 — 🟡 SHIPPED-NOT-BAKED. SWEEP SHORTS CLEAR A HIGHER FLOOR.**
  Three independent measures over 12 sessions say long and short sweeps are not
  the same trade: **win rate 81% vs 33%**, **never-favourable 4% vs 33%**, and
  **forward drift BUILDING +0.001 → +0.081 → +0.314 (52/56/67% positive) versus
  falling −0.148 → −0.215 → −0.290 (33% positive)**. Dollars agree: +$2,844 on
  27 vs −$1,403.50 on 6.
  **n=6 IS THIN AND THIS IS A PRIOR, NOT A FIT.** What earns it is the
  MECHANISM, which predates the data: the 2026-07-27 PLTR incident was exactly a
  short reversal into a +7.2% up-trending tape, and is why `trend_opp` exists at
  all. The data agrees with a known mechanism rather than deciding on its own.
  **⚠️ CALL IT WHAT IT IS: THIS NEAR-DISABLES SHORTS.** SWEEP's score is capped
  near **0.265** (measured max, 08-07 replay — it is the only scorer with an
  age-decay soft-necessary, half-life 3 bars), so a 0.20 floor admits only the
  top sliver. At −$233/trade that is defensible, but it is a near-disable
  wearing a threshold and must be read that way, not as a dial.
  `OT_SWEEP_SETUP_FLOOR_SHORT=0.05` restores parity with longs without a deploy;
  longs are untouched at 0.05.

- `[DESK]` **CNT.3 — 🟡 SHIPPED-NOT-BAKED. THE RUNAWAY HANDOFF DOES NOT FIRE
  UNDER COMPRESSION.** COMPRESSION/Continuation is **39 trades, 28% WR, −$454**,
  and COMPRESSION is the **worst never-favourable cell in the book at 80%**
  (LIFT 1.98, n=45).
  **WHY THOSE 39 EXIST AT ALL:** continuation cannot enter on a compression
  LABEL — every direction branch requires TRENDING or BREAKOUT — so all 39 are
  RUNAWAY HANDOFFS, which ignore the label by design.
  **THE MECHANISM IS A FLAT CONTRADICTION: a runaway asserts EXPANSION while the
  label asserts COILING.** The handoff's licence to ignore the label is exactly
  what makes it valuable after a real runaway (the label commonly flips to
  BREAKOUT or SWEEP); this is the one place that licence clearly costs.
  `OT_CONT_HANDOFF_IN_COMPRESSION=1` restores the old behaviour.

- `[DESK]` **DRF.1 — 🔴 OPEN. THE DRIFT MEASUREMENT NEEDS A POSITIVE CONTROL
  BEFORE ANYTHING IS CONCLUDED FROM IT.**
  `a2_cooccurrence` (option 47) measures forward drift from LABEL STATES and
  finds nothing anywhere — every bucket, every horizon, inside ±0.03%. That was
  about to be read as *"the regime label carries no directional edge"*, which
  would have been a large architectural conclusion. **But that tool has only a
  NULL control (RANGE_ONLY). No bucket in it is one we KNOW carries edge, so it
  has never been shown capable of DETECTING edge.**
  **ORB nets +$10,156 over 12 sessions.** Drift after an ORB break must be
  visible. If the instrument cannot see the one strategy we know works, the
  instrument is wrong — horizon, signing, or sampling — and nothing drawn from
  label-state drift stands.
  **HOW — `tests/trigger_drift.py` v1.0, BUILT 08-07, NOT YET RUN on the real
  corpus.** Every CLOSED TRADE is a trigger that actually fired. For each, it
  takes the entry timestamp, finds that symbol-day's price series in the replay
  corpus, and measures signed forward change at 10/20/30 bars — **SIGNED BY THE
  TRADE'S OWN DIRECTION**, so a profitable short reads positive — bucketed by
  `setup_type`. ORB Short/Long are the control arms; handoff, standalone and
  Sweep Long are the comparisons.
  **⚠️ THE HORIZON IS NOT THE HOLD.** It deliberately ignores the exit: "what
  did the underlying do in the next N minutes", not "what did we make". A
  trigger can drift well and still lose money to a bad stop — **that separation
  is the whole point, and MFE/MAE cannot provide it** because they are
  premium-based and bounded by the exit.
  **⚠️ THE RANDOM ARM IS THE NULL.** Drift is also measured from random ticks on
  the same symbol-days, seeded for reproducibility. Without it "ORB drifts
  +0.05%" is unreadable — the question is whether it drifts MORE than an
  arbitrary moment on the same tape.
  **⚠️ TIMEZONE — the trap that already inverted one verdict in this repo.**
  `entry_time` is UTC by deliberate design; the replay corpus stamps `ts` as ET
  wall-clock. Converted with `zoneinfo`, never a fixed offset (a fixed −4/−5 is
  wrong on one side of every DST boundary), and if `zoneinfo` is unavailable the
  tool REFUSES to guess rather than silently mis-matching. Unmatched triggers are
  DROPPED AND COUNTED, never snapped to a neighbouring minute.
  **PROVEN ON PLANTED DATA:** a +0.02%/bar window with ORB Long triggers inside
  it and "noise" triggers outside → ORB Long median **+0.200%, 100% positive**,
  noise **−0.010%**, null arm **0.000%**, 40/40 triggers matched through the
  conversion.
  **WHAT EACH OUTCOME MEANS.** ORB well above the null → the instrument works,
  and the label-state nulls become a real finding about labels. ORB at the null
  → the instrument is blind and `a2_cooccurrence`'s result must be withdrawn,
  not acted on.

- `[DESK]` **AX.3 — 🟡 KEEP `direction_conf`, KILL `pair_conf`, EMIT THE AXES.**
  **WHAT DIED, and it is recorded so it stays dead.** `pair_conf = min(direction,
  volatility)` measured at gap **+0.001** against `direction_conf`'s **+0.188**
  over 571 trades — the WORST of the three, the opposite of the hypothesis. The
  failure is STRUCTURAL, not tunable: the volatility axis is at or near zero on
  most ticks (BREAKOUT exactly 0 on 63.8%, COMPRESSION on 79.5%, `is_expanding`
  true on 9.6% of shadow ticks), so `min()` over a sparse axis collapses toward
  zero and DESTROYS what the direction axis carried. It is retained in the
  payload ONLY so `axis_crosstab.py` still runs, and now ships with
  `pair_conf_status: "DEAD — does not separate; use direction_conf"` so a future
  caller cannot read a plausible float and build on a measured dead end. A test
  pins that marker. Any rescue variant needs independent justification — fitting
  one to this failure is the re-litigating the marker exists to prevent.
  **WHAT SURVIVED, and it is the bigger result.** `direction_conf` — the RAW
  Layer-1 direction score — separates favourable from never-favourable at
  **+0.188 on n=571**, roughly double the best separation found anywhere else
  (`setup_score`'s best cell 0.80 vs 0.91; `regime_conviction` 0.99 vs 1.00,
  flat). **The RAW score separates where the INTEGRATED conviction does not**,
  which points at Layer-2 integration as a possible destroyer of signal.
  **AND TWO CELLS THE FUSED LABEL WAS BURYING.** As a LABEL, TRENDING_BEAR is the
  worst regime in the book (95 trades, 35%, **−$6,137**); as an AXIS, BEAR totals
  149 trades at **+$4,391**, driven by **BEAR/EXPANDING at +$5,059** — the best
  cell in the table. And RANGING splits cleanly on volatility: RANGE/EXPANDING
  **+$1,619** vs RANGE/NEUTRAL **−$2,752** (50% never-favourable, the worst rate
  here). Same underlying scores, opposite verdicts.
  **PLACEMENT FINDING:** `trend_continuation_standalone` puts **51% of its 136
  trades in BULL/EXPANDING**, the largest cell and a −$2,334 one. That is a
  concrete mechanism for its negative drift — not diffusely bad, concentrated in
  the worst high-count cell.
  **NEXT — NOT BUILT:** emit `direction`, `direction_conf`, `volatility`,
  `volatility_conf` onto the signal journal so `direction_conf`'s +0.188 can be
  confirmed OUT-OF-SAMPLE on forward sessions. Log-only; anything that GATES on
  it is post-freeze. ⚠️ In-sample separation is a hypothesis, not a threshold —
  the same discipline the floor sweep refuses to break.

- `[SCHEDULE]` **ONE-WEEK SLIP — DECIDED 2026-08-07.** Operator: *"I have
  decided to slip everything to the right by one week, to account for the major
  engine changes this week for intraday regime flips and blocked strategies that
  had to be un-gated."*
  **FREEZE 2026-08-21 → 2026-08-28 · GO-LIVE (tiny size) 2026-08-31 →
  TUESDAY 2026-09-08 · FULL SIZE 2026-09-14 → 2026-09-21.** Every epoch boundary
  moves with them.
  **WHY TUESDAY AND NOT MONDAY:** a straight one-week slip lands go-live on
  Mon 2026-09-07, which is **Labor Day — US markets closed**. The choice was
  Tue 09-08 (first open after the slipped date) or Mon 09-14 (holds the
  Monday-rollout convention but costs a second week and collides with the old
  full-size date). Operator chose Tuesday; the Monday convention is deliberately
  broken this once.
  **WHY THE SLIP IS RIGHT:** the freeze exists to bank a STATIONARY window, and
  the engine stopped being stationary on 08-06. This week landed
  conviction_integrator v2.1 (F7), SWP.1, CNT.1, CNT.2 and now RGM.3. Freezing
  on 08-21 would have banked ~2 sessions of post-change behaviour; 08-28 banks
  ~7.
  **⚠️ EVM READING:** every dated item shifts, so PV recomputes and SPI will
  JUMP on the first run after these dates land. **That jump is a RE-BASELINE,
  not recovered schedule** — brief it as such. And pass `--asof` explicitly:
  control runs UTC, the operator is Central, so after ~19:00 Central an
  unqualified run briefs tomorrow's PV.

- `[DESK]` **RGM.3 — 🟡 SHIPPED-NOT-BAKED. SWEEP_REVERSAL LEAVES THE REGIME
  SET.** Operator, twice: *"why is sweep reversal a regime when it's a strategy?
  Like, where did that even come from?"*
  **THE DOCUMENTATION ALREADY AGREED.** `docs/MECHANICS.md:304` heads its own
  section **`SWEEP_REVERSAL (event overlay — hard-veto triple × age-decay)`** —
  the only one of the six the docs do not call a regime. It was modelled as an
  EVENT, correctly, and filed in the `Regime` enum anyway, next to `UNKNOWN`
  which was later eliminated. The enum is a grab bag, not a taxonomy.
  **AND IT COULD NEVER HAVE WON.** It is the only scorer carrying an AGE-DECAY
  soft-necessary — `0.5 ** (sweep_age_bars / SWEEP_HALFLIFE_BARS)`, half-life
  **3 bars** — so its score HALVES every three minutes by construction. A
  decaying score entered into an argmax against persistent states that peg at
  1.0 loses structurally, not by tuning. Measured on the 08-07 replay (11,231
  ticks, 29 symbol-sessions): SWEEP non-zero on **22%** of ticks yet
  **p50 0.0, p90 0.0, max 0.265, dominant 1%** against TRENDING_BULL's max 1.0 /
  dominant 31%.
  **WHAT CHANGED — conviction_integrator v2.2:** `INTEGRATED_REGIMES` 6 → 5,
  `_TIEBREAK_ORDER` loses SWEEP, its `RegimeParams` row is removed.
  **THE SCORER IS UNTOUCHED** — `regime_confluence._sweep` still runs every tick
  and its score still reaches `ctx["l1"].scores`, because **SWP.1's dispatch
  gate now DEPENDS on it**. This changes what can be EMITTED, nothing about what
  is measured. A test pins the scorer's continued existence for exactly that
  reason: deleting `_sweep` as "no longer a regime" would take the sweep trade
  dark again and raise nothing.
  **⚠️ THE TIE-BREAK HEAD MOVES, and this is the quiet win.** SWEEP was FIRST,
  so on an all-zero tick the emitted label WAS SWEEP_REVERSAL — the
  least-supported regime won precisely the 4.2% of ticks where the engine knew
  nothing. The head is now BREAKOUT_VOLATILE, at least a state the tape can
  actually be in.
  **⚠️ SIDE BENEFIT:** `stale` clears only when EVERY integrated dimension is
  non-None. With sweep out, a None sweep score can no longer pin the book
  stale — the same failure class that made L2 unreachable for weeks. Pinned by a
  test.
  **⚠️ EVERY POOLED PER-REGIME STATISTIC IS NOW ON A DIFFERENT BASIS** and is
  NOT comparable to the 12-session history banked before this. Say so in the
  first post-bake rollup rather than letting a shifted distribution read as a
  behaviour change.

- `[DESK]` **CNT.2 — 🟡 SHIPPED-NOT-BAKED. THE INSURANCE GATE FOR CONTINUATION.**
  Operator's call 2026-08-07: *"BOS being unable to save a trade that went bad
  out of the gate — that is correct. So we need a smart insurance policy for
  that situation."*
  **THE HOLE IS EXACT AND OBSERVABLE.** `BOSTracker.protected_level` starts
  `None` and is set only when the trade makes a new CLOSING HIGH past entry. So
  BOS (gate 2b) — continuation's thesis invalidator, deliberately UNGATED on
  P&L — is structurally BLIND on a trade that goes wrong from the first tick.
  That is precisely the population that runs to the floor: **45 trades, realized
  −29%, MFE +1%.**
  **THE HANDOFF NEEDS NO TIME WINDOW.** 2c arms ONLY while
  `protected_level is None` and disarms permanently the instant BOS has a level
  to defend. No overlap, no double jeopardy, no arbitrary N-minute knob — the
  condition IS the blind window.
  **THE LEVEL WAS ALREADY COMPUTED AND WAS DEAD CODE.**
  `continuation_strategy:447/450` stamps
  `underlying_stop = gap.bottom − 0.5*atr` (long) / `gap.top + 0.5*atr` (short)
  at entry; `trade_logger:206` persists it; the ONLY reader was `query.py:233`,
  for display. Zero new telemetry.
  **STRUCTURAL, NOT PREMIUM-PERCENT — and that is the whole point.** A tighter
  premium floor was MEASURED to net ≈ −0.15 units because it cuts winners that
  merely dip (peak is late, drawdown early). This level is the ENTRY PREMISE
  INVERTED: continuation enters on a pullback INTO an unfilled 5m FVG expecting
  resumption, so a close beyond the far edge plus a half-ATR buffer means the
  pullback was the reversal continuing. Reads `iloc[-2]` — the same fully-closed
  candle BOS reads, so the two gates cannot disagree about what price did.
  **IT DOES NOT REOPEN THE JULY DECISION.** `underlying_stop` was rejected as
  THE exit because "a gap fill is NOT trend failure" and "the FVG level is
  STATIC so it protects nothing once the trade works". Neither objection applies
  to a gate that lives only while BOS is blind and yields the moment it wakes.
  This fills the hole that decision knowingly left.
  **⚠️ THE LEVEL HAS NEVER BEEN READ BY ANYTHING THAT TRADES** — no track
  record, treat as an untested prior. Exits tag `insurance_stop` so the rollup
  scores it apart from `max_loss_floor` (45) and `bos_exit` (111). Kill switch
  `OT_CONT_INSURANCE=0`.
  **⚠️ MAGNITUDE NOT YET QUANTIFIABLE.** Pricing it needs per-trade replay of 1m
  tape against the stamped level; stored MFE/MAE cannot answer it. The only
  anchor is that `bos_exit` trades die at MAE **−5%** against the floor's
  **−29%**.
  **BUILD NOTE:** `_bos` construction was hoisted OUT of the `df_1m is not None`
  guard so 2c cannot reference an unbound name — the same NameError class as
  defect W. Pinned by a test.

- `[DESK]` **CNT.1 — 🟡 SHIPPED-NOT-BAKED. CONTINUATION MAY NOW FIRE UNDER
  BREAKOUT_VOLATILE.** Operator's call 2026-08-07: *"I want to ungate the
  continuation trade on breakout to gather data. Let's assign it the
  direction."*
  **THE BAR WAS STRUCTURAL, NOT A QUALITY JUDGEMENT.** `continuation_strategy`
  derives direction FROM THE LABEL — `TRENDING_BULL → long/call`,
  `TRENDING_BEAR → short/put`, `elif is_handoff → the runaway's direction`,
  `else return None`. BREAKOUT_VOLATILE asserts volatility EXPANSION and says
  nothing about which way, so there was no branch that could assign one. Nobody
  ever decided breakout tape was poor continuation tape.
  **THE FIX TAKES THE MISSING HALF FROM THE TREND ENGINE** — `trend.overall_
  direction` (BULLISH/BEARISH; NEUTRAL self-vetoes), the same field `_sweep`
  already reads to compute `opposed`. This is the runaway handoff's move,
  sourced from the vote rather than from the ORB.
  **⚠️ WHY AN ADX BAR AND NOT THE CONVICTION FLOOR — the trap this avoids:**
  under a non-trending label `_label_trending` is False, so continuation's
  `CONTINUATION_CONV_FLOOR` check is **SKIPPED ENTIRELY** — the identical hole
  the handoff path carries. Falling back to `regime.conviction` would be worse
  than nothing, because under BREAKOUT that is BREAKOUT's conviction, not the
  trend's. Direction comes from the trend engine, so the quality bar comes from
  there too: `primary_adx >= CONT_BREAKOUT_MIN_ADX`, default **25 =
  ADX_TREND_THRESHOLD**, the same bar the rest of the system uses to call a
  trend a trend. A PRIOR, not a fit.
  **⚠️ ENTRIES ARE TAGGED `trend_continuation_breakout`.** The point of turning
  this on is to COLLECT DATA on it; pooled under `_standalone` it would be
  invisible against 141 trades of existing history. Pinned by a test.
  **WIDENING THE DISPATCH TUPLE ALONE DOES NOT OPEN THE TRADE** — the strategy's
  direction branch does, and it self-vetoes on a directionless tape. Also pinned.
  Kill switch `OT_CONT_BREAKOUT_DIRECTION=0`.
  **CONTEXT FROM THE 11-SESSION ROLLUP that makes this worth watching closely:**
  continuation's entire loss is the SHORT side — TRENDING_BULL/Continuation 193
  trades **+$19**, RANGING/Continuation 82 **+$578.50**, BREAKOUT/Continuation
  (handoff only, today) 48 **+$12**, but **TRENDING_BEAR/Continuation 57 trades
  −$3,035.50**. So the new path's SHORT entries are the ones to score first, and
  the separate tag is what makes that possible.

- `[DESK]` **SWP.1 — 🔴 OPEN. SWEEP MUST STOP GATING ON REGIME.** Operator
  ruling 2026-08-07: *"Sweep isn't a regime. The trade should only require a
  move into a named liquidity pool/level, accompanied by a rejection or
  exhaustion. I never asked for a regime called 'sweep'."*
  **THE RULING IS RIGHT AND THREE INDEPENDENT LINES ALREADY SAID SO:**
  `auto_label` treats SWEEP as a SINGLE-EVENT tag; `label_agreement`'s own notes
  record that BREAKOUT and SWEEP are "single-event properties, not
  session-dominant states"; and the census has SWEEP winning **0.4% of live
  ticks** with **96% exact zeros**. A regime is a persistent condition of the
  tape; a sweep is a thing that happens at 10:47. Filing it as a regime was a
  category error, and the 96% zero rate is what that error looks like in data.
  **THE TRADE IS GATED TWICE**, both on the label: `main.py` ~1325
  (`regime.primary_regime == Regime.SWEEP_REVERSAL`) and
  `sweep_reversal_strategy.py:121`. And it sits at Priority 2.5 behind
  `if signal is None`, so ORB and Continuation both get first refusal.
  **F7 NARROWED IT FURTHER — a predictable cost of the emission fix.** Under
  v2.0 the label could flip to SWEEP on a momentary argmax at conviction 0.05;
  under v2.1 a challenger needs 0.65 AND a 0.12 margin, which a regime scoring
  zero 96% of the time will rarely reach. The agreement gate's one recorded
  debit — SWEEP in-family falling 3.5% → 1.3% — was the leading indicator, and
  it was explained away rather than heeded.
  **⚠️ THE PLTR PROTECTION IS INSIDE THE SCORE, NOT THE STRATEGY.**
  `regime_confluence.py:680` computes `trend_opp = 1.0 - (opp_adx * opp_mom)`
  and passes it as `soft_necessary`. Fully opposed → 0 → SWEEP annihilated →
  label never commits → gate never opens. **So the regime gate is currently
  CARRYING the trend-opposition protection** from the 07-27 PLTR incident
  (shorted a +7.2% up-trending tape, −27.8%). Remove the gate without
  relocating it and that failure mode returns. NON-NEGOTIABLE.
  **HOW — use the L1 `_sweep` SCORE as the gate AND the conviction, without
  requiring it to win the argmax.** `_sweep` already computes exactly the
  operator's condition set: named-level match, `rejq_val`, `exh_val`,
  `age_decay`, `trend_opp`. `main.py` already computes the full confluence every
  tick, so the score and breakdown are ALREADY IN HAND — passing them costs
  nothing. That solves all three dependencies at once: trend_opp travels WITH
  the score, the strategy gets its own setup conviction for
  `_sweep_target_delta` (today it reads `regime.conviction`, which after
  ungating would be the AMBIENT regime's conviction — a nonsense input to sweep
  strike selection), and the label gate disappears.
  **✅ BUILT 2026-08-07 — the floor came from the corpus, not from a guess.**
  19 sessions / 523 symbol-days: SWEEP is non-zero on **4.0%** of ticks
  (7,555 of 186,582 — 96% annihilated), and of those p25=0.004, p50=0.016,
  p75=0.068, p90=0.154, p99=0.489, max=0.717. Floor table (ticks / sym-days /
  ticks-per-symday): 0.05 → 2193/78/28.1 · 0.10 → 1294/68/19.0 · 0.20 →
  544/50/10.9 · 0.30 → 265/29/9.1 · 0.50 → 70/10/7.0.
  **SHIPPED `SWEEP_SETUP_FLOOR = 0.05`** (env `OT_SWEEP_SETUP_FLOOR`), chosen
  MAX-PERMISSIVE for the collection phase per the operator, to be tightened on
  live fires.
  **THE STRUCTURAL ARGUMENT FOR A LOW FLOOR, which is the real justification:**
  `_sweep`'s three hard vetoes are `veto_loc` (a NAMED level), `veto_reclaim`
  (rejected back through) and `veto_accept` (not accepted beyond). All three
  must pass for the score to be non-zero at all — so **every non-zero tick
  already satisfies the operator's stated spec verbatim.** Magnitude above zero
  is quality grading, not qualification. 0.05 is a thin noise guard over
  `score > 0`, not a quality bar.
  **PERMISSIVENESS CANNOT PRE-EMPT OTHER SETUPS:** sweep remains Priority 2.5
  behind `if signal is None`, so ORB and Continuation always take first refusal.
  A loose floor risks bad sweep trades in the GAPS, never stolen ones. Pinned by
  a test.
  **THE OPERATOR'S EXHAUSTION ASYMMETRY WAS ALREADY IN THE CODE** and needed no
  change — only unblocking. Two terms, both keyed on
  `trend_state.primary_momentum`: `opp_mom = {ACCEL 1.0, FLAT 0.6, DECEL 0.25,
  "" 0.8}` feeding `trend_opp`, and the corroborator `exh_val = {DECEL 1.0,
  FLAT 0.5, ACCEL 0.0, "" 0.0}`. As the opposing move decelerates, suppression
  falls AND corroboration rises — sweep conviction climbs exactly as
  continuation's thesis dies, which is what the operator described.
  **⚠️ BUT THE `""` CASE DOUBLE-PENALISES, AND IT IS THE NEXT THING TO MEASURE.**
  With no 5m momentum vote: `opp_mom = 0.8` (near-full suppression) AND
  `exh_val = 0.0` (zero corroboration) — and `exh_val` is one of only TWO
  corroborators, so a missing vote both crushes the multiplier and removes half
  the evidence. Missing data reads as "accelerating against you". This is a
  prime suspect for the 96% zeros and is the same family as the known
  "trend vote STARVED" / align_frac 0.67 ceiling. **MEASURE: the distribution of
  `breakdown.SWEEP_REVERSAL.momentum` on ticks where all three hard vetoes
  passed. If `""` dominates, the ungating alone will not revive the trade.**
  **WHAT SHIPPED:** config v4.2 (the knob) · main v5.6 (captures the full
  `ConfluenceResult` into `ctx["l1"]` — `evidence()` already called `score()`
  internally so it costs nothing — and gates on
  `_sweep_setup >= SWEEP_SETUP_FLOOR`) · sweep_reversal_strategy v3.3 (in-strategy
  label gate removed; new `setup_score` kwarg becomes the strategy's conviction,
  threaded through both `_long_reversal` and `_short_reversal`) ·
  `tests/test_sweep_ungated.py` (6 tests, including a canary asserting
  `trend_opp` is still soft-necessary, because losing it re-opens PLTR silently).
  **TWO ERRORS CAUGHT IN-BUILD AND WORTH KEEPING:** (1) the first patch defined
  `conv` in `generate_signal` and used it inside the builder methods where it
  was out of scope — the same NameError class as defect W and the `mid` incident;
  (2) the first absence-check test failed against CORRECT code because main
  v5.6's changelog *quotes the very line it removed* — a canary that fires on
  documentation is worse than none, so the tests now strip the module docstring
  via `ast` before scanning.
  **⚠️ THE FLOOR SHOULD STILL COME FROM DATA WHEN IT IS TIGHTENED.** The old gate was effectively "wins the
  argmax". Post-excavation pooled sweeps were WEAK (old max 0.125), so a
  0.55-style floor blocks everything and 0.05 fires on noise.
  `tests/sweep_score_dist.py` v1.0 prints the nonzero-score distribution and
  what each candidate floor would admit, in ticks and in symbol-days. Ship the
  choice as a stated PRIOR behind `OT_SWEEP_SETUP_FLOOR` (operator's category 1
  — set a baseline where none exists), not as a fit.
  **⚠️ SECOND DEFECT FOUND IN THE SAME LOG SWEEP, unrelated to the gate:**
  `select_sweep_strike` logs `band empty->nearest` constantly and lands on
  deltas from **0.19 to 0.55** against a 0.45 target, because
  `SWEEP_DELTA_TOLERANCE = 0.04` is empty on most chains. That is degrading
  CONTINUATION staged picks today and will degrade sweep the moment it fires.
  **⚠️ A LOG LINE THAT LIES:** `select_sweep_strike` is a SHARED selector and its
  message names the FUNCTION, not the caller — so continuation's staged picks
  emit thousands of lines a day reading "Sweep strike:". Rename it or add the
  caller. It cost a wrong conclusion in this very session.

- `[DESK]` **MEM.1 — 🔴 OPEN. THE SPX OPTIONSBOT LEAK IS REAL, ISOLATED AND
  MEASURED.** Two option-14 RSS samples 16.4 minutes apart, 15 boxes:
  **fourteen FLAT** — most moved by kilobytes, and MU **−1.9 MB** / NVDA
  **−4.5 MB** actually FELL, which is what a healthy allocator returning memory
  looks like. **SPX went 297,532K → 390,984K = +93.5 MB = 5.7 MB/min.**
  **QQQ IS THE CONTROL THAT CLOSES IT:** comparable chain, also ALWAYS_ON,
  **+8 KB in 16 minutes.** Growth is therefore NOT proportional to chain size —
  it is binary. SPX retains, QQQ does not.
  **THIS EXONERATES THE F7 BAKE.** All 15 boxes run conviction_integrator v2.1
  as of 08-06 night; a fleet-wide change cannot produce a one-box leak, and the
  08-06 OOM predates the bake. The amplification worry (F7 holds positions
  longer → more open-position chain lookups) is downgraded, NOT closed.
  **THE CEILING IS PHYSICAL RAM, NOT A CGROUP LIMIT:** `MemoryMax=infinity`
  fleet-wide, boxes are 951 MB with **ZERO SWAP**, and every box already sits at
  73–79% used with ~200–250 MB available. No swap means no degraded stage — the
  kernel goes straight from tight to `status=9/KILL`, and it picks the largest
  RSS. That is why the peak reads an identical 419M on both 08-06 and 08-07: not
  a cap being hit, but the level at which optionsbot + candle-feed + OS exceeds
  951 MB.
  **ARITHMETIC OFFERED AS CONSISTENCY, NOT EVIDENCE:** 5.7 MB/min over a 15s
  tick is ~1.4 MB retained per tick; a 724-option SPX chain at ~2 KB/object is
  ~1.4 MB — the size of exactly one full chain build. Source reading came up
  EMPTY (`_struct_cache` is keyed by symbol and overwritten, `chain_snapshot`
  holds one string bucket), which is exactly why the next step measures.
  **HOW — `tests/mem_tracer.py` v1.0, BUILT 08-07, NOT YET RUN.** Drives the
  real per-tick sequence from main.py's GEX block (`fetch_chain` →
  `compute_gex` → `chain_snapshot`) under `tracemalloc`, diffing a WARM
  reference against a later snapshot so first-tick caches that are SUPPOSED to
  persist are not counted as a leak. Reports the top sites by retained size with
  file:line and a full traceback. Diff machinery proven against a planted 10 MB
  leak (recovered 10.0 MB, correct site).
  **IT ALSO REPORTS RSS ALONGSIDE THE TRACED TOTAL, and that divergence is a
  finding in its own right:** if RSS climbs while traced memory does not, the
  retention is NOT in Python objects — a C extension, allocator arena
  fragmentation or unclosed handles — and the answer is a different tool, not a
  different guess.
  **⚠️ RUN CONSTRAINT, ENFORCED IN CODE:** the probe is a SECOND ~200 MB process
  on a 951 MB box with ~206 MB available and no swap. Running it beside the live
  bot can itself trigger the OOM killer, which would pick the LIVE bot as the
  largest RSS. It refuses to start below `--min-avail-mb` (default 320). Either
  stop optionsbot on SPX for the run, or **resize the box first** — resizing is
  reversible and is wanted anyway if the verdict is structural.
  **⚠️ SWAP IS NOT THE REMEDY HERE.** A swapfile delays 5.7 MB/min by hours; it
  does not stop it. Worth having fleet-wide as a cushion, filed separately.

- `[DESK]` **RGM.2 — 🔴 OPEN. THE LAYER-1 DISCRIMINATION PROBLEM.** F7 stops the
  LABEL thrashing; it does nothing about the EVIDENCE the label is chosen from.
  The operator's framing and it is the right one: recognition is fast but it is
  not DISCRIMINATING, and a stable label chosen from an undiscriminating vector
  is still a guess — just a steadier one.
  **THE MECHANISM IS THE GRAMMAR.** A hard veto at 0 does not merely lower a
  score, it **destroys the ordering**: every vetoed regime lands on the same
  value, so two regimes at 0.00 are not "weak by different amounts", they are
  indistinguishable. F3 already showed 45.7-96.0% of scores sit at exactly 0
  per regime; what is NOT yet known is the property of the VECTOR — on a given
  tick, is there anything to choose between?
  **HOW (step 0, built 08-07, NOT YET RUN):** `tests/discrimination_census.py`
  v1.0 reads the `scores` block already in the corpus — no engine run. Reports
  (1) DEAD TICKS, all six at exactly 0, where the label falls to
  `_TIEBREAK_ORDER` whose head is SWEEP_REVERSAL, a regime above zero on 4% of
  ticks — a material share here is the same family of silent defect as the
  case-mismatch gate that made L2 unreachable for weeks; (2) zero-argmax ticks;
  (3) SEPARATION, the #1−#2 gap, computed with dead ticks EXCLUDED so a
  degenerate vector cannot masquerade as a close contest; (4) live regimes per
  tick. Proven on planted data with every count recovered exactly.
  **HOW (step 0b, NOT BUILT):** the conviction distribution AT ENTRY, from the
  signal journal. L3 gates on conviction, so if entries only fire high the
  undiscriminated half of the session is already being declined and the harm is
  bounded; if entries fire near 0.3 the gates are not protecting and this
  jumps the queue. **This is the number that sets RGM.2's priority.**
  **THE THREE FIX FAMILIES, once the census names the shape:**
  **A — targeted veto softening** (floor or steep ramp instead of
  annihilation), which preserves ordering. Must be SELECTIVE and evidenced per
  veto: REGIME_TRUTHS §0 holds that premium regimes deliberately keep mass in
  vetoes because the expensive error is CLAIMING the regime, and the v1.3
  excavation already proved a blanket re-slot backfires (COMPRESSION scored
  0.25 on wide-band RANGE tape). Small enough to land pre-freeze IF one or two
  vetoes dominate.
  **B — change the accumulation seam.** `_combine()` is the SINGLE seam all
  five scorers route through, so log-odds / noisy-OR is a one-function change,
  not another excavation: a strong negative becomes a large negative
  contribution rather than an annihilator and the vector stays ordered. This is
  closest to the 07-27 intent — "a departure from Boolean architecture toward a
  truly conviction-scaled consensus model". **POST-FREEZE.**
  **C — split into AXES** rather than six mutually-exclusive labels. A2.R
  established cross-horizon co-occurrence is a REAL state, so forcing one
  argmax collapses a truth the tape supports. Emit trendiness / volatility
  expansion / location and let each strategy gate on the axis it needs.
  Architectural — realistically **POST-GO-LIVE**.
  **⚠️ CALENDAR HONESTY:** B and C are not landing before 08-31. Only the
  census, step 0b, and possibly a narrow A fit before the freeze.
  **⚠️ WHAT THE CENSUS CANNOT SAY:** not that the scores are WRONG. A veto
  that fires often may be correctly describing a condition that genuinely comes
  and goes. It measures whether there is information to RANK with;
  `label_agreement.py` asks whether the ranking is right, and
  `veto_attribution.py` asks which veto did it.

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
  🔴 **PREMISE CORRECTED 2026-08-15 (FEED.2, v4.89):** "no overnight tape exists
  historically" was true only because the feed requested `tho=true`. FORWARD of
  the FEED.2 bake the tape exists, so the ON tier can be validated on collected
  data rather than shipping purely as a prior — but **nothing before that bake
  can be retro-validated**: DXFeed history is same-evening only and those nights
  were never captured.
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
- `[DESK]` **VW.1f — three defects the VWAP ledger's own first output exposed.**
  Filed as scope on 2026-08-08 rather than patched on the spot, because nothing
  on the fleet depends on it and the last time this tool was patched a layer at
  a time it cost five versions. **(a) ~29 trades vanish silently** — 304 rows
  minus 40 reported unjoinable leaves 264 mappable, but only 235 join; a trade
  that maps to a family yet never matches a signal group is dropped with no
  by-cause line, which is the exact gap by-cause reporting was built to close.
  Add a MAPPED-BUT-UNMATCHED count. **(b) The mixed-eras warning cried wolf on
  its first outing** — all three dates were pre-bake and `[era] emitted 9,596`
  is exactly TCS's own total, so the split was BY TRACK, not by date; warn only
  when a SINGLE track shows both. **(c) The verdict floor tests TOTAL trades,
  so a verdict printed off a 5-trade arm** — require a floor on both arms, and
  say in the caveat that the majority-alignment collapse systematically shrinks
  the minority arm the verdict rests on. Ships as ledger v1.6.
- `[DESK]` **CV.1 — two canary reds on a PRISTINE clone.** `check_versions.sh`
  pins `v5.4 main header current` while `main.py` is at **v5.8**, and one canary
  expects `tests/condor_plan_lifetime.py`, which does not exist. Not introduced
  by any 08-08 delivery — reproduced on a clean clone. The cost is that the
  sweep now ends `DONE — 2 CANARY/PARITY FAILURE(S)` on a clean checkout, so
  **its DONE banner has stopped being usable as a gate** — WORKING_AGREEMENT §17,
  an alarm that cries wolf is one that gets filtered. Re-point the pin to v5.8;
  delete or restore the orphaned canary. Two one-line edits.
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

### EPOCH 2 — CALIBRATE & FREEZE — Mon Aug 17 → Sun Aug 30

*Goal: one consolidated calibration deploy Monday, then hands off L1/L2/entry
logic for two weeks. Everything else this epoch is offline or log-only — which the
roadmap explicitly permits during the freeze (L3.1/L3.2/P3 phase 1 drive nothing).*

**✅ Tue Aug 11 — FIRST SESSION ON FIVE BEHAVIOURAL CHANGES — CLOSED**

**THE SESSION READ (the day's first item, done):** 21 trades, **+$1,182.50**,
48% win, median hold **16.3 min** — against 08-10's 92 trades at −$596 with a
3.0 min median. **6x fewer trades, 5x longer holds, profitable.** Continuation
went from worst strategy in the book to best (13 trades, +$2,433);
`continuation_trail` 9 trades / 78% / +$2,958; `bos_exit` 35 → 1; `regime_flip`
19 → 2. Zero RANGING and zero COMPRESSION trades — CNT.6 accounts for both.
**THE LOSS IS ENTIRELY ORB: 7 trades, 29%, −$1,291**, concentrated in
`orb_structure_stop` (5, 0% win, −$1,700) and BREAKOUT_VOLATILE/ORB (−$1,130).
Untouched by anything shipped and it is the next cell to look at.
⚠️ Every bucket is thin; one session. And the exit-behaviour note stands:
winners held 17.3 min vs losers 15.0 — **exits may still be cutting runners as
fast as mistakes.**

**✅ SHIPPED AND PUSHED TODAY** (all baked except where noted):
- `[DESK]` **CNT.7 ✅ SHIPPED 08-11** — ATR-scaled tolerance on the confirmation bar. The strict
  comparison was rejecting TIES by 3-9 cents (QQQ 0.011%, PLTR 0.023%). 0.40 ATR
  derived from a clean gap in the logged misses: ties 0.073-0.360, genuine
  failures 1.133-3.355.
- `[DESK]` **BFLY.1 ✅ SHIPPED 08-11** — butterfly readiness scores the GEX-PIN thesis, not the
  COMPRESSION label. It was reporting would_fire=2132 against ONE trade because
  it graded a different trade entirely.
- `[DESK]` **LIQ.1 ✅ SHIPPED 08-11** — London/Asia out as sweepable pools (London overlaps RTH by
  2.5h, so its "level" was set by the price being traded); dedupe now keeps the
  NAMED twin (it was zeroing the sweep score on textbook raids).
- `[DESK]` **LIQ.3 ✅ SHIPPED 08-11** — running invalidation replaces the clock. 32.9% of the
  stale sweeps the 8-bar gate refused still had a LIVE thesis.
- `[DESK]` **SWP.4 ✅ SHIPPED 08-11** — recovery anchored to the reclaimed LEVEL, not the wick.
- `[DESK]` **SWP.5 ✅ SHIPPED 08-11** — liveness gate; age survives only as a 4h backstop.
- `[DESK]` **RGM.6 ✅ SHIPPED 08-11** — the fallback resolves to the L1 argmax, not UNKNOWN.
- `[DESK]` **DEVTOOLS ✅ SHIPPED 08-11** — v1.28 `ask_scope` tolerates spaces after
  commas; a space was SILENTLY TRUNCATING the symbol list and running on the
  wrong boxes.
- **TOOLS (read-only):** `condor_block_attribution`, `sweep_opportunity_audit`
  v1.1, `rgm5_fallthrough`, `sweep_score_dist` (existing, re-used).
- **INFRA:** 1GB swap on all 28 t2.micro boxes (SPX already had 2GB). MEM.2
  closed — no leak, ~710MB steady state, undersized box.

**⬜ UNRESOLVED — CARRIED OUT OF TODAY**
- `[DESK]` **SPX INSTANCE UPGRADE TO t3.medium — not yet done.** ~710MB steady
  state against 1905MB total with 649MB free; it has OOM'd twice. Swapfile is on
  the EBS root and survives the stop/start. Its root disk is also tight
  (`disk_avail=647M` vs ~1700M elsewhere) — grow the volume in the same stop.
- `[DESK]` **SWEEP REFUSALS ARE INVISIBLE: 9 of 11 paths in
  `sweep_reversal_strategy` are `logger.debug` against `LOG_LEVEL="INFO"`.**
  Every investigation today was elimination-by-reading because those lines do
  not exist. Promoting them is one file, log-only, freeze-safe — and it would
  make the next drought one grep instead of an evening.
- `[DESK]` **⚠️ SWP.3's LONDON BONUS IS FITTED TO AN ARTEFACT.** It was weighted
  on the shadow observer's 61.3% London share, and LIQ.1 established London was
  NEAREST BECAUSE IT TRACKED PRICE. Treat as a CORRECTION, not an option.
  Label/entry-affecting ⇒ **Mon Aug 17 deploy deadline**.
- `[DESK·DATA]` **`SWEEP_STALE_HARD_BARS = 48` (4h) IS A PRIOR** — nothing in
  the data picked it, and 414 setups hit it across 90 symbol-days. First number
  to re-derive once live data exists.
- `[DESK·DATA]` **THE LIQ.1 DEDUPE BUG'S LIVE INCIDENCE IS UNKNOWN.** The 08-11
  corpus shows `veto_loc` PASSING on 99.6% of ticks, so it is real but may be
  rare. Do not read it as the whole explanation for the drought.
- `[DESK·DATA]` **TWO TOOLS DISAGREE ON `scores.SWEEP_REVERSAL`** — same field,
  same date: `sweep_score_dist` reports nonzero p50 0.008 / p90 0.083;
  `sweep_opportunity_audit` reports p50 0.000 / p90 0.002. One is wrong.
  **Resolve before anyone moves a sweep floor on either.**
- `[DESK]` **THE ORB 11:00 CUTOFF — three perfect setups missed on 08-11**
  between 11:00 and 12:00, all second attempts after an earlier stop. The
  engine already counts `attempt_number` and already re-arms on a close back
  inside, so the ONLY thing blocking a second setup is the same 11:00 constant
  that gates entry. Operator's prior: the second presentation is usually the
  better one. **Measurable from banked data — ORB trades by `attempt_number`,
  never-favourable rate — before touching the constant.**
- `[DESK·DATA]` **VERIFY RGM.6 TOMORROW: does UNKNOWN fall toward its ~2.4%
  floor?** The engine tag is now FOUR states — `[L2 c=]` / `[L2-hold c=]` /
  `[L1 c=]` / `[v13]`. `grep -c '[v13]'` has been the fallback-rate measure all
  week; **a drop in it is a RELABELLING, not a fix.** Count all four.
- `[DESK·DATA]` **BUTTERFLY: gates 1x5 are the likely blocker, not the regime.**
  SPX logged `env=PINNING` at 15:29 ET — 90 minutes after the 12:00-14:00 window
  shut. GEX pinning is structurally late-day; the window is midday. Measure when
  PINNING appears against the window before moving either.
- `[DESK·DATA]` **CONDOR: the plan formed and the LEGS never triggered.** AAPL
  11:11:00, conviction **0.1549**, triggers ±0.8% from spot. The regime gate is
  not the blocker (224 RANGING ticks fell inside the window). Two open
  questions: whether a conviction FLOOR belongs on the plan gate (it reads the
  label only), and whether `CONDOR_TRIGGER_APPROACH = 0.65` is reachable in a
  range tight enough to be worth trading.
- `[DESK·DATA]` **THE 21.3% ORB RISK-LEG WIDENING IS STILL UNEXPLAINED** —
  measured 08-08, cause never identified, and the boundary-alignment change that
  might have addressed it was correctly REJECTED on backtest.

**⬜ Tue Aug 11 — ORIGINAL PLAN (both items closed)**
- `[DESK·DATA]` **READ TODAY BEFORE CHANGING ANYTHING ELSE.** CNT.4 (1-bar
  confirmation), CNT.5 (BOS distance floor), CNT.6 (continuation blocked in the
  premium regimes), SWP.3 (sweep approach factor) and RGM.4 (per-regime
  theta_commit) ALL went live on the 08-10 bake (`539d04c20f`). Expect:
  continuation volume DOWN, butterfly/condor REAPPEARING, RANGING committing
  more often (2.1% → ~3.3% of runs), and a LOWER continuation win rate with a
  BETTER loss profile. **None of those is a regression** — read win rate and
  loss distribution together, and do not pool per-regime stats across 08-10.
- `[DESK]` **RGM.5 — the v13 classifier still emits SWEEP_REVERSAL.** Deferred
  from 08-10 by the operator, deliberately, so today's five changes can be read
  against a label set that did not also move. `regime_classifier.py:171` assigns
  it at PRIORITY 1 of five; RGM.3 removed it from the **L2 integrator only**, so
  the label reappears on every tick where `main` falls back to v13.
  **⚠️ MEASURE THE FALL-THROUGH BEFORE CUTTING.** `_is_sweep_reversal` is
  evaluated FIRST, so the ticks it absorbs have NEVER been scored by the four
  rungs below (BREAKOUT → COMPRESSION → TRENDING → RANGING-default). Run the
  classifier over the replay corpus with that branch disabled and COUNT what
  those ticks become. The likely answer is BREAKOUT_VOLATILE — the one label
  whose only dispatch effect is SUBTRACTIVE — which would MOVE the dead zone
  rather than remove it.
  **⚠️ DO NOT NARROW THE FALLBACK PATH INSTEAD.** That was considered and
  rejected: `L2.5 STALE — HOLDING` is 0 on every box while v13 transitions run
  162-229 per box per session, so the fallback is LOAD-BEARING. The hard gate
  blocks every trade on an UNDEFINED regime (only ORB has a bypass), so
  narrowing it would silence continuation, butterfly and condor across the whole
  cold-start and stale window — to fix 0.6% of ticks. Wrong tool.
  **THE COST OF LEAVING IT, for scale:** a ~0.6% dispatch dead zone where the
  label matches no strategy gate, so only ORB can fire. Small, and true for
  weeks already.

**⬜ Fri Aug 14 — AFTER THE CLOSE**

- `[DESK]` **⚠️ OBSERVER DEBT — THREE READS, ALL DUE TODAY, ALL WITH A DELETE
  CRITERION.** Operator, 2026-08-12: *"I don't want/need any more observers
  unless you're putting down firm dates to check them, because right now we have
  more observers than workers and I don't have the capacity to track another
  one."* Correct, and the debt is mine: three observe-only mechanisms shipped in
  two days with no date attached to any of them. **The cautionary case is the
  chain archive — written 2026-07-23 and not read until 2026-08-12, twenty days
  later, and only then because a question happened to need it.** A rule that
  applies from here: **an observer ships with an evaluation date and a delete
  criterion, or it does not ship.**

  - **VEL.1 — velocity stall** (exit_engine v4.16, shipped 08-12 observe-only).
    READ: `grep 'VELOCITY STALL (observe-only' bot.log` across the fleet for
    08-13 and 08-14. Report firings/session, the ratio distribution, and whether
    CONTINUATION and SWEEP ratios resemble ORB's — that last one decides whether
    `VELOCITY_MEASURED_STRATEGIES` can be extended past ORB.
    **DECIDE:** enforce (`OT_VELOCITY_ENFORCE=1`), extend the measured list, or
    **DELETE.**
    ⚠️ **DELETE CRITERION: zero firings across both sessions ⇒ remove it.** A
    mechanism that never triggers is not cautious, it is dead code that still
    has to be read, tested and maintained. Note the floors rest on **n=22 at the
    20-minute mark**, the thinnest part of the curve.

  - **PF.2 — pitchfork observer** (shipped 08-11, live from the 08-12 wake).
    READ: `pos_pct` on the `pitchfork` journal events, joined to continuation
    fires — where was price in the channel when continuation fired? Also whether
    84 daily bars SEGMENT into epochs or draw one channel around everything, and
    whether the §4.3 pivot arm ever builds on real frames or containment is
    carrying it entirely.
    **DECIDE:** continue to the first consumer (continuation's pullback rail
    replacing `bb_middle`), or stop.
    ⚠️ **DELETE CRITERION: no daily fork builds on any box ⇒ the frame fix did
    not take and the overlay is inert.** §11 still governs — v4.0 tags when TWO
    consumers are independently proven, not when the overlay exists.

  - **BFLY.1 — butterfly readiness** (shipped 08-11).
    READ: does the pin-thesis score ever APPROACH firing, and did gates 1x5 ever
    open together? SPX logged `env=PINNING` at **15:29 ET**, ninety minutes after
    the 12:00-14:00 window shut — GEX pinning is structurally late-day while the
    window is midday, so they may be near-mutually-exclusive BY CONSTRUCTION.
    **DECIDE:** move the window on evidence, or stop grading a trade that cannot
    fire.
    ⚠️ **DELETE CRITERION: PINNING never lands inside the window across the
    sample ⇒ the readiness track is scoring an unreachable trade.**

- `[DESK·DATA]` **SHD.2 — shadow re-pull (already scheduled; the one observer
  that HAS paid).** It produced the London 61.3% share (→ LIQ.1), the 14.0%
  within-0.5-ATR figure that JUSTIFIED the permissive 0.05 sweep floor, and the
  18.1%-vs-4% UNKNOWN divergence (→ RGM.6). ⚠️ Respect the 08-08 bake boundary;
  do not pool across it. ⚠️ And carry the correction: **LIQ.1 UNDERMINED the
  London finding it produced** — London was nearest BECAUSE it tracked price, so
  SWP.3's London bonus is fitted to an artefact and is a CORRECTION, not an
  option.
- `[DESK]` **RGM.5 — CUT THE v13 CLASSIFIER'S SWEEP_REVERSAL BRANCH. MEASURED
  2026-08-11, DEFERRED TO TODAY BY THE OPERATOR.** Rationale for the deferral,
  in their words: "we've made a lot of engine changes in the last two days,
  let's give it till close of business Friday." Correct — CNT.4/5/6/7, SWP.3/4/5,
  RGM.4, LIQ.1/3 and BFLY.1 all landed inside 48 hours and none has a full week
  of sessions behind it.
  **THE MEASUREMENT IS DONE — `tests/rgm5_fallthrough.py` v1.0, 3 tapes / 3,007
  ticks, using the SHIPPING engines rather than stubs** (stubbing vol/trend/
  structure would decide the answer by construction). Ask the shipping
  classifier twice, once with `_is_sweep_reversal` disabled:
      SWEEP_REVERSAL is **0.7% of v13 ticks** (22 of 3,007)
      they become: TRENDING_BULL 40.9% · UNKNOWN 36.4% · COMPRESSION 18.2% ·
                   TRENDING_BEAR 4.5%
      ⇒ **14 of 22 newly tradeable, 8 still dead. The cut buys ~0.45% of ticks.**
  **THE BACKLOG'S PREDICTION WAS WRONG AND IS RETRACTED:** it expected mostly
  BREAKOUT_VOLATILE (subtractive, would have MOVED the dead zone). Only 0.1% of
  all v13 ticks are BREAKOUT at all. The cut is directionally right; it is just
  small.
  **⇒ RECOMMENDATION: cut it, but it is not urgent.** Read the split against
  what each label enables at dispatch, then remove the branch.

- `[DESK·DATA]` **⚠️ RGM.6 — `UNKNOWN` IS 19.0% OF v13 CLASSIFIER LABELS, AND
  IT IS 27x THE SWEEP DEAD ZONE.** Found incidentally while measuring RGM.5 and
  it is the more valuable finding by an order of magnitude. UNKNOWN trips the
  HARD GATE at the top of dispatch — only ORB carries a bypass — so on roughly
  **one fallback tick in five, four of the five strategies are structurally
  excluded.** Corroborated live: the 08-11 fit report shows UNKNOWN at 18.1%
  against 4% in the offline L1 harness, so this is not a tape artefact.
  ⚠️ NOTE THE ASYMMETRY WITH L1: acceptance check A5 ("no all-zero ticks,
  UNKNOWN eliminated") passes at 2% on the same date. So L1 has essentially
  eliminated UNKNOWN and the **v13 fallback classifier has not** — the two
  layers disagree about a fifth of the fallback tape. Measure what those ticks
  ARE before proposing anything: the same `rgm5_fallthrough.py` prints the full
  v13 distribution and can be pointed at this directly.


- `[DESK·DATA]` **NF.1 — examine the trades data for pairs that were NEVER
  favourable, and make adjustments.** Operator request 2026-08-08. Which trade
  combinations x market conditions have no salvage in them — they lose more than
  they win and there is nothing about the ENTRY that can be fixed. **Explicitly
  NOT** trades that a stop adjustment could have rescued; those are a different
  problem and must not be swept in. Discriminator: a trade whose MFE never
  reached the cut was never up, so no stop, trail or exit can reach it —
  `excursion_report` already labels this per trade. Split the window at the 08-08
  bake; do not pool.

**⬜ Mon Aug 17 — DEPLOY MONDAY 2 (the calibration deploy) — FREEZE WINDOW OPENS**
- Deploy in one pass: **level hierarchy + ON H/L** (mapper) · **L2.4 calibrated
  priors** · **L1.6 frozen flat-angle cut** · **L1.11 ramp fits**. Verify canaries,
  restart, watch the emitted distribution and label churn live.
- Declare the **L2.6 freeze-candidate window: Aug 10 → Aug 21.** No L1 truth, L2
  prior, or entry-logic deploy until Fri Aug 28 EOD. Anything discovered goes in
  this file with a post-freeze date.
  **VALIDATE (the watch):** nightly, from harvested artifacts only — regime_log
  churn vs the L2.4 offline prediction (N.1) · emitted-distribution shift vs the
  trailing diary · A5 residual on the nightly replay · fire-rate vs trailing mean
  in conditional_tables. Four numbers, all already landing on control; the freeze
  verdict on Aug 21 is written from them, not from impressions.

**⬜ Tue Aug 18**
- `[FLEET]` **L3.1 close-out.** Confirm `signal_journal` jsonl captures full fleet sessions;
  the harvest pull landed 07-27 (v0.5.0) — verify the conductor phase reports it
  and the manifest counts match boxes-run. Log-only; freeze-safe.
  **HOW/VALIDATE:** per-box event counts × session from the harvested jsonl;
  every traded box > 0 scored events, dispositions present for every fired trade
  (join journal → trades.db by symbol+timestamp, orphan count = 0). Existing data
  end-to-end.

**⬜ Wed Aug 19**
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

**⬜ Thu Aug 20**

- `[DESK·DATA]` **AV — GAP CLASS x TIME OF DAY IS A CONDITIONING VARIABLE AND NOTHING
  **⏱ RE-DATED 2026-08-04 from Sat Aug 1 to Thu Aug 20, and RE-TAGGED `[DESK·DATA]`.** It was dated due 08-01 while its own text records it OPENED 08-02 — due before it existed. And it waits on ~40 trades per cell to read a 0.20 R effect, a DC&A dependency rather than effort: it was counted against execution for sessions that had not happened yet.
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

**⬜ Fri Aug 21**
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

**⬜ Sat Aug 22 – Sun Aug 23**
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

**⬜ Mon Aug 24** *(no deploy — freeze holds)*
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

**⬜ Tue Aug 25 — sweep evidence day (the decision the whole sweep track waits on)**
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

**⬜ Wed Aug 26**
- `[DESK→DEPLOY]` **Build the confirmed sweep changes on the TESTER** (level_strength floor and/or
  reclaim tightening and/or stop tightening — only what Aug 18 convicted). Mapper/
  strategy logic → tester-first, deploy Mon Aug 31.
  **HOW:** each convicted change behind its own env knob (`OT_SWEEP_LS_FLOOR`,
  `OT_SWEEP_MAX_CLOSES_BEYOND`, …) so rollback is a config flip.
  **VALIDATE:** tester replay over the banked sweep set — the change must block
  exactly the population Aug 18 convicted (row-level reconciliation, not
  aggregate), and nothing else. Post-deploy, the L3.2 ledger's `gate_block` rows
  carry forward outcomes on everything newly blocked — the standing live
  validator for every gate this file ships.

**⬜ Thu Aug 27**
- `[DESK]` **L3.3 — gate matrix behind a flag, built + tester.** `fires iff regime ∈
  permissive AND C ≥ bar(trade_type)` in dispatch; provisional bars ORB/sweep
  ~0.40, condor ~0.65, butterfly ~0.70; flag-off byte-identical to today. Deploys
  Mon Aug 31, paper.
  **HOW:** the permissive×bar table in dispatch behind `OT_GATE_MATRIX`; flag-off
  path proven byte-identical by replaying a banked session through both and
  diffing decisions.
  **VALIDATE:** conviction is on every trade row and every journaled signal
  (existing since 07-24/07-18), so the matrix's effect is fully auditable:
  flag-on paper week → blocked set enumerated in the L3.2 ledger with forward
  outcomes; bars judged on L3.4's marginal-expectancy curve (conditional_tables,
  holdout enforced Aug 22) on BOTH precision and recall axes.
- `[DESK→DEPLOY]` **N.5 — ✅ BUILT 2026-08-04, ⏱ PULLED FORWARD from Thu Aug 27
  build / Mon Aug 31 deploy to the **Mon Aug 17** bake. ⬜ NOT YET PUSHED.**
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
  **⬜ REMAINING:** push → bake Mon Aug 17 → confirm paper rows populate with
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

**⬜ Fri Aug 28 — FREEZE DECLARED (EOD)**
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

**⬜ Sat Aug 29 – Sun Aug 30**

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

### EPOCH 3 — GATES ON & GO LIVE — Mon Aug 31 → Fri Sep 11

**⬜ Mon Aug 31 — DEPLOY MONDAY 3 (fresh RTH rollout)**
- Deploy: **L3.3 gate matrix** (flag on, paper, bars provisional/wide) + the
  **Aug-18-confirmed sweep changes** + **N.5 latency telemetry** + any K/I code
  decided Aug 17. Fire-rate watch all week. **L3.4 campaign formally starts** on
  post-freeze data and runs underneath everything from here on.
  **VALIDATE:** same four nightly watch numbers + the L3.2 ledger now populating
  gate-matrix blocks with forward outcomes.

**⬜ Tue Sep 1**
- `[FLEET]` **Mode-isolation live-switch rehearsal on ONE box.** Switch paper→live→paper;
  verify defect-Q end-to-end: archives created, mode-scoped queries return zero
  cross-mode rows, no paper row visible to the live loop, breaker reads only live
  P&L.
  **HOW/VALIDATE:** scripted rehearsal with assertions, not eyeballs — after each
  switch: archived DB exists with the mode+stamp name; `realized_pnl_today()` and
  `get_open_trades()` return only current-mode rows (seed one paper row first so
  the negative case is actually exercised); breaker state re-derives clean.
  Existing machinery under test; the seeded-row check is the addition.

**⬜ Wed Sep 2**
- `[DESK]` **Entry/exit path shakedown vs the resolved audit (N/O/P).** Re-run
  `test_entry_fill_confirmation`, `test_roll_is_real`, `test_mode_isolation` at
  HEAD; walk the order_confirm deadlines, cancel-and-walk-away, partial booking,
  and paging paths against the tiny-account config on paper.
  **VALIDATE:** the suite + a forced-partial drill (limit far from mark on the
  tiny account's paper twin so the bounded poll and partial-stash paths actually
  execute); N.5 columns populate during the drill — proving the latency capture
  before it matters.

**⬜ Thu Sep 3**
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

**⬜ Fri Sep 4 — GO/NO-GO REVIEW**
- Gate checklist, every box or no-go: suite green at HEAD · canaries pass fleet-
  wide · freeze intact since Aug 10 · gate matrix behaving across 4 paper
  sessions · mode-isolation rehearsal clean · fill-confirmation shakedown clean ·
  paging live · live config staged (1 contract, SPX+QQQ, bars one bucket above the
  paper crossing per L3.6).
  **VALIDATE:** every checklist line points at an artifact produced above — this
  review reads evidence, it does not generate it.

**⬜ Sat Sep 5 – Sun Sep 6**
- Live-day runbook written (who watches what, the raise-back trigger, the
  kill-switch: `OT_REGIME_ENGINE=v13` rollback path re-verified, configure.sh
  back-to-paper path re-verified). Final rehearsal.
  **VALIDATE:** both rollback paths *executed* on the rehearsal box, not read.

**⬜ Mon Sep 7 — GO LIVE, RTH (tiny size)** 🎯
- `[FLEET]` **L3.6 descent, step 0:** live, minimum size, SPX + QQQ, bars one bucket above
  the paper crossing. This is the tiny-account live shakedown that has gated the
  fill-confirmation work since 07-15 — now with the whole scrub list behind it.

**⬜ Tue Sep 8 – Fri Sep 11 — LIVE, first week of September** ✅
- Daily: fill-quality audit (live fill vs mark, per the 07-15 divergence-audit
  template — now sharing N.4's comparison schema so paper-vs-live divergence is
  one diff) · phantom-P&L reconcile check at each close · ladder fill-latency
  read from the **N.5 columns** (this is the TC.2 stop-trigger dataset — the −40%
  trigger vs 35%/25% question gets answered by these numbers, not by guessing).
- `[DESK·DATA]` **Fri Sep 11:** week-1 live review — divergence report, latency distribution,
  descent decision drafted.
  **VALIDATE:** all three daily checks read collected rows (trades.db + N.5 +
  broker_reconcile records + chain archive); nothing in the review depends on a
  measurement that wasn't scheduled above.

---

### RAMP — Mon Sep 14 → Fri Sep 25

**⬜ Mon Sep 14 — Labor Day, markets closed.** Analysis day: first live-week

- `[DESK]` **A2.3 — THE LOG-ODDS REFORMULATION. The correct endpoint. HOLD UNTIL
  **⏱ RE-DATED 2026-08-04 from Sun Aug 2 to Mon Sep 14 (post-go-live analysis day).** This item's own first line says HOLD UNTIL AFTER GO-LIVE (Aug 31), and it was nonetheless dated 08-02 and counted overdue against execution. The schedule now matches the item.
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

**⬜ Tue Sep 15 — descend one notch.** Half size and/or widen the symbol set —
only if week 1 was clean. Raise-back trigger stays armed: first negative read on
a newly-admitted bucket → back up a notch, no debate.
  **VALIDATE:** "clean" is defined by the Sep 4 review's three artifacts; the
  raise-back trigger reads held-out conditional-table cells (L3.5), never the
  fit set.

**⬜ Wed Sep 16 – Fri Sep 18 — hold the notch.** Watch, don't touch.

**⬜ Mon Sep 21 — FULL POSITION SIZES, RTH** 🎯 — mid-September, contingent on two
clean live weeks. The L3.4 campaign keeps placing final bars underneath; a bar
that the marginal-expectancy data moves, moves.

**⬜ Tue Sep 22 – Fri Sep 25 — full-size steady state** + close-out review of this
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

- **CNT.7 ✅ 2026-08-11 — the confirmation gate was rejecting TIES.** CNT.4
  required a STRICT close beyond the tagging bar's extreme; the live log shows
  misses of 3-9 cents (QQQ 720.34 vs 720.26 = 0.011%; PLTR 0.023%). Fixed with an
  ATR-scaled tolerance, `continuation_strategy` v1.6. **0.40 is DERIVED** from a
  clean gap in the logged misses — ties 0.073-0.360 ATR, genuine failures
  1.133-3.355. My first draft used 0.05 and would have rejected every one of
  them; a test pins that it cannot come back.
- **BFLY.1 ✅ 2026-08-11 — the butterfly readiness track scored a DIFFERENT
  TRADE.** The strategy is a GEX-pin play (Gate 5 requires PINNING, the tent is
  centred on `pin_strike`); the track graded the COMPRESSION label as a hard
  veto plus a boolean squeeze. **would_fire=2132 against ONE trade**, R p50
  0.995. `trade_readiness` v1.8 scores pin distance in expected-move units, pin
  firmness from |net_gex|, and a window that ramps toward noon. Log-only.
- **LIQ.1 ✅ 2026-08-11 — London/Asia out as sweepable pools, and the dedupe
  keeps the NAMED twin.** London runs 07:00-16:00 UTC against RTH 13:30-20:00 —
  a 2.5h overlap — so its "level" was set by the price being traded. And a
  PDH/PDL almost always also sits on an equal-high/low cluster, so one raid made
  two sweeps that collided in the dedupe; the unnamed one won on insertion order
  and `veto_loc` then zeroed the score. Fabricated PDL raid: **0.000 → 1.000**.
- **LIQ.3 ✅ 2026-08-11 — running invalidation.** `closes_beyond` asks the right
  question but is a BIRTH-TIME snapshot over the 2-3 bars after the raid, never
  updated, so nothing ever re-checked whether the level still held.
- **SWP.4 ✅ 2026-08-11 — recovery anchored to the reclaimed LEVEL.** Measured
  from the wick extreme, a DEEPER rejection made the entry look FARTHER away —
  the gate penalised the quality it should reward. 2.4% → 0.11% on the same raid.
- **SWP.5 ✅ 2026-08-11 — liveness replaces the clock.** Operator: "if the market
  makers are driving the price to either extreme what difference does it make if
  it takes an hour or if it takes all day?" **32.9% of the stale sweeps the
  8-bar gate refused still had a LIVE thesis** (854 of 2,593 over 90 symbol-days).
  Refusals went from **98.4% "too old" → 77.2% INVALIDATED + 13.9% backstop**,
  and setups reaching strike selection went **5 → 40**.
- **RGM.6 ✅ 2026-08-11 — the fallback resolves to a KNOWN label.** L1 is
  all-zero on only **2.4-3.0%** of ticks (every session since 07-15) while the
  v13 fallback emitted UNKNOWN on ~18-19% — a known answer existed seven times
  more often than the engine was blind. Ladder is now committed L2 → held
  incumbent → **L1 argmax** → v13. `main` v6.1.
- **CV.1 ✅ 2026-08-11 — check_versions reports ALL GREEN on a clean checkout**
  for the first time in weeks. The orphaned `condor_plan_lifetime` canary is
  removed with its reasoning inline; a permanently-red gate trains the reader to
  skip the DONE banner, at which point every other canary stops working.
- **VW.1f ✅ 2026-08-11 — the three ledger defects its own first output exposed.**
  ~29 mapped-but-unmatched trades vanishing silently; the MIXED ERAS warning
  firing on three all-pre-bake dates (the split was BY TRACK, not by date); and
  the verdict floor testing TOTAL trades so CONTINUATION printed a verdict off a
  MISALIGNED arm of five against 228 aligned. `vwap_orientation_ledger` v1.6.
- **MEM.2 ✅ 2026-08-11 — NO LEAK.** Two independent SPX sessions plateau
  (689→712MB over 1,120 ticks; 499→698MB then flat). The rise is a SINGLE ~185MB
  step from a lazily-imported dependency, which is also why `traced_growth` read
  +0.0MB. The 419M "OOM peak" was never a climbing curve — SPX's steady state is
  ~710MB on a box that could not hold it. Capacity, not a leak.

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

- **🔴 v4.74 — 2026-08-14 — TCS.2 STAGE 1: THE TC.6 EXIT DIED ON EVERY RESTART.**
  `strategy/structure.py` v1.0 (new) · `exit_engine` v4.20 · 8 tests (162 total).
  **Found while designing the credit-vertical type hierarchy — this is a LIVE
  DEFECT, not groundwork.**

  **`is_trend_credit` IS NOT A COLUMN.** 69 columns in the trades table and it is
  not one of them. It was written into the in-memory record and never persisted.
  `get_open_trades_live()` does `SELECT *`, so **any restart rehydrated an open
  trend-participation position WITHOUT the flag**, the exit branch gated on it
  stopped firing, and the leg dropped into the condor ladder with the ratchet and
  the **25%% premium stop**.
  **⚠️ SAME BUG AS THE 08-14 IDENTITY FIX, ONE LEVEL DOWN:** fixed for the process
  that OPENED the trade, still broken for any process that INHERITS it — and the
  hop that dropped it is a **systemctl restart, which happens on every bake.**

  **THE FIX IS TO DERIVE, NOT TO CARRY.** `strategy` and `setup_type` ARE real
  columns, already written correctly, already round-tripping. `structure.of()`
  reads them.
  **⚠️ WHY NOT JUST ADD THE COLUMN:** it would fix tomorrow and not today — every
  position opened before the migration still rehydrates without it, `SELECT *`
  returns None, and None reads as False. **The exact failure, silently.**
  Deriving works on rows that already exist, including any open right now, and on
  the 108 mislabelled rows from 08-14 (`strategy="IronCondorStrategy"` with
  `setup_type="trend_credit_short"` — the setup type is the only surviving truth
  in those).
  **FAILS CLOSED:** an unrecognised record is DIRECTIONAL, the most restrictive
  reading. A misread must never hand a position a LOOSER exit than it earned.
  The old flag is still honoured when present; only its ABSENCE stopped meaning
  "not a trend credit".

  **Stage 1 of the type hierarchy the operator called for** — `CreditVertical`
  base with `IronCondorLeg` and `TrendParticipation` specialising it, so identity
  is the OBJECT rather than a flag that must be copied at every hop. Stage 1 is
  the discriminator and it round-trips; stages 2 (base class, arithmetic lifted
  verbatim) and 3 (dispatch on type) follow. **Operator's call, and the evidence
  supports it: every defect found today was a HALF-MEASURE, not an over-reach.**

- **v4.73 — 2026-08-14 — TCS.1: TREND PARTICIPATION DE-COUPLED FROM THE CONDOR.**
  `strategy/credit_vertical.py` v1.0 (new, shared) · `trend_credit_spread.py` ·
  `iron_condor_strategy.py` · `base_strategy.py` · `config` · 154 tests.

  **THE COUPLING WAS THE CAUSE OF THE 108 BAD TRADES, not a tidiness issue.**
  TC.6 borrowed **six `CONDOR_*` constants**, **five condor methods**, set
  `is_iron_condor = True`, and executed and exited through
  `_execute_condor_leg` / `_evaluate_condor_leg`. Two consequences:
  · changing a condor knob silently retuned a DIFFERENT TRADE, and nothing said so;
  · because TC.6 rode the condor's execution path, its identity had to survive
    as a FLAG on a record the condor built — and when that path hardcoded condor
    identity, the flag never arrived. **A trade living inside another trade's
    plumbing fails the moment one hop drops a field.**

  **WHAT CHANGED:** shared selection math lifted VERBATIM into
  `strategy/credit_vertical.py`, imported by both and owned by neither; TC.6 gets
  `TCS_*` constants; the condor keeps thin delegating wrappers so its own call
  sites are untouched.
  **⚠️ VALUES ARE PROVABLY IDENTICAL** — a test asserts each `TCS_*` default
  still equals the `CONDOR_*` value it replaced, so a future divergence is a
  DECISION rather than a drift. (The check earned its place immediately: I
  guessed `TCS_WING_WIDTH_SPX = 25` and the condor's real value is **5**.)

  **`is_iron_condor` → `is_credit_vertical`.** It NEVER meant "this is a condor":
  all four uses select CREDIT-SPREAD MATH — validity by four legs, stop as a
  RISING spread value, TP as decay toward zero. **That mis-naming is why TC.6 had
  to declare itself a condor to get correct arithmetic.** Kept as a two-way
  property ALIAS so both names address ONE field — a missed rename cannot produce
  a signal that is a credit vertical to one half of the system and a debit to the
  other.

  **⚠️ THREE THINGS THE FINE-TOOTH PASS CAUGHT, ALL SELF-INFLICTED MINUTES
  EARLIER:**
  1. **I renamed the SETTER and not the FIELD.** `sig.is_credit_vertical = True`
     was an attribute nothing read, so `is_valid` and `stop_premium()` would have
     used **DEBIT math on a credit spread** — the identity-chain bug's exact
     shape, reintroduced while fixing it.
  2. **I created the shared module and only half-wired it** — the condor kept its
     own copies of all six helpers, so there were TWO lineages, which is what the
     module exists to remove.
  3. **An absence check matched its own explanatory comment** — WORKING_AGREEMENT
     20, third occurrence. Now scoped by AST to a real `ImportFrom`.

- **🔴 v4.72 — 2026-08-14 — SIM.1/2/3 REVERTED. THEY DUPLICATED
  `replay_confluence.py` AND MODIFIED A LIVE MODULE TO DO IT.**
  `utils/time_utils.py` restored to e594d91 · `data/hot_book.py`,
  `tests/replay_sim.py`, `tests/tcs_v21_backtest.py` DELETED · `devtools` v1.30
  drops option 58 · `FLEET_STATE_2026-08-13.md` folded into HISTORY and deleted.

  **THE CAUSE IS A PROCESS FAILURE, NOT A DESIGN ONE.** The operator's opening
  instruction on this thread was *"Read all available md files in both repos"*
  and *"Rule#1: ALWAYS adhere to the working agreement."* I read BACKLOG,
  WORKING_AGREEMENT and MECHANICS on demand and never read ROADMAP, VALIDATION,
  HISTORY, FILE_MAP or the whitepaper. Two days of work sat on that gap.

  **WHAT IT COST:**
  · **`replay_confluence.py` HAS DONE THIS SINCE v1.2, 2026-07-21** —
    `--warm-sessions`, default 8, as-of replay over deterministic tape. I
    rebuilt it as `hot_book` + `replay_sim`, 774 lines, in ignorance.
  · **AND I REBUILT IT WITH THE BUG ITS v2.2 EXISTS TO PREVENT.** That version
    (2026-08-01) added FRAME CAPS FROM CONFIG *"so the replay sees exactly what
    LIVE sees… at warm >= 7 the replay's 1h frame reaches 55+ bars and VOTES,
    while live holds it at 50 and it stays NEUTRAL. The offline corpus would
    have carried a directional vote production does not have."* My hot book
    reported **"✅ PRIMED — 100%% of the trend vote live"** and called it an
    achievement. **By this repo's own standard that is the DEFECT**, not the
    goal.
  · **A LIVE MODULE WAS MODIFIED FOR A TEST ARTIFACT.** `utils/time_utils.py`
    has **14 call sites across five modules** — precisely the wide fan-in
    WORKING_AGREEMENT 7 says to check `FILE_MAP.md` before touching. I did not.
    Being inert in production was luck, not diligence. Reverted exactly; the
    only consumer was `replay_sim`, so nothing is orphaned.
  · **A NEW DOC FILE WAS CREATED** against `docs/README.md`'s explicit rule —
    *"don't create a new file… Completed work → HISTORY. The sprawl this
    replaced grew one well-intentioned file at a time."* Folded in verbatim with
    a `<!-- was: -->` provenance marker; docs back to the sanctioned set.

  **⚠️ AND THE TERMINOLOGY WENT TO THE WRONG PLACE.** The operator asked to
  codify trend continuation vs trend participation; I put it in a strategy
  changelog header and BACKLOG. `MECHANICS.md` — which `docs/README.md` names as
  the home for behaviour — had **zero** mentions. Now defined there, under
  §Strategies, with the stale "log-only readiness track" framing marked
  SUPERSEDED. BACKLOG points at it rather than duplicating it.

  **KEPT, DELIBERATELY:** every defect fix and every operator-directed change —
  TC.6's terminal return and identity chain, CNT.1's exit half, AFD.1
  pre-dispatch, TC.6 v2.1 with the sovereign ORB bound, CND.7's ratchet scope,
  the 15:45 vertical hold, GRD.2, SWP.3. **149 tests pass after the revert.**
  ⚠️ NEXT, AGREED AND SEPARATE: de-couple TC.6 from the condor's namespace and
  plumbing. It currently borrows SIX `CONDOR_*` constants, five methods, sets
  `is_iron_condor = True`, and routes through `_execute_condor_leg` /
  `_evaluate_condor_leg` — **which is exactly why a dropped flag produced 108
  bad trades.** A trade living inside another trade's plumbing.

- **v4.71 — 2026-08-14 — SIM.3: THE SYNTHETIC PAD.** `data/hot_book.py` ·
  `replay_sim --pad` · `devtools` v1.29 option 58 prompts for it.
  Operator: *"What if you duplicate the current session x10 just for the sake of
  warming the trend engine?"* then *"Synthetic please. It will go further."*

  **⚠️ DUPLICATING THE SESSION WOULD HAVE PUT THE FUTURE IN THE WARMUP.** At
  09:35 the EMAs would already encode the 15:45 close, nine times over, and
  every trend read for the whole replay would be contaminated by the day's
  outcome — **the easiest way to manufacture a beautiful, meaningless backtest,
  and INVISIBLE IN THE OUTPUT.** So the pad runs BACKWARD FROM THE SESSION'S
  FIRST BAR instead: that bar is known at 09:30, so it carries NO LOOKAHEAD,
  and it sits at the right price level with no cross-symbol contamination.

  **IT PRIMES 100%% OF THE VOTE FROM ZERO ARCHIVE DEPTH** — 1d=57, 1h=399,
  15m=1540, 5m=4504 — which real history cannot do near the start of the
  archive (2026-07-23 has only 8 prior dirs, leaving 1h at ~52 of the 55
  needed).
  **AND THE ENGINE DEMONSTRABLY READS STATE OFF IT:** 09:31 NEUTRAL/ADX 0.0 →
  09:45 BULLISH/ADX 34.9 → 10:30 BEARISH/20.7 → 13:00 BULLISH/10.4.

  **TWO DESIGN DETAILS THAT ARE NOT COSMETIC:**
  · **NOT FLAT-CLOSED.** A perfectly flat series gives true range ZERO and
    ADX/ATR divide by it — **NaN, not zero.** Each pad bar reuses the first real
    bar's high/low, so TR is non-zero while directional movement is nil.
  · **ONE SESSION PER PRIOR CALENDAR DAY, not N*390 consecutive minutes.**
    Walking back continuously spans ~15 days for 57 sessions, so the DAILY
    resample saw 16 bars and `1d` stayed starved — **the pad looked generous and
    primed nothing.** Caught only because `verify_prime` counts bars per frame.

  **⚠️ THE STATED COST, printed on every padded run:** the pad is flat, so the
  trend vote starts NEUTRAL and becomes real only as genuine bars accumulate.
  **A padded replay UNDER-FIRES early in the session** — live, the engine has
  real prior-day history and can read a trend at 09:31. Conservative and
  directionally known, which is the right way to be wrong. **Do not read an
  early-session absence as a result.**

  **🔴 CASE SENSITIVITY, TWICE IN ONE MODULE.** The operator typed `spx`; the
  archive holds `SPX_ohlc_*.csv` and `SPX.jsonl.gz`. The OHLC loader reported
  "tape is not harvested yet" and the chain loader reported "0 chain snapshots"
  — **both for data sitting right there.** Fixed at every archive read, not just
  the one that bit first.
  ⚠️ Also: `git checkout devtools.sh` in the sandbox reverted BELOW the pushed
  option 58, because the sandbox clone trails origin. Restoring a file is not
  the same as restoring the repo.

- **v4.70 — 2026-08-14 — SIM.2: THE HOT BOOK IS A GENERIC MODULE.**
  `data/hot_book.py` v1.0 · `devtools` v1.29 (option **58**) · replay delegates.
  Operator: *"I want a generic hot book to prime every run regardless of which
  symbol we are running... just as long as the trend engine will read states
  after it's warm."*

  **IT VERIFIES THE PRIME AGAINST THE ENGINE'S OWN CONSTANTS**, never a number
  written here: `EMA_SLOW + 5` imported from config, and `tf_weights` parsed
  from `trend_engine` so a frame added there cannot go unverified. **Counting
  SESSIONS is a proxy; counting BARS PER FRAME at the first tick is the fact.**

  **AND IT REPORTS WEIGHT LOST, NOT PASS/FAIL** — because a starved frame votes
  NEUTRAL and contributes NOTHING, so the aggregate still works at reduced
  weight. Measured: **12 warmup sessions → 85%% of the vote live (usable);
  2 sessions → 65%% (not usable).**
  ⚠️ **THE `1d` FRAME NEEDS 55 DAILY BARS — about 11 WEEKS of archive**, and the
  OHLC archive starts around 2026-07-13. So **1d is starved on every realistic
  replay** and the run carries 85%% of the trend weight. That is a data-depth
  fact, not a defect, and it is printed on every run rather than discovered.

  **⚠️ THE HARD LIMIT (operator: "we don't have the tape for that session
  yet"):** a session is replayable ONLY after the EOD conductor has harvested
  its OHLC to control. **Same-day replay is impossible before EOD.** Stated in
  the module, in the menu entry, and in the failure message.
  ⚠️ ASKED IS NOT LOADED: a session directory can exist without a given symbol
  in it, so the report always prints asked / dirs / **LOADED** and names what
  was missing. Asking for 10 and getting 3 must be visible.

  **🔴 AND THE HOT BOOK EXPOSED A BUG IT HAD JUST CREATED.** With the book
  loaded, `df` spans eleven sessions — and the driver's tick filter was
  TIME-OF-DAY ONLY, so it selected 09:30-10:00 on EVERY preloaded session:
  **23 ticks for a 30-minute window, replaying dates nobody asked for and
  starting ~10 sessions before the target with an unprimed engine.** Caught
  because the prime check reported NOT PRIMED and the tick COUNT did not match
  the window — neither would have been visible without the verification.
  Ticks are now scoped to the target date.

- **v4.69 — 2026-08-14 — SIM.1: A REPLAY SIMULATOR. `tests/replay_sim.py` v1.0
  + `utils/time_utils` injectable clock.** Operator: *"With the inert trading
  bot on control, why don't we exercise the trading engines on real saved tapes
  after a change?"* **We should have, and the blocker was one function.**

  **`now_et()` IS THE ONE CHOKE POINT** every time-based gate funnels through —
  14 call sites across main, exit_engine, orb_engine, sweep and readiness.
  `set_sim_clock(dt)` makes it injectable. **Production is byte-identical when
  unset**: `_SIM_NOW` is None in every live process and the function returns
  `datetime.now(ET)` exactly as before.

  **THE DESIGN IS ONE LIST.** REAL, imported and called unmodified:
  VolatilityEngine, TrendEngine, StructureAnalyzer, LiquidityMapper, ORBEngine,
  the regime classifier, every strategy, SetupScorer, ExitEngine, RiskManager.
  FAKED, exactly three: **the cache** (a shim serving resampled 1m/5m/15m/1h
  truncated at the replay tick), **the clock**, and **the chain** (archived
  snapshots adapted to the `OptionsChain` shape). `run_analysis` takes
  everything from `get_cache()` and then calls the real engines, which is why
  faking one dependency reaches all of them.
  ⚠️ **NO LOOKAHEAD** — `df[df.index <= now]` on every call, asserted not
  assumed. A replay that can see the next bar is the easiest way to manufacture
  a result.

  **THE HOT BOOK (operator's requirement).** The trend engine needs EMA_SLOW+5 =
  **55 bars on its slowest frame** — 55 hourly bars is ~9 sessions. Starting at
  09:30 on the target date hands every trend-gated strategy a STARVED vote, so
  nothing fires and **the run reports a quiet day that never happened — the most
  dangerous failure a simulator can have: silence that looks like a result.**
  `--warmup` (default 10) preloads prior sessions; verified 3,931 1m bars and
  797 5m bars at 10:00 with a live BULLISH vote and ADX 21.8.

  **VIX FROM THE ARCHIVE, NOT THE FEED.** The operator was right that every box
  pulls VIX live, and `signal_journal` records `macro.vix` on every scored event
  — so it is already archived AND timestamped. The replay reads it from there.
  **Replaying August tape against today's VIX is not a replay.**

  **WHY IT MATTERS MORE THAN ANY TOOL BUILT THIS WEEK.** Every defect found on
  2026-08-14 was an INTERACTION defect that passed unit tests on both sides:
  TC.6 firing 40x in an hour, breakout continuations exiting in 15 seconds,
  AFD.1 consuming the slot and trading nothing, TC.6's identity never reaching
  the record. **All four are visible in a replay and none needed P&L to spot.**
  ⚠️ It also **REPLACES** `spread_counterfactual`, `slippage_audit` and
  `tcs_v21_backtest` rather than joining them — each re-implements a slice of an
  engine we already own, which is the second-lineage failure WORKING_AGREEMENT 7
  forbids.

  **STAGE 1 (this delivery) drives ANALYSIS end to end.** STAGE 2 wires dispatch
  and an execution sink so the trade list is produced and can be **diffed
  against what the fleet actually did on the same date — any divergence is a bug
  in one of them.**
  ⚠️ KNOWN LIMITS, printed in the output: **volume is synthetic** (constant 0 —
  the archive carries none, so any volume-derived signal is INERT here, not
  measured); fills come from a 5-minute snapshot, so no queue position and no
  intra-window quote movement; and a startup STARVED-vote warning is cosmetic
  (it fires from a caller during module import, before the shim installs —
  check `ctx`, not the log).

- **🔴 v4.68 — 2026-08-14 — THE HANDOFF DROPPED EVERY FLAG. TC.6's IDENTITY
  NEVER REACHED THE RECORD.** `main` v6.8 · 12 tests (149 total).
  **Found by auditing the LOGIC against stated intent — not by a test, and not
  by watching P&L.** Operator: *"I don't need P&L — I'm asking if the logic is
  written, sound, and true to the intent I named?"*

  **THE STRATEGY AND THE EXIT ENGINE WERE BOTH CORRECT AND THE TRADE STILL DID
  THE WRONG THING.** `_execute_condor_leg` builds the record for BOTH a condor
  leg and a trend credit spread, and hardcoded condor identity onto both:
  · **`is_trend_credit` never reached the record**, so the exit branch — gated
    on `record.get("is_trend_credit")` — **COULD NEVER FIRE.** Every TC.6 leg
    fell into the condor ladder with the ratchet and the 25%% premium stop.
    **That is the `stop=$0.69` on a $0.55 credit in the 10:02 Telegram alerts**,
    and it means the terminal-return fix shipped that morning repaired a branch
    that never executed.
  · **`underlying_stop` was never set**, so even had the branch fired the breach
    rule would have had NO BOUND and skipped itself silently.
  · **`strategy` and `regime` were hardcoded**, so TC.6 trades logged as
    IronCondorStrategy in RANGING and their P&L was attributed to the condor —
    which is why they never appeared in any continuation query.

  **FIX:** identity comes from the SIGNAL, never from the function it routes
  through. `_is_tcs` drives `strategy`, `regime`, `underlying_stop`,
  `is_trend_credit`, and **`stop_premium = 0.0`** for a trend credit spread.
  The condor path is untouched.

  **⚠️ THE LESSON: A FLAG IS ONLY REAL IF IT SURVIVES EVERY HOP.** Unit tests on
  the producer and the consumer both passed while the wire between them was cut.
  The new tests are CHAIN assertions — signal -> record -> exit — because that
  is the only place the defect was visible.

  **ALSO IN THIS DELIVERY — the not-exceeded filter is dis-inherited, and it was
  worse than redundant: IT MADE THE BOUND DECORATIVE.** `session_low <= orb_low
  < orb_high` (the opening range is PART of the session), so requiring a put
  strike to clear BOTH collapsed to the session low **every time** — the strike
  was always placed below the ORB LOW and never at the operator's level, so the
  ENTRY placed it somewhere the EXIT never referenced. Mirrored for calls.
  Operator: *"wouldn't the orb bounds be 'richer' than the furthest away it's
  been?"* Yes — the bound sits CLOSER to spot. Measured on one quote: **credit
  0.60 at the bound vs 0.20 under the filter, 3x.** And POP is the better
  instrument anyway: "price traded here today" is backward-looking, while POP
  asks the same question in sigma*sqrt(T) terms FROM NOW.

  **`tests/tcs_v21_backtest.py`** replays the shipped gate stack sequentially
  against archived chains and tape. ⚠️ **IT BACKTESTS ONE OF THE THREE
  CORRECTIONS.** The direction gate is a PROXY (the trend vote and ADX are NOT
  archived; reimplementing the trend engine would be a second lineage), so the
  live gate is stricter and the trade count is an UPPER BOUND. **CNT.1's exit
  fix and AFD.1's pre-dispatch move are not backtestable at all** — the
  counterfactual is not in the data, and any number claiming otherwise would be
  fabricated. Settlement math verified directly against six planted cases;
  max loss is width-credit and never more.

- **v4.67 — 2026-08-14 — NAMING CODIFIED + TC.6 v2.1 DIS-INHERITS THE CONDOR.**
  `trend_credit_spread` v2.1 · `main` v6.7 · `exit_engine` · `config` v4.18 ·
  135 tests.

  **🔵 TERMINOLOGY, FIXED (operator, 2026-08-14) — the definitions now live in
  `MECHANICS.md` §Strategies, which is where behaviour is documented. Recorded
  here only as the pointer.**

  **THE LEVEL vs THE ENGINE — and v2.0 over-corrected.** Operator: *"those
  levels are fixtures."* The ORB ENGINE must not gate an afternoon trade (no
  runaway flag, no slot arbitration, nothing a restart can erase); the ORB LEVEL
  is a price on a chart. `main._opening_range()` recomputes it from the TAPE
  using the SAME window constants the engine uses — restart-proof, available
  past the cutoff, and incapable of becoming a second opinion about where the
  range is. His own note on the earlier call: *"In the heat of the moment,
  post-11am my instinct was to dismiss any orb-related thesis as to why they
  weren't firing."*

  **DIS-INHERITED FROM THE CONDOR:**
  · **the 0.80 x EM minimum distance.** The condor needs an EM floor because it
    sells around a PIN with no structural level to lean on; TC.6 HAS one. A
    strike must clear BOTH constraints in `_select_beyond_rail`, so **an EM
    floor beyond the ORB high would push the strike past the specified level —
    a FITTED percentage silently overriding a STRUCTURAL one.** Neutralised with
    a non-binding sentinel rather than deleted, because the selector is shared
    and the condor still needs it.
  · **the nickel close.** A profit exit caps a position whose measured EV was
    HELD TO EXPIRY, UNMANAGED.
  RETAINED deliberately: quote width (liquidity is universal), POP >= 0.70 (the
  operator's own 70-80%% band, stated about exactly this trade), the
  not-exceeded session extreme, and deferral to an active condor plan.

  **ADDED — PRICE MUST BE OUTSIDE THE RANGE AT ENTRY.** The exit calls a close
  back through the bound INVALIDATION, so entering while price is already inside
  means **the trade is born in the state its own exit calls dead** — the exact
  CNT.1 failure shape that made every breakout continuation a one-tick artefact
  for a week. Entry and exit must agree about the same level.

  **REMOVED — the 30-minute cooldown.** Operator: *"It's gated enough. The
  cooldown is excessive."* It was an emergency brake during the rapid-fire
  incident and the wrong instrument for the right worry: the loop came from a
  $0.06 credit sitting one cent from a nickel close and one cent from a mis-set
  stop, all now fixed at the source. **A timer stacked on nine substantive gates
  suppresses valid re-entries without preventing a single bad one.** The config
  constant survives at 0 so a re-add needs no config change.

  **THE ENTRY, CONCRETELY:** opening range 582.50/578.10, price 588.00 at 13:20,
  session low 585.00, ADX 27, vote BULLISH. Price is OUTSIDE the range → put
  spread beneath the move, bound = ORB high 582.50 → **short 582.50 / long
  577.50**, ~$0.55 credit on a $5 width. Exits only on a 1-minute close back
  below 582.50, or 15:45.
  ⚠️ TWO THINGS CAN STILL MOVE THE STRIKE OFF THE BOUND: the not-exceeded
  session extreme (if price traded below the ORB high during the afternoon) and
  POP (if the runaway is shallow). Both are defensible; both mean the bound is
  not sovereign, which is an open question for the operator.

- **🔴 v4.66 — 2026-08-14 — THE SLOT MAP, AUDITED AND ENFORCED.** `main` v6.6 ·
  `trend_credit_spread` v2.0 · 10 tests (129 across the 08-13/14 suites).

  **THE SPEC, as the operator stated it:** *"The reason it requires a runaway
  before 11am is because ORB OWNS THAT SLOT. So a runaway is the only exception
  a different trade can execute."* and *"Trend participation should have nothing
  to do with orb range after the 11AM cutoff... If they are linked in any way
  after 11AM, then it's wrong."*
  BEFORE 11:00 — ORB owns it; a runaway is SLOT ARBITRATION, freeing it for
  `trend_continuation_handoff` (first refusal, by dispatch order) or
  SweepReversal (only on a NAMED level, main.py:1683).
  AFTER 11:00 — ORB/Continuation/Sweep all blocked by AFD.1 (all three are debit
  directional). Three non-overlapping regimes, one occupant each: condor
  (RANGING + daily fork), butterfly (12:00-14:00 + PINNING GEX), TC.6
  (directional trend vote). TC.6 defers to an active condor plan.

  **🔴 DEFECT 1 — AFD.1 WAS A POST-SELECTION VETO, AND THAT IS PROBABLY WHY TC.6
  FIRED ZERO TIMES ON 2026-08-14.** The gate ran at line 1818, AFTER ORB (1571),
  continuation (1631), sweep (1672), butterfly, condor and TC.6 (1786) had all
  been evaluated. So past 11:00 a debit strategy still **WON** the slot:
  `signal` went non-None, **TC.6 sits behind `if signal is None` and never
  ran**, and only then was the debit signal refused. **The tick produced NO
  TRADE AT ALL, and the slot the spec assigns to TC.6 was consumed by a strategy
  forbidden to trade in it.**
  Placing the gate after selection was right for JOURNALLING (the refused signal
  is fully formed) and **wrong for ARBITRATION**. Now computed ONCE before
  Priority 1; ORB/Continuation/Sweep are SKIPPED, not evaluated-then-refused.
  The post-selection gate is RETAINED as defence in depth — it costs nothing,
  still journals a fully-formed refusal, and catches a future strategy added to
  `DEBIT_DIRECTIONAL_STRATEGIES` that forgets the pre-gate.
  ⚠️ **NO UNIT TEST OF THE PREDICATE COULD HAVE CAUGHT THIS.**
  `_afternoon_debit_blocked` was always correct — it was simply CALLED TOO LATE.
  The new tests are SOURCE-ORDER assertions, and the ordering test is verified
  to FAIL against the version that shipped this morning.

  **TC.6 v2.0 — THE ORB LINK IS SEVERED ENTIRELY.** No `orb` parameter, no
  `invalidation_reason` gate. Anchored on the **SESSION EXTREME** — the
  operator's own original framing, *"a vertical spread at the floor of the
  Move"* — with direction from the **live trend vote** (`overall_direction` +
  ADX, the same source CNT.1's breakout branch uses).
  WHY THE ORB ANCHOR WAS WRONG FROM THE START: (a) it is a 09:30-09:35 structure,
  four hours stale by 13:00; (b) the morning runaway and the afternoon trend can
  be DIFFERENT MOVES, even opposite ones — the gate would PASS and the trade
  would be incoherent; (c) `orb_state.json` is **WRITE-ONLY, no load path
  anywhere**, so the ORB engine is memory-only and the 10:37 restart wiped
  `invalidation_reason` on all 15 boxes — and since ORB cannot re-arm past its
  cutoff, the flag was gone PERMANENTLY for the session. Persisting it would
  have preserved a bad design and made it durable.
  Measured basis (`spread_counterfactual --anchor floor`, 18 sessions):
  TRENDING_BEAR +0.39/+0.48/+0.46 and TRENDING_BULL +0.60/+0.66/+0.78 at
  0.00%%/0.25%%/0.50%% beyond the floor. ⚠️ **Both arms positive, so this is a
  GENERAL credit edge, not a regime-specific one** — weaker evidence than the
  ORB result whose control FAILED. Stated plainly.
  Every early return now LOGS. A gate that can silence a strategy for a whole
  session without leaving a line is how 2026-08-14's afternoon was spent
  guessing.

  **⚠️ TWO ORDERING DEFECTS FOUND AND NOT FIXED — deliberately, mid-session:**
  (a) TC.6 sits BELOW butterfly and condor behind `if signal is None`, so a
  butterfly at 12:30 skips it. They *should* never collide (butterfly needs
  RANGING/COMPRESSION + a GEX pin, TC.6 needs a directional vote) — but nothing
  ENFORCES that, and ordering decides if they ever do.
  (b) Pre-11:00, continuation at Priority 2 still starves butterfly (P3) and
  condor (P4), both behind `if signal is None`. Measured over 13 sessions:
  **RANGING → continuation 94 vs condor 27; COMPRESSION → continuation 39 vs
  butterfly 6.** Documented in CNT.6's own comment. Changing dispatch priority
  is a larger behavioural change than a mid-session hotfix should carry.

- **🔴 v4.65 — 2026-08-14 — CNT.1 SHIPPED HALF A FEATURE ON 2026-08-07 AND IT
  RAN BROKEN FOR A WEEK.** `exit_engine` v4.19 + 9 tests (119 across the
  08-13/14 suites).

  **THE CONTRADICTION.** CNT.1's ENTRY branch lets continuation OPEN on
  `BREAKOUT_VOLATILE` — direction from the trend vote instead of the label,
  gated on ADX — and tags it `trend_continuation_breakout`. `still_trending` in
  the EXIT only ever accepted `TRENDING_BULL` / `TRENDING_BEAR`.
  **So every breakout continuation was BORN ALREADY FAILING ITS OWN EXIT TEST.**
  Open on tick N with the label at BREAKOUT_VOLATILE; on tick N+1 the exit reads
  **the same unchanged label**, finds it is not TRENDING_*, and closes as
  `regime_flip`. **THE LABEL NEVER FLIPPED — the exit reason was a lie**, and
  the block sits BEFORE `bos_exit`, so nothing else ever got a look.

  **THE TIMESTAMPS ARE THE PROOF.** SMH 14:24:19→14:24:34, re-enter
  14:24:49→14:25:04, eight in a row. **15-second holds — exactly one tick.** A
  hold equal to the tick interval, identical every time, is a structural exit
  firing immediately, not a market outcome. P&L was symmetric noise because a
  one-tick hold is one tick of random walk minus the spread: SMH's eight netted
  **−$29**, GS's eight **+$331** on the identical mechanism.

  **⚠️ AND THE DIAGNOSTIC TRAP IS THE MORE VALUABLE RECORD.** Eight identical
  15-second trades read as CHURN, and I proposed a per-symbol cooldown — the
  same fix that was correct for TC.6 an hour earlier. **A cooldown would have
  spaced out incoherent trades and hidden the evidence that exposed the
  defect** — strictly worse than leaving it alone. The operator rejected it:
  *"It's not a re-entry or cooldown problem. It's firing random losing trades
  into the ether & immediately stopping out. That is not a coherent setup. The
  fact that it's doing it in succession is only a side effect. If they were
  profitable it wouldn't be a problem!"* **The symptom is not the bug, and the
  right fix for one symptom is not the right fix for the same symptom with a
  different cause.**

  **THE FIX.** `still_trending` accepts `BREAKOUT_VOLATILE` when
  `setup_type` ends in `_breakout`. A breakout continuation lives or dies on the
  TREND VOTE it was born from, not on a label test it was never able to pass.
  Scoped: standalone and handoff are unchanged, a genuine flip to RANGING still
  exits, and a MISSING `setup_type` does NOT grant the exemption (fails closed,
  so an old row keeps its ordinary exit).

  ⚠️ **THIS IS A FIX, NOT A FIT** — nameable without reference to P&L: entry and
  exit disagreed about the same label. ⚠️ It also means **every
  `trend_continuation_breakout` row since 2026-08-07 is a one-tick artefact** and
  must be excluded from any study of continuation's edge.

- **🔴 v4.64 — 2026-08-14 — TC.6 LIVE HOTFIX. IT RAPID-FIRED THE WHOLE FLEET AND
  STOPPED OUT ON EVERY LEG.** `exit_engine` v4.18 · `trend_credit_spread` v1.1 ·
  `config` v4.17. **First live session after the 08-13 bake.**

  **WHAT WAS SEEN, 10:02 ET:** NVDA sold a $5-wide for **$0.06**, PLTR a $6-wide
  for **$0.08**, SPX a $5-wide for $0.55 — every box firing in succession, each
  closing within seconds, all at a loss.

  **DEFECT 1 (the losses) — THE TC.6 EXIT BRANCH HAD NO TERMINAL RETURN.** When
  neither breach NOR nickel fired it fell straight through to the ratchet and
  the 25%% condor stop. `_execute_condor_leg` writes
  `stop_premium = credit x 1.25` at entry, so a **$0.06 credit put the stop at
  $0.07 — one cent of widening closed the trade.** The measured EV was HELD TO
  EXPIRY, UNMANAGED; a premium stop is a different trade, which is the entire
  reason the branch exists.
  **⚠️ THE TEST THAT MISSED IT** asserted the branch CONTAINED two
  `return decision` statements. It did. Neither covered the path where NEITHER
  condition fires — **the path that was broken. Counting returns proves nothing
  about the path that has none.** Now asserted on the branch's LAST STATEMENT
  via AST, and **verified to FAIL against the exact version that shipped.**

  **DEFECT 2 (the firing) — THREE MISSING ENTRY GATES:**
  (a) **NO AFTERNOON GATE.** Designed as afternoon trend participation, coded
      against `GLOBAL_NO_ENTRY_ET` (14:00) only. Fired at 10:02. Now
      `TCS_START_ET` = 11:00, matching AFD.1.
  (b) **NO RE-ENTRY COOLDOWN.** With a $0.06 credit and a $0.05 nickel close the
      trade closed on the tick it opened and reopened immediately. "No
      per-session limit" was the operator's call and STANDS — **a loop is a
      defect, not a limit question.** 30 min.
  (c) **NO EXPECTATION OF PROFIT.** Operator: *"The trade should at least enter
      on some expectation of profit, not all willy nilly like this."*

  **⚠️ AND THE POP FLOOR CAUSED (c). POP rises with distance, so requiring
  POP >= 0.70 selects for FAR strikes — and far strikes collect almost nothing.
  I shipped the probability half of the gate without the payoff half. A gate
  that only demands SAFETY systematically finds the WORST-PAID trade that clears
  it.** The fix is not a second flat floor but ONE JOINT INEQUALITY:
  `EV = credit*POP - L*width*(1-POP) > 0` ⇒ **`credit/width > L*(1-POP)/POP`** —
  a LOW-POP strike must pay richly, a HIGH-POP strike may be thin.
  `L` (loss given breach, fraction of width) = **0.5**, a stated prior:
  **not 1.0**, because a breach rarely runs the full width by the bell (TC.7's
  ORB cell measured E[loss] 0.35 on a $5 wide = 7%% at 90%% terminal-OK) and at
  L=1.0 a POP-0.70 strike would need 30%% of width, which essentially never
  occurs — **over-correcting into silence is its own failure.** Requires 21.4%%
  at POP 0.70, 5.6%% at 0.90, 2.1%% at 0.96.
  **Verified against the live fills: NVDA (1.2%%) and PLTR (1.3%%) BLOCKED on EV
  alone even at POP 0.96; SPX (11%%) PASSES.**

  Retained alongside it: a nickel-relative floor (credit >= 4x the nickel close)
  because $0.06 against a $0.05 close is one cent of total profit potential —
  that is a MECHANICS failure, not an economics one, and the EV test does not
  catch it.

- **v4.63 — 2026-08-13 — FLEET STATE RECORDED + THE CLOCK RESET + TC.6 KILL
  SWITCH.** `docs/FLEET_STATE_2026-08-13.md` v1.0 · `config` v4.15 ·
  `trend_credit_spread` v1.0.

  **BAKED: `7efd320` across 29/29 boxes**, 928 files synced, pycache cleared,
  optionsbot active on all 29, then shut down clean. Hotfix `e639099` on top.
  **This is the first time in the project's history that eleven behavioural
  changes have landed in one bake** — and the alternative on the table that
  morning was regressing the fleet to options_trader v2.

  **`docs/FLEET_STATE_2026-08-13.md` is the account.** Per change: what, why,
  the expected benefit with its measured basis, the env knob that tunes it, the
  verification signature, and the honest trade-off. Also records what shipped
  INERT (LIQ.4 unwired, FRC.2's ladder at `OT_ENTRY_LADDER=0`) and **why FRC.2
  must stay off until `fill_model` gates paper fills** — an aggressive rung with
  assume-fill logic manufactures edge and would look like the best change ever
  made.

  **PART 0 RESET.** The Aug 17 / Sep 8 rows are HISTORICAL. **The live anchor is
  Fri 2026-08-28.** The two weeks to it are a MEASUREMENT window, not a tuning
  window — most of the 08-13 thresholds are stated priors, and re-fitting them on
  the data that motivated them converts an out-of-sample validation into an
  in-sample one.

  **TC.6 KILL SWITCH — `OT_TCS_ACTIVE` (config v4.15).** TC.6 was the ONLY new
  FIRING strategy shipped without an env-level off switch; stopping it would have
  needed a code change and a re-bake on a strategy that has never executed a live
  order. **Default is ON and the operator is deliberately leaving it on:** *"bad
  trades are still GOOD data."* The switch is for DEFECTS — a traceback or a fire
  loop — not for losing trades. It fires only after a runaway on a trending
  afternoon, so observations will be scarce and killing it on the first loser
  leaves nothing to read.

  **THE LARGEST UNBUILT LEVER, restated so it is not lost:** FRC.1's spread
  quintiles. **Q5 carries $60,185 — 60%% of ALL friction — for −$169 of gross;
  Q4+Q5 are 79%% of friction against −$6,337.** Cutting them removes four-fifths
  of transaction cost AND improves gross, from a pre-entry filter needing no
  forecast.

- **🔴 v4.62 — 2026-08-13 — HOTFIX: FRC.3's TICK-SIZE FETCH HAD NO CACHE GUARD.**
  `options_chain` + `tick_size` (`needs_venue_rule`). **Found while the operator
  was mid-bake; caught before it reached the fleet.**

  **THE DEFECT.** The r109 patch carried the comment *"cache the VENUE'S price
  grid once per symbol per session"* and **did no cache check whatsoever**. So
  it fired an extra `NestedOptionChain.get()` on EVERY `fetch_chain()` — and
  `fetch_chain` is called from three places in the tick loop (main.py:1524,
  2024, 2172). That is **hundreds of needless SDK calls per box per session**,
  real rate-limit exposure, on a live path, **described by a comment that
  claimed the opposite.**

  **THE FIX.** `needs_venue_rule(symbol)` — fetch only when there is neither a
  cached rule NOR a recorded failure. **A failed attempt counts as answered**:
  retrying a broken fetch every tick is the same hot loop with a worse error
  rate, and the fallback already logs a warning each time it prices off the
  guess.

  **⚠️ THE TELL WAS VISIBLE AND I MISSED IT TWICE.** The `a_get` correction had
  been applied on top of the original block rather than replacing it, so the
  same eight-line comment appeared TWICE in the file. A duplicated comment is
  the signature of an edit applied twice, and it was sitting directly above the
  unguarded call. **I read that block three times — to verify the SDK method
  name, to verify `run_async`, and to package it — and never once asked whether
  the code did what its own comment said.** Verifying the line I changed is not
  the same as reading the block it lives in.

  **AND THE VERIFICATION COMMAND HIT MY OWN DOCUMENTED TRAP:** `grep -c`
  returns exit status 1 on a zero count, which killed an `&&` chain and made a
  successful check look like a failure — the exact hazard recorded this morning
  in the fleet-command rule. `|| true`, or wrap it in `echo`.

- **v4.61 — 2026-08-13 — SWP.3 SHIPPED.** `trade_readiness` v1.9 + 8 tests (143
  across today's suites). **Every item approved this morning is now built.**

  **THE SIGN IS REFUTED BY THREE INDEPENDENT MEASUREMENTS**, none of which knew
  about the others: **LIQ.1** — the London level TRACKS PRICE rather than being
  approached by it; **ANT.1** — appr_val −41%, appr_touches −45% against
  outcome; **ANT.2** — fitted weights −0.39 / −0.40. `appr_val` entered
  `_combine` as a POSITIVE corroborator at weight 0.25.

  **WHY NOT SIMPLY INVERT IT.** `1 - appr_val` asserts *"far from any named
  level = ready"*, which is nonsense for a SWEEP — the trade is penetration and
  rejection AT a level. The likelier mechanism is that **PROXIMITY IS
  PRE-SWEEP**: price near a pool means the sweep has not happened yet, so the
  term was scoring the setup's ABSENCE. **We know the sign is wrong and we do
  NOT know the right functional form**, and asserting an inverted one swaps one
  unfitted prior for another. Weight ZERO; `appr_val`, `appr_touches`,
  `appr_dist_atr` and `appr_name` STAY JOURNALED so the follow-up study needs no
  new collection.

  **⚠️ THE RENORMALISATION IS THE REAL RISK, NOT THE REMOVAL.** `TR_STAGE_BAR`
  (0.35) and `TR_ARM_BAR` (0.55) are ABSOLUTE thresholds against the
  corroborator SUM, and the four weights summed to exactly 1.0. Dropping 0.25
  without redistributing would compress every sweep score by a quarter and make
  the arm bar effectively unreachable — **the sweep track would go quiet and it
  would look like a correction rather than a behaviour change.**
  0.30/0.20/0.25 → **0.400/0.267/0.333**. Tests pin the sum at 1.0, the factor
  ordering (conv > exh > fresh), that a maxed score can still ARM, and that a
  lone corroborator still cannot — plus a deliberate-failure check proving the
  sum assertion is reachable rather than vacuous.
  The env override is documented as NOT standalone: raising `SWEEP_APPR_W` alone
  pushes the sum past 1.0 and inflates every score against the absolute bars.

  **LOG-ONLY** — `main.py:2045` calls `_readiness.assess_all()` and DISCARDS the
  return, so no trade changes today. What it fixes is that every FUTURE fit
  against the readiness composite would otherwise inherit a term measured to
  point backwards.

  **⚠️ PROCESS NOTE, three failed attempts on one header.** This file uses `#`
  COMMENT headers, not a module docstring — my first insert wrote bare text into
  module scope (`SyntaxError` on an em dash), my repair loop then searched for a
  line it had already renamed and ran off the end, and a test asserted on a
  phrase the comment wraps across two lines. Restored from git and reapplied.
  **Testing prose is fine; testing prose LAYOUT is not** — assert on
  wrap-stable fragments.

- **v4.60 — 2026-08-13 — GRD.2 SHIPPED (FULL SEND).** `continuation_strategy`
  v1.7 + 10 tests (135 across today's suites). **The oldest open item on the
  board, approved this morning and built tonight.**

  **THE BOT WAS NEVER TARGET-FREE. IT WAS TARGET-BLIND.** `trend_strike_plan`
  has always computed `target_price` (EM fraction scaled by ADX + conviction)
  and USED IT to pick the strike — then discarded it. One line restores it, and
  three consumers that were inert on **77% of fleet volume** wake up:
  · **`_rrr()`** returned None on every continuation signal. That is why `rrr`
    appears in ORB's scorer table and nowhere else, and why the MIN_RRR floor
    was structurally inert across most of the book. `rrr` is also the ONE
    dimension measured to separate anywhere, and it has been unmeasurable on the
    strategy carrying most of the volume.
  · **`_pools_in_path`** scans `entry < p < target`; with 0.0 a LONG's window is
    **empty by construction**, so `liquidity_clear` was a STRUCTURAL constant at
    1.000, not a measured one. The scorer showing it flat was the symptom.
  · **`_update_post_target_trail`** is guarded on `underlying_target > 0`, so
    continuation always fell back to the blunt 85% trail instead of the FVG
    floor past 100% TP.

  **⚠️ NOT A TAKE-PROFIT, AND NOTHING CONSUMES IT AS ONE.** The operator's
  no-target design stands verbatim — *"the multiple is a want, not a need... use
  stops creatively so nothing stops them running when they're correct, but the
  leash tightens quickly when they're wrong."* This is the R denominator and the
  trail's reference. A test asserts no exit fires on reaching it, so a future
  edit cannot quietly turn it into one.

  **⚠️ THE ENTRY GATE BARELY MOVES — ARITHMETIC, NOT OPINION.**
  `liq_score = max(1 - n*0.25, 0)` at weight 0.20 removes AT MOST **0.20** from
  a continuation total whose measured p50 is **0.885**, against a `grade_b` bar
  of **0.55**. Even 4+ blocking pools leaves **0.685** and still fires. **THE
  REAL BEHAVIOURAL CHANGE IS THE EXIT TRAIL.** A test pins the arithmetic so the
  claim fails loudly if a weight or the bar ever moves.
  ORB's A/B grade ALSO reads `_pools_in_path` — but ORB already populated its
  target, and GRD.1 set continuation's `grade_a` to 1.01 so it cannot grade A
  regardless. That path is untouched.

  **PLACEMENT MATTERS:** `_plan` is built AFTER the signal is constructed, so
  the assignment cannot live in the `OptionsSignal(...)` call and must sit after
  the `if not _plan["ok"]` return — otherwise a failed plan writes 0.0 and looks
  populated. Both pinned by tests.

  **ATTRIBUTION WARNING FOR THE FIRST BAKED SESSION.** Nothing from 2026-08-13
  has reached the fleet. GRD.1, the 0.15 stop floor, AFD.1, PF.5/PF.6, CND.7,
  the 15:45 vertical hold, TC.6 and now GRD.2 all land in ONE bake. Read the
  first session as **"did anything break"**, not "which change helped" — the
  three separately-observable GRD.2 signatures (`rrr` appearing in the scorer
  breakdown, `liquidity_clear` moving off 1.000, `post_target_trail` appearing
  in `exit_reason`) are the only per-change attribution available.

- **v4.59 — 2026-08-13 — FRC.3: THE VENUE'S PRICE GRID, ON EVERY ORDER PATH.**
  `execution/tick_size.py` v1.0 + `limit_ladder` v1.4 + `options_chain` + 20
  tests (125 across today's suites).

  Operator: *"Would the box know from the options chain what increment is
  allowed?"* then *"that should extend to all orders unambiguously."* **It does,
  and it now does.**

  **THE SDK HAS IT: `NestedOptionChain.tick_sizes`** — a list of
  `TickSize(value, threshold, symbol)`. `threshold` expresses the $3.00 boundary
  GENERICALLY, so nothing hardcodes 3.00 or assumes a single breakpoint. Fetched
  once per symbol per session (static instrument metadata, not a quote) and
  cached. **This replaces the `PENNY_CLASSES` guess I shipped hours earlier and
  flagged as unverified** — Penny Interval Program membership is a broker/OCC
  fact that changes and is not derivable on this box.

  **RESOLUTION ORDER, so ORDER TIME NEVER GUESSES:**
  1. **VENUE RULE** — authoritative.
  2. **QUOTE PROOF** — an off-nickel bid PROVES a penny grid. **ASYMMETRIC:** it
     can only REFINE downward, never coarsen, because every nickel is also a
     valid penny. Free, and a live cross-check that can override a stale rule.
  3. **`PENNY_CLASSES`** — last resort, and it **LOGS A WARNING** when reached,
     so "how often are we still guessing" is a number rather than an assumption.
  **EVERY RESOLUTION CARRIES ITS SOURCE** (venue / quote / list / default). If a
  fill returns at a price we did not post, the log must say which produced it —
  otherwise silent venue adjustment is undiagnosable.

  **⚠️ AND THE BIGGER FIX: `limit_at_mark` PRICES EVERY EXIT** plus the
  15:40-15:44 flatten reposts and every condor leg — far more orders than the
  entry ladder — and it was doing `round(px, 2)`. It now snaps to the grid too.
  Callers that pass no symbol keep the old behaviour, so nothing breaks while
  the fetch is proven. Snapping stays DIRECTIONAL (buy down, sell up): nearest
  would make ~half of all limits MORE aggressive than specified, and rounding
  INTO the market costs money silently while rounding away costs fill
  probability, which `fill_model` measures.

  **⚠️ TWO SDK FACTS VERIFIED RATHER THAN ASSUMED, both of which would have
  failed SILENTLY.** There is no `a_get` on this build — it is `get` — and `get`
  is a **COROUTINE despite the sync-looking name**, so it needs `run_async`.
  Either mistake raises into the `except`, marks the fetch failed, and falls
  back to the guess **forever**, with only a debug line. Checked against the
  installed package with `inspect.iscoroutinefunction`.

  **⚠️ AND A TEST FIXTURE I GOT WRONG TWICE, worth recording because the failure
  looked like a defect and was not.** The penny-vs-coarse assertion needs a
  quote where **both bid and ask sit ON the nickel grid** (1.90 / 2.20) so no
  penny proof fires, while the half-spread (0.15) puts the RUNGS off the grid so
  the class is the only deciding fact. My first two fixtures used off-nickel
  quotes, which correctly proved penny for BOTH symbols and made the ladders
  identical. **The resolver was right and the test was wrong** — third attempt
  computed the values first and asserted from measurement.
  A companion test now pins the proof explicitly: a non-penny class quoting 2.11
  IS quoting in pennies, whatever any list says.

- **v4.58 — 2026-08-13 — FRC.2: THE ENTRY LIMIT LADDER AND THE FILL MODEL.**
  `limit_ladder` v1.4 + `execution/fill_model.py` v1.0 + `config` v4.13/v4.14 +
  19 tests. **SHIPS INERT — `ENTRY_LADDER_ACTIVE` defaults to 0.**

  **WHY THIS OUTRANKS EVERY SELECTION LEVER.** FRC.1 measured the fleet's gross
  edge at **+$2.70/trade against $126/trade of round-trip friction — ~2%% of the
  spread it trades in.** Capturing half the half-spread on entry is worth on the
  order of **$31/trade**. Fill quality is an order of magnitude larger than
  anything on the trade-selection list.

  **THE OPERATOR'S TECHNIQUE, his worked example:** bid 1.95 / ask 2.35 -> mark
  2.15. *"I would try 2.05, 2.10 and then 2.15"*, stepping every 15s, terminal
  rung sitting at mark and re-anchoring — *"let it sit at Mark in case price
  comes back and the plan can activate."* Encoded as fractions of the
  HALF-spread out from mark: `[0.50, 0.25, 0.00]`.

  **WHY THIS IS NOT v1.0's SHADE, WHICH v1.1 CORRECTLY REMOVED.** That one moved
  a FIXED NUMBER OF TICKS past the mark — *"guesswork about a spread we cannot
  see"*. This takes bid/ask explicitly and scales with the measured spread: a
  penny-wide quote shades a fraction of a cent, a dollar-wide one shades twenty.
  Same objection, different mechanism, and a test pins that a wide quote shades
  wider than a narrow one.

  **⚠️ VENUE INCREMENTS — operator: *"some contracts allow one cent increments
  others are five cents and even a few other are $.10."*** He is right and
  `round(px, 2)` was wrong. TWO dimensions: the CLASS decides penny eligibility,
  the PRICE LEVEL decides the step above $3.00. Penny class $0.01/$0.05;
  non-penny $0.05/$0.10. **An unpostable limit is rejected — or worse, SILENTLY
  ADJUSTED by the venue, which is a fill at a price nobody chose with nothing in
  the logs to explain it.** Unknown symbols are treated as NON-PENNY, because a
  coarser increment is always valid while a finer one may not be. Rounding is
  DIRECTIONAL (buy down, sell up): nearest-rounding would make ~half the rungs
  MORE aggressive than specified, which on a dime class is a nickel of
  unrequested aggression per rung. `PENNY_CLASSES` is a STARTING list and is
  flagged as unverified — membership is a broker/OCC fact, not derivable here.
  Coarse grids COLLAPSE rungs rather than posting the same price three times.

  **⚠️ AND THE FILL MODEL IS WHY THIS SHIPS INERT.** `paper_fill_price` books the
  posted price and assumes it fills — defensible AT THE MARK, indefensible
  INSIDE the spread. Shade without a fill test and every trade books 2.05 while
  no missed entry is ever modelled: **the more aggressive the rung, the larger
  the manufactured gain, and rung 1 would look like the best change this system
  has ever made.** `fill_model.would_fill()` tests the FAR SIDE — a BUY needs the
  ASK to come down to us, not the mid to drift — because testing the mid reports
  a fill roughly twice as often and recreates exactly the optimism being
  removed. A resting limit gets ITS price, not a better one. No fill returns
  None and carries NO PRICE, so "fill at the last rung anyway" is awkward by
  construction.
  ⚠️ QUEUE POSITION IS NOT MODELLED and cannot be from this data — a limit AT
  the touch may still not fill behind size. So this remains optimistic about
  QUEUE (second-order) rather than about PRICE (first-order, previously
  unmodelled entirely).

  **19/19 PASS**, including two deliberate-failure checks: `would_fill` must be
  able to REFUSE on a quote that never came to us, and the same quote on a penny
  vs nickel class must produce DIFFERENT ladders — otherwise the increment is
  not being applied.
  ⚠️ NOT WIRED into `entry_engine`. The primitives and their tests land first;
  turning `ENTRY_LADDER_ACTIVE` on without the fill model gating paper fills
  would produce a fake win, which is precisely what this delivery is built to
  prevent.

- **v4.57 — 2026-08-13 — `slippage_audit` v1.1: PRICED ZERO OF 805 JOINED
  TRADES.** `contract` is nested under `signal` in a scored row, not top-level.
  **Two working references existed in the repo and I matched neither** —
  `scorer_backtest` handles exactly this shape for `strategy`
  (`r.get("strategy") or (r.get("signal") or {}).get("strategy")`) and
  `factor_sweep`:138 reads `con = sig.get("contract")`. The join was fine; only
  the field path was wrong.
  **AND THE DIAGNOSTIC WAS THE REAL COST.** v1.0 kept ONE counter for "spread or
  premium or qty missing", so the output said 805 trades lacked *something*
  without naming which — a round trip on the box to learn what a per-field count
  would have printed. **A diagnostic that cannot name the failing field is not a
  diagnostic**, and this is the same class as the `orb_conversion` conversion
  rates above 100%: the output contained the tell and nothing surfaced it.
  Now counts each field separately and prints them on an empty result.

- **v4.56 — 2026-08-13 — FRC.1: WHAT DOES THE BOOK LOOK LIKE ONCE YOU CROSS?**
  `tests/slippage_audit.py` v1.0.

  **THE GAP NOBODY HAS PRICED.** `PAPER_FILL_SLIPPAGE_PCT` is **0.0** and
  commission is not modelled anywhere. `limit_ladder.paper_fill_price` books the
  MARK, and is explicit about what it assumes: *"paper is now honest about PRICE
  but still optimistic about FILL RATE — the residual gap to model later is
  no-fill risk, not slippage."* Under a mark-limit policy that is a defensible
  baseline — but **every number produced today (the +$463 book, TC.7's
  +$0.52/spread, the POP validation) is measured against a fill that may not
  happen at that price.**

  **IT DOES NOT NEED A FORWARD WEEK.** `contract.spread_pct_of_mid` is already
  journaled per scored trade and `contracts` is in trades.db, so friction is
  computable on sessions ALREADY COLLECTED. Round trip costs ONE FULL SPREAD
  (buy the ask = mid + half, sell the bid = mid - half), so
  `friction = spread_pct_of_mid * entry_premium * contracts * 100`.

  **⚠️ THREE LIMITS, PRINTED IN THE OUTPUT RATHER THAN BURIED:** the spread is
  measured AT ENTRY and 0DTE exit spreads are usually wider, so this is a **LOWER
  BOUND**; it assumes you cross BOTH ways, so the truth sits between this net and
  the gross and WHERE it sits is a **fill-rate** question the tool cannot answer;
  and commission is absent from the data entirely (`--commission` adds it
  explicitly rather than inventing one).

  **THE COHORT IT EXISTS FOR.** 279 of 843 trades close in under a minute, ~218
  of them `regime_flip` at a **0.3-minute median hold** for **+$1,308 gross**. A
  mark-limit posted and cancelled within eighteen seconds is exactly where
  "assume it fills" is least true, and that population pays entry AND exit
  friction on every trade. **If friction exceeds its gross it is a
  pure-subtraction population regardless of what the mark-based P&L says** — and
  that is a SELECTION finding, not a fill finding, so it does not go away by
  filling better. The report flags any cohort whose sign flips.

  Fixture-verified against planted truth: $60/trade friction across 10 trades
  reproduces exactly ($600 friction, $800 gross, $200 net) and the sub-minute
  cohort planted to invert does invert (**+$80 gross -> −$160 net**).

  **NEXT AFTER THIS (operator-approved order): the `spread_pct_of_mid` friction
  gate.** Widest quintile 125 trades, 37%% win, **−$4,626** — a PRE-ENTRY filter
  needing no forecast, and this audit's quintile table is its own evidence base.

- **v4.55 — 2026-08-13 — TC.6 IS BUILT AND WIRED.** `strategy/trend_credit_spread.py`
  v1.0 + `exit_engine` v4.17 + `main` v6.4 + `config` v4.12 + 8 tests (104 across
  today's suites).

  **THE TRADE.** Sell a defined-risk vertical BEYOND the broken ORB boundary
  after a runaway. A runaway broke the opening range and never retested, so the
  boundary IS the floor of that move and the level `orb_structure_stop` already
  calls thesis death — structure and invalidation become the same event.
  MEASURED (`spread_counterfactual --anchor orb`, runaway-handoff arm, 18
  sessions): EV positive at EVERY offset; the 0.00% cell — the strike AT the
  boundary — **n=30, +$0.52/spread, 90% terminal OK, 79% RECOVERED**, with entry
  sitting p50 +0.91% above the boundary. The STANDALONE control was mostly
  NEGATIVE on the same anchor, so **the edge is runaway-specific by
  construction** and `invalidation_reason == "runaway"` is a hard gate.

  **TIMING IS THE POP GATE, NOT A CLOCK.** Proximity cannot trigger it — in a
  runaway price moves AWAY from the boundary, so waiting for a return is waiting
  for the thesis to fail. The runaway confirmation is the event; POP decides
  when it may fire, and the same distance is a larger z later in the session.
  The afternoon-credit thesis arrives from the arithmetic rather than a
  hardcoded hour.

  **EXIT: BREACH OR NICKEL, NOTHING ELSE.** Operator's spec, and not a
  simplification — **the measured EV was HELD TO EXPIRY, UNMANAGED**, so a
  premium stop bolted on afterwards is a different trade whose paper results
  would not transfer. BREACH is a **CLOSED BAR** beyond the boundary (a wick is
  a touch; only a close decides acceptance). The ladder is now: 15:45 close →
  TC.6 breach/nickel (returns) → regime flip → ratchet → TP → nickel, so a TC.6
  leg can never reach the ratchet or the 25% stop. A test pins the ORDER, and a
  guard asserts no premium-stop symbol appears inside the branch — verified able
  to fail by injecting one.

  **STRIKE SELECTION HAS ONE OWNER** — it imports
  `IronCondorStrategy._select_beyond_rail` rather than cloning it.
  **DEFERS TO THE CONDOR** when a plan holds the symbol: the condor is already
  the only strategy allowed two concurrent positions, and a third credit spread
  on one underlying is unmanaged risk.
  **NOT blocked by AFD.1** — `DEBIT_DIRECTIONAL_STRATEGIES` is a name list and a
  credit vertical is not on it. Correct by construction.

  **`config` v4.12 — VERTICAL_HOLD_TO_ET (15:45).** The flatten ladder opens at
  15:40 so a DEBIT position gets a mark-limit phase before the cross, and that
  ladder is why it was NOT moved globally: opening it at 15:45 would force every
  EOD exit marketable — the exact failure `time_utils` v3.8 fixed, expensive on
  a book whose widest spread quintile already costs −$37/trade. **A short
  vertical has the opposite sign**: it decays TOWARD the holder, so 15:40-15:45
  is the steepest part of its curve. Operator: *"It's 5 more minutes of
  exponentially rising profit curve."*
  ⚠️ **NOT held past 15:45, and this is a hard limit.** Every instrument except
  SPX is AMERICAN-STYLE and PHYSICALLY SETTLED, so a spread finishing BETWEEN
  the strikes assigns the short and leaves an unhedged overnight stock position.
  "Defined risk" is true at settlement, not through assignment — and the paper
  engine has NO assignment model, so it would report a clean result that does
  not survive going live.

  **🔴 CND.8 — FOLLOW-UP, AND IT IS BIGGER THAN TONIGHT'S FIXES. THE CONDOR HAS
  NO STRUCTURAL EXIT.** `_condor_sibling_open()` is the ONLY cross-leg awareness
  anywhere in the exit path. The ratchet keys on `trade_id`, the stop reads that
  leg's own premium, the regime flip that leg's own side, the nickel that leg's
  own value. **A "condor" is two independent verticals plus one interlock plus
  the roll — the structure exists in the plan and in entry, and does NOT exist
  in the exit logic.** There is no combined-value exit, no net-credit stop, no
  "both sides safe, close the structure" rule. Measured consequence: 5 of 14
  condor symbol-days had BOTH sides stopped. Before designing it, re-measure the
  double-stop rate under condor v2 — the 5-of-14 predates dualfloor, when both
  legs fired 15 seconds apart mid-channel, which is the worst possible
  configuration for whipsaw.

  **⚠️ FOUR MISPLACED EDITS CAUGHT TODAY, all by verification rather than care:
  a duplicate config block, a changelog with no code behind it, two silent
  no-op `.replace` calls, a block landing in `_evaluate_orb` instead of the
  condor path, and an instantiation landing inside an `except` body.** Method
  changed in response: slice to the target function FIRST, then assert the
  enclosing function by AST afterwards, and assert module-level bindings by AST
  rather than by grep. Every one of those was invisible to `ast.parse`.

- **v4.54 — 2026-08-13 — CND.7: THE RATCHET WAS DISASSEMBLING WORKING CONDORS.**
  `exit_engine` v4.17 + `config` v4.11 + 7 tests.

  Operator, on being shown the exit ladder: *"So you're telling me a take profit
  signal could disassemble a working condor? And also a floor percentage loss
  would fire before the roll plan went into effect? I don't want either of those
  scenarios ever happening."*

  **ONE OF THE TWO WAS ALREADY PREVENTED.** The take-profit at exit_engine:1412
  already reads `and not self._condor_sibling_open(record)`, is time-gated to
  after the entry cutoff, and the sibling check **FAILS CLOSED** (True on error
  = treat as condor = do not TP). It can only ever fire on a standalone.

  **THE OTHER WAS REAL, AND THE RATCHET IS THE MECHANISM.** The base -25% stop
  only ever fires on the TESTED side — a credit spread's value RISES as price
  approaches your short. **The ratchet does the opposite: it tightens the
  UNTESTED side's stop to breakeven at +20% and +20%-locked at +40% precisely
  BECAUSE that side is winning.** On the reversal the tested leg stops at -25%
  and the untested leg hits its ratcheted stop as well — **a leg price never
  went near, closed by a stop that exists only because it was profitable.**
  That is the double-stop (**5 of 14 condor symbol-days had BOTH sides
  stopped**), and it fires BEFORE the roll can ever be used, because the roll
  needs a tested side. `_condor_sibling_open()` was sitting right there and the
  ratchet never called it.

  **FIX:** while the sibling is open, the base floor is the ONLY stop. No tier,
  and the stored high-water is neither applied nor updated, so a leg returning
  to standalone resumes from a level it genuinely earned rather than one set
  while the structure was intact.

  **NOT CHANGED, and I nearly over-applied this:** the adverse-regime-flip exit.
  It is DIRECTION-AWARE — a call spread exits only on TRENDING_BULL, which IS
  price rising toward that short strike — so it already fires only on the
  threatened side and is a tested-side exit by construction.

  **PRESERVED:** `condor_stop` went **0% -> 19% win** after the ratchet shipped,
  but that evidence came mostly from STANDALONES (18 of 46 legs never got a
  second side). Scoping keeps the gain exactly where it was measured and removes
  it only where it takes apart a working structure.
  ⚠️ ACCEPTED COST, stated to the operator before shipping: an untested leg that
  runs to +40% and reverses now gives it back rather than locking +20%.

  **⚠️ THE STRUCTURAL FINDING UNDERNEATH, worth its own workstream.**
  `_condor_sibling_open()` is the ONLY cross-leg awareness in the entire exit
  path. The ratchet keys on `trade_id`, the stop reads that leg's own premium,
  the regime flip that leg's own side, the nickel that leg's own value. **A
  "condor" is two independent verticals plus one interlock plus the roll — the
  structure exists in the plan and in entry, and does NOT exist in the exit
  logic.** There is no combined-value exit, no net-credit stop, no "both sides
  safe, close the structure" rule. That is the next condor question and it is
  bigger than this fix.

  **7/7 PASS**, including a deliberate-failure check (scope on vs off must
  DIFFER, and must LOOSEN not tighten) and a source-shape assertion that the
  engine still contains the branch the test models — scoped to a definition, not
  a mention, per WORKING_AGREEMENT 20.

- **v4.53 — 2026-08-13 — PF.5 IS WIRED. `main` v6.3 + `config` v4.10 + condor
  `decide()` + 27 tests.** The pitchfork overlay now has a consumer that trades.

  **THE GATE TAKES EFFECT.** `_condor_rails()` returns the DAILY rails or None,
  and **None means NO CONDOR** — operator: *"consider the condor off the table
  if we don't have guardrails. That is the insurance policy that eliminates a
  bad decision in an unpredictable session."* **DEFAULTS OFF-SAFE:** a caller
  that forgets to pass rails gets no plan rather than a silently un-anchored
  one. The failure mode must be missing trades, never unguarded ones, and a test
  pins it.
  **MEASURED COST, from `pitchfork_digest` 2026-08-12:** 13 distinct daily forks
  across **7 of 15 boxes** (CVX, GS, LLY, QQQ, TLT, UNH full-session; MU
  partial). So roughly half the fleet becomes condor-ineligible. Accepted:
  *"I'm ok with not getting the condor if the fork isn't there."*

  **⚠️ AND THE DAILY CHANNEL POSITION SAYS WHAT IT WILL ACTUALLY PRODUCE.** On
  the 1d frame `pos_pct` runs p10 **40.8** / p50 74.2 / p90 98.5 — price lives
  in the UPPER HALF and **essentially never visits the lower daily tine** (the
  1h frame is the mirror image at p10 3.0, which is exactly why it is the wrong
  guardrail for a position you hold). Under the touch trigger the CALL side arms
  often and the PUT side rarely, so expect **mostly call-side standalones and
  few completed two-sided condors.** That is arguably correct behaviour — if
  price never approaches the lower tine the put side was never rich, and selling
  it anyway is the thing this change exists to stop. One session, 13 forks:
  a shape, not a distribution.

  **THE ANCHOR.** The rail replaces the BB half of the dual floor; **`0.80 * EM`
  survives as a MINIMUM DISTANCE** so a rail sitting on top of spot can never
  produce a strike with no breathing room — that fallback bled for ~3 weeks and
  does not come back through a new door. Selection then applies, in order:
  beyond the rail → beyond the min distance → **beyond the session extreme** →
  quote width within `CONDOR_MAX_QUOTE_WIDTH` → **POP >= `CONDOR_MIN_POP`** →
  most liquid by bid/ask width, tie-break nearest the rail. Every skip logs the
  full reason set, so the gate can be calibrated from its own rejections rather
  than guessed twice.

  **`_session_extremes()` takes the max across BOTH frames**, because each is a
  rolling window and neither is guaranteed to reach 09:30. A late window
  UNDERSTATES the extreme, which LOOSENS the filter rather than tightening it —
  so the failure direction is a missed rejection, not a wrong one. A missing
  extreme is logged as a **plumbing fault** rather than silently trading with
  the filter switched off.

  **`config` v4.10** adds `CONDOR_MAX_QUOTE_WIDTH` (0.25 of mid). Ranking alone
  NEVER REFUSES — it returns the least-bad strike even when every candidate is
  broken, and on 0DTE a nickel of noise on a wide quote trips the 25% stop on
  the QUOTE rather than on price. Stated PRIOR reasoned from an adjacent
  population, labelled as such.

  **27/27 PASS**, now including the end-to-end gate (`rails=None` → no plan) and
  a signature smoke test, because a `TypeError` on three new kwargs would be a
  live crash on every condor evaluation past 11:11.
  ⚠️ `CONDOR_PF_TIMEFRAME` and `CONDOR_MAX_QUOTE_WIDTH` were BOTH used before
  being imported and caught by the AST name sweep — the third and fourth such
  catch today. That sweep now runs before any condor packaging, and the gate
  does a real `import` rather than only an `ast.parse`.

- **v4.52 — 2026-08-13 — PF.6: THE POP FLOOR, AND IT VALIDATES OUT-OF-SAMPLE.**
  `config` v4.9 + condor helpers + 25 tests (was 15).

  Operator: *"Selling late afternoon premium on zero DTE is incredibly risky so
  just make sure that the factors appear favorable before executing. There
  should be a reasonable expectation of trade success better than 50-50...
  somewhere near the 70 to 80%% range."* And on tone: *"this approach is already
  inherently risky. I'm aware of that and I'm comfortable with it so don't be
  too restrictive."* → floor at the BOTTOM of his band, **0.70**, env-tunable.

  **POP = Phi(z), z = distance / (sigma * sqrt(bars_left))**, horizon to the
  **15:45 flatten** rather than the bell, because a condor leg is CLOSED at the
  hard close and using 16:00 overstates T. Driftless and normal deliberately —
  a drift term would be a forecast, and the one thing measured all day is that
  this system's directional forecasts do not separate. Normal understates fat
  tails, so it reads slightly OPTIMISTIC on the extremes; the 0.70 floor absorbs
  some of that. Degenerate inputs return 0.0 and FAIL — a missing ATR must never
  read as a safe trade.

  **⚠️ VALIDATED ON DATA IT WAS NOT FITTED TO.** TC.7's handoff arm, terminal-OK
  against measured EV: **58%→−0.23 · 54%→−0.33 · 63%→−0.24 · 67%→−0.09** then
  **76%→+0.33 · 78%→+0.32 · 88%→+0.35**. **Every cell below 70%% lost money;
  every cell at/above 76%% made it.** The sign flips inside the operator's stated
  band. Nobody searched for 0.70 — it is a stated risk preference, not an
  argmax, which is exactly why it is usable and why it must NOT be re-tuned on
  this same data later. Honest cost: on the STANDALONE arm the sub-70 cells were
  marginally POSITIVE (+0.08 at 61%%, +0.04 at 69%%), so the floor gives up ~$0.12
  a spread there; all meaningful EV (+0.20 to +0.67) is above 70.
  ⚠️ ONE arm, ONE conviction band, ~40 spreads a cell over 25 symbol-days, and a
  sign flip read across two cells either side. Striking, not yet a fitted
  threshold.

  **THE TIME-OF-DAY PROPERTY IS THE POINT.** Measured in the module: 3.0 points
  out is **POP 0.829 with 40 bars left and 0.983 with 8** — identical geometry,
  different session remaining. Every offset table built before this pooled hours
  and could not express it, which is why the credit_edge hour curve looked like
  an edge appearing when it was really T shrinking.

  **QUOTE-WIDTH FLOOR added alongside**, because **ranking alone never
  refuses** — `_liquidity_rank` returns the least-bad strike even when every
  candidate is broken. On a 0DTE credit spread a nickel of noise on a wide quote
  trips the 25%% stop on the QUOTE rather than on price. Default 25%% of mid as a
  stated PRIOR, not a fit: factor_sweep put the worst continuation quintile at
  `spread_pct_of_mid` 0.13-0.88 and the two best under 0.043, which is an
  adjacent population (debit entries, not condor shorts) — so it is reasoned
  from a neighbour and labelled as such. The rejected-leg log is what would fit
  it properly.

  **⚠️ SIX MISSING IMPORTS CAUGHT BY AN AST SWEEP BEFORE PACKAGING** —
  `HARD_CLOSE_ET`, `CONDOR_MIN_POP`, `CONDOR_POP_BAR_MIN`,
  `CONDOR_PITCHFORK_ANCHOR`, `CONDOR_REQUIRE_FORK`, `CONDOR_PF_FLAT_SLOPE`. The
  first would have been a live **NameError on the first condor evaluation past
  11:11** — the same class that crashed IWM twice (continuation `mid`, butterfly
  `_mult`) and is only ever caught by a box falling over. `ast.parse` +
  import-name diff, then a real `import`, now runs before any condor packaging.

  **25/25 PASS**, including four deliberate-failure checks: each of the three
  strike filters must MOVE the selection when relaxed; the POP floor must change
  which strike wins; and **the same near strike must FAIL early and PASS late**,
  which is the only way to know `bars_left` actually reaches the calculation
  rather than the gate being time-blind.

- **v4.51 — 2026-08-13 — PF.5: THE PITCHFORK GETS ITS FIRST CONSUMER.**
  `config` v4.8 + `iron_condor_strategy` v-pfanchor + 15 tests.

  **STATE OF THE OVERLAY, CONFIRMED BY READING IT.** The pitchfork is NOT in
  concept phase — `analysis/pitchfork.py` is a full implementation (Fork with
  `median_at`/`upper_at`/`lower_at`/`rails_at`/`is_born_by`/`rail_at_time`,
  pivot detection, variants, the §4.3.6 containment builder),
  `pitchfork_lifecycle.py` handles birth/invalidation/supersession, and
  `pitchfork_observer.py` journals the rails on a cadence. **But there is
  exactly ONE call site in the entire repo** — `main.py:2091`, `_pf_snap`,
  wrapped in a bare `except: pass`, gated on `OT_PF_OBSERVE` — and **nothing
  has ever read the rails back.** Built, live, unconsumed. This is the consumer
  the white paper pre-registered, and the reason it pre-registered it: strike
  placement produces a CREDIT, directly comparable on identical tape.

  **DAILY FORK, and the reasoning is the operator's:** *"It's a guardrail, not
  the road."* A daily fork is invalidated only by DAILY closes, so an intraday
  session **cannot kill it** — the rail a spread was sold against is still there
  while the spread is open. The hourly fork has a measured p50 lifetime of 5
  bars plus a k=3 confirmation lag, so it can be born mid-window and dead before
  the close; that re-anchors intraday, which is another indicator, not a
  guardrail. **NO FORK -> NO CONDOR**, accepted volume cost: *"I'm ok with not
  getting the condor if the fork isn't there. We have other trades & the trend
  participation credit spread is going to fill in a lot of the gaps."*

  **THE STRIKE RULE — three filters, then liquidity.** *"the short strike should
  be just outside the range of the rail at the most liquid strike where price
  has still not exceeded."* A strike qualifies only if beyond the RAIL, beyond
  the surviving `0.80 * EM` MINIMUM DISTANCE (retained so a rail sitting on spot
  cannot produce a strike with no room — the exact ~3-week bleed v-dualfloor
  fixed), and **beyond the SESSION EXTREME**. That last one is new: nothing in
  the codebase has ever tested a short strike against the session's own high or
  low, and **a level price has already traded through today is a level the
  market has PROVEN it can reach.** No inside fallback, ever.

  **⚠️ AND A DEAD INPUT FOUND WHILE BUILDING IT.** The old selector ranked
  liquidity as `open_interest + volume` — and `factor_sweep` found BOTH CONSTANT
  across the entire joined sample. So `max_liq` was 0, the `else: top =
  eligible` branch took **every** call, and **"most liquid" has silently
  resolved to "nearest the floor" since v-dualfloor shipped.** The comment even
  anticipated the case (*"no OI/vol data"*), which is why it degraded quietly
  instead of failing. Ranking now keys on **BID/ASK WIDTH** — populated, and the
  measure that actually matters on a 0DTE credit spread where a nickel-wide
  quote trips a stop on quote noise rather than on price. OI/volume survive only
  as a tie-break and only when non-zero, so it is correct either way.
  ⚠️ STILL WORTH CONFIRMING ON A BOX: whether OI/volume are genuinely zero LIVE
  or only dropped in the journal. Different bug, different fix.

  **LEG ORDER FROM SLOPE.** Up-sloping fork fills the PUT side first (price
  travels the lower rail toward the upper across the session), down-sloping
  fills the CALL side first. `CONDOR_PF_FLAT_SLOPE` exists because **a SIGN is
  not a SLOPE** — below it the drift is noise and ordering off it reads a coin
  flip as structure, so the caller keeps its existing proximity rule.

  **ACCEPTED RISK, his words:** *"If it gets breached, then our fork may also
  become invalid & I can live with that because we are accepting that risk for
  an asymmetric payoff if it holds."* So a breach and a fork invalidation are
  THE SAME EVENT — structure and overlay agree on when the thesis died.

  **15/15 PASS**, including two deliberate-failure checks: relaxing each of the
  three filters in turn must MOVE the selection (otherwise that filter is not
  applied and the happy-path tests would pass against a version ignoring it),
  and flipping which contract carries the tight quote must move the selection
  (otherwise width is not deciding). The liquidity test runs with **OI and
  volume both ZERO** — the state the fleet is actually in — because a test with
  populated depth would pass against the broken ranker too.
  ⚠️ NOT YET WIRED: `decide()` still needs the rails and session extremes
  plumbed from main.py. The helpers are tested in isolation; the strategy does
  not consult them until that lands.

- **v4.50 — 2026-08-13 — LIQ.4: THE LIQUIDITY LEDGER. `analysis/liquidity_ledger.py`
  v1.0 + 15 tests.** Operator, on being told the pool set lives only in RAM:
  *"Our liquidity mapper exists only in memory??? It needs to reset at the
  beginning of RTH and capture at least 3 previous highs & lows and write them
  to a location and update it when the level is touched (held/breached)."*

  **WHAT WAS ACTUALLY WRONG — worse than "not persisted".**
  `LiquidityMapper.analyze()` opens with `lmap = LiquidityMap()` and re-derives
  every pool from the candle window ON EVERY CALL. Consequences:
  · **`touch_count` is not a running count** — it is `len(cluster)`, how many
    bars in the lookback sat at that level when the map was last rebuilt. A
    floor price hammers into five times today does not accumulate.
  · `swept` / `rejection_confirmed` are per-build snapshots — the same defect
    class LIQ.3 fixed one level down, where `closes_beyond` was a birth-time
    snapshot that had to become a per-tick question.
  · a clean SINGLE-touch low that price respects three times **never becomes a
    pool at all** — `_find_pools` requires >=2 equal bars within
    EQUAL_LEVEL_PCT.
  So nothing could answer *"is this floor holding?"*, and nothing was archived.

  **THE SPEC, and the operator's sentence is the whole design:** *"the wick
  counts as a touch, but only a close counts as acceptance or rejection."*
  **THREE counters per level, never one** — `touches` (wick contact, says
  nothing about who won), `holds` (closed back on the origin side), `breaches`
  (closed beyond). A single number cannot distinguish a level being DEFENDED
  from one being GIVEN UP, which is the entire question the floor thesis asks.
  *"It should live on the standalone bot boxes"* → per-box
  `data/liquidity_ledger/<date>/<SYMBOL>.json`, the same convention as the chain
  archive. The bot owns its level book; control is a consumer, never the source.
  Resets at RTH open, seeded with PDH/PDL and prior extremes, >=3 per side.

  **DESIGN CALLS WORTH KEEPING:**
  · **Seeds are supplied by the CALLER.** The ledger does NOT derive what a
    prior high is — `LiquidityMapper` owns that, and a competing derivation here
    is exactly the second-lineage failure WORKING_AGREEMENT 7 forbids.
  · **Closed bars only.** Feeding a forming bar counts a wick that has not
    finished printing and a close that is not a close.
  · **Atomic write** via tempfile + `os.replace`. A strategy may read the file
    while the loop writes it, and a half-written JSON reads as an EMPTY level
    set — indistinguishable from "no levels found", i.e. a silent wrong answer
    rather than a loud failure.
  · **Fire-and-forget**, every entry point swallowing every exception, per
    `chain_snapshot.py`. Telemetry that can halt trading is a liability.
  · **v1.0 WRITES AND DOES NOT GATE.** Prove the levels are the ones a human
    would have drawn before wiring them to anything that fires.

  **15/15 PASS.** The suite is built around the one failure that would make
  every floor in the book look strong: **counting a bar that never reached the
  level as a HOLD.** Two deliberate-failure checks run — one proving the reach
  test is applied *and* not over-strict (both directions fail silently), one
  proving two bars with IDENTICAL wicks and opposite closes score differently,
  which is the only way to know the CLOSE is deciding acceptance.
  ⚠️ NOT YET WIRED into the tick path — the module collects nothing until it is.
  That is the next step and it is deliberately separate from the build.

- **v4.49 — 2026-08-13 — ✅ THE ORB ANCHOR IS SUPPORTED, AND `--anchor floor`
  FOR TRENDING_BEAR.**

  **BFL.1 — THE OPERATOR'S STRUCTURAL STRIKE RULE WORKS, AND THE CONTROL PROVES
  IT IS RUNAWAY-SPECIFIC.** `--anchor orb`, conviction [1.0,1.01), 18 sessions.
  RUNAWAY HANDOFF (150 spreads / 18 symbol-days; long on the subset −$746):
  entry-to-boundary p10 +0.02% · p25 +0.24% · **p50 +0.91%** · p75 +1.85% ·
  p90 +2.65%, only 10% at/through. EV/spread **0.00% n=30 +0.52** (47% touched,
  **90% terminal OK, 79% RECOVERED**) · 0.25% +0.32 · 0.50% +0.24 · 0.75% +0.62
  · 1.00% +0.57 · 1.50% +0.67 · 2.00% +0.39 · 3.00% +0.46 — **every cell
  positive**, and the 0.00% cell (the strike AT the boundary, his literal
  proposal) is the only one clearing n=30 and the strongest result measured so
  far.
  STANDALONE CONTROL: entry-to-boundary **p50 −0.21%, 64% AT OR THROUGH the
  boundary**; EV mostly NEGATIVE (−0.21 / −0.51 / −0.09 / −0.17). **The inverse
  of the entry-anchored run, where the control beat the treatment everywhere.**
  MECHANISM: the ORB boundary is only a floor WHEN THERE WAS A RUNAWAY — price
  broke the range and never retested, so the boundary sits genuinely below the
  fill. Without a runaway it is at or above the fill and the structural strike
  lands inside the money. **The rule is runaway-specific by construction.**
  It also escapes TC.7's finding (conditioning a spread on the CONTINUATION
  signal made it worse than unconditional) because it conditions on the RUNAWAY
  and anchors on the RANGE — different trigger, different strike rule.
  ⚠️ Only the 0.00% cell clears n=30; the rest are UNDERPOWERED (n=10-29). The
  modelling asymmetry still favours the spread, but the arm is positive at every
  offset so the tilt is not carrying the result.
  **DISPOSITION: the first thing measured today that supports BUILDING rather
  than cutting.**

  **BFL.2 — `--anchor floor` + `--regime`, for the TRENDING_BEAR thesis.**
  Operator: *"There is no way I'm going to have the bots sit out during trending
  bear"* and *"massive downward moves almost always end with them hitting a hard
  floor. There's some spot of support that they hammer into and they cannot go
  past it."* TRENDING_BEAR is the worst regime in the book — **118 trades, 36%
  win, −$7,373.50**. The structure is his ORB rule mirrored: **sell a put spread
  BENEATH the floor rather than buy puts into the move**, which also explains
  the losses mechanically — a long put chasing a down move dies when the move
  stalls at support, exactly what a debit cannot survive and a credit is
  indifferent to. Both his cases reduce to ONE structure: a bull move's floor is
  the level it broke from, a bear move's floor is the support it hammers into;
  sell beneath it either way.

  **⚠️ COLLECTION GAP FOUND WHILE BUILDING IT — THE POOL LIST IS NOT ON DISK.**
  `LiquidityPool` carries price / kind / touch_count / name / is_named / swept
  and lives ONLY IN MEMORY; there is no `liq_ctx` in the journal and nothing
  writes the pools. **The input to every named-level decision is not archived** —
  same class as the chain archive before 2026-07-23. So the floor is
  reconstructed from the tape, and ONLY the deterministic parts: **PDL** (prior
  session low) and **SESS_LOW** (running low up to the entry minute — up to,
  never past, since a level formed after the fill is information the trade did
  not have). **EQUAL-LOWS ARE DELIBERATELY EXCLUDED**: reproducing the mapper's
  swing definition here would create a SECOND LINEAGE of the same concept, which
  WORKING_AGREEMENT 7 and the pitchfork white paper both forbid, and a floor
  built on a slightly different pivot rule is not the floor the bot would have
  used. **Two exact levels is the honest scope and the result is a LOWER BOUND
  on what a full pool set would find.** Fixture-verified: planted PDL 492.0 and
  SESS_LOW 494.0 against a 500 entry selects SESS_LOW at p50 **+1.20%**.

- **v4.48 — 2026-08-13 — TC.7 ANSWERED (NEGATIVE), AND `--anchor orb` FOR THE
  OPERATOR'S STRUCTURAL STRIKE RULE.**

  **TC.7 RESULT — THE SPREAD REROUTE IS NOT SUPPORTED.** conviction [1.0,1.01),
  width 5, 18 sessions. HANDOFF (128 trades, 293 spreads, 25 symbol-days, actual
  long **−$3,065**) EV/spread: 0.25% **−0.23** · 0.50% **−0.33** · 0.75%
  **−0.24** · 1.00% **−0.09** · 1.50% +0.33 · 2.00% +0.32 · 3.00% +0.35.
  **Negative at every strike distance anyone would actually sell.**
  STANDALONE control (128 trades, 393 spreads, 34 symbol-days, long −$1,208):
  +0.08 · +0.04 · +0.20 · +0.36 · +0.62 · +0.67 · +0.56 — **better at EVERY
  offset.** That is the pre-registered discriminator firing: the spread does
  better on the path where the long was already less bad, so **the handoff peg
  is simply worse tape — worse for longs AND worse for spreads.** Rerouting
  moves the loss rather than removing it.
  **⚠️ THE THIRD READING IS THE CONSTRAINT ON TC.6.** `credit_edge`'s
  UNCONDITIONAL afternoon spot-anchored call side ran **+0.65 to +0.66** at the
  same offsets. Both TC.7 arms are worse than that everywhere. **Conditioning a
  short vertical on a continuation signal makes it WORSE than selling one at a
  fixed distance from spot with no signal at all.** If credit spreads are the
  afternoon vehicle, the entry trigger is not where the edge lives.
  ⚠️ COVERAGE: only ~42 of 128 trades priced per offset (49 / 40 skipped for no
  chain within 10 min), so ~a third of each population is measured — and it is
  the third with a chain archive at that minute. Uncorrected selection risk.
  ⚠️ The modelling asymmetry still FAVOURS the spread and the handoff arm is
  negative anyway, which strengthens the verdict rather than weakening it.

  **`spread_counterfactual` v1.3 — `--anchor orb`.** Operator: *"set the put
  spread at the top of the orb range for a runaway long and the bottom of the
  orb range for the call spread on a runaway short."* **The broken ORB boundary
  IS the invalidation level** — on a runaway long price broke the range and never
  retested, so the ORB high is the floor of the move and the level
  `orb_structure_stop` calls thesis death. A put spread short there loses only if
  the setup was wrong. Structural, not a fitted percentage.
  **THE ENTRY-TO-BOUNDARY DISTRIBUTION IS PRINTED FIRST AND IT IS THE ANSWER.**
  v1.2 found the handoff negative below 1.00% and positive from 1.50%. The
  handoff enters on a pullback into an FVG above the broken range, so the
  boundary sits some distance below the fill. **If that distance clusters at
  1.5%+ the rule is structurally in the money by construction; if it clusters
  near 0.5% it is not, and no strike tuning fixes it.** Reconstructed from the
  09:30-09:35 bars already in the OHLC — no new collection.
  ⚠️ Offsets mean distance beyond THE BOUNDARY under this anchor, and 0.00% (the
  operator's literal proposal) is included. ⚠️ Run the standalone control on the
  identical anchor: if it also wins, this is a general edge and not a
  runaway-specific one. Fixture-verified — planted ORB high 497.0 against a 500
  entry reads p50 **+0.60%** exactly.

- **v4.47 — 2026-08-13 — `spread_counterfactual` v1.2: OOM-KILLED. BOUNDED WORK,
  UNBOUNDED MEMORY.** v1.1 cached every parsed chain snapshot for every
  `(date, symbol)` it touched and never evicted — ~78 snapshots x ~120 contracts
  x 13 fields as Python dicts, times a couple of hundred symbol-days, resident
  simultaneously. The kernel killed it before one row printed, on BOTH arms.
  **THE FIX IS SCOPE, NOT CLEVERNESS:** group the population by
  `(date, symbol)`, collect that group's target minutes BEFORE opening the file,
  stream the `.jsonl.gz` once keeping only snapshots within the match window of
  a target, price the group, drop it. The file is still read exactly once; peak
  residency is one symbol-day. Verified identical output to v1.1 on the fixture
  with **peak snapshots resident = 2**.
  ⚠️ **WHY NO FIXTURE CAUGHT IT, and this is the third instance of one shape
  today.** The fixture is one symbol, one date, one chain file — **a
  single-symbol-day fixture cannot exercise a cache that only grows across
  symbol-days.** Directly parallel to v1.0's single-snapshot fixture missing the
  sort tie, one level up in scale. Pattern to carry: **a fixture tests the
  logic at n=1; it does not test what the logic COSTS at n=many.** Scale
  failures need a fixture with scale, and this one still has none — the guard
  here is the restructure plus a printed peak-residency line, not a test.
  Related standing context: the SPX box's known OOM at a 419M peak. Control is
  not immune, and read-only tools are not exempt from memory discipline.

- **v4.46 — 2026-08-13 — `spread_counterfactual` v1.1: CRASH ON THE FIRST REAL
  RUN, AND THE FIXTURE COULD NOT HAVE CAUGHT IT.** `sorted(snaps)` on
  `(minute, dict)` tuples — when two chain snapshots share a minute, Python
  falls through to comparing the DICTS and raises. Now sorted on the KEY ONLY.
  **THE REUSABLE LESSON IS THE FIXTURE, NOT THE SORT.** The fixture wrote ONE
  snapshot per symbol-day, so the tuple comparator was never reached — **a
  single-element list cannot exercise a sort, and a fixture that cannot produce
  a TIE cannot test a tie-break.** Same family as the deliberate-failure rule
  already in the method notes: a fixture that cannot fail is not evidence. The
  fixture now writes two snapshots at the same minute and reproduces the crash
  against v1.0.
  ✅ NOT AFFECTED: the join and the conviction filter were correct on the first
  run — both arms returned **population 128, unmatched 0**, exactly the band
  HND.1 identified.

- **v4.45 — 2026-08-13 — HND.1 + TC.7. ONE BAND CARRIES MORE THAN THE WHOLE
  STRATEGY LOSS, AND ENG.2 CLOSES NEGATIVE.**

  **✅ ENG.2 CLOSED — THERE WAS NEVER AN ORB VOLUME COLLAPSE.** `orb_conversion`
  v1.1 with the `trade_id` dedupe, 6 covered sessions per arm: arm A br/sess
  **23.5** ent/sess **7.3** conv **31%**; arm B br/sess **32.0** ent/sess **9.3**
  conv **29%**. Conversion FLAT against the tool's own ~2% MDE, break supply UP
  36%, entries UP 27%. No gate started and the setups did not stop. **The
  "~$4,400/session of lost ORB" was duplicate inflation and is VOID.** ORB trades
  eight or nine times a session and always has. Dedupe visibly working — pre-07-20
  sessions now read 1/0/7/4/5 entries where v1.0 printed 88/88/95/31/38.
  **Disposition: stop looking for a recoverable ORB gate.**

  **🔑 HND.1 — THE PEGGED-CONVICTION HANDOFF BAND.** `factor_sweep --setup-type`,
  `reg.conviction` bands. **handoff, conviction EXACTLY 1.00: n=128, 41% win,
  −$52/trade, −$6,623** — larger than ContinuationStrategy's entire −$6,351;
  everything else in continuation nets roughly +$272. **The SAME peg through
  STANDALONE: n=128, 50% win, +$1/trade, +$179.** Same conviction, same count,
  opposite outcome.
  **AND THE RELAXED FLOOR IS NOT THE DEFECT.** `CONTINUATION_CONV_FLOOR = 0.45`;
  standalone's lowest band starts at **0.4554** (right at it) while handoff
  reaches to **0.2554** (below it) — so the floor demonstrably steps aside, **and
  those sub-floor trades are the BEST band in either table** (77 trades, 57% win,
  +$23/trade, +$1,745).
  **MECHANISM:** the handoff's licence is that the label is UNRELIABLE after a
  runaway. When the label is ALSO pegged at maximum you have the runaway AND
  total regime confidence — the move is finished and obvious. Lateness in its
  purest form.
  ⚠️ **NOT A ZERO-WINNER CUT** (53 winners in the band), so it must not ship as a
  hard gate under the pre-registered rule. Routing/sizing signal. Both tables
  correctly read NON-MONOTONE / UNDERPOWERED — this is a single-band
  concentration, not a trend. The two paths have OPPOSITE shapes (standalone
  loses at LOW conviction and is flat at the peg; handoff wins at LOW and dies at
  the peg) and probably should not share a scorer profile.

  **TC.7 — `tests/spread_counterfactual.py` v1.0: would these have paid as short
  verticals?** Operator: *"those opportunities would have fared better as
  vertical spreads instead of paying long premium to chase spent moves."*
  **TERMINAL ONLY, and that is his correction, not a detail.** The first design
  counted MAXIMUM ADVERSE EXCURSION — wrong, and the same error
  `tcs_floor_durability` v1.1 was rewritten to fix: MAE counts a TOUCH, a
  defined-risk spread only loses on ACCEPTANCE. *"With a credit spread it doesn't
  matter that it turned against me as long as it doesn't breach."* On the impulse
  population that distinction was worth everything — intraday held 14.7%,
  terminal OK 56.1%, **41.4% RECOVERED**. **Every trade that dipped through a
  candidate short strike and came back is a LOSS for the long and a WIN for the
  spread**, and an MAE test measures that whole population out of existence. The
  tool reports INTRADAY / TERMINAL / **RECOVERED** separately and never merges
  them. "Never favorable" is IRRELEVANT here — it says the LONG never went green.
  Geometry: a bull handoff buys calls, so the credit equivalent sells a PUT
  spread BENEATH entry; the adverse side is the side that matters, but only at
  the close.
  ⚠️ **THE ASYMMETRY IS PRINTED IN THE OUTPUT, not left to the reader:** the long
  number is REAL (fills, slippage, management, early closes), the spread number
  is MODELLED (archived quotes at the posted bid, held to expiry, no management,
  no assignment, no commission). That tilts toward the counterfactual by
  construction — **a narrow win for the spread is a NULL, not a result.**
  Fixture-verified on a planted dip-and-recover: RECOVERED 100% at every offset
  price touched through, all terminal-OK.

  **`tests/scorer_backtest.py` v1.2** — `load_trades` now carries the raw row
  (for `underlying_entry`/`direction`) and **de-duplicates by `trade_id`**.
  ⚠️ Consequence: the joined counts printed by v1.0/v1.1 were slightly inflated;
  `trade_report` reduces 1,567 rows to 843 unique even post-trim.

- **v4.44 — 2026-08-13 — TIMELINE PAUSED; THREE TOOL DEFECTS FIXED; THE STOP
  DEFAULT MOVED.**

  **⚠️ THE CLOCK IN PART 0 IS SUSPENDED.** Operator, 2026-08-13: the Sep 8
  go-live, the Aug 17 deploy Monday and the Aug 17→30 L2.6 freeze window are
  **paused indefinitely until P&L standings recover**. Consequence for
  everything below: **entry-affecting changes are no longer gated to a Monday** —
  they ship when built and verified. His read on how we got here: *"We've been
  super permissive with our entries to evaluate our stops so in all fairness,
  the stops are doing the heavy lifting on the entire system right now and it
  seems like the only winner that's ungated is the orb trade."*

  **`config` v4.7 — `CONTINUATION_STOP_LOSS_PCT` 0.25 → 0.15.** The REPO DEFAULT
  is the fleet lever; the env var is the per-box override. Floor sweep: n=66
  across 9 sessions, 0% win, a 15% floor stops all 66 with ZERO winners cut,
  +8.85 units of entry premium against +2.25. Rides the bake already scheduled.

  **`tests/orb_conversion.py` v1.1 — DE-DUPLICATE BY `trade_id`, and v1.0's
  headline was an artefact.** trades.db is cumulative and harvest copied the
  whole growing file into each dated folder, so the date meant "when pulled".
  76% of rows were duplicates (measured by `trim_trade_dbs`), the live folders
  were trimmed and the pre-07-23 archive was not — so v1.0 inflated one side
  only. **That is what produced the 07-23 "collapse" from 73 entries to 5 and
  the impossible 391%/268%/317% conversion rates. Entries over breaks cannot
  exceed 100%; the arithmetic was the tell.** Now keyed on `trade_id` across the
  run AND attributed to the session in `entry_time`; rows without an id are
  counted and reported rather than dropped. Fixture-verified against a planted
  cumulative corpus: 18 distinct trades recovered from folders totalling 72 rows.
  ⚠️ **`tests/engine_arms.py` STILL LACKS THIS DEDUPE — ENG.1 stays void.**

  **`tests/factor_sweep.py` v1.1 — two defects of my own, both found by reading
  v1.0's output rather than by a test.**
  (a) **HOURS WERE UTC LABELLED AS ET.** `entry_time` is UTC; v1.0 read `.hour`
      off it directly, so bands printed 13..17 and `minutes_from_open` started
      at 245 for a 09:30 open. This is the exact mistake `excursion_report`
      documents and refuses to make. Now ZoneInfo-converted with a NAMED
      fallback, so missing tzdata is visible instead of shifting every band four
      hours. Corrected, continuation-only reads 09:00 +$8/trade · **10:00 −$18
      (−$4,195 on 238 trades)** · 11:00 −$5 · 12:00 +$15 · **13:00 −$34** — the
      same shape `trade_report` gets with a proper conversion, so the
      session-phase finding cross-validates on continuation alone.
  (b) **`MONOTONE` FIRED ON TWO BANDS.** `derived.confluence_count` takes only
      the values 3 and 4, and v1.0 called that "MONOTONE RISING". Across two
      cells monotonicity is arithmetic, not evidence. Now floored at three
      bands; below it the verdict reads TOO FEW BANDS. **So the direct test of
      this project's central premise did not run and has not run — the variable
      barely varies. Absent measurement, neither support nor refutation.**
  (c) `--setup-type` for the handoff question: `trend_continuation_handoff` is
      386 trades / 62% of continuation volume at 52% never-favorable against
      standalone's 33%, and it is the path where `CONTINUATION_CONV_FLOOR`
      deliberately steps aside. Filtering the sweep asks whether that population
      differs in `reg.conviction` (the floor was skipped) or only in outcome
      (post-runaway tape is simply bad). **Those need opposite fixes**, and
      nothing has distinguished them yet.

- **v4.42 — 2026-08-13 — AFD.1: THE AFTERNOON DEBIT BLOCK. `main` v6.2 /
  `config` v4.6 / `tests/test_afternoon_debit_block.py` v1.0.**
  Operator, verbatim: *"The only other Long that can fire is either part of a
  butterfly or an iron condor vertical spread from 11 o'clock onwards."*
  ORB / Continuation / SweepReversal are refused past
  `DEBIT_DIRECTIONAL_CUTOFF_ET` (11:00 ET; `OT_DEBIT_CUTOFF_ET` and
  `OT_DEBIT_BLOCK_ACTIVE` move the hour or kill the rule without a deploy).
  ENTRIES ONLY — open positions manage normally.

  **PLACED AFTER THE SIGNAL IS CHOSEN, not at dispatch**, for three reasons that
  are all about future-proofing rather than today: one gate instead of three, so
  a strategy added later cannot silently bypass it; the refused signal is fully
  formed, so the journal records WHAT WAS REFUSED (a gate that vetoes invisibly
  can never be calibrated from its own rejections — the same reasoning that put
  gates E and F *after* the score in `setup_scorer`); and **condor legs never
  reach it**, having routed through `_execute_condor_leg` earlier, so the credit
  path is exempt BY CONSTRUCTION rather than by a list entry that could rot.

  **⚠️ IN A TRENDING AFTERNOON THIS LEAVES NOTHING FIRING.** The condor
  self-gates to RANGING (main.py:1607) and cancels Leg 1 on a directional flip —
  23 of 23 plan deaths on 2026-08-04 were exactly that — and the butterfly needs
  PINNING GEX. That window belongs to the trend credit spread (TC.6), which is
  **NOT BUILT**. Dark on purpose until it is: the measured cost of that window
  is negative (10:00 −$8,715 · 11:00-14:00 −$1,539.50 on a whole book of +$463).

  **THREE THINGS THIS DELIVERY CAUGHT IN ITSELF, recorded because the catching
  is the point.**
  1. **A DUPLICATE RULE, NEARLY SHIPPED.** A parallel `AFTERNOON_NO_DEBIT_*`
     block was drafted on top of the existing `DEBIT_DIRECTIONAL_*` one — two
     names for one rule with the later assignment silently winning. Collapsed to
     a single definition and **pinned by a test** asserting each constant is
     defined exactly once.
  2. **THE CANARY-PROSE TRAP, HIT AGAIN AND CAUGHT BY THE TEST ON ITS FIRST
     RUN.** The absence check for the removed block tripped on the changelog
     entry *describing* the removal. Now scoped to `^NAME\s*=` — an absence
     canary must test for a DEFINITION, never for the name appearing anywhere.
     Third occurrence in this repo (`_orb_quality`, main v5.6, this).
     **PROMOTED TO WORKING_AGREEMENT §20 (v4.43, operator's instruction)** —
     three occurrences is a standing rule, not a war story. The section states
     the mechanism (rule 5 REQUIRES the changelog to name what it removed, so a
     substring canary is guaranteed to trip on good hygiene — the two rules
     collide by construction), the scoping patterns per artefact type, and the
     corollary that matters most: **if you find yourself avoiding a name in a
     changelog so a grep stays green, the canary is wrong, not the prose.**
  3. **THE CONDOR EXEMPTION IS POSITIONAL, SO A SOURCE-ORDER TEST GUARDS IT.**
     Nothing in the predicate would notice if the gate moved above
     `_execute_condor_leg`; legs would simply start being blocked, and the only
     symptom would be a credit strategy quietly not trading in the afternoon —
     the exact behaviour this change exists to protect.

  The predicate was extracted from an inline condition to
  `main._afternoon_debit_blocked()` so it has ONE definition and can be tested
  without standing up the whole entry path. **10/10 pass**, including three
  deliberate-failure checks that prove the suite can go red: empty the strategy
  set, move the cutoff past the sample time, and a reversed-source fixture for
  the ordering assertion.

- **⚠️ TC.4b's REFUTATION IS DOWNGRADED TO CONFOUNDED.** `--control matched`
  draws its pseudo-impulse at a RANDOM earlier minute across the whole session
  (`elig = [i for i in range(len(bars)) if len(bars) - i - 1 >= 5]`), so in a
  trending tape the control floor sits systematically FURTHER FROM SPOT than a
  recent impulse origin. The strike curve then measures offsets as a percentage
  *of each floor*, so at the same nominal offset the control's strike is further
  from price — and safer for a trivial distance reason. **The test conflates "is
  this level special?" with "is this level far?"** The −3.6% ±1.7% therefore does
  NOT establish that the impulse origin is anti-selecting. The fix is a
  DISTANCE-MATCHED control: draw the control floor at the same %-from-spot as
  the real one. Until that runs, TC.4's premise is UNTESTED, not refuted — and
  the operator's "vertical spread at the floor of the move" is unharmed by it.

- **v4.41 — 2026-08-13 — TC.5's POPULATION WAS WRONG. `credit_edge` v1.2.**
  Operator: *"The vertical is sold when the price is sitting in close proximity
  to the short strike level so that it's rich in premium & can withstand a
  little pressure... essentially a 'touch' of the channel outer tines should
  trigger a short strike selection just out of reach and with good liquidity."*
  **v1.1 priced a spread at EVERY snapshot regardless of where price sat**, which
  pools price MID-CHANNEL (strike far, credit thin, safety high) with price AT
  THE TINE (strike near, credit rich, risk real) and reports the blend. That is
  why credit averaged only 14-19% of width. **The touch IS the trade.** Fixture
  proof of exactly that: unconditioned credit 0.39, touch-conditioned **0.55** on
  the same tape.
  (1) `--approach` — call side fires only at high `pos_pct`, put side only at
      low. **Not a new emission**: `pitchfork_observer` already journals
      `pos_pct` (0% lower tine, 100% upper), and this is the same shape as the
      condor's existing `CONDOR_TRIGGER_APPROACH`.
  (2) **OTM GUARD, PER SIDE.** v1.1 never checked the PROJECTED tine was
      out-of-the-money against spot, so a stale or near-flat fork projected a
      tine at or inside spot and the tool priced short calls BELOW THE MONEY —
      that is the `flat/call` cell in the 08-12 run (n=184, 22% safe, E[loss]
      3.89, EV −3.04) dragging the whole pitchfork arm negative. Per SIDE, not
      per snapshot: a steeply rising channel legitimately projects its LOWER
      tine above spot by the bell, which kills the put side and leaves the call
      side perfectly sellable. A per-snapshot guard would throw away the good
      side with the bad.
  (3) LIQUIDITY on **bid/ask width**, not volume/OI — factor_sweep found
      `contract.volume` and `contract.oi` CONSTANT on the joined sample (zeros).
      A filter on a constant is a filter that does nothing.
  (4) **EFFECTIVE n IS SYMBOL-DAYS.** v1.1 printed n=139,600 spreads; every
      spread from one symbol-day shares ONE terminal close and snapshots repeat
      every 5 min on the same underlying, so the real count was **~336
      independent outcomes**. Reporting spreads as n overstated power by two
      orders of magnitude, and the header now says so before any table.

- **⚠️ TWO CAVEATS ON THE v1.1 SPOT RESULTS, both mine, before anyone cites them.**
  The 12-session window since 07-28 shows put `E[loss]` running ~2× call
  `E[loss]` at every offset — **that is almost certainly tape direction, not an
  edge**, since the window contains the 08-05 contraction. A call-biased rule
  fitted here inverts in a bull stretch. **Do not build side asymmetry off
  twelve sessions.** What DOES survive: EV/spread rising 09:00 **+0.24** →
  12:00 **+0.52**, monotone through midday, because that is a within-run
  comparison on the identical ladder and the conditioning problem hits both ends
  equally. **The operator's theta argument is measured.**

- **v4.40 — 2026-08-13 — TC.6: THE AFTERNOON TREND-CREDIT ENGINE IS STILL
  UNBUILT, AND IT NOW HAS A DIFFERENT SHORT-STRIKE RULE.** `[DESK→DEPLOY]`
  Operator: *"don't forget to come back to the credit spread on trend
  participation in the afternoons because that's when we don't wanna be long
  premium. The engine for that trade's construction has not been built yet."*
  **Standing item — do not let it fall off.** There is still no
  `strategy/vertical_spread_strategy.py`; what exists is
  `trade_readiness._trend_credit_spread()`, live and log-only since 2026-07-28.

  **WHAT CHANGED TODAY: the anchor, not the trade.** TC.4b's matched control
  refuted the impulse origin as a selector (−3.6% ±1.7% terminal, WORSE than an
  arbitrary recent extreme, at every offset). So the engine must not be built
  around `floor_px`. The trade — sell defined risk beyond a level, in the
  afternoon, held to the bell — is unaffected and the absolute curve supports
  it (terminal failure 8.8-12.9% at 1.00% out). **What it needs is a short-strike
  rule from a level that IS selecting.** Three candidates, all measurable on the
  same ladder by `credit_edge`: distance beyond SPOT (baseline, 3 weeks of
  chains, runnable now), the PROJECTED PITCHFORK TINE (PF.4, coverage from
  08-12), and VWAP (item AI, banked since the v1.5 bake, unavailable on SPX).
  **Sequencing: the spot arm produces the baseline EV, and no engine gets built
  until an anchor beats it.** Build belongs in the Aug 24 paper deploy per TC.4's
  own note — post-freeze, four weeks before full size.

- **`tests/credit_edge.py` v1.1 — `--anchor pitchfork`, and why the operator's
  leg-ordering rule does not have to be encoded.** His point: a fork has slope
  and therefore TIME. The short strike is FIXED once sold; the tine keeps
  moving. On an UP-sloping fork a PUT sold at today's lower tine gets SAFER
  every bar (the channel rises away from it) while a CALL sold at today's upper
  tine gets more DANGEROUS (the channel rises INTO it). So the honest call
  strike is the tine **projected to the bell**, and the buffer it needs is
  `slope × bars_remaining` — which SHRINKS as the session runs.
  **⇒ ONE RULE REPRODUCES HIS ORDERING:** sell each side when its strike clears
  the tine projected to the close. Up-slope → the put clears immediately and the
  call only clears late; down-slope → mirrored. No slope-sign branch, and it
  handles what a branch gets wrong: a near-flat fork (both sides sellable early)
  and a steep one late in the day (neither is).
  `rails_at(idx)` already extrapolates — `rail_at_time()` says so outright
  (*"Bars beyond the frame extrapolate at one index per bar"*) — so nothing new
  is needed geometrically. SLOPE IS DERIVED, NOT ASSUMED: fitted from two
  observations of the SAME fork, keyed on `(tf, born_idx)`, because a
  re-anchored fork is a different object and pooling them fits a slope across a
  discontinuity. A fork seen ONCE is SKIPPED, never projected flat, and the
  skipped count is printed — unmeasured coverage, not an absent fork.
  Adds a **SLOPE × SIDE** table stating the prediction before the data arrives:
  up-slope should price the PUT side better and the CALL side worse. If that
  asymmetry is absent, the slope is not doing the work the ordering rule assumes.
  ⚠️ **COVERAGE IS THE BINDING CONSTRAINT, NOT THE MATHS** — PF.2's observer
  began at the 08-12 wake, so expect this arm to REFUSE for a while. Also worth
  holding: the time element is an HOURLY-fork phenomenon (a daily fork barely
  moves across one session), and the hourly fork is ~3h late by §4.4 with a
  measured p50 lifetime of 5 bars.

- **v4.39 — 2026-08-13 — TC.4's PREMISE IS REFUTED; THE AFTERNOON-CREDIT DESIGN
  SURVIVES IT; TC.5 PRICES THE OTHER HALF.**

  **TC.4b CLOSED, NEGATIVE.** `tcs_floor_durability` v1.3, `--since 2026-07-28
  --control matched`, ARMED: 6,445 distinct impulses (deduped from 41,216 scored
  rows). Intraday floor held 14.7%, terminal OK 56.1%. **THE MATCHED CONTROL IS
  THE VERDICT: impulse minus control, TERMINAL −3.6% ±1.7%.** An ARBITRARY recent
  extreme on the same symbol-day survived BETTER (59.7%), and beat the impulse at
  EVERY offset on the strike curve with the relative gap widening outward (3× at
  3.00%). The tool pre-registered exactly this reading. **The impulse origin is
  not selecting anything — it is mildly anti-selecting.**
  **`TR_TCS_IMPULSE_SD_LO/HI` → DEAD.** establish 2.0-2.5 n=2186 intraday 14% /
  terminal 57%; screaming ≥2.5 n=4248 intraday 15% / terminal 56%. Flat, against
  an MDE of 2%. Arming already requires magnitude so there is no low-SD variance
  to fit a ramp against. Time-to-failure p50 **6 min** — a wrong thesis, not a
  0DTE out of clock.

  **BUT THE ABSOLUTE CURVE SAYS THE OPERATOR IS RIGHT ABOUT AFTERNOON CREDIT.**
  Terminal failure at 1.00% beyond the floor is 8.8-12.9%; at 1.50%, 4.2-7.4%. A
  defined-risk short ~1% beyond ANY recent extreme survives to the bell ~9 times
  in 10. **The design is supported; needing the IMPULSE STATE is not.** TC.4 was
  built around the one input measured to carry nothing.

- **TC.5 — `tests/credit_edge.py` v1.0: what does the short vertical actually
  PAY?** `[DESK]` The durability tool said it itself — *"further OTM collects
  less credit, and this table prices no credit at all. It bounds RISK."* Survival
  alone decides nothing: 98.5% survival at 3% out may collect three cents.
  Prices REAL ARCHIVED QUOTES from `chain_snapshots` — **credit = short BID −
  long ASK** (cross both) — against the session's last OHLC close, on the SAME
  offset ladder the durability curve prints so the two read side by side.
  **The load-bearing detail: E[loss] is the EXACT expiry payoff, capped at
  width, not a full-width loss on every breach.** A vertical held to expiry loses
  only the distance price finished BEYOND the short strike; treating every breach
  as max loss is the easiest way to make a viable credit trade look unviable.
  Reports EV/spread and EV/width per offset AND **by hour**, so the operator's
  theta argument — less clock left, less chance to reach the strike — is
  measured rather than assumed. Anchors on SPOT deliberately: the impulse anchor
  was just measured selecting nothing.
  Verified on fixtures; **partial-loss check passed exactly** (0.75% → 4.20,
  1.00% → 3.00, 1.50% → 0.50, capped at width beyond that, puts all safe).
  ⚠️ Assumes HELD TO EXPIRY — no management, stop, roll, early assignment or
  commission. It prices the trade as proposed, and cannot be compared to a
  managed book.

- **VWAP — THE STATUS THE OPERATOR ASKED FOR, and the two uses have OPPOSITE
  verdicts.** As an ENTRY FILTER (item E) it is **dead on evidence**: the ledger
  over 08-05/06/07 found the hard gate would block 5 trades losing $858 while
  KEEPING 228 aligned trades losing $5,049.50 — *"an entry filter cannot repair a
  trigger with negative drift."* As the **condor's MIDPOINT ANCHOR (item AI) it
  is live and has never been revisited.** VW.2 CLOSED 2026-08-08 and my
  hypothesis was wrong: the payload was never empty — 08-06 shows BELOW 5,058 /
  ABOVE 3,912, 554 NONE — so *"VWAP data has been banking correctly since the
  v1.5 bake, and item AI's condor midpoint has its input after all."* ⚠️ THE
  BLOCKER THAT SENDS THIS TO THE PITCHFORK: SPX cash prints volume 0 on every
  DXFeed bar, so `vwap=0.0 / price_vs_vwap=NONE` — a VWAP anchor is silently
  unavailable on one of the two ALWAYS_ON boxes.

- **PF.4 — YES, THE PITCHFORK WORK SUPPORTS CONDOR SHORT-STRIKE PLACEMENT, and
  the data is already journaling.** `pitchfork_observer._state()` records
  **`upper` / `median` / `lower` — the TINE PRICES themselves** per timeframe,
  not merely `pos_pct`. That is exactly what strike placement needs:
  - `median` (the sloped midline) is a drop-in candidate for the condor TRIGGER
    anchor, currently `bb_middle` — and iron_condor's own header names the open
    question verbatim: *"Makes the anchor question (VWAP? pitchfork median?)
    answerable with a number instead of an argument."*
  - `upper` / `lower` are candidates for the STRIKE FLOOR, currently the
    `v-dualfloor` prior of `0.80 × EM` OR the BB band, whichever is farther —
    a prior nobody fitted.
  - A pitchfork needs only PRICE, so it works on SPX where VWAP cannot.
  **`credit_edge`'s `--anchor` is the test bench:** same tape, same ladder,
  terminal EV for tine-anchored vs BB vs spot. Whichever anchor prices better is
  the answer, and it replaces an argument with a number.
  ⚠️ **COVERAGE IS THE CONSTRAINT:** PF.2's observer began journaling at the
  2026-08-12 wake, so this is ~2 sessions (13 daily forks / 7 symbols, 41 hourly
  / 13 symbols). Underpowered today, accumulating daily. The spot-anchored run
  is available now and is the baseline the tine run must beat.

- **v4.38 — 2026-08-13 — ⚠️ ROLL.1: NOTHING IDENTIFIED THIS SESSION IS LIVE ON
  THE FLEET. Operator: *"at some point we're gonna have to start implementing
  the changes. Nothing that we've identified so far has been rolled out."*
  HE IS RIGHT, AND THE REASON IS THE BAKE, NOT THE WORK.** GRD.1 is at origin
  (`1db919f`), ENG.1 at `d395bba`, excursion v3.1 at dtp `ae367ca` — all
  PUSHED, none BAKED. The boxes traded 2026-08-13 on pre-GRD.1 code. Per §18,
  a PUSHED item is ◐ and never ✅, and only the third state changes any of the
  data being collected.

  **DEPLOYABLE TONIGHT — neither item is entry-affecting, so neither waits for
  Mon Aug 17:**
  1. **BAKE GRD.1** (`setup_scorer` v1.7, already at origin). The weighted
     total is arithmetically unchanged and `grade_b` is untouched, so the
     fire/no-fire population is provably identical — verified over 200,000
     random signals, zero divergence in total OR in the REJECT boundary. The
     only behavioural change is that continuation stops drawing the 1.5× size
     multiplier on an anti-predictive grade. **That is a SIZING change, and
     sizing is explicitly outside the Aug 17 entry gate.** Worth ~$2,748 on the
     18-session sample.
  2. **`OT_CONT_STOP_PCT` 0.25 -> 0.15.** Env knob (config.py:819), no code
     deploy. Floor sweep, `max_loss_floor / ContinuationStrategy`, n=66 across
     9 sessions, **0% win rate**: a 15% floor stops all 66 with **ZERO WINNERS
     CUT**, NET DELTA **+8.85** units of entry premium against +2.25 at the
     current 25%. Meets the pre-registered cheapest-threshold-catching-zero-
     winners rule rather than an in-sample argmax. This cohort is BY DEFINITION
     the trades where no structural stop fired — not regime_flip, not bos_exit,
     not insurance_stop — so tightening it does not pre-empt a thesis test the
     way an `orb_structure_stop` floor would. **That proposal was WITHDRAWN**
     on the operator's correction: the ORB structure stop IS the thesis
     invalidation, its 0% win rate is a definition rather than a defect, and
     exit_engine's own comment makes the argument — *a premium-percent stop on
     0DTE measures gamma, not thesis*.

  **CONTROL-SIDE, NOT DEADLINE-BOUND:** the fleet cut (14 symbols clear ratio
  ≥3 at 60 bars; GS/LLY/COST condemned at ANY intraday horizon by the sqrt-t
  arithmetic — they would need ~1,190 / ~1,970 / ~780 bars to reach ratio 3).

  **MON AUG 17, ENTRY-AFFECTING:** the SWP.3 approach-weighting correction
  (three independent lines, ready) and GRD.2 if the operator approves it.

- **ENG.2 — `tests/orb_conversion.py` v1.0: did ORB's setups stop, or did a
  gate start?** `[DESK]` ENG.1 found the largest number in the project — ORB
  earned **$5,966/session pre-excavation and $1,551 after**, while per-trade
  value ROSE ($111.9 → $172.4) and never-favorable IMPROVED (38% → 22%). The
  engine did not get worse at picking ORBs; it got better and nearly stopped.
  **~$4,400/session, larger than the entry punch list combined.**
  Counts `retest_check` events (a break registered and was being worked)
  **deduplicated to (symbol, direction, attempt)** — a break evaluated over 200
  ticks is one setup, not 200, which is the tick-inflation trap that made the
  sweep opportunity audit read 4,303 "opportunities" from a handful of events —
  against ORB entries in trades.db. Flat break supply with collapsed conversion
  = a recoverable GATE; breaks falling in step = July's tape and nothing to
  restore. ⚠️ ENG.1's flat available-move figure (0.322 vs 0.344) does NOT
  settle this: that statistic is DIRECTIONLESS, and a tape can offer identical
  movement with far fewer clean range breaks. A session with trades but no
  journal is reported UNCOVERED and excluded from the rate rather than counted
  as zero breaks — counting missing telemetry as absent setups would invent the
  "setups stopped" answer. Fixture-verified incl. the uncovered-session path.

- **`tests/engine_arms.py` v1.1 — two defects found on the first real run.**
  (a) `--split` was documented as the last session of ARM A but assigns
  `d < split` to A, so `--split 2026-07-27` put the **07-27 session in arm B**
  — and deploys land in the EVENING (07-23's was confirmed 21:22–21:51), so the
  boxes traded 07-27 on the PRIMITIVE engine. Now documented and defaulted as
  the FIRST session of ARM B, 2026-07-28. **ENG.1's published arm B is one
  session wrong and should be re-run before it is cited.**
  (b) The ruleset audit printed *"journal starts later than these sessions"*
  when it found no stamps — but the journal covers 07-20 onward and the real
  cause is that the `ruleset` field postdates those rows. It reported a WRONG
  REASON, which is the renders-cleanly-means-something-else failure class,
  committed inside the audit built to catch it. Now distinguishes no-directory
  / empty-directory / files-present-but-field-absent.

- **v4.37 — 2026-08-13 — ENG.1: DID THE 07-27 EXCAVATION TRADE WORSE THAN THE
  PRIMITIVE L1 IT REPLACED?** `[DESK]` Operator: *"the layer one engine was
  arguably trading better than the upgraded confluence engine"* and *"the
  earliest trading on the primitive engine was wildly successful, but I
  intentionally steered it away with the goal of developing the confluence
  tests that made prediction a priority."*

  **This is the largest open question in the project and it outranks the entry
  punch list.** Five independent lines now point the same way: ORB is the
  profitable strategy and is the one setup_scorer v1.4 deliberately STRIPPED of
  confluence inputs; the regime label carries no forward drift beyond ±0.03% at
  any horizon; `SETUP.nf ≈ SETUP.ok`; `RGCV.nf ≈ RGCV.ok`; and sweep dried up
  at the excavation. If the primitive arm wins in a vol-matched window, GRD.1/2/3
  are rearranging furniture.

  **THE DATES MAKE IT TESTABLE, WHICH WAS NOT EXPECTED.** `92c89d7` (2026-07-27,
  "excavate the confluence engine") lands **eight days before** the 08-05
  volatility contraction, so the engine change and the tape change SEPARATE.
  Arm A = everything on or before 07-24 (trade DBs reach 07-13 via
  `trades/_archive_pre_2026-07-23`, complete, no gaps). Arm B = 07-28 → **08-04,
  hard stop** — crossing 08-05 would let a 15-25%/hour movement collapse answer
  a question about the engine.

  **SCHEMA BOUNDARY FOUND (probe, 2026-08-13):** `max_premium_seen` appears
  between 07-14 (absent) and 07-21 (present); `max_premium_seen_at` only from
  08-03. So MFE / never-favorable / capture exist on 07-20→07-24 (5 sessions)
  vs 07-28→08-04 (6) — balanced — while 07-13→07-17 supports NET ONLY.
  ⚠️ `excursion_report.usable()` DROPS rows without `max_premium_seen`, so an
  option-40 run reaching into mid-July silently thins the primitive arm for a
  reason unrelated to the engine.

  **BUILT — `tests/engine_arms.py` v1.0.** Reads both the live and archived
  trade folders. Reports per arm: n, sessions, symbols, net, $/trade, win%,
  never-favorable, and **`$/move` — net per trade divided by that arm's median
  available movement**, computed from the OHLC CSVs alone (deliberately NOT via
  `regime_replay_<date>.jsonl`, which does not exist for mid-July and would have
  made the primitive arm look empty for a non-engine reason). `$/move` is the
  column to read: raw dollars let the TAPE answer a question about the ENGINE.
  Rows lacking `max_premium_seen` are counted and shown as `n(mfe)`, never
  silently dropped. Adds a RULESET AUDIT reading the journal's per-row commit
  stamp, because BUILT ≠ PUSHED ≠ BAKED and the 07-27 split date is an
  assumption until the stamps confirm the boxes actually ran it.
  Verified on fixtures with a planted edge difference; **deliberate-failure
  check passed** — with identical engines and a 2× tape difference, `$/move`
  does not manufacture a win for the primitive arm.
  ⚠️ NATURAL EXPERIMENT, NOT A CONTROLLED ONE. The 07-24 runaway reroute sits
  INSIDE arm A, and CNT/SWP/LIQ landed after arm B — a difference is
  attributable to the system as it stood, not to `regime_confluence` v1.3
  alone. ⚠️ AND IT MAY COME BACK UNDERPOWERED: mid-July per-symbol DBs hold
  single-digit-to-25 rows, so arm A may not clear the n=40 / 3-session floor.
  That is a legitimate outcome — absent measurement, not a null.

- **`day_trader_pro/excursion_report.py` v3.1 — `insurance_stop` was reported
  NOWHERE.** It is the MIDDLE tier of continuation's three-stop precedence (BOS
  protected_level → structural `insurance_stop` → 25% premium floor). Tier 1
  reached the LEASH VERDICT via `bos_exit`, tier 3 reached the FLOOR VERDICT via
  `FLOOR_REASON_PREFIXES`, and tier 2 fell through both plus the `unlisted`
  fallback, which matches on the substring `"trail"`. Added to `TRAIL_FLAVORS`,
  and a new **UNREPORTED-REASONS audit** now names any exit family that reaches
  neither verdict block — the same failure class as v3.0's substring guard:
  output that renders cleanly while omitting the thing you would have looked for.

- **v4.36 — 2026-08-13 — WORKING_AGREEMENT §19: COMMANDS GO IN A CODE BOX, ONE
  LINE, SEMICOLON-SEPARATED.** Operator's instruction, shipped into the repo so
  it survives this thread. Covers presentation (a fenced code box, because a
  prose-wrapped command picks up soft wraps and smart quotes on mobile and has
  to be reconstructed by eye), form (`;` not `&&`, extending §1's single-line
  rule to the separator), and the one thing `;` costs: it does not
  short-circuit, so §15's fail-loudly-stage-nothing gate has to live inside a
  single-line `if ...; then ...; else echo "GATE FAILED"; fi` rather than
  relying on `&&`. Related trap recorded in the same section — a tool exiting
  non-zero on an empty-but-valid result cancels a trailing `&& rm -f`, which is
  how the r88 archive survived three deploys that all looked successful.
  **Delivery r89 was superseded by r90 without landing; this entry and v4.35
  ship together.**

- **v4.35 — 2026-08-13 — GRD.1: THE CONTINUATION GRADE IS ONE NUMBER COUNTED
  TWICE PLUS TWO CONSTANTS — AND IT BUYS 1.5x SIZE ON LATENESS.** Found by
  reading HEAD, not by a study. `ContinuationStrategy` has no entry in
  `STRATEGY_PROFILES`, so it fell through to `"default"`, where
  `regime_conviction` weighs 0.30 and `signal_quality` 0.25 — and
  `continuation_strategy.py:614` sets `signal.conviction = regime.conviction`.
  **55% of the grade is one column weighted twice.** `scorer_backtest` printed
  the fingerprint and nobody read it as one: both dimensions show identical
  medians AND identical spreads (0.913 / 0.636) over 619 trades, which is what a
  duplicated column looks like. `vwap_alignment` and `liquidity_clear` measured
  CONSTANT at 1.000 across all 619 — another 35%. **~90% duplicate or constant;
  only `macro_context` (0.10, flat) varies independently.**

  The grade INVERTS because of it: **A 399 trades -$8,244 (-$21/trade at 1.5x)
  vs B 220 trades +$1,893 (+$9)**. High regime conviction means the trend is
  already obvious, which means LATE — the confluence failure restated per trade.
  `setup_scorer` **v1.4 stripped exactly this from the ORB** ("regime conviction
  in costume") and left it on the strategy carrying **77% of fleet volume**.

  **SHIPPED — setup_scorer v1.7, explicit continuation profile.** The weighted
  total is **arithmetically unchanged** (0.55*conv is what 0.30+0.25 on one
  number already computed) and `grade_b` stays 0.55, so **the fire/no-fire
  population is provably identical — proven over 200,000 random signals, zero
  divergence in total OR in the REJECT boundary.** The only behavioural change:
  `grade_a` sits at 1.01, above the maximum achievable total of 1.00, so **no
  continuation setup earns the 1.5x upgrade** until an input is proven to
  separate. Not a permanent verdict — a refusal to pay 1.5x for a coin flip. On
  the measured sample that is worth **~$2,748**. A GLOBAL flatten was rejected:
  ORB's grade sorts CORRECTLY (+$56 vs -$25/trade) and earns its multiplier, so
  the same change fleet-wide would have cost ORB $2,203 to save continuation
  $2,748 — net +$545, not worth it. **Per-strategy or not at all.**

- **⚠️ GRD.2 — CONTINUATION NEVER SETS `underlying_target`. NOT FIXED — NEEDS A
  DECISION.** `[DESK→DEPLOY]` ORB sets entry/stop/target; continuation sets
  entry and stop and **never assigns a target**, though `trend_strike_plan`
  computes one (`_plan["target_price"]`, an expected-move fraction scaled by
  ADX+conviction) and uses it to pick the strike. Consequences, all silent:
  - `_rrr()` returns **None on every continuation signal** — which is why `rrr`
    appears in the ORB scorer table and nowhere else. **The MIN_RRR floor (item
    F) is structurally INERT on 77% of volume** and always has been; `None` is
    treated as absence-of-evidence by design, so the gate cannot fire.
  - `rrr` is the **one dimension measured to separate anywhere** (ORB: win p50
    4.164 vs lose p50 4.851, sep -0.687 — *negatively*; high advertised R:R
    loses). It is unmeasurable on continuation because a field is never filled.
  - **Populating it is NOT inert** and that is why it did not ship with GRD.1.
    Two dormant paths wake up: (a) `_pools_in_path` — with target 0.0 a LONG's
    window `entry < p < 0.0` is empty by construction, so `liquidity_clear` has
    been structurally dead on continuation longs, and filling the target makes
    it live, **which moves the score and therefore the fire boundary**;
    (b) `exit_engine._update_post_target_trail` — guarded on
    `underlying_target > 0`, so continuation has always fallen back to the 85%
    tightened trail instead of the FVG floor. **This changes exits.**
  - N.2's own note applies: a factor column cannot be backfilled, so every
    session it is missing is conditional data that never exists.

- **GRD.3 — `tests/factor_sweep.py` v1.0: sweep what we RECORD but never
  SCORE.** `[DESK]` The journal carries ~30 numbers per signal; the scorer reads
  five. This bands the other twenty-five against realised P&L — `rrr`,
  `contract.spread_pct_of_mid` (the per-trade version of SEL.1's 42x symbol
  lever, on the contract actually bought), delta/iv/theta/volume/oi,
  `entry_premium`, `vol.atr` and `bb_width` (the per-signal proxy for "is a
  worthwhile move available today"), `macro.vix`, hour, and
  **`confluence_count` — the direct test of the project's central premise**, on
  805 trades instead of by argument.

  Method is deliberately NOT scorer_backtest's: **a winner-median vs
  loser-median test is blind to a sparse or binary column.** ORB's
  `pools_in_path` reads "flat" (both medians 0.000, 78% of the population is
  zero) while the grade built from it separates +$56 vs -$25. So: quintile
  BANDS, **monotonicity as the verdict rather than spread**, a WINNERS-CAUGHT
  column on every cut, and a refusal to grade any band under the sample floor.
  Verified against a fixture with a planted truth, a planted null and a planted
  constant — and the **deliberate-failure check passed**: on a pure-noise
  rebuild the same factor that read MONOTONE FALLING reads NON-MONOTONE.
  ⚠️ In-sample over ~25 factors: about one will look monotone by chance.
  Output is a CANDIDATE for held-out re-derivation (ANT.2 pattern), not a weight.

- **`tests/scorer_backtest.py` v1.1** — each scored record now carries `raw`,
  the whole journal line, so factor_sweep imports the join instead of rewriting
  it. **Two tools have independently re-implemented this join and both got it
  wrong** (ANT.1 v1.0 grouped 128,503 rows as `None`; `grade_inversion_check`
  v1.0 joined zero of 805 and is still an uncommitted loose file on control).
  ONE JOIN, ONE OWNER.

- **v4.34 — 2026-08-12 EOD — ANT.1: THE PREMISE, TESTED AT LAST — AND `r` DOES
  NOT PREDICT. But individual FACTORS do, and the aggregation destroys them.**
  128,503 labelled readiness rows across 18 sessions, joined to forward tape
  movement (directionless, the WEAK test on purpose). No new collection.

  **⚠️ FIRST, MY OWN VERDICT LOGIC WAS WRONG AND FLATTERED THE RESULT.** The tool
  flagged continuation "80% SEPARATES" and sweep "162% SEPARATES" — but it
  measured SPREAD across r bands, not MONOTONICITY. **The tables are U-SHAPED and
  the LOWEST band wins:**
      continuation  r 0.0-0.2 -> **0.340** · 0.2-0.4 0.189 · 0.4-0.6 0.231 ·
                    0.6-0.8 0.220 · 0.8-1.0 0.238   (p50 @10 bars)
      sweep         r 0.0-0.2 -> **0.468** · 0.2-0.4 0.207 · 0.4-0.6 0.182 ·
                    0.6-0.8 0.179 · 0.8-1.0 0.216
  The warning text I wrote says "a MONOTONE rise is the claim, not merely a
  spread" — and the code did not check it. **Fix the verdict to require
  monotonicity before this tool is used again.**

  **⇒ `r` DOES NOT PREDICT. LOW readiness precedes MORE movement than high.**
  That is the CONFLUENCE FAILURE AGAIN, inside the layer built to avoid it:
  readiness rises as evidence accumulates, and evidence accumulates AFTER the
  move begins. Same mechanism that made the setup scorer's A grade an
  anti-signal (A −$8,244 / B +$1,893).
  - **SLOPE IS FLAT** — the premise's sharpest form ("a picture ASSEMBLING should
    beat one merely HIGH"): continuation Q1 0.218 → Q4 0.243; sweep 0.186 →
    0.205; butterfly and TCS show nothing. **The distinctive claim does not
    survive its own test.**
  - **MACHINE STATE IS FLAT** — ARMED barely differs from DORMANT on any track.

  **⇒ BUT THE FACTOR TABLE IS THE REAL FINDING, AND IT IS ACTIONABLE.** Single
  factors separate strongly where their COMBINATION `r` does not:
  - **SWEEP'S FACTORS SEPARATE HARD AND ALL NEGATIVELY: `appr_touches` −45% ·
    `appr_val` −41% · `age_bars` −31%.** FEWER touches, WEAKER approach and a
    YOUNGER sweep precede MORE movement. **SWP.3's approach factor is scoring
    BACKWARDS** — the same factor fitted to the shadow observer's 61.3% London
    share that LIQ.1 then showed was an artefact (London tracked price because
    its window overlaps RTH by 2.5h). **Two independent lines now say SWP.3's
    weighting is wrong.**
  - **CONDOR `room_val` +77% (put) and +45% (call)** — the strongest HONEST
    signal in the run, on the strategy that never fires. condor_call `conv` +39%.
  - **BUTTERFLY `conv` +60%**, its only non-constant factor besides `narrow_val`.
  - **`conv` INVERTS BY STRATEGY:** continuation −6% · sweep +25% · butterfly
    +60% · condor_call +39%. One input, four different relationships — so a
    single global weighting for it cannot be right.
  - **TCS `floor_px` −40%**, and its `mom_val`/`ext_damp`/`armext_*` are all
    CONSTANTS.
  - ⚠️ CONSTANTS EVERYWHERE: continuation `mom_val`; butterfly `squeeze_val`;
    sweep `is_sweep`, `fresh_val`; condor `origin_px/origin_em/ext_val/ext_frac/
    ext_fires`. **A constant cannot be thresholded and cannot be re-weighted —
    fixing it means changing what it MEASURES.**

  **⇒ WHAT THIS CHANGES.** The roadmap's Phase-1 premise — "gate on the
  anticipation layer" — **does not survive as stated**: `r` is not a predictor.
  But the layer is not worthless. It carries factors with real signal that the
  aggregation cancels, several of them NEGATIVE where the design assumed
  positive. **The work is re-deriving the combination from measured signs and
  magnitudes, not gating on `r` as it stands.**
  ⚠️ SCOPE: this is the DIRECTIONLESS test — availability, not direction. A
  factor that cannot predict available movement cannot predict a directional
  outcome, so failures here are conclusive; successes are necessary and not
  sufficient. And readiness journals on state CHANGE and heartbeat, so this
  measures the moments readiness chose to record, a biased sample by
  construction.

  **TOOL:** `readiness_label_study` v1.1 (v1.0 read the emitter's inner dict and
  assumed top level; the payload nests under a `readiness` key, so all 128,503
  rows grouped as `None` and every table printed empty — the join was always
  correct, only the field path was wrong).
- **v4.33 — 2026-08-12 EOD — SELECTION AND SIZING: four shippable conclusions,
  and the volatility contraction confirmed a second way.**

  **SEL.1 SYMBOL EDGE (15 sessions, ~5,300 ticks/symbol).** ratio = median
  available move / breakeven, at the traded 0.15-0.25 delta bucket:
  **QQQ 24.8 · SPX 18.3 · NVDA 15.0 · TSLA 14.1 · IWM 8.8 · AMZN 6.9 · PLTR 6.7
  · AAPL 6.6 · MU 6.1 · GOOGL 5.0 · NFLX 3.7 · AMD 3.2 | AVGO 2.7 · ORCL 2.2 ·
  MSFT/UNH 1.7 · GLD 1.5 · DIA/CRM/META 1.3 | SMH 1.0 · XOM/JPM/CVX 0.9 ·
  COST 0.6 · GS 0.5 · LLY 0.4.**
  ⚠️ THE TAIL VIEW IS THE HONEST SELECTION STATISTIC, not the median ratio. COST
  is ratio 0.6 yet made **+$1,985** on two long-hold ORB trades. `payable%` (share
  of ticks offering >=3x breakeven): QQQ 100% · GOOGL 79% · AMD 54% · **AVGO 44%
  · ORCL 29% · MSFT 21% · UNH 14% · GLD 14% · DIA 11%** (TAIL ONLY — size down,
  do NOT ban) · CRM 9% · META 8.8% · SMH 4.9% (thin but real) · **COST 0.5% ·
  GS 0.3% · LLY 0.4% (NO PAYABLE TAIL).**
  ⚠️ **HORIZON DEPENDENCE, unresolved:** the ratio measures a 20-BAR window while
  COST's two winners held 102 and 24 minutes. A long-hold symbol is
  systematically understated. **Re-run with `--horizon 60` before condemning
  COST/CRM/META** — GS and LLY should stay condemned at any horizon (p99 ratios
  2.2 and 2.1 against breakevens near 0.8%), and that is the test of whether the
  horizon explanation holds or is a rationalisation.

  **SPD.1 — DELTA SELECTION IS OFF THE PUNCH LIST.** 710,897 contract rows.
  Breakeven by delta: 0.05-0.15 **0.186%** · fleet's 0.15-0.25 **0.136%** ·
  optimum 0.25-0.35 **0.127%** · 0.60-0.85 **0.230%**. **Moving to the optimum
  buys 7%** — spread and leverage nearly cancel across the chain. The SYMBOL axis
  spans **42x**. The lever is which boxes wake, not which strike they buy.

  **SEL.2 FLEET CORRELATION — 13 boxes are 2.8 EFFECTIVE BETS** (mean pairwise
  rho 0.300, 5-min signed returns, 15 sessions).
  - **QQQ/SPX 0.907** are one position. Semis complex: AVGO/QQQ 0.791, MU/QQQ
    0.770, AMD/QQQ 0.757, AMD/MU 0.753. **IWM/SPX 0.757** — IWM is NOT the
    small-cap diversifier it looks like.
  - **THE DIVERSIFIERS INVERT THE CULLING LOGIC: NFLX −0.042** (and NEGATIVE to
    the semis: MU −0.245, AMD −0.235, AVGO −0.154), AAPL 0.046, GOOGL 0.186,
    AMZN 0.222, PLTR 0.239. **NFLX has the WORST payability ratio on the "trade
    it" list (3.7) and is the most valuable symbol for portfolio structure.**
    Cutting to the highest-ratio names RAISES per-trade edge and LOWERS the
    number of bets — they pull opposite ways.
  - ⚠️ **DIVERSIFICATION ERODES WHEN IT MATTERS: quiet half rho 0.238 → 3.4
    effective; busy half rho 0.327 → 2.6.** Correlation is highest on the days
    with the MOST movement, i.e. concentration and opportunity arrive together.
    **Size against the BUSY figure.** Worst session: **2026-07-29, rho 0.545 at
    0.140% median move — 13 boxes behaving as 1.7 positions.**
  - PRACTICAL: ~$15K across 13 boxes is roughly **$5.8K of independent risk** on
    a typical day and less on a busy one.

  **⚠️ THE VOLATILITY CONTRACTION IS CONFIRMED BY A SECOND, INDEPENDENT PATH.**
  SEL.2's per-session median |return| (5-min bars, straight from OHLC): **0.099-
  0.140% before 08-05, 0.057-0.086% after — roughly halved.** The preclusion
  census reached the same conclusion from replay ticks + forward tape excursion.
  Different data path, same answer. **The 08-05 "regression" is the market.**

  **⇒ FOUR SHIPPABLE CONCLUSIONS, none requiring the research phase:**
  1. **Drop GS and LLY** — no payable tail at any hour including the open.
  2. **Time-box the tier-2 names** (AVGO, ORCL, MSFT, UNH, GLD, DIA, CRM, META)
     to roughly the first two hours; they cross below 1.0 between 11:00 and 13:00.
  3. **Size on ~2.6 effective bets, not 13.**
  4. **Delta selection is worthless — drop it from the punch list.**
  ⚠️ Cutting to 13 also drops the fleet under the DXFeed subscription cap that
  forced the 15-of-29 selection, so the morning report becomes INFORMATIONAL
  (context for sizing) rather than DISCERNING (a gate that can be wrong) —
  operator's framing, and it removes the failure mode where a real setup sat out
  because the box was never woken.

  **TOOLS:** `spread_by_delta` v1.0 · `symbol_edge` v1.1 (tail view) ·
  `fleet_correlation` v1.1 (stress split). All read-only, all on data already
  on disk.
- **v4.32 — 2026-08-12 EOD — THE ENTRY-SIDE SESSION. Six measurements, and the
  first one stopped a wrong revert.** Operator: *"After nearly 2 months at this,
  I'm struggling to understand why these bots suck so bad… I'm challenging you
  to salvage this project."* What follows is the answer as far as the data goes.

  **1. ⚠️⚠️ THE 08-05 "REGRESSION" IS A VOLATILITY CONTRACTION, NOT A CODE
  DEFECT — AND I WAS ONE STEP FROM REVERTING ORB.1 AND N.8 FOR IT.** ORB was
  **+$11,426 over 07-24..08-04** and **−$8,089 over 08-05..08-12** on identical
  code, with long-hold win rate collapsing 72% → 38% on an IDENTICAL count of 29
  trades. I hunted a regression through exit_engine (last behavioural change
  07-31), ORB.1, N.8 and the BF.1-4 feed changes. **The tape settled it: median
  available underlying movement fell 15-25% in EVERY HOUR after 08-05** (09:00
  0.67→0.57 · 10:00 0.44→0.35 · 11:00 0.32→0.24 · 13:00 0.22→0.18 · 15:00
  0.27→0.21). **Hours are a tape property; no engine change can touch them.**
  On 0DTE a 20% cut in available movement is far more than a 20% cut in P&L —
  theta is unchanged while the numerator shrinks.
  **⇒ STANDING RULE: any P&L comparison spanning 08-05 must be NORMALISED BY
  AVAILABLE MOVEMENT, or volatility gets attributed to code.**
  ⚠️ RANGING fell 0.33→0.19, roughly TWICE the tape's decline — so about half of
  that is dilution from RGM.4 + RGM.6 absorbing formerly-UNKNOWN quiet ticks
  into the labelled population, exactly as the operator suspected ("we smoothed
  out the labels to get rid of the unknown segments").

  **2. THE CONFLUENCE SCORER IS NON-PREDICTIVE ACROSS THE ARSENAL**
  (`scorer_backtest` v1.0 — 18 sessions, 805 joined trades, 38 unmatched; reads
  the `scored` events INCLUDING below-B REJECTS, a control arm never used
  before). Continuation: **every dimension sep = 0.000.** `vwap_alignment` and
  `liquidity_clear` are CONSTANTS; `signal_quality`, `regime_conviction`,
  `macro_context` vary and still have IDENTICAL winner/loser medians.
  **AND THE GRADE IS INVERTED WHERE IT MATTERS:** continuation A = 399 trades
  **−$8,244**, B = 220 trades **+$1,893**. Sweep A = 3 trades 67%, B = 28 trades
  **82%**. ORB's `rrr` separates BACKWARDS (sep −0.687).
  **THE CAUSE, one mechanism explaining all of it: every quality input is a
  CONFLUENCE COUNT, and things agree AFTER a move is underway.** On a decaying
  instrument a high score means you are LATE. ⚠️ **ORB IS THE CONTROL THAT
  PROVES IT** — setup_scorer v1.4 deliberately stripped those inputs from ORB
  ("regime conviction in costume") and ORB is the profitable strategy
  (**+$5,775**). The bar also refuses almost nothing: refused median total
  **0.456** against a taken median of **0.885**.

  **3. THE TRAIL HAS A DEAD ZONE FROM +20% TO +25%.** `_update_fvg_trail` seeds
  `current_trail` at ENTRY premium and only engages once
  `current_premium * FVG_TRAIL_LOCK_PCT (0.80)` BEATS it — i.e. peak ≥ **+25%**
  — while `FVG_TRAIL_ARM_PCT` arms at **+20%**. In between it runs every tick,
  computes a floor, and SILENTLY DISCARDS IT. QQQ 2026-08-12 peaked **+22.5%**,
  had no trail at any point, and closed **−42.2% after 70.5 min**.
  ⚠️ THE SEED IS NOT THE BUG — refusing to lock a loss is deliberate. The
  MISMATCH between arm and engage is.
  ⚠️ AND MY OWN COUNTERFACTUAL WAS BIASED: `trail_engage_sweep` computes the
  trail from `max_premium_seen`, which is the peak reached UNDER THE LOOSE
  TRAIL. A tighter trail would have fired earlier at a lower peak, so its
  "zero HURT at every lock" column gives the tight trail credit for a peak it
  would have prevented. **Do not size a lock change on those numbers.**

  **4. ORB SPLITS ON PEAK PREMIUM, and the split is total.** 15 sessions:
  never-green 28 trades **0% win**; 0-10% peak 45 trades **0%**; +10-20% peak 11
  trades **0%**. **84 trades peaked below +20% and NOT ONE WON.** Above: +20-25%
  13/85%, +25-50% 32/94%, **>+50% 28 trades / 100% / +$23,773.**
  ⇒ the book is fat-tailed and **WIN RATE IS THE WRONG TARGET** — ORB is
  +$5,775 at a 43% win rate. Optimising it cuts the tail that pays.

  **5. PRE.1 PRECLUSION CENSUS — 187,589 ticks, NO HARD PRECLUSION EXISTS.**
  Every condition has a counterexample; the lowest MAX is COMPRESSION at 2.35%.
  But the tendencies are monotone across all horizons: at 0.27% / 20 bars,
  **09:00 86.8% · SWEEP_REVERSAL 80.8% · STALE 81.9% · COMPRESSION 40.1% ·
  13:00 38.6% · 14:00 38.6%.**
  ⚠️ SWEEP_REVERSAL is the most movement-rich label by **19 points** — but it is
  **absent post-08-08** (RGM.3 removed it cleanly), so that figure describes the
  old engine. The STATE is worth exposing as a FLAG, not restored to the argmax:
  at **0.55% of ticks** it loses an argmax against five labels structurally,
  which is why RGM.3 removed it and SWP.1 rewired sweep onto the L1 score.
  ⚠️ L1 BREADTH IS FLAT — 0,1,2,3,4 regimes scoring >0 all ~33-37%. **More
  agreement predicts nothing**, which is finding #2 appearing in the tape itself.

  **6. SPD.1 + SEL.1 — DELTA BARELY MATTERS. SYMBOL IS A 42x LEVER.**
  710,897 contract rows from the chain archive. Breakeven (the underlying %%
  move that pays the round-trip spread) by delta: 0.05-0.15 **0.186%** · the
  fleet's 0.15-0.25 **0.136%** · optimum 0.25-0.35 **0.127%** · 0.60-0.85
  **0.230%**. **Moving to the optimal bucket buys 7%** — spread and leverage
  very nearly cancel across the chain, so "buy closer to the money" is worth
  almost nothing. **DELTA SELECTION IS OFF THE PUNCH LIST.**
  By SYMBOL at the traded bucket, ratio = median available move / breakeven:
  **SPX 18.0 · QQQ 16.1 · NVDA 13.9 · TSLA 11.6 · GOOGL 6.4 · AVGO 1.8 ·
  SMH 1.0 · JPM 0.9 · CVX 0.9 · LLY 0.4 · GS 0.4.**
  **LLY and GS cannot pay their own spread on a typical move in ANY hour** —
  breakeven 0.714%/0.704% against typical moves of 0.271%/0.261%. Corroborated:
  LLY −$18, GS −$303.
  **AND A THIRD OF THE FLEET DIES AFTER 11:00** — AVGO 4.1 at 09:00 → 1.1 at
  13:00; SMH/JPM/CVX/XOM all cross below 1.0 between 11:00 and 13:00. **That is
  a WAKE and ENTRY-WINDOW decision, not a setup-quality one.**
  ⚠️ CONSERVATIVE BY CONSTRUCTION: breakeven is the full round-trip cross while
  `limit_ladder` posts AT the mark, so the residual is NO-FILL RISK not price.
  Halve it and every ratio doubles — treat <1 as a flag to measure fill rate on.
  ⚠️ 3 sessions post-08-08 only. **Run `--since 2026-07-23` before condemning a
  symbol**, and confirm LLY/GS breakeven is the SYMBOL and not the delta bucket
  landing on unusually cheap contracts for those names.

  **TOOLS SHIPPED (all read-only, all reading data already on disk):**
  `orb_stall_study` v1.2 · `velocity_feasibility` v1.0 (**first ever read of the
  chain archive, 20 days after it started writing**) · `trail_engage_sweep` v1.0
  · `scorer_backtest` v1.0 · `preclusion_census` v1.0 · `spread_by_delta` v1.0 ·
  `symbol_edge` v1.0 · `pitchfork_digest` v1.0.
  **SHIPPED TO THE FLEET:** VEL.1 velocity stall (exit_engine v4.16, step 2c,
  **observe-only**, Fri 08-14 evaluation date + delete criterion).

  **⚠️ THE MISALLOCATION, recorded because it is the lesson:** five exits shipped
  in two days (CNT.5, SWP.4/5, LIQ.1/3, VEL.1) while every report said the
  problem is ENTRIES. The entry-side work above is what should have come first.
- **v4.31 — 2026-08-12 — OBSERVER DEBT: FIRM DATES AND DELETE CRITERIA.**
  Operator: *"no more observers unless we're actually going to use the data."*
  Three observe-only mechanisms had shipped in two days with no evaluation date
  — VEL.1, PF.2, BFLY.1. All three now carry a **Fri Aug 14 read, a named
  decision, and a DELETE CRITERION**. The cautionary case is on the record: the
  chain archive was written 2026-07-23 and first read 2026-08-12, twenty days
  later, only because a question happened to need it.
  **STANDING RULE FROM HERE: an observer ships with an evaluation date and a
  delete criterion, or it does not ship.**
  ⚠️ Recorded in fairness to the one that HAS paid: the shadow observer produced
  the London 61.3% share (→ LIQ.1), the 14.0%-within-0.5-ATR figure that
  justified keeping the permissive 0.05 sweep floor, and the 18.1%-vs-4% UNKNOWN
  divergence (→ RGM.6). It is the exception, not the pattern — and LIQ.1 then
  UNDERMINED the very London finding it produced.
- **v4.30 — 2026-08-12 — VEL.1: THE VELOCITY STALL — THE THIRD QUESTION, and
  the FIRST READ OF THE CHAIN ARCHIVE.** Operator: "theta is a real beast on
  every long contract near expiry."
  **THE GAP, found by reading the 1m tape on three hard-stop trades.** They did
  NOT fail the structure stop — **the structure stop never had cause to fire.**
  QQQ and AVGO both ended their holds with the underlying BELOW the short entry
  and never once closed through the structural level. QQQ: **0 closes above
  structure, 50 minutes, -42.2%.** The loss was pure premium decay while the
  thesis stayed technically valid.
  `_theta_bleed` could not help either, correctly: **its gate 1 is a GAIN
  FLOOR**, so a losing position is invisible to it. QQQ peaked +22.5% at 5.75
  min — inside the 20-min blackout AND already above the 20% trail ceiling, so
  theta was silent BY DESIGN; by the time the blackout lifted the gain was gone
  and the 10% floor locked it out permanently.
  **⇒ "the setup has not invalidated AND has not worked" had NO OWNER.**
  - **THE STATISTIC NEEDS NO TARGET**, which is why it generalises beyond ORB:
    `bev = |theta| / (|delta| * 1440)` = underlying pts/min at which delta gains
    exactly offset decay. `ratio = delivered / bev`, and **1.0 IS THE FLAT
    LINE** — below it the position bleeds even while the thesis is intact.
  - **MEASURED, 15 sessions / 145 ORB trades, against the chain archive that had
    been accumulating unread since 2026-07-23** (`tests/velocity_feasibility.py`
    — the first tool ever to read it; 0 strikes missing, staleness median 2.3
    min). Among trades STILL OPEN at each mark: winners p10 / losers p50 —
    **5m: -21.1 / -37.3 (no separation) · 10m: 3.9 / -6.7 · 15m: 18.0 / 0.3 ·
    20m: 29.8 / 0.9.** The median surviving LOSER treads water at ~1.0 while the
    bottom decile of WINNERS runs at 30x it. Different regimes, not a marginal
    difference.
  - **⚠️ THE ENTRY-FILTER FORM WAS MEASURED AND REJECTED — INVERTED, not merely
    weak.** Feasibility ratio at entry ran HIGHER for LOSERS at every percentile
    (losers p50 **5.05** vs winners **3.87**, n=145); a filter would have blocked
    8 winners against 2 losers at a 1.5 threshold. Cause: a wide range gives a
    distant target AND a big required move — **feasibility and difficulty are
    the same axis pointing opposite ways.** Recorded in the code so it is not
    rebuilt.
  - **⚠️ AND THE GREEKS DO NOT PREDICT:** winners vs losers at entry are
    near-identical — delta 0.295/0.297, theta 0.865/0.816, gamma 0.038/0.042,
    IV 49.8%/52.5%. Nothing about the CONTRACT chosen separates outcomes, which
    is consistent with everything else pointing at SELECTION.
  **SHIPPED (exit_engine v4.16 step 2c, position_manager v3.1):** four gates —
  GRACE 10 min (**forced by data**: winners p10 at 5 min is -21.1, so the bottom
  decile of eventual WINNERS was moving AWAY), MEASURED-strategy gate, a floor
  at winners p10 x STRICTNESS, and CONFIRM x3 (**QQQ crossed back ABOVE
  breakeven at minutes 41-61 before dying at 70** — a single-tick rule
  oscillates). **ORDER IS DELIBERATE: theta_bleed FIRST**, so a stalled winner
  exits GREEN. **INDEPENDENT gates, never a combined score** — the QQQ failure
  was two mechanisms each correctly saying "not my problem".
  **⚠️ SHIPS OBSERVE-ONLY** (`OT_VELOCITY_ENFORCE=0`): floors rest on n=22 at the
  20-min mark and are ORB-derived. Non-ORB strategies are logged, never cut.
  **⚠️ TWO ERRORS IN MY OWN TOOL, both of which INFLATED the case for a rule and
  both caught before anything shipped:** `orb_stall_study` v1.0 never checked
  whether a trade was still OPEN at the mark (median loser hold is 4.0 min, so
  most of a claimed $14,559 was unreachable by construction), and its `$saved`
  summed the FULL realized loss as if cutting mid-trade recovered everything.
  v1.1 gates on `hold >= mark` and labels the column an upper bound. **The
  progress-toward-target rule died on the corrected numbers** — losers p50 sits
  ABOVE winners p10 at three of four marks once survivorship is removed.
  **⚠️ AND THE UNDEFINED-NAME GATE EARNED ITS KEEP AGAIN** — caught `Dict` used
  without import in the new counter annotation. 8 tests, 5 canaries, suite 429.
- **v4.29 — 2026-08-11 EOD — PF.2: THE PITCHFORK OVERLAY SHIPS, WEIGHT 0.**
  Operator: "build it & send it. I'll deploy it now & we will see what happens
  tomorrow. It's observe only, so win-win." Gates nothing, is read by no
  strategy, never raises.
  **⚠️ IT CAN LEGITIMATELY COLLECT THROUGH THE FREEZE.** EPOCH 2 hands off
  L1/L2/entry logic Aug 17 → Aug 30 but "everything else this epoch is offline
  or log-only". A weight-0 overlay IS log-only, so unlike RGM.5 and the London
  bonus this does NOT face the Mon Aug 17 deadline — it gets two extra weeks of
  observation while everything else is frozen.
  - **THE PREREQUISITE WAS ONE NUMBER, AND THE DATA WAS ALREADY THERE.**
    Verified live on SPX and GLD: each box holds **84 daily bars (2026-06-11 →
    08-11)** in its own `feed_store.db`, while `TIMEFRAMES["1d"]["candles"] = 10`
    clipped the frame handed to the engines to ten. **The history was never
    missing — the frame was.** Raised to 60. No new fetch, no new timing, no
    batching, nothing for session_guard to collide with. Every collection scheme
    discussed tonight (batched wakes, harvest-time pulls, an RTH-open fetch,
    yfinance, the TastyTrade sandbox) was solving a problem that did not exist.
  - **§4.3.6 CONTAINMENT ANCHOR (pitchfork v1.3) — the operator's construction:**
    "start at the present date and go backwards, and anything that falls out of
    the channel is not included in this pitchfork." **It INVERTS §4.3** —
    containment defines the extent, anchors follow. **It REMOVES a parameter
    rather than adding one:** §4.3's RECENCY imposes one timescale on every
    symbol, and the objection was that "some forks are gonna be shorter than
    other ones — some will be a week old, some months." Under containment the
    span is an OUTPUT. Measured, identical parameters: **NVDA 1h 12 bars, SPX 1h
    32, SMCI 1h 139.** And it BUILDS where §4.3 refuses all six symbol-timeframes
    tested: SMCI 1d **100% of closes contained, price at 42% of channel**.
  - **AN OPEN QUESTION CLOSED:** §12 listed variant choice as "reasoned, not
    evidenced". On SMCI daily modified_schiff contains 100% while raw **Andrews
    produces no contained fork at all** — the steep-median pathology §3.2
    predicted, now measured.
  - **`analysis/pitchfork_observer.py` v1.0** — box-local, per the operator's
    architecture rule ("the bots were designed to function without a controller;
    the controller is only intended if you're running a fleet"). Builds daily +
    hourly on a 5-min cadence from the box's own frames, journals `pitchfork`
    with `pos_pct` — **0% = on the lower tine, 100% = the upper.** That is the
    join key for the first consumer.
  **⚠️ THE FIRST CONSUMER IS CONTINUATION'S PULLBACK RAIL, NOT THE CONDOR.** The
  measurement plan named condor strikes, but the selector wakes MOVERS by design
  so the condor is structurally starved (1 plan, 0 fills on 08-11) — and the
  pitchfork is a TREND object being validated on a RANGE trade. Continuation is
  now the best strategy in the book and fires 13-76 times a session. **The touch
  study needed n≈600 and was unreachable; "where was price relative to the rail
  when continuation fired" is ONE observation per trade.**
  **⚠️ WHAT THIS HAS NOT ESTABLISHED: that the fork PAYS.** Containment is easy
  on a wide channel. §11 still governs — **v4.0 tags when TWO consumers are
  independently proven**, not when the overlay exists.
  **⚠️ THIRD DELIBERATE-FAILURE CHECK TODAY THAT PASSED WHEN IT SHOULD HAVE GONE
  RED.** Deleting the §4.4 confirmation-lag guard broke nothing, because the
  fixture's P2 sat mid-frame where the guard never fires. Fixed with
  `_leg_p2_at_the_edge` — P2 within k of the end is the ONLY shape that
  exercises it. A fork born before its lag is served is anchored on information
  that did not exist, and every backtest result from it is fiction.
  11 tests, 5 canaries, suite 421.
- **v4.28 — 2026-08-11 EOD — THE DAY SCRUBBED: fixes registered, unresolved
  carried.** Operator: "scrub the backlog, add our fixes and our unresolved for
  the day."
  **⚠️ THE LEDGER LESSON RECURRED AND IS WORTH RE-STATING.** Writing today's
  shipped work as prose under the Tue Aug 11 header moved BAC and NOT EV —
  because `evm_status` earns value from **PART 3, the RESOLVED REGISTER**, not
  from ✅ markers in PART 1. Same shape as the 08-08 finding that items filed in
  PART 0 carry zero EV weight. **Work is not "recorded" until it is in the
  register.** Ten resolutions registered: CNT.7, BFLY.1, LIQ.1, LIQ.3, SWP.4,
  SWP.5, RGM.6, CV.1, VW.1f, MEM.2.
  **MEASURED: EV 41 → 51, BAC 172 → 182, PV 97 → 107, SPI 0.42 → 0.48.** SV
  stays −56 — registering completed work does not reduce the schedule variance,
  it corrects an understated EV. The remaining −56 is real.
  **ELEVEN UNRESOLVED ITEMS CARRIED OUT OF TODAY** under the Tue Aug 11 header,
  the sharpest being: the SPX t3.medium upgrade (still pending, has OOM'd
  twice); the 9 sweep refusal paths logging at DEBUG against a fleet on INFO;
  **SWP.3's London bonus, now fitted to an artefact and therefore a CORRECTION
  with a Mon Aug 17 deadline**; and two tools disagreeing on
  `scores.SWEEP_REVERSAL` — resolve that before anyone moves a sweep floor.
- **v4.27 — 2026-08-11 EOD — RGM.6 SHIPPED: THE FALLBACK RESOLVES TO A KNOWN
  LABEL.** Operator: "unknown should be virtually eliminated by the time we
  freeze layer 1… there should be ways to extrapolate and resolve to a KNOWN
  label" — and, on scheduling, "that one can ship right now, we already have
  enough on our plate Friday."
  **THE DIARY SIZES IT EXACTLY.** L1 is all-zero on **2.4-3.0% of ticks on every
  session since 07-15** (stale flat at 6.5-6.8%), while the v13 fallback emitted
  UNKNOWN on **~18-19%**. A known answer existed roughly SEVEN TIMES more often
  than the engine was genuinely blind, and it was discarded every time.
  **CAUSE:** v5.0's hold covered STALE ticks only. The other fall-through — the
  code's own "empty committed label on a WARM book" — went straight to the v13
  classifier, which re-derives from scratch with NO MEMORY.
  **FIX (main v6.1):** the ladder is now committed L2 → held incumbent → **L1
  ARGMAX** → v13, and UNKNOWN is reserved for the ~2.4% that are genuinely
  all-zero. ⚠️ Conviction is CARRIED, not invented: an L1-argmax label carries
  L1's raw score, below theta_commit by construction, so downstream gates see a
  weak label as weak. `OT_RGM6_L1_ARGMAX=0` restores the old ladder.
  **⚠️ THE ENGINE TAG IS NOW FOUR STATES — [L2 c=] / [L2-hold c=] / [L1 c=] /
  [v13].** `grep -c '[v13]'` has been the fallback-rate measure all week; a DROP
  in it after this deploy is a RELABELLING, not a fix. Count the four.
  **⚠️ EXPECT per-regime statistics to be NOT POOLABLE across this deploy** —
  the labelled population gains a low-conviction tail that did not exist before.
  6 tests, 4 canaries, suite 411.
  **AND A DATED FINDING WORTH CARRYING: F7 IS WHAT KILLED RANGING, not the ramp
  de-saturation.** The diary dates it precisely — 08-06 RANG **28%** at
  churn-cut 1.49x; 08-07 RANG **3%** at churn-cut **7.59x**. Protecting the
  incumbent stopped a regime that cannot clear theta_commit from ever taking the
  label. RGM.4's recovery to 4% on 08-11 is exactly the doubling it predicted,
  and confirms the diagnosis from the other side.
- **v4.26 — 2026-08-11 EOD — RGM.5 MEASURED AND DEFERRED TO FRI AUG 14; RGM.6
  FILED.** Operator: "we've made a lot of engine changes in the last two days,
  let's give it till close of business Friday." The measurement the 08-11 item
  required is DONE (`tests/rgm5_fallthrough.py` v1.0, read-only): SWEEP_REVERSAL
  is **0.7% of v13 classifier ticks**, and cutting the branch makes **14 of 22
  newly tradeable** — about **0.45% of all ticks**. Directionally right, small.
  **The backlog's own prediction is RETRACTED** — it expected the ticks to land
  on BREAKOUT_VOLATILE and MOVE the dead zone; only 0.1% of v13 ticks are
  BREAKOUT at all. **⚠️ MY FIRST VERDICT IN THAT TOOL WAS ALSO WRONG and is
  fixed in v1.0: it counted only BREAKOUT as "still dead" and therefore called a
  63.6% UNKNOWN fall-through a genuine improvement. UNKNOWN is the SAME dead
  zone wearing a different name** — it hard-gates everything but ORB.
  **THE BIGGER FINDING, filed as RGM.6: UNKNOWN is 19.0% of v13 labels — 27x the
  sweep dead zone**, and L1's A5 acceptance check reports UNKNOWN eliminated at
  2% on the same date. The two layers disagree about a fifth of the fallback
  tape, and the live fit report's 18.1% says it is not a tape artefact.
- **v4.25 — 2026-08-11 — LIQ.1 + SWP.4: THREE DEFECTS THAT ZEROED THE SWEEP
  SCORE ON TEXTBOOK RAIDS.** Operator: "we have to unshackle it." Found by
  running the REAL code over a FABRICATED tape carrying an engineered PDL sweep
  — none was visible in production, because every relevant refusal logs at
  DEBUG against a fleet on INFO.
  - **LONDON WAS A SELF-REFERENTIAL MOVING TARGET.** Operator diagnosed it:
    "the London session in particular was creating a moving target and that has
    to go." The window is 07:00-16:00 UTC against RTH 13:30-20:00 — **a 2.5
    HOUR OVERLAP** — so from 09:30 to 12:00 ET "London High" is set by the price
    being traded. Sweeping it sweeps a level RTH made seconds ago. **⚠️ THIS
    RETROACTIVELY UNDERMINES THE SHADOW OBSERVER'S 61.3% LONDON FIGURE** —
    London was nearest BECAUSE it tracked price, so SWP.3's London bonus was
    fitted to an artefact and should be revisited. Asia removed with it. The
    lmap FIELDS stay populated so shadow/primitives keeps its census; only the
    sweepable POOL goes. `OT_LIQ_SESSION_POOLS=1` restores.
  - **THE DEDUPE DELETED THE NAMED SWEEP.** A PDH/PDL almost always ALSO sits on
    an equal-high/low cluster — that coincidence is WHY it is liquidity — so one
    raid makes TWO sweeps with identical kind, pool_price and bars_ago. They
    collide on the dedupe key; the tiebreak `mins < cmins` is FALSE on equality,
    so the FIRST-inserted survived and unnamed pools are found first.
    `swept_named_level` came back EMPTY, `veto_loc` hard-vetoed, **and the SWEEP
    SCORE WAS EXACTLY 0.000 on a perfect raid.** Measured on the fabricated
    tape: **0.000 before the fix, 1.000 after.** It also made v3.1's "named
    takes precedence" filter DEAD CODE — that filter reads the ALREADY-DEDUPED
    list. **⚠️ LIVE INCIDENCE UNKNOWN: the 08-11 corpus shows veto_loc PASSING
    on 99.6% of ticks, so this is real but may be rare. Not the whole story.**
  - **THE RECOVERY WINDOW PENALISED GOOD REJECTIONS.** `recovery_pct` measured
    from the WICK EXTREME, so a DEEPER rejection made the entry look FARTHER
    away. On the fabricated raid a 2.36% rejection produced 2.4% against a 2.0%
    cap and was refused — on the best setup the scorer can produce. Anchored to
    the reclaimed LEVEL it reads **0.11%**. Wick depth is rejection QUALITY and
    `rejq_val` already scores it. Both sides changed.
  **VERIFIED END TO END on three fabricated scenarios:** excellent PDL raid now
  passes EVERY logic gate (L1 **1.000**); a weak one is still refused as too old
  (L1 **0.000**); the same excellent raid into an ACCELERATING opposing trend
  scores **0.150** — a tenth of A, still above the long floor. **The
  discrimination survives the unshackling.** 6 tests, 4 canaries, suite 403.
  **⚠️ STILL OPEN — THE AGE INTERACTION, and it is the volume driver.** A
  separate harness over 90 real symbol-days found **98.3% of setups reaching the
  strategy refused as "Sweep too old", median age 45 bars against a cutoff of
  8.** Cause: `recent_sweep` holds the NAMED sweep by precedence with no expiry,
  so one early raid occupies the slot all session and fresher sweeps never enter
  it. Removing London/Asia shrinks the named set and should reduce this, but the
  precedence-without-expiry shape is untouched and needs its own decision.
  **⚠️ AND THE DEBUG LOGGING: 9 of 11 refusal paths in the strategy are
  `logger.debug` against `LOG_LEVEL="INFO"`.** Every investigation this evening
  was elimination-by-reading because those lines do not exist. Promoting them is
  one file, log-only, and would make the next drought one grep.
- **v4.25b — 2026-08-11 — UNSHACKLING THE SWEEP: FOUR DEFECTS, ALL FOUND BY
  ⬜ RENUMBERED v4.25 -> v4.25b during the 2026-08-15 scrub: TWO UNRELATED
  ENTRIES SHARED v4.25, which breaks any lookup by version. Content untouched.
  RUNNING THE REAL CODE RATHER THAN READING IT.** Operator: "that trade has been
  good to us. We need to get it firing again." None of these was visible in
  production, because 9 of 11 refusal paths in the strategy log at DEBUG against
  a fleet on `LOG_LEVEL="INFO"`.
  - **LIQ.1(a) LONDON WAS A SELF-REFERENTIAL MOVING TARGET.** Operator
    diagnosed it. London runs 07:00-16:00 UTC against RTH 13:30-20:00 — **a 2.5
    HOUR OVERLAP** — so from 09:30 to 12:00 ET "London High" is set by the price
    being traded. **⚠️ THIS RETROACTIVELY UNDERMINES THE SHADOW OBSERVER'S 61.3%
    LONDON SHARE** — London was nearest BECAUSE it tracked price, so SWP.3's
    London bonus was fitted to an artefact and needs revisiting. Asia removed
    with it. Fields stay for telemetry; only the sweepable POOL goes.
  - **LIQ.1(b) THE DEDUPE DELETED THE NAMED SWEEP.** A PDH/PDL almost always
    also sits on an equal-high/low cluster, so one raid makes two sweeps with
    identical kind/price/age. The tiebreak `mins < cmins` is FALSE on equality,
    so the first-inserted won — and unnamed pools are found first.
    `swept_named_level` came back EMPTY, `veto_loc` hard-vetoed, **the SWEEP
    SCORE WAS EXACTLY 0.000 on a perfect raid.** Fabricated PDL raid: **0.000
    before, 1.000 after.** ⚠️ Live incidence unknown — the 08-11 corpus shows
    veto_loc passing 99.6%, so real but possibly rare.
  - **SWP.4 THE RECOVERY WINDOW PENALISED GOOD REJECTIONS.** Measured from the
    WICK EXTREME, so a deeper rejection made the entry look farther away. A
    2.36% rejection produced 2.4% against a 2.0% cap and was refused. Anchored
    to the reclaimed LEVEL it reads **0.11%**.
  - **SWP.5 + LIQ.3 LIVENESS REPLACES THE CLOCK — the operator's insight.**
    "If the market makers are driving the price to either extreme what
    difference does it make if it takes an hour or if it takes all day?" None.
    `SWEEP_MAX_AGE_BARS = 8` was standing in for an invalidation test the code
    did not have: `closes_beyond` asks exactly the right question but is a
    **BIRTH-TIME snapshot**, counted over the 2-3 bars after the raid and never
    updated. **MEASURED over 90 real symbol-days: of the stale sweeps the gate
    refused, 32.9% still had a LIVE thesis** (854 of 2,593) — ~9.5 valid setups
    discarded per symbol-day on a clock. LIQ.3 recomputes invalidation every
    tick; SWP.5 gates on it.
  **RESULT on the same 90 symbol-days: refusals went from 98.4% "too old" to
  77.2% INVALIDATED (the level actually failed) + 13.9% backstop, and setups
  reaching STRIKE SELECTION went 5 → 40.**
  **⚠️ THREE THINGS TO HOLD.** (1) `SWEEP_STALE_HARD_BARS = 48` (4h) is a
  PRIOR — nothing in the data picked it; 414 setups hit it. (2) Every count here
  is NVDA/SPX/SMCI with stubbed regime and vol state: the gate ORDERING is real,
  the absolute numbers are not the fleet. (3) **REJECTED AND RECORDED: LIQ.2**,
  scoping named-precedence to fresh sweeps — built and measured, moved refusals
  98.6% → 98.4%, and evicts exactly the stale-but-live setups SWP.5 exists to
  keep. Dropped. 8 tests, 7 canaries, suite 405.
- **v4.24 — 2026-08-11 — CNT.7: the confirmation gate was rejecting TIES.**
  Operator, on a strong downtrend day that went untraded: "that's about as
  strong a trend as we're gonna get… it's too literal right now." Correct.
  CNT.4 required the confirmation bar to close STRICTLY beyond the tagging
  bar's extreme, and the live log shows misses of **3-9 cents** — QQQ 720.34 vs
  720.26 (0.011%), PLTR 175.22 vs 175.18 (0.023%), CVX 3c, TSLA 4c, SPX 1.55 on
  7735 (0.02%). The bar closed AT the extreme and was rejected on a
  rounding-level margin. **The thesis was right; the comparison was not.**
  Fixed with an ATR-scaled tolerance (continuation_strategy v1.6), same
  principle as the BOS distance floor — a fixed cent value cannot serve both
  QQQ and GLD.
  **0.40 IS DERIVED, NOT PREFERRED.** Every logged miss in ATR units splits
  into two populations with NOTHING between them: **ties 0.073-0.360, genuine
  failures 1.133-3.355** — a 3x gap. Any value between separates them.
  **⚠️ MY FIRST DRAFT WAS 0.05 AND WOULD HAVE REJECTED EVERY ONE OF THEM** — a
  no-op wearing the name of a fix. Caught only by testing the constant against
  the actual logged misses instead of shipping it, and now pinned by a test so
  it cannot come back. One session of evidence; re-derive after a week.
  **ALSO FOUND IN THE SAME LOGS: the counts are inflated ~3-4x.** The
  confirmation re-evaluates every 15s against the same closed bar pair, so ONE
  setup logs up to four identical lines (QQQ 15:23:15/30/45, 15:24:00 all read
  `need 720.21 got 720.66`). Fleet-wide 165 NOTCONF is really ~50 distinct
  setups. Not fixed — the duplication is harmless and de-duplicating it is a
  separate change — but **do not read NOTCONF as a setup count.**
  **AND CNT.6 IS WORKING HARD:** GLD **273** blocks, LLY **419**, TSLA 80,
  META 62, NFLX 50, all with NOTCONF=0 — those boxes sat in premium regimes all
  day and continuation was correctly refused. That is the squeeze fix doing its
  job on its first session. 12 tests, 3 canaries, suite 397 passed.
- **v4.23 — 2026-08-11 — BFLY.1: the butterfly readiness track was scoring a
  DIFFERENT TRADE from the one the strategy fires.** Operator: "the intent of
  that trade was if GEX was pinning and we had reason to believe price would
  migrate to the pin, we'd put on a cheap debit butterfly AT THE PIN… if the
  trade isn't written that way currently, it needs to be."
  **THE STRATEGY IS WRITTEN CORRECTLY — I was wrong to imply otherwise.**
  `butterfly_strategy` Gate 5 hard-refuses unless `gex_environment ==
  "PINNING"`, the body is `gex.pin_strike` not ATM, and its own header states
  the thesis: "enter the pin-centered tent while price is still a walk away."
  My earlier claim that the gate had no GEX came from checking
  `macro.butterfly_allowed` — which is the **VIX** kill-switch — and reporting
  that as the whole gate. Both exist.
  **WHAT WAS DEFECTIVE IS THE READINESS TRACK.** `_butterfly` graded `coil` (the
  COMPRESSION label) as a HARD VETO plus a boolean squeeze and band width — a
  compression play. **Not one of the five gates that actually block the strategy
  was in it**: no pin, no pin distance, no GEX environment, no 12:00-14:00
  window, no one-per-session. Consequence measured 2026-08-10: **would_fire=2132
  against ONE trade**, R p50 0.995 / p90 1.000. The thing it measured was ready
  all day; the thing that has to be true almost never was.
  **trade_readiness v1.8** replaces it with terms that RISE as the thesis comes
  true: `pin_val` (distance to the pin in EXPECTED-MOVE units), `firm_val`
  (|net_gex| — the strategy's PINNING flag is binary and cannot rank a 2.3M pin
  above a 0.1M one), `win_val` (ramps UP toward noon, ZERO after 14:00), and
  `gex_val` as a soft-necessary (PINNING 1.0 / NEUTRAL 0.35 / TRENDING 0.10) so
  a non-pinning tape reads "not yet" rather than "never". Coil survives DEMOTED
  to a corroborator. Observed: **0.115 → 0.342 → 0.930** as the pin firms and
  price walks in; **0.093** on a trending tape with identical pin geometry;
  0.155 warming at 10:45; 0.000 once the window shuts.
  **⚠️ LOG-ONLY — this changes what the score SAYS, not what fires.** Promotion
  was already solved by CNT.6: butterfly sits at Priority 3 behind
  `if signal is None`, so the only thing that ever blocked it was continuation
  firing above it, and CNT.6 removed continuation from RANGING/COMPRESSION. The
  operator's two rules — no continuation in a range, no neutral play in a trend
  — are now both enforced without a dispatch change.
  **⚠️ THE LIKELY REMAINING BLOCKER IS 1 x 5, NOT THE REGIME.** SPX logged
  `env=PINNING` at **15:29 ET** — after the 14:00 window shut. GEX pinning is
  naturally a late-day phenomenon as gamma concentrates into expiry, so gates 1
  and 5 may be close to mutually exclusive BY CONSTRUCTION. **Measure before
  moving the window:** per session, the ET timestamps where `env=PINNING`
  appears, crossed against the committed label. If pinning clusters after 14:00
  the WINDOW is wrong; if it pins inside the window on a trending label, CNT.6
  and RGM.4 may have already fixed it. 8 tests, 3 canaries, suite 392 passed.
  **A NOTE ON THE TESTS, because it is the second time today:** the first
  deliberate-failure check PASSED with the veto restored, i.e. the test could
  not fail. `_combine` treats `hard_vetoes` as a ZERO TEST rather than a
  multiplier, so restoring `coil` changes nothing on a COMPRESSION (1.0) or
  RANGING (0.5) tick. Only a label with `coil_val == 0.0` discriminates. A test
  that cannot fail is worth nothing, and both instances today were caught only
  by actually running the negative case.
- **v4.22 — 2026-08-10 EOD — RGM.5 scheduled for Tue Aug 11, with the option
  comparison recorded.** Deferred one day by the operator so today's five
  behavioural changes can be read against a label set that did not also move —
  the right call: changing labels underneath the first session of CNT.4/5/6,
  SWP.3 and RGM.4 would confound all of them. Filed as a dated PART 1 item so
  `evm_status` counts it, with the rejected alternative (narrowing the v13
  fallback path) recorded alongside the reason: the fallback is load-bearing and
  narrowing it would silence three strategies across the cold-start window to
  fix 0.6% of ticks. Also records the measurement that must precede the cut —
  what those ticks classify as once the sweep branch is disabled.
- **v4.21 — 2026-08-10 EOD — CATCH-UP: three shipped changes had NO backlog
  entry, plus CV.1, VW.1f and a correction to RGM.3.**
  **⚠️ THE PROCESS FAILURE FIRST, because it is mine and it is the operator's
  own standing rule: CNT.4, CNT.5 and SWP.3 were built, pushed AND BAKED with
  no BACKLOG entry.** The rule is explicit — `docs/BACKLOG.md` ships in every
  archive, because EV only moves when the backlog records it and this thread is
  the sole place that record is produced. I complied on r41 and r50/r53 and
  dropped it on r44/r45/r46 as the deliveries got faster. Same shape as the
  `rm -f` lapse the same day: the last clause is the first thing lost when a
  command grows. Backfilled below.
  - **CNT.4 — 1-BAR CONFIRMATION ON CONTINUATION ENTRIES** (continuation_strategy
    v1.5, `OT_CONT_REQUIRE_CONFIRM`). The FVG tag alone commits while price is
    still moving AGAINST the trend — a bet on a resumption that has not
    happened. Now the bar AFTER the tag must CLOSE BEYOND that bar's extreme in
    the trend direction: a miniature break of structure, deliberately the
    weakest test that still requires price to have DONE something. Fewer trades
    by design; setups that never confirm are never taken. Expect a LOWER win
    rate with a BETTER loss profile — read them together. **Shipped without the
    offline counterfactual at the operator's direction; the first week of
    post-deploy data IS the evidence.**
  - **CNT.5 — BOS PROTECTED LEVEL FLOORED AT `BOS_MIN_DIST_ATR * ATR`**
    (exit_engine v4.15). The level was seeded from the LOW of the first bar
    closing above entry, which on a pullback entry sits a hair under entry — so
    it landed INSIDE the symbol's noise band and any wiggle fired it. Observed
    live: **JPM in $1.26 12:49 → out $0.00 12:50 → back in $1.26 the same
    minute**, and QQQ fragmenting ONE move into four scratches
    (+$30/+$45.50/+$35/+$7). The re-entry loop is a SYMPTOM — it cannot happen
    unless the position closes. Corroborated the same session by `bos_exit`
    changing character: MFE +9% / giveback 8% against its historic +2%, i.e.
    cutting LIVE moves rather than stopping dead ones. `min_dist=0` is
    byte-identical to the old behaviour, ratchet included, and a test pins that.
  - **SWP.3 — SWEEP READINESS APPROACH FACTOR** (trade_readiness v1.7).
    Conviction now rises as price nears a named pool, scaled by how well that
    level has HELD; distance is price delta normalised by ATR (operator's spec).
    Bounds FITTED from the shadow observer — 14.0% of observations within 0.5
    ATR, median 2.32 — after my first draft of 0.15/1.20 would have scored the
    MEDIAN TICK AT ZERO and left the factor dead across ~3/4 of the session.
    London gets a modest 1.15 bonus (61.3% of nearest-level observations) and
    deliberately NOT a multiplier: that is a frequency of PROXIMITY, not of
    profitability. `appr_name` now lands on every readiness record so "which
    levels get swept" becomes a data question.
  - **⚠️ RGM.3 IS INCOMPLETE — CORRECTION TO SWP.3's STATED PREMISE.** I said the
    `is_sweep` label hard-veto had made the readiness track a PERMANENT ZERO
    after RGM.3, and used that to justify removing it. **Not true as stated.**
    `regime_classifier.py:171` still assigns `SWEEP_REVERSAL` at HIGHEST
    priority — RGM.3 removed it from the **L2 integrator only** — and `main`
    falls back to the v13 classifier whenever L2 is not committing. So both
    readings were right: `COMMITTED_SWEEP=0` fleet-wide AND readiness scored
    R p50 0.525 on 65 of 11,136 ticks via the fallback path. The veto removal
    still stands (0.6% of ticks is not a functioning arming track) but **the
    category error RGM.3 was meant to end survives in a second place, and that
    is now an open item.**
  - **CV.1 CLOSED — check_versions is ALL GREEN for the first time in weeks.**
    The canary pinned `tests/condor_plan_lifetime.py`, which exists at no HEAD
    in this repo, so a PERFECTLY CLEAN checkout ended `DONE — CANARY
    FAILURE(S)`. A permanently-red gate trains the reader to skip its own DONE
    banner (WORKING_AGREEMENT §17). Removed with the reasoning inline, NOT
    silently: `condor_approach.py` covers adjacent ground but carries no "WOULD
    A PAUSE HAVE HELPED" marker, so it is not a rename and the canary was not
    re-pointed on a guess. **If the file exists off-repo, restore the FILE and
    the line rather than leaving the check deleted.**
  - **VW.1f CLOSED — the three defects the ledger's own first output exposed**
    (v1.6). (a) ~29 trades that MAPPED but never MATCHED were dropped with no
    line anywhere; now counted and listed. (b) The mixed-eras warning fired on
    three ALL-PRE-BAKE dates because the split was BY TRACK not by date — the
    9,596 "emitted" was exactly TCS's own total; now warns only when a SINGLE
    TRACK holds both. (c) The verdict floor tested TOTAL trades, so CONTINUATION
    printed "orientation looks right" off a MISALIGNED arm of FIVE against 228
    aligned; now MIN_ARM_TRADES=8 on EACH arm, with the majority-alignment
    collapse's shrinking of the minority arm stated in the output.
- **v4.20 — 2026-08-10 — RGM.4: the bot recognised range all along; it could
  not COMMIT it.** Operator: "if my bot doesn't recognize ranging when it's
  clearly ranging, then it's broken." The classifier was not the broken part.
  **L1 wins the argmax for RANGING on 24.2% of ticks — essentially TRENDING
  BULL's 23.5% — while L2 emits RANGING on 2%** (209,061 ticks, 21 replay
  files). `ranging_commit_probe` split the two candidate causes: **83.2% of
  failed runs were CEILING** — peak EVIDENCE never reached the 0.65 bar either,
  and conviction asymptotes to its evidence, so no `tau_up` change could reach
  it. RANGING evidence p50 0.322 / p90 0.779 / **max 0.982 — it never pegs**;
  TRENDING p90 **1.000**. One global `theta_commit` was being applied to scores
  living on different scales.
  **THE CAUSE IS AN INTERACTION OF TWO CORRECT DECISIONS.** `room_s =
  ramp(bb_width_pct, 0.17, 1.00)` is a SOFT-NECESSARY, so it multiplies the
  whole score; bb_width_pct p50 0.44 puts it at ~0.33 — **which is exactly the
  observed peak evidence 0.322**. Those bounds were widened 0.20 → 1.00 to stop
  RANGING over-firing and it worked (dominance 44% → 27%). F7 then made
  `theta_commit` mandatory for every challenger. Neither change was wrong;
  nobody re-derived one against the other. Category-3 at the INTERACTION level
  rather than in a single constant — one for SPEC.1.
  **A REJECTED ALTERNATIVE, recorded so it is not re-proposed.** The operator
  proposed replacing the width proxy with directionless travel ("amount of
  up/down movement over a period"), with COMPRESSION as the narrowing end of
  the same axis. Measured: **travel overlaps RANGING/COMPRESSION at 0.766 and
  cannot even separate a range from a TREND** (p50 1.24 vs 1.19), while
  `bb_width_pct` overlaps at **0.040** — near-perfect. The efficiency half of
  the model WAS confirmed (trends 0.20 vs range 0.139 / compression 0.127). The
  input is right; the BAR was wrong. `tests/travel_efficiency_probe.py` shipped
  read-only.
  **THE FIX (conviction_integrator v2.3): a per-regime commit bar, RANGING at
  0.60, DERIVED not preferred.** `tau_up` 780 was fitted so commits land at
  ~17-19 bars — past the 12-15 bar window where TRENDS hold a false flat,
  inside the 24-29 where true ranges do. At RANGING's p90 evidence: 0.65 → 23.4
  bars (LATE, outside the design), **0.60 → 19.1 (in it)**, 0.50 → 13.3 (inside
  the impostor window, rejected). So this RESTORES the timing `tau_up` was
  fitted to produce — it is not a loosening, and `tau_up` is untouched.
  **⚠️ EXPECT 2.1% → ~3.3% of RANGING runs committing. Modest, not a
  transformation** — evidence p50 0.322 means most ranging argmax ticks are
  genuinely weak and SHOULD not commit. 7 tests, 3 canaries, suite 384 passed.
  Kill switch `OT_L2_THETA_COMMIT_RANGING=0.65`.
- **v4.19 — 2026-08-10 — CNT.6: continuation was trading RANGING and
  COMPRESSION, and squeezing out the strategies those regimes exist for.**
  Operator: "trend continuation dominating the afternoons would suggest every
  single ticker is trending hard all afternoon — that's not even remotely
  likely… if they can't fire, then by definition they are broken & if trend
  continuation is blocking all other setups, it is broken." Both halves were
  right. **The mechanism is the `_is_runaway` bypass**: the dispatch gate read
  `_is_runaway OR regime in (TRENDING_BULL, TRENDING_BEAR, BREAKOUT_VOLATILE)`,
  so an ORB runaway flag skipped the label check entirely and continuation fired
  on ANY tape at Priority 2 — ahead of Butterfly (P3) and Condor (P4), both
  behind `if signal is None` and therefore never evaluated. **Measured over 13
  sessions: RANGING → Continuation 94 vs IronCondor 27; COMPRESSION →
  Continuation 39 vs Butterfly 6** — 3.5x and 6.5x the opportunities, inside the
  regimes those strategies are for. And a continuation in a range contradicts
  its own premise: RANGING asserts there is no trend to continue. **Fixed at
  DISPATCH, not in the strategy** — CNT.3 already blocked the COMPRESSION
  handoff inside `continuation_strategy` and the squeeze continued, because a
  strategy-level veto still consumes the slot on its way to returning None.
  main v6.0, `OT_CONT_BLOCK_PREMIUM=0` restores the old behaviour exactly.
  6 tests, 4 canaries, suite 377 passed. **Expect continuation volume to fall
  and butterfly/condor to reappear — that is the change working, not a
  regression.**
  **⚠️ NOT FIXED HERE, AND CONDOR NEEDS IT: RANGING is emitted on only ~2% of
  L2 ticks** (08-10 replay: BULL 44% BEAR 21% COMP 20% BREA 13% RANG 2%). Freeing
  the dispatch slot is necessary but NOT SUFFICIENT for condor volume — the
  condor is also starved by the label itself, which is an L1 question and its own
  investigation. Butterfly is better placed: COMPRESSION is 20% of ticks, so the
  slot was its binding constraint.
- **v4.18 — 2026-08-08 — NF.1 scheduled for Friday 2026-08-14 after the close.**
  Examine the trades data for trade-combination x market-condition pairs that
  were never favourable — no salvage, entry fundamentally flawed — and make
  adjustments. Distinct from trades a stop change could have saved, which are
  excluded. Filed under a new Fri Aug 14 PART 1 header so `evm_status` counts it.
- **v4.17 — 2026-08-08 EOD — THE BAKE MOVED TO SATURDAY, AND FOUR CORRECTIONS.**
  Written because the record had started to lie in three separate places at
  once. **(1) THE FLEET WAS BAKED AND RESTARTED SAT 08-08 ~16:30 ET**, not
  Monday — all 29 boxes on `43911e9a3d` == origin/main, verified twice
  (bake VERIFY + an independent option-14 fan-out whose startup timestamps prove
  the lines came from THIS restart). PART 0.9 records it; PART 0.8's "none
  BAKED" claim is struck rather than deleted, so the next reader sees the plan
  change instead of a clean sheet that hides it. **(2) THE COLUMNS WERE STALE
  IN BOTH DIRECTIONS** — sixteen rows read `⬜ needs a bake` / `next bake` /
  `tonight's reflash`, and their **pushed** column read `⬜` on work that had
  been on origin for days. Anything at HEAD is now physically on every box, so
  both flip. **AX.3 is the deliberate exception and stays ⬜:** its emission was
  never BUILT, and a bake cannot help a thing that does not exist — marking it
  baked would have been precisely the laundered green. **(3) THE LEDGER'S FIRST
  REAL VERDICT GETS A DISPOSITION, per the standing rule that a study without
  one is unfinished work: item E's hard gate DOES NOT SHIP.** It would block 5
  trades losing $858 while keeping 228 aligned trades losing $5,049.50 — VWAP
  alignment does not reach continuation's problem, which is the same answer
  `trigger_drift` gave from the other side. **(4) TWO NEW OPEN ITEMS FILED AS
  SCOPE, NOT HIDDEN AS PROSE** — VW.1f (three defects the ledger's own first
  output exposed, including a verdict printed off a 5-trade arm and a
  mixed-eras alarm that cried wolf) and CV.1 (two canary reds at clean HEAD that
  have made `check_versions.sh`'s DONE banner unusable as a gate). **MEASURED, not asserted:
  BAC 147 -> 149, PV 93 -> 95, SV -52 -> -54, SPI(all) 0.44 -> 0.43, DESK
  overdue 26 -> 28** (`--asof 2026-08-08`). That is scope discovery honestly
  recorded, not slippage — and the DESK-overdue count is the number that should
  sting.
  **⚠️ A LESSON WORTH MORE THAN THE ITEMS: the delivery table is a LEDGER, not
  the PLAN.** `evm_status.py` parses **PART 1 + PART 2 only**, matching
  `- \`[TAG]\` **NAME` under a dated `**⬜ Day**` header. VW.1f and CV.1 were
  first filed in the PART 0 delivery table and the EVM run came back
  BYTE-IDENTICAL to pristine HEAD — the items existed, were readable, looked
  filed, and carried **zero** earned-value weight. Caught only by diffing the
  run against a clean clone rather than trusting that writing it down was
  enough. **Anything meant to count must land in PART 1 with a tag and a
  date**; a row in the ledger is documentation, not plan. Also recorded: 29 boxes
  are up over the weekend by choice, which means **Monday trades all 29 rather
  than the usual ~15** (read from `orchestrator.run()` and the absence of any
  selection gate in `main.py`), stacking a cohort-composition change on top of
  the engine change — while the day-rollover path was CHECKED and is safe.
- **v4.16 — 2026-08-08 — VW.1e: `dir` on every track, fixed at the SOURCE.**
  VW.1d taught the ledger to derive direction; this fixes why it had to. Only
  `_trend_credit_spread` journaled `dir` — five tracks emitted nothing, and
  nothing caught it because a field with one writer looks optional until a
  reader needs it. trade_readiness **v1.6** stamps `dir` on every track from
  the source that knows: sweep's comes from the LIVE `liq_map`, which no
  offline tool could recover at all. Ledger **v1.5** prefers the emitted field
  and keeps the derivation for banked history, and now prints the
  emitted-vs-derived ERA SPLIT with a warning when a run spans both — pooling
  across Monday's bake is the standing hazard and a caveat nobody reads is not
  a control. Also BACKFILLED trade_readiness's missing **v1.5** changelog entry
  and put a version on its title line: it shipped with neither while
  `check_versions` already pinned "v1.5", which is precisely the drift
  WORKING_AGREEMENT rule 5 exists to stop. Recorded rather than quietly
  corrected. 7 tests, 4 canaries, deliberate-failure verified, suite 339/1.
  **⚠️ TWO PRE-EXISTING CANARY REDS confirmed at clean HEAD and NOT introduced
  here:** `main.py` pins a v5.4 header string while main is at v5.8, and a
  canary points at `tests/condor_plan_lifetime.py`, which does not exist. A
  sweep that is permanently red trains the reader to ignore its own DONE
  banner — the cried-wolf failure this repo has already paid for once. Left
  untouched pending the operator's call rather than folded into this delivery.
- **v4.15 — 2026-08-08 — VW.1d: the join layer, the fifth and final one.** The
  operator's v1.3 run showed the remaining problem: 30,565 "undecidable", only
  TREND_CREDIT_SPREAD in the table, and 304 trade rows joined to ZERO trades.
  This time the whole path was traced (emitter → event → section → field)
  before anything was patched, and three stacked defects fell out of one read:
  `factors.dir` exists on only the TCS track; the trade join compared track
  slugs to strategy class names; and TCS has no firing engine, so its 0-trade
  INSUFFICIENT verdict was forced. Ledger v1.4 resolves direction per strategy
  (the emitter's own rules), normalizes the trade join by family, attributes
  condor legs via setup_type, and reports every undecidable record and dropped
  trade BY CAUSE. Symptom reproduced on planted data first, fix proven on the
  same fixture. PART 0.8's mid-flight note closed.
- **v4.14 — 2026-08-08 — PART 0.8: thread handoff.** The working thread hit its
  attachment limit. Records the bake state (30 deliveries pushed, none baked —
  the fleet runs F7 only until Monday's restart), the one item still mid-flight
  (`vwap_orientation_ledger` v1.3, correct as far as it goes, with a further
  defect the operator observed but could not share before the limit), and the
  three findings that should govern next week. Written so the next thread starts
  from fact rather than a summary of a summary.
- **v4.13 — 2026-08-08 — VW.1c: the event filter, and the fourth wrong
  assumption about one tool.** v1.2 resolved all five fields correctly and the
  run STILL returned 419 undecidable, zero decidable. The event whitelist
  accepted only `("scored","fired","entry","entered")` — names predating
  `trade_readiness` v1.5 — while the records carrying `readiness.market` are
  `readiness`, `readiness_would_fire` and `readiness_staged_pick`. **11,584
  records skipped on 2026-08-06 alone**, and the 419 survivors were `scored`
  rows with no market section. Now PREFIX-matched on `readiness*`; an exact list
  is what kept this tool three versions behind its own emitter.
  **VW.2 IS CLOSED AND MY HYPOTHESIS WAS WRONG.** The payload was never empty:
  08-06 shows BELOW **5,058** / ABOVE **3,912**, 554 NONE. VWAP data has been
  banking correctly since the v1.5 bake, and item AI's condor midpoint has its
  input after all.
  **⚠️ THE LESSON, and it cost FOUR versions of one file:** I patched the layer
  that had just failed — field names, then depth, then paths, then the filter —
  instead of tracing the whole path once. Each fix was correct and each was one
  layer short. When a tool returns nothing twice, stop fixing and READ THE PATH
  END TO END: emitter → event name → section → field.
- **v4.12 — 2026-08-08 — three loose ends from Saturday, closed or dated.**
  **SHD.2a CLOSED — it was never a fault.** All 29 boxes read `enabled` +
  `active`; the thin ones have barely been SELECTED to trade, and the observer
  only runs on a woken box. The operator's explanation required no failures;
  mine required six identical ones. **SMCI's 11 records is the one genuine
  remnant** and is dated Monday.
  **VW.2 OPENED, and it is the important one.** VW.1b fixed the SCHEMA — all
  five fields now resolve — but the first real run over 39,344 records returned
  **419 undecidable and ZERO decidable**, every row "index/NONE side". A fixed
  schema over a null payload is not a fixed pipeline, and if
  `volatility_engine.vwap` is not reaching `_market_snapshot` then item AI's
  VWAP-anchored condor midpoint still has nothing accumulating — which was the
  entire reason this had a deadline.
  **THE PATTERN WORTH NAMING: today produced THREE tools that resolved their
  inputs and then found nothing** (rejection ledger's MISSED column with no
  null arm, the axis conjunction, this). Resolving an input is not the same as
  having data, and each was caught only because the tool announced what it could
  not find rather than printing an empty table.
- **v4.11 — 2026-08-08 — VW.1b: the paths, read off the emitter instead of
  guessed.** v1.1 made discovery path-aware — necessary, and it proved itself by
  resolving `readiness.strategy` — but I then INVENTED the remaining paths
  (`vwap.vwap`, `factors.dir`) and the tool found NONE of them across 39,344
  records over three sessions. `trade_readiness._journal()` settles it: it emits
  ONE section, `readiness=`, holding `market` and `factors`, so everything sits
  TWO levels deep — `readiness.market.vwap`, `readiness.market.price_vs_vwap`,
  `readiness.factors.dir`. **The field NAMES in the standing note were right the
  whole time; the DEPTH was wrong**, which is why two flat renames and one
  shallow path all missed. There is no price field at all: `_market_snapshot`
  emits `dist_pct`, which is better here because it is comparable across a $30
  symbol and a $900 one.
  **⚠️ THE TOOL EARNED ITS KEEP.** It printed `(NOT FOUND)` per field and
  REFUSED to run. A silent zero-row ledger would have read as "no
  misorientation" rather than "wrong key" — the laundered-green failure, avoided
  because v1.0 was built to name what it could not find.
  **THE LESSON, third time today:** path-awareness fixed the ACCESSOR; only
  reading the EMITTER fixed the PATHS. Making a lookup more capable does not tell
  you what to look up.
- **v4.10 — 2026-08-08 — SATURDAY IN THE BOOKS. PART 0.7 records the day's
  consequences, not its commits.** 26 deliveries: the engine changed five times
  (F7 emission, RGM.3, SWP.1/2, CNT.1/2/3), four measuring instruments were built
  and each was given a CONTROL before its output was trusted, the schedule
  slipped a week into the plan itself, and the working agreement gained the rule
  that every study owes a disposition — kill, keep or codify.
  Three findings carried forward: the edge is in the TRIGGER not the LABEL;
  `direction_conf` separates at +0.188 where setup_score and regime_conviction do
  not; and the fused label was burying BEAR/EXPANDING (+$5,059) inside the
  worst-reading regime in the book. One hypothesis killed on purpose
  (`pair_conf`, +0.001, stamped dead in its own payload). Four of my own wrong
  calls recorded, because the corrections are the transferable part.
  **⚠️ NOTHING IS BAKED UNTIL MONDAY. Every per-regime statistic is now on a
  different basis than the 12-session history — do not pool across the bake.**
- **v4.09 — 2026-08-07 — VW.1: the VWAP ledger can finally read the journal, and
  the diagnosis I had been carrying was wrong.** It exited rc=1 for two nights
  and the standing note said "three field renames". It was not: `_first_key`
  tested `n in rec` — TOP-LEVEL keys only — while the journal nests these under
  sections (`readiness.strategy`, `factors.dir`). **No flat rename could ever
  have reached them.** v1.1 makes CAND entries DOTTED PATHS and routes every
  accessor through `dig()`, so the next schema section costs one tuple entry
  rather than another dead tool. Added `pnl_usd`, which is what the trades table
  actually calls it. Proven on a realistic nested record: discovery resolved
  `readiness.strategy`, `factors.dir`, `vwap.price_vs_vwap` and `vwap.price`.
  **⚠️ IT CAN ONLY SEE SESSIONS FROM THE trade_readiness v1.5 BAKE FORWARD.**
  Before 2026-08-05, VWAP was computed every tick by volatility_engine and NEVER
  WRITTEN DOWN — so earlier journals have no VWAP at all and their emptiness is
  not a finding. Item AI's condor fix (a VWAP-anchored midpoint) cannot be
  evaluated on data that does not exist, which is why this had a deadline: every
  session from here is history you either have or you do not.
  **THE GENERAL LESSON, worth more than the fix:** a diagnosis that survives two
  nights unexamined becomes a fact. "Three renames" was written down once and
  repeated since; reading the accessor took one grep.
- **v4.08 — 2026-08-07 — AX.3: keep the part that separated, kill the part that
  did not, and mark the corpse.** `pair_conf` is dead (+0.001 vs
  `direction_conf`'s +0.188) and the failure is structural — a conjunction over a
  sparse axis collapses. It stays in the payload only so the cross-tab runs, now
  carrying `pair_conf_status: DEAD` so nobody builds on it by accident.
  `direction_conf` survives as the first score in this system to clearly separate
  outcomes, at roughly double anything measured before, and it is the RAW L1
  score rather than the L2 integrated one. Emission onto the journal is the next
  step and is deliberately not built tonight.
- **v4.07 — 2026-08-07 — AX.2: the test that can kill AX.1.** `axis_crosstab.py`
  scores every closed trade in the 3x3 of direction x volatility, then reports
  `pair_conf` split by outcome — nf (never favourable) vs ok — **the same
  comparison the excursion report already runs on setup_score and regime
  conviction, both of which come back nf ≈ ok.** The claim is that a conjunction
  separates where its components do not; the third line is read against the first
  two, and if it adds nothing the idea is recorded as DEAD rather than
  re-litigated.
  Never-favourable is a PRICE-PATH label from `max_premium_seen` vs
  `entry_premium`, independent of stops, sizing and fills — so it cannot be
  contaminated by exit logic, which is why realized P&L is the wrong target.
  Score vectors come from the REPLAY CORPUS at the entry tick, since the trade
  row stores only the fused label. UTC→ET via zoneinfo; unmatched rows dropped
  and counted.
  **⚠️ A DEFECT IN MY OWN TOOL, CAUGHT BY THE PLANTED RUN AND WORTH THE ENTRY:**
  the first version printed **"SEPARATES" with n_nf=0** — `_pct([], 50)` returns
  0.0, so the verdict logic read a +0.900 gap out of an EMPTY list. A tool that
  announces a finding from no data is the laundered-green failure this repo
  keeps catching. It now REFUSES below 15 per arm and says "absent measurement,
  not a null result".
- **v4.06 — 2026-08-07 — AX.1: the conjunction is codified, and gates nothing.**
  Operator: *"it's the conjunction that I would like to codify somehow."*
  The six regimes are TWO orthogonal oppositions the argmax fuses and half
  discards — direction (BULL/BEAR ←→ RANGING) and volatility (BREAKOUT ←→
  COMPRESSION). `analysis/regime_axes.py` splits any L1 score vector into both,
  reporting each axis's winner, LEVEL and MARGIN separately, plus
  **`pair_conf = min(direction_conf, volatility_conf)`**.
  **WHY `min` AND NOT A MEAN — it is the whole claim.** A mean lets a confident
  direction paper over an unknown volatility state; `min` is low whenever EITHER
  axis is unsure and is bounded above by both, so it cannot manufacture
  confidence its components lack. A deliberate-failure run swapping `min` for a
  mean turns two tests red.
  **THE FALSIFIABLE HOPE:** `SETUP.nf ≈ SETUP.ok` and `RGCV.nf ≈ RGCV.ok` say
  neither existing score separates good trades from bad, so no threshold on
  either can. **A conjunction can separate where its components do not.** If the
  3×3 cross-tab shows no separation either, the idea dies cheaply.
  **THE EVIDENCE THAT PROMPTED IT:** continuation makes money ONLY where it is
  not supposed to work — RANGING 82 trades **+$578.50** against TRENDING_BULL
  252 **−$3,221** and TRENDING_BEAR 85 **−$4,952**.
  **⚠️ MARGIN IS DELIBERATELY NOT FOLDED IN:** 0.90 against 0.89 is a high level
  and a terrible margin, and collapsing them would hide which is missing — the
  same error that made the census's p50 separation of 0.347 look healthy.
  **⚠️ AN EMPTY AXIS RETURNS NEUTRAL, NEVER A TIE-BREAK HEAD** — a tie-break
  head is how SWEEP_REVERSAL won the 4.2% of ticks where the engine knew
  nothing. And SWEEP is on NEITHER axis: it is an event overlay, and putting it
  on one repeats the exact category error RGM.3 just undid.
  **NEXT, both read-only:** score the 692 trades in the 3×3 (~77/cell), then
  condition `trigger_drift` on the PAIR instead of the label. Anything that
  GATES on it is RGM.2 Stage 3, post-go-live.
- **v4.05 — 2026-08-07 — SHD.2/SHD.3: the shadow data gets a calibration date
  and a pre-freeze confirmation date.** The first-ever read produced three
  numbers that should set dials rather than decorate a report — named levels are
  **61.3% London High/Low**, only **14.0%** of observations sit within 0.5 ATR of
  a named level (median **2.32 ATR**), and live `UNKNOWN` is **18.1%** against
  the offline harness's 4%. Re-pull **Fri Aug 14**, the last working day before
  the **Mon Aug 17** calibration deploy, so the numbers can actually move a knob.
  Re-pull again **Wed Aug 26**, two days before the **Fri Aug 28** freeze — not
  to calibrate but to confirm the distributions have not drifted out from under
  the calibration. **A freeze declares a baseline; declaring one on a
  distribution that moved after the dials were set is how a frozen baseline
  becomes a frozen mistake.**
  **⚠️ SHD.2a FIRST, ON MON AUG 10:** GS has zero sessions, SMCI eleven records,
  and DIA/GLD/IWM/TLT exactly one each — the 07-22 enable-at-boot signature. Every
  session missed between now and the 14th is unrecoverable, so reviving those six
  is worth more than anything done to the data afterwards.
  **⚠️ THE AUG 14 PULL SPANS TWO ENGINES** — RGM.3 bakes Monday, so `regime`
  values must be split at the bake date, never pooled. Same basis rule as the
  per-regime statistics.
- **v4.04 — 2026-08-07 — SHD.1: the shadow observer's data leaves the fleet for
  the first time, and gets a reader.** It has run fleet-wide since 07-22 and
  **nothing has ever consumed it** — no analyzer, no report, no devtools option —
  and `harvest.py` has no shadow class, so every file sat on its own box's EBS.
  **282,350 records, 188 files, 238 MB across 29 boxes.**
  `tests/shadow_summary.py` v1.0 leads with FILL RATE, not record count: a
  primitive null on most ticks is not evidence however many rows carry the key,
  and the first line of every session has `velocity`/`roc_*`/`intrabar_pos` null
  BY CONSTRUCTION, so a `head -1` reads as empty when the field may be fine.
  Streams one file at a time — three earlier tools in this repo died of
  load-everything-then-filter and 238 MB is exactly that trap.
  **WHY IT MATTERS NOW:** SWP.1's hard vetoes are "a NAMED level, swept and
  rejected", and the observer has recorded `nearest_named_above/below` with
  `dist_pct` and `dist_atr` every 15s for 13 sessions — the distribution
  underneath the gate that shipped today, collected by something that scores
  nothing and trades nothing.
  **⚠️ TWO CAVEATS THE TOOL REPEATS IN ITS OWN OUTPUT.** Coverage is wildly
  uneven — GS zero sessions, SMCI ELEVEN LINES, and DIA/GLD/IWM/TLT exactly one
  1,560-line session each, which is one clean RTH day then nothing: **the
  original 07-22 failure signature, so the enable-at-boot fix did not take on
  those boxes.** And every `regime` value here came from the PRE-RGM.3
  six-regime engine, so pooling with post-Monday data repeats the basis error.
  **PULL METHOD, worth keeping:** `ssh_util.scp_pull` builds `scp` with NO `-r`
  and is a single-FILE helper (its docstring says `trades.db`). Handed a
  directory it fails on every box, and its callers discard stderr — so the first
  attempt returned a bare list of 29 failures with no reason. Third discarded
  return value to cost a diagnosis this week. The working form tars on the box
  and streams it back.
- **v4.03 — 2026-08-07 — every one of tonight's nineteen deliveries now has a
  DATED check-in with a falsifiable question.** PART 0.6. Code that is pushed has
  changed nothing until its effect is read back, and today produced a lot of
  pushed code: the emission fix, sweep ungated then removed from the regime set,
  continuation opened to breakout tape, the insurance gate, two tuning priors,
  the drift instrument, the rejection ledger, the ruleset stamp, the memory
  tracer and the slip itself. Each row names what would FALSIFY the change, not
  just when to look — "review" is how a check-in becomes a formality.
  Carries the two caveats that outlive the table: 08-03/08-04 are permanently
  thin (session guard, 14 boxes, tape unrecoverable) and must be marked PARTIAL
  wherever pooled; and N.7's ruleset stamp applies only FORWARD, so the
  12-session history stays un-attributable.
- **v4.02 — 2026-08-07 — N.7: journal rows now say which engine made the
  decision.** Every cross-date analysis of these rows has been pooling decisions
  from different rulesets with no way to declare it — L3.2a could only emit
  `decision_hash: null`, and the same gap was named on 07-29 about engine
  identity, where this was the fix proposed and not built. 08-07 alone changed
  the emission law, the regime set, two dispatch gates, an exit gate and two
  floors. `signal_journal` v1.2 stamps `ruleset` on every row, resolved ONCE at
  import — a `git rev-parse` per line would put a subprocess in the trading
  loop, and a process runs one ruleset for its whole life anyway. Falls back to
  `"unknown"` rather than a partial hash: a wrong hash is worse than an absent
  one because it looks attributable. Log-only.
  **⚠️ IT ONLY APPLIES FORWARD.** Every row banked before this deploy has no
  ruleset, so the 12-session history stays un-attributable. L3.2a's cross-date
  totals keep their caveat until a week of stamped rows exists.
  **⚠️ AND L3.2a's FIRST RUN NEEDS A NULL ARM BEFORE IT IS QUOTED.** 2,451 rows:
  retest_near_miss 73% MISSED, invalid_signal 63%, scored:REJECT 78%,
  sizing_rejected 53% — all majority MISSED, which looks like every gate is too
  tight. But MFE >= 0.10% over 20 bars is a bar ordinary intraday range clears
  most of the time, and the ledger has NO NULL — the same omission that made
  `a2_cooccurrence` unreadable until ORB gave it a positive control. **Read the
  MFE/MAE RATIO instead:** retest_near_miss 1.04 and invalid_signal 0.91 are
  SYMMETRIC (noise, 2,271 of the rows); `sizing_rejected` is **0.15** — adverse
  excursion 6.5x favourable, genuinely dodging damage despite its 53% label; and
  `scored:REJECT` at **1.31** is the only real too-tight candidate (n=142).
  v1.1 owes a seeded random arm and the ratio as headline.
- **v4.01 — 2026-08-07 — L3.2a: the rejection ledger, the first look at what the
  system DECLINED.** Every measurement so far — never-favourable, the floor
  sweep, trigger drift, excursions — reads only trades that FIRED, so none can
  say what a gate COSTS. The ledger consolidates `scored` rejects, `disposition`
  rejects, N.2 `gate_block:*` and `retest_check` near-misses into one row and
  labels each **DODGED** (tape went against the intended direction) or **MISSED**
  (it went the intended way). A gate that is mostly MISSED is too tight and is
  costing money invisibly.
  **TWO HONEST FINDINGS FROM BUILDING IT, both worth more than the tool.**
  (1) **The item's own prescribed validation does not prove what it claims.** It
  says shift the decision timestamp +1 bar and confirm outcomes change. They do —
  but they change whether the window starts at `idx` or `idx+1`, because shifting
  the index moves the reference price either way. **It passed on a deliberately
  leaking build.** The property is structural and is now pinned structurally, by
  a hand-built series where including the decision bar gives a different known
  answer; `--verify` is kept only as a degenerate-join sanity check.
  (2) **The version-hash requirement CANNOT be met retrospectively.** The journal
  does not stamp the ruleset that made the decision — the same gap noted 07-29
  about engine identity. Rows carry `analysis_hash` and an explicit
  `decision_hash: null`, and the tool SAYS SO in its own output. 2026-08-07 alone
  changed the emission law, the regime set, two dispatch gates, an exit gate and
  two floors, so cross-date pooling spans engines. **The fix is upstream: stamp
  the ruleset onto the journal event.** Filed, not built.
- **v4.00 — 2026-08-07 — GATE.1: the acceptance gate stops asking the wrong
  question of three of its four tags.** v1.0 scored every tag against the
  SESSION-MODAL label, but only TREND is a whole-session characterisation. PIN
  is a LAST-HOUR property, so a day that trended from the open and coiled into
  the close was counted as a miss. BREAKOUT and SWEEP are SINGLE-EVENT tags and
  are now reported **NOT SCORED** — scoring them needs a breach timestamp that
  `session_labels.jsonl` does not carry, and a wrong number is worse than none.
  **v1.0's PIN 8.9% / BREAKOUT 2.8-6.4% / SWEEP 0.0% are RETRACTED** — they were
  the tool's error, not the engine's, and they were quoted once before that was
  caught. TREND's numbers (63.4% → 69.1% modal, 47.5% → 57.8% in-family) are
  UNAFFECTED, so the F7 verdict they carried still stands.
- **v3.99 — 2026-08-07 — MEM.2: the memory tracer moves INSIDE the bot.** The
  standalone probe failed four times in one afternoon and not once for a reason
  about memory — wrong box, un-pulled file, `tmux sh -c` inheriting neither
  .bashrc nor the systemd unit environment (no credentials, and OT_INSTRUMENT
  defaulting to QQQ on the SPX box), and an `xargs env` workaround that echoed
  every secret to the terminal. One root cause: a second process cannot easily
  inherit the trading environment, and **the bot already has it**.
  `utils/mem_trace.py` is env-gated by `OT_MEM_TRACE`, costs one bool test per
  tick when off, and takes a WARM reference before diffing so first-tick caches
  are not reported as growth. It also says so explicitly when RSS climbs while
  traced memory does not — that divergence means the leak is not in Python
  objects and tracemalloc cannot see it.
  ⚠️ tracemalloc adds ~10-30% memory overhead, which on a 951 MB box is itself a
  risk: **SPX only, which is why it was resized first.** Never fleet-wide.
  main v5.8. mem_tracer v1.1 finally gets the symbol banner and the empty-fetch
  abort that were flagged after the FIRST failed run and not shipped — that gap
  then cost two more runs.
- **v3.98 — 2026-08-07 — THE SLIP IS NOW IN THE SCHEDULE, not just in the
  changelog.** v3.95 recorded the DECISION; the dated plan still read the old
  one, so `evm_status.py` would have briefed the wrong PV and every overdue count
  would have been wrong — the number that is supposed to sting. 70 date tokens
  shifted seven days from Deploy Monday 2 onward. **Epoch 1's past dates were
  deliberately NOT moved**: already-overdue items stay overdue, because slipping
  them would erase the accountability signal rather than reschedule it.
  Labor Day is a fixed holiday and did not slip, which is why GO LIVE is
  **Tue Sep 8**. Freeze **Fri Aug 28**, Deploy Monday 3 **Mon Aug 31**, descent
  notch Tue Sep 15, FULL SIZE **Mon Sep 21**.
- **v3.97 — 2026-08-07 — SWP.2 + CNT.3: the first tuning changes carried by
  data, both filed as PRIORS rather than fits.** Sweep shorts get their own
  0.20 floor (longs stay 0.05) on three agreeing measures plus the PLTR
  mechanism — and it is stated plainly that against a ~0.265 score ceiling this
  near-disables shorts rather than trimming them. The runaway handoff stops
  firing under COMPRESSION, where it is 28% WR / −$454 and sits in the worst
  never-favourable cell at 80%, because a runaway asserts expansion while the
  label asserts coiling. Both env-reversible. config v4.5, strategy v3.4, 6
  tests, deliberate-failure verified.
  One canary of my own had to be loosened: CNT.1's test pinned the handoff
  branch's EXACT TEXT and fired on CNT.3's correct edit. Rewritten to assert the
  branch still EXISTS — a canary that fires on intended changes gets loosened
  under pressure, which is how it stops protecting anything.
  **SHIPPED, NOT BAKED.**
- **v3.96 — 2026-08-07 — DRF.1: the drift measurement gets a positive control.**
  Option 47 finds no forward drift in any label state, but it only ever had a
  null control — nothing in it is known to carry edge, so it has never been shown
  able to detect any. `tests/trigger_drift.py` v1.0 conditions drift on the ENTRY
  TRIGGER instead, signed by trade direction, with ORB (+$10,156 over 12
  sessions) as the positive control and a seeded random arm as the null. It
  ignores the exit on purpose, which is what separates a bad entry from a bad
  stop — something MFE/MAE cannot do. UTC→ET via zoneinfo with a refusal rather
  than a guessed offset. Planted proof separated a drift window from noise
  cleanly. **BUILT, NOT YET RUN.**
- **v3.95 — 2026-08-07 — RGM.3: sweep stops being a regime, and the schedule
  slips a week.** `docs/MECHANICS.md` already called SWEEP_REVERSAL an "event
  overlay"; it was in the `Regime` enum anyway, and being the only scorer with a
  3-bar age-decay half-life it could never win an argmax against states that peg
  at 1.0 — 22% non-zero on 08-07 yet max 0.265 and dominant on 1%.
  conviction_integrator v2.2 drops it from `INTEGRATED_REGIMES` and
  `_TIEBREAK_ORDER`; the scorer stays because SWP.1's gate reads it. Two side
  effects worth the change on their own: the tie-break head moves off the
  least-supported regime, and a None sweep score can no longer pin the book
  stale. Schedule slipped one week — freeze 08-28, go-live Tue 09-08 (09-07 is
  Labor Day), full size 09-21. **SHIPPED, NOT BAKED; per-regime history is now
  on a different basis.**
- **v3.94 — 2026-08-07 — CNT.2: the insurance gate, covering BOS's blind
  window.** BOS is already continuation's ungated thesis invalidator, but its
  tracker has no protected level until the trade first goes favourable — so it
  cannot reach a trade that fails from the first tick, which is the 45-trade
  population dying at −29% with MFE +1%. Gate 2c arms the already-stamped
  `underlying_stop` (dead code until now, read only by query.py) ONLY while
  `protected_level is None`, making the handoff exact without a time knob.
  Structural rather than premium-percent, because the floor sweep proved a
  tighter premium stop nets ~zero by cutting winners that merely dip. Tagged
  `insurance_stop`. config v4.4, exit_engine v4.14, 7 tests,
  deliberate-failure test passed. **SHIPPED, NOT BAKED — and the level has never
  been read by anything that trades, so it is an untested prior.**
- **v3.93 — 2026-08-07 — CNT.1: continuation ungated on BREAKOUT_VOLATILE, with
  direction supplied by the trend engine.** The bar was never a quality
  judgement — the label carries no direction, so no branch could assign one.
  `trend.overall_direction` supplies it; NEUTRAL self-vetoes; `primary_adx >= 25`
  is the quality bar, chosen because under a non-trending label continuation's
  conviction floor is skipped and BREAKOUT's conviction is not the trend's.
  Entries tagged `trend_continuation_breakout` so the rollup can score them apart
  from the 141-trade `_standalone` history — without that split the data this is
  being turned on to collect would be unreadable. config v4.3, main v5.7,
  strategy branch, 6 tests, deliberate-failure test passed.
  **SHIPPED, NOT BAKED.**
- **v3.92 — 2026-08-07 — SWP.1 BUILT: sweep no longer gates on the regime
  label.** Dispatch qualifies on the L1 `_sweep` setup score, whose three hard
  vetoes are the operator's spec verbatim — named level, rejected back through,
  not accepted beyond — so every non-zero tick already qualifies and the floor
  is a noise guard rather than a quality bar. `SWEEP_SETUP_FLOOR = 0.05` set
  from the corpus (non-zero on 4.0% of ticks; p50 0.016, p90 0.154), deliberately
  max-permissive for collection and knob-tunable without a deploy. The PLTR
  trend-opposition guard survives because it lives as a soft-necessary INSIDE
  the score, and a test now asserts that. The operator's "conviction should rise
  as continuation falls" turned out to be already encoded in `opp_mom` and
  `exh_val` — it needed unblocking, not building. Filed against it: the empty-
  momentum case double-penalises sweep and is the next measurement. config v4.2,
  main v5.6, strategy v3.3, 6 new tests, deliberate-failure test passed.
  **BUILT AND PUSHED; NOT BAKED — the fleet still runs the old gate.**
- **v3.91 — 2026-08-07 — SWP.1 opened: sweep stops being a regime.** Operator
  ruling that sweep is an event, not a market state — confirmed by three
  independent lines already in the record. A fleet log grep proved ZERO sweep
  activity for the session; every `Sweep strike:` line came from CONTINUATION
  readiness through a shared selector whose log message names the function
  rather than the caller (`target=0.45` = `TR_CONT_TARGET_DELTA`). Design
  settled: gate on the L1 `_sweep` SCORE rather than the committed label, which
  keeps the PLTR trend-opposition protection inside the score where it already
  lives and gives the strategy its own setup conviction. Floor to be set from
  `tests/sweep_score_dist.py` v1.0 and shipped as a stated prior behind
  `OT_SWEEP_SETUP_FLOOR`. Two adjacent defects filed: an empty delta band
  landing picks from 0.19 to 0.55, and a log line that misattributes continuation
  work to sweep. **TOOL BUILT; the change is NOT written and NOT baked.**
- **v3.90 — 2026-08-07 — MEM.1: the SPX leak is confirmed, isolated to one box,
  and now has a tracer.** Fourteen boxes flat over 16.4 minutes (two of them
  falling); SPX +93.5 MB = 5.7 MB/min, with QQQ at +8 KB as the control that
  rules out chain size. Same code fleet-wide, so the F7 bake is exonerated. The
  ceiling turned out to be physical RAM — 951 MB boxes, no cgroup limit, zero
  swap, already 73–79% used — which explains the identical 419M peaks on two
  consecutive days. `tests/mem_tracer.py` v1.0 diffs a warm tracemalloc
  reference across the real per-tick chain path and names the retaining line;
  it refuses to start without headroom, because a second 200 MB process on that
  box would get the LIVE bot killed. **BUILT, NOT YET RUN — needs RTH and either
  a stopped bot or a resized instance.**
- **v3.89 — 2026-08-07 — RGM.1 F7 CLOSED AS MEASURED; the churn has a cause, a
  fix, and five independent checks.** 96.9% of label switches came from an
  emission branch with no commit bar, no margin and no dwell, at a median
  incumbent conviction of 0.08. Real-tape A/B: **20.8 → 4.2 switches per
  symbol-day**. Pre-registered agreement gate: TREND modal 63.4 → 69.1%,
  in-family 47.5 → 57.8% — steadier AND more right. Scope held (`L1 IDENTICAL`,
  and identical re-emitted baselines prove conviction dynamics unchanged). Suite
  287/rc=0, emission tests confirmed by name. Recorded against it: SWEEP
  in-family fell, 4.2 is above the stated 2–4, the switch count is one session,
  and **it is not BAKED**. Nine unresolved items carried forward, including the
  355-vs-13,860 contradiction and the `regime_flip` bucketing question that
  changes which strategy the churn was killing. Layer 1 remains untouched
  (RGM.2): 41.9% of ticks still carry one live regime or none.
- **v3.88 — 2026-08-07 — RGM.2 opened: the Layer-1 discrimination problem gets
  a tool before it gets an opinion.** F7 fixed WHICH label is emitted; RGM.2 is
  about whether the score vector carries enough information to choose one at
  all. The insight that makes it measurable: a hard veto does not lower a
  score, it destroys the ORDERING, so the question is not per-regime zero rates
  (already known) but whether a given TICK has anything to choose between.
  `tests/discrimination_census.py` v1.0 answers it off the existing corpus with
  no engine run — dead ticks, zero-argmax ticks, #1−#2 separation with dead
  ticks excluded, and live-regime count. Filed with three fix families ranked
  by surgicality and an honest calendar: only the census and a narrow veto fix
  fit before the freeze. **BUILT, NOT YET RUN.**
- **v3.87 — 2026-08-06 — RGM.1 F7: the unprotected branch is closed, behind a
  live A/B.** `conviction_integrator` v2.1 applies commit+margin in both
  branches and holds the incumbent when nothing qualifies, restoring the
  contract the module's own header has always claimed. Protection arms on the
  first committed read so a cold book is not pinned to the tiebreak head. Both
  laws now run every tick and each reports the other's label, so tomorrow's
  session measures the divergence on live tape instead of inferring it — and
  `OT_L2_PROTECT_BELOW_HOLD=0` runs the control. main v5.5 logs the pair on
  CHANGE only. `tests/label_agreement.py` v1.0 is the acceptance gate, with its
  hypothesis pre-registered before any number was read: if agreement against
  the price-action ground truth FALLS, the deploy dies. Built and proven on the
  desk; **not baked, and the authoritative suite run on control is not yet
  read.**
- **v3.86 — 2026-08-06 — RGM.1 F7: the emission law stops protecting the label
  below theta_hold.** Above 0.45 conviction a challenger must clear commit AND
  a margin; below 0.45 the incumbent is replaced by bare argmax every tick, with
  no commit bar, no margin and no dwell — contradicting the module's own header
  contract that a single-tick flicker can never move a held label. This is a
  correctness defect, not a tuning preference, and it explains why the switching
  cost failed: delta lives only in the protected branch, so that sweep tuned a
  knob outside the path where the churn happens. RANGING is singled out by its
  own asymmetry (13 min to build, ~1 min to fade), which parks it below the hold
  line. `tests/emission_law_sweep.py` v1.0 re-decides candidate laws over the
  RECORDED conviction vectors — 99.9% faithful on a planted world, where the
  current law gives 141.5 switches/symbol-day and protect-below-hold gives 1.0,
  a cliff rather than the delta sweep's slope. **BUILT, NOT YET RUN on the
  corpus.** Recorded honestly: a steadier label is not thereby a correct one.
- **v3.85 — 2026-08-06 — RGM.1: the fallback run-length probe ships.**
  `tests/rng_probe.py` v1.0 — the measurement the investigation has been blocked
  on. Answers whether RANGING's 11,972 no-bar-window ticks are one contiguous
  warm-up block or short isolated bursts, and therefore whether the churn is a
  bar-availability problem wearing a classification costume. Two discriminators
  beyond the original spec: the ts gap entering each mid-session run (tape
  contiguous => the input flapped, a plumbing bug; tape gapped => missing bars),
  and implied crossings counted with veto_attribution v1.1's semantics so the
  13,860 branch-change figure is checked like-for-like. Recorded honestly:
  **BUILT and proven on a planted corpus, NOT YET RUN on the real corpus** — the
  run is the deliverable and EV does not move until it produces a verdict.
  Read-only; any resulting fix to the veto grammar or the RANGING fallback
  remains POST-FREEZE.
- **v3.84 — 2026-08-06 — RGM.1: the fleet is churning, not trading.** Median
  hold 0.3 min, regime_flip exits 12->43->59 across three sessions, RANGING
  closing 54 of 95 trades at ~0% excursion. Three offline tools built
  (regime_switch_cost, score_series, veto_attribution). A switching cost does NOT
  fix it — the grammar is multiplicative, so a transition is a boolean flip and
  hysteresis cannot fight a boolean. Scores are sparse (45-96% exactly zero).
  RANGING's dominant cause is a BRANCH change into its no-bar-window fallback,
  which points at bar availability rather than the market. Next step: fallback
  run-lengths and first-appearance index.
- **v3.83 — 2026-08-05 — VW.1: VWAP was computed every tick and never written
  down.** vwap_orientation has never run — not a broken tool but one built
  against a schema that never landed; a scan of 11,138 journal records found no
  VWAP field anywhere while volatility_engine had it on its state all along.
  trade_readiness v1.5 emits {vwap, price_vs_vwap, dist_pct} per tick, signed and
  percent-of-VWAP so symbols are comparable. Needed before the freeze because
  AI's condor fix is VWAP-anchored and cannot be tested on absent history.
- **v3.82 — 2026-08-05 — A2.R: the co-occurrence question is CLOSED as research.**
  The drift study is null (+0.011% at 30 bars vs control, n≈3,500) against its own
  pre-registered criterion, so HTF direction is not a drift term inside a range.
  What co-occurrence costs is not forecast quality but RANGING losing argmax on
  98% of those ticks, hiding a true range state from the condor and butterfly.
  Recorded alongside it: L2 commits at conviction 1.00 on exactly those ticks —
  confidence and predictive value have come apart. Split-into-axes filed as a
  post-freeze candidate, gated on an offline measurement rather than the argument.
  Full write-up in MECHANICS.
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
  Thu Aug 27 build / Mon Aug 31 deploy to built-now / bakes Aug 10 on the same
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
  New item on Tue Aug 4, ✅ built same day, bakes Mon Aug 17. It closes a hole
  that was invisible because it was in the ROADMAP rather than here: TC.2's
  counterfactual names an observability precursor and the precursor had no date,
  no owner and no code. Filed as scope DISCOVERED, not slippage — it adds to BAC
  and EV together. Also corrects a claim made earlier in the same session that
  BoS levels needed capturing: they do not, and reading HEAD is what settled it.
- **v3.54 — 2026-08-04 — TWO DATES CORRECTED TO MATCH WHAT THE ITEMS SAY ABOUT
  THEMSELVES.** **AV** moved Sat Aug 1 → Thu Aug 20 and re-tagged `[DESK·DATA]`:
  dated due 08-01 while its own text records it OPENED 08-02 — due before it
  existed — and it waits on ~40 trades per cell for a 0.20 R read, a DC&A
  dependency rather than effort. **A2.3** moved Sun Aug 2 → Mon Sep 14: its own
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
