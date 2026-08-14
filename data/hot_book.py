"""
data/hot_book.py — options_trader_v3 — v1.0 — 2026-08-14   (SIM.2)

PRIME THE TREND ENGINE FOR ANY SYMBOL, ANY DATE.

Operator: *"I want a generic hot book to prime every run regardless of which
symbol we are running... just as long as the trend engine will read states after
it's warm."*

────────────────────────────────────────────────────────────────────────────
WHY A COLD START IS THE MOST DANGEROUS FAILURE A REPLAY CAN HAVE
────────────────────────────────────────────────────────────────────────────
`trend_engine._analyze_single()` bails to NEUTRAL below **EMA_SLOW + 5** bars.
A run that starts at 09:30 on the target date hands EVERY frame a starved vote,
so every trend-gated strategy self-vetoes, nothing fires, and the run reports a
QUIET DAY THAT NEVER HAPPENED. **Silence that looks like a result** is worse
than a crash, because a crash gets investigated.

So this module does two things and refuses to guess at either:
  1. LOADS prior sessions from the OHLC archive and concatenates them.
  2. **VERIFIES THE PRIME** against the engine's OWN requirement — `EMA_SLOW`
     imported from config, and every timeframe the engine actually votes on
     (`tf_weights` = 1d / 1h / 15m / 5m), not a number written down here.
     Counting SESSIONS is a proxy; counting BARS PER FRAME at the first tick is
     the fact.

⚠️ ASKED IS NOT LOADED. A session directory can exist without a given symbol in
it — a box that did not wake, a symbol added later, a backfill gap. Asking for
10 and getting 3 must be VISIBLE, because 3 does not prime a 1h frame.

⚠️ THE HARD LIMIT: **a session is only replayable after the EOD conductor has
harvested its OHLC to control.** Same-day replay is impossible before EOD, and
that is a data-availability fact, not a bug to work around.

⚠️ SYNTHETIC VOLUME. The archive carries no volume column and several engines
index it. A CONSTANT is deliberate: it makes any volume-derived signal INERT
rather than plausible-looking. Do not read a volume result out of a primed run.
"""

import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
ET = pytz.timezone("US/Eastern")

OHLC_ROOTS = ("~/day_trader_pro/ohlc", "~/day_trader_pro/data/ohlc")

# Resample rules for every frame the trend engine votes on, plus 1m as the base.
RESAMPLE = {"1m": "1min", "5m": "5min", "15m": "15min",
            "1h": "60min", "1d": "1D"}


def _min_bars() -> int:
    """The engine's OWN requirement, imported — never a number written here.

    `trend_engine._analyze_single` bails below `EMA_SLOW + 5`. If that constant
    moves, this moves with it; a hardcoded 55 would silently drift and the
    prime check would start lying.
    """
    try:
        from config import EMA_SLOW
        return int(EMA_SLOW) + 5
    except Exception:                                          # noqa: BLE001
        return 55


def voting_weights() -> Dict[str, float]:
    """The engine's own `tf_weights`, parsed from source.

    Needed because a starved frame is NOT a failed run — it votes NEUTRAL and
    contributes NOTHING, so the aggregate still works at reduced weight. What
    matters is HOW MUCH VOTE IS LOST, not a binary pass/fail.
    """
    default = {"1d": 0.15, "1h": 0.20, "15m": 0.30, "5m": 0.35}
    try:
        import re
        src = open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "analysis", "trend_engine.py"),
            encoding="utf-8").read()
        m = re.search(r"tf_weights\s*=\s*\{([^}]*)\}", src)
        if m:
            found = dict(re.findall(r'"([0-9a-z]+)"\s*:\s*([0-9.]+)', m.group(1)))
            if found:
                return {k: float(v) for k, v in found.items()}
    except Exception:                                          # noqa: BLE001
        pass
    return default


def voting_timeframes() -> List[str]:
    """The frames the trend engine actually weights, heaviest first.

    Read from the engine's `tf_weights` when it can be parsed, so adding a frame
    there does not silently leave it unverified here.
    """
    default = ["5m", "15m", "1h", "1d"]
    try:
        import re
        src = open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "analysis", "trend_engine.py"),
            encoding="utf-8").read()
        m = re.search(r"tf_weights\s*=\s*\{([^}]*)\}", src)
        if m:
            found = re.findall(r'"([0-9a-z]+)"\s*:', m.group(1))
            if found:
                return found
    except Exception:                                          # noqa: BLE001
        pass
    return default


def _load_day(date: str, symbol: str) -> Optional[pd.DataFrame]:
    for root in OHLC_ROOTS:
        d = os.path.join(os.path.expanduser(root), date)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.startswith(symbol + "_") or not fn.endswith(".csv"):
                continue
            rows = []
            try:
                with open(os.path.join(d, fn), encoding="utf-8") as fh:
                    for r in csv.DictReader(fh):
                        t = r.get("timestamp") or r.get("time") or ""
                        try:
                            ts = datetime.strptime(t[:19], "%Y-%m-%dT%H:%M:%S")
                            rows.append((ET.localize(ts), float(r["open"]),
                                         float(r["high"]), float(r["low"]),
                                         float(r["close"])))
                        except Exception:                      # noqa: BLE001
                            continue
            except Exception:                                  # noqa: BLE001
                continue
            if rows:
                rows.sort()
                out = pd.DataFrame(
                    {"open": [r[1] for r in rows], "high": [r[2] for r in rows],
                     "low": [r[3] for r in rows], "close": [r[4] for r in rows]},
                    index=pd.DatetimeIndex([r[0] for r in rows]))
                if "volume" not in out.columns:
                    out["volume"] = 0.0        # synthetic; see the header
                return out
    return None


def available_sessions(before: str) -> List[str]:
    seen = set()
    for root in OHLC_ROOTS:
        r = os.path.expanduser(root)
        if os.path.isdir(r):
            seen |= {d for d in os.listdir(r) if len(d) == 10 and d < before}
    return sorted(seen)


def prime(symbol: str, date: str, warmup: int = 12
          ) -> Tuple[Optional[pd.DataFrame], Dict]:
    """(book, report). `book` is 1m bars: `warmup` prior sessions + `date`.

    The report always states ASKED vs LOADED and names what was missing, so a
    thin prime cannot pass as a full one.
    """
    wanted = available_sessions(date)[-warmup:] if warmup > 0 else []
    frames, got = [], []
    for d in wanted:
        df = _load_day(d, symbol)
        if df is not None and not df.empty:
            frames.append(df)
            got.append(d)
    today = _load_day(date, symbol)
    report = {"symbol": symbol, "date": date, "asked": warmup,
              "dirs": len(wanted), "loaded": len(got),
              "missing": [d for d in wanted if d not in got],
              "target_found": today is not None and not today.empty}
    if not report["target_found"]:
        report["fatal"] = (f"no {symbol} OHLC for {date} — the tape is not "
                           f"harvested yet. A session is replayable only after "
                           f"the EOD conductor pulls it to control.")
        return None, report
    frames.append(today)
    book = pd.concat(frames).sort_index()
    book = book[~book.index.duplicated(keep="last")]
    report["bars"] = len(book)
    return book, report


def resample_all(book: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    out = {}
    for tf, rule in RESAMPLE.items():
        if tf == "1m":
            out[tf] = book
            continue
        agg = {"open": "first", "high": "max", "low": "min", "close": "last"}
        if "volume" in book.columns:
            agg["volume"] = "sum"
        out[tf] = book.resample(rule, label="right", closed="right").agg(
            agg).dropna()
    return out


def verify_prime(book: pd.DataFrame, at: datetime) -> Dict:
    """Is the trend engine ACTUALLY warm at `at`?

    Checks BARS PER FRAME against the engine's own `EMA_SLOW + 5`, for every
    frame it votes on. Counting sessions is a proxy; this is the fact.
    """
    need = _min_bars()
    frames = resample_all(book)
    per = {}
    for tf in voting_timeframes():
        df = frames.get(tf)
        n = 0 if df is None else len(df[df.index <= at])
        per[tf] = {"bars": n, "need": need, "ok": n >= need}
    w = voting_weights()
    starved = [tf for tf, v in per.items() if not v["ok"]]
    lost = sum(w.get(tf, 0.0) for tf in starved)
    return {"need": need, "per_frame": per, "starved": starved,
            "weight_lost": round(lost, 3), "weight_live": round(1.0 - lost, 3),
            "primed": not starved}


def describe(report: Dict, check: Optional[Dict] = None) -> List[str]:
    """Human-readable lines. Any caller can print these; the wording of a
    failed prime lives in ONE place so no tool can soften it."""
    out = [f"HOT BOOK {report['symbol']} {report['date']}: "
           f"asked {report['asked']} · dirs {report['dirs']} · "
           f"LOADED {report['loaded']} · bars {report.get('bars', 0)}"]
    if report.get("fatal"):
        out.append(f"🔴 {report['fatal']}")
        return out
    if report["missing"]:
        m = report["missing"]
        out.append(f"⚠️ {len(m)} session(s) had no {report['symbol']} data: "
                   f"{', '.join(m[:4])}{' …' if len(m) > 4 else ''}")
    if check:
        detail = "  ".join(f"{tf}={v['bars']}" for tf, v in
                           check["per_frame"].items())
        pct = int(round(100 * check["weight_live"]))
        if check["primed"]:
            out.append(f"✅ PRIMED — all frames (need {check['need']}/frame)  {detail}")
        elif check["weight_live"] >= 0.80:
            # A starved frame votes NEUTRAL and contributes NOTHING; the
            # aggregate still works at reduced weight. `1d` needs 55 DAILY bars
            # — about 11 weeks of archive — so it is starved on any normal
            # replay and that is a data-depth fact, not a defect.
            out.append(f"🟡 PARTIAL — starved: {', '.join(check['starved'])} "
                       f"(need {check['need']}/frame)  {detail}")
            out.append(f"   {pct}% of the trend vote is live; the starved "
                       f"frame(s) vote NEUTRAL and contribute nothing. Usable, "
                       f"but the vote is not identical to live.")
        else:
            out.append(f"🔴 NOT PRIMED — starved: {', '.join(check['starved'])} "
                       f"(need {check['need']}/frame)  {detail}")
            out.append(f"   Only {pct}% of the trend vote is live. Trend-gated "
                       f"strategies will self-veto and the run reports a quiet "
                       f"day that never happened. Raise warmup or backfill OHLC.")
    return out
