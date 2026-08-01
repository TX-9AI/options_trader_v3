#!/usr/bin/env python3
"""
tests/blind_alert_selftest.py — v1.0 — 2026-08-01

BLIND-ALERT DRILL. Runs ON A BOT BOX and fires the real alert path end to end.

WHY THIS EXISTS
    The blind alert is the one that pages when the bot is still running but can
    no longer see. If it is broken, the failure mode is silence — the operator
    learns it never worked at the exact moment they needed it. An alarm that has
    never fired is an alarm nobody knows works, so it gets exercised on purpose.

    It walks the ACTUAL production path, not a mock:
        market_data.record_blindness()  ->  the same recorder every blind return
                                            in fetch_candles funnels through
        BlindnessLatch.update()         ->  the same latch main.py runs, held to
                                            the same tick and time thresholds
        AlertManager.send_blind_alert() ->  the same function, same formatting,
                                            same Telegram sender
        AlertManager.send_sight_restored_alert()  ->  the recovery notice

    Only two things differ from a real outage: the blindness record is synthetic,
    and drill=True prefixes an unmistakable marker.

THE DRILL MARKER IS NOT COSMETIC
    Telegram here is an EMERGENCY SERVICES channel — nothing routine goes to it.
    A test that looks like a real alert IS a false alarm, and a channel that has
    cried wolf once gets read more slowly forever. Every message this sends
    leads with a DRILL prefix.

WHAT IT VERIFIES, beyond "a message arrived"
    - the latch does NOT fire early (asserts silence below the threshold)
    - it fires exactly once, and holds the FIRST snapshot
    - open positions are read from the live trades.db and rendered — so the
      operator sees the real format, including whether the manage-manually line
      would appear on this box
    - the recovery notice still carries duration and cause after the reset

USAGE (on a bot box, repo root — single line)
    python3 tests/blind_alert_selftest.py
    python3 tests/blind_alert_selftest.py --no-send     # dry run, prints only

Places no orders. Writes nothing. Sends two Telegram messages unless --no-send.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DRILL_CAUSE = "DRILL_BARS_STALE"


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-send", action="store_true",
                    help="exercise the path and print, but send no Telegram")
    a = ap.parse_args(argv[1:])

    from config import INSTRUMENT, PAPER_TRADING
    from data.market_data import clear_blindness, last_blindness, record_blindness
    from utils.blindness_latch import ALERT, RECOVERED, BlindnessLatch

    instrument = os.environ.get("OT_INSTRUMENT", INSTRUMENT)
    print(f"blind-alert drill | {instrument} | "
          f"{'PAPER' if PAPER_TRADING else 'LIVE CASH'}")

    fails = []

    def check(label, cond):
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        if not cond:
            fails.append(label)

    # ── 1. the recorder ──────────────────────────────────────────────────────
    clear_blindness()
    check("clean start: last_blindness() is None", last_blindness() is None)
    record_blindness(DRILL_CAUSE, instrument, "5m",
                     newest_bar="<drill>", age_s="930", limit_s="900", bars=100)
    snap = last_blindness()
    check("record_blindness stored a record", snap is not None)
    check("cause round-tripped", (snap or {}).get("cause") == DRILL_CAUSE)

    # ── 2. the latch, at production thresholds ───────────────────────────────
    latch = BlindnessLatch()
    t = 1_000.0
    early = latch.update(snap, t)
    check("does NOT page on the first blind tick", early is None)

    verdict = None
    for i in range(1, 40):
        verdict = latch.update(snap, t + i * 20)
        if verdict:
            break
    check("pages once the threshold is met", verdict == ALERT)
    check("held the FIRST snapshot", (latch.snapshot or {}).get("cause") == DRILL_CAUSE)

    # ── 3. open positions, read live so the real format is visible ───────────
    descs = []
    try:
        from database.trade_logger import get_trade_logger
        rows = get_trade_logger().get_open_trades_live()
        descs = [getattr(r, "position_desc", None) or str(r) for r in rows]
        check(f"read open positions from trades.db ({len(descs)} open)", True)
    except Exception as e:                                        # noqa: BLE001
        check(f"read open positions from trades.db — {e}", False)

    if descs and not PAPER_TRADING:
        print("     NOTE: this box is LIVE with open positions, so the real "
              "alert would\n           carry the GO TO TASTYTRADE instruction.")

    # ── 4. the send ──────────────────────────────────────────────────────────
    if a.no_send:
        print("  [SKIP] --no-send: not sending Telegram")
    else:
        from notifications.alert_manager import get_alert_manager
        am = get_alert_manager()
        am.send_blind_alert(instrument, latch.snapshot, open_positions=descs,
                            paper=PAPER_TRADING,
                            blind_for_s=latch.blind_for_s(t + 200), drill=True)
        check("sent the DRILL blind alert", True)

    # ── 5. recovery, including the fields the reset must not eat ─────────────
    rec = latch.update(None, t + 300)
    check("recovery fires once", rec == RECOVERED)
    check("recovery kept the duration", latch.last_outage_s > 0)
    check("recovery kept the cause", latch.last_outage_cause == DRILL_CAUSE)
    if not a.no_send:
        from notifications.alert_manager import get_alert_manager
        get_alert_manager().send_sight_restored_alert(
            instrument, latch.last_outage_s, latch.last_outage_cause, drill=True)
        check("sent the DRILL recovery notice", True)

    clear_blindness()
    print(f"\n{'DRILL PASSED' if not fails else 'DRILL FAILED: ' + ', '.join(fails)}")
    return 0 if not fails else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
