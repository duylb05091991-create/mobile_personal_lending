# Name-identity map — Nopbai Mobile Personal Loan (Capstone I-11 runtime)

Every code module / package / process resolves to exactly one Lab 1 name. One
spelling per thing; the single source is `src/nopbai/names.py`. No name is forked.

## Process / collapse

The whole runtime is **one process** (`uvicorn nopbai.app:app`) with **one
in-memory store** and **in-process** calls between modules. This is a documented
collapse permitted by `capstone.md` ("one process / in-memory store / in-process
bus if modules keep Lab 1 / I-4 strings and the name map says so"). No I-4
container becomes a new identity; each remains a named module inside the process.

| Collapse | Stands for (I-9 location) | Documented as |
|----------|---------------------------|----------------|
| Single OS process `nopbai.app` | Lending application runtime (I-9) | one process |
| In-memory `DecisionStore`, `AuditLog` | Evidence data store (I-9) | in-memory store |
| In-process Python calls between container modules | Lending application runtime (I-9) | in-process bus |
| In-process fakes for I-3 externals | External banking integration zone (I-9) | mocked backing services |

## I-4 internal containers → code

| I-4 container (Lab 1) | Code module (`src/nopbai/…`) | Type identity |
|-----------------------|------------------------------|---------------|
| `Mobile App` | `containers/mobile_app.py` → `MobileApp` | I-4 container (collapsed module) |
| `Loan Application Service` | `containers/loan_application_service.py` → `LoanApplicationService` | I-4 container; I-7 owner of `Loan Application` |
| `Credit Scoring Adapter` | `containers/credit_scoring_adapter.py` → `CreditScoringAdapter` | I-4 container (boundary) |
| `Decision Engine` | `containers/decision_engine/engine.py` → `DecisionEngine` | I-4 container (I-11 selected; L3 drilled) |
| `Policy Engine` | `containers/policy_engine.py` → `PolicyEngine` | I-4 container; I-7 owner of `Policy Configuration` |
| `Account Validation Service` | `containers/account_validation_service.py` → `AccountValidationService` | I-4 container |
| `Disbursement Adapter` | `containers/disbursement_adapter.py` → `DisbursementAdapter` | I-4 container (boundary) |
| `Decision Store` | `containers/decision_store.py` → `DecisionStore` | I-4 container; I-7 owner of `Loan Offer`, `Decision Record` |
| `Audit Log` | `containers/audit_log.py` → `AuditLog` | I-4 container (evidence only) |

## Decision Engine L3 components (inside the one selected container)

These are modules **inside** `Decision Engine`, not new I-4 containers.

| Component (Lab 3 / Lab 9 §5.2) | Code (`containers/decision_engine/…`) |
|--------------------------------|----------------------------------------|
| `Decision Orchestrator` | flow methods on `engine.py → DecisionEngine` |
| `Eligibility Evaluator` | `components.py → EligibilityEvaluator` |
| `Score Coordinator` | `components.py → ScoreCoordinator` |
| `Policy Evaluation Module` | `components.py → PolicyEvaluationModule` |
| `Offer Builder` | `components.py → OfferBuilder` |
| `Decision Recorder` | `components.py → DecisionRecorder` |

## I-3 external systems → mocked backing services (in-process fakes)

| I-3 external (Lab 1) | Code (`src/nopbai/external/…`) | Contract |
|----------------------|--------------------------------|----------|
| `Credit Scoring System` | `credit_scoring_system.py → CreditScoringSystemFake` | C-01 |
| `ESB Integration Layer` | `esb_integration_layer.py → EsbIntegrationLayerFake` | C-02 |
| `Core Banking` | `core_banking.py → CoreBankingFake` | C-03 |

## I-6 object and states → code

| Lab 1 | Code |
|-------|------|
| `Loan Application` (I-6 object) | `domain/loan_application.py → LoanApplication` |
| States `Draft…Failed` (9) | `names.py` constants; guarded transitions on `LoanApplication` |
| `Loan Offer`, `Decision Record` (I-7) | `containers/decision_store.py` dataclasses |
| `Disbursement Record` (I-7, Core Banking master) | `external/core_banking.py → DisbursementRecord` |

## Actors → code

| Actor (I-2) | Code use |
|-------------|----------|
| `Customer` | authenticated principal (CON.5 header); demo/test caller |
| `Loan Operations Specialist` | reconciliation queue target on the CON.4 posting-failure alt (audit event) |

## ASSUMPTION rows (Lab 1 Input gaps; one string used everywhere)

Where Lab 1 / the Requirement Document left a value open (Q1–Q5, open points), a
plausible simulated value is used and marked `ASSUMPTION`. None invents a new
I-4 / I-6 / I-11 / external.

| ASSUMPTION | Value used | Why |
|------------|------------|-----|
| Scoring payload (Q3) | `customer_id` only; simulated score in [300,850] | Lab 1 leaves scoring fields open |
| Policy amount/rate rule (Q1/Q2) | max = min(score-derived ceiling, 100,000,000 VND); rate = f(score) | needed to compute a Loan Offer; CON.1 cap is the hard invariant |
| Payment account (Q4) | `payment_account_id` + eligibility flag on the application | Lab 1 leaves the payment account open |
| Response-time / availability (Q5) | not asserted at runtime | out of the approved Lab 1–4 baseline (Lab 7 §4.1) |
| CON.5 AuthN mechanism | required `X-Customer-Id` principal header (no IAM product) | Lab 9 open point: mechanism governed by CON.5, not a new product |
| CON.4 status split | validation failure → 422; posting/confirmation failure → 502 | one named CON.4 alt, two drawn branches (G6-A04/A05) |
