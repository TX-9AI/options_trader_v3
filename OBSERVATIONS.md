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

## 2026-07-24 — Sweep Reversal: high win-rate, negative expectancy
**STATUS: OBSERVING** (decision 2026-07-24: let the pattern stack across more days
before any fix — do NOT install a circuit breaker or change the strategy yet, as
that would contaminate the very pattern we're trying to see).

**Evidence (fleet_trades, 99 sweep trades across 8 sessions: 07-06,07,08,15,16,20,22,24):**
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
