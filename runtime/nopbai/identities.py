"""Frozen Lab 1 identities used by the Capstone runtime."""

MOBILE_APP = "Mobile App"
LOAN_APPLICATION_SERVICE = "Loan Application Service"
CREDIT_SCORING_ADAPTER = "Credit Scoring Adapter"
DECISION_ENGINE = "Decision Engine"
POLICY_ENGINE = "Policy Engine"
ACCOUNT_VALIDATION_SERVICE = "Account Validation Service"
DISBURSEMENT_ADAPTER = "Disbursement Adapter"
DECISION_STORE = "Decision Store"
AUDIT_LOG = "Audit Log"

I4_IDENTITIES = (
    MOBILE_APP,
    LOAN_APPLICATION_SERVICE,
    CREDIT_SCORING_ADAPTER,
    DECISION_ENGINE,
    POLICY_ENGINE,
    ACCOUNT_VALIDATION_SERVICE,
    DISBURSEMENT_ADAPTER,
    DECISION_STORE,
    AUDIT_LOG,
)

CREDIT_SCORING_SYSTEM = "Credit Scoring System"
ESB_INTEGRATION_LAYER = "ESB Integration Layer"
CORE_BANKING = "Core Banking"

I3_IDENTITIES = (
    CREDIT_SCORING_SYSTEM,
    ESB_INTEGRATION_LAYER,
    CORE_BANKING,
)

DECISION_ENGINE_COMPONENTS = (
    "Decision Orchestrator",
    "Eligibility Evaluator",
    "Score Coordinator",
    "Policy Evaluation Module",
    "Offer Builder",
    "Decision Recorder",
)

LOAN_APPLICATION_STATES = (
    "Draft",
    "Submitted",
    "Scoring",
    "OfferReady",
    "Approved",
    "AccountValidated",
    "Rejected",
    "Disbursed",
    "Failed",
)

TRANSITION_OPERATIONS = (
    "start_application",
    "start_scoring",
    "reject_out_of_segment",
    "mark_offer_ready",
    "fail_scoring",
    "approve_agreement",
    "reject_policy",
    "decline_offer",
    "validate_account",
    "fail_account_validation",
    "complete_disbursement",
    "fail_posting",
)

# Lab 10's exact participant-to-SUT assignment for the twelve I-6 operations.
# Loan Application Service remains the only writer; this mapping records the
# modeled I-4 participant that performed the behavior leading to each write.
TRANSITION_PERFORMERS = {
    "start_application": MOBILE_APP,
    "start_scoring": LOAN_APPLICATION_SERVICE,
    "reject_out_of_segment": LOAN_APPLICATION_SERVICE,
    "mark_offer_ready": DECISION_ENGINE,
    "fail_scoring": CREDIT_SCORING_ADAPTER,
    "approve_agreement": MOBILE_APP,
    "reject_policy": DECISION_ENGINE,
    "decline_offer": MOBILE_APP,
    "validate_account": ACCOUNT_VALIDATION_SERVICE,
    "fail_account_validation": ACCOUNT_VALIDATION_SERVICE,
    "complete_disbursement": DISBURSEMENT_ADAPTER,
    "fail_posting": DISBURSEMENT_ADAPTER,
}
