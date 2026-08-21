# Motivation / Strategy — Nopbai Mobile Personal Loan

**Status:** Corrected architecture draft; Lab 8 evidence is not accepted until Lab 7 and Labs 1-6 archive are complete.
**RACI:** EA R; Business Owner A; SA, BA, Sec C.
**Language:** ArchiMate motivation and strategy only.

## Header

| Field | Value |
| --- | --- |
| Viewpoint | ArchiMate Motivation / Strategy |
| Transition | To-Be |
| Owner | Enterprise Architect |
| Date | 2026-08-21 |
| Scope | Nopbai Mobile Personal Loan; branch and manual standard-path lending out of scope |

## Motivation

Customer demand for a fast mobile journey, the need for controlled personalized lending, and the need for secure accounting evidence motivate the initiative.

## Goals and outcomes

| ID | Type | Statement |
| --- | --- | --- |
| MOT.GOAL.01 | Goal | Provide a mobile-first unsecured personal loan journey. |
| MOT.GOAL.02 | Goal | Automate eligibility, scoring, policy, amount, rate, and decisioning. |
| MOT.GOAL.03 | Goal | Provide a policy-compliant Nopbai Personal Loan offer. |
| MOT.GOAL.04 | Goal | Disburse approved loans and post accounting reliably. |
| MOT.GOAL.05 | Goal | Preserve explainable, secure, auditable decision evidence. |
| MOT.OUT.01 | Outcome | ASSUMPTION: standard decisions return within P95 <= 30 seconds. |
| MOT.OUT.02 | Outcome | Eligible customers complete the standard journey without manual underwriting. |
| MOT.OUT.03 | Outcome | Offers use the calculated amount and personalized rate from shared policy rules. |
| MOT.OUT.04 | Outcome | Disbursement occurs only after approval and account validation. |
| MOT.OUT.05 | Outcome | Score, policy basis, calculations, integrations, and outcomes are traceable. |

## Capabilities and requirements

| Capability | Realized by |
| --- | --- |
| Loan application intake | Mobile App, Loan Application Service |
| Eligibility and scoring | Decision Engine, Credit Scoring Adapter |
| Policy and offer calculation | Policy Engine, Decision Engine |
| Account validation and disbursement | Account Validation Service, Disbursement Adapter |
| Accounting integration | ESB Integration Layer, Core Banking |
| Decision traceability | Decision Store, Audit Log |

FR-01 through FR-11 are realized by the containers and paths listed in [Requirement_Document.md](Requirement_Document.md). The constraints are:

- CON.1: amount <= 100,000,000 VND.
- CON.2: existing salaried customers aged 22-35 only.
- CON.3: near-real-time scoring with controlled timeout handling.
- CON.4: approval and account validation precede disbursement and accounting.
- CON.5: customer data and evidence are protected and auditable.

## Architecture implication

Keep Mobile App channel-only. Keep Credit Scoring System, ESB Integration Layer, and Core Banking external. Keep adapters, Decision Engine, Policy Engine, Account Validation Service, stores, and Audit Log internal. Do not place protocols or container internals on this ArchiMate view.
