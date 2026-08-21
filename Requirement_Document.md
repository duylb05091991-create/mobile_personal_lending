# Requirement Document

## 1. Project Overview

This project is for a mobile-first personal loan product targeted at salaried customers. The objective is to enable customers to apply for a loan through a mobile app, receive an automated decision in near real time, and receive disbursement immediately to their payment account when approved.

The product is designed for existing customers in the age group of 22 to 35, with salaried income profiles.

## 2. Business Objective

The business aims to provide a fast, digital, and automated lending experience that:

- reduces manual underwriting effort,
- accelerates approval decisions,
- personalizes lending offers based on credit risk,
- improves customer experience through mobile self-service,
- supports immediate disbursement to customer accounts,
- integrates lending accounting with the core banking system.

## 3. Business Scope

### In Scope
- Unsecured loan product with a maximum limit of 100 million VND
- Loan application via mobile app
- Automated credit scoring in near real time
- Customized interest rate based on credit score
- Recommend and calculate the maximum eligible amount a customer can borrow
- Auto approval or auto rejection decisioning
- Limit increase recommendations
- Immediate disbursement to customer payment account
- Integration of accounting entries into Core Banking through ESB
- Credit scoring performed by a separate risk analysis system

### Out of Scope
- Secured lending products
- Business loans or SME lending
- Manual review workflows for standard automated decisions
- Physical branch-based onboarding
- Non-salaried or self-employed customer segments in the initial scope
- Production-grade system implementation details beyond the requirement definition

## 4. Target Customers

- Existing customers
- Salaried employees
- Age range: 22–35
- Customers who meet the bank’s credit and affordability standards for digital lending

## 5. User Roles

### Customer
- Submits a loan application through the mobile app
- Reviews loan offer details
- Accepts the final loan terms when applicable

### Internal Operations / Risk Team
- Monitors policy thresholds and decision outcomes
- Reviews exceptions or policy breaches outside the automated flow

### Core Banking and Integration Layer
- Receives accounting and transaction updates
- Confirms disbursement and ledger postings

## 6. Functional Requirements

### FR-01: Loan application submission
The system shall allow a customer to submit a loan application via the mobile app.

### FR-02: Customer eligibility assessment
The system shall evaluate customer eligibility based on available customer and credit data.

### FR-03: Credit scoring integration
The system shall integrate with a credit scoring system to obtain a near real-time credit score for the customer.

### FR-04: Maximum eligible amount calculation
The system shall calculate the maximum borrowable amount based on the customer’s credit profile and policy rules.

### FR-05: Personalized interest rate
The system shall determine a customized interest rate for each customer based on the credit score and the product policy.

### FR-06: Offer recommendation
The system shall recommend or present a loan offer with a proposed limit and rate.

### FR-07: Auto decisioning
The system shall automatically approve or reject the loan application without human intervention when the decision falls within policy thresholds.

### FR-08: Limit increase recommendation
The system shall provide recommendations for limit increase opportunities to eligible existing customers.

### FR-09: Immediate disbursement
When approved, the system shall disburse the approved amount immediately to the customer’s payment account.

### FR-10: Accounting integration
The system shall send accounting entries to Core Banking through the ESB integration layer.

### FR-11: Decision traceability
The system shall retain sufficient data to explain the automated decision, including the associated score, policy basis, and calculated amount.

## 7. Business Rules

- Maximum unsecured loan amount is capped at 100 million VND.
- Auto approval or rejection is allowed based on predefined policy rules.
- Credit score is a key determinant of eligibility, borrowing limit, and offered interest rate.
- The maximum amount suggested must be compatible with credit score and policy approval rules.
- Immediate disbursement is allowed only after successful approval and account validation.
- Accounting entries must be posted to Core Banking as part of the transaction lifecycle.

## 8. Non-Functional Requirements

### NFR-01: Performance
The system shall process loan application decisions in near real time to support a smooth mobile experience.

### NFR-02: Availability
The lending service shall be available to support customer transactions during normal banking operating hours and business-critical scenarios.

### NFR-03: Reliability
The system shall minimize failed or incorrect decisioning and ensure the correct accounting flow for approved transactions.

### NFR-04: Security
The system shall protect customer data, enforce secure authentication and authorization, and maintain compliance with banking security standards.

### NFR-05: Auditability
The system shall log decision-making details, integration events, and transaction outcomes for audit, compliance, and dispute handling.

### NFR-06: Data integrity
The system shall ensure data consistency across customer records, scoring inputs, loan decisions, and Core Banking accounting records.

### NFR-07: Scalability
The system shall support increasing numbers of mobile loan requests without degrading response time or service quality.

### NFR-08: Compliance
The system shall comply with internal risk policies, data privacy rules, and financial regulatory requirements applicable to lending operations.

## 9. External Systems and Dependencies

### Credit Scoring System
- Provides customer risk score
- Determines eligibility and scoring-based evaluation

### Core Banking System
- Receives accounting entries and transaction postings
- Supports payment disbursement and ledger updates

### ESB Integration Layer
- Ensures integration and message routing between the lending application and banking systems

### Mobile App
- Front-end channel for application submission and offer acceptance

## 10. Key Assumptions

- Customers are existing bank customers with available account data.
- Credit scoring data is available in near real time.
- Product policy rules and approval thresholds are defined and configurable.
- Core Banking and ESB interfaces are available for integration.
- The mobile app can display approved offers and trigger disbursement actions.

## 11. Success Criteria

The initiative is successful when:

- customers can complete a mobile loan application with little or no manual intervention,
- decisions are generated automatically in near real time,
- approved amounts align with risk and policy thresholds,
- disbursement is completed immediately after approval,
- accounting entries are correctly posted to Core Banking,
- all decision flows are auditable and secure.

## 12. Open Questions

- What specific eligibility and affordability rules will be used for the 22–35 salaried customer segment?
- What are the exact scoring thresholds for approval, rejection, and limit increase?
- What data fields are required from the credit scoring system?
- Which payment account is used for disbursement in the initial rollout?
- What are the exact non-functional SLA targets for response time and availability?

## 13. Summary

This requirement defines a digital personal lending product focused on automated credit decisions, personalized loan offers, and immediate disbursement. The design objective is to support a fast, low-friction borrowing journey while maintaining control through policy-based automation, secure integrations, and reliable banking system connectivity.
