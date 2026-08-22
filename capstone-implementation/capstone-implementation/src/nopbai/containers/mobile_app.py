"""Mobile App (I-4 container).

Captures applications, displays Loan Offers and decisions, collects agreement
acceptance. I-9 forbidden path: Mobile App must NOT perform credit evaluation and
must NOT write directly to Core Banking. This class therefore holds a reference
ONLY to Loan Application Service; it has no handle to Credit Scoring Adapter,
Credit Scoring System, ESB Integration Layer, or Core Banking. The absence of
those collaborators is the structural guarantee (see test_hard_rules.py).
"""
from __future__ import annotations

from .. import names as N
from .loan_application_service import (
    DisburseResult,
    LoanApplicationService,
    RecommendResult,
    SubmitResult,
)


class MobileApp:
    NAME = N.MOBILE_APP

    def __init__(self, loan_application_service: LoanApplicationService):
        # Mobile App only knows Loan Application Service. No scoring, no Core Banking.
        self._las = loan_application_service

    def submit_application(self, **payload) -> SubmitResult:
        return self._las.submit_and_decide(**payload)

    def accept_agreement(self, application_id: str):
        return self._las.accept_agreement(application_id)

    def decline_offer(self, application_id: str):
        return self._las.decline_offer(application_id)

    def request_disbursement(self, application_id: str, *, posting_fails: bool = False) -> DisburseResult:
        return self._las.disburse(application_id, posting_fails=posting_fails)

    def request_limit_increase(self, **payload) -> RecommendResult:
        return self._las.recommend_limit_increase(**payload)
