# Spec-trace — in-scope path → OpenAPI operation → test id

Every in-scope path traces to an OpenAPI `operationId` and at least one executed
test. No code sits off this trace; no OpenAPI operation is without a test. Test
ids reference the pytest node names (which carry the Lab 3 `T-xx` / Lab 10
`G6-Sxx` / `G6-Axx` markers).

## I-11 use cases (happy path + drawn alts)

| In-scope path (use case / branch) | I-6 / CON | OpenAPI operationId | Test id |
|-----------------------------------|-----------|---------------------|---------|
| UC1 Submit and Decide — happy | Draft→Submitted→Scoring→OfferReady (T-01,02,04) | `submitAndDecideLoanApplication` | `test_uc1…::test_T04_happy_path_offer_ready` |
| UC1 alt **CON.3** scoring timeout *(named in I-11)* | Scoring→Failed (T-05) | `submitAndDecideLoanApplication` (503) | `test_uc1…::test_T14_G6A02_con3_scoring_timeout_named_alt` |
| UC1 alt CON.2 out-of-segment | Submitted→Rejected (T-03) | `submitAndDecideLoanApplication` (422) | `test_uc1…::test_T13_G6A01_con2_out_of_segment` |
| UC1 alt CON.1 amount cap | OfferReady→Rejected (T-07) | `submitAndDecideLoanApplication` (422) | `test_uc1…::test_T15_G6A03_con1_amount_cap` |
| UC1 customer declines | OfferReady→Rejected (T-08) | `declineLoanOffer` | `test_uc1…::test_T08_customer_declines_offer` |
| UC2 accept agreement | OfferReady→Approved (T-06) | `acceptLoanAgreement` | `test_uc2…::_to_approved` (used by all UC2 tests) |
| UC2 Disburse — happy | Approved→AccountValidated→Disbursed (T-09,11) | `disburseApprovedLoanApplication` | `test_uc2…::test_T11_happy_disbursement` |
| UC2 alt **CON.4** validation fail *(named in I-11)* | Approved→Failed (T-10) | `disburseApprovedLoanApplication` (422) | `test_uc2…::test_T10_G6A04_con4_validation_failure_named_alt` |
| UC2 alt **CON.4** posting fail *(named in I-11)* | AccountValidated→Failed (T-12) | `disburseApprovedLoanApplication` (502) | `test_uc2…::test_T12_G6A05_con4_posting_failure_named_alt` |
| UC3 Recommend Limit Increase — happy | (no I-6 transition; Loan Offer) | `recommendLimitIncrease` | `test_uc3…::test_happy_recommendation` |
| UC3 alt **CON.2** out-of-segment *(named in I-11)* | — | `recommendLimitIncrease` (422) | `test_uc3…::test_T18_G6A06_con2_out_of_segment_named_alt` |
| UC3 alt CON.1 amount cap | — | `recommendLimitIncrease` (422) | `test_uc3…::test_T19_G6A07_con1_amount_cap` |

## In-scope Lab 3 contract rows (I-8 edges) → OpenAPI + test

| Contract | Producer → Consumer | Mode | OpenAPI operationId | Test id |
|----------|---------------------|------|---------------------|---------|
| C-01 Get Credit Score | Credit Scoring Adapter → Credit Scoring System | Sync | `getCreditScore` | `test_hard_rules::test_I9_mobile_app_cannot_perform_credit_evaluation` + `test_contract_openapi::test_backing_contracts_document_forbidden_path` |
| C-02 Disbursement and Accounting Request | Disbursement Adapter → ESB Integration Layer | Async | `sendDisbursementAndAccounting` | `test_uc2…::test_T11_happy_disbursement` (runtime path) + `test_contract_openapi` |
| C-03 Post Disbursement and Accounting | ESB Integration Layer → Core Banking | Async | `postDisbursementAndAccounting` | `test_hard_rules::test_I9_direct_mobile_app_to_core_banking_is_rejected` + `test_contract_openapi` |

## Hard rules / cross-cutting (proved by negative tests on this slice)

| Rule | OpenAPI surface | Test id |
|------|-----------------|---------|
| I-5: no approval before scoring/policy | (domain guard) | `test_hard_rules::test_I5_cannot_approve_before_scoring` |
| I-5 / CON.4: no disbursement before approval + validation | `disburseApprovedLoanApplication` | `test_hard_rules::test_I5_cannot_disburse_before_approval` |
| I-9 forbidden: Mobile App → Core Banking | `postDisbursementAndAccounting` (403) | `test_hard_rules::test_I9_direct_mobile_app_to_core_banking_is_rejected` |
| I-9 forbidden: Mobile App performs credit evaluation | `getCreditScore` (403) | `test_hard_rules::test_I9_mobile_app_cannot_perform_credit_evaluation` |
| CON.5 (EX-05): unauthenticated access denied | all public ops (401) | `test_con5_auth::*` |
| All 12 I-6 transitions (G6-S01…S12) | (domain type) | `test_state_machine::test_G6_S01…S12` |

## N/A rows

Other Lab 3 / G6 rows that the three I-11 use cases do not need are listed in
`SCOPE_NA.md` — not extra code, and not silently dropped from an I-11 path.
