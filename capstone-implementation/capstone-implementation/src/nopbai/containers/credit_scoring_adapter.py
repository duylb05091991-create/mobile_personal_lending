"""Credit Scoring Adapter (I-4 container).

The only container that calls `Credit Scoring System` (I-3). It normalizes the
response and converts a timeout/unavailable outcome into a *controlled* failure
(CON.3) rather than letting it approve. Isolates the external contract C-01.
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import names as N
from ..external.credit_scoring_system import CreditScoringSystemFake


@dataclass
class ScoreResult:
    ok: bool
    credit_score: int | None
    con: str | None  # CON.3 when scoring failed


class CreditScoringAdapter:
    NAME = N.CREDIT_SCORING_ADAPTER

    def __init__(self, credit_scoring_system: CreditScoringSystemFake):
        self._css = credit_scoring_system

    def get_normalized_score(self, customer_id: str, *, timeout: bool = False) -> ScoreResult:
        """C-01 Get Credit Score, normalized. Timeout -> controlled CON.3 failure."""
        try:
            score = self._css.get_credit_score(customer_id, caller=self.NAME, timeout=timeout)
            return ScoreResult(ok=True, credit_score=score, con=None)
        except TimeoutError:
            # Controlled exception per CON.3; no exception leaks up to force approval.
            return ScoreResult(ok=False, credit_score=None, con=N.CON_3)
