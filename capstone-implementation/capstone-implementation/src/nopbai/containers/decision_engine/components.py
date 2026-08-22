"""Decision Engine L3 components (the one I-11 selected container).

These are internal modules of `Decision Engine`, NOT additional I-4 containers
(see NAME_IDENTITY_MAP.md). Neighbours (Credit Scoring Adapter, Policy Engine,
Decision Store, Audit Log) are black boxes reached through their own container
objects.
"""
from __future__ import annotations

from ... import names as N
from ..audit_log import AuditLog
from ..credit_scoring_adapter import CreditScoringAdapter, ScoreResult
from ..decision_store import DecisionRecord, DecisionStore, LoanOffer
from ..policy_engine import PolicyEngine, PolicyOutcome


class EligibilityEvaluator:
    """Confirms the decisioning-side eligibility result.

    Note: the CON.2 initial-segment rejection is owned by `Loan Application Service`
    (Lab 10 feedback: single owner, rejected before Decision Engine). This
    component confirms the application handed over is in-segment and records the
    eligibility basis; it does not re-own CON.2.
    """

    NAME = N.ELIGIBILITY_EVALUATOR

    def confirm_eligible(self, is_existing_salaried: bool, age: int) -> bool:
        return bool(is_existing_salaried and 22 <= age <= 35)


class ScoreCoordinator:
    """Requests the Credit Score through Credit Scoring Adapter and turns success
    or timeout into a decision input (CON.3)."""

    NAME = N.SCORE_COORDINATOR

    def __init__(self, credit_scoring_adapter: CreditScoringAdapter):
        self._adapter = credit_scoring_adapter

    def collect(self, customer_id: str, *, timeout: bool = False) -> ScoreResult:
        return self._adapter.get_normalized_score(customer_id, timeout=timeout)


class PolicyEvaluationModule:
    """Requests maximum amount, personalized rate, and policy outcome from
    Policy Engine (CON.1 owner)."""

    NAME = N.POLICY_EVALUATION_MODULE

    def __init__(self, policy_engine: PolicyEngine):
        self._policy = policy_engine

    def evaluate(self, requested_amount_vnd: int, credit_score: int) -> PolicyOutcome:
        return self._policy.evaluate(requested_amount_vnd, credit_score)


class OfferBuilder:
    """Creates the customer-facing Loan Offer from accepted score and policy terms."""

    NAME = N.OFFER_BUILDER

    def build(self, application_id: str, outcome: PolicyOutcome, *, kind: str) -> LoanOffer:
        return LoanOffer(
            application_id=application_id,
            amount_vnd=outcome.max_amount_vnd,
            interest_rate=outcome.interest_rate,
            kind=kind,
        )


class DecisionRecorder:
    """Persists decision evidence to Decision Store (I-7 owner of Loan Offer and
    Decision Record) and appends audit events to Audit Log. It is the SOLE writer
    of Loan Offer / Decision Record, so no two modules master the same I-7 object."""

    NAME = N.DECISION_RECORDER

    def __init__(self, decision_store: DecisionStore, audit_log: AuditLog):
        self._store = decision_store
        self._audit = audit_log

    def record(
        self,
        application_id: str,
        *,
        credit_score: int | None,
        policy_basis: str,
        decision: str,
        con: str | None,
        loan_offer: LoanOffer | None,
    ) -> DecisionRecord:
        offer_id = None
        if loan_offer is not None:
            self._store.save_offer(loan_offer)
            offer_id = loan_offer.id
        record = self._store.save_record(
            DecisionRecord(
                application_id=application_id,
                credit_score=credit_score,
                policy_basis=policy_basis,
                decision=decision,
                con=con,
                loan_offer_id=offer_id,
            )
        )
        self._audit.append(
            actor=f"{N.DECISION_ENGINE}/{self.NAME}",
            application_id=application_id,
            event=f"Decision {decision} recorded; basis: {policy_basis}",
            con=con,
        )
        return record
