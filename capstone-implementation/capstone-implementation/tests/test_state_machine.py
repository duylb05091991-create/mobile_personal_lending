"""G6-S coverage: every one of the twelve I-6 transitions, executed on the
Loan Application aggregate (SUT names are the I-4 owners in the use-case tests;
here we prove the type's transitions directly). Also proves terminal states and
illegal transitions are rejected (OOP: states are constrained, not free strings).
"""
import pytest

from nopbai import names as N
from nopbai.domain.errors import IllegalTransition
from nopbai.domain.loan_application import LoanApplication


def _app(**kw) -> LoanApplication:
    base = dict(
        customer_id="CUST-001",
        requested_amount_vnd=20_000_000,
        customer_age=30,
        is_existing_salaried=True,
        payment_account_id="ACC-001",
    )
    base.update(kw)
    return LoanApplication(**base)


# --- the twelve transitions (G6-S01 .. G6-S12) -------------------------------
def test_G6_S01_draft_to_submitted():           # T-01
    a = _app(); assert a.state == N.DRAFT
    a.to_submitted(); assert a.state == N.SUBMITTED


def test_G6_S02_submitted_to_scoring():         # T-02
    a = _app(); a.to_submitted(); a.to_scoring(); assert a.state == N.SCORING


def test_G6_S03_submitted_to_rejected_con2():   # T-03
    a = _app(); a.to_submitted(); a.reject_out_of_segment()
    assert a.state == N.REJECTED and a.is_terminal


def test_G6_S04_scoring_to_offerready():        # T-04
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready()
    assert a.state == N.OFFER_READY


def test_G6_S05_scoring_to_failed_con3():        # T-05
    a = _app(); a.to_submitted(); a.to_scoring(); a.fail_scoring()
    assert a.state == N.FAILED and a.is_terminal


def test_G6_S06_offerready_to_approved():        # T-06
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready(); a.approve()
    assert a.state == N.APPROVED


def test_G6_S07_offerready_to_rejected_con1():   # T-07
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready(); a.reject_policy()
    assert a.state == N.REJECTED and a.is_terminal


def test_G6_S08_offerready_to_rejected_decline(): # T-08
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready(); a.decline()
    assert a.state == N.REJECTED and a.is_terminal


def test_G6_S09_approved_to_accountvalidated():  # T-09
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready(); a.approve()
    a.to_account_validated(); assert a.state == N.ACCOUNT_VALIDATED


def test_G6_S10_approved_to_failed_con4():       # T-10
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready(); a.approve()
    a.fail_validation(); assert a.state == N.FAILED and a.is_terminal


def test_G6_S11_accountvalidated_to_disbursed(): # T-11
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready(); a.approve()
    a.to_account_validated(); a.to_disbursed()
    assert a.state == N.DISBURSED and a.is_terminal


def test_G6_S12_accountvalidated_to_failed_con4(): # T-12
    a = _app(); a.to_submitted(); a.to_scoring(); a.to_offer_ready(); a.approve()
    a.to_account_validated(); a.fail_posting()
    assert a.state == N.FAILED and a.is_terminal


# --- illegal transitions are rejected (constrained states) -------------------
def test_terminal_states_have_no_outgoing_transition():
    a = _app(); a.to_submitted(); a.reject_out_of_segment()
    for op in (a.to_scoring, a.approve, a.to_disbursed, a.to_account_validated):
        with pytest.raises(IllegalTransition):
            op()


def test_all_nine_states_are_exactly_i6():
    expected = {
        N.DRAFT, N.SUBMITTED, N.SCORING, N.OFFER_READY, N.APPROVED,
        N.ACCOUNT_VALIDATED, N.REJECTED, N.DISBURSED, N.FAILED,
    }
    assert len(expected) == 9
    assert N.TERMINAL_STATES == {N.REJECTED, N.DISBURSED, N.FAILED}
