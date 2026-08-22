"""Hard rules impossible (capstone.md).

A test must ATTEMPT the violation and the runtime must REJECT it (assert on the
rejection). Covers the I-5 hard rules and the I-9 forbidden path on this slice.
We do NOT build the rest of the landscape to prove them.
"""
import pytest

from nopbai import names as N
from nopbai.domain.errors import ForbiddenPathError, IllegalTransition
from nopbai.domain.loan_application import LoanApplication

BASE = dict(
    customer_id="CUST-001",
    requested_amount_vnd=20_000_000,
    customer_age=30,
    is_existing_salaried=True,
    payment_account_id="ACC-001",
)


# --- I-5: "No approval before eligibility, scoring, policy, amount calc" -------
def test_I5_cannot_approve_before_scoring():
    a = LoanApplication(**BASE)
    a.to_submitted()
    with pytest.raises(IllegalTransition):
        a.approve()  # OfferReady is required; Submitted -> Approved is illegal


# --- I-5: "No disbursement/posting before approval and account validation" -----
def test_I5_cannot_disburse_before_approval(client, auth, platform):
    r = client.post("/loan-applications", headers=auth, json=BASE)
    app_id = r.json()["application_id"]  # state OfferReady, not yet Approved
    with pytest.raises(IllegalTransition):
        platform.loan_application_service.disburse(app_id)  # skip agreement -> rejected


# --- I-9 forbidden path: Mobile App must not write directly to Core Banking ----
def test_I9_mobile_app_has_no_core_banking_or_scoring_handle(platform):
    # Structural guarantee: Mobile App only collaborates with Loan Application Service.
    collaborators = vars(platform.mobile_app)
    assert set(collaborators) == {"_las"}
    for forbidden in ("core_banking", "credit_scoring_system", "esb", "_esb"):
        assert forbidden not in collaborators


def test_I9_direct_mobile_app_to_core_banking_is_rejected(client):
    # Attempt the forbidden write directly; runtime rejects with 403.
    r = client.post(
        "/backing/core-banking/postings",
        headers={"X-Caller": N.MOBILE_APP},
        json={"application_id": "LA-x", "amount_vnd": 10_000_000, "disbursement_reference": "r"},
    )
    assert r.status_code == 403
    assert r.json()["detail"]["error_code"] in (N.CON_4, N.CON_5)


def test_I9_mobile_app_cannot_perform_credit_evaluation(client):
    # Mobile App performing credit evaluation is the forbidden path; rejected 403.
    r = client.post(
        "/backing/credit-scoring-system/scores",
        headers={"X-Caller": N.MOBILE_APP},
        json={"customer_id": "CUST-001"},
    )
    assert r.status_code == 403


def test_I9_core_banking_fake_rejects_non_esb_caller(platform):
    with pytest.raises(ForbiddenPathError):
        platform.core_banking.post_disbursement_and_accounting(
            "LA-x", 10_000_000, "r", caller=N.DISBURSEMENT_ADAPTER  # must go via ESB
        )
