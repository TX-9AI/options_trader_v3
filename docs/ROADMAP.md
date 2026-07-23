# ROADMAP.md — options_trader v3: boolean regime gates → conviction-bar gating

**v2.0 — 2026-07-18 — CHECKLIST REWRITE.** Supersedes the v1.0 prose plan
(2026-07-10). Same destination, same four phases, now as a tracked checklist:
every step is marked ✅ DONE / 🔄 IN PROGRESS / ⬜ NOT STARTED, done steps keep a
one-line note of *how*, and remaining steps carry *what it will take to close
them*. The three-layer target is unchanged:

> **Layer 1** — instantaneous per-regime confluence scores (evidence).
> **Layer 2** — leaky conviction integrator with persistence (a stable label +
>   a first-class conviction number).
> **Layer 3** — trade gates: `fires iff regime ∈ permissive AND C ≥ bar(trade_type)`,
>   every bar placed empirically at the marginal fee-adjusted-ROI zero crossing.

**Core invariant (never violated):** regime shapes the trade; trade outcomes
never feed back into regime classification.

**Where we are in one sentence:** the *machinery* for L1 and L2 is built and
proven in shadow/replay; what remains is **calibration data** — real trend,
sweep, and pin tape, labeled — which only calendar time on the live tape can
produce. L3 is the genuinely unbuilt layer and is gated on that data.

---

## LAYER 1 — Instantaneous confluence scorer (evidence)

**Status: BUILT, calibration ~50%. The scorer is done; its thresholds await
labeled tape.**

- ✅ **L1.1 — Single canonical scorer.** `regime_confluence.py` v1.1 is the sole
  Layer 1 (`hard_veto × soft_necessary × Σ corroborators`). The duplicate
  `EvidenceAdapter` math was deleted (defect A). One implementation, no
  circularity.
- ✅ **L1.2 — Truth grammar written.** `REGIME_TRUTHS.md` v0.2 — per-regime hard
  vetoes + graded confluence + the discriminator matrix.
- ✅ **L1.3 — Replayable over deterministic tape.** `tests/replay_confluence.py`
  v2.0 runs the *real* engines as-of, bar by bar, over the DXFeed 1-min CSVs;
  writes per-tick jsonl + diary. Structural acceptance (Tier A) 5/5 on the
  07-09/07-10 sample.
- ✅ **L1.4 — Proven end-to-end at fleet scale.** 29 symbols, 10,651 ticks;
  RANGING correctly dominates chop; UNKNOWN reclamation confirmed real.
- ✅ **L1.5 — trend_engine direction fix (v3.1).** The dead-4h weight bug that
  made TRENDING unreachable is fixed (intraday-primary tf_weights); backtested,
  TRENDING roughly doubled, gain came entirely from the UNKNOWN bucket, chop
  unchanged. Live on the fleet since 2026-07-17.
- 🔄 **L1.6 — Freeze the flat-angle cut from multi-day base rates.** First-light
  says `FLAT_ANGLE_CUT_DEG = 20°` is too low (genuine-RANGING p90 = 22°,
  explaining the 13% all-zero residual). *To close:* sweep 16–26° against
  **≥ several distinct labeled sessions** with the rotating 30% holdout — never
  off one day. **Needs: accumulated labeled tape + the flat-angle-by-label
  distribution the harness already prints.**
- 🔄 **L1.7 — Complete the per-regime truth tables (Tier B acceptance).** Each
  regime must fire on its own tape:
  - ✅ RANGING — validated (64% dominance on the 07-09 chop day).
  - ⬜ TRENDING — **tape gap.** 0% in the sample because there is no trend day in
    it. *To close:* one genuine trend day on tape, labeled, showing TRENDING_*
    dominant ≥ ~50% with RANGING vetoed through it.
  - ⬜ SWEEP — **tape gap.** *To close:* one mapper-confirmed named-zone reclaim,
    labeled, showing SWEEP > 0 at the sweep bar decaying over ~3 bars.
  - 🔄 COMPRESSION — partial. *To close:* a clean coil-into-pin session showing
    COMPRESSION rising vs RANGING through the final hour.
  - 🔄 BREAKOUT — partial (have MU/NVDA). *To close:* more clean breakouts
    holding BREAKOUT > 0 through the BB re-entry flicker at ADX 43–50.
- ✅ **L1.8 — EOD labeling tool.** `day_trader_pro/label_day.sh` v1.0 tags each
  session's trend/sweep/pin/breakout symbols → `reports/session_labels.jsonl`;
  `--gaps` prints the Tier-B shopping list. This is the mechanism that fills
  L1.6/L1.7. *Habit, not code, is the remaining work.*
- ⬜ **L1.9 — Offline replay HTF-depth fix (BOOKMARK) — defect S.** The daily
  replay feeds one day-folder at a time, starving 1h/1d, so the diary
  under-reports TRENDING even after L1.5. *To close:* persist a rolling
  ~15-session **bar** window per symbol (engines are stateless — bars, not
  state), load+append+roll each EOD, score today warm. **Build and prove inert
  on the TESTER first**, then graft onto `validate_regime.sh`. `regime_backfill
  --rebuild` re-scores history once it lands. *Blocks honest closure of the
  TRENDING Tier-B row via the daily diary.*

- ✅ **L1.10 — Ramp de-saturation (scores were switches, not dials).** Audit of
  60,341 ticks found the scorer's ramp bounds set for far narrower tape than the
  fleet actually trades: `room_s` pegged at 1.0 on 72.7% of scored ticks (hi
  bound at input p27), `osc_s` on 70.5% (hi at p30). RANGING therefore hit
  p90 = 1.0 every session and tied with TRENDING on 14–25% of ticks, leaving the
  L2 argmax to break those ties on integration speed (τ_up 40s vs 780s) rather
  than evidence. *Closed by:* (a) `regime_confluence.py` v1.2 — all 14 ramp
  bounds env-overridable via `OT_RC_<NAME>`, so calibration is a config change
  with instant rollback; (b) `room_s` and `osc_s` re-fitted from tape and
  promoted to defaults (`RANGE_ROOM_LO` 0.05→0.17, `RANGE_ROOM_HI` 0.20→1.00,
  `OSC_CROSS_LO` 2→4, `OSC_CROSS_HI` 5→10). Fitted on 6 sessions
  (07-14/15/16/17/20/21; **07-13 excluded — ADX-starved, no warm-up**), and the
  pool independently re-derives the same bounds — convergence, not a one-day fit.
  *Result:* `room_s` 15.8%→66.2% graded, `osc_s` 22.5%→60.0%, RANGING p90
  1.0→0.476, **A2 violations 14.4%→4.3% of ticks** (−71% to −79%, consistent on
  every session). New tooling: `tests/ramp_calibration.py` (per-term saturation +
  input percentiles + suggested bounds) and `tests/a2_cooccurrence.py` (A2
  tie-break audit + HTF-conditioned forward drift with a RANGE_ONLY control);
  `day_trader_pro/devtools.sh` v1.17 item 52 runs the latter.
  *Two findings recorded, not yet actioned:* **(i)** `OSC_CROSS_*` is shared with
  `_compression` (few crossings = coil), so the crossings axis is a see-saw —
  widening it also lifts COMPRESSION (p90 0.65→0.879); it is now the term to
  watch. **(ii)** The residual 4.3% is **not** saturation — it is genuine
  cross-horizon co-occurrence (TRENDING reads 1d/1h/15m/5m, RANGING reads a
  25-bar 1-minute window), so A2's premise of same-horizon mutual exclusivity is
  itself mis-specified. Re-specifying A2 is a REGIME_TRUTHS decision, not a
  calibration one.
- ⬜ **L1.11 — Fit the remaining ramps (`flat_s`, `adx_s`, `align_val`).** Left
  deliberately untouched by L1.10. `flat_s` is a conditional sample (only ticks
  past the flat veto) so its measured distribution is the wrong population.
  `adx_s`/`align_val` cannot be fitted from replay at all: `align_frac` never
  exceeds 0.67 across the pool, the offline HTF-starvation signature. **Gated on
  L1.9 (bookmark)** or on fitting from live `feed_store.db` depth instead.

**Layer-1 DONE means:** on ≥ 10 sessions × 29 symbols of labeled tape, every
Tier-B row passes, the flat cut is frozen on multi-day base rates with the
holdout honored, no 15-s chatter, and every displacement has a nameable truth.
**Remaining: L1.6, L1.7 (TREND+SWEEP+pin+breakout tape), L1.9, L1.11. All gated
on calendar time + labeling — no code blocker except the bookmark. L1.10 (ramp
de-saturation) is DONE and its tooling (`ramp_calibration.py`) also supplies the
by-label distribution L1.6 needs.**

---

## LAYER 2 — Conviction integrator (stable label + conviction)

**Status: PORTED and shadow-proven. Drives nothing yet, by design; calibration
and live-wiring remain.**

- ✅ **L2.1 — Consensus core ported in-repo (Phase 0.1).**
  `analysis/conviction_integrator.py` v2.0 — leaky per-regime conviction, decay
  resistance scaled by banked conviction, dt-aware, restart-persistent, embedded
  14/14 validation suite against the 07-09 failure catalog (defect B).
- ✅ **L2.2 — v3 emission law.** Always emit argmax + conviction; the UNKNOWN
  fallback is deleted from emission. Indecision is a low conviction number on a
  best-fit label, never a seventh label. θ_hold/displacement hysteresis kept
  (no chatter, no blend). The STALE/data-fault no-trade state survives; the
  indecision no-trade state does not.
- ✅ **L2.3 — Fed by the canonical L1.** The integrator consumes
  `regime_confluence.evidence()` (not its own duplicate math); both run in
  `replay_confluence.py` v2.0, which emits an `l2` object per tick and a
  Layer-2 report section (emitted distribution, label switches vs L1 flips —
  the churn metric — stale%).
- ⬜ **L2.4 — Calibrate the priors against real evidence distributions.** Every
  threshold in the integrator is a PRIOR. *To close:* recompute them from the
  accumulated labeled tape once L1 Tier-B passes — the integrator's decay/commit
  constants want the same multi-day distributions the flat cut does.
  **Gated on Layer 1 being DONE** (calibrating L2 on an uncalibrated L1 is
  circular).
- ✅ **L2.5 — L2 wired into the live loop (shipped 2026-07-21, `main.py` v4.0).**
  Shipped **wider than the original spec below**: this entry called for an
  observe-only in-process shadow that "drives no trade", but what deployed makes
  the integrator's committed label the **live trade gate** — `primary_regime`
  and `conviction` are overridden by L2, replacing the v1.3 classifier's raw
  argmax. Driver was a real defect: v1.3 dropped to UNKNOWN mid-trend at avg
  ADX ≈ 29, a hard no-trade gate firing during the strongest conditions; the
  integrator holds a regime through single-tick evidence drops (θ_hold
  hysteresis) and never emits UNKNOWN. **The conviction NUMBER is still
  observe-only** — gates run wide open, conviction logged not gated, L3 tunes
  bars later; paper P&L is the arbiter. v1.3 still runs and populates
  RegimeState's rich fields. Book persisted per box
  (`data/integrator_state.json`), warm-loaded at boot.
  **Rollback: `OT_REGIME_ENGINE=v13`.**
  *Sequencing note:* this landed **ahead of L2.4** (prior calibration), so the
  live label is currently driven by uncalibrated priors. That inverts the
  roadmap's own L2.4→L2.5→L2.6 order and is worth closing deliberately.
  *Consequence for L1 work:* because L2 labels now gate trades, any L1 scoring
  change (e.g. `regime_confluence.py` v1.2 ramp de-saturation) is a **live
  trading behaviour change**, not an analysis-layer one.
  *NOTE:* the `shadow-observer.service` on the QQQ paper box (2026-07-18) is a
  **different** shadow subsystem — velocity primitives + sweep-precursor
  scorers, not the conviction integrator. It advances the separate
  sweep-precursor track.
- ⬜ **L2.6 — Freeze the L2 weights as a stable baseline.** The pitchfork and any
  new conviction dimension can only be measured against a *frozen* L2. *To
  close:* a clean ~2-week hands-off production window (the one starting Monday
  2026-07-18) with L2 calibrated and unchanged. **This is the real gate for
  everything downstream of L2.**

**Layer-2 DONE means:** priors calibrated on real distributions, L2 running live
and logging, weights frozen against a clean baseline. **Remaining: L2.4, L2.6.
L2.5 is DONE (2026-07-21) but shipped ahead of L2.4, so the live gate currently
runs on uncalibrated priors — closing L2.4 is now the priority, not optional.**

---

## LAYER 3 — Conviction-bar trade gates (the genuinely new build)

**Status: NOT STARTED. 0% — this is the real remaining engineering + the core
empirical campaign.**

- 🔄 **L3.1 — Instrument every signal (Phase 3.1) — LOG-ONLY, STARTED 2026-07-18.**
  ✅ Built this session: `analysis/signal_journal.py` v1.0 + `setup_scorer` v1.3
  (`scored` events for every scored signal, **below-B REJECTs included**, with
  bid/ask/spread/IV quote context) + `main.py` v3.9 (`disposition`:
  fired/sizing_rejected/invalid; `condor_plan`/`condor_leg` conviction) +
  `orb_engine` v3.7 (defect-G `retest_depth_px` + near-miss `retest_check`
  distribution). *To fully close:* let it run and confirm the jsonl captures a
  full session across the fleet; optionally add an EOD-conductor collection
  phase once volume justifies (deliberately not wired yet).
- ⬜ **L3.2 — Missed-trade / rejection ledger (recall) (Phase 3.1b) — NOT STARTED.**
  L3.1 measures **precision** (of trades taken, which were good?). This step
  measures **recall** (of trades we *should* have taken, how many did we miss?) —
  the other half of calibration, and invisible without it. A tuned bar that
  raises win-rate-on-taken while silently discarding most of the edge looks like
  progress and isn't; this is the guard against that. Two false-negative classes,
  kept distinct:
  - **(a) Threshold near-miss** — a setup fully *formed* but a gate *declined* it
    (conviction below the bar, sizing reject, ORB retest just outside tolerance).
    L3.1 already emits the raw events (`scored` below-B REJECTs, `disposition`,
    `retest_check`); this step is the layer *on top* that consolidates them.
  - **(b) Coverage gap** — *no* setup formed at all, yet the market did the thing
    a strategy exists to catch (a clean range the condor never engaged; a decisive
    break no ORB armed on). Not in L3.1 at all — found by scanning each strategy's
    target market-condition and asking "was a live setup present during it?"
  *The deliverable* = `analysis/rejection_ledger.py` + an EOD summary artifact
  (`reports/rejection_summary_<date>.jsonl` + human digest) that, per strategy per
  session, records every near-miss with: strategy, timestamp, the setup state at
  decision, the **exact failing gate/clause**, the conviction/score if any, and —
  the piece that makes it calibration-grade — the **forward outcome**: what price
  did over the next N bars / to the setup's would-be stop and target, so each
  rejection is labeled *dodged-a-loss* vs *missed-a-winner*. Reuses the same
  as-of replay machinery as `replay_confluence.py` (no look-ahead: outcomes are
  computed only from bars *after* the decision bar). Log-only, drives nothing.
  *To close:* build against `signal_journal` events + the store tape; prove the
  forward-outcome join is leak-free on a known session; confirm both classes (a)
  and (b) populate across a fleet session. **Gated on L3.1 data flowing; not
  gated on L2 freeze** (it observes the *current* ruleset — see caveat below).
  ⚠️ **Ruleset-relative:** a near-miss is only meaningful against a *fixed*
  ruleset. While strategy gates are still changing (e.g. the sweep ORB-ownership
  gate, sweep v3.2), a rejection logged today may not be one next week. Before L1
  truths freeze this ledger is a **gap-finder** (surfaces gross coverage holes and
  obviously-mis-set bars); *after* L2.6 freeze it becomes **calibration-grade**
  recall input to L3.4. Tag every ledger row with the ruleset/version hash so
  pre-freeze and post-freeze rows are never pooled.
- ⬜ **L3.3 — Define the gate matrix (Phase 2).** Replace identity-only dispatch
  with `fires iff regime ∈ permissive AND C ≥ bar(trade_type)`. Provisional
  bars encode binary-vs-nuanced (ORB/sweep low ~0.40; condor ~0.65; butterfly
  ~0.70 — all placeholders). *To close:* write the permissive×bar table into
  dispatch behind a flag, still in paper. **Gated on L2 frozen (L2.6).**
- ⬜ **L3.4 — Calibrate bars from ROI + recall (Phase 3 — the 3–6 week campaign).**
  Paper runs gates wide open (~0.20 floor fleet-wide); bucket **fee-adjusted** ROI
  by conviction decile per trade type; place each bar at the lowest bucket whose
  *marginal* expectancy ≥ 0 (not cumulative). Min ~40 trades/bucket. **The L3.2
  rejection ledger enters here as the recall axis:** a candidate bar is judged not
  only by the expectancy of trades it *admits* (precision, from L3.1) but by the
  expectancy of the near-misses it *excludes* (recall, from L3.2). Lowering a bar
  is only justified when the newly-admitted bucket's *marginal* expectancy ≥ 0 in
  BOTH the taken-trade curve and the missed-trade forward outcomes — otherwise the
  bar is discarding positive-expectancy setups (recall loss) or admitting noise
  (precision loss). *To close:* the fleet generates the distribution over weeks;
  needs L3.1 + L3.2 data flowing + the circularity split (fit sessions ≠
  acceptance sessions).
- ⬜ **L3.5 — Circularity + statistics guards.** Fee/slippage-adjusted P&L only;
  haircut 0DTE spread slippage; split tape so bars are never fit on the sessions
  used to tune L1 truths; pooled-fleet curve + per-symbol sanity check. The L3.2
  ledger's forward outcomes are held to the *same* leak-free / holdout discipline
  as taken-trade P&L. *To close:* enforce the holdout in the bucketer.
- ⬜ **L3.6 — Live descent, safely (Phase 3.5).** Go live with each bar one
  bucket ABOVE its paper crossing, descend one notch per review window, watch
  the newly-admitted bucket's realized expectancy, raise back on the first
  negative read. *To close:* requires the tiny-account live shakedown already
  gating the fill-confirmation work, then a bar to descend.
- ⬜ **L3.7 — Wire live + delete UNKNOWN + keep calibrated (Phase 4).** Replace
  the classify path and dispatch gate; grep the fleet tooling (status.py,
  query.py, alerts) and delete UNKNOWN from the enum; keep the data-fault
  no-trade. Recalibrate on a rolling window (monthly, or after any L1 truth
  change — a definition change invalidates the conviction distribution beneath
  the bars). *To close:* everything above, done and stable.

**Layer-3 DONE means (end state):** every trade type carries an empirically-
placed conviction bar in every permissive regime, the classifier never
abstains, "no trade" is either a data fault or the honest verdict of the bars —
never a dead spot — and every bar is defensible on **both** axes: the trades it
admits are positive-expectancy (precision) and the trades it excludes are not
(recall). **Remaining: L3.2–L3.7 (all of it). L3.1 is started and log-only.**

---

## The critical path, plainly

```
L1.6 + L1.7 (labeled TREND/SWEEP/pin/breakout tape)   <- calendar time + label_day.sh
   |__ L1.9 bookmark (unblocks honest offline TRENDING) <- tester-first build
        |__ LAYER 1 DONE
             |__ L2.4 calibrate priors -> L2.5 shadow live -> L2.6 FREEZE weights
                  |__ LAYER 2 DONE  (+ the clean 2-week baseline)
                       |__ L3.3 gate matrix -> L3.4 ROI+recall campaign (3-6 wk paper)
                            -> L3.5 guards -> L3.6 live descent -> L3.7 wire live
                                 |__ LAYER 3 DONE = the vision
```

Two things run *in parallel* and don't block the path:
- **L3.1 instrumentation + L3.2 rejection ledger** are both log-only and both
  bank calibration-grade data ahead of the L3.4 campaign — L3.1 the taken-trade
  (precision) side, L3.2 the missed-trade (recall) side. Neither is gated on the
  L2 freeze to *run*; both are ruleset-relative, so their rows are version-tagged
  and only pooled for calibration after L2.6.
- **The sweep-precursor observer** (`shadow-observer.service`, live on the QQQ
  paper box since 2026-07-18, stage 1) is banking velocity-primitive data to
  validate against `data/OHLC/` before its scorers (stage 2) are ever trusted —
  the sweep-reversal precursor track, independent of the L1→L2→L3 spine.
- **The pitchfork** (see README §PLANNED) is gated on **L2.6** (frozen weights),
  not on all of L3 — it enters as a new conviction dimension the moment L2 is a
  stable baseline.

## Risks worth re-stating

1. **Removing UNKNOWN shifts all safety onto the bars.** Stay in paper through
   L3.4. (The fleet already is.)
2. **Circularity is the quiet killer.** L3.5's holdout is not optional; neither
   is L1's (fit the flat cut and the bars on different sessions than you accept
   on). The L3.2 ledger's forward outcomes are held to the same discipline —
   outcomes computed only from post-decision bars, never look-ahead.
3. **Precision without recall is a mirage.** Tuning bars on taken-trades alone
   (L3.1) can raise win-rate while silently shedding most of the edge. L3.2 is
   the counterweight; a bar is not "calibrated" until it is defended on both
   axes. This is *why* L3.2 exists as its own step and not a footnote to L3.4.
4. **Cold-start labels are noise by design** (argmax of near-zero convictions at
   9:31). Harmless only because bars gate trades and the ORB lockout covers the
   commit window — preserve both.
5. **Non-stationarity.** A bar placed in a low-VIX month drifts. L3.7's
   recalibration cadence is architecture, not maintenance.
