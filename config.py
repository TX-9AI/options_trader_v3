"""
config.py — options_trader v3.3
v3.3 — 2026-07-13 — CUTOFF DISAMBIGUATION (defect H). Two constants named so
        similarly they were confused for one rule are now named for their scope,
        and the global cutoff is no longer hardcoded outside config.
        (a) NO_ENTRY_AFTER_ET -> ORB_NO_ENTRY_AFTER_ET. Unchanged at (11, 0).
            It is, and always was, the ORB-scoped cutoff (orb_engine v3.6) and
            the arm condition for sweep reversal (sweep_reversal_strategy v3.1).
        (b) NEW: GLOBAL_NO_ENTRY_ET = (14, 0) — the global 0DTE entry cutoff for
            ALL strategies. utils/time_utils v3.1 now READS this instead of
            hardcoding dtime(14, 0), so config is finally the single source of
            truth for both cutoffs.
        NOT a behaviour change: both cutoffs keep their exact prior values.
v1.0 — original release
v1.1 — 2026-06-27 — remove Twilio, fix SWEEP_TARGET_DELTA to 0.08,
        remove Grade C, add BUTTERFLY_ENTRY_CUTOFF_ET
v1.2 — 2026-06-29 — butterfly overhaul: fixed wings by instrument,
        GEX pin proximity gate (1x expected move), noon-2PM entry window,
        one-per-session limit, TP reduced to 20%
v1.3 — 2026-07-02 — narrow SPX condor wings 25->5 so each vertical is
        affordable (max loss ~$235/contract), enabling half-budget-per-side
        condor sizing.
v1.4 — 2026-07-02 — add DAILY_LOSS_LIMIT_USD (default = per-trade risk): halts
        new entries when the day's NET P&L is down by that amount.
v1.5 — 2026-07-02 — add single-name instruments (NFLX/META/MU/MSFT/TSLA/AAPL/
        NVDA/SMCI/ORCL) as DIRECTIONAL-ONLY: ORB + sweep only, no condor/
        butterfly. Widens paper-trading coverage for data collection.
v1.6 — 2026-07-03 — expand the tradeable universe to the full screener list.
v1.8 — 2026-07-15 — live fill-confirmation knobs (LIVE_FILL_*, v3.5) and
        reconcile cadence (BROKER_RECONCILE_INTERVAL_MIN, v3.6); and
        BROKER_RECONCILE_ENABLED now defaults to the trading mode (LIVE=on,
        PAPER=off) so going live via configure.sh auto-enables reconciliation —
        explicit OT_BROKER_RECONCILE=True/False still overrides.
v2.0 — 2026-07-15 — RUNNER REFINEMENTS (all env-tunable): MAX_LOSS_PCT
        25%→40% for directionals (butterfly pinned at 25% via
        BUTTERFLY_STOP_LOSS_PCT); USE_5M_FVG_TRAIL (5-minute FVGs anchor
        trails); FVG_FLOOR_MAX_LOCK_PCT=0.90 clamp; POST_TARGET_TRAIL_LOCK_PCT
        0.85→0.75 (leash no longer inverts past target);
        SWEEP_POST_TARGET_TRAIL=True (sweep runners trail past +100% instead
        of the hard TP).
v1.9 — 2026-07-15 — LIVE_ENTRY_DEADLINE_SECONDS (entry fill-confirmation
        window, defect O) and PAPER_FILL_SLIPPAGE_PCT now env-tunable with an
        honest 1% default applied against the trade (defect R).
        Neutral strategies run ONLY on true-0DTE index products (SPY/QQQ/SPX/
        IWM); every other symbol (single names + weekly-only ETFs) is
        directional-only, derived automatically from FULL_STRATEGY_INSTRUMENTS.
v1.7 — 2026-07-03 — sweep strike delta now scales with reversal strength
        (strong->far-OTM, weak->near-ATM); ORB strike snapping breaks toward
        higher/lower delta; paper fills at the exact bid/ask midpoint (no
        slippage) — all orders priced at the mark.
v3.0 — 2026-07-10 — repo-wide v3.0 bump: Yahoo-Finance purge & data stream
        mapping optimization (all market data now flows from the single
        shared TastyTrade candle feed — see data/candle_feed.py). No logic
        change in this file.
v3.2 — 2026-07-12 — TOLERANCES REMOVED + SESSION_LOSS_LIMIT deleted.
        (a) ORB_BREAK_BUFFER (0.05% of price) REMOVED. It gated the break on the
            close clearing the range by a PERCENTAGE — $0.49 on MU, ~$3.00 on SPX.
            The retest is already the noise filter (a meaningless break fails it),
            so the buffer only cost real setups while scaling into a hole on
            high-priced instruments. See orb_engine v3.5.
        (b) SESSION_LOSS_LIMIT (the integer 2) DELETED. It was a COUNT of losing
            trades from the v1.x count-based circuit breaker, and it is NOT the
            daily loss halt. It has been vestigial since risk_manager v1.4, which
            requests a regime reassessment after EVERY losing trade — the count
            gates nothing. It survived only in dashboards, which printed
            "Session CB: 2 losses -> halt" for a halt that could never occur.
            The REAL halt is DAILY_LOSS_LIMIT_USD (below): dollars, net for the
            day, so a green day keeps trading no matter how many losses stack up.
v3.1 — 2026-07-12 — DEAD-CONSTANT PURGE + honest comments.
        (a) BUTTERFLY_ENTRY_CUTOFF_ET 15:00 -> 14:00. The 15:00 value was
            UNREACHABLE: main.py calls session_guard.can_enter() WITHOUT
            is_butterfly=True, so the generic 14:00 cutoff always fired first.
            14:00 is also the intended rule (post-14:00 tape gets erratic on
            dealer hedging). This makes config agree with live behaviour; it is
            NOT a behaviour change.
        (b) REMOVED, never imported by any module (verified by grep across the
            tree and by git log -S back to the initial commit):
              ORB_TRAIL_ACTIVATION   — duplicate of TRAIL_ACTIVATION_PCT
              CONDOR_SHORT_DELTA     — from iron_condor v1.0 (delta selection),
              CONDOR_DELTA_TOLERANCE   dead since v1.1 made strikes BB-anchored
              MIN_TF_CONFLUENCE      — concept lives in regime_classifier v1.3 as
                                       a HARDCODED `aligned_timeframes < 2`; the
                                       config value (1) was LOOSER and unwired
              ENTRY_COOLDOWN_MINUTES — ORB's state machine IS the cooldown
                                       (waiting / armed / open are exclusive)
        (c) The Iron Condor comment claiming "Delta-based strike selection is
            primary" was false since v1.1 — strikes are Bollinger-Band anchored
            with NO delta anywhere. Corrected.
        (d) MIN_RRR and VWAP_FILTER_ACTIVE are RETAINED but explicitly marked
            UNWIRED. Both are genesis constants (present at the initial commit,
            never referenced, never mentioned in any changelog). They are kept
            because each names an intended feature that was never built — see
            the notes at their definitions. Deleting them would erase the only
            evidence the intent existed.

All secrets come from environment variables — never from hardcoded values
or editable files. The setup_ec2.sh script writes them into the systemd
unit so the bot has them at runtime without any manual file editing.

Tunable strategy parameters live here and are safe to commit.
"""

import os
from dataclasses import dataclass
from typing import Optional


# ─── ENVIRONMENT HELPERS ──────────────────────────────────────────────────────

def _require(key: str) -> str:
    val = os.environ.get(key, "")
    if not val:
        raise EnvironmentError(
            f"\n\n  ❌  Missing required environment variable: {key}\n"
            f"      Run setup_ec2.sh to configure this bot properly.\n"
            f"      For local dev, export {key}='...' in your shell.\n"
        )
    return val

def _optional(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


# ─── TASTYTRADE CREDENTIALS (from environment) ────────────────────────────────

def get_tt_client_secret()  -> str: return _require("TT_CLIENT_SECRET")
def get_tt_refresh_token()  -> str: return _require("TT_REFRESH_TOKEN")
def get_tt_account_number() -> str: return _require("TT_ACCOUNT_NUMBER")


# ─── TELEGRAM ALERTS (from environment) ──────────────────────────────────────

def get_telegram_token()    -> str: return _optional("TELEGRAM_TOKEN")
def get_telegram_chat_id()  -> str: return _optional("TELEGRAM_CHAT_ID")

def telegram_configured() -> bool:
    return bool(get_telegram_token() and get_telegram_chat_id())


# ─── INSTRUMENT SELECTION ─────────────────────────────────────────────────────

INSTRUMENT          = os.environ.get("OT_INSTRUMENT", "QQQ")

# Tradeable universe. Strike increments are a per-price-band starting point;
# the options chain resolves to the nearest liquid strike, so a slightly-off
# value is not fatal — tune a name here only if its fills consistently miss.
STRIKE_INCREMENTS = {
    # Index products with true 0DTE — full strategy set (condor/butterfly OK)
    "SPY": 1, "QQQ": 1, "SPX": 5, "IWM": 1,
    # Weekly-only ETFs — directional only
    "DIA": 1, "SMH": 1, "TLT": 1, "GLD": 1,
    # Single names — directional only
    "AAPL": 5, "MSFT": 5, "META": 5, "MU": 5, "TSLA": 5, "NVDA": 1,
    "NFLX": 1, "ORCL": 1, "SMCI": 1, "PLTR": 1, "AMD": 1, "AMZN": 1,
    "GOOGL": 1, "XOM": 1, "CVX": 1, "JPM": 5, "GS": 5, "LLY": 5,
    "UNH": 5, "AVGO": 5, "CRM": 5, "COST": 5,
}
STRIKE_INCREMENT    = STRIKE_INCREMENTS.get(INSTRUMENT, 1)

# Neutral strategies (iron condor, butterfly) require true-0DTE decay and strike
# density, so they run ONLY on these. Every other tradeable symbol is
# directional-only (ORB + Sweep Reversal), derived automatically — add a symbol
# to STRIKE_INCREMENTS and it's directional unless it's listed here.
# 2026-07-14 (operator directive): neutral strategies enabled FLEET-WIDE for
# data collection — every configured symbol runs butterfly/condor eligibility.
# Was {"SPY","QQQ","SPX","IWM"}, which silently excluded 26 of 29 live boxes.
FULL_STRATEGY_INSTRUMENTS    = set(STRIKE_INCREMENTS)

# ── Butterfly discount gate (2026-07-14, operator directive) ──────────────────
# The fly's edge is buying the tent at a DISCOUNT while price still has to walk
# into it: require net_debit <= this fraction of wing width (0.33 => min ~2:1
# reward:risk). Self-normalizing across symbols; needs only marks. PRIOR —
# calibrate from logged debit-ratio vs outcome once fleet-wide entries accrue.
BUTTERFLY_MAX_DEBIT_PCT_WIDTH = 0.33
DIRECTIONAL_ONLY_INSTRUMENTS = set(STRIKE_INCREMENTS) - FULL_STRATEGY_INSTRUMENTS
DIRECTIONAL_ONLY             = INSTRUMENT in DIRECTIONAL_ONLY_INSTRUMENTS
CONTRACT_MULTIPLIER = 100

# ─── ACCOUNT & RISK ───────────────────────────────────────────────────────────

RISK_PER_TRADE_USD  = float(os.environ.get("OT_RISK_USD", "200"))
# Daily loss limit: halt NEW entries when the day's NET realized P&L is down by
# this much. Defaults to one trade's risk; override via OT_DAILY_LOSS_LIMIT.
DAILY_LOSS_LIMIT_USD = float(os.environ.get("OT_DAILY_LOSS_LIMIT", str(RISK_PER_TRADE_USD)))
# v2.0 (runner refinement): the universal directional premium floor, now 40%
# by default. On 0DTE, gamma routinely wicks a healthy trade -25% while the
# thesis (impulsive origin) is intact — the old floor front-ran the structure
# stop and stopped winners on noise. Sizing is FULL-PREMIUM based (risk unit =
# position size), so at $1000 positions a floored trade now costs ~$400 (was
# ~$250) — set OT_DAILY_LOSS_LIMIT with that in mind. Butterflies keep their
# own 25% (their 20%-of-max TP can't carry a 40% stop); condors keep
# CONDOR_STOP_LOSS_PCT. Env-tunable for A/B: OT_MAX_LOSS_PCT=0.25 restores.
MAX_LOSS_PCT        = float(os.environ.get("OT_MAX_LOSS_PCT", "0.40"))
BUTTERFLY_STOP_LOSS_PCT = 0.25   # pin plays keep the tight floor (see above)
# Max-loss stop applied to an ADOPTED position (one discovered open at the
# broker on a LIVE restart with no DB plan). Defaults to the same threshold
# every strategy already respects, so an adopted position exits at the same
# "degree of red" our normal stops would have. Long: stop = entry*(1-pct);
# short: stop = entry*(1+pct).
ADOPTED_STOP_PCT    = float(os.environ.get("OT_ADOPTED_STOP_PCT", str(MAX_LOSS_PCT)))
# Master switch for LIVE broker<->DB position reconciliation (adopt / keep /
# phantom-close + v3.6 phantom P&L recovery).
# v1.8: FOLLOWS TRADING MODE by default — flipping to LIVE via configure.sh
# (or any other way OT_PAPER_TRADING=False is set) enables reconciliation
# automatically; nothing extra to remember on go-live. Paper stays OFF (paper
# never reconciles; the DB is truth there). An explicit OT_BROKER_RECONCILE
# =True/False still overrides in either direction — the escape hatch if
# get_open_option_positions() ever needs re-verifying on a live box.
_reconcile_env = os.environ.get("OT_BROKER_RECONCILE", "")
if _reconcile_env in ("True", "False"):
    BROKER_RECONCILE_ENABLED = _reconcile_env == "True"
else:
    BROKER_RECONCILE_ENABLED = os.environ.get("OT_PAPER_TRADING", "True") == "False"
# v3.6: minutes between intraday reconcile sweeps (was hardcoded 30). On top of
# these interval slots, dedicated wind-down sweeps fire at 15:45, 15:50, and a
# final 15:57 pass — the post-flatten truth check (the main loop goes dormant
# at 16:00, so the last sweep must land inside the hard-close window).
BROKER_RECONCILE_INTERVAL_MIN = int(os.environ.get("OT_BROKER_RECONCILE_INTERVAL_MIN", "10"))

# ─── PAPER TRADING ────────────────────────────────────────────────────────────

PAPER_TRADING       = os.environ.get("OT_PAPER_TRADING", "True") != "False"

# ─── VIX / IV THRESHOLDS ──────────────────────────────────────────────────────

VIX_LOW_THRESHOLD           = 15
VIX_ELEVATED_THRESHOLD      = 20
VIX_CRISIS_THRESHOLD        = 30
VIX_BUTTERFLY_DISABLE       = 20
VIX_BUTTERFLY_HALF_SIZE     = 15
VIX_NO_ENTRY_THRESHOLD      = 30
IV_RANK_HIGH                = 50

# ─── SESSION / TIME RULES ─────────────────────────────────────────────────────

TIMEZONE                    = "US/Eastern"
RTH_OPEN_ET                 = (9, 30)
RTH_CLOSE_ET                = (16, 0)
HARD_CLOSE_ET               = (15, 45)
# v3.8: the end-of-day flatten OPENS here and posts mark-limits (re-priced each
# ~15s tick) so positions can close without paying the spread; at HARD_CLOSE_ET
# it crosses unconditionally. An unfilled 0DTE at the bell is an expiry (and an
# assignment on a short leg), not an overnight hold — so the cross is absolute.
FLATTEN_WINDOW_OPEN_ET      = (15, 40)
ORB_NO_ENTRY_AFTER_ET       = (11, 0)   # ORB-SCOPED: ORB entries valid until 11:00 ET.
                                        #   Also the ARM condition for sweep reversal.
GLOBAL_NO_ENTRY_ET          = (14, 0)   # GLOBAL: no new 0DTE entries after 14:00 ET,
                                        #   ANY strategy. Read by utils/time_utils.
BUTTERFLY_ENTRY_CUTOFF_ET   = (14, 0)   # was 15:00 and unreachable (see v3.1 header)
BUTTERFLY_ENTRY_START_ET    = (12, 0)   # No butterfly entries before noon
ORB_WINDOW_MINUTES          = 5

# ─── ORB STRATEGY ─────────────────────────────────────────────────────────────

ORB_MAX_RETEST_BARS         = 12
ORB_TP_MULTIPLIER           = 1.0
FED_DAY_ORB_BOOST           = 0.20

# ─── ORB REGIME GATE SWITCH (v3.2) ────────────────────────────────────────────
# When True, a CONFIRMED ORB break+retest fires regardless of the regime label —
# including UNKNOWN and SWEEP_REVERSAL. The ORB engine's break+retest is self-
# validating (the classifier does not even test for it), so the label is not
# consulted for the go/no-go; only the setup scorer's B-threshold and the ORB
# engine's own structure gate it. Under UNKNOWN the regime_conviction dimension
# simply contributes 0 to the score. Under SWEEP_REVERSAL, ORB wins (the engine
# no longer defers its OPEN to the sweep). Set False to restore strict v2 gating
# (UNKNOWN/sweep block ORB). Every ORB that fires under UNKNOWN is logged with
# regime=UNKNOWN — labeled tape for the shadow observer.
ORB_FIRES_REGARDLESS_OF_REGIME = True
# When snapping an ORB strike target to the nearest available strike, break
# toward the "higher" (more ITM / participation) or "lower" (further OTM) delta.
ORB_STRIKE_DELTA_BIAS       = "lower"

# ─── SWEEP REVERSAL STRATEGY ──────────────────────────────────────────────────

# Sweep OTM strike delta scales INVERSELY with reversal strength (conviction):
# a strong snap-back can carry a far-OTM (low-delta) strike ITM for max leverage;
# a weak move needs a nearer, higher-delta strike to actually participate.
SWEEP_DELTA_STRONG          = 0.08   # conviction -> 1.0 : far-OTM, max leverage
SWEEP_DELTA_WEAK            = 0.30   # conviction -> 0.0 : near-ATM, participation
SWEEP_DELTA_TOLERANCE       = 0.04   # acceptable band around the target delta
SWEEP_MIN_REJECTION_PCT     = 0.003
SWEEP_MAX_AGE_BARS          = 8
# Entry-window tuning (separate pass from detection). The recovery window is now
# ATR-aware: a fast reversal on a volatile name that has already moved isn't
# rejected as "too far" — the window is the LARGER of a floor % or a multiple of
# ATR%. BOS lookback is configurable and also accepts a BOS that printed on the
# just-closed candle (so a 1-tick-late evaluation doesn't miss it).
SWEEP_MAX_RECOVERY_PCT      = 0.02   # floor recovery window (fraction of sweep price)
SWEEP_RECOVERY_ATR_MULT     = 1.5    # ...or this × ATR%, whichever is larger
SWEEP_BOS_LOOKBACK          = 5      # 1m candles used as the BOS structure reference

# ─── BUTTERFLY STRATEGY ───────────────────────────────────────────────────────

BUTTERFLY_TP_PCT            = 0.20   # 20% of max profit
BUTTERFLY_MAX_HOLD_MIN      = 150

# Fixed wing widths by instrument
BUTTERFLY_WING_SPX          = 25     # 25-point wings on SPX
BUTTERFLY_WING_QQQ          = 5      # $5 wings on QQQ/SPY

# GEX pin proximity gate: price must be within 1x expected move of pin
# Formula: underlying × VIX% × sqrt(hours_remaining/6.5) / sqrt(252)
# Computed at runtime in butterfly_strategy.py
BUTTERFLY_GEX_PIN_PROXIMITY_MULT = 1.0  # Multiplier on expected move

# ─── IRON CONDOR STRATEGY ─────────────────────────────────────────────────────
# Fallback for RANGING regime when no GEX pin is available for a butterfly.
# Strike selection is BOLLINGER-BAND ANCHORED — there is NO delta anywhere in the
# condor path (short call = lowest liquid strike at/above the BB upper band; short
# put = highest liquid strike at/below the BB lower band). Delta is deliberately
# excluded: it is relative to where price sits, not to the actual range boundary.
# The expected-move guardrail is a sanity check only, not a parallel sizing method.

CONDOR_WING_WIDTH_SPX       = 5      # Narrow wings — affordable verticals (was 25)
CONDOR_WING_WIDTH_QQQ       = 5      # Fixed wing width in points on QQQ/SPY
CONDOR_EXPECTED_MOVE_GUARDRAIL_MULT = 1.2  # Short strikes must be within this x EM
CONDOR_PROXIMITY_STRIKES    = 2      # (legacy) strikes inside the short — superseded by CONDOR_TRIGGER_APPROACH
# Fraction of the distance from the BB midline to each short strike that price
# must travel before that side's spread fires. Higher = price must get closer
# to the band before selling (richer premium, fewer fills). Env-tunable for A/B.
CONDOR_TRIGGER_APPROACH     = float(os.environ.get("OT_CONDOR_TRIGGER_APPROACH", "0.65"))
                                     # (2 strikes = 10pt on SPX, $2 on QQQ — scales naturally)
CONDOR_STOP_LOSS_PCT        = 0.25   # Exit if spread value rises to 125% of credit received
CONDOR_NICKEL_CLOSE         = 0.05   # Close leg when spread value decays to $0.05
CONDOR_ENTRY_START_ET       = (11, 0)   # No condor entries before 11 AM (after ORB window closes)
CONDOR_ENTRY_CUTOFF_ET      = (14, 0)   # Standard entry cutoff

# ─── EXIT MANAGEMENT ──────────────────────────────────────────────────────────

TRAIL_ACTIVATION_PCT        = 0.50
TRAIL_LOCK_PCT              = 0.25

# ─── LONG-OPTION THETA PROTECTION + FVG PROFIT TRAIL ──────────────────────────
# Theta bleed: exit a PROFITABLE long when the projected time decay over the next
# THETA_LOOKAHEAD_MIN minutes would erase the current unrealized gain (direction
# hasn't gone against us — the option is just handing the profit back to time).
THETA_LOOKAHEAD_MIN         = 20     # minutes of decay to project
RTH_MINUTES                 = 390    # 6.5h session, to convert daily theta → per-min
# FVG-anchored trailing stop for longs: once armed, the stop parks at the FAR
# edge of the nearest unfilled in-favor 1m FVG (room to pull back INTO the gap
# for continuation); a close beyond the gap exits. Falls back to a % lock.
FVG_TRAIL_ARM_PCT           = 0.20   # arm once the trade is up this much
FVG_TRAIL_LOCK_PCT          = 0.80   # premium floor = 80% of current when no FVG
# v2.0 runner refinements (all env-tunable for paper A/B):
# 5-minute FVGs anchor the trails instead of 1-minute — structurally
# meaningful gaps, natural gamma room; 1m stays for structure stop and BOS.
USE_5M_FVG_TRAIL            = os.environ.get("OT_USE_5M_FVG_TRAIL", "True") != "False"
# An FVG-derived floor may never sit tighter than this fraction of current
# premium — a gap hugging price can't turn the runner leash into a tripwire.
FVG_FLOOR_MAX_LOCK_PCT      = float(os.environ.get("OT_FVG_FLOOR_MAX_LOCK_PCT", "0.90"))
# Post-target no-FVG fallback lock. Was 0.85 — TIGHTER than the pre-target
# 75% ratchet, an inverted leash that harvested proven runners on one gamma
# wick. Now matches the pre-target trail.
POST_TARGET_TRAIL_LOCK_PCT  = float(os.environ.get("OT_POST_TARGET_TRAIL_LOCK_PCT", "0.75"))
# Sweep reversals get the ORB post-target trail instead of the +100%
# guillotine (the one hard TP among directionals). False restores target_hit.
SWEEP_POST_TARGET_TRAIL     = os.environ.get("OT_SWEEP_POST_TARGET_TRAIL", "True") != "False"

POLL_INTERVAL_SECONDS       = 15

# ─── REGIME CLASSIFICATION ────────────────────────────────────────────────────

ADX_TREND_THRESHOLD         = 25
ADX_RANGE_THRESHOLD         = 25   # v3.3 (2026-07-14): was 20 — closed the ADX
                                   # DEAD ZONE. _is_ranging required adx<20 while
                                   # _is_trending requires adx>=25, so ordinary
                                   # mild-drift tape at ADX 20-25 matched NO regime
                                   # and fell to UNKNOWN (hard no-trade). Measured
                                   # live: AAPL sat at ADX 19.26 — 0.74 under the
                                   # cliff — flickering RANGING<->UNKNOWN all session;
                                   # ~85% of fleet ticks were UNKNOWN on 07-13/07-14
                                   # and the fleet took ZERO trades for two days.
                                   # A range does not stop being a range because ADX
                                   # ticked 19.9 -> 20.1; it is the same regime with
                                   # LOWER CONVICTION. _ranging_conviction already
                                   # ramps on 1 - adx/ADX_RANGE_THRESHOLD, so raising
                                   # the gate to the trend line extends that ramp
                                   # across the gap: ADX 12 -> ~0.52, ADX 24 -> ~0.16.
                                   # Matches docs/REGIME_TRUTHS.md, which defines ADX
                                   # for RANGING as "any (allowed)" and strength as a
                                   # SOFT-NECESSARY ramp, never a cliff.
                                   # PRIOR — recalibrate from multi-day tape.
ATR_EXPANSION_MULTIPLIER    = 1.5
BB_WIDTH_COMPRESSION_PCT    = 0.20
SWEEP_REJECTION_CANDLES     = 3
EQUAL_LEVEL_PCT             = 0.001
REGIME_REASSESS_MINUTES     = 5

# ─── SETUP SCORING ────────────────────────────────────────────────────────────

GRADE_A_MIN_SCORE           = 0.78
GRADE_B_MIN_SCORE           = 0.55

# ── Brief nudge (2026-07-15) ─────────────────────────────────────────────────
# Signed pre-market move-probability prior applied post-sum in setup_scorer:
# +w·strength for ORB, -w·strength for neutrals, 0 for sweep reversal. This
# value is the hard cap (strength is 0..1). Small on purpose — a tie-breaker,
# never an override. Calibrate from the signal ledger once entries accrue.
BRIEF_CONVICTION_WEIGHT     = 0.05
GRADE_SIZE_MULTIPLIER       = {"A": 1.5, "B": 1.0}

# ─── VOLATILITY / TREND ───────────────────────────────────────────────────────

ATR_PERIOD                  = 14
ATR_STOP_MULTIPLIER         = 1.5
BB_PERIOD                   = 20
BB_STD                      = 2.0
EMA_FAST                    = 9
EMA_MID                     = 21
EMA_SLOW                    = 50
EMA_ANCHOR                  = 200

# ─── LIQUIDITY MAPPING ────────────────────────────────────────────────────────

EQUAL_HIGH_LOW_LOOKBACK     = 50
IMBALANCE_MIN_SIZE_PCT      = 0.002
LIQUIDITY_BUFFER_PCT        = 0.003

# ─── SIGNAL VALIDATION ────────────────────────────────────────────────────────

# ⚠️ UNWIRED — neither constant is imported anywhere. Both date to the initial
# commit and appear in no changelog. Retained deliberately as a record of intent:
#   MIN_RRR            — no risk/reward floor exists in the codebase. ORB's RRR is
#                        structural (stop = impulsive origin, target = 100% of range
#                        width), so it varies per setup and is currently ungated.
#   VWAP_FILTER_ACTIVE — implies a HARD VWAP gate. None exists. What is live is a
#                        SOFT score in setup_scorer (vwap_alignment, weight 0.15;
#                        a misaligned trade scores 0.25 on that dimension and can
#                        still clear the 0.55 B-threshold). NOTE: crypto_trader
#                        learned the opposite lesson the hard way — shorts above
#                        VWAP / longs below VWAP had to become HARD blocks. That
#                        lesson is NOT ported here. Open decision.
MIN_RRR                     = 1.3    # UNWIRED
VWAP_FILTER_ACTIVE          = True   # UNWIRED

# ─── STRUCTURE ANALYSIS ───────────────────────────────────────────────────────

SWING_LOOKBACK              = 10
MIN_SWING_SIZE_ATR          = 0.5
FVG_MIN_SIZE_PCT            = 0.001
SR_TOUCH_MIN                = 2
SR_ZONE_PCT                 = 0.002
ORDER_BLOCK_LOOKBACK        = 20

# ─── ORDER EXECUTION ──────────────────────────────────────────────────────────

LIMIT_RETRY_SECONDS         = 30
LIMIT_IMPROVE_TICKS         = 1
# v1.9 (audit defect R): paper fills now model live friction instead of the
# frictionless exact-mid fill. Applied AGAINST the trade on every paper entry:
# debits pay (1+pct)·mid, credits receive (1−pct)·mid — condor legs included
# (they previously ignored this knob entirely). Default 1%: modest, but paper
# stops structurally flattering live. Set OT_PAPER_SLIPPAGE_PCT=0.0 to restore
# the old frictionless fills for apples-to-apples comparison with history.
PAPER_FILL_SLIPPAGE_PCT     = float(os.environ.get("OT_PAPER_SLIPPAGE_PCT", "0.01"))

# ─── TASTYTRADE API ───────────────────────────────────────────────────────────

TT_BASE_URL                 = "https://api.tastytrade.com"
TT_PAPER_BASE_URL           = "https://api.cert.tastyworks.com"

# ─── MACRO / FED CALENDAR ─────────────────────────────────────────────────────

FOREX_FACTORY_URL           = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
MACRO_FETCH_INTERVAL_MIN    = 60
FED_EVENT_KEYWORDS          = ["FOMC", "Fed", "Federal Funds Rate", "Powell"]

# ─── TIMEFRAMES ───────────────────────────────────────────────────────────────

TIMEFRAMES = {
    "1d":  {"candles": 10,  "role": "bias"},
    "1h":  {"candles": 50,  "role": "structure"},
    "15m": {"candles": 50,  "role": "trend"},
    "5m":  {"candles": 100, "role": "entry_context"},
    "1m":  {"candles": 60,  "role": "trigger"},
}

CACHE_STALENESS_SECONDS = {
    "1d":  3600,
    "1h":  300,
    "15m": 120,
    "5m":  30,
    "1m":  10,
}

# ─── NOTIFICATIONS ────────────────────────────────────────────────────────────

NOTIFY_ON_ENTRY             = True
NOTIFY_ON_EXIT              = True
NOTIFY_ON_CIRCUIT_BREAK     = True
NOTIFY_ON_REGIME_CHANGE     = True

# ─── DATABASE & LOGGING ───────────────────────────────────────────────────────

DB_PATH                     = os.path.expanduser("~/options-trader/trades.db")
LOG_LEVEL                   = "INFO"
LOG_FILE                    = os.path.expanduser("~/options-trader/bot.log")
LOG_ROTATION_MB             = 50

# ─── BOT IDENTITY ─────────────────────────────────────────────────────────────

BOT_NAME                    = os.environ.get("OT_BOT_NAME", "OptionsTrader")

# ─── LIVE EXIT FILL-CONFIRMATION (v3.5) ──────────────────────────────────────
# Governs ExitEngine._confirm_and_book_live_exit (live/cash mode ONLY — the
# paper path never reads these). See FABLE_SPEC_live_exit_fill_confirmation.md.

# Seconds between broker order-status polls while a close order is working.
LIVE_FILL_POLL_SECONDS      = float(os.environ.get("OT_LIVE_FILL_POLL_SECONDS", "2"))
# Total seconds to wait for a fill before cancelling and handing the position
# back to the caller's retry loop (15:45→16:00 hard-close retries + paging).
LIVE_FILL_DEADLINE_SECONDS  = float(os.environ.get("OT_LIVE_FILL_DEADLINE_SECONDS", "30"))
# Marketable-limit buffer ($/share THROUGH the mark) for multi-leg closes.
# tastytrade rejects MARKET orders on spreads, so closes go out as aggressive
# limits: vertical debit = min(mark + buffer, spread width); butterfly credit
# = max(mark - buffer, one tick). Retry ticks re-price at a fresh mark.
LIVE_CLOSE_LIMIT_BUFFER     = float(os.environ.get("OT_LIVE_CLOSE_LIMIT_BUFFER", "0.10"))
# v1.9 (audit defect O): bounded fill-confirmation window for ENTRY orders.
# Entries are optional (unlike exits): unfilled at the deadline -> cancel and
# walk away; the strategy re-evaluates next tick. Whatever DID fill is booked.
LIVE_ENTRY_DEADLINE_SECONDS = float(os.environ.get("OT_LIVE_ENTRY_DEADLINE_SECONDS", "20"))


@dataclass
class SessionConfig:
    """Runtime session config — populated at startup."""
    paper_trading:      bool    = True
    instrument:         str     = "QQQ"
    risk_per_trade_usd: float   = 200.0
    notes:              str     = ""
    confirmed_at:       Optional[str] = None

# ─── CONTINUATION (trend-pullback) exhaustion exit ────────────────────────────
# Exhaustion detection for the trend-continuation runner. Extension tightens the
# trail; momentum divergence exits. All env-tunable for paper-phase calibration.
CONTINUATION_EXHAUST_EXT_ATR    = float(os.environ.get("OT_CONT_EXT_ATR", "2.0"))   # ATRs from midline = "stretched"
CONTINUATION_EXHAUST_MIN_GAIN   = float(os.environ.get("OT_CONT_MIN_GAIN", "0.15")) # only manage exhaustion past +15%
CONTINUATION_EXHAUST_TRAIL_LOCK = float(os.environ.get("OT_CONT_TRAIL_LOCK", "0.85"))# extension tightens trail to 85% of premium
