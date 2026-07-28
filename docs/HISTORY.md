# HISTORY — incidents, audits, and completed specs

Resolved work, kept for the record. Read before re-litigating a fix: these describe why things are the way they are.

**Consolidated 2026-07-28.** Nothing was rewritten or summarised — each
former file is preserved verbatim as a section below, so historical
decisions stay on the record and fixes don't get quietly reverted.

## Contents

- **options_trader v3.0 — CHANGELOG**  <sub>(was `docs/CHANGELOG.md`)</sub>
- **DIAGNOSIS RESPONSE — DXLink session exhaustion — 2026-07-13**  <sub>(was `docs/DIAGNOSIS_session_exhaustion_2026-07-13.md`)</sub>
- **HANDOFF — DXLink session-exhaustion fix — state as of 2026-07-13 (night)**  <sub>(was `docs/HANDOFF_dxlink_fix_state.md`)</sub>
- **AUDIT — Paper→Live behavioral divergence · 2026-07-15**  <sub>(was `docs/AUDIT_paper_live_divergence_2026-07-15.md`)</sub>
- **AUDIT — Header/Changelog Compliance + Stale-Reference Sweep — 2026-07-23**  <sub>(was `docs/AUDIT_header_compliance_2026-07-23.md`)</sub>
- **FABLE SPEC — Live exit fill-confirmation (`_confirm_and_book_live_exit`)**  <sub>(was `docs/FABLE_SPEC_live_exit_fill_confirmation.md`)</sub>

---


<!-- ================= was: docs/CHANGELOG.md ================= -->

##### options_trader v3.0 — CHANGELOG
**2026-07-10 — Yahoo-Finance purge & data stream mapping optimization**
Built against options_trader_v2 `main` @ HEAD `a181dd2fd10c2f8c7c1cb97792edcea565afc71c`.
v2 repo preserved untouched; this tree is the new v3 repo root.

##### Why
The bot trades and logs on TastyTrade (DXLink/DXFeed) candles, but market data
was pulled from the legacy Yahoo-Finance client — a different series that
provably diverges from the traded tape (caught on the 5-minute opening range).
Every process now derives its data from the same TastyTrade feed the bot
trades on. The purge is total: the legacy-source residue grep (§6.4 of the
purge spec, run via `tests/verify_feed_v3.sh`) returns zero hits across code,
config, shell, docs, and requirements — including this changelog.

##### Architecture (one producer, many readers — per box)
- **NEW `data/candle_feed.py` v3.0 + `candle-feed.service`** — owns the box's
  ONLY DXLinkStreamer subscription: this box's symbol across 1m/5m/15m/1h/1d
  plus VIX (1m/1d). Per-interval backfill (session open for 1m; deeper for
  higher TFs), last-write-wins bar correction, reconnect w/ backoff, bounded
  rolling history, reuses get_session()/get_loop(). Persists to SQLite (WAL):
  `candles(symbol,interval,ts_epoch_ms,o,h,l,c,v)` + `feed_meta` (per-interval
  last_write + global heartbeat). Index boxes: `OT_DXFEED_SYMBOL` override;
  store path override: `OT_FEED_DB`.
- It is FORBIDDEN for any consumer (bot, shadow observer, candle logger,
  query tools) to open its own DXFeed stream.

##### Changed files (logic)
| File | v | Change |
|---|---|---|
| `data/candle_feed.py` | 3.0 | NEW — single producer service |
| `deploy/candle-feed.service` | 3.0 | NEW — reference unit (setup_ec2 generates the real one) |
| `data/market_data.py` | 3.0 | Rewritten as store READER. Contract preserved exactly: `fetch_candles`/`fetch_quote`/`fetch_all_candles` signatures + return shapes unchanged. Fail loud: None + WARNING on missing store or heartbeat > `OT_FEED_STALE_S` (120s). Young session returns real partial data; intraday windows never padded across the overnight gap (`OT_FEED_INTRADAY_SCOPE=continuous` escape hatch). Yahoo period map deleted. |
| `data/macro_data.py` | 3.0 | VIX via `fetch_quote("VIX")` (store-first, TastyTrade REST secondary — the one sanctioned non-DXFeed fallback). Stale→default-20 chain preserved, now WARNING-level. |
| `data/candle_logger.py` | 3.0 | Converted to store CONSUMER (no second subscription); same CSV output; its old subscribe/drain moved into candle_feed as a persistent stream. |
| `data/data_cache.py` | 3.0 | ONE surgical fix (staleness guard): refresh failing past 3× staleness ceiling ⇒ `get()` returns None — a dead feed can no longer be masked by an aging cached frame. |
| `setup_ec2.sh` | 3.2 | Yahoo dep dropped; installs/enables candle-feed.service; optionsbot `After=`/`Wants=` candle-feed; feed starts first. |
| `requirements.txt` | — | Yahoo dep removed; no new deps (sqlite3 stdlib). |
| `deploy/candle-logger.service` | 3.0 | Consumer notes; no creds needed by logger. |
| `test_candle_logger.py` | 3.0 | Rewritten for store-consumer design (synthetic store, offline). |
| `tests/test_market_data_contract.py` | 3.0 | NEW — seam contract acceptance test (§6.1), offline. |
| `tests/verify_feed_v3.sh` | 3.0 | NEW — ON-BOX acceptance gate: single-subscription proof, store health, ORB equivalence, zero-Yahoo grep. |

##### Comment/doc scrubs (no logic change)
`analysis/get_orb_range.py` (v3.0 entry), `analysis/orb_engine.py`,
`README.md` (v3.0 changelog + deps), `deploy/README_candle_logger.md`.

##### Repo-wide v3.0 bump (no logic change)
Every remaining .py/.sh received a `v3.0 — 2026-07-10` changelog entry citing
the purge, with title versions set to v3.0: all engines, strategies,
execution, risk, notifications, database, utils, main.py, config.py, query.py,
status.py, eod_summary.py, and all shell tooling.

##### NOT touched
Trading/risk/execution/strategy logic, `PAPER_TRADING` default (True),
Telegram, broker reconciliation, GEX, ORB engine logic — all behavior
unchanged above the data seam. The off-repo shadow observer rides the
preserved `get_cache()` seam with zero changes (restart it after deploy).

##### Verification status
- §6.1 Contract test: **17/17 PASS** offline (`python -m tests.test_market_data_contract`).
- §6.4 Zero-Yahoo grep: **CLEAN** repo-wide.
- §6.2 ORB equivalence + §6.3 single-subscription proof: **ON-BOX gates** —
  run `bash tests/verify_feed_v3.sh` on one box during RTH (paper) before
  fleet deploy. Also confirms backfill depth per interval (entitlement) and
  VIX entitlement per the candle_feed FIRST-RUN CHECKLIST.

---


<!-- ================= was: docs/DIAGNOSIS_session_exhaustion_2026-07-13.md ================= -->

##### DIAGNOSIS RESPONSE — DXLink session exhaustion — 2026-07-13

Verified against fleet HEAD `818d312` in a pinned worktree, the GOOGL HEAD `a42445e`,
and the **actual installed tastytrade SDK 13.0.0 source** (not its docs). Verdict up
front: **§3 is CONFIRMED with one correction and one addition. §1's causal chain is
half wrong — the mechanism that blocked the trades is not the regime.** Details, then
solutions.

---

##### 1 · The three questions, answered from code

##### Q1 — Is `fetch_chain()` genuinely opening a new DXLinkStreamer per tick?

**YES — confirmed, and it's worse than stated.** `main.py:775` calls
`get_chain_fetcher().fetch_chain()` under the comment "*Compute GEX every tick*",
unconditionally, every 15 s poll. That reaches `_async_fetch_greeks_quotes`
(`options_chain.py:218`): `async with DXLinkStreamer(session)` per call.

The addition: SDK 13.0.0's context entry does a **fresh REST call
(`GET /api-quote-tokens`) on every open** before dialing the websocket. So each tick
is: REST token fetch → TCP+TLS+WS handshake → SETUP → AUTH → subscribe → collect →
teardown. Per box, ~4 full connection lifecycles per minute, ~1,560 per RTH session.
×24–28 boxes.

`main.py:471` (entry path) is NOT a second churn source — `ctx.get("chain") or fetch`
reuses the tick's chain. Position management receives the same `ctx["chain"]`.

##### Q2 — Anything else opening DXLink connections?

**NO.** Full-tree enumeration at `818d312`: exactly two live openers —
`candle_feed.py:327` (persistent, one per box, correct) and `options_chain.py:218`
(per-tick, the problem). `gex_data` consumes the chain (confirmed — no streamer).
`check_sdk.py` is a manual diagnostic. The `observer/` tarballs cannot be grepped
(defect D) — if the shadow subsystem is running anywhere, it is unaudited; worth one
`fleet.py run "ss -tnp | grep -c 443"`-style check, but nothing in the *importable*
tree opens a third stream.

##### Q3 — Is there a teardown/close() bug making sessions leak?

**NO client-side leak — read the SDK's actual lifecycle.** `__asynccontextmanager__`
nests `AsyncClient` → `aconnect_ws` → `create_task_group`. On BOTH the happy path and
the error path (the `_reader` task raises `TastytradeError("Fatal streamer error: …")`
on the ERROR frame — which surfaces exactly as your logged *"unhandled errors in a
TaskGroup (1 sub-exception)"*), the stack unwinds through the context managers and the
websocket is closed. Python is releasing the sockets.

**The pile-up is server-side accounting, and the protocol explains it.** The SDK's
SETUP message negotiates `keepaliveTimeout: 60` — DXLink holds a session slot up to
60 s around each connection's lifecycle. With a 15 s redial cadence, each churning box
plausibly occupies **2–4 session slots at once** (one live + recently-closed slots
still inside their timeout window). 24 churning boxes × 2–4 + 29 persistent
candle-feeds ≈ **75–140 slots demanded** against an unpublished cap. I searched; the
cap is genuinely not published anywhere (developer docs, SDK repos, help center). We
know only: 29 persistent feeds alone ran fine for weeks → cap > 29; last-week's
steady state with churn also ran → the tip into failure was likely marginal.

**This also explains your two dead ends.** Restarting one box does nothing because the
pool is an account-level resource kept saturated by everyone else's redials. And the
failure is self-sustaining: **every rejected attempt is itself a short-lived session**
(the ERROR arrives after connect), so 24 boxes retrying every 15 s hold the pool at
the ceiling indefinitely. It will not heal while the bots run. Stopping the fleet was
the right call and is the only thing that drains it.

---

##### 2 · CORRECTION to §1 — the causal chain that actually blocked the trades

The handoff's chain says: *no Greeks → GEX empty → regime degrades to UNKNOWN →
hard gate → no trades.* **The regime link is wrong, and your own fleet table proves
it:** most boxes sat in RANGING/COMPRESSION, not UNKNOWN.

The classifier's signature is `classify(vol_state, trend_state, structure, liq_map,
macro, trigger)` — **it consumes nothing chain- or GEX-derived.** Regimes were
computed normally all day off the (healthy) candle store. The GOOGL log line you
quoted is that one box's dispatch message, not the fleet mechanism.

**The real kill path is the liquidity filter.** With the streamer rejected,
`_fetch_greeks_and_quotes` returns `({}, {})`, `_apply_market_data` never runs a
merge, and every contract keeps `mark = 0.0`. Then:

- `options_chain.py:299` — `candidates = [c for c in contracts if c.mark > 0.05]` → **empty**
- `options_chain.py:327` — sweep delta-band: `c.mark > 0.05 and 0 < |delta| ≤ 0.55` → **empty** (delta is also 0)
- `:353/:356` — condor legs: `c.mark > 0` → **empty**

So in **every** regime, every strategy's strike selection returned nothing and
`generate_signal` returned None — a perfectly plausible-looking "no setup" day.
Butterflies were additionally dead at the GEX gate (no gamma → no PINNING). Spot~$0
is cosmetic fallout (`spot_price` comes from the ATM-call scan at `:165`, which needs
deltas).

**Why this correction matters:** when validating the fix, the green signal is
**marks > 0 and a successful strike selection log**, not regime labels. Watching
regimes would pass/fail for the wrong reasons.

---

##### 3 · Problem C (the four crash-loopers) — explained, no new work needed

AAPL/NFLX/TSLA (17 restarts), GLD (14), blank regime, `sess_errs = 0`. The math
identifies the cause: the loop's error breaker exits the process at **30 errors**, one
per 15 s tick = **7.5 min per death cycle** (+ restart delay). RTH 9:30 → sweep at
~11:45 is 135 min ≈ **17–18 cycles. The table says 17 and 14.** That is the
poison-candle kill loop (`fetch_quote` → year-2038 row wins "latest", `close=0.0` →
`ValueError` in `run_analysis`) — which fires **before** the GEX fetch in the tick,
which is exactly why those four boxes show `sess_errs = 0` and blank regime.

Hypothesis for why only these four of 28 poison-carrying boxes crash-loop: their
poison row landed in the **1m** table (the one `fetch_quote` reads); the other boxes'
poison sits in other timeframes. One-line verification per box:
`sqlite3 ~/options-trader/data/feed_store.db "SELECT tf, COUNT(*) FROM candles WHERE ts > 2000000000000 GROUP BY tf"`
— expect `1m` rows on exactly AAPL/NFLX/TSLA/GLD.

**Remedy: the already-shipped candle_feed v3.2/v3.3 + `purge_poison()`** (running on
GOOGL). These four need the fleet bake, nothing new. Do not build anything for C.

---

##### 4 · Solutions, with tradeoffs

**Option 2 (centralize chain on control) — REJECT.** Single point of failure for 29
deliberately-independent bots, and 1-REPORTER is credential-free by design
(`validate_regime.sh`: "no credentials, no live path"). Breaking that isolation to
dodge a session cap is trading a transport problem for an architecture regression.
Keep in the drawer only if the cap proves brutally low (<40).

**Option 3 (REST for Greeks/marks) — REJECT as primary, keep as backstop.** Marks via
REST exist (the `fetch_quote` fallback already uses it). Greeks via REST: could not
confirm availability; moot under the recommendation below. REST polling for 110
strikes per box per tick would just move the throttling problem to the REST rate
limiter.

**Option 4 (throttle chain fetches) — necessary hygiene, insufficient alone.** The
chain *structure* is static intraday and never needed re-fetching every 15 s. But
while HOLDING a position the exit engine prices premiums off chain marks every tick —
throttling stales the exact data the −25% floor and trails read. Any throttle must be
state-aware (flat: slow; in-position: fast), at which point in-position churn returns.
Component, not solution.

**Option 1 (persistent per-box chain streamer) — the RIGHT SHIP-TONIGHT FIX.** One
long-lived `DXLinkStreamer` inside `options_chain`, opened lazily on first use,
subscriptions updated (subscribe new strikes / unsubscribe stale) instead of
reconnecting, reconnect-with-backoff on error. Steady state: **58 persistent sessions
(2/box), zero churn.** Risk: the cap is unknown — 58 could still sit above it. But the
evidence is on our side: last week ran 29 persistent + heavy churn without errors, so
the cap comfortably exceeds 29 + churn-overlap; 58 clean sessions is *less* demand
than that. Smallest change, contained in one file, per-box isolation untouched,
provable on one box in minutes.

**Option 1b (consolidate Greeks/Quote into candle-feed) — the RIGHT DESTINATION.**
The handoff names the gap itself: v3.0 consolidated **candles only**. Doctrine says
one producer, many readers — finish it: candle-feed subscribes Greeks+Quote for the
box's chain symbols on its **existing** socket, writes them to the store;
`options_chain` becomes a pure store reader like `market_data`. **29 total sessions —
the number proven safe for weeks.** Cost: bigger build — a desired-symbols handshake
(options_chain writes the strike list to a store table; the feed reconciles
subscriptions each flush cycle), a greeks/quotes schema, staleness semantics, and
`verify_feed_v3.sh` extensions. Touches the most protected file on the box.

##### Recommendation

**Ship Option 1 now, schedule 1b as the v3 completion.** Tonight's goal is trading
tomorrow with zero churn and minimal blast radius; that is Option 1 in one file
(`options_chain.py`), testable on QQQ-TEST against live DXLink before any fleet
motion. 1b is the architecturally correct end state but touches candle_feed — the one
component that worked flawlessly today — and deserves an unhurried build + the
verify-feed acceptance gate, not a market-holiday-eve rush. If you want, 1 → 1b
becomes invisible later: consumers never see the transport.

Add one cheap piece of Option 4 to Option 1 regardless: rebuild the chain
*structure* (REST strike list) at most every N minutes; the persistent stream keeps
Greeks/marks per-tick fresh continuously. And one **fail-loud guard** (today's real
lesson): if a built chain has zero contracts with `mark > 0`, log ERROR and return
`None` instead of a plausible-looking dead chain — `attempt_new_entry` already
handles a None chain correctly. Silent structural validity with dead values is what
hid this for five hours.

---

##### 5 · Re-arm sequence (proposed — no action taken)

1. Fleet stays STOPPED (bots). Candle-feeds keep running — they are innocent and
   their sessions are stable.
2. Let the pool drain ≥ 15 min from the last bot stop (covers any lingering timeout
   windows several times over).
3. I build Option 1 (+ zero-mark fail-loud + structure-refresh throttle) as a
   complete `options_chain.py`, versioned, with an offline test + a live single-box
   acceptance script.
4. Prove on QQQ-TEST during RTH: `sess_errs = 0` over 30+ min, marks > 0, one
   successful strike-selection log, `ss -tn | grep -c :443` shows exactly 2
   persistent connections.
5. Bake fleet-wide **together with the already-shipped v3.1–v3.3 + butterfly fix**
   (28 boxes are still on `818d312` and carry the poison landmine + the four
   crash-loopers).
6. Restart the fleet staged — 5 boxes, watch 10 min, then the rest — so if 58
   sessions does brush the cap, it shows up at +10, not +29.

**Awaiting your go on Option 1 before writing any code.**

---


<!-- ================= was: docs/HANDOFF_dxlink_fix_state.md ================= -->

##### HANDOFF — DXLink session-exhaustion fix — state as of 2026-07-13 (night)

**Purpose: resume-from-here document.** If this thread dies, give this file (plus
`DIAGNOSIS_session_exhaustion_2026-07-13.md`) to the next session. Diagnosis SETTLED,
**cap MEASURED, Option 1b BUILT and offline-verified 11/11.** What remains is
deployment. Do not re-derive §1–§3.

---

##### 1 · Incident + diagnosis (settled — do not re-diagnose)

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

##### 2 · The cap was MEASURED — this drove the design

**Option 1** (persistent streamer per box, `options_chain` v3.1) was built, verified,
and fleet-tested 07-13 afternoon. Result: with 29 candle-feeds holding sessions, only
**~6–11 of 29 chain streamers were ever admitted** (AMZN/CRM/DIA/LLY/MU/SMH stable;
AAPL/GS/PLTR/TLT/XOM connected-then-died; 16 locked out in backoff all afternoon).
**Empirical concurrent-session cap ≈ 40–45.** Option 1's 58 steady-state sessions do
not fit. v3.1 behaved perfectly within itself — backoff held retries at the 60 s cap
(~25 errs/30 min vs ~120 before), fail-loud refused every corpse chain — it is simply
arithmetic-blocked. **Jason green-lit Option 1b.**

##### 3 · What is BUILT and VERIFIED (deploy these two files together)

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

##### 4 · Fleet state right now

- 29 `optionsbot` units STOPPED (some may have been restarted for the v3.1 test —
  re-stop before baking). `candle-feed` units RUNNING everywhere (v3.3-era on 28
  boxes, whatever GOOGL has).
- Repo `origin/main` has everything through options_chain **v3.1**; v3.4 feed +
  v3.2 chain are in this session's outputs, NOT yet pushed.

##### 5 · REMAINING STEPS

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

##### 6 · Open threads (not blocking re-arm)

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

##### 7 · Standing constraints (unchanged)

Complete files only, never patches · version header bumped on every change · clone
repo + read HEAD before writing · single-line commands for mobile · PAPER_TRADING
default True · trading/risk/strategy logic untouched (this was transport-only) ·
one box proves it before the fleet.

---


<!-- ================= was: docs/AUDIT_paper_live_divergence_2026-07-15.md ================= -->

##### AUDIT — Paper→Live behavioral divergence · 2026-07-15

**Scope:** every `paper_trading` / `PAPER_TRADING` / `paper_trade` branch in the
repo, plus every live order-placement and P&L-booking path, audited for
behavior that changes — or breaks — when `OT_PAPER_TRADING` flips to `False`.
Prompted by the 15:45 hard-close `$0.00` booking bug (fixed in exit_engine
v3.4/v3.5): the question was *what else is of that species*.

**Verdict in one line:** the EXIT side is now fill-confirmed and safe (v3.5),
the reconcile side recovers truth (v3.6) — but the **ENTRY side has the same
submission-equals-fill disease**, the **broken-wing roll opens a fictional
position in live**, and **paper and live rows share one trades.db with no mode
filter**, so two weeks of paper history will contaminate the live daily-loss
breaker on day one.

Files audited: `main.py`, `execution/entry_engine.py`, `execution/exit_engine.py`,
`execution/position_manager.py`, `execution/broker_reconcile.py`,
`strategy/condor_roll.py`, `database/trade_logger.py`, `risk/risk_manager.py`,
`risk/session_guard.py`, `data/tasty_client.py`, `notifications/alert_manager.py`,
`status.py`, `eod_summary.py`, `query.py`, `config.py`, `configure.sh`.

---

##### 🔴 CRITICAL — will misbehave or lose position-truth in live

##### L1 — Entries book on SUBMISSION, not on broker fill (all three entry paths)

The entry side never got the FillResult treatment. Every live entry path
records the position as open — at a price that is not the fill — the moment
the order is *accepted*, exactly the class of bug that produced the $0.00
exits.

**L1a · Condor legs** (`main._execute_condor_leg`): places the 2-leg vertical
as a LIMIT at mid-credit, then books
`fill_credit = response.order.price or net_credit` immediately. `.price` on a
just-placed order is the *limit you asked for*, not a fill, and a mid-credit
limit is precisely the kind of order that sits unfilled. Consequences of a
never-filled entry: a DB position that does not exist at the broker, managed
every tick, "closed" at 15:45 with real close orders the broker rejects, and
`notify_leg_filled()` advances the condor legging state machine on a fill that
never happened — Leg 2 can arm off a fictional Leg 1.

**L1b · Single legs** (`entry_engine._place_single_leg`): MARKET order, then
`fill_price = float(placed.price or signal.entry_premium)`. A market order has
no `.price`, so this **always** books the signal-time mark as the entry — the
recorded entry premium in live is never the actual fill. Stops/targets and P&L
all key off a number the broker never printed. (Market orders nearly always
fill, so position existence is usually fine — the *price* is what's wrong.)

**L1c · Butterfly** (`entry_engine._place_butterfly`) — broken three ways:
1. **Wrong price sign.** The debit is sent as a POSITIVE `price` with
   `price_effect=DEBIT`. Verified against the SDK (v8+ through 13.x):
   `NewOrder.price` is **signed** (negative=debit, positive=credit) and
   `price_effect` is silently ignored. A positive-priced opening fly demands a
   *credit* to buy a debit spread — it will never fill.
2. **Fill check that can't succeed.** It reads `placed.status` immediately
   after submission, looking for "Filled" — the status at that instant is
   Received/Routed. So even a correctly priced order goes: place → sleep →
   cancel → re-place → cancel → give up.
3. **Double-position race.** If the first order fills during the sleep, the
   `delete_order` fails (exception swallowed with `pass`) and attempt 2 places
   a **second** butterfly.

**Fix shape:** an entry-side mirror of exit_engine v3.5 —
`_confirm_entry_fill(order_id)` polling to a bounded deadline, record written
ONLY on a confirmed fill at the broker's per-leg net fill price, signed limit
prices, cancel-and-resolve on timeout. Until then the deliberate "entry logic
is v2.5" stance in the README should be read as **live entries are not
validated**.

##### L2 — Broken-wing roll opens a FICTIONAL vertical in live

`strategy/condor_roll._execute_roll` step 2 carries the comment "*live order
placement mirrors _execute_condor_leg*" — **but no order is placed**. The code
writes the rolled vertical's DB record and moves on. In live: the real
untested vertical is closed (correctly, fill-confirmed via v3.5), then the bot
books and "manages" a new vertical that was never opened at the broker. The
rolled structure's risk-free math is fiction; reconcile will eventually flag
the ghost. Secondary: step 1 books the close at `plan.close_cost` instead of
the confirmed `fill.fill_price` it *just received* from the v3.5 close.

**Fix shape:** place the rolled vertical as a real signed-credit limit order
with fill confirmation before writing the record; book step 1 at
`fill.fill_price`. Alternatively gate `check_and_execute_roll` behind
`paper_trading` until built — a silent no-roll is strictly safer live than a
ghost position.

##### L3 — One trades.db, no mode filter: paper history contaminates live truth

There is **no `paper_trade` filter** in the queries that matter:

- `realized_pnl_today()` — **the DAILY_LOSS_LIMIT source of truth** — sums
  every closed row. On switch day, two weeks of paper habits plus any paper
  rows closed that ET day gate the *live* breaker. A red paper morning can
  halt real-money entries; a green one can mask a real-money halt.
- `get_open_trades()` / `get_open_trades_live()` — startup recovery and the
  position manager hand any still-open paper rows (unexpired weeklies, or
  rows with unknown expiry, which are deliberately kept) to the LIVE bot,
  which manages them, submits real close orders for them, collects broker
  rejects and pages until reconcile phantoms them — and the phantom booking
  then *also* lands in live realized P&L.
- The only DB wipe in the system is on **instrument** change, paper mode only.
  **Mode** change wipes nothing and archives nothing.

**Fix shape (small, do first):** mode-aware queries — filter
`paper_trade = (0 if live else 1)` in `get_open_trades` and
`_closed_today_rows` — plus a `configure.sh` step on switching to LIVE that
archives `trades.db → trades_paper_YYYY-MM-DD.db` (preserving the two weeks of
paper data rather than mixing or deleting it).

---

##### 🟡 MODERATE — expectation and hygiene

##### M1 — Paper fills are perfect; live fills are not
`PAPER_FILL_SLIPPAGE_PCT = 0.0`: paper enters AND exits at the exact
mid/mark, both sides, every time. Live pays spread crossing on entry, and the
v3.5 close buys through the mark by `LIVE_CLOSE_LIMIT_BUFFER` to get filled.
Two weeks of paper P&L is therefore a structurally *optimistic* estimate —
materially so on wide SPX spreads. Not a bug; a calibration warning. Consider
a nonzero paper slippage (even 1–2%) so paper stats stop flattering.

##### M2 — Dashboards report mixed modes
`status.py`, `eod_summary.py`, and the risk manager's session stats aggregate
paper and live rows together (`query.py` at least prints the flag per trade).
After L3's filter lands this mostly resolves itself; until then, switch-day
dashboards lie.

##### M3 — Live-only code paths have never executed
`get_open_option_positions()` is written version-robustly (sync on tastytrade
12.x, coroutine on 13.x) but its field access has only been verified against
SDK source, never a live account — same for every live order path. Reconcile
now auto-enables with LIVE (v3.6/config v1.8), which makes the tiny-account
shakedown *more* important, not less: first live session should be 1 contract,
minimal width, watching `journalctl` and Telegram.

---

##### ✅ VERIFIED SAFE across the switch (so you don't re-audit them)

- **Exits** — fill-confirmed (v3.5): submit → bounded poll → book only on the
  broker's net fill; partials weighted; idempotent resume; verticals close as
  2-leg spread orders with signed debit limits; butterfly closes are
  marketable limits. Acceptance tests A–E pass.
- **15:45→16:00 flatten retry + paging** — mode-agnostic, books only via
  `_execute_exit`, which refuses unconfirmed fills.
- **Reconcile (v3.6)** — auto-follows mode; interval sweeps
  (`BROKER_RECONCILE_INTERVAL_MIN`, default 10) plus 15:45/15:50/15:57
  wind-down passes; phantom P&L recovered from order history; fail-safe on
  bad/empty broker reads; paper never reconciles.
- **DAILY_LOSS_LIMIT mechanics** — DB-seeded, restart-proof, net-based
  (content is compromised by L3 until filtered, but the mechanism is sound).
- **Regime/conviction/session gates, candle feed, sizing** — mode-agnostic by
  construction; single TastyTrade/DXFeed feed serves both modes identically.

---

##### Recommended order of work before cash

1. **L3** — mode-filter the two queries + archive-on-switch in configure.sh.
   Smallest change, prevents day-one contamination no matter what else ships.
2. **L1** — entry-side fill confirmation (mirror of exit v3.5). Condor legs
   first (the strategy you actually run), then single-leg price readback, then
   butterfly (or gate butterflies off in live until rebuilt).
3. **L2** — real order in the roll, or gate the roll to paper.
4. **M1** — nonzero paper slippage so the next two weeks of paper predict live.
5. Tiny-account live shakedown (1 contract) with reconcile auto-on, per the
   v3.5 spec's acceptance criteria.

---


<!-- ================= was: docs/AUDIT_header_compliance_2026-07-23.md ================= -->

##### AUDIT — Header/Changelog Compliance + Stale-Reference Sweep — 2026-07-23

Scope: full clone of `options_trader_v3` at HEAD `5740a05`. Every .py/.sh/.md read;
title-vs-newest-changelog verified per the standing convention (title line == newest
dated entry). All fixes are doc/comment-only **except one real bug** (§3).
Post-fix: `check_versions.sh` **0 red / 89 green**, test suite **37/37 pass**.

##### 1. Mis-numbered / duplicate changelog entries (relabeled, titles synced)

| File | Was | Now | Why |
|---|---|---|---|
| `risk/risk_manager.py` | `v1.4 — 2026-07-23` (full-budget condor sizing) | **v3.2** (+ v3.3, see §3) | File was already at v3.1; v1.4 was non-monotonic and duplicated the 2026-07-02 v1.4 |
| `strategy/butterfly_strategy.py` | `v1.4 — 2026-07-14` (discount gate); title v3.0 | **v3.2**, title v3.2 | v3.1 (07-12) already existed |
| `status.py` | second `v1.12 — 2026-07-20` | **v1.13**, title v1.13 | Duplicated the 2026-07-06 v1.12; in-code `# v1.12 fix` comments re-pointed |

##### 2. Stale title lines synced (no new version — matches the 07-16 precedent)

`analysis/trend_engine.py` → v3.2 · `analysis/structure_analyzer.py` → v3.0 ·
`data/market_data.py` v3.0 → v3.2 · `database/trade_logger.py` → v3.8 ·
`configure.sh` "v1.5" banner → v2.0 · `validate_regime.sh` v2.0 → **v2.2** (new entry:
removed two retired `data/harvest` paths from its Data block — the layout that
`migrate_data_layout.sh` deliberately rmdir'd) · `snapshot.sh` duplicate v1.1 line deduped.

##### 3. REAL BUG found and fixed — `risk_manager` v3.3

The 07-23 full-budget change renamed the sizing variable but left the **success-path
`logger.info` f-string referencing the deleted old name** → `NameError` on **every
condor-leg sizing that produces ≥1 contract** at fleet risk levels. Reproduced
(`spread_width=5.0, credit=0.50, risk=$1050` → NameError), fixed, re-verified
(B: 2 contracts, A: 3 contracts, clean log). The `check_versions` absence canary was
**legitimately RED at HEAD** on exactly this and the deploy shipped anyway — the
canary works; the pre-push gate of "run it and read the reds" is the part that slipped.
Lesson also encoded: changelog **prose** that names a canary-absence-checked token
re-trips the canary (same trap the `_orb_quality` comment already documents).

##### 4. `check_versions.sh` → v3.7

Label-correction sweep entry + prose refs updated ("risk v1.4"→v3.2, "status v1.12"→
v1.13, line-173 canary description). Fingerprints (code greps) unchanged.

##### 5. README.md — manifest re-synced + discarded-process references corrected

- Manifest rows: `main` v4.0→**v4.2** (chain archival), `config` "v3.3 stale"→**v3.9
  current**, `exit_engine` "v3.8 un-bumped"→**v4.1** (condor v2 + continuation rework),
  `entry_engine` →v3.9, `position_manager` →v3.9, `limit_ladder` →v1.3,
  `condor_roll` →v3.8, `risk_manager` →v3.3, `butterfly` →v3.2, `status` →v1.13,
  `trend_engine` +v3.2, `market_data` +v3.2.
- **Condor section**: "half the grade budget" (retired 07-23 → full budget), "pending
  leg is cancelled" (retired → **pauses**, iron_condor v3.2), per-leg exits updated to
  the v4.1 ratchet + time-gated TP.
- **Continuation exit table**: −40% floor → **−25% `CONTINUATION_STOP_LOSS_PCT`**;
  theta-bleed row added (v4.0 enabled it); trail now 5m-FVG-anchored.
- **Shadow section**: timers `shadow-start`/`shadow-stop` marked **RETIRED 2026-07-22**
  (edge-trigger fired while boxes were stopped overnight); enable-at-boot noted;
  **fleet-wide (29-box)** rollout supersedes "QQQ box only".
- **`validate_regime.sh` row**: "executing copy lives at `~/validate_regime.sh`, sync
  manually" **deleted** — contradicted the 07-23 repoint (repo copy is canonical);
  devtools wrapper numbers corrected **40–44 → 42–46** (v1.18 renumber).
- Defect U: dated resolution note appended.

##### 6. `docs/EXIT_RULES.md` — was frozen at exit_engine v3.8 (2026-07-15)

Now synced to **v4.1**: universal hard close reflects the 15:40 mark-limit → 15:45
MARKET escalation; condor section carries the ratcheting stop + time-gated TP@25% and
the leg-2 **pause** (was "cancelled"); a full **Trend Continuation** section added
(it had none — the strategy postdated the doc); summary corrected to six strategies /
four hard TPs (with the sweep +100% default-replacement noted).

##### 7. `shadow_devtools.sh` → v1.2

Timer status/banner items now label `shadow-start`/`shadow-stop` **RETIRED
(disabled = healthy)** so the menu can never read as "broken timers, go fix them."

##### 8. Flagged, not changed (your call)

- **`tests/validate_regime.sh` is a byte-identical duplicate of the root copy**
  (nothing references it — zero hits repo-wide). Per your loose-files principle it
  should be deleted; I synced it identically for now so it can't drift ahead, but one
  canonical copy is the right end state.
- `tests/a2_cooccurrence.py` / `ramp_calibration.py` keep read-only `data/harvest`
  **fallback globs explicitly marked legacy** — harmless (they read nothing there now);
  left in place. `tests/regime_diary.py`'s usage example still shows `--harvest
  .../data/harvest` in a docstring; low-priority.
- Defect Z (`fleet_trades` cross-date contamination) remains OPEN per the README.

---


<!-- ================= was: docs/FABLE_SPEC_live_exit_fill_confirmation.md ================= -->

##### FABLE SPEC — Live exit fill-confirmation (`_confirm_and_book_live_exit`)

**Repo:** `github.com/TX-9AI/options_trader_v3` · **Owner of this file after build:** Fable
**Status:** paper side is DONE and deployed; this is the LIVE half only.
**Hard rule:** do not touch the paper path or the shared contract below — build only
the live method. One owner per file: you own `_confirm_and_book_live_exit` and the
broker-polling helpers; the seam it plugs into is fixed.

---

##### The one-sentence problem

When the bot closes a position in **live/cash** mode, it must book P&L **only after the
broker confirms the fill, at the broker's actual fill price** — never at a mark, never at
entry, never a fabricated `$0.00`, and an unconfirmed close must remain an **open
position**, not a booked row.

##### Why this exists (the bug that motivated it)

On 2026-07-15 the 15:45 hard-close flattened ~8 condor legs and logged **every one at
`pnl=+$0.00`**. Root cause: `flatten_all` booked P&L on order *submission success*, at a
fallback price (entry premium), with **no fill confirmation**. In paper that's a
reconcilable bookkeeping error. In live it is a position-truth catastrophe: the DB says
flat, the broker may not be, P&L is fiction, and the `DAILY_LOSS_LIMIT` circuit breaker
(which halts on realized P&L) is now reading fabricated numbers. This spec closes that
hole for live trading.

##### What is already done (do not redo, do not change)

`execution/exit_engine.py` v3.4 and `execution/position_manager.py` v3.4 now use a shared
result contract. **This is the seam. It is fixed. Build to it.**

```python
@dataclass
class FillResult:
    confirmed:  bool                      # True ONLY on a real, completed close
    fill_price: Optional[float] = None    # ACTUAL close price; None iff not confirmed
    order_id:   Optional[str]   = None    # broker order id (live)
    partial:    bool            = False   # partially filled, remainder still working
    detail:     str             = ""      # human-readable status for logs/alerts
```

- `place_exit_order(record, reason, mark_price=None) -> FillResult`
  - **PAPER (built, frozen):** simulates the fill at `mark_price`, returns
    `FillResult(confirmed=True, fill_price=mark_price)`. One pass — a simulated close
    always succeeds; no polling, no retry, no reuse.
  - **LIVE (your job):** calls `self._confirm_and_book_live_exit(record, reason, mark_price)`.
- `_execute_exit` (position_manager) books **only** when `fill.confirmed and fill.fill_price
  is not None`, using `fill.fill_price`. On `confirmed=False` it books nothing and returns
  `False`, and `flatten_all` retries every tick 15:45→16:00 and escalates. **You do not need
  to touch any of this** — return a correct `FillResult` and the accounting is handled.
- `_submit_live_close(record) -> bool` already exists: it submits the SELL_TO_CLOSE / spread
  order via the tastytrade SDK and returns submit success. **Submission is not a fill** — it
  is provided for you to call as step 1, nothing more.
- Current live stub raises `NotImplementedError` on purpose, so cash cannot be enabled until
  you ship this. That is the safety property; preserve it until the real thing is proven.

##### What you must build

Implement `ExitEngine._confirm_and_book_live_exit(self, record, reason, mark_price) ->
FillResult` with this contract:

1. **Submit** the close (use `_submit_live_close(record)` or inline equivalent) and **capture
   the broker order id.** If submission fails → `FillResult(confirmed=False,
   detail="submit failed")`.
2. **Poll** broker order status for that order id on a **bounded** loop:
   - poll interval and total deadline configurable (propose `LIVE_FILL_POLL_SECONDS` and
     `LIVE_FILL_DEADLINE_SECONDS` in `config.py`; sensible defaults e.g. 2s / 30s);
   - terminal states: `filled`, `partially_filled`, `rejected`, `cancelled`, `expired`;
   - respect API rate limits (this runs during the session-limited window).
3. **Book only on a confirmed FULL fill:** return `FillResult(confirmed=True,
   fill_price=<broker fill price>, order_id=...)`. The fill price is the broker's, read back
   from the filled order — **not** `mark_price`, which is context only.
4. **Partial fills:** either (a) track the remainder to completion and return the
   quantity-weighted average fill price once fully closed, or (b) return
   `FillResult(confirmed=False, partial=True, detail=...)` and let the caller retry — pick
   one and document it. Never book a partial as if it were whole.
5. **Not filled by deadline / rejected / error:** return `FillResult(confirmed=False,
   detail=<why>)`. The position **stays open**; the 15:45→16:00 retry loop will re-attempt
   and page. Never fabricate a price, never mark closed.
6. **Spreads (condor legs):** a leg is a two-legged vertical. Confirm the **spread** closed
   (both legs), and return the **net** spread fill price on the same credit basis the P&L
   math expects (`_execute_exit` computes `entry_prem - fill_price` for credit-signed
   positions — so `fill_price` must be the net spread value, matching how the paper mark is
   `short_mark - long_mark`).

##### Acceptance tests (must pass before cash)

- **A — happy path:** submitted → filled → `FillResult(confirmed=True)` with the broker fill
  price; DB row closes; P&L matches `(entry - fill) * contracts * 100` for a credit spread.
- **B — the orphan test (the whole point):** submit an order that does **not** fill by the
  deadline → `confirmed=False`, **P&L booked = none**, DB row **still open**, alert fired.
  A submitted-but-unfilled order must **never** produce a `$0.00` (or any) booked close.
- **C — reject:** broker rejects → `confirmed=False`, position open, no booking.
- **D — partial:** partial then complete → single correct net fill price; or documented
  retry. Never books the partial as whole.
- **E — paper untouched:** `PAPER_TRADING=True` still books the simulated mark in one pass;
  no polling path entered.

##### What you'll need from Jason

- Live tastytrade **API credentials** for a funded but **tiny** account (test with 1
  contract / minimal width). Jason has offered these — request them for the test account,
  not production size.
- Confirmation of the tastytrade SDK's order-status object shape (fields for state, filled
  quantity, average fill price) — verify against the live SDK, do not assume.

##### Guardrails

- Complete files, never patches; bump the header of every file you change with what changed.
- Clone repo HEAD and read before editing — this file's paper seam is v3.4; build on it.
- Do not weaken the fail-loud stub until the acceptance tests pass; a half-built live path
  must still refuse to book rather than book an orphan.
- `PAPER_TRADING` default stays `True`. Nothing you build may change paper behavior.

---

