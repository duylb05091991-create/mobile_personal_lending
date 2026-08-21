# Lab 9 — C4 Context and Container After Pack

**Status:** Draft after-pack; requires Lab 8 review.

## RACI

| Artifact | R | A | C |
| --- | --- | --- | --- |
| C4 Context L1 | SA | Owner | EA, BA, Sec |
| C4 Container L2 | SA | EA | DA, Sec, Dev, Ops |
| C4 Component L3 optional | Dev | SA | Sec, Test |

## C4 Context L1

People: Customer. System in focus: Nopbai Personal Loan Platform. Externals: Credit Scoring System, ESB Integration Layer, Core Banking. Relationships describe what happens, not protocols. No internal containers appear.

## C4 Container L2

| Container | Responsibility |
| --- | --- |
| Mobile App | Application and offer channel |
| Loan Application Service | Application validation and lifecycle |
| Credit Scoring Adapter | External scoring contract |
| Decision Engine | Orchestration and decision |
| Policy Engine | Amount, rate, and decision rules |
| Account Validation Service | Payment account validation |
| Disbursement Adapter | Idempotent disbursement request |
| Decision Store | Decision and offer persistence |
| Audit Log | Evidence persistence |

Externals remain Credit Scoring System, ESB Integration Layer, and Core Banking.

## Container relationship labels

- Mobile App -> Loan Application Service: HTTPS sync, submit Loan Application.
- Credit Scoring Adapter -> Credit Scoring System: HTTPS sync, Get Credit Score.
- Decision Engine -> Policy Engine: in-process sync, calculate amount and rate.
- Account Validation Service -> Disbursement Adapter: in-process sync, authorize disbursement.
- Disbursement Adapter -> ESB Integration Layer: message async, Submit Disbursement and Accounting Request.
- ESB Integration Layer -> Core Banking: message async with confirmation, validate and post.
- Decision Engine -> Decision Store / Audit Log: persistence sync.

## Optional component

Decision Engine is the only selected container for C4 Component. Its modules are Eligibility Coordinator, Scoring Result Handler, Offer Calculator, Decision Evaluator, Limit Increase Recommender, and Decision Evidence Writer.
