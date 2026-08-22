"""CON.5 (EX-05): unauthorized access to protected decisioning is denied and no
decision state is produced. Authenticated access succeeds.
"""
from nopbai import names as N

SUBMIT = dict(
    customer_id="CUST-001", requested_amount_vnd=20_000_000, customer_age=30,
    is_existing_salaried=True, payment_account_id="ACC-001",
)


def test_EX05_submit_requires_authentication(client, platform):
    r = client.post("/loan-applications", json=SUBMIT)  # no X-Customer-Id
    assert r.status_code == 401
    assert r.json()["detail"]["error_code"] == N.CON_5
    # No Decision Record was produced for an unauthenticated request.
    assert platform.decision_store._records == {}  # noqa: SLF001


def test_EX05_limit_increase_requires_authentication(client):
    r = client.post(
        "/limit-increase-recommendations",
        json={"customer_id": "C", "requested_amount_vnd": 1, "customer_age": 30, "is_existing_salaried": True},
    )
    assert r.status_code == 401


def test_EX05_disbursement_requires_authentication(client):
    r = client.post("/loan-applications/LA-x/disbursement", json={})
    assert r.status_code == 401


def test_authenticated_access_succeeds(client, auth):
    r = client.post("/loan-applications", headers=auth, json=SUBMIT)
    assert r.status_code == 201
