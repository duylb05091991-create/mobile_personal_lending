# Lab 8 - ArchiMate views (named set)

**Status:** Lab 8 after-pack view specification - Draft.  
**Primary sources:** Lab 1, Lab 2, Lab 3, Lab 4, and Lab 7.  
**Scope rule:** Lab 5 and Lab 6 are not required inputs under the agreed Lab 7 scope.  
**Language rule:** Each view uses ArchiMate only. C4 containers, UML lifelines, protocols, and test IDs are not drawn as elements in these views.

## 1. View set and gate placement

| # | Named view | Question answered | Required gate | Status |
|---|------------|------------------|---------------|--------|
| 1 | Motivation | Why is the change needed and what constrains it? | G1 | Pending Owner review |
| 2 | Business Process | What business steps and decisions occur? | G2 | Pending BA/Test review |
| 3 | Application Cooperation | Which application containers cooperate? | No new gate; supports G3 | Draft |
| 4 | Technology / hybrid | Where are the named elements deployed and what path is forbidden? | Supports G3 | Draft |

These are four named views, not an all-layer model. Names must resolve to the Lab 1 identity index and Lab 4 cleanup baseline.

## 2. Shared naming and modeling rules

- System-in-focus: `Nopbai Personal Loan Platform`.
- Product: `Nopbai Mobile Personal Loan`.
- Actors: `Customer`; `Loan Operations Specialist`.
- External systems: `Credit Scoring System`; `ESB Integration Layer`; `Core Banking`.
- Internal application containers: `Mobile App`; `Loan Application Service`; `Credit Scoring Adapter`; `Decision Engine`; `Policy Engine`; `Account Validation Service`; `Disbursement Adapter`; `Decision Store`; `Audit Log`.
- Business process object: `Loan Application`.
- Named states are not drawn as application containers; the process view may reference outcomes using the exact strings `Draft`, `Submitted`, `Scoring`, `OfferReady`, `Approved`, `AccountValidated`, `Rejected`, `Disbursed`, and `Failed`.
- Constraints are exactly `CON.1` through `CON.5`.
- Do not add a gateway, event bus, IAM product, vendor, production host, database product, pod, or credential.
- Do not use UML sequence messages, C4 notation, test IDs, or component internals in these ArchiMate views.

## 3. View 1 - Motivation

### 3.1 Header

```text
Title:      Nopbai Mobile Personal Loan - Motivation
Viewpoint:  ArchiMate Motivation
Layer(s):   Motivation
As-Is | To-Be | Transition:  To-Be
Owner:      EA - Nguyễn Cương Quyết (TN)
RACI:       R EA - Nguyễn Cương Quyết (TN)
            A Owner - Nguyễn Minh Hoàng
            C BA/Test - Lý Bá Duy; SA - Vũ Thế Quân
            I Dev - Nguyễn Thanh Hải
Version:    v1.0  Date 2026-08-21  Status Draft
Legend:     influence, association, realization, constraint relationships listed below
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      in-scope / out-of-scope from Lab 1 I-1
```

### 3.2 Elements to show

| Element type | Exact element or text | Meaning |
|--------------|-----------------------|---------|
| Assessment | Manual or fragmented assessment | Current pain/baseline from I-1 |
| Goal | Provide a mobile-first unsecured personal loan journey with automated, policy-controlled decisioning and immediate disbursement. | Change goal from I-1 |
| Outcome | **ASSUMPTION:** Return an automated loan decision within P95 <= 30 seconds for standard applications. | Measurable outcome from I-1 |
| Capability | Mobile loan application capture | Implied by the goal |
| Capability | Eligibility and policy decisioning | Implied by the goal and constraints |
| Capability | Near-real-time credit assessment | Implied by CON.3 and the outcome |
| Capability | Offer and limit recommendation | In-scope outcome |
| Capability | Controlled account validation and disbursement | Implied by CON.4 |
| Capability | Decision traceability | Implied by CON.5 |
| Constraint | `CON.1` Unsecured loan amount must not exceed 100,000,000 VND. | Amount cap |
| Constraint | `CON.2` Only existing salaried customers aged 22-35 are in the initial segment. | Initial customer boundary |
| Constraint | `CON.3` Credit scoring must return near-real-time data; timeout is a controlled exception. | Scoring control |
| Constraint | `CON.4` No disbursement or accounting posting before approval and successful account validation. | Disbursement control |
| Constraint | `CON.5` Customer data and decision evidence must be protected and auditable. | Security/audit control |

### 3.3 Relationships to show

- `Manual or fragmented assessment` influences the Goal as the reason for change.
- The Goal realizes the target state represented by `Nopbai Mobile Personal Loan`.
- The Goal realizes the six named capabilities.
- `CON.1` constrains `Eligibility and policy decisioning` and `Offer and limit recommendation`.
- `CON.2` constrains `Mobile loan application capture` and `Eligibility and policy decisioning`.
- `CON.3` constrains `Near-real-time credit assessment`.
- `CON.4` constrains `Controlled account validation and disbursement`.
- `CON.5` constrains `Decision traceability`.
- The Outcome is associated with `Near-real-time credit assessment` and `Eligibility and policy decisioning`.

### 3.4 View 1 boundary

Must show Goal, Outcome, capabilities, baseline pain, and `CON.1` through `CON.5`. Must not show protocols, containers, deployment locations, UML messages, database products, pods, or component internals.

**G1 evidence:** Goal, Outcome, and all five constraints are explicitly listed. G1 remains **Pending** until Owner approval.

## 4. View 2 - Business Process

### 4.1 Header

```text
Title:      Nopbai Mobile Personal Loan - Business Process
Viewpoint:  ArchiMate Business Process
Layer(s):   Business
As-Is | To-Be | Transition:  To-Be
Owner:      BA/Test - Lý Bá Duy
RACI:       R BA/Test - Lý Bá Duy
            A Owner - Nguyễn Minh Hoàng
            C EA - Nguyễn Cương Quyết (TN); SA - Vũ Thế Quân
            I Dev - Nguyễn Thanh Hải
Version:    v1.0  Date 2026-08-21  Status Draft
Legend:     triggering, sequencing, branching, realization, and constraint relationships listed below
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      standard unsecured loan journey in Lab 1 I-1
```

### 4.2 Process elements and sequence

| Order | Business process step | Business actor/object | Expected state or outcome |
|------:|------------------------|-----------------------|---------------------------|
| 1 | Submit Loan Application | `Customer`; `Loan Application` | `Draft -> Submitted` |
| 2 | Validate Loan Application and customer segment | `Loan Application`; `Customer` | `Submitted -> Scoring` or `Submitted -> Rejected` |
| 3 | Assess Credit Score and policy eligibility | `Credit Score`; `Policy Configuration` | `Scoring -> OfferReady` or `Scoring -> Failed` |
| 4 | Create and present Loan Offer | `Loan Offer`; `Customer` | `OfferReady` |
| 5 | Accept Nopbai Personal Loan Agreement | `Customer`; `Nopbai Personal Loan Agreement` | `OfferReady -> Approved` or `OfferReady -> Rejected` |
| 6 | Validate payment account | `Customer Profile`; payment account | `Approved -> AccountValidated` or `Approved -> Failed` |
| 7 | Disburse and record accounting outcome | `Disbursement Record` | `AccountValidated -> Disbursed` or `AccountValidated -> Failed` |

### 4.3 Decision branches and constraints

- At step 2, apply `CON.2`: an out-of-segment customer follows `Submitted -> Rejected`; no decisioning continues.
- At step 3, apply `CON.3`: unavailable or timed-out scoring follows `Scoring -> Failed`; no approval occurs.
- At step 3 or 4, apply `CON.1`: an amount above 100,000,000 VND follows `OfferReady -> Rejected`; no approval occurs.
- At step 6 and 7, apply `CON.4`: no disbursement or accounting posting occurs before approval and successful account validation.
- Across all steps, apply `CON.5`: customer data and decision evidence are protected and auditable.
- Customer decline at step 5 follows `OfferReady -> Rejected` and stops account validation.

### 4.4 Process relationships

- `Customer` triggers `Submit Loan Application` and participates in `Accept Nopbai Personal Loan Agreement`.
- The business processes follow the sequence 1 through 7.
- Each decision branch realizes the corresponding exact state transition.
- `CON.1` through `CON.5` constrain the relevant process decisions.
- The process realizes the Goal from View 1.

### 4.5 View 2 boundary

Must show the happy-path business process, business object movement, decision branches, and `CON.*`. Must not show C4 containers as process boxes, sync/async labels, HTTPS, message contracts, UML lifelines, modules, or test IDs.

**G2 evidence:** the process uses the exact I-6 states and includes all decision branches defined by Lab 1 and Lab 2. G2 remains **Pending** until BA/Test approval.

## 5. View 3 - Application Cooperation

### 5.1 Header

```text
Title:      Nopbai Mobile Personal Loan - Application Cooperation
Viewpoint:  ArchiMate Application Cooperation
Layer(s):   Application
As-Is | To-Be | Transition:  To-Be
Owner:      SA - Vũ Thế Quân
RACI:       R SA - Vũ Thế Quân
            A EA - Nguyễn Cương Quyết (TN)
            C Dev - Nguyễn Thanh Hải; BA/Test - Lý Bá Duy
            I Owner - Nguyễn Minh Hoàng
Version:    v1.0  Date 2026-08-21  Status Draft
Legend:     application cooperation, serving, access, and flow relationships listed below
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      I-4 internal containers and I-3 external systems only
```

### 5.2 Application elements

**Internal application components, using exact I-4 strings:**

- `Mobile App`
- `Loan Application Service`
- `Credit Scoring Adapter`
- `Decision Engine`
- `Policy Engine`
- `Account Validation Service`
- `Disbursement Adapter`
- `Decision Store`
- `Audit Log`

**External application systems, using exact I-3 strings:**

- `Credit Scoring System`
- `ESB Integration Layer`
- `Core Banking`

### 5.3 Relationships to show

| Producer / source | Consumer / target | Relationship | Meaning |
|-------------------|-------------------|--------------|---------|
| `Customer` | `Mobile App` | Uses | Customer submits applications, reviews Loan Offers, and accepts the agreement |
| `Mobile App` | `Loan Application Service` | Serves / flows to | Application capture and validation request |
| `Loan Application Service` | `Decision Engine` | Serves / flows to | Starts eligibility and decisioning |
| `Decision Engine` | `Credit Scoring Adapter` | Serves / flows to | Requests normalized scoring |
| `Credit Scoring Adapter` | `Credit Scoring System` | Serves / flows to | Retrieves a near-real-time Credit Score |
| `Decision Engine` | `Policy Engine` | Serves / flows to | Requests amount, rate, and policy evaluation |
| `Decision Engine` | `Mobile App` | Serves / flows to | Returns Loan Offer and decision |
| `Decision Engine` | `Decision Store` | Accesses / flows to | Persists score, policy basis, calculations, Loan Offer, and Decision Record |
| `Decision Engine` | `Audit Log` | Accesses / flows to | Records decision and integration evidence |
| `Customer` | `Account Validation Service` | Uses / triggers | Account validation follows agreement acceptance |
| `Account Validation Service` | `Disbursement Adapter` | Serves / flows to | Allows disbursement only after successful validation |
| `Disbursement Adapter` | `ESB Integration Layer` | Serves / flows to | Sends disbursement and accounting request |
| `ESB Integration Layer` | `Core Banking` | Serves / flows to | Routes request and confirmation to Core Banking |
| `Core Banking` | `Account Validation Service` | Serves / flows to | Confirms payment account eligibility |
| `Core Banking` | `Disbursement Adapter` | Serves / flows to | Returns posting and disbursement outcome |
| `Decision Store` | `Audit Log` | Associated evidence flow | Evidence is retained for traceability where applicable |

### 5.4 Application view boundary

The view must contain only named application components/systems and their cooperation relationships. Do not show modules such as `Decision Orchestrator`, deployment locations, database products, UML messages, or protocol labels. Do not rename an I-4 container.

**G3 support:** this view establishes the application name identity used later by C4. G3 is not passed by this view alone and remains **Pending**.

## 6. View 4 - Technology / hybrid

### 6.1 Header

```text
Title:      Nopbai Mobile Personal Loan - Technology and Deployment
Viewpoint:  ArchiMate Technology / hybrid
Layer(s):   Technology and Application deployment
As-Is | To-Be | Transition:  To-Be
Owner:      Dev - Nguyễn Thanh Hải
RACI:       R Dev - Nguyễn Thanh Hải
            A SA - Vũ Thế Quân
            C EA - Nguyễn Cương Quyết (TN); BA/Test - Lý Bá Duy
            I Owner - Nguyễn Minh Hoàng
Version:    v1.0  Date 2026-08-21  Status Draft
Legend:     deployment, assignment, communication path, and forbidden path listed below
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      I-9 locations and assigned I-4/I-3 elements
```

### 6.2 Locations and assigned elements

| Location from I-9 | Assigned elements |
|-------------------|-------------------|
| Customer mobile device | `Mobile App` |
| Lending application runtime | `Loan Application Service`; `Credit Scoring Adapter`; `Decision Engine`; `Policy Engine`; `Account Validation Service`; `Disbursement Adapter` |
| Evidence data store | `Decision Store`; `Audit Log` |
| External banking integration zone | `Credit Scoring System`; `ESB Integration Layer`; `Core Banking` |

### 6.3 Technology/deployment relationships

- `Mobile App` is assigned to Customer mobile device.
- The six lending service containers are assigned to Lending application runtime.
- `Decision Store` and `Audit Log` are assigned to Evidence data store.
- `Credit Scoring System`, `ESB Integration Layer`, and `Core Banking` are assigned to External banking integration zone.
- The communication path for scoring connects `Credit Scoring Adapter` to `Credit Scoring System`.
- The communication path for disbursement/accounting connects `Disbursement Adapter` to `ESB Integration Layer` and then `Core Banking`.
- The forbidden path is explicitly marked: `Mobile App` must not write directly to `Core Banking` or perform credit evaluation.
- The approved path is marked: all credit evaluation goes through internal services and `Credit Scoring Adapter`; disbursement/accounting goes through `Disbursement Adapter` and `ESB Integration Layer`.

### 6.4 View 4 boundary

Must show I-9 locations, assigned named elements, approved integration boundaries, and the forbidden direct path. Must not show pods, clusters, Docker, hostnames, credentials, vendor products, JDBC, or a channel writing directly to a core ledger database.

**G3 support:** the technology view confirms deployment and forbidden-path evidence. G3 remains **Pending** until the complete after-pack application/container review.

## 7. Lab 8 completion check

- [x] Four named view specifications are present.
- [x] View 1 contains Goal, Outcome, capabilities, and `CON.1` through `CON.5` for G1.
- [x] View 2 contains the I-5 happy path, exact I-6 state outcomes, and constraint branches for G2.
- [x] View 3 uses the exact I-4 internal container names and I-3 external system names.
- [x] View 4 uses the exact I-9 deployment locations and includes the forbidden path.
- [x] Each view has a header, legend, scope, and one RACI assignment.
- [x] No view introduces a system, actor, container, object, state, or constraint outside Lab 1-4.
- [x] No UML/C4 mixed notation is used inside the ArchiMate views.
- [ ] G1 formally approved by Owner.
- [ ] G2 formally approved by BA/Test.

**Current result:** Lab 8 view specification is complete as a Draft. G1 and G2 remain `Pending`; the views are ready for diagram rendering and review.
