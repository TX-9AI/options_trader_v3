# HANDOFF — DXLink session-exhaustion fix — state as of 2026-07-13 (evening)

**Purpose: resume-from-here document.** If this thread dies, give this file (plus
`DIAGNOSIS_session_exhaustion_2026-07-13.md`) to the next session. The diagnosis is
SETTLED and the fix is BUILT AND OFFLINE-VERIFIED; what remains is deployment and
live acceptance. Do not re-derive anything in §1–§3.

---

## 1 · Incident (settled — do not re-diagnose)

2026-07-13: zero trades fleet-wide. Root cause **confirmed against code + SDK 13.0.0
source**: `main.py:775` fetched the options chain every 15 s tick; `options_chain.py`
opened a **new DXLinkStreamer websocket per call** (each open also does a fresh
`GET /api-quote-tokens`). ~24 boxes × 4 dials/min saturated TastyTrade's unpublished
concurrent-session pool (protocol holds 60 s keepalive windows → each churning box
occupies 2–4 slots). **No client-side leak** — SDK teardown is clean; the pile-up is
server-side accounting + redial cadence. The outage was **self-sustaining**: every
rejected retry is itself a short-lived session.

**Kill mechanism (CORRECTED from the original handoff):** the regime never degraded —
the classifier consumes nothing chain-derived. Empty quote maps → every contract kept
`mark=0.0` → the `mark > 0.05` liquidity filters (`options_chain.py` strike
selectors) rejected **every strike in every regime**. Fleet table showed
RANGING/COMPRESSION, not UNKNOWN. **Post-fix validation watches marks + strike
selection, NOT regime labels.**

**Problem C (4 crash-looping boxes — AAPL/NFLX/TSLA/GLD):** separate, already
understood. 30-error breaker × 15 s = 7.5-min death cycles; 135 RTH minutes ≈ 17
restarts (matches the table). Cause: poison candle in the **1m** table →
`fetch_quote` ValueError, which fires **before** the GEX fetch (hence sess_errs=0,
blank regime). Remedy: the already-shipped candle_feed v3.2/v3.3 + `purge_poison()`
(currently only on GOOGL). Verify per box:
`sqlite3 ~/options-trader/data/feed_store.db "SELECT tf, COUNT(*) FROM candles WHERE ts > 2000000000000 GROUP BY tf"`
— expect `1m` rows on exactly those four.

## 2 · Decision (made by Jason)

**Option 1** — persistent per-box chain streamer — plus two riders (structure-fetch
throttle, zero-mark fail-loud). Option 1b (fold Greeks/Quote into candle-feed; 29
total sessions) is the agreed **future destination**, deliberately deferred: it
touches candle_feed, the one component that worked flawlessly through the incident.
Option 2 (centralize on control) REJECTED: SPOF + control is credential-free by
design. Option 3 (REST Greeks) rejected as primary.

## 3 · What is BUILT and VERIFIED (this session)

**`data/options_chain.py` v3.1** — complete file delivered to outputs. Changes:
1. ONE persistent `DXLinkStreamer` per process (lazy connect on the shared
   tasty_client loop thread, held via `AsyncExitStack`). Subscriptions reconciled
   (only never-seen symbols subscribed); **expiry rollover** unsubscribes all +
   clears maps (bots run continuously across days).
2. **Reconnect backoff** 5s→60s cap (env: `OT_CHAIN_RECONNECT_BASE_S/_MAX_S`) — a
   saturated pool is never hammered at tick cadence again.
3. Latest-value Greeks/Quote maps persist across ticks (non-blocking drain per tick;
   brief blocking collect only for never-seen symbols). **Staleness ceiling**
   `OT_CHAIN_STALE_S=120`: stream down + old marks → refuse to serve them.
4. **FAIL-LOUD:** a built chain with zero live marks returns `None` + ERROR log
   (never again a plausible-looking corpse). `None` is also strictly safer for an
   open position than zero marks (premium=0 would trip the −25% floor on garbage).
5. Chain **structure** (REST strike list) cached `OT_CHAIN_STRUCT_REFRESH_S=1800` —
   static intraday; marks ride the stream.

**Verified offline (12/12):** persistent reuse (1 instance across ticks) · zero new
subscriptions on steady-state ticks · structure REST cached · expiry rollover
unsubscribe · fail-loud on dead stream · backoff blocks redial + doubles ·
reconnect after backoff · healthy pass resets backoff · stale-mark refusal. Plus:
py_compile on 3.12 AND 3.14 · `main.py` imports clean · ORB 10/10, contract 17/17,
theta 7/7 suites pass. **NOT yet tested against live DXLink** — that is the next step.

**Steady state after deploy: 2 sessions/box (candle-feed + chain), zero churn.**

## 4 · Fleet state right now

- All 29 `optionsbot` units **STOPPED** (~11:50 ET); boxes up; `candle-feed` units
  RUNNING (innocent — their persistent sessions are stable).
- 28 boxes on `818d312` — these LACK: market_data v3.1, candle_feed v3.2/v3.3
  (poison guard + cross-thread fix), butterfly/main v3.1, and everything from the
  07-12 remediation batch that landed after their last bake.
- GOOGL on `a42445e` (has Fable's 07-13 fixes, not options_chain v3.1).
- Session pool: draining since the stop; hours of margin by re-arm time.

## 5 · REMAINING STEPS (in order)

1. **Push `options_chain.py` v3.1** (from outputs) to
   `github.com/TX-9AI/options_trader_v3` → `data/` folder, replacing the existing
   file. (Web upload as usual.)
2. **Prove on ONE box** (QQQ-TEST, ip 3.144.75.22, or GOOGL) during RTH Tue 07-14:
   ```
   cd ~/options-trader && git pull --ff-only && find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null; sudo systemctl restart optionsbot
   ```
   Acceptance (30+ min): `journalctl -u optionsbot --since "-30 min" | grep -c "exceeded the configured limit"` → **0** ·
   `journalctl -u optionsbot --since "-30 min" | grep -m1 "Chain streamer CONNECTED"` → present once ·
   `journalctl -u optionsbot --since "-10 min" | grep -m3 "Chain built"` → spot and marks nonzero ·
   `ss -tn state established '( dport = :443 )' | tail -n +2 | wc -l` → small and FLAT across checks (was climbing/churning before).
3. **Fleet bake (item 25, RTH-safe, or 23 after hours)** — v3.1 rides along with
   everything else the 28 boxes are missing (poison fix heals problem C
   automatically; `purge_poison()` runs at feed start).
4. **Staged restart:** 5 boxes → watch 10 min for session errors → remaining 24.
   If 58 stable sessions still brushes the cap (not expected — last week ran 29
   persistent + heavy churn), the escalation path is Option 1b.
5. **After first clean session:** confirm exit_reason labels look right (F5 fix is
   also newly live fleet-wide) and the replay diary picks up L2 tracks (item 40).

## 6 · Open threads (not blocking re-arm)

- **Option 1b** (Greeks/Quote into candle-feed; 29 sessions total) — the doctrine
  completion. Build unhurried behind `verify_feed_v3.sh`.
- **Problem C verification** — run the sqlite one-liner on AAPL/NFLX/TSLA/GLD to
  confirm the 1m-table hypothesis (curiosity only; the fix ships regardless).
- **`observer/` tarballs** (defect D) — still ungreppable; confirmed nothing in the
  importable tree opens a third DXLink stream, but the tarballs remain unaudited.
- **Session cap** — unpublished (searched dev docs/SDKs/help center). Design margin,
  not knowledge: 29 proven safe for weeks, 58 almost certainly fine, churn never again.
- The full 07-12 audit findings register (F4 named-levels starvation, F27 condor
  Leg-2 gates, etc.) lives in `AUDIT_options_trader_v3_2026-07-12.md` — untouched by
  this incident.

## 7 · Standing constraints (unchanged)

Complete files only, never patches · version header bumped on every change · clone
repo + read HEAD before writing · single-line commands for mobile · PAPER_TRADING
default True · trading/risk/strategy logic untouched (this was transport-only) ·
one box proves it before the fleet.
