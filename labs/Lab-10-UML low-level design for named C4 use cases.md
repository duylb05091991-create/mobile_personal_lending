# Lab 10 - UML low-level design for named C4 use cases

**Status:** Lab 10 after-pack UML specification - Draft.  
**Primary sources:** Lab 1, Lab 2, Lab 3, Lab 4, Lab 7, Lab 8, and Lab 9.  
**Scope assumption:** Lab 5 and Lab 6 are not required inputs for this artifact.  
**R:** Dev  
**A:** SA  
**C:** Test, BA  
**G6 status:** Pending coverage review.

## 1. Scope and naming rules

This file defines UML low-level design for the three named use cases in Lab 1 I-11. It uses the C4 names established in Lab 9 and the cleaned identity baseline from Lab 4.

- Use cases: `Submit and Decide Loan Application`, `Disburse Approved Loan Application`, and `Recommend Limit Increase`.
- Actors: `Customer` and `Loan Operations Specialist`.
- System and containers: use only the exact names from Lab 1 I-4 and Lab 9.
- `Loan Application` is the one lifecycle object for the State machine.
- Internal modules are allowed only inside the selected `Decision Engine` container.
- Every sequence has at least one `alt` branch and names the relevant `CON.*` constraint.
- Lab 5 and Lab 6 are not required inputs under the agreed scope assumption; this file creates the required UML behavior specification directly from Lab 1-4 and Lab 9 names.
- No source code, runtime test, deployment, or second Component view is introduced.

## 2. Shared diagram header and RACI

### 2.1 Header template

Use the following header on each UML artifact:

```text
Title:      ________________________________
Viewpoint:  UML ____________________________
Layer(s):   Base - delivery behavior
As-Is | To-Be | Transition:  To-Be
Owner:      Role ________  Name ____________
RACI:       R ____  A ____  C ____  I ____
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     actor, C4 container, internal Decision Engine module, message, state, alt
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      named I-11 use cases only; no out-of-scope lending journeys
```

### 2.2 Artifact assignments

| Artifact | R | A | C | I |
|----------|---|---|---|---|
| UML Sequence - `Submit and Decide Loan Application` | Nguyễn Thanh Hải | Vũ Thế Quân | Lý Bá Duy | Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng |
| UML Sequence - `Disburse Approved Loan Application` | Nguyễn Thanh Hải | Vũ Thế Quân | Lý Bá Duy | Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng |
| UML Sequence - `Recommend Limit Increase` | Nguyễn Thanh Hải | Vũ Thế Quân | Lý Bá Duy | Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng |
| UML State - `Loan Application` | Lý Bá Duy | Vũ Thế Quân | Nguyễn Thanh Hải | Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng |
| Participant = SUT map and G6 coverage | Lý Bá Duy | Vũ Thế Quân | Nguyễn Thanh Hải; Nguyễn Cương Quyết (TN) | Nguyễn Minh Hoàng |

`Nguyễn Thanh Hải` is the Dev role name used in this Lab 10 artifact. The assignment must be confirmed by the Owner before formal approval.

## 3. UML Sequence - Submit and Decide Loan Application

### 3.1 Header

```text
Title:      Submit and Decide Loan Application
Viewpoint:  UML Sequence
Layer(s):   Base - delivery behavior
As-Is | To-Be | Transition:  To-Be
Owner:      Dev  Name Nguyễn Thanh Hải
RACI:       R Nguyễn Thanh Hải  A Vũ Thế Quân  C Lý Bá Duy  I Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     Customer, C4 containers, Decision Engine modules, messages, alt branches
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      standard application decisioning
```

### 3.2 Lifelines

| Lifeline | Kind | Resolution |
|----------|------|------------|
| `Customer` | Actor | Lab 1 I-2 actor |
| `Mobile App` | C4 container | Lab 9 L2 container |
| `Loan Application Service` | C4 container | Lab 9 L2 container |
| `Decision Engine` | C4 container | Lab 9 L2 container |
| `Credit Scoring Adapter` | C4 container | Lab 9 L2 container |
| `Credit Scoring System` | External system | Lab 9 external system |
| `Policy Engine` | C4 container | Lab 9 L2 container |
| `Decision Store` | C4 container | Lab 9 L2 container |
| `Audit Log` | C4 container | Lab 9 L2 container |
| `Eligibility Evaluator` | Component inside `Decision Engine` | Only inside the selected container |
| `Score Coordinator` | Component inside `Decision Engine` | Only inside the selected container |
| `Policy Evaluation Module` | Component inside `Decision Engine` | Only inside the selected container |
| `Offer Builder` | Component inside `Decision Engine` | Only inside the selected container |
| `Decision Recorder` | Component inside `Decision Engine` | Only inside the selected container |

### 3.3 Main sequence

| Step | Sender | Receiver | Message |
|-----:|--------|----------|---------|
| 1 | `Customer` | `Mobile App` | Submit `Loan Application` |
| 2 | `Mobile App` | `Loan Application Service` | Validate and store submitted application |
| 3 | `Loan Application Service` | `Decision Engine` | Start eligibility and decisioning |
| 4 | `Decision Engine` / `Eligibility Evaluator` | `Loan Application Service` | Request customer segment and application eligibility |
| 5 | `Loan Application Service` | `Decision Engine` / `Eligibility Evaluator` | Return eligible result |
| 6 | `Decision Engine` / `Score Coordinator` | `Credit Scoring Adapter` | Request near-real-time `Credit Score` |
| 7 | `Credit Scoring Adapter` | `Credit Scoring System` | `Get Credit Score` using the defined sync scoring boundary |
| 8 | `Credit Scoring System` | `Credit Scoring Adapter` | Return `Credit Score` |
| 9 | `Credit Scoring Adapter` | `Decision Engine` / `Score Coordinator` | Return normalized score |
| 10 | `Decision Engine` / `Policy Evaluation Module` | `Policy Engine` | Request maximum amount, rate, and policy evaluation |
| 11 | `Policy Engine` | `Decision Engine` / `Policy Evaluation Module` | Return calculated terms and policy result |
| 12 | `Decision Engine` / `Offer Builder` | `Decision Engine` | Create `Loan Offer` |
| 13 | `Decision Engine` / `Decision Recorder` | `Decision Store` | Persist score, policy basis, calculations, `Loan Offer`, and `Decision Record` |
| 14 | `Decision Engine` / `Decision Recorder` | `Audit Log` | Record decision and integration evidence |
| 15 | `Decision Engine` | `Mobile App` | Return `Loan Offer` and decision outcome |
| 16 | `Mobile App` | `Customer` | Display `Loan Offer` and decision |

### 3.4 Alternatives

- **alt `CON.2`:** `Loan Application Service` returns an out-of-segment result. `Decision Engine` records `Submitted -> Rejected`, stores the reason, and returns rejection through `Mobile App`. No scoring or approval occurs.
- **alt `CON.3`:** `Credit Scoring System` times out or is unavailable. `Credit Scoring Adapter` returns controlled failure; `Decision Engine` records `Scoring -> Failed` and does not approve.
- **alt `CON.1`:** `Policy Engine` reports an unsecured amount above 100,000,000 VND. `Decision Engine` records `OfferReady -> Rejected`, retains policy evidence, and does not approve.

## 4. UML Sequence - Disburse Approved Loan Application

### 4.1 Header

```text
Title:      Disburse Approved Loan Application
Viewpoint:  UML Sequence
Layer(s):   Base - delivery behavior
As-Is | To-Be | Transition:  To-Be
Owner:      Dev  Name Nguyễn Thanh Hải
RACI:       R Nguyễn Thanh Hải  A Vũ Thế Quân  C Lý Bá Duy  I Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     Customer, C4 containers, messages, state outcomes, alt branches
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      approved application disbursement
```

### 4.2 Lifelines

| Lifeline | Kind | Resolution |
|----------|------|------------|
| `Customer` | Actor | Lab 1 I-2 actor |
| `Mobile App` | C4 container | Lab 9 L2 container |
| `Account Validation Service` | C4 container | Lab 9 L2 container |
| `Disbursement Adapter` | C4 container | Lab 9 L2 container |
| `ESB Integration Layer` | External system | Lab 9 external system |
| `Core Banking` | External system | Lab 9 external system |
| `Decision Store` | C4 container | Lab 9 L2 container |
| `Audit Log` | C4 container | Lab 9 L2 container |

### 4.3 Main sequence

| Step | Sender | Receiver | Message |
|-----:|--------|----------|---------|
| 1 | `Customer` | `Mobile App` | Accept `Nopbai Personal Loan Agreement` |
| 2 | `Mobile App` | `Account Validation Service` | Request payment-account validation |
| 3 | `Account Validation Service` | `Core Banking` | Request account eligibility confirmation |
| 4 | `Core Banking` | `Account Validation Service` | Return eligible payment-account result |
| 5 | `Account Validation Service` | `Disbursement Adapter` | Start approved disbursement after successful validation |
| 6 | `Disbursement Adapter` | `ESB Integration Layer` | Send disbursement and accounting request asynchronously |
| 7 | `ESB Integration Layer` | `Core Banking` | Route posting and disbursement request asynchronously |
| 8 | `Core Banking` | `ESB Integration Layer` | Return posting and disbursement confirmation or failure |
| 9 | `ESB Integration Layer` | `Disbursement Adapter` | Return routed banking outcome |
| 10 | `Disbursement Adapter` | `Decision Store` | Persist `Disbursement Record` and outcome |
| 11 | `Disbursement Adapter` | `Audit Log` | Record integration and transaction evidence |
| 12 | `Disbursement Adapter` | `Mobile App` | Return disbursement outcome |
| 13 | `Mobile App` | `Customer` | Display disbursement result |

### 4.4 Alternatives

- **alt `CON.4` - account validation failure:** `Core Banking` cannot confirm an eligible account. `Account Validation Service` returns failure; `Mobile App` records `Approved -> Failed`; `Disbursement Adapter` sends no disbursement request.
- **alt `CON.4` - posting failure:** `Core Banking` cannot confirm the posting or payment outcome. `Disbursement Adapter` records `AccountValidated -> Failed`, retains the `Disbursement Record`, and does not mark the application `Disbursed`.

## 5. UML Sequence - Recommend Limit Increase

### 5.1 Header

```text
Title:      Recommend Limit Increase
Viewpoint:  UML Sequence
Layer(s):   Base - delivery behavior
As-Is | To-Be | Transition:  To-Be
Owner:      Dev  Name Nguyễn Thanh Hải
RACI:       R Nguyễn Thanh Hải  A Vũ Thế Quân  C Lý Bá Duy  I Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     Customer, C4 containers, Decision Engine modules, alt branches
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      eligible existing customer recommendation
```

### 5.2 Lifelines

| Lifeline | Kind | Resolution |
|----------|------|------------|
| `Customer` | Actor | Lab 1 I-2 actor |
| `Mobile App` | C4 container | Lab 9 L2 container |
| `Decision Engine` | C4 container | Lab 9 L2 container |
| `Loan Application Service` | C4 container | Lab 9 L2 container |
| `Policy Engine` | C4 container | Lab 9 L2 container |
| `Decision Store` | C4 container | Lab 9 L2 container |
| `Audit Log` | C4 container | Lab 9 L2 container |
| `Eligibility Evaluator` | Component inside `Decision Engine` | Only inside the selected container |
| `Offer Builder` | Component inside `Decision Engine` | Only inside the selected container |
| `Decision Recorder` | Component inside `Decision Engine` | Only inside the selected container |

### 5.3 Main sequence

| Step | Sender | Receiver | Message |
|-----:|--------|----------|---------|
| 1 | `Customer` | `Mobile App` | Request a limit-increase recommendation |
| 2 | `Mobile App` | `Decision Engine` | Start recommendation evaluation |
| 3 | `Decision Engine` / `Eligibility Evaluator` | `Loan Application Service` | Request existing-customer segment eligibility |
| 4 | `Loan Application Service` | `Decision Engine` / `Eligibility Evaluator` | Return eligible customer result |
| 5 | `Decision Engine` / `Offer Builder` | `Policy Engine` | Request recommendation amount and policy terms |
| 6 | `Policy Engine` | `Decision Engine` / `Offer Builder` | Return recommendation terms |
| 7 | `Decision Engine` / `Decision Recorder` | `Decision Store` | Persist recommendation and decision evidence |
| 8 | `Decision Engine` / `Decision Recorder` | `Audit Log` | Record recommendation evidence |
| 9 | `Decision Engine` | `Mobile App` | Return limit-increase recommendation |
| 10 | `Mobile App` | `Customer` | Display recommendation |

### 5.4 Alternatives

- **alt `CON.2`:** `Loan Application Service` returns an out-of-segment result. `Decision Engine` rejects the recommendation, records the reason, and returns the rejection through `Mobile App`.
- **alt `CON.1`:** `Policy Engine` determines that the recommended unsecured amount exceeds 100,000,000 VND. `Decision Engine` rejects the recommendation and retains policy evidence.

## 6. UML State - Loan Application

### 6.1 Header

```text
Title:      Loan Application lifecycle
Viewpoint:  UML State
Layer(s):   Base - delivery behavior
As-Is | To-Be | Transition:  To-Be
Owner:      Test  Name Lý Bá Duy
RACI:       R Lý Bá Duy  A Vũ Thế Quân  C Nguyễn Thanh Hải  I Nguyễn Cương Quyết (TN); Nguyễn Minh Hoàng
Version:    v1.0  Date 2026-08-22  Status Draft
Legend:     state, trigger, guard, terminal state, and constraint
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      one object: `Loan Application`
```

### 6.2 State machine

| From state | Trigger / guard | To state | Terminal |
|------------|-----------------|----------|----------|
| `Draft` | Customer starts an application | `Submitted` | No |
| `Submitted` | Customer submits through `Mobile App` | `Scoring` | No |
| `Submitted` | Out-of-segment customer; `CON.2` | `Rejected` | Yes |
| `Scoring` | `Credit Scoring Adapter` returns a `Credit Score` | `OfferReady` | No |
| `Scoring` | Scoring timeout or unavailable; `CON.3` | `Failed` | Yes |
| `OfferReady` | Customer accepts `Nopbai Personal Loan Agreement` | `Approved` | No |
| `OfferReady` | Policy cap or decision rule rejects the offer; `CON.1` | `Rejected` | Yes |
| `OfferReady` | Customer declines the `Loan Offer` | `Rejected` | Yes |
| `Approved` | `Account Validation Service` confirms payment account | `AccountValidated` | No |
| `Approved` | Account validation fails; `CON.4` | `Failed` | Yes |
| `AccountValidated` | `Disbursement Adapter` sends request and `Core Banking` confirms | `Disbursed` | Yes |
| `AccountValidated` | Posting or confirmation fails; `CON.4` | `Failed` | Yes |

Terminal states are exactly `Rejected`, `Disbursed`, and `Failed`.

## 7. Participant = SUT map

Every container lifeline and test SUT resolves to an exact Lab 1 I-4 name. Actor lifelines resolve to Lab 1 I-2 names. Component names resolve only inside `Decision Engine`.

| Participant or SUT | Resolution | Allowed use |
|--------------------|------------|-------------|
| `Customer` | Lab 1 I-2 actor | Sequence participant |
| `Loan Operations Specialist` | Lab 1 I-2 actor | Optional exception/reconciliation participant only |
| `Mobile App` | Lab 1 I-4 container | Sequence participant / SUT |
| `Loan Application Service` | Lab 1 I-4 container | Sequence participant / SUT |
| `Credit Scoring Adapter` | Lab 1 I-4 container | Sequence participant / SUT |
| `Decision Engine` | Lab 1 I-4 container | Sequence participant / SUT |
| `Policy Engine` | Lab 1 I-4 container | Sequence participant / SUT |
| `Account Validation Service` | Lab 1 I-4 container | Sequence participant / SUT |
| `Disbursement Adapter` | Lab 1 I-4 container | Sequence participant / SUT |
| `Decision Store` | Lab 1 I-4 container | Sequence participant / SUT |
| `Audit Log` | Lab 1 I-4 container | Sequence participant / SUT |
| `Credit Scoring System` | Lab 1 I-3 external system | External sequence participant |
| `ESB Integration Layer` | Lab 1 I-3 external system | External sequence participant |
| `Core Banking` | Lab 1 I-3 external system | External sequence participant |
| `Decision Orchestrator` | Component inside `Decision Engine` | Internal component only |
| `Eligibility Evaluator` | Component inside `Decision Engine` | Internal component only |
| `Score Coordinator` | Component inside `Decision Engine` | Internal component only |
| `Policy Evaluation Module` | Component inside `Decision Engine` | Internal component only |
| `Offer Builder` | Component inside `Decision Engine` | Internal component only |
| `Decision Recorder` | Component inside `Decision Engine` | Internal component only |

## 8. G6 coverage note

The coverage list is planned evidence, not executed testing. Every I-6 transition and every named-use-case sequence alternative is mapped below.

### 8.1 State-transition coverage

| Coverage ID | State transition | Planned test | SUT |
|-------------|------------------|--------------|-----|
| G6-S01 | `Draft -> Submitted` | Customer starts and submits a Loan Application | `Mobile App` |
| G6-S02 | `Submitted -> Scoring` | Valid in-segment application starts decisioning | `Loan Application Service` |
| G6-S03 | `Submitted -> Rejected`; `CON.2` | Out-of-segment application is rejected before scoring | `Loan Application Service` |
| G6-S04 | `Scoring -> OfferReady` | Credit Score and accepted policy evaluation create a Loan Offer | `Decision Engine` |
| G6-S05 | `Scoring -> Failed`; `CON.3` | Scoring timeout produces controlled failure | `Credit Scoring Adapter` |
| G6-S06 | `OfferReady -> Approved` | Customer accepts the agreement and policy allows approval | `Decision Engine` |
| G6-S07 | `OfferReady -> Rejected`; `CON.1` | Amount cap breach rejects the Loan Offer | `Decision Engine` |
| G6-S08 | `OfferReady -> Rejected` | Customer declines the Loan Offer | `Mobile App` |
| G6-S09 | `Approved -> AccountValidated` | Eligible payment account is confirmed | `Account Validation Service` |
| G6-S10 | `Approved -> Failed`; `CON.4` | Account validation failure prevents disbursement | `Account Validation Service` |
| G6-S11 | `AccountValidated -> Disbursed` | Core Banking confirms posting and disbursement | `Disbursement Adapter` |
| G6-S12 | `AccountValidated -> Failed`; `CON.4` | Posting confirmation failure prevents `Disbursed` | `Disbursement Adapter` |

### 8.2 Sequence alternative coverage

| Coverage ID | Use case | Alternative | Planned test | SUT |
|-------------|----------|-------------|--------------|-----|
| G6-A01 | `Submit and Decide Loan Application` | `CON.2` out-of-segment | Rejection skips scoring and approval | `Decision Engine` |
| G6-A02 | `Submit and Decide Loan Application` | `CON.3` scoring timeout | Controlled failure produces `Failed` | `Credit Scoring Adapter` |
| G6-A03 | `Submit and Decide Loan Application` | `CON.1` amount cap | Offer is rejected and policy evidence retained | `Decision Engine` |
| G6-A04 | `Disburse Approved Loan Application` | `CON.4` account validation failure | No disbursement request is sent | `Account Validation Service` |
| G6-A05 | `Disburse Approved Loan Application` | `CON.4` posting failure | Application is not marked `Disbursed` | `Disbursement Adapter` |
| G6-A06 | `Recommend Limit Increase` | `CON.2` out-of-segment | Recommendation is rejected | `Decision Engine` |
| G6-A07 | `Recommend Limit Increase` | `CON.1` amount cap | Recommendation is rejected | `Decision Engine` |

## 9. Comparison note: Lab 5 baseline versus this Lab 10 specification

Lab 5 is not available or required under the agreed scope assumption. The comparison therefore records the intended audit dimensions rather than claiming a direct file-to-file audit.

| Audit dimension | Lab 5 baseline | Lab 10 Guide result |
|-----------------|----------------|---------------------|
| Named use cases | Not supplied | All three I-11 use cases are specified |
| Participant names | Not supplied | Container participants resolve to Lab 9/I-4 names; modules stay inside `Decision Engine` |
| State object | Not supplied | One object only: `Loan Application` |
| State names | Not supplied | Exact I-6 states are used |
| Exception branches | Not supplied | Every sequence has `alt` branches with `CON.*` |
| Header and RACI | Not supplied | Header and per-artifact RACI are defined |
| Mixed language | Not supplied | UML is used for behavior/state; C4 names are referenced, not redrawn as another notation |
| G6 coverage | Not supplied | All 12 state-transition branches and 7 sequence alternatives are listed |

## 10. Lab 10 completion check

- [x] Three named UML sequence specifications are present.
- [x] Each sequence has at least one `alt` branch with a `CON.*` reference.
- [x] One UML State specification exists for `Loan Application`.
- [x] State names match Lab 1 I-6 exactly.
- [x] Participant and SUT names resolve to Lab 1 I-2/I-3/I-4 or allowed internal modules.
- [x] Internal modules appear only inside `Decision Engine`.
- [x] G6 coverage lists all 12 state-transition rows and 7 sequence alternatives.
- [x] Each artifact has a header, legend, scope, and RACI assignment.
- [x] No source code, runtime test, deployment, or new system is introduced.
- [ ] G6 formally approved by Test/SA.

**Current result:** Lab 10 is complete as a Draft UML specification. G6 remains **Pending** until Test/SA review and approval.
