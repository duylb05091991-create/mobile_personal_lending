# Analysis — Nopbai Mobile Personal Loan

**Status:** Lab 1 identity-aligned draft; no quality-gate register is applied here.

## Problem and target state

The baseline is manual or fragmented assessment. The target is a mobile flow in which Loan Application Service validates the request, Decision Engine coordinates scoring and policy, Mobile App presents the offer, and approved applications move through Account Validation Service, Disbursement Adapter, ESB Integration Layer, and Core Banking.

## Requirements mapping

FR-01 and FR-02 map to Mobile App and Loan Application Service. FR-03 maps to Credit Scoring Adapter and Credit Scoring System. FR-04 through FR-08 map to Decision Engine and Policy Engine. FR-09 and FR-10 map to Account Validation Service, Disbursement Adapter, ESB Integration Layer, and Core Banking. FR-11 maps to Decision Store and Audit Log.

## Exception paths

- Scoring timeout: Credit Scoring Adapter returns a controlled failure; Decision Engine rejects or routes to Loan Operations Specialist according to policy, with no approval.
- Account validation failure: Account Validation Service rejects the flow; Disbursement Adapter is not called.
- Policy cap breach: Decision Engine rejects or routes an exception; amount never exceeds 100,000,000 VND.
- Accounting confirmation failure: Disbursement Adapter records `Failed`, prevents duplicate posting with an idempotency key, and supports reconciliation.

## Modeling boundary

ArchiMate describes motivation, business, application cooperation, and technology. C4 describes the system context and internal containers. UML will describe the Loan Application lifecycle and named use cases after the before pack is completed. The internal containers are exactly those listed in I-4 of [list.md](list.md).

## Open assumptions

Q1-Q5 remain open: eligibility rules, score thresholds, scoring fields, payment account choice, and numeric SLA targets.
