"""Policy Engine (I-4 container).

I-7 source of truth for `Policy Configuration`. Domain-driven standard: the CON.1
amount-cap invariant lives in this owner, not copied into adapters or the UI.
Applies eligibility, amount, rate, and approval rules and returns a policy
outcome; Decision Engine acts on that verdict.
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import names as N


@dataclass
class PolicyOutcome:
    accepted: bool
    max_amount_vnd: int
    interest_rate: float
    con: str | None       # CON.1 when the cap is the reason for rejection
    basis: str


class PolicyEngine:
    NAME = N.POLICY_ENGINE

    # Policy Configuration (simulated). CON.1 hard value comes from names.py.
    AMOUNT_CAP_VND = N.UNSECURED_AMOUNT_CAP_VND

    def evaluate(self, requested_amount_vnd: int, credit_score: int) -> PolicyOutcome:
        """Calculate maximum eligible amount, personalized rate, and policy result.

        CON.1: an unsecured amount above the cap is rejected here (in the owner).
        """
        # Simulated affordability: higher score -> higher ceiling, capped by CON.1.
        score_ceiling = int((credit_score / 850) * (self.AMOUNT_CAP_VND + 20_000_000))
        max_amount = min(score_ceiling, self.AMOUNT_CAP_VND)

        # CON.1 hard rule: never allow an amount above the cap.
        if requested_amount_vnd > self.AMOUNT_CAP_VND:
            return PolicyOutcome(
                accepted=False,
                max_amount_vnd=max_amount,
                interest_rate=0.0,
                con=N.CON_1,
                basis=(
                    f"Requested {requested_amount_vnd:,} VND exceeds unsecured cap "
                    f"{self.AMOUNT_CAP_VND:,} VND ({N.CON_1})"
                ),
            )

        if requested_amount_vnd > max_amount:
            return PolicyOutcome(
                accepted=False,
                max_amount_vnd=max_amount,
                interest_rate=0.0,
                con=N.CON_1,
                basis=(
                    f"Requested {requested_amount_vnd:,} VND exceeds policy maximum "
                    f"{max_amount:,} VND for score {credit_score} ({N.CON_1})"
                ),
            )

        # Personalized rate: lower score -> higher rate.
        interest_rate = round(0.30 - (credit_score / 850) * 0.15, 4)
        return PolicyOutcome(
            accepted=True,
            max_amount_vnd=max_amount,
            interest_rate=interest_rate,
            con=None,
            basis=f"Approved within cap; score {credit_score}; max {max_amount:,} VND",
        )
