"""Account Validation Service (I-4 container).

Confirms the customer payment account is eligible before disbursement (CON.4).

Model note: Lab 9 drew an `Account Validation Service -> Core Banking` HTTPS edge,
but the Lab 10 feedback correction explicitly REMOVED that edge ("account
validation completes before Disbursement Adapter enters the ESB/Core Banking
asynchronous path"). Following the later after-pack decision (Models win; Lab 10
audit), this service validates payment-account eligibility as its own
responsibility and does not open a synchronous Core Banking edge in the
disbursement slice. Only `Disbursement Adapter` enters the ESB/Core Banking path.
This Lab 9 <-> Lab 10 divergence is flagged in README.md for SA to reconcile in
the pack.
"""
from __future__ import annotations

from .. import names as N


class AccountValidationService:
    NAME = N.ACCOUNT_VALIDATION_SERVICE

    def validate_payment_account(self, account_id: str, eligible: bool) -> bool:
        """Return True if the payment account is eligible. CON.4: on failure the
        caller must NOT send any disbursement request."""
        return bool(eligible)
