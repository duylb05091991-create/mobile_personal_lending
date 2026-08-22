"""Decision Store (I-4 container).

I-7 source of truth for `Loan Offer` and `Decision Record`. In-memory store
(documented collapse: one in-memory store, see NAME_IDENTITY_MAP.md). Only the
Decision Engine's `Decision Recorder` component writes here, so no two modules
master the same I-7 object.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from .. import names as N


@dataclass
class LoanOffer:
    """I-7: Loan Offer - proposed customer-facing terms. Mastered by Decision Store."""

    application_id: str
    amount_vnd: int
    interest_rate: float
    kind: str  # "standard" or "limit-increase"
    id: str = field(default_factory=lambda: f"OFFER-{uuid.uuid4().hex[:10]}")


@dataclass
class DecisionRecord:
    """I-7: Decision Record - score, policy basis, calculations, final decision;
    references the Loan Offer. Mastered by Decision Store."""

    application_id: str
    credit_score: int | None
    policy_basis: str
    decision: str            # "OfferReady" | "Rejected" | "Failed"
    con: str | None          # governing CON.* if any
    loan_offer_id: str | None
    id: str = field(default_factory=lambda: f"DR-{uuid.uuid4().hex[:10]}")


class DecisionStore:
    NAME = N.DECISION_STORE

    def __init__(self) -> None:
        self._offers: dict[str, LoanOffer] = {}
        self._records: dict[str, DecisionRecord] = {}

    def save_offer(self, offer: LoanOffer) -> LoanOffer:
        self._offers[offer.id] = offer
        return offer

    def save_record(self, record: DecisionRecord) -> DecisionRecord:
        self._records[record.id] = record
        return record

    def get_offer(self, offer_id: str) -> LoanOffer | None:
        return self._offers.get(offer_id)

    def records_for(self, application_id: str) -> list[DecisionRecord]:
        return [r for r in self._records.values() if r.application_id == application_id]
