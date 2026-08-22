# Lab 9 - C4 Context and Container

**Status:** Lab 9 after-pack architecture specification - Draft.  
**Primary sources:** Lab 1, Lab 2, Lab 3, Lab 4, Lab 7, and Lab 8.  
**Scope assumption:** Lab 5 and Lab 6 are not required inputs for this artifact.  
**Required gate:** G3 - C4 Context + Container.  
**RACI:** Artifact-specific assignments are defined in each view header.

## 1. Scope and modeling rules

This file defines exactly one C4 Context view (L1), one C4 Container view (L2), and one optional C4 Component view (L3) inside the selected `Decision Engine` container.

- C4 Context contains people, the system-in-focus, and named external systems only.
- C4 Container contains the system-in-focus, all named I-4 internal containers, and named external systems where needed.
- C4 Component contains internals of `Decision Engine` only.
- All names resolve to the Lab 1 identity index and Lab 4 cleanup baseline.
- Lab 5 and Lab 6 are not required inputs under the agreed scope assumption.
- No new person, external system, container, component, database, product, host, or runtime environment is introduced.
- C4 relationships describe what happens. Protocol and sync/async labels appear only on the Container view, not the Context view.

## 2. Shared identity index

### 2.1 Person

- `Customer`

`Loan Operations Specialist` is a named actor in Lab 1 but is not part of the standard application path. It may be shown only as an optional exception/reconciliation user if needed; it is not required on the single standard Context path.

### 2.2 System-in-focus

- `Nopbai Personal Loan Platform`

### 2.3 External systems

- `Credit Scoring System`
- `ESB Integration Layer`
- `Core Banking`

### 2.4 Internal containers

- `Mobile App`
- `Loan Application Service`
- `Credit Scoring Adapter`
- `Decision Engine`
- `Policy Engine`
- `Account Validation Service`
- `Disbursement Adapter`
- `Decision Store`
- `Audit Log`

### 2.5 Selected Component container

- `Decision Engine`

Only this container may be expanded at Component level.

## 3. C4 Context - L1

### 3.1 Header

```text
Title:      Nopbai Personal Loan Platform - C4 Context
Viewpoint:  C4 Context (L1)
Layer(s):   System context
As-Is | To-Be | Transition:  To-Be
Owner:      SA - Vũ Thế Quân
RACI:       R SA - Vũ Thế Quân
            A Owner - Nguyễn Minh Hoàng
            C EA - Nguyễn Cương Quyết (TN); BA/Test - Lý Bá Duy
            I Dev - Nguyễn Thanh Hải
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     person, system-in-focus, external system, and business relationship
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      Nopbai Mobile Personal Loan standard journey
```

### 3.2 Elements to draw

| Element | Type | Description |
|---------|------|-------------|
| `Customer` | Person | Applies for a loan, reviews a Loan Offer, accepts the Nopbai Personal Loan Agreement, and receives the decision/disbursement outcome |
| `Loan Operations Specialist` | Person | Reviews policy exceptions and reconciliation cases; not part of the standard approval path |
| `Nopbai Personal Loan Platform` | Software system | Captures the application, performs policy-controlled decisioning, creates the Loan Offer, validates the payment account, and coordinates disbursement |
| `Credit Scoring System` | External software system | Returns a near-real-time Credit Score for an existing customer |
| `ESB Integration Layer` | External software system | Routes accounting and disbursement messages between the platform and Core Banking |
| `Core Banking` | External software system | Validates the payment account and records ledger and disbursement outcomes |

### 3.3 Relationships to draw

| Source | Target | Relationship label |
|--------|--------|-------------------|
| `Customer` | `Nopbai Personal Loan Platform` | Submits a Loan Application, reviews a Loan Offer, accepts the agreement, and receives the decision |
| `Loan Operations Specialist` | `Nopbai Personal Loan Platform` | Reviews policy exceptions and reconciliation cases |
| `Nopbai Personal Loan Platform` | `Credit Scoring System` | Obtains a Credit Score for loan decisioning |
| `Nopbai Personal Loan Platform` | `ESB Integration Layer` | Sends disbursement and accounting requests for routing |
| `ESB Integration Layer` | `Core Banking` | Routes payment-account and disbursement/accounting interactions |
| `Core Banking` | `Nopbai Personal Loan Platform` | Returns account validation and disbursement/accounting outcomes |

### 3.4 Context boundaries

The Context view must not show:

- `Mobile App`, `Loan Application Service`, or any other internal container.
- `Decision Engine` modules or Component names.
- Databases, deployment locations, pods, clusters, or infrastructure products.
- HTTPS, message, sync, async, OpenAPI, or contract details.
- UML lifelines, state transitions, test IDs, or ArchiMate elements.

The Context view contains no container internals. It shows the system boundary and named external relationships only.

## 4. C4 Container - L2

### 4.1 Header

```text
Title:      Nopbai Personal Loan Platform - C4 Containers
Viewpoint:  C4 Container (L2)
Layer(s):   System decomposition
As-Is | To-Be | Transition:  To-Be
Owner:      SA - Vũ Thế Quân
RACI:       R SA - Vũ Thế Quân
            A EA - Nguyễn Cương Quyết (TN)
            C Dev - Nguyễn Thanh Hải; BA/Test - Lý Bá Duy
            I Owner - Nguyễn Minh Hoàng
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     person, container, external system, protocol, and sync/async relationship
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      all I-4 containers and required I-3 external systems
```

### 4.2 Containers to draw

| Container | Type | Responsibility |
|-----------|------|----------------|
| `Mobile App` | Internal container | Captures applications, displays Loan Offers and decisions, and collects agreement acceptance |
| `Loan Application Service` | Internal container | Validates and manages submitted Loan Applications |
| `Credit Scoring Adapter` | Internal container | Requests and normalizes responses from `Credit Scoring System` |
| `Decision Engine` | Internal container | Orchestrates eligibility, score, policy, offer, and approval or rejection decisions |
| `Policy Engine` | Internal container | Applies configurable eligibility, amount, rate, and approval rules |
| `Account Validation Service` | Internal container | Confirms that the customer payment account is eligible before disbursement |
| `Disbursement Adapter` | Internal container | Creates an idempotent disbursement request and handles the posting outcome |
| `Decision Store` | Internal container | Persists score, policy basis, calculations, Loan Offers, and Decision Records |
| `Audit Log` | Internal container | Persists decision, integration, and transaction evidence |
| `Credit Scoring System` | External system | Returns a near-real-time Credit Score |
| `ESB Integration Layer` | External system | Routes accounting and disbursement messages |
| `Core Banking` | External system | Validates the payment account and records ledger and disbursement outcomes |

### 4.3 Container relationships

| Source | Target | Protocol / mode | Relationship label and purpose |
|--------|--------|-----------------|-------------------------------|
| `Customer` | `Mobile App` | User interaction | Submits a Loan Application, reviews a Loan Offer, and accepts the agreement |
| `Mobile App` | `Loan Application Service` | HTTPS / Sync | Sends application data for validation and lifecycle management |
| `Loan Application Service` | `Decision Engine` | HTTPS / Sync | Starts eligibility and decisioning |
| `Decision Engine` | `Credit Scoring Adapter` | HTTPS / Sync | Requests a normalized Credit Score |
| `Credit Scoring Adapter` | `Credit Scoring System` | HTTPS / Sync | Requests and receives a near-real-time Credit Score |
| `Decision Engine` | `Policy Engine` | HTTPS / Sync | Requests maximum amount, personalized rate, and policy evaluation |
| `Decision Engine` | `Decision Store` | Internal call / Sync | Persists score, policy basis, calculations, Loan Offer, and Decision Record |
| `Decision Engine` | `Audit Log` | Internal call / Sync | Records decision and integration evidence |
| `Decision Engine` | `Mobile App` | HTTPS / Sync | Returns the Loan Offer and decision outcome |
| `Mobile App` | `Account Validation Service` | HTTPS / Sync | Sends the account-validation request after Customer accepts the agreement |
| `Account Validation Service` | `Core Banking` | HTTPS / Sync | Requests payment-account eligibility confirmation |
| `Account Validation Service` | `Disbursement Adapter` | Internal call / Sync | Allows disbursement only after successful account validation |
| `Disbursement Adapter` | `ESB Integration Layer` | Message / Async | Sends disbursement and accounting request |
| `ESB Integration Layer` | `Core Banking` | Message / Async | Routes the posting and disbursement request |
| `Core Banking` | `ESB Integration Layer` | Message / Async | Returns posting and disbursement confirmation or failure |
| `ESB Integration Layer` | `Disbursement Adapter` | Message / Async | Returns the routed banking outcome |

### 4.4 Required constraints on the Container view

- `CON.1`: the `Decision Engine` and `Policy Engine` relationship must support rejection when the unsecured amount exceeds 100,000,000 VND.
- `CON.2`: the `Loan Application Service` and `Decision Engine` relationship must reject an out-of-segment customer before decisioning.
- `CON.3`: the `Credit Scoring Adapter` and `Credit Scoring System` relationship must show a controlled timeout/failure path; it cannot approve without a Credit Score.
- `CON.4`: the path must be `Account Validation Service` -> `Disbursement Adapter` -> `ESB Integration Layer` -> `Core Banking`; no direct `Mobile App` -> `Core Banking` path is allowed.
- `CON.5`: `Decision Store` and `Audit Log` must be included as evidence boundaries for protected and auditable decision data.

### 4.5 Container boundaries

The Container view must not:

- Expand more than one container.
- Show modules inside `Decision Engine` or any other container.
- Add a gateway, event bus, IAM product, database product, vendor, pod, cluster, or host.
- Rename an I-4 container or I-3 external system.
- Use an unnamed external system.
- Draw a direct `Mobile App` to `Core Banking` relationship.

## 5. C4 Component - L3 - optional Decision Engine view

This optional view is included because Lab 1 I-11 selects `Decision Engine`. It is one Component view only and does not expand any other container.

### 5.1 Header

```text
Title:      Decision Engine - C4 Components
Viewpoint:  C4 Component (L3)
Layer(s):   One-container design
As-Is | To-Be | Transition:  To-Be
Owner:      Dev - Nguyễn Thanh Hải
RACI:       R Dev - Nguyễn Thanh Hải
            A SA - Vũ Thế Quân
            C BA/Test - Lý Bá Duy
            I Owner - Nguyễn Minh Hoàng; EA - Nguyễn Cương Quyết (TN)
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     component, black-box neighbour, and internal relationship
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      internals of `Decision Engine` only
```

### 5.2 Components to draw

| Component inside `Decision Engine` | Responsibility |
|------------------------------------|----------------|
| Decision Orchestrator | Controls the decision flow and state outcome |
| Eligibility Evaluator | Checks the initial customer segment and eligibility result |
| Score Coordinator | Requests the Credit Score and handles success or timeout input |
| Policy Evaluation Module | Requests maximum amount, personalized rate, and policy outcome |
| Offer Builder | Creates the customer-facing Loan Offer from score and policy results |
| Decision Recorder | Persists decision evidence and sends audit events |

### 5.3 Black-box neighbours

The following are shown as black-box neighbours, not expanded:

- `Loan Application Service`
- `Credit Scoring Adapter`
- `Policy Engine`
- `Mobile App`
- `Decision Store`
- `Audit Log`

`Credit Scoring System`, `ESB Integration Layer`, and `Core Banking` remain outside this Component boundary. `Decision Engine` does not call `Credit Scoring System` or `Core Banking` directly.

### 5.4 Component relationships

| Source | Target | Relationship |
|--------|--------|--------------|
| Decision Orchestrator | Eligibility Evaluator | Requests eligibility evaluation |
| Decision Orchestrator | Score Coordinator | Starts score collection |
| Decision Orchestrator | Policy Evaluation Module | Starts policy evaluation |
| Policy Evaluation Module | Offer Builder | Supplies accepted score and policy terms |
| Offer Builder | Decision Recorder | Supplies Loan Offer and decision evidence |
| Decision Recorder | `Decision Store` | Persists Loan Offer and Decision Record |
| Decision Recorder | `Audit Log` | Records decision and integration evidence |
| Eligibility Evaluator | `Loan Application Service` | Receives application eligibility input |
| Score Coordinator | `Credit Scoring Adapter` | Requests normalized Credit Score |
| Policy Evaluation Module | `Policy Engine` | Requests policy calculation and decision |
| Decision Orchestrator | `Mobile App` | Returns decision and Loan Offer |

## 6. G3 evidence and open points

### 6.1 G3 evidence

| G3 rule | Evidence |
|---------|----------|
| No unnamed externals | Context and Container use only the three I-3 external systems |
| Sync/async labeled | Container relationships label HTTPS/Sync and Message/Async where required |
| Names match Input index | All containers and external systems use exact Lab 1 strings |
| Context has no internals | L1 contains only `Customer`, the system-in-focus, and external systems |
| One Component container | L3 expands `Decision Engine` only |
| Forbidden path controlled | No direct `Mobile App` -> `Core Banking` relationship is defined |

### 6.2 Open points

- Exact protocol details remain unresolved; `HTTPS` and message labels are design assumptions from Lab 1 I-8, not production contracts.
- Exact authentication and authorization mechanism remains governed by `CON.5` and is not expanded into a new product.
- Availability, capacity, and regulatory targets from the supporting Requirement Document remain outside the current approved baseline.

**G3 status:** **Pending** SA/EA review. This file is architecture design evidence, not implementation or runtime proof.

## 7. Lab 9 completion check

- [x] Exactly one C4 Context (L1) specification is present.
- [x] Exactly one C4 Container (L2) specification is present.
- [x] Optional Component view expands `Decision Engine` only.
- [x] Context contains people, system-in-focus, and named externals only.
- [x] Container contains all nine I-4 containers and the three I-3 external systems.
- [x] Container relationships identify protocol and Sync/Async mode.
- [x] All names match the Lab 1 identity index and Lab 4 baseline.
- [x] The forbidden direct `Mobile App` -> `Core Banking` path is explicitly excluded.
- [x] Each view has a header, legend, scope, and one RACI assignment.
- [x] No new external system, product, database, host, pod, or cluster is introduced.
- [ ] G3 formally approved by SA/EA.

**Current result:** Lab 9 is complete as a Draft architecture specification. G3 remains **Pending** until SA/EA review and approval.
