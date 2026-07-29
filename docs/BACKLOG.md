# BACKLOG — work that needs doing

Everything we know needs attention: defects, evidenced findings, and deferred
fixes. One list, because they are all the same thing — **work that is not done.**

**Status motif** (kept from the old defect register):
`✅ RESOLVED` · `🔄 IN PROGRESS / MEASUREMENT SHIPPED` · `⚠️ OPEN` · `⬜ NOT STARTED`

Resolved items are **kept, not deleted** — they record why something is the way it
is, so a fix does not get quietly reverted later.

**Consolidated 2026-07-28** from `README.md`'s defect register (items A–AA) and
`docs/OBSERVATIONS.md`. Both are preserved verbatim below.

---

## PART 1 — Defect register (was: README.md § OPEN DEFECTS AND UNRESOLVED DECISIONS)

**This section is the scrub list. Everything here is known. Items marked ✅ RESOLVED
carry the resolution date and the fixing file versions; everything else remains open.**

### A. ✅ RESOLVED 2026-07-12 — Two Layer-1 implementations
There WERE two: `analysis/regime_confluence.py` and `conviction_integrator.EvidenceAdapter`,
both producing an evidence vector with divergent per-regime math — the circularity failure
`ROADMAP.md` §Risks names. **Resolved by `conviction_integrator.py` v2.0:** `EvidenceAdapter`
and its duplicated `ramp()`/`flat_angle_deg()`/`midline_crossings()` are **deleted**.
`RegimeConfluenceScorer` is the sole Layer 1; the integrator consumes its
`.evidence()` vector and imports the regime labels from it (guarded, with string fallbacks
for isolation).

### B. ✅ RESOLVED 2026-07-12 — Layer 2 ported in-repo (Phase 0.1 done)
`analysis/conviction_integrator.py` **v2.0** is in-tree with the v3 emission law: **always
argmax** — the `UNKNOWN` fallback is deleted from emission; indecision is a low conviction
number on a best-fit label, never a seventh label. The θ_hold/θ_commit/δ hysteresis band is
kept for label stability, and the **STALE/gap state survives** (data faults still block;
indecision does not). Priors untouched — they await tape calibration.
`regime_confluence.py` (v1.1: fixed a silent config-import failure that ran every constant
on fallbacks) now feeds both the Layer-1 replay AND the integrator's Layer-2 tracks in
`tests/replay_confluence.py` v2.0. **Still shadow-only:** no live-loop path touches either —
that is ROADMAP Phase 0.2, deliberately not yet wired.

### C. ✅ RESOLVED 2026-07-13 — `docs/REPLAY_VALIDATION.md` false premise
It justified replaying over the DXFeed CSVs on the claim that the shadow observer *"scores off
yfinance"* and was therefore a divergent feed. **The claim was false.** Read straight from the
now-extracted source: `shadow/observer.py` acquires data through exactly one call —
`get_cache(symbol)` → `data/data_cache.py` → `data/market_data.py` — and since the v3.0 purge
`market_data` reads the on-box shared SQLite store written by `candle_feed.py`
(TastyTrade/DXFeed), read-only, heartbeat-guarded. No yfinance in the repo; none in
`requirements.txt`. **The observer scores off the same DXFeed tape the CSVs are cut from.**

**Resolved by `REPLAY_VALIDATION.md` v1.1:** the conclusion stands, on a true premise. The reason
to calibrate on the CSVs is **sampling, not source** — the observer's jsonl is tick-cadenced and
staleness-gated (a frame may repeat across ticks, or serve `None` past the hard-stale ceiling),
while the CSVs are deterministic, evenly-spaced 1-min bars. Same tape, different sampling;
calibration needs the deterministic one. The identical false claim in
`tests/replay_confluence.py`'s header comment was corrected in the same pass.

### D. ✅ RESOLVED 2026-07-13 — Shadow observer extracted from its tarballs
`observer/shadow_ops_v1.0.tar` and `observer/shadow_subsystem_v1.0.tar` are **extracted and
deleted**; the `observer/` directory is gone. All 13 members landed and were diffed
byte-for-byte against the archives.

**Correction to this defect's own instruction.** It said *"extract to `observer/shadow/`"*. **That
was wrong** — the package belongs at **repo root `shadow/`**, and that is where it now lives.
Three independent reasons: `shadow-observer.service` runs `python -m shadow.observer`; the modules
import each other as `from shadow.primitives import ...`; and `observer.py` derives `REPO_ROOT` as
two levels up from itself, so nested under `observer/` its output would land in
`observer/data/shadow/`. Non-code members go to root (`shadow_devtools.sh`) and `deploy/`
(5 unit/timer files).

**Extraction immediately paid for itself:** with the code greppable, `observer.py`'s docstring was
found still describing a yfinance feed — the exact rot this defect predicted, and the thing that
made defect C's false premise plausible. Fixed in `observer.py` **v1.1** (docstring only, zero
code change).

**Two traps caught in the same pass:**
- `shadow_devtools.sh` uploaded through the GitHub web UI landed at mode `100644`. The browser
  uploader **cannot** set the exec bit — it writes every blob `100644`. `./shadow_devtools.sh`
  fails with permission denied until the mode is committed from a clone. **Anything executable must
  be pushed from a shell, never the web UI.**
- `.gitignore` had no `data/shadow/` rule (the archived copy did). Added — without it the
  observer's runtime jsonl shows as untracked on every box.

**⚠️ Half resolved 2026-07-18 — script fixed, service half still open.**
`shadow_devtools.sh` **v1.1** now self-locates (`REPO="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"`, mirroring `observer.py:61`) — it runs from any checkout,
including the control box's `~/options-trader-v3`. **Still open:**
`deploy/shadow-observer.service` hardcodes `WorkingDirectory`/`ExecStart` to
`/home/ubuntu/options-trader`. That matches the 29 boxes' canonical path — and the observer is now
**live on the QQQ paper box** (2026-07-18) at exactly that path, so the hardcode is correct for the
one box it runs on. Templatizing the unit (sed the path at install time, like `setup_ec2.sh` does
for `optionsbot.service`) remains the durable fix before any **non-standard-path** deployment.
Same class as the installer repo-pointer bug.

### E. `VWAP_FILTER_ACTIVE` — a hard gate that was never built
Marked `UNWIRED`. Genesis constant: present at the initial commit, never referenced, **mentioned
in zero changelog entries.** What exists is a *soft* score in `setup_scorer` (weight 0.15;
misaligned = 0.25 on that dimension). It **cannot veto anything**:

```
Short ORB · UNKNOWN regime · price ABOVE VWAP  (i.e. shorting into strength)
  regime_conviction  0.20 × 0.00 = 0.000
  orb_quality        0.30 × 1.00 = 0.300
  vwap_alignment     0.15 × 0.25 = 0.0375   ← the "filter"
  liquidity_clear    0.20 × 1.00 = 0.200
  macro_context      0.15 × 0.50 = 0.075
                                 = 0.6125  →  Grade B  →  FIRES
```

VWAP misalignment costs **11 points on a 100-point scale, against a 55 threshold.**
**`crypto_trader` learned the opposite lesson the hard way** — shorts above VWAP and longs below
VWAP had to become **hard blocks**, because a relaxed validator let shorts into a strong uptrend
and produced consecutive losses. **That lesson is not ported here.**

### F. `MIN_RRR` — a risk/reward floor that was never built
Marked `UNWIRED`. Same genesis story, same changelog silence. No RRR floor exists anywhere. The
ORB's RRR is *structural* (stop = impulsive origin, target = 100% of range width), so it varies
per setup and is currently **ungated**.

### G. 🔄 MEASUREMENT SHIPPED 2026-07-18 — the near-miss retest is now logged (not yet graded)
The removed grace band was *intended* to admit a "B-grade almost-retest" (the wick approaches the
range but doesn't enter). **The code never did that** — the same condition's first clause already
required the wick to enter, so the near-miss never fired. The defect prescribed: if it is worth
grading, **measure it, don't gate it.** Done as of `orb_engine` v3.7 — every armed 1-min candle
emits a `retest_check` event to `analysis/signal_journal` carrying the penetration depth in PX
(**negative = near-miss**, wick approached but never entered) plus `orb_width`, and the confirming
candle records `ORBData.retest_depth_px`. Depth is logged in PX and divided by tape ATR **offline**
(ATR-relative per this defect — never a percentage; percentages scale into holes on high-priced
instruments, the root cause of every tolerance bug this file has had). **Still open:** whether to
feed `retest_depth` into `orb_quality` at all — that decision belongs to the Phase-3 ROI buckets
once the depth distribution has accumulated. The measurement gates nothing today.

### H. ✅ RESOLVED 2026-07-13 — Two "no entry after" times in two files
`config.NO_ENTRY_AFTER_ET = (11, 0)` (ORB-only) vs `time_utils.NO_ENTRY = dtime(14, 0)`
**hardcoded**, so editing config could not move the global cutoff.

**Resolved by `config.py` v3.3 + `utils/time_utils.py` v3.1**, with the call sites renamed in
`main.py` v3.3, `analysis/orb_engine.py` v3.6, `strategy/sweep_reversal_strategy.py` v3.1:

| constant | value | scope |
|---|---|---|
| `ORB_NO_ENTRY_AFTER_ET` | `(11, 0)` | **ORB-scoped.** The ORB entry cutoff — *and* the arm condition for sweep reversal. |
| `GLOBAL_NO_ENTRY_ET` | `(14, 0)` | **Global.** No new 0DTE entries after 14:00, any strategy. `time_utils.NO_ENTRY` now reads it. |

**Not a behaviour change** — both cutoffs keep their exact prior values (asserted at runtime:
`NO_ENTRY == 14:00`, `ORB_NO_ENTRY_AFTER_ET == (11, 0)`).

**The trap this defect was hiding.** The obvious fix — point `time_utils.NO_ENTRY` at the existing
`NO_ENTRY_AFTER_ET` — would have **silently moved the global 0DTE cutoff from 14:00 to 11:00**,
because the two names describe *different rules*, not one rule written twice. The rename exists so
that can never be misread again. `orb_engine.py` is where it matters most: `past_orb_cutoff` uses
the 11:00 constant while `is_past_entry_cutoff()` (deciding EXPIRED vs re-arm) uses the 14:00 one —
two cutoffs, one file, previously near-indistinguishable by name.

### I. `session_guard.can_enter(is_butterfly=...)` is an inert branch
`main.py` never passes `is_butterfly=True`, so the butterfly-specific cutoff path is unreachable.
Config v3.1 set `BUTTERFLY_ENTRY_CUTOFF_ET = (14, 0)` so that config agrees with live behavior.
**If 15:00 is ever wanted, the call site must be fixed too.**

### J. The repo-wide v3.0 bump destroyed version legibility
Every file's title reads `v3.0` regardless of actual maturity, so version headers no longer carry
information. `check_versions.sh` can confirm a deploy landed; it can no longer tell you what is
*mature*.

### K. Re-arm: unresolved
`runaway` and `timeout` never re-arm. Note the v3.5 origin gate makes this partly redundant —
after a runaway, price is extended and **cannot produce a valid break candle** until it returns to
the range anyway. A unified rule (*"re-arm on any invalidation before 11:00; the origin gate
decides whether a break is real"*) would be simpler and could not fire an extended breakout.
**Counter-argument:** current behavior is a deliberate hand-off to Sweep Reversal. Unchanged
pending a decision.

### L. ✅ RESOLVED 2026-07-13 — `fix_structure_analyzer.sh` deleted
A dead one-off patching a `None`-format crash already fixed in-tree by `structure_analyzer.py`
v1.1 (2026-06-30). Nothing referenced it. **Deleted.**

### M. Known pending, not addressed
Ghost folder on Windows tarball extraction · `setup_ec2.bat` security warning on double-click ·
dedicated Telegram bot for options-trader notifications.

### N. ✅ RESOLVED 2026-07-15 — Exits booked on submission at fabricated prices
The 15:45 hard close booked ~8 condor legs at `pnl=+$0.00` (order *submission*
treated as a fill, price fell back to entry premium). Fixed by the FillResult
contract (exit_engine/position_manager v3.4) + live fill-confirmation
(exit_engine v3.5) + phantom P&L recovery and denser reconcile cadence
(main/broker_reconcile/trade_logger v3.6). See "Fill-confirmed exits" above
and `docs/AUDIT_paper_live_divergence_2026-07-15.md`.

### O. ✅ RESOLVED 2026-07-15 — LIVE ENTRIES book on submission, not on broker fill
All three entry paths now record ONLY broker-confirmed fills at the broker's
per-leg net price, sized to the CONFIRMED quantity, via
`execution/order_confirm.confirm_order_fill` (bounded by
`LIVE_ENTRY_DEADLINE_SECONDS`; unfilled → cancel and walk away; partial →
book the filled size; uncancellable → page + reconcile adopts).
**Condor legs** (main v3.7): signed-credit limit at mid; `notify_leg_filled()`
advances only on real fills. **Single legs** (entry_engine v3.7): MARKET, fill
price read back from fills — never the signal mark. **Butterfly**
(entry_engine v3.7): debit priced NEGATIVE (signed convention — the old
positive price could never fill); attempt 2 (mid + `LIMIT_IMPROVE_TICKS`)
placed ONLY after attempt 1 is confirmed dead with zero fills, closing the
double-position race; butterfly records now persist lower/center/upper leg
SYMBOLS (the v3.5 live close and reconcile both require them). Paper mirrors
live friction via `PAPER_FILL_SLIPPAGE_PCT` (env-tunable `OT_PAPER_SLIPPAGE_PCT`,
default 1% against the trade — defect R) and returns the requested quantity in
one pass. Tests 1–14: `tests/test_entry_fill_confirmation.py`. Original finding:
The entry-side twin of defect N, found in the 2026-07-15 paper→live audit —
**NOT yet fixed**. (a) Condor legs book `response.order.price or net_credit`
the instant the mid-credit LIMIT is accepted — a never-filled entry becomes a
managed ghost, and `notify_leg_filled()` advances the legging state machine on
it. (b) Single-leg MARKET entries book `placed.price or signal.entry_premium`;
a market order has no `.price`, so the recorded entry is ALWAYS the signal
mark, never the fill. (c) Butterfly entries are broken three ways: debit sent
as a POSITIVE price (the SDK's signed convention reads that as demanding a
CREDIT — can never fill); fill detection reads `status` immediately after
submission (always Received/Routed → place/cancel churn); a fill during the
retry sleep plus a swallowed cancel failure can open a DOUBLE position.
**Fix shape:** entry mirror of exit v3.5 (bounded poll, record only confirmed
per-leg net fills, signed limits). Until built, live entries are unvalidated
regardless of how good paper looks. Full detail:
`docs/AUDIT_paper_live_divergence_2026-07-15.md` §L1.

### P. ✅ RESOLVED 2026-07-15 — Broken-wing roll opens a FICTIONAL vertical in live
Fixed (condor_roll v3.7): the rolled vertical is now a REAL signed-credit
limit order, fill-confirmed via `execution/order_confirm` — the record books
only confirmed contracts at the broker's net credit. The close of the old
untested vertical books the ACTUAL `fill.fill_price` (both modes route through
`place_exit_order`; paper mirrors live friction on the rolled credit). If the
open fails after the close succeeded, position-truth is preserved, a
HALF-COMPLETE page fires, and the roll re-evaluates next tick. The risk-free
claim is re-checked against the ACTUAL fill credit and pages if it came in
light. Tests: `tests/test_roll_is_real.py`. Original finding:
`condor_roll._execute_roll` step 2 claims "live order placement mirrors
_execute_condor_leg" — **no order is placed**; the rolled vertical is written
to the DB only. Live: the real untested vertical closes (fill-confirmed),
then a position that never existed is booked and managed. Secondary: step 1
books the close at `plan.close_cost` instead of the confirmed
`fill.fill_price` it just received. **NOT yet fixed** — either place a real
signed-credit order with fill confirmation, or gate the roll to paper. Audit
§L2.

### Q. ✅ RESOLVED 2026-07-15 — One `trades.db`, no mode filter (mode isolation shipped)
Fixed by trade_logger v3.7 (every decision/session query — `get_open_trades`,
`realized_pnl_today`, session losses, expired autoclose — is scoped to the
current mode via `COALESCE(paper_trade,1)`; legacy NULL rows count as paper,
the safe direction) + configure.sh v2.0 (trades.db and WAL sidecars archived
as `trades_<mode>_<stamp>.db` on EVERY mode switch, so histories never share a
file to begin with). Tests: `tests/test_mode_isolation.py`. Original finding:
`realized_pnl_today()` (the DAILY_LOSS_LIMIT source of truth) and
`get_open_trades()`/`get_open_trades_live()` (startup recovery, position
manager) ignore the `paper_trade` column. Switching to live after weeks of
paper: paper P&L closed the same ET day gates the LIVE breaker, and any
still-open paper rows are handed to the live bot, which submits real close
orders for them until reconcile phantoms them — polluting live realized P&L
again. Only *instrument* changes wipe the DB (paper mode only); *mode* changes
wipe nothing. **NOT yet fixed** — mode-filter both queries + archive
`trades.db` on switching to LIVE in configure.sh. Audit §L3. **Do this one
first: smallest change, blocks day-one contamination.**

### R. ✅ RESOLVED 2026-07-15 — Paper fills are perfect (was `PAPER_FILL_SLIPPAGE_PCT = 0.0`)
**⚠️ PARTIALLY SUPERSEDED 2026-07-22 by the mark-limit policy:** single-leg and butterfly paper
entries now book the mark with **no** slippage markup (live posts a mark-limit and fills at the
mark or not at all, so a markup would make paper pessimistic on price while staying optimistic
on fill rate). The knob **still applies to condor paper credits** (`main.py` `_paper_fill`
path). This split is inconsistent — see defect T.
Original resolution: env-tunable (`OT_PAPER_SLIPPAGE_PCT`), default **1% against the trade**
(debits pay more, credits receive less), applied uniformly — condor legs
included, which previously ignored the knob. Set `0.0` for apples-to-apples
comparison with pre-change paper history. Original finding:
Paper enters and exits at the exact mid, both sides, every trade; live pays
spread crossing on entry and buys through the mark by
`LIVE_CLOSE_LIMIT_BUFFER` on exit. Paper P&L is therefore a structurally
optimistic estimate of live — materially so on wide SPX spreads. Consider
nonzero paper slippage so the next stretch of paper predicts live. Audit §M1.

### S. Offline replay is HTF-starved — the diary under-reports TRENDING by construction
The daily regime replay (`validate_regime.sh run_date` → `tests/replay_confluence.py`)
feeds the harness **one day-folder at a time**, so the 1h/1d timeframes never accumulate
enough bars to clear their EMA warmups: `trend_engine` returns NEUTRAL on the starved
timeframes and the vote dilutes — the exact mechanism behind the 0-TRENDING-in-34,925-ticks
finding (2026-07-16), *partially* addressed by trend v3.1's reweighting but structurally
present in every diary row scored on single-day tape. **Live boxes are unaffected**
(feed_store.db carries weeks of depth — why live trend detection works). Consequence:
diary baseline rows are trend-blind until fixed, and the Tier-B TRENDING acceptance row
cannot be honestly closed through the daily replay even once a real trend day is on tape.
**Fix = the BOOKMARK:** persist a rolling ~15-session window of **bars** per symbol
(bars, not engine state — the engines are stateless pure functions of the dataframes
passed in, so no serialization/drift risk), load+append+roll each EOD run, score today
with warm depth. Scores only ONE day per run (avoids the abandoned seed-builder's
per-bar full-stack slowness). Build and prove on the TESTER against copies of real
`ohlc/<date>/` folders **before** grafting onto `validate_regime.sh` — the EOD conductor
chain is finally flawless and stays untouched until the bookmark is proven inert.
Mitigation meanwhile: `regime_backfill --rebuild` re-scores all dated tape once the
bookmark lands, so no diary row is permanently lost — they are just wrong until rebuilt.

---

### T. ⚠️ NEW 2026-07-22 — Mark-limit change left the friction model split and the test suite red
Three loose ends from the limit-ladder pass, found in audit:
1. **The suite fails at HEAD.** `tests/test_entry_fill_confirmation.py::test_paper_entries_mirror_live_friction`
   still asserts the defect-R behavior (paper single fills at mark×1.01). `entry_engine` v3.8
   deliberately changed paper singles/butterflies to book the bare mark, and the test was not
   updated. 35/36 pass; deploy canaries that grep strings won't catch this.
2. **Inconsistent paper friction across strategies.** Condor paper credits are still haircut by
   `PAPER_FILL_SLIPPAGE_PCT` (`main.py`, `fill_credit = net_credit × (1 − pct)`) while
   singles/butterflies book the raw mark. Either apply the mark-limit rationale to condors too
   (live condor entries are already mid-credit limits) or document why condors keep the haircut.
3. **Dead import:** `position_manager.py` imports `PAPER_FILL_SLIPPAGE_PCT` and never uses it.

### U. ⚠️ NEW 2026-07-22 — Version-header discipline broke on the 07-17→07-22 passes

> **Update 2026-07-23 (full-repo header audit):** every title re-synced to its newest
> changelog entry (`main` v4.2, `exit_engine` v4.1, `config` v3.9 verified current;
> `trend_engine` v3.2, `market_data` v3.2, `trade_logger` v3.8, `structure_analyzer` v3.0
> titles added). Mis-numbered entries relabeled: `risk_manager` v1.4→**v3.2**,
> `butterfly_strategy` v1.4→**v3.2**, `status.py` duplicate v1.12→**v1.13**;
> `configure.sh` title v1.5→**v2.0**; `validate_regime.sh` v2.0→**v2.2** (retired
> `data/harvest` paths removed). Manifest re-synced. `check_versions.sh` v3.7 records the sweep.
The repo standard is "bump the header on every change." Violations found:
- `config.py` — header still **v3.3 (07-13)**; `FLATTEN_WINDOW_OPEN_ET` (07-22),
  `CONDOR_TRIGGER_APPROACH` (07-17), the RC env plumbing, and the v2.0 runner knobs all landed
  without a top-line bump (the changelog inside is also non-monotonic: v1.8/v2.0 entries sit
  under a v3.3 title).
- `execution/exit_engine.py` — the 07-22 mark-limit close rework is annotated **"v3.8"**,
  colliding with 07-15's v3.8 runner refinements. Two different change-sets share one version.
- `utils/time_utils.py` — header still **v3.1**; the 15:40 flatten-window change is only noted
  in body comments marked "v3.8".
- `strategy/iron_condor_strategy.py` — header still **v3.1 (07-12)**; the premium-rich
  band-approach trigger rework (07-17) was never bumped.
- `check_versions.sh` — **no canaries for anything after 07-18**: sweep v3.2 ORB-ownership,
  main v4.0 L2 wiring, regime_confluence v1.2 bounds, orb_engine v3.9 timeout,
  `limit_ladder.py`, `FLATTEN_WINDOW_OPEN_ET`, status v1.12. A stale sync of any 07-20→07-22
  file would pass the check today.

---

### V. ✅ RESOLVED 2026-07-22 — The ORB was scored, not gated (regime/VWAP/macro could veto a mechanical trade)
The ORB ran through the same 5-dimension weighted sum as every other strategy:
`regime_conviction` (0.20), `orb_quality` (0.30), `vwap_alignment` (0.15),
`liquidity_clear` (0.20), `macro_context` (0.15), graded against a 0.55 B-bar.
Three things were wrong, by the trade's own design:
1. **Regime leaked back in.** The ORB is deliberately NOT regime-gated at
   dispatch (it fires in every regime incl. UNKNOWN) — yet `regime_conviction`
   was 20%% of its grade. Ungated at dispatch, re-gated at the scorer.
2. **`orb_quality` measured nothing it claimed.** Its docstring said "break
   clarity, retest quality"; the code was `0.2 x confluence_count` minus a
   liquidity penalty. Geometry (break strength, retest depth) was never scored
   — it is validated upstream by the ORB state machine, so by the scorer a
   confirmed ORB carried a flat 2-factor base of 0.40.
3. **Liquidity could VETO.** An unnamed cluster in path subtracted enough from
   the weighted total to push a confirmed break under the B-bar and return
   `None` — no trade. Found live: SPX 2026-07-22 09:53, a confirmed ORB Long
   scored 0.4462 vs 0.55 and was REJECTED four ticks running.
The only dimension that actually varied per-setup was regime conviction, so the
A/B grade was regime conviction in costume — on a regime-agnostic trade.
**Resolved (`setup_scorer` v1.4):** the ORB short-circuits to `_grade_orb`
BEFORE the weighted machinery. A confirmed ORB ALWAYS trades; the ONLY grade
input is liquidity in the path to the 100%% TP — clear path = **A (1.5x)**, an
unswept pool between entry and target = **B (1.0x)**. Liquidity downgrades
A→B, never vetoes. Regime, VWAP, macro, confluence count, brief nudge and the
late-session modifier no longer touch the ORB grade (verified: a clear-path ORB
grades A even under UNKNOWN / conviction 0 / CRISIS VIX / VWAP-against). The
5-dimension path is byte-unchanged for sweep / condor / butterfly / default.
`_orb_quality` is deleted; `check_versions.sh` v3.2 pins `_grade_orb` and an
ABSENCE check on `_orb_quality`. **Live behaviour change:** ORB fire-rate rises
(today's four SPX rejects would all have traded), so the clean baseline stretch
resets to this deploy.

---

### X. ✅ RESOLVED 2026-07-23 — Condor legs round-tripped from ~+25% to −25% with no way to keep a gain
Forensic postmortem of 46 unique condor legs (07-07 → 07-22). **Every stopped
leg was GREEN FIRST** — median peak +24.2% (pre-fix) / +31.4% (post) using
`min_premium_seen`; essentially none were never-green. They reached ~+25%,
reversed, and hit the −25% stop. Cause: **nothing existed between entry and the
$0.05 nickel close** (≈96% decay). The condor was the only strategy with no
ratchet, while directional trades all have FVG trails. Meanwhile the stop sat
~2–3 ticks away (median credit $1.16 → stop $0.29) — 4× closer than the target.
**Resolved (`exit_engine` v4.1):** ratcheting stop — +20% → breakeven, +40% →
lock +20%, tightens only. Plus a **time-gated** take-profit at 25% that fires
ONLY after `CONDOR_ENTRY_CUTOFF_ET` and ONLY when the opposite side is not open
(`_condor_sibling_open`). The gating is load-bearing: **a take-profit before the
cutoff would structurally guarantee the condor never forms**, because the move
that makes side one profitable IS the move that carries price to the far band to
trigger side two. Backtest, 18 standalone legs: TP@25% turned −$242.77 into
−$8.43; on 28 condor legs a TP was WORSE at every level, confirming a condor leg
must never be closed on profit — the only reason to close one is the roll.
A ≥10-minute min-hold gates the TP as a quote-noise filter (a +25% mark move on
a nickel-wide 0DTE spread can be one tick). Also `risk_manager` v3.2 (relabeled from a mis-numbered v1.4): verticals
now sized at the **full** grade budget (18 of 46 legs never got a second side,
so half-sizing chronically under-sized a structure that never existed), and
`iron_condor` v3.2: leg 2 **pauses** on a non-RANGING tick instead of cancelling.

### Y. ✅ RESOLVED 2026-07-23 — Condor window opened before Bollinger was computable
`CONDOR_ENTRY_START_ET` was `(11, 0)`, but BB needs `BB_PERIOD`(20) 5-minute
bars — the first valid `bb_middle` is ~11:05 ET (verified on the 07-22 tape).
`decide()` falls back to `mid = current_price` when `bb_middle == 0`, so for the
first ten minutes of the window strikes and triggers were computed with **no
volatility reference at all**. Resolved: window opens **11:11**, clearing 11:05
with margin and removing the fallback path.

### Z. ⚠️ OPEN 2026-07-23 — `fleet_trades_<date>.json` contains trades from OTHER dates
The consolidated rollups are not date-clean. Deduping by `trade_id` collapsed
143 apparent condor legs to **46 unique**; **61%** sat in a file whose date did
not match their `entry_time`. `fleet_trades_2026-07-13.json` contains only
trades from 07-07 → 07-10 — nothing from 07-13. `fleet_trades_2026-07-15.json`
is truncated (2 KB, no condor legs) though that date's DB holds 41.
**Consequence:** any analysis bucketed by filename is wrong. Always dedupe by
`trade_id` and bucket by `entry_time[:10]`. Suspect `consolidate_trades.py` does
not filter by date, or the harvested box DBs were stale. Clean post-fix data
should come from the per-symbol `trades.db` on the boxes, pulled directly.
**Unfixed — day_trader_pro side.**

### AA. ⚠️ OPEN 2026-07-23 — Condor legs fired both sides one tick apart; mechanism unexplained
Every dual-sided condor from 07-07 → 07-17 opened both legs **15 seconds apart
at an identical `underlying_entry`** (IWM on four separate days, plus AVGO, JPM,
NFLX, TSLA, XOM, AAPL, PLTR). I hypothesised circularity — a trigger measured
against a strike that is itself placed relative to current price — but **reading
the code disproved it**: `_select_by_band` anchors strikes to `bb_upper`/
`bb_lower`, and the triggers anchor to `bb_middle`. The geometry is not
circular, and the trigger algebra says both sides cannot satisfy simultaneously
while `short_put < short_call`. **No validated explanation yet.** Note there are
ZERO two-sided condors after 07-17, so it is unknown whether this survived the
07-17 rich-trigger deploy — the post-fix sample is 7 legs. Entry logic was
deliberately left UNCHANGED in the v2 build rather than rewritten on a
disproven hypothesis. Defect Y removes one contributing hole (the
`current_price` fallback). Watch for recurrence in the six-day test.

---

---

## PART 2 — Evidenced findings and deferred fixes (was: docs/OBSERVATIONS.md)

Running log of things we've **noticed and understood but deliberately not fixed yet.**
The point of this file is continuity across work sessions: an observation captured
here survives even when the thread that found it is gone.

## Rules for this file
- **Nothing goes in without evidence.** Every entry cites the data (report, query,
  trade count, dates) that produced it. A hunch with no numbers is not an entry.
- **Every entry has a STATUS** (see legend). The status is the first thing you read.
- **Deferred means deferred.** An entry here is explicitly *not* a work item yet.
  When we decide to act, it moves to the ROADMAP / a build, and its status here
  becomes RESOLVED with a pointer to what was done.
- **Sample size is stated, always.** "n=7, one session" and "n=99, 8 sessions" are
  different confidence levels and must never read the same.
- Newest entries at the top. Date every observation and every update to it.

## Status legend
- `OBSERVING` — pattern seen, deliberately accumulating more data before any fix.
- `HYPOTHESIS` — a proposed cause, not yet confirmed across enough data.
- `CONFIRMED` — pattern holds across multiple sessions; cause understood; fix deferred to L3 / later.
- `WATCH` — minor or uncertain; noting it so it isn't lost, not actively studying it.
- `RESOLVED` — acted on; says what was done and where.

---

## 2026-07-24 (eve) — Sweep washout: what's the fingerprint? (three dead ends + one live lead)
**STATUS: HYPOTHESIS** (level-conviction lead is the strongest; capture shipped, awaiting data)

> **UPDATE 2026-07-24 (late) — TAPE/REGIME FINGERPRINT CONFIRMED-NEGATIVE.** The warm
> `--rebuild` backfill finished (ADX bookmark working — every day 07-14→07-24 now reads
> [DIRECTIONAL] not [CHOP], with real TREND dominance 26–39% that cold-start had hidden).
> With the engine's OWN logged flat-angle (trustworthy, not my miscalibrated
> reconstruction), the diary shows **the flat-angle does NOT separate good from washout
> sweep days**: 07-15 GOOD (6/8) had p90 **29.1°** — the HIGHEST — while washouts 07-22
> (0/2) and 07-24 (2/7) sat at 26.3° / 26.0°, i.e. slightly LOWER. All four cluster in a
> tight 26–29° band. 07-24 was also the MOST ranging recent day (RANG 30%) and still a
> washout. So directional character (trend / flat-angle / chop) is ruled OUT as the sweep
> discriminator — good and washout days look the same at the regime level. This
> STRENGTHENS the level-quality lead below: the difference must live somewhere the regime
> diary can't see — i.e. WHAT the sweep reached for, not what kind of day it was.

Tried to find what separated a GOOD sweep day (07-15: 6/8, +881) from a WASHOUT
(07-24: 2/7, −1687), same symbol AVGO, both current-engine. Measured off raw OHLC:

**Three intraday-structure metrics tried at n=1 — NONE separated the days cleanly:**
- **Open-side persistence** (% bars above/below the open): *looked* decisive (99% one
  side on washout vs 81% on good) — but it was a **net-move artifact**. VWAP killed it.
- **VWAP crossings**: pointed the OPPOSITE way (washout 32 vs good 25 — washout looked
  MORE mean-reverting). So "one-sided" was an illusion of the open anchor.
- **Two-axis chop score** (midline_crossings × flat_angle, the real regime_confluence
  fns): flat across both days. NB the reconstructed flat-angle was inflated (~28° med vs
  the engine's logged ~8° on AAPL) because ATR-14-on-1m ≠ the engine's ATR — so this
  score was built on a miscalibrated input and can't be trusted. **Read logged angle
  from replay jsonl, never reconstruct from candles.**
- The only real difference was **net move** (−0.11% vs −1.41%) — not tradeable (only
  known at close). The two days are **structurally similar** on every 25-bar-window
  metric available. Fingerprint is NOT in intraday window shape, at least not at n=1.

**THE LIVE LEAD — level conviction (Jason's hypothesis, the best one yet):**
The washout sweeps may have fired against **low-conviction levels (equal-highs/
equal-lows)** rather than **named pools (PDH/PDL/session)**. Mechanism: a named level
has real resting liquidity to fuel a reversal; an equal-H/L is self-defined with little
behind it, so price blows through and doesn't snap back. Partial corroboration:
`liquidity_mapper` had a bug (fixed v3.1, 07-14) where named-level detection saw
**0 of 1,367 evals** — so during 07-06 (a washout), named levels were INVISIBLE and
every sweep fired against equal-H/L by default. Exactly the hypothesis, mechanically
forced, for at least that day.

**Could NOT test it** — the swept-level type was computed at signal time and **not
persisted to the trade record** (notes empty, confluence_factors None). Same class of
gap as the ADX-not-logged issue.

**ACTION TAKEN (shipped, not deferred):** added `swept_level_name` + `level_strength`
(0..1: equal-H/L≈0.2, named PDL/PDH 0.6–1.0 scaled by touch_count) to OptionsSignal,
stamped in both sweep paths, and written to the trade record (schema + auto-migration).
Files: base_strategy, sweep_reversal_strategy, trade_logger, entry_engine (v-obs2).
**Starting Monday every sweep records what KIND of level it hit.** Then this becomes
directly answerable: do named-level sweeps win and equal-H/L sweeps lose? Value not
boolean, so a future sweep gate could threshold on level_strength.

**To close:** accumulate current-engine sweeps with level_strength logged; check
win-rate / expectancy by level_strength bucket. If equal-H/L sweeps are the losers,
the fix is a level_strength floor on the sweep gate (L3).

---

## 2026-07-24 (eve) — Sweep confirmation is real but the RECLAIM test is loose
**STATUS: HYPOTHESIS / watch** (candidate tightening identified; confirm against Monday
data before changing — do NOT fix now).

Answered "does the sweep wait for rejection confirmation, or anticipate it?" — it
**waits**, correctly. `sweep_reversal_strategy.py:125` hard-gates on `sweep.confirmed`;
`confirmed=True` is only set when `reclaimed and rejection_pct >= 0.002`
(`liquidity_mapper.py` ~430). The v1.3 fix already killed the old "penetration =
sweep" bug. So entry is confirmation-based, not anticipatory — the conservative,
correct design. Not front-running.

**BUT the reclaim test is weak** (`liquidity_mapper.py:425-426`):
`reclaimed = closes[i] <= pool.price or any(closes[k] <= pool.price for k in window)`
— satisfied by a **single close back inside the level anywhere in the rejection
window**. It does NOT require the reclaim to HOLD (the docstring says "close back inside
AND hold" but the code only checks that *at least one* close dipped back in).
`closes_beyond` (how many closes ACCEPTED through the level) is recorded but does NOT
gate confirmation. So a sweep can "confirm" on one close ticking back inside, then
continue straight through on the next candle — a **failed rejection dressed as a
confirmed one.** On a grind-through (washout) day this is exactly what produces the
−40% MAE / barely-green pattern: momentary dip inside → "confirmed" → continuation runs
it over.

**Compounds with the level-quality lead:** on a weak equal-H/L level, a one-close
reclaim is especially likely to be noise that doesn't hold — weak level + loose reclaim
stack.

**Candidate tightening (deferred, testable):** require `closes_beyond == 0` after the
reclaim, or require the reclaim to hold N candles, so a sweep only confirms if the
rejection actually STUCK. **Test first, don't just apply:** now that trades capture
level context, check whether losing sweeps have higher `closes_beyond` than winners once
Monday-forward data accumulates. If yes, tighten the reclaim; if not, leave it. This is
mapper logic (affects what fires) — tester-first when the time comes.

---

## 2026-07-24 (eve) — Level hierarchy + missing Overnight High/Low (NEXT BUILD)
**STATUS: HYPOTHESIS / action queued** (logic change — do tester-first, NOT folded
into the observability commit).

Two related gaps in `liquidity_mapper`:

1. **No Overnight High/Low.** The mapper identifies PDH/PDL + Asia/London/NY session
   H/L (8 named levels) + unnamed equal-H/L pools — but **no explicit overnight
   high/low.** ON H/L is one of the most-raided levels at the cash open; its absence
   means true ON raids either go untagged or match only an individual session extreme.
   Risk: real high-conviction ON raids are landing in the "equal-H/L / low-conviction"
   bucket by default, which would corrupt the very sweep-postmortem analysis we just
   instrumented. (ON H/L is derivable as the extremes across the Asia+London span, i.e.
   the pre-NY-open window — the session data is already collected.)

2. **Named levels are a flat `is_named` boolean — no hierarchy.** PDH and "Asia Low"
   currently carry identical weight. They should not.

**DESIRED LEVEL HIERARCHY (Jason, 2026-07-24), highest→lowest conviction:**
- **Overnight High/Low — dominant, or at least EQUIVALENT to PDH/PDL.** (top tier)
- **PDH / PDL** — top tier alongside ON H/L.
- **Historic S/R** — established prior support/resistance (multi-day). (mid tier)
- **Uniform / equal H/L** — self-defined equal-highs/lows. **LOWEST** conviction.

This replaces the flat `is_named` bool with a graded `level_strength` reflecting the
tier (value not boolean, consistent with the whole system). Session H/L (Asia/London/
NY individually) sit below ON H/L and PDH/PDL — they're components, not the headline.

**To close:** add `overnight_high`/`overnight_low` to LiquidityMap + `_add_named_pool`
as a named tier; replace flat is_named weighting with the tiered level_strength above;
prove inert on the TESTER first (mapper logic touches what sweeps can fire against —
that's trading behavior, not just logging, and the mapper's wall-clock bug history
demands caution). Then the level_strength already flowing to the trade record (shipped
this session) carries the *tiered* value and the postmortem buckets become meaningful.

---

## 2026-07-24 (eve) — Trade record was missing regime context at entry
> **Field reference: [docs/TRADE_RECORD_FIELDS.md](TRADE_RECORD_FIELDS.md)** — what each
> observability field means, how to query it, and known issues (the conviction
> scale is compressed/quantized — see the 2026-07-28 findings there).

**STATUS: RESOLVED.** The trades table never had an ADX field — ADX lived only in the
separate `regime_log` table, so every trade showed adx=0.0 (structural blank, not a
starvation bug). Fixed as observability: added `adx_at_entry`, `regime_conviction`,
`flat_angle_deg` to the trade record (schema + auto-migration + wired through all entry
paths). Live Monday-forward. **Historical trades still blank** — ADX-at-entry for past
trades must be reconstructed by timestamp-joining `regime_log` (offered; deferred).
NB: the trade record's ADX is only as warm as the classifier's — live is warm now (400-
bar store), replay warmed by the bookmark; the two fixes are what make this field real.

---
**STATUS: OBSERVING** (decision 2026-07-24: let the pattern stack across more days
before any fix — do NOT install a circuit breaker or change the strategy yet, as
that would contaminate the very pattern we're trying to see).

**Evidence (fleet_trades, 99 sweep trades across 8 sessions: 07-06,07,08,15,16,20,22,24):**
> ⚠️ **SAMPLE CAVEAT (added 2026-07-24 eve):** the pre-07-13 sessions
> (07-06/07/08 = 75 of these 99 trades) ran a **different trading engine** — different
> entries and exits, since-fixed bugs. Pooling them with the current engine
> (07-13 onward) compares two systems. The current-engine sweep sample is only
> ~24 trades (07-13→07-24), of which the washouts (07-22, 07-24) are most losses.
> Treat the 75%/n=99 numbers below as **mostly the OLD engine** — the current-engine
> pattern is far thinner and genuinely needs to stack. Candle tape also only exists
> from 07-13 (same engine boundary).
- Overall sweep win rate **75%** (74/99) but net **−$3,444**. Winning 3 of 4 and
  still losing money → payoff asymmetry: losers are much larger than winners.
- **Setup score does NOT discriminate.** Winner scores min/med/max 0.52/0.62/0.82;
  loser scores 0.56/0.68/0.83 — losers score *higher* if anything. Across n=99 the
  conviction score has no predictive power for sweep outcomes. Raising the sweep bar
  would only cut volume, not improve expectancy.
- Losses cluster on **washout days**: 07-06 went 0/5 (−$2,279), 07-22 0/2 (−$879),
  07-24 5 losers all `stop_hit` at −40% to −46% (−$1,687 net). A single washout day
  erases several good days (07-08 was 35/41 wins, +$982).
- Per-trade excursion (07-24): MFE ~+12% before dying to MAE ~−43% on the losers —
  they barely went green, then hit the wide stop. Winners trailed out ~+25% off a
  ~+60% MFE peak (giveback ~34%).

**Read:** entries are *good* (75% hit rate proves the setup fires on real reversals).
The problem is **risk/exit asymmetry** — stop is wide (~−40%+) while winners are
booked ~+25%, so a normal loss outweighs a normal win, and washout days hemorrhage.
This is an EXIT/SIZING problem, not an entry or conviction problem.

**Ruled out (with evidence):**
- NOT conviction — score is noise at n=99.
- NOT entry direction — LOW-sweeps are 83% lifetime (47 trades); 07-24's 2/6 LOW was
  an anomaly for that side, not the norm. Earlier "fading a trend" read was
  over-fit to one down day and is retracted.
- NOT a broken stop — stops fired correctly, capping each loss ~−42% as designed.

**What to watch as days accumulate (no action, just observe):**
- Does 75%-win / negative-net hold, or regress?
- **Washout-day fingerprint:** tag each 0-fer day with regime / ADX / VIX. Hypothesis
  to confirm or kill — washouts are strong-trend days where reversals get run over.
- LOW vs HIGH win-rate split vs the day's direction (trend-alignment signal).
- Whether score ever develops a discriminating threshold at larger n.

**When we act (deferred to L3):** first candidate is tightening the sweep stop toward
the winners' realized magnitude; second is a washout-day stand-down rule. Not before
the washout-day regime fingerprint is confirmed across more sessions.
