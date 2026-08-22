"""Credit Scoring System - mocked I-3 external (in-process fake).

capstone.md: "I-3 is mocked (stub or in-process fake)." This fake never calls a
real host and embeds no secret. It is the backing service for contract C-01
(Get Credit Score). Only `Credit Scoring Adapter` may call it - a direct call
tagged from any other caller (e.g. Mobile App performing credit evaluation) is
an I-9 forbidden path and is rejected.
"""
from __future__ import annotations

from .. import names as N
from ..domain.errors import ForbiddenPathError

# Callers permitted to reach the Credit Scoring System (I-8 C-01 producer only).
_ALLOWED_CALLERS = frozenset({N.CREDIT_SCORING_ADAPTER})


class CreditScoringSystemFake:
    """Simulated near-real-time scorer. Deterministic by scenario flag."""

    NAME = N.CREDIT_SCORING_SYSTEM

    def get_credit_score(self, customer_id: str, *, caller: str, timeout: bool = False) -> int:
        """C-01 Get Credit Score.

        `timeout=True` simulates CON.3 (timeout/unavailable) and raises TimeoutError,
        which the adapter converts into a controlled failure. `caller` enforces the
        I-9 forbidden path: only Credit Scoring Adapter may perform credit evaluation.
        """
        if caller not in _ALLOWED_CALLERS:
            raise ForbiddenPathError(
                f"{caller} may not call {self.NAME} directly (I-9 forbidden path; "
                f"credit evaluation is not performed by {caller})",
                con=N.CON_5,
            )
        if timeout:
            raise TimeoutError(f"{self.NAME} timeout/unavailable (CON.3)")
        # Simulated score in [300, 850]; stable per customer_id.
        return 300 + (abs(hash(customer_id)) % 551)
