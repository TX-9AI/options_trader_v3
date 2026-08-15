"""
analysis/liquidity_ledger.py — options_trader_v3 — v1.0
v1.0 — 2026-08-13 — THE MISSING OBJECT. `LiquidityMapper.analyze()` opens with
        `lmap = LiquidityMap()` and re-derives every pool from the candle window
        on EVERY CALL. Nothing survives a tick, so:
          · `touch_count` is NOT a running count — it is `len(cluster)`, i.e.
            how many bars in the lookback happened to sit at that level when the
            map was last rebuilt. A floor price hammers into five times today
            does not accumulate.
          · `swept` / `rejection_confirmed` are per-build snapshots. Same defect
            class LIQ.3 already fixed one level down, where `closes_beyond` was
            a birth-time snapshot that had to become a per-tick question.
          · a clean SINGLE-touch low that price respects three times never
            becomes a pool at all — `_find_pools` requires >=2 equal bars within
            EQUAL_LEVEL_PCT.
        So there was no object that could answer "is this floor holding?", and
        nothing was archived: the input to every named-level decision existed
        only in RAM. Same class as the chain archive before 2026-07-23.

        OPERATOR'S SPEC, 2026-08-13, verbatim on the part that matters:
        *"the wick counts as a touch, but only a close counts as acceptance or
        rejection."* Hence THREE counters per level, never one — `touches`
        (wick), `holds` (closed back on the origin side), `breaches` (closed
        beyond). A single number cannot say whether a level is being defended
        or given up, which is the entire question.

        *"It should live on the standalone bot boxes."* Written per-box under
        `data/liquidity_ledger/<date>/<SYMBOL>.json`, next to the chain archive
        and by the same convention. The bot owns its own level book; control is
        a consumer, never the source.

        RESET AT RTH OPEN, seeded with PDH/PDL and the prior session's extremes,
        carrying at least MIN_LEVELS_PER_SIDE highs and lows.

⚠️ FIRE-AND-FORGET. Every public entry point swallows every exception. A ledger
   failure must never reach the trading loop — `chain_snapshot.py` is the model
   and the reason: this is telemetry, and telemetry that can halt trading is a
   liability, not an asset.

⚠️ v1.0 WRITES AND DOES NOT GATE. Nothing reads this to make a decision yet.
   Prove the levels are the ones a human would have drawn before wiring them to
   anything that fires.

STATE, not an event log. The file is the CURRENT book, rewritten atomically on
change. Timing of individual touches is deliberately out of scope for v1 — the
counts are what the floor thesis needs, and an append log can be added later
without changing this schema.
"""

import json
import os
import tempfile
from typing import Dict, List, Optional

import logging

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 1

# Self-locate: <repo>/analysis/liquidity_ledger.py -> <repo>/data/liquidity_ledger/
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUT_ROOT = os.path.join(_REPO_ROOT, "data", "liquidity_ledger")

# Operator: "capture at least 3 previous highs & lows".
MIN_LEVELS_PER_SIDE = 3
# A level is "touched" when a bar's wick reaches within this fraction of it.
# Not zero: an exact float equality on a price never fires.
# ── LIQ.7 (2026-08-15) — ONE DEFINITION OF A ZONE ────────────────────────────
# Was 0.0002 (2bp). Raised to 0.002 (20bp) to MATCH `within_pct(..., 0.002)`,
# the tolerance `liquidity_mapper._add_named_pool` already uses to decide two
# prices are the same level. Operator: *"Reach within a small margin of error is
# good enough. A level is a ZONE, not a fixed number."*
# ⚠️ THE OLD VALUE UNDERCOUNTED EXACTLY WHAT THE SIZING RULE REWARDS. On a $580
# underlying 2bp is 12 CENTS — a clean approach that reversed just short of the
# level did not register as a test at all, so the most-defended levels looked
# untested. 20bp is $1.16 there, which is the zone the rest of the system
# already treats as one level.
# ⚠️ AND IT CHANGES WHAT EVERY LEDGER NUMBER MEANS. Counts before and after this
# are not comparable; the ledger has collected nothing yet, so there is no
# history to invalidate.
TOUCH_TOL_PCT = float(os.environ.get("OT_LEDGER_TOUCH_TOL", "0.002"))


class Level:
    """One horizontal level and its running contact history.

    THREE COUNTERS, per the operator's rule. `touches` is wick contact and says
    nothing about who won; `holds` and `breaches` are decided by the CLOSE and
    are the only two that carry information about whether the level is being
    defended.
    """

    __slots__ = ("price", "kind", "name", "is_named", "touches", "holds",
                 "breaches", "first_seen", "last_touch", "last_result")

    def __init__(self, price: float, kind: str, name: str = "",
                 is_named: bool = False, first_seen: str = ""):
        self.price = round(float(price), 4)
        self.kind = kind                      # "high" | "low"
        self.name = name                      # PDH / PDL / PRIOR_HIGH_2 / ...
        self.is_named = bool(is_named)
        self.touches = 0
        self.holds = 0
        self.breaches = 0
        self.first_seen = first_seen
        self.last_touch = ""
        self.last_result = ""                 # "hold" | "breach" | ""

    def as_dict(self) -> dict:
        return {
            "price": self.price, "kind": self.kind, "name": self.name,
            "is_named": self.is_named, "touches": self.touches,
            "holds": self.holds, "breaches": self.breaches,
            "first_seen": self.first_seen, "last_touch": self.last_touch,
            "last_result": self.last_result,
        }


class LiquidityLedger:
    """Session-scoped, persistent level book for ONE symbol on ONE box."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.date = ""
        self.levels: List[Level] = []
        self._dirty = False

    # ── session lifecycle ────────────────────────────────────────────────────

    def reset_for_session(self, date: str, seeds=None) -> None:
        """Clear and reseed. Called at RTH open.

        `seeds` is an iterable of (price, kind, name, is_named). The CALLER
        supplies them because the ledger must not own a second definition of
        what a prior high is — `LiquidityMapper` already owns that, and a
        competing derivation here is exactly the second-lineage failure
        WORKING_AGREEMENT 7 forbids.
        """
        try:
            self.date = date
            self.levels = []
            for s in (seeds or []):
                self.add_level(*s, first_seen=date)
            self._dirty = True
        except Exception as e:                                 # noqa: BLE001
            logger.debug("ledger reset skipped: %s", e)

    def add_level(self, price: float, kind: str, name: str = "",
                  is_named: bool = False, first_seen: str = "") -> None:
        try:
            if not price or price <= 0 or kind not in ("high", "low"):
                return
            for lv in self.levels:
                if lv.kind == kind and abs(lv.price - price) <= \
                        abs(price) * TOUCH_TOL_PCT:
                    return                                     # already held
            self.levels.append(Level(price, kind, name, is_named,
                                     first_seen or self.date))
            self._dirty = True
        except Exception as e:                                 # noqa: BLE001
            logger.debug("ledger add_level skipped: %s", e)

    # ── the update, and the whole point of the module ────────────────────────

    def on_closed_bar(self, high: float, low: float, close: float,
                      ts: str = "") -> None:
        """Apply ONE CLOSED bar to every level.

        THE RULE, and it is the operator's, not an interpretation:
          · WICK reaches the level            -> touches += 1
          · CLOSE beyond it                   -> breaches += 1   (acceptance)
          · CLOSE back on the origin side     -> holds    += 1   (rejection)
        A bar that never reaches the level does nothing at all — it is neither
        a hold nor a breach, and counting it as either is how a level that was
        simply far away starts looking defended.

        ⚠️ CLOSED BARS ONLY. Feeding a forming bar would count a wick that has
        not finished printing and a close that is not a close.
        """
        try:
            high, low, close = float(high), float(low), float(close)
            for lv in self.levels:
                tol = abs(lv.price) * TOUCH_TOL_PCT
                if lv.kind == "high":
                    reached = high >= lv.price - tol
                    accepted = close > lv.price + tol
                else:
                    reached = low <= lv.price + tol
                    accepted = close < lv.price - tol
                if not reached:
                    continue
                lv.touches += 1
                lv.last_touch = ts
                if accepted:
                    lv.breaches += 1
                    lv.last_result = "breach"
                else:
                    lv.holds += 1
                    lv.last_result = "hold"
                self._dirty = True
        except Exception as e:                                 # noqa: BLE001
            logger.debug("ledger on_closed_bar skipped: %s", e)

    # ── read side (nothing gates on this in v1) ──────────────────────────────

    def floors_below(self, price: float) -> List[Level]:
        """Levels below `price`, nearest first. The floor thesis' input."""
        try:
            out = [lv for lv in self.levels
                   if lv.kind == "low" and lv.price < price]
            return sorted(out, key=lambda lv: -lv.price)
        except Exception:                                      # noqa: BLE001
            return []

    def ceilings_above(self, price: float) -> List[Level]:
        try:
            out = [lv for lv in self.levels
                   if lv.kind == "high" and lv.price > price]
            return sorted(out, key=lambda lv: lv.price)
        except Exception:                                      # noqa: BLE001
            return []

    def coverage(self) -> Dict[str, int]:
        highs = sum(1 for lv in self.levels if lv.kind == "high")
        lows = sum(1 for lv in self.levels if lv.kind == "low")
        return {"highs": highs, "lows": lows,
                "meets_minimum": int(highs >= MIN_LEVELS_PER_SIDE
                                     and lows >= MIN_LEVELS_PER_SIDE)}

    # ── persistence ──────────────────────────────────────────────────────────

    def write(self, force: bool = False) -> bool:
        """Atomic rewrite of the current book. Returns True if it wrote.

        Atomic because a strategy may read this file while the loop writes it;
        a half-written JSON would be read as a corrupt or EMPTY level set, and
        an empty level set is indistinguishable from "no levels found" — a
        silent wrong answer rather than a loud failure.
        """
        try:
            if not self._dirty and not force:
                return False
            if not self.date:
                return False
            day_dir = os.path.join(_OUT_ROOT, self.date)
            os.makedirs(day_dir, exist_ok=True)
            path = os.path.join(day_dir, f"{self.symbol}.json")
            payload = {
                "schema_version": SCHEMA_VERSION,
                "symbol": self.symbol,
                "date": self.date,
                "coverage": self.coverage(),
                "touch_tol_pct": TOUCH_TOL_PCT,
                "levels": [lv.as_dict() for lv in self.levels],
            }
            fd, tmp = tempfile.mkstemp(dir=day_dir, suffix=".tmp")
            with os.fdopen(fd, "w") as f:
                json.dump(payload, f, default=str)
            os.replace(tmp, path)                  # atomic on POSIX
            self._dirty = False
            return True
        except Exception as e:                                 # noqa: BLE001
            logger.debug("ledger write skipped: %s", e)
            return False


_LEDGER: Optional[LiquidityLedger] = None


def get_ledger(symbol: str = "") -> LiquidityLedger:
    global _LEDGER
    if _LEDGER is None:
        _LEDGER = LiquidityLedger(symbol or os.environ.get("OT_INSTRUMENT", "?"))
    return _LEDGER
