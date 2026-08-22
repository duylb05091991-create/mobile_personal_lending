# Lab 3 - Implement architecture, design, and test

**R:** Dev (build list, Component, contracts) · Test (test spec)  
**A:** SA  
**Status:** Lab 3 current-language design specification. This file describes what will be built and tested; it does not contain source code, runtime tests, deployment, or a quality-gate register.

## Scope and source

This file uses the locked identity from Lab 1 and the requirements and exception paths from Lab 2.

- System-in-focus: `Nopbai Personal Loan Platform`
- Product: `Nopbai Mobile Personal Loan`
- Moving object: `Loan Application`
- Actors: `Customer`, `Loan Operations Specialist`
- External systems: `Credit Scoring System`, `ESB Integration Layer`, `Core Banking`
- Internal containers: `Mobile App`, `Loan Application Service`, `Credit Scoring Adapter`, `Decision Engine`, `Policy Engine`, `Account Validation Service`, `Disbursement Adapter`, `Decision Store`, `Audit Log`
- Selected container for optional Component view: `Decision Engine`
- States: `Draft`, `Submitted`, `Scoring`, `OfferReady`, `Approved`, `AccountValidated`, `Rejected`, `Disbursed`, `Failed`
- Constraints: `CON.1` through `CON.5`

## 1. Build list

Every Lab 1 internal container is listed once. The owner is a team member acting in the Dev role. The environment is taken from Lab 1 deployment locations.

| Order | Container | Owner (Dev) | Environment from I-9 | Build responsibility |
|------:|-----------|-------------|----------------------|----------------------|
| 1 | `Mobile App` | Vũ Thế Quân | Customer mobile device | Capture applications, display Loan Offers and decisions, collect agreement acceptance |
| 2 | `Loan Application Service` | Lý Bá Duy | Lending application runtime | Validate and manage submitted Loan Applications |
| 3 | `Credit Scoring Adapter` | Nguyễn Thanh Hải | Lending application runtime | Request and normalize Credit Score responses |
| 4 | `Decision Engine` | Nguyễn Cương Quyết (TN) | Lending application runtime | Orchestrate eligibility, scoring, policy, offer, and approval or rejection decisions |
| 5 | `Policy Engine` | Nguyễn Minh Hoàng | Lending application runtime | Apply eligibility, amount, rate, and approval rules |
| 6 | `Account Validation Service` | Nguyễn Thanh Hải | Lending application runtime | Validate the customer payment account before disbursement |
| 7 | `Disbursement Adapter` | Lý Bá Duy | Lending application runtime | Create an idempotent disbursement request and handle the posting outcome |
| 8 | `Decision Store` | Nguyễn Minh Hoàng | Evidence data store | Persist score, policy basis, calculations, Loan Offers, and decision records |
| 9 | `Audit Log` | Vũ Thế Quân | Evidence data store | Persist decision, integration, and transaction evidence |

The external systems remain black boxes in this build list. No new gateway, event bus, IAM product, database, vendor, or production system is introduced.

## 2. To-be Component - Decision Engine

This is the one selected container from Lab 1 I-11. The following modules are internal to `Decision Engine`; they are not additional containers or external systems.

| Module inside `Decision Engine` | Responsibility | Main neighbour |
|--------------------------------|----------------|----------------|
| Decision Orchestrator | Controls the decision flow and state outcome | `Loan Application Service`, `Mobile App` |
| Eligibility Evaluator | Checks the initial customer segment and eligibility result | `Loan Application Service` |
| Score Coordinator | Requests the Credit Score and converts success or timeout into a decision input | `Credit Scoring Adapter` |
| Policy Evaluation Module | Requests maximum amount, personalized rate, and policy outcome | `Policy Engine` |
| Offer Builder | Creates the customer-facing Loan Offer from the accepted score and policy results | `Policy Engine`, `Decision Store` |
| Decision Recorder | Persists decision evidence and sends audit events | `Decision Store`, `Audit Log` |

### Component boundaries

- `Decision Engine` owns orchestration and decision outcomes; it does not directly call `Credit Scoring System` or `Core Banking`.
- `Credit Scoring Adapter` remains the boundary for the `Credit Scoring System` contract.
- `Policy Engine` remains the source of truth for `Policy Configuration`.
- `Decision Store` remains the source of truth for `Loan Offer` and `Decision Record`.
- `Mobile App` does not perform credit evaluation and does not write directly to `Core Banking`.
- `Account Validation Service` and `Disbursement Adapter` are neighbours for the later disbursement use case; they are not expanded here.

## 3. To-be sequence - Submit and Decide Loan Application

This sequence focuses on the selected `Decision Engine` container. Internal modules are shown only inside that container. The external systems are black boxes.

| Step | Sender | Receiver | Message / result | Owner |
|-----:|--------|----------|-----------------|-------|
| 1 | `Customer` | `Mobile App` | Submit `Loan Application` | `Mobile App` |
| 2 | `Mobile App` | `Loan Application Service` | Submit application data for validation | `Loan Application Service` |
| 3 | `Loan Application Service` | `Decision Engine` | Start eligibility and decisioning for the submitted application | `Decision Orchestrator` |
| 4 | `Decision Engine` | Eligibility Evaluator | Check existing salaried customer segment aged 22-35 | `Eligibility Evaluator` |
| 5 | Eligibility Evaluator | `Decision Engine` | Return eligible result | `Eligibility Evaluator` |
| 6 | `Decision Engine` | `Credit Scoring Adapter` | Request near-real-time Credit Score | `Score Coordinator` |
| 7 | `Credit Scoring Adapter` | `Credit Scoring System` | Sync HTTPS request for Credit Score | `Credit Scoring Adapter` |
| 8 | `Credit Scoring System` | `Credit Scoring Adapter` | Return Credit Score | `Credit Scoring Adapter` |
| 9 | `Credit Scoring Adapter` | `Decision Engine` | Return normalized Credit Score | `Score Coordinator` |
| 10 | `Decision Engine` | `Policy Engine` | Calculate maximum eligible amount, rate, and policy result | `Policy Evaluation Module` |
| 11 | `Policy Engine` | `Decision Engine` | Return policy evaluation and calculated terms | `Policy Evaluation Module` |
| 12 | `Decision Engine` | Offer Builder | Create the Loan Offer | `Offer Builder` |
| 13 | Offer Builder | `Decision Engine` | Return the Loan Offer | `Offer Builder` |
| 14 | `Decision Engine` | `Decision Store` | Persist score, policy basis, calculations, Loan Offer, and Decision Record | `Decision Recorder` |
| 15 | `Decision Engine` | `Audit Log` | Append decision and integration evidence | `Decision Recorder` |
| 16 | `Decision Engine` | `Mobile App` | Return Loan Offer and decision outcome | `Decision Orchestrator` |
| 17 | `Mobile App` | `Customer` | Display the Loan Offer and decision | `Mobile App` |

### Sequence exception fragments

- **alt `CON.2` - out-of-segment customer:** `Eligibility Evaluator` returns ineligible; `Decision Engine` sets the `Loan Application` to `Rejected`, records the reason through `Decision Recorder`, and returns rejection through `Mobile App`. No scoring or approval occurs.
- **alt `CON.3` - Credit Scoring System timeout or unavailable:** `Credit Scoring Adapter` returns a controlled failure; `Decision Engine` sets the `Loan Application` to `Failed`, records timeout evidence, and does not approve.
- **alt `CON.1` - amount cap breach:** `Policy Engine` reports that the calculated unsecured amount exceeds 100,000,000 VND; `Decision Engine` rejects the Loan Offer, records the policy basis, and does not approve.

## 4. Contract register

Each row corresponds to an integration relationship in Lab 1 I-8. The adapter boundaries isolate external contracts; no direct Mobile App to Core Banking relationship exists.

| Contract ID | Producer | Consumer | Mode | Mechanism | Operation / event | Payload or outcome | Failure handling |
|-------------|----------|----------|------|-----------|-------------------|-------------------|------------------|
| C-01 | `Credit Scoring Adapter` | `Credit Scoring System` | Sync | HTTPS request/response | `Get Credit Score` | Request for existing customer; response contains `Credit Score` | Timeout or unavailable response becomes `Scoring -> Failed`; no approval |
| C-02 | `Disbursement Adapter` | `ESB Integration Layer` | Async | Message with confirmation and reconciliation | `Disbursement and Accounting Request` | Approved application, validated account, amount, and disbursement reference | Do not mark `Disbursed` until confirmation; reconcile failure |
| C-03 | `ESB Integration Layer` | `Core Banking` | Async | Message with confirmation and reconciliation | `Post Disbursement and Accounting` | Account and transaction instruction; confirmation contains posting and disbursement outcome | Return failure through the integration path; retain transaction evidence |

### Contract rules

- `Credit Scoring Adapter` is the only container that calls `Credit Scoring System`.
- `Disbursement Adapter` is the only internal container that sends the disbursement request into `ESB Integration Layer`.
- `ESB Integration Layer` is the only path to `Core Banking` for disbursement and accounting.
- All contract rows use only external systems from I-3 and containers from I-4.

## 5. Exception specification

These are modeled failure paths, not executed tests or production controls.

| Exception ID | Constraint | Trigger | Compensating action | Performer | State / evidence |
|--------------|------------|---------|---------------------|-----------|------------------|
| EX-01 | `CON.1` | Policy calculation exceeds the unsecured amount cap | Reject the Loan Offer, prevent approval, and retain the policy basis | `Decision Engine` with `Policy Engine` | `OfferReady -> Rejected`; `Decision Store`, `Audit Log` |
| EX-02 | `CON.2` | Customer is not an existing salaried customer aged 22-35 | Reject before scoring and decisioning; record the rejection reason | `Loan Application Service` with `Decision Engine` | `Submitted -> Rejected`; `Decision Store`, `Audit Log` |
| EX-03 | `CON.3` | `Credit Scoring System` times out or is unavailable | Stop decisioning, do not approve, and record the controlled timeout | `Credit Scoring Adapter` with `Decision Engine` | `Scoring -> Failed`; `Audit Log` |
| EX-04 | `CON.4` | Account validation fails or Core Banking cannot confirm posting | Do not send or complete disbursement when validation fails; reconcile posting failure and retain evidence | `Account Validation Service`, `Disbursement Adapter`, and `ESB Integration Layer` | `Approved -> Failed` or `AccountValidated -> Failed`; `Audit Log`, `Disbursement Record` |
| EX-05 | `CON.5` | Unauthorized access to customer data or decision evidence is attempted | Deny access and retain security evidence for audit | Owning service and `Audit Log` | No approval state change; `Audit Log` evidence |

## 6. Test specification

The tests are planned design evidence only. No code is implemented and no test is executed in Lab 3. Every state transition from Lab 1 I-6 and every sequence `alt` in this file is covered.

| Test ID | Coverage source | SUT | Scenario / input | Expected result |
|---------|-----------------|-----|------------------|-----------------|
| T-01 | I-6: `Draft -> Submitted` | `Mobile App` | `Customer` starts an application | A `Loan Application` is created in `Submitted` |
| T-02 | I-6: `Submitted -> Scoring` | `Loan Application Service` | Valid in-segment application is submitted | Validation succeeds and decisioning starts in `Scoring` |
| T-03 | I-6 / `CON.2`: `Submitted -> Rejected` | `Loan Application Service` | Customer is outside the existing salaried 22-35 segment | Application is rejected before scoring; reason is recorded |
| T-04 | I-6: `Scoring -> OfferReady` | `Decision Engine` | `Credit Scoring Adapter` returns a Credit Score and `Policy Engine` returns an accepted policy evaluation | A Loan Offer is created and state becomes `OfferReady` |
| T-05 | I-6 / `CON.3`: `Scoring -> Failed` | `Credit Scoring Adapter` | Credit Scoring System times out or is unavailable | State becomes `Failed`; no approval is produced |
| T-06 | I-6: `OfferReady -> Approved` | `Decision Engine` | Customer accepts the Nopbai Personal Loan Agreement and policy rules allow approval | State becomes `Approved` |
| T-07 | I-6 / `CON.1`: `OfferReady -> Rejected` | `Decision Engine` | Calculated unsecured amount exceeds 100,000,000 VND | Offer is rejected; approval does not occur |
| T-08 | I-6: `OfferReady -> Rejected` | `Mobile App` | Customer declines the Loan Offer | State becomes `Rejected`; account validation does not start |
| T-09 | I-6: `Approved -> AccountValidated` | `Account Validation Service` | Approved application has an eligible payment account | Account is validated and state becomes `AccountValidated` |
| T-10 | I-6 / `CON.4`: `Approved -> Failed` | `Account Validation Service` | Core Banking cannot confirm an eligible payment account | State becomes `Failed`; Disbursement Adapter sends no request |
| T-11 | I-6: `AccountValidated -> Disbursed` | `Disbursement Adapter` | ESB Integration Layer and Core Banking confirm posting and disbursement | State becomes `Disbursed`; Disbursement Record is retained |
| T-12 | I-6 / `CON.4`: `AccountValidated -> Failed` | `Disbursement Adapter` | Core Banking posting or confirmation fails | State becomes `Failed`; application is not marked `Disbursed` |
| T-13 | Sequence alt `CON.2` | `Decision Engine` | Eligibility Evaluator returns out-of-segment | Rejection is returned; scoring and approval are skipped; evidence is recorded |
| T-14 | Sequence alt `CON.3` | `Credit Scoring Adapter` | Credit Scoring System does not return near-real-time data | Controlled failure is returned; state becomes `Failed`; no approval |
| T-15 | Sequence alt `CON.1` | `Decision Engine` | Policy Engine reports amount cap breach | Loan Offer is rejected and policy basis is stored and audited |

## Lab 3 completion check

- Build list contains every I-4 internal container, one owner, build order, and I-9 environment.
- Component view contains internals for `Decision Engine` only, as selected in I-11.
- To-be sequence uses the named use case `Submit and Decide Loan Application` and includes `CON.1`, `CON.2`, and `CON.3` alternatives.
- Contract register contains one row for each explicit I-8 integration edge.
- Exception specification covers `CON.1` through `CON.5` with trigger, compensating action, performer, and evidence.
- Test specification covers all twelve I-6 transitions and all three sequence alternatives.
- Every SUT is an exact I-4 container name.
- No new external system, actor, container, state, or production implementation detail is introduced.
- No Guide header, RACI, ArchiMate/C4 diagram, source code, runtime test, or deployment is included.
