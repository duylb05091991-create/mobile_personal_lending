"""UC1 - Submit and Decide Loan Application.

SUTs: Mobile App (submit), Loan Application Service (segment/lifecycle),
Credit Scoring Adapter (CON.3), Decision Engine (CON.1). Named alt in I-11: CON.3.
"""
from nopbai import names as N

BASE = dict(
    customer_id="CUST-001",
    requested_amount_vnd=20_000_000,
    customer_age=30,
    is_existing_salaried=True,
    payment_account_id="ACC-001",
)


def test_T04_happy_path_offer_ready(client, auth, platform):
    r = client.post("/loan-applications", headers=auth, json=BASE)
    assert r.status_code == 201
    body = r.json()
    assert body["state"] == N.OFFER_READY
    assert body["loan_offer"]["amount_vnd"] <= N.UNSECURED_AMOUNT_CAP_VND
    # Decision Record + Loan Offer persisted in Decision Store (I-7 owner).
    recs = platform.decision_store.records_for(body["application_id"])
    assert any(rec.decision == N.OFFER_READY for rec in recs)


def test_T14_G6A02_con3_scoring_timeout_named_alt(client, auth, platform):
    payload = {**BASE, "customer_id": "CUST-TO", "simulate_scoring_timeout": True}
    r = client.post("/loan-applications", headers=auth, json=payload)
    assert r.status_code == 503                      # documented CON.3 status
    assert r.json()["detail"]["error_code"] == N.CON_3
    assert r.json()["detail"]["state"] == N.FAILED   # compensating: record Failed, no approval
    app_id = platform.loan_application_service._apps  # noqa: SLF001 - test introspection
    # No application reached Approved.
    assert all(a.state != N.APPROVED for a in app_id.values())


def test_T13_G6A01_con2_out_of_segment(client, auth):
    payload = {**BASE, "customer_id": "CUST-OOS", "customer_age": 50}
    r = client.post("/loan-applications", headers=auth, json=payload)
    assert r.status_code == 422
    assert r.json()["detail"]["error_code"] == N.CON_2
    assert r.json()["detail"]["state"] == N.REJECTED


def test_T15_G6A03_con1_amount_cap(client, auth):
    payload = {**BASE, "customer_id": "CUST-BIG", "requested_amount_vnd": 200_000_000}
    r = client.post("/loan-applications", headers=auth, json=payload)
    assert r.status_code == 422
    assert r.json()["detail"]["error_code"] == N.CON_1
    assert r.json()["detail"]["state"] == N.REJECTED


def test_T08_customer_declines_offer(client, auth):
    r = client.post("/loan-applications", headers=auth, json=BASE)
    app_id = r.json()["application_id"]
    d = client.post(f"/loan-applications/{app_id}/decline", headers=auth)
    assert d.status_code == 200 and d.json()["state"] == N.REJECTED
