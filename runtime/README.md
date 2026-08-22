# Nopbai Personal Loan Platform - Capstone runtime

This folder is the independent, runnable I-11 slice defined by Labs 1-10. It implements exactly three named I-11 use cases and the three Lab 3 contract-register operations in one Python 3.9 standard-library process. The implementation is outside the modeling packs and does not modify Labs 1-10.

## What is included

- All three I-11 happy paths and all seven alternatives frozen in Lab 10.
- A typed `Loan Application` with the nine exact I-6 states and twelve exact transitions. Every transition records the exact I-4 `performed_by` participant and the sole `written_by` owner, `Loan Application Service`.
- Exactly nine logical I-4 modules, collapsed into one process as documented in [`NAME-IDENTITY-MAP.md`](NAME-IDENTITY-MAP.md).
- Exactly three I-3 in-process fakes listed in [`I-3-MOCK-LIST.md`](I-3-MOCK-LIST.md); no live external call or production credential.
- Exactly six `POST` operations in OpenAPI 3.0.3 at [`openapi.json`](openapi.json).
- Runtime validation enforces each committed request schema (required/allowed fields, primitive types, and enums) and returns only documented `CON.*` error envelopes.
- An in-memory store and in-process queue. C-02/C-03 preserve Message with confirmation and reconciliation / Async semantics.
- Executable G4-G6, I-5/I-9 negative, ownership, compensation, and P95 evidence traced in [`SPEC-TRACE.md`](SPEC-TRACE.md).

## Requirements

- Python 3.9 or newer.
- No package installation and no external network access. The runnable API binds only to the local simulation address unless the operator changes the non-secret host/port configuration.
- Run commands from this `runtime` directory.

## Run all automated tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The suite uses stable IDs `CAP-I11-*`, `CAP-A*`, `CAP-C*`, `CAP-S*`, `CAP-N*`, `CAP-OAS-01`, `CAP-I3-01`, and `CAP-P95-01`. A passing run is test evidence, not human SA acceptance.

## Run the demonstration

```bash
python3 -m nopbai
```

This starts the deterministic local HTTP simulation at `http://127.0.0.1:8080`. It uses the same application facade and route register as the tests; it is not a production server and makes no outbound call. `NOPBAI_HOST` and `NOPBAI_PORT` may change the local bind address; neither setting is a credential.

With the process running, execute the happy path from a second terminal:

```bash
curl -sS -X POST 'http://127.0.0.1:8080/loan-applications:submit-and-decide' \
  -H 'Content-Type: application/json' \
  -H 'X-Simulated-Authorized: true' \
  -d '{"customer_id":"demo-happy","existing_customer":true,"salaried":true,"age":30,"requested_amount":50000000,"scoring_mode":"success","policy_mode":"accept"}'
```

Then execute the named `alt CON.3`:

```bash
curl -sS -X POST 'http://127.0.0.1:8080/loan-applications:submit-and-decide' \
  -H 'Content-Type: application/json' \
  -H 'X-Simulated-Authorized: true' \
  -d '{"customer_id":"demo-con3","existing_customer":true,"salaried":true,"age":30,"requested_amount":50000000,"scoring_mode":"timeout","policy_mode":"accept"}'
```

Stop the local process with `Ctrl-C` after the live calls.

## Required ten-minute demo order

1. State the exact I-1 goal: “Provide a mobile-first unsecured personal loan journey with automated, policy-controlled decisioning and immediate disbursement.”
2. Show one I-11 UML sequence from `../labs/Lab-10-UML low-level design for named C4 use cases.md` and identify the exact I-4 participants.
3. Run `python3 -m nopbai`, then execute the happy-path request above and show `Submit and Decide Loan Application` returning `OfferReady` plus a `Loan Offer`.
4. Execute the timeout request above and show the live named `alt CON.3`: `503`, `Scoring -> Failed`, no approval, and retained audit evidence asserted by `CAP-A02`.
5. Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` and show the executed report.

## Frozen operation boundary

| Source identity | Method and path | `operationId` | Required `X-Caller` | Success |
|---|---|---|---|---|
| `Submit and Decide Loan Application` | `POST /loan-applications:submit-and-decide` | `submitAndDecideLoanApplication` | N/A | `200` |
| `Disburse Approved Loan Application` | `POST /loan-applications/{loanApplicationId}:disburse` | `disburseApprovedLoanApplication` | N/A | `200` |
| `Recommend Limit Increase` | `POST /customers/{customerId}:recommend-limit-increase` | `recommendLimitIncrease` | N/A | `200` |
| C-01 `Get Credit Score` | `POST /integration/credit-scoring:get-credit-score` | `getCreditScore` | `Credit Scoring Adapter` | `200` |
| C-02 `Disbursement and Accounting Request` | `POST /integration/disbursements:request` | `disbursementAndAccountingRequest` | `Disbursement Adapter` | `202` |
| C-03 `Post Disbursement and Accounting` | `POST /integration/disbursements:post` | `postDisbursementAndAccounting` | `ESB Integration Layer` | `202` |

Every call uses the string header `X-Simulated-Authorized`. Literal `true` permits the simulation; `false` or absence returns the stable `403 CON.5` envelope. This switch is not a credential. C-01 through C-03 additionally require the exact, case-sensitive modeled caller shown above. A missing or wrong `X-Caller` returns `403 CON.5`, records `access-denied`, and runs neither the adapter nor the I-3 fake. The three I-11 operations do not accept or require `X-Caller`.

The direct C-02/C-03 test envelopes cannot manufacture lifecycle authority. C-02 requires the actual `Loan Application Service`-owned state `AccountValidated` and its exact requested amount; C-03 additionally requires the accepted pending C-02 message. A failed precondition returns `502 CON.4` without an unauthorized enqueue or Core Banking call.

Agreement acceptance is a distinct internal `Mobile App -> Loan Application Service` step and is not a seventh public operation. The existing disbursement operation requires the application to be `Approved`; it cannot auto-accept an `OfferReady` application. `CAP-N02` executes that real skip attempt and proves that state, account validation, ESB, and Core Banking remain untouched.

## Stable error contract

```json
{
  "error": {
    "constraint": "CON.3",
    "reason": "Credit Scoring System timeout",
    "state": "Failed"
  }
}
```

`constraint` is one of `CON.1` through `CON.5`; `reason` is a controlled string; `state` is an exact I-6 state or `null`. Each named alternative also performs the G5 compensation in [`SPEC-TRACE.md`](SPEC-TRACE.md).

## Scope boundary

The runtime does not build secured/business/SME lending, branch onboarding, manual underwriting, a Loan Operations Specialist workflow, production infrastructure, a mobile binary, or any real I-3 connection. Customer decline is tested as the existing `OfferReady -> Rejected` transition, not exposed as a fourth use case. No route outside the six OpenAPI operations is callable.

## Acceptance

Lab 10 design approval allowed implementation to start. The remediated runtime requires a Dev R implementation commit followed by a distinct SA A signature-only commit; the current scorer-valid status is recorded in [`SA-ACCEPTANCE.md`](SA-ACCEPTANCE.md).
