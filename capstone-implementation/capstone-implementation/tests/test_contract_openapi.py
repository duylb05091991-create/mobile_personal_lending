"""G4 / OpenAPI: the served contract has exactly the in-scope operations, every
named alt / CON.* is a documented error response with the same status the runtime
returns, and the committed openapi.yaml matches the served spec (no drift, no
extra operations).
"""
import pathlib

import yaml

# operationId -> the (in-scope path) it traces to
PLATFORM_OPS = {
    "submitAndDecideLoanApplication",   # UC1
    "acceptLoanAgreement",              # UC2 (OfferReady->Approved)
    "declineLoanOffer",                 # UC1 (OfferReady->Rejected)
    "disburseApprovedLoanApplication",  # UC2
    "recommendLimitIncrease",           # UC3
}
BACKING_OPS = {
    "getCreditScore",                   # C-01
    "sendDisbursementAndAccounting",    # C-02
    "postDisbursementAndAccounting",    # C-03
}
ALL_OPS = PLATFORM_OPS | BACKING_OPS


def _operation_ids(spec) -> set[str]:
    ids = set()
    for methods in spec["paths"].values():
        for op in methods.values():
            if isinstance(op, dict) and "operationId" in op:
                ids.add(op["operationId"])
    return ids


def _op_by_id(spec, op_id):
    for methods in spec["paths"].values():
        for op in methods.values():
            if isinstance(op, dict) and op.get("operationId") == op_id:
                return op
    raise KeyError(op_id)


def test_served_spec_has_exactly_the_in_scope_operations(app):
    ids = _operation_ids(app.openapi())
    assert ids == ALL_OPS, f"unexpected/missing operations: {ids ^ ALL_OPS}"


def test_named_alts_documented_with_runtime_status(app):
    spec = app.openapi()
    # UC1: CON.2/CON.1 -> 422, CON.3 -> 503, CON.5 -> 401
    uc1 = _op_by_id(spec, "submitAndDecideLoanApplication")["responses"]
    assert {"201", "422", "503", "401"} <= set(uc1)
    # UC2: CON.4 validation -> 422, CON.4 posting -> 502, CON.5 -> 401
    uc2 = _op_by_id(spec, "disburseApprovedLoanApplication")["responses"]
    assert {"200", "422", "502", "401"} <= set(uc2)
    # UC3: CON.2/CON.1 -> 422, CON.5 -> 401
    uc3 = _op_by_id(spec, "recommendLimitIncrease")["responses"]
    assert {"201", "422", "401"} <= set(uc3)


def test_backing_contracts_document_forbidden_path(app):
    spec = app.openapi()
    for op_id in BACKING_OPS:
        assert "403" in _op_by_id(spec, op_id)["responses"]


def test_committed_openapi_matches_served(app):
    committed_path = pathlib.Path(__file__).resolve().parents[1] / "openapi.yaml"
    assert committed_path.exists(), "run scripts/export_openapi.py to generate openapi.yaml"
    committed = yaml.safe_load(committed_path.read_text())
    assert committed == app.openapi(), "committed openapi.yaml drifted from the served spec"
