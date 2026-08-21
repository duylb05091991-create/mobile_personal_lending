# Lab 5 — UML Before Pack

**Status:** Draft, current-style before pack. No Guide header or RACI.

## Named use cases

- Submit and Decide Loan Application
- Disburse Approved Loan Application
- Recommend Limit Increase

## Activity flow

Customer submits through Mobile App -> Loan Application Service validates -> Decision Engine requests Credit Score through Credit Scoring Adapter -> Policy Engine calculates amount and rate -> Decision Engine creates Loan Offer -> Customer accepts Nopbai Personal Loan Agreement -> Account Validation Service validates account -> Disbursement Adapter sends through ESB Integration Layer -> Core Banking confirms -> Decision Store and Audit Log record evidence.

Decision branches: `CON.1` rejects over-cap amount; `CON.2` rejects out-of-segment request; `CON.3` records Failed on scoring timeout; `CON.4` records Failed on account or posting failure.

## State machine

Object: **Loan Application**. States: Draft, Submitted, Scoring, OfferReady, Approved, AccountValidated, Rejected, Disbursed, Failed. Terminal states: Rejected, Disbursed, Failed.

## Planned G6 checklist

| Transition / alt | Planned test |
| --- | --- |
| Draft -> Submitted | T-01 |
| Submitted -> Scoring | T-02 |
| Submitted -> Rejected, CON.2 | T-02A |
| Scoring -> OfferReady | T-03 |
| Scoring -> Failed, CON.3 | T-04 |
| OfferReady -> Approved | T-05 |
| OfferReady -> Rejected, CON.1 | T-06 |
| OfferReady -> Rejected, customer declines | T-06A |
| Approved -> AccountValidated | T-07 |
| Approved -> Failed, CON.4 | T-08 |
| AccountValidated -> Disbursed | T-09 |
| AccountValidated -> Failed, CON.4 | T-10 |
| Limit Increase alt, CON.2 | T-11 |

See [../puml/labs/lab-5-submit-decide.puml](../puml/labs/lab-5-submit-decide.puml), [../puml/labs/lab-5-disburse.puml](../puml/labs/lab-5-disburse.puml), [../puml/labs/lab-5-limit-increase.puml](../puml/labs/lab-5-limit-increase.puml), and [../puml/labs/lab-5-activity.puml](../puml/labs/lab-5-activity.puml).
