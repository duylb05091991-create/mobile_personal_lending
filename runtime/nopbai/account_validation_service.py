"""Local simulated Account Validation Service; it never calls Core Banking."""

from .identities import ACCOUNT_VALIDATION_SERVICE


class AccountValidationService:
    identity = ACCOUNT_VALIDATION_SERVICE

    def __init__(self, audit_log, disbursement_adapter):
        self.audit_log = audit_log
        self.disbursement_adapter = disbursement_adapter
        self.calls = []

    @property
    def call_count(self):
        return len(self.calls)

    def validate(self, loan_application_id, account_eligible):
        eligible = account_eligible is True
        self.calls.append(
            {
                "loan_application_id": loan_application_id,
                "account_eligible": account_eligible,
                "eligible": eligible,
            }
        )
        self.audit_log.append(
            self.identity,
            "account-validation-success" if eligible else "account-validation-failure",
            loan_application_id,
            None if eligible else "CON.4",
            None if eligible else "Payment account is not eligible",
        )
        return eligible

    def start_disbursement(self, loan_application_id, amount, posting_mode):
        message = self.disbursement_adapter.request(
            loan_application_id, amount, True, posting_mode, "AccountValidated"
        )
        confirmation = self.disbursement_adapter.post(
            loan_application_id, posting_mode, "AccountValidated"
        )
        return message, confirmation
