# Lab 6 — Integration Ecosystem

**Status:** Draft, before pack. Model only; no products installed.

## Ecosystem sketch

Internal containers: Mobile App, Loan Application Service, Credit Scoring Adapter, Decision Engine, Policy Engine, Account Validation Service, Disbursement Adapter, Decision Store, Audit Log. External systems: Credit Scoring System, ESB Integration Layer, Core Banking.

## Integration edges

| Edge | Label |
| --- | --- |
| Credit Scoring Adapter -> Credit Scoring System | HTTPS; sync; Get Credit Score |
| Disbursement Adapter -> ESB Integration Layer | Message; async; Submit Disbursement and Accounting Request |
| ESB Integration Layer -> Core Banking | Message; async; Validate Account, Post Accounting, Confirm Outcome |

Adapters are containers because the team builds them. Credit Scoring System, ESB Integration Layer, and Core Banking remain external systems. No separate IAM product is added.

## Negative evidence

No Docker, cluster, broker administration, IAM realm, production credentials, or running integration product is included. Product names may only be labels later.

## Archive gate

Labs 1-6 must be copied to `before-pack/` unchanged before Lab 7 begins. This file does not claim that archive has been completed.
