# Runtime specification trace

Specification authority is Lab 1 I-1 through I-11, the Labs 8-10 after pack, the Lab 3 contract/exception/test registers, Lab 7 G1-G6, and [`openapi.json`](openapi.json). This file does not add another use case, state, container, external system, or operation.

## Public operation trace

| Model source | Path | `operationId` | Success | Mode | Executable test IDs |
|---|---|---|---|---|---|
| I-11 `Submit and Decide Loan Application` | `POST /loan-applications:submit-and-decide` | `submitAndDecideLoanApplication` | `200` | Application operation / Sync envelope | `CAP-I11-01`, `CAP-A01`, `CAP-A02`, `CAP-A03`, `CAP-N01`, `CAP-N04`, `CAP-N07`, `CAP-P95-01`, `CAP-OAS-01` |
| I-11 `Disburse Approved Loan Application` | `POST /loan-applications/{loanApplicationId}:disburse` | `disburseApprovedLoanApplication` | `200` | Application operation; internally preserves C-02/C-03 Async | `CAP-I11-02`, `CAP-A04`, `CAP-A05`, `CAP-N02`, `CAP-N03`, `CAP-N07`, `CAP-OAS-01` |
| I-11 `Recommend Limit Increase` | `POST /customers/{customerId}:recommend-limit-increase` | `recommendLimitIncrease` | `200` | Application operation / Sync envelope | `CAP-I11-03`, `CAP-A06`, `CAP-A07`, `CAP-OAS-01` |
| C-01 `Get Credit Score` | `POST /integration/credit-scoring:get-credit-score` | `getCreditScore` | `200` | HTTPS request/response / Sync | `CAP-C01`, `CAP-OAS-01` |
| C-02 `Disbursement and Accounting Request` | `POST /integration/disbursements:request` | `disbursementAndAccountingRequest` | `202` | Message with confirmation and reconciliation / Async | `CAP-C02`, `CAP-N09`, `CAP-OAS-01` |
| C-03 `Post Disbursement and Accounting` | `POST /integration/disbursements:post` | `postDisbursementAndAccounting` | `202` | Message with confirmation and reconciliation / Async | `CAP-C03`, `CAP-N10`, `CAP-OAS-01` |

There are exactly six paths, each with exactly one `POST` operation. `CAP-OAS-01` compares the runtime route and request-contract registers with `openapi.json`, including methods, `operationId`, exact `summary` / `x-model-operation`, status sets, required fields, allowed properties, primitive types, and enums. It also executes malformed requests to prove the runtime does not silently accept payloads outside the committed schema.

## I-11 happy paths and drawn alternatives

| Test ID | G6 source | Use case | Trigger | Expected state/result and compensation | SUT |
|---|---|---|---|---|---|
| `CAP-I11-01` | I-11 happy path | `Submit and Decide Loan Application` | Eligible salaried existing customer aged 22-35, successful score, accepted policy and amount <= 100,000,000 VND | `Loan Offer` and decision evidence are persisted; state reaches `OfferReady`; response is `200` | `Decision Engine` |
| `CAP-I11-02` | I-11 happy path | `Disburse Approved Loan Application` | Approved application, accepted agreement, eligible account, confirmed posting | Account is validated; C-02/C-03 pass through the in-process async queue; `Core Banking` fake creates the `Disbursement Record` reference; state reaches `Disbursed`; response is `200` | `Disbursement Adapter` |
| `CAP-I11-03` | I-11 happy path | `Recommend Limit Increase` | Eligible existing customer and accepted policy/amount | The existing I-7 `Loan Offer` is stored in `Decision Store` and returned with `200`; no recommendation identity is created | `Decision Engine` |
| `CAP-A01` | `G6-A01` | `Submit and Decide Loan Application` | `CON.2`: outside initial segment | `Loan Application Service` rejects `Submitted -> Rejected` before calling `Decision Engine`; scoring/approval are skipped and rejection evidence is appended | `Loan Application Service` |
| `CAP-A02` | `G6-A02` | `Submit and Decide Loan Application` | `CON.3`: scoring timeout/unavailable | `Credit Scoring Adapter` returns controlled failure; decisioning stops, state becomes `Failed`, approval is absent, and timeout evidence is appended; response is `503` | `Credit Scoring Adapter` |
| `CAP-A03` | `G6-A03` | `Submit and Decide Loan Application` | `CON.1`: amount cap or policy rejection | `Decision Engine` rejects `OfferReady -> Rejected`, prevents approval, persists policy basis/evidence, and returns `422` | `Decision Engine` |
| `CAP-A04` | `G6-A04` | `Disburse Approved Loan Application` | `CON.4`: account validation fails | `Account Validation Service` changes `Approved -> Failed`, records evidence, and sends no request to `Disbursement Adapter`; response is `422` | `Account Validation Service` |
| `CAP-A05` | `G6-A05` | `Disburse Approved Loan Application` | `CON.4`: posting/confirmation fails | `Disbursement Adapter` does not mark `Disbursed`, changes `AccountValidated -> Failed`, retains reconciliation evidence, and returns `502` | `Disbursement Adapter` |
| `CAP-A06` | `G6-A06` | `Recommend Limit Increase` | `CON.2`: outside initial segment | `Loan Application Service` rejects before `Decision Engine` evaluation, records evidence, returns `422`, and creates no `Loan Offer` | `Loan Application Service` |
| `CAP-A07` | `G6-A07` | `Recommend Limit Increase` | `CON.1`: amount cap or policy rejection | `Decision Engine` rejects, persists policy basis and audit evidence, returns `422`, and creates no `Loan Offer` | `Decision Engine` |

This table is the G5 executable compensation specification: each `CAP-A*` assertion checks both the stable error and the named state/neighbour/evidence compensation. Merely observing a 4xx/5xx does not pass the test.

## I-6 transition trace

| Test ID | G6 source | Exact transition | Trigger | SUT |
|---|---|---|---|---|
| `CAP-S01` | `G6-S01` / `T-01` | `Draft -> Submitted` | Customer starts and submits a `Loan Application` | `Mobile App` |
| `CAP-S02` | `G6-S02` / `T-02` | `Submitted -> Scoring` | Valid in-segment application starts decisioning | `Loan Application Service` |
| `CAP-S03` | `G6-S03` / `T-03` | `Submitted -> Rejected` | `CON.2` segment rejection before decisioning | `Loan Application Service` |
| `CAP-S04` | `G6-S04` / `T-04` | `Scoring -> OfferReady` | Score and accepted policy produce a `Loan Offer` | `Decision Engine` |
| `CAP-S05` | `G6-S05` / `T-05` | `Scoring -> Failed` | `CON.3` controlled scoring failure | `Credit Scoring Adapter` |
| `CAP-S06` | `G6-S06` / `T-06` | `OfferReady -> Approved` | Customer accepts `Nopbai Personal Loan Agreement` through `Mobile App` | `Mobile App` |
| `CAP-S07` | `G6-S07` / `T-07` | `OfferReady -> Rejected` | `CON.1` amount cap or policy rejection | `Decision Engine` |
| `CAP-S08` | `G6-S08` / `T-08` | `OfferReady -> Rejected` | Customer declines the `Loan Offer` | `Mobile App` |
| `CAP-S09` | `G6-S09` / `T-09` | `Approved -> AccountValidated` | Eligible payment account confirmed | `Account Validation Service` |
| `CAP-S10` | `G6-S10` / `T-10` | `Approved -> Failed` | `CON.4` account validation failure | `Account Validation Service` |
| `CAP-S11` | `G6-S11` / `T-11` | `AccountValidated -> Disbursed` | Confirmed ESB/Core Banking outcome | `Disbursement Adapter` |
| `CAP-S12` | `G6-S12` / `T-12` | `AccountValidated -> Failed` | `CON.4` posting/confirmation failure | `Disbursement Adapter` |

All state tests exercise the typed `Loan Application` object. Terminal states remain exactly `Rejected`, `Disbursed`, and `Failed`; the tests do not expose additional public paths.

## Contract, hard-rule, and quality evidence

| Test ID | Requirement | Executable assertion |
|---|---|---|
| `CAP-C01` | C-01 `Get Credit Score` | Only `Credit Scoring Adapter` calls the `Credit Scoring System` fake; success is `200`; controlled timeout is `503 CON.3`; mode remains HTTPS request/response / Sync |
| `CAP-C02` | C-02 `Disbursement and Accounting Request` | Only `Disbursement Adapter` puts the request on the in-process queue; accepted envelope is `202`; mode remains Message with confirmation and reconciliation / Async |
| `CAP-C03` | C-03 `Post Disbursement and Accounting` | Only `ESB Integration Layer` invokes the `Core Banking` fake through the queue; accepted envelope is `202`; the returned reference remains owned by `Core Banking` |
| `CAP-N01` | I-5 approval prerequisites | Attempts to skip segment eligibility, scoring, accepted policy, or maximum-amount calculation are rejected under `CON.1`, `CON.2`, or `CON.3`; no `Approved`/`Disbursed` result is possible |
| `CAP-N02` | I-5 / `CON.4` approval and product-purpose preconditions | Disbursement of a missing/not-approved `Loan Application`, or of the `limit-increase` lifecycle used only by `Recommend Limit Increase`, returns `422 CON.4`; state is retained and no ESB/Core Banking activity occurs |
| `CAP-N03` | I-5 / `CON.4` account-validation precondition | A failed account validation cannot reach `Disbursement Adapter`; response is `422 CON.4` and downstream state is unchanged |
| `CAP-N04` | I-5 / `CON.1` amount cap | An amount greater than 100,000,000 VND returns `422 CON.1`, creates no `Loan Offer`, and cannot approve |
| `CAP-N05` | I-5 / I-9 forbidden credit evaluation | Test attempts credit evaluation from `Mobile App`; the unregistered path is rejected and the scoring fake call count is unchanged |
| `CAP-N06` | I-5 / I-9 forbidden Core Banking write | Test attempts a `Mobile App` -> `Core Banking` write; the unregistered path is rejected and Core Banking fake state is unchanged |
| `CAP-N07` | `CON.5` authorization and auditability | A false `X-Simulated-Authorized` call returns `403 CON.5`, retains the exact state, touches no downstream fake, and appends security evidence |
| `CAP-N08` | I-7 single ownership | Mutation of a defensive `Loan Application` view cannot change the owner-held aggregate; `Decision Store` has no application collection |
| `CAP-N09` | C-02 / `CON.4` owner-state precondition | A direct C-02 caller cannot assert `account_validated=true` to bypass the actual `Loan Application Service`-owned `AccountValidated` state or alter the owner-held amount; runtime returns `502 CON.4` and queues nothing |
| `CAP-N10` | C-03 / `CON.4` pending-message and owner-state precondition | A direct C-03 caller cannot post without an owner-authorized, pending C-02 message for an `AccountValidated` application; runtime returns `502 CON.4` and does not call `Core Banking` |
| `CAP-OAS-01` | G4 runtime/spec parity | Loaded OpenAPI version is `3.0.3`; exactly six `POST` operations exist; route, `operationId`, exact model string, status sets, and request-field contracts equal the runtime registers; malformed/missing/extra fields are rejected with documented `CON.*` envelopes |
| `CAP-I3-01` | I-3 is mocked | Exactly `Credit Scoring System`, `ESB Integration Layer`, and `Core Banking` are in-process fakes; no real host, socket, credential, or production secret is used |
| `CAP-P95-01` | I-1 measurable outcome | Multiple standard happy-path decisions are measured and calculated P95 remains <= 30 seconds |

## Source-code trace

| Code | Model authority | Primary executable evidence |
|---|---|---|
| `nopbai/mobile_app.py` | I-4 `Mobile App`; I-5 steps 1/3/4; I-9 forbidden path | `CAP-I11-01..03`, `CAP-S01`, `CAP-S06`, `CAP-S08`, `CAP-N05`, `CAP-N06` |
| `nopbai/loan_application_service.py` | I-4 `Loan Application Service`; I-7 `Loan Application`; `CON.2` | `CAP-A01`, `CAP-A06`, `CAP-S02`, `CAP-S03`, `CAP-N08..N10` |
| `nopbai/credit_scoring_adapter.py` | I-4 `Credit Scoring Adapter`; C-01; `CON.3` | `CAP-A02`, `CAP-C01`, `CAP-S05` |
| `nopbai/decision_engine.py` | I-4 `Decision Engine`; one I-11 expanded container; `CON.1` | `CAP-I11-01`, `CAP-I11-03`, `CAP-A03`, `CAP-A07`, `CAP-S04`, `CAP-S07` |
| `nopbai/policy_engine.py` | I-4 `Policy Engine`; I-7 `Policy Configuration`; `CON.1` | `CAP-I11-01`, `CAP-I11-03`, `CAP-A03`, `CAP-A07` |
| `nopbai/account_validation_service.py` | I-4 `Account Validation Service`; local read-only account input; `CON.4` | `CAP-A04`, `CAP-S09`, `CAP-S10` |
| `nopbai/disbursement_adapter.py` | I-4 `Disbursement Adapter`; C-02; `CON.4` reconciliation | `CAP-I11-02`, `CAP-A05`, `CAP-C02`, `CAP-C03`, `CAP-S11`, `CAP-S12`, `CAP-N09`, `CAP-N10` |
| `nopbai/decision_store.py` | I-4 `Decision Store`; I-7 `Loan Offer` and `Decision Record` | `CAP-I11-01`, `CAP-I11-03`, `CAP-A03`, `CAP-A07` |
| `nopbai/audit_log.py` | I-4 `Audit Log`; `CON.5` evidence | `CAP-A01..A07`, `CAP-N07` |
| `nopbai/application.py` | Three exact I-11 application operations and composition | `CAP-I11-01..03`, `CAP-A01..A07` |
| `nopbai/domain.py` | Typed I-6 `Loan Application` and nine exact states under the I-7 owner | `CAP-S01..S12`, `CAP-N08` |
| `nopbai/fakes.py` | Three exact I-3 black boxes; C-01 through C-03; in-process bus | `CAP-C01..C03`, `CAP-I3-01`, `CAP-N02`, `CAP-N03`, `CAP-N05..N07`, `CAP-N09`, `CAP-N10` |
| `nopbai/routing.py` | Exactly six frozen operations, request shapes, and stable status/error form | `CAP-C01..C03`, `CAP-I11-01..03`, `CAP-N01..N07`, `CAP-N09`, `CAP-N10`, `CAP-OAS-01` |
| `nopbai/identities.py` | Exact Lab 1 / Lab 10 strings | `CAP-OAS-01`, `CAP-I3-01` |
| `nopbai/errors.py` | Stable `CON.*` error envelope | `CAP-A01..A07`, `CAP-N01..N04`, `CAP-N07`, `CAP-OAS-01` |
| `nopbai/__main__.py` | Local simulation transport for the required demonstration; not a new I-4 identity | README live requests plus the same application paths covered by `CAP-I11-01` and `CAP-A02` |
| `tests/test_capstone_runtime.py` | Executable G4-G6, I-11, G5, I-5/I-9, I-7, I-3, and P95 evidence | All 38 stable IDs: `CAP-I11-01..03`, `CAP-A01..A07`, `CAP-C01..C03`, `CAP-S01..S12`, `CAP-N01..N10`, `CAP-OAS-01`, `CAP-I3-01`, `CAP-P95-01` |
| `openapi.json` | G4 public contract for exactly the six frozen operations | `CAP-OAS-01`, with operation execution in `CAP-I11-01..03` and `CAP-C01..C03` |

Package initializers contain no behavior and do not establish an identity.

## N/A: deliberately not built

| Source item | Capstone disposition |
|---|---|
| `Loan Operations Specialist` review of policy exceptions/reconciliation | N/A: not an I-11 standard-path use case; evidence is retained, but no manual-review operation is added |
| Customer declines `Loan Offer` | Covered as internal I-6 transition `CAP-S08`; N/A as a fourth public use case/path |
| Secured loans, business/SME loans, branch onboarding, manual underwriting | N/A per I-1 out of scope |
| Non-salaried or otherwise out-of-segment lending | N/A as a supported product journey; attempted inputs execute the required `CON.2` negative path only |
| Real I-3 connectivity, production credentials, production customer data | N/A and prohibited; `CAP-I3-01` proves the three fakes |
| Gateway, cluster, pod, database product, external message-broker product, mobile binary | N/A: product/infrastructure stand-up is not Capstone output and would create extra identities/deployables |
| Any operation outside the six rows above | N/A and non-callable; `CAP-OAS-01` proves absence |
