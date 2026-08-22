"""Executable G4-G6 and hard-rule checks for the Nopbai capstone slice.

The stable ``CAP-*`` identifiers in test names and docstrings are part of the
spec-trace.  This suite deliberately uses only Python's standard library.
"""

import json
import math
import socket
import sys
import time
import unittest
from pathlib import Path
from unittest import mock


RUNTIME_ROOT = Path(__file__).resolve().parents[1]
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from nopbai.application import create_application  # noqa: E402
from nopbai.domain import LoanApplication, LoanApplicationState  # noqa: E402
from nopbai.identities import TRANSITION_OPERATIONS  # noqa: E402
from nopbai.routing import REQUEST_CONTRACTS  # noqa: E402


# Exact I-4 / Lab 9 container identities.  Every SUT assertion uses one of
# these constants instead of a code-only alias.
MOBILE_APP = "Mobile App"
LOAN_APPLICATION_SERVICE = "Loan Application Service"
CREDIT_SCORING_ADAPTER = "Credit Scoring Adapter"
DECISION_ENGINE = "Decision Engine"
POLICY_ENGINE = "Policy Engine"
ACCOUNT_VALIDATION_SERVICE = "Account Validation Service"
DISBURSEMENT_ADAPTER = "Disbursement Adapter"
DECISION_STORE = "Decision Store"
AUDIT_LOG = "Audit Log"

I4_CONTAINERS = {
    MOBILE_APP,
    LOAN_APPLICATION_SERVICE,
    CREDIT_SCORING_ADAPTER,
    DECISION_ENGINE,
    POLICY_ENGINE,
    ACCOUNT_VALIDATION_SERVICE,
    DISBURSEMENT_ADAPTER,
    DECISION_STORE,
    AUDIT_LOG,
}

I3_FAKES = {
    "Credit Scoring System",
    "ESB Integration Layer",
    "Core Banking",
}

AUTHORIZED = {"X-Simulated-Authorized": "true"}

SUBMIT_PATH = "/loan-applications:submit-and-decide"
DISBURSE_TEMPLATE = "/loan-applications/{loanApplicationId}:disburse"
RECOMMEND_TEMPLATE = "/customers/{customerId}:recommend-limit-increase"
C01_PATH = "/integration/credit-scoring:get-credit-score"
C02_PATH = "/integration/disbursements:request"
C03_PATH = "/integration/disbursements:post"

OPENAPI_OPERATIONS = {
    SUBMIT_PATH: {
        "operationId": "submitAndDecideLoanApplication",
        "modelOperation": "Submit and Decide Loan Application",
        "statuses": {"200", "403", "422", "503"},
    },
    DISBURSE_TEMPLATE: {
        "operationId": "disburseApprovedLoanApplication",
        "modelOperation": "Disburse Approved Loan Application",
        "statuses": {"200", "403", "422", "502"},
    },
    RECOMMEND_TEMPLATE: {
        "operationId": "recommendLimitIncrease",
        "modelOperation": "Recommend Limit Increase",
        "statuses": {"200", "403", "422"},
    },
    C01_PATH: {
        "operationId": "getCreditScore",
        "modelOperation": "Get Credit Score",
        "statuses": {"200", "403", "503"},
    },
    C02_PATH: {
        "operationId": "disbursementAndAccountingRequest",
        "modelOperation": "Disbursement and Accounting Request",
        "statuses": {"202", "403", "502"},
    },
    C03_PATH: {
        "operationId": "postDisbursementAndAccounting",
        "modelOperation": "Post Disbursement and Accounting",
        "statuses": {"202", "403", "502"},
    },
}


class CapstoneRuntimeTestCase(unittest.TestCase):
    """Shared black-box requests and white-box evidence helpers."""

    maxDiff = None

    def setUp(self):
        self.app = create_application()
        self.assertEqual(set(self.app.containers), I4_CONTAINERS)
        self.assertEqual(set(self.app.fakes), I3_FAKES)
        self.assertEqual(
            tuple(state.value for state in LoanApplicationState),
            (
                "Draft",
                "Submitted",
                "Scoring",
                "OfferReady",
                "Approved",
                "AccountValidated",
                "Rejected",
                "Disbursed",
                "Failed",
            ),
        )
        self.assertFalse(hasattr(self.app.mobile_app, "decision_engine"))
        self.assertFalse(hasattr(self.app.mobile_app, "disbursement_adapter"))
        self.assertIs(
            self.app.loan_application_service.decision_engine,
            self.app.decision_engine,
        )
        self.assertIs(
            self.app.account_validation_service.disbursement_adapter,
            self.app.disbursement_adapter,
        )
        self.assertFalse(
            hasattr(self.app.account_validation_service, "core_banking")
        )
        self.assertFalse(hasattr(self.app.disbursement_adapter, "core_banking"))
        self.assertIs(
            self.app.esb_integration_layer.core_banking,
            self.app.core_banking,
        )

    def handle(self, method, path, body=None, headers=None, app=None):
        target = app or self.app
        return target.handle(
            method,
            path,
            {} if body is None else body,
            AUTHORIZED if headers is None else headers,
        )

    def submit_body(self, customer_id="customer-standard", **overrides):
        body = {
            "customer_id": customer_id,
            "existing_customer": True,
            "salaried": True,
            "age": 30,
            "requested_amount": 50_000_000,
            "scoring_mode": "success",
            "policy_mode": "accept",
        }
        body.update(overrides)
        return body

    def recommend_body(self, customer_id="customer-standard", **overrides):
        body = {
            "existing_customer": True,
            "salaried": True,
            "age": 30,
            "requested_amount": 60_000_000,
            "policy_mode": "accept",
        }
        body.update(overrides)
        return body

    def submit_happy(self, customer_id="customer-standard", app=None, **overrides):
        target = app or self.app
        status, payload = self.handle(
            "POST",
            SUBMIT_PATH,
            self.submit_body(customer_id, **overrides),
            app=target,
        )
        self.assertEqual(status, 200, payload)
        self.assertEqual(set(payload), {"loan_application_id", "state", "loan_offer"})
        self.assertEqual(payload["state"], "OfferReady")
        self.assertIsInstance(payload["loan_offer"], dict)
        self.assertTrue(payload["loan_offer"])
        return payload["loan_application_id"], payload

    def disburse_happy(self, loan_application_id, app=None):
        target = app or self.app
        status, payload = self.handle(
            "POST",
            DISBURSE_TEMPLATE.replace("{loanApplicationId}", loan_application_id),
            {"account_eligible": True, "posting_mode": "success"},
            app=target,
        )
        self.assertEqual(status, 200, payload)
        self.assertEqual(
            set(payload),
            {
                "loan_application_id",
                "state",
                "disbursement_record_reference",
                "confirmation",
            },
        )
        self.assertEqual(payload["loan_application_id"], loan_application_id)
        self.assertEqual(payload["state"], "Disbursed")
        self.assertEqual(payload["confirmation"], "confirmed")
        self.assertTrue(payload["disbursement_record_reference"])
        return payload

    def _create_account_validated_application(
        self,
        customer_id="contract-customer",
        requested_amount=50_000_000,
        app=None,
    ):
        """Create a contract fixture through the I-7 owner's guarded methods.

        This is deliberately not a public route or a new use case.  It prepares
        the exact precondition under which the public C-02/C-03 operations may
        accept a message.
        """
        target = app or self.app
        loan_application_id, _ = self.submit_happy(
            customer_id,
            app=target,
            requested_amount=requested_amount,
        )
        target.mobile_app.accept_loan_agreement(loan_application_id)
        validated = target.mobile_app.validate_payment_account(
            loan_application_id, True
        )
        self.assertEqual(validated["state"], "AccountValidated")
        self.assertEqual(validated["requested_amount"], requested_amount)
        self.assertGreater(target.decision_engine.call_count, 0)
        self.assertGreater(target.policy_engine.call_count, 0)
        self.assertGreater(target.account_validation_service.call_count, 0)
        return loan_application_id, requested_amount

    def assert_error(self, status, payload, expected_status, constraint, state):
        self.assertEqual(status, expected_status, payload)
        self.assertEqual(set(payload), {"error"})
        self.assertEqual(set(payload["error"]), {"constraint", "reason", "state"})
        self.assertEqual(payload["error"]["constraint"], constraint)
        self.assertEqual(payload["error"]["state"], state)
        self.assertIsInstance(payload["error"]["reason"], str)
        self.assertTrue(payload["error"]["reason"].strip())

    @staticmethod
    def object_text(value):
        return json.dumps(
            value,
            default=lambda item: getattr(item, "__dict__", str(item)),
            ensure_ascii=False,
            sort_keys=True,
        )

    def audit_text(self, app=None):
        target = app or self.app
        return self.object_text(target.audit_log.events)

    def assert_audit_contains(self, *terms, app=None):
        text = self.audit_text(app=app).lower()
        for term in terms:
            self.assertIn(str(term).lower(), text)

    def application_record(self, loan_application_id, app=None):
        target = app or self.app
        service = target.loan_application_service
        if hasattr(service, "get_application"):
            return service.get_application(loan_application_id)
        return service.applications[loan_application_id]

    def application_state(self, loan_application_id, app=None):
        record = self.application_record(loan_application_id, app=app)
        if isinstance(record, dict):
            return record["state"]
        return record.state

    def history(self, loan_application_id, app=None):
        target = app or self.app
        history = target.loan_application_service.transition_history
        if isinstance(history, dict):
            return history.get(loan_application_id, [])
        return [
            entry
            for entry in history
            if (
                isinstance(entry, dict)
                and entry.get("loan_application_id") == loan_application_id
            )
            or getattr(entry, "loan_application_id", None) == loan_application_id
        ]

    @staticmethod
    def transition_pair(entry):
        if isinstance(entry, str):
            if "->" in entry:
                before, after = entry.split("->", 1)
                return before.strip(), after.strip()
            return None
        if isinstance(entry, (list, tuple)) and len(entry) >= 2:
            return str(entry[0]), str(entry[1])
        if isinstance(entry, dict):
            before = (
                entry.get("from_state")
                or entry.get("from")
                or entry.get("previous_state")
            )
            after = (
                entry.get("to_state")
                or entry.get("to")
                or entry.get("next_state")
                or entry.get("state")
            )
            if before is not None and after is not None:
                return str(before), str(after)
            return None
        before = (
            getattr(entry, "from_state", None)
            or getattr(entry, "previous_state", None)
        )
        after = (
            getattr(entry, "to_state", None)
            or getattr(entry, "next_state", None)
            or getattr(entry, "state", None)
        )
        if before is not None and after is not None:
            return str(before), str(after)
        return None

    def assert_transition(self, loan_application_id, before, after, sut, app=None):
        with self.subTest(SUT=sut, transition="{} -> {}".format(before, after)):
            pairs = {
                pair
                for pair in (
                    self.transition_pair(entry)
                    for entry in self.history(loan_application_id, app=app)
                )
                if pair is not None
            }
            self.assertIn((before, after), pairs)

    @staticmethod
    def call_total(item):
        values = []
        for attribute in (
            "call_count",
            "request_count",
            "enqueue_count",
            "post_count",
        ):
            value = getattr(item, attribute, None)
            if isinstance(value, int):
                values.append(value)
        for attribute in ("calls", "messages", "confirmations"):
            value = getattr(item, attribute, None)
            if value is not None:
                try:
                    values.append(len(value))
                except TypeError:
                    pass
        return sum(values)

    def downstream_snapshot(self, app=None):
        target = app or self.app
        return {
            name: self.call_total(target.fakes[name])
            for name in ("ESB Integration Layer", "Core Banking")
        }


class TestI11HappyPaths(CapstoneRuntimeTestCase):
    def test_CAP_I11_01_submit_and_decide_happy(self):
        """CAP-I11-01: Submit and Decide Loan Application happy path."""
        with self.subTest(SUT=DECISION_ENGINE):
            loan_id, payload = self.submit_happy("cap-i11-01")
            self.assertEqual(self.application_state(loan_id), "OfferReady")
            stored_offer = self.app.decision_store.find_offer_for_application(loan_id)
            stored_decision = self.app.decision_store.find_decision_for_application(loan_id)
            self.assertIsNotNone(stored_offer)
            self.assertIsNotNone(stored_decision)
            self.assert_audit_contains(loan_id, "decision-completed")
            self.assertEqual(payload["loan_offer"], stored_offer)

    def test_CAP_I11_02_disburse_approved_happy(self):
        """CAP-I11-02: Disburse Approved Loan Application happy path."""
        with self.subTest(SUT=DISBURSEMENT_ADAPTER):
            loan_id, _ = self.submit_happy("cap-i11-02")
            result = self.disburse_happy(loan_id)
            self.assertEqual(self.application_state(loan_id), "Disbursed")
            core = self.app.fakes["Core Banking"]
            self.assertIn(
                result["disbursement_record_reference"],
                self.object_text(core.disbursement_records),
            )
            self.assert_audit_contains(loan_id, "disbursement-confirmed")

    def test_CAP_I11_03_recommend_limit_increase_happy(self):
        """CAP-I11-03: Recommend Limit Increase happy path."""
        customer_id = "cap-i11-03"
        with self.subTest(SUT=DECISION_ENGINE):
            status, payload = self.handle(
                "POST",
                RECOMMEND_TEMPLATE.replace("{customerId}", customer_id),
                self.recommend_body(customer_id),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(set(payload), {"loan_application_id", "state", "loan_offer"})
            self.assertEqual(payload["state"], "OfferReady")
            self.assertIsInstance(payload["loan_offer"], dict)
            loan_id = payload["loan_application_id"]
            self.assertEqual(self.application_state(loan_id), "OfferReady")
            self.assert_transition(loan_id, "Draft", "Submitted", MOBILE_APP)
            self.assert_transition(
                loan_id,
                "Submitted",
                "Scoring",
                LOAN_APPLICATION_SERVICE,
            )
            self.assert_transition(loan_id, "Scoring", "OfferReady", DECISION_ENGINE)
            self.assert_audit_contains(loan_id, "limit-increase-recommended")


class TestSequenceAlternativesAndG5(CapstoneRuntimeTestCase):
    def test_CAP_A01_submit_CON2_compensates_before_decisioning(self):
        """CAP-A01: Submit CON.2 rejects before scoring/decisioning and audits."""
        scoring_before = self.call_total(self.app.fakes["Credit Scoring System"])
        with self.subTest(SUT=LOAN_APPLICATION_SERVICE):
            status, payload = self.handle(
                "POST",
                SUBMIT_PATH,
                self.submit_body("cap-a01", existing_customer=False),
            )
            self.assert_error(status, payload, 422, "CON.2", "Rejected")
            self.assertEqual(
                self.call_total(self.app.fakes["Credit Scoring System"]),
                scoring_before,
            )
            self.assertFalse(self.app.decision_store.loan_offers)
            loan_id = next(iter(self.app.loan_application_service.applications))
            self.assertEqual(self.application_state(loan_id), "Rejected")
            self.assert_audit_contains("CON.2", "segment-rejection", loan_id)

    def test_CAP_A02_submit_CON3_timeout_fails_without_approval(self):
        """CAP-A02: Submit CON.3 records Failed, no approval, with evidence."""
        with self.subTest(SUT=CREDIT_SCORING_ADAPTER):
            status, payload = self.handle(
                "POST",
                SUBMIT_PATH,
                self.submit_body("cap-a02", scoring_mode="timeout"),
            )
            self.assert_error(status, payload, 503, "CON.3", "Failed")
            self.assertFalse(self.app.decision_store.loan_offers)
            loan_id = next(iter(self.app.loan_application_service.applications))
            self.assertEqual(self.application_state(loan_id), "Failed")
            self.assert_audit_contains("CON.3", "scoring-timeout", "timeout", loan_id)

    def test_CAP_A03_submit_CON1_rejects_and_retains_policy_evidence(self):
        """CAP-A03: Submit CON.1 rejects, keeps policy basis, no Loan Offer."""
        with self.subTest(SUT=DECISION_ENGINE):
            status, payload = self.handle(
                "POST",
                SUBMIT_PATH,
                self.submit_body("cap-a03", requested_amount=100_000_001),
            )
            self.assert_error(status, payload, 422, "CON.1", "Rejected")
            self.assertFalse(self.app.decision_store.loan_offers)
            self.assertTrue(self.app.decision_store.decision_records)
            self.assertIn("100,000,000", self.object_text(self.app.decision_store.decision_records))
            loan_id = next(iter(self.app.loan_application_service.applications))
            self.assertEqual(self.application_state(loan_id), "Rejected")
            self.assert_audit_contains("CON.1", "policy-rejection", loan_id)

    def test_CAP_A04_disburse_validation_failure_sends_nothing_downstream(self):
        """CAP-A04: CON.4 validation failure records Failed and sends nothing."""
        loan_id, _ = self.submit_happy("cap-a04")
        before = self.downstream_snapshot()
        with self.subTest(SUT=ACCOUNT_VALIDATION_SERVICE):
            status, payload = self.handle(
                "POST",
                DISBURSE_TEMPLATE.replace("{loanApplicationId}", loan_id),
                {"account_eligible": False, "posting_mode": "success"},
            )
            self.assert_error(status, payload, 422, "CON.4", "Failed")
            self.assertEqual(self.downstream_snapshot(), before)
            self.assertEqual(self.application_state(loan_id), "Failed")
            self.assert_audit_contains("CON.4", "account-validation-failure", loan_id)

    def test_CAP_A05_disburse_posting_failure_reconciles_and_does_not_complete(self):
        """CAP-A05: CON.4 posting failure starts reconciliation and stays Failed."""
        loan_id, _ = self.submit_happy("cap-a05")
        before = self.downstream_snapshot()
        with self.subTest(SUT=DISBURSEMENT_ADAPTER):
            status, payload = self.handle(
                "POST",
                DISBURSE_TEMPLATE.replace("{loanApplicationId}", loan_id),
                {"account_eligible": True, "posting_mode": "failure"},
            )
            self.assert_error(status, payload, 502, "CON.4", "Failed")
            after = self.downstream_snapshot()
            self.assertGreater(after["ESB Integration Layer"], before["ESB Integration Layer"])
            self.assertGreater(after["Core Banking"], before["Core Banking"])
            self.assertEqual(self.application_state(loan_id), "Failed")
            failed_records = list(
                self.app.fakes["Core Banking"].disbursement_records.values()
            )
            self.assertTrue(failed_records)
            self.assertFalse(
                any(record.get("status") == "confirmed" for record in failed_records)
            )
            self.assert_audit_contains("CON.4", "reconciliation", "Failed")

    def test_CAP_A06_recommend_CON2_rejects_before_decision_engine(self):
        """CAP-A06: Recommend CON.2 rejects before Decision Engine evaluation."""
        customer_id = "cap-a06"
        with self.subTest(SUT=LOAN_APPLICATION_SERVICE):
            status, payload = self.handle(
                "POST",
                RECOMMEND_TEMPLATE.replace("{customerId}", customer_id),
                self.recommend_body(customer_id, salaried=False),
            )
            self.assert_error(status, payload, 422, "CON.2", "Rejected")
            self.assertFalse(self.app.decision_store.loan_offers)
            loan_id = next(iter(self.app.loan_application_service.applications))
            self.assert_transition(
                loan_id,
                "Submitted",
                "Rejected",
                LOAN_APPLICATION_SERVICE,
            )
            self.assert_audit_contains("CON.2", "segment-rejection", loan_id)

    def test_CAP_A07_recommend_CON1_rejects_and_retains_policy_basis(self):
        """CAP-A07: Recommend CON.1 rejects, audits, and creates no new offer."""
        customer_id = "cap-a07"
        with self.subTest(SUT=DECISION_ENGINE):
            status, payload = self.handle(
                "POST",
                RECOMMEND_TEMPLATE.replace("{customerId}", customer_id),
                self.recommend_body(customer_id, requested_amount=100_000_001),
            )
            self.assert_error(status, payload, 422, "CON.1", "Rejected")
            self.assertFalse(self.app.decision_store.loan_offers)
            self.assertTrue(self.app.decision_store.decision_records)
            loan_id = next(iter(self.app.loan_application_service.applications))
            self.assert_transition(
                loan_id,
                "OfferReady",
                "Rejected",
                DECISION_ENGINE,
            )
            self.assert_audit_contains("CON.1", "policy-rejection", loan_id)


class TestG6StateTransitions(CapstoneRuntimeTestCase):
    def test_CAP_S01_draft_to_submitted(self):
        """CAP-S01: Draft -> Submitted; SUT Mobile App."""
        loan_id, _ = self.submit_happy("cap-s01")
        self.assert_transition(loan_id, "Draft", "Submitted", MOBILE_APP)

    def test_CAP_S02_submitted_to_scoring(self):
        """CAP-S02: Submitted -> Scoring; SUT Loan Application Service."""
        loan_id, _ = self.submit_happy("cap-s02")
        self.assert_transition(
            loan_id,
            "Submitted",
            "Scoring",
            LOAN_APPLICATION_SERVICE,
        )

    def test_CAP_S03_submitted_to_rejected(self):
        """CAP-S03: Submitted -> Rejected CON.2; SUT Loan Application Service."""
        status, payload = self.handle(
            "POST",
            SUBMIT_PATH,
            self.submit_body("cap-s03", age=40),
        )
        self.assert_error(status, payload, 422, "CON.2", "Rejected")
        loan_id = next(iter(self.app.loan_application_service.applications))
        self.assert_transition(
            loan_id,
            "Submitted",
            "Rejected",
            LOAN_APPLICATION_SERVICE,
        )

    def test_CAP_S04_scoring_to_offer_ready(self):
        """CAP-S04: Scoring -> OfferReady; SUT Decision Engine."""
        loan_id, _ = self.submit_happy("cap-s04")
        self.assert_transition(loan_id, "Scoring", "OfferReady", DECISION_ENGINE)

    def test_CAP_S05_scoring_to_failed(self):
        """CAP-S05: Scoring -> Failed CON.3; SUT Credit Scoring Adapter."""
        status, payload = self.handle(
            "POST",
            SUBMIT_PATH,
            self.submit_body("cap-s05", scoring_mode="unavailable"),
        )
        self.assert_error(status, payload, 503, "CON.3", "Failed")
        loan_id = next(iter(self.app.loan_application_service.applications))
        self.assert_transition(
            loan_id,
            "Scoring",
            "Failed",
            CREDIT_SCORING_ADAPTER,
        )

    def test_CAP_S06_offer_ready_to_approved(self):
        """CAP-S06: OfferReady -> Approved; SUT Mobile App."""
        loan_id, _ = self.submit_happy("cap-s06")
        self.disburse_happy(loan_id)
        self.assert_transition(loan_id, "OfferReady", "Approved", MOBILE_APP)

    def test_CAP_S07_offer_ready_to_rejected_by_policy(self):
        """CAP-S07: OfferReady -> Rejected CON.1; SUT Decision Engine."""
        status, payload = self.handle(
            "POST",
            SUBMIT_PATH,
            self.submit_body("cap-s07", policy_mode="reject"),
        )
        self.assert_error(status, payload, 422, "CON.1", "Rejected")
        loan_id = next(iter(self.app.loan_application_service.applications))
        self.assert_transition(loan_id, "OfferReady", "Rejected", DECISION_ENGINE)

    def test_CAP_S08_offer_ready_to_rejected_by_customer_decline(self):
        """CAP-S08: OfferReady -> Rejected on decline; SUT Mobile App."""
        loan_id, _ = self.submit_happy("cap-s08")
        with self.subTest(SUT=MOBILE_APP):
            self.assertTrue(
                hasattr(self.app.mobile_app, "decline_loan_offer"),
                "Mobile App must invoke the owner without adding a fourth public route.",
            )
            result = self.app.mobile_app.decline_loan_offer(loan_id)
            if isinstance(result, dict) and "state" in result:
                self.assertEqual(result["state"], "Rejected")
            self.assertEqual(self.application_state(loan_id), "Rejected")
            self.assert_transition(loan_id, "OfferReady", "Rejected", MOBILE_APP)

    def test_CAP_S09_approved_to_account_validated(self):
        """CAP-S09: Approved -> AccountValidated; SUT Account Validation Service."""
        loan_id, _ = self.submit_happy("cap-s09")
        self.disburse_happy(loan_id)
        self.assert_transition(
            loan_id,
            "Approved",
            "AccountValidated",
            ACCOUNT_VALIDATION_SERVICE,
        )

    def test_CAP_S10_approved_to_failed(self):
        """CAP-S10: Approved -> Failed CON.4; SUT Account Validation Service."""
        loan_id, _ = self.submit_happy("cap-s10")
        status, payload = self.handle(
            "POST",
            DISBURSE_TEMPLATE.replace("{loanApplicationId}", loan_id),
            {"account_eligible": False, "posting_mode": "success"},
        )
        self.assert_error(status, payload, 422, "CON.4", "Failed")
        self.assert_transition(
            loan_id,
            "Approved",
            "Failed",
            ACCOUNT_VALIDATION_SERVICE,
        )

    def test_CAP_S11_account_validated_to_disbursed(self):
        """CAP-S11: AccountValidated -> Disbursed; SUT Disbursement Adapter."""
        loan_id, _ = self.submit_happy("cap-s11")
        self.disburse_happy(loan_id)
        self.assert_transition(
            loan_id,
            "AccountValidated",
            "Disbursed",
            DISBURSEMENT_ADAPTER,
        )

    def test_CAP_S12_account_validated_to_failed(self):
        """CAP-S12: AccountValidated -> Failed CON.4; SUT Disbursement Adapter."""
        loan_id, _ = self.submit_happy("cap-s12")
        status, payload = self.handle(
            "POST",
            DISBURSE_TEMPLATE.replace("{loanApplicationId}", loan_id),
            {"account_eligible": True, "posting_mode": "failure"},
        )
        self.assert_error(status, payload, 502, "CON.4", "Failed")
        self.assert_transition(
            loan_id,
            "AccountValidated",
            "Failed",
            DISBURSEMENT_ADAPTER,
        )


class TestHardRulesAndOwnership(CapstoneRuntimeTestCase):
    def test_CAP_N01_approval_without_prerequisites_is_impossible(self):
        """CAP-N01: approval cannot skip eligibility, scoring, policy, or max."""
        for operation in TRANSITION_OPERATIONS:
            self.assertFalse(
                hasattr(self.app.loan_application_service, operation),
                "Low-level positive transition must not be a public container command: "
                + operation,
            )
        attempts = (
            (LOAN_APPLICATION_SERVICE, {"existing_customer": False}, 422, "CON.2"),
            (CREDIT_SCORING_ADAPTER, {"scoring_mode": "timeout"}, 503, "CON.3"),
            (DECISION_ENGINE, {"policy_mode": "reject"}, 422, "CON.1"),
            (POLICY_ENGINE, {"requested_amount": 100_000_001}, 422, "CON.1"),
        )
        for index, (sut, overrides, expected_status, constraint) in enumerate(attempts):
            app = create_application()
            with self.subTest(SUT=sut, prerequisite=constraint):
                status, payload = self.handle(
                    "POST",
                    SUBMIT_PATH,
                    self.submit_body("cap-n01-{}".format(index), **overrides),
                    app=app,
                )
                self.assertEqual(status, expected_status, payload)
                self.assertEqual(payload["error"]["constraint"], constraint)
                self.assertNotIn(payload["error"]["state"], {"Approved", "Disbursed"})

    def test_CAP_N02_disbursement_before_approved_is_rejected(self):
        """CAP-N02: disbursement rejects missing approval or wrong lifecycle purpose."""
        before = self.downstream_snapshot()
        with self.subTest(SUT=ACCOUNT_VALIDATION_SERVICE):
            status, payload = self.handle(
                "POST",
                DISBURSE_TEMPLATE.replace("{loanApplicationId}", "cap-n02-not-approved"),
                {"account_eligible": True, "posting_mode": "success"},
            )
            self.assert_error(status, payload, 422, "CON.4", None)
            self.assertEqual(self.downstream_snapshot(), before)

        customer_id = "cap-n02-limit-increase"
        status, recommendation = self.handle(
            "POST",
            RECOMMEND_TEMPLATE.replace("{customerId}", customer_id),
            self.recommend_body(customer_id),
        )
        self.assertEqual(status, 200, recommendation)
        recommendation_id = recommendation["loan_application_id"]
        before_recommend_disburse = self.downstream_snapshot()
        scoring_before = self.app.credit_scoring_system.call_count
        with self.subTest(
            SUT=ACCOUNT_VALIDATION_SERVICE,
            attempt="limit-increase-purpose",
        ):
            status, payload = self.handle(
                "POST",
                DISBURSE_TEMPLATE.replace(
                    "{loanApplicationId}", recommendation_id
                ),
                {"account_eligible": True, "posting_mode": "success"},
            )
            self.assert_error(status, payload, 422, "CON.4", "OfferReady")
            self.assertEqual(
                self.application_state(recommendation_id), "OfferReady"
            )
            self.assertEqual(
                self.downstream_snapshot(), before_recommend_disburse
            )
            self.assertEqual(
                self.app.credit_scoring_system.call_count, scoring_before
            )

    def test_CAP_N03_disbursement_before_account_validated_is_rejected(self):
        """CAP-N03: I-11 disburse cannot pass failed account validation."""
        loan_id, _ = self.submit_happy("cap-n03")
        before = self.downstream_snapshot()
        with self.subTest(SUT=DISBURSEMENT_ADAPTER):
            status, payload = self.handle(
                "POST",
                DISBURSE_TEMPLATE.replace("{loanApplicationId}", loan_id),
                {"account_eligible": False, "posting_mode": "success"},
            )
            self.assert_error(status, payload, 422, "CON.4", "Failed")
            self.assertEqual(self.downstream_snapshot(), before)

    def test_CAP_N04_amount_above_100m_is_rejected(self):
        """CAP-N04: amount greater than 100,000,000 VND cannot be approved."""
        with self.subTest(SUT=POLICY_ENGINE):
            status, payload = self.handle(
                "POST",
                SUBMIT_PATH,
                self.submit_body("cap-n04", requested_amount=100_000_001),
            )
            self.assert_error(status, payload, 422, "CON.1", "Rejected")
            self.assertFalse(self.app.decision_store.loan_offers)

    def test_CAP_N05_mobile_app_credit_evaluation_attempt_is_rejected(self):
        """CAP-N05: forbidden Mobile App credit evaluation is rejected."""
        forbidden_path = "/mobile-app:credit-evaluate"
        scoring_before = self.call_total(self.app.fakes["Credit Scoring System"])
        with self.subTest(SUT=MOBILE_APP):
            self.assertNotIn(forbidden_path, self.app.route_registry)
            status, _ = self.handle(
                "POST",
                forbidden_path,
                {"customer_id": "cap-n05"},
            )
            self.assertIn(status, {403, 404})
            self.assertEqual(
                self.call_total(self.app.fakes["Credit Scoring System"]),
                scoring_before,
            )

    def test_CAP_N06_mobile_app_to_core_banking_is_rejected_and_fake_untouched(self):
        """CAP-N06: forbidden Mobile App -> Core Banking call is rejected."""
        forbidden_path = "/core-banking:post-from-mobile-app"
        core = self.app.fakes["Core Banking"]
        before = self.call_total(core)
        with self.subTest(SUT=MOBILE_APP):
            self.assertNotIn(forbidden_path, self.app.route_registry)
            status, _ = self.handle(
                "POST",
                forbidden_path,
                {"loan_application_id": "cap-n06"},
            )
            self.assertIn(status, {403, 404})
            self.assertEqual(self.call_total(core), before)

    def test_CAP_N07_unauthorized_CON5_is_audited_without_state_change(self):
        """CAP-N07: unauthorized CON.5 is denied, audited, and state-safe."""
        loan_id, _ = self.submit_happy("cap-n07")
        before_state = self.application_state(loan_id)
        before_downstream = self.downstream_snapshot()
        for rejected_value in ("false", "TRUE", True):
            with self.subTest(
                SUT=LOAN_APPLICATION_SERVICE,
                simulated_authorized=rejected_value,
            ):
                status, payload = self.handle(
                    "POST",
                    DISBURSE_TEMPLATE.replace("{loanApplicationId}", loan_id),
                    {"account_eligible": True, "posting_mode": "success"},
                    headers={"X-Simulated-Authorized": rejected_value},
                )
                self.assert_error(status, payload, 403, "CON.5", before_state)
                self.assertEqual(self.application_state(loan_id), before_state)
                self.assertEqual(self.downstream_snapshot(), before_downstream)
        self.assert_audit_contains("CON.5", "access-denied")

    def test_CAP_N08_I7_owner_returns_defensive_application_view(self):
        """CAP-N08: only Loan Application Service can mutate Loan Application."""
        loan_id, _ = self.submit_happy("cap-n08")
        with self.subTest(SUT=LOAN_APPLICATION_SERVICE):
            owned = self.app.loan_application_service._applications[loan_id]
            self.assertIsInstance(owned, LoanApplication)
            self.assertFalse(hasattr(owned, "transition"))
            exposed = self.application_record(loan_id)
            try:
                if isinstance(exposed, dict):
                    exposed["state"] = "Disbursed"
                else:
                    exposed.state = "Disbursed"
            except (AttributeError, TypeError, ValueError):
                pass
            self.assertEqual(self.application_state(loan_id), "OfferReady")
            self.assertFalse(hasattr(self.app.decision_store, "applications"))

    def test_CAP_N09_C02_rejects_forged_validation_and_amount(self):
        """CAP-N09: C-02 rejects forged ownership/state/amount before ESB/Core."""
        valid_amount = 50_000_000
        before = self.downstream_snapshot()
        with self.subTest(SUT=DISBURSEMENT_ADAPTER, attempt="nonexistent-id"):
            status, payload = self.handle(
                "POST",
                C02_PATH,
                {
                    "loan_application_id": "cap-n09-nonexistent",
                    "account_validated": True,
                    "amount": valid_amount,
                    "posting_mode": "success",
                },
            )
            self.assert_error(status, payload, 502, "CON.4", None)
            self.assertEqual(self.downstream_snapshot(), before)

        loan_id, approved_amount = self._create_account_validated_application(
            "cap-n09-real",
            valid_amount,
        )
        before_mismatch = self.downstream_snapshot()
        with self.subTest(SUT=DISBURSEMENT_ADAPTER, attempt="amount-mismatch"):
            status, payload = self.handle(
                "POST",
                C02_PATH,
                {
                    "loan_application_id": loan_id,
                    "account_validated": True,
                    "amount": approved_amount - 1,
                    "posting_mode": "success",
                },
            )
            self.assert_error(
                status,
                payload,
                502,
                "CON.4",
                "AccountValidated",
            )
            self.assertEqual(self.downstream_snapshot(), before_mismatch)

    def test_CAP_N10_C03_rejects_without_pending_C02_or_wrong_state(self):
        """CAP-N10: C-03 rejects no-pending/wrong-state attempts before Core."""
        loan_id, amount = self._create_account_validated_application("cap-n10-ready")
        core = self.app.fakes["Core Banking"]
        before_core = self.call_total(core)
        before_esb = self.call_total(self.app.fakes["ESB Integration Layer"])
        with self.subTest(SUT=DISBURSEMENT_ADAPTER, attempt="no-pending-C02"):
            status, payload = self.handle(
                "POST",
                C03_PATH,
                {
                    "loan_application_id": loan_id,
                    "account_validated": True,
                    "amount": amount,
                    "posting_mode": "success",
                },
            )
            self.assert_error(
                status,
                payload,
                502,
                "CON.4",
                "AccountValidated",
            )
            self.assertEqual(self.call_total(core), before_core)
            self.assertEqual(
                self.call_total(self.app.fakes["ESB Integration Layer"]),
                before_esb,
            )

        offer_ready_id, _ = self.submit_happy("cap-n10-wrong-state")
        before_wrong_state = self.downstream_snapshot()
        with self.subTest(SUT=DISBURSEMENT_ADAPTER, attempt="wrong-state"):
            status, payload = self.handle(
                "POST",
                C03_PATH,
                {
                    "loan_application_id": offer_ready_id,
                    "account_validated": True,
                    "amount": 50_000_000,
                    "posting_mode": "success",
                },
            )
            self.assert_error(status, payload, 502, "CON.4", "OfferReady")
            self.assertEqual(self.downstream_snapshot(), before_wrong_state)


class TestDirectContracts(CapstoneRuntimeTestCase):
    def test_CAP_C01_get_credit_score_contract(self):
        """CAP-C01: direct Get Credit Score is C-01 HTTPS/Sync."""
        with self.subTest(SUT=CREDIT_SCORING_ADAPTER):
            status, payload = self.handle(
                "POST",
                C01_PATH,
                {"customer_id": "cap-c01", "scoring_mode": "success"},
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(set(payload), {"customer_id", "credit_score"})
            self.assertEqual(payload["customer_id"], "cap-c01")
            self.assertIsInstance(payload["credit_score"], (int, float))

    def test_CAP_C02_disbursement_and_accounting_request_contract(self):
        """CAP-C02: direct C-02 request is accepted asynchronously."""
        loan_id, amount = self._create_account_validated_application("cap-c02")
        with self.subTest(SUT=DISBURSEMENT_ADAPTER):
            status, payload = self.handle(
                "POST",
                C02_PATH,
                {
                    "loan_application_id": loan_id,
                    "account_validated": True,
                    "amount": amount,
                    "posting_mode": "success",
                },
            )
            self.assertEqual(status, 202, payload)
            self.assertEqual(
                set(payload),
                {"message_id", "loan_application_id", "status"},
            )
            self.assertEqual(payload["loan_application_id"], loan_id)
            self.assertEqual(payload["status"], "accepted")
            self.assertGreater(
                self.app.fakes["ESB Integration Layer"].enqueue_count,
                0,
            )

    def test_CAP_C03_post_disbursement_and_accounting_contract(self):
        """CAP-C03: direct C-03 posting is confirmed asynchronously."""
        loan_id, amount = self._create_account_validated_application("cap-c03")
        with self.subTest(SUT=DISBURSEMENT_ADAPTER):
            request_status, request_payload = self.handle(
                "POST",
                C02_PATH,
                {
                    "loan_application_id": loan_id,
                    "account_validated": True,
                    "amount": amount,
                    "posting_mode": "success",
                },
            )
            self.assertEqual(request_status, 202, request_payload)
            status, payload = self.handle(
                "POST",
                C03_PATH,
                {
                    "loan_application_id": loan_id,
                    "account_validated": True,
                    "amount": amount,
                    "posting_mode": "success",
                },
            )
            self.assertEqual(status, 202, payload)
            self.assertEqual(
                set(payload),
                {
                    "message_id",
                    "loan_application_id",
                    "status",
                    "disbursement_record_reference",
                },
            )
            self.assertEqual(payload["loan_application_id"], loan_id)
            self.assertEqual(payload["status"], "confirmed")
            self.assertTrue(payload["disbursement_record_reference"])
            self.assertGreater(self.app.fakes["Core Banking"].post_count, 0)


class TestOpenAPIParity(CapstoneRuntimeTestCase):
    @staticmethod
    def resolve_parameter(spec, parameter):
        if "$ref" not in parameter:
            return parameter
        prefix = "#/components/parameters/"
        reference = parameter["$ref"]
        if not reference.startswith(prefix):
            raise AssertionError("Unsupported parameter reference: {}".format(reference))
        return spec["components"]["parameters"][reference[len(prefix) :]]

    def test_CAP_OAS_01_exact_six_operations_and_runtime_parity(self):
        """CAP-OAS-01: exact six OpenAPI operations equal route_registry."""
        openapi_path = RUNTIME_ROOT / "openapi.json"
        self.assertTrue(openapi_path.is_file(), openapi_path)
        with openapi_path.open("r", encoding="utf-8") as stream:
            spec = json.load(stream)

        self.assertEqual(spec["openapi"], "3.0.3")
        self.assertEqual(set(spec["paths"]), set(OPENAPI_OPERATIONS))
        self.assertEqual(set(self.app.route_registry), set(OPENAPI_OPERATIONS))

        for path, expected in OPENAPI_OPERATIONS.items():
            with self.subTest(path=path, operationId=expected["operationId"]):
                path_item = spec["paths"][path]
                methods = {
                    key.lower()
                    for key in path_item
                    if key.lower()
                    in {"get", "put", "post", "delete", "patch", "head", "options", "trace"}
                }
                self.assertEqual(methods, {"post"})
                operation = path_item["post"]
                self.assertEqual(operation["operationId"], expected["operationId"])
                self.assertEqual(operation["summary"], expected["modelOperation"])
                self.assertEqual(
                    operation["x-model-operation"],
                    expected["modelOperation"],
                )
                self.assertEqual(set(operation["responses"]), expected["statuses"])

                parameters = list(path_item.get("parameters", [])) + list(
                    operation.get("parameters", [])
                )
                resolved = [self.resolve_parameter(spec, item) for item in parameters]
                self.assertTrue(
                    any(
                        item.get("name") == "X-Simulated-Authorized"
                        and item.get("in") == "header"
                        and item.get("required") is True
                        for item in resolved
                    ),
                    "{} must require X-Simulated-Authorized".format(path),
                )

                route = self.app.route_registry[path]
                self.assertEqual(route["method"].upper(), "POST")
                self.assertEqual(route["path"], path)
                self.assertEqual(route["operationId"], expected["operationId"])
                runtime_statuses = {
                    str(value)
                    for value in route.get("successStatuses", [])
                    + route.get("errorStatuses", [])
                }
                self.assertEqual(runtime_statuses, expected["statuses"])

                request_schema_ref = operation["requestBody"]["content"][
                    "application/json"
                ]["schema"]["$ref"]
                schema_name = request_schema_ref.rsplit("/", 1)[-1]
                request_schema = spec["components"]["schemas"][schema_name]
                runtime_contract = REQUEST_CONTRACTS[path]
                self.assertIs(request_schema["additionalProperties"], False)
                self.assertEqual(
                    set(request_schema["required"]),
                    set(runtime_contract["required"]),
                )
                self.assertEqual(
                    set(request_schema["properties"]),
                    set(runtime_contract["fields"]),
                )
                for field_name, (field_kind, allowed, _, _) in runtime_contract[
                    "fields"
                ].items():
                    field_schema = request_schema["properties"][field_name]
                    expected_type = {
                        "string": "string",
                        "boolean": "boolean",
                        "integer": "integer",
                        "positive_integer": "integer",
                        "enum": "string",
                    }[field_kind]
                    self.assertEqual(field_schema["type"], expected_type)
                    if field_kind == "positive_integer":
                        self.assertEqual(field_schema["minimum"], 1)
                    if field_kind == "enum":
                        self.assertEqual(set(field_schema["enum"]), set(allowed))

        missing_modes = self.submit_body("cap-oas-missing")
        del missing_modes["scoring_mode"]
        del missing_modes["policy_mode"]
        status, payload = self.handle("POST", SUBMIT_PATH, missing_modes)
        self.assert_error(status, payload, 503, "CON.3", None)

        status, payload = self.handle("POST", C01_PATH, {})
        self.assert_error(status, payload, 503, "CON.3", None)

        status, payload = self.handle(
            "POST",
            C01_PATH,
            {
                "customer_id": "cap-oas-extra",
                "scoring_mode": "not-in-openapi",
                "unexpected": True,
            },
        )
        self.assert_error(status, payload, 503, "CON.3", None)


class TestSimulatedExternalsAndPerformance(CapstoneRuntimeTestCase):
    def test_CAP_I3_01_only_named_fakes_and_no_live_network(self):
        """CAP-I3-01: exact I-3 fakes serve the slice without live network."""
        self.assertEqual(set(self.app.fakes), I3_FAKES)
        original_connect = socket.socket.connect
        del original_connect  # Keep the patch target explicit and lint-clean.
        with mock.patch.object(
            socket.socket,
            "connect",
            side_effect=AssertionError("A live network call is forbidden"),
        ):
            loan_id, _ = self.submit_happy("cap-i3-01")
            self.disburse_happy(loan_id)
        for name in I3_FAKES:
            with self.subTest(fake=name):
                self.assertGreater(self.call_total(self.app.fakes[name]), 0)

    def test_CAP_P95_01_deterministic_decision_batch_within_30_seconds(self):
        """CAP-P95-01: deterministic standard decisions have P95 <= 30 seconds."""
        app = create_application()
        durations = []
        batch_size = 100
        for index in range(batch_size):
            started = time.perf_counter()
            status, payload = self.handle(
                "POST",
                SUBMIT_PATH,
                self.submit_body("cap-p95-{:03d}".format(index)),
                app=app,
            )
            durations.append(time.perf_counter() - started)
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload["state"], "OfferReady")

        durations.sort()
        p95_index = int(math.ceil(0.95 * batch_size)) - 1
        p95_seconds = durations[p95_index]
        self.assertLessEqual(
            p95_seconds,
            30.0,
            "Measured deterministic P95 was {:.6f}s".format(p95_seconds),
        )


if __name__ == "__main__":
    unittest.main()
