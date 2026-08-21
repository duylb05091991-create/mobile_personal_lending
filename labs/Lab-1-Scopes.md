## I-1. Team and topic

| Field | Your value |
|-------|------------|
| Group | Team 4: Nguyễn Cương Quyết (TN), Vũ Thế Quân, Lý Bá Duy, Nguyễn Thanh Hải, Nguyễn Minh Hoàng |
| Topic / initiative name | Nopbai Mobile Personal Loan |
| System-in-focus | Nopbai Personal Loan Platform |
| Goal | Provide a mobile-first unsecured personal loan journey with automated, policy-controlled decisioning and immediate disbursement. |
| Outcome (measurable) | ASSUMPTION: return an automated loan decision within P95 <= 30 seconds for standard applications. |
| Product | Nopbai Mobile Personal Loan |
| Contract | Nopbai Personal Loan Agreement |
| Baseline → target | Manual or fragmented assessment -> automated Mobile App application, decision, and disbursement flow. |
| In scope | Existing salaried customers aged 22-35; unsecured loans up to 100,000,000 VND; Mobile App; Loan Application Service; Credit Scoring Adapter and Credit Scoring System integration; Decision Engine; Policy Engine; Loan Offer; limit-increase recommendation; auto approval or rejection; Account Validation Service; Disbursement Adapter; ESB Integration Layer to Core Banking; Decision Store; Audit Log. |
| Out of scope | Secured loans; business or SME loans; branch onboarding; non-salaried customers; manual underwriting on the standard path; production implementation details; real customer data; production credentials. |

## I-2. Actors

| Name | ArchiMate | C4 (Person or —) | Role in the process |
|------|-----------|------------------|---------------------|
| Customer | Business Actor | Person | Submits the application, reviews the Loan Offer, and accepts the Nopbai Personal Loan Agreement. |
| Loan Operations Specialist | Business Actor | Person | Reviews only policy exceptions and reconciliation cases; not part of the standard approval path. |

## I-3. External systems

| Name (simulated) | Responsibility |
|------------------|----------------|
| Credit Scoring System | Returns a near-real-time Credit Score for an existing customer. |
| ESB Integration Layer | Routes accounting and disbursement messages between the platform and Core Banking. |
| Core Banking | Validates the payment account and records ledger and disbursement outcomes. |

Do not use real vendor contract IDs or production host names.

## I-4. Internal containers

Same strings on ArchiMate Application Cooperation and C4 Container.

| Name | Responsibility |
|------|----------------|
| Mobile App | Captures applications, displays Loan Offers and decisions, and collects agreement acceptance. |
| Loan Application Service | Validates and manages submitted Loan Applications. |
| Credit Scoring Adapter | Requests and normalizes responses from Credit Scoring System. |
| Decision Engine | Orchestrates eligibility, score, policy, offer, and approval or rejection decisions. |
| Policy Engine | Applies configurable eligibility, amount, rate, and approval rules. |
| Account Validation Service | Confirms that the customer payment account is eligible before disbursement. |
| Disbursement Adapter | Creates an idempotent disbursement request and handles the posting outcome. |
| Decision Store | Persists score, policy basis, calculations, Loan Offers, and decision records. |
| Audit Log | Persists decision, integration, and transaction evidence for audit. |

## I-5. Business process (happy path)

Numbered steps. Name the business object that moves.

1. Customer uses Mobile App to submit a Loan Application.
2. Loan Application Service validates the Loan Application and sends it through Decision Engine, Credit Scoring Adapter, and Policy Engine.
3. Decision Engine creates a Loan Offer, returns it through Mobile App, and records decision evidence in Decision Store and Audit Log.
4. Customer accepts the Nopbai Personal Loan Agreement.
5. Account Validation Service validates the customer payment account.
6. Disbursement Adapter sends the approved request through ESB Integration Layer to Core Banking, which confirms the disbursement and accounting outcome.

**Principle / hard rules** (what must never happen):

- No approval before eligibility, scoring, policy evaluation, and maximum amount calculation.
- No disbursement or accounting posting before approval and successful account validation.
- Mobile App must not perform credit evaluation or write directly to Core Banking.
- The unsecured loan amount must not exceed 100,000,000 VND.

## I-6. Named object states (use exactly on UML State)

**Object:** Loan Application (one business / data object — not a container)

| From state | Trigger / event | Next state | Next state terminal? |
|-------|-----------------|------------|-----------|
| Draft | Customer starts an application | Submitted | No |
| Submitted | Customer submits through Mobile App | Scoring | No |
| Submitted | Loan Application Service identifies an out-of-segment customer (`CON.2`) | Rejected | Yes |
| Scoring | Credit Scoring Adapter returns a Credit Score | OfferReady | No |
| Scoring | Credit Scoring System times out or is unavailable (`CON.3`) | Failed | Yes |
| OfferReady | Customer accepts the Nopbai Personal Loan Agreement | Approved | No |
| OfferReady | Policy cap or other decision rule rejects the Loan Offer (`CON.1`) | Rejected | Yes |
| OfferReady | Customer declines the Loan Offer | Rejected | Yes |
| Approved | Account Validation Service confirms the payment account | AccountValidated | No |
| Approved | Account validation fails (`CON.4`) | Failed | Yes |
| AccountValidated | Disbursement Adapter sends the request and Core Banking confirms the outcome | Disbursed | Yes |
| AccountValidated | Core Banking posting or confirmation fails (`CON.4`) | Failed | Yes |

**Terminal states** (list them; every machine needs at least one):

- Rejected, Disbursed, Failed

Use these exact state strings on the UML State machine (Lab 5 / Lab 10) and in the Lab 3 test spec.

## I-7. Source of truth

| Data object | Meaning | Source of truth (one container or external) |
|-------------|---------|---------------------------------------------|
| Loan Application | Customer request and lifecycle state | Loan Application Service |
| Customer Profile | Existing customer, income, and account information | Core Banking |
| Credit Score | Risk score used by decisioning | Credit Scoring System |
| Policy Configuration | Eligibility, amount, rate, and decision rules | Policy Engine |
| Loan Offer | Proposed amount, rate, and repayment terms | Decision Store |
| Decision Record | Score, policy basis, calculations, final decision, and reference to the Loan Offer | Decision Store |
| Disbursement Record | Account validation and posting outcome | Core Banking |

`Loan Offer` owns the proposed customer-facing terms. `Decision Record` owns the decision evidence and final outcome, and references the `Loan Offer`; they are distinct records even though both are stored in Decision Store.

## I-8. Integration (label sync vs async on Container)

| Pattern | Mechanism | Example on your landscape |
|---------|-----------|---------------------------|
| Sync | HTTPS request/response | Credit Scoring Adapter -> Credit Scoring System for near-real-time scoring |
| Async | Message with confirmation and reconciliation | Disbursement Adapter -> ESB Integration Layer -> Core Banking for accounting and disbursement |
| Legacy / adapter (if any) | Adapter boundary | Credit Scoring Adapter and Disbursement Adapter isolate external contracts |

## I-9. Deployment

| Location | What runs there |
|----------|-----------------|
| Customer mobile device | Mobile App |
| Lending application runtime | Loan Application Service, Credit Scoring Adapter, Decision Engine, Policy Engine, Account Validation Service, Disbursement Adapter |
| Evidence data store | Decision Store, Audit Log |
| External banking integration zone | Credit Scoring System, ESB Integration Layer, Core Banking |

Forbidden path: Mobile App must not write directly to Core Banking or perform credit evaluation; all such actions go through the internal services and explicit external integration boundaries.

## I-10. Constraints (must appear on Motivation and on decision branches)

| ID | Constraint | Effect on the process |
|----|------------|------------------------|
| CON.1 | Unsecured loan amount must not exceed 100,000,000 VND. | Decision Engine rejects the Loan Offer when the calculated amount exceeds the cap. |
| CON.2 | Only existing salaried customers aged 22-35 are in the initial segment. | Loan Application Service rejects applications outside the product segment before decisioning. |
| CON.3 | Credit scoring must return near-real-time data; timeout is a controlled exception. | Credit Scoring Adapter sends a timeout outcome to Decision Engine, which records Failed and does not approve. |
| CON.4 | No disbursement or accounting posting before approval and successful account validation. | Account Validation Service must succeed before Disbursement Adapter sends a request through ESB Integration Layer. |
| CON.5 | Customer data and decision evidence must be protected and auditable. | Services enforce authenticated and authorized access and write traceability to Decision Store and Audit Log. |

## I-11. Named use cases for UML (not every component)

| Use case | Happy path | At least one exception (`alt`) |
|----------|------------|--------------------------------|
| Submit and Decide Loan Application | Customer submits through Mobile App; Loan Application Service validates; Decision Engine obtains Credit Score, applies Policy Engine, creates Loan Offer, and records decision evidence. | `alt CON.3`: Credit Scoring System timeout -> record Failed; no approval. |
| Disburse Approved Loan Application | Customer accepts Nopbai Personal Loan Agreement; Account Validation Service succeeds; Disbursement Adapter sends through ESB Integration Layer; Core Banking confirms. | `alt CON.4`: account validation or accounting confirmation fails -> record Failed; no disbursement completion. |
| Recommend Limit Increase | Decision Engine evaluates an eligible existing customer and creates a recommendation through Mobile App. | `alt CON.2`: customer is outside the initial segment -> reject the recommendation. |

**One container** for optional C4 Component (circle one): Decision Engine

---


# Legend

Short names used in the labs. `*` is a wildcard: `CON.*` means every constraint ID, not an element named `CON.*`.  
RACI letters and role abbreviations are in the [Guide](#guide).

### Input index

| Short | Means |
|-------|--------|
| **I-*** | Any Input section (`I-1`…`I-11`) |
| **I-1** | Team, topic, system-in-focus, goal, outcome, product, in/out |
| **I-2** | Actors |
| **I-3** | External systems |
| **I-4** | Internal containers (same strings on Application Cooperation and C4 Container) |
| **I-5** | Happy-path process + hard rules |
| **I-6** | Named object states (UML State) |
| **I-7** | Source of truth |
| **I-8** | Integration (sync / async / adapter) |
| **I-9** | Deployment locations + one forbidden path |
| **I-10** | Constraints table (`CON.1`…) |
| **I-11** | Named use cases + the **one** container for optional C4 Component |

### Constraints and optional ArchiMate IDs

| Short | Means |
|-------|--------|
| **CON.*** | All constraints from I-10 |
| **CON.n** | One constraint (`CON.1`, `CON.2`, or a named ID such as `CON.KYC`) |
| **MOT.CON.n** | Same rule drawn as an ArchiMate Motivation **Constraint** (optional prefix) |
| **MOT.GOAL.n** / **MOT.OUT.n** / **MOT.REQ.n** | Optional Motivation IDs for Goal / Outcome / Requirement |
| **STR.CAP.n** | Optional Strategy **Capability** ID |

### Quality gates

Full pass rules stay in the Guide. Do not add **G7**.

| Short | Means | Blocks |
|-------|--------|--------|
| **G1–G6** | The six quality gates (adopt as written) | — |
| **G1** | Strategy signed — goal, outcome, `CON.*` listed | Solution design |
| **G2** | Process + states — named states match the state view | Dev + Test design |
| **G3** | C4 Context + Container — names, externals, sync/async | Implementation |
| **G4** | Contracts — one contract per Container relationship | Coding of integrations |
| **G5** | Critical exception path — compensating action from `CON.*` | Production release |
| **G6** | Test coverage — every state transition and sequence `alt` | UAT sign-off |

### C4 zoom and UML / test

| Short | Means |
|-------|--------|
| **L1** | C4 Context |
| **L2** | C4 Container |
| **L3** | C4 Component — internals of **one** container |
| **L4** | C4 Code — out of pack unless I-1 scoped it |
| **`alt`** | UML sequence fragment: exception / decision branch (show `CON.*`) |
| **SUT** | System under test — must be a C4 / I-4 container name |
| **⊆** | Participants are a **subset** of named containers (and actors) |
| **LLD** | Low-level design (UML), not an MVP |

### Lab wording

| Short | Means |
|-------|--------|
| **Bound form** | The deliverable shape is fixed. Produce exactly the listed artifacts — no substitutes, no extras, no free-form slide deck instead |
| **Before pack** | Labs 1, 2 (before), 8, 9, 6, 5, 10 as first drawn, in your current style. Archived unchanged |
| **After pack** | The same views from Lab 4, restyled to the Guide |
| **Sitting** | One lab worked start-to-finish. Finish Done-when before opening the next |

### Other

| Short | Means |
|-------|--------|
| **AuthN** | Authentication |
| **IAM** | Identity and access management product (do not add as a new system if AuthN is already on the gateway) |
| **UAT** | User acceptance test |
| **MVP** | Minimum viable product — not trainee output in these labs |
| **JDBC** | Database protocol — fail if drawn on Motivation / Process |


# Submit checklist

Complete **Lab 1 then 2 then 3 … then 10**. Tick a row only when that lab is Done.

- [ ] **Lab 1:** Input I-1–I-11 complete
- [ ] **Lab 2:** requirements in current language; **no** G1–G6
- [ ] **Lab 3:** build list, to-be Component, to-be sequence, contract register, exception spec, test spec
- [ ] **Lab 4:** messy 1–3 copies kept; cleaned pack + comparison note (Guide not used)
- [ ] **Lab 5:** UML for named use cases; one object per state machine; archived
- [ ] **Lab 6:** ecosystem modeled, not built; **Labs 1–6 archived**
- [ ] **Lab 7:** adoption record + G1–G6 register. Not started before archive
- [ ] **Lab 8:** four named ArchiMate views; header + RACI; G1 / G2
- [ ] **Lab 9:** one Context (no internals) + one Container (sync/async); header + RACI
- [ ] **Lab 10:** Lab 5 UML audited vs C4 names; G6 note; comparison note
- [ ] After views: header + RACI + legend; English; simulated names only
- [ ] No MVP; no Kong / Keycloak / Kafka stand-up
