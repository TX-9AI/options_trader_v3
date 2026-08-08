#!/usr/bin/env python3
"""
tests/vwap_orientation_ledger.py — v1.3 — 2026-08-08

v1.3 — 2026-08-08 — THE EVENT FILTER, the fourth and last layer. v1.2 resolved
       all five fields correctly and the run STILL returned 419 undecidable and
       ZERO decidable. Cause: the event whitelist accepted only
       ("scored","fired","entry","entered") — names predating trade_readiness
       v1.5 — while the records carrying `readiness.market` are named
       `readiness`, `readiness_would_fire` and `readiness_staged_pick`. On
       2026-08-06 alone that is 11,584 records skipped before their VWAP side
       was read; the 419 survivors were `scored` rows with no market section.
       The data was never missing: BELOW 5,058 / ABOVE 3,912 that same day.
       Now PREFIX-matched on `readiness*` rather than enumerated — an exact list
       is precisely what kept this tool three versions behind its own emitter.
       ⚠️ THE LESSON, and it cost four versions: I patched the layer that had
       just failed, four times, instead of tracing the whole path once. Field
       names, then depth, then paths, then the filter. Each fix was correct and
       each was one layer short.

v1.2 — 2026-08-08 — PATHS VERIFIED AGAINST THE EMITTER. v1.1 made discovery
       path-aware, which was necessary but not sufficient: I then GUESSED the
       paths (`vwap.vwap`, `factors.dir`) and the tool found neither across
       39,344 records. Reading `trade_readiness._journal()` settles it — it
       emits ONE section, `readiness=`, holding `market` and `factors`, so
       everything is TWO levels deep: `readiness.market.vwap`,
       `readiness.market.price_vs_vwap`, `readiness.factors.dir`. The field
       NAMES in the standing note were right; the DEPTH was wrong, which is why
       two flat renames and one shallow path all missed.
       There is NO price field — `dist_pct` replaces it and is better, being
       comparable across symbols.
       ⚠️ THE TOOL EARNED ITS KEEP HERE: it printed "(NOT FOUND)" per field and
       REFUSED rather than producing an empty ledger. A silent zero-row report
       would have read as "no misorientation" instead of "wrong key".

v1.1 — 2026-08-07 — PATH-AWARE DISCOVERY. This tool exited rc=1 for two nights
       against a schema that had never landed, and the diagnosis "three field
       renames" was wrong. `_first_key` tested `n in rec` — TOP-LEVEL keys only
       — while the journal nests these under sections: `readiness.strategy` and
       `factors.dir`. **No flat rename could have reached them.** CAND entries
       may now be DOTTED PATHS and every accessor goes through `dig()`, so the
       next schema section costs one tuple entry instead of another dead tool.
       Also added `pnl_usd`, which is what the trades table actually calls it.
       ⚠️ trade_readiness v1.5 (2026-08-05) is what began emitting
       `{vwap, price_vs_vwap, dist_pct}` at all — before it, VWAP was computed
       every tick by volatility_engine and NEVER WRITTEN DOWN. So this tool can
       only see sessions from that bake forward; earlier journals have no VWAP
       to read and their absence is not a finding.

WHAT THIS ANSWERS
    Backlog item E proposes a VWAP_FILTER_ACTIVE HARD GATE across the scored
    strategies: short requires price <= VWAP, long requires price >= VWAP.
    This tool asks the only question that should decide it — per strategy, would
    that gate have blocked winners or losers?

WHY PER STRATEGY, NOT FLEET-WIDE
    VWAP alignment is a TREND-FOLLOWING filter. Sweep Reversal is a MEAN-
    REVERSION strategy: it enters counter to an extension by design, so a long
    after a downside sweep is very likely BELOW VWAP at entry. A global gate
    would veto that setup structurally, not occasionally. Continuation is the
    opposite case — alignment is exactly what it wants. One number cannot serve
    both, which is why the output is split by strategy x direction x alignment
    and never aggregated into a single verdict.

THE RULE THIS TOOL OBEYS  (design principle, 2026-07-30)
    Outcomes may FALSIFY, never FIT. This prints evidence that a factor looks
    correctly or incorrectly ORIENTED for a given strategy. It does NOT emit a
    weight, a threshold, or a suggested value, and nothing in the live path
    reads its output. A verdict's only permitted next step is a design review
    whose conclusion must be justifiable on MECHANISM — "this is a trend filter
    on a reversion strategy" — not on the P&L that flagged it.

SAMPLE DISCIPLINE
    Small samples produce spurious signs. Any cell below MIN_CELL is printed as
    INSUFFICIENT and never given a verdict. One good session is not evidence.

USAGE (control server)
    python3 tests/vwap_orientation_ledger.py 2026-07-29
    python3 tests/vwap_orientation_ledger.py 2026-07-27 2026-07-28 2026-07-29
    python3 tests/vwap_orientation_ledger.py --schema 2026-07-29   # discovery only

Read-only. stdlib only. Touches no database and no fleet.
"""

import glob
import json
import os
import sys
from collections import defaultdict

JOURNAL_ROOT = os.path.expanduser("~/day_trader_pro/signal_journal")
REPORTS_ROOT = os.path.expanduser("~/day_trader_pro/reports")
MIN_CELL = 12          # below this a cell gets no verdict, only a count

# Field-name candidates, most specific first. The journal and trade schemas have
# both drifted over the project's life, so this discovers rather than assumes —
# and prints what it found so a wrong guess is visible instead of silent.
# v1.1 — CANDIDATES MAY BE DOTTED PATHS. The real defect was never three wrong
# names: `_first_key` tested `n in rec`, i.e. TOP-LEVEL keys only, while the
# journal nests these under sections. `readiness.strategy` and `factors.dir` are
# where they actually live, and no flat rename could ever have reached them.
# Fixing the ACCESSOR rather than the names also means the next schema section
# costs one tuple entry instead of another dead tool.
CAND = {
    # v1.2 — VERIFIED AGAINST THE EMITTER, not guessed. `trade_readiness`
    # v1.5 `_journal()` emits ONE section, `readiness=`, containing
    # `market` (from `_market_snapshot`) and `factors` (from the scorer). So
    # everything is TWO levels deep. v1.1 guessed `vwap.vwap` and `factors.dir`
    # and found neither across 39,344 records — the field NAMES were right all
    # along, the DEPTH was wrong, which is why two flat renames and one shallow
    # path all missed.
    "vwap":      ("readiness.market.vwap", "vwap", "vwap_at_entry",
                  "session_vwap"),
    "rel":       ("readiness.market.price_vs_vwap", "price_vs_vwap",
                  "vwap_side", "price_vs_vwap_at_entry"),
    # NOTE: there is NO price field. `_market_snapshot` emits `dist_pct` —
    # signed % from VWAP — which is BETTER than a raw price here because it is
    # comparable across a $30 symbol and a $900 one. `aligned()` works from
    # `rel` alone, so price stays optional.
    "price":     ("readiness.market.dist_pct", "price", "underlying",
                  "underlying_price", "spot", "last"),
    "strategy":  ("readiness.strategy", "strategy", "setup", "strategy_name",
                  "setup_type"),
    "direction": ("readiness.factors.dir", "direction", "side", "bias", "dir"),
    "symbol":    ("symbol", "sym", "ticker", "instrument"),
    "event":     ("event", "kind", "type"),
    "pnl":       ("pnl", "pnl_usd", "realized_pnl", "profit", "pl", "net_pnl"),
}


def dig(rec, path):
    """Read a dotted path out of a nested record. None if any hop is missing.

    `rec.get("readiness.strategy")` returns None on a nested dict — silently,
    which is exactly how this tool exited rc=1 for two nights against a schema
    that had never landed flat.
    """
    if not path:
        return None
    cur = rec
    for hop in str(path).split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(hop)
        if cur is None:
            return None
    return cur


def _first_key(rec, names):
    for n in names:
        if dig(rec, n) is not None:
            return n
    return None


def discover(records, want):
    """Map logical field -> actual key, from real records."""
    found = {}
    for logical in want:
        for rec in records:
            k = _first_key(rec, CAND[logical])
            if k:
                found[logical] = k
                break
    return found


def load_journal(dates):
    recs = []
    for d in dates:
        for path in sorted(glob.glob(os.path.join(JOURNAL_ROOT, d, "*.jsonl"))):
            sym = os.path.basename(path).split(".")[0]
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:      # noqa: BLE001 — a half-flushed tail line
                        continue
                    r.setdefault("_sym", sym)
                    r.setdefault("_date", d)
                    recs.append(r)
    return recs


def load_trades(dates):
    out = []
    for d in dates:
        p = os.path.join(REPORTS_ROOT, f"fleet_trades_{d}.json")
        if not os.path.isfile(p):
            continue
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception as exc:           # noqa: BLE001
            print(f"  ! could not read {p}: {exc}")
            continue
        rows = data if isinstance(data, list) else (
            data.get("trades") or data.get("rows") or [])
        if isinstance(rows, dict):
            rows = list(rows.values())
        for r in rows:
            if isinstance(r, dict):
                r.setdefault("_date", d)
                out.append(r)
    return out


def aligned(rel, direction, vwap, price):
    """True when the E gate would PERMIT this entry.

    Gate as specified: long requires price >= VWAP, short requires price <= VWAP.
    Returns None when undecidable — notably price_vs_vwap == "NONE", the cash-index
    case from the 2026-07-17 zero-volume fix, where the gate is specified inert.
    """
    d = (direction or "").upper()
    is_long = d.startswith("L") or "BULL" in d or d == "CALL"
    is_short = d.startswith("S") or "BEAR" in d or d == "PUT"
    if not (is_long or is_short):
        return None
    if rel:
        r = str(rel).upper()
        if r in ("NONE", "", "UNKNOWN"):
            return None
        if r.startswith("ABOVE"):
            return True if is_long else False
        if r.startswith("BELOW"):
            return False if is_long else True
        return None
    try:
        if vwap in (None, 0) or price is None:
            return None
        return (price >= vwap) if is_long else (price <= vwap)
    except Exception:                      # noqa: BLE001
        return None


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    schema_only = "--schema" in argv
    if not args:
        print(__doc__.strip().split("USAGE")[1].strip())
        return 2

    jrecs = load_journal(args)
    trades = load_trades(args)
    print(f"dates: {', '.join(args)}")
    print(f"journal records: {len(jrecs)}   trade rows: {len(trades)}")
    if not jrecs:
        print("\nNo journal records found. Expected "
              f"{JOURNAL_ROOT}/<date>/<SYM>.jsonl — is the date harvested?")
        return 1

    jmap = discover(jrecs, ("vwap", "rel", "price", "strategy",
                            "direction", "symbol", "event"))
    tmap = discover(trades, ("strategy", "direction", "symbol", "pnl")) if trades else {}
    print("\n--- discovered journal fields ---")
    for k in ("event", "symbol", "strategy", "direction", "vwap", "rel", "price"):
        print(f"    {k:<10} -> {jmap.get(k) or '(NOT FOUND)'}")
    if trades:
        print("--- discovered trade fields ---")
        for k in ("symbol", "strategy", "direction", "pnl"):
            print(f"    {k:<10} -> {tmap.get(k) or '(NOT FOUND)'}")
    if schema_only:
        return 0

    missing = [k for k in ("rel", "direction") if k not in jmap]
    if missing and "vwap" not in jmap:
        print(f"\nCannot proceed: no VWAP-side field found ({missing}). "
              "Add the real key name to CAND at the top of this file.")
        return 1

    # ── outcomes keyed by (symbol, strategy, direction) ─────────────────────
    pnl_by = defaultdict(list)
    if trades and tmap.get("pnl"):
        for t in trades:
            key = (str(dig(t, tmap.get("symbol")) or "").upper(),
                   str(dig(t, tmap.get("strategy")) or "").upper(),
                   str(dig(t, tmap.get("direction")) or "").upper())
            try:
                pnl_by[key].append(float(dig(t, tmap["pnl"]) or 0.0))
            except Exception:              # noqa: BLE001
                pass

    # ── SIGNAL-level alignment, then TRADE-level P&L attributed ONCE ────────
    # v1.0 note: an early cut summed every matching trade into every matching
    # signal, inflating P&L by the signal count. Each trade is now counted once.
    # Journal rows carry no trade id, so a trade inherits the MAJORITY alignment
    # of its (symbol, strategy, direction) group — an approximation, and labelled
    # as one. It is sound for a per-strategy orientation read and NOT sound for
    # anything that needs per-trade precision.
    sig = defaultdict(lambda: {"aligned": 0, "misaligned": 0})
    undecidable = 0
    for r in jrecs:
        # v1.3 — THE EVENT FILTER WAS THE LAST LAYER, and it silently discarded
        # everything that matters. It accepted only ("scored","fired","entry",
        # "entered") — names from before `trade_readiness` v1.5 existed. The
        # journal's readiness events are `readiness`, `readiness_would_fire` and
        # `readiness_staged_pick`, and ONLY THOSE carry `readiness.market`. So
        # 11,584 records on 2026-08-06 were skipped before their VWAP side was
        # ever read, and the 419 that survived were `scored` rows, which have no
        # market section at all — hence "419 undecidable, zero decidable".
        # Prefix-matched rather than enumerated: `readiness_*` is a growing
        # family and an exact list is what put this tool three versions behind
        # its own emitter.
        _ev = str(dig(r, jmap["event"]) or "").lower() if jmap.get("event") else ""
        if _ev and not (_ev.startswith("readiness")
                        or _ev in ("scored", "fired", "entry", "entered")):
            continue
        strat = str(dig(r, jmap.get("strategy")) or "UNKNOWN").upper()
        direc = str(dig(r, jmap.get("direction")) or "").upper()
        ok = aligned(dig(r, jmap.get("rel")), direc,
                     dig(r, jmap.get("vwap")), dig(r, jmap.get("price")))
        if ok is None:
            undecidable += 1
            continue
        sig[(r.get("_sym", "").upper(), strat, direc)][
            "aligned" if ok else "misaligned"] += 1

    cells = defaultdict(lambda: {"n": 0, "trades": 0, "wins": 0, "pnl": 0.0})
    for key, counts in sig.items():
        _, strat, direc = key
        al = "ALIGNED" if counts["aligned"] >= counts["misaligned"] else "MISALIGNED"
        c = cells[(strat, direc, al)]
        c["n"] += counts["aligned"] + counts["misaligned"]
        for v in pnl_by.get(key, []):        # each trade consumed exactly once
            c["trades"] += 1
            c["pnl"] += v
            c["wins"] += 1 if v > 0 else 0

    print(f"\nundecidable (index/NONE side, gate inert by spec): {undecidable}")
    print("\n" + "=" * 74)
    print("  WOULD THE E GATE HAVE BLOCKED WINNERS OR LOSERS?  (per strategy)")
    print("=" * 74)
    print(f"  {'STRATEGY':<20}{'DIR':<6}{'ALIGNMENT':<12}"
          f"{'SIGNALS':>8}{'TRADES':>7}{'WINS':>6}{'P&L':>11}")
    for (strat, direc, al), c in sorted(cells.items()):
        print(f"  {strat:<20}{direc:<6}{al:<12}{c['n']:>8}{c['trades']:>7}"
              f"{c['wins']:>6}{c['pnl']:>11.2f}")
    print("  (trades inherit their group's majority alignment — approximate, "
          "sound for orientation, not for per-trade precision)")

    print("\n" + "-" * 74)
    print("  ORIENTATION READ  (falsification only — no weights suggested)")
    print("-" * 74)
    strategies = sorted({s for s, _, _ in cells})
    for strat in strategies:
        a = sum(c["n"] for (s, _, al), c in cells.items()
                if s == strat and al == "ALIGNED")
        m = sum(c["n"] for (s, _, al), c in cells.items()
                if s == strat and al == "MISALIGNED")
        apnl = sum(c["pnl"] for (s, _, al), c in cells.items()
                   if s == strat and al == "ALIGNED")
        mpnl = sum(c["pnl"] for (s, _, al), c in cells.items()
                   if s == strat and al == "MISALIGNED")
        tr = sum(c["trades"] for (s2, _, _), c in cells.items() if s2 == strat)
        if a + m < MIN_CELL or tr < 3:
            print(f"  {strat:<22} INSUFFICIENT ({a + m} signals, {tr} trades) "
                  f"— no verdict")
            continue
        if mpnl > 0 and mpnl >= apnl:
            print(f"  {strat:<22} GATE WOULD HAVE BLOCKED NET WINNERS "
                  f"(misaligned P&L {mpnl:+.2f} vs aligned {apnl:+.2f}) "
                  f"-> orientation looks WRONG for this strategy")
        elif mpnl < 0:
            print(f"  {strat:<22} gate would have blocked net losers "
                  f"(misaligned P&L {mpnl:+.2f}) -> orientation looks right")
        else:
            print(f"  {strat:<22} inconclusive "
                  f"(aligned {apnl:+.2f} / misaligned {mpnl:+.2f})")

    print("\n  Reminder: a verdict here licenses a DESIGN REVIEW, not a dial.")
    print("  Any change must be defensible on mechanism, not on this P&L.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
