"""Single source of truth for Lab 1 identity strings.

Clean-code standard (capstone.md): "Use Lab 1 strings in code, OpenAPI, tests,
and the name map - one spelling per thing." Every container name, state, actor,
external system, and constraint id is defined exactly once here and imported
everywhere else. No string that names a Lab 1 thing is written twice.

Do not fork a name. If a name is wrong, SA fixes the after pack first (see
SIGNOFF.md / Models win), then this file is retied.
"""

# --- I-1 system-in-focus / product -------------------------------------------
SYSTEM_IN_FOCUS = "Nopbai Personal Loan Platform"
PRODUCT = "Nopbai Mobile Personal Loan"
CONTRACT = "Nopbai Personal Loan Agreement"
GOAL = (
    "Provide a mobile-first unsecured personal loan journey with automated, "
    "policy-controlled decisioning and immediate disbursement."
)

# --- I-2 actors ---------------------------------------------------------------
CUSTOMER = "Customer"
LOAN_OPERATIONS_SPECIALIST = "Loan Operations Specialist"

# --- I-3 external systems (mocked backing services) ---------------------------
CREDIT_SCORING_SYSTEM = "Credit Scoring System"
ESB_INTEGRATION_LAYER = "ESB Integration Layer"
CORE_BANKING = "Core Banking"

# --- I-4 internal containers --------------------------------------------------
MOBILE_APP = "Mobile App"
LOAN_APPLICATION_SERVICE = "Loan Application Service"
CREDIT_SCORING_ADAPTER = "Credit Scoring Adapter"
DECISION_ENGINE = "Decision Engine"
POLICY_ENGINE = "Policy Engine"
ACCOUNT_VALIDATION_SERVICE = "Account Validation Service"
DISBURSEMENT_ADAPTER = "Disbursement Adapter"
DECISION_STORE = "Decision Store"
AUDIT_LOG = "Audit Log"

# --- Decision Engine L3 components (I-11 selected container) -------------------
DECISION_ORCHESTRATOR = "Decision Orchestrator"
ELIGIBILITY_EVALUATOR = "Eligibility Evaluator"
SCORE_COORDINATOR = "Score Coordinator"
POLICY_EVALUATION_MODULE = "Policy Evaluation Module"
OFFER_BUILDER = "Offer Builder"
DECISION_RECORDER = "Decision Recorder"

# --- I-6 states (Loan Application) --------------------------------------------
DRAFT = "Draft"
SUBMITTED = "Submitted"
SCORING = "Scoring"
OFFER_READY = "OfferReady"
APPROVED = "Approved"
ACCOUNT_VALIDATED = "AccountValidated"
REJECTED = "Rejected"
DISBURSED = "Disbursed"
FAILED = "Failed"

TERMINAL_STATES = frozenset({REJECTED, DISBURSED, FAILED})

# --- I-6 moving object --------------------------------------------------------
LOAN_APPLICATION = "Loan Application"
LOAN_OFFER = "Loan Offer"
DECISION_RECORD = "Decision Record"
DISBURSEMENT_RECORD = "Disbursement Record"

# --- I-10 constraints ---------------------------------------------------------
CON_1 = "CON.1"  # amount must not exceed 100,000,000 VND
CON_2 = "CON.2"  # existing salaried customers aged 22-35 only
CON_3 = "CON.3"  # scoring near-real-time; timeout is controlled exception
CON_4 = "CON.4"  # no disbursement/posting before approval + account validation
CON_5 = "CON.5"  # customer data / decision evidence protected and auditable

# --- CON.1 hard value ---------------------------------------------------------
UNSECURED_AMOUNT_CAP_VND = 100_000_000

# --- I-3 contract ids (Lab 3 contract register) -------------------------------
C_01 = "C-01"  # Credit Scoring Adapter -> Credit Scoring System (Get Credit Score)
C_02 = "C-02"  # Disbursement Adapter -> ESB Integration Layer
C_03 = "C-03"  # ESB Integration Layer -> Core Banking (Post Disbursement and Accounting)
