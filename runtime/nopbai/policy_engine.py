"""Policy Engine: source of truth for the simulated Policy Configuration."""

from .identities import POLICY_ENGINE


class PolicyEngine:
    identity = POLICY_ENGINE
    amount_cap = 100000000

    def __init__(self):
        self.calls = []
        self.policy_configuration = {
            "maximum_unsecured_amount": self.amount_cap,
            "annual_interest_rate": 0.12,
            "term_months": 12,
        }

    @property
    def call_count(self):
        return len(self.calls)

    def evaluate(self, requested_amount, policy_mode="accept"):
        amount_is_valid = (
            isinstance(requested_amount, int)
            and not isinstance(requested_amount, bool)
            and requested_amount > 0
        )
        accepted = amount_is_valid and requested_amount <= self.amount_cap and policy_mode == "accept"
        reason = None
        if not amount_is_valid:
            reason = "Requested amount must be a positive whole number of VND"
        elif requested_amount > self.amount_cap:
            reason = "Requested amount exceeds the 100,000,000 VND unsecured cap"
        elif policy_mode != "accept":
            reason = "Policy Engine returned a rejected policy result"
        result = {
            "accepted": accepted,
            "amount": min(requested_amount, self.amount_cap) if amount_is_valid else 0,
            "annual_interest_rate": self.policy_configuration["annual_interest_rate"],
            "term_months": self.policy_configuration["term_months"],
            "basis": reason or "Policy-compliant amount and terms",
        }
        self.calls.append({"requested_amount": requested_amount, "policy_mode": policy_mode, "result": result.copy()})
        return result
