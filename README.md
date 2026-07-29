# Options Trader v3 — Vertigo Capital

Automated day-trading suite utilising the TastyTrade/DXFeed data stream for 0-DTE
options. Entries, exits, position sizing and risk are driven by two weighted
scores:

- **Confluence** — the weighted accumulation of evidence *for a setup*. Each
  factor contributes according to its own weight, so agreement builds a graded
  score rather than tripping a switch.
- **Conviction** — the weighted score *for the regime* the setup is firing into,
  produced by the Layer-1/Layer-2 regime engine.

Confluence decides whether the setup is real; conviction decides how much the
system believes the conditions around it. Together they determine whether a trade
fires, how large it is, and which strike it takes. Runs across a 29-box fleet,
one symbol per box.

**Documentation map:** [`docs/README.md`](docs/README.md) routes by question.
Behaviour → [`docs/MECHANICS.md`](docs/MECHANICS.md) · Work outstanding →
[`docs/BACKLOG.md`](docs/BACKLOG.md) · Plans → [`docs/ROADMAP.md`](docs/ROADMAP.md)
· Module dependency map → [`docs/FILE_MAP.md`](docs/FILE_MAP.md) · Operating rules
→ [`docs/WORKING_AGREEMENT.md`](docs/WORKING_AGREEMENT.md)

---

## Deployment

```bash
curl -fsSL https://raw.githubusercontent.com/TX-9AI/options_trader_v3/main/install.sh -o install.sh && bash install.sh
```


```bash
cd ~/options-trader
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
sudo systemctl restart optionsbot
bash check_versions.sh
```


**`config.py` must always default to `PAPER_TRADING = True`.**

---

---

## Architecture

### Fleet topology — and the parity invariant

**This repo is one artifact deployed into two different roles.**

- **29 trading boxes** (EC2, one symbol each) run `main.py` under `optionsbot.service`, plus
  `candle-feed.service`. 29, not 30: `STRIKE_INCREMENTS` is a strike-increment *lookup table*
  (a superset, 30 entries); SPY is defined but not deployed, because SPX covers it.
- **1 control server** runs `fleet.py`. **`fleet.py` lives in `day_trader_pro`, not here** —
  which is why `harden_hosts.sh` and `pull_today_ohlc.sh` reference a file that isn't in this
  tree: they are *invoked by* control, they do not invoke it.

`tests/` ships to all 29 boxes but is *exercised* on control, against harvested,
fleet-aggregated tape. That is deliberate: the harnesses **import the live engines**
(`orb_engine`, `regime_classifier`, `regime_confluence`, `exit_engine`) rather than
re-implementing them, so a backtest always runs the *same execution model the fleet is
running*.

> **INVARIANT — any engine patch deployed to the fleet must also be deployed to control.**
> Otherwise the backtest silently stops being apples-to-apples. It will still run, still
> produce numbers, and those numbers will be measuring a bot that no longer exists.
> **Nothing currently enforces this.** It belongs in `check_versions.sh`.

For the full module-by-module map — what each file calls and what calls it — see
[`docs/FILE_MAP.md`](docs/FILE_MAP.md).

---

## Regime engine (running since 2026-07-21: L1 `regime_confluence.py` v1.3 → L2 `conviction_integrator.py` v2.0, wired in `main.py` v4.0)

**The live label is the Layer-2 committed label.** Every tick, `regime_confluence.evidence()`
(hard_veto × soft_necessary × Σ corroborators, per REGIME_TRUTHS) feeds the leaky conviction
integrator; the integrator's committed argmax overrides `primary_regime`/`conviction`. θ_hold /
displacement hysteresis holds a regime through single-tick evidence drops (the v1.3 defect this
fixes: dropping to `UNKNOWN` mid-trend at avg ADX ≈ 29 — a hard no-trade gate firing during the
strongest conditions). **`UNKNOWN` is never emitted live**; `stale` (data fault) remains the only
hard no-trade marker. The book persists per box (`data/integrator_state.json`), warm-loaded at
boot. **The conviction NUMBER is observe-only** — logged, not gated; L3 places the bars later.
Rollback: `OT_REGIME_ENGINE=v13`.

Full regime definitions, the factor grammar, and every threshold live in
[`docs/MECHANICS.md`](docs/MECHANICS.md).

---

## Strategies

What each one is and when it wants to trade. Entry gates, thresholds and exit
paths are in [`docs/MECHANICS.md`](docs/MECHANICS.md).

| strategy | what it is | fires when |
|---|---|---|
| **ORB** (flagship) | Opening-range breakout. Mechanical by design — no confluence gates. | Price breaks the 5-min opening range and returns to retest it, closing back outside. |
| **Sweep Reversal** | Fades a liquidity sweep — price runs a level, fails, reverses. | A named level is swept and price reclaims it with a confirmed rejection. |
| **Trend Continuation** | Joins an established trend on a pullback. | Trend is confirmed and a 1-min wick tags the nearest unfilled 5-min FVG. |
| **Iron Condor** | Two independent credit spreads either side of a range. Short premium. | Range-bound tape; each side fires on its own trigger, at a strike beyond both 0.80×expected-move and the Bollinger band. |
| **Debit Butterfly** | Pins a compression coil to a target price. | Compression regime with a credible pin. |
| **Broken-Wing Roll** | Repairs a threatened condor side by rolling it into an asymmetric structure. | A condor side is under pressure and the roll is credit-positive. |

**In development** (not firing; see [`docs/ROADMAP.md`](docs/ROADMAP.md)):

- **Trend Credit Spread (TC.4)** — participates in a strong trend that never pulls
  back, by selling premium beneath it (PCS in a bull, CCS in a bear). Readiness
  track is live and log-only; the firing engine is gated on calibration and on the
  Layer-1 excavation.
- **Pitchfork sloped S/R** — designed, not built, gated on Layer 2. See
  [`docs/WHITEPAPER_pitchfork_overlay.md`](docs/WHITEPAPER_pitchfork_overlay.md).

## Exits

Every position has a stop, and most have a structural or trailing exit that fires
before it. Exits are evaluated every tick; first match wins. The complete
catalogue — every strategy, every path, with current values — is in
[`docs/MECHANICS.md`](docs/MECHANICS.md).

**End of day, every position:** at **15:40 ET** the flatten window opens and exits
post at the mark, re-priced every tick; at **15:45 ET** anything still open is
closed with a MARKET order, no exceptions.

## Risk

- **Grade A = 1.5× base risk · Grade B = 1.0×. There is no Grade C** — below-threshold setups
  return `None` and never fire.
- **Regime reassessment after *every* losing trade.** A loss is fresh information about whether
  the regime read still holds.
- **The only circuit breaker is `DAILY_LOSS_LIMIT_USD`** (default = one trade's risk). It halts
  **new entries** when the day's **NET realized P&L** is down by that amount. Wins offset
  losses — a green day keeps trading no matter how many individual losses stack up; only a
  genuinely red day halts. Seeded from the DB on startup, so it survives restarts within the
  session. Open positions keep being managed to their exits. Override via `configure.sh` →
  option 6.
  > The old count-based breaker (`SESSION_LOSS_LIMIT = 2`) was **deleted in config v3.2.** It
  > had gated nothing since risk_manager v1.4 — which requests a reassessment after *every*
  > loss — yet four dashboards still printed *"Session CB: 2 losses → halt"*, a halt that could
  > never occur. `session_losses` survives as a statistic only.
- **Broker reconciliation** (`execution/broker_reconcile.py`, v3.6): **auto-follows the
  trading mode** — flipping to LIVE via `configure.sh` enables it, PAPER keeps it off, and an
  explicit `OT_BROKER_RECONCILE=True/False` pins it either way (configure.sh warns loudly on
  go-live if it's pinned off). Runs at startup and intraday every
  `BROKER_RECONCILE_INTERVAL_MIN` minutes (default **10**), plus wind-down sweeps at
  **15:45, 15:50, and 15:57** — the last guaranteed look before the loop goes dormant at 16:00.
  A broker position with no DB plan is *adopted* (sign-correct `ADOPTED_STOP_PCT` stop);
  a DB row absent at the broker is a *phantom* and is closed — **v3.6: at its REAL fill,
  recovered from broker order history** (`match_closing_fills` — closing actions only, manual
  closes split across multiple orders are quantity-weighted, history reaches back to the
  phantom's entry date on restart). Only when no closing order exists (expiry, assignment)
  does it fall back to the flagged `$0.00` booking. Recovered P&L is written to the DB, so
  `DAILY_LOSS_LIMIT` gates on truth even for positions you closed by hand. Phantom Telegram
  alerts carry the recovered P&L. Paper never reconciles.

---

## Session windows

| Gate | Window |
|---|---|
| **Opening-range lockout** | **No entries for any strategy before 9:35 ET.** Universal floor at `can_enter`; opens at 9:35:00 sharp. |
| ORB | 9:35 – **11:00** ET (hard cutoff) |
| Trend Continuation | 9:35 – 14:00 ET (trending regime only; runaway-ORB handoff + standalone) |
| Iron Condor | 11:00 – 14:00 ET |
| Butterfly | 12:00 – 14:00 ET (requires GEX PINNING) |
| Sweep Reversal | 9:35 – 14:00 ET |
| Global entry cutoff | **14:00 ET** — past this the tape turns erratic on dealer hedging |
| Hard close | 15:45 ET, all positions |
| VIX > 20 | Blocks butterflies (halved size in the 15–20 zone) |
| VIX > 30 | Blocks all new entries |
| Fed day | **The bot trades Fed days.** `is_fed_day` only boosts ORB conviction. |

---

---

## Changelog

Big-ticket changes only — what was added, removed, or fundamentally altered. The
full per-file history is in the git log and in
[`docs/HISTORY.md`](docs/HISTORY.md).

**2026-07-28**
- **Confluence engine excavated** (`regime_confluence` v1.3). `_sweep`,
  `_breakout`, `_ranging` and `_compression` rebuilt as accumulating evidence
  instead of boolean gates with constant filler; trend wired into `_sweep`.
- **Condor strike selection replaced.** Short strike must now clear both
  0.80 × expected-move and the Bollinger band; liquid selection biased outward,
  no inside fallback. Replaced BB-anchoring, which had no minimum-distance floor.
- **Condor legs made independent.** Both triggers checked every tick; either side
  fires on its own conditions. Replaced sequential leg-1-then-leg-2 gating.
- **ORB liquidity veto removed.** A named pool in the target path now downgrades
  the entry (grade A→B, reduced size) as designed, instead of blocking it. The
  veto had been present since the initial commit.
- **Continuation pullback trigger rewired** from the BB midline to a 1-min wick
  tagging the nearest unfilled 5-min FVG.
- **Trade readiness** gained the arm-origin extension clock (v1.4) and a trend
  credit-spread track (v1.3, log-only).
- Documentation consolidated: 18 docs → 8; root README 1,392 → ~250 lines.

**2026-07-27**
- **Runaway ORB reroute** — a runaway now hands to continuation (with-trend on a
  pullback) instead of sweep reversal; post-runaway sweeps gated to named levels.
- **Sweep strike floor** — `SWEEP_DELTA_STRONG` 0.08 → 0.12 so high conviction
  stops buying unreachable far-OTM contracts.

**2026-07-24**
- **Trade-record observability** — `adx_at_entry`, `regime_conviction`,
  `flat_angle_deg`, `swept_level_name`, `level_strength` captured on every trade.
  See [`docs/MECHANICS.md`](docs/MECHANICS.md).

**2026-07-22 / 07-23**
- **Mark-limit execution** — orders post at the mark and never cross the spread,
  with a 15:40 flatten ladder escalating to a 15:45 market close.
- **Condor per-leg stop and roll** hardened; condor window moved behind a
  computable Bollinger.

**2026-07-21**
- **Regime engine live** — Layer-1 confluence scorer into a Layer-2 conviction
  integrator, replacing the single-shot classifier.

**2026-07-15 / 07-18**
- **Fill-confirmed exits and entries** — a close is only booked when the broker
  confirms; paper and live isolated in separate trade stores.
- **Trend Continuation** strategy added. **Signal journal** instrumentation added.

**2026-07-10 → 07-12**
- **Yahoo Finance purged**; one candle producer per box feeding many readers.
- **ORB made definitional** — stop rework, regime un-gate, and the retest model
  that the flagship still runs on.

## Security
Credentials live in the systemd environment only — never in source. `.gitignore` excludes
`credentials.py`, `*.pem`, `orb_range.json`, `orb_state.json`. `snapshot.sh` redacts secrets before
archiving.
