# The Pitchfork Overlay — Design White Paper
### options_trader v4.0 milestone · drafted 2026-07-23 · §4.1 corrected 2026-08-01 (PF.1) · §5.3(b) corrected 2026-08-03 (AW), amended same day — the proposed fix measured WORSE
*Revision 2026-08-01 — §7 correction (application #2's target was removed on
07-28), §7.3 A2 note promoted to a live hypothesis, and a four-phase build split
added as §13. The design is unchanged; what changed is the schedule and one
stale row.*

---

## 1. Thesis

Every level this system currently trades against is **horizontal or static**:
Bollinger bands, VWAP, named liquidity pools, ORB range boundaries, fixed
percentage stops. Markets do not move horizontally. A trend is a *sloped
channel*, and the system has no object that represents one.

The pitchfork overlay introduces that object: a persistent, deterministically
placed, sloped support/resistance channel that lives until the structure that
created it breaks. It is not an indicator that recomputes every bar — it is a
**stateful geometric assertion about the tape** that either survives or is
invalidated.

**One line:** the pitchfork gives the system a way to say *"price is trading
inside this channel, sloping this way, and here is where its walls are right
now."*

---

## 2. Why this, why now

Three concrete failures in the current system motivate it, all documented:

**Bollinger describes where price has been, not where it is.** After a
directional move the bands stay stretched while price coils tightly inside
them. Observed 2026-07-23 on SPX: a −1.45% trend day, then a ~17-point
consolidation from 14:00 onward sitting inside a far wider envelope.
Band-anchored condor strikes in that state are far OTM and cheap — the exact
opposite of the premium-rich entry the design wants.

**VWAP is structurally dead on SPX.** The 2026-07-17 zero-volume guard sets
`vwap = 0.0 / price_vs_vwap = "NONE"` because SPX cash reports `volume = 0` on
every DXFeed bar. Any VWAP-anchored logic silently has no reference on one of
the two ALWAYS_ON boxes. **A pitchfork needs only price — never volume.** It
works identically on SPX and on AVGO, with no per-symbol special case.

**Stops are premium-relative, not structural.** `CONDOR_STOP_LOSS_PCT = 0.25`
on a median $0.70 credit is a 17.6¢ move — inside the bid/ask noise band on a
0DTE spread. The forensic finding was unambiguous: essentially every stopped
condor leg was *green first*, peaking at a median +24% before round-tripping
into the stop. A stop placed at a structural level rather than a percentage of
premium is the correct answer to that class of failure.

---

## 3. Geometry

### 3.1 Construction

Three pivots, alternating in direction:

| Pivot | Bullish fork | Bearish fork |
|---|---|---|
| **P0** (handle origin) | swing low | swing high |
| **P1** | swing high | swing low |
| **P2** | swing low, `> P0` | swing high, `< P0` |

- **M** = midpoint of the segment `P1→P2`
- **Median Line (ML)** = the ray from `P0` through `M`, extended forward
- **Upper Median Line (UML)** = parallel to ML, through `P1` (bullish) / `P2` (bearish)
- **Lower Median Line (LML)** = parallel to ML, through `P2` (bullish) / `P1` (bearish)

All three rails share one slope. A rail's price at any future time is therefore
a trivial evaluation:

```
rail_price(t) = anchor_price + slope * (t - anchor_time)
```

This matters for cost: the fork is **placed once**, and thereafter each tick
only evaluates three linear functions. There is no rolling window, no
recomputation, no lookback cost.

### 3.2 Variant selection

| Variant | P0 treatment | Effect |
|---|---|---|
| Standard Andrews | P0 as-is | Steep when `P0→P1` is a large move |
| Schiff | P0 raised/lowered to midpoint *price* of `P0,P1` | Flattens slope |
| Modified Schiff | P0 moved to midpoint of `P0,P1` in *both* time and price | Most stable |

**Default: Modified Schiff.** Standard Andrews produces pathologically steep
medians when `P0` is distant, and a steep median runs away from price — useless
for the condor strike-anchoring use case, which needs a channel that brackets
*current* price.

All three variants should be **computed and logged in parallel during the
shadow stage**, and the choice settled by measurement rather than by this
document. Cost is negligible — three sets of three linear functions.

---

## 4. Anchor selection — the deterministic rule

This is the entire ballgame. Pitchforks are notoriously subjective; a
discretionary trader eyeballs "obvious" pivots. If anchor selection requires
judgment, the overlay is unbacktestable and worthless. **Placement must be a
pure function of the tape.**

### 4.1 Source

> **CORRECTED 2026-08-01 during PF.1. The paragraph below was wrong, and it is
> left visible rather than quietly rewritten.** It claimed `LiquidityMapper`
> already computes swing pivots and that the overlay would consume them. Neither
> is true at HEAD. LiquidityMapper computes equal-high/low **price clusters**
> (`_find_pools`), sweeps and named session levels — there is no fractal pivot in
> it. The real implementation is `utils.math_utils.find_swing_highs/lows`,
> consumed by **StructureAnalyzer**. A price cluster and a fractal pivot are
> different objects; anchoring on the wrong one would have produced a different
> overlay than this document specifies.
>
> **The overlay therefore owns its own pivot definition, in `analysis/pitchfork.py`.**
> Three reasons: (1) `find_swing_highs` feeds StructureAnalyzer →
> `structure_sequence` → a HARD VETO in `_trending`, so putting anchor evolution
> there makes every PF.2/PF.3 tweak a diff against the live trading path — a
> definition this module owns can change freely and be deleted if the overlay
> does not earn its keep; (2) L2.6 protects entry *behaviour*, and a weight-0
> object is outside it while editing a helper the veto reads is arguably inside;
> (3) it would be a different definition regardless — this document requires a
> **fixed `k`**, whereas `_find_swings` uses `lb = min(SWING_LOOKBACK,
> len(highs)//4)`, deriving fractal order from frame length, so anchors would
> shift as the frame grows. That is §4.4's failure mode through another door.
>
> **Defect found in the shared helper and filed, not fixed:**
> `find_swing_highs` tests `prices[i] == max(window)` — float equality — so on
> equal highs it emits **every tied bar** as a pivot, destroying the alternation a
> P0/P1/P2 triple depends on. It affects StructureAnalyzer's swing sets today, so
> fixing it moves `structure_sequence` → TRENDING's veto → what gets traded. The
> fix belongs post-freeze. `tests/test_pitchfork_construct.py` carries a
> reproduction.
>
> **Attribution risk this creates:** if the fork uses different pivots, a credit
> improvement at PF.3 could come from the pivots rather than the geometry.
> Mitigated as §3.2 handles the variants — log **both** pivot sets in parallel
> during shadow and record which triple each selects, so PF.3 attributes with
> data. `pitchfork.pivots_shared()` exists for that comparison and for nothing
> else.

*Superseded original:* `LiquidityMapper` already computes swing pivots. The
overlay consumes those — it does **not** introduce a second, competing
definition of a swing.

A swing high at bar `i` on timeframe `T` is confirmed when
`high[i] > high[i-k .. i-1]` and `high[i] > high[i+1 .. i+k]`, for fractal order
`k`. Swing lows mirror this.

### 4.2 Anchor timeframes

Two forks per symbol, both persistent, coexisting:

| Fork | Bars | `k` | Structure captured |
|---|---|---|---|
| **Daily** | 1d | 2 | Multi-week |
| **Hourly** | 1h | 3 | Multi-day |

The 5m and 1m frames are **execution** timeframes and are deliberately excluded
— they are too noisy to anchor a persistent object, and a fork that re-anchors
constantly is just a lagging indicator wearing a costume.

### 4.3 Qualification filters

A pivot triple `(P0, P1, P2)` becomes a fork only if **all** hold:

1. **Significance** — `|P1 − P0| ≥ S × ATR(T)` and `|P2 − P1| ≥ S × ATR(T)`.
   Start `S = 1.0`.
2. **Separation** — consecutive pivots at least `2k+1` bars apart, guaranteeing
   non-overlapping fractal windows.
3. **Structural validity** — bullish requires `P2 > P0`; bearish requires
   `P2 < P0`. A violated leg is not a directional structure and gets no fork.
4. **Recency** — `P2`'s confirmation is within `R` bars of now. Start `R = 40`
   on the anchor timeframe. Older structure is stale.
5. **Uniqueness** — the three most recent *confirmed, alternating* pivots
   satisfying 1–4. No search, no optimization, no "best fit."

### 4.4 The confirmation-lag rule — non-negotiable

**A fork is born at `timestamp(P2) + k bars`, never at `timestamp(P2)`.**

A swing low is not knowable until `k` bars after it prints. Any backtest that
places a fork at the pivot's own timestamp is using information that did not
exist, and every result it produces is fiction. This single rule is the
difference between a validated overlay and an elaborate way to fool ourselves.

It also has a live consequence: forks lag structure by `k` bars by construction.
On the hourly fork with `k=3`, that is a three-hour lag. This is a *feature* —
it is what prevents re-anchoring on noise — but it must be stated plainly so
nobody later "optimizes" it away.

**Dependency:** the offline replay is HTF-starved (defect S — the rolling-window
bookmark, still unbuilt). Pitchfork validation on replay tape requires that
bookmark to exist first, or daily/hourly pivots will be unavailable in
backtest for the same reason TRENDING under-reports today.

---

## 5. Lifecycle

### 5.1 Birth

At `P2` confirmation, if all qualification filters pass and no active fork
exists for that `(symbol, timeframe)`.

### 5.2 Persistence

The fork **holds until invalidated**. It is explicitly *not* recomputed each
bar, each tick, or each session. Overnight persistence is expected and correct —
a daily fork should survive weeks.

**Crucially: tagging the median or either tine is NOT invalidation.** Those are
the *tradeable events* the whole overlay exists to produce. A fork that dies
when price touches it has inverted its own purpose.

### 5.3 Invalidation — four conditions

**(a) Structural break — P0 violation.**
A close beyond `P0` in the invalidating direction (bullish fork: close below
`P0.price`). The leg that defined the fork is gone; so is the fork. Strongest
and cleanest condition.

**(b) Adverse tine break.**

> **CORRECTED 2026-08-03. The rule below cannot work as written for a sloped
> object, and the original is left visible rather than quietly rewritten.**
> Measured on 29 symbols of real hourly tape: **24 of 27 invalidations (88.9%)
> were this condition** against 3 structural, with a median fork life of **five
> hourly bars** — under one session, where §5.2 expects a persistent object to
> survive far longer.
>
> A sensitivity sweep over `N ∈ {2,3,4,6}` × `D ∈ {0.25,0.5,1.0}` **never brought
> adverse-tine below 50% of deaths** (88.9% → 56.5% at the loosest corner) while
> deaths barely moved (27 → 23). A magnitude problem collapses when the threshold
> loosens; this asymptotes. So the **form** is wrong, not the numbers.
>
> **Two mechanisms, the second dominant:**
>
> 1. *It is time-dependent.* All three rails share the fork's slope, so a bullish
>    fork's **lower** rail rises. Price need not weaken to end up beyond it — it
>    only has to stand still. Demonstrated on a stationary fixture: the written
>    form invalidated after **43 bars of perfectly flat price**, zero adverse
>    movement.
> 2. *Counting closes is noise-sensitive, and this is what produces the 88.9%.*
>    A five-bar median life is far faster than mechanism 1 alone can explain. Two
>    consecutive hourly closes 0.25 ATR beyond a rail is an ordinary retracement,
>    not a structural event — and a bigger `N` still counts the same kind of thing.
>
> **The replacement asks a different question.** As written the condition asks
> *"is price beyond the rail?"*. For a persistent object it should ask *"has price
> **established itself** beyond the rail?"* — and the fork already owns the right
> primitive, being anchored on fractal pivots. **Invalidate when a CONFIRMED PIVOT
> forms beyond the counter-trend tine**, judged against the rail at the *pivot's
> own index*. Same `_pivots` machinery, one lineage, and it inherits §4.4's
> confirmation lag instead of fighting it. It addresses both mechanisms: a pivot
> requires the excursion to have structure, and judging at the pivot's index
> removes the time-dependence.
>
> Corroborating: the 3 structural deaths are rare precisely because **P0 violation
> is already pivot-anchored**. The one condition tied to structure rather than to
> a moving line is the one that behaves.
>
> **AMENDED SAME DAY — THE PIVOT REPLACEMENT WAS MEASURED AND IT IS WORSE.**
> Best adverse-share over the same grid: **CLOSES 56.5%, PIVOT 72.0%.** The
> replacement proposed above is not supported by the tape and is recorded here as
> failed rather than quietly kept.
>
> *Why it failed, and it was foreseeable:* **a k=3 fractal pivot is not a
> structural filter.** It is a local extremum over a seven-bar window, and an
> ordinary pullback produces one every few bars. The claim that "a pivot requires
> the excursion to have structure" was wrong — it requires a local low, which is
> nearly free.
>
> **WHAT THE TWO FAILURES TOGETHER POINT AT.** Both attempts to fix the KILL RULE
> failed, while the same tape shows **22 ACCELERATION events on 33 births** —
> price exceeding the *trend*-side tine — alongside 56-89% adverse deaths on the
> *counter* side. **Price is leaving the channel on both sides, routinely.** No
> invalidation rule can look good if the fork is not describing the price envelope
> in the first place. That makes this a **geometry** question, not a threshold
> one, and it lands on **§12 open question 2 (variant)** — which §3.2 itself flags
> as chosen "on reasoning, not evidence".
>
> Measured on a trending fixture: **andrews slope +0.70/bar, channel width 29.6;
> modified_schiff +0.26 and 23.5; schiff +0.17 and 22.1.** Andrews is both STEEPER
> and WIDER — the shape that would contain price escaping on both sides.
> `pitchfork_prior_sweep` v1.2 tests that rather than assuming it, holding N/D at
> the paper's own values so the variant is the only thing changing, and reporting
> ACCELERATION PER FORK since "channel too narrow" is the hypothesis and
> acceleration is its direct symptom.
>
> **Nothing is switched on the strength of this.** §5.3(b) as written remains the
> default; the pivot form stays available and OFF; the variant question is open.
>
> Implemented as `adverse_mode="pivot"` in `analysis/pitchfork_lifecycle.py`
> v1.2, **shipping OFF** so both forms stay measurable side by side. Switching the
> default is a separate, deliberate act — and per **AW** the hourly fork is off
> the critical path, so there is no reason to rush it.

*Superseded original:* `N` consecutive anchor-timeframe closes beyond the
**counter-trend** tine by `≥ D × ATR`. Start `N = 2`, `D = 0.25`.

> **Asymmetry, deliberate:** breaking the *trend-side* tine is **acceleration,
> not invalidation** — this is Andrews' own teaching and it is correct. A
> bullish fork whose price closes above the UML is not wrong; it is
> understating the move. Flag it, optionally trigger a re-anchor to a steeper
> fork, but **do not kill the fork on strength.**

**(c) Supersession.**
A newer qualifying triple forms on the same timeframe with a more recent `P2`
**and** materially different geometry — slope differing by `> X%` or median
displaced by `> Y × ATR`. The material-difference guard exists to prevent
churn; without it, every marginal new pivot would re-anchor.

**(d) Staleness (optional, measure before enabling).**
No rail interaction within `Z × ATR` for `W` bars. A fork price has ignored for
a month is describing structure that no longer governs. Ship this **off**, and
turn it on only if the shadow data shows stale forks polluting the signal.

---

## 6. Multi-fork resolution

- **At most one active fork per `(symbol, anchor timeframe)`.**
- Daily and hourly forks coexist and may legitimately disagree.
- **Rail strength** = `f(timeframe rank, touch count, confluence)`.
- **Confluence:** when a daily rail sits within `C × ATR` of an hourly rail,
  they form a composite zone with boosted strength. This is the highest-value
  signal the overlay produces and is the natural analogue of a multi-touch
  horizontal pool.
- **Precedence:** higher timeframe governs *zone strength*; lower timeframe
  governs *entry timing*.

Forks fold into `LiquidityMapper` as **sloped zones** alongside its existing
horizontal pools — not as a separate module. A consumer asking "what structure
is near price?" should get one answer covering both kinds.

---

## 7. Applications

The question was which parts of the system benefit. The honest answer is
*most of them*, which is itself the argument for the v4.0 designation.

### 7.1 Entry

| # | Consumer | Application |
|---|---|---|
| 1 | **Iron condor strike anchoring** | Sell the call at/outside UML, the put at/outside LML. Mutually exclusive by construction (price cannot be at both rails). Replaces `_select_by_band`'s BB anchor with a channel that tracks the live structure. **Works on SPX where VWAP cannot.** |
| 2 | **Continuation pullback rail** | ⚠️ **TARGET MOVED — see the correction note below §7.4.** The ML remains the structural version of a pullback reference, but the constant this row named is gone. |
| 3 | **Sweep reversal** | A sweep *into* a rail is materially higher-probability than a sweep into open air. Adds a proximity dimension the strategy currently lacks. |
| 4 | **ORB retest quality** | A retest occurring *at* a rail is a genuine structural quality signal — a strong candidate for the real `orb_quality` the deleted function only claimed to measure. Would extend the A/B grade beyond liquidity-in-path without reintroducing regime. |
| 5 | **Rejection fade** (future trade) | This trade wants "a level rejected multiple times on the HTF." A rail with a touch count **is** that object, delivered directly. |
| 6 | **Butterfly center strike** | GEX pin confluence with the ML gives a two-source pin target. |

### 7.2 Exit and management

| # | Consumer | Application |
|---|---|---|
| 7 | **Structural stops** | Stop beyond a rail rather than a fixed % of premium. Directly addresses the finding that a 25% stop on a $0.70 credit is 17.6¢ — inside the noise. |
| 8 | **Targets** | The opposite tine is a natural, structurally-derived target. |
| 9 | **Sloped trailing** | FVG trails are horizontal. A trail that *slopes with the median* tightens naturally as a trend ages — strictly better geometry for the continuation runner and ORB runners. |
| 10 | **Continuation exhaustion** | Currently ATR-extension from `bb_middle`. Distance beyond the UML is the structural version, normalized by channel width rather than raw ATR. |
| 11 | **Condor roll trigger** | "Tested" becomes structural — price reached that side's rail — rather than premium-derived. |

### 7.3 Scoring and regime

| # | Consumer | Application |
|---|---|---|
| 12 | **`setup_scorer`** | New dimension: rail proximity × rail strength. The natural home for the structural quality the scorer has never measured. |
| 13 | **L1 `regime_confluence`** | Rail-relative position as a **corroborator**. Price riding the UML corroborates trending; price oscillating between tines corroborates ranging. |
| 14 | **L2 conviction** | Rail strength as an evidence weight. |
| 15 | **Channel width as volatility** | `|UML − LML|` is a structural volatility measure that does not lag the way a 20-period BB does — plausibly a better COMPRESSION input. |

> **Note on A2.** The daily and hourly forks can legitimately slope in opposite
> directions. That is not a contradiction to be resolved — it is precisely the
> "each horizon carries its own weight" architecture already adopted, expressed
> geometrically. The overlay may therefore give the A2 cross-horizon
> co-occurrence residual a *structural* explanation rather than a statistical
> one.

### 7.4 Risk

| # | Consumer | Application |
|---|---|---|
| 16 | **Position sizing** | A tighter *structural* stop means more contracts for the same dollar risk. Sizing improves as a downstream consequence of better stop placement. |
| 17 | **`LiquidityMapper`** | Sloped zones become first-class objects alongside horizontal pools. |

> ### ⚠️ Correction — application #2's target no longer exists (added 2026-08-01)
>
> This paper was drafted 2026-07-23. On **2026-07-28** the `v-fvg-pullback`
> rewrite replaced continuation's BB-midline entry trigger with a **1-minute wick
> tagging an unfilled 5-minute FVG**. `CONTINUATION_MIDLINE_ATR` and
> `CONTINUATION_MAX_PULLBACK_R` are now **orphaned constants**, referenced only
> in comments describing their own removal (`continuation_strategy.py:10,157`).
>
> The application is not dead — a sloped pullback reference is still the right
> idea — but it is no longer a drop-in replacement for a named constant, and the
> head-to-head has no current baseline to measure against. It must be re-derived
> against the FVG trigger before it can be ranked.
>
> **The general lesson, which matters more than this one row:** §7 enumerates 17
> consumers against a codebase that moves weekly. **Re-read §7 against HEAD
> before committing to any consumer order.** A replacement target that has
> already been replaced produces a head-to-head with nothing on the other side.

### 7.5 What the overlay must NOT do

- **It must not define regime.** Regime classification stays with L1/L2. The
  fork corroborates; it never labels. (Prior architectural decision, preserved.)
- **It must not gate anything in v1.** Ships at weight 0.
- **It must not be placed by the vision API.** Non-deterministic,
  un-backtestable, opaque. The API's only legitimate role is *offline
  anchor-quality validation* — a sanity check on whether the deterministic rule
  picks pivots a human would recognize.

---

## 8. Architectural note — the second stateful object

The engines are currently **stateless pure functions**: `trend_engine.analyze(dataframes)`
returns a `TrendState` derived entirely from its inputs. The pitchfork breaks
that pattern. It is the second persistent-state object in the system, after the
L2 conviction integrator's book.

It therefore inherits the same requirements: per-box JSON persistence
(`data/pitchfork_state.json`), warm-load at boot, and an explicit answer for a
missing or corrupt state file.

**That answer is unusually clean here.** Because anchor selection is
deterministic, **fork state is fully reconstructible from tape.** Persistence is
a startup optimization, not a correctness requirement — unlike the integrator's
book, which is path-dependent and genuinely lossy if discarded. A box that loses
its pitchfork state rebuilds identical forks from history. This is a strong
argument for keeping anchor selection deterministic even if a heuristic tweak
later looks tempting.

---

## 9. Measurement plan

Ships at **weight 0**. Logs everything, changes nothing.

**Shadow instrumentation** (per tick, per active fork): fork id, timeframe,
variant, slope, the three rail prices, distance from price to each rail in ATR,
touch events, invalidation events with reason.

**Head-to-head, pre-registered.** For each consumer, the comparison must be
specified *before* the data is collected:

| Consumer | Metric | Comparison |
|---|---|---|
| Condor strikes | credit collected at entry; stop-out rate | rail-anchored vs BB-anchored, same tape |
| Continuation | pullback-entry hit rate; MFE | ML vs `bb_middle` |
| Stops | stop distance; stop-out rate; round-trip rate | structural vs fixed-% |

**The condor case is the one to prove first.** It is the most measurable: strike
placement produces a *credit*, a single number directly comparable against the
BB-anchored version on identical tape. No attribution problem, no confounds.

**Vehicle:** the QQQ twin — production QQQ on the current engine versus a
pitchfork-enabled twin, same execution data, one variable.

---

## 10. Risks and honest limitations

1. **Determinism is the whole bet.** If the anchor rule needs per-symbol tuning
   to look sensible, the overlay has failed and should be abandoned rather than
   patched. Watch for this specifically.
2. **Look-ahead is the easiest way to fake success.** §4.4 exists because this
   failure mode is silent and produces beautiful backtests.
3. **Parameter surface.** `k, S, R, N, D, X, Y, Z, W, C` — ten knobs. Every one
   is an overfitting opportunity. **Pre-register starting values, validate on
   held-out tape, and resist tuning on the same data used to measure.**
4. **HTF feed dependency.** Anchors come from daily/hourly bars on the isolated
   feed. Replay validation additionally blocks on defect S.
5. **Confirmation lag is real.** A three-hour lag on the hourly fork means the
   overlay is structurally late by design. Acceptable for context; disqualifying
   for execution timing.
6. **Consumer sprawl.** Seventeen applications are listed above. Building more
   than one before any is proven would be the same mistake as shipping four
   engine changes into a frozen baseline window. **Prove the condor case, then
   expand.**

---

## 11. Build sequence

| Phase | Deliverable | Gate |
|---|---|---|
| **0** | Pivot extraction + fork construction, offline on the tester. All three variants. | Deterministic placement reproduces on repeated runs over identical tape |
| **1** | Shadow logging on the QQQ twin, weight 0 | A full session of fork lifecycle events with no engine impact |
| **2** | **First consumer: condor strike anchoring**, measured head-to-head | Credit collected beats BB-anchored on held-out tape |
| **3** | Continuation ML rail; structural stops and targets | Each measured independently |
| **4** | Scoring dimensions (`setup_scorer`, L1 corroborator, L2 weight) | Post-freeze, post-L2.4 calibration |

**v4.0 is tagged when at least two consumers are independently proven** — not
when the overlay merely exists. The version number should mark validated
capability, not new code.

---

## 12. Open questions for the build

1. **`k` per timeframe** — is 2 (daily) / 3 (hourly) right, or should `k` be
   derived from realized volatility rather than fixed?
2. **Variant** — Modified Schiff is the proposed default on reasoning, not
   evidence. The shadow stage decides.
3. **Touch definition** — within `C × ATR` of a rail? A close beyond and back?
   This determines the touch-count attribute that the rejection-fade trade
   depends on.
4. **Warm-up** — how much history does a symbol need before its first fork is
   trustworthy?
5. **Sequencing against the freeze** — the overlay is queued behind the L2.6
   baseline freeze and built in a git fork. That ordering should not change
   because this document is exciting.


---

## APPENDIX — migrated from the root README (2026-07-28)

<!-- ================= was: README.md § PLANNED — Pitchfork sloped S/R ================= -->

# 🔱 PLANNED — Pitchfork sloped S/R (designed, NOT built, gated on Layer 2)

**Status: design-complete, deliberately unbuilt. Do not deploy before Layer 2 is ready.**
This section is the build brief so the next hands (or the next thread) inherit the full
requirement, not a hunch.

#### What it is

An Andrews-style **median-line pitchfork** used as *sloped* support/resistance — the tilted
cousin of the Bollinger Band (BB is `mean ± σ` around a **horizontal** MA; a pitchfork is the
median line ± tines around a **sloped** axis anchored to three swing pivots). It is folded
**into `LiquidityMapper` as a long-lived sloped-zone object**, not a separate module — because
an S/R level and a liquidity pool are frequently the *same* price described twice, and unifying
them lets one zone carry both its S/R character and its liquidity character.

#### Hard requirements (these are the spec, not suggestions)

- **HTF-anchored.** Pivots come from **daily/hourly** swings, computed on HTF data — never by
  zooming out an intraday calc. An LTF-anchored fork redraws every 20 minutes and means nothing.
- **Placed once, persists until invalidated.** A fork is not re-anchored on every wiggle. It
  stands until price *earns* its death: a **decisive close beyond the outer tine** on the wrong
  side, **or** the anchoring swing structure itself is broken. It is **NOT** invalidated by
  price merely tagging the median or a tine — those are *reactions*, the fork working as
  designed. (Naive implementations kill the fork on first touch; do not.)
- **Deterministic placement off `LiquidityMapper` swing pivots.** A pitchfork is pure
  coordinate geometry once the three pivots are chosen; the only hard problem is *anchor
  selection*, solved with a scoring rule (pick the anchoring price has reacted to most),
  validated offline. **NOT the vision API** — non-deterministic, un-backtestable, opaque in the
  live loop; that violates the "regime shapes the trade, outcomes never feed classification"
  discipline. The API's only legitimate role here is **offline anchor-quality validation**
  (batch-check that the deterministic anchors look sane across many tapes), never the live call.
- **Bands, not lines.** Zones are ranges (the tines are ranges by construction), which composes
  with liquidity pools and the BB/ORB ranges already in use.

#### Where it contributes (ranked by whether it moves P&L)

1. **Conviction scoring** — rail-distance + confluence as new dimensions. A setup entering *at*
   a strong confluence zone is objectively higher-probability. This is the real payoff.
2. **The continuation trade's exit** — structural-level proximity is the **highest-confidence
   exhaustion signal** (a spent move *at a level* beats a spent move in open air). This is the
   `_evaluate_continuation` "ADD structural-level proximity" hook, already flagged in-code.
3. **Exit/target anchors** — the opposite rail is a natural target / trail-tighten point.
4. **NOT regime definition.** A fork tells you *where* a trend pauses, not *whether* you are
   trending. Regime stays ADX/structure/BB-driven. Do not wire it into the classifier.

#### Empirical weight — ship at zero

The pitchfork conviction dimension **ships at weight 0 (shadow)** and is calibrated to
*realized edge* from paper data — exactly as `conviction_integrator` was deployed to observe
before it gated. The weight is a function of `(rail strength × timeframe × confluence)` and is
**allowed to stay 0** if the tape shows no edge. Do not hand-tune a weight; discover it.

#### What we are WAITING FOR — the gate

**Build it when ready; do NOT deploy it until Layer 2 is set.** "Set" means:

1. **Trend labels trusted in production** — the `trend_engine v3.1` fix has weeks of live
   confirmation, not one afternoon.
2. **Conviction weights frozen** — the pitchfork enters as a *new* conviction dimension, and
   that is only measurable if the *existing* Layer-2 weights are a stable baseline. Calibrating
   a new dimension against a moving target is impossible. **This is the real gate.**
3. **A clean baseline logged** — a stretch of untouched production performance to compare the
   pitchfork twin against.

Concretely: **~2-week hands-off window from the 2026-07-XX day-zero** (materially changed
engine: trend v3.1 + VWAP + condor triggers + continuation), *then* the pitchfork build spins
up against a frozen Layer-2.

#### How it gets built (isolation plan)

- An **ironically-named git fork** of this repo (keeps the production fleet's `git pull` safe).
  Pitchfork lives in **additive, separate modules** so upstream merges stay clean.
- Its own **isolated yfinance HTF feed** (cannibalized from v1/v2) — *not* the broker DXFeed
  stream. Adequate because the fork is HTF *context*, never execution; the entry fill still
  happens on real DXFeed price. Keep the two feeds strictly separated — yfinance HTF in, fork
  geometry out, **no yfinance price ever touches an entry/exit decision.**
- Backtest/replay harness **resident on the tester**.
- Proven via a **QQQ twin A/B**: the pitchfork-weighted tester vs a production QQQ twin on the
  current engine — same execution data, one variable (pitchfork conviction).
- **First concrete deliverable when the build starts:** the swing-pivot rule that anchors the
  fork + the invalidation condition. Everything else is geometry that follows from those two.

#### Related future trade (prelude only, not scheduled)

**Rejection-fade** — the near-opposite of continuation. Sell a **premium-rich credit spread**
at a level that has been **firmly rejected**, with conviction **scaling up by HTF rejection
count** (a level rejected three times on the daily >> a one-touch). Continuation trades *with*
momentum into a level expecting breakthrough (debit); rejection-fade sells *against* momentum
into a level expecting it to hold (credit). This trade *wants* the pitchfork/LiquidityMapper
multi-touch HTF zone with a rejection-count attribute — it is the pitchfork's natural partner.

---

---

## 13. Build phasing — added 2026-08-01

The backlog had gated **everything** pitchfork behind L2.6 (Aug 21). That
conflates three activities with completely different risk profiles, and it has a
concrete cost: construction would begin **ten days before live capital**, and
the condor — which item AI names the fork as the instrument to fix — would stay
broken straight through go-live.

Only the last of these needs the freeze.

### 13.1 CONSTRUCT — can start immediately

Geometry engine in a git fork: deterministic anchor selection, three variants
computed in parallel, rails evaluated as `anchor + slope*(t - anchor_time)`.
Consumed by nothing, gating nothing, weight 0.

**Why the freeze does not apply.** L2.6 protects L1/L2/**entry behaviour**. An
object that nothing reads cannot alter behaviour. The freeze is a behavioural
guarantee, not a moratorium on files.

### 13.2 FIT — the blocker cleared 2026-08-01

§4.4's confirmation-lag rule made replay validation depend on **defect S**, the
HTF-starvation bookmark. That dependency is now evidenced rather than assumed:
raising the replay's `--warm-sessions` from 5 to 15 moved TRENDING dom%
**30% → 36%** and TRENDING_BEAR's p90 **0.439 → 0.65**, on identical tape, with
RANGING/COMPRESSION each giving up only 1–2 points. Anchor selection needs
exactly that HTF depth.

Starts after **Aug 5** (L1.CAL.2 confirms it on the rebuilt corpus).

**Caveat carried from that same experiment:** more warm-up made **A2 worse**
(179 → 196 violating ticks). See §13.5.

### 13.3 MEASURE — ~Aug 10, condor strikes only

Head-to-head on the QQQ twin at weight 0, against the chain archive (needs ~2
weeks, which lands about then). Condor first for the reason §9 already gives:
strike placement produces a **credit**, one number, directly comparable on
identical tape with no attribution problem.

**Resist every other consumer until this one has a number.** §12 names consumer
sprawl as a headline risk, and the project has already paid for that mistake
once by shipping four engine changes into a frozen window.

### 13.4 WIRE — post-L2.6 (Aug 21) at the earliest; realistically September

Anything that changes what gets traded. This is what the freeze is for. **v4.0
tags at TWO independently proven consumers**, not when the overlay exists.

### 13.5 A2 — the overlay may be a fourth hypothesis, so do not erase the evidence

§7.3 notes that the daily and hourly forks can legitimately slope in **opposite
directions**, and that this may give the A2 co-occurrence residual a
**structural** explanation rather than a statistical one.

That is now live. The A2 root cause was identified 2026-08-01: **A3 passes with
zero violations because BREAKOUT and COMPRESSION read the same `atr_ratio` in
opposite directions — one measurement, two ends — while TRENDING reads `adx` and
RANGING reads midline `angle`, two unrelated measurements with nothing coupling
them.** The staged fix is A2.1 (characterise) → A2.2 (shared axis, Kaufman
Efficiency Ratio) → A2.3 (log-odds, making the invariant a property rather than
a check).

**The warning this section adds:** if some fraction of the ~196 violating ticks
is genuine cross-horizon disagreement, a single-axis reformulation would
**erase** that signal rather than fix it. A2.1's characterisation should record
whether violators cluster on symbols/times where a daily and an hourly fork
would plausibly disagree — which cannot be checked until §13.1 exists. **That is
a further argument for constructing early even though nothing consumes it.**
