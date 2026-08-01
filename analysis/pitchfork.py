"""
analysis/pitchfork.py — options_trader_v3 — v1.1

PF.1 CONSTRUCT. Andrews pitchfork geometry. Weight 0. Consumed by nothing,
gating nothing. See docs/WHITEPAPER_pitchfork_overlay.md for the full design.

v1.1 — 2026-08-01 — REJECTION REASONS. build_fork returned a bare None, so when
        a2_rail_drift found 1,030 ticks with no usable fork there was no way to
        tell WHY: a corpus too short to contain a qualifying triple, or §4.3
        filters too tight for a ~105-bar hourly series. Those have opposite
        responses — wait for sessions to accrue, vs revisit the priors. Every
        return-None path now records a reason in `last_reject_reason()`.
        Additive only: no filter, threshold or geometry changed, and the return
        contract is unchanged. Read by tests/pitchfork_filter_audit.py.
v1.0 — 2026-08-01 — first construct. Deterministic anchor selection, three
        variants in parallel, rails as anchor + slope*(bars from anchor).

WHY THIS IS A PERSISTENT OBJECT AND NOT AN INDICATOR
    Every level the system trades against today is horizontal or static — BB,
    VWAP, named pools, ORB boundaries, fixed-% stops. A trend is a SLOPED
    CHANNEL and nothing in the system represents one.
    Deeper than that: an indicator recomputes from a window each tick and
    remembers nothing, so the bot can never hold a belief about its environment
    across time. A fork is an assertion — "this channel is in effect until
    invalidated" — which is what recognition means here. Three properties follow,
    and none of them are optional:

      RECONSTRUCTIBLE   Anchor selection is a PURE FUNCTION of the tape, so fork
                        state can always be rederived from bars. State that
                        cannot be rederived is where errors compound invisibly.
                        Unlike the L2 integrator's path-dependent book,
                        persistence here is a startup optimisation, NOT a
                        correctness requirement. Do not trade this away later for
                        a heuristic that looks better on a chart.
      HONEST ABOUT TIME §4.4's confirmation-lag rule is enforced structurally, not
                        by convention: a fork is born at index(P2) + k bars and
                        `born_idx` is computed, never passed in. A swing low is
                        not knowable until k bars after it prints, and a backtest
                        that anchors at the pivot's own timestamp is fiction.
      SELF-DESCRIBING   Every Fork carries its anchors, variant, birth index, the
                        lag applied, and the filters it passed. What the bot
                        claims to see has to be auditable rather than asserted.

WHY THIS MODULE DEFINES ITS OWN SWING PIVOTS — and the ugly part, stated plainly
    The white paper §4.1 says LiquidityMapper already computes swing pivots and
    that the overlay consumes those rather than introducing a second definition.
    **That is not true at HEAD, and the paper needs correcting.** LiquidityMapper
    computes equal-high/low PRICE CLUSTERS (_find_pools), sweeps and named session
    levels — no fractal pivot anywhere. The real implementation is
    utils.math_utils.find_swing_highs/lows, consumed by StructureAnalyzer.

    Consuming that shared helper was considered and rejected for THREE reasons:

      1. SEGREGATION. find_swing_highs feeds StructureAnalyzer ->
         structure_sequence -> a HARD VETO in regime_confluence._trending, plus
         the A4 invariant. Putting pitchfork evolution inside a function the live
         gate reads makes every PF.2/PF.3 anchor tweak a diff against the trading
         path. A definition owned by this module can change freely for six weeks
         and can be DELETED outright if the overlay does not earn its keep.
      2. THE FREEZE. L2.6 protects L1/L2/entry BEHAVIOUR. A weight-0 object is
         genuinely outside it; editing a helper the veto reads is arguably inside.
      3. IT WOULD BE A DIFFERENT DEFINITION ANYWAY. The paper needs a FIXED k
         (2 daily, 3 hourly). _find_swings uses `lb = min(SWING_LOOKBACK,
         len(highs)//4)` — fractal order DERIVED FROM FRAME LENGTH, so anchors
         would shift as the frame grows. That is §4.4's failure mode arriving
         through a different door.

    DEFECT FOUND IN THE SHARED HELPER, NOT FIXED HERE, DELIBERATELY FILED:
    utils.math_utils.find_swing_highs tests `prices[i] == max(window)` — float
    equality. On equal highs it emits BOTH bars as pivots, which would break the
    alternation a P0/P1/P2 triple depends on. It also affects StructureAnalyzer's
    swing sets today, so fixing it changes structure_sequence, which changes
    TRENDING's veto, which changes what gets traded — three weeks before go-live.
    It is a real defect and it is written down rather than routed around; the fix
    belongs post-freeze. This module simply does not inherit it (see _pivots).

    ATTRIBUTION RISK this creates, and the mitigation: if the fork uses different
    pivots, a credit improvement at PF.3 could come from the better pivots rather
    than the fork geometry. Mitigated the same way the paper handles Schiff vs
    Modified Schiff — log BOTH pivot sets in parallel during shadow and record
    which triple each would select, so PF.3 attributes with data instead of
    argument. `pivots_shared()` exists for exactly that comparison.

WHY SLOPE IS PER BAR, NOT PER SECOND
    A pitchfork is drawn on a chart, and charts compress non-trading time. In
    wall-clock space a daily fork's slope would be diluted by every weekend and
    holiday, and the rails would sag away from price across a long gap. Slope is
    therefore RISE PER BAR on the anchor timeframe, and rails are evaluated at a
    bar index. `rail_at_time()` maps a timestamp to an index against the same
    frame the fork was built from, so callers can still ask in time terms.

NOT IMPLEMENTED HERE, ON PURPOSE
    Lifecycle/invalidation (§5), multi-fork resolution (§6) and every consumer in
    §7 are later phases. §12 names CONSUMER SPRAWL as a headline risk and this
    project has already paid for it once. This file computes geometry and stops.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import pandas as pd

logger = logging.getLogger(__name__)

# ── §4.2 anchor timeframes. 5m/1m are execution frames and are deliberately
# excluded — a fork that re-anchors constantly is a lagging indicator in costume.
FRACTAL_K: Dict[str, int] = {"1d": 2, "1h": 3}

# ── §4.3 qualification filters. Pre-registered starting values; §10 names the
# ten-parameter surface as an overfitting risk, so these are PRIORS, not fits.
SIGNIFICANCE_ATR = 1.0     # S — |P1-P0| and |P2-P1| must each clear S * ATR
RECENCY_BARS     = 40      # R — P2's CONFIRMATION must be within R bars of now

# Why the most recent build_fork call returned None. Diagnostic only — nothing
# in the geometry reads it, and it is deliberately NOT part of the return
# contract, so no caller can start branching on it.
_LAST_REJECT: Optional[str] = None


def last_reject_reason() -> Optional[str]:
    """Reason the most recent build_fork() returned None, or None on success."""
    return _LAST_REJECT


def _reject(reason: str):
    global _LAST_REJECT
    _LAST_REJECT = reason
    return None


VARIANTS = ("andrews", "schiff", "modified_schiff")
DEFAULT_VARIANT = "modified_schiff"


@dataclass(frozen=True)
class Pivot:
    """A confirmed fractal pivot. `confirmed_idx` is when it became KNOWABLE."""
    idx: int                 # bar index where the extreme printed
    price: float
    kind: str                # "high" | "low"
    k: int
    timeframe: str

    @property
    def confirmed_idx(self) -> int:
        """§4.4 — not knowable until k bars after it prints."""
        return self.idx + self.k


@dataclass(frozen=True)
class Fork:
    """A pitchfork: a persistent geometric assertion about the tape.

    Carries its own provenance so what it claims can be audited — anchors,
    variant, when it was born, the lag applied, and which filters it passed.
    """
    symbol: str
    timeframe: str
    direction: str                  # "bullish" | "bearish"
    variant: str
    p0: Pivot
    p1: Pivot
    p2: Pivot
    # effective handle origin after the variant transform (§3.2)
    origin_idx: float
    origin_price: float
    # the median line's slope, in price per BAR on `timeframe`
    slope: float
    born_idx: int                   # §4.4 — index(P2) + k. Computed, never given.
    k: int
    atr_at_birth: float
    filters_passed: Tuple[str, ...] = field(default_factory=tuple)

    # ── rails ────────────────────────────────────────────────────────────────
    def median_at(self, idx: float) -> float:
        return self.origin_price + self.slope * (idx - self.origin_idx)

    def _offset(self, pivot: Pivot) -> float:
        """Perpendicular offset of a parallel rail, expressed as a price delta at
        the pivot's own index — which is all a same-slope parallel needs."""
        return pivot.price - self.median_at(pivot.idx)

    def upper_at(self, idx: float) -> float:
        """UML — through P1 (bullish) / P2 (bearish), per §3.1."""
        through = self.p1 if self.direction == "bullish" else self.p2
        return self.median_at(idx) + self._offset(through)

    def lower_at(self, idx: float) -> float:
        """LML — through P2 (bullish) / P1 (bearish), per §3.1."""
        through = self.p2 if self.direction == "bullish" else self.p1
        return self.median_at(idx) + self._offset(through)

    def rails_at(self, idx: float) -> Dict[str, float]:
        return {"upper": self.upper_at(idx),
                "median": self.median_at(idx),
                "lower": self.lower_at(idx)}

    def channel_width_at(self, idx: float) -> float:
        return abs(self.upper_at(idx) - self.lower_at(idx))

    def is_born_by(self, idx: int) -> bool:
        """§4.4 guard. Any caller evaluating a fork before this is using
        information that did not exist."""
        return idx >= self.born_idx

    def rail_at_time(self, ts: pd.Timestamp, index: pd.DatetimeIndex) -> Dict[str, float]:
        """Evaluate in time terms by mapping the timestamp to a bar index on the
        SAME frame the fork was built from. Bars beyond the frame extrapolate at
        one index per bar, which is the charting convention the slope assumes."""
        pos = index.searchsorted(ts)
        return self.rails_at(float(pos))

    def describe(self) -> str:
        return (f"{self.symbol} {self.timeframe} {self.direction} "
                f"[{self.variant}] P0={self.p0.price:.2f}@{self.p0.idx} "
                f"P1={self.p1.price:.2f}@{self.p1.idx} "
                f"P2={self.p2.price:.2f}@{self.p2.idx} "
                f"slope={self.slope:.4f}/bar born@{self.born_idx} "
                f"(lag {self.k} bars) filters={','.join(self.filters_passed)}")


# ── pivots ───────────────────────────────────────────────────────────────────
def _pivots(highs: Sequence[float], lows: Sequence[float], k: int,
            timeframe: str) -> List[Pivot]:
    """Fixed-k fractal pivots, in bar order.

    Strict inequality on BOTH sides. utils.math_utils uses `prices[i] ==
    max(window)`, which on equal highs marks every tied bar a pivot and destroys
    the alternation a triple depends on. A plateau here yields no pivot at all,
    which is the honest answer: a flat top has no single turning bar.
    """
    out: List[Pivot] = []
    n = min(len(highs), len(lows))
    for i in range(k, n - k):
        left_h, right_h = highs[i - k:i], highs[i + 1:i + k + 1]
        if all(highs[i] > h for h in left_h) and all(highs[i] > h for h in right_h):
            out.append(Pivot(i, float(highs[i]), "high", k, timeframe))
            continue                      # one bar cannot be both
        left_l, right_l = lows[i - k:i], lows[i + 1:i + k + 1]
        if all(lows[i] < v for v in left_l) and all(lows[i] < v for v in right_l):
            out.append(Pivot(i, float(lows[i]), "low", k, timeframe))
    return out


def pivots_shared(highs: Sequence[float], lows: Sequence[float],
                  lookback: int, timeframe: str) -> List[Pivot]:
    """The SHARED definition (utils.math_utils), for side-by-side logging only.

    Exists so PF.3 can attribute a measured improvement to fork geometry rather
    than to better pivots — see the module docstring. Never used to build a fork.
    """
    from utils.math_utils import find_swing_highs, find_swing_lows
    out = [Pivot(i, float(p), "high", lookback, timeframe)
           for i, p in find_swing_highs(list(highs), lookback)]
    out += [Pivot(i, float(p), "low", lookback, timeframe)
            for i, p in find_swing_lows(list(lows), lookback)]
    return sorted(out, key=lambda p: p.idx)


def _alternating_tail(pivots: List[Pivot]) -> List[Pivot]:
    """Collapse runs of same-kind pivots to the most EXTREME of each run, so the
    sequence strictly alternates. §4.3.5 wants the three most recent confirmed
    alternating pivots — no search, no best fit."""
    if not pivots:
        return []
    out: List[Pivot] = [pivots[0]]
    for p in pivots[1:]:
        if p.kind == out[-1].kind:
            better = (p.price > out[-1].price) if p.kind == "high" else (p.price < out[-1].price)
            if better:
                out[-1] = p
        else:
            out.append(p)
    return out


# ── variants (§3.2) ──────────────────────────────────────────────────────────
def _origin(p0: Pivot, p1: Pivot, variant: str) -> Tuple[float, float]:
    """Effective handle origin (idx, price) after the variant transform."""
    if variant == "andrews":
        return float(p0.idx), p0.price
    if variant == "schiff":                       # price only
        return float(p0.idx), (p0.price + p1.price) / 2.0
    if variant == "modified_schiff":              # time AND price
        return (p0.idx + p1.idx) / 2.0, (p0.price + p1.price) / 2.0
    raise ValueError(f"unknown variant {variant!r}")


def build_fork(symbol: str, df: pd.DataFrame, timeframe: str, atr: float,
               variant: str = DEFAULT_VARIANT,
               now_idx: Optional[int] = None,
               significance_atr: float = SIGNIFICANCE_ATR,
               recency_bars: int = RECENCY_BARS) -> Optional[Fork]:
    """Build the one qualifying fork for (symbol, timeframe), or None.

    Pure function of the frame — same bars in, same fork out, always. `atr` is
    passed rather than computed so this module owns no second ATR definition.
    Returns None (never raises, never guesses) when no triple qualifies.
    """
    k = FRACTAL_K.get(timeframe)
    if k is None:
        logger.debug("pitchfork: %s is not an anchor timeframe", timeframe)
        return _reject("NOT_ANCHOR_TF")
    if df is None or len(df) < (2 * k + 1) * 3:
        return _reject("FRAME_TOO_SHORT")
    if not atr or atr <= 0:
        return _reject("NO_ATR")

    highs, lows = df["high"].tolist(), df["low"].tolist()
    now_idx = len(df) - 1 if now_idx is None else now_idx

    # §4.4 — only pivots already CONFIRMED as of now_idx may be used.
    confirmed = [p for p in _pivots(highs, lows, k, timeframe)
                 if p.confirmed_idx <= now_idx]
    alt = _alternating_tail(confirmed)
    if len(alt) < 3:
        return _reject("FEWER_THAN_3_ALTERNATING_PIVOTS")

    p0, p1, p2 = alt[-3], alt[-2], alt[-1]
    passed: List[str] = []

    # 3. structural validity — bullish needs P2 > P0, bearish P2 < P0
    if p0.kind == "low" and p1.kind == "high":
        direction = "bullish"
        if not p2.price > p0.price:
            return _reject("STRUCTURAL_bull_P2_not_above_P0")
    elif p0.kind == "high" and p1.kind == "low":
        direction = "bearish"
        if not p2.price < p0.price:
            return _reject("STRUCTURAL_bear_P2_not_below_P0")
    else:
        return _reject("STRUCTURAL_pivot_kinds_not_alternating")
    passed.append("structural")

    # 1. significance — each leg must be a real move, not noise
    if abs(p1.price - p0.price) < significance_atr * atr:
        return _reject("SIGNIFICANCE_leg_P0P1")
    if abs(p2.price - p1.price) < significance_atr * atr:
        return _reject("SIGNIFICANCE_leg_P1P2")
    passed.append("significance")

    # 2. separation — non-overlapping fractal windows
    if (p1.idx - p0.idx) < (2 * k + 1) or (p2.idx - p1.idx) < (2 * k + 1):
        return _reject("SEPARATION")
    passed.append("separation")

    # 4. recency — measured on CONFIRMATION, not on the pivot's own bar
    if (now_idx - p2.confirmed_idx) > recency_bars:
        return _reject("RECENCY")
    passed.append("recency")
    passed.append("uniqueness")           # by construction: the last three

    origin_idx, origin_price = _origin(p0, p1, variant)
    m_idx = (p1.idx + p2.idx) / 2.0
    m_price = (p1.price + p2.price) / 2.0
    if m_idx == origin_idx:
        return _reject("DEGENERATE_vertical_median")
    slope = (m_price - origin_price) / (m_idx - origin_idx)

    global _LAST_REJECT
    _LAST_REJECT = None
    return Fork(symbol=symbol, timeframe=timeframe, direction=direction,
                variant=variant, p0=p0, p1=p1, p2=p2,
                origin_idx=origin_idx, origin_price=origin_price, slope=slope,
                born_idx=p2.idx + k, k=k, atr_at_birth=float(atr),
                filters_passed=tuple(passed))


def build_all_variants(symbol: str, df: pd.DataFrame, timeframe: str,
                       atr: float, **kw) -> Dict[str, Optional[Fork]]:
    """All three variants on the same anchors, per §3.2 — the choice is settled
    by measurement during shadow, not by the design document. Cost is three sets
    of three linear functions."""
    return {v: build_fork(symbol, df, timeframe, atr, variant=v, **kw)
            for v in VARIANTS}
