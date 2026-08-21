# Business Process — Nopbai Mobile Personal Loan

**Status:** Corrected architecture draft; not a completed Lab 5 UML artifact.
**RACI:** BA/PO R; Business Owner A; EA, SA, Sec, Test C.
**Language:** ArchiMate Business Process only. No protocols or C4 container boxes.

## Header

| Field | Value |
| --- | --- |
| Viewpoint | ArchiMate Business Process |
| Transition | To-Be |
| Owner | Business Analyst / Product Owner |
| Date | 2026-08-21 |

## Happy path

1. Customer submits a Loan Application through Mobile App.
2. Loan Application Service validates the customer segment and request.
3. Decision Engine obtains a Credit Score through Credit Scoring Adapter.
4. Policy Engine calculates the eligible amount and personalized rate.
5. Decision Engine creates a Loan Offer and returns it through Mobile App.
6. Customer accepts the Nopbai Personal Loan Agreement.
7. Account Validation Service validates the payment account.
8. Disbursement Adapter sends the approved request through ESB Integration Layer to Core Banking.
9. Decision Store and Audit Log retain the decision and transaction evidence.

## Process and constraints

| Branch | Constraint | Business response |
| --- | --- | --- |
| Score timeout | CON.3 | Controlled rejection or exception review; no approval. |
| Amount over cap | CON.1 | Reject or escalate; amount cannot exceed 100,000,000 VND. |
| Ineligible segment | CON.2 | Reject before decisioning. |
| Account validation failure | CON.4 | Reject; no disbursement or accounting posting. |
| Evidence access or protection issue | CON.5 | Block processing and record an audit event. |

The view names business roles, services, objects, and process steps. Protocol and sync/async labels belong in the later C4 Container view.
