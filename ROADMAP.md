# ROADMAP.md — options_trader v3: from boolean regime gates to conviction-bar gating

v1.0 — 2026-07-10 — Written against v2 @ `a181dd2` and v3 @ `49d7af8` (full-tree
diff). Companion to the v3 README's "Reasoning Model" section. This document is
the reconciliation (Part 1), the honest distance-to-vision assessment (Part 2),
and the build plan to the calibrated end state (Part 3).

---

## Part 1 — Reconciliation: the reasoning functions, v2 vs v3-as-it-stands vs v3-vision

| Layer | v2 (and v3 today — identical code) | v3 vision (target) |
|---|---|---|
| **Classification** | Memoryless boolean cascade, first-match-wins priority (sweep → breakout → compression → trending → ranging), re-run from scratch every tick. `regime_classifier.py` v1.3. | Consensus integrator: per-regime conviction accumulating agreement and bleeding on conflict, weighted by banked conviction. New data is referential to the established frame, never judged in isolation. |
| **The label** | Boolean verdict. A regime either qualifies or it doesn't; "how characteristic" exists only as a post-hoc conviction number that gates nothing. | Single argmax label + conviction as a first-class output. Less-characteristic tape = same label, lower conviction (0.89 → 0.37). No blending — displacement only, when a competitor's accumulated conviction overtakes. |
| **Dead spots** | UNKNOWN is a regime and a hard no-trade gate (`main.py` ~L469); the 07-09 post-mortem showed it eating clean breakouts via 15-s flicker and warehousing 88% of its dwell in unnamed-but-real chop. | UNKNOWN eliminated as a regime. Every tape state gets its best-fit label; indecision is expressed as conviction, and untradeability becomes *emergent* (no trade type's bar is cleared). The only remaining hard block is the data-fault state (stale feed / restart gap) — a data-integrity condition, not a regime opinion, already enforced by candle_feed's heartbeat (`OT_FEED_STALE_S`). |
| **Trade gating** | Two-layer: (1) regime *identity* must be in the strategy's permissive set (dispatch block, `main.py` L473–560); (2) `setup_scorer` A/B grade where regime conviction is one weighted dimension (20–30%) inside a composite score vs static per-strategy thresholds (B ≈ 0.52–0.55). Conviction never gates directly. | Regime conviction becomes the primary gate: trade fires iff regime ∈ permissive set AND `C_regime ≥ bar(trade_type)`. Bars differ by confluence character — binary-factor trades clear low bars, nuanced-factor trades clear high bars — and every bar is placed empirically at the marginal-ROI zero crossing. Setup grading survives as the *sizing* layer (A=1.5×, B=1.0×), not the gate. |
| **Data substrate** | v2: Yahoo-Finance client — a different series than the traded tape (caught diverging on the opening range). | **Shipped in v3.0:** single shared TastyTrade/DXFeed store per box; every consumer reads the traded tape. This is the load-bearing prerequisite — conviction-vs-ROI calibration on a divergent feed would be calibrating a board the bot never plays on. |

What the tree diff actually shows: every reasoning file in v3 carries an explicit
*"v3.0 bump — no logic change in this file"* header. The deltas are
`data/candle_feed.py` (+contract test), `market_data.py` rewritten as a store
reader with byte-identical signatures, the candle logger converted to a
consumer, and one condor-alert display fix (main v3.1).

## Part 2 — Distance from the vision, stated plainly

- **Reasoning code in the v3 repo embodying the consensus model: 0%.** The
  classify path, the UNKNOWN gate, and the dispatch are v2's, verbatim.
- **The consensus mechanism itself: ~70% built — off-repo.** The conviction
  integrator running shadow on QQQ-TEST *is* the weighted
  agreement-vs-frame model: leaky per-regime integration, decay resistance
  scaled by banked conviction, single-label emission with
  displacement-by-competitor, restart persistence, and a 14/14 validation
  suite against the 07-09 failure catalog. It is not a v2 artifact — it never
  touched v2's logic; it consumes engine states and emits labels. Discarding
  it with v2 means re-deriving the same math. **Port it; change one thing:**
  its emission law still ends in "below threshold → UNKNOWN." The v3 emission
  law is *always emit argmax + conviction* (hysteresis and displacement kept —
  they are exactly the no-blend/no-chatter requirement).
- **Regime truths: ~50%.** Sweep (v1.1: location + penetration + rejection)
  and trending (v1.2/1.3: strength + direction + non-contradicting structure,
  alignment as corroboration) are definition-complete. Ranging has its
  deal-breaker truth validated (flat value center, arctan-normalized) with
  oscillation confirmation prototyped. Breakout is partial (expansion +
  envelope, momentum-carry drafted, velocity-at-level flagged as the future
  discriminator). Compression is the weakest — currently just a BB-width
  percentile, no discriminating truth against early-ranging.
- **Conviction-bar gating and ROI calibration: 0% — not started.** This is the
  genuinely new build. Nothing in `main.py` or `setup_scorer.py` gates on
  regime conviction directly, and no logging currently captures what is needed
  to calibrate the bars (conviction at signal time, including for signals a
  gate *blocks*).

## Part 3 — The build plan

### Phase 0 — Port the consensus core into v3 (days)
1. Bring `conviction_integrator.py` into `analysis/` with the v3 emission law:
   always emit argmax + conviction; delete the UNKNOWN fallback from emission.
   Keep θ_hold/displacement hysteresis (single-label stability). Keep the
   STALE/gap state and wire it to candle_feed's heartbeat — **the no-trade
   condition for data faults survives; the no-trade condition for indecision
   does not.**
2. Shadow it in-process on QQQ-TEST against the live v1.3 classifier, both
   reading the *shared store* (the observer already consumes `get_cache()`
   unchanged — the v3.0 seam guarantee). Log per tick: both labels, the full
   conviction vector, trigger, stale flag.
3. Session cold-start: warm-start replay from the store's session bars at
   9:30–9:35 (the ORB-formation lockout already blocks entries pre-9:35, which
   conveniently covers the integrator's directional commit time).

### Phase 1 — Finish the regime truths (1–2 weeks, tape-driven)
For each regime, complete the truth table: **hard truths** (definitional
vetoes that make regimes mutually exclusive) + **graded confluence** (evidence
feeding the integrator). Work outstanding, in priority order:
1. **RANGING** — freeze the flat-angle cutoff from multi-day base rates (one
   day clusters everyone at 24–32°; the 20° prior needs the accumulated store
   history), keep oscillation as confirmation, keep the no-R² rule (scatter is
   allowed; only the center must hold).
2. **BREAKOUT_VOLATILE** — formalize the momentum carry (high ADX holds
   evidence through envelope re-entry) and specify its truth against TRENDING:
   breakout = expansion *through* a level; trending = sustained directional
   strength. Velocity sign-behavior at mapped levels is the eventual
   first-class discriminator (accelerate-through vs decelerate-reverse) —
   design now, build after Phase 3.
3. **COMPRESSION** — needs its truths written: contraction *persisting*
   (width percentile falling or floored over N bars) + range-center stability,
   so it stops being "narrow bands right now."
4. **Non-overlap audit** — for every regime pair, name the truth that
   separates them. Replay disagreements between shadow and v1.3 on logged tape
   (extend `tests/replay_classifier.py`) and human-audit a sample of sessions.

**Acceptance for Phase 1:** on ≥ 10 sessions × 29 symbols of store tape, the
integrator's label track has no 15-s chatter, shark-fin chop carries RANGING,
disguised trends never commit RANGING, and every displacement has a nameable
truth behind it.

### Phase 2 — The gate matrix: trade types per regime + provisional bars (days)
Replace the identity-only dispatch with `fires iff regime ∈ permissive AND
C ≥ bar(trade_type)`. Provisional bars encode the binary-vs-nuanced principle
(all numbers are placeholders for Phase 3 to overwrite):

| Trade type | Confluence character | Permissive regimes | Provisional bar |
|---|---|---|---|
| ORB long call/put | Binary (range break, close outside, retest) | BREAKOUT_VOLATILE, TRENDING_*, RANGING, COMPRESSION | **0.40** |
| Sweep reversal | Binary (named zone, penetration, reclaim) | SWEEP_REVERSAL | **0.40** |
| Iron condor (legged) | Nuanced (range character, boundary quality) | RANGING | **0.65** |
| Debit butterfly | Nuanced (GEX pin quality, proximity, quiet tape) | RANGING, COMPRESSION | **0.70** |
| BWB roll | Adjustment, not an entry — stays premium-math-gated | (inherits condor) | n/a |

Setup grading (A/B) remains as the sizing multiplier; the daily-loss halt,
session windows, and ORB lockout are untouched. Directional trades keep low
bars because their factors answer yes/no; premium structures keep high bars
because selling into a disguised trend is the expensive failure and their
factors carry the nuance.

### Phase 3 — Calibrate the bars from ROI (the core empirical campaign, 3–6 weeks of paper)
Your stated method — lower each gate until ROI goes negative — implemented so
it converges fast and never has to *realize* the negative ROI to find it:

1. **Instrument first.** Log at signal time, for EVERY signal (fired *and*
   gate-blocked): trade type, regime, conviction, setup score, GEX context,
   fees estimate, and eventual outcome for fired ones. A gate you can't
   counterfactual is a gate you can't calibrate.
2. **Paper runs the gates wide open.** In paper there is no cost to firing the
   marginal trade — so drop every bar to a floor (~0.20) fleet-wide and let
   all 29 boxes generate the distribution. This *is* the descent, run in
   parallel instead of sequentially.
3. **Bucket, don't cumulate.** Per trade type: bucket **fee-adjusted** ROI by
   conviction (deciles). The gate belongs at the lowest bucket whose marginal
   expectancy is ≥ 0 — not where *cumulative* ROI turns negative, because by
   then a mass of negative-EV trades is already inside the tent. Minimum ~40
   trades per bucket before trusting a crossing (the fleet makes this
   attainable in weeks; single-symbol would take months).
4. **Guard the statistics.** Fee/slippage-adjusted P&L is the only metric
   (the crypto lesson); haircut paper fills for 0DTE spread slippage; split
   the tape so bars are never calibrated on the sessions used to tune regime
   truths; prefer pooled-fleet curves with a per-symbol sanity check (an
   SPX-only crossing is not an AMD crossing).
5. **Live descent, safely.** Go live with each bar one bucket ABOVE its paper
   crossing. Then apply the descent literally, one notch per review window,
   watching the *marginal* (newly-admitted) bucket's realized expectancy —
   raise back on the first significant negative read. The gate converges to
   the crossing from the profitable side.

### Phase 4 — Wire live + keep it calibrated (ongoing)
- Replace the classify path and dispatch gate; delete UNKNOWN from the regime
  enum (grep the fleet tooling — status.py, query.py, alerts — for the
  string). Data-fault no-trade stays, driven by feed heartbeat + integrator
  STALE.
- Deployment discipline unchanged: full files, fresh-clone version reads,
  `__pycache__` purge, never mid-RTH.
- Recalibration cadence: re-run the bucket analysis on a rolling window
  (monthly, or after any regime-truth change — a definition change invalidates
  the conviction distribution beneath the bars).
- End state: every trade type carries an empirically-placed conviction bar in
  every permissive regime, the classifier never abstains, and "no trade" is
  either a data fault or the honest verdict of the bars — never a dead spot.

## Risks worth naming now
1. **Removing UNKNOWN shifts all safety onto the bars.** Until Phase 3
   completes, provisional bars are guesses — keep the fleet in paper through
   the calibration campaign (it already is).
2. **Cold-start labels are noise-labeled by design** (argmax of near-zero
   convictions at 9:31). Harmless only because bars gate trades and the ORB
   lockout covers the commit window — preserve both.
3. **Circularity** is the quiet killer: truths tuned and bars calibrated on
   the same sessions will look beautiful and mean nothing. The split in
   Phase 3.4 is not optional.
4. **Non-stationarity**: a bar placed in a low-VIX month drifts. The Phase 4
   cadence is part of the architecture, not maintenance.
