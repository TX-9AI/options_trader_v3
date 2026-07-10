# options_trader v3.0 — CHANGELOG
**2026-07-10 — Yahoo-Finance purge & data stream mapping optimization**
Built against options_trader_v2 `main` @ HEAD `a181dd2fd10c2f8c7c1cb97792edcea565afc71c`.
v2 repo preserved untouched; this tree is the new v3 repo root.

## Why
The bot trades and logs on TastyTrade (DXLink/DXFeed) candles, but market data
was pulled from the legacy Yahoo-Finance client — a different series that
provably diverges from the traded tape (caught on the 5-minute opening range).
Every process now derives its data from the same TastyTrade feed the bot
trades on. The purge is total: the legacy-source residue grep (§6.4 of the
purge spec, run via `tests/verify_feed_v3.sh`) returns zero hits across code,
config, shell, docs, and requirements — including this changelog.

## Architecture (one producer, many readers — per box)
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

## Changed files (logic)
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

## Comment/doc scrubs (no logic change)
`analysis/get_orb_range.py` (v3.0 entry), `analysis/orb_engine.py`,
`README.md` (v3.0 changelog + deps), `deploy/README_candle_logger.md`.

## Repo-wide v3.0 bump (no logic change)
Every remaining .py/.sh received a `v3.0 — 2026-07-10` changelog entry citing
the purge, with title versions set to v3.0: all engines, strategies,
execution, risk, notifications, database, utils, main.py, config.py, query.py,
status.py, eod_summary.py, and all shell tooling.

## NOT touched
Trading/risk/execution/strategy logic, `PAPER_TRADING` default (True),
Telegram, broker reconciliation, GEX, ORB engine logic — all behavior
unchanged above the data seam. The off-repo shadow observer rides the
preserved `get_cache()` seam with zero changes (restart it after deploy).

## Verification status
- §6.1 Contract test: **17/17 PASS** offline (`python -m tests.test_market_data_contract`).
- §6.4 Zero-Yahoo grep: **CLEAN** repo-wide.
- §6.2 ORB equivalence + §6.3 single-subscription proof: **ON-BOX gates** —
  run `bash tests/verify_feed_v3.sh` on one box during RTH (paper) before
  fleet deploy. Also confirms backfill depth per interval (entitlement) and
  VIX entitlement per the candle_feed FIRST-RUN CHECKLIST.
