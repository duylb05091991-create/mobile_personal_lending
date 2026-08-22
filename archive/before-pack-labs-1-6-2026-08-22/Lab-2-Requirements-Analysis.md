# Lab 2 - Requirements, Analysis, Quality-Gate Boundary

**R:** BA (requirements)  
**A:** Owner  
**Status:** Lab 2 current-language draft. Lab 1 is the source of identity. This file does not approve Lab 2 or create a quality-gate register.

## Scope and source

This file uses the following locked Lab 1 names exactly:

- System-in-focus: `Nopbai Personal Loan Platform`
- Product: `Nopbai Mobile Personal Loan`
- Moving object: `Loan Application`
- Actors: `Customer`, `Loan Operations Specialist`
- External systems: `Credit Scoring System`, `ESB Integration Layer`, `Core Banking`
- Internal containers: `Mobile App`, `Loan Application Service`, `Credit Scoring Adapter`, `Decision Engine`, `Policy Engine`, `Account Validation Service`, `Disbursement Adapter`, `Decision Store`, `Audit Log`
- States: `Draft`, `Submitted`, `Scoring`, `OfferReady`, `Approved`, `AccountValidated`, `Rejected`, `Disbursed`, `Failed`
- Constraints: `CON.1` through `CON.5`

**Goal:** Provide a mobile-first unsecured personal loan journey with automated, policy-controlled decisioning and immediate disbursement.

**Outcome:** **ASSUMPTION:** Return an automated loan decision within P95 <= 30 seconds for standard applications.

**Scope boundary:** Existing salaried customers aged 22-35; unsecured loans up to 100,000,000 VND; Mobile App submission; scoring; policy-based amount and rate; Loan Offer; limit-increase recommendation; automatic approval or rejection; account validation; disbursement; accounting through ESB Integration Layer to Core Banking; Decision Store and Audit Log traceability.

## Requirements list

### Functional requirements

| ID | Requirement | Source / reason | Primary container or actor | State / object effect |
|----|-------------|----------------|----------------------------|-----------------------|
| FR-01 | Mobile App shall allow Customer to submit a Loan Application. | Goal; I-5 step 1 | Customer; Mobile App | `Draft -> Submitted`; Loan Application |
| FR-02 | Loan Application Service shall validate the Loan Application and customer eligibility before decisioning. | CON.2; I-5 step 2 | Loan Application Service | `Submitted -> Scoring` or `Submitted -> Rejected`; Loan Application |
| FR-03 | Credit Scoring Adapter shall retrieve a near-real-time Credit Score from Credit Scoring System. | CON.3; I-5 step 2 | Credit Scoring Adapter; Credit Scoring System | `Scoring -> OfferReady` or `Scoring -> Failed`; Credit Score |
| FR-04 | Policy Engine shall calculate the maximum eligible amount. | CON.1; I-5 step 2 | Policy Engine | Supports policy evaluation before `OfferReady`; Loan Offer |
| FR-05 | Policy Engine shall calculate a personalized interest rate. | Goal; I-5 step 2 | Policy Engine | Supports policy-compliant Loan Offer; Loan Offer |
| FR-06 | Decision Engine shall create and return a Loan Offer through Mobile App. | Goal; I-5 step 3 | Decision Engine; Mobile App | `Scoring -> OfferReady`; Loan Offer |
| FR-07 | Decision Engine shall approve or reject the Loan Application within policy rules. | CON.1 and CON.2; I-5 hard rules | Decision Engine | `OfferReady -> Approved` or `OfferReady -> Rejected`; Loan Application |
| FR-08 | Decision Engine shall support a limit-increase recommendation for an eligible existing customer. | In-scope outcome; I-11 use case | Decision Engine; Mobile App | Recommendation is rejected when `CON.2` fails; Loan Offer recommendation |
| FR-09 | Customer shall accept the Nopbai Personal Loan Agreement before Account Validation Service validates the payment account and disbursement proceeds. | I-5 steps 4-5; I-6 | Customer; Account Validation Service | `OfferReady -> Approved -> AccountValidated`; Loan Application |
| FR-10 | Account Validation Service and Disbursement Adapter shall support disbursement only after approval and successful account validation. | CON.4; I-5 steps 4-6 | Account Validation Service; Disbursement Adapter | `Approved -> AccountValidated -> Disbursed` or `Failed`; Disbursement Record |
| FR-11 | Disbursement Adapter shall send accounting and disbursement requests through ESB Integration Layer to Core Banking. | I-5 step 6; forbidden-path rule | Disbursement Adapter; ESB Integration Layer; Core Banking | `AccountValidated -> Disbursed` or `Failed`; Disbursement Record |
| FR-12 | Decision Store and Audit Log shall retain score, policy basis, calculations, Loan Offer, Decision Record, integration events, and outcomes. | CON.5; I-5 step 3 and step 6 | Decision Store; Audit Log | Evidence covers all relevant Loan Application states |

### Non-functional requirements

| ID | Requirement | Source / reason | Verification intent |
|----|-------------|----------------|---------------------|
| NFR-01 | Decisioning shall support a near-real-time Mobile App experience. | Outcome; CON.3 | Measure standard decision response time against the **ASSUMPTION** P95 <= 30 seconds target. |
| NFR-02 | The solution shall minimize incorrect decisions and failed accounting flows. | Goal; CON.1 and CON.4 | Check policy decision paths, account validation, and accounting failure handling. |
| NFR-03 | Customer data shall be protected with secure authentication, authorization, and banking security controls. | CON.5; out-of-scope production details excluded | Confirm access-control and protection requirements without naming a production product. |
| NFR-04 | Decisions, integrations, and transaction outcomes shall be auditable. | CON.5; FR-12 | Confirm evidence is written to Decision Store and Audit Log. |
| NFR-05 | Data shall remain consistent across the named containers and external systems that own Loan Application, Customer Profile, Credit Score, Policy Configuration, Loan Offer, Decision Record, and Disbursement Record. | I-7 source-of-truth rules; CON.5 | Trace each object to its single source of truth and integration outcome. |

## Analysis

### As-is and to-be

| Concern | As-is: manual or fragmented assessment | To-be: Nopbai Mobile Personal Loan |
|---------|----------------------------------------|------------------------------------------|
| Customer entry | Customer journey is manual or fragmented. | Customer uses Mobile App to submit a Loan Application. |
| Eligibility | Eligibility checks are not consistently automated. | Loan Application Service checks the existing salaried customer segment before decisioning. |
| Scoring | Credit information may be obtained through fragmented assessment. | Credit Scoring Adapter requests a near-real-time Credit Score from Credit Scoring System. |
| Decisioning | Assessment and policy decisions are fragmented. | Decision Engine coordinates Credit Scoring Adapter and Policy Engine, then applies policy-controlled approval or rejection. |
| Offer | Offer information is not produced through one automated journey. | Decision Engine creates a Loan Offer and Mobile App presents it to Customer. |
| Agreement and account | Acceptance and account checks are separate manual activities. | Customer accepts the Nopbai Personal Loan Agreement, then Account Validation Service validates the payment account. |
| Disbursement | Disbursement and accounting may require fragmented handoffs. | Disbursement Adapter sends through ESB Integration Layer to Core Banking only after approval and account validation. |
| Evidence | Decision evidence may be difficult to reconstruct. | Decision Store owns Loan Offer and Decision Record data; Audit Log retains decision, integration, and transaction evidence. |

### Capabilities implied by the goal

| Capability | Realized by | Boundary |
|------------|--------------|----------|
| Mobile loan application capture | Mobile App; Loan Application Service | Only the existing salaried customer segment is in scope. |
| Eligibility and policy decisioning | Decision Engine; Policy Engine | No approval before eligibility, Credit Score, policy evaluation, and maximum amount calculation. |
| Near-real-time credit assessment | Credit Scoring Adapter; Credit Scoring System | Timeout is a controlled exception and cannot approve an application. |
| Offer and limit recommendation | Decision Engine; Mobile App; Decision Store | Loan Offer terms are distinct from Decision Record evidence. |
| Controlled account validation | Account Validation Service; Core Banking through ESB Integration Layer | No disbursement or accounting posting before successful validation. |
| Idempotent disbursement and accounting | Disbursement Adapter; ESB Integration Layer; Core Banking | The Mobile App has no direct Core Banking path. |
| Decision traceability | Decision Store; Audit Log | Customer data and decision evidence must be protected and auditable. |

### Exception paths

| Exception | Trigger | Expected handling | State / evidence |
|-----------|---------|-------------------|------------------|
| Out-of-segment application | Customer is not an existing salaried customer aged 22-35. | Loan Application Service rejects before decisioning. | `Submitted -> Rejected`; record the reason in Decision Record and Audit Log. |
| Amount cap breach | Calculated unsecured amount exceeds 100,000,000 VND. | Decision Engine rejects the Loan Offer; no approval. | `OfferReady -> Rejected`; retain policy basis in Decision Store and Audit Log. |
| Credit scoring timeout | Credit Scoring System does not return near-real-time data. | Credit Scoring Adapter reports the controlled exception; Decision Engine does not approve. | `Scoring -> Failed`; record timeout evidence. |
| Customer declines Loan Offer | Customer does not accept the Loan Offer. | Do not continue to approval or account validation. | `OfferReady -> Rejected`; record the customer outcome. |
| Account validation failure | Core Banking cannot confirm an eligible payment account. | Disbursement Adapter must not send the disbursement request. | `Approved -> Failed`; record the failure and traceability evidence. |
| Accounting or disbursement failure | Core Banking cannot confirm the posting or payment outcome. | Do not mark the Loan Application as disbursed; reconcile the outcome. | `AccountValidated -> Failed`; record integration and transaction evidence. |
| Decision evidence access violation | Unauthorized access to customer data or evidence is attempted. | Deny access and retain auditable security evidence. | No business-state approval; Audit Log evidence. |

### Open assumptions and questions

The following are not resolved by Lab 2 and must not be silently converted into product facts:

- **Q1:** Exact eligibility and affordability rules.
- **Q2:** Credit Scoring System thresholds.
- **Q3:** Credit Scoring System request and response payload fields.
- **Q4:** Initial payment account definition and validation details.
- **Q5:** Final response-time and availability targets.

## Trace table

Each row traces a requirement to a Lab 1 process step, constraint or goal, and named object or state. No row introduces a system, actor, container, state, or object outside the Lab 1 identity index.

| Requirement | Lab 1 source | Process step | Constraint / rule | Named object or state |
|-------------|--------------|--------------|-------------------|-----------------------|
| FR-01 | Goal; I-5 | Step 1 | Mobile App must capture the submission | Loan Application; `Draft -> Submitted` |
| FR-02 | I-5; I-10 | Step 2 | `CON.2` | Loan Application; `Submitted -> Scoring` or `Rejected` |
| FR-03 | I-5; I-8 | Step 2 | `CON.3` | Credit Score; `Scoring -> OfferReady` or `Failed` |
| FR-04 | Goal; I-5 | Step 2 | `CON.1` | Loan Offer; `OfferReady` |
| FR-05 | Goal; I-5 | Step 2 | Policy hard rule | Loan Offer; `OfferReady` |
| FR-06 | Goal; I-5 | Step 3 | Policy hard rule | Loan Offer; `OfferReady` |
| FR-07 | I-5; I-6 | Step 3 | `CON.1`, `CON.2` | Loan Application; `OfferReady -> Approved` or `Rejected` |
| FR-08 | I-1; I-11 | Step 3 | `CON.2` | Loan Offer recommendation; `OfferReady` or rejection outcome |
| FR-09 | I-5; I-6 | Steps 4-5 | Agreement acceptance before account validation | Loan Application; `OfferReady -> Approved -> AccountValidated` |
| FR-10 | I-5; I-6 | Steps 4-6 | `CON.4` | Loan Application; `Approved -> AccountValidated -> Disbursed` or `Failed` |
| FR-11 | I-8; I-9 | Step 6 | Forbidden direct path; `CON.4` | Disbursement Record; `AccountValidated -> Disbursed` or `Failed` |
| FR-12 | I-7; I-5 | Steps 3 and 6 | `CON.5` | Loan Offer; Decision Record; Audit Log; all relevant states |
| NFR-01 | I-1 outcome; I-8 | Steps 2-3 | `CON.3` | `Scoring`; `OfferReady` |
| NFR-02 | Goal; I-5 | Steps 2-6 | `CON.1`, `CON.4` | Approved, Rejected, Failed, Disbursed |
| NFR-03 | I-10 | All evidence access | `CON.5` | Customer Profile; Decision Record; Audit Log |
| NFR-04 | I-7; I-10 | Steps 3 and 6 | `CON.5` | Decision Store; Audit Log |
| NFR-05 | I-7; I-8 | Steps 2-6 | Source-of-truth rules | Loan Application; Customer Profile; Credit Score; Policy Configuration; Loan Offer; Decision Record; Disbursement Record |

## Quality-gate boundary for Lab 2

Lab 2 does **not** create or pass a quality-gate register. Quality gates are deferred to Lab 7 as required by `list.md`. This file provides requirement and analysis evidence only:

- No pass/fail gate table is defined here.
- No competing quality-gate set is introduced.
- No C4 or ArchiMate diagram is required for this Lab 2 artifact.
- The requirements and trace table are inputs to later labs; they are not runtime proof, UAT evidence, or an approval record.

## Lab 2 completion check

- Requirements list exists in current language.
- As-is/to-be analysis exists.
- Exception paths are named for `CON.1` through `CON.5` where applicable.
- Trace table covers FR-01 through FR-12 and NFR-01 through NFR-05.
- Lab 1 goal, outcome, process, states, and constraints are represented.
- All names are drawn from the Lab 1 identity index.
- No quality-gate register is included.
