#!/usr/bin/env python3
# options_trader_v3/warehouse/s3_push.py — v1.0
"""
Box-side warehouse pusher — ships locally-written archives to S3.

CHANGELOG
    v1.0 — 2026-08-12 — initial release. Chain snapshots only; other streams
           (trades.db, signal journal, feed_store) land in later versions
           behind the same ledger + verify machinery.

WHY THIS EXISTS
    Option chains are NOT reconstructible after the session. A quote for a
    strike nobody selected is gone permanently at 16:00 — no vendor, no
    backfill, no replay recovers it. Today the only copy lives on the box that
    wrote it, and that box is STOPPED after the session. Because the morning
    selector picks movers, a box that traded today may not wake for weeks; its
    archive is unreachable that whole time and lost outright if the box is
    rebuilt. This module moves each snapshot to durable storage within one
    cadence interval of it being written.

DESIGN RULES
  1. NEVER raises. main() returns 0 unconditionally. A full disk, an expired
     credential, a truncated file, a network partition — all degrade to
     "pushed nothing this run", never to a traceback and never to a non-zero
     exit that would make a fleet fan-out discard the output of every box.
  2. NOT IN THE TRADING LOOP. Runs as its own systemd timer under system
     python. The bot's behaviour is byte-identical whether this module exists
     or not, and installing it requires no bot restart.
  3. STDLIB + boto3 ONLY. System python has boto3 1.40.72 fleet-wide; the bot
     venv does not, and this module must never need it. No pandas, no repo
     imports — it reads files, it does not import the writer.
  4. SILENT WHEN IDLE. On any given day ~14 boxes never trade and therefore
     have no chains at all. "Nothing to push" is the NORMAL state and prints
     nothing. An idle box that looks like a failure is how a real failure gets
     ignored (WORKING_AGREEMENT §17).
  5. CONFIRMED MEANS READ-BACK-AND-COMPARE. A 200 from PutObject proves bytes
     were accepted, not that the object is retrievable, parseable or equal to
     what we sent. Every object is re-read and byte-compared before the ledger
     records it. The ledger is what a future scrub will gate deletion on, so a
     false confirmation there is a data-loss bug, not a reporting bug.

KEY CONVENTION
    raw/chain_snapshots/dt=<YYYY-MM-DD>/sym=<SYM>/<epoch_ms>-<sha256[:16]>.json

    Hive-style dt=/sym= so Athena or Glue can discover partitions without a
    custom parser. The suffix is a CONTENT HASH rather than a uuid4: a uuid
    makes every retry write a duplicate object, while a content hash makes the
    push idempotent — a re-run after a crash mid-verify overwrites the same
    key with identical bytes instead of creating a second copy of one snapshot.
    Collision safety is unchanged (concurrent boxes write different symbols,
    and two identical snapshots ARE the same snapshot).

LEDGER
    ~/.vertigo_warehouse/chain_ledger.json, one entry per source file:
        {"<path>": {"n": <lines confirmed>, "last_sha": ..., "last_key": ...,
                    "confirmed_utc": ...}}
    Source files are append-only, so a confirmed line count is a valid resume
    point. Written atomically (tmp + os.replace) so a kill mid-write cannot
    leave a truncated ledger — which would silently re-push or, worse, look
    like more was confirmed than actually was.

    The ledger lives OUTSIDE the repo. Nothing this module writes lands in the
    working tree, so there is no scaffolding to remember to clean up.
"""

import gzip
import hashlib
import json
import os
import socket
import sys
from datetime import datetime, timezone

SCHEMA_VERSION = 1
DATATYPE = "chain_snapshot"

BUCKET = os.environ.get("OT_S3_BUCKET", "vertigo-warehouse-tx9ai")
REGION = os.environ.get("OT_S3_REGION", "us-east-2")
PREFIX = os.environ.get("OT_S3_PREFIX", "raw")
# Kill switch, house style: one env var per change, default ON.
ENABLED = os.environ.get("OT_S3_PUSH", "1") != "0"

_HOME = os.path.expanduser("~")
SRC_ROOT = os.environ.get(
    "OT_CHAIN_ROOT", os.path.join(_HOME, "options-trader", "data", "chain_snapshots")
)
STATE_DIR = os.environ.get("OT_WAREHOUSE_STATE", os.path.join(_HOME, ".vertigo_warehouse"))
LEDGER_PATH = os.path.join(STATE_DIR, "chain_ledger.json")

HOST = socket.gethostname()


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _epoch_ms(rec: dict, fallback_ms: int) -> int:
    """Snapshot time in epoch ms, from the record's own ET timestamp."""
    try:
        dt = datetime.fromisoformat(str(rec.get("ts_et", "")))
        if dt.tzinfo is None:
            return fallback_ms
        return int(dt.timestamp() * 1000)
    except Exception:
        return fallback_ms


def read_lines(path: str):
    """All COMPLETE lines from a multi-member gzip file.

    The bot appends to this file while we read it, so the final member may be
    partially written. gzip raises at that point; every line already yielded
    is intact, so we keep those and stop. The partial line is picked up on the
    next run once the writer has finished it.
    """
    out = []
    try:
        with gzip.open(path, "rb") as f:
            for raw in f:
                out.append(raw)
    except Exception:
        pass
    if out and not out[-1].endswith(b"\n"):
        out.pop()
    return out


def load_ledger(path: str = LEDGER_PATH) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_ledger(ledger: dict, path: str = LEDGER_PATH) -> bool:
    """Atomic write. A torn ledger is worse than no ledger: it can claim more
    lines confirmed than actually landed, and a future scrub keys on it."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(ledger, f, separators=(",", ":"))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        return True
    except Exception:
        return False


def envelope(rec: dict, sym: str, day: str, line_idx: int, src_file: str) -> bytes:
    """Wrap the raw snapshot with provenance and a schema version.

    The version is stamped per object, never inferred from the key, because
    journal shapes have already changed several times this month and a
    warehouse that cannot tell v1 rows from v3 rows pools incompatible data.
    """
    env = {
        "schema_version": SCHEMA_VERSION,
        "datatype": DATATYPE,
        "symbol": sym,
        "dt": day,
        "src_host": HOST,
        "src_file": src_file,
        "src_line": line_idx,
        "pushed_at_utc": _now_utc(),
        "record": rec,
    }
    return json.dumps(env, separators=(",", ":"), default=str).encode("utf-8")


def put_and_verify(s3, bucket: str, key: str, body: bytes) -> bool:
    """PUT then GET then byte-compare. Anything short of equality is False."""
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body)
    except Exception:
        return False
    try:
        got = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    except Exception:
        return False
    return got == body


def push_file(s3, bucket, path, day, sym, ledger):
    """Push every unconfirmed line of one source file. Returns (pushed, failed)."""
    lines = read_lines(path)
    entry = ledger.get(path) or {}
    start = int(entry.get("n", 0) or 0)
    if start > len(lines):
        # File shrank — a rotation, a rebuild, or a different file at the same
        # path. Resuming from a stale offset would skip real data, so restart.
        start = 0

    pushed = 0
    failed = 0
    mtime_ms = 0
    try:
        mtime_ms = int(os.path.getmtime(path) * 1000)
    except Exception:
        pass

    for idx in range(start, len(lines)):
        raw = lines[idx]
        try:
            rec = json.loads(raw)
        except Exception:
            # Not valid JSON yet. Stop here rather than skipping: skipping
            # would advance the offset past a line that never got pushed.
            break
        body = envelope(rec, sym, day, idx, os.path.basename(path))
        sha = _sha256(body)
        key = "{}/{}s/dt={}/sym={}/{}-{}.json".format(
            PREFIX, DATATYPE, day, sym, _epoch_ms(rec, mtime_ms), sha[:16]
        )
        if not put_and_verify(s3, bucket, key, body):
            failed += 1
            break  # stop this file; next run retries from the same offset
        ledger[path] = {
            "n": idx + 1,
            "last_sha": sha,
            "last_key": key,
            "confirmed_utc": _now_utc(),
        }
        pushed += 1
    return pushed, failed


def discover(root: str = SRC_ROOT):
    """(path, day, symbol) for every archive file on this box."""
    found = []
    try:
        for day in sorted(os.listdir(root)):
            day_dir = os.path.join(root, day)
            if not os.path.isdir(day_dir):
                continue
            for name in sorted(os.listdir(day_dir)):
                if not name.endswith(".jsonl.gz"):
                    continue
                sym = name[: -len(".jsonl.gz")]
                found.append((os.path.join(day_dir, name), day, sym))
    except Exception:
        pass
    return found


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    report = "--report" in argv

    try:
        if not ENABLED:
            if report:
                print("s3_push: DISABLED via OT_S3_PUSH=0")
            return 0

        files = discover()
        if not files and not report:
            return 0  # idle box, the normal case. Say nothing.

        import boto3  # imported late so a missing SDK cannot break --report

        s3 = boto3.client("s3", region_name=REGION)
        ledger = load_ledger()
        total_pushed = 0
        total_failed = 0

        for path, day, sym in files:
            p, f = push_file(s3, BUCKET, path, day, sym, ledger)
            total_pushed += p
            total_failed += f

        if total_pushed or total_failed:
            save_ledger(ledger)

        if total_pushed or total_failed or report:
            print(
                "s3_push host={} files={} pushed={} failed={} bucket={}".format(
                    HOST, len(files), total_pushed, total_failed, BUCKET
                )
            )
        return 0
    except Exception as exc:  # noqa: BLE001 — rule 1
        try:
            print("s3_push: run aborted, nothing confirmed: {}".format(exc))
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
