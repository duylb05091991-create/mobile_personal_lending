# Lab 2 — Requirements, Analysis, and Trace

**Status:** Draft, current-language before pack. Lab 1 identity source: [../list.md](../list.md).

## Requirements

| ID | Requirement | Goal / outcome | Process / state | Constraint |
| --- | --- | --- | --- | --- |
| FR-01 | Mobile App accepts a Loan Application. | Mobile journey | Draft -> Submitted | CON.2 |
| FR-02 | Loan Application Service validates the application and segment. | Automated journey | Submitted -> Scoring | CON.2 |
| FR-03 | Credit Scoring Adapter retrieves a Credit Score. | Automated decision | Scoring -> OfferReady | CON.3 |
| FR-04 | Policy Engine calculates the maximum eligible amount. | Controlled offer | Scoring -> OfferReady | CON.1 |
| FR-05 | Policy Engine calculates the personalized rate. | Controlled offer | Scoring -> OfferReady | CON.1 |
| FR-06 | Decision Engine creates a Loan Offer. | Customer experience | OfferReady | CON.1 |
| FR-07 | Decision Engine approves or rejects within policy. | Automated decision | OfferReady -> Approved / Rejected | CON.1 |
| FR-08 | Decision Engine recommends a limit increase for an eligible existing customer. | Customer value | OfferReady | CON.2 |
| FR-09 | Account Validation Service validates the payment account before disbursement. | Reliable funds access | Approved -> AccountValidated / Failed | CON.4 |
| FR-10 | Disbursement Adapter posts through ESB Integration Layer to Core Banking. | Reliable accounting | AccountValidated -> Disbursed / Failed | CON.4 |
| FR-11 | Decision Store and Audit Log retain evidence. | Explainable outcome | all decision states | CON.5 |

## Analysis

**As-is:** fragmented or manual assessment slows approval and separates decision evidence from transaction outcome.

**To-be:** Mobile App submits the Loan Application; Loan Application Service validates it; Decision Engine coordinates Credit Scoring Adapter and Policy Engine; Mobile App presents the Loan Offer; Account Validation Service and Disbursement Adapter complete the approved flow through ESB Integration Layer and Core Banking.

**Capabilities implied by the goal:** application intake, eligibility and scoring, policy and offer calculation, automated decisioning, account validation and disbursement, and decision traceability.

**Exceptions:** scoring timeout records Failed; amount over cap is Rejected; account validation failure records Failed with no disbursement; accounting confirmation failure records Failed and requires reconciliation; out-of-segment limit increase is rejected.

## Trace table

| Requirement | Process step | Constraint | Object / state |
| --- | --- | --- | --- |
| FR-01 | Submit Loan Application | CON.2 | Loan Application / Submitted |
| FR-02 | Validate application | CON.2 | Loan Application / Scoring |
| FR-03 | Retrieve Credit Score | CON.3 | Credit Score / OfferReady |
| FR-04 | Calculate amount | CON.1 | Loan Offer / OfferReady |
| FR-05 | Calculate rate | CON.1 | Loan Offer / OfferReady |
| FR-06 | Present Loan Offer | CON.1 | Loan Offer / OfferReady |
| FR-07 | Apply decision | CON.1 | Loan Application / Approved or Rejected |
| FR-08 | Recommend Limit Increase | CON.2 | Loan Offer / OfferReady |
| FR-09 | Validate account | CON.4 | Disbursement Record / AccountValidated or Failed |
| FR-10 | Disburse and post | CON.4 | Disbursement Record / Disbursed or Failed |
| FR-11 | Record evidence | CON.5 | Decision Record / all states |

## Open assumptions

Q1-Q5 remain open: eligibility details, scoring thresholds, scoring payload fields, payment account choice, and numeric SLA targets.
