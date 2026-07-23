# DIAGNOSIS RESPONSE — DXLink session exhaustion — 2026-07-13

Verified against fleet HEAD `818d312` in a pinned worktree, the GOOGL HEAD `a42445e`,
and the **actual installed tastytrade SDK 13.0.0 source** (not its docs). Verdict up
front: **§3 is CONFIRMED with one correction and one addition. §1's causal chain is
half wrong — the mechanism that blocked the trades is not the regime.** Details, then
solutions.

---

## 1 · The three questions, answered from code

### Q1 — Is `fetch_chain()` genuinely opening a new DXLinkStreamer per tick?

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

### Q2 — Anything else opening DXLink connections?

**NO.** Full-tree enumeration at `818d312`: exactly two live openers —
`candle_feed.py:327` (persistent, one per box, correct) and `options_chain.py:218`
(per-tick, the problem). `gex_data` consumes the chain (confirmed — no streamer).
`check_sdk.py` is a manual diagnostic. The `observer/` tarballs cannot be grepped
(defect D) — if the shadow subsystem is running anywhere, it is unaudited; worth one
`fleet.py run "ss -tnp | grep -c 443"`-style check, but nothing in the *importable*
tree opens a third stream.

### Q3 — Is there a teardown/close() bug making sessions leak?

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

## 2 · CORRECTION to §1 — the causal chain that actually blocked the trades

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

## 3 · Problem C (the four crash-loopers) — explained, no new work needed

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

## 4 · Solutions, with tradeoffs

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

### Recommendation

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

## 5 · Re-arm sequence (proposed — no action taken)

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
