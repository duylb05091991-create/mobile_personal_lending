"""One-process composition root and the public request handler."""

import re

from .account_validation_service import AccountValidationService
from .audit_log import AuditLog
from .credit_scoring_adapter import CreditScoringAdapter
from .decision_engine import DecisionEngine
from .decision_store import DecisionStore
from .disbursement_adapter import DisbursementAdapter
from .errors import ConstraintViolation
from .fakes import CoreBanking, CreditScoringSystem, ESBIntegrationLayer
from .identities import (
    ACCOUNT_VALIDATION_SERVICE,
    AUDIT_LOG,
    CORE_BANKING,
    CREDIT_SCORING_ADAPTER,
    CREDIT_SCORING_SYSTEM,
    DECISION_ENGINE,
    DECISION_STORE,
    DISBURSEMENT_ADAPTER,
    ESB_INTEGRATION_LAYER,
    LOAN_APPLICATION_SERVICE,
    MOBILE_APP,
    POLICY_ENGINE,
)
from .loan_application_service import LoanApplicationService
from .mobile_app import MobileApp
from .policy_engine import PolicyEngine
from .routing import REQUEST_CONTRACTS, ROUTE_REGISTRY


class RuntimeApplication:
    """Composition helper, not an additional I-4 identity or deployable unit."""

    _disburse_pattern = re.compile(r"^/loan-applications/([^/:]+):disburse$")
    _recommend_pattern = re.compile(r"^/customers/([^/:]+):recommend-limit-increase$")

    def __init__(self):
        self.audit_log = AuditLog()
        self.decision_store = DecisionStore()
        self.credit_scoring_system = CreditScoringSystem()
        self.core_banking = CoreBanking()
        self.esb_integration_layer = ESBIntegrationLayer(self.core_banking)
        self.policy_engine = PolicyEngine()
        self.credit_scoring_adapter = CreditScoringAdapter(self.credit_scoring_system)
        self.disbursement_adapter = DisbursementAdapter(
            self.esb_integration_layer, self.audit_log
        )
        self.decision_engine = DecisionEngine(
            self.credit_scoring_adapter,
            self.policy_engine,
            self.decision_store,
            self.audit_log,
        )
        self.loan_application_service = LoanApplicationService(
            self.audit_log, self.decision_engine
        )
        self.account_validation_service = AccountValidationService(
            self.audit_log, self.disbursement_adapter
        )
        self.mobile_app = MobileApp(
            self.loan_application_service,
            self.account_validation_service,
        )
        self.containers = {
            MOBILE_APP: self.mobile_app,
            LOAN_APPLICATION_SERVICE: self.loan_application_service,
            CREDIT_SCORING_ADAPTER: self.credit_scoring_adapter,
            DECISION_ENGINE: self.decision_engine,
            POLICY_ENGINE: self.policy_engine,
            ACCOUNT_VALIDATION_SERVICE: self.account_validation_service,
            DISBURSEMENT_ADAPTER: self.disbursement_adapter,
            DECISION_STORE: self.decision_store,
            AUDIT_LOG: self.audit_log,
        }
        self.fakes = {
            CREDIT_SCORING_SYSTEM: self.credit_scoring_system,
            ESB_INTEGRATION_LAYER: self.esb_integration_layer,
            CORE_BANKING: self.core_banking,
        }
        self.route_registry = ROUTE_REGISTRY

    @staticmethod
    def _authorized(headers):
        return RuntimeApplication._header_value(
            headers, "X-Simulated-Authorized"
        ) == "true"

    @staticmethod
    def _header_value(headers, name):
        expected = name.lower()
        for key, value in headers.items():
            if str(key).lower() == expected:
                return str(value)
        return None

    def _state_for_request(self, path, body):
        match = self._disburse_pattern.match(path)
        loan_application_id = (
            match.group(1) if match else body.get("loan_application_id")
        )
        if loan_application_id:
            application = self.loan_application_service.get_application(
                loan_application_id
            )
            if application:
                return application["state"]
        return None

    def _deny(self, path, body):
        state = self._state_for_request(path, body)
        subject_id = self._subject_for_request(path, body)
        reason = "Unauthorized request: X-Simulated-Authorized: true is required"
        self.audit_log.append(
            AUDIT_LOG,
            "access-denied",
            subject_id,
            "CON.5",
            reason,
            {"path": path},
        )
        return 403, ConstraintViolation("CON.5", reason, state, 403).body()

    def _deny_caller(self, route_key, path, body, headers):
        route = self.route_registry[route_key]
        required = route["allowedCaller"]
        actual = self._header_value(headers, "X-Caller")
        state = self._state_for_request(path, body)
        subject_id = self._subject_for_request(path, body)
        reason = "Forbidden caller: X-Caller must be {0} for {1}".format(
            required, route["contractId"]
        )
        self.audit_log.append(
            AUDIT_LOG,
            "access-denied",
            subject_id,
            "CON.5",
            reason,
            {
                "path": path,
                "actual_caller": actual,
                "required_caller": required,
                "contract_id": route["contractId"],
            },
        )
        return 403, ConstraintViolation("CON.5", reason, state, 403).body()

    def _subject_for_request(self, path, body):
        match = self._disburse_pattern.match(path)
        if match:
            return match.group(1)
        match = self._recommend_pattern.match(path)
        if match:
            return match.group(1)
        return body.get("loan_application_id") or body.get("customer_id")

    def handle(self, method: str, path: str, body: dict, headers: dict):
        body = body if isinstance(body, dict) else {}
        headers = headers if isinstance(headers, dict) else {}
        method = str(method).upper()
        route_key = self._route_key(path)
        if route_key is None:
            return 404, {
                "error": {
                    "constraint": "CON.5",
                    "reason": "No callable operation exists for this path",
                    "state": None,
                }
            }
        if method != "POST":
            return 405, {
                "error": {
                    "constraint": "CON.5",
                    "reason": "Only POST is callable for this operation",
                    "state": self._state_for_request(path, body),
                }
            }
        if not self._authorized(headers):
            return self._deny(path, body)
        route = self.route_registry[route_key]
        allowed_caller = route.get("allowedCaller")
        if (
            allowed_caller is not None
            and self._header_value(headers, "X-Caller") != allowed_caller
        ):
            return self._deny_caller(route_key, path, body, headers)
        try:
            self._validate_contract(route_key, path, body)
            if path == "/loan-applications:submit-and-decide":
                return 200, self.mobile_app.submit_and_decide(body)
            match = self._disburse_pattern.match(path)
            if match:
                return 200, self.mobile_app.disburse(match.group(1), body)
            match = self._recommend_pattern.match(path)
            if match:
                return 200, self.mobile_app.recommend_limit_increase(
                    match.group(1), body
                )
            if path == "/integration/credit-scoring:get-credit-score":
                score = self.credit_scoring_adapter.get_credit_score(
                    body.get("customer_id"), body.get("scoring_mode", "success"), None
                )
                return 200, {
                    "customer_id": body.get("customer_id"),
                    "credit_score": score,
                }
            if path == "/integration/disbursements:request":
                return self._request_disbursement_message(body)
            return self._post_disbursement_message(body)
        except ConstraintViolation as violation:
            return violation.status, violation.body()

    def _route_key(self, path):
        if path in REQUEST_CONTRACTS:
            return path
        if self._disburse_pattern.match(path) is not None:
            return "/loan-applications/{loanApplicationId}:disburse"
        if self._recommend_pattern.match(path) is not None:
            return "/customers/{customerId}:recommend-limit-increase"
        return None

    @staticmethod
    def _matches_field(value, field_kind, allowed):
        if field_kind == "string":
            return isinstance(value, str) and len(value) >= 1
        if field_kind == "boolean":
            return isinstance(value, bool)
        if field_kind == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if field_kind == "positive_integer":
            return (
                isinstance(value, int)
                and not isinstance(value, bool)
                and value > 0
            )
        if field_kind == "enum":
            return isinstance(value, str) and value in allowed
        return False

    def _validate_contract(self, route_key, path, body):
        contract = REQUEST_CONTRACTS[route_key]
        state = self._state_for_request(path, body)
        fields = contract["fields"]
        extra = sorted(set(body) - set(fields))
        if extra:
            constraint, status = contract["extra_error"]
            raise ConstraintViolation(
                constraint,
                "Request contains fields outside the frozen OpenAPI contract: {0}".format(
                    ", ".join(extra)
                ),
                state,
                status,
            )
        for name in contract["required"]:
            field_kind, allowed, constraint, status = fields[name]
            if name not in body:
                raise ConstraintViolation(
                    constraint,
                    "Request is missing required OpenAPI field: {0}".format(name),
                    state,
                    status,
                )
            if not self._matches_field(body[name], field_kind, allowed):
                raise ConstraintViolation(
                    constraint,
                    "Request field does not match the frozen OpenAPI schema: {0}".format(
                        name
                    ),
                    state,
                    status,
                )

    def _request_disbursement_message(self, body):
        loan_application_id = body.get("loan_application_id")
        application = self.loan_application_service.get_application(loan_application_id)
        state = application["state"] if application else None
        if (
            application is None
            or state != "AccountValidated"
            or body.get("account_validated") is not True
            or body.get("amount") != application["requested_amount"]
        ):
            raise ConstraintViolation(
                "CON.4",
                "C-02 requires the LAS-owned AccountValidated application and its approved amount",
                state,
                502,
            )
        message = self.disbursement_adapter.request(
            loan_application_id,
            body.get("amount"),
            body.get("account_validated"),
            body.get("posting_mode", "success"),
            state,
        )
        return 202, {
            "message_id": message["message_id"],
            "loan_application_id": message["loan_application_id"],
            "status": "accepted",
        }

    def _post_disbursement_message(self, body):
        loan_application_id = body.get("loan_application_id")
        application = self.loan_application_service.get_application(loan_application_id)
        state = application["state"] if application else None
        if (
            application is None
            or state != "AccountValidated"
            or body.get("account_validated") is not True
            or body.get("amount") != application["requested_amount"]
        ):
            raise ConstraintViolation(
                "CON.4",
                "C-03 requires the LAS-owned AccountValidated application and its approved amount",
                state,
                502,
            )
        pending = self.esb_integration_layer.find_pending(loan_application_id)
        if pending is None:
            raise ConstraintViolation(
                "CON.4",
                "C-03 requires an accepted C-02 message before posting",
                state,
                502,
            )
        confirmation = self.disbursement_adapter.post(
            loan_application_id, body.get("posting_mode", "success"), state
        )
        return 202, {
            "message_id": confirmation["message_id"],
            "loan_application_id": confirmation["loan_application_id"],
            "status": "confirmed",
            "disbursement_record_reference": confirmation["disbursement_record_reference"],
        }


def create_application():
    return RuntimeApplication()
