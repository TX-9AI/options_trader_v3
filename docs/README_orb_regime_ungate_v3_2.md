# ORB Regime Un-Gate — v3.2 (2026-07-11)

## Scope

Lets the flagship **5-minute ORB break-and-retest fire regardless of the regime
label** — including `UNKNOWN` and `SWEEP_REVERSAL` — behind a single config
switch. The ORB engine's break+retest is self-validating; the classifier does
not even test for it, so the label is not consulted for the go/no-go decision.

This pass sits **on top of the v3.1 stop rework** (`orb_engine` + `exit_engine`).
Deploy them together — the four files below are the complete, consistent set.

Files:

- `config.py` — new switch `ORB_FIRES_REGARDLESS_OF_REGIME` (default `True`)
- `main.py` (v3.2) — dispatch un-gate
- `analysis/orb_engine.py` (v3.2) — stop rework (v3.1) **+** sweep-deferral guard
- `execution/exit_engine.py` (v3.1) — structure stop (from the stop-fix pass, unchanged)

**Not included (still queued):** the ORB-target-path conviction haircut and the
proximity-graded sweep demotion. Those touch scoring, not gating, and are a
separate pass.

---

## Why this exists

The ORB is the highest-quality, fully mechanical setup in the book, and v2 was
blocking it: during the opening-range window the classifier frequently returns
`UNKNOWN` (a single 5m frame early in the session rarely resolves to a named
regime), and `UNKNOWN` was a hard no-trade. So the best setup was being gated by
a label that says nothing about whether the setup is present.

The fix is one rule: **a confirmed ORB fires regardless of the label.** The
break+retest is the edge; the regime dimension becomes a *scoring input*, not a
veto.

---

## What changed

### `config.py`

```python
ORB_FIRES_REGARDLESS_OF_REGIME = True   # set False to restore strict v2 gating
```

### `main.py` (v3.2) — `run_entry_logic`

Two edits, both switch-gated:

1. **Hard UNKNOWN gate bypassed for a confirmed ORB.** The `UNKNOWN`/undefined
   no-trade gate no longer vetoes when the engine is in a confirmed `OPEN_LONG`/
   `OPEN_SHORT` state. A genuinely unclassified tape with *no* ORB setup still
   blocks (only a proven setup bypasses).
2. **ORB dispatch admits `UNKNOWN` and `SWEEP_REVERSAL`.** A confirmed ORB now
   dispatches under those labels too (previously only TRENDING/BREAKOUT/RANGING/
   COMPRESSION).

### `analysis/orb_engine.py` (v3.2)

The retest confirm previously **deferred** (left the setup awaiting retest)
whenever the regime was `SWEEP_REVERSAL`, so a sweep label suppressed a valid
ORB. Now guarded by the switch: with it on, the engine confirms OPEN under a
sweep label so the dispatch can fire it — **ORB beats sweep.** (The v3.1 stop
logic is unchanged.)

---

## Expected behavior (verified truth table)

| regime label | ORB engine confirmed? | switch | outcome |
|---|---|---|---|
| UNKNOWN | yes | **on** | **ORB fires** |
| UNKNOWN | yes | off | blocked (v2 behavior) |
| UNKNOWN | no | on | blocked (no setup to bypass) |
| SWEEP_REVERSAL | yes | **on** | **ORB fires (beats sweep)** |
| SWEEP_REVERSAL | yes | off | falls to sweep strategy (v2 behavior) |
| RANGING / COMPRESSION / TRENDING / BREAKOUT | yes | either | ORB fires (unchanged) |
| None / undefined | — | on | blocked (no crash) |

What does **not** change:

- **The setup scorer still governs.** A confirmed ORB under `UNKNOWN` still has to
  clear the B threshold. `regime_conviction` simply contributes 0 (its 0.20
  weight), so only ORBs that earn a B on break quality + VWAP + liquidity + macro
  fire; marginal ones are still refused. The scorer *is* the consensus filter.
- **Exits are unchanged.** v3.1 structure stop (close beyond the impulsive origin)
  + the unconditional −25% premium floor. The un-gate changes entry, not exit.
- **Sweep / butterfly / condor are untouched.** They self-gate on their own regime
  values and do not fire under `UNKNOWN`. This pass only frees the ORB.

---

## Interaction with the shadow observer

Every ORB that fires under `UNKNOWN` is logged with `regime=UNKNOWN` on the trade
record. That is precisely the labeled tape the shadow subsystem exists to
capture: it can now record the Layer-1 confluence scores (`regime_confluence`)
and raw factors at the moment an `UNKNOWN`-labeled ORB fires and resolves, which
is the corpus the v3 conviction integrator needs to be calibrated against. In
other words, un-gating the ORB is also what starts *feeding* the shadow program
the exact population v2 was starving it of.

---

## What this does and does not establish

- **Verified:** the gate logic (all 9 regime/state/switch combinations), the
  engine confirming OPEN under a sweep label, syntax and imports across all four
  files. The un-gate does what it says and is fully reversible via the switch.
- **Not established here:** that the newly-fired ORBs are net-profitable. That is
  a **paper-forward** question — option-premium P&L can't be reconstructed from
  underlying OHLC. The posture is deliberate: these are lower-information trades
  (the tape was `UNKNOWN`), taken to generate labeled data, with the scorer's
  B-threshold and the v3.1 stops containing the downside. Expect a lower hit rate
  than regime-confirmed ORBs; that's the point.
- **Reminder on single-day tape:** the classifier is starved on one session, so
  the exact "how often was the ORB window `UNKNOWN`" rate is only reliable live —
  which the shadow program will now measure directly.

---

## Deploy

All four files are one consistent set (v3.1 stops + v3.2 un-gate). Ship together:

```
scp config.py   <box>:<repo>/config.py ;
scp main.py     <box>:<repo>/main.py ;
scp orb_engine.py  <box>:<repo>/analysis/orb_engine.py ;
scp exit_engine.py <box>:<repo>/execution/exit_engine.py ;
```

No new dependencies, no schema changes. To roll back the un-gate alone, set
`ORB_FIRES_REGARDLESS_OF_REGIME = False` (restores strict v2 gating; the v3.1 stop
rework stays in force). Restart the bot service to load the changes; confirm
`PAPER_TRADING` is set as intended before the first session.
