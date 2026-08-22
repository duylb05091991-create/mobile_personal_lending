"""ESB Integration Layer - mocked I-3 external (in-process fake).

Backing service for contract C-02 (Disbursement and Accounting Request). It is
the only path to Core Banking (C-03). Async is modelled as a request that returns
a confirmation/failure outcome after routing to Core Banking. Only the
`Disbursement Adapter` may send into the ESB (C-02 producer).
"""
from __future__ import annotations

from .. import names as N
from ..domain.errors import ForbiddenPathError
from .core_banking import CoreBankingFake, DisbursementRecord

_ALLOWED_CALLERS = frozenset({N.DISBURSEMENT_ADAPTER})


class EsbIntegrationLayerFake:
    """Simulated message bus + reconciliation with confirmation."""

    NAME = N.ESB_INTEGRATION_LAYER

    def __init__(self, core_banking: CoreBankingFake):
        self._core_banking = core_banking

    def send_disbursement_and_accounting(
        self,
        application_id: str,
        amount_vnd: int,
        disbursement_reference: str,
        *,
        caller: str,
        posting_fails: bool = False,
    ) -> DisbursementRecord:
        """C-02 send -> routes to C-03 Post Disbursement and Accounting.

        Message/Async with confirmation. `caller` guard keeps the only-Disbursement-
        Adapter rule; the ESB then posts to Core Banking as the sole permitted C-03
        caller.
        """
        if caller not in _ALLOWED_CALLERS:
            raise ForbiddenPathError(
                f"{caller} may not send into {self.NAME} "
                f"(only {N.DISBURSEMENT_ADAPTER} may send C-02)",
                con=N.CON_4,
            )
        # ESB is the sole permitted caller of Core Banking C-03.
        return self._core_banking.post_disbursement_and_accounting(
            application_id,
            amount_vnd,
            disbursement_reference,
            caller=self.NAME,
            posting_fails=posting_fails,
        )
