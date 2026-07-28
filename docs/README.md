# docs/ — index

Seven files, by function. Start here.

| file | read it when you want to know… |
|---|---|
| **MECHANICS.md** | How the bot decides, sizes, and exits. Regime definitions (L1), every exit path, trade-record observability fields, ORB regime/stop models. |
| **ROADMAP.md** | What we're building and in what order. The L1→L3 campaign, the Trade Construction season, what's gated on what. |
| **OBSERVATIONS.md** | What we know is wrong but haven't fixed. Evidenced findings, deferred fixes, status legend. |
| **WORKING_AGREEMENT.md** | How we work. Operating rules — single-line commands, box topology, version/changelog discipline, prove-before-ship. |
| **VALIDATION.md** | How we validate. Replay/calibration against tape, and the offline backtest harness. |
| **HISTORY.md** | Why something is the way it is. Resolved incidents, audits, completed specs — **read before re-litigating a fix.** |
| **WHITEPAPER_pitchfork_overlay.md** | The pitchfork overlay design. |

Consolidated 2026-07-28 from 18 files into 7. Nothing was rewritten or summarised
— former files are preserved verbatim as sections, so historical decisions stay on
the record and fixes don't get quietly reverted. Provenance markers
(`<!-- was: docs/X.md -->`) mark each original.

**Adding docs: don't create a new file.** Findings → OBSERVATIONS. Completed work
→ HISTORY. Behaviour → MECHANICS. Plans → ROADMAP. The sprawl this replaced grew
one well-intentioned file at a time.
