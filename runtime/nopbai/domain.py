"""I-6 lifecycle aggregate; only Loan Application Service keeps live instances."""

from dataclasses import dataclass, field
from enum import Enum

from .errors import ConstraintViolation


class LoanApplicationState(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    SCORING = "Scoring"
    OFFER_READY = "OfferReady"
    APPROVED = "Approved"
    ACCOUNT_VALIDATED = "AccountValidated"
    REJECTED = "Rejected"
    DISBURSED = "Disbursed"
    FAILED = "Failed"


@dataclass
class LoanApplication:
    loan_application_id: str
    customer_id: str
    requested_amount: int
    purpose: str = "personal-loan"
    _state: LoanApplicationState = LoanApplicationState.DRAFT
    _reasons: list = field(default_factory=list)

    def snapshot(self):
        return {
            "loan_application_id": self.loan_application_id,
            "customer_id": self.customer_id,
            "requested_amount": self.requested_amount,
            "purpose": self.purpose,
            "state": self._state.value,
            "reasons": list(self._reasons),
        }

    def _transition(self, operation, expected, target, constraint=None, reason=None):
        """Guard and perform one I-6 operation on the aggregate.

        Live aggregate instances remain private to Loan Application Service;
        callers receive only snapshots.
        """
        if self._state is not expected:
            raise ConstraintViolation(
                constraint or "CON.4",
                "{0} requires state {1}; current state is {2}".format(
                    operation, expected.value, self._state.value
                ),
                self._state.value,
                422,
            )
        previous = self._state
        self._state = target
        if reason:
            self._reasons.append(reason)
        return {
            "operation": operation,
            "loan_application_id": self.loan_application_id,
            "from_state": previous.value,
            "to_state": target.value,
            "constraint": constraint,
            "reason": reason,
        }
