# docs/FLEET_STATE_2026-08-13.md — v1.0

**WHERE THE FLEET STANDS AFTER 2026-08-13.**

Baked `7efd320` across **29/29 boxes**, all services active, then the hotfix
`e639099` on top. This is the largest single-day behavioural change in the
project's history: **eleven changes that alter what trades**, landing together
because the alternative on the table that morning was regressing the fleet to
options_trader v2 and restarting from the primitive engine.

---

## 0. THE FINDING THAT DROVE EVERYTHING

The operator's own summary, and it is the most accurate sentence written all day:

> *"I demanded so much confluence for a decision that it ended up simply being
> confirmation instead (the move has happened)."*

Six independent measurements point at it:

| evidence | reading |
|---|---|
| grade A 399 trades **−$21/trade** vs grade B 220 at **+$9** | high score = worse |
| `reg.conviction` pegged at 1.00: **−$25/trade**; lowest band **+$17** | high conviction = late |
| handoff × conviction 1.00: **n=128, −$6,623** | one band > the whole strategy's loss |
| handoff 52% never-favorable vs standalone 33% | the relaxed-gate path is the bad half |
| MFE at **89% of hold**, 81% late | the move is over when we exit |
| scorer separates "will it go green", not "will it pay" | it grades favorability, not profit |

**⚠️ AND THE DIRECT TEST STILL HAS NOT RUN.** `factor_sweep` found
`derived.confluence_count` takes only TWO values across 619 trades — 3 and 4.
There is no low-confluence population anywhere in the sample. **You cannot
measure the cost of a filter you never relax**, which is precisely how a
confirmation requirement hides inside what looks like a confluence model. The
diagnosis is well-supported by proxies; it is not yet directly measured.

---

## 1. BEHAVIOURAL CHANGES — these alter what trades

### GRD.1 — continuation stops buying 1.5× size
`risk/setup_scorer.py` v1.7

**Why.** `ContinuationStrategy` had no entry in `STRATEGY_PROFILES` and fell to
`"default"`, where `regime_conviction` 0.30 and `signal_quality` 0.25 weighted
**the same number twice** (continuation sets `signal.conviction =
regime.conviction`). Add `vwap_alignment` and `liquidity_clear`, both measured
constants at 1.000, and **~90% of the grade was duplicate or constant.**

**What changed.** Explicit profile: `regime_conviction` 0.55 (the old 0.30+0.25
on one number), `grade_b` **0.55 UNCHANGED** so the fire boundary is provably
identical — verified over 200,000 random signals, zero divergence. `grade_a`
**1.01**, above the maximum achievable 1.00, so no continuation setup earns the
1.5× multiplier until an input is proven to separate.

**Expected benefit.** ~**+$2,748** on the 18-session sample. Sizing only.

**Tuning.** No env knob. To restore A-grades, lower `grade_a` below 1.0 — but
only after a scorer input demonstrably separates. **Second-order effect to
watch:** smaller continuation losses mean fewer daily-loss-breaker trips, so
boxes may stay alive longer and trade further into the afternoon.

**Verification.** No continuation trade should carry a 1.5× multiplier.

---

### STOP FLOOR 0.25 → 0.15
`config.py` v4.7 · `OT_CONT_STOP_PCT`

**Why.** The `max_loss_floor / ContinuationStrategy` cohort is **66 trades over
9 sessions at a 0% win rate.** A 15% floor stops all 66 with **ZERO winners
cut** — net delta **+8.85** units of entry premium against +2.25 at 25%. Meets
the pre-registered cheapest-threshold-catching-no-winners rule rather than an
in-sample argmax.

**⚠️ What this cohort is.** BY DEFINITION the trades where NO structural stop
fired — not regime_flip, not bos_exit, not insurance_stop. The thesis was still
technically intact and the premium died anyway. Zero winners cut over 9 sessions
is evidence it cost nothing; it is not proof it cannot.

**Tuning.** `OT_CONT_STOP_PCT` is the per-box override; the repo default is the
fleet lever. If winners start getting cut, 0.20 is the next stop up.

---

### AFD.1 — no long premium after 11:00
`main.py` v6.2 · `config.py` v4.6 · `OT_DEBIT_CUTOFF_ET`, `OT_DEBIT_BLOCK_ACTIVE`

**Why.** Operator: *"The only other Long that can fire is either part of a
butterfly or an iron condor vertical spread from 11 o'clock onwards."* Measured,
843 trades / 15 sessions: open 09:30-10:00 **+$10,717.50** against 10:00-11:00
**−$8,715** and 11:00-14:00 **−$1,539.50**, on a whole book of **+$463**.

**What changed.** ORB / Continuation / SweepReversal refused past 11:00. Placed
AFTER the signal is chosen — one gate instead of three, the refused signal is
fully formed so the journal records `gate_block:afternoon_debit`, and condor legs
never reach it (they route through `_execute_condor_leg` earlier), so the credit
path is exempt **by construction** rather than by a list entry that could rot.

**Expected benefit.** ~**+$2,901** on continuation alone across 18 sessions.

**⚠️ Known trade-off.** It also removes the 12:00 hour, which was continuation's
only positive afternoon hour (**+$1,225**, n=81 — about four trades a session, so
possibly noise). A 13:00 cutoff would have saved more on this sample. The
operator chose 11:00 on structural grounds (theta), not P&L, and that reasoning
survives a noisy cell.

**Tuning.** `OT_DEBIT_CUTOFF_ET="13:00"` moves the hour with no deploy.
`OT_DEBIT_BLOCK_ACTIVE=0` disables it.

**⚠️ NOT ADDRESSED:** the 10:00 hour, **−$8,715** — still the largest single
negative in the book and untouched by this change.

---

### PF.5 — the condor anchors on the daily pitchfork
`strategy/iron_condor_strategy.py` · `main.py` v6.3 · `analysis/pitchfork_observer.py`

**Why.** The pitchfork has been built, live and **unconsumed** since 2026-08-12 —
full geometry, lifecycle, and an observer journaling rails, with exactly ONE call
site (`main.py:2091`) and **nothing ever reading the rails back.** The white
paper pre-registered condor strikes as the first consumer because strike
placement produces a credit directly comparable on identical tape.

**What changed.** Short strikes anchor on the rails. A strike qualifies only if
beyond the RAIL, beyond the surviving `0.80 × EM` MINIMUM DISTANCE (retained so a
rail on top of spot cannot produce a strike with no room — the ~3-week bleed
`v-dualfloor` fixed), and **beyond the SESSION EXTREME** (new: a level price has
already traded through is a level the market has PROVEN it can reach). Leg order
from the fork's slope. **NO FORK → NO CONDOR.**

**Daily, not hourly**, and deliberately: a daily fork is invalidated only by
DAILY closes, so an intraday session cannot move the rail a spread was sold
against. The hourly fork has a p50 lifetime of 5 bars and a k=3 confirmation lag.

**Expected behaviour, not benefit.** Measured coverage 2026-08-12: **13 daily
forks across 7 of 15 boxes**, so roughly half the fleet is condor-ineligible.
**And the daily `pos_pct` runs p10 40.8 / p50 74.2 / p90 98.5** — price lives in
the upper half and essentially never visits the lower daily tine. **Expect mostly
call-side standalones and few completed two-sided condors.** That is arguably
correct: if price never approaches the lower tine, the put side was never rich.

**Tuning.** `OT_CONDOR_REQUIRE_FORK=0` restores condors without a fork.
`OT_CONDOR_PF_ANCHOR=0` reverts to the dual floor. `OT_CONDOR_PF_TF=hourly`
switches frames. `OT_CONDOR_PF_FLAT` sets the slope epsilon below which leg
ordering falls back to proximity.

---

### PF.6 — POP floor and quote-width floor
`config.py` v4.9/v4.10 · `OT_CONDOR_MIN_POP`, `OT_CONDOR_MAX_QUOTE_WIDTH`

**Why.** Operator: *"There should be a reasonable expectation of trade success
better than 50-50... somewhere near the 70 to 80% range."*

**POP = Φ(z), z = distance / (σ·√bars_left)**, horizon to the **15:45 flatten**
(a condor leg is closed there, so using the bell overstates T). Driftless and
normal deliberately — a drift term is a forecast, and this system's directional
forecasts do not separate. Degenerate inputs return 0.0 and FAIL; a missing ATR
must never read as safe.

**⚠️ VALIDATED OUT-OF-SAMPLE.** TC.7's handoff arm, terminal-OK against measured
EV: **58%→−0.23 · 54%→−0.33 · 63%→−0.24 · 67%→−0.09**, then **76%→+0.33 ·
78%→+0.32 · 88%→+0.35**. **Every cell below 70% lost money; every cell at 76%+
made it.** Nobody searched for 0.70 — it is a stated risk preference, not an
argmax, **which is exactly why it must NOT be re-tuned on this same data.**

**Honest cost.** On the STANDALONE arm the sub-70 cells were marginally POSITIVE
(+0.08 at 61%, +0.04 at 69%), so the floor gives up ~$0.12/spread there.

**Quote-width floor 0.25 of mid.** A RANKING never refuses — it returns the
least-bad strike even when every candidate is broken, and on 0DTE a nickel of
noise on a wide quote trips the stop on the QUOTE rather than on price. **0.25 is
a stated PRIOR reasoned from an adjacent population** (factor_sweep's worst
continuation quintile ran 0.13-0.88 at −$37/trade; the two best under 0.043) —
debit entries, not condor shorts. The rejected-leg log is what would fit it
properly.

**Tuning.** `OT_CONDOR_MIN_POP` 0.70 → 0.75/0.80 tightens toward the top of the
band. `OT_CONDOR_MAX_QUOTE_WIDTH` loosens if legs are being refused too often —
the skip log prints the width that failed.

---

### CND.7 — the ratchet no longer closes untested legs
`execution/exit_engine.py` v4.17 · `OT_CONDOR_RATCHET_STANDALONE_ONLY`

**Why, and this is the sharpest defect found all day.** The base −25% stop only
ever fires on the TESTED side, because a credit spread's value RISES as price
approaches your short. **The ratchet does the opposite: it tightens the UNTESTED
side's stop to breakeven at +20% and +20%-locked at +40% precisely BECAUSE that
side is winning.** On the reversal the tested leg stops at −25% **and the
untested leg hits its ratcheted stop too** — a leg price never went near, closed
by a stop that exists only because it was profitable. **That is the double-stop:
5 of 14 condor symbol-days had BOTH sides stopped.** And it fires BEFORE the roll
can ever be used, because the roll needs a tested side.

**What changed.** While `_condor_sibling_open()` is true, the base floor is the
ONLY stop. No tier, and the stored high-water is neither applied nor updated, so
a leg returning to standalone resumes from a level it genuinely earned.

**Preserved.** `condor_stop` went **0% → 19% win** after the ratchet shipped —
but that came mostly from STANDALONES (18 of 46 legs never got a second side).
Scoping keeps the gain where it was measured.

**⚠️ Accepted cost.** An untested leg that runs to +40% and reverses now gives it
back rather than locking +20%.

**Not changed, deliberately:** the adverse-regime-flip exit is direction-aware —
a call spread exits only on TRENDING_BULL, which IS price rising toward that
short strike — so it already fires only on the threatened side.

---

### VERTICALS HOLD TO 15:45
`config.py` v4.12 · `OT_VERTICAL_HOLD_1545`

**Why.** The flatten ladder opens at 15:40 so a DEBIT position gets a mark-limit
phase before the 15:45 cross. **A short vertical has the opposite sign** — it
decays TOWARD the holder, so 15:40-15:45 is the steepest part of its curve.
Operator: *"It's 5 more minutes of exponentially rising profit curve."*

**Why the ladder was NOT moved globally.** Opening it at 15:45 forces every EOD
exit marketable — the exact failure `time_utils` v3.8 fixed, and expensive on a
book whose widest spread quintile already costs −$37/trade.

**⚠️ NOT held past 15:45, and this is a hard limit.** Every instrument except SPX
is AMERICAN-STYLE and PHYSICALLY SETTLED, so a spread finishing BETWEEN the
strikes assigns the short and leaves an unhedged overnight stock position.
"Defined risk" is true at settlement, not through assignment — **and the paper
engine has no assignment model, so it would report a clean result that does not
survive going live.**

---

### TC.6 — the trend credit spread
`strategy/trend_credit_spread.py` v1.0 · `main.py` v6.4 · `OT_TCS_ACTIVE`

**Why.** The afternoon needed a vehicle. AFD.1 blocks long premium, the condor
self-gates to RANGING, and the butterfly needs PINNING GEX — so a **trending**
afternoon had nothing.

**The trade.** After an ORB runaway, sell a defined-risk vertical BEYOND the
broken boundary. Price broke the range and never retested, so the boundary IS the
floor of that move and the level `orb_structure_stop` already calls thesis death.
**Structure and invalidation become the same event.**

**Measured** (`spread_counterfactual --anchor orb`, runaway-handoff arm, 18
sessions): EV positive at EVERY offset; the 0.00% cell — the strike AT the
boundary — **n=30, +$0.52/spread, 90% terminal OK, 79% RECOVERED**, entry sitting
p50 +0.91% above the boundary. **The STANDALONE control was mostly NEGATIVE on
the same anchor**, because without a runaway the boundary sits at or above the
fill 64% of the time. **Runaway-specific by construction.**

**Exit: BREACH OR NICKEL, nothing else.** No premium stop, no ratchet — **the
measured EV was HELD TO EXPIRY, UNMANAGED**, so a stop bolted on is a different
trade. Breach is a CLOSED BAR beyond the boundary; a wick is a touch.

**⚠️ HIGHEST-RISK ITEM TOMORROW.** Never executed a live order. Fires through
`_execute_condor_leg`. Defers when a condor plan holds the symbol.

**Tuning.** `OT_TCS_ACTIVE=0` kills it — **for defects, not for bad trades.**
Operator: *"bad trades are still good data."* It only fires after a runaway on a
trending afternoon, so observations will be scarce; killing it on the first loser
leaves nothing to read.

---

### GRD.2 — continuation populates `underlying_target`
`strategy/continuation_strategy.py` v1.7

**Why.** `trend_strike_plan` has ALWAYS computed the target and USED IT to pick
the strike, then discarded it. **The bot was never target-free; it was
target-blind**, and three consumers sat inert on 77% of fleet volume: `_rrr()`
returned None on every continuation signal (why `rrr` appears in ORB's scorer
table and nowhere else, and why MIN_RRR was structurally inert);
`_pools_in_path` scans `entry < p < target`, so with 0.0 a LONG's window is
**empty by construction** and `liquidity_clear` was a STRUCTURAL constant at
1.000; and `_update_post_target_trail` is guarded on `> 0`, so continuation
always fell back to the blunt 85% trail instead of the FVG floor past 100% TP.

**⚠️ NOT A TAKE-PROFIT.** The no-target design stands. This is the R denominator
and the trail's reference. A test asserts no exit fires on reaching it.

**⚠️ The entry gate barely moves — arithmetic, not opinion.** `liq_score` at
weight 0.20 removes AT MOST 0.20 from a total whose p50 is 0.885 against a 0.55
bar. Even 4+ blocking pools leaves 0.685 and still fires. **The real change is
the exit trail.**

**Verification signatures — the only per-change attribution available tomorrow:**
`rrr` appearing in the scorer breakdown · `liquidity_clear` moving off 1.000 ·
`post_target_trail` appearing in `exit_reason`.

---

### SWP.3 — the approach corroborator's sign is refuted
`analysis/trade_readiness.py` v1.9 · `SWEEP_APPR_W`

**Why.** Three independent measurements: **LIQ.1** (the London level TRACKS PRICE
rather than being approached by it), **ANT.1** (appr_val −41%, appr_touches
−45%), **ANT.2** (fitted weights −0.39 / −0.40).

**Not inverted.** `1 - appr_val` asserts "far from any named level = ready",
nonsense for a SWEEP. The likelier mechanism is that **proximity is PRE-sweep**:
price near a pool means the sweep has not happened, so the term was scoring the
setup's ABSENCE. Sign wrong, form unknown — removed from the composite, KEPT in
the journal.

**⚠️ The renormalisation was the real risk.** The four weights summed to exactly
1.0 and the stage/arm bars are ABSOLUTE. Dropping 0.25 without redistributing
would compress every sweep score by a quarter and make the arm bar effectively
unreachable — **the track would go quiet while looking like a correction.**
0.30/0.20/0.25 → **0.400/0.267/0.333**.

**LOG-ONLY** — `main.py:2045` discards `assess_all()`'s return, so no trade
changes today. It stops every FUTURE fit inheriting a backwards term.

**⚠️ Tuning warning.** Raising `SWEEP_APPR_W` alone pushes the sum past 1.0 and
inflates every score against the absolute bars. **Change all four together or not
at all.**

---

### FRC.3 — the venue's price grid, on every order path
`execution/tick_size.py` · `limit_ladder.py` v1.4 · `data/options_chain.py`

**Why.** Option increments are class- AND level-dependent, and `round(px, 2)`
posts UNPOSTABLE limits on nickel/dime classes. An invalid limit is rejected —
or **silently adjusted by the venue, which is a fill at a price nobody chose with
nothing in the logs to explain it.**

**Resolution order, so order time never guesses:** venue rule
(`NestedOptionChain.tick_sizes`, authoritative, cached per symbol) → quote proof
(an off-nickel bid PROVES penny; **asymmetric**, refines downward only) →
`PENNY_CLASSES` last resort, **which logs a warning**. Every resolution records
its source.

**And the bigger fix:** `limit_at_mark` prices EVERY exit plus the 15:40-15:44
reposts — far more orders than the entry ladder — and it was doing `round(px, 2)`.

**🔴 HOTFIX `e639099`.** The first version had the comment *"once per symbol per
session"* and **no cache check**, firing an extra SDK call on every
`fetch_chain()` — called from three places in the tick loop. `needs_venue_rule()`
now guards it, and a failed attempt counts as answered so a broken fetch does not
become the same hot loop.

---

## 2. SHIPPED INERT — built, tested, not active

| item | state | to activate |
|---|---|---|
| **LIQ.4** liquidity ledger | built, **NOT WIRED** — collects nothing | needs a tick-path call + RTH reset |
| **FRC.2** entry limit ladder | `OT_ENTRY_LADDER=0` | **do NOT enable before the fill model gates paper fills** |
| `fill_model.would_fill()` | built, unused | the gate FRC.2 depends on |

**⚠️ WHY FRC.2 MUST STAY OFF.** `paper_fill_price` books the posted price and
assumes it fills. Shade the limit without a fill test and every trade books the
aggressive rung while **no missed entry is ever modelled** — the more aggressive
the rung, the larger the manufactured gain. **Rung 1 would look like the best
change this system has ever made and be entirely fake.**

---

## 3. TOOLING — read-only, no behaviour

`slippage_audit` (FRC.1) · `spread_counterfactual` (TC.7, anchors: entry / orb /
floor) · `factor_sweep` v1.1 (ET hours, monotone band floor, `--setup-type`) ·
`orb_conversion` v1.1 (trade_id dedupe) · `scorer_backtest` v1.2 (raw row +
dedupe) · `credit_edge` v1.2 (touch trigger, per-side OTM guard, effective-n) ·
WORKING_AGREEMENT **§20** (an absence canary tests for a definition, never a
mention).

---

## 4. THE NUMBER THAT REFRAMES EVERYTHING — FRC.1

**Gross +$2,156 over 800 trades = +$2.70/trade, against average friction of
$126/trade. The system's edge is ~2% of the round-trip spread it trades in.**

The −$98,454 headline is a **worst case** assuming every order crosses; the bot
posts mark-limits. **But the relative ranking is valid regardless**, and the
quintile table is decisive: **Q5 carries $60,185 — 60% of ALL friction — for
−$169 of gross.** Q4+Q5 together are 79% of friction against −$6,337.

**Cutting them removes four-fifths of transaction cost AND improves gross.** It
is a pre-entry filter needing no forecast. **This is the largest unbuilt lever on
the board.**

---

## 5. WHAT TO WATCH TOMORROW

Read the first session as **"did anything break"**, not "which change helped."
Eleven behavioural changes in one bake; attribution is not available except for
GRD.2's three signatures.

**Expected, not defects:** `Condor: NO PLAN — no usable daily pitchfork` on ~half
the boxes · `liquidity_clear` off 1.000 · `STRATEGY: BLOCKED — … afternoon debit
cutoff` after 11:00 · few or zero `[tcs]` lines (runaway + trending is rare).

**Actual defects:** any traceback · `[tick] NO VENUE RULE` on a symbol that
should have one · TC.6 firing repeatedly on one symbol · condors going to zero
fleet-wide.

---

## 6. THE NEXT GATE — FRIDAY 2026-08-28

Operator's schedule, set 2026-08-13:

1. **Fri Aug 28** — evaluate paper P&L impact after the bugs are worked out.
2. **Resume L1 dial freezing.** L2 is mostly complete — a few verifications
   remain; chatter is nearly eliminated.
3. **Then L3.**
4. **Then final trade adjustments + stop-quality evaluation.**
5. **Then live cash, reduced size for the first week.**

**The two weeks to Aug 28 are a measurement window.** The changes are in; the
question is what they do. Resist re-tuning on the first bad session — most of
today's thresholds are stated priors rather than fits, and re-fitting them on the
data that motivated them is how an out-of-sample validation becomes an in-sample
one.
