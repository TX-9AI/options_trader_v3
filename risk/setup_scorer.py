"""
risk/setup_scorer.py — Scores and grades options trade signals A/B.
v1.4 — 2026-07-22 — ORB IS A GEOMETRY GATE, NOT A WEIGHTED SCORE. The ORB
        was being run through the same 5-dimension weighted sum as every
        other strategy (regime_conviction, orb_quality, vwap_alignment,
        liquidity_clear, macro_context). That was wrong for this trade by
        design: the ORB is regime-AGNOSTIC (it is deliberately not regime-
        gated at dispatch) yet regime_conviction was 20%% of its grade; VWAP
        and macro have no bearing on a mechanically-confirmed break+retest;
        and orb_quality was a confluence-COUNT proxy (0.2*n) that never
        measured the geometry its docstring claimed. Net effect: the A/B
        grade of an ORB was regime conviction in costume, and liquidity-in-
        path could VETO a confirmed setup by dragging the weighted total
        under the bar.
        NOW: the ORB short-circuits BEFORE the weighted machinery. A
        confirmed ORB ALWAYS trades. The ONLY grade input is whether an
        unswept liquidity pool sits between the breakout and the 100%% TP:
          - clear path  -> A (1.5x size)
          - pool in path -> B (1.0x size)
        Liquidity can downgrade A->B; it can NEVER veto. No regime, no VWAP,
        no macro, no confluence count, no brief nudge, no session modifier
        touch the ORB grade. _orb_quality is DELETED. The 5-dimension path is
        unchanged for SweepReversal / Butterfly / Condor / default.
v1.3 — 2026-07-18 — SIGNAL JOURNAL (ROADMAP Phase 3.1 instrumentation, log-only):
        every scored signal — including below-B REJECTS — emits one `scored`
        event to analysis/signal_journal with the full breakdown, thresholds,
        regime conviction, quote context (bid/ask/spread/IV at signal time)
        and vol/macro snapshot. Zero behavior change: the journal call is
        wrapped so any failure degrades to a missing log line, never an
        exception; grading logic is untouched. This is the perishable data
        the Phase-3 conviction-bar buckets need — "a gate you can't
        counterfactual is a gate you can't calibrate."
v1.2 — 2026-07-15 — BRIEF NUDGE: a signed post-sum adjustment (cap ±0.05) from
        the pre-market move-probability brief. This box reads its own line from
        ~/brief_flags.json ({symbol, strength 0..1, date}); the nudge is
        +strength·cap for ORB (catalyst helps a breakout), -strength·cap for
        butterfly/condor (catalyst fights a pin/range), and ZERO for sweep
        reversal (structure-driven, catalyst-agnostic). Applied to the final
        total AFTER the weighted sum and late-session modifier, BEFORE the
        grade compare — so the ±0.05 lands literally on the score as a
        tie-breaker; it can never rescue a bad setup or sink a good one.
        Absent/stale/mismatched flag file => strength 0 => no nudge. Knob:
        config.BRIEF_CONVICTION_WEIGHT (default 0.05).
v3.0 — original release — A/B/C grading
v1.1 — 2026-06-30 — eliminated C grade entirely. There is no such thing
        as a C-grade setup by definition — anything below the B threshold
        is not a valid trade and returns None instead of a downsized
        position. This prevents marginal/low-conviction setups from ever
        firing in live trading regardless of available capital.
        Grade determines position size multiplier: A=1.5x, B=1.0x.
v1.2 — 2026-07-02 — remove duplicate Fed-day boost. is_fed_day was being
        applied twice on ORB: once in the macro_context dimension (its
        designated home) and again inside _orb_quality, double-counting the
        effect and polluting a dimension that measures confluence/regime/
        liquidity. Fed-day now boosts ORB through macro_context only.
v3.0 — 2026-07-10 — repo-wide v3.0 bump: Yahoo-Finance purge & data stream
        mapping optimization (all market data now flows from the single
        shared TastyTrade candle feed — see data/candle_feed.py). No logic
        change in this file.
"""

import logging
from dataclasses import dataclass
from typing import Optional

from strategy.base_strategy import OptionsSignal
from analysis.regime_classifier import RegimeState, Regime
from analysis.volatility_engine import VolatilityState
from analysis.structure_analyzer import StructureMap
from analysis.liquidity_mapper import LiquidityMap
from data.macro_data import MacroSnapshot
from config import GRADE_SIZE_MULTIPLIER, GRADE_A_MIN_SCORE, GRADE_B_MIN_SCORE
try:
    from config import BRIEF_CONVICTION_WEIGHT
except Exception:
    BRIEF_CONVICTION_WEIGHT = 0.05
from utils.time_utils import current_session_label

# Signal journal (v1.3) — log-only instrumentation. Guarded import: if the
# module is absent or broken the scorer runs exactly as before.
try:
    from analysis import signal_journal as _journal
except Exception:
    _journal = None

logger = logging.getLogger(__name__)


@dataclass
class SetupScore:
    grade:           str   = "B"
    score:           float = 0.0
    size_multiplier: float = 1.0
    breakdown:       dict  = None

    def __post_init__(self):
        if self.breakdown is None:
            self.breakdown = {}


# ─── Strategy-specific scoring profiles ──────────────────────────────────────

STRATEGY_PROFILES = {
    # ORB IS NOT SCORED HERE (v1.4). It short-circuits to _grade_orb before the
    # weighted sum: a confirmed ORB always trades, graded A/B on liquidity-in-
    # path ONLY. This profile is retained for reference/telemetry but these
    # weights are DEAD for the ORB — do not re-point score() at them.
    "ORBStrategy": {
        "score_weights": {},   # unused — see _grade_orb
        "grade_a": 0.78,       # retained for any legacy reader; not applied
        "grade_b": 0.55,
    },
    "SweepReversal": {
        "score_weights": {
            "regime_conviction":    0.25,
            "sweep_quality":        0.35,   # Rejection %, freshness, named level
            "vwap_alignment":       0.10,
            "liquidity_clear":      0.20,
            "macro_context":        0.10,
        },
        "grade_a": 0.75,
        "grade_b": 0.52,
    },
    "ButterflyStrategy": {
        "score_weights": {
            "regime_conviction":    0.30,   # Need clean ranging regime
            "range_quality":        0.35,   # BB width, ADX, time in range
            "vwap_alignment":       0.15,
            "liquidity_clear":      0.10,
            "macro_context":        0.10,
        },
        "grade_a": 0.75,
        "grade_b": 0.52,
    },
    "default": {
        "score_weights": {
            "regime_conviction":    0.30,
            "signal_quality":       0.25,
            "vwap_alignment":       0.15,
            "liquidity_clear":      0.20,
            "macro_context":        0.10,
        },
        "grade_a": 0.78,
        "grade_b": 0.55,
    },
}


class SetupScorer:
    """
    Scores an options signal using strategy-specific weights.
    Returns A or B grade only — anything scoring below the B threshold
    is not a valid trade and returns None.
    """

    def _brief_strength(self) -> float:
        """This box's pre-market move-strength (0..1) from ~/brief_flags.json,
        cached for the process. Any problem — missing file, stale date, wrong
        symbol, malformed — yields 0.0 (no nudge). Never raises."""
        if getattr(self, "_brief_cached", None) is not None:
            return self._brief_cached
        strength = 0.0
        try:
            import os, json, datetime
            path = os.path.expanduser("~/brief_flags.json")
            my_symbol = os.environ.get("OT_INSTRUMENT", "")
            if os.path.isfile(path):
                with open(path) as fh:
                    d = json.load(fh)
                today = datetime.date.today().isoformat()
                if d.get("symbol") == my_symbol and d.get("date") == today:
                    strength = max(0.0, min(1.0, float(d.get("strength", 0.0))))
        except Exception:
            strength = 0.0
        self._brief_cached = strength
        return strength

    def score(self,
              signal:    OptionsSignal,
              regime:    RegimeState,
              vol_state: VolatilityState,
              structure: StructureMap,
              liq_map:   LiquidityMap,
              macro:     Optional[MacroSnapshot] = None) -> Optional[SetupScore]:
        """
        Returns SetupScore for A or B grade setups only.
        Returns None if the setup scores below the B threshold —
        there is no C grade. A below-threshold setup is not a trade.
        """

        breakdown = {}
        name      = signal.strategy_name
        profile   = STRATEGY_PROFILES.get(name, STRATEGY_PROFILES["default"])
        weights   = profile["score_weights"]
        grade_a   = profile["grade_a"]
        grade_b   = profile["grade_b"]

        # ── ORB: geometry gate, not a weighted score (v1.4) ───────────────────
        # A confirmed ORB break+retest ALWAYS trades — the ORB state machine
        # already validated the geometry (body/wick rules) before this signal
        # existed, and the trade is regime-agnostic by design. The ONLY grade
        # input is liquidity in the path to the 100%% TP: clear -> A, pool in
        # the way -> B. Never a veto. Nothing else (regime/VWAP/macro/session/
        # brief) touches it. Returns here, before the 5-dimension machinery.
        if name == "ORBStrategy":
            return self._grade_orb(signal, liq_map, regime, vol_state, macro)

        # ── 1. Regime Conviction ──────────────────────────────────────────────
        reg_score = regime.conviction
        breakdown["regime_conviction"] = round(reg_score, 3)

        # ── 2. Strategy-specific quality score ───────────────────────────────
        if name == "SweepReversal":
            quality_score = self._sweep_quality(signal, liq_map, regime)
            breakdown["sweep_quality"] = round(quality_score, 3)
        elif name == "ButterflyStrategy":
            quality_score = self._range_quality(regime, vol_state)
            breakdown["range_quality"] = round(quality_score, 3)
        else:
            quality_score = signal.conviction
            breakdown["signal_quality"] = round(quality_score, 3)

        # ── 3. VWAP alignment ─────────────────────────────────────────────────
        vwap_score = 0.5
        if vol_state.vwap > 0:
            if signal.direction == "long" and vol_state.price_vs_vwap == "ABOVE":
                vwap_score = 1.0
            elif signal.direction == "short" and vol_state.price_vs_vwap == "BELOW":
                vwap_score = 1.0
            elif signal.direction == "neutral":
                vwap_score = 0.7   # Butterfly — VWAP matters less
            else:
                vwap_score = 0.25
        breakdown["vwap_alignment"] = round(vwap_score, 3)

        # ── 4. Liquidity path clear ───────────────────────────────────────────
        # (ORB never reaches here — it is graded by _grade_orb and returns
        # above. This weighted liquidity dimension is for sweep/condor/default;
        # it reuses the same path test but as a graded drag, not an A/B pick.)
        liq_score = 1.0
        if not signal.is_butterfly:
            pools_blocking = self._pools_in_path(signal, liq_map)
            liq_score = max(1.0 - len(pools_blocking) * 0.25, 0.0)
        breakdown["liquidity_clear"] = round(liq_score, 3)

        # ── 5. Macro context ──────────────────────────────────────────────────
        macro_score = 0.5
        if macro:
            if macro.is_fed_day and name == "ORBStrategy":
                macro_score = 1.0   # Fed day boosts ORB
            elif macro.vix_regime == "LOW":
                macro_score = 0.8
            elif macro.vix_regime == "ELEVATED":
                macro_score = 0.3
            elif macro.vix_regime == "CRISIS":
                macro_score = 0.0
            elif macro.vix_regime == "NORMAL":
                macro_score = 0.6
        breakdown["macro_context"] = round(macro_score, 3)

        # ── Weighted total ────────────────────────────────────────────────────
        total = 0.0
        for dim, w in weights.items():
            val = breakdown.get(dim, 0.5)
            total += val * w

        # Session time modifier — penalize late-session entries
        session = current_session_label()
        if session == "late_session":
            total *= 0.85

        # ── Brief nudge (v1.2) — signed pre-market prior, post-sum tie-breaker ──
        # ORB: +  (catalyst supports a breakout)
        # Butterfly/Condor: -  (catalyst fights a pin/range)
        # SweepReversal: 0  (structure-driven; catalyst-agnostic)
        brief_sign = {"ORBStrategy": 1.0,
                      "ButterflyStrategy": -1.0,
                      "IronCondorStrategy": -1.0,
                      "SweepReversal": 0.0}.get(name, 0.0)
        if brief_sign != 0.0:
            nudge = brief_sign * self._brief_strength() * BRIEF_CONVICTION_WEIGHT
            if nudge != 0.0:
                total += nudge
                breakdown["brief_nudge"] = round(nudge, 4)

        # ── Grade — A or B only. No C grade exists. ─────────────────────────────
        if total >= grade_a:
            grade = "A"
        elif total >= grade_b:
            grade = "B"
        else:
            logger.info(
                f"Setup REJECTED — below B threshold: score={total:.2f} "
                f"(need >= {grade_b:.2f}) strategy={name} "
                f"breakdown={breakdown}"
            )
            self._journal_scored(signal, regime, vol_state, macro,
                                 total, "REJECT", breakdown,
                                 grade_a, grade_b, session)
            return None

        multiplier = GRADE_SIZE_MULTIPLIER[grade]

        result = SetupScore(
            grade=grade,
            score=round(total, 3),
            size_multiplier=multiplier,
            breakdown=breakdown
        )

        logger.info(
            f"Setup grade: {grade} score={total:.2f} "
            f"strategy={name} mult={multiplier}x "
            f"breakdown={breakdown}"
        )
        self._journal_scored(signal, regime, vol_state, macro,
                             total, grade, breakdown,
                             grade_a, grade_b, session)
        return result

    @staticmethod
    def _journal_scored(signal, regime, vol_state, macro,
                        total, grade, breakdown, grade_a, grade_b, session):
        """v1.3 — one `scored` event per scored signal, REJECTs included.
        Log-only; every failure is swallowed inside signal_journal."""
        if _journal is None:
            return
        try:
            _journal.journal(
                "scored",
                signal   = _journal.signal_ctx(signal),
                regime   = _journal.regime_ctx(regime),
                vol      = _journal.vol_ctx(vol_state),
                macro    = _journal.macro_ctx(macro),
                score    = {"total": round(float(total), 4),
                            "grade": grade,
                            "grade_a_bar": grade_a,
                            "grade_b_bar": grade_b,
                            "breakdown": breakdown,
                            "session": session},
            )
        except Exception:
            pass

    def _grade_orb(self, signal: OptionsSignal,
                   liq_map:   LiquidityMap,
                   regime:    RegimeState,
                   vol_state: VolatilityState,
                   macro) -> Optional["SetupScore"]:
        """The WHOLE ORB grade (v1.4). A confirmed ORB always trades; the only
        question is size.

        A  — no unswept liquidity pool between the breakout and the 100%% TP.
        B  — a pool sits in that path (the target may not be cleanly
             reachable), so the same setup trades at base size.

        There is no REJECT branch here: a confirmed ORB is never a no-trade on
        quality grounds. (Session/RTH/cutoff gating lives in session_guard, not
        here.) Regime, VWAP, macro, confluence count and the brief nudge are
        deliberately absent — this trade is geometry, validated upstream by the
        ORB state machine, plus one liquidity modifier.
        """
        pools_blocking = self._pools_in_path(signal, liq_map)
        grade = "A" if not pools_blocking else "B"
        multiplier = GRADE_SIZE_MULTIPLIER[grade]

        breakdown = {
            "orb_geometry": "confirmed",          # the gate the state machine passed
            "pools_in_path": len(pools_blocking),
            "liquidity_path": "clear" if grade == "A" else "pool_in_path",
        }

        logger.info(
            f"ORB grade: {grade} ({'clear path' if grade=='A' else ''}"
            f"{len(pools_blocking)} pool(s) in path) mult={multiplier}x"
        )
        # Journal it like any other scored signal (REJECT path is unreachable
        # for the ORB, so grade is always A or B here). total is reported as
        # the multiplier for a stable numeric field; there is no weighted sum.
        self._journal_scored(signal, regime, vol_state, macro,
                             float(multiplier), grade, breakdown,
                             grade_a=None, grade_b=None,
                             session=current_session_label())
        return SetupScore(
            grade=grade,
            score=round(float(multiplier), 3),
            size_multiplier=multiplier,
            breakdown=breakdown,
        )

    @staticmethod
    def _pools_in_path(signal, liq_map) -> list:
        """Unswept pools between entry and the 100%% TP, in the trade direction.
        A long is blocked by an unswept HIGH between entry and target; a short
        by an unswept LOW. This is the same path test the old dimension-4
        used — now it selects A vs B instead of subtracting a weighted drag."""
        return [
            p for p in liq_map.pools
            if not p.swept and (
                (signal.direction == "long"  and p.kind == "high" and
                 signal.underlying_entry < p.price < signal.underlying_target) or
                (signal.direction == "short" and p.kind == "low" and
                 signal.underlying_target < p.price < signal.underlying_entry)
            )
        ]

    def _sweep_quality(self, signal: OptionsSignal,
                        liq_map: LiquidityMap,
                        regime: RegimeState) -> float:
        """Sweep quality: rejection %, freshness, named level."""
        if not liq_map.recent_sweep:
            return 0.3
        sweep = liq_map.recent_sweep
        rejection_score = min(sweep.rejection_pct / 0.01, 1.0)
        age_score       = max(0, 1 - (liq_map.sweep_age_bars / 8))
        named_bonus     = 0.15 if sweep.swept_named_level else 0.0
        return min(rejection_score * 0.45 + age_score * 0.4 + named_bonus, 1.0)

    def _range_quality(self, regime: RegimeState,
                        vol_state: VolatilityState) -> float:
        """Ranging quality: low ADX, BB squeeze, stable ATR."""
        adx_score = max(0, 1 - regime.adx / 25)
        bb_score  = max(0, 1 - vol_state.bb_width_pct * 3)
        vol_score = 1.0 if vol_state.atr_state in ("STABLE", "CONTRACTING") else 0.5
        return adx_score * 0.4 + bb_score * 0.4 + vol_score * 0.2


# Singleton
_scorer: Optional[SetupScorer] = None


def get_setup_scorer() -> SetupScorer:
    global _scorer
    if _scorer is None:
        _scorer = SetupScorer()
    return _scorer
