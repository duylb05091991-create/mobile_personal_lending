# Quality gates — Architecture

Reviewer checklist for an architecture pack for the mobile personal loan product.

**Source of truth.** [Domain.md](Domain.md), [Requirement_Document.md](Requirement_Document.md), [Analysis.md](Analysis.md).

**When applied.** Before accepting the architecture pack or any C4 context/container view for this product.

**Pass rule.** The pack fails if any Must row is Fail, if any automatic-fail anti-pattern is present, or if an open assumption is treated as a decided product rule. Should rows do not block the pack, but they must still be marked Pass, Fail, or N/A with a comment.

Notation (C4-PlantUML, Mermaid C4, Structurizr, or other) is free. Content is not. Do not invent latency, availability, or SLA numbers.

---

## Sign-off

**Pack title:** ________________________________  
**Author:** ________________________________  
**Reviewer:** ________________________________  
**Date:** ________________________________

**Approval:** [ ] Approved  [ ] Changes requested

---

## Required contents

The architecture pack must contain all of the following. Missing a section is Fail for the matching Must row.

| # | Section / artifact | Must show |
|---|---|---|
| A1 | System context (C4 L1) | Person: Customer. System-in-focus: Mobile Loan Platform. Externals only: Credit Scoring System, Core Banking, ESB Integration Layer. No branch staff, fraud engine, or manual underwriting as a primary actor. |
| A2 | Container view (C4 L2) | Mobile app client; loan application service; decision engine; credit scoring adapter; policy engine; loan decision store; accounting adapter; ESB; Core Banking; audit log. Clear separation of decisioning, integration, and data persistence. |
| A3 | Decisioning gate | The system must evaluate eligibility, score, affordability, policy, and maximum amount before approval or rejection. All decision logic should be explicit and traceable. |
| A4 | Two critical integration paths | Credit scoring request path and accounting/disbursement path. Score retrieval is near-real-time; accounting posting is tied to approval and EsB/Core Banking flow. |
| A5 | Integration notes | Sync credit scoring call; async or confirmable accounting/disbursement flow with idempotent posting; explicit policy and decision traceability. |
| A6 | Cross-cutting | Idempotency key, decision traceability, shared policy configuration, account validation, and auditability. |
| A7 | NFR section | Only NFR-01…NFR-08. No invented latency, availability, or SLA numbers. |
| A8 | Open assumptions | Q1–Q5 listed as open, or closed only with an explicit requirement change. |
| A9 | Traceability | Table: containers / paths → FR-01…FR-11. |
| A10 | Optional component (C4 L3) | If present: drill-down of one container (prefer decision engine or loan application service). Absence of L3 is not Fail. |

---

## Automatic Fail (anti-patterns)

Any one of these is Fail for the whole pack, even if other rows pass.

- Manual underwriting or bank staff on the default approval path
- Loan approval logic hidden in the mobile app as the only decision engine
- Credit scoring or accounting calls embedded inside a single monolith container with no explicit integration boundary
- Missing explicit account validation before disbursement
- Policy and rate logic not visible as a shared configuration or decision component
- Disbursement occurring before approval or account validation is complete
- Invented numeric caps, exact score thresholds, SLA numbers, or fees presented as architecture facts without a requirement change
- Open questions Q1–Q5 silently closed as settled product facts
- Customer data exposed without clear security and audit boundaries

---

## Review checklist

Mark Pass or Fail. Comment is required on Fail.

| ID | Check | Must / Should | Trace | Pass | Fail | Comment |
|---|---|---|---|---|---|---|
| AG-01 | Context includes Customer + system-in-focus + externals Credit Scoring System, Core Banking, ESB | Must | Domain + Req scope | | | |
| AG-02 | Context has no manual-review actor, branch staff, or fraud engine as a normal participant | Must | Scope / out-of-scope | | | |
| AG-03 | Container names align with the project vocabulary: Mobile App, Loan Application Service, Decision Engine, Credit Scoring Adapter, Policy Engine, Account Validation, Disbursement Adapter, ESB, Core Banking, Decision Store, Audit Log | Must | Analysis §2, Domain scope | | | |
| AG-04 | The decisioning path is explicit: submit application → eligibility → credit score → policy → max amount/rate → decision | Must | FR-01..FR-07 | | | |
| AG-05 | Product policy and score thresholds are modeled as shared configuration, not ad hoc logic in the UI | Must | FR-04, FR-05, FR-07 | | | |
| AG-06 | Offer recommendation and max eligible amount are part of the same decision flow and use a shared policy rule set | Must | FR-04, FR-05, FR-06 | | | |
| AG-07 | Credit scoring integration is a distinct external system and adapter; it is not hidden inside the app | Must | FR-03, Analysis §3, §7 | | | |
| AG-08 | Account validation occurs before disbursement and before accounting entries are sent | Must | FR-09, FR-10, Business Rules | | | |
| AG-09 | Disbursement is only shown after approval and account validation succeed | Must | FR-07, FR-09 | | | |
| AG-10 | Accounting entries are sent via ESB to Core Banking; Core Banking remains external | Must | FR-10, Integration dependencies | | | |
| AG-11 | The architecture keeps decision traceability as a first-class service/store; score, policy basis, and computed result are persisted | Must | FR-11, NFR-05 | | | |
| AG-12 | Audit logs capture decision-making and integration actions without violating banking security expectations | Must | NFR-04, NFR-05 | | | |
| AG-13 | The design shows a clear read/write split for decision data and loan ledger/audit evidence | Should | NFR-06, FR-11 | | | |
| AG-14 | Scoring timeout / outage is represented as a critical exception path and not silently ignored | Must | Analysis §8 | | | |
| AG-15 | Account validation failure is represented as a reject path with no disbursement | Must | Analysis §8, FR-09 | | | |
| AG-16 | Accounting post failure includes compensating action or reconciliation requirement | Must | Analysis §8, FR-10 | | | |
| AG-17 | Policy breach or amount over cap path is modeled as an escalation or reject flow | Must | Analysis §8, FR-04, FR-07 | | | |
| AG-18 | NFR section contains only NFR-01…NFR-08; no invented numbers or SLA values | Must | A7, Requirement_Document | | | |
| AG-19 | Open questions Q1–Q5 are listed as open assumptions and not treated as final design decisions | Must | A8, Open Questions | | | |
| AG-20 | Traceability table maps containers / paths to FR-01..FR-11 | Must | A9 | | | |
| AG-21 | Optional L3 view, if present, drills one container without mixing context names and internal modules incorrectly | Should | A10 | | | |
| AG-22 | Mobile app is channel-only and does not perform core banking posting or credit evaluation on its own | Should | Domain scope | | | |
| AG-23 | The architecture distinguishes near-real-time scoring from asynchronous accounting and reconciliation flows | Should | NFR-01, NFR-03, FR-03, FR-10 | | | |
| AG-24 | Security boundary and authN/authZ are implied at the app, API/service, and external integration edges | Should | NFR-04 | | | |

---

## Traceability table (required in the architecture pack)

Copy into the architecture pack. Reviewer fails AG-20 if any requirement lacks a container or path.

| Requirement | Container(s) / path | Notes |
|---|---|---|
| FR-01 Loan application submission | Mobile App → Loan Application Service | Channel submission and validation |
| FR-02 Eligibility assessment | Loan Application Service → Policy Engine / Decision Engine | Evaluate customer data and eligibility |
| FR-03 Credit scoring integration | Loan Application Service / Decision Engine → Credit Scoring Adapter → Credit Scoring System | Near-real-time score retrieval |
| FR-04 Maximum eligible amount calculation | Policy Engine / Decision Engine | Policy-based max eligible amount |
| FR-05 Personalized interest rate | Policy Engine / Decision Engine | Score-driven pricing |
| FR-06 Offer recommendation | Decision Engine → Mobile App | Present limit + rate |
| FR-07 Auto decisioning | Decision Engine → Loan Decision Store | Approve/reject within policy |
| FR-08 Limit increase recommendation | Decision Engine / Policy Engine | Eligible existing-customer logic |
| FR-09 Immediate disbursement | Decision Engine → Disbursement Adapter → ESB → Core Banking | Only after approval and validation |
| FR-10 Accounting integration | Loan Application Service / Disbursement Adapter → ESB → Core Banking | Ledger and posting flow |
| FR-11 Decision traceability | Decision Engine → Decision Store + Audit Log | Persist policy basis, score, calculations |

---

## NFR allowed in this pack

Do not add rows beyond this table unless Requirement_Document.md changes.

| ID | Allowed statement |
|---|---|
| NFR-01 | Loan decisioning must be near real time to support a smooth mobile experience. |
| NFR-02 | The lending service must remain available during business-critical processing periods. |
| NFR-03 | The platform must minimize incorrect decisions and failed accounting flows. |
| NFR-04 | Customer data must be protected with strong authentication, authorization, and compliance controls. |
| NFR-05 | Decision events, integrations, and transaction outcomes must be auditable and explainable. |
| NFR-06 | Data consistency must be preserved across customer records, scoring, decisions, and banking ledger entries. |
| NFR-07 | The platform must scale to support increasing mobile loan demand without latency degradation. |
| NFR-08 | The solution must comply with risk, privacy, and financial regulatory requirements. |

---

## Open assumptions to carry forward

These are the open questions from the requirements pack and may remain open unless the product owner changes the requirements.

| ID | Open question | Why it matters |
|---|---|---|
| Q1 | Exact eligibility and affordability rules for salaried customers age 22–35 | Needed for policy and decision threshold definition |
| Q2 | Exact score thresholds for approve / reject / review / limit increase | Needed for automated decision rules |
| Q3 | Required data fields from the credit scoring system | Needed for interface contract and adapter design |
| Q4 | Which payment account is used for disbursement in initial rollout | Needed for validation and disbursement logic |
| Q5 | Numeric SLA targets for response time and availability | Needed for performance and operational design |

---

## Architecture guidance for this product

The architecture pack should emphasize the following facts from the domain and requirements:

- The product is mobile-first and designed for existing salaried customers in the age band 22–35.
- The system is for unsecured loans, capped at 100,000,000 VND.
- The platform evaluates a customer’s eligibility, obtains a near-real-time credit score, calculates maximum eligible amount, determines a personalized interest rate, and presents an offer.
- Auto decisioning is a central business capability and must be traceable through stored decision artifacts.
- Immediate disbursement is allowed only after approval and account validation.
- Accounting and ledger updates are sent through the ESB layer to Core Banking.
- High-risk or policy-violating cases should trigger reject or review logic, not silent approval.

The architecture should show the loan system as a bounded platform with explicit external systems and a clear decisioning boundary, while keeping business process and exception handling visible rather than hidden inside a single box.

---

## Minimal architecture shape

A compliant architecture pack should be able to describe the following flow:

1. Customer submits a loan application through the mobile app.
2. The loan application service validates the request.
3. The decision engine or policy engine checks eligibility and policy constraints.
4. The credit scoring adapter requests a near-real-time score from the external system.
5. The decision engine calculates the eligible amount and personalized rate.
6. The system generates a recommendation or approval decision.
7. If approved, the disbursement adapter validates the account and posts to Core Banking via ESB.
8. The decision, score, policy basis, and amount are stored for traceability and audit.

This flow is the backbone of the architecture evidence used to pass Gate G3.
