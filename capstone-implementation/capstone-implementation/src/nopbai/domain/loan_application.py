"""Loan Application aggregate - the one I-6 lifecycle object as a TYPE.

OOP standard (capstone.md): "The I-6 named object is a type ... State transitions
are operations on that type, not a bag of scripts." States live as constrained
transitions, never as unconstrained strings. Every one of the twelve I-6
transitions is a method here; each asserts the allowed source state and raises
IllegalTransition otherwise. Terminal states (Rejected, Disbursed, Failed) have
no outgoing transition.

Domain-driven standard: this aggregate is owned by exactly one container,
`Loan Application Service` (I-7 source of truth for `Loan Application`). No other
module mutates its state; they call Loan Application Service, which owns the
lifecycle. That keeps CON.* / I-5 ordering invariants in one owner.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from .. import names as N
from .errors import IllegalTransition

# The twelve I-6 transitions, keyed (from_state -> set of allowed to_states).
# Source: Lab 1 I-6. Used to guard every operation below.
_ALLOWED: dict[str, set[str]] = {
    N.DRAFT: {N.SUBMITTED},
    N.SUBMITTED: {N.SCORING, N.REJECTED},
    N.SCORING: {N.OFFER_READY, N.FAILED},
    N.OFFER_READY: {N.APPROVED, N.REJECTED},
    N.APPROVED: {N.ACCOUNT_VALIDATED, N.FAILED},
    N.ACCOUNT_VALIDATED: {N.DISBURSED, N.FAILED},
    # terminal states intentionally absent -> any transition raises
}


@dataclass
class LoanApplication:
    """A single Loan Application and its lifecycle state (I-6)."""

    customer_id: str
    requested_amount_vnd: int
    customer_age: int
    is_existing_salaried: bool
    payment_account_id: str
    payment_account_eligible: bool = True
    id: str = field(default_factory=lambda: f"LA-{uuid.uuid4().hex[:12]}")
    state: str = N.DRAFT
    reason: str | None = None

    # -- guarded transition primitive ----------------------------------------
    def _transition(self, to_state: str, *, con: str | None = None, reason: str | None = None) -> None:
        allowed = _ALLOWED.get(self.state, set())
        if to_state not in allowed:
            raise IllegalTransition(
                f"{N.LOAN_APPLICATION} {self.id}: illegal transition "
                f"{self.state} -> {to_state}",
                con=con,
                state=self.state,
            )
        self.state = to_state
        self.reason = reason

    # -- the twelve I-6 transitions as named operations ----------------------
    def to_submitted(self) -> None:                       # Draft -> Submitted (T-01)
        self._transition(N.SUBMITTED)

    def to_scoring(self) -> None:                         # Submitted -> Scoring (T-02)
        self._transition(N.SCORING)

    def reject_out_of_segment(self) -> None:              # Submitted -> Rejected, CON.2 (T-03)
        self._transition(N.REJECTED, con=N.CON_2, reason="out-of-segment (CON.2)")

    def to_offer_ready(self) -> None:                     # Scoring -> OfferReady (T-04)
        self._transition(N.OFFER_READY)

    def fail_scoring(self) -> None:                       # Scoring -> Failed, CON.3 (T-05)
        self._transition(N.FAILED, con=N.CON_3, reason="scoring timeout/unavailable (CON.3)")

    def approve(self) -> None:                            # OfferReady -> Approved (T-06)
        self._transition(N.APPROVED)

    def reject_policy(self) -> None:                      # OfferReady -> Rejected, CON.1 (T-07)
        self._transition(N.REJECTED, con=N.CON_1, reason="amount cap / policy rejection (CON.1)")

    def decline(self) -> None:                            # OfferReady -> Rejected (T-08)
        self._transition(N.REJECTED, reason="customer declined the Loan Offer")

    def to_account_validated(self) -> None:               # Approved -> AccountValidated (T-09)
        self._transition(N.ACCOUNT_VALIDATED)

    def fail_validation(self) -> None:                    # Approved -> Failed, CON.4 (T-10)
        self._transition(N.FAILED, con=N.CON_4, reason="account validation failed (CON.4)")

    def to_disbursed(self) -> None:                       # AccountValidated -> Disbursed (T-11)
        self._transition(N.DISBURSED)

    def fail_posting(self) -> None:                       # AccountValidated -> Failed, CON.4 (T-12)
        self._transition(N.FAILED, con=N.CON_4, reason="posting/confirmation failed (CON.4)")

    # -- helpers -------------------------------------------------------------
    @property
    def is_terminal(self) -> bool:
        return self.state in N.TERMINAL_STATES
