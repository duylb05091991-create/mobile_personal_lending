# I-3 mock list

All and only the three Lab 1 I-3 systems are simulated. They are deterministic in-process fakes in `nopbai.fakes`; they open no socket, resolve no host, and require no secret or production credential.

| Exact I-3 system | Fake behavior | Allowed caller/path | Failure mode | Evidence |
|---|---|---|---|---|
| `Credit Scoring System` | Returns a deterministic near-real-time `Credit Score` for `scoring_mode=success`; records a call count | `Credit Scoring Adapter` through C-01 `Get Credit Score` only | `scoring_mode=timeout` or `unavailable` becomes `503 CON.3`; decisioning stops and no approval is produced | `CAP-C01`, `CAP-A02`, `CAP-I3-01`, `CAP-N01`, `CAP-N05` |
| `ESB Integration Layer` | Accepts the C-02 message, records it in an in-process FIFO queue, routes C-03, and retains confirmation/reconciliation evidence | `Disbursement Adapter` through C-02 `Disbursement and Accounting Request` only | A failed posting outcome is returned on the same asynchronous contract and becomes `502 CON.4`; reconciliation evidence remains | `CAP-C02`, `CAP-A05`, `CAP-I3-01`, `CAP-N02`, `CAP-N03`, `CAP-N06`, `CAP-N07`, `CAP-N09`, `CAP-N10` |
| `Core Banking` | Produces a deterministic posting confirmation and the master `Disbursement Record` reference | `ESB Integration Layer` through C-03 `Post Disbursement and Accounting` only | `posting_mode=failure` produces the controlled C-03 failure; no successful record is claimed | `CAP-C03`, `CAP-A05`, `CAP-I3-01`, `CAP-N02`, `CAP-N03`, `CAP-N06`, `CAP-N07`, `CAP-N10` |

## Boundary rules

- C-01 remains HTTPS request/response / Sync at the architectural boundary even though the fake is an in-process function.
- C-02 and C-03 remain Message with confirmation and reconciliation / Async. Their committed OpenAPI operations are simulation envelopes: `202` means that an in-process message was accepted, not that the architectural contract became synchronous.
- The real C-01, C-02, and C-03 simulation operations require exact `X-Caller` values `Credit Scoring Adapter`, `Disbursement Adapter`, and `ESB Integration Layer`, respectively. Wrong or missing callers receive audited `403 CON.5` before request validation or fake dispatch.
- `Account Validation Service` evaluates the SA-approved simulated, read-only `account_eligible` input received through `Mobile App`. It does not call the `Core Banking` fake and does not become source of truth for `Customer Profile`.
- `Core Banking` remains the sole I-7 source of truth for `Customer Profile` and `Disbursement Record`. The runtime stores only its simulated record reference in `Audit Log`.
- The runtime has no configuration field for an external URL and contains no API key, password, token, certificate, vendor identifier, or customer record.
- A fake call counter and queue/evidence snapshots make forbidden-call and compensation assertions executable rather than documentary.

## Simulation inputs

| Input | Values | Meaning |
|---|---|---|
| `scoring_mode` | `success`, `timeout`, `unavailable` | Deterministically selects the C-01 result |
| `posting_mode` | `success`, `failure` | Deterministically selects the C-02/C-03 confirmation/reconciliation result |
| `account_eligible` | `true`, `false` | Local read-only validation input; not a Core Banking response or copied `Customer Profile` |
| `X-Simulated-Authorized` | string `true`, string `false` | Test-only `CON.5` switch; explicitly not a credential |
| `X-Caller` | exact modeled source per C-01/C-02/C-03 | Test-harness enforcement of the frozen I-9 boundary; omitted from I-11 operations and explicitly not a credential |
