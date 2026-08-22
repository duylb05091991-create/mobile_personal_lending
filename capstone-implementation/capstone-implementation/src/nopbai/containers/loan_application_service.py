"""Loan Application Service (I-4 container).

I-7 source of truth for `Loan Application`. It is the ONLY module that mutates
Loan Application state - every I-6 transition is applied here on the aggregate.
It owns the CON.2 initial-segment rejection (Lab 10 feedback: single owner,
rejected before Decision Engine). Decision Engine returns a decision outcome;
this service persists the resulting state.
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import names as N
from ..domain.loan_application import LoanApplication
from .account_validation_service import AccountValidationService
from .audit_log import AuditLog
from .credit_scoring_adapter import CreditScoringAdapter
from .decision_engine.engine import DecisionEngine
from .decision_store import DecisionStore, LoanOffer
from .disbursement_adapter import DisbursementAdapter


@dataclass
class SubmitResult:
    application_id: str
    state: str
    con: str | None
    loan_offer: LoanOffer | None
    reason: str | None


@dataclass
class DisburseResult:
    application_id: str
    state: str
    con: str | None
    reference: str | None
    reason: str | None


@dataclass
class RecommendResult:
    application_id: str
    accepted: bool
    con: str | None
    loan_offer: LoanOffer | None
    reason: str | None


class LoanApplicationService:
    NAME = N.LOAN_APPLICATION_SERVICE

    def __init__(
        self,
        decision_engine: DecisionEngine,
        account_validation_service: AccountValidationService,
        disbursement_adapter: DisbursementAdapter,
        credit_scoring_adapter: CreditScoringAdapter,
        decision_store: DecisionStore,
        audit_log: AuditLog,
    ):
        self._decision_engine = decision_engine
        self._account_validation = account_validation_service
        self._disbursement_adapter = disbursement_adapter
        self._credit_scoring_adapter = credit_scoring_adapter
        self._store = decision_store
        self._audit = audit_log
        self._apps: dict[str, LoanApplication] = {}

    def get(self, application_id: str) -> LoanApplication | None:
        return self._apps.get(application_id)

    def _in_segment(self, app: LoanApplication) -> bool:
        return app.is_existing_salaried and 22 <= app.customer_age <= 35

    # -- UC1: Submit and Decide Loan Application ------------------------------
    def submit_and_decide(
        self,
        *,
        customer_id: str,
        requested_amount_vnd: int,
        customer_age: int,
        is_existing_salaried: bool,
        payment_account_id: str,
        scoring_timeout: bool = False,
    ) -> SubmitResult:
        app = LoanApplication(
            customer_id=customer_id,
            requested_amount_vnd=requested_amount_vnd,
            customer_age=customer_age,
            is_existing_salaried=is_existing_salaried,
            payment_account_id=payment_account_id,
        )
        app.to_submitted()  # Draft -> Submitted (T-01)
        self._apps[app.id] = app

        # CON.2: reject out-of-segment BEFORE any decisioning (single owner here).
        if not self._in_segment(app):
            app.reject_out_of_segment()  # Submitted -> Rejected (T-03)
            self._audit.append(self.NAME, app.id, "Rejected before decisioning", con=N.CON_2)
            return SubmitResult(app.id, app.state, N.CON_2, None, app.reason)

        app.to_scoring()  # Submitted -> Scoring (T-02)

        outcome = self._decision_engine.decide(
            app.id, customer_id, requested_amount_vnd, scoring_timeout=scoring_timeout
        )

        if outcome.outcome == N.FAILED:            # CON.3 scoring timeout
            app.fail_scoring()                      # Scoring -> Failed (T-05)
            return SubmitResult(app.id, app.state, N.CON_3, None, app.reason)

        # Score succeeded -> OfferReady is reachable.
        app.to_offer_ready()                        # Scoring -> OfferReady (T-04)
        if outcome.outcome == N.REJECTED:           # CON.1 policy/amount-cap rejection
            app.reject_policy()                     # OfferReady -> Rejected (T-07)
            return SubmitResult(app.id, app.state, outcome.con, None, app.reason)

        # Happy path: Loan Offer created, application stays OfferReady.
        return SubmitResult(app.id, app.state, None, outcome.loan_offer, None)

    # -- OfferReady branches --------------------------------------------------
    def accept_agreement(self, application_id: str) -> LoanApplication:
        app = self._require(application_id)
        app.approve()  # OfferReady -> Approved (T-06)
        self._audit.append(self.NAME, app.id, f"{N.CONTRACT} accepted; Approved")
        return app

    def decline_offer(self, application_id: str) -> LoanApplication:
        app = self._require(application_id)
        app.decline()  # OfferReady -> Rejected (T-08)
        self._audit.append(self.NAME, app.id, "Customer declined the Loan Offer")
        return app

    # -- UC2: Disburse Approved Loan Application ------------------------------
    def disburse(self, application_id: str, *, posting_fails: bool = False) -> DisburseResult:
        app = self._require(application_id)

        # Account validation (CON.4). On failure: no disbursement request is sent.
        eligible = self._account_validation.validate_payment_account(
            app.payment_account_id, app.payment_account_eligible
        )
        if not eligible:
            app.fail_validation()  # Approved -> Failed (T-10)
            self._audit.append(
                self.NAME, app.id, "Account validation failed; no disbursement sent", con=N.CON_4
            )
            return DisburseResult(app.id, app.state, N.CON_4, None, app.reason)

        app.to_account_validated()  # Approved -> AccountValidated (T-09)

        outcome = self._disbursement_adapter.send(
            app.id, app.requested_amount_vnd, posting_fails=posting_fails
        )
        if not outcome.confirmed:
            app.fail_posting()  # AccountValidated -> Failed (T-12)
            self._audit.append(
                self.NAME,
                app.id,
                f"Posting/confirmation failed; reconciliation queued to "
                f"{N.LOAN_OPERATIONS_SPECIALIST}; {N.CORE_BANKING} ref {outcome.reference}",
                con=N.CON_4,
            )
            return DisburseResult(app.id, app.state, N.CON_4, outcome.reference, app.reason)

        app.to_disbursed()  # AccountValidated -> Disbursed (T-11)
        self._audit.append(
            self.NAME,
            app.id,
            f"Disbursed; {N.CORE_BANKING} {N.DISBURSEMENT_RECORD} ref {outcome.reference}",
        )
        return DisburseResult(app.id, app.state, None, outcome.reference, None)

    # -- UC3: Recommend Limit Increase ---------------------------------------
    def recommend_limit_increase(
        self,
        *,
        customer_id: str,
        requested_amount_vnd: int,
        customer_age: int,
        is_existing_salaried: bool,
    ) -> RecommendResult:
        # UC3 does not drive the I-6 Loan Application lifecycle; the customer-facing
        # result is the existing I-7 object Loan Offer (no new Recommendation object).
        recommendation_id = f"REC-{customer_id}"

        # CON.2: reject out-of-segment before Decision Engine evaluation (single owner).
        if not (is_existing_salaried and 22 <= customer_age <= 35):
            self._audit.append(self.NAME, recommendation_id, "Recommendation rejected", con=N.CON_2)
            return RecommendResult(recommendation_id, False, N.CON_2, None, "out-of-segment (CON.2)")

        # Existing-customer near-real-time score (no CON.3 branch is exposed for UC3).
        score = self._credit_scoring_adapter.get_normalized_score(customer_id)
        outcome = self._decision_engine.recommend_limit_increase(
            recommendation_id, requested_amount_vnd, score.credit_score
        )
        if outcome.outcome == N.REJECTED:  # CON.1 amount cap / policy rejection
            return RecommendResult(recommendation_id, False, outcome.con, None, outcome.policy_basis)
        return RecommendResult(recommendation_id, True, None, outcome.loan_offer, None)

    # -- internal -------------------------------------------------------------
    def _require(self, application_id: str) -> LoanApplication:
        app = self._apps.get(application_id)
        if app is None:
            raise KeyError(f"Unknown {N.LOAN_APPLICATION}: {application_id}")
        return app
