# Lab 3 — Implementation, Design, and Test Specification

**Status:** Draft, current-language before pack. No C4 diagram and no Guide header/RACI.

## Build list

| Order | Container | Owner | Environment |
| --- | --- | --- | --- |
| 1 | Mobile App | Dev | Customer mobile device |
| 2 | Loan Application Service | Dev | Lending application runtime |
| 3 | Credit Scoring Adapter | Dev | Lending application runtime |
| 4 | Decision Engine | Dev | Lending application runtime |
| 5 | Policy Engine | Dev | Lending application runtime |
| 6 | Account Validation Service | Dev | Lending application runtime |
| 7 | Disbursement Adapter | Dev | Lending application runtime |
| 8 | Decision Store | Dev | Evidence data store |
| 9 | Audit Log | Dev | Evidence data store |

## Selected-container component specification

Selected container: **Decision Engine**. Modules: Eligibility Coordinator, Scoring Result Handler, Offer Calculator, Decision Evaluator, Limit Increase Recommender, Decision Evidence Writer. Neighbours remain black boxes: Loan Application Service, Credit Scoring Adapter, Policy Engine, Account Validation Service, Mobile App, Decision Store, Audit Log.

## To-be sequence: Submit and Decide Loan Application

Customer -> Mobile App: submit Loan Application
Mobile App -> Loan Application Service: validate and create
Loan Application Service -> Decision Engine: start decision
Decision Engine -> Credit Scoring Adapter: request Credit Score
Credit Scoring Adapter -> Decision Engine: return Credit Score
Decision Engine -> Policy Engine: calculate amount and rate
Policy Engine -> Decision Engine: return Policy Configuration result
Decision Engine -> Decision Store: persist Decision Record
Decision Engine -> Audit Log: record evidence
Decision Engine -> Mobile App: present Loan Offer

`alt CON.3`: scoring timeout -> Decision Engine records Failed and does not approve.
`alt CON.1`: amount exceeds cap -> Decision Engine rejects.

## Contract register

| Producer | Consumer | Mode | Operation / event |
| --- | --- | --- | --- |
| Credit Scoring Adapter | Credit Scoring System | Sync | Get Credit Score |
| Disbursement Adapter | ESB Integration Layer | Async | Submit Disbursement and Accounting Request |
| ESB Integration Layer | Core Banking | Async + confirmation | Validate Account, Post Accounting, Confirm Outcome |

## Exception specification

| Trigger | Constraint | Compensating action | Owner |
| --- | --- | --- | --- |
| Scoring timeout | CON.3 | Record Failed, notify Customer, retain evidence | Decision Engine |
| Amount over cap | CON.1 | Reject Loan Offer and retain policy result | Decision Engine |
| Account validation failure | CON.4 | Do not call disbursement; record Failed | Account Validation Service |
| Accounting confirmation failure | CON.4 | Prevent duplicate retry with idempotency key; reconcile | Disbursement Adapter |

## Test specification

| ID | Source | SUT | Expected result |
| --- | --- | --- | --- |
| T-01 | Draft -> Submitted | Mobile App | Loan Application is created |
| T-02 | Submitted -> Scoring | Loan Application Service | Eligible request enters scoring |
| T-02A | Submitted -> Rejected | Loan Application Service | Out-of-segment request is rejected under CON.2 |
| T-03 | Scoring -> OfferReady | Credit Scoring Adapter | Credit Score is accepted |
| T-04 | Scoring -> Failed | Credit Scoring Adapter | Timeout is controlled and no approval occurs |
| T-05 | OfferReady -> Approved | Decision Engine | Accepted agreement produces Approved |
| T-06 | OfferReady -> Rejected | Decision Engine | Policy breach rejects |
| T-06A | OfferReady -> Rejected | Mobile App / Decision Engine | Customer declines the Loan Offer |
| T-07 | Approved -> AccountValidated | Account Validation Service | Valid account permits disbursement |
| T-08 | Approved -> Failed | Account Validation Service | Invalid account blocks disbursement |
| T-09 | AccountValidated -> Disbursed | Disbursement Adapter | Core Banking confirmation completes flow |
| T-10 | AccountValidated -> Failed | Disbursement Adapter | Posting failure is reconciled |
| T-11 | sequence alt CON.3 | Decision Engine | Failed recorded |
| T-12 | sequence alt CON.1 | Decision Engine | Rejected recorded |

All SUT values are I-4 container names.
