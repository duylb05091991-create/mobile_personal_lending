"""Mobile App entry behavior for the three exact I-11 use cases."""

from .errors import ConstraintViolation
from .identities import MOBILE_APP


class MobileApp:
    identity = MOBILE_APP

    def __init__(
        self,
        loan_application_service,
        account_validation_service,
    ):
        self.loan_application_service = loan_application_service
        self.account_validation_service = account_validation_service
        self.calls = []

    @property
    def call_count(self):
        return len(self.calls)

    def submit_and_decide(self, body):
        call = {"operation": "submit_and_decide"}
        self.calls.append(call)
        application, offer = self.loan_application_service.submit_and_decide(
            body.get("customer_id"),
            body.get("existing_customer"),
            body.get("salaried"),
            body.get("age"),
            body.get("requested_amount"),
            body.get("scoring_mode", "success"),
            body.get("policy_mode", "accept"),
        )
        call["loan_application_id"] = application["loan_application_id"]
        return {
            "loan_application_id": application["loan_application_id"],
            "state": application["state"],
            "loan_offer": offer,
        }

    def recommend_limit_increase(self, customer_id, body):
        call = {
            "operation": "recommend_limit_increase",
            "customer_id": customer_id,
        }
        self.calls.append(call)
        application, offer = (
            self.loan_application_service.recommend_limit_increase(
                customer_id,
                body.get("existing_customer"),
                body.get("salaried"),
                body.get("age"),
                body.get("requested_amount"),
                body.get("policy_mode", "accept"),
            )
        )
        call["loan_application_id"] = application["loan_application_id"]
        return {
            "loan_application_id": application["loan_application_id"],
            "state": application["state"],
            "loan_offer": offer,
        }

    def disburse(self, loan_application_id, body):
        self.calls.append(
            {"operation": "disburse", "loan_application_id": loan_application_id}
        )
        application = self.loan_application_service.get_application(loan_application_id)
        if application is None:
            raise ConstraintViolation(
                "CON.4", "Loan Application does not exist", None, 422
            )
        if application["state"] != "Approved":
            raise ConstraintViolation(
                "CON.4",
                "Disbursement requires prior Loan Agreement acceptance and Approved state",
                application["state"],
                422,
            )
        validated = self.validate_payment_account(
            loan_application_id, body.get("account_eligible")
        )
        try:
            _, confirmation = self.account_validation_service.start_disbursement(
                loan_application_id,
                validated["requested_amount"],
                body.get("posting_mode", "success"),
            )
        except ConstraintViolation as violation:
            failed = self.loan_application_service.record_disbursement_outcome(
                loan_application_id, False, violation.reason
            )
            raise ConstraintViolation("CON.4", violation.reason, failed["state"], 502)
        completed = self.loan_application_service.record_disbursement_outcome(
            loan_application_id, True
        )
        return {
            "loan_application_id": loan_application_id,
            "state": completed["state"],
            "disbursement_record_reference": confirmation["disbursement_record_reference"],
            "confirmation": "confirmed",
        }

    def decline_loan_offer(self, loan_application_id):
        self.calls.append(
            {
                "operation": "decline_loan_offer",
                "loan_application_id": loan_application_id,
            }
        )
        return self.loan_application_service.record_customer_decline(
            loan_application_id
        )

    def accept_loan_agreement(self, loan_application_id):
        """Execute the modeled agreement-acceptance step; this is not a public route."""
        self.calls.append(
            {"operation": "accept_loan_agreement", "loan_application_id": loan_application_id}
        )
        return self.loan_application_service.record_agreement_acceptance(
            loan_application_id
        )

    def validate_payment_account(self, loan_application_id, account_eligible):
        """Execute account validation and ask the lifecycle owner to record its outcome."""
        if not self.account_validation_service.validate(
            loan_application_id, account_eligible
        ):
            failed = self.loan_application_service.record_account_validation(
                loan_application_id, False, "Payment account validation failed"
            )
            raise ConstraintViolation(
                "CON.4",
                "Payment account validation failed; no disbursement request sent",
                failed["state"],
                422,
            )
        return self.loan_application_service.record_account_validation(
            loan_application_id, True
        )
