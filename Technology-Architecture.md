# 13 — Technology Architecture

**Pack:** Architecture (ArchiMate)  
**RACI:** Ops **R**, SA **A**, Sec/Dev **C**  
**Handbook:** §3.1, §4.5  
**Language:** ArchiMate technology layer — logical nodes, middleware, and runtime environments  
**Glossary:** [20-appendix.md](20-appendix.md)  
**Names:** consistent with the broader Nopbai architecture dossier.

## Diagram header

```
Title:      Technology Architecture — Mobile Personal Loan Product
Viewpoint:  ArchiMate
Layer(s):   Tech
As-Is | To-Be | Transition:  To-Be
Owner:      Role Operations / Solution Architect  Name ________
Version:    v0.1.0  Date 2026-08-21  Status Draft
Legend:     logical nodes, middleware, application assignment, integration path
Scope:      in-scope digital lending runtime / out-of-scope branch or manual processing
```

## Status

| Field | Value |
| --- | --- |
| Status | Draft |
| N/A reason | Not applicable |
| Owner | Ops / SA |
| Date | 2026-08-21 |

## Purpose

This technology architecture view explains the logical runtime landscape for the digital lending product. It shows where the application components are hosted, which middleware and integration services connect them, and how the app interacts with external banking systems.

## Logical technology components

| Node / environment | Description | Assigned applications |
| --- | --- | --- |
| Mobile Channel Tier | Customer-facing digital touchpoint and secure interaction layer | Mobile App |
| Lending Service Tier | Business and orchestration functions for application processing | Loan Application Service, Decision Engine, Policy Engine |
| Integration Tier | Standardized integration and routing services | Credit Scoring Adapter, Disbursement Adapter, ESB Integration Layer |
| Data & Evidence Tier | Stores for decisions, traceability, and operational evidence | Decision Store, Audit Log |
| External Banking Tier | Core banking and risk evaluation providers | Credit Scoring System, Core Banking |

## Technology path summary

| Path | Direction | Purpose |
| --- | --- | --- |
| Mobile App → Loan Application Service | Application call | Loan request submission and validation |
| Loan Application Service → Decision Engine | Service orchestration | Business rule and decision flow |
| Decision Engine → Credit Scoring Adapter → Credit Scoring System | Integration | Real-time risk score retrieval |
| Decision Engine → Policy Engine | Internal decision logic | Amount and rate calculation |
| Decision Engine → Mobile App | Response path | Offer and approval response |
| Disbursement Adapter → ESB Integration Layer → Core Banking | Banking integration | Disbursement and ledger posting |
| Decision Engine → Decision Store / Audit Log | Evidence path | Decision traceability and audit retention |

## Technology interpretation

The technology design follows a layered runtime approach:

- customer-facing channel is separated from transactional business logic,
- lending services form the operational core of the product,
- integration services isolate external bank and credit risk dependencies,
- data and evidence stores preserve auditability and traceability,
- external banking systems remain outside the product’s direct control but are integrated through clearly defined interfaces.

This view provides the logical runtime context that supports the later C4 container, deployment, and UML design artifacts.
