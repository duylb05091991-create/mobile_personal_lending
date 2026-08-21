# 05 — C4 Context (L1)

**Pack:** Solution (C4)  
**RACI:** SA **R**, Business Owner **A**, EA/BA **C**  
**Handbook:** §3.1, §4.7  
**Language:** C4 Context only. Relationships are *what happens*, not protocol. No internal containers.  
**Glossary:** [20-appendix.md](20-appendix.md)  
**Names:** consistent with the dossier naming used in the earlier architecture and business views.

## Diagram header

```
Title:      C4 Context — Nopbai Personal Loan Platform
Viewpoint:  C4 Context (L1)
Layer(s):   Solution / Business / App / Integration
As-Is | To-Be | Transition:  To-Be
Owner:      Role Solution Architect  Name ________
Version:    v0.1.0  Date 2026-08-21  Status Draft
Legend:     system-in-focus + actors + external systems
Scope:      in-scope digital lending flow / out-of-scope manual review and branch channels
```

## Status

| Field | Value |
| --- | --- |
| Status | Draft |
| N/A reason | Not applicable |
| Owner | SA |
| Date | 2026-08-21 |

## Purpose

This C4 Context view shows the system-in-focus and its direct actors and external dependencies. It does not expose internal containers or application internals. The purpose is to define the product boundary clearly before moving to the C4 Container view.

## System context narrative

The Nopbai Personal Loan Platform sits at the center of the mobile lending workflow. The Customer submits a loan application through the digital channel. The platform evaluates the customer, retrieves a near real-time credit score, applies policy rules to determine the maximum eligible amount and interest rate, and then sends the final decision to the customer. The platform also integrates with the credit scoring service, the ESB integration layer, and Core Banking for disbursement and accounting updates.

## Context relationships

| From | To | Relationship | Purpose |
| --- | --- | --- | --- |
| Customer | Nopbai Personal Loan Platform | Submits loan application | Initiates the digital lending journey |
| Customer | Nopbai Personal Loan Platform | Reviews offer and accepts terms | Completes the final decision step |
| Nopbai Personal Loan Platform | Credit Scoring System | Requests credit assessment | Determines eligibility and score |
| Nopbai Personal Loan Platform | ESB Integration Layer | Sends routing and transaction messages | Bridges lending workflows with banking services |
| ESB Integration Layer | Core Banking | Posts accounting and disbursement requests | Completes posting and confirmation |
| Nopbai Personal Loan Platform | Core Banking | Confirms disbursement outcome | Records the final transaction result |

## Context actors and systems

| Element | Type | Description |
| --- | --- | --- |
| Customer | Person | Existing salaried customer submitting and reviewing a loan application |
| Nopbai Personal Loan Platform | System | Main digital lending platform for application intake, decisioning, and offer handling |
| Credit Scoring System | External System | External scoring provider that returns near real-time risk data |
| ESB Integration Layer | External System | Integration gateway for bank-to-bank transaction and accounting message flow |
| Core Banking | External System | Banking core for account validation, ledger posting, and disbursement confirmation |

## Architectural interpretation

This C4 Context view defines a clear product boundary:

- the customer is the primary actor,
- the loan platform is the system-in-focus,
- the scoring system, ESB, and Core Banking are external dependencies,
- the architecture remains deliberately free of internal container details until the C4 Container view is created.

This context is the correct starting point for the later solution design pack and acts as the boundary definition for the product’s system behavior and integration model.
