"""Loan Application Service: sole owner of Loan Application lifecycle state."""

from .domain import LoanApplication, LoanApplicationState
from .errors import ConstraintViolation
from .identities import LOAN_APPLICATION_SERVICE, TRANSITION_PERFORMERS


class LoanApplicationService:
    identity = LOAN_APPLICATION_SERVICE

    def __init__(self, audit_log, decision_engine):
        self.audit_log = audit_log
        self.decision_engine = decision_engine
        self._applications = {}
        self.transition_history = []
        self.calls = []
        self._next_id = 1

    @property
    def applications(self):
        """Defensive snapshots; callers cannot mutate the owned aggregates."""
        return {key: value.snapshot() for key, value in self._applications.items()}

    @property
    def call_count(self):
        return len(self.calls)

    def _create_draft(self, customer_id, requested_amount, purpose="personal-loan"):
        loan_application_id = "LA-{0:04d}".format(self._next_id)
        self._next_id += 1
        application = LoanApplication(
            loan_application_id=loan_application_id,
            customer_id=customer_id,
            requested_amount=requested_amount,
            purpose=purpose,
        )
        self._applications[loan_application_id] = application
        self.calls.append({"operation": "create_draft", "loan_application_id": loan_application_id})
        return application.snapshot()

    def get_application(self, loan_application_id):
        application = self._applications.get(loan_application_id)
        return application.snapshot() if application is not None else None

    @staticmethod
    def _in_initial_segment(existing_customer, salaried, age):
        return (
            existing_customer is True
            and salaried is True
            and isinstance(age, int)
            and not isinstance(age, bool)
            and 22 <= age <= 35
        )

    def submit_and_decide(
        self,
        customer_id,
        existing_customer,
        salaried,
        age,
        requested_amount,
        scoring_mode,
        policy_mode,
    ):
        application = self._create_draft(customer_id, requested_amount)
        loan_application_id = application["loan_application_id"]
        self._start_application(loan_application_id)
        if not self._in_initial_segment(existing_customer, salaried, age):
            reason = "Customer is outside the existing salaried age 22-35 segment"
            rejected = self._reject_out_of_segment(loan_application_id, reason)
            raise ConstraintViolation("CON.2", reason, rejected["state"], 422)
        scoring = self._start_scoring(loan_application_id)
        try:
            credit_score = self.decision_engine.collect_score(
                scoring, scoring_mode, segment_validated=True
            )
        except ConstraintViolation as violation:
            failed = self._fail_scoring(loan_application_id, violation.reason)
            raise ConstraintViolation("CON.3", violation.reason, failed["state"], 503)
        offer_ready = self._mark_offer_ready(loan_application_id)
        try:
            offer = self.decision_engine.create_offer(offer_ready, credit_score, policy_mode)
        except ConstraintViolation as violation:
            rejected = self._reject_policy(loan_application_id, violation.reason)
            raise ConstraintViolation("CON.1", violation.reason, rejected["state"], 422)
        return self.get_application(loan_application_id), offer

    def recommend_limit_increase(
        self,
        customer_id,
        existing_customer,
        salaried,
        age,
        requested_amount,
        policy_mode,
    ):
        application = self._create_draft(customer_id, requested_amount, "limit-increase")
        loan_application_id = application["loan_application_id"]
        self._start_application(loan_application_id)
        if not self._in_initial_segment(existing_customer, salaried, age):
            reason = "Customer is outside the existing salaried age 22-35 segment"
            rejected = self._reject_out_of_segment(loan_application_id, reason)
            raise ConstraintViolation("CON.2", reason, rejected["state"], 422)
        scoring = self._start_scoring(loan_application_id)
        try:
            offer = self.decision_engine.recommend_offer(scoring, None, policy_mode)
        except ConstraintViolation as violation:
            self._mark_offer_ready(loan_application_id)
            rejected = self._reject_policy(loan_application_id, violation.reason)
            raise ConstraintViolation("CON.1", violation.reason, rejected["state"], 422)
        self._mark_offer_ready(loan_application_id)
        return self.get_application(loan_application_id), offer

    # Public lifecycle commands preserve the modeled container coupling while
    # keeping low-level positive transition primitives internal to the owner.
    def record_agreement_acceptance(self, loan_application_id):
        application = self._require(loan_application_id)
        if application.purpose != "personal-loan":
            raise ConstraintViolation(
                "CON.4",
                "Only the personal-loan journey can enter approved disbursement",
                application._state.value,
                422,
            )
        return self._approve_agreement(loan_application_id)

    def record_customer_decline(self, loan_application_id):
        return self._decline_offer(loan_application_id)

    def record_account_validation(self, loan_application_id, eligible, reason=None):
        if eligible is True:
            return self._validate_account(loan_application_id)
        return self._fail_account_validation(
            loan_application_id,
            reason or "Payment account validation failed",
        )

    def record_disbursement_outcome(self, loan_application_id, confirmed, reason=None):
        if confirmed is True:
            return self._complete_disbursement(loan_application_id)
        return self._fail_posting(
            loan_application_id,
            reason or "Posting or confirmation failed",
        )

    def _require(self, loan_application_id):
        application = self._applications.get(loan_application_id)
        if application is None:
            raise ConstraintViolation(
                "CON.4",
                "Loan Application does not exist in Loan Application Service",
                None,
                422,
            )
        return application

    def _transition(
        self,
        loan_application_id,
        operation,
        expected,
        target,
        constraint=None,
        reason=None,
    ):
        application = self._require(loan_application_id)
        performed_by = TRANSITION_PERFORMERS[operation]
        evidence = application._transition(
            operation,
            expected,
            target,
            performed_by,
            self.identity,
            constraint,
            reason,
        )
        self.transition_history.append(evidence)
        self.calls.append(evidence.copy())
        self.audit_log.append(
            self.identity,
            "recommendation-lifecycle-transition"
            if application.purpose == "limit-increase"
            else "lifecycle-transition",
            loan_application_id,
            constraint,
            reason,
            {
                "customer_id": application.customer_id,
                "purpose": application.purpose,
                "from_state": evidence["from_state"],
                "to_state": evidence["to_state"],
                "operation": operation,
                "performed_by": evidence["performed_by"],
                "written_by": evidence["written_by"],
            },
        )
        return application.snapshot()

    # The following are the exact twelve guarded I-6 transition operations.
    def _start_application(self, loan_application_id):
        return self._transition(
            loan_application_id,
            "start_application",
            LoanApplicationState.DRAFT,
            LoanApplicationState.SUBMITTED,
        )

    def _start_scoring(self, loan_application_id):
        return self._transition(
            loan_application_id,
            "start_scoring",
            LoanApplicationState.SUBMITTED,
            LoanApplicationState.SCORING,
        )

    def _reject_out_of_segment(self, loan_application_id, reason):
        result = self._transition(
            loan_application_id,
            "reject_out_of_segment",
            LoanApplicationState.SUBMITTED,
            LoanApplicationState.REJECTED,
            "CON.2",
            reason,
        )
        self.audit_log.append(
            self.identity, "segment-rejection", loan_application_id, "CON.2", reason
        )
        return result

    def _mark_offer_ready(self, loan_application_id):
        return self._transition(
            loan_application_id,
            "mark_offer_ready",
            LoanApplicationState.SCORING,
            LoanApplicationState.OFFER_READY,
        )

    def _fail_scoring(self, loan_application_id, reason):
        return self._transition(
            loan_application_id,
            "fail_scoring",
            LoanApplicationState.SCORING,
            LoanApplicationState.FAILED,
            "CON.3",
            reason,
        )

    def _approve_agreement(self, loan_application_id):
        return self._transition(
            loan_application_id,
            "approve_agreement",
            LoanApplicationState.OFFER_READY,
            LoanApplicationState.APPROVED,
            "CON.4",
        )

    def _reject_policy(self, loan_application_id, reason):
        return self._transition(
            loan_application_id,
            "reject_policy",
            LoanApplicationState.OFFER_READY,
            LoanApplicationState.REJECTED,
            "CON.1",
            reason,
        )

    def _decline_offer(self, loan_application_id, reason="Customer declined the Loan Offer"):
        return self._transition(
            loan_application_id,
            "decline_offer",
            LoanApplicationState.OFFER_READY,
            LoanApplicationState.REJECTED,
            None,
            reason,
        )

    def _validate_account(self, loan_application_id):
        return self._transition(
            loan_application_id,
            "validate_account",
            LoanApplicationState.APPROVED,
            LoanApplicationState.ACCOUNT_VALIDATED,
            "CON.4",
        )

    def _fail_account_validation(self, loan_application_id, reason):
        return self._transition(
            loan_application_id,
            "fail_account_validation",
            LoanApplicationState.APPROVED,
            LoanApplicationState.FAILED,
            "CON.4",
            reason,
        )

    def _complete_disbursement(self, loan_application_id):
        return self._transition(
            loan_application_id,
            "complete_disbursement",
            LoanApplicationState.ACCOUNT_VALIDATED,
            LoanApplicationState.DISBURSED,
            "CON.4",
        )

    def _fail_posting(self, loan_application_id, reason):
        return self._transition(
            loan_application_id,
            "fail_posting",
            LoanApplicationState.ACCOUNT_VALIDATED,
            LoanApplicationState.FAILED,
            "CON.4",
            reason,
        )
