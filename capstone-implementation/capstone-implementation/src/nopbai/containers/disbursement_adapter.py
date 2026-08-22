"""Disbursement Adapter (I-4 container).

The only internal container that sends the disbursement request into the
`ESB Integration Layer` (C-02), which routes to `Core Banking` (C-03). Creates an
idempotent request and handles the posting outcome. CON.4: it is only reached
after approval and successful account validation; on posting/confirmation failure
it does not mark Disbursed and retains reconciliation evidence.
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import names as N
from ..external.esb_integration_layer import EsbIntegrationLayerFake


@dataclass
class DisbursementOutcome:
    confirmed: bool
    reference: str
    con: str | None  # CON.4 when posting/confirmation failed


class DisbursementAdapter:
    NAME = N.DISBURSEMENT_ADAPTER

    def __init__(self, esb_integration_layer: EsbIntegrationLayerFake):
        self._esb = esb_integration_layer

    def _reference(self, application_id: str) -> str:
        # Idempotent reference derived from the application id.
        return f"DISB-{application_id}"

    def send(self, application_id: str, amount_vnd: int, *, posting_fails: bool = False) -> DisbursementOutcome:
        """C-02 Disbursement and Accounting Request (Message/Async, with confirmation)."""
        reference = self._reference(application_id)
        record = self._esb.send_disbursement_and_accounting(
            application_id,
            amount_vnd,
            reference,
            caller=self.NAME,
            posting_fails=posting_fails,
        )
        if not record.confirmed:
            return DisbursementOutcome(confirmed=False, reference=record.reference, con=N.CON_4)
        return DisbursementOutcome(confirmed=True, reference=record.reference, con=None)
