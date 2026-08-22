"""Decision Engine (I-4 container) - the one I-11 selected container.

Orchestrates eligibility, score, policy, offer, and approval/rejection decisions
via its `Decision Orchestrator` and the other five L3 components. It returns a
DecisionOutcome; it does NOT mutate `Loan Application` state - that object is
owned by `Loan Application Service` (I-7). Decision Engine does not call
`Credit Scoring System` or `Core Banking` directly.
"""
from __future__ import annotations

from dataclasses import dataclass

from ... import names as N
from ..audit_log import AuditLog
from ..credit_scoring_adapter import CreditScoringAdapter
from ..decision_store import DecisionStore, LoanOffer
from ..policy_engine import PolicyEngine
from .components import (
    DecisionRecorder,
    EligibilityEvaluator,
    OfferBuilder,
    PolicyEvaluationModule,
    ScoreCoordinator,
)


@dataclass
class DecisionOutcome:
    outcome: str            # "OfferReady" | "Rejected" | "Failed"
    con: str | None
    loan_offer: LoanOffer | None
    credit_score: int | None
    policy_basis: str


class DecisionEngine:
    NAME = N.DECISION_ENGINE

    def __init__(
        self,
        credit_scoring_adapter: CreditScoringAdapter,
        policy_engine: PolicyEngine,
        decision_store: DecisionStore,
        audit_log: AuditLog,
    ):
        # Decision Orchestrator is realized by this class's flow methods.
        self.eligibility_evaluator = EligibilityEvaluator()
        self.score_coordinator = ScoreCoordinator(credit_scoring_adapter)
        self.policy_evaluation_module = PolicyEvaluationModule(policy_engine)
        self.offer_builder = OfferBuilder()
        self.decision_recorder = DecisionRecorder(decision_store, audit_log)

    # -- UC1: Submit and Decide (score -> policy -> offer) --------------------
    def decide(
        self,
        application_id: str,
        customer_id: str,
        requested_amount_vnd: int,
        *,
        scoring_timeout: bool = False,
    ) -> DecisionOutcome:
        # Score collection (CON.3 controlled failure).
        score = self.score_coordinator.collect(customer_id, timeout=scoring_timeout)
        if not score.ok:
            self.decision_recorder.record(
                application_id,
                credit_score=None,
                policy_basis="Scoring timeout/unavailable; no approval",
                decision=N.FAILED,
                con=N.CON_3,
                loan_offer=None,
            )
            return DecisionOutcome(N.FAILED, N.CON_3, None, None, "scoring timeout (CON.3)")

        # Policy evaluation (CON.1 amount cap owned by Policy Engine).
        outcome = self.policy_evaluation_module.evaluate(requested_amount_vnd, score.credit_score)
        if not outcome.accepted:
            self.decision_recorder.record(
                application_id,
                credit_score=score.credit_score,
                policy_basis=outcome.basis,
                decision=N.REJECTED,
                con=outcome.con,
                loan_offer=None,
            )
            return DecisionOutcome(N.REJECTED, outcome.con, None, score.credit_score, outcome.basis)

        # Build and persist the Loan Offer + Decision Record.
        offer = self.offer_builder.build(application_id, outcome, kind="standard")
        self.decision_recorder.record(
            application_id,
            credit_score=score.credit_score,
            policy_basis=outcome.basis,
            decision=N.OFFER_READY,
            con=None,
            loan_offer=offer,
        )
        return DecisionOutcome(N.OFFER_READY, None, offer, score.credit_score, outcome.basis)

    # -- UC3: Recommend Limit Increase (eligible existing customer) -----------
    def recommend_limit_increase(
        self,
        application_id: str,
        requested_amount_vnd: int,
        credit_score: int,
    ) -> DecisionOutcome:
        outcome = self.policy_evaluation_module.evaluate(requested_amount_vnd, credit_score)
        if not outcome.accepted:
            self.decision_recorder.record(
                application_id,
                credit_score=credit_score,
                policy_basis=outcome.basis,
                decision=N.REJECTED,
                con=outcome.con,
                loan_offer=None,
            )
            return DecisionOutcome(N.REJECTED, outcome.con, None, credit_score, outcome.basis)

        offer = self.offer_builder.build(application_id, outcome, kind="limit-increase")
        self.decision_recorder.record(
            application_id,
            credit_score=credit_score,
            policy_basis=outcome.basis,
            decision=N.OFFER_READY,
            con=None,
            loan_offer=offer,
        )
        return DecisionOutcome(N.OFFER_READY, None, offer, credit_score, outcome.basis)
