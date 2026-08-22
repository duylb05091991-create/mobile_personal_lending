"""Audit Log evidence boundary."""

from copy import deepcopy

from .identities import AUDIT_LOG


class AuditLog:
    identity = AUDIT_LOG

    def __init__(self):
        self.events = []

    @property
    def call_count(self):
        return len(self.events)

    @property
    def calls(self):
        return self.events

    def append(self, source, event_type, subject_id=None, constraint=None, reason=None, details=None):
        event = {
            "sequence": len(self.events) + 1,
            "source": source,
            "event_type": event_type,
            "subject_id": subject_id,
            "constraint": constraint,
            "reason": reason,
            "details": deepcopy(details) if details is not None else {},
        }
        self.events.append(event)
        return deepcopy(event)

