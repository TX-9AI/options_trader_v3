#!/bin/bash
# v3.7 — 2026-07-23 — HEADER-AUDIT LABEL CORRECTIONS (no canary logic change):
#         risk_manager's 2026-07-23 full-budget entry relabeled v1.4 -> v3.2
#         (the file was already at v3.1); butterfly's 2026-07-14 discount gate
#         v1.4 -> v3.2; status.py's duplicated v1.12 (2026-07-20) -> v1.13.
#         Prose references below updated to match. Fingerprints unchanged.
#         BONUS CATCH: the half_budget absence canary was legitimately RED —
#         risk_manager's success-path log still referenced the deleted
#         half_budget variable (NameError on every successful condor-leg
#         sizing). Fixed as risk_manager v3.3; canary now green.
# v3.6 — 2026-07-23 — chain-archival fingerprints. A stale sync silently stops
#         archiving option chains, and chains cannot be backfilled — every
#         un-archived session is a permanent hole in the dataset.
# v3.5 — 2026-07-23 — condor v2 fingerprints (exit_engine v4.1, risk v3.2,
#         iron_condor v3.2, 11:11 gate). A stale sync silently restores the
#         un-ratcheted stop (every stopped leg round-tripped from ~+25% to
#         -25%), the half-size verticals, the leg-2 CANCEL, or the 11:00 window
#         that runs on a bb_middle=current_price fallback.
# v3.4 — 2026-07-22 — continuation EXIT-rework fingerprints (exit_engine v4.0):
#         5m-anchored trail, theta-bleed enabled, 25%% backstop. A stale file
#         silently reverts to 1m tripwire trails and NO theta protection.
# v3.3 — 2026-07-22 — continuation-unblock fingerprints (defect W). Pins that
#         TrendState surfaces primary_momentum and that the strategy READS it
#         — a stale sync of either file silently re-blocks the trade forever
#         with no error and no log, which is exactly how it hid for 4 days.
#         Also an ABSENCE check on the phantom "STEADY" value.
# v3.2 — 2026-07-22 — ORB geometry-gate fingerprints (setup_scorer v1.4).
#         Pins that the ORB grades via _grade_orb (liquidity-in-path A/B only)
#         and that _orb_quality is GONE — a stale file would silently restore
#         the regime/VWAP/macro-weighted ORB score that could veto a confirmed
#         break. Absence-check on _orb_quality is inverted (see below).
# v3.1 — 2026-07-22 — CANARY GAP CLOSED (audit defect U). Before this the
#         newest fingerprint was dated 2026-07-18: a stale sync of ANY file
#         shipped 07-20 → 07-22 (orb v3.9, sweep v3.2, main v4.0/v4.1,
#         regime_confluence v1.2, the whole limit_ladder execution change,
#         status v1.13) passed this check silently — the exact failure mode
#         this script exists to catch, and the one that caused the 07-16
#         unmanaged-position incident. Adds 16 fingerprints covering every
#         post-07-18 change, and pins the two VALUES (not just the names)
#         that a stale file would revert: the de-saturated ramp bound and the
#         paper-friction default.
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

# ══ 2026-07-20 → 07-22 fingerprints ══════════════════════════════
# Everything below post-dates the day-zero block. A box that misses any ONE of
# these is running a materially different engine from the control checkout and
# the parity invariant is broken — re-sync before trusting a session's data.

# ORB v3.9 (2026-07-20) — stale-retest timeout on REAL bars, and re-arming
check "analysis/orb_engine.py"           "_rearm"                       "v3.9 timeout re-arms (not terminal) — SMH missed-short fix"
check "analysis/orb_engine.py"           "bars_since_break"             "v3.9 timeout counts deduped 1m bars, not 15s loop ticks"

# status v1.12 (2026-07-20) — daily-loss banner reads the LIVE unit env
check "status.py"                        "get_runtime_env"              "v1.12 loss-limit read via runtime env (false \$200 HALT fix)"

# main v4.0 / L2.5 (2026-07-21) — the Layer-2 label drives live trading
check "main.py"                          "OT_REGIME_ENGINE"             "v4.0 L2 committed label drives regime (+v13 rollback)"
check "main.py"                          "ConvictionIntegrator"         "v4.0 integrator wired into the live loop"
check "main.py"                          "integrator_state.json"        "v4.0 conviction book persisted per box"

# sweep v3.2 (2026-07-21) — ORB-ownership gate
check "strategy/sweep_reversal_strategy.py" "_orb_released_price"       "v3.2 sweep blocked until the ORB releases price"

# regime_confluence v1.2 (2026-07-22) — ramp de-saturation. PIN THE VALUES:
# a stale file keeps the constant NAMES and silently reverts the bounds, which
# is invisible to a name-only check and would re-saturate RANGING.
check "analysis/regime_confluence.py"    "RANGE_ROOM_LO\", 0.17"        "v1.2 room_s lower bound de-saturated (0.05 -> 0.17)"
check "analysis/regime_confluence.py"    "OSC_CROSS_HI\", 10.0"         "v1.2 osc_s upper bound de-saturated (5 -> 10)"
check "analysis/regime_confluence.py"    "_envf"                        "v1.2 all 14 ramp bounds env-overridable (OT_RC_*)"

# limit_ladder (2026-07-22) — the mark-limit execution policy
check "execution/limit_ladder.py"        "hard_close_order_mode"        "limit ladder present: 15:40 mark-limit -> 15:45 MARKET"
check "execution/entry_engine.py"        "limit_at_mark"                "v3.9 entries post a LIMIT at the mark (was MARKET)"
check "execution/exit_engine.py"         "limit_at_mark"                "closes post at the mark, re-priced each tick"
check "config.py"                        "FLATTEN_WINDOW_OPEN_ET"       "flatten window opens 15:40 (config + time_utils)"
check "utils/time_utils.py"              "FLATTEN_WINDOW_OPEN"          "v3.8 is_hard_close_time() opens at 15:40"

# paper-friction unification (2026-07-22, audit defect T) — one authority
check "execution/limit_ladder.py"        "def paper_fill_credit"        "v1.3 single paper-pricing authority (credit side)"
check "main.py"                          "paper_fill_credit"            "v4.1 condor leg paper credit uses the shared authority"
check "strategy/condor_roll.py"          "paper_fill_credit"            "v3.8 rolled vertical uses the shared authority"
check "config.py"                        "OT_PAPER_SLIPPAGE_PCT\", \"0.0\"" "paper friction default 0.0 (books the mark)"

# ── ORB geometry gate (setup_scorer v1.4, 2026-07-22) ────────────────────
check "risk/setup_scorer.py"             "_grade_orb"                   "v1.4 ORB graded by geometry gate (liquidity-in-path A/B only)"
check "risk/setup_scorer.py"             "_pools_in_path"               "v1.4 ORB A/B selector = unswept pool between entry and TP"

# ── trend continuation unblocked (defect W, 2026-07-22) ──────────────────
check "analysis/trend_engine.py"         "primary_momentum"             "v3.2 TrendState surfaces primary_momentum (5m vote)"
check "strategy/continuation_strategy.py" "primary_momentum"            "v1.1 continuation READS primary_momentum (was silently \"\")"
check "config.py"                        "OT_CONT_STOP_PCT"             "continuation backstop 25%% (was blanket 40%%)"
check "execution/exit_engine.py"         "CONTINUATION_STOP_LOSS_PCT"   "v4.0 continuation floor uses its own pct, not MAX_LOSS_PCT"
check "execution/exit_engine.py"         "_fvg_frame(df_1m, df_5m),"    "v4.0 continuation trail anchors to 5m FVGs"

# ── condor v2 (2026-07-23) ────────────────────────────────────────────────
check "config.py"                        "(11, 11)"                     "condor window opens 11:11 (BB valid; no current_price fallback)"
check "config.py"                        "OT_CONDOR_RATCHET_BE"         "condor ratchet knobs present"
check "config.py"                        "OT_CONDOR_TP_PCT"             "condor time-gated TP knob present"
check "execution/exit_engine.py"         "_condor_ratchet"              "v4.1 condor ratcheting stop (BE at +20%, lock +20% at +40%)"
check "execution/exit_engine.py"         "_condor_sibling_open"         "v4.1 TP fires only on a STANDALONE, never a condor leg"
check "execution/exit_engine.py"         "condor_tp pnl="               "v4.1 time-gated take-profit exit reason"
check "risk/risk_manager.py"             "leg_budget"                   "v3.2 condor vertical sized at FULL budget (was half)"
check "analysis/chain_snapshot.py"       "def snapshot"                 "chain archival module present (full 0DTE chain -> .jsonl.gz)"
check "analysis/chain_snapshot.py"       "vega"                         "chain archival keeps gamma+vega (signal_journal drops them)"
check "main.py"                          "chain_snapshot import snapshot" "v4.2 chain archival wired into the every-tick GEX block"
check "strategy/iron_condor_strategy.py" "Leg 2 PAUSED"                 "v3.2 leg 2 pauses on non-RANGING (was CANCELLED)"
# ABSENCE: the half-size budget must be gone
if grep -q "half_budget" risk/risk_manager.py 2>/dev/null; then
    echo "  \u2717 STALE:   risk_manager still half-sizes condor verticals (expected FULL budget)"
else
    echo "  \u2713 PRESENT: condor verticals sized at full budget (no half_budget)"
fi
# ABSENCE: "STEADY" is a phantom — trend_engine emits ACCELERATING/DECELERATING/
# FLAT only. Its return means a stale continuation_strategy.py is back.
if grep -qE 'momentum in \("ACCELERATING", "STEADY"\)' strategy/continuation_strategy.py 2>/dev/null; then
    echo "  \u2717 STALE:   continuation_strategy uses phantom STEADY value — pre-v1.1 file restored"
else
    echo "  \u2713 PRESENT: continuation momentum vocabulary is ACCELERATING/FLAT (no phantom STEADY)"
fi
# ABSENCE check: _orb_quality must be GONE from executable code. A stale sync
# that restores it re-introduces the regime/VWAP/macro-weighted ORB score. We
# grep only for a CALL (self._orb_quality(), def _orb_quality) — the string
# survives in the v1.4 changelog prose, which is fine.
if grep -qE "def _orb_quality|self\._orb_quality\(" risk/setup_scorer.py 2>/dev/null; then
    echo "  \u2717 STALE:   _orb_quality is BACK in setup_scorer.py — ORB weighted score restored (expected DELETED)"
else
    echo "  \u2713 PRESENT: _orb_quality deleted from code (ORB is a geometry gate)"
fi

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
