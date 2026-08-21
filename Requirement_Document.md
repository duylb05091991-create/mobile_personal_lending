# Requirement Document — Nopbai Mobile Personal Loan

**Status:** Lab 1 identity-aligned draft; requirements are not approved as Lab 2 until Lab 1 is formally marked Done.

## Objective and scope

Nopbai Mobile Personal Loan enables existing salaried customers aged 22-35 to apply through Mobile App, receive an automated decision, and receive disbursement after approval and account validation.

In scope are unsecured loans up to 100,000,000 VND, scoring, policy-based amount and rate calculation, offer recommendation, automated approval or rejection, account validation, disbursement, accounting through ESB Integration Layer to Core Banking, and traceability. Secured loans, SME loans, branch onboarding, non-salaried customers, manual underwriting on the standard path, production credentials, and real customer data are out of scope.

## Functional requirements

| ID | Requirement |
| --- | --- |
| FR-01 | Mobile App shall allow Customer to submit a Loan Application. |
| FR-02 | Loan Application Service shall validate customer and application eligibility. |
| FR-03 | Credit Scoring Adapter shall retrieve a near-real-time score from Credit Scoring System. |
| FR-04 | Policy Engine shall calculate the maximum eligible amount. |
| FR-05 | Policy Engine shall calculate a personalized interest rate. |
| FR-06 | Decision Engine shall create and return a Loan Offer. |
| FR-07 | Decision Engine shall approve or reject applications within policy rules. |
| FR-08 | Decision Engine shall support a limit-increase recommendation for eligible existing customers. |
| FR-09 | Account Validation Service and Disbursement Adapter shall support disbursement only after approval and validation. |
| FR-10 | Disbursement Adapter shall send accounting and disbursement requests through ESB Integration Layer to Core Banking. |
| FR-11 | Decision Store and Audit Log shall retain score, policy basis, calculations, decisions, integration events, and outcomes. |

## Business rules and constraints

- CON.1: Unsecured loan amount must not exceed 100,000,000 VND.
- CON.2: Initial segment is existing salaried customers aged 22-35.
- CON.3: Credit scoring is near real time; timeout is a controlled exception.
- CON.4: No disbursement or accounting posting before approval and successful account validation.
- CON.5: Customer data and decision evidence must be protected and auditable.

## Non-functional requirements

| ID | Requirement |
| --- | --- |
| NFR-01 | Decisioning shall support a near-real-time mobile experience. |
| NFR-02 | The lending service shall be available during normal banking operating hours and business-critical scenarios. |
| NFR-03 | The solution shall minimize incorrect decisions and failed accounting flows. |
| NFR-04 | Customer data shall be protected with secure authentication, authorization, and banking security controls. |
| NFR-05 | Decisions, integrations, and transaction outcomes shall be auditable. |
| NFR-06 | Data shall remain consistent across applications, scoring, decisions, and Core Banking records. |
| NFR-07 | The solution shall support increasing mobile loan requests without degrading service quality. |
| NFR-08 | The solution shall comply with applicable lending, privacy, risk, and financial regulations. |

## Open questions

Q1 exact eligibility and affordability rules; Q2 scoring thresholds; Q3 scoring payload fields; Q4 initial payment account; Q5 response-time and availability targets. These remain open assumptions.
