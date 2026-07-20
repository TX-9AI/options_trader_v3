Both repos cloned, all 14 md docs read (ROADMAP v2.0, REGIME_TRUTHS v0.2, REPLAY_VALIDATION, README defect ledger, harness docs, DTP README), plus the integrator source for the actual priors. Answers:

**1) Will the remaining unknown chunk resolve into known buckets with lower scores?**

Yes — that's literally the designed end state, and it happens at two levels:

- **Layer 2 (already built):** conviction_integrator v2.0's emission law is always-argmax. UNKNOWN is deleted from emission; "indecision is a low conviction number on a best-fit label, never a seventh label." So once L2 is live-wired, every market tick gets exactly what you described: *this regime, weakly held*.
- **Layer 1 (the residual you're seeing):** the 13% all-zero residual was autopsied in REPLAY_VALIDATION §4, and the answer is encouraging — most of it is genuine ranges over-vetoed because FLAT_ANGLE_CUT_DEG=20° is too low (v1.3-labeled genuine RANGING has an angle p90 of 22.1°, so >10% of real ranges sit above your veto and get zeroed into silence). The L1.6 calibration sweep (16–26° against multi-day labeled tape) reclaims those into RANGING at a *graded* score via the flatness-depth soft-necessary ramp — exactly "it's RANGING, but not strongly characterized." Genuine regime transitions already score two regimes moderately by design, which L2 resolves.

Two deliberate exceptions never convert: the data-fault/STALE state and pre-open None (unobservable ≠ a regime). Those stay hard no-trade forever, and should. Also worth noting: the "unknown during most sessions" you see in the daily diaries is partly the offline HTF-starvation artifact (defect S / the L1.9 bookmark), not the live boxes' actual view.

**2) What gets calibrated at Layer 2 (L2.4)?**

The integrator's priors — every one of these is currently a guess awaiting your labeled tape:

- **θ_commit = 0.65** (conviction to emit a regime) and **θ_hold = 0.45** (conviction to keep it — the hysteresis band)
- **δ_displace = 0.12** (margin a challenger needs over the incumbent)
- **dt_max = 90s** and **τ_stale = 600s** (gap/staleness handling)
- **Per-regime τ_up / τ_dn0 / λ** (rise constant, decay floor, decay-resistance exponent): trending/breakout 40/25/2.2, sweep 25/15/1.5, compression 180/40/2.0, ranging 780/60/2.0

The template for how they get fit is already in the code comments: RANGING's τ_up=780 was chosen so commitment lands at ~17–19 bars — past the 12–15-bar impostor-flat window, inside the 24–29-bar genuine-range window. Those bar-count distributions are exactly what the labeled tape re-derives per regime. One sequencing caution on "2 weeks to freeze": the roadmap order is L2.4 calibrate → L2.5 wire shadow into the live loop → L2.6 freeze, and L2.4 is gated on Layer 1 Tier-B passing first (calibrating L2 on an uncalibrated L1 is circular). The tape you bank these two weeks serves both, but the freeze is the *last* step, not the first.

**3) Feedback on L2 tuning, and configurability after Layer 3?**

Feedback: yes, purpose-built. replay_confluence v2.0 emits an `l2` object per tick plus a Layer-2 report section — emitted distribution, **label-switches-vs-L1-flips (the churn metric)**, and stale%. That churn number is the direct measure of whether the integrator is doing its one job: stability without lag. The signal journal (v3.9) also logs conviction on every scored signal, so L2's downstream value shows up in the L3 ROI buckets later. Important boundary: L2 effectiveness is assessed on *label behavior* against labeled tape, never on trade P&L — the core invariant forbids outcomes feeding regime.

Configurability: mechanically, everything stays env-tunable — nothing hard-freezes. Architecturally, the answer is **epoch-frozen, not permanently frozen**. L3's conviction bars are placed against a specific frozen conviction distribution; L3.6 states it plainly — any L1 truth or L2 change "invalidates the conviction distribution beneath the bars" and forces a bar recalibration. So the ideal state isn't "L2 locked forever, only L3 tunes" — it's "L2 changes are allowed but expensive: touch L2, re-run the L3 campaign." Routine ongoing tuning lives at L3 (rolling monthly recalibration); L2 changes are deliberate epoch boundaries.

**4) Layer 3 calibration parameters:**

- **The gate matrix (L3.2):** the permissive-regime set per trade type, plus **bar(trade_type)** — the conviction floor each trade must clear. Provisional placeholders: ORB/sweep ~0.40, condor ~0.65, butterfly ~0.70.
- **Bar placement method (L3.3):** paper runs wide open at a ~0.20 fleet floor; fee-adjusted ROI bucketed by conviction decile per trade type; each bar placed at the lowest bucket whose *marginal* (not cumulative) expectancy ≥ 0; minimum ~40 trades/bucket. 3–6 week campaign.
- **Live descent schedule (L3.5):** starting offset (one bucket above the paper crossing), descent rate per review window, raise-back trigger on first negative read.
- **Recalibration cadence (L3.6):** monthly rolling window, or immediately after any L1 truth change.

Plus the L3.4 constraint that isn't a knob but governs all of them: fit sessions ≠ acceptance sessions, and slippage-haircut P&L only.

**5) The soundboard.**

It's less science fiction than you'd think — you've already built most of it without naming it. The sliders exist: essentially every parameter is env-tunable (30 OT_ vars in config alone, plus the regime PRIORs, integrator priors, and exit knobs). The feedback engines exist: signal journal, MFE/MAE excursion telemetry, the regime diary/replay harness, label_day.sh, and the backtest harness. And the per-slider optimization signal has already been demonstrated once, manually: the flat-angle-by-label distribution table is exactly a VU meter above the FLAT_ANGLE_CUT_DEG fader saying "you're set to 20, the data says slide toward 22+." REGIME_TRUTHS §4 is literally the soundboard's channel list — every knob with its calibration data source named.

So the buildable version, with what's in place today: an offline dashboard (a React artifact or nightly HTML report reading the banked JSONLs/CSVs) where each channel shows current value, its empirical distribution from labeled tape, and a suggested position. That's real and could exist within weeks of data accumulating.

The version to *not* build is motorized faders — a closed loop that moves sliders automatically. Your own architecture forbids it for good reasons: the circularity guard (fit set ≠ acceptance set), the frozen-baseline requirement, the strict calibration order (L1 before L2 before L3), minimum sample sizes, and the one-variable-at-a-time discipline behind the pitchfork twin. Twenty sliders self-adjusting simultaneously on live feedback would fit noise and destroy your ability to attribute anything. The right mental model: the board shows you where every fader *should* go; a human hand (or the scheduled L3.6 recal) moves them, one epoch at a time.
