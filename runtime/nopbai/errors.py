"""Controlled errors shared by the in-process runtime."""


class ConstraintViolation(Exception):
    def __init__(self, constraint, reason, state=None, status=422):
        super().__init__(reason)
        self.constraint = constraint
        self.reason = reason
        self.state = state
        self.status = status

    def body(self):
        return {
            "error": {
                "constraint": self.constraint,
                "reason": self.reason,
                "state": self.state,
            }
        }

