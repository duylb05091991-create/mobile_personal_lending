"""HTTP routes for the Nopbai Personal Loan Platform.

Two groups of operations, all in one served OpenAPI (G4):
  * Platform operations that realize the three I-11 use cases (public contract).
  * The three in-scope Lab 3 contract rows C-01/C-02/C-03, served as the
    simulated I-3 backing-service contracts (loopback only, no real host, no
    secret). The adapters use the same in-process fakes, so served contract and
    runtime behavior share one implementation and cannot drift.

Every named alt / CON.* maps to a fixed status code + ErrorBody so the document
and the runtime match exactly.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Path

from .. import names as N
from ..domain.errors import ForbiddenPathError
from ..platform import Platform
from .auth import require_principal
from .schemas import (
    ApplicationStateResponse,
    CreditScoreRequest,
    CreditScoreResponse,
    DisbursementAccountingRequest,
    DisbursementAccountingResponse,
    DisbursementRequest,
    DisbursementResponse,
    ErrorBody,
    LimitIncreaseRequest,
    LimitIncreaseResponse,
    LoanOfferResponse,
    SubmitApplicationRequest,
    SubmitApplicationResponse,
)

# Fixed status codes for each CON.* alt (documented == runtime).
STATUS_FOR_CON = {
    N.CON_1: 422,  # amount cap / policy rejection
    N.CON_2: 422,  # out-of-segment rejection
    N.CON_3: 503,   # scoring timeout (controlled)
}
# CON.4 has two documented failures: validation (422) vs posting/confirmation (502).
CON4_VALIDATION_STATUS = 422
CON4_POSTING_STATUS = 502


def _error(con: str, state: str | None, detail: str, http_status: int) -> HTTPException:
    return HTTPException(
        status_code=http_status,
        detail=ErrorBody(error_code=con, state=state, detail=detail or con).model_dump(),
    )


def _offer_response(offer) -> LoanOfferResponse:
    return LoanOfferResponse(
        loan_offer_id=offer.id,
        application_id=offer.application_id,
        amount_vnd=offer.amount_vnd,
        interest_rate=offer.interest_rate,
        kind=offer.kind,
    )


def create_router(platform: Platform) -> APIRouter:
    router = APIRouter()

    # =====================================================================
    # UC1 - Submit and Decide Loan Application
    #   named alt (I-11): CON.3 scoring timeout -> Failed, no approval
    #   also in-scope: CON.2 out-of-segment, CON.1 amount cap
    # =====================================================================
    @router.post(
        "/loan-applications",
        tags=["Submit and Decide Loan Application"],
        operation_id="submitAndDecideLoanApplication",
        status_code=201,
        response_model=SubmitApplicationResponse,
        responses={
            422: {"model": ErrorBody, "description": "CON.2 out-of-segment or CON.1 amount cap"},
            503: {"model": ErrorBody, "description": "CON.3 scoring timeout (controlled)"},
            401: {"model": ErrorBody, "description": "CON.5 unauthenticated"},
        },
    )
    def submit_and_decide(
        body: SubmitApplicationRequest,
        principal: str = Depends(require_principal),
    ) -> SubmitApplicationResponse:
        result = platform.mobile_app.submit_application(
            customer_id=body.customer_id,
            requested_amount_vnd=body.requested_amount_vnd,
            customer_age=body.customer_age,
            is_existing_salaried=body.is_existing_salaried,
            payment_account_id=body.payment_account_id,
            scoring_timeout=body.simulate_scoring_timeout,
        )
        if result.con in STATUS_FOR_CON:
            raise _error(result.con, result.state, result.reason or "", STATUS_FOR_CON[result.con])
        return SubmitApplicationResponse(
            application_id=result.application_id,
            state=result.state,
            loan_offer=_offer_response(result.loan_offer),
        )

    # OfferReady -> Approved (accept agreement)
    @router.post(
        "/loan-applications/{application_id}/agreement",
        tags=["Disburse Approved Loan Application"],
        operation_id="acceptLoanAgreement",
        response_model=ApplicationStateResponse,
        responses={401: {"model": ErrorBody}},
    )
    def accept_agreement(
        application_id: str = Path(...),
        principal: str = Depends(require_principal),
    ) -> ApplicationStateResponse:
        app = platform.mobile_app.accept_agreement(application_id)
        return ApplicationStateResponse(application_id=app.id, state=app.state)

    # OfferReady -> Rejected (customer declines)
    @router.post(
        "/loan-applications/{application_id}/decline",
        tags=["Submit and Decide Loan Application"],
        operation_id="declineLoanOffer",
        response_model=ApplicationStateResponse,
        responses={401: {"model": ErrorBody}},
    )
    def decline_offer(
        application_id: str = Path(...),
        principal: str = Depends(require_principal),
    ) -> ApplicationStateResponse:
        app = platform.mobile_app.decline_offer(application_id)
        return ApplicationStateResponse(application_id=app.id, state=app.state)

    # =====================================================================
    # UC2 - Disburse Approved Loan Application
    #   named alt (I-11): CON.4 validation or posting/confirmation failure
    # =====================================================================
    @router.post(
        "/loan-applications/{application_id}/disbursement",
        tags=["Disburse Approved Loan Application"],
        operation_id="disburseApprovedLoanApplication",
        response_model=DisbursementResponse,
        responses={
            422: {"model": ErrorBody, "description": "CON.4 account validation failed"},
            502: {"model": ErrorBody, "description": "CON.4 posting/confirmation failed"},
            401: {"model": ErrorBody, "description": "CON.5 unauthenticated"},
        },
    )
    def disburse(
        body: DisbursementRequest,
        application_id: str = Path(...),
        principal: str = Depends(require_principal),
    ) -> DisbursementResponse:
        result = platform.mobile_app.request_disbursement(
            application_id, posting_fails=body.simulate_posting_failure
        )
        if result.con == N.CON_4 and result.state == N.FAILED and result.reference is None:
            # validation failure: no request was sent
            raise _error(N.CON_4, result.state, result.reason or "", CON4_VALIDATION_STATUS)
        if result.con == N.CON_4:
            # posting/confirmation failure: reconciliation queued
            raise _error(N.CON_4, result.state, result.reason or "", CON4_POSTING_STATUS)
        return DisbursementResponse(
            application_id=result.application_id,
            state=result.state,
            disbursement_reference=result.reference,
        )

    # =====================================================================
    # UC3 - Recommend Limit Increase
    #   named alt (I-11): CON.2 out-of-segment -> reject recommendation
    #   also in-scope: CON.1 amount cap
    # =====================================================================
    @router.post(
        "/limit-increase-recommendations",
        tags=["Recommend Limit Increase"],
        operation_id="recommendLimitIncrease",
        status_code=201,
        response_model=LimitIncreaseResponse,
        responses={
            422: {"model": ErrorBody, "description": "CON.2 out-of-segment or CON.1 amount cap"},
            401: {"model": ErrorBody, "description": "CON.5 unauthenticated"},
        },
    )
    def recommend_limit_increase(
        body: LimitIncreaseRequest,
        principal: str = Depends(require_principal),
    ) -> LimitIncreaseResponse:
        result = platform.mobile_app.request_limit_increase(
            customer_id=body.customer_id,
            requested_amount_vnd=body.requested_amount_vnd,
            customer_age=body.customer_age,
            is_existing_salaried=body.is_existing_salaried,
        )
        if result.con in (N.CON_2, N.CON_1):
            raise _error(result.con, None, result.reason or "", STATUS_FOR_CON[result.con])
        return LimitIncreaseResponse(
            recommendation_id=result.application_id,
            loan_offer=_offer_response(result.loan_offer),
        )

    # =====================================================================
    # Backing-service contracts (simulated I-3). Loopback only, no real host.
    # =====================================================================
    def _forbidden(exc: ForbiddenPathError) -> HTTPException:
        return HTTPException(
            status_code=403,
            detail=ErrorBody(error_code=exc.con or N.CON_5, state=None, detail=exc.message).model_dump(),
        )

    # C-01 Get Credit Score (Credit Scoring Adapter -> Credit Scoring System)
    @router.post(
        "/backing/credit-scoring-system/scores",
        tags=["C-01 backing: Credit Scoring System (mock)"],
        operation_id="getCreditScore",
        response_model=CreditScoreResponse,
        responses={
            403: {"model": ErrorBody, "description": "I-9 forbidden caller"},
            504: {"model": ErrorBody, "description": "CON.3 timeout/unavailable"},
        },
    )
    def c01_get_credit_score(
        body: CreditScoreRequest,
        x_caller: str = Header(..., description="Calling container (must be Credit Scoring Adapter)"),
    ) -> CreditScoreResponse:
        try:
            score = platform.credit_scoring_system.get_credit_score(body.customer_id, caller=x_caller)
        except ForbiddenPathError as exc:
            raise _forbidden(exc)
        return CreditScoreResponse(customer_id=body.customer_id, credit_score=score)

    # C-02 Disbursement and Accounting Request (Disbursement Adapter -> ESB)
    @router.post(
        "/backing/esb-integration-layer/disbursements",
        tags=["C-02 backing: ESB Integration Layer (mock)"],
        operation_id="sendDisbursementAndAccounting",
        response_model=DisbursementAccountingResponse,
        responses={403: {"model": ErrorBody, "description": "I-9 forbidden caller"}},
    )
    def c02_send_disbursement(
        body: DisbursementAccountingRequest,
        x_caller: str = Header(..., description="Calling container (must be Disbursement Adapter)"),
    ) -> DisbursementAccountingResponse:
        try:
            record = platform.esb_integration_layer.send_disbursement_and_accounting(
                body.application_id,
                body.amount_vnd,
                body.disbursement_reference,
                caller=x_caller,
                posting_fails=body.simulate_posting_failure,
            )
        except ForbiddenPathError as exc:
            raise _forbidden(exc)
        return DisbursementAccountingResponse(
            reference=record.reference,
            application_id=record.application_id,
            amount_vnd=record.amount_vnd,
            confirmed=record.confirmed,
        )

    # C-03 Post Disbursement and Accounting (ESB Integration Layer -> Core Banking)
    @router.post(
        "/backing/core-banking/postings",
        tags=["C-03 backing: Core Banking (mock)"],
        operation_id="postDisbursementAndAccounting",
        response_model=DisbursementAccountingResponse,
        responses={403: {"model": ErrorBody, "description": "I-9 forbidden caller (e.g. Mobile App direct)"}},
    )
    def c03_post_disbursement(
        body: DisbursementAccountingRequest,
        x_caller: str = Header(..., description="Calling container (must be ESB Integration Layer)"),
    ) -> DisbursementAccountingResponse:
        try:
            record = platform.core_banking.post_disbursement_and_accounting(
                body.application_id,
                body.amount_vnd,
                body.disbursement_reference,
                caller=x_caller,
                posting_fails=body.simulate_posting_failure,
            )
        except ForbiddenPathError as exc:
            raise _forbidden(exc)
        return DisbursementAccountingResponse(
            reference=record.reference,
            application_id=record.application_id,
            amount_vnd=record.amount_vnd,
            confirmed=record.confirmed,
        )

    return router
