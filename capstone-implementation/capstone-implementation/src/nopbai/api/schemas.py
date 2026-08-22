"""API request/response schemas.

The `ErrorBody` is the single error shape returned for every named `alt` / CON.*.
Because FastAPI generates the OpenAPI from these models, the served contract and
the runtime status/body cannot drift (G4 / OpenAPI standard).
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class SubmitApplicationRequest(BaseModel):
    customer_id: str = Field(..., examples=["CUST-001"])
    requested_amount_vnd: int = Field(..., examples=[50_000_000])
    customer_age: int = Field(..., examples=[30])
    is_existing_salaried: bool = Field(..., examples=[True])
    payment_account_id: str = Field(..., examples=["ACC-001"])
    # Simulation-only switch to exercise the CON.3 scoring-timeout alt.
    simulate_scoring_timeout: bool = Field(default=False)


class LimitIncreaseRequest(BaseModel):
    customer_id: str = Field(..., examples=["CUST-001"])
    requested_amount_vnd: int = Field(..., examples=[80_000_000])
    customer_age: int = Field(..., examples=[30])
    is_existing_salaried: bool = Field(..., examples=[True])


class DisbursementRequest(BaseModel):
    # Simulation-only switch to exercise the CON.4 posting-failure alt.
    simulate_posting_failure: bool = Field(default=False)


class LoanOfferResponse(BaseModel):
    loan_offer_id: str
    application_id: str
    amount_vnd: int
    interest_rate: float
    kind: str


class SubmitApplicationResponse(BaseModel):
    application_id: str
    state: str
    loan_offer: LoanOfferResponse


class ApplicationStateResponse(BaseModel):
    application_id: str
    state: str


class DisbursementResponse(BaseModel):
    application_id: str
    state: str
    disbursement_reference: str


class LimitIncreaseResponse(BaseModel):
    recommendation_id: str
    loan_offer: LoanOfferResponse


class ErrorBody(BaseModel):
    """Stable error body for every named alt / CON.*. `error_code` is the CON.* id."""

    error_code: str = Field(..., examples=["CON.1"])
    state: str | None = Field(default=None, examples=["Rejected"])
    detail: str = Field(..., examples=["amount cap / policy rejection (CON.1)"])


# --- backing-service (mocked I-3) contract schemas: C-01, C-02, C-03 ---------
class CreditScoreRequest(BaseModel):
    customer_id: str


class CreditScoreResponse(BaseModel):
    customer_id: str
    credit_score: int


class DisbursementAccountingRequest(BaseModel):
    application_id: str
    amount_vnd: int
    disbursement_reference: str
    simulate_posting_failure: bool = False


class DisbursementAccountingResponse(BaseModel):
    reference: str
    application_id: str
    amount_vnd: int
    confirmed: bool
