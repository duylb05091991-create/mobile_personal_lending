# Application Cooperation — Nopbai Mobile Personal Loan

**Status:** Corrected architecture draft; C4 Container is the later solution view.
**RACI:** SA R; EA A; Dev, DA, Sec C.
**Language:** ArchiMate Application Cooperation only.

## Header

| Field | Value |
| --- | --- |
| Viewpoint | ArchiMate Application |
| Transition | To-Be |
| Owner | Solution Architect |
| Date | 2026-08-21 |

## Internal application components

| Component | Responsibility |
| --- | --- |
| Mobile App | Captures applications and displays offers and outcomes. |
| Loan Application Service | Validates and manages Loan Application. |
| Credit Scoring Adapter | Isolates the Credit Scoring System contract. |
| Decision Engine | Orchestrates scoring, policy, offer, decision, and evidence. |
| Policy Engine | Applies Policy Configuration. |
| Account Validation Service | Validates the payment account before disbursement. |
| Disbursement Adapter | Creates idempotent posting requests and handles outcomes. |
| Decision Store | Persists Decision Record and calculations. |
| Audit Log | Persists integration and transaction evidence. |

## Cooperation relationships

| From | To | Relationship | Purpose |
| --- | --- | --- | --- |
| Mobile App | Loan Application Service | Serving | Submit and validate Loan Application |
| Loan Application Service | Decision Engine | Serving | Start decision flow |
| Decision Engine | Credit Scoring Adapter | Serving | Request Credit Score |
| Credit Scoring Adapter | Credit Scoring System | Serving | External scoring request |
| Decision Engine | Policy Engine | Serving | Calculate amount, rate, and decision |
| Decision Engine | Mobile App | Serving | Return Loan Offer and outcome |
| Decision Engine | Decision Store | Serving | Persist Decision Record |
| Decision Engine | Audit Log | Serving | Persist decision evidence |
| Account Validation Service | Disbursement Adapter | Serving | Permit disbursement after validation |
| Disbursement Adapter | ESB Integration Layer | Serving | Send accounting and disbursement request |
| ESB Integration Layer | Core Banking | Serving | Post and confirm banking transaction |

ESB Integration Layer and Core Banking are external systems, not internal application components.
