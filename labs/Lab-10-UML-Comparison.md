# Lab 10 — UML After Pack and Comparison

**Status:** Draft after-pack; requires Lab 9 review.
**RACI:** Dev R; SA A; Test and BA C.

## Audited participants

Every lifeline is an I-4 container or I-2 actor: Customer, Mobile App, Loan Application Service, Credit Scoring Adapter, Decision Engine, Policy Engine, Account Validation Service, Disbursement Adapter, Decision Store, Audit Log, ESB Integration Layer, and Core Banking. Decision Engine modules appear only inside its optional component view.

## Audited use cases

- Submit and Decide Loan Application: includes `alt CON.3` scoring timeout and `alt CON.1` over-cap rejection.
- Disburse Approved Loan Application: includes `alt CON.4` account validation or posting failure.
- Recommend Limit Increase: includes `alt CON.2` out-of-segment rejection.

Audited sequence sources: [submit and decide](../puml/labs/lab-10-submit-decide-after.puml), [disburse](../puml/labs/lab-10-disburse-after.puml), and [recommend limit increase](../puml/labs/lab-10-limit-increase-after.puml).

## State coverage

Loan Application transitions covered: Draft -> Submitted; Submitted -> Scoring; Scoring -> OfferReady; Scoring -> Failed; OfferReady -> Approved; OfferReady -> Rejected; Approved -> AccountValidated; Approved -> Failed; AccountValidated -> Disbursed; AccountValidated -> Failed.

## Participant-to-SUT map

| Participant | SUT / identity source |
| --- | --- |
| Mobile App | Mobile App / I-4 |
| Loan Application Service | Loan Application Service / I-4 |
| Decision Engine | Decision Engine / I-4 |
| Credit Scoring Adapter | Credit Scoring Adapter / I-4 |
| Policy Engine | Policy Engine / I-4 |
| Account Validation Service | Account Validation Service / I-4 |
| Disbursement Adapter | Disbursement Adapter / I-4 |
| Decision Store | Decision Store / I-4 |
| Audit Log | Audit Log / I-4 |
| ESB Integration Layer | ESB Integration Layer / I-3 external |
| Core Banking | Core Banking / I-3 external |

## Coverage note

All state transitions and named sequence alternatives map to planned tests T-01 through T-12 in Lab 3. No new use cases or participants are introduced.

## Comparison: Lab 5 vs Lab 10

| Concern | Lab 5 before | Lab 10 after |
| --- | --- | --- |
| Language | Current-style UML | UML aligned to C4 names |
| Participants | May be informal | Every lifeline resolves to I-2/I-4 |
| Exceptions | Named CON.* branches | Audited CON.* branches and coverage |
| State | One Loan Application object | Same one object and exact transitions |
| Governance | No header/RACI | Guide header/RACI and G6 evidence |
