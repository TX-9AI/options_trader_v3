# EXIT RULES — every way every trade closes, and what it's set at

Extracted from the running code (`exit_engine.py` v3.8, `base_strategy.py`,
`config.py` v2.0), 2026-07-15 — **updated for the runner refinements** (all
env-tunable for paper A/B): directional floor 25%→**40%** (`OT_MAX_LOSS_PCT`);
trails anchor to **5-minute FVGs** (`OT_USE_5M_FVG_TRAIL`); FVG floors clamped
to ≤ **90% of current** (`OT_FVG_FLOOR_MAX_LOCK_PCT`); post-target fallback
**85%→75%** (`OT_POST_TARGET_TRAIL_LOCK_PCT`); sweep's +100% hard TP replaced
by the post-target trail (`OT_SWEEP_POST_TARGET_TRAIL`). Butterfly floor stays
25%; condor unchanged. Sizing is full-premium based, so at $1000 positions a
floored directional now costs ~$400 — set `OT_DAILY_LOSS_LIMIT` to match
(e.g. 3 stops = $1,200). New telemetry: `max_premium_seen` / `min_premium_seen`
per trade (MFE/MAE) for evidence-based tuning. Evaluated **every tick, first
match wins**, in the order listed per strategy.

Each exit is tagged by its role in the design:
- 🛑 **LOSS-MINIMIZER** — fires on losing trades to cap the damage
- 📉 **GIVE-BACK EXIT** — books a PROFIT, but only when the market starts
  taking it back (trail/structure/momentum) — the "let runners run" family
- 🎯 **HARD TAKE-PROFIT** — closes at a fixed profit level regardless
- ⏰ **TIME EXIT** — the clock, not price

---

## Universal (every strategy, every mode)

| Exit | Trigger | Value | Tag |
|---|---|---|---|
| Hard close | Time ≥ 15:45 ET | flatten_all retries every tick to 16:00, pages on failure | ⏰ |

---

## ORB (the flagship) — **no hard take-profit exists, by design**

| # | Exit | Trigger | Set at | Tag |
|---|---|---|---|---|
| 1 | Hard close | 15:45 ET | — | ⏰ |
| 2 | **Hard stop (−25% floor)** | premium ≤ `stop_premium` | **entry × 0.60 (−40%, `MAX_LOSS_PCT`)** — immutable, set at entry, checked UNCONDITIONALLY every tick regardless of trail state; label carries the record's actual floor pct | 🛑 |
| 3 | **Structure stop** | last CLOSED 1m candle beyond the impulsive candle's wick (`underlying_stop`): close < impulsive low (long) / > impulsive high (short). Closing back inside the ORB range does NOT stop | thesis level, set at entry | 🛑 (thesis death — can fire green or red) |
| 4 | **Theta bleed** | ALL of: held ≥ **20 min** · gain ≥ **+10%** · gain < **+20%** (trail ceiling) · projected decay over next **20 min** (per CALENDAR day, θ×20/1440) ≥ current gain | narrow window: a small, stalled winner only | 📉 |
| 5 | **Past +100%** ("target") | premium ≥ entry × 2.0 (`ORB_TP_MULTIPLIER = 1.0`) — **NO exit fires.** Trail tightens: nearest unfilled in-favor **5m** FVG (1m fallback) converted to a premium floor, else **85% of current premium** | the runner regime | 📉 |
| 6 | **Trail (below +100%)** | Two trails, HIGHER governs: **FVG trail** arms at **+20%** (floor = FVG level, else 80% of current — `FVG_TRAIL_LOCK_PCT`); **% trail** arms at **+50%** (`TRAIL_ACTIVATION_PCT`), initial lock at entry × 1.25 (`TRAIL_LOCK_PCT`), then ratchets to **75% of current premium**, never down | 📉 |

**ORB never exits "at target."** +100% just switches it into the tightest
trail. Every profitable ORB exit is the market taking some back: trail hit,
FVG floor hit, structure break, or theta about to eat a stalled small gain.

## Sweep Reversal

| # | Exit | Trigger | Set at | Tag |
|---|---|---|---|---|
| 1 | Hard close | 15:45 ET | — | ⏰ |
| 2 | Hard stop | premium ≤ `stop_premium` | **entry × 0.60** (−40%) | 🛑 |
| 3 | **Past +100%** | `SWEEP_POST_TARGET_TRAIL=True` (default): NO hard exit — switches to the ORB post-target trail (5m FVG / 75%-of-current fallback). Env False restores the old `target_hit` guillotine | 📉 (was the one hard TP among directionals) |
| 4 | **BOS exit** | 1-min break of structure against the position — only once pnl > 0 (a healthy retest that hasn't moved yet can't be BOS'd out) | structure-defined | 📉 |
| 5 | Theta bleed | same four gates as ORB (≥20 min, gain in [+10%, +20%), decay ≥ gain) | 📉 |
| 6 | Trail | same dual trail as ORB: FVG arms +20%, % trail arms +50% → 75%-of-current ratchet, higher governs, floored at the −25% stop | 📉 |

## Iron Condor legs (credit verticals — P&L is inverted: spread value ↓ = profit)

| # | Exit | Trigger | Set at | Tag |
|---|---|---|---|---|
| 1 | Hard close | 15:45 ET | — | ⏰ |
| 2 | **Adverse regime flip** | direction-aware: call spread exits on TRENDING_BULL / BREAKOUT_VOLATILE; put spread on TRENDING_BEAR / BREAKOUT_VOLATILE. A FAVORABLE flip holds (Leg 2 gets cancelled by the strategy instead) | regime engine | 🛑 (thesis death, pre-emptive) |
| 3 | **Condor stop** | spread value ≥ credit × **1.25** (`CONDOR_STOP_LOSS_PCT = 0.25`) | −25% of credit received | 🛑 |
| 4 | **Nickel close** | spread value ≤ **$0.05** (`CONDOR_NICKEL_CLOSE`) | ~all the credit captured; closes to free margin and kill tail risk | 🎯 |
| — | **Broken-wing roll** | not an exit: when one side is tested and rolling the untested side makes it risk-free, the untested vertical closes (books its P&L) and re-opens rolled. Final form — no further adjustments | strategy | — |

## Debit Butterfly

| # | Exit | Trigger | Set at | Tag |
|---|---|---|---|---|
| 1 | Hard close | 15:45 ET | — | ⏰ |
| 2 | **Regime flip** | regime becomes TRENDING_BULL / TRENDING_BEAR / BREAKOUT_VOLATILE — any trend breaks the pinning thesis, either direction | regime engine | 🛑 (pre-emptive) |
| 3 | **Max hold** | held ≥ **150 min** (`BUTTERFLY_MAX_HOLD_MIN`, 2.5h) | ⏰ |
| 4 | Hard stop | net value ≤ `stop_premium` | **net debit × 0.75** (−25%) | 🛑 |
| 5 | **Target hit** | net value ≥ debit + **20% of max profit** (`BUTTERFLY_TP_PCT = 0.20`) | 🎯 (deliberately modest — pin plays decay fast) |

No trail, no BOS on butterflies.

## Adopted positions (found at the broker with no DB plan)

| # | Exit | Trigger | Set at | Tag |
|---|---|---|---|---|
| 1 | Hard close | 15:45 ET | — | ⏰ |
| 2 | Hard stop | sign-correct: long ≤ entry × 0.75; short ≥ entry × 1.25 (`ADOPTED_STOP_PCT = 0.25`, tracking `MAX_LOSS_PCT`) | 🛑 |
| 3 | Trail (LONGS only) | standard % trail (arms +50%, 75%-of-current ratchet). Lone adopted shorts (anomaly) get stop + hard close only — no trail | 📉 |

Already past its stop when adopted → exits first tick ("if red exit, if green
manage").

---

## The design, confirmed by the tags

Count the profit-side exits: across all five strategies there are exactly
**three 🎯 hard take-profits** — sweep's +100%, the condor nickel close, and
the butterfly's 20%-of-max — and two of those (nickel, butterfly) exist
because *holding* a nearly-max-profit 0DTE credit/pin structure is pure tail
risk for pennies. Everything else that books a profit is 📉 **give-back
triggered**: trails that only ratchet up, FVG floors, BOS, the impulsive-origin
structure stop, theta protection on stalled small winners. The flagship (ORB)
has **no hard TP at all** — +100% only tightens the leash.

So yes: by construction, most winning exits WILL log as some form of "stop"
(`trail_stop_hit`, `post_target_trail`, `bos_exit`, `orb_structure_stop` in
the green, `theta_bleed`) — that is the runner philosophy working, not stops
misfiring. The v3.3 exit-reason integrity fix matters here: labels are now
truthful (a post-target trail exit at +140% logs as a trail, never as
`hard_stop_25pct`), so the `exit_reason` distribution in the DB can be read
at face value when checking this design against results.

**The one number to watch:** the loss side is a single flat rule everywhere —
**−25% of premium/credit/debit** (`stop_premium`, immutable since v3.3) plus
thesis stops (structure, adverse regime) that usually fire before the dollars
do. Loss-minimization = whichever dies first, premium or thesis.
