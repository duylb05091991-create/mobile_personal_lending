# Technology Architecture — Nopbai Mobile Personal Loan

**Status:** Corrected architecture draft; logical technology only.
**RACI:** Ops R; SA A; Sec, Dev C.
**Language:** ArchiMate Technology only; no product deployment claims.

## Header

| Field | Value |
| --- | --- |
| Viewpoint | ArchiMate Technology |
| Transition | To-Be |
| Owner | Operations |
| Date | 2026-08-21 |

## Logical locations

| Location | Assigned logical elements |
| --- | --- |
| Customer mobile device | Mobile App |
| Lending application runtime | Loan Application Service, Decision Engine, Policy Engine, Account Validation Service, Credit Scoring Adapter, Disbursement Adapter |
| Evidence data store | Decision Store, Audit Log |
| External banking integration zone | Credit Scoring System, ESB Integration Layer, Core Banking |

## Technology relationships

| From | To | Purpose |
| --- | --- | --- |
| Mobile App | Loan Application Service | Secure application submission and response |
| Decision Engine | Credit Scoring Adapter | Isolate scoring integration |
| Credit Scoring Adapter | Credit Scoring System | Near-real-time score retrieval |
| Disbursement Adapter | ESB Integration Layer | Route accounting and disbursement messages |
| ESB Integration Layer | Core Banking | Account validation, posting, and confirmation |
| Decision Store | Audit Log | Correlate decision and transaction evidence |

The channel does not write directly to the Core Banking ledger. Any technology products used later are labels, not new identity entries in I-4.
