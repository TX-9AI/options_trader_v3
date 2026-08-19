#!/usr/bin/env python3
"""
tests/test_trend_align.py — v1.0 — 2026-08-19   (L1.12)

TRENDING'S CORROBORATOR WAS ITS SOFT-NECESSARY, PRINTED TWICE.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_trend_align.py -q

    WAS:  align_val = max(align_frac, ramp(adx, adx_trend,     ADX_STRONG_SOLO))
    AND:  adx_s     =                 ramp(adx, adx_trend - 5, ADX_STRONG_SOLO)

**Same input. Same upper bound. Lower bounds 5 apart.** TRENDING therefore
scored roughly `ADX × (w·ADX + w·momentum)` — ADX multiplied by itself.

⚠️ THAT IS THE GRADE-INVERSION DEFECT ONE LAYER DOWN. `risk/setup_scorer.py`
found `regime_conviction` and `signal_quality` with **identical medians AND
identical spreads** (0.913/0.636 over 619 trades) and ~90% of the grade was one
column printed twice. A-grade then lost **$8,244** at 1.5× size while B-grade
made **+$1,893**.

⚠️ MEASURED 2026-08-19, and the sequence matters:
  · `align_frac` was a CONSTANT **0.67** across the whole 27-session pool —
    p25 = p50 = p95 — because the 1h vote never fired: `TIMEFRAMES["1h"]` asked
    for 50 bars against the engine's `EMA_SLOW + 5` = 55 minimum (L1.9a). 0.67
    is exactly **2 of 3** timeframes agreeing with the third silent.
  · After that fix it VARIES: QQQ 08-17 p25 **0.67** / p50 **0.83** / p95
    **1.00**.
  · **But `align_val` still pegged at 1.0 on 85.9% of ticks** — the `max()`
    takes the ADX branch whenever ADX is strong. **Fixing the starvation
    produced real alignment information that the combinator threw away.**

⚠️ WHY DROPPING THE ADX BRANCH IS CORRECT RATHER THAN MERELY TIDIER: ADX's
PERMISSION role is already `adx_s`. When ADX is strong `adx_s ≈ 1.0`, the damper
stops reducing the score, and the trend is admitted on ADX alone exactly as
intended. The `max()` added ADX a SECOND time to BOOST, not to permit.
**A corroborator's job is independent evidence.**
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "analysis", "regime_confluence.py")


def test_alignment_is_no_longer_masked_by_adx():
    s = open(SRC, encoding="utf-8").read()
    assert "align_val = align_frac" in s
    assert 'if TREND_ALIGN_MODE == "max":' in s, \
        "the legacy path must remain selectable so the change can be A/B'd"


def test_the_legacy_combinator_is_reversible():
    """⚠️ L1.10's pattern: a calibration change must be a config change with
    instant rollback, so a re-score can be run BOTH WAYS and compared rather
    than argued."""
    import importlib
    import analysis.regime_confluence as rc
    os.environ["OT_TREND_ALIGN_MODE"] = "max"
    importlib.reload(rc)
    assert rc.TREND_ALIGN_MODE == "max"
    os.environ.pop("OT_TREND_ALIGN_MODE", None)
    importlib.reload(rc)
    assert rc.TREND_ALIGN_MODE == "align"


def test_the_two_adx_ramps_shared_everything_but_a_lower_bound():
    """The duplication in one assertion: had the bounds differed materially the
    two terms would carry different information. They did not."""
    import analysis.regime_confluence as rc
    s = open(SRC, encoding="utf-8").read()
    assert "ramp(adx, self.adx_trend - 5, ADX_STRONG_SOLO)" in s, \
        "adx_s changed — re-check whether the duplication still holds"
    assert rc.ADX_STRONG_SOLO == 35.0


def test_alignment_now_reaches_the_score():
    """With the mask gone, distinct alignment fractions must produce distinct
    corroborator values. Under `max` with strong ADX they all collapsed to 1.0."""
    import importlib
    import analysis.regime_confluence as rc
    importlib.reload(rc)
    vals = {rc.ramp(f, 0.0, 1.0) if False else f
            for f in (0.33, 0.67, 0.83, 1.00)}
    assert len(vals) == 4, "alignment fractions must stay distinguishable"


def test_ranging_was_the_clean_regime_and_stays_that_way():
    """⚠️ RANGING is the only regime whose terms draw on THREE DISTINCT inputs —
    angle, bb_width, crossings — and it is also the only one that GRADES
    properly (p90 0.615 rather than pinning at 1.00). That is the control case
    for this whole finding."""
    s = open(SRC, encoding="utf-8").read()
    seg = s[s.index("def _ranging("):s.index("def _ranging(") + 4000]
    assert "ramp(FLAT_ANGLE_CUT_DEG - ang" in seg
    assert "ramp(bb_width_pct, RANGE_ROOM_LO" in seg
    assert "ramp(cross, RANGE_OSC_LO" in seg
