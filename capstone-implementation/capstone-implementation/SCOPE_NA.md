# Scope — N/A rows (listed, not built)

`capstone.md`: "I-1 'in scope' items that are not I-11 use cases are out — list
them N/A, do not build them." And: other Lab 3 / G6 rows the I-11 use cases do
not need are N/A on the spec-trace — **not extra code, and not silently omitted
from an I-11 path**.

## I-1 "In scope" that is NOT one of the three I-11 use cases → N/A

The three I-11 use cases are: *Submit and Decide Loan Application*, *Disburse
Approved Loan Application*, *Recommend Limit Increase*. The following I-1 in-scope
items are realized only insofar as an I-11 use case needs them; they are **not**
built as independent use cases:

| I-1 in-scope item | Status | Reason |
|-------------------|--------|--------|
| Auto approval or rejection | Covered inside UC1/UC3 decisioning | not a separate I-11 use case |
| Loan Offer creation | Covered inside UC1/UC3 | output of the decision, not a standalone use case |
| Account validation | Covered inside UC2 | a step of Disburse, not a standalone use case |
| Accounting through ESB → Core Banking | Covered inside UC2 (C-02/C-03) | a step of Disburse |
| Decision Store / Audit Log traceability | Covered across UC1–UC3 | evidence, not a use case |
| Customer segment onboarding (age/salaried gate) | Enforced as CON.2 in UC1/UC3 | a constraint, not a use case |

## Lab 3 contract / exception / G6 rows → N/A

| Row | Status | Reason |
|-----|--------|--------|
| EX-05 (CON.5) as a standalone integration | Enforced cross-cutting (auth guard + audit); tested in `test_con5_auth` | no dedicated I-11 use case; still not dropped from any I-11 path |
| Any Lab 3 contract beyond C-01/C-02/C-03 | none exist | contract register has exactly three rows |

## Explicitly OUT (Lab 1 I-1 Out of scope) — not built, not mocked as features

Secured loans; business/SME loans; branch onboarding; non-salaried customers;
manual underwriting on the standard path; production implementation details; real
customer data; production credentials. None appears in the runtime.
