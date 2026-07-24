# WORKING_AGREEMENT.md — how we operate (read this first, every new thread)

This file is operating discipline for the assistant across threads. None of it is
about the trading system's *logic* (that's OBSERVATIONS.md / ROADMAP.md) — it's
about **how work gets done here without repeating mistakes that have each cost
multiple sessions.** Every rule below was learned the painful way.

New thread? Read this file before touching anything.

---

## 1. Commands must be SINGLE-LINE. No exceptions.
The user runs commands on mobile (Termius) through the fleet **service-menu
fan-out**, not direct SSH. Multi-line anything gets **truncated and butchered**
before it runs.
- **NO** heredocs (`<<'EOF'`), **NO** multi-line `python3 -c` blocks, **NO** line
  continuations, **NO** pasted scripts. One line, always.
- If logic needs more than one line, write it as a file, have the user download/stage
  it, and run it as `python3 script.py` — do not inline it.

## 2. Quoting must survive the menu's SSH wrapping.
The menu wraps the command and ships it over SSH, adding **an extra shell-quoting
layer** vs. a direct prompt. Nested quotes collide with that wrapping.
- Keep to **one consistent nesting level**. When a command needs both quote types
  (e.g. a `sqlite3 "SELECT ... '2026-07-24' ..."`), structure it so the menu's extra
  layer doesn't collide — and never go three deep.
- Give **menu-ready** commands, not direct-shell commands.

## 3. Know which box you're on. The paths differ — this bit us repeatedly.
- **Bot / fleet boxes:** the running bot's working directory is **`~/options-trader`**
  (NO suffix). Per-box `trades.db`, the live process, and per-box data live here.
  Fleet commands run via the menu fan-out (option 14) and execute in this dir.
- **Control / reporter box** (`ip-...-32-218`): has TWO relevant dirs —
  **`~/options-trader-v3`** = the clone of the GitHub repo (repo name is
  `options-trader-v3`), and **`~/day_trader_pro`** = the reporter + devtools service
  menu (`./dev*`), the replay harness, the diary, `reports/`, `fleet_trades_<date>.json`.
  The control box has NO running-bot `trades.db` of its own.
- **The trap:** `~/options-trader` exists on **bot boxes**, NOT on the control box.
  Sending `cd ~/options-trader` while the user is on the *control* box fails (this
  happened, repeatedly). Always resolve the path to the box the user is actually on:
  bot box → `~/options-trader`; control box → `~/options-trader-v3` (repo) or
  `~/day_trader_pro` (tooling).

## 4. Landed files go to /home/ubuntu, then get moved/extracted.
When the user uploads files to a box — TAR archives or loose files — assume they land
in **`/home/ubuntu/`**. We extract (TAR) or move (loose files) into the repo with
commands **before staging and committing**. This worked well when both sides assumed
the same thing; assume it by default.

## 5. Version-control & housekeeping discipline is NOT optional.
Stale headers, banners, and changelogs bit us repeatedly (a banner reading v3.5 while
the code was v3.7; two divergent `candle_feed.py` lineages). Every file the assistant
edits:
- **Bump the header/version** and add a **dated changelog line saying what changed.**
- **Update the banner/log-version string** if the file logs one, so it matches the header.
- Never leave a changelog describing behavior the code no longer has.
- If a doc references the changed code (README file-structure tables, etc.), update the
  reference in the same edit so the repo never self-contradicts.

## 6. Verify the deploy landed BEFORE restarting. Every time.
Pushes have silently failed or been clobbered more than once (a fix landing three
times and vanishing; parallel edits overwriting each other). The gate:
- After `git fetch && git reset --hard origin/main`, echo a **version + marker check**
  (`echo "v=$(grep ...) marker=$(grep -c ...)"`) and confirm the expected values
  **before** `systemctl restart`.
- Never restart on an unverified/unexpected version string. If it's wrong, the push
  didn't land — fix the push, don't restart.

## 7. One owner per file.
Two agents (assistant + Fable) editing the same file through the repo with no merge
created divergent lineages that cost days.
- The assistant **retains ownership of a file until it proves unable** to accomplish
  the task; only then does it go to Fable, via a tight spec.
- When editing a file another agent owns (e.g. Fable's `entry_engine.py`,
  `order_confirm.py`), **build from repo HEAD in that file's existing idiom** — do not
  create a second lineage. Preserve its conventions (signed-price, confirm machinery, etc.).

## 8. Clone HEAD and READ before editing. Memory is not evidence.
The assistant burned turns "fixing" code from a stale mental model, and had to be
stopped. Hard rule:
- Every edit starts with a **fresh clone** and **reading the actual current file.**
- Any question about repo state ("did this land?", "what's uncommitted?") gets a
  **clone-and-grep**, never a recollection. (Answered one such question from memory and
  was wrong — said the Fable spec was missing when it was the replay bookmark.)

## 9. Prove it in the sandbox before presenting.
Fixes that stuck were run against real data / a real repro first. Fixes asserted from
reasoning embarrassed us.
- Standard = **compiles + behavioral proof against real rows/tape**, shown, before the
  file is presented. "This should work" is not proof.

## 10. Live vs. replay vs. paper is a real distinction — always name it.
We nearly fixed *production* for what were **replay-only** artifacts (ADX cold-start
until 14:00 was the replay's single-day resample, not live), and nearly trusted
**paper** numbers that were optimistic vs. live ($0.00 hard-close fills; entry-only
slippage). Before diagnosing anything, ask: **is this the live path, the replay/diary
path, or the paper fill model?** They fail differently and get fixed differently.

## 11. Check the user's prior — don't just confirm it.
Twice the user held a strong belief and the valuable move was to **test it against
data**: once it confirmed (live regime_log proved ADX warm at the open), once it
retracted a wrong read (sweeps "fading a trend" was over-fit to one day; LOW-sweeps are
83% lifetime). Agreement is cheap; a checked answer is the job.

## 12. Thin samples find mechanisms, not conclusions.
n=7 (one session) tells you **what to look at**; n=99 (many sessions) tells you **what's
true.** No dial moves on one session. When the user says "understand it, don't fix it
yet," that is the correct discipline — capture it in OBSERVATIONS.md and let it stack.

---

## 13. The control box already has a devtools SERVICE MENU. Use it before building.
On the control box (`~/day_trader_pro`, run `./dev*`), the **devtools service menu**
(v1.22 as of 2026-07-24) already exposes most of what we reach for. Before writing a
query or script, check whether a menu option does it. Reference (numbers may drift —
re-read the menu if unsure):

- **Orchestration:** 1 full spool-up (mock) · 2 EOD aggregate (mock) · 3 reset mock ·
  4 dry-run spool-up (real reads) · 5 dry-run EOD aggregate (real reads)
- **Registry & master switch:** 6 instance map · 7 reconcile map · 8 swap/pin instance
  ID · 9 control status · 10 ENABLE control · 11 DISABLE control
- **Fleet (inspect & fan-out):** 12 fleet list · 13 fleet ping ·
  **14 Run command (all running)** ← the fan-out we use for fleet commands ·
  15 status.py+query.py (one/all/some) · **16 Pull trades.db (one/all/some)** ·
  17 Pull OHLC for a day (one/all/some)
- **Debug/logs (remote):** 18 service status (bot+candle-feed) · 19 journal tail ·
  20 feed health (store freshness) · 21 bot log tail
- **Maintenance (wake_and_bake):** 22 dry-run · 23 FULL (wake→bake→restart→STOP) ·
  24 wake · 25 bake only (sync, no restart — RTH-safe) · 26 leave on · 27 EMERGENCY STOP
- **Repoint (migrate fleet→new repo):** 28 check · 29 full · 30 full+wake · 31 no
  restart · 32 scoped · 33 mock preview
- **Snapshot & tests:** 34 snapshot dir→repo-ready tarball · 35 test selection (mock) ·
  36 test Telegram
- **Control repo ↔ GitHub (force sync):** **37 PUSH→GitHub (this server = source of
  truth)** · **38 PULL←GitHub (GitHub = source of truth)**
- **Trades data:** **39 re-run consolidation→`fleet_trades_<date>.json`(+.csv)** ·
  **40 excursion report (MFE/MAE)→`reports/excursions_<date>.txt`** ·
  **41 trade breakdown (cross-day: regime/strategy/grade + regime×strategy)**
- **Regime validation (L1 confluence, tape-only):** 42 run replay today · 43 replay a
  date · 44 view a day's report · **45 view the diary (all days)** · 46 backfill missing
  days · 47 A2 co-occurrence + HTF drift (auto-finds replay logs)
- **EOD/backfill/live P&L:** **48 live P&L standings (read-only)** · 49 backfill missing
  OHLC · 50 EOD conductor (dry-run→confirm→run)
- **Utilities:** 51 OHLC 21-day fetch (yfinance) · 52 rotate fleet tokens/secrets ·
  53 audit fleet credentials (read-only) · 54 verify fleet credentials WORK (TT SDK,
  Telegram, GitHub)

**Rule:** if the user needs trades pulled, a report, a replay, live P&L, or a deploy —
a menu option almost certainly exists. Point them at the number instead of writing a
one-off. The excursion/breakdown/diary reports (40/41/45) are already the analysis
surface we keep re-deriving by hand.

## 14. Data lives in SEPARATE folders — candles, trades, reports.
On the control box the data is split by kind, not co-mingled:
- **candles / OHLC** — its own folder (the replay/backfill tape; `data/OHLC/<date>/…`).
- **trades** — its own folder (`fleet_trades_<date>.json` / `.csv`, per-day consolidated).
- **reports** — its own folder (`reports/excursions_<date>.txt`,
  `reports/regime_replay_<date>.jsonl`, the diary, etc.).
When looking for a file, go to the folder for its *kind*; don't assume everything sits
together. (This is why "which file / which folder" questions get a `ls` of the right
subfolder, not a guess.)

---

### Companion files
- **OBSERVATIONS.md** — evidenced findings about the *system*, deferred fixes.
- **ROADMAP.md** — the L1→L2→L3 build plan and where each piece stands.
- **README.md** — architecture + defect log.
