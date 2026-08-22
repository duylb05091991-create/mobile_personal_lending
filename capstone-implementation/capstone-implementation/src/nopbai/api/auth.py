"""CON.5 access guard.

CON.5 requires authenticated and authorized access to protected customer data and
decision evidence. This is a minimal principal check (a required authenticated
caller header) - it does NOT introduce an IAM product or a new container, per the
"do not invent" principle and the Lab 9 open point that the exact AuthN mechanism
is governed by CON.5 and not expanded into a product.
"""
from __future__ import annotations

from fastapi import Header, HTTPException

from .. import names as N
from .schemas import ErrorBody


async def require_principal(x_customer_id: str | None = Header(default=None)) -> str:
    """Return the authenticated customer principal, or 401 (CON.5)."""
    if not x_customer_id:
        raise HTTPException(
            status_code=401,
            detail=ErrorBody(
                error_code=N.CON_5,
                state=None,
                detail="Unauthenticated access to protected decisioning is denied (CON.5)",
            ).model_dump(),
        )
    return x_customer_id
