# Lab 4 - Standardize following modeling-driven design

**R:** SA  
**A:** EA  
**Status:** Lab 4 first cleanup using the team's current method. This file keeps the Lab 1-3 before pack unchanged as the source baseline. It does not apply the Guide, add a header or RACI, or create ArchiMate, C4, or UML diagrams.

## Scope and source

- Lab 1 remains the authority for identity: names, actors, external systems, internal containers, states, constraints, source-of-truth objects, and named use cases.
- Lab 2 remains the authority for the current-language requirements and trace table.
- Lab 3 remains the authority for the initial build list, selected Component, sequence, contracts, exception specification, and test specification.
- `Requirement_Document.md` is treated as a supporting draft. It does not override the Lab 1 identity index or silently add unresolved requirements to the cleaned pack.
- Messy source files are retained unchanged: `Lab-1-Scopes.md`, `Lab-2-Requirements-Analysis.md`, and `Lab-3-Implement architecture, design, and test.md`.

## 1. Cleaned 1-3 pack

### 1.1 Name and responsibility index

| Category | Locked names | Cleanup rule |
|----------|--------------|--------------|
| System-in-focus | `Nopbai Personal Loan Platform` | Use this exact system name; do not replace it with a generic platform name |
| Product | `Nopbai Mobile Personal Loan` | Use this exact product name |
| Contract | `Nopbai Personal Loan Agreement` | Use this exact contract name when agreement acceptance is discussed |
| Actors | `Customer`; `Loan Operations Specialist` | Use only these two actor names; the specialist is not on the standard approval path |
| External systems | `Credit Scoring System`; `ESB Integration Layer`; `Core Banking` | Use only these three external names |
| Internal containers | `Mobile App`; `Loan Application Service`; `Credit Scoring Adapter`; `Decision Engine`; `Policy Engine`; `Account Validation Service`; `Disbursement Adapter`; `Decision Store`; `Audit Log` | Use these exact strings for containers, build-list items, neighbours, contract endpoints, and SUTs |
| Moving object | `Loan Application` | Use as the one lifecycle object |
| Other named objects | `Customer Profile`; `Credit Score`; `Policy Configuration`; `Loan Offer`; `Decision Record`; `Disbursement Record` | Preserve I-7 source-of-truth ownership |
| States | `Draft`; `Submitted`; `Scoring`; `OfferReady`; `Approved`; `AccountValidated`; `Rejected`; `Disbursed`; `Failed` | Use these exact strings for transitions and tests |
| Constraints | `CON.1`; `CON.2`; `CON.3`; `CON.4`; `CON.5` | Use the same constraint ID on each decision or exception branch |
| Selected Component container | `Decision Engine` | Only this container may have internal modules in the Lab 3 design pack |

### 1.2 Cleaned container and deployment list

| Order | Exact container | Owner (Dev) | I-9 location | Cleaned responsibility |
|------:|-----------------|-------------|--------------|------------------------|
| 1 | `Mobile App` | Vũ Thế Quân | Customer mobile device | Capture applications, display Loan Offers and decisions, and collect agreement acceptance |
| 2 | `Loan Application Service` | Lý Bá Duy | Lending application runtime | Validate and manage submitted Loan Applications |
| 3 | `Credit Scoring Adapter` | Nguyễn Thanh Hải | Lending application runtime | Request and normalize responses from `Credit Scoring System` |
| 4 | `Decision Engine` | Nguyễn Cương Quyết (TN) | Lending application runtime | Orchestrate eligibility, score, policy, offer, and approval or rejection decisions |
| 5 | `Policy Engine` | Nguyễn Minh Hoàng | Lending application runtime | Apply eligibility, amount, rate, and approval rules |
| 6 | `Account Validation Service` | Nguyễn Thanh Hải | Lending application runtime | Confirm the payment account is eligible before disbursement |
| 7 | `Disbursement Adapter` | Lý Bá Duy | Lending application runtime | Create an idempotent disbursement request and handle the posting outcome |
| 8 | `Decision Store` | Nguyễn Minh Hoàng | Evidence data store | Persist score, policy basis, calculations, Loan Offers, and Decision Records |
| 9 | `Audit Log` | Vũ Thế Quân | Evidence data store | Persist decision, integration, and transaction evidence |

No external system is treated as an internal container. No gateway, event bus, IAM product, database product, vendor, or production host is added.

### 1.3 Cleaned Component contents

`Decision Engine` is the only selected container. Its modules are implementation internals, not additional I-4 containers.

| Module | Parent container | Responsibility | Allowed neighbour names |
|--------|------------------|----------------|-------------------------|
| Decision Orchestrator | `Decision Engine` | Control the decision flow and state outcome | `Loan Application Service`; `Mobile App` |
| Eligibility Evaluator | `Decision Engine` | Check the initial customer segment and eligibility result | `Loan Application Service` |
| Score Coordinator | `Decision Engine` | Request the Credit Score and handle success or timeout input | `Credit Scoring Adapter` |
| Policy Evaluation Module | `Decision Engine` | Request maximum amount, personalized rate, and policy outcome | `Policy Engine` |
| Offer Builder | `Decision Engine` | Create the customer-facing Loan Offer | `Policy Engine`; `Decision Store` |
| Decision Recorder | `Decision Engine` | Persist decision evidence and send audit events | `Decision Store`; `Audit Log` |

The cleaned relationship is: `Decision Engine` calls the named neighbour containers; the modules above own the internal steps. A module name must not be used as a container, external system, or SUT.

### 1.4 Cleaned sequence: Submit and Decide Loan Application

The sequence below keeps the Lab 3 use case but makes the grain explicit. `Decision Engine` is the participant container. Module names appear only after the container is entered; `Credit Scoring System` remains an external black box.

| Step | Participant / owner | Action or result |
|-----:|--------------------|------------------|
| 1 | `Customer` -> `Mobile App` | Submit `Loan Application` |
| 2 | `Mobile App` -> `Loan Application Service` | Submit application data for validation |
| 3 | `Loan Application Service` -> `Decision Engine` | Start eligibility and decisioning |
| 4 | `Decision Engine` / Eligibility Evaluator | Check the existing salaried customer segment aged 22-35 |
| 5 | Eligibility Evaluator -> `Decision Engine` | Return eligible result |
| 6 | `Decision Engine` / Score Coordinator -> `Credit Scoring Adapter` | Request near-real-time Credit Score |
| 7 | `Credit Scoring Adapter` -> `Credit Scoring System` | Send sync HTTPS `Get Credit Score` request |
| 8 | `Credit Scoring System` -> `Credit Scoring Adapter` | Return Credit Score |
| 9 | `Credit Scoring Adapter` -> `Decision Engine` / Score Coordinator | Return normalized Credit Score |
| 10 | `Decision Engine` / Policy Evaluation Module -> `Policy Engine` | Request amount, rate, and policy evaluation |
| 11 | `Policy Engine` -> `Decision Engine` / Policy Evaluation Module | Return calculated terms and policy result |
| 12 | `Decision Engine` / Offer Builder | Create and return the Loan Offer |
| 13 | `Decision Engine` / Decision Recorder -> `Decision Store` | Persist score, policy basis, calculations, Loan Offer, and Decision Record |
| 14 | `Decision Engine` / Decision Recorder -> `Audit Log` | Append decision and integration evidence |
| 15 | `Decision Engine` -> `Mobile App` -> `Customer` | Return and display the Loan Offer and decision |

Cleaned alternatives:

- `CON.2`: `Eligibility Evaluator` returns ineligible; `Decision Engine` sets `Submitted -> Rejected`, records the reason, and skips scoring.
- `CON.3`: `Credit Scoring Adapter` reports timeout or unavailable scoring; `Decision Engine` sets `Scoring -> Failed`, records evidence, and does not approve.
- `CON.1`: `Policy Engine` reports an amount above the cap; `Decision Engine` sets `OfferReady -> Rejected`, records the policy basis, and does not approve.

This sequence is for the selected `Decision Engine` container and does not replace the three named UML use cases required by Lab 5.

### 1.5 Cleaned contract register

| Contract ID | Producer | Consumer | Mode | Mechanism | Operation / event | Cleaned rule |
|-------------|----------|----------|------|-----------|-------------------|--------------|
| C-01 | `Credit Scoring Adapter` | `Credit Scoring System` | Sync | HTTPS request/response | `Get Credit Score` | Only `Credit Scoring Adapter` crosses this scoring boundary |
| C-02 | `Disbursement Adapter` | `ESB Integration Layer` | Async | Message with confirmation and reconciliation | `Disbursement and Accounting Request` | Disbursement starts only after approval and account validation |
| C-03 | `ESB Integration Layer` | `Core Banking` | Async | Message with confirmation and reconciliation | `Post Disbursement and Accounting` | The ESB path is required; no direct `Mobile App` path exists |

Each row is an explicit I-8 edge. The adapter boundary is a responsibility rule, not a fourth invented system.

### 1.6 Cleaned exception specification

| Exception ID | Constraint | Trigger | Compensating action | Performer | State / evidence |
|--------------|------------|---------|---------------------|-----------|------------------|
| EX-01 | `CON.1` | Calculated unsecured amount exceeds 100,000,000 VND | Reject the Loan Offer, prevent approval, and retain policy basis | `Decision Engine` with `Policy Engine` | `OfferReady -> Rejected`; `Decision Store`; `Audit Log` |
| EX-02 | `CON.2` | Customer is outside the existing salaried 22-35 segment | Reject before scoring and record the reason | `Loan Application Service` with `Decision Engine` | `Submitted -> Rejected`; `Decision Store`; `Audit Log` |
| EX-03 | `CON.3` | `Credit Scoring System` times out or is unavailable | Stop decisioning, do not approve, and record timeout evidence | `Credit Scoring Adapter` with `Decision Engine` | `Scoring -> Failed`; `Audit Log` |
| EX-04 | `CON.4` | Account validation or Core Banking posting confirmation fails | Do not complete disbursement; reconcile the posting outcome and retain evidence | `Account Validation Service`; `Disbursement Adapter`; `ESB Integration Layer` | `Approved -> Failed` or `AccountValidated -> Failed`; `Disbursement Record`; `Audit Log` |
| EX-05 | `CON.5` | Unauthorized access to customer data or decision evidence is attempted | Deny access and retain security evidence | Owning service and `Audit Log` | No business approval transition; `Audit Log` |

### 1.7 Cleaned test specification

The test IDs remain stable. Every I-6 transition and every cleaned sequence alternative has one planned test. SUTs are exact I-4 container names.

| Test ID | Coverage source | SUT | Expected result |
|---------|-----------------|-----|-----------------|
| T-01 | `Draft -> Submitted` | `Mobile App` | Customer starts an application and the Loan Application enters `Submitted` |
| T-02 | `Submitted -> Scoring` | `Loan Application Service` | Valid in-segment submission starts decisioning in `Scoring` |
| T-03 | `Submitted -> Rejected`; `CON.2` | `Loan Application Service` | Out-of-segment application is rejected before scoring and the reason is recorded |
| T-04 | `Scoring -> OfferReady` | `Decision Engine` | Credit Score and accepted policy evaluation produce a Loan Offer in `OfferReady` |
| T-05 | `Scoring -> Failed`; `CON.3` | `Credit Scoring Adapter` | Timeout produces `Failed`; no approval is produced |
| T-06 | `OfferReady -> Approved` | `Decision Engine` | Agreement acceptance and policy approval produce `Approved` |
| T-07 | `OfferReady -> Rejected`; `CON.1` | `Decision Engine` | Amount cap breach rejects the Loan Offer |
| T-08 | `OfferReady -> Rejected` | `Mobile App` | Customer decline produces `Rejected`; account validation does not start |
| T-09 | `Approved -> AccountValidated` | `Account Validation Service` | Eligible payment account produces `AccountValidated` |
| T-10 | `Approved -> Failed`; `CON.4` | `Account Validation Service` | Account validation failure produces `Failed`; no disbursement request is sent |
| T-11 | `AccountValidated -> Disbursed` | `Disbursement Adapter` | Confirmed ESB/Core Banking outcome produces `Disbursed` |
| T-12 | `AccountValidated -> Failed`; `CON.4` | `Disbursement Adapter` | Posting failure produces `Failed`; application is not marked `Disbursed` |
| T-13 | Sequence alt `CON.2` | `Decision Engine` | Eligibility rejection skips scoring and approval and records evidence |
| T-14 | Sequence alt `CON.3` | `Credit Scoring Adapter` | Controlled scoring failure produces `Failed` and no approval |
| T-15 | Sequence alt `CON.1` | `Decision Engine` | Amount cap breach rejects the Loan Offer and stores policy evidence |

## 2. Name-identity check

| Check | Result | Evidence in cleaned pack |
|-------|--------|--------------------------|
| System-in-focus and product | Pass | Exact Lab 1 strings are used in the scope and identity index |
| Actors | Pass | Only `Customer` and `Loan Operations Specialist` are named as actors |
| External systems | Pass | Only `Credit Scoring System`, `ESB Integration Layer`, and `Core Banking` are used |
| Internal containers | Pass | All nine I-4 strings are used consistently in build, neighbour, contract, and SUT fields |
| Selected Component | Pass | Only `Decision Engine` has internal modules |
| Moving object and states | Pass | `Loan Application` and all nine I-6 states are unchanged |
| Source-of-truth objects | Pass | I-7 objects retain their named owners; `Loan Offer` and `Decision Record` remain distinct |
| Integration modes | Pass | Credit scoring is Sync; disbursement/accounting is Async; adapter boundaries are preserved |
| Constraints | Pass | `CON.1` through `CON.5` are retained on decision and exception branches |
| Production details | Pass | No production host, credential, vendor, runtime stack, or installed product is introduced |

## 3. Defect list from the before pack

The before pack means the first-written Lab 1, Lab 2, and Lab 3 artifacts. The source files are kept unchanged; these defects are recorded rather than silently rewritten in place.

| Defect ID | Before-pack defect or ambiguity | Owner | Cleanup decision |
|-----------|--------------------------------|-------|-----------------|
| D-01 | Lab 3 used module names such as `Eligibility Evaluator` and `Offer Builder` as sequence participants without always showing their parent container. | Dev / SA | Show the parent as `Decision Engine` and keep modules explicitly inside that container |
| D-02 | Lab 3 sequence owner fields mixed container owners and internal module owners without stating the grain. | Dev | Separate participant container from internal module owner in the cleaned sequence |
| D-03 | Requirement_Document FR numbering did not match the current Lab 2 list because Lab 2 made agreement acceptance explicit as FR-09 and retained evidence as FR-12. | BA | Lab 2 is the current requirements authority; the cleaned pack keeps the explicit agreement and evidence requirements |
| D-04 | Requirement_Document listed availability, capacity, and regulatory NFRs without a Lab 1 identity or agreed target. | BA / Owner | Keep those as unresolved or deferred questions; do not add them to the Lab 4 cleaned design pack |
| D-05 | Requirement_Document used broad phrases such as “decisions” and “applications” where Lab 1 distinguishes `Decision Record`, `Loan Application`, and `Loan Offer`. | BA / SA | Use the I-7 object names and preserve the distinct source-of-truth ownership |
| D-06 | Lab 3 described the selected Decision Engine sequence only; it did not provide sequences for all I-11 use cases. | SA / Dev | Keep this as a Lab 3 boundary; Lab 5 must create one UML sequence for each named use case |
| D-07 | Lab 3 build owners were plausible team assignments, but the role-to-person mapping was not formally recorded in Lab 1. | Owner | Retain the assignments as current working assumptions and record the roster formally in the later required lab |
| D-08 | An earlier Lab 3 review found T-04's SUT responsibility was too broad for `Credit Scoring Adapter` while its expected result included offer creation. The current Lab 3 source already contains the correction. | Test / Dev | Preserve the corrected `Decision Engine` SUT and record the review history without changing the Lab 3 baseline |

## 4. Comparison note

### What was cleaned

- Exact identity strings were collected into one index and applied to the cleaned build, Component, sequence, contract, exception, and test artifacts.
- Internal modules were separated from I-4 containers, with `Decision Engine` explicitly acting as their parent.
- Sequence ownership was clarified so external systems and neighbour containers remain black boxes while modules own internal actions.
- Contract rows were aligned to the three explicit I-8 edges and no adapter was turned into a new system.
- State transitions, constraint IDs, source-of-truth objects, and SUT names were made consistent across Lab 2 and Lab 3.
- The Requirement Document was treated as a supporting draft; unresolved NFRs were not silently promoted to product facts.

### What is still not standardized or known

- Exact eligibility and affordability rules remain Q1.
- Credit scoring thresholds and payload fields remain Q2 and Q3.
- Payment account definition and validation details remain Q4.
- Final response-time and availability targets remain Q5.
- The team has not yet formally recorded the role-to-person roster for later approvals.
- Lab 5 still needs to create the UML sequence, activity, and state artifacts for all named use cases.

## Lab 4 completion check

- Messy Lab 1-3 source files are retained unchanged.
- Cleaned 1-3 pack is present in this file.
- Name-identity check covers actors, externals, containers, objects, states, constraints, and integration modes.
- Defect list records before-pack issues with an owner.
- Comparison note records both completed cleanup and unresolved standardization questions.
- No Guide, after-pack header, RACI, ArchiMate, C4, or UML diagram was applied in this Lab 4 cleanup.
