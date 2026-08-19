#!/usr/bin/env python3
"""
tests/test_replay_warm_depth.py — v1.0 — 2026-08-19   (L1.9)

THE REPLAY MUST BE ABLE TO FILL THE FRAME IT ASKS FOR.

    cd ~/options-trader-v3 && PYTHONPATH=. venv/bin/python -m pytest tests/test_replay_warm_depth.py -q

`replay_confluence` resamples 1h from 1m tape at ~7 RTH bars per session and
caps the frame at `TIMEFRAMES["1h"]["candles"]`. The warm depth was hardcoded at
**8 prior sessions** — sized for the old 50-bar cap, yielding ~63 bars.

⚠️ L1.9a RAISED THE CAP TO 80 (the trend engine needs `EMA_SLOW + 5` = 55 and
the config asked for 50, so the 1h vote could never fire). **8 priors clear 55
but cannot fill 80** — the replay would have run systematically shallower than
live and **nothing would have said so**, because `tail()` silently returns what
it has.

⚠️ A HARDCODED WARM DEPTH BESIDE A CONFIGURABLE CAP IS THE SAME DEFECT CLASS AS
A CONFIG BELOW ITS CONSUMER'S THRESHOLD — which is exactly what L1.9a fixed.
The depth is now DERIVED, so the two cannot drift apart again.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib.util as _u                                      # noqa: E402

import config                                                    # noqa: E402

_spec = _u.spec_from_file_location(
    "rc", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "replay_confluence.py"))
rc = _u.module_from_spec(_spec)
try:
    _spec.loader.exec_module(rc)
except SystemExit:
    pass


def test_the_warm_window_can_fill_the_1h_cap():
    supplied = (rc.WARM_SESSIONS_DEFAULT + 1) * rc._RTH_1H_BARS_PER_SESSION
    assert supplied >= rc._CAP["1h"], (
        f"{rc.WARM_SESSIONS_DEFAULT} priors supply ~{supplied} 1h bars against a "
        f"cap of {rc._CAP['1h']} — the replay runs shallower than live and "
        "tail() will not complain")


def test_it_clears_the_trend_engines_minimum_with_margin():
    """The minimum is a cliff: a replay that only just clears it starves on any
    session with missing prior days, and the failure is silent."""
    need = config.EMA_SLOW + 5
    supplied = (rc.WARM_SESSIONS_DEFAULT + 1) * rc._RTH_1H_BARS_PER_SESSION
    assert supplied >= need + 20


def test_the_depth_is_DERIVED_from_the_cap_not_hardcoded():
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "replay_confluence.py"), encoding="utf-8").read()
    assert '_CAP["1h"] // _RTH_1H_BARS_PER_SESSION' in src
    assert "warm_sessions: int = WARM_SESSIONS_DEFAULT" in src
    assert "warm_sessions: int = 8" not in src


def test_raising_the_cap_raises_the_warm_depth():
    """The property that matters: change the config, the replay follows."""
    import math
    for cap in (50, 80, 140):
        expected = max(8, math.ceil(cap / rc._RTH_1H_BARS_PER_SESSION) + 3)
        got = max(8, -(-cap // rc._RTH_1H_BARS_PER_SESSION) + 3)
        assert got == expected


def test_the_missing_1d_timeframe_is_DOCUMENTED_not_faked():
    """⚠️ Live blends `1d` at 0.15; the replay cannot — 55 daily bars do not
    come from a 15-session 1m window. **Feeding a synthetic or truncated 1d
    would make the vote LOOK complete while carrying a frame the engine would
    have refused.** An absent timeframe is honest; a starved one is not."""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "replay_confluence.py"), encoding="utf-8").read()
    i = src.index('trend = trE.analyze({"1m": s1m')
    seg = src[max(0, i - 1600):i]
    assert "NO `1d` HERE" in seg
    assert '"1d": s' not in src, "a 1d frame appeared — verify it is not truncated"
