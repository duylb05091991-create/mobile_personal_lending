"""Decision Engine and its six approved internal collaborators."""

from .errors import ConstraintViolation
from .identities import DECISION_ENGINE


class EligibilityEvaluator:
    """Consumes the segment-validation outcome; LAS owns the CON.2 rule."""

    def evaluate(self, segment_validated):
        return segment_validated is True


class ScoreCoordinator:
    def __init__(self, credit_scoring_adapter):
        self.credit_scoring_adapter = credit_scoring_adapter

    def collect(self, customer_id, scoring_mode, state):
        return self.credit_scoring_adapter.get_credit_score(customer_id, scoring_mode, state)


class PolicyEvaluationModule:
    def __init__(self, policy_engine):
        self.policy_engine = policy_engine

    def evaluate(self, requested_amount, policy_mode):
        return self.policy_engine.evaluate(requested_amount, policy_mode)


class OfferBuilder:
    def build_terms(self, policy_result):
        return {
            "amount": policy_result["amount"],
            "annual_interest_rate": policy_result["annual_interest_rate"],
            "term_months": policy_result["term_months"],
        }


class DecisionRecorder:
    def __init__(self, decision_store, audit_log):
        self.decision_store = decision_store
        self.audit_log = audit_log

    def record_offer(self, application, terms, credit_score, policy_basis, event_type):
        offer, decision = self.decision_store.persist(
            application["loan_application_id"],
            application["customer_id"],
            terms["amount"],
            terms["annual_interest_rate"],
            terms["term_months"],
            credit_score,
            policy_basis,
            "OfferReady",
        )
        self.audit_log.append(
            DECISION_ENGINE,
            event_type,
            application["loan_application_id"],
            None,
            None,
            {
                "loan_offer_id": offer["loan_offer_id"],
                "decision_record_id": decision["decision_record_id"],
            },
        )
        return offer

    def record_failure(self, application, constraint, reason, event_type):
        decision = self.decision_store.persist_failure(
            application["loan_application_id"], reason, application["state"]
        )
        self.audit_log.append(
            DECISION_ENGINE,
            event_type,
            application["loan_application_id"],
            constraint,
            reason,
            {"decision_record_id": decision["decision_record_id"]},
        )
        return decision


class DecisionOrchestrator:
    def __init__(self, score_coordinator, policy_evaluation_module, offer_builder, decision_recorder):
        self.score_coordinator = score_coordinator
        self.policy_evaluation_module = policy_evaluation_module
        self.offer_builder = offer_builder
        self.decision_recorder = decision_recorder

    def collect_score(self, application, scoring_mode):
        try:
            return self.score_coordinator.collect(
                application["customer_id"], scoring_mode, application["state"]
            )
        except ConstraintViolation as violation:
            failed_view = dict(application)
            failed_view["state"] = "Failed"
            self.decision_recorder.record_failure(
                failed_view, "CON.3", violation.reason, "scoring-timeout"
            )
            raise

    def create_offer(self, application, credit_score, policy_mode, event_type="decision-completed"):
        policy_result = self.policy_evaluation_module.evaluate(
            application["requested_amount"], policy_mode
        )
        if not policy_result["accepted"]:
            rejected_view = dict(application)
            rejected_view["state"] = "Rejected"
            self.decision_recorder.record_failure(
                rejected_view, "CON.1", policy_result["basis"], "policy-rejection"
            )
            raise ConstraintViolation("CON.1", policy_result["basis"], "OfferReady", 422)
        terms = self.offer_builder.build_terms(policy_result)
        return self.decision_recorder.record_offer(
            application, terms, credit_score, policy_result["basis"], event_type
        )


class DecisionEngine:
    identity = DECISION_ENGINE

    def __init__(self, credit_scoring_adapter, policy_engine, decision_store, audit_log):
        self.calls = []
        self.eligibility_evaluator = EligibilityEvaluator()
        self.score_coordinator = ScoreCoordinator(credit_scoring_adapter)
        self.policy_evaluation_module = PolicyEvaluationModule(policy_engine)
        self.offer_builder = OfferBuilder()
        self.decision_recorder = DecisionRecorder(decision_store, audit_log)
        self.decision_orchestrator = DecisionOrchestrator(
            self.score_coordinator,
            self.policy_evaluation_module,
            self.offer_builder,
            self.decision_recorder,
        )

    @property
    def call_count(self):
        return len(self.calls)

    def collect_score(self, application, scoring_mode, segment_validated):
        self.calls.append(
            {
                "operation": "collect_score",
                "loan_application_id": application["loan_application_id"],
            }
        )
        if not self.eligibility_evaluator.evaluate(segment_validated):
            raise ConstraintViolation(
                "CON.2",
                "Loan Application Service segment validation is required before scoring",
                application["state"],
                422,
            )
        return self.decision_orchestrator.collect_score(application, scoring_mode)

    def create_offer(self, application, credit_score, policy_mode="accept"):
        self.calls.append(
            {
                "operation": "create_offer",
                "loan_application_id": application["loan_application_id"],
            }
        )
        return self.decision_orchestrator.create_offer(
            application, credit_score, policy_mode, "decision-completed"
        )

    def recommend_offer(self, application, credit_score, policy_mode="accept"):
        self.calls.append(
            {
                "operation": "recommend_offer",
                "loan_application_id": application["loan_application_id"],
            }
        )
        return self.decision_orchestrator.create_offer(
            application, credit_score, policy_mode, "limit-increase-recommended"
        )
