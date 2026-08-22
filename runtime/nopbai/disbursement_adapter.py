"""Disbursement Adapter boundary for idempotent C-02/C-03 messages."""

from copy import deepcopy

from .errors import ConstraintViolation
from .identities import DISBURSEMENT_ADAPTER


class DisbursementAdapter:
    identity = DISBURSEMENT_ADAPTER

    def __init__(self, esb_integration_layer, audit_log):
        self.esb_integration_layer = esb_integration_layer
        self.audit_log = audit_log
        self.calls = []
        self.idempotency = {}

    @property
    def call_count(self):
        return len(self.calls)

    @property
    def request_count(self):
        return sum(1 for call in self.calls if call["operation"] == "request")

    def request(self, loan_application_id, amount, account_validated, posting_mode="success", state=None):
        if account_validated is not True or state != "AccountValidated":
            raise ConstraintViolation(
                "CON.4",
                "Disbursement requires a Loan Application in AccountValidated state",
                state,
                502,
            )
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise ConstraintViolation(
                "CON.4",
                "Disbursement message amount must be the positive owner-approved amount",
                state,
                502,
            )
        existing = self.idempotency.get(loan_application_id)
        if existing is not None:
            return deepcopy(existing)
        message = self.esb_integration_layer.enqueue(
            loan_application_id, amount, account_validated, posting_mode
        )
        self.idempotency[loan_application_id] = message
        self.calls.append(
            {
                "operation": "request",
                "loan_application_id": loan_application_id,
                "message_id": message["message_id"],
            }
        )
        return deepcopy(message)

    def post(self, loan_application_id, posting_mode="success", state=None):
        pending = self.esb_integration_layer.find_pending(loan_application_id)
        if pending is None:
            raise ConstraintViolation(
                "CON.4",
                "No accepted asynchronous disbursement message is pending",
                state,
                502,
            )
        confirmation = self.esb_integration_layer.post(
            pending["message_id"], posting_mode
        )
        self.calls.append(
            {
                "operation": "post",
                "loan_application_id": loan_application_id,
                "message_id": pending["message_id"],
                "status": confirmation["status"],
            }
        )
        if confirmation["status"] != "success":
            self.audit_log.append(
                self.identity,
                "disbursement-reconciliation",
                loan_application_id,
                "CON.4",
                confirmation["reason"],
                {
                    "message_id": pending["message_id"],
                    "disbursement_record_reference": confirmation["disbursement_record_reference"],
                },
            )
            raise ConstraintViolation("CON.4", confirmation["reason"], state, 502)
        self.audit_log.append(
            self.identity,
            "disbursement-confirmed",
            loan_application_id,
            None,
            None,
            {
                "message_id": pending["message_id"],
                "disbursement_record_reference": confirmation["disbursement_record_reference"],
            },
        )
        return confirmation
