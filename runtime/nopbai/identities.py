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

