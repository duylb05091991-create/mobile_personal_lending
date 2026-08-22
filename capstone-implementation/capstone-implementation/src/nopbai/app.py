"""FastAPI application for the Nopbai Personal Loan Platform.

The served OpenAPI at /openapi.json is generated from the routes, so the public
contract (G4) always matches the running API. `create_app()` builds a fresh
platform graph per app instance for clean tests.
"""
from __future__ import annotations

from fastapi import FastAPI

from . import names as N
from .api.routes import create_router
from .platform import Platform, build_platform


def create_app(platform: Platform | None = None) -> FastAPI:
    platform = platform or build_platform()
    app = FastAPI(
        title=f"{N.SYSTEM_IN_FOCUS} API",
        version="1.0.0",
        description=(
            f"Public contract for {N.PRODUCT}. Realizes the three I-11 use cases "
            "(Submit and Decide Loan Application, Disburse Approved Loan Application, "
            "Recommend Limit Increase) and documents the in-scope Lab 3 contract "
            "rows C-01/C-02/C-03 as simulated I-3 backing services."
        ),
    )
    app.state.platform = platform
    app.include_router(create_router(platform))
    return app


# Module-level app for `uvicorn nopbai.app:app`.
app = create_app()
