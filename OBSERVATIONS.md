# OBSERVATIONS.md — evidenced findings, deferred fixes

Running log of things we've **noticed and understood but deliberately not fixed yet.**
The point of this file is continuity across work sessions: an observation captured
here survives even when the thread that found it is gone.

## Rules for this file
- **Nothing goes in without evidence.** Every entry cites the data (report, query,
  trade count, dates) that produced it. A hunch with no numbers is not an entry.
- **Every entry has a STATUS** (see legend). The status is the first thing you read.
- **Deferred means deferred.** An entry here is explicitly *not* a work item yet.
  When we decide to act, it moves to the ROADMAP / a build, and its status here
  becomes RESOLVED with a pointer to what was done.
- **Sample size is stated, always.** "n=7, one session" and "n=99, 8 sessions" are
  different confidence levels and must never read the same.
- Newest entries at the top. Date every observation and every update to it.

## Status legend
- `OBSERVING` — pattern seen, deliberately accumulating more data before any fix.
- `HYPOTHESIS` — a proposed cause, not yet confirmed across enough data.
- `CONFIRMED` — pattern holds across multiple sessions; cause understood; fix deferred to L3 / later.
- `WATCH` — minor or uncertain; noting it so it isn't lost, not actively studying it.
- `RESOLVED` — acted on; says what was done and where.

---

## 2026-07-24 (eve) — Sweep washout: what's the fingerprint? (three dead ends + one live lead)
**STATUS: HYPOTHESIS** (level-conviction lead is the strongest; capture shipped, awaiting data)

Tried to find what separated a GOOD sweep day (07-15: 6/8, +881) from a WASHOUT
(07-24: 2/7, −1687), same symbol AVGO, both current-engine. Measured off raw OHLC:

**Three intraday-structure metrics tried at n=1 — NONE separated the days cleanly:**
- **Open-side persistence** (% bars above/below the open): *looked* decisive (99% one
  side on washout vs 81% on good) — but it was a **net-move artifact**. VWAP killed it.
- **VWAP crossings**: pointed the OPPOSITE way (washout 32 vs good 25 — washout looked
  MORE mean-reverting). So "one-sided" was an illusion of the open anchor.
- **Two-axis chop score** (midline_crossings × flat_angle, the real regime_confluence
  fns): flat across both days. NB the reconstructed flat-angle was inflated (~28° med vs
  the engine's logged ~8° on AAPL) because ATR-14-on-1m ≠ the engine's ATR — so this
  score was built on a miscalibrated input and can't be trusted. **Read logged angle
  from replay jsonl, never reconstruct from candles.**
- The only real difference was **net move** (−0.11% vs −1.41%) — not tradeable (only
  known at close). The two days are **structurally similar** on every 25-bar-window
  metric available. Fingerprint is NOT in intraday window shape, at least not at n=1.

**THE LIVE LEAD — level conviction (Jason's hypothesis, the best one yet):**
The washout sweeps may have fired against **low-conviction levels (equal-highs/
equal-lows)** rather than **named pools (PDH/PDL/session)**. Mechanism: a named level
has real resting liquidity to fuel a reversal; an equal-H/L is self-defined with little
behind it, so price blows through and doesn't snap back. Partial corroboration:
`liquidity_mapper` had a bug (fixed v3.1, 07-14) where named-level detection saw
**0 of 1,367 evals** — so during 07-06 (a washout), named levels were INVISIBLE and
every sweep fired against equal-H/L by default. Exactly the hypothesis, mechanically
forced, for at least that day.

**Could NOT test it** — the swept-level type was computed at signal time and **not
persisted to the trade record** (notes empty, confluence_factors None). Same class of
gap as the ADX-not-logged issue.

**ACTION TAKEN (shipped, not deferred):** added `swept_level_name` + `level_strength`
(0..1: equal-H/L≈0.2, named PDL/PDH 0.6–1.0 scaled by touch_count) to OptionsSignal,
stamped in both sweep paths, and written to the trade record (schema + auto-migration).
Files: base_strategy, sweep_reversal_strategy, trade_logger, entry_engine (v-obs2).
**Starting Monday every sweep records what KIND of level it hit.** Then this becomes
directly answerable: do named-level sweeps win and equal-H/L sweeps lose? Value not
boolean, so a future sweep gate could threshold on level_strength.

**To close:** accumulate current-engine sweeps with level_strength logged; check
win-rate / expectancy by level_strength bucket. If equal-H/L sweeps are the losers,
the fix is a level_strength floor on the sweep gate (L3).

---

## 2026-07-24 (eve) — Level hierarchy + missing Overnight High/Low (NEXT BUILD)
**STATUS: HYPOTHESIS / action queued** (logic change — do tester-first, NOT folded
into the observability commit).

Two related gaps in `liquidity_mapper`:

1. **No Overnight High/Low.** The mapper identifies PDH/PDL + Asia/London/NY session
   H/L (8 named levels) + unnamed equal-H/L pools — but **no explicit overnight
   high/low.** ON H/L is one of the most-raided levels at the cash open; its absence
   means true ON raids either go untagged or match only an individual session extreme.
   Risk: real high-conviction ON raids are landing in the "equal-H/L / low-conviction"
   bucket by default, which would corrupt the very sweep-postmortem analysis we just
   instrumented. (ON H/L is derivable as the extremes across the Asia+London span, i.e.
   the pre-NY-open window — the session data is already collected.)

2. **Named levels are a flat `is_named` boolean — no hierarchy.** PDH and "Asia Low"
   currently carry identical weight. They should not.

**DESIRED LEVEL HIERARCHY (Jason, 2026-07-24), highest→lowest conviction:**
- **Overnight High/Low — dominant, or at least EQUIVALENT to PDH/PDL.** (top tier)
- **PDH / PDL** — top tier alongside ON H/L.
- **Historic S/R** — established prior support/resistance (multi-day). (mid tier)
- **Uniform / equal H/L** — self-defined equal-highs/lows. **LOWEST** conviction.

This replaces the flat `is_named` bool with a graded `level_strength` reflecting the
tier (value not boolean, consistent with the whole system). Session H/L (Asia/London/
NY individually) sit below ON H/L and PDH/PDL — they're components, not the headline.

**To close:** add `overnight_high`/`overnight_low` to LiquidityMap + `_add_named_pool`
as a named tier; replace flat is_named weighting with the tiered level_strength above;
prove inert on the TESTER first (mapper logic touches what sweeps can fire against —
that's trading behavior, not just logging, and the mapper's wall-clock bug history
demands caution). Then the level_strength already flowing to the trade record (shipped
this session) carries the *tiered* value and the postmortem buckets become meaningful.

---

## 2026-07-24 (eve) — Trade record was missing regime context at entry
**STATUS: RESOLVED.** The trades table never had an ADX field — ADX lived only in the
separate `regime_log` table, so every trade showed adx=0.0 (structural blank, not a
starvation bug). Fixed as observability: added `adx_at_entry`, `regime_conviction`,
`flat_angle_deg` to the trade record (schema + auto-migration + wired through all entry
paths). Live Monday-forward. **Historical trades still blank** — ADX-at-entry for past
trades must be reconstructed by timestamp-joining `regime_log` (offered; deferred).
NB: the trade record's ADX is only as warm as the classifier's — live is warm now (400-
bar store), replay warmed by the bookmark; the two fixes are what make this field real.

---
**STATUS: OBSERVING** (decision 2026-07-24: let the pattern stack across more days
before any fix — do NOT install a circuit breaker or change the strategy yet, as
that would contaminate the very pattern we're trying to see).

**Evidence (fleet_trades, 99 sweep trades across 8 sessions: 07-06,07,08,15,16,20,22,24):**
> ⚠️ **SAMPLE CAVEAT (added 2026-07-24 eve):** the pre-07-13 sessions
> (07-06/07/08 = 75 of these 99 trades) ran a **different trading engine** — different
> entries and exits, since-fixed bugs. Pooling them with the current engine
> (07-13 onward) compares two systems. The current-engine sweep sample is only
> ~24 trades (07-13→07-24), of which the washouts (07-22, 07-24) are most losses.
> Treat the 75%/n=99 numbers below as **mostly the OLD engine** — the current-engine
> pattern is far thinner and genuinely needs to stack. Candle tape also only exists
> from 07-13 (same engine boundary).
- Overall sweep win rate **75%** (74/99) but net **−$3,444**. Winning 3 of 4 and
  still losing money → payoff asymmetry: losers are much larger than winners.
- **Setup score does NOT discriminate.** Winner scores min/med/max 0.52/0.62/0.82;
  loser scores 0.56/0.68/0.83 — losers score *higher* if anything. Across n=99 the
  conviction score has no predictive power for sweep outcomes. Raising the sweep bar
  would only cut volume, not improve expectancy.
- Losses cluster on **washout days**: 07-06 went 0/5 (−$2,279), 07-22 0/2 (−$879),
  07-24 5 losers all `stop_hit` at −40% to −46% (−$1,687 net). A single washout day
  erases several good days (07-08 was 35/41 wins, +$982).
- Per-trade excursion (07-24): MFE ~+12% before dying to MAE ~−43% on the losers —
  they barely went green, then hit the wide stop. Winners trailed out ~+25% off a
  ~+60% MFE peak (giveback ~34%).

**Read:** entries are *good* (75% hit rate proves the setup fires on real reversals).
The problem is **risk/exit asymmetry** — stop is wide (~−40%+) while winners are
booked ~+25%, so a normal loss outweighs a normal win, and washout days hemorrhage.
This is an EXIT/SIZING problem, not an entry or conviction problem.

**Ruled out (with evidence):**
- NOT conviction — score is noise at n=99.
- NOT entry direction — LOW-sweeps are 83% lifetime (47 trades); 07-24's 2/6 LOW was
  an anomaly for that side, not the norm. Earlier "fading a trend" read was
  over-fit to one down day and is retracted.
- NOT a broken stop — stops fired correctly, capping each loss ~−42% as designed.

**What to watch as days accumulate (no action, just observe):**
- Does 75%-win / negative-net hold, or regress?
- **Washout-day fingerprint:** tag each 0-fer day with regime / ADX / VIX. Hypothesis
  to confirm or kill — washouts are strong-trend days where reversals get run over.
- LOW vs HIGH win-rate split vs the day's direction (trend-alignment signal).
- Whether score ever develops a discriminating threshold at larger n.

**When we act (deferred to L3):** first candidate is tightening the sweep stop toward
the winners' realized magnitude; second is a washout-day stand-down rule. Not before
the washout-day regime fingerprint is confirmed across more sessions.
