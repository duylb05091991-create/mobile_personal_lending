"""Audit Log (I-4 container).

Persists decision, integration, and transaction evidence for audit (CON.5).
In-memory (documented collapse). It retains references and evidence only; it is
NOT a second master for any I-7 object (e.g. Disbursement Record stays mastered
by Core Banking; Audit Log keeps the reference/evidence).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .. import names as N


@dataclass
class AuditEntry:
    actor: str          # which container/component wrote the evidence
    application_id: str
    event: str
    con: str | None = None
    at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AuditLog:
    NAME = N.AUDIT_LOG

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def append(self, actor: str, application_id: str, event: str, con: str | None = None) -> AuditEntry:
        entry = AuditEntry(actor=actor, application_id=application_id, event=event, con=con)
        self._entries.append(entry)
        return entry

    def entries_for(self, application_id: str) -> list[AuditEntry]:
        return [e for e in self._entries if e.application_id == application_id]

    def all(self) -> list[AuditEntry]:
        return list(self._entries)
