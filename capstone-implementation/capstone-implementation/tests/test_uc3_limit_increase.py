"""UC3 - Recommend Limit Increase.

SUTs: Loan Application Service (CON.2 segment), Decision Engine (CON.1).
Named alt in I-11: CON.2. Customer-facing result is the existing I-7 Loan Offer.
"""
from nopbai import names as N

BASE = dict(
    customer_id="CUST-001",
    requested_amount_vnd=20_000_000,
    customer_age=30,
    is_existing_salaried=True,
)


def test_happy_recommendation(client, auth):
    r = client.post("/limit-increase-recommendations", headers=auth, json=BASE)
    assert r.status_code == 201
    assert r.json()["loan_offer"]["kind"] == "limit-increase"


def test_T18_G6A06_con2_out_of_segment_named_alt(client, auth):
    r = client.post("/limit-increase-recommendations", headers=auth, json={**BASE, "customer_age": 19})
    assert r.status_code == 422
    assert r.json()["detail"]["error_code"] == N.CON_2


def test_T19_G6A07_con1_amount_cap(client, auth):
    r = client.post(
        "/limit-increase-recommendations", headers=auth,
        json={**BASE, "requested_amount_vnd": 200_000_000},
    )
    assert r.status_code == 422
    assert r.json()["detail"]["error_code"] == N.CON_1
