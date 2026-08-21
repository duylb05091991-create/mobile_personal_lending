# Organization / Product — Nopbai Mobile Personal Loan

**Status:** Corrected architecture draft; Lab 8 evidence is not accepted until the prescribed lab sequence is complete.
**RACI:** BA/PO R; Business Owner A; EA C.
**Language:** ArchiMate Business only.

## Header

| Field | Value |
| --- | --- |
| Viewpoint | ArchiMate Business Organization / Product |
| Transition | To-Be |
| Owner | Business Analyst / Product Owner |
| Date | 2026-08-21 |

## Actors and roles

| Actor | Role | Responsibility |
| --- | --- | --- |
| Customer | Loan Applicant | Submits the application, reviews the offer, and accepts the Nopbai Personal Loan Agreement. |
| Loan Operations Specialist | Exception Reviewer | Reviews policy exceptions and reconciliation cases only. |

## Product structure

| Element | Name | Description |
| --- | --- | --- |
| Product | Nopbai Mobile Personal Loan | Unsecured personal loan for existing salaried customers aged 22-35. |
| Channel | Mobile App | Customer application and offer channel. |
| Contract | Nopbai Personal Loan Agreement | Terms accepted by Customer after an approved offer. |

## Business objects

| Object | Meaning |
| --- | --- |
| Loan Application | Customer request and lifecycle state. |
| Customer Profile | Existing customer, income, and account information. |
| Credit Score | Risk score returned by Credit Scoring System. |
| Policy Configuration | Eligibility, amount, rate, and decision rules. |
| Loan Offer | Proposed amount and personalized rate. |
| Decision Record | Final decision with score and policy evidence. |
| Disbursement Record | Account validation and posting outcome. |

## Business services

| Service | Served role | Realization boundary |
| --- | --- | --- |
| Loan application intake | Loan Applicant | Mobile App and Loan Application Service |
| Eligibility and scoring | Loan Applicant | Decision Engine and Credit Scoring Adapter |
| Offer calculation and decisioning | Loan Applicant | Policy Engine and Decision Engine |
| Account validation and disbursement | Loan Applicant | Account Validation Service and Disbursement Adapter |
| Decision traceability | Loan Operations Specialist | Decision Store and Audit Log |
