"""UC2 - Disburse Approved Loan Application.

SUTs: Account Validation Service (CON.4 validation), Disbursement Adapter
(CON.4 posting). Named alt in I-11: CON.4 (validation OR posting/confirmation).
G5: the compensating action must actually happen (state changes / no disbursement),
not a bare 4xx.
"""
from nopbai import names as N

BASE = dict(
    customer_id="CUST-001",
    requested_amount_vnd=20_000_000,
    customer_age=30,
    is_existing_salaried=True,
    payment_account_id="ACC-001",
)


def _to_approved(client, auth, **overrides):
    r = client.post("/loan-applications", headers=auth, json={**BASE, **overrides})
    app_id = r.json()["application_id"]
    client.post(f"/loan-applications/{app_id}/agreement", headers=auth)
    return app_id


def test_T11_happy_disbursement(client, auth, platform):
    app_id = _to_approved(client, auth)
    r = client.post(f"/loan-applications/{app_id}/disbursement", headers=auth, json={})
    assert r.status_code == 200
    assert r.json()["state"] == N.DISBURSED
    assert r.json()["disbursement_reference"]
    # G5/CON.4: Core Banking Disbursement Record reference retained in Audit Log.
    events = [e.event for e in platform.audit_log.entries_for(app_id)]
    assert any(N.DISBURSEMENT_RECORD in e for e in events)


def test_T10_G6A04_con4_validation_failure_named_alt(client, auth, platform):
    # Mark the payment account ineligible -> validation fails -> no request sent.
    app_id = _to_approved(client, auth)
    platform.loan_application_service._apps[app_id].payment_account_eligible = False  # noqa: SLF001
    r = client.post(f"/loan-applications/{app_id}/disbursement", headers=auth, json={})
    assert r.status_code == 422                       # documented CON.4 validation status
    assert r.json()["detail"]["error_code"] == N.CON_4
    # Compensation actually happened: state Failed, application not Disbursed.
    assert platform.loan_application_service._apps[app_id].state == N.FAILED  # noqa: SLF001


def test_T12_G6A05_con4_posting_failure_named_alt(client, auth, platform):
    app_id = _to_approved(client, auth, customer_id="CUST-PF")
    r = client.post(
        f"/loan-applications/{app_id}/disbursement",
        headers=auth,
        json={"simulate_posting_failure": True},
    )
    assert r.status_code == 502                       # documented CON.4 posting status
    assert r.json()["detail"]["error_code"] == N.CON_4
    assert r.json()["detail"]["state"] == N.FAILED
    # Compensation: not marked Disbursed; reconciliation queued to Loan Ops Specialist.
    events = [e.event for e in platform.audit_log.entries_for(app_id)]
    assert any(N.LOAN_OPERATIONS_SPECIALIST in e for e in events)
    assert platform.loan_application_service._apps[app_id].state == N.FAILED  # noqa: SLF001
