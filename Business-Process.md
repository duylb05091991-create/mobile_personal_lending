# 02 — Business Process

**Pack:** Business (ArchiMate)  
**RACI:** BA/PO **R**, Business Owner **A**, EA/SA/Sec/Test **C**  
**Handbook:** §3.1, §4.2  
**Language:** ArchiMate only — process steps and triggering relationships, not C4 containers or protocol labels  
**Glossary:** [20-appendix.md](20-appendix.md)  
**Names:** use the same naming conventions as the project dossier.

## Diagram header

```
Title:      Business Process — Mobile Personal Loan Product
Viewpoint:  ArchiMate
Layer(s):   Business
As-Is | To-Be | Transition:  To-Be
Owner:      Role Business Analyst / Product Owner  Name ________
Version:    v0.1.0  Date 2026-08-21  Status Draft
Legend:     triggering, business services, business objects
Scope:      in-scope mobile lending process / out-of-scope manual branch-based lending
```

## Status

| Field | Value |
| --- | --- |
| Status | Draft |
| N/A reason | Not applicable |
| Owner | BA / Product Owner |
| Date | 2026-08-21 |

## Purpose

This view describes the primary business flow for a customer applying for a personal loan, receiving a credit decision, and obtaining disbursement when approved. It also identifies the key decision points and business artifacts involved.

## Primary business process

### Process flow

1. Customer opens the mobile app and submits a loan application.
2. System validates the customer and loan request details.
3. Eligibility and customer profile checks are performed.
4. Credit scoring system is called to obtain the near real-time score.
5. Policy engine calculates the maximum eligible amount and personalized interest rate.
6. Offer recommendation is created and shown to the customer.
7. Auto decisioning is applied against policy thresholds.
8. If approved, account validation is performed.
9. Disbursement is triggered and accounting entries are posted through ESB to Core Banking.
10. Decision and transaction evidence are stored for audit and traceability.

## Step table

| Step | Business Role | Business Service | Business Object | Application Component |
| --- | --- | --- | --- | --- |
| 1 | Customer | Loan application intake | Loan Application | Mobile App |
| 2 | Loan Applicant | Eligibility validation | Customer Profile | Loan Service |
| 3 | Risk & Credit Evaluator | Credit assessment | Credit Score | Scoring Adapter |
| 4 | Product / Operations | Offer calculation | Policy Configuration | Policy Engine |
| 5 | Customer | Offer presentation | Loan Offer | Mobile App |
| 6 | Loan Operations | Auto decisioning | Decision Record | Decision Engine |
| 7 | Loan Operations | Account validation | Disbursement Record | Account Validation Service |
| 8 | Loan Operations | Disbursement and accounting | Disbursement Record | ESB / Core Banking |
| 9 | Risk / Compliance | Decision traceability | Decision Record | Audit Log / Decision Store |

## Exception handling paths

| Exception | Business response |
| --- | --- |
| Credit score unavailable or timed out | Reject or route to exception handling based on policy |
| Account validation fails | Reject application; no disbursement |
| Policy cap exceeded | Reject or escalate to policy review |
| Accounting posting fails | Trigger compensating action or reconciliation flow |

## Business process summary

The main flow is designed to be fast and mostly automated, with decision-quality controls built in through policy, scoring, and traceability. It balances customer speed with operational discipline and compliance accountability.

This business process is the direct foundation for later solution design views such as C4 context and UML sequence models.
