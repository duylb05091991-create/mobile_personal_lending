"""Core Banking - mocked I-3 external (in-process fake).

Backing service for contract C-03 (Post Disbursement and Accounting). I-7 makes
Core Banking the source of truth for `Disbursement Record`. Per Lab 3 contract
rules and I-9, only the `ESB Integration Layer` reaches Core Banking for posting
(Disbursement Adapter -> ESB Integration Layer -> Core Banking). A direct call
from `Mobile App` (or anything other than ESB Integration Layer) is the I-9
forbidden path and is rejected.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from .. import names as N
from ..domain.errors import ForbiddenPathError

# Only the ESB Integration Layer may post to Core Banking (C-03 producer).
_ALLOWED_CALLERS = frozenset({N.ESB_INTEGRATION_LAYER})


@dataclass
class DisbursementRecord:
    """I-7: Disbursement Record - mastered by Core Banking."""

    reference: str
    application_id: str
    amount_vnd: int
    confirmed: bool


class CoreBankingFake:
    """Simulated ledger/disbursement system of record."""

    NAME = N.CORE_BANKING

    def post_disbursement_and_accounting(
        self,
        application_id: str,
        amount_vnd: int,
        disbursement_reference: str,
        *,
        caller: str,
        posting_fails: bool = False,
    ) -> DisbursementRecord:
        """C-03 Post Disbursement and Accounting.

        `posting_fails=True` simulates CON.4 posting/confirmation failure. `caller`
        enforces the I-9 forbidden path: Mobile App must not write directly to
        Core Banking.
        """
        if caller not in _ALLOWED_CALLERS:
            raise ForbiddenPathError(
                f"{caller} may not write directly to {self.NAME} "
                f"(I-9 forbidden path; only {N.ESB_INTEGRATION_LAYER} may post)",
                con=N.CON_4,
            )
        if posting_fails:
            # Record retained for reconciliation, but not confirmed.
            return DisbursementRecord(
                reference=disbursement_reference,
                application_id=application_id,
                amount_vnd=amount_vnd,
                confirmed=False,
            )
        return DisbursementRecord(
            reference=disbursement_reference or f"CB-{uuid.uuid4().hex[:10]}",
            application_id=application_id,
            amount_vnd=amount_vnd,
            confirmed=True,
        )
