"""
analysis/pitchfork_lifecycle.py — options_trader_v3 — v1.1

PF/AS. §5 of docs/WHITEPAPER_pitchfork_overlay.md — the fork HOLDS UNTIL
INVALIDATED. Weight 0. Consumed by nothing, gating nothing.

v1.1 — 2026-08-03 — coverage() UNDERCOUNTED SUPERSESSION CHAINS. It paired only
        BORN→INVALIDATED, but a supersession emits SUPERSEDED then BORN, so each
        new BORN overwrote the open span without banking it and every held bar
        before the LAST fork vanished. On a churn-heavy frame it reported 1.8%
        coverage against a 42.2% birth rate — coverage below the birth rate is
        arithmetically impossible and would have read as the fork being MORE
        starved than before lifecycle existed. Caught by running it, not reading
        it.
v1.0 — 2026-08-03 — first lifecycle. Birth, persistence, the four invalidation
        conditions, and the acceleration asymmetry.
        A SPENT TRIPLE CANNOT RE-BIRTH, and the tests are what found it. The
        first cut retired a fork and then, on the SAME bar, called build_fork —
        which still saw the same qualifying P0/P1/P2 and handed back an identical
        fork. A structural break killed it and it reincarnated instantly. §5.1 is
        precise: birth is "at P2 CONFIRMATION", a specific bar, not "whenever a
        triple qualifies". So the retired fork's P2 index is remembered and the
        next birth requires a STRICTLY NEWER P2. Without lifecycle tests this
        would have shipped and every invalidation would have been a no-op.

WHY THIS EXISTS — the bug it fixes is mine, and it invalidated a measurement
    PF.1 shipped geometry only and said so ("this file computes geometry and
    stops"). Then `tests/a2_rail_drift.py` called `build_fork` once per hourly bar
    and used the result only when it returned non-None. `build_fork` is STATELESS
    — it recomputes from scratch every call — so that treated the fork as a
    PER-BAR INDICATOR, which is precisely what §5.2 says it is not:

        "The fork holds until invalidated. It is explicitly *not* recomputed each
         bar, each tick, or each session."

    The filter audit then measured 156 forks from 2,297 attempts and called it
    6.8%. That is the BIRTH RATE, not coverage. 156 births across 29 symbols is
    ~5 anchor events per symbol in three weeks — entirely reasonable for a
    PERSISTENT object. With lifecycle, one fork born at hour 20 covers hours 20 →
    invalidation, which can be days. Predictor 2's starvation (n=78, REFUSED at
    every horizon) is expected to be a consequence of that error rather than a
    property of the data.

    This is also the persistence mandate made literal: the fork is the bot
    asserting "this channel is in effect until something ends it". A per-bar
    recompute cannot hold a belief across time, and holding beliefs across time
    is the whole point.

RECONSTRUCTIBLE FROM TAPE — the property everything else rests on
    `replay()` walks a frame bar by bar and produces the complete fork history
    deterministically. Same bars in, same history out, always. So tracker state
    is never load-bearing: it can always be rederived, which is what separates
    this from the L2 integrator's path-dependent book. Persistence to disk would
    be a startup optimisation, never a correctness requirement. Do not trade that
    away later for a heuristic that looks better on a chart.

THE FOUR CONDITIONS (§5.3), and the one that is NOT a condition
    (a) STRUCTURAL BREAK — a close beyond P0 in the invalidating direction
        (bullish: close < P0.price). The leg that defined the fork is gone, so is
        the fork. Strongest and cleanest.
    (b) ADVERSE TINE BREAK — N consecutive anchor-timeframe closes beyond the
        COUNTER-TREND tine by >= D x ATR. N=2, D=0.25 as the paper's priors.
    (c) SUPERSESSION — a newer qualifying triple with a more recent P2 AND
        materially different geometry. The material-difference guard is what
        prevents churn; without it every marginal new pivot re-anchors.
    (d) STALENESS — no rail interaction within Z x ATR for W bars. **SHIPS OFF.**
        §5.3(d) says measure before enabling, so it is implemented, defaulted
        off, and left off until shadow data justifies it.

    **TAGGING A RAIL IS NOT INVALIDATION.** §5.2: those are the tradeable events
    the overlay exists to produce. A fork that dies when price touches it has
    inverted its own purpose.

    **AND BREAKING THE TREND-SIDE TINE IS ACCELERATION, NOT INVALIDATION.**
    Andrews' own teaching, and §5.3 is emphatic: a bullish fork closing above its
    UML is not wrong, it is UNDERSTATING the move. Flagged as an event, never
    fatal. This asymmetry is the single easiest thing to get backwards — a naive
    "price left the channel, kill it" rule would kill forks on exactly the moves
    they called correctly.

PARAMETERS NOT GIVEN BY THE PAPER
    §5.3(c) specifies "slope differing by > X%" and "median displaced by > Y x
    ATR" without values. Pre-registered here as X=25%, Y=1.0 — deliberately loose,
    because the guard exists to stop churn and a tight guard defeats it. §10 names
    the ten-parameter surface as a headline overfitting risk, so these are PRIORS
    to be measured against, not fitted.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd

from analysis.pitchfork import DEFAULT_VARIANT, Fork, build_fork, last_reject_reason

logger = logging.getLogger(__name__)

# §5.3(b) — adverse tine break
ADVERSE_CLOSES = 2          # N
ADVERSE_ATR = 0.25          # D

# §5.3(c) — supersession's material-difference guard. Not given by the paper;
# pre-registered loose, because a tight guard reintroduces the churn it prevents.
SUPERSEDE_SLOPE_PCT = 0.25  # X — |slope change| / |old slope|
SUPERSEDE_MEDIAN_ATR = 1.0  # Y — median displacement in ATR

# §5.3(d) — staleness. SHIPS OFF. Implemented so the measurement is possible.
STALE_ENABLED = False
STALE_TOUCH_ATR = 0.25      # Z — within this of a rail counts as interaction
STALE_BARS = 60             # W

BORN = "BORN"
INVALIDATED = "INVALIDATED"
SUPERSEDED = "SUPERSEDED"
ACCELERATION = "ACCELERATION"
TOUCH = "TOUCH"


@dataclass(frozen=True)
class ForkEvent:
    """One thing that happened to a fork, with the bar it happened on.

    The event log IS the provenance — what the bot claims to have seen, when it
    saw it, and why it stopped believing it. A fork that vanished with no
    INVALIDATED event would be unauditable.
    """
    kind: str
    idx: int
    reason: str
    symbol: str
    timeframe: str
    direction: str = ""
    detail: Dict = field(default_factory=dict)

    def __str__(self) -> str:
        d = " ".join(f"{k}={v}" for k, v in self.detail.items())
        return (f"[{self.idx:>4}] {self.kind:<12} {self.symbol} {self.timeframe} "
                f"{self.direction:<8} {self.reason}" + (f" | {d}" if d else ""))


class ForkTracker:
    """Holds AT MOST ONE active fork for a (symbol, timeframe) — §6's rule — and
    steps it forward one bar at a time.

    Stateful by design, but never authoritative: `replay()` rebuilds the whole
    history from bars, so the state is a cache of something always recomputable.
    """

    def __init__(self, symbol: str, timeframe: str,
                 variant: str = DEFAULT_VARIANT,
                 adverse_closes: int = ADVERSE_CLOSES,
                 adverse_atr: float = ADVERSE_ATR,
                 stale_enabled: bool = STALE_ENABLED,
                 stale_bars: int = STALE_BARS):
        self.symbol = symbol
        self.timeframe = timeframe
        self.variant = variant
        self.adverse_closes = adverse_closes
        self.adverse_atr = adverse_atr
        self.stale_enabled = stale_enabled
        self.stale_bars = stale_bars

        self.active: Optional[Fork] = None
        self.events: List[ForkEvent] = []
        # Which fork was ACTIVE at each bar index. This is what a consumer needs:
        # asking "was a fork in effect at bar i" is the whole point of a
        # persistent object, and it is not answerable from build_fork, which only
        # ever says "could one be built from scratch here".
        self.active_by_idx: Dict[int, Fork] = {}
        self._adverse_run = 0          # consecutive closes beyond the counter tine
        self._last_touch_idx: Optional[int] = None
        self._born_idx: Optional[int] = None
        # §5.1 — birth is at P2 CONFIRMATION, not at any bar where a triple
        # happens to qualify. A retired fork's triple is SPENT: without this the
        # same P0/P1/P2 is rebuilt on the very next call and invalidation becomes
        # a no-op, which is exactly what the first cut did.
        self._spent_p2_idx: int = -1

    # ── helpers ─────────────────────────────────────────────────────────────
    def _log(self, kind, idx, reason, **detail):
        ev = ForkEvent(kind, idx, reason, self.symbol, self.timeframe,
                       self.active.direction if self.active else "", detail)
        self.events.append(ev)
        logger.debug("pitchfork %s", ev)
        return ev

    def _counter_tine(self, fk: Fork, idx: float) -> float:
        """The tine price ACTION must break to invalidate — the one opposite the
        trend. Bullish forks die below the LOWER rail; getting this backwards
        would kill forks on strength, which §5.3 explicitly forbids."""
        return fk.lower_at(idx) if fk.direction == "bullish" else fk.upper_at(idx)

    def _trend_tine(self, fk: Fork, idx: float) -> float:
        return fk.upper_at(idx) if fk.direction == "bullish" else fk.lower_at(idx)

    def _touched(self, fk: Fork, idx: int, high: float, low: float,
                 atr: float) -> bool:
        """Did the bar interact with any rail? Needed by staleness (d), and it is
        the raw material for §6's touch-count rail strength later."""
        tol = STALE_TOUCH_ATR * atr
        for rail in (fk.upper_at(idx), fk.median_at(idx), fk.lower_at(idx)):
            if (low - tol) <= rail <= (high + tol):
                return True
        return False

    # ── the one call a caller makes per bar ─────────────────────────────────
    def step(self, df: pd.DataFrame, atr: float, now_idx: int) -> Optional[Fork]:
        """Advance to bar `now_idx`. Returns the ACTIVE fork, or None.

        Order matters: invalidation is checked BEFORE birth, so a fork that dies
        on this bar can be replaced on the same bar rather than leaving a gap.
        """
        if df is None or now_idx <= 0 or now_idx >= len(df):
            return self.active
        result = self._step(df, atr, now_idx)
        if result is not None:
            self.active_by_idx[now_idx] = result
        return result

    def _step(self, df: pd.DataFrame, atr: float, now_idx: int) -> Optional[Fork]:
        bar = df.iloc[now_idx]
        close, high, low = float(bar["close"]), float(bar["high"]), float(bar["low"])

        if self.active is not None:
            fk = self.active

            # touch bookkeeping first — a touch is NOT invalidation (§5.2), it is
            # the event the overlay exists to produce, and it also resets (d).
            if atr > 0 and self._touched(fk, now_idx, high, low, atr):
                self._last_touch_idx = now_idx
                self._log(TOUCH, now_idx, "rail interaction")

            # (a) structural break — P0 violation, strongest and cleanest
            broke_p0 = (close < fk.p0.price if fk.direction == "bullish"
                        else close > fk.p0.price)
            if broke_p0:
                self._log(INVALIDATED, now_idx, "structural break: close beyond P0",
                          close=f"{close:.2f}", p0=f"{fk.p0.price:.2f}")
                self._retire()
            else:
                # ACCELERATION — trend-side tine broken. NOT fatal. §5.3's
                # asymmetry: the fork is understating the move, not wrong.
                trend_rail = self._trend_tine(fk, now_idx)
                beyond_trend = (close > trend_rail if fk.direction == "bullish"
                                else close < trend_rail)
                if beyond_trend:
                    self._log(ACCELERATION, now_idx,
                              "closed beyond the TREND-side tine — understating "
                              "the move, fork HELD",
                              close=f"{close:.2f}", rail=f"{trend_rail:.2f}")

                # (b) adverse tine break — N consecutive closes beyond the
                # COUNTER-trend tine by >= D * ATR
                counter = self._counter_tine(fk, now_idx)
                margin = self.adverse_atr * atr
                beyond_counter = (close < counter - margin
                                  if fk.direction == "bullish"
                                  else close > counter + margin)
                self._adverse_run = self._adverse_run + 1 if beyond_counter else 0
                if self._adverse_run >= self.adverse_closes:
                    self._log(INVALIDATED, now_idx,
                              f"adverse tine break: {self._adverse_run} closes "
                              f"beyond the counter tine by >= {self.adverse_atr} ATR",
                              close=f"{close:.2f}", rail=f"{counter:.2f}")
                    self._retire()

            # (d) staleness — implemented, SHIPS OFF (§5.3 says measure first)
            if (self.active is not None and self.stale_enabled
                    and self._born_idx is not None):
                since = now_idx - (self._last_touch_idx
                                   if self._last_touch_idx is not None
                                   else self._born_idx)
                if since >= self.stale_bars:
                    self._log(INVALIDATED, now_idx,
                              f"stale: no rail interaction for {since} bars",
                              bars=since)
                    self._retire()

        # (c) supersession, and birth when there is nothing active
        candidate = build_fork(self.symbol, df.iloc[:now_idx + 1], self.timeframe,
                               atr, variant=self.variant, now_idx=now_idx)

        if self.active is None:
            if candidate is not None and candidate.p2.idx <= self._spent_p2_idx:
                logger.debug("pitchfork %s %s idx=%d: triple P2=%d already spent",
                             self.symbol, self.timeframe, now_idx,
                             candidate.p2.idx)
                return None
            if candidate is not None:
                self.active = candidate
                self._born_idx = now_idx
                self._adverse_run = 0
                self._last_touch_idx = None
                self._log(BORN, now_idx, "qualifying triple confirmed",
                          slope=f"{candidate.slope:.4f}",
                          p2=f"{candidate.p2.idx}")
            else:
                # not an error — most bars have no qualifying structure, which is
                # the engine correctly refusing chop
                logger.debug("pitchfork %s %s idx=%d: no fork (%s)", self.symbol,
                             self.timeframe, now_idx, last_reject_reason())
            return self.active

        if candidate is not None and candidate.p2.idx > self.active.p2.idx:
            if self._materially_different(self.active, candidate, atr, now_idx):
                self._log(SUPERSEDED, now_idx,
                          "newer triple with materially different geometry",
                          old_slope=f"{self.active.slope:.4f}",
                          new_slope=f"{candidate.slope:.4f}")
                self.active = candidate
                self._born_idx = now_idx
                self._adverse_run = 0
                self._last_touch_idx = None
                self._log(BORN, now_idx, "supersession", p2=f"{candidate.p2.idx}")
        return self.active

    def _materially_different(self, old: Fork, new: Fork, atr: float,
                              idx: int) -> bool:
        """§5.3(c)'s churn guard. Without it every marginal new pivot re-anchors
        and the fork stops being persistent at all — which would reintroduce the
        per-bar-indicator bug this module exists to fix."""
        if abs(old.slope) > 0:
            if abs(new.slope - old.slope) / abs(old.slope) > SUPERSEDE_SLOPE_PCT:
                return True
        elif abs(new.slope) > 0:
            return True
        if atr > 0:
            if abs(new.median_at(idx) - old.median_at(idx)) > SUPERSEDE_MEDIAN_ATR * atr:
                return True
        return False

    def _retire(self):
        if self.active is not None:
            self._spent_p2_idx = max(self._spent_p2_idx, self.active.p2.idx)
        self.active = None
        self._adverse_run = 0
        self._last_touch_idx = None
        self._born_idx = None

    # ── coverage, the number the filter audit could not report ──────────────
    def coverage(self, n_bars: int) -> float:
        """Fraction of bars with an active fork. THIS is the number that matters;
        the filter audit's 6.8% was the BIRTH rate and they are not comparable."""
        if n_bars <= 0:
            return 0.0
        held, cur = 0, None
        for ev in self.events:
            if ev.kind == BORN:
                # v1.1 — bank the open span FIRST. A supersession emits
                # SUPERSEDED then BORN, so the old code overwrote `cur` without
                # accumulating and every held bar before the final fork was
                # discarded. On a churn-heavy frame that reported coverage BELOW
                # the birth rate, which is impossible and would have looked like
                # the fork being even more starved than before lifecycle existed.
                if cur is not None:
                    held += ev.idx - cur
                cur = ev.idx
            elif ev.kind == INVALIDATED and cur is not None:
                held += ev.idx - cur
                cur = None
        if cur is not None:
            held += n_bars - 1 - cur
        return held / n_bars


def replay(symbol: str, df: pd.DataFrame, timeframe: str, atr_series_vals,
           start: int = 20, **kw) -> ForkTracker:
    """Walk the frame bar by bar and produce the full fork history.

    Deterministic: same bars in, same history out. This is what makes tracker
    state a cache rather than a source of truth — and it is the only honest way
    to measure coverage, since coverage is a property of the SEQUENCE, not of any
    single bar.

    `atr_series_vals` is indexed like `df` so each bar is judged on the ATR that
    obtained AT THAT BAR, not on a single end-of-frame value.
    """
    tr = ForkTracker(symbol, timeframe, **kw)
    for i in range(start, len(df)):
        try:
            atr = float(atr_series_vals[i])
        except Exception:                                        # noqa: BLE001
            atr = 0.0
        if atr <= 0:
            continue
        tr.step(df, atr, i)
    return tr
