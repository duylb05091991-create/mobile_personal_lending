"""The exact six-operation SA-approved route registry."""

from .identities import (
    CREDIT_SCORING_ADAPTER,
    DISBURSEMENT_ADAPTER,
    ESB_INTEGRATION_LAYER,
)

ROUTE_REGISTRY = {
    "/loan-applications:submit-and-decide": {
        "method": "POST",
        "path": "/loan-applications:submit-and-decide",
        "operationId": "submitAndDecideLoanApplication",
        "source": "Submit and Decide Loan Application",
        "summary": "Submit and Decide Loan Application",
        "x-model-operation": "Submit and Decide Loan Application",
        "successStatuses": (200,),
        "errorStatuses": (422, 503, 403),
    },
    "/loan-applications/{loanApplicationId}:disburse": {
        "method": "POST",
        "path": "/loan-applications/{loanApplicationId}:disburse",
        "operationId": "disburseApprovedLoanApplication",
        "source": "Disburse Approved Loan Application",
        "summary": "Disburse Approved Loan Application",
        "x-model-operation": "Disburse Approved Loan Application",
        "successStatuses": (200,),
        "errorStatuses": (422, 502, 403),
    },
    "/customers/{customerId}:recommend-limit-increase": {
        "method": "POST",
        "path": "/customers/{customerId}:recommend-limit-increase",
        "operationId": "recommendLimitIncrease",
        "source": "Recommend Limit Increase",
        "summary": "Recommend Limit Increase",
        "x-model-operation": "Recommend Limit Increase",
        "successStatuses": (200,),
        "errorStatuses": (422, 403),
    },
    "/integration/credit-scoring:get-credit-score": {
        "method": "POST",
        "path": "/integration/credit-scoring:get-credit-score",
        "operationId": "getCreditScore",
        "source": "Get Credit Score",
        "summary": "Get Credit Score",
        "x-model-operation": "Get Credit Score",
        "contractId": "C-01",
        "allowedCaller": CREDIT_SCORING_ADAPTER,
        "successStatuses": (200,),
        "errorStatuses": (503, 403),
    },
    "/integration/disbursements:request": {
        "method": "POST",
        "path": "/integration/disbursements:request",
        "operationId": "disbursementAndAccountingRequest",
        "source": "Disbursement and Accounting Request",
        "summary": "Disbursement and Accounting Request",
        "x-model-operation": "Disbursement and Accounting Request",
        "contractId": "C-02",
        "allowedCaller": DISBURSEMENT_ADAPTER,
        "successStatuses": (202,),
        "errorStatuses": (502, 403),
    },
    "/integration/disbursements:post": {
        "method": "POST",
        "path": "/integration/disbursements:post",
        "operationId": "postDisbursementAndAccounting",
        "source": "Post Disbursement and Accounting",
        "summary": "Post Disbursement and Accounting",
        "x-model-operation": "Post Disbursement and Accounting",
        "contractId": "C-03",
        "allowedCaller": ESB_INTEGRATION_LAYER,
        "successStatuses": (202,),
        "errorStatuses": (502, 403),
    },
}


# Transport-shape metadata for the committed OpenAPI request schemas.  This is
# validation of the six frozen envelopes, not a seventh operation or a domain
# rule.  Business constraints remain in their named I-7 owners.
REQUEST_CONTRACTS = {
    "/loan-applications:submit-and-decide": {
        "required": (
            "customer_id",
            "existing_customer",
            "salaried",
            "age",
            "requested_amount",
            "scoring_mode",
            "policy_mode",
        ),
        "fields": {
            "customer_id": ("string", None, "CON.2", 422),
            "existing_customer": ("boolean", None, "CON.2", 422),
            "salaried": ("boolean", None, "CON.2", 422),
            "age": ("integer", None, "CON.2", 422),
            "requested_amount": ("positive_integer", None, "CON.1", 422),
            "scoring_mode": ("enum", ("success", "timeout", "unavailable"), "CON.3", 503),
            "policy_mode": ("enum", ("accept", "reject"), "CON.1", 422),
        },
        "extra_error": ("CON.1", 422),
    },
    "/loan-applications/{loanApplicationId}:disburse": {
        "required": ("account_eligible", "posting_mode"),
        "fields": {
            "account_eligible": ("boolean", None, "CON.4", 422),
            "posting_mode": ("enum", ("success", "failure"), "CON.4", 422),
        },
        "extra_error": ("CON.4", 422),
    },
    "/customers/{customerId}:recommend-limit-increase": {
        "required": (
            "existing_customer",
            "salaried",
            "age",
            "requested_amount",
            "policy_mode",
        ),
        "fields": {
            "existing_customer": ("boolean", None, "CON.2", 422),
            "salaried": ("boolean", None, "CON.2", 422),
            "age": ("integer", None, "CON.2", 422),
            "requested_amount": ("positive_integer", None, "CON.1", 422),
            "policy_mode": ("enum", ("accept", "reject"), "CON.1", 422),
        },
        "extra_error": ("CON.1", 422),
    },
    "/integration/credit-scoring:get-credit-score": {
        "required": ("customer_id", "scoring_mode"),
        "fields": {
            "customer_id": ("string", None, "CON.3", 503),
            "scoring_mode": ("enum", ("success", "timeout", "unavailable"), "CON.3", 503),
        },
        "extra_error": ("CON.3", 503),
    },
    "/integration/disbursements:request": {
        "required": (
            "loan_application_id",
            "account_validated",
            "amount",
            "posting_mode",
        ),
        "fields": {
            "loan_application_id": ("string", None, "CON.4", 502),
            "account_validated": ("boolean", None, "CON.4", 502),
            "amount": ("positive_integer", None, "CON.4", 502),
            "posting_mode": ("enum", ("success", "failure"), "CON.4", 502),
        },
        "extra_error": ("CON.4", 502),
    },
    "/integration/disbursements:post": {
        "required": (
            "loan_application_id",
            "account_validated",
            "amount",
            "posting_mode",
        ),
        "fields": {
            "loan_application_id": ("string", None, "CON.4", 502),
            "account_validated": ("boolean", None, "CON.4", 502),
            "amount": ("positive_integer", None, "CON.4", 502),
            "posting_mode": ("enum", ("success", "failure"), "CON.4", 502),
        },
        "extra_error": ("CON.4", 502),
    },
}
