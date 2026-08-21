# Analysis — Mobile Personal Loan Product

## Purpose
Summarize and analyze the requirements in `Requirement_Document.md` and map them into a modeling-driven design approach following the `list.md` Guide. This analysis is intended to feed Lab 2 (requirements + analysis) and the subsequent architecture pack (ArchiMate → C4 → UML).

## Executive Summary
- Objective: deliver a mobile-first unsecured personal loan for salaried customers (age 22–35) with near real-time automated decisions, personalized offers, and immediate disbursement.
- Key constraints: unsecured loans only, max 100,000,000 VND, credit scoring is external and near real-time, Core Banking + ESB integration required.
- Priorities: reliable auto decisioning, secure accounting integration, decision traceability, and low-latency responses.

## Requirements (condensed)
- FR-01 Loan application submission — mobile app channel.
- FR-02 Eligibility assessment — uses customer & credit data.
- FR-03 Credit scoring integration — near real-time score retrieval.
- FR-04 Max eligible amount calculation — policy-based computation.
- FR-05 Personalized interest rate — score-driven pricing.
- FR-06 Offer recommendation — present limit + rate.
- FR-07 Auto decisioning — automated approve/reject within policy.
- FR-08 Limit increase recommendation — for eligible existing customers.
- FR-09 Immediate disbursement — on successful approval and account validation.
- FR-10 Accounting integration — post entries to Core Banking via ESB.
- FR-11 Decision traceability — store score, policy basis, calculations.

## Non-Functional Summary
- NFR-01 Performance: near real-time decisioning (target SLA TBD).
- NFR-02 Availability: support customer transactions during business-critical times.
- NFR-03 Reliability: minimize incorrect decisions and failed accounting flows.
- NFR-04 Security: protect customer data; strong AuthN/AuthZ.
- NFR-05 Auditability: logs for decisions, integrations, transactions.
- NFR-06 Data integrity: consistency across scoring, decisions, ledger.
- NFR-07 Scalability: handle growing mobile requests without latency degradation.
- NFR-08 Compliance: meet risk, privacy, and regulatory rules.

## Traceability (high level)
- Each FR traces to the Business Objective(s): accelerate approvals, personalize offers, integrate accounting.
- FR-03, FR-04, FR-05, FR-07, FR-11 directly depend on the external Credit Scoring System and the policy configuration.
- FR-09 and FR-10 depend on Core Banking + ESB availability and account validation rules.

## Mapping to Modeling Languages (per `list.md` Guide)
- ArchiMate (top/why): Motivation, business capabilities, governance, constraints (useful for G1 evidence).
- C4 (middle/what): C4 Context (system-in-focus + externals) and C4 Container (lending app, scoring adapter, ESB integrator, accounting adapter, mobile app). Label sync vs async on integrations.
- UML (base/how): Sequence diagrams for the happy + exception paths (loan submit → scoring → decision → disbursement), state machine for the loan application object, activity for business process.

## Suggested Artifacts (Lab 2 deliverables)
- Requirements list (this file + a structured CSV/MD table) tracing each FR → Goal / Business Rule / process step.
- Analysis document (this file) covering As-Is, To-Be, capabilities, exceptions, and modeling choices.
- Gate register (G1–G6) with pass rules and evidence pointers (ArchiMate view, C4 Pack, UML sequences).
- Trace table: requirement ID → process step → CON.* → named object/state.

## Suggested RACI (artifact-level)
- Requirements / Analysis: R = BA · A = Owner · C = EA, SA · I = Dev, Test, Ops.
- C4 Context + Container: R = SA · A = Owner · C = Dev, Sec, Ops.
- UML sequences / State: R = Dev/Test · A = SA · C = BA.

## Gate Register (G1–G6) — proposed pass rules and evidence
- G1 Strategy signed: Pass rule — Owner approves Motivation & measurable outcomes; Evidence — ArchiMate Motivation view and this analysis.
- G2 Process + states: Pass rule — BA/Test sign-off on named states and business process; Evidence — Business Process (ArchiMate/UML Activity) + State machine.
- G3 C4 Context + Container: Pass rule — SA/Owner sign-off, names match Input index; Evidence — C4 Context + Container diagrams, integration labels.
- G4 Contracts: Pass rule — Contract (OpenAPI or equivalent) exists for every container relationship on Container diagram; Evidence — API contract doc + interface list.
- G5 Critical exception path: Pass rule — exception and compensating actions modeled for critical failures; Evidence — UML sequence alt paths and activity compensations.
- G6 Test coverage: Pass rule — planned tests for each alt + state transition; Evidence — G6 checklist mapping transitions → test scenarios.

## Analysis: As-Is vs To-Be (brief)
- As-Is: existing customers with account data; credit scoring available externally; manual underwriting currently slows decisions (implicit from goals).
- To-Be: mobile-first flow with automated score-driven decisioning, immediate disbursement, and integrated accounting entries; decision traceability for audit and dispute resolution.

## Key Exception Paths (to model)
- Scoring unavailable / timeout — fallback: queue + manual review or soft-decline (define policy).
- Account validation fails — reject with remediation steps; no disbursement.
- Accounting post fails — compensate: reverse disbursement if posted; ensure idempotent posting and reconciliation.
- Policy breach (e.g., amount > cap) — escalate to manual review; log and audit.

## Open Questions & Actions (from `Requirement_Document.md`)
- Q1: Exact eligibility and affordability rules for the 22–35 salaried segment. (Action: BA to define CON.* rules)
- Q2: Exact scoring thresholds for approve / reject / review / limit increase. (Action: Risk to provide threshold table)
- Q3: Required data fields from the credit scoring system. (Action: Integration design to request schema)
- Q4: Which payment account is used for disbursement in initial rollout. (Action: Product decision)
- Q5: SLA targets for response time and availability. (Action: Ops to propose numeric SLAs)

## Prioritization (recommended)
1. FR-03 Credit scoring integration — blocker for auto decisioning.
2. FR-07 Auto decisioning — business value (fast decisions).
3. FR-09 Immediate disbursement + FR-10 Accounting integration — must be reliable and atomic.
4. FR-11 Decision traceability — compliance and audit.
5. FR-04/FR-05 Offer calculations and pricing.

## Data & Integration Notes
- Design all external integrations (Credit Scoring, Core Banking, ESB) as explicit C4 Containers. Mark sync vs async (scoring: sync/near-real-time; accounting: async with confirmation). Use contracts for every integration.
- Ensure idempotency and reconciliation for accounting postings (use unique transaction IDs).

## Risks & Mitigations
- Risk: Scoring latency causes poor UX. Mitigation: set timeouts, fallback messaging, and queue-to-manual workflows.
- Risk: Incorrect accounting postings. Mitigation: idempotent posts, two-phase confirmations, and reconciliation jobs.
- Risk: Policy misconfiguration leads to erroneous approvals. Mitigation: policy configuration CI with gated rollout and audit logs.

## Next steps (recommended immediate tasks)
1. Confirm the CON.* constraints and scoring thresholds (BA + Risk).  
2. Define the exact credit-scoring payload & response schema (Integration owner).  
3. Draft C4 Context and Container diagrams (SA) for G3 evidence.  
4. Draft UML sequence for the loan application happy path + key alts (Dev/Test).  
5. Produce Gate register entries with evidence pointers (Owner, BA, SA).  

## Appendix: High-level Trace Table (example)
| Req ID | Requirement | Process Step | Constraint / Business Rule |
|---|---|---|---|
| FR-01 | Loan application submission | App submit → validate input | Must be existing customer |
| FR-03 | Credit scoring integration | Call scoring service | Scoring available near real time |
| FR-07 | Auto decisioning | Decision engine applies policy | Max loan ≤ 100M VND; policy thresholds |
| FR-09 | Immediate disbursement | Disburse → post accounting | Account validated; idempotent posting |
| FR-11 | Decision traceability | Persist decision artifacts | Store score, policy ID, computed amount |

---
Prepared to convert this analysis into the Lab 2 deliverables (requirements table, gate register, trace table) and to produce the ArchiMate / C4 / UML artifacts per the Guide.
