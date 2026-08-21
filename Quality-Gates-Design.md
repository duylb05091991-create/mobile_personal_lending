# Quality gates — Design

Reviewer checklist for a logical / solution design pack for the mobile personal loan product.

**Source of truth.** [Domain.md](Domain.md), [Requirement_Document.md](Requirement_Document.md), [Analysis.md](Analysis.md).

**When applied.** Before accepting any UML, sequence, activity, or state design pack for this product.

**Pass rule.** The pack fails if any Must row is Fail, if any automatic-fail anti-pattern is present, or if an open assumption is treated as a decided product rule. Should rows do not block the pack, but they must still be marked Pass, Fail, or N/A with a comment.

Notation (PlantUML, Mermaid, or other) is free. Content is not.

---

## Sign-off

**Pack title:** ________________________________  
**Author:** ________________________________  
**Reviewer:** ________________________________  
**Date:** ________________________________

**Approval:** [ ] Approved  [ ] Changes requested

---

## Required contents

The design pack must contain all of the following. Missing a section is Fail for the matching Must row.

| # | Section / artifact | Must show |
|---|---|---|
| D1 | Scope | Pointers to Domain / Requirements / Analysis; in-scope FR-01…FR-11; out-of-scope reminder for non-salaried customers, branch-based onboarding, and manual underwriting in the standard path. |
| D2 | Domain / class design | `LoanApplication`, `CustomerProfile`, `CreditScore`, `PolicyConfiguration`, `LoanOffer`, `DecisionAudit`, and `DisbursementRecord` with identities such as `applicationId`, `customerId`, `score`, `eligibleAmount`, `interestRate`, `decision`, `businessDay`, and `idempotencyKey` where applicable. |
| D3 | Sequence — application and scoring | FR-01 to FR-03: Customer → Mobile App → Loan Application Service → Credit Scoring Adapter → Credit Scoring System → Decision Engine. |
| D4 | Sequence — approval and disbursement | FR-07 to FR-10: Decision Engine → Policy Engine → Account Validation → Disbursement Adapter → ESB → Core Banking. |
| D5 | Decision-rule fragment | Eligibility, credit score, affordability, maximum eligible amount, and interest-rate logic appear before offer generation and approval decision. |
| D6 | State machine | States such as `Submitted`, `Scoring`, `OfferReady`, `Approved`, `Rejected`, `Disbursed`, `Failed`, and `Reviewed` only if review is explicitly used. No implicit `PendingApproval` on the normal flow. |
| D7 | History / traceability | Decision record and audit log showing score, policy version, calculation output, and final decision. |
| D8 | Idempotency and retry | Same application or same request key returns the existing outcome; a new key is a new decision request. |
| D9 | Fail paths | Score unavailable / timeout; account validation failure; accounting post failure; amount above policy cap; rejected decision path. |
| D10 | BR evidence table | Every key product rule mapped to a named diagram fragment. Empty cell = Fail for that rule. |
| D11 | Open assumptions | Q1–Q5 listed as open or closed only by an explicit requirement change. |

---

## Automatic Fail (anti-patterns)

Any one of these is Fail for the whole pack, even if other rows pass.

- Approval or disbursement performed directly in the mobile app without a backend decision component
- Credit scoring or accounting logic hidden inside a single monolith without explicit adapters or interfaces
- Manual approval queue shown as the default path for eligible applicants
- Score threshold, max loan cap, or interest-rate formula treated as product fact without the requirement change
- Disbursement before approval or before account validation is complete
- History used as an operational ledger rather than as an auditable read model
- `PendingApproval` or branch-staff approval used as a normal accepted state in the loan flow
- UTC-midnight logic used instead of the product’s business clock for decisioning and audit windows
- Open questions Q1–Q5 silently closed as final product facts

---

## Review checklist

Mark Pass or Fail. Comment is required on Fail.

| ID | Check | Must / Should | Trace | Pass | Fail | Comment |
|---|---|---|---|---|---|---|
| DG-01 | Scope lists FR-01…FR-11 and the in-scope/out-of-scope boundary | Must | D1 | | | |
| DG-02 | Domain model includes `LoanApplication`, `CustomerProfile`, `CreditScore`, `PolicyConfiguration`, `LoanOffer`, `DecisionAudit`, `DisbursementRecord` | Must | D2 | | | |
| DG-03 | Sequence distinguishes request submission, score retrieval, eligibility evaluation, and final decision | Must | D3, D5 | | | |
| DG-04 | Credit scoring is external and uses a dedicated adapter; no direct credit-score logic in the app | Must | FR-03, D3 | | | |
| DG-05 | Eligibility check happens before offer generation and before auto-approval decision | Must | FR-02, FR-04, FR-06, FR-07 | | | |
| DG-06 | Maximum eligible amount and personalized rate are calculated from policy and score, not hard-coded on the UI | Must | FR-04, FR-05, FR-06 | | | |
| DG-07 | Sequence shows approval, reject, and offer-present flows as separate outcomes | Must | FR-06, FR-07 | | | |
| DG-08 | Approval triggers account validation, then disbursement, then accounting integration | Must | FR-07, FR-09, FR-10 | | | |
| DG-09 | Disbursement is not allowed without successful approval + account validation | Must | FR-09, D4 | | | |
| DG-10 | Core Banking posting happens through ESB; the ESB is a named integration boundary | Must | FR-10 | | | |
| DG-11 | Decision artifact records score, policy basis, computed amount, and final decision | Must | FR-11, D7 | | | |
| DG-12 | Audit log is traceable to the same application ID and decision event | Must | FR-11, D7 | | | |
| DG-13 | Scoring timeout or scoring outage is modeled as an exception path and not silently treated as success | Must | Analysis §8, FR-03 | | | |
| DG-14 | Account validation failure is modeled as a reject/no-disbursement path | Must | Analysis §8, FR-09 | | | |
| DG-15 | Accounting post failure includes compensating action, reconciliation, or explicit failed state handling | Must | Analysis §8, FR-10 | | | |
| DG-16 | Policy violation or loan amount above cap is represented as a reject/review result | Must | FR-04, FR-07, Analysis §8 | | | |
| DG-17 | State machine uses only the allowed product lifecycle and no unrelated staff or approval states in the default path | Must | D6 | | | |
| DG-18 | Retry / duplicate request logic prevents repeated disbursement or duplicate accounting post | Must | FR-11, D8 | | | |
| DG-19 | New application ID or new idempotency key is treated as a new loan request; same key is not a new loan | Must | D8 | | | |
| DG-20 | The design includes explicit fail states for score failure, account failure, and posting failure | Must | D9 | | | |
| DG-21 | Decision-making logic uses shared policy configuration rather than per-screen constants | Should | FR-04, FR-05, FR-07 | | | |
| DG-22 | History / audit records are clearly separated from the transaction posting flow | Should | NFR-05, NFR-06 | | | |
| DG-23 | Security and audit boundaries appear at app/service and external integration edges | Should | NFR-04, NFR-05 | | | |
| DG-24 | The design aligns the same names used in the architecture pack: Mobile App, Loan Application Service, Decision Engine, Credit Scoring Adapter, Policy Engine, ESB, Core Banking, Decision Store, Audit Log | Should | Architecture / naming consistency | | | |
| DG-25 | Open questions Q1–Q5 are listed as open, not treated as settled decisions | Must | D11 | | | |

---

## BR evidence table (required in the design pack)

Copy into the design pack. Reviewer fails DG-10 if any Evidence cell is empty.

| BR | Rule (short) | Evidence (diagram / section name) |
|---|---|---|
| BR-01 | Loan application is submitted through the mobile app | |
| BR-02 | Eligibility is validated before decisioning | |
| BR-03 | Credit score is retrieved from the external scoring system | |
| BR-04 | Maximum eligible amount is policy-based | |
| BR-05 | Interest rate is score-based | |
| BR-06 | Offer recommendation is generated before final approval | |
| BR-07 | Auto decisioning is based on policy thresholds | |
| BR-08 | Existing customers may be eligible for a limit increase recommendation | |
| BR-09 | Disbursement occurs only after approval | |
| BR-10 | Core Banking posting is routed through ESB | |
| BR-11 | Decision traceability stores score, policy basis, and calculated amount | |
| BR-12 | History and audit are readable without replaying all external calls | |
| BR-13 | The flow supports secure access and customer data protection | |
| BR-14 | Scoring outage / timeout has an explicit exception path | |
| BR-15 | Account failure blocks disbursement and accounting | |
| BR-16 | Policy breach or cap exceed leads to reject or review | |
| BR-17 | Same request key does not result in duplicate disbursement | |
| BR-18 | Decision and audit use a common business context for traceability | |

---

## Design guidance for this product

The design pack should describe the loan lifecycle clearly and consistently:

1. Customer submits a loan application from the mobile app.
2. The loan application service validates the request, reads customer data, and checks eligibility.
3. The credit scoring adapter calls the external scoring system for a near-real-time result.
4. The policy engine applies the product rules for eligible amount and interest rate.
5. The decision engine determines the final decision and creates an offer or rejection.
6. If approved, the system validates the payment account and calls the disbursement adapter.
7. The accounting adapter sends the transaction data to Core Banking via ESB.
8. A decision record and audit log capture the score, policy basis, and final outcome.

This is the core thread the design evidence should model and prove.

---

## Minimal design shape

A compliant design pack should be able to show the following:

- A customer-facing mobile application as the initiation front end.
- A service layer for application intake and validation.
- A decision engine that consumes customer profile, score, and policy configuration.
- A dedicated scoring adapter for the external scoring system.
- A policy engine that calculates eligible amount, pricing, and recommendation.
- A disbursement path that validates account and posts to Core Banking over ESB.
- Audit and traceability records that support explanation and compliance review.

This is the minimum evidence needed to pass the design gate for this project.
