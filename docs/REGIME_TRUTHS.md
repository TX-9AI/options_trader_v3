# REGIME_TRUTHS.md — Layer 1 (Regime Confluence) definitional truth audit

**v0.2 — 2026-07-11 — Definitional only; all thresholds PRIOR.** Companion to
`analysis/regime_confluence.py` v1.0 (this document's implementation; smoke-verified,
tape-unvalidated).
Written against **v3 HEAD `49d7af8`** (engines + `regime_classifier.py` v1.3) and the
off-repo reference `conviction_integrator.py` v1.0 (`EvidenceAdapter`, built vs
`ef76b4a`/v1.2 — every field it reads was re-verified present at `49d7af8`).

Changelog:
- **v0.2** — RANGING gains a **`room_s` soft-necessary** on `bb_width_pct` (a range
  needs room to oscillate; as the container squeezes, range-ness hands off to
  COMPRESSION on the same width axis). Discriminator matrix + calibration table
  updated. Sync with `regime_confluence.py` v1.0.
- **v0.1** — initial six-regime audit, three-tier factor grammar, discriminator
  matrix, UNKNOWN disposition table.

Scope: **Layer 1 only.** This document defines *what the tape is at this instant*
per regime. It does not smooth, remember, count-over-N, or accumulate — that is
Layer 2 (the conviction integrator). It does not reference strikes, premium,
sizing, fills, or tradability — that is Layer 3. Where a truth *wants* persistence,
it is written in its instantaneous form and the persistence is handed to Layer 2
in a **[→L2]** margin note.

---

## 0. The factor grammar (decisions #3 and #4, resolved)

Every factor is sorted into exactly one of three roles. The per-regime score is:

```
score_R = ( ∏ hard_veto_i ∈ {0,1} )          # definitional gates — any 0 ⇒ regime impossible
        × ( ∏ soft_necessary_j ∈ [0,1] )      # graded necessary conditions (ramps, not cliffs)
        × ( Σ w_k · corroborator_k ),  Σ w_k = 1   # independent compensatory evidence
```

This is the brief's `(∏ vetoes) × (Σ wᵢfᵢ)` **taken literally**, with the middle
term added: factors that are *necessary but graded* live outside the sum as soft
multipliers, so the sum contains only genuinely compensatory evidence. The
adapter's hand-rolled products (`expand_s * outside_s`, `max(align, ramp(adx))`)
are exactly this pattern discovered ad hoc; here it is made explicit.

**Why this shape and not a global product or global sum** (rationale — does NOT
enter runtime code):

- A global **product** makes every factor a quasi-veto; the score sits near 0
  except in perfect windows and spikes rarely. Fed to the leaky integrator, a
  mostly-zero signal reads as *disagreement*, conviction bleeds, and genuine
  regimes fight to commit. It also depresses the evidence ceiling below the
  ~0.85 the Layer-2 τ/θ constants were derived against.
- A global **sum** lets a real veto (flat center in a trend) be out-voted by
  agreeing corroborators — the disguised-trend failure that sells premium into a
  move.
- **Failure-cost asymmetry** decides the lean per regime: directional regimes
  (BREAKOUT, TRENDING) keep corroborators *compensatory* — the expensive error is
  *missing* the move (the 07-09 UNKNOWN disaster). Premium regimes (RANGING,
  COMPRESSION) keep more of their mass in *hard vetoes* — the expensive error is
  *claiming range during a disguised trend*. This asymmetry sorts the factors; it
  is recorded here as design rationale and is **never** a runtime reference to any
  trade type.

**Role legend:** `⛔ HARD VETO` (∈{0,1}) · `◐ SOFT-NECESSARY` (∈[0,1], multiplies) ·
`✚ CORROBORATOR` (∈[0,1], weighted-summed) · `[→L2]` persistence deferred to Layer 2.

**Input vocabulary** (verified at HEAD; these are the only readable fields):
`TrendState`: primary_adx, aligned_timeframes/total_timeframes, overall_direction,
is_bullish/is_bearish · `TrendVote`: momentum {ACCELERATING/DECELERATING/FLAT} ·
`VolatilityState`: atr_current, atr_avg_20, atr_state {EXPANDING/CONTRACTING/STABLE},
bb_width_pct, bb_state {SQUEEZE/EXPANDING/NORMAL}, price_vs_bb {INSIDE/ABOVE_UPPER/
BELOW_LOWER}, is_expanding, is_compressing, price_vs_vwap · `StructureMap`:
structure_sequence {HH_HL/LH_LL/MIXED/NEUTRAL}, in_sr_zone, nearest_sr_distance_pct ·
`LiquidityMap`: recent_sweep, sweep_age_bars, named levels · `LiquiditySweep`:
reclaimed, closes_beyond, rejection_pct, swept_named_level, bars_ago · plus the
Layer-1-internal **flat_angle_deg(closes, atr)** and **midline_crossings(closes)**
computed over the rolling 25-bar window (a property of the current window — legal).

---

## 1. TASK 1 — Per-regime truth audit

### TRENDING_BULL / TRENDING_BEAR  *(directional — corroborators compensatory)*

The two are one definition; `overall_direction` routes the score to one label and
zeroes the other. `_BEAR` flips the sign on every directional read.

| role | factor | field / formula | PRIOR |
|---|---|---|---|
| ⛔ HARD VETO | no contradicting structure | `structure_sequence` ≠ contra (contra = LH_LL for bull, HH_HL for bear) | — |
| ⛔ HARD VETO | direction is not neutral | `overall_direction` ∈ {BULLISH, BEARISH} | — |
| ◐ SOFT-NECESSARY | trend strength | `ramp(primary_adx, ADX_TREND−5, ADX_STRONG_SOLO)` = ramp(20, 35) | 20 / 35 |
| ✚ CORROBORATOR | timeframe alignment | `aligned_timeframes / total_timeframes` | w≈0.6 |
| ✚ CORROBORATOR | momentum accelerating | `momentum == ACCELERATING` (per primary TF) | w≈0.4 |

**Settled hard truths:** structure-contradiction veto (v1.2) and non-neutral
direction. A tape whose swings print LH_LL cannot be a bull trend regardless of ADX.
**Graded:** ADX strength is necessary-but-graded — soft, not a cliff. Alignment is
**corroboration, not a gate** — the v1.3 coverage fix: above `ADX_STRONG_SOLO=35`,
unambiguous strength carries the trend even when alignment momentarily fractures.
Encoded as a corroborator (in the sum), so weak alignment *lowers* the score without
zeroing it — this is precisely what stops the 07-09 clean-breakout-scored-UNKNOWN
failure. **Wrongly excluded by v1.3's boolean form:** marginal-ADX trends with
perfect alignment scored identically to strong-ADX trends; graded ADX fixes this.
**Discriminator vs adjacent regimes:** see matrix — the load-bearing one is the
value-center veto against RANGING (a trend's value migrates; a range's does not),
expressed there as RANGING's flat-angle veto being TRENDING's mirror.

*Note — ADX slope:* rising/falling ADX would strengthen this, but true ADX-slope is
not a HEAD field. `momentum {ACCELERATING/DECELERATING}` is the instantaneous proxy
and is used. A dedicated ADX-slope field is a **proposed engine addition**, not
assumed here. **[→L2]** "ADX has been rising for N ticks" is persistence — the
integrator banks a rising series of TRENDING evidence; Layer 1 only reports
accelerating-*now*.

---

### BREAKOUT_VOLATILE  *(directional — necessary-conjunctive, minimal sum)*

| role | factor | field / formula | PRIOR |
|---|---|---|---|
| ◐ SOFT-NECESSARY | range expanding | `ramp(atr_current/atr_avg_20, 1.0, 1.5)` if `is_expanding` else same ramp(1.1,1.6)×0.6 | 1.0/1.5 |
| ◐ SOFT-NECESSARY | price accepting outside envelope | `1.0 if price_vs_bb≠INSIDE else ramp(primary_adx, 38, 50)` | 38/50 |
| ✚ CORROBORATOR | (reserved) velocity-at-level | *proposed — see below* | — |

Breakout is genuinely **two necessary conditions with almost no corroborators**, so
its score is a soft-necessary product and the sum is (for now) near-empty — the one
place the adapter's "product" form is *correct* and is kept. Expansion answers "is
energy releasing," envelope-acceptance answers "through a level, not just poking."

**Momentum carry (the anchor), and why it is Layer 1 and not Layer 2:** the
envelope factor does **not** hard-zero on a momentary BB re-entry — at clearly-high
ADX (`ramp(38,50)`) an inside-band print still scores. This reads **only current
ADX**: "high ADX *now* means an inside print *now* doesn't contradict breakout." It
is a statement about this tick, so it is legal Layer 1. Remembering that price *was*
outside 3 ticks ago would be memory — illegal; not done. **[→L2]** persistence of
the breakout across a genuine multi-tick re-entry is the integrator's decay
resistance, not ours.

**Discriminator vs TRENDING:** breakout = expansion *through* a level (envelope +
`atr_state=EXPANDING`); trending = sustained strength that is agnostic to expansion
(a trend runs at any vol). **Discriminator vs SWEEP at a level:** acceptance
(`closes_beyond ≥ 2`) is breakout; penetrate-then-reclaim is sweep — the same level,
opposite resolution. **Future first-class discriminator (proposed, Phase-3+):**
velocity sign at the mapped level — accelerate-*through* vs decelerate-*reverse* —
which would separate BREAKOUT from SWEEP on the *approach*, before the reclaim
resolves. Needs an engine velocity field; flagged, not assumed.

---

### RANGING  *(premium — hard veto carries the weight)*

| role | factor | field / formula | PRIOR |
|---|---|---|---|
| ⛔ HARD VETO | flat value center | `flat_angle_deg(w25, atr) < FLAT_ANGLE_CUT_DEG` | 20° |
| ◐ SOFT-NECESSARY | flatness depth | `ramp(CUT − angle, 0, FLAT_ANGLE_SOFT_DEG)` | soft 8° |
| ◐ SOFT-NECESSARY | room to oscillate | `ramp(bb_width_pct, RANGE_ROOM_LO, RANGE_ROOM_HI)` | 0.05 / 0.20 |
| ✚ CORROBORATOR | midline oscillation | `ramp(midline_crossings(w25), 2, 5)`, blended `0.4 + 0.6·osc` | 2/5 |

**The deal-breaker truth (validated):** a trend cannot hold a flat value center —
its value migrates; a range oscillates around a stable local one. `flat_angle_deg`
is instrument-agnostic by the `ATR·√n` normalization (fixed the SPX raw-percent
false-flat, 48%→17%), so one 20° cutoff serves SPX and a $4 name. At/above the cut
the regime is **vetoed to 0.0** no matter how low ADX looks. **Local-center anchor:**
the window's own regression midline — valid *only because the veto has certified it
flat* (session VWAP too strict, trailing mean too loose; in a trend the veto fires
first, so the trailing-mean leak is structurally blocked). **No R²/fit filter** —
shark-fin scatter is expected; only the center must hold. Oscillation is
**confirmation only** and enters as a corroborator: crossing *frequency*
distinguishes rotation (a range) from a pin/drift, not residual balance (which is
near-balanced by construction).

**Room to oscillate (v0.2 — the COMPRESSION handoff):** a range needs room. As the
container squeezes toward zero width, the tape is no longer *oscillating across* a
range — the oscillation is dying into a coil, and range-ness must fade. `room_s`
ramps RANGING down over `bb_width_pct ∈ [0.05, 0.20]`; this is the exact instantaneous
complement of COMPRESSION's `narrow_s` — the **same width axis pushing the two regimes
apart**, RANGING fading as COMPRESSION rises. A normal/wide flat center with active
crossings stays full RANGING; a squeezed flat center hands off. It does **not** require
wide bands (energetic chop at moderate width still ranges) — it only bites at genuine
squeeze. In the transition both score moderately, which is honest; Layer 2 resolves.

**Wrongly excluded by v1.3:** the old `_is_ranging` (ADX<20 + price INSIDE bands)
was too strict to claim energetic mean-reverting chop — the 88% of the 07-09 UNKNOWN
dwell. Elevated ADX and BB pokes are **allowed** here: fin stabs hit the edges by
nature. The angle read is what admits that chop as RANGING. **Honest caveat:** a
single 25-bar window is a noisy estimator — a marginal drift can read 12° on one
window. That is *why Layer 2 exists*: single-window misreads don't persist, ranges
do. Layer 1 reports the honest per-window angle; the impostor separation is
downstream. **[→L2]** "held the flat angle 24–29 bars" (genuine) vs "12–15 bars"
(impostor) is the integrator's slow RANGING τ_up — never a Layer-1 counter.

**Fallback** (bars unavailable): reduced-ceiling quiet-range read (`adx <
ADX_RANGE_THRESHOLD` and `price_vs_bb=INSIDE` and not expanding) → 0.6, so the
regime is not blind. Returns **None** only when the window/ATR are unreadable
(unobservable ≠ contradicted).

---

### COMPRESSION  *(premium — the weakest regime; truths written here)*

**This is the regime the ROADMAP flags as "little more than a BB-width percentile."**
The adapter's current read (`ramp(0.20 − bb_width_pct, 0, 0.15) × quiet`) has **no
flat-center truth and no discriminator against early-RANGING** — its known gap. New
Layer-1 definition:

| role | factor | field / formula | PRIOR |
|---|---|---|---|
| ⛔ HARD VETO | flat value center | `flat_angle_deg(w25, atr) < FLAT_ANGLE_CUT_DEG` | 20° (shared w/ RANGING) |
| ◐ SOFT-NECESSARY | bands narrow | `ramp(BB_WIDTH_COMPRESSION_PCT − bb_width_pct, 0, 0.15)` | 0.20 |
| ◐ SOFT-NECESSARY | not expanding | `1.0 if atr_state∈{CONTRACTING,STABLE} and not is_expanding else 0.0` | — |
| ✚ CORROBORATOR | squeeze state | `1.0 if bb_state == SQUEEZE else 0.0` | w=1.0 |

**The discriminator we owe — COMPRESSION vs early-RANGING:** *both* are flat-center
(so both take the flat-angle veto — this is the fix: compression now shares RANGING's
center truth instead of ignoring it). They separate on **band width regime**:
RANGING oscillates across a flat center at *normal/expanded* width (crossings are its
signature); COMPRESSION is a flat center at *contracted* width with the crossings
*collapsing* toward the midline. In Layer-1 instantaneous terms: low `bb_width_pct` +
`atr_state=CONTRACTING/STABLE` + `bb_state=SQUEEZE` = compression; normal width +
oscillation = ranging. The handoff is **symmetric on the width axis** (v0.2):
COMPRESSION's `narrow_s` rises exactly as RANGING's `room_s` falls, so squeeze moves
score from one to the other rather than lighting both. **Potential-energy read
(instantaneous):** a range *spends* energy — excursions reach the edges and turn
around (crossings, at width); a coil *stores* it — the envelope tightens while
excursions fade (SQUEEZE + collapsing crossings, encoded as the `stored` corroborator
`1 − osc`). Both flat-center; the separator is release-vs-absorb, read at one tick.
A tape can score *both* moderately during the transition — that is honest, and Layer 2
resolves which is committing.

**[→L2] — the "persisting" truth is explicitly NOT here.** The ROADMAP wants
"contraction persisting — width percentile falling or floored *over N bars*." That
"over N bars" is accumulation and is **deferred to the integrator**: Layer 1 reports
narrow-and-flat-*now*; the integrator banking a run of high COMPRESSION ticks *is*
"it has been coiling." Writing an N-bar counter here would double-smooth the system.
**Discriminator vs BREAKOUT:** exact opposite on the width axis — `is_expanding` /
`atr_state=EXPANDING` zeroes the not-expanding factor, so a tape cannot score
COMPRESSION and BREAKOUT together.

---

### SWEEP_REVERSAL  *(event overlay — hard-veto triple × age-decay)*

| role | factor | field / formula | PRIOR |
|---|---|---|---|
| ⛔ HARD VETO | LOCATION — named zone swept | `recent_sweep.swept_named_level` non-empty | — |
| ⛔ HARD VETO | REJECTION — reclaimed | `recent_sweep.reclaimed == True` | — |
| ⛔ HARD VETO | non-acceptance | `recent_sweep.closes_beyond < SWEEP_ACCEPT_CLOSES` | <2 |
| ◐ SOFT-NECESSARY | rejection strength | `ramp(rejection_pct, 0.002, 0.008)` | 0.002/0.008 |
| ◐ SOFT-NECESSARY | age-decay | `0.5 ** (sweep_age_bars / SWEEP_HALFLIFE_BARS)` | half-life 3 bars |

**The sweep truth triple (definitional, closed — v1.1):** LOCATION + PENETRATION +
REJECTION. All three are hard vetoes no other regime touches — its specialism made
literal. **Acceptance = breakout, not sweep:** `closes_beyond ≥ 2` fails the
non-acceptance veto, which is the exact BREAKOUT-at-a-level discriminator. **Age
decay is the key event-property:** a sweep without follow-through must *evaporate* —
the `0.5**(age/3bars)` half-life is what lets a rising BREAKOUT *displace* a stale
sweep instead of the sweep lingering (the AMZN failure). This decay reads
`sweep_age_bars` (a current field), so it is instantaneous, not memory. **[→L2]** the
*displacement* of a stale sweep by a competitor is the integrator's δ-margin
mechanic; Layer 1 only decays the evidence.

---

## 2. Discriminator matrix (mutual exclusivity from truths, not cascade order)

The system reduces to **three organizing binary truths** stacked with graded
evidence. Read each column for the axis that separates the pair.

| axis (normalized) | TREND_BULL | TREND_BEAR | RANGING | COMPRESSION | BREAKOUT | SWEEP |
|---|---|---|---|---|---|---|
| **value center** (flat_angle) | migrating ⛔ | migrating ⛔ | **flat ⛔** | **flat ⛔** | migrating | — |
| **band width** (bb_width_pct/state) | — | — | **needs room ◐** | **contracting ◐** | **expanding ◐** | — |
| **level resolution** (closes_beyond/reclaim) | — | — | — | — | **accept-through ◐** | **reclaim ⛔** |
| ADX strength | ≥mid ◐ | ≥mid ◐ | any (allowed) | low | ≥high ◐ | — |
| direction | bull ⛔ | bear ⛔ | — | — | (breakout dir) | (reject dir) |
| oscillation crossings | low | low | **high ✚** | collapsing | — | — |
| named-zone location | — | — | — | — | — | **present ⛔** |

**The three cleaving truths:**
1. **value center migrating vs flat** — cleaves {TRENDING, BREAKOUT} from {RANGING,
   COMPRESSION} before any other factor speaks. The master discriminator.
2. **band width contracting vs expanding** — within flat-center, splits COMPRESSION
   (contracting) from RANGING (normal); within migrating, marks BREAKOUT (expanding).
3. **acceptance vs rejection at a level** — within migrating-at-a-level, splits
   BREAKOUT (accept-through) from SWEEP (penetrate-reclaim).

Everything else is graded confluence stacked on top. **A signal's role is
regime-relative and that is the consensus mechanic:** high ADX lifts TRENDING/
BREAKOUT and is *allowed* under RANGING; width-contraction lifts COMPRESSION and
zeroes BREAKOUT. A tape where ADX rises *and* width contracts genuinely scores two
regimes moderately and *should* — the ambiguity is honest, and Layer 2 sorts it over
time. Mutual exclusivity is enforced by opposing truths, never by priority order.

---

## 3. TASK 2 — UNKNOWN disposition table

UNKNOWN is eliminated **as a regime**. Every population it absorbed gets an explicit
destination. Layer 1's obligation: **always emit scores, never abstain** (the adapter
already satisfies this — it returns per-regime floats/None, never a global UNKNOWN).
The UNKNOWN *emission* deletion is Layer 2's port task (ROADMAP Phase 0), not Layer 1.

| UNKNOWN population (07-09 autopsy) | share | new destination | mechanism |
|---|---|---|---|
| Breakout flicker (BB re-entry at ADX 43–50) | 12% (≤30s) | **BREAKOUT** score stays >0 | momentum carry: `outside_s=ramp(adx,38,50)` doesn't zero on inside print |
| Energetic shark-fin chop (flat VWAP, high-vol fin stabs) | 88% (long dwell) | **RANGING** score dominant | flat-angle veto passes + crossings corroborate; elevated ADX/pokes allowed |
| Genuine regime-to-regime transition | — | **both** regimes score moderately | honest low/split scores; Layer 2 displacement resolves, no UNKNOWN interlude |
| Pre-open / insufficient bars | — | RANGING **None** (fallback if partial) | `None` = unobservable; integrator stale-decays, ORB lockout covers commit window |
| Engine-state fault (stale feed / restart gap) | — | **DATA-FAULT state** (not a regime) | owned by `candle_feed` heartbeat + integrator STALE; the only surviving hard block |

**`UNKNOWN` string-scrub checklist** (Phase 4 — grep the fleet before enum deletion):
`analysis/regime_classifier.py` (enum + `_classify` fallback) · `main.py` (dispatch
no-trade gate ~L469–560) · `status.py` · `query.py` · `eod_summary.py` ·
`notifications/` (regime-change alerts) · `conviction_integrator.py` emission law
(§2 — the `→ UNKNOWN` fallback becomes always-argmax) · any `data/shadow/` JSONL
readers keyed on the label. Data-fault no-trade **survives**; indecision no-trade
does not.

---

## 4. Open calibration knobs (all PRIOR — fit from candle-logger tape, never one day)

| knob | current PRIOR | calibration plan |
|---|---|---|
| **FLAT_ANGLE_CUT_DEG** | 20° | **top priority.** Sweep 16–26° against labeled range/trend windows from multi-day store tape. One day clusters everyone at 24–32° — needs base rates. |
| FLAT_ANGLE_SOFT_DEG | 8° | joint with the cut, from the same labeled windows |
| crossings ramp | 2 / 5 | rotation-vs-pin frequency on confirmed ranges |
| ADX ramps (trend/breakout) | 20/35, 38/50 | ROC of score vs labeled trend/breakout onset |
| bb_width compression ramp | 0.20 / 0.15 | squeeze base rate; separate early-compression from ranging |
| RANGE_ROOM_LO / _HI | 0.05 / 0.20 | width at which RANGING hands off to COMPRESSION; fit jointly with the compression ramp against the same squeeze base rate |
| sweep rejection ramp | 0.002 / 0.008 | confirmed-sweep rejection_pct distribution |
| sweep half-life | 3 bars | follow-through-vs-evaporation survival curve |
| corroborator weights `w_k` | see tables | **Phase 1 tape** — per-regime, one factor at a time |

**Circularity guard:** truths tuned and weights calibrated on the *same* sessions
look beautiful and mean nothing. Split the tape — the sessions used to set these
thresholds must not be the sessions used to validate the scorer.

---

## 5. Provenance & boundary ledger

- **Read from HEAD `49d7af8`:** all engine fields, enums, config thresholds, v1.3
  classifier logic. Every field cited above verified present.
- **Reference (off-repo):** `conviction_integrator.py` v1.0 `EvidenceAdapter` — the
  Layer-1 prototype this document audits and re-sorts into the three-tier grammar.
  Built vs `ef76b4a`/v1.2; field-compatible with HEAD (re-verified).
- **Layer boundary held:** no factor references a trade, strike, premium, size, or
  ROI (Layer 3). No factor remembers, counts-over-N, or accumulates (Layer 2) —
  every persistence-flavored truth carries a **[→L2]** deferral. Failure-cost
  asymmetry is design rationale only; it is absent from runtime.
- **Not yet validated on real tape:** the entire Layer-1 factor design. Synthetic
  sims validated the *integrator*, never the *adapter*. Monday's shadow run is the
  first real-tape test — expect PRIOR knobs to move.

**Open decisions carried forward (none block the build):**
- ADX-slope and velocity-at-level are **proposed engine additions**, used via
  proxies (`momentum`, and nothing yet) until built — not assumed present.
- GRIND / VOLATILE_RANGE seventh-regime candidates remain **shelved** (insufficient
  non-chop tape); resume conditions logged separately.

---
*Next deliverable: `analysis/regime_confluence.py` v1.0 — the standalone module
implementing this document (adapter lifted from `conviction_integrator.py`, re-sorted
to the three-tier grammar, breakdown/audit dict added, guarded imports, no side
effects). Then the Layer-1 validation plan for Monday's shadow tape.*
