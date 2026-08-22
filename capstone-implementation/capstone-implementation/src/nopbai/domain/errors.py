"""Domain errors.

These make the I-5 hard rules and I-9 forbidden path *impossible* to skip in the
runtime, not merely documented. Each maps to a stable OpenAPI error body so the
served contract and the runtime status/body cannot drift.
"""
from __future__ import annotations


class DomainError(Exception):
    """Base class. Carries the CON.* id and the resulting Loan Application state."""

    def __init__(self, message: str, *, con: str | None = None, state: str | None = None):
        super().__init__(message)
        self.message = message
        self.con = con
        self.state = state


class IllegalTransition(DomainError):
    """A Loan Application state transition that I-6 does not allow.

    Enforces I-5 hard rules structurally: e.g. you cannot Approve before Scoring,
    or Disburse before AccountValidated. Raised by the aggregate, never bypassable.
    """


class HardRuleViolation(DomainError):
    """A named I-5 / CON.* invariant was breached (e.g. CON.1 amount cap)."""


class ForbiddenPathError(DomainError):
    """An I-9 forbidden path was attempted (e.g. Mobile App -> Core Banking directly,
    or Mobile App performing credit evaluation). The runtime rejects it."""


class Unauthorized(DomainError):
    """CON.5: unauthenticated or unauthorized access to protected data/decisioning."""
