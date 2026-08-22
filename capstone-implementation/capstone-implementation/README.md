# Nopbai Mobile Personal Loan — Capstone I-11 runtime

Team 4. This is the **implementation** of the three I-11 use cases from the
team's modeling packs (Lab 1 identity; Lab 3 contracts/exception/test spec; Lab 7
G1–G6/RACI; Lab 9 C4; Lab 10 audited sequences + G6 coverage). It is **not** a
modeling lab.

> **Location (capstone.md):** this folder is a **sibling of the modeling packs**,
> never inside the before pack, after pack, or Lab 7 file. Nothing here modifies
> `mobile_personal_lending-main/`.

## Source of truth

This team's Lab 1 Input and after pack (Labs 8–10), plus Lab 3 register/exception/
test spec and Lab 7 G1–G6. Not another team's topic, not the Day-3 SME brief.
Where Lab 1 leaves a value open, a simulated value is used and marked
`ASSUMPTION` in `NAME_IDENTITY_MAP.md`.

## The three I-11 use cases (with the alt named in I-11)

| Use case | Happy path | Named `alt` |
|----------|------------|-------------|
| Submit and Decide Loan Application | submit → segment gate → score → policy → Loan Offer | **CON.3** scoring timeout → Failed, no approval |
| Disburse Approved Loan Application | accept agreement → account validation → async disburse via ESB → Core Banking confirm | **CON.4** validation or posting/confirmation fails → Failed, no disbursement |
| Recommend Limit Increase | eligible existing customer → policy → limit-increase Loan Offer | **CON.2** out-of-segment → reject |

All three happy paths, all seven drawn alts (Lab 10 G6-A01…A07), and all twelve
I-6 transitions (G6-S01…S12) are implemented and tested.

## Run it

```bash
python -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) Automated tests (G6 executes — 39 tests)
pytest

# 2) Regenerate the served OpenAPI file (G4)
PYTHONPATH=src python scripts/export_openapi.py   # writes openapi.yaml

# 3) 10-minute demo: I-1 goal → I-11 sequence → live happy → live named alt → test report
PYTHONPATH=src python scripts/demo.py

# 4) Serve the live API (OpenAPI at http://127.0.0.1:8000/docs and /openapi.json)
PYTHONPATH=src uvicorn nopbai.app:app --reload
```

Every request needs an authenticated principal header (CON.5): `X-Customer-Id: CUST-001`.

## Architecture (one collapsed process)

Nine I-4 containers + the Decision Engine's six L3 components run as one process
with one in-memory store and in-process calls — a **documented collapse**
(`NAME_IDENTITY_MAP.md`). Each container keeps its exact Lab 1 name. The three I-3
externals (`Credit Scoring System`, `ESB Integration Layer`, `Core Banking`) are
**in-process fakes** (`MOCK_LIST.md`); no real host, no secret.

```
Customer ──(X-Customer-Id, CON.5)──> Mobile App ──> Loan Application Service ──> Decision Engine
                                        │                (I-7 Loan Application)      ├─ Score Coordinator ─> Credit Scoring Adapter ─(C-01)─> Credit Scoring System*
                                        │                                            ├─ Policy Evaluation ─> Policy Engine (CON.1 cap, I-7 Policy Config)
                                        │                                            ├─ Offer Builder
                                        │                                            └─ Decision Recorder ─> Decision Store (I-7 Loan Offer/Decision Record) + Audit Log
                                        └──> Account Validation Service ──> Disbursement Adapter ─(C-02)─> ESB Integration Layer* ─(C-03)─> Core Banking*
                                                                                                 (* = mocked I-3, loopback only)
```

## How this maps to the four scoring lenses

- **Architecture (25%)** — realizes the after pack, not a new landscape. No new
  external/container/state; collapse documented; I-3 mocked; product names not
  used. See `NAME_IDENTITY_MAP.md`.
- **Design (25%)** — G4 OpenAPI served + committed (`openapi.yaml`), one operation
  per in-scope path incl. C-01/C-02/C-03; spec-trace complete (`SPEC_TRACE.md`);
  OOP (Loan Application is a type; transitions are its operations); domain-driven
  (CON.*/I-5 in I-7 owners); G5 specified per named alt.
- **Code quality (20%)** — one spelling per thing (`src/nopbai/names.py`); name
  map incl. collapse/ASSUMPTION rows; no out-of-scope path callable; no secrets;
  implementation outside the modeling packs; SA sign-off record (`SIGNOFF.md`).
- **Test coverage (30%)** — 39 tests execute G6; SUTs are I-4 names; I-5 skip and
  I-9 forbidden path are **attempted and rejected**; CON.* alts asserted against
  the OpenAPI status/body; I-3 mocked in tests.

## G1–G6 on the runtime

- **G1/G2/G3 still hold** — goal/outcome/CON.* true of the runtime; process and
  the nine I-6 states match; C4 names, I-3 externals, and sync/async unchanged.
- **G4** — OpenAPI is the served + committed public contract; generated from the
  app, so it cannot drift.
- **G5** — each named alt runs the Lab 3 exception spec: trigger + compensating
  action + performer; tests assert the compensation happens.
- **G6** — automated tests run; every transition and drawn alt is covered.

## Known model divergence (flagged, not silently "fixed")

Lab 9 draws an `Account Validation Service → Core Banking` HTTPS edge; the Lab 10
feedback correction removed it. The runtime follows the later Lab 10 decision and
flags this for SA to reconcile in the after pack (`SIGNOFF.md`).

## Files

```
README.md  NAME_IDENTITY_MAP.md  SPEC_TRACE.md  MOCK_LIST.md  SCOPE_NA.md  SIGNOFF.md
openapi.yaml  requirements.txt  pyproject.toml
src/nopbai/…   (names, domain, containers, external, api, app, platform)
tests/…        (uc1, uc2, uc3, state_machine, hard_rules, con5_auth, contract_openapi)
scripts/…      (export_openapi.py, demo.py)
```
