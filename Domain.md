# Domain — Nopbai Mobile Personal Loan

**Status:** Lab 1 identity-aligned draft; not a completed Lab 2 artifact.

## Product scope

Nopbai Mobile Personal Loan is an unsecured loan product for existing salaried customers aged 22-35. The product supports mobile application, automated credit scoring, policy-based amount and rate calculation, offer presentation, approval or rejection, account validation, immediate disbursement, and accounting through ESB Integration Layer to Core Banking.

## In scope

- Unsecured loans up to 100,000,000 VND
- Existing salaried customers aged 22-35
- Mobile App application and offer acceptance
- Credit Scoring System integration through Credit Scoring Adapter
- Policy-based eligibility, amount, and rate calculation
- Automated approval or rejection through Decision Engine
- Account validation before disbursement
- Disbursement and accounting through ESB Integration Layer to Core Banking
- Decision Store and Audit Log traceability

## Out of scope

- Secured loans
- Business or SME loans
- Branch onboarding
- Non-salaried customers
- Manual underwriting on the standard path
- Production implementation details, credentials, and real customer data

## Domain objects

| Object | Meaning | Source of truth |
| --- | --- | --- |
| Loan Application | Customer request and lifecycle state | Loan Application Service |
| Customer Profile | Existing customer, income, and account information | Core Banking |
| Credit Score | Risk score used by decisioning | Credit Scoring System |
| Policy Configuration | Eligibility, amount, rate, and decision rules | Policy Engine |
| Decision Record | Score, policy basis, calculations, offer, and final decision | Decision Store |
| Disbursement Record | Account validation and posting outcome | Core Banking |

## Core states

`Draft` -> `Submitted` -> `Scoring` -> `OfferReady` -> `Approved` -> `AccountValidated` -> `Disbursed`

Terminal states are `Rejected`, `Disbursed`, and `Failed`.

## Domain rules

- Decision Engine must evaluate eligibility, score, policy, maximum amount, and rate before approval.
- The amount must not exceed 100,000,000 VND.
- No disbursement or accounting posting occurs before approval and successful account validation.
- Mobile App is a channel and must not perform credit evaluation or write directly to Core Banking.
