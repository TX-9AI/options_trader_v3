# POSTMORTEM — 2026-08-03

**Day: −$3,149.50 net · 88 trades · 15/15 boxes.**

Reproduce every number here from the devtools menu — nothing in this document
needs a new tool:

| number | where it comes from |
|---|---|
| day P&L, per-symbol | **48** — Live P&L standings |
| exit-reason / hold / P&L distributions | `tests/flicker_audit.py` |
| cross-day regime × strategy × grade | **41** — Trade breakdown |
| MFE/MAE per trade | **40** — Excursion report |

---

## THE ORGANIZING PRINCIPLE, and it is not "what should we tighten"

The fleet is **deliberately permissive right now**. We are collecting a broad
sample across as many environments as we can reach, precisely so that later we
can decide which strategies belong in which conditions. Operator, this session:

> *"There's no penalty for the trades being wrong right now or even the stops
> being wrong. We're collecting a broad range of data to figure out the best
> place to put everything, and for that we have to allow the trades to fire
> away."*

So a losing day is not, by itself, a finding. **The postmortem's job is to sort
the day into two buckets that get treated completely differently** — and to
resist the tightening reflex, which is the wrong output at this stage.

**BUCKET 1 — DEFECTS.** Wrong regardless of how permissive the environment is.
No gate setting makes them intentional. These get fixed immediately, **not
because they cost money but because they CORRUPT THE SAMPLE we are collecting.**

**BUCKET 2 — PERMISSIVENESS COSTS.** The system took the trade it was designed
to take and the environment did not cooperate. **This is the data.** Recording
it as a defect would be wrong, and "fixing" it would delete the observation.

Six weeks from now, when the tightening decisions actually get made, we will
want to know which line items were evidence and which were bugs contaminating
the evidence. That is what this split preserves.

---

## BUCKET 1 — DEFECTS

### 1.1 The regime-flicker exit — FOUND, DIAGNOSED, FIXED SAME DAY

Exit-reason distribution, window 2026-07-23 onward, 215 closed trades:

```
exit reason        n   hold p25   p50    p75   |pnl| p50
trail             93      3.0     4.8   10.8     203.50
stop              48      3.0     6.0   12.8     159.50
max_loss          31      3.0     4.8    7.8     400.00
regime_flip       26      0.2     0.8    3.0      48.00     <-
bos               13      7.2    12.0   15.2      90.00
```

**Half of all regime-flip exits close in under 48 seconds. A quarter close in
under 12 seconds.** Every other exit reason sits at 5–12 minutes. A position that
lives twelve seconds has not had time to be right or wrong — only to pay a
round-trip spread, which is roughly what the $48 median loss is.

By strategy: **ContinuationStrategy 19/99 (19%), IronCondorStrategy 6/22 (27%)**,
ORBStrategy **0/59**, SweepReversal **0/33**. The defect touches three strategies
and cannot break the other two.

**ROOT CAUSE — the fallback, not the flag.** `main.py` read
`st.regime and not st.stale` correctly. But when the book went stale it **fell
through to the v1.3 classifier — raw L1 argmax** — which is exactly the churn L2
exists to remove (436 committed switches vs 695 argmax flips). `exit_engine`
checks regime-flip **second**, before any price-based stop. So one wobbled tick
closed the position. And the trigger is routine: v4.6's own note records that
*"a tick gap over dt_max=90s re-stales every tick."*

**WHY IT IS A BUCKET-1 DEFECT even though losses are acceptable right now.** A
flickered exit does not merely cost $48. It writes a row tagged
`ContinuationStrategy / TRENDING / −$48` which will later be counted as evidence
about **continuation in a trending regime**. It is not. It is evidence about an
exit mechanism. Twenty-six such rows drag down a measurement they were never
about. **The defect is not the money — it is the mislabelled sample.**

**FIX — `main.py` v5.0, live on 29/29 boxes at `5dd425303d`.** Two rules, no new
parameter, nothing to tune:

- **stale + a committed label → HOLD that label** rather than falling back.
  Holding is *declining to act* on unknown information; the position stays
  protected the whole time by every price-based stop (15:45 hard close,
  break-of-structure, trail, stop, max loss) — none of which read the label.
- **stale → NO NEW ENTRIES.** Opening a position *is* a decision against a
  classification the engine cannot currently confirm. Costs are asymmetric: a
  missed entry costs opportunity, a wrong entry costs capital.

A cold book at the open still falls back to v1.3 — that path was always correct
(no prior state exists to hold) and is unchanged. **The fix does not reduce
firing.** It prevents premature exits, so each trade actually expresses its setup.

**VERIFY IT LANDED:** tomorrow's bot log should show `L2.5 STALE — HOLDING <label>`
and `Entry blocked: regime book is STALE`. Silence on both all session means the
branch is not being reached. Then re-run `flicker_audit` after a few sessions —
regime_flip hold times are the direct before/after.

### 1.2 The EOD conductor cannot send Telegram — OPEN

From tonight's run:

```
[BACKFILL] ⚠️ 7 symbol(s) still without candles (AMD, AVGO, CVX, DIA, GLD, GS, IWM)
[notify]   missing DTP_TELEGRAM_TOKEN/DTP_TELEGRAM_CHAT_ID; cannot send.
```

**Every EOD warning the conductor has ever raised has gone to a journal nobody
reads.** Tonight that swallowed a real one. Same box-versus-control credential
split as Saturday's blind-alert drill, one layer up: the bot boxes have
`TELEGRAM_TOKEN` in their systemd unit; the control conductor looks for
`DTP_`-prefixed variables that were never set.

Bucket 1 by the same test — it is wrong regardless of how permissive the trading
is, and it means we have been running EOD blind without knowing.

### 1.3 A constraint, not a defect, discovered alongside it

`DXFeed history is same-evening only`. A box that sat out a session can **never**
have its candles backfilled afterwards. So the short-tape gaps found on 08-01
(p10 = 241 rows against a 391-row full session) are **permanent once the day
passes**. Nothing to fix — but it means tape coverage is a use-it-or-lose-it
resource, which raises the cost of a box failing to wake.

---

## BUCKET 2 — PERMISSIVENESS COSTS (this is the data)

Today's two largest losses, both reviewed by the operator, both **good setups**:

```
MSFT   −$1,169.00   3 trades   ≈ −$390/trade
QQQ    −$1,327.00   5 trades   ≈ −$265/trade
```

Those two are **two-thirds of the day's loss on 8 of 88 trades.** The per-trade
sizes sit at or near the `max_loss` exit's median |P&L| of **$400.00**, which is
consistent with positions carried to the 40% floor rather than bled out.

**Operator's read: the entries were good, price chopped and did not cooperate.**

That is exactly what this bucket is for. The system took the trades it was
designed to take, in an environment we are deliberately allowing it into, and the
environment was unkind. **Recording this as a defect would delete an observation
we are paying for.**

### The unifying mechanism, worth noting because it links both buckets

The flicker and the MSFT/QQQ losses are **the same classifier failing in opposite
directions**: the label wobbling *off* a live trend in one case, holding onto a
*dead* one in the other. That coherence is why the v5.0 hold helps both ends —
holding a committed label through a stale tick is also holding it through the
noise that would otherwise have re-labelled a dying trend late.

**But that second half is a hypothesis, not a finding.** Nothing here shows the
MSFT/QQQ entries were mis-labelled. Every trade row carries `regime` and
`regime_conviction` **at entry**, so it is answerable from
`fleet_trades_2026-08-03.json` — now written — via menu **41**:

- entered on TRENDING with **high** conviction, then chopped → the classifier was
  wrong about the environment; look at the entry gate
- entered with conviction **barely over the 0.45 floor** → the gate let a marginal
  read through; look at the floor
- entered cleanly and the trend genuinely reversed → **nothing to fix; that is the
  business**

---

## WHAT EACH BUCKET IS EVIDENCE FOR

**Bucket 1 is evidence about the machine.** It tells us nothing about which
strategies work in which conditions, and every uncorrected Bucket-1 item makes
the Bucket-2 evidence noisier. Fix on sight.

**Bucket 2 is evidence about the market, and it is the entire point of the
current permissive posture.** MSFT and QQQ chopping through good setups is a data
point about continuation in a choppy tape. We want more of those, not fewer.

**The tightening decisions come later, from Bucket 2 only.** The relevant clocks:
**AV** revisits gap-class × outcome on **2026-08-13** (n≈40/cell, reads a 0.20 R
effect); the sentiment-score correlation revisits ~**2026-09-05**. Both need
accumulated sessions, and both are contaminated by anything left in Bucket 1.

---

*Filed 2026-08-03. Numbers reproducible from devtools 48, 41, 40 and
`tests/flicker_audit.py`. Note that `flicker_audit`'s window ran BEFORE tonight's
consolidation, so today's 88 trades are not yet in the 215 — a re-run now
includes them.*
