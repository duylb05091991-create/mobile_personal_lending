# Name and identity map

This map binds the one-process Python implementation to the exact Lab 1 I-4 names. A Python module, class, helper, in-memory collection, or fake is not an additional C4 Container or deployable identity.

## I-4 container collapse

| Exact I-4 container | Python module | Runtime representation | I-9 location represented | Physical process |
|---|---|---|---|---|
| `Mobile App` | `nopbai.mobile_app` | `MobileApp` simulation boundary | `Customer mobile device` | `python3 -m nopbai` |
| `Loan Application Service` | `nopbai.loan_application_service` | `LoanApplicationService` and authority over the `Loan Application` lifecycle | `Lending application runtime` | `python3 -m nopbai` |
| `Credit Scoring Adapter` | `nopbai.credit_scoring_adapter` | `CreditScoringAdapter` | `Lending application runtime` | `python3 -m nopbai` |
| `Decision Engine` | `nopbai.decision_engine` | `DecisionEngine` | `Lending application runtime` | `python3 -m nopbai` |
| `Policy Engine` | `nopbai.policy_engine` | `PolicyEngine` | `Lending application runtime` | `python3 -m nopbai` |
| `Account Validation Service` | `nopbai.account_validation_service` | `AccountValidationService` | `Lending application runtime` | `python3 -m nopbai` |
| `Disbursement Adapter` | `nopbai.disbursement_adapter` | `DisbursementAdapter` | `Lending application runtime` | `python3 -m nopbai` |
| `Decision Store` | `nopbai.decision_store` | `DecisionStore` in-memory evidence collection | `Evidence data store` | `python3 -m nopbai` |
| `Audit Log` | `nopbai.audit_log` | `AuditLog` append-only in-memory evidence collection | `Evidence data store` | `python3 -m nopbai` |

The nine rows above are the complete I-4 set. They are logical module boundaries collapsed into one standard-library process. The collapse does not create a tenth container and does not claim that a cluster, database, gateway, message-broker product, or production deployment was built.

## Supporting code that has no I-4 identity

| Code | Purpose | Identity rule |
|---|---|---|
| `nopbai.application` | Composition root and application-operation facade | Helper only; delegates to the nine mapped I-4 modules |
| `nopbai.domain` | Typed I-6 `Loan Application` aggregate and exact state enumeration | Domain helper under `Loan Application Service` ownership; not a container or second owner |
| `nopbai.identities` | Exact model strings, six paths, and six operation IDs | Constants only; not a container |
| `nopbai.errors` | Stable `CON.*` error envelope | Helper only; not a container or use case |
| `nopbai.fakes` | The three I-3 fakes and in-process asynchronous simulation | Mock backing services; not I-4 and not production systems |
| `nopbai.routing` | Dispatch for the six frozen OpenAPI operations | In-process helper; not an API-gateway identity |
| `nopbai.__main__` | Local HTTP simulation and ten-minute demonstration entry point | Starts the same collapsed process; not another deployable or production server |

## I-3 simulated external systems

| Exact I-3 name | Simulation | Allowed boundary | Production connectivity |
|---|---|---|---|
| `Credit Scoring System` | In-process deterministic fake returning a `Credit Score` or a controlled timeout/unavailable result | Called only by `Credit Scoring Adapter` using C-01 `Get Credit Score`, preserving HTTPS request/response / Sync semantics | None |
| `ESB Integration Layer` | In-process fake queue with confirmation and reconciliation evidence | Receives only from `Disbursement Adapter` using C-02 `Disbursement and Accounting Request`; routes C-03 onward | None |
| `Core Banking` | In-process deterministic fake for posting outcome and a `Disbursement Record` reference | Reached only through `ESB Integration Layer` using C-03 `Post Disbursement and Accounting` | None |

No real host, network call, customer record, vendor contract ID, secret, token, or production credential exists in this runtime.

## I-9 one-process collapse

| Exact I-9 location | What the process represents | Collapse note |
|---|---|---|
| `Customer mobile device` | `Mobile App` module | Logical presentation boundary in the process; no mobile binary is produced |
| `Lending application runtime` | `Loan Application Service`, `Credit Scoring Adapter`, `Decision Engine`, `Policy Engine`, `Account Validation Service`, `Disbursement Adapter` | Six exact service modules in one process |
| `Evidence data store` | `Decision Store`, `Audit Log` | In-memory collections, cleared when the process ends |
| `External banking integration zone` | Fakes labeled `Credit Scoring System`, `ESB Integration Layer`, and `Core Banking` | Simulation only; these fakes are not real deployments |

The I-9 forbidden path is preserved: `Mobile App` has no callable route to `Core Banking` and performs no credit evaluation.

## I-7 ownership

| Exact I-7 object | Sole source of truth | Runtime treatment |
|---|---|---|
| `Loan Application` | `Loan Application Service` | The typed aggregate and its transitions execute under this service's authority; other modules return inputs or request transitions but do not become owners |
| `Customer Profile` | `Core Banking` | The SA-approved account-validation request contains a simulated read-only eligibility input; it neither copies nor moves ownership |
| `Credit Score` | `Credit Scoring System` | The fake creates the simulated score; `Credit Scoring Adapter` only normalizes it |
| `Policy Configuration` | `Policy Engine` | Policy and amount-cap rules are enforced here and orchestrated by `Decision Engine` |
| `Loan Offer` | `Decision Store` | Persisted once by the exact owner and referenced by the response |
| `Decision Record` | `Decision Store` | Stored separately from, and references, the `Loan Offer` |
| `Disbursement Record` | `Core Banking` | The fake creates the master reference; `Audit Log` stores evidence/reference only |

## Allowed Lab 9 coupling

| Source | Target | Protocol / mode |
|---|---|---|
| `Mobile App` | `Loan Application Service` | HTTPS / Sync |
| `Loan Application Service` | `Decision Engine` | HTTPS / Sync |
| `Loan Application Service` | `Audit Log` | Internal call / Sync |
| `Decision Engine` | `Credit Scoring Adapter` | HTTPS / Sync |
| `Decision Engine` | `Policy Engine` | HTTPS / Sync |
| `Decision Engine` | `Decision Store` | Internal call / Sync |
| `Decision Engine` | `Audit Log` | Internal call / Sync |
| `Decision Engine` | `Mobile App` | HTTPS / Sync |
| `Mobile App` | `Account Validation Service` | HTTPS / Sync |
| `Account Validation Service` | `Audit Log` | Internal call / Sync |
| `Account Validation Service` | `Disbursement Adapter` | Internal call / Sync |
| `Disbursement Adapter` | `Audit Log` | Internal call / Sync |
| `Credit Scoring Adapter` | `Credit Scoring System` | HTTPS request/response / Sync |
| `Disbursement Adapter` | `ESB Integration Layer` | Message with confirmation and reconciliation / Async |
| `ESB Integration Layer` | `Core Banking` | Message with confirmation and reconciliation / Async |

Return values and asynchronous outcome legs use the initiating relationship and do not introduce another coupling. In particular, the runtime has no `Mobile App` -> `Core Banking`, `Account Validation Service` -> `Core Banking`, `Decision Engine` -> `Credit Scoring System`, or `Decision Engine` -> `Core Banking` call.

## Explicit assumptions

| ASSUMPTION | One frozen runtime choice |
|---|---|
| `ASSUMPTION-01` | The six URL paths, JSON fields, envelope statuses, and `X-Simulated-Authorized` string header are the SA-approved Capstone transport form; they do not add a use case or architectural protocol. |
| `ASSUMPTION-02` | Literal header value `true` grants simulated access and `false` or absence produces `403 CON.5`; it is a test switch, not a credential. |
| `ASSUMPTION-03` | Identifiers, score, offer rate/term, message IDs, and record references are deterministic simulated values suitable only for tests and demonstration. |
| `ASSUMPTION-04` | C-02 and C-03 are exposed as test-harness envelopes returning `202`; work, confirmation, and reconciliation remain an in-process Message / Async mechanism. |
| `ASSUMPTION-05` | The account-eligibility Boolean is a simulated read-only input received through `Mobile App`; `Account Validation Service` makes no direct `Core Banking` call. |
| `ASSUMPTION-06` | Process memory is the only persistence and queue medium. Restarting the demo clears applications, evidence, and messages. |
| `ASSUMPTION-07` | P95 is measured around deterministic, local `Submit and Decide Loan Application` calls; the acceptance threshold remains the exact I-1 outcome `P95 <= 30 seconds`. |
| `ASSUMPTION-08` | The SA-approved standalone `Recommend Limit Increase` mapping reuses the existing `Loan Application` lifecycle as `Draft -> Submitted -> Scoring -> OfferReady` (or the existing `Rejected` alternatives) and returns the existing `Loan Offer`. In this use case, `Scoring` is the frozen decision-evaluation lifecycle stage; no C-01 call is added because the approved Lab 10 Recommend sequence contains no credit-scoring leg. |
