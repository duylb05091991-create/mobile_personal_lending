"""Shared pytest fixtures. Each test gets a fresh platform graph (in-memory)."""
import warnings

import pytest
from fastapi.testclient import TestClient

from nopbai.app import create_app
from nopbai.platform import build_platform

warnings.filterwarnings("ignore")  # silence starlette/httpx deprecation noise


@pytest.fixture()
def platform():
    return build_platform()


@pytest.fixture()
def app(platform):
    return create_app(platform)


@pytest.fixture()
def client(app):
    return TestClient(app)


@pytest.fixture()
def auth():
    """CON.5 authenticated principal header."""
    return {"X-Customer-Id": "CUST-001"}
