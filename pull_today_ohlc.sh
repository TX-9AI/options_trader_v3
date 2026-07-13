#!/usr/bin/env bash
# options_trader_v3/pull_today_ohlc.sh — one-shot EOD retrieval of TODAY's FULL 1-min session on THIS box.
# v1.2 — 2026-07-10 — Hoist TT_* cred fetch to the top of __work so BOTH the v3 --once refill and a
#        v2 self-subscribing logger run with creds in-process (v3 logger ignores them). This lets the
#        EOD timer's oneshot service call `__work` directly and keep NO secrets in the unit file.
# v1.1 — 2026-07-10 — Full-session correctness fix. The v3 candle-feed store is pruned to
#        max(need,60)*PRUNE_FACTOR = 240 one-minute bars, but an RTH session is ~390 (09:30-16:00),
#        so a plain store read after ~noon silently drops the morning (opening range / ORB window).
#        On v3 this now ALWAYS rebuilds the full session first via ONE synchronous producer pass
#        (data.candle_feed --once backfills 1m from 09:30 and flushes), stopping candle-feed first
#        so there is never a second live producer (Mandate 2), then reads+exports, then restores the
#        feed. Guard: if it is still RTH (before 16:00 ET) AND the feed is live, it will NOT stop the
#        feed (would starve the trading bot) — it reads the store and flags the result as partial.
#        Symbol is passed explicitly (--symbols) so it never depends on OT_INSTRUMENT being in env.
# v1.0 — 2026-07-10 — initial: background-detached retrieval (fleet.py run has a ~22s SSH ceiling;
#        a v2 drain / --once warm can exceed it), --check readout, v2/v3 aware.
#
# Usage (from the control server):
#   1) python fleet.py run 'bash ~/options-trader/pull_today_ohlc.sh'            # launch on all
#   2) (wait ~60s) python fleet.py run 'bash ~/options-trader/pull_today_ohlc.sh --check'
#   3) python fleet.py pull ohlc --day <today-ET>                                # SCP to control
set -uo pipefail

DIR=/home/ubuntu/options-trader
VENV="$DIR/venv"
PY="$VENV/bin/python"; [ -x "$PY" ] || PY=/usr/bin/python3
LOG="$DIR/pull_today_ohlc.log"
FULL_SESSION_BARS=380          # soft completeness threshold for the "short session" flag
cd "$DIR" 2>/dev/null || { echo "🚨 $DIR not found"; exit 9; }

TODAY=$(TZ=America/New_York date +%F)
SYM=$(systemctl show optionsbot -p Environment --value 2>/dev/null | tr ' ' '\n' | grep '^OT_INSTRUMENT=' | head -1 | cut -d= -f2-)
[ -n "$SYM" ] || SYM=$("$PY" -c 'from config import INSTRUMENT; print(INSTRUMENT)' 2>/dev/null)
CSV="$DIR/data/OHLC/$TODAY/${SYM}.csv"

csv_rows() { if [ -f "$CSV" ]; then echo $(( $(wc -l < "$CSV") - 1 )); else echo -1; fi; }
run_logger() { timeout 180 "$PY" -m data.candle_logger --date "$TODAY" --symbols "$SYM" 2>&1; }

# ── --check: fast status readout (well under the SSH ceiling) ─────────────────
if [ "${1:-}" = "--check" ]; then
    R=$(csv_rows)
    if   [ "$R" -ge "$FULL_SESSION_BARS" ]; then echo "✅ $SYM $TODAY: $R bars (full session)"
    elif [ "$R" -gt 0 ]; then echo "✅ $SYM $TODAY: $R bars (⚠ short of a full ~390-bar session)"
    elif [ "$R" -eq 0 ]; then echo "🚨 $SYM $TODAY: 0 bars (store empty / entitlement — see log)"
    else echo "… $SYM $TODAY: not written yet (still running?)"; tail -n 2 "$LOG" 2>/dev/null; fi
    exit 0
fi

# ── __work: the (possibly long) full-session retrieval; runs detached, logs to $LOG ──
if [ "${1:-}" = "__work" ]; then
    IS_V3=0; [ -f data/candle_feed.py ] && IS_V3=1
    NOWHM=$(( 10#$(TZ=America/New_York date +%H%M) ))
    POSTCLOSE=0; [ "$NOWHM" -ge 1600 ] && POSTCLOSE=1
    echo "=== $(date '+%F %T %Z') pull start $SYM $TODAY (v$([ "$IS_V3" = 1 ] && echo 3 || echo 2), postclose=$POSTCLOSE) ==="

    # Creds up front: the v3 --once refill needs them, and a v2 self-subscribing logger needs them
    # in-process. The v3 logger ignores them (it reads the store). Sourced from the running bot unit.
    EL=$(systemctl show optionsbot -p Environment --value 2>/dev/null)
    gv() { echo "$EL" | tr ' ' '\n' | grep "^$1=" | head -1 | cut -d= -f2-; }
    OT_INSTRUMENT=$(gv OT_INSTRUMENT)
    TT_CLIENT_SECRET=$(gv TT_CLIENT_SECRET)
    TT_REFRESH_TOKEN=$(gv TT_REFRESH_TOKEN)
    TT_ACCOUNT_NUMBER=$(gv TT_ACCOUNT_NUMBER)
    export OT_INSTRUMENT TT_CLIENT_SECRET TT_REFRESH_TOKEN TT_ACCOUNT_NUMBER
    HAVE_CREDS=0
    [ -n "$TT_CLIENT_SECRET" ] && [ -n "$TT_REFRESH_TOKEN" ] && [ -n "$TT_ACCOUNT_NUMBER" ] && HAVE_CREDS=1

    if [ "$IS_V3" = "1" ]; then
        FEED=$(systemctl is-active candle-feed 2>/dev/null || echo unknown)
        if [ "$FEED" = "active" ] && [ "$POSTCLOSE" = "0" ]; then
            echo "RTH + feed live: NOT stopping the feed (would starve the bot). Reading store as-is;"
            echo "result may be PARTIAL (1m store holds ~240 bars). Re-run after 16:00 ET for a full session."
            run_logger
        else
            # Safe to rebuild the full session with a single producer pass.
            [ "$FEED" = "active" ] && { echo "stopping candle-feed for a single-producer refill"; sudo systemctl stop candle-feed; }
            if [ "$HAVE_CREDS" = "1" ]; then
                echo "refilling full session via one synchronous producer pass (candle_feed --once)"
                timeout 200 "$PY" -m data.candle_feed --once 2>&1
            else
                echo "cannot refill: TT_* creds not present in the optionsbot unit — reading store (may be partial)"
            fi
            [ "$FEED" = "active" ] && { echo "restarting candle-feed"; sudo systemctl start candle-feed; }
            run_logger
        fi
    else
        # v2: the logger self-subscribes to DXFeed from 09:30 → full session directly (needs creds).
        [ "$HAVE_CREDS" = "1" ] || echo "warning: v2 logger needs TT_* creds and none were found in the optionsbot unit"
        run_logger
    fi

    echo "=== $(date '+%F %T %Z') pull done: $(csv_rows) bars → $CSV ==="
    exit 0
fi

# ── default: detach the work so the SSH call returns immediately ──────────────
: > "$LOG" 2>/dev/null || true
setsid bash "$DIR/pull_today_ohlc.sh" __work >>"$LOG" 2>&1 </dev/null &
disown 2>/dev/null || true
echo "launched $SYM full-session pull for $TODAY (bg) → check: bash ~/options-trader/pull_today_ohlc.sh --check"
exit 0
