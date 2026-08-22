"""Composition root for the Nopbai Personal Loan Platform.

This is the ONE process (documented collapse - see NAME_IDENTITY_MAP.md). It
instantiates every I-4 container as a module object and the three I-3 mocked
backing services as in-process fakes, then wires them per the Lab 9 Container
relationships and Lab 3 contract register. No new container, product, or external
is introduced; the three external names remain simulated fakes.
"""
from __future__ import annotations

from dataclasses import dataclass

from .containers.account_validation_service import AccountValidationService
from .containers.audit_log import AuditLog
from .containers.credit_scoring_adapter import CreditScoringAdapter
from .containers.decision_engine.engine import DecisionEngine
from .containers.decision_store import DecisionStore
from .containers.disbursement_adapter import DisbursementAdapter
from .containers.loan_application_service import LoanApplicationService
from .containers.mobile_app import MobileApp
from .containers.policy_engine import PolicyEngine
from .external.core_banking import CoreBankingFake
from .external.credit_scoring_system import CreditScoringSystemFake
from .external.esb_integration_layer import EsbIntegrationLayerFake


@dataclass
class Platform:
    """Holds every wired container + mock so tests and the API share one graph."""

    # I-3 mocked backing services
    credit_scoring_system: CreditScoringSystemFake
    esb_integration_layer: EsbIntegrationLayerFake
    core_banking: CoreBankingFake
    # I-4 containers
    mobile_app: MobileApp
    loan_application_service: LoanApplicationService
    credit_scoring_adapter: CreditScoringAdapter
    decision_engine: DecisionEngine
    policy_engine: PolicyEngine
    account_validation_service: AccountValidationService
    disbursement_adapter: DisbursementAdapter
    decision_store: DecisionStore
    audit_log: AuditLog


def build_platform() -> Platform:
    # Evidence stores (in-memory collapse).
    decision_store = DecisionStore()
    audit_log = AuditLog()

    # I-3 mocks. Core Banking is the sole target of the ESB; ESB is the sole
    # sender's target; both enforce their I-9 caller guards.
    core_banking = CoreBankingFake()
    esb_integration_layer = EsbIntegrationLayerFake(core_banking)
    credit_scoring_system = CreditScoringSystemFake()

    # Adapters (isolate the two external contracts C-01, C-02/C-03).
    credit_scoring_adapter = CreditScoringAdapter(credit_scoring_system)
    disbursement_adapter = DisbursementAdapter(esb_integration_layer)

    # Policy + Decision Engine (with its six L3 components).
    policy_engine = PolicyEngine()
    decision_engine = DecisionEngine(
        credit_scoring_adapter, policy_engine, decision_store, audit_log
    )

    account_validation_service = AccountValidationService()

    # Loan Application Service owns the Loan Application lifecycle.
    loan_application_service = LoanApplicationService(
        decision_engine=decision_engine,
        account_validation_service=account_validation_service,
        disbursement_adapter=disbursement_adapter,
        credit_scoring_adapter=credit_scoring_adapter,
        decision_store=decision_store,
        audit_log=audit_log,
    )

    mobile_app = MobileApp(loan_application_service)

    return Platform(
        credit_scoring_system=credit_scoring_system,
        esb_integration_layer=esb_integration_layer,
        core_banking=core_banking,
        mobile_app=mobile_app,
        loan_application_service=loan_application_service,
        credit_scoring_adapter=credit_scoring_adapter,
        decision_engine=decision_engine,
        policy_engine=policy_engine,
        account_validation_service=account_validation_service,
        disbursement_adapter=disbursement_adapter,
        decision_store=decision_store,
        audit_log=audit_log,
    )
