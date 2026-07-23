# The Pitchfork Overlay — Design White Paper
### options_trader v4.0 milestone · drafted 2026-07-23

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

`LiquidityMapper` already computes swing pivots. The overlay consumes those —
it does **not** introduce a second, competing definition of a swing.

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
`N` consecutive anchor-timeframe closes beyond the **counter-trend** tine by
`≥ D × ATR`. Start `N = 2`, `D = 0.25`.

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
| 2 | **Continuation pullback rail** | The ML is the structural version of `bb_middle`. Current gate is `CONTINUATION_MIDLINE_ATR = 0.35 × ATR` around a flat mean; the ML slopes with the trend the trade is riding. |
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
