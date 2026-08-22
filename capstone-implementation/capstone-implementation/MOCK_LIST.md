# I-3 mock list

`capstone.md`: "I-3 is mocked (stub or in-process fake). Fail if the runtime
calls a real host or embeds a live secret." All three I-3 externals are
**in-process fakes**. No network host is contacted; no secret or credential is
embedded anywhere in source or config.

| I-3 external (Lab 1) | Mock type | Code | Simulates | Contract |
|----------------------|-----------|------|-----------|----------|
| `Credit Scoring System` | in-process fake | `external/credit_scoring_system.py → CreditScoringSystemFake` | near-real-time score; CON.3 timeout via `timeout=True`; I-9 caller guard | C-01 |
| `ESB Integration Layer` | in-process fake | `external/esb_integration_layer.py → EsbIntegrationLayerFake` | async message + confirmation; routes to Core Banking; caller guard | C-02 |
| `Core Banking` | in-process fake | `external/core_banking.py → CoreBankingFake` | posting/confirmation; CON.4 failure via `posting_fails=True`; masters `Disbursement Record`; I-9 caller guard | C-03 |

Notes:

- The mocks are also exposed as **served contract routes** under `/backing/…`
  (loopback only) so the three Lab 3 contract rows appear as OpenAPI operations
  with the same behavior the adapters invoke in-process — no drift.
- The mocks are deterministic (no randomness that would flake tests): the
  simulated score is stable per `customer_id`; failures are driven only by
  explicit simulation switches in the request body.
- No production system name, vendor id, host, or credential appears. Product
  labels (Kong / Kafka / Keycloak) are **not** used and nothing is stood up.
