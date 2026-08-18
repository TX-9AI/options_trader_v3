# TRANSITION ROADMAP — CONFIRMATORY → ANTICIPATORY
**Vertigo Capital · options_trader_v3 + day_trader_pro**
**Opened 2026-08-17 at `e64da15`. Supersedes ROADMAP.md and BACKLOG.md as the
governing plan until the gate in Phase 0 is answered.**

---

## STATUS OF EVERYTHING ELSE

**`docs/BACKLOG.md` — PAUSED.** Not abandoned. 62 open `[DESK]` items and 198
open squares stay exactly where they are. Work returns from it **only** when it
serves the retool, and it returns by being named in a phase below, not by being
picked up because it was next.

**GO-LIVE — PAUSED.** The Fri Aug 28 anchor evaluated paper P&L of a fleet whose
**entry logic is the thing under replacement**. That number would measure a
system we are mid-way through changing, and would be read as a verdict on a
premise that has never actually run. **There is no live-cash date until Phase 0
returns an answer.** Collection continues; the fleet keeps trading paper.

⚠️ **WHAT IS NOT PAUSED:** collection, the EOD conductor, the S3 push, the
warehouse, and **the exit stack**. Nothing in this roadmap touches exits — see
the asymmetry below.

---

## THE FINDING THIS PLAN EXISTS TO ACT ON

**The founding premise:** infer a pattern *forming*, express it as a confidence
factor, **scale the entry on that confidence**.

**What was built instead:** a confidence number that confirms moves already
made. Measured, repeatedly, in-repo:

- ORB grade **inverted**: A 399 trades **−$8,244** at 1.5× size vs B 220 trades
  **+$1,893**. ~90% of the grade was one column printed twice plus two
  constants. Its own conclusion: *"High conviction means the trend is already
  obvious, which means LATE."*
- Conviction **inverts in the premium regimes**: RANGING `RGCV.nf` **1.00** vs
  `.ok` **0.34**; COMPRESSION 0.59 vs 0.36. **1.00 vs 1.00 in trend** — no
  separation anywhere.
- **Layer 3 is `NOT STARTED. 0%`** (ROADMAP §L3, verified). The gate-and-scale
  premise **was never run**. A proxy assembly ran instead and inverted.
  **The premise is UNTESTED, not refuted.** That is the single most important
  sentence in this document.

**Fable's verdict (2026-08-17): RETOOL WITH A NEW CORE.** Lagging is
**assembled, not structural** — a leaky integrator over argmax agreement can
only be confident once winning has persisted. That is a property of the
combiner, not of the data.

**⚠️ THE ASYMMETRY THAT GOVERNS EVERY DECISION BELOW.** This system already uses
confirmation where confirmation belongs — the **exit** stack: `orb_trail_stop`
95% win / 107 trades / +$37,848; `theta_bleed` 100% / 107; `continuation_trail`
85% / 149. **Confirmation is CORRECT at exits and WRONG at entries.** The retool
moves one boundary. It does not touch the plumbing, and it must not touch the
exits.

---

## PHASE 0 — THE GATE. **NOTHING ELSE STARTS UNTIL THIS ANSWERS.**

> **Does anything already collected separate favourable from never-favourable
> trades AT DECISION TIME?**

**P0.1 — `tests/separation_probe.py` v1.0 — ✅ BUILT 2026-08-17** *(control-side, read-only; no bake, no box touched)*
Run the never-favourable split — reusing `axis_crosstab` / `a2_excursion`
machinery — against **every decision-time primitive**, as-of joined at each
historical entry stamp:

| primitive | source | depth | note |
|---|---|---|---|
| shadow velocity + level-position | `shadow/` per-tick jsonl, 29 boxes | since 07-22, ~4 wks | **deepest candidate** |
| readiness grade + machine state | `signal_journal` | since 07-27, ~3 wks | LOG-ONLY today |
| ORB geometry (`retest_depth_px`, origin distance) | `orb_engine` v3.7 journal | since 07-18 | joinable now |
| `direction_conf` | replay via `regime_axes` | n=571 measured once | **already separates +0.188** |
| pitchfork `pos_pct` | replay from banked tape | thin live (~08-13) | replayable |
| ledger touch/hold/breach | `liquidity_ledger` | days only (08-15) | **REFUSE per §12** — report n only |

**PRE-REGISTERED SUCCESS CRITERION — written before the run, not after:**
> nf below ok, **CI-separated**, on **n ≥ 200 across ≥ 10 sessions**, with
> **stable sign across at least the two post-LIQ.1 windows**.

**Rules:** window-tagged across the four archive regimes (pre-LIQ.1 · post-LIQ.1
08-12 · post-LIQ.6 08-15 · post-FEED.2 08-17) · **08-14 excluded** (130 of 153
trades are identity-chain/CNT.1 artifacts) · `trend_continuation_breakout` rows
from 08-07 excluded · n and sessions on every cell · underpowered cells
**refused, not reported**.

**THE THREE OUTCOMES, AND WHAT EACH MEANS:**
- **A primitive clears** → it is the confidence factor. The remaining work is
  **wiring**, and Phase 1 begins.
- **Nothing clears, including shadow velocity with four fleet-weeks** → the
  honest escalation is **new inputs**, not a new combiner. Phase 1 is replaced
  by a chain-derived expectation build.
- **Ambiguous** → say so. An absent measurement is not a null.

**P0.2 — Verify the chain-snapshot corpus** *(read-only, 30 min)*
⚠️ Fable flagged chain snapshots as unharvested and irreproducible — **that is
stale**: `harvest.py` v0.5.1 has pulled `data/chain_snapshots` to control since
**2026-07-27**. Confirm what actually landed (dates, size, per-strike IV/greeks
completeness). **This is the fallback input class if P0.1 returns nothing**, and
it is the only dataset that cannot be reconstructed later.

**P0.3 — AX.3's unbuilt half: emit `direction_conf` onto the journal**
`analysis/regime_axes.py:10` records `nf 0.697 / ok 0.885 / gap +0.188 —
SEPARATES`, and **nothing journals it.** A measured separator that drives
nothing. Emission is the precondition for testing it forward under the same
rules as everything else. **Carried forward from BACKLOG AX.3.**

---

## PHASE 1 — WIRE THE SEPARATOR, LOG-ONLY *(conditional on P0.1 clearing)*

**P1.1 — Emit the winning primitive at decision time**, journaled, gating
nothing. The repo's own established pattern.

**P1.2 — Selection-clean measurement.** Measured on trades the score did **not**
gate — otherwise the bar manufactures its own calibration. Pair with
**L3.2a's rejection ledger** (`analysis/rejection_ledger.py`, already built,
carried forward): *a bar that only shrinks the book is not confidence, it is
fear.*

**P1.3 — The QQQ acceptance test.** On 2026-08-17 the operator called QQQ's
first half a range **while it was happening** — no clean impulsive candle, price
rotating inside a prior range, failure to hold the break. The engine said
**TRENDING_BULL at 81% conviction** and three directional trades stopped out.

**THE TEST IS AT TRIGGER TIME, NOT AT 09:35.** An earlier draft of this document
said 09:35 and the operator was right to reject it: at 09:35 there is **one 5m
bar of RTH**, no break has been attempted, so *"failure to hold the break"* is
not computable and *"rotating inside a prior range"* has no swings to read.
**ORB fires 09:35–11:00** — the decision instant is whenever the trigger fires,
possibly 10:15, and by then the break attempt and its failure ARE observable.
The three QQQ trades stopped out through the morning, not at the open.

**What is genuinely available at 09:35** is narrower and worth building anyway:
position inside yesterday's range, gap size (**A2.6b**), overnight range width
vs ATR (**now available post-FEED.2**), opening-range width vs typical.

**⚠️ AND THE SIGNAL IS PERMISSIVE-UNTIL-DISQUALIFIED (operator, 2026-08-17):**
> *"If we need a few bars before asserting ranging, that's an acceptable goal.
> Even if it means we allow ORB entries until it establishes unfavorable
> conditions."*

**THIS MAKES IT A REVOCATION SIGNAL, NOT AN AUTHORISATION SIGNAL, AND THE
DISTINCTION IS LOAD-BEARING:**
- A signal that must **GRANT** permission has to be right EARLY or it costs
  trades it should have allowed — it would be graded against prescience. That
  is the trap the 09:35 framing walked into.
- A signal that **REVOKES** permission costs **nothing until it fires**, so it
  may take the bars it needs. ORB keeps firing on its own confirmed geometry:
  regime-agnostic by design and profitable in TRENDING_BULL (+$4,394),
  TRENDING_BEAR (+$4,196), BREAKOUT_VOLATILE (+$2,729) and UNKNOWN (+$3,483).
- ⚠️ **THE TARGET CELL IS ALREADY LATE-FORMING, WHICH IS WHY THIS WORKS.**
  `RANGING × ORB` is 15 trades at **−$192.73** over 26 sessions — entries taken
  **after** a range had established. **A revocation signal needing 3–6 bars
  still catches them.**
- ⚠️ **THE COST OF BEING SLOW IS BOUNDED AND MEASURABLE:** trades taken between
  the range establishing and the signal firing. That is a number the probe can
  report, not an unknown.

**PASS = the engine withdraws permission before the second and third QQQ 08-17
entries, using only tape available at each instant, AND does not withdraw it on
the trending sessions above.** Both halves required — a signal that revokes
everything is not a signal. Concrete pass/fail on real sessions, honestly
scoped, and it does not require prescience.

---

## PHASE 2 — THE GATE AND THE SIZE *(conditional on Phase 1)*

**The five preconditions before any score sizes an entry**, in order — all
carried from Fable Q4:

1. **Separation with direction** — nf-rate falls monotonically across score
   deciles, out-of-fit-window, CI-separated at the extremes. *RGCV fails this
   today in the inverted direction.*
2. **Selection-clean** — tested on ungated trades (Phase 1).
3. **Window stability** — stable sign and rough magnitude across the four
   archive regimes. A separator that flips across LIQ.6 is a level artifact.
4. **Marginal-ROI placement, not quantile placement** — the size step sits where
   fee-adjusted expectancy of the top band exceeds the base band by more than
   the added risk. **This is L3.4's own spec, never reached.**
5. **A payoff structure that tolerates being early.**
   ⚠️ **DESIGN REASONING, NOT EVIDENCE.** An anticipatory signal is early by
   definition; early *debit* bleeds theta while it waits, bounded *credit*
   collects. **TC.6 has four trades ever, all 2026-08-17** — §12 forbids any
   empirical claim from that. Treat as a hypothesis to test, not a finding.
   Fable presented this as a precondition; it is a preference until measured.

**P2.4 — FRC.1 sits underneath all of it.** The fleet's gross edge is ~2% of its
own round-trip spread. **No confidence factor survives contact with friction it
was not measured against.** Carried forward.

---

## PHASE 3 — WHAT RETURNS FROM THE PAUSED BACKLOG, AND WHY

**Triage test, stated so it can be checked:** an item returns only if it
**(a)** produces a decision-time signal, **(b)** enables the separation test, or
**(c)** protects data that cannot be recreated. Everything else stays paused —
**including nearly-finished work**.

**RETURNS — (a) decision-time signal:**
- **AX.3** — `direction_conf` emission. *The only measured separator.* → P0.3
- **Level.1 / Level.2** — graded `level_strength` (ON H/L · PDH/PDL > multi-day
  S/R > session H/L > equal-H/L) replacing the flat `is_named` bool. **Position
  state, not momentum** — exactly the class the operator's QQQ read used.
  ⚠️ **Now unblocked**: FEED.2 (08-17) delivers the overnight tape ON H/L needs,
  which is why this sat queued since 07-24.
- **RGM.2** — the Layer-1 discrimination census. Reframed: not "fix the label"
  but "which L1 features carry decision-time information."

**RETURNS — (b) enables the test:**
- **L3.2a** — rejection ledger, already built. The selection-clean half.
- **DRF.1** — trigger-conditioned drift with its positive control. **Its result
  already points here**: the edge lives in the entry TRIGGER, not the label.
- **A2.6b `gap_pct`** — the overnight gap is never measured. Cheap, and it is a
  decision-time input available before the open.

**RETURNS — (c) irreplaceable data:**
- **MEM.1** — the SPX OOM leak. Not a signal, but a box that dies mid-session
  loses tape that DXFeed's same-evening history makes unrecoverable.
- **WH.5 follow-through** — warehouse confirmation. The separation probe reads
  collected artifacts; a silent shortfall corrupts the input.

**STAYS PAUSED — named so the decision is visible, not silent:**
- Every **exit** item — CND.8, F3, the floor sweep, trail tuning. *Confirmation
  is correct at exits and they are the measured winners.*
- **Grade/scorer calibration** on the existing factor set — the factors are the
  thing being replaced.
- **BFLY / condor / TC.6 entry tuning** — downstream of the confidence quantity.
- **L1.6 / L1.7 / L1.9 / L1.11 and the L2.6 freeze.** ⚠️ **Freezing L2 would
  lock in the confirmatory conviction this roadmap exists to replace.** The
  251 TRENDING candidates and the labeling habit keep their value and wait.
- **A2.x, PF.x, VW.x, RPT.x** — measurement refinements to a path under review.

---

## HOW THIS ENDS

**If P0.1 clears:** Phases 1–2 run, BACKLOG resumes filtered through the new
core, and a go-live date is set **after** a confidence factor has passed all
five preconditions — not before.

**If P0.1 returns nothing:** that is the finding, and it is worth more than the
plan. The escalation is **new inputs** — chain-derived expectation first, since
it is already collected and cannot be backfilled — **not a new codebase**.
Fable's inventory is explicit that nothing goes wholesale: *deleting working
measurement infrastructure to rebuild it is the 774-line-duplicate error at
larger scale.*

**⚠️ AND THE HONEST FAILURE CASE:** if no input class available at decision time
separates outcomes, the premise itself may not be reachable with this data.
**That would be worth knowing.** Two months of good engineering pointed at the
wrong quantity is still the wrong quantity — and the measurement discipline that
made this detectable is the reason we can find out cheaply rather than after
go-live.
