# Lab 4 — Before-Pack Cleanup

**Status:** Draft, current-style cleanup. The original Lab 1–3 drafts must be archived unchanged before this cleaned copy is accepted.

## Cleaned pack

The cleaned requirements, analysis, and implementation specification use the I-1–I-11 names from [../list.md](../list.md). The canonical identity is: Customer; Loan Operations Specialist; Credit Scoring System; ESB Integration Layer; Core Banking; Mobile App; Loan Application Service; Credit Scoring Adapter; Decision Engine; Policy Engine; Account Validation Service; Disbursement Adapter; Decision Store; Audit Log; Loan Application; Loan Offer; Decision Record; Disbursement Record.

## Name-identity check

| Check | Result |
| --- | --- |
| Actors are people | Pass |
| I-3 externals are not I-4 containers | Pass |
| Every process participant is I-2, I-3, or I-4 | Pass |
| Loan Offer has one source of truth | Pass: Decision Store |
| Failed state is reachable | Pass |
| CON.1-CON.5 have process effects | Pass |

## Defects found in first drafts

| Defect | Owner |
| --- | --- |
| Blank name-identity index | BA / SA |
| Forked system and container names | SA |
| External systems duplicated as internal components | SA |
| Loan Offer missing from source-of-truth table | DA |
| Failed state unreachable | Test |
| Limit-increase recommendation not represented in Lab 1 | BA |
| Premature Guide headers and custom gates | EA |

## Comparison note

Cleaned items are spelling, external boundary, source-of-truth, state reachability, and requirement coverage. Standardization is intentionally limited to the current-language pack; ArchiMate, C4, UML, headers, RACI, and G1-G6 remain deferred to Labs 7-10.

## Archive requirement

Create an unchanged `before-pack/` copy of Lab 1, Lab 2, and Lab 3 before accepting this sitting as Done.
