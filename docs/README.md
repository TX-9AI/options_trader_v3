# docs/ — index

Eight files, by function. Start here.

| file | read it when you want to know… |
|---|---|
| **MECHANICS.md** | How the bot decides, sizes, and exits. Regime definitions (L1), the readiness engine, the ORB model, every exit path, trade-record observability fields. |
| **BACKLOG.md** | What still needs doing. Defects, evidenced findings, deferred fixes — one list, with status (✅ / 🔄 / ⚠️ / ⬜). Resolved items are kept so fixes don't get reverted. |
| **ROADMAP.md** | What we're building and in what order. The L1→L3 campaign, the Trade Construction season, what's gated on what. |
| **FILE_MAP.md** | Every module, what it calls, what calls it. Generated from real imports. Use before changing anything with wide fan-in. |
| **WORKING_AGREEMENT.md** | How we work. Single-line commands, box topology, version/changelog discipline, prove-before-ship. |
| **VALIDATION.md** | How we validate. Replay/calibration against tape, and the offline backtest harness. |
| **HISTORY.md** | Why something is the way it is. Resolved incidents, audits, completed specs, superseded rollout notes — **read before re-litigating a fix.** |
| **WHITEPAPER_pitchfork_overlay.md** | The pitchfork overlay design (planned, gated on Layer 2). |

Consolidated 2026-07-28: 18 docs → 8, and the root README went 1,392 → 389 lines
with its historical and mechanical sections migrated here. Nothing was rewritten
or summarised — former content is preserved verbatim in sections, with
`<!-- was: … -->` provenance markers.

**Adding docs: don't create a new file.** Work outstanding → BACKLOG. Completed
work → HISTORY. Behaviour → MECHANICS. Plans → ROADMAP. The sprawl this replaced
grew one well-intentioned file at a time.
