# 08 — Application Cooperation / Application Architecture

**Pack:** Architecture (ArchiMate)  
**RACI:** SA **R**, EA/DA/Dev **C**  
**Handbook:** §3.1, §4.3  
**Language:** ArchiMate application layer — serving and cooperation, not C4 protocol labels  
**Glossary:** [20-appendix.md](20-appendix.md)  
**Names:** consistent with the business and solution naming used in the dossier.

## Diagram header

```
Title:      Application Architecture — Mobile Personal Loan Product
Viewpoint:  ArchiMate
Layer(s):   App
As-Is | To-Be | Transition:  To-Be
Owner:      Role Solution Architect  Name ________
Version:    v0.1.0  Date 2026-08-21  Status Draft
Legend:     serving and cooperation relationships
Scope:      in-scope digital lending application components / out-of-scope manual process
```

## Status

| Field | Value |
| --- | --- |
| Status | Draft |
| N/A reason | Not applicable |
| Owner | SA |
| Date | 2026-08-21 |

## Purpose

This application architecture view explains how the main application components work together to support the mobile loan journey. It shows logical cooperation between the channel, decisioning, policy, integration, and accounting components.

## Application cooperation view

The core intent is:
- the mobile app captures and submits the application,
- the loan application service validates the request,
- the decision engine coordinates scoring, policy pricing, and offer generation,
- the disbursement and accounting adapter completes the post-approval flow,
- the decision store and audit log capture evidence for traceability.

## Application cooperation table

| From | To | ArchiMate relationship | Contract / interface |
| --- | --- | --- | --- |
| Mobile App | Loan Application Service | Serving | Loan submission API |
| Loan Application Service | Decision Engine | Serving | Eligibility and offer request |
| Decision Engine | Credit Scoring Adapter | Serving | Score request / response |
| Decision Engine | Policy Engine | Serving | Max amount and pricing rules |
| Decision Engine | Decision Store | Serving | Decision persistence |
| Decision Engine | Mobile App | Serving | Offer and decision response |
| Disbursement Adapter | ESB Integration Layer | Serving | Accounting and disbursement request |
| ESB Integration Layer | Core Banking | Serving | Posting and confirmation |
| Audit Log | Decision Store | Serving | Decision evidence correlation |

## Application components

| Component | Responsibility |
| --- | --- |
| Mobile App | Customer entry point for application, offer review, and acceptance |
| Loan Application Service | Receives and validates the application request |
| Decision Engine | Orchestrates scoring, eligibility, amount calculation, offer generation, and approval decision |
| Credit Scoring Adapter | Wraps the external score retrieval interface |
| Policy Engine | Applies product policy and pricing rules |
| Disbursement Adapter | Validates account and triggers payout and accounting flow |
| ESB Integration Layer | Routes and orchestrates interactions with Core Banking |
| Decision Store | Stores decision data and decision artifacts |
| Audit Log | Keeps decision and transaction evidence for review and audit |

## Architectural interpretation

This application architecture is intentionally built around clear responsibilities:

- the channel is separate from business logic,
- decisioning is centralized and policy driven,
- external systems are isolated behind adapters,
- disbursement and posting are handled through a clear integration layer,
- decision evidence is retained as a dedicated concern.

The application cooperation view is the logical bridge between the business strategy and the later C4 and UML design views.
