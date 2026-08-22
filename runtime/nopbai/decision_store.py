"""Decision Store: sole owner of Loan Offer and Decision Record."""

from copy import deepcopy

from .errors import ConstraintViolation
from .identities import DECISION_STORE


class DecisionStore:
    identity = DECISION_STORE

    def __init__(self):
        self.loan_offers = {}
        self.decision_records = {}
        self.calls = []
        self._next_offer_id = 1
        self._next_decision_id = 1

    @property
    def call_count(self):
        return len(self.calls)

    def persist(
        self,
        loan_application_id,
        customer_id,
        amount,
        annual_interest_rate,
        term_months,
        credit_score,
        policy_basis,
        outcome,
    ):
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise ConstraintViolation(
                "CON.1",
                "Decision Store refuses a Loan Offer with an invalid amount",
                "OfferReady",
                422,
            )
        loan_offer_id = "LO-{0:04d}".format(self._next_offer_id)
        self._next_offer_id += 1
        decision_record_id = "DR-{0:04d}".format(self._next_decision_id)
        self._next_decision_id += 1
        offer = {
            "loan_offer_id": loan_offer_id,
            "loan_application_id": loan_application_id,
            "customer_id": customer_id,
            "amount": amount,
            "annual_interest_rate": annual_interest_rate,
            "term_months": term_months,
            "outcome": outcome,
        }
        decision = {
            "decision_record_id": decision_record_id,
            "loan_application_id": loan_application_id,
            "loan_offer_id": loan_offer_id,
            "credit_score": credit_score,
            "policy_basis": policy_basis,
            "outcome": outcome,
        }
        self.loan_offers[loan_offer_id] = offer
        self.decision_records[decision_record_id] = decision
        self.calls.append(
            {
                "operation": "persist",
                "loan_application_id": loan_application_id,
                "loan_offer_id": loan_offer_id,
                "decision_record_id": decision_record_id,
            }
        )
        return deepcopy(offer), deepcopy(decision)

    def persist_failure(self, loan_application_id, policy_basis, outcome):
        decision_record_id = "DR-{0:04d}".format(self._next_decision_id)
        self._next_decision_id += 1
        decision = {
            "decision_record_id": decision_record_id,
            "loan_application_id": loan_application_id,
            "loan_offer_id": None,
            "credit_score": None,
            "policy_basis": policy_basis,
            "outcome": outcome,
        }
        self.decision_records[decision_record_id] = decision
        self.calls.append(
            {
                "operation": "persist_failure",
                "loan_application_id": loan_application_id,
                "decision_record_id": decision_record_id,
            }
        )
        return deepcopy(decision)

    def find_offer_for_application(self, loan_application_id):
        for offer in reversed(tuple(self.loan_offers.values())):
            if offer["loan_application_id"] == loan_application_id:
                return deepcopy(offer)
        return None

    def find_decision_for_application(self, loan_application_id):
        for decision in reversed(tuple(self.decision_records.values())):
            if decision["loan_application_id"] == loan_application_id:
                return deepcopy(decision)
        return None
