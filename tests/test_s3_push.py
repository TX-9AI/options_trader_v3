#!/usr/bin/env python3
# options_trader_v3/tests/test_s3_push.py — v1.0
"""
Behavioural proof for warehouse/s3_push.py against planted archives.

CHANGELOG
    v1.0 — 2026-08-12 — initial release, alongside s3_push v1.0.

No AWS, no moto: a stub client records every put and serves gets back, so the
verify path is exercised for real. Includes DELIBERATE-FAILURE cases — a stub
that corrupts on read, and one that rejects a put — because a verify step that
cannot be made to fail is not a verify step.
"""

import gzip
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

TMP = tempfile.mkdtemp(prefix="s3push_")
os.environ["OT_CHAIN_ROOT"] = os.path.join(TMP, "chain_snapshots")
os.environ["OT_WAREHOUSE_STATE"] = os.path.join(TMP, "state")

from warehouse import s3_push  # noqa: E402

s3_push.SRC_ROOT = os.environ["OT_CHAIN_ROOT"]
s3_push.LEDGER_PATH = os.path.join(os.environ["OT_WAREHOUSE_STATE"], "chain_ledger.json")

FAILS = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("" if cond else "  <- " + str(detail)))
    if not cond:
        FAILS.append(name)


class StubS3:
    """Records objects. mangle=True corrupts on read; reject=True refuses puts."""

    def __init__(self, mangle=False, reject=False):
        self.store = {}
        self.puts = 0
        self.mangle = mangle
        self.reject = reject

    def put_object(self, Bucket, Key, Body):
        if self.reject:
            raise RuntimeError("AccessDenied (simulated)")
        self.puts += 1
        self.store[Key] = Body
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def get_object(self, Bucket, Key):
        data = self.store[Key]
        if self.mangle:
            data = data + b"tamper"

        class _B:
            def read(self_inner):
                return data

        return {"Body": _B()}


def snap(ts_et, sym, n=3):
    return {
        "ts_et": ts_et,
        "symbol": sym,
        "event": "chain_snapshot",
        "expiry": "2026-08-12",
        "underlying": 431.25,
        "regime": "TRENDING_BULL",
        "n_calls": n,
        "n_puts": n,
        "contracts": [
            {"occ": "X%d" % i, "type": "C", "strike": 400 + i, "bid": 1.0, "ask": 1.1,
             "mark": 1.05, "delta": 0.5, "gamma": 0.01, "theta": -0.2, "vega": 0.03,
             "iv": 0.22, "oi": 10, "vol": 5}
            for i in range(n * 2)
        ],
    }


def write_archive(day, sym, records, partial_tail=False):
    d = os.path.join(os.environ["OT_CHAIN_ROOT"], day)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, sym + ".jsonl.gz")
    for r in records:
        with gzip.open(p, "ab") as f:
            f.write((json.dumps(r) + "\n").encode())
    if partial_tail:
        with gzip.open(p, "ab") as f:
            f.write(b'{"ts_et": "2026-08-12T14:5')  # no newline, mid-write
    return p


def reset():
    shutil.rmtree(os.environ["OT_CHAIN_ROOT"], ignore_errors=True)
    shutil.rmtree(os.environ["OT_WAREHOUSE_STATE"], ignore_errors=True)


print("\n=== s3_push v1.0 behavioural proof ===\n")

# 1 — a clean push of three snapshots
reset()
p = write_archive("2026-08-12", "SPX", [snap("2026-08-12T09:35:00-04:00", "SPX"),
                                        snap("2026-08-12T09:40:00-04:00", "SPX"),
                                        snap("2026-08-12T09:45:00-04:00", "SPX")])
s3 = StubS3()
led = {}
pushed, failed = s3_push.push_file(s3, "B", p, "2026-08-12", "SPX", led)
check("3 snapshots pushed", pushed == 3, pushed)
check("0 failed", failed == 0, failed)
check("ledger records 3 confirmed", led[p]["n"] == 3, led.get(p))
keys = sorted(s3.store)
check("hive dt= partition in key", all("/dt=2026-08-12/" in k for k in keys), keys[:1])
check("hive sym= partition in key", all("/sym=SPX/" in k for k in keys), keys[:1])
check("raw/ prefix", all(k.startswith("raw/chain_snapshots/") for k in keys), keys[:1])
body0 = json.loads(s3.store[keys[0]])
check("schema_version stamped", body0["schema_version"] == 1, body0.get("schema_version"))
check("gamma+vega survive the round trip",
      body0["record"]["contracts"][0]["gamma"] == 0.01
      and body0["record"]["contracts"][0]["vega"] == 0.03)
check("provenance carries host+line", "src_host" in body0 and body0["src_line"] == 0)

# 2 — resume: a second run over the same file pushes nothing
pushed2, _ = s3_push.push_file(s3, "B", p, "2026-08-12", "SPX", led)
check("re-run pushes 0 (ledger resume)", pushed2 == 0, pushed2)
check("no duplicate objects", len(s3.store) == 3, len(s3.store))

# 3 — append two more, only the new ones go
write_archive("2026-08-12", "SPX", [snap("2026-08-12T09:50:00-04:00", "SPX"),
                                    snap("2026-08-12T09:55:00-04:00", "SPX")])
pushed3, _ = s3_push.push_file(s3, "B", p, "2026-08-12", "SPX", led)
check("appended 2 -> pushed exactly 2", pushed3 == 2, pushed3)
check("5 objects total", len(s3.store) == 5, len(s3.store))

# 4 — idempotency: same content re-pushed lands on the SAME key
s3b = StubS3()
led_b = {}
s3_push.push_file(s3b, "B", p, "2026-08-12", "SPX", led_b)
first_keys = set(s3b.store)
led_b.clear()  # simulate a lost ledger -> full re-push
s3_push.push_file(s3b, "B", p, "2026-08-12", "SPX", led_b)
check("lost ledger re-push creates NO duplicates (content-hash key)",
      set(s3b.store) == first_keys and len(s3b.store) == 5, len(s3b.store))

# 5 — a partially written trailing line is not pushed, and does not advance
reset()
p2 = write_archive("2026-08-12", "QQQ", [snap("2026-08-12T10:00:00-04:00", "QQQ"),
                                         snap("2026-08-12T10:05:00-04:00", "QQQ")],
                   partial_tail=True)
s3c = StubS3()
led_c = {}
pushed4, _ = s3_push.push_file(s3c, "B", p2, "2026-08-12", "QQQ", led_c)
check("partial tail: only complete lines push", pushed4 == 2, pushed4)
check("offset stops at the complete lines", led_c[p2]["n"] == 2, led_c.get(p2))

# 6 — DELIBERATE FAILURE: read-back mismatch must NOT confirm
reset()
p3 = write_archive("2026-08-12", "MU", [snap("2026-08-12T11:00:00-04:00", "MU")])
s3d = StubS3(mangle=True)
led_d = {}
pushed5, failed5 = s3_push.push_file(s3d, "B", p3, "2026-08-12", "MU", led_d)
check("tampered read-back -> 0 confirmed", pushed5 == 0, pushed5)
check("tampered read-back -> counted as failed", failed5 == 1, failed5)
check("tampered read-back -> ledger NOT advanced", p3 not in led_d, led_d)
check("the PUT did happen (so this proves VERIFY caught it)", s3d.puts == 1, s3d.puts)

# 7 — DELIBERATE FAILURE: rejected put must not confirm, and must not raise
s3e = StubS3(reject=True)
led_e = {}
pushed6, failed6 = s3_push.push_file(s3e, "B", p3, "2026-08-12", "MU", led_e)
check("rejected put -> 0 confirmed, no exception", pushed6 == 0 and failed6 == 1)
check("rejected put -> ledger untouched", led_e == {}, led_e)

# 8 — retry after an outage resumes and confirms
s3f = StubS3()
pushed7, failed7 = s3_push.push_file(s3f, "B", p3, "2026-08-12", "MU", led_e)
check("retry after outage confirms", pushed7 == 1 and failed7 == 0, (pushed7, failed7))

# 9 — a shrunk file restarts rather than skipping
led_f = {p3: {"n": 99, "last_sha": "x", "last_key": "x", "confirmed_utc": "x"}}
s3g = StubS3()
pushed8, _ = s3_push.push_file(s3g, "B", p3, "2026-08-12", "MU", led_f)
check("stale offset past EOF -> restart from 0", pushed8 == 1, pushed8)

# 10 — idle box: discover finds nothing, main() is silent and returns 0
reset()
os.makedirs(os.environ["OT_CHAIN_ROOT"], exist_ok=True)
check("idle box discovers no files", s3_push.discover() == [], s3_push.discover())
rc = s3_push.main([])
check("idle box main() returns 0", rc == 0, rc)

# 11 — ledger survives a round trip to disk
led_g = {"/x": {"n": 4, "last_sha": "abc", "last_key": "k", "confirmed_utc": "t"}}
check("ledger saves", s3_push.save_ledger(led_g, s3_push.LEDGER_PATH))
check("ledger reloads identically", s3_push.load_ledger(s3_push.LEDGER_PATH) == led_g)

# 12 — never raises even when the source root is nonsense
s3_push.SRC_ROOT = "/nonexistent/nope"
check("missing root -> empty discover, no raise", s3_push.discover("/nonexistent/nope") == [])
check("main() with missing root returns 0", s3_push.main([]) == 0)

shutil.rmtree(TMP, ignore_errors=True)
print("\n" + ("ALL CHECKS PASSED" if not FAILS else "FAILURES: " + ", ".join(FAILS)))
sys.exit(1 if FAILS else 0)
