# FILE_MAP — every module, what it calls, and what calls it

**Generated from the actual imports at HEAD, not from memory.** 88 Python modules
(87 → 88 on 2026-08-04: `analysis/entry_snapshot.py`, BACKLOG N.7)
across 11 local packages. Use this for audits, for tracing blast radius before a
change, and for answering "if I touch this, what breaks?"

Regenerate after structural changes — it is a snapshot, and it will drift.

## How to read it

- **calls** — local modules this file imports (external libs omitted).
- **called by** — local modules that import this file. An empty list means it is
  an entry point (`main.py`, the ops scripts) or a leaf.
- Files under `tests/` and `deploy/` are excluded; they ship but are not part of
  the runtime import graph.

## Fan-in leaderboard — the modules with the widest blast radius

Change these with the most care; a break here reaches everything downstream.

| module | imported by | some of the importers |
|---|---|---|
| `config.py` | 48 | chain_snapshot.py, liquidity_mapper.py, orb_engine.py, regime_classifier.py, regime_confluence.py, signal_journal.py … |
| `utils/time_utils.py` | 15 | orb_engine.py, regime_classifier.py, trade_logger.py, broker_reconcile.py, entry_engine.py, exit_engine.py … |
| `analysis/regime_classifier.py` | 12 | regime_confluence.py, main.py, setup_scorer.py, observer.py, butterfly_strategy.py, continuation_strategy.py … |
| `analysis/volatility_engine.py` | 11 | regime_classifier.py, main.py, setup_scorer.py, observer.py, butterfly_strategy.py, continuation_strategy.py … |
| `analysis/liquidity_mapper.py` | 9 | regime_classifier.py, main.py, setup_scorer.py, observer.py, butterfly_strategy.py, orb_strategy.py … |
| `data/tasty_client.py` | 9 | candle_feed.py, market_data.py, options_chain.py, entry_engine.py, exit_engine.py, position_manager.py … |
| `notifications/alert_manager.py` | 9 | eod_summary.py, entry_engine.py, exit_engine.py, position_manager.py, main.py, risk_manager.py … |
| `database/trade_logger.py` | 9 | entry_engine.py, exit_engine.py, position_manager.py, main.py, risk_manager.py, condor_roll.py … |
| `utils/math_utils.py` | 8 | liquidity_mapper.py, orb_engine.py, structure_analyzer.py, trend_engine.py, volatility_engine.py, options_chain.py … |
| `data/macro_data.py` | 8 | regime_classifier.py, main.py, session_guard.py, setup_scorer.py, butterfly_strategy.py, iron_condor_strategy.py … |
| `data/options_chain.py` | 8 | trade_readiness.py, gex_data.py, main.py, base_strategy.py, butterfly_strategy.py, iron_condor_strategy.py … |
| `strategy/base_strategy.py` | 8 | entry_engine.py, setup_scorer.py, butterfly_strategy.py, continuation_strategy.py, iron_condor_strategy.py, orb_strategy.py … |
---

### Root

**`config.py`** — options_trader v4.0
  - calls: _(nothing local)_
  - called by: `chain_snapshot.py`, `liquidity_mapper.py`, `orb_engine.py`, `regime_classifier.py`, `regime_confluence.py`, `signal_journal.py`, `structure_analyzer.py`, `trend_engine.py`, `volatility_engine.py`, `candle_feed.py`, `candle_logger.py`, `data_cache.py`, `macro_data.py`, `market_data.py`, `options_chain.py`, `tasty_client.py`, `trade_logger.py`, `debug_status.py`, `broker_reconcile.py`, `entry_engine.py`, `exit_engine.py`, `limit_ladder.py`, `order_confirm.py`, `position_manager.py`, `main.py`, `alert_manager.py`, `telegram_sender.py`, `query.py`, `risk_manager.py`, `session_guard.py`, `setup_scorer.py`, `eod_compare.py`, `observer.py`, `status.py`, `butterfly_strategy.py`, `condor_roll.py`, `continuation_strategy.py`, `iron_condor_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`, `stress_theta_bleed.py`, `backtest_harness.py`, `canary_condor_dualfloor.py`, `test_entry_fill_confirmation.py`, `test_phantom_pnl_recovery.py`, `test_roll_is_real.py`, `test_runner_refinements.py`, `time_utils.py`

**`debug_status.py`** — Verbose debug for status.py instrument issue
  - calls: `config.py`
  - called by: _(entry point / leaf)_

**`eod_summary.py`** — End-of-day P&L writer. Runs on EACH bot box at ~15:50 ET (own systemd timer),
  - calls: `alert_manager.py`, `query.py`
  - called by: _(entry point / leaf)_

**`main.py`** — options_trader v4.4
  - calls: `chain_snapshot.py`, `conviction_integrator.py`, `entry_snapshot.py`, `liquidity_mapper.py`, `orb_engine.py`, `regime_classifier.py`, `regime_confluence.py`, `structure_analyzer.py`, `trade_readiness.py`, `trend_engine.py`, `volatility_engine.py`, `config.py`, `data_cache.py`, `gex_data.py`, `macro_data.py`, `options_chain.py`, `tasty_client.py`, `trade_logger.py`, `broker_reconcile.py`, `entry_engine.py`, `limit_ladder.py`, `order_confirm.py`, `position_manager.py`, `alert_manager.py`, `risk_manager.py`, `session_guard.py`, `setup_scorer.py`, `butterfly_strategy.py`, `condor_roll.py`, `continuation_strategy.py`, `iron_condor_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`, `time_utils.py`
  - called by: `test_phantom_pnl_recovery.py`

**`query.py`** — OptionsTrader Performance Dashboard
  - calls: `config.py`, `market_data.py`
  - called by: `eod_summary.py`

**`status.py`** — Live bot status snapshot. v1.13
  - calls: `config.py`
  - called by: _(entry point / leaf)_

**`stress_theta_bleed.py`** — Offline stress test for _theta_bleed v3.0 gates. Patches minutes_since to
  - calls: `config.py`, `exit_engine.py`
  - called by: _(entry point / leaf)_

**`test_candle_logger.py`** — Offline self-test for data/candle_logger.py v3.0 — builds a synthetic feed
  - calls: `candle_feed.py`, `candle_logger.py`
  - called by: _(entry point / leaf)_


### `analysis/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`entry_snapshot.py`** — entry-time FVG/structure capture (LOG-ONLY, never trades).
  - calls: `exit_engine.py` (LAZY, inside the function — module-level it would drag the
    TastyTrade SDK into every offline consumer of `analysis/`), `time_utils.py`
  - called by: `main.py`

**`chain_snapshot.py`** — full option-chain archival (LOG-ONLY, never trades).
  - calls: `config.py`
  - called by: `main.py`

**`conviction_integrator.py`** — Layer 2: persistence
  - calls: `regime_confluence.py`
  - called by: `main.py`, `replay_confluence.py`

**`get_orb_range.py`** — Resolve the opening range for the instrument and
  - calls: `market_data.py`
  - called by: _(entry point / leaf)_

**`liquidity_mapper.py`** — v3.1 — 2026-07-14 — AS-OF named levels.
  - calls: `config.py`, `math_utils.py`
  - called by: `regime_classifier.py`, `main.py`, `setup_scorer.py`, `observer.py`, `butterfly_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`, `backtest_harness.py`, `replay_confluence.py`

**`orb_engine.py`** — Opening Range Breakout state machine.
  - calls: `signal_journal.py`, `config.py`, `math_utils.py`, `time_utils.py`
  - called by: `position_manager.py`, `main.py`, `base_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`, `backtest_harness.py`, `test_orb_retest_v33.py`

**`regime_classifier.py`** — Market regime classification.
  - calls: `liquidity_mapper.py`, `structure_analyzer.py`, `trend_engine.py`, `volatility_engine.py`, `config.py`, `macro_data.py`, `time_utils.py`
  - called by: `regime_confluence.py`, `main.py`, `setup_scorer.py`, `observer.py`, `butterfly_strategy.py`, `continuation_strategy.py`, `iron_condor_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`, `backtest_harness.py`, `canary_continuation_fvg_pullback.py`, `replay_confluence.py`

**`regime_confluence.py`** — options_trader_v3
  - calls: `regime_classifier.py`, `config.py`
  - called by: `conviction_integrator.py`, `trade_readiness.py`, `main.py`, `backtest_harness.py`, `replay_confluence.py`

**`signal_journal.py`** — signal-time instrumentation (LOG-ONLY, never trades).
  - calls: `config.py`
  - called by: `orb_engine.py`

**`structure_analyzer.py`** — Market structure analysis. v3.0
  - calls: `config.py`, `math_utils.py`
  - called by: `regime_classifier.py`, `main.py`, `setup_scorer.py`, `observer.py`, `sweep_reversal_strategy.py`, `backtest_harness.py`, `replay_confluence.py`

**`trade_readiness.py`** — options_trader_v3
  - calls: `regime_confluence.py`, `options_chain.py`, `sweep_reversal_strategy.py`
  - called by: `main.py`, `canary_condor_dualfloor.py`, `canary_trend_credit_spread.py`

**`trend_engine.py`** — Trend detection via EMA stacks, ADX, momentum. v3.2
  - calls: `config.py`, `math_utils.py`
  - called by: `regime_classifier.py`, `main.py`, `observer.py`, `continuation_strategy.py`, `backtest_harness.py`, `replay_confluence.py`

**`volatility_engine.py`** — Volatility regime detection.
  - calls: `config.py`, `math_utils.py`
  - called by: `regime_classifier.py`, `main.py`, `setup_scorer.py`, `observer.py`, `butterfly_strategy.py`, `continuation_strategy.py`, `iron_condor_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`, `backtest_harness.py`, `replay_confluence.py`


### `data/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`candle_feed.py`** — addendum v3.8 (see below); original header follows.
  - calls: `config.py`, `tasty_client.py`
  - called by: `candle_logger.py`, `market_data.py`, `test_candle_logger.py`, `test_market_data_contract.py`

**`candle_logger.py`** — end-of-day 1-minute candle logger. v3.1
  - calls: `config.py`, `candle_feed.py`
  - called by: `test_candle_logger.py`

**`data_cache.py`** — Caches underlying OHLCV candles to reduce API calls.
  - calls: `config.py`, `market_data.py`
  - called by: `main.py`, `observer.py`, `test_market_data_contract.py`

**`gex_data.py`** — v3.1 — 2026-07-14 — SCALE-FREE GEX ENVIRONMENT.
  - calls: `options_chain.py`
  - called by: `main.py`

**`macro_data.py`** — VIX level, IV rank, and Fed/FOMC
  - calls: `config.py`, `market_data.py`
  - called by: `regime_classifier.py`, `main.py`, `session_guard.py`, `setup_scorer.py`, `butterfly_strategy.py`, `iron_condor_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`

**`market_data.py`** — Underlying price data (candles + live
  - calls: `config.py`, `candle_feed.py`, `tasty_client.py`
  - called by: `get_orb_range.py`, `data_cache.py`, `macro_data.py`, `query.py`, `test_market_data_contract.py`

**`options_chain.py`** — Options chain data from TastyTrade SDK.
  - calls: `config.py`, `tasty_client.py`, `math_utils.py`
  - called by: `trade_readiness.py`, `gex_data.py`, `main.py`, `base_strategy.py`, `butterfly_strategy.py`, `iron_condor_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`

**`tasty_client.py`** — TastyTrade session via the official tastytrade SDK.
  - calls: `config.py`
  - called by: `candle_feed.py`, `market_data.py`, `options_chain.py`, `entry_engine.py`, `exit_engine.py`, `position_manager.py`, `main.py`, `condor_roll.py`, `test_roll_is_real.py`


### `database/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`trade_logger.py`** — Options trade logging (SQLite). v3.8
  - calls: `config.py`, `time_utils.py`
  - called by: `entry_engine.py`, `exit_engine.py`, `position_manager.py`, `main.py`, `risk_manager.py`, `condor_roll.py`, `test_mode_isolation.py`, `test_roll_is_real.py`, `test_runner_refinements.py`


### `execution/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`broker_reconcile.py`** — LIVE broker⇄DB position reconciliation.
  - calls: `config.py`, `time_utils.py`
  - called by: `main.py`, `test_phantom_pnl_recovery.py`

**`entry_engine.py`** — Options order placement via TastyTrade SDK.
  - calls: `config.py`, `tasty_client.py`, `trade_logger.py`, `limit_ladder.py`, `order_confirm.py`, `alert_manager.py`, `risk_manager.py`, `setup_scorer.py`, `base_strategy.py`, `time_utils.py`
  - called by: `main.py`, `test_entry_fill_confirmation.py`

**`exit_engine.py`** — Strategy-aware exit logic for all options positions.
  - calls: `config.py`, `tasty_client.py`, `trade_logger.py`, `limit_ladder.py`, `alert_manager.py`, `time_utils.py`
  - called by: `position_manager.py`, `condor_roll.py`, `stress_theta_bleed.py`, `test_roll_is_real.py`, `test_runner_refinements.py`

**`limit_ladder.py`** — Mid-anchored limit pricing for entries and exits.
  - calls: `config.py`
  - called by: `entry_engine.py`, `exit_engine.py`, `main.py`, `condor_roll.py`, `test_entry_fill_confirmation.py`

**`order_confirm.py`** — LIVE entry-order fill confirmation (audit defect O).
  - calls: `config.py`
  - called by: `entry_engine.py`, `main.py`, `condor_roll.py`, `test_entry_fill_confirmation.py`

**`position_manager.py`** — Manages the single open options position.
  - calls: `orb_engine.py`, `config.py`, `tasty_client.py`, `trade_logger.py`, `exit_engine.py`, `alert_manager.py`, `risk_manager.py`
  - called by: `main.py`


### `notifications/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`alert_manager.py`** — Telegram alerts for options_trader.
  - calls: `config.py`, `telegram_sender.py`, `time_utils.py`
  - called by: `eod_summary.py`, `entry_engine.py`, `exit_engine.py`, `position_manager.py`, `main.py`, `risk_manager.py`, `condor_roll.py`, `test_entry_fill_confirmation.py`, `test_roll_is_real.py`

**`telegram_sender.py`** — Telegram alerts via Bot API.
  - calls: `config.py`
  - called by: `alert_manager.py`

**`test_telegram.py`** — Telegram connectivity test for options_trader.
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_


### `risk/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`risk_manager.py`** — Position sizing and session circuit breaker. v3.3
  - calls: `config.py`, `trade_logger.py`, `alert_manager.py`, `math_utils.py`, `time_utils.py`
  - called by: `entry_engine.py`, `position_manager.py`, `main.py`

**`session_guard.py`** — Session boundary enforcement.
  - calls: `config.py`, `macro_data.py`, `time_utils.py`
  - called by: `main.py`

**`setup_scorer.py`** — Scores and grades options trade signals A/B.
  - calls: `liquidity_mapper.py`, `regime_classifier.py`, `structure_analyzer.py`, `volatility_engine.py`, `config.py`, `macro_data.py`, `base_strategy.py`, `time_utils.py`
  - called by: `entry_engine.py`, `main.py`


### `shadow/`

**`__init__.py`** — shadow/ — OBSERVE-ONLY conviction-scoring subsystem.
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`eod_compare.py`** — EOD would-have-fired vs actually-fired comparison.
  - calls: `config.py`
  - called by: _(entry point / leaf)_

**`observer.py`** — the shadow observer service (OBSERVE-ONLY, never trades).
  - calls: `liquidity_mapper.py`, `regime_classifier.py`, `structure_analyzer.py`, `trend_engine.py`, `volatility_engine.py`, `config.py`, `data_cache.py`, `primitives.py`, `scorers.py`
  - called by: _(entry point / leaf)_

**`primitives.py`** — shared, pattern-agnostic primitives (velocity / magnitude / position).
  - calls: _(nothing local)_
  - called by: `observer.py`, `registry.py`, `scorers.py`

**`registry.py`** — registry of named "completeness" conjunctions.
  - calls: `primitives.py`
  - called by: _(entry point / leaf)_

**`scorers.py`** — per-pattern conviction scorers (shadow: sweep-reversal first).
  - calls: `primitives.py`
  - called by: `observer.py`

**`trading_day.py`** — shadow/trading_day.py v1.0 — standalone US-market trading-day check.
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_


### `strategy/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`base_strategy.py`** — Abstract base and OptionsSignal for all strategies.
  - calls: `orb_engine.py`, `options_chain.py`
  - called by: `entry_engine.py`, `setup_scorer.py`, `butterfly_strategy.py`, `continuation_strategy.py`, `iron_condor_strategy.py`, `orb_strategy.py`, `sweep_reversal_strategy.py`, `test_runner_refinements.py`

**`butterfly_strategy.py`** — Debit butterfly for RANGING/COMPRESSION regimes. v3.2
  - calls: `liquidity_mapper.py`, `regime_classifier.py`, `volatility_engine.py`, `config.py`, `macro_data.py`, `options_chain.py`, `base_strategy.py`
  - called by: `main.py`

**`condor_roll.py`** — Broken-wing roll of a live iron condor.
  - calls: `config.py`, `tasty_client.py`, `trade_logger.py`, `exit_engine.py`, `limit_ladder.py`, `order_confirm.py`, `alert_manager.py`, `time_utils.py`
  - called by: `main.py`, `test_roll_is_real.py`

**`continuation_strategy.py`** — Trend-continuation on pullback.
  - calls: `regime_classifier.py`, `trend_engine.py`, `volatility_engine.py`, `config.py`, `base_strategy.py`
  - called by: `main.py`, `canary_continuation_fvg_pullback.py`

**`iron_condor_strategy.py`** — v-dualfloor + v-indep-legs — 2026-07-28 — TWO FIXES to strike selection and legging.
  - calls: `regime_classifier.py`, `volatility_engine.py`, `config.py`, `macro_data.py`, `options_chain.py`, `base_strategy.py`
  - called by: `main.py`, `canary_condor_dualfloor.py`

**`orb_strategy.py`** — ORB break-and-retest signal generation.
  - calls: `liquidity_mapper.py`, `orb_engine.py`, `regime_classifier.py`, `volatility_engine.py`, `config.py`, `macro_data.py`, `options_chain.py`, `base_strategy.py`, `math_utils.py`
  - called by: `main.py`

**`sweep_reversal_strategy.py`** — Post-liquidity-sweep reversal for options.
  - calls: `liquidity_mapper.py`, `orb_engine.py`, `regime_classifier.py`, `structure_analyzer.py`, `volatility_engine.py`, `config.py`, `macro_data.py`, `options_chain.py`, `base_strategy.py`, `time_utils.py`
  - called by: `trade_readiness.py`, `main.py`


### `tests/`

**`a2_cooccurrence.py`** — A2 co-occurrence analyzer — what actually happens when TRENDING and RANGING
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`backtest_harness.py`** — offline multi-day backtest over spliced 1-minute tape.
  - calls: `liquidity_mapper.py`, `orb_engine.py`, `regime_classifier.py`, `regime_confluence.py`, `structure_analyzer.py`, `trend_engine.py`, `volatility_engine.py`, `config.py`, `replay_confluence.py`
  - called by: _(entry point / leaf)_

**`canary_condor_dualfloor.py`** — !/usr/bin/env python3
  - calls: `trade_readiness.py`, `config.py`, `iron_condor_strategy.py`
  - called by: _(entry point / leaf)_

**`canary_continuation_fvg_pullback.py`** — !/usr/bin/env python3
  - calls: `regime_classifier.py`, `continuation_strategy.py`
  - called by: _(entry point / leaf)_

**`canary_trend_credit_spread.py`** — !/usr/bin/env python3
  - calls: `trade_readiness.py`
  - called by: _(entry point / leaf)_

**`chain_reconstruction_check.py`** — v1.0 — Does a greek-based Taylor
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`conditional_tables.py`** — v1.1 — Conditional-probability tables from the
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`ramp_calibration.py`** — Ramp calibration — find WHICH scoring term is saturating and where its ramp
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`readiness_digest.py`** — !/usr/bin/env python3
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`regime_backfill.py`** — !/usr/bin/env python3
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`regime_diary.py`** — !/usr/bin/env python3
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`replay_classifier.py`** — Replay the CORRECTED sweep logic over tonight's 6 candle files.
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`replay_confluence.py`** — !/usr/bin/env python3
  - calls: `conviction_integrator.py`, `liquidity_mapper.py`, `regime_classifier.py`, `regime_confluence.py`, `structure_analyzer.py`, `trend_engine.py`, `volatility_engine.py`
  - called by: `backtest_harness.py`

**`test_entry_fill_confirmation.py`** — audit defect O part 1 (condor entry)
  - calls: `config.py`, `entry_engine.py`, `limit_ladder.py`, `order_confirm.py`, `alert_manager.py`
  - called by: _(entry point / leaf)_

**`test_market_data_contract.py`** — v3.0 seam contract test.
  - calls: `candle_feed.py`, `data_cache.py`, `market_data.py`
  - called by: _(entry point / leaf)_

**`test_mode_isolation.py`** — audit defect Q: paper and live rows in one
  - calls: `trade_logger.py`, `time_utils.py`
  - called by: _(entry point / leaf)_

**`test_orb_retest_v33.py`** — v1.0 — 2026-07-12.
  - calls: `orb_engine.py`
  - called by: _(entry point / leaf)_

**`test_phantom_pnl_recovery.py`** — v3.6 phantom P&L recovery + reconcile
  - calls: `config.py`, `broker_reconcile.py`, `main.py`
  - called by: _(entry point / leaf)_

**`test_regime_gate.py`** — Pressure-test: every state-transition combination through the gate +
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`test_roll_is_real.py`** — audit defect P: the broken-wing roll must place a
  - calls: `config.py`, `tasty_client.py`, `trade_logger.py`, `exit_engine.py`, `alert_manager.py`, `condor_roll.py`
  - called by: _(entry point / leaf)_

**`test_runner_refinements.py`** — exit_engine v3.8 / config v2.0 /
  - calls: `config.py`, `trade_logger.py`, `exit_engine.py`, `base_strategy.py`, `time_utils.py`
  - called by: _(entry point / leaf)_


### `utils/`

**`__init__.py`**
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`check_sdk.py`** — TastyTrade SDK Diagnostic Tool
  - calls: _(nothing local)_
  - called by: _(entry point / leaf)_

**`math_utils.py`** — Math helpers for options trading.
  - calls: _(nothing local)_
  - called by: `liquidity_mapper.py`, `orb_engine.py`, `structure_analyzer.py`, `trend_engine.py`, `volatility_engine.py`, `options_chain.py`, `risk_manager.py`, `orb_strategy.py`

**`time_utils.py`** — Timezone, RTH session helpers, and time utilities.
  - calls: `config.py`
  - called by: `orb_engine.py`, `regime_classifier.py`, `trade_logger.py`, `broker_reconcile.py`, `entry_engine.py`, `exit_engine.py`, `main.py`, `alert_manager.py`, `risk_manager.py`, `session_guard.py`, `setup_scorer.py`, `condor_roll.py`, `sweep_reversal_strategy.py`, `test_mode_isolation.py`, `test_runner_refinements.py`
