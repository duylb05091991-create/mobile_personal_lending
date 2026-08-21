# C4 Context (L1) — Nopbai Personal Loan Platform

**Status:** Corrected draft; Lab 9 evidence is not accepted until Lab 8 is Done.
**RACI:** SA R; Business Owner A; EA/BA C.
**Language:** C4 Context only. No internal containers, databases, buses, or protocols.

## Header

| Field | Value |
| --- | --- |
| Viewpoint | C4 Context (L1) |
| Transition | To-Be |
| Owner | Solution Architect |
| Date | 2026-08-21 |
| Scope | Customer, system-in-focus, and I-3 external systems only |

## Context elements

| Element | Type | Responsibility |
| --- | --- | --- |
| Customer | Person | Applies, reviews the Loan Offer, and accepts the Nopbai Personal Loan Agreement. |
| Nopbai Personal Loan Platform | System in focus | Provides the digital application, decision, offer, validation, disbursement, and traceability journey. |
| Credit Scoring System | External system | Returns a near-real-time Credit Score. |
| ESB Integration Layer | External system | Routes accounting and disbursement messages. |
| Core Banking | External system | Validates accounts and records posting and disbursement outcomes. |

## Relationships

| From | To | What happens |
| --- | --- | --- |
| Customer | Nopbai Personal Loan Platform | Submits a Loan Application. |
| Customer | Nopbai Personal Loan Platform | Reviews a Loan Offer and accepts the contract. |
| Nopbai Personal Loan Platform | Credit Scoring System | Requests a Credit Score. |
| Nopbai Personal Loan Platform | ESB Integration Layer | Sends an approved disbursement and accounting request. |
| ESB Integration Layer | Core Banking | Routes the request for validation, posting, and confirmation. |

This L1 view intentionally does not show Mobile App, Decision Engine, adapters, stores, or any other I-4 container.
