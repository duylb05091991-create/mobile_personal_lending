"""10-minute capstone demo (order per capstone.md):
  I-1 goal -> one I-11 sequence on screen -> live happy path -> live named alt/CON.* -> test report.

Run: PYTHONPATH=src python scripts/demo.py
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient  # noqa: E402

from nopbai import names as N  # noqa: E402
from nopbai.app import create_app  # noqa: E402

LINE = "=" * 74
AUTH = {"X-Customer-Id": "CUST-001"}


def banner(title: str) -> None:
    print(f"\n{LINE}\n{title}\n{LINE}")


def main() -> None:
    client = TestClient(create_app())

    banner("1. I-1 GOAL")
    print(f"System-in-focus : {N.SYSTEM_IN_FOCUS}")
    print(f"Product         : {N.PRODUCT}")
    print(f"Goal            : {N.GOAL}")

    banner("2. I-11 SEQUENCE ON SCREEN  (Submit and Decide Loan Application)")
    print(
        "Customer -> Mobile App -> Loan Application Service (CON.2 segment gate)\n"
        "  -> Decision Engine [Score Coordinator -> Credit Scoring Adapter (C-01, CON.3)\n"
        "     -> Policy Evaluation Module -> Policy Engine (CON.1 cap)\n"
        "     -> Offer Builder -> Decision Recorder -> Decision Store + Audit Log]\n"
        "  -> Loan Offer returned via Mobile App"
    )

    banner("3. LIVE HAPPY PATH  (Submit and Decide -> Disburse)")
    r = client.post(
        "/loan-applications", headers=AUTH,
        json={"customer_id": "CUST-001", "requested_amount_vnd": 20_000_000,
              "customer_age": 30, "is_existing_salaried": True, "payment_account_id": "ACC-001"},
    )
    print(f"POST /loan-applications -> {r.status_code}  state={r.json()['state']}  "
          f"offer={r.json()['loan_offer']['amount_vnd']:,} VND @ {r.json()['loan_offer']['interest_rate']}")
    app_id = r.json()["application_id"]
    a = client.post(f"/loan-applications/{app_id}/agreement", headers=AUTH)
    print(f"POST .../agreement     -> {a.status_code}  state={a.json()['state']}")
    d = client.post(f"/loan-applications/{app_id}/disbursement", headers=AUTH, json={})
    print(f"POST .../disbursement  -> {d.status_code}  state={d.json()['state']}  "
          f"ref={d.json()['disbursement_reference']}")

    banner("4. LIVE NAMED ALT / CON.*")
    t = client.post(
        "/loan-applications", headers=AUTH,
        json={"customer_id": "CUST-TO", "requested_amount_vnd": 20_000_000, "customer_age": 30,
              "is_existing_salaried": True, "payment_account_id": "ACC-TO",
              "simulate_scoring_timeout": True},
    )
    print(f"UC1 alt CON.3 (scoring timeout) -> {t.status_code}  body={t.json()['detail']}")

    a2 = client.post(
        "/loan-applications", headers=AUTH,
        json={"customer_id": "CUST-2", "requested_amount_vnd": 20_000_000, "customer_age": 30,
              "is_existing_salaried": True, "payment_account_id": "ACC-2"},
    )
    app2 = a2.json()["application_id"]
    client.post(f"/loan-applications/{app2}/agreement", headers=AUTH)
    p = client.post(f"/loan-applications/{app2}/disbursement", headers=AUTH,
                    json={"simulate_posting_failure": True})
    print(f"UC2 alt CON.4 (posting fail)    -> {p.status_code}  body={p.json()['detail']}")

    seg = client.post(
        "/limit-increase-recommendations", headers=AUTH,
        json={"customer_id": "CUST-9", "requested_amount_vnd": 20_000_000,
              "customer_age": 19, "is_existing_salaried": True},
    )
    print(f"UC3 alt CON.2 (out-of-segment)  -> {seg.status_code}  body={seg.json()['detail']}")

    forb = client.post("/backing/core-banking/postings", headers={"X-Caller": N.MOBILE_APP},
                       json={"application_id": "LA-x", "amount_vnd": 1, "disbursement_reference": "r"})
    print(f"I-9 forbidden (Mobile App -> Core Banking) -> {forb.status_code}  REJECTED")

    banner("5. TEST REPORT")
    root = pathlib.Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=root, env={**__import__("os").environ, "PYTHONPATH": "src"},
    )


if __name__ == "__main__":
    main()
