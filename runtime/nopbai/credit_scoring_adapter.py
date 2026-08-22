"""Credit Scoring Adapter boundary for C-01 Get Credit Score."""

from .errors import ConstraintViolation
from .identities import CREDIT_SCORING_ADAPTER


class CreditScoringAdapter:
    identity = CREDIT_SCORING_ADAPTER

    def __init__(self, credit_scoring_system):
        self.credit_scoring_system = credit_scoring_system
        self.calls = []

    @property
    def call_count(self):
        return len(self.calls)

    def get_credit_score(self, customer_id, scoring_mode="success", state=None):
        self.calls.append({"customer_id": customer_id, "scoring_mode": scoring_mode})
        outcome = self.credit_scoring_system.get_credit_score(customer_id, scoring_mode)
        if outcome["status"] != "success":
            raise ConstraintViolation("CON.3", outcome["reason"], state, 503)
        return outcome["credit_score"]

