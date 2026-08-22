# Sign-off — Capstone I-11 runtime

Capstone RACI (`capstone.md`): **R** Dev · **A** SA · **C** Test. The runtime is
accepted only when it traces to OpenAPI + G6 and SA signs. AI-generated or
human-written code has **no authority** over a named view; if code and the after
pack disagree, SA fixes the after pack first, then Dev reties the spec-trace.

## Acceptance record

| RACI | Role | Name (Lab 7 roster) | Sign / date |
|------|------|---------------------|-------------|
| **R** | Dev | Nguyễn Thanh Hải (+ per-container Dev owners, Lab 3 build list) | ______________ |
| **A** | SA | Vũ Thế Quân | ______________ |
| **C** | Test | Lý Bá Duy | ______________ |

> The signature cells are left blank for the human accountable (SA) to sign.
> The structure and evidence below are what SA reviews before signing.

## Evidence SA accepts against

- **Spec-trace complete** — `SPEC_TRACE.md`: every in-scope path → OpenAPI
  operation → executed test id; no code off the trace.
- **G4 OpenAPI served + committed** — `openapi.yaml` is generated from the running
  app (`scripts/export_openapi.py`); `test_contract_openapi` asserts served ==
  committed and that each named alt / CON.* is documented with the runtime status.
- **G5 on named alts** — each I-11 `alt` runs the Lab 3 exception spec (trigger +
  compensating action + performer); tests assert the compensation *happens*
  (state change / no disbursement / reconciliation), not a bare 4xx.
- **G6 executes** — 39 automated tests run (not a checklist); SUT names are exact
  I-4 strings; all 12 I-6 transitions and all 7 drawn alts are covered.
- **G1–G3 still hold** — no new external, renamed container, or new state; names
  match Lab 1; sync/async preserved (see README "G1–G3 hold").

## Models-win divergence flagged for SA

Lab 9 §4.3 draws an `Account Validation Service → Core Banking` (HTTPS/Sync) edge;
the Lab 10 feedback correction **removed** it. The runtime follows the later
Lab 10 decision (no synchronous Core Banking edge in the disbursement slice; only
Disbursement Adapter enters the ESB/Core Banking async path). **Action for SA:**
reconcile Lab 9 with the Lab 10 correction in the after pack, then confirm the
spec-trace still ties. The code is not "fixed" unilaterally beyond following the
more recent after-pack decision.
