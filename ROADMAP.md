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

**Layer-1 DONE means:** on ≥ 10 sessions × 29 symbols of labeled tape, every
Tier-B row passes, the flat cut is frozen on multi-day base rates with the
holdout honored, no 15-s chatter, and every displacement has a nameable truth.
**Remaining: L1.6, L1.7 (TREND+SWEEP+pin+breakout tape), L1.9. All gated on
calendar time + labeling — no code blocker except the bookmark.**

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
- ⬜ **L2.5 — Wire L2 into the live loop as in-process shadow (Phase 0.2).**
  Currently NO live-loop path touches the integrator (verified). *To close:*
  run it in-process on the ALWAYS_ON boxes against the live v1.3 classifier,
  both reading the shared store; log both labels + the full conviction vector +
  stale flag per tick; warm-start from session bars at 9:30–9:35 (the ORB
  lockout covers the commit window). Observe-only — still drives no trade.
- ⬜ **L2.6 — Freeze the L2 weights as a stable baseline.** The pitchfork and any
  new conviction dimension can only be measured against a *frozen* L2. *To
  close:* a clean ~2-week hands-off production window (the one starting Monday
  2026-07-18) with L2 calibrated and unchanged. **This is the real gate for
  everything downstream of L2.**

**Layer-2 DONE means:** priors calibrated on real distributions, L2 shadow-
running live and logging, weights frozen against a clean baseline. **Remaining:
L2.4, L2.5, L2.6 — all gated on Layer 1 finishing first.**

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
- ⬜ **L3.2 — Define the gate matrix (Phase 2).** Replace identity-only dispatch
  with `fires iff regime ∈ permissive AND C ≥ bar(trade_type)`. Provisional
  bars encode binary-vs-nuanced (ORB/sweep low ~0.40; condor ~0.65; butterfly
  ~0.70 — all placeholders). *To close:* write the permissive×bar table into
  dispatch behind a flag, still in paper. **Gated on L2 frozen (L2.6).**
- ⬜ **L3.3 — Calibrate bars from ROI (Phase 3 — the 3–6 week campaign).** Paper
  runs gates wide open (~0.20 floor fleet-wide); bucket **fee-adjusted** ROI by
  conviction decile per trade type; place each bar at the lowest bucket whose
  *marginal* expectancy ≥ 0 (not cumulative). Min ~40 trades/bucket. *To close:*
  the fleet generates the distribution over weeks; needs L3.1 data flowing +
  the circularity split (fit sessions ≠ acceptance sessions).
- ⬜ **L3.4 — Circularity + statistics guards.** Fee/slippage-adjusted P&L only;
  haircut 0DTE spread slippage; split tape so bars are never fit on the sessions
  used to tune L1 truths; pooled-fleet curve + per-symbol sanity check. *To
  close:* enforce the holdout in the bucketer.
- ⬜ **L3.5 — Live descent, safely (Phase 3.5).** Go live with each bar one
  bucket ABOVE its paper crossing, descend one notch per review window, watch
  the newly-admitted bucket's realized expectancy, raise back on the first
  negative read. *To close:* requires the tiny-account live shakedown already
  gating the fill-confirmation work, then a bar to descend.
- ⬜ **L3.6 — Wire live + delete UNKNOWN + keep calibrated (Phase 4).** Replace
  the classify path and dispatch gate; grep the fleet tooling (status.py,
  query.py, alerts) and delete UNKNOWN from the enum; keep the data-fault
  no-trade. Recalibrate on a rolling window (monthly, or after any L1 truth
  change — a definition change invalidates the conviction distribution beneath
  the bars). *To close:* everything above, done and stable.

**Layer-3 DONE means (end state):** every trade type carries an empirically-
placed conviction bar in every permissive regime, the classifier never
abstains, and "no trade" is either a data fault or the honest verdict of the
bars — never a dead spot. **Remaining: L3.2–L3.6 (all of it). L3.1 is started
and log-only.**

---

## The critical path, plainly

```
L1.6 + L1.7 (labeled TREND/SWEEP/pin/breakout tape)   <- calendar time + label_day.sh
   |__ L1.9 bookmark (unblocks honest offline TRENDING) <- tester-first build
        |__ LAYER 1 DONE
             |__ L2.4 calibrate priors -> L2.5 shadow live -> L2.6 FREEZE weights
                  |__ LAYER 2 DONE  (+ the clean 2-week baseline)
                       |__ L3.2 gate matrix -> L3.3 ROI campaign (3-6 wk paper)
                            -> L3.4 guards -> L3.5 live descent -> L3.6 wire live
                                 |__ LAYER 3 DONE = the vision
```

Two things run *in parallel* and don't block the path:
- **L3.1 instrumentation** is already logging — every session from Monday is
  calibration-grade data banked ahead of the L3.3 campaign.
- **The pitchfork** (see README §PLANNED) is gated on **L2.6** (frozen weights),
  not on all of L3 — it enters as a new conviction dimension the moment L2 is a
  stable baseline.

## Risks worth re-stating

1. **Removing UNKNOWN shifts all safety onto the bars.** Stay in paper through
   L3.3. (The fleet already is.)
2. **Circularity is the quiet killer.** L3.4's holdout is not optional; neither
   is L1's (fit the flat cut and the bars on different sessions than you accept
   on).
3. **Cold-start labels are noise by design** (argmax of near-zero convictions at
   9:31). Harmless only because bars gate trades and the ORB lockout covers the
   commit window — preserve both.
4. **Non-stationarity.** A bar placed in a low-VIX month drifts. L3.6's
   recalibration cadence is architecture, not maintenance.
