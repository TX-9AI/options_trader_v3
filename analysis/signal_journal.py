"""
analysis/signal_journal.py — signal-time instrumentation (LOG-ONLY, never trades).
v1.0 — 2026-07-18 — initial release.

WHY THIS EXISTS (ROADMAP Phase 3.1, verbatim):
    "Instrument first. Log at signal time, for EVERY signal (fired AND
     gate-blocked): trade type, regime, conviction, setup score, GEX context,
     fees estimate, and eventual outcome for fired ones. A gate you can't
     counterfactual is a gate you can't calibrate."

The 1-min OHLC tape is replayable forever; what is NOT reconstructible after
16:00 is what the option chain looked like at signal time — premium, bid/ask
spread, IV, greeks — and which gate disposed of the signal. This module makes
that perishable context durable. Without it, every session between now and the
Phase-3 calibration campaign is tape that can never become calibration data.

DESIGN RULES (non-negotiable):
  1. This module can NEVER crash the trading loop. Every public function
     swallows every exception (logged at DEBUG). A full disk, a bad payload,
     a permissions error — all degrade to "no journal line", never to a raised
     exception. The bot's behavior with this module present is byte-identical
     to its behavior with the module deleted.
  2. LOG-ONLY. Imports nothing from execution/, risk/, strategy/,
     notifications/. Holds no state beyond an open-file cache. Never reads
     trades.db, never touches the store.
  3. Append-only JSONL, one line per event:
         data/signal_journal/<YYYY-MM-DD>/<SYMBOL>.jsonl
     Self-locates the repo root (mirrors shadow/observer.py) — no /var/lib,
     no per-box path. Collected off-box by snapshot.sh / harvest like the
     other data/ products (add to the EOD chain when the volume justifies it).

EVENT VOCABULARY (the offline bucketer keys on `event`):
  scored        — emitted by risk/setup_scorer.score() for EVERY scored
                  signal, including below-B rejections (grade="REJECT").
                  Carries the full breakdown, thresholds, quote context.
  disposition   — emitted by main.attempt_new_entry for what happened AFTER
                  scoring: fired | sizing_rejected | invalid_signal.
                  Carries ORB retest_depth when the signal is an ORB.
  retest_check  — emitted by orb_engine._check_for_retest for every 1-min
                  candle examined while ARMED (defect G): the penetration
                  depth distribution INCLUDING near-misses (negative depth =
                  wick never entered the range). Raw px + orb_width; divide
                  by tape ATR offline (ATR-relative per defect G, never a
                  percentage).
  condor_plan   — condor plan created (regime + conviction at decision time).
  condor_leg    — condor leg trigger fired (regime + conviction at fire time).

Joining scored -> disposition -> trades.db outcome: events within the same
second for the same symbol/strategy are the same signal (the loop is
single-threaded per box; one signal per tick). `ts_et` is the join key.
"""

import json
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

ET = ZoneInfo("America/New_York")

# Self-locate: <repo>/analysis/signal_journal.py -> <repo>/data/signal_journal/
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUT_ROOT = os.path.join(_REPO_ROOT, "data", "signal_journal")

try:
    from config import INSTRUMENT as _SYMBOL
except Exception:                                    # config unreadable — still never raise
    _SYMBOL = os.environ.get("OT_INSTRUMENT", "UNKNOWN")


def _round(x, nd=4):
    try:
        return round(float(x), nd)
    except Exception:
        return None


def contract_ctx(c) -> dict:
    """Quote context for one OptionContract — the perishable part. None-safe."""
    if c is None:
        return None
    try:
        bid, ask, mark = float(c.bid), float(c.ask), float(c.mark)
        mid = (bid + ask) / 2.0 if (bid > 0 or ask > 0) else mark
        spread = (ask - bid) if ask >= bid else 0.0
        return {
            "occ":        getattr(c, "symbol", ""),
            "strike":     _round(getattr(c, "strike", 0.0), 2),
            "type":       getattr(c, "option_type", ""),
            "bid":        _round(bid, 4),
            "ask":        _round(ask, 4),
            "mark":       _round(mark, 4),
            "mid":        _round(mid, 4),
            "spread":     _round(spread, 4),
            "spread_pct_of_mid": _round(spread / mid, 4) if mid else None,
            "iv":         _round(getattr(c, "iv", 0.0), 4),
            "delta":      _round(getattr(c, "delta", 0.0), 4),
            "theta":      _round(getattr(c, "theta", 0.0), 4),
            "volume":     int(getattr(c, "volume", 0) or 0),
            "oi":         int(getattr(c, "open_interest", 0) or 0),
        }
    except Exception:
        return None


def signal_ctx(signal) -> dict:
    """Everything the OptionsSignal knows at signal time. None-safe."""
    if signal is None:
        return None
    try:
        d = {
            "strategy":         getattr(signal, "strategy_name", ""),
            "setup_type":       getattr(signal, "setup_type", ""),
            "direction":        getattr(signal, "direction", ""),
            "option_side":      getattr(signal, "option_side", ""),
            "underlying_entry": _round(getattr(signal, "underlying_entry", 0.0), 4),
            "underlying_stop":  _round(getattr(signal, "underlying_stop", 0.0), 4),
            "underlying_target": _round(getattr(signal, "underlying_target", 0.0), 4),
            "entry_premium":    _round(getattr(signal, "entry_premium", 0.0), 4),
            "conviction":       _round(getattr(signal, "conviction", 0.0), 4),
            "confluence":       list(getattr(signal, "confluence_factors", []) or []),
            "notes":            getattr(signal, "notes", ""),
            "contract":         contract_ctx(getattr(signal, "contract", None)),
        }
        if getattr(signal, "is_butterfly", False):
            d["is_butterfly"] = True
            d["net_debit"] = _round(getattr(signal, "net_debit", 0.0), 4)
            d["legs"] = {
                "lower":  contract_ctx(getattr(signal, "lower_contract", None)),
                "center": contract_ctx(getattr(signal, "center_contract", None)),
                "upper":  contract_ctx(getattr(signal, "upper_contract", None)),
            }
        return d
    except Exception:
        return None


def regime_ctx(regime) -> dict:
    if regime is None:
        return None
    try:
        return {
            "label":      str(getattr(regime, "primary_regime", "")),
            "conviction": _round(getattr(regime, "conviction", 0.0), 4),
        }
    except Exception:
        return None


def vol_ctx(vol_state) -> dict:
    if vol_state is None:
        return None
    try:
        return {
            "atr":            _round(getattr(vol_state, "atr_current", 0.0), 4),
            "bb_width":       _round(getattr(vol_state, "bb_width_current", 0.0), 6),
            "vwap":           _round(getattr(vol_state, "vwap", 0.0), 4),
            "price_vs_vwap":  getattr(vol_state, "price_vs_vwap", ""),
        }
    except Exception:
        return None


def macro_ctx(macro) -> dict:
    if macro is None:
        return None
    try:
        return {
            "vix":        _round(getattr(macro, "vix", 0.0), 2),
            "vix_regime": getattr(macro, "vix_regime", ""),
            "is_fed_day": bool(getattr(macro, "is_fed_day", False)),
        }
    except Exception:
        return None


def journal(event: str, **sections):
    """
    Append one JSONL event line. Swallows ALL exceptions — a journal failure
    must never become a trading-loop failure. Sections are pre-built dicts
    (use the *_ctx helpers) or plain scalars.
    """
    try:
        now = datetime.now(tz=ET)
        row = {"ts_et": now.isoformat(timespec="seconds"),
               "symbol": _SYMBOL,
               "event": event}
        for k, v in sections.items():
            if v is not None:
                row[k] = v
        day_dir = os.path.join(_OUT_ROOT, now.strftime("%Y-%m-%d"))
        os.makedirs(day_dir, exist_ok=True)
        path = os.path.join(day_dir, f"{_SYMBOL}.jsonl")
        with open(path, "a") as f:
            f.write(json.dumps(row, default=str) + "\n")
    except Exception as e:                            # noqa: BLE001 — by design
        logger.debug(f"signal_journal write skipped: {e}")
