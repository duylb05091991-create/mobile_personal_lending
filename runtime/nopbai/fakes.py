"""Deterministic in-process fakes for the three exact I-3 systems."""

from copy import deepcopy

from .identities import CORE_BANKING, CREDIT_SCORING_SYSTEM, ESB_INTEGRATION_LAYER


class CreditScoringSystem:
    identity = CREDIT_SCORING_SYSTEM

    def __init__(self):
        self.calls = []

    @property
    def call_count(self):
        return len(self.calls)

    def get_credit_score(self, customer_id, scoring_mode="success"):
        call = {"customer_id": customer_id, "scoring_mode": scoring_mode}
        self.calls.append(call)
        if scoring_mode in ("timeout", "unavailable"):
            return {
                "status": scoring_mode,
                "credit_score": None,
                "reason": "Credit Scoring System {0}".format(scoring_mode),
            }
        return {"status": "success", "credit_score": 720, "reason": None}


class ESBIntegrationLayer:
    identity = ESB_INTEGRATION_LAYER

    def __init__(self, core_banking):
        self.core_banking = core_banking
        self.messages = {}
        self.confirmations = []
        self.calls = []
        self._next_message_id = 1

    @property
    def enqueue_count(self):
        return sum(1 for call in self.calls if call["operation"] == "enqueue")

    @property
    def post_count(self):
        return sum(1 for call in self.calls if call["operation"] == "post")

    @property
    def call_count(self):
        return len(self.calls)

    def enqueue(self, loan_application_id, amount, account_validated, posting_mode):
        message_id = "MSG-{0:04d}".format(self._next_message_id)
        self._next_message_id += 1
        message = {
            "message_id": message_id,
            "loan_application_id": loan_application_id,
            "amount": amount,
            "account_validated": bool(account_validated),
            "posting_mode": posting_mode,
            "status": "accepted",
        }
        self.messages[message_id] = message
        self.calls.append({"operation": "enqueue", "message_id": message_id})
        return deepcopy(message)

    def find_pending(self, loan_application_id):
        for message in reversed(tuple(self.messages.values())):
            if message["loan_application_id"] == loan_application_id and message["status"] == "accepted":
                return deepcopy(message)
        return None

    def post(self, message_id, posting_mode=None):
        message = self.messages.get(message_id)
        if message is None or message["status"] != "accepted":
            return {
                "status": "failure",
                "reason": "No accepted asynchronous disbursement message is pending",
                "message_id": message_id,
                "disbursement_record_reference": None,
            }
        selected_mode = posting_mode or message["posting_mode"]
        self.calls.append({"operation": "post", "message_id": message_id})
        outcome = self.core_banking.post_disbursement(message, selected_mode)
        confirmation = {
            "message_id": message_id,
            "loan_application_id": message["loan_application_id"],
            "status": outcome["status"],
            "reason": outcome.get("reason"),
            "disbursement_record_reference": outcome.get("disbursement_record_reference"),
        }
        self.confirmations.append(confirmation)
        message["status"] = "confirmed" if outcome["status"] == "success" else "reconciliation-required"
        return deepcopy(confirmation)


class CoreBanking:
    identity = CORE_BANKING

    def __init__(self):
        self.customer_profiles = {}
        self.disbursement_records = {}
        self.calls = []
        self._next_record_id = 1

    @property
    def call_count(self):
        return len(self.calls)

    @property
    def post_count(self):
        return len(self.calls)

    def seed_customer_profile(self, customer_id, profile):
        value = deepcopy(profile)
        value["customer_id"] = customer_id
        self.customer_profiles[customer_id] = value
        return deepcopy(value)

    def post_disbursement(self, message, posting_mode="success"):
        record_id = "CB-DR-{0:04d}".format(self._next_record_id)
        self._next_record_id += 1
        confirmed = posting_mode == "success"
        record = {
            "disbursement_record_reference": record_id,
            "loan_application_id": message["loan_application_id"],
            "amount": message["amount"],
            "status": "confirmed" if confirmed else "reconciliation-required",
            "message_id": message["message_id"],
        }
        self.disbursement_records[record_id] = record
        self.calls.append(
            {
                "operation": "post_disbursement",
                "message_id": message["message_id"],
                "posting_mode": posting_mode,
                "record_reference": record_id,
            }
        )
        if confirmed:
            return {
                "status": "success",
                "reason": None,
                "disbursement_record_reference": record_id,
            }
        return {
            "status": "failure",
            "reason": "Core Banking posting or confirmation failed; reconciliation required",
            "disbursement_record_reference": record_id,
        }
