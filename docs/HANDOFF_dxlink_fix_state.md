# HANDOFF — DXLink session-exhaustion fix — state as of 2026-07-13 (night)

**Purpose: resume-from-here document.** If this thread dies, give this file (plus
`DIAGNOSIS_session_exhaustion_2026-07-13.md`) to the next session. Diagnosis SETTLED,
**cap MEASURED, Option 1b BUILT and offline-verified 11/11.** What remains is
deployment. Do not re-derive §1–§3.

---

## 1 · Incident + diagnosis (settled — do not re-diagnose)

2026-07-13: zero trades fleet-wide. Confirmed root cause: `options_chain.py` opened a
new DXLinkStreamer per 15 s tick per box (each open = fresh REST token + full WS
lifecycle); ~24 boxes' churn saturated TastyTrade's session pool. No client-side leak
(SDK 13.0.0 teardown verified clean); server-side 60 s keepalive windows × redial
cadence. **Kill mechanism (corrected):** regime never degraded — empty quote maps →
`mark=0.0` → the `mark > 0.05` liquidity filters rejected every strike in every
regime. Validate with marks + strike selection, never regime labels.

**Problem C** (AAPL/NFLX/TSLA/GLD crash loops, 17/17/17/14 restarts): poison candle
in the 1m table → `fetch_quote` ValueError → 30-error breaker → 7.5-min death cycles
(135 RTH min ≈ 17 ✓). Healed automatically by candle_feed ≥ v3.2 `purge_poison()` in
the fleet bake. No new work.

## 2 · The cap was MEASURED — this drove the design

**Option 1** (persistent streamer per box, `options_chain` v3.1) was built, verified,
and fleet-tested 07-13 afternoon. Result: with 29 candle-feeds holding sessions, only
**~6–11 of 29 chain streamers were ever admitted** (AMZN/CRM/DIA/LLY/MU/SMH stable;
AAPL/GS/PLTR/TLT/XOM connected-then-died; 16 locked out in backoff all afternoon).
**Empirical concurrent-session cap ≈ 40–45.** Option 1's 58 steady-state sessions do
not fit. v3.1 behaved perfectly within itself — backoff held retries at the 60 s cap
(~25 errs/30 min vs ~120 before), fail-loud refused every corpse chain — it is simply
arithmetic-blocked. **Jason green-lit Option 1b.**

## 3 · What is BUILT and VERIFIED (deploy these two files together)

**`data/candle_feed.py` v3.4** — chain marks on the feed's EXISTING socket:
- New store tables: `chain_subs` (single row: expiry + JSON symbol list, written by
  the bot) and `chain_marks` (latest bid/ask/greeks per streamer symbol, written by
  the feed; quote and greeks upserts each preserve the other's columns).
- `_reconcile_chain_subs()` every 2 s flush cycle: subscribes deltas; expiry rollover
  → `unsubscribe_all(Greeks/Quote)` + clear marks table + resubscribe. Socket
  reconnect resets chain state and re-reconciles (same path as candle resubscribe).
- Greeks/Quote events drain non-blocking each loop pass; marks ride the existing
  flush. **Candle logic byte-untouched** (verified by diff: only the import line and
  version banner changed).

**`data/options_chain.py` v3.2** — pure store reader; **the bot process now opens
ZERO DXLink connections** (import removed; `main.py` imports clean on 3.12 AND 3.14 —
and yes, removing the import initially reproduced the exact P0-1 annotation bug from
the 07-12 audit; caught by the 3.12 test discipline, annotations fixed):
- Publishes desired symbols+expiry to `chain_subs` (only on change); reads
  `chain_marks` with the staleness ceiling (`OT_CHAIN_STALE_S=120` — stale marks are
  refused, never served).
- Kept from v3.1: structure cache (`OT_CHAIN_STRUCT_REFRESH_S=1800`), zero-mark
  FAIL-LOUD — now **bootstrap-aware** (`OT_CHAIN_BOOTSTRAP_S=30`: quiet INFO while
  the feed populates after a fresh subscribe; ERROR after).
- Old feed on the box (≤v3.3) → helpful error: "is candle_feed v3.4 running?".

**Fleet steady state: exactly 29 DXLink sessions (one per box, the feed's).**
Verified offline 11/11 end-to-end (real FeedStore + real CandleFeed machinery driven
by a fake streamer + real reader): subs publish → feed subscribe (both types, exact
set) → events → flush → marks rows → chain built with correct mark/greeks →
steady-state reconcile subscribes nothing → expiry rollover unsubscribes+clears →
stale refusal → missing-table hint. Plus ORB 10/10, contract 17/17, theta 7/7.

## 4 · Fleet state right now

- 29 `optionsbot` units STOPPED (some may have been restarted for the v3.1 test —
  re-stop before baking). `candle-feed` units RUNNING everywhere (v3.3-era on 28
  boxes, whatever GOOGL has).
- Repo `origin/main` has everything through options_chain **v3.1**; v3.4 feed +
  v3.2 chain are in this session's outputs, NOT yet pushed.

## 5 · REMAINING STEPS

1. **Push BOTH files** to `github.com/TX-9AI/options_trader_v3` → `data/` folder:
   `candle_feed.py` (v3.4) + `options_chain.py` (v3.2). They ship as a pair — v3.2
   bot with v3.3 feed fails loud (safe, but trades nothing).
2. **Prove on ONE box** (any; QQQ-TEST fine). Single line:
   `cd ~/options-trader && git pull --ff-only && sudo systemctl restart candle-feed && sleep 5 && sudo systemctl restart optionsbot`
   (feed restart is safe: `subscribe_candle` backfills from the session start on
   reconnect). Acceptance after ~10 min RTH:
   - `journalctl -u optionsbot --since "-10 min" | grep -m1 "Chain subs published"` → once
   - `journalctl -u candle-feed --since "-10 min" | grep -m1 "chain marks: subscribed"` → present
   - `journalctl -u optionsbot --since "-10 min" | grep "Chain built" | tail -2` → real spot, real counts
   - `journalctl -u optionsbot --since "-10 min" | grep -c "exceeded the configured limit"` → 0
   - `ss -tn state established '( dport = :443 )' | tail -n +2 | wc -l` → ~1–3, flat
3. **Fleet bake** (devtools 25 RTH-safe / 23 after-hours) — rides with everything
   the 28 boxes still lack from 07-12/07-13. Then restart candle-feed AND optionsbot
   on all (feed restart is required for v3.4 tables/subscriptions):
   `python3 fleet.py run "cd ~/options-trader && sudo systemctl restart candle-feed && sleep 5 && sudo systemctl restart optionsbot"`
4. **Staged**: 5 boxes → 10 min watch (same acceptance) → remaining 24. Expected
   total account sessions: 29. Headroom vs measured cap: ~11–16.
5. After first clean session: exit_reason labels sane (F5 newly fleet-wide), replay
   diary L2 tracks flowing (devtools 40).

## 6 · Open threads (not blocking re-arm)

- **`verify_feed_v3.sh`** — not yet extended for chain_marks/chain_subs checks;
  worth one section once the fleet is stable (freshness + row counts).
- **`options_chain` v3.1** — superseded same-day by v3.2; its header records both.
  If anyone finds v3.1 running anywhere, it is safe (backoff + fail-loud) but
  session-hungry — upgrade it.
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
