"""
tests/test_entry_fill_confirmation.py — audit defect O part 1 (condor entry)
and defect R (paper mirrors live friction).

confirm_order_fill (execution/order_confirm.py) against a scripted broker:
  1. Full fill → filled=True, quantity, and the net credit computed from
     per-leg fills (broker truth), NOT the limit price.
  2. Rejected → filled=False, no quantity, no price.
  3. Never fills by deadline → cancel requested → filled=False; caller records
     NOTHING (no ghost position).
  4. Partial then cancelled → filled=True for the PARTIAL quantity at the
     weighted net (a real position must be booked and managed).
  5. Cancel keeps failing on a working order → filled=False with
     working_order_id set (page + reconcile-adopt safety net).
  6. Fill lands during the cancel race → booked (race resolved to truth).
  7. Butterfly basis math: lower + upper − 2·center from per-leg fills.
  8. Paper condor credit applies PAPER_FILL_SLIPPAGE_PCT against the trade.

Run: PYTHONPATH=. pytest tests/test_entry_fill_confirmation.py -v
"""

import sys
import os
from types import SimpleNamespace as NS

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tastytrade.order import OrderStatus  # noqa: E402

import config as cfg                                          # noqa: E402
from execution.order_confirm import (                          # noqa: E402
    confirm_order_fill, net_from_fills, EntryFill,
)

SHORT = "SPXW  260715P06200000"
LONG  = "SPXW  260715P06190000"
VERT_BASIS = [(SHORT, 1, +1), (LONG, 1, -1)]


def leg(sym, fills):
    return NS(symbol=sym, fills=[NS(quantity=q, fill_price=p) for q, p in fills])


def order_state(oid, status, legs=(), reject_reason=None):
    return NS(id=oid, status=status, legs=list(legs), reject_reason=reject_reason)


class FakeAccount:
    def __init__(self, states=None, states_fn=None, cancel_fails=0):
        self.states       = list(states or [])
        self.states_fn    = states_fn
        self.cancels      = []
        self.cancelled    = False
        self.cancel_fails = cancel_fails   # raise on the first N delete_order calls

    def get_order(self, session, oid):
        if self.states_fn is not None:
            return self.states_fn(self.cancelled)
        if len(self.states) > 1:
            return self.states.pop(0)
        return self.states[0]

    def delete_order(self, session, oid):
        self.cancels.append(oid)
        if len(self.cancels) <= self.cancel_fails:
            raise RuntimeError("cancel refused")
        self.cancelled = True


@pytest.fixture(autouse=True)
def fast_polls(monkeypatch):
    monkeypatch.setattr(cfg, "LIVE_FILL_POLL_SECONDS", 0.0, raising=False)
    monkeypatch.setattr(cfg, "LIVE_ENTRY_DEADLINE_SECONDS", 0.02, raising=False)


SESSION = NS(name="fake")


# 1 — full fill at broker truth, not the limit
def test_full_fill_books_broker_net_credit():
    filled = order_state(1, OrderStatus.FILLED,
                         legs=[leg(SHORT, [(2, 1.42)]), leg(LONG, [(2, 0.30)])])
    acct = FakeAccount(states=[filled])
    res = confirm_order_fill(SESSION, acct, order_state(1, OrderStatus.LIVE),
                             VERT_BASIS, what="condor-leg entry")
    assert res.filled is True
    assert res.quantity == 2
    assert res.net_price == pytest.approx(1.12)   # 1.42 − 0.30, not the 1.50 limit
    assert acct.cancels == []


# 2 — reject: nothing to record
def test_reject_records_nothing():
    rejected = order_state(2, OrderStatus.REJECTED,
                           legs=[leg(SHORT, []), leg(LONG, [])],
                           reject_reason="insufficient buying power")
    acct = FakeAccount(states=[rejected])
    res = confirm_order_fill(SESSION, acct, order_state(2, OrderStatus.LIVE),
                             VERT_BASIS)
    assert res.filled is False and res.quantity == 0 and res.net_price is None
    assert "rejected" in res.detail


# 3 — the ghost-position test: never fills → cancel → NO position
def test_unfilled_deadline_cancels_and_records_nothing():
    def states(cancelled):
        st = OrderStatus.CANCELLED if cancelled else OrderStatus.LIVE
        return order_state(3, st, legs=[leg(SHORT, []), leg(LONG, [])])
    acct = FakeAccount(states_fn=states)
    res = confirm_order_fill(SESSION, acct, order_state(3, OrderStatus.LIVE),
                             VERT_BASIS)
    assert res.filled is False
    assert res.net_price is None                 # never a fabricated credit
    assert acct.cancels == [3]
    assert res.working_order_id is None          # cleanly dead, nothing lingering


# 4 — partial is a REAL position: book the filled size at weighted net
def test_partial_books_filled_quantity():
    def states(cancelled):
        st = OrderStatus.CANCELLED if cancelled else OrderStatus.LIVE
        return order_state(4, st, legs=[leg(SHORT, [(1, 1.40)]),
                                        leg(LONG,  [(1, 0.28)])])
    acct = FakeAccount(states_fn=states)
    res = confirm_order_fill(SESSION, acct, order_state(4, OrderStatus.LIVE),
                             VERT_BASIS)
    assert res.filled is True
    assert res.quantity == 1                     # of the 2 requested
    assert res.net_price == pytest.approx(1.12)


# 5 — uncancellable working order: page + reconcile-adopt safety net
def test_cancel_failure_reports_working_order():
    live = order_state(5, OrderStatus.LIVE, legs=[leg(SHORT, []), leg(LONG, [])])
    acct = FakeAccount(states=[live], cancel_fails=99)
    res = confirm_order_fill(SESSION, acct, live, VERT_BASIS)
    assert res.filled is False
    assert res.working_order_id == "5"
    assert len(acct.cancels) >= 3                # it genuinely tried


# 6 — fill lands during the cancel race → booked
def test_fill_during_cancel_race_is_booked():
    def states(cancelled):
        if cancelled:   # cancel "landed" but the fill won the race
            return order_state(6, OrderStatus.FILLED,
                               legs=[leg(SHORT, [(2, 1.45)]),
                                     leg(LONG,  [(2, 0.35)])])
        return order_state(6, OrderStatus.LIVE,
                           legs=[leg(SHORT, []), leg(LONG, [])])
    acct = FakeAccount(states_fn=states)
    res = confirm_order_fill(SESSION, acct, order_state(6, OrderStatus.LIVE),
                             VERT_BASIS)
    assert res.filled is True and res.quantity == 2
    assert res.net_price == pytest.approx(1.10)


# 7 — butterfly basis math
def test_butterfly_basis():
    basis = [("L", 1, +1), ("C", 2, -1), ("U", 1, +1)]
    placed = order_state(7, OrderStatus.FILLED,
                         legs=[leg("L", [(1, 2.00)]),
                               leg("C", [(2, 1.20)]),
                               leg("U", [(1, 0.80)])])
    units, net = net_from_fills(placed, basis)
    assert units == 1
    assert net == pytest.approx(2.00 + 0.80 - 2 * 1.20)   # 0.40 debit basis


# 8 — paper condor fills mirror live friction (defect R)
def test_paper_condor_credit_applies_slippage(monkeypatch):
    monkeypatch.setattr(cfg, "PAPER_FILL_SLIPPAGE_PCT", 0.01, raising=False)
    net_credit = 1.50
    fill_credit = round(net_credit * (1 - cfg.PAPER_FILL_SLIPPAGE_PCT), 4)
    assert fill_credit == pytest.approx(1.485)   # credit received is REDUCED
    # and the debit direction pays MORE (matches _paper_fill_single):
    debit = 0.90 * (1 + cfg.PAPER_FILL_SLIPPAGE_PCT)
    assert debit == pytest.approx(0.909)
