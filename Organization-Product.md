# 03 — Organization / Product

**Pack:** Business (ArchiMate)  
**RACI:** BA/PO **R** (product), EA **C**, Business Owner **A**  
**Handbook:** §3.1  
**Language:** ArchiMate Business — actors, roles, objects, services, product composition  
**Glossary:** [20-appendix.md](20-appendix.md)  
**Names:** use the same naming conventions as the project dossier.

## Diagram header

```
Title:      Organization / Product — Mobile Personal Loan Product
Viewpoint:  ArchiMate
Layer(s):   Business
As-Is | To-Be | Transition:  To-Be
Owner:      Role Product Owner / Business Analyst  Name ________
Version:    v0.1.0  Date 2026-08-21  Status Draft
Legend:     actors, roles, product, services, business objects
Scope:      in-scope mobile lending product / out-of-scope branch-based manual lending
```

## Status

| Field | Value |
| --- | --- |
| Status | Draft |
| N/A reason | Not applicable |
| Owner | BA / Product Owner |
| Date | 2026-08-21 |

## Purpose

This view defines the business participants, roles, product structure, and core business services associated with the mobile personal loan capability. It distinguishes the product from its supporting channels and external systems.

## Organization

| Type | Name | Notes |
| --- | --- | --- |
| Business Actor | Customer | Applies for a loan through mobile app |
| Business Actor | Bank | Owns retail lending service and operating policy |
| Business Actor | Credit Scoring System | External risk evaluation provider |
| Business Actor | Core Banking | External ledger and payment posting provider |
| Business Role | Loan Applicant | Customer role for submitting and accepting loan terms |
| Business Role | Risk & Credit Evaluator | Performs scoring and policy-based assessment |
| Business Role | Loan Operations | Oversees approved disbursement and accounting outcome |

## Product structure

| Item | Name | Notes |
| --- | --- | --- |
| Product | Mobile Personal Loan | Primary product under scope |
| Channel | Mobile App | Entry channel for application and offer acceptance |
| Variant / Rail | Standard digital loan journey | Default automated path |
| Contract | Loan Agreement / Offer Terms | Accepted by customer if approved |

## Business objects

These business objects map to the product’s information model and loan lifecycle:

| Business Object | Meaning |
| --- | --- |
| Customer Profile | Customer identity, income type, account, and eligibility data |
| Loan Application | Customer request with requested amount and purpose |
| Credit Score | Risk score returned by external scoring service |
| Policy Configuration | Approved rules for max amount, rate, and decision thresholds |
| Loan Offer | Proposed amount, rate, and repayment terms |
| Decision Record | Final approval or rejection with policy and score evidence |
| Disbursement Record | Account validation and payment posting record |

## Business services

| Business Service | Serves | Realized by |
| --- | --- | --- |
| Loan application intake | Loan Applicant | Mobile App + Loan Service |
| Eligibility and scoring | Risk & Credit Evaluator | Decision Engine + Scoring Adapter |
| Offer calculation | Loan Operations / Product | Policy Engine + Decision Engine |
| Auto decisioning | Loan Operations | Decision Engine |
| Disbursement and accounting | Loan Operations | Disbursement Adapter + ESB + Core Banking |
| Decision traceability | Risk / Compliance | Decision Store + Audit Log |

## Product view summary

The product is a digital, unsecured personal loan for existing salaried customers. It is delivered through the mobile app and supported by automated decisioning, external credit scoring, policy-based offer calculation, and banking integration for disbursement and posting.

The distinguishing feature is the blend of a customer-facing digital channel with a policy-driven automated backend process, while preserving compliance, traceability, and accurate ledger postings.
