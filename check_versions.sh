#!/bin/bash
# v3.0 — 2026-07-10 — repo-wide v3.0 bump: Yahoo-Finance purge & data stream
#         mapping optimization (single shared TastyTrade candle feed). No
#         logic change in this file.
# =============================================================================
# check_versions.sh — Recursively verify version headers and key fixes
# across the entire options_trader project.
#
# Excludes: venv, __pycache__, .git, *.pem, trades.db*, bot.log, snapshots
#
# Run from ~/options-trader
# =============================================================================

cd "$(dirname "$0")" || exit 1

echo ""
echo "============================================================"
echo "  RECURSIVE VERSION HEADER CHECK — $(date)"
echo "  Directory: $(pwd)"
echo "============================================================"
echo ""

# Find every .py and .sh file in the project, excluding noise
FILES=$(find . \
    -type d \( -name venv -o -name __pycache__ -o -name .git -o -name snapshots \) -prune \
    -o -type f \( -name "*.py" -o -name "*.sh" \) -print \
    | sed 's|^\./||' \
    | sort)

TOTAL=0
for f in $FILES; do
    TOTAL=$((TOTAL+1))
    echo "------------------------------------------------------------"
    echo "FILE: $f"
    echo "  Last modified: $(stat -c '%y' "$f" 2>/dev/null || stat -f '%Sm' "$f" 2>/dev/null)"
    echo "  Size: $(wc -l < "$f") lines"
    echo "  Header:"
    head -12 "$f" | sed 's/^/    /'
    echo ""
done

echo "============================================================"
echo "  TOTAL FILES SCANNED: $TOTAL"
echo "============================================================"
echo ""
echo "============================================================"
echo "  CRITICAL FIX CHECKS — today's session"
echo "============================================================"
echo ""

check() {
    local file="$1"
    local pattern="$2"
    local label="$3"
    if [ -f "$file" ] && grep -q "$pattern" "$file" 2>/dev/null; then
        echo "  \u2713 PRESENT: $label  (in $file)"
    else
        echo "  \u2717 MISSING: $label  (expected in $file)"
    fi
}

check "main.py"                          "ORBState.OPEN_LONG"           "ORB state fix (OPEN_LONG not CONFIRMED_LONG)"
check "main.py"                          "STRATEGY: NO TRADE"           "NO TRADE log line"
check "main.py"                          "send_shutdown_alert"          "Shutdown alert hook"
check "main.py"                          "signal.SIGTERM"               "SIGTERM handler"
check "main.py"                          "score is None"                "Handles scorer returning None (no Grade C)"
check "analysis/orb_engine.py"           "OPEN_LONG"                    "ORB engine state rename"
check "analysis/orb_engine.py"           "_rearm"                       "ORB re-arm logic"
check "analysis/get_orb_range.py"        "in_opening_window"            "Today-gated 9:30 candle resolve (range moved out of orb_engine)"
check "analysis/orb_engine.py"           "_load_range_from_file"        "ORB range consumed via file handoff (orb_range.json)"
check "analysis/trend_engine.py"         'tf == "5m"'                   "ADX from 5m timeframe"

# ── v3.5-v3.8 remediation fingerprints (stale-sync canaries) ──────────────
check "execution/exit_engine.py"         "_confirm_and_book_live_exit"  "v3.5 fill-confirmed live exits"
check "execution/order_confirm.py"       "confirm_order_fill"           "v3.7 entry fill-confirmation module"
check "main.py"                          "confirm_order_fill"           "v3.7 condor legs book on confirmed fill"
check "execution/broker_reconcile.py"    "phantom_pnl"                  "v3.6 phantom P&L recovery"
check "database/trade_logger.py"         "max_premium_seen"             "v3.8 MFE/MAE telemetry columns"
check "database/trade_logger.py"         'COALESCE(paper_trade,1)'      "v3.7 mode-scoped queries (defect Q)"
check "strategy/condor_roll.py"          "ROLL IS REAL"                 "v3.7 roll places a real order (defect P)"
check "config.py"                        "SWEEP_POST_TARGET_TRAIL"      "v2.0 runner refinements in config"
check "execution/position_manager.py"    "df_5m"                        "v3.8 5m FVG trail anchor threaded"

# ── 2026-07-17/18 day-zero fingerprints (trend v3.1 + VWAP + condor + continuation) ──
check "analysis/trend_engine.py"         '"5m": 0.35'                   "trend v3.1 intraday-primary tf_weights (dead-4h fix)"
check "analysis/volatility_engine.py"    'price_vs_vwap = "NONE"'       "VWAP zero-volume guard (SPX NaN->BELOW fix)"
check "config.py"                        "CONDOR_TRIGGER_APPROACH"      "condor premium-rich band-approach triggers"
check "strategy/continuation_strategy.py" "ContinuationStrategy"        "continuation trade strategy present"
check "main.py"                          "_continuation_strategy"       "continuation registered in dispatch"
check "execution/exit_engine.py"         "_evaluate_continuation"       "continuation exhaustion exit"
check "strategy/continuation_strategy.py" "CONTINUATION_CONV_FLOOR"     "continuation conviction floor present"
check "config.py"                        "CONTINUATION_EXHAUST_EXT_ATR" "continuation exhaustion config block"

# ── v3.9 Phase-3.1 instrumentation fingerprints (log-only) ────────────────
check "analysis/signal_journal.py"       "def journal"                  "v1.0 signal journal module present"
check "risk/setup_scorer.py"             "_journal_scored"              "v1.3 scorer emits scored events (REJECTs included)"
check "analysis/orb_engine.py"           "retest_depth_px"              "v3.7 defect-G retest depth measurement"
check "main.py"                          "condor_leg"                   "v3.9 condor conviction journaled at fire time"
check "status.py"                        "ORB High"                    "Structured ORB display"
check "status.py"                        "No Trade"                    "No Trade display string"
check "notifications/alert_manager.py"   "send_shutdown_alert"          "Shutdown alert method"
check "notifications/alert_manager.py"   "INSTRUMENT"                   "Ticker in alerts"
check "notifications/alert_manager.py"   "send_regime_alert"            "Regime alert present (should be no-op/pass)"
check "risk/setup_scorer.py"             "return None"                  "Grade C elimination (returns None)"
check "risk/setup_scorer.py"             "Optional\[SetupScore\]"       "Score return type updated"
check "strategy/butterfly_strategy.py"   "gex_environment"              "GEX field name fix"
check "strategy/butterfly_strategy.py"   "BUTTERFLY_WING_SPX"           "Fixed wing widths"
check "strategy/butterfly_strategy.py"   "_fired_today"                 "One butterfly per session"
check "strategy/orb_strategy.py"         "ORBState.OPEN_LONG"           "ORB strategy state rename"
check "execution/exit_engine.py"         "POST_TARGET_TRAIL_LOCK_PCT"   "FVG trail past 100% TP"
check "execution/exit_engine.py"         "_find_1m_fvgs"                "1m FVG detection"
check "execution/position_manager.py"    "notify_position_closed"       "ORB re-arm hook on position close"
check "config.py"                        "BUTTERFLY_WING_SPX"           "Butterfly config constants"
check "config.py"                        "BUTTERFLY_ENTRY_START_ET"     "Butterfly noon entry window"
check "push.sh"                          "Detected malformed remote"    "Self-healing remote URL"
check "push.sh"                          "diverged"                    "Diverged history handling"
check "setup_ec2.sh"                     'GITHUB_REPO#https://'         "GitHub URL normalization"

echo ""
echo "============================================================"
echo "  GIT STATE"
echo "============================================================"
git log --oneline -10 2>/dev/null
echo ""
echo "Remote:"
git remote get-url origin 2>/dev/null
echo ""
echo "Uncommitted changes:"
git status --short 2>/dev/null
echo ""
echo "============================================================"
echo "  DONE"
echo "============================================================"
