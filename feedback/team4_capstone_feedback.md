# Team 4 — Capstone feedback (pass 1)

**Official score:** [`capstone-scoring.md`](capstone-scoring.md)  
**To:** Nguyễn Cương Quyết (TN), Vũ Thế Quân, Lý Bá Duy, Nguyễn Thanh Hải, Nguyễn Minh Hoàng  
**Repo:** https://github.com/duylb05091991-create/mobile_personal_lending · `main` @ `117f813` · `capstone-implementation/capstone-implementation/`  
**Rubric:** `Labs/capstone.md` · scoring `Labs/rubrics/capstone-scoring.md`  
**Lab 10:** Pass (`9ed974d`, re-review) · Labs 1–10 locked this sitting  
**Prior:** none (first sitting)  
**RACI:** Dev **R** Nguyễn Thanh Hải · SA **A** Vũ Thế Quân · Test **C** Lý Bá Duy  
**This commit:** `117f813` *Capstone project* — author **`ly duy <duylb05091991@gmail.com>`** (Test **C**, not Dev **R**)  
**Suite:** `PYTHONPATH=src pytest` in the inner folder — **39/39 pass**  
**Verdict: Sitting Done. No automatic fail. Weighted total 7.8 / 10. Not pass.**

This sitting is **implement what you designed**. Source of truth is **this team’s** Lab 1 index and after pack (Labs 8–10), plus Lab 3 register / exception / test spec and Lab 7 G1–G6. I-11 only. Models win.

**Done ≠ pass.** Output rows are present; G4–G6 execute; no Fail-if tick. Pass for any follow-on is **≥ 9.0 / 10**. This HEAD does not meet that bar.

HEAD `117f813` adds the runtime next to the packs. Labs 1–10 were not restyled to match the code. Independent re-run: **39/39**.

---

## What is already good

Honest one-process collapse. Nine I-4 names as modules; only **Decision Engine** is drilled to L3. I-6 is a type with twelve guarded transitions. I-7 owners are not shared. All three I-11 use cases run, including the `alt` named in I-11. G5 is a state/evidence change, not a bare 4xx. I-9 is an HTTP attempt with `X-Caller: Mobile App` → 403, plus a structural “Mobile App has only `_las`” check. G4 drift is tested (`served == committed`). They flagged the leftover Lab 9 `Account Validation Service → Core Banking` edge instead of silently rewriting the pack.

---

## Automatic fail

None ticked. Same twelve clauses. C8 is a lens row, not a Fail-if tick. Blank `SIGNOFF.md` is not a fabricated sign.

| Tick | Fail if | Hit? |
|------|---------|------|
| [ ] | Lab 10 not Done | No |
| [ ] | Forked or invented names | No — one spelling in `names.py`; `ASSUMPTION` rows exist |
| [ ] | Missing I-11 use case or named `alt` | No |
| [ ] | Real I-3 or production credentials | No |
| [ ] | OpenAPI missing or drifted from runtime | No — `test_committed_openapi_matches_served` |
| [ ] | Extra I-4 / I-6 / product as a new identity | No |
| [ ] | Extra deployable without collapse | No — one process, mapped |
| [ ] | I-5 / I-9 violation possible (no attempt) | No — attempts exist. **Smell:** I-5 disbursement skip is a service `IllegalTransition`, not HTTP |
| [ ] | I-7 ownership shared or moved | No |
| [ ] | Domain rules outside I-7 owner | No — CON.1 in `Policy Engine` |
| [ ] | Code not on the spec-trace | No for the eight public ops |
| [ ] | Implementation inside modeling packs | No — sibling folder. **Smell:** `list.md` was moved *into* this folder; instructor `capstone.md` / `capstone-scoring.md` sit at repo root |

---

## Bound form / pack contents

| File that counts | Result |
|------------------|--------|
| Runnable I-11 | Pass — FastAPI `nopbai.app:app`. **Smell:** runtime lives one directory deeper than the parent README |
| OpenAPI | Pass — served + committed; C-01 / C-02 / C-03 as `/backing/…` loopback |
| Automated tests | Pass — 39 executed here |
| Name-identity map | Pass — collapse + I-9 locations + `ASSUMPTION` |
| Spec-trace | Pass — path → `operationId` → pytest node |
| I-3 mock list | Pass — three in-process fakes; no host |
| Collapse mapped | Pass — one process / in-memory / in-process bus |

Leftover, not Output: repo-root `capstone.md`, `capstone-scoring.md`; parent-folder copies of README / name map / OpenAPI / spec-trace / `SIGNOFF.md`; `capstone-implementation/list.md` (was repo-root `list.md`).

---

## I-11 (copy Lab 1 strings)

| Use case (Lab 1) | Happy | Named `alt` | G5 |
|------------------|-------|-------------|----|
| Submit and Decide Loan Application | Pass — HTTP 201, `OfferReady`, `Loan Offer` in Decision Store | Pass — **CON.3** 503 / `Failed`. Also CON.2, CON.1, decline | Pass — who = Credit Scoring Adapter + Decision Engine; no approval |
| Disburse Approved Loan Application | Pass — accept → `Disbursed` + Core Banking reference | Pass — **CON.4** validation 422 / posting 502 | Pass — who = AVS (no DA send) / Disbursement Adapter (reconciliation queued). **Smell:** LAS writes the audit, not AVS / DA as Lab 10 draws |
| Recommend Limit Increase | Pass — limit-increase `Loan Offer` (no new Recommendation object) | Pass — **CON.2** 422. Also CON.1 | Pass — who = Loan Application Service before Decision Engine |

I-1 in-scope that is not I-11, listed N/A: auto approval/rejection, standalone Loan Offer, standalone account validation, standalone ESB posting, standalone Decision Store / Audit Log, segment onboarding as a use case. See `SCOPE_NA.md`.

---

## Architecture — 25% (8 / 10)

| # | Mark | Comment |
|---|------|---------|
| A1 | P | Goal / CON.1–CON.5 true of the runtime |
| A2 | Ptl | Nine I-6 states, twelve transitions. `Draft` / `Submitted` / `Scoring` are not HTTP-observable; one POST lands on `OfferReady` |
| A3 | Ptl | C4 names and I-3 strings match. Sync C-01 / async C-02–C-03 labelled. Lab 10 still draws `Mobile App → Account Validation Service` and `AVS → Disbursement Adapter`; runtime is `Mobile App → LAS → AVS`, then `LAS → DA`. Lab 9 `AVS → Core Banking` is flagged, not coded |
| A4 | P | One process documented |
| A5 | Ptl | Extra `LAS → Credit Scoring Adapter` on Recommend Limit Increase (Lab 10 canvas has no scoring). Disbursement orchestration sits on LAS, not the Lab 10 edges |
| A6 | P | No extra deployable |
| A7 | Ptl | Process → Lending application runtime; in-memory → Evidence data store; fakes → External banking integration zone. `Mobile App` I-9 location is still “customer mobile device” with no explicit device-collapse row |
| A8 | Ptl | L3 only inside Decision Engine. `Eligibility Evaluator` is constructed and never called |
| A9 | Ptl | Collapse, not a second landscape. Lab 10 coupling is not the runtime graph |
| A10 | P | Three I-3 fakes. No cluster. Product names unused |

Deduct: Lab 10 disbursement / UC3 edges; mid-state collapse; unused L3 box.

---

## Design — 25% (8 / 10)

| # | Mark | Comment |
|---|------|---------|
| D1 | P | Three use cases, happy + named `alt`, plus the seven Lab 10 drawn alts |
| D2 | P | G4 is OpenAPI. Five platform ops + three backing contracts |
| D3 | P | CON.2/CON.1 → 422; CON.3 → 503; CON.4 → 422/502; CON.5 → 401 |
| D4 | P | `SPEC_TRACE.md` 1:1 with pytest nodes |
| D5 | P | `SCOPE_NA.md`. No extra use case |
| D6 | Ptl | `LoanApplication` is a type; transitions are its operations. G6-S01…S12 prove the type, not the Lab 10 SUT |
| D7 | P | Lab 1 language. CON.1 in Policy Engine; CON.2 in LAS; Decision Store masters `Loan Offer` / `Decision Record` |
| D8 | P | Lab 3 exception spec named; runtime compensates |
| D9 | Ptl | Spec is Labs 1–10 + OpenAPI + G6. SA has not signed. Commit author is Test **C** |

---

## Code quality — 20% (7 / 10)

| # | Mark | Comment |
|---|------|---------|
| C1 | P | `names.py` is the single spelling |
| C2 | P | Collapse + `ASSUMPTION` (score payload, rate rule, payment-account flag, CON.5 header, CON.4 status split) |
| C3 | Ptl | One reason per I-4 on paper. LAS orchestrates UC2; `Eligibility Evaluator` is dead; UC3 scoring lives on LAS |
| C4 | P | Eight `operationId`s; drift test forbids extras |
| C5 | P | No secret, no real host |
| C6 | Ptl | Sibling of packs. Nested `capstone-implementation/capstone-implementation/`. Parent README’s `pytest` / `uvicorn` will fail. `list.md` moved here. Instructor brief copied to repo root |
| C7 | P | Routes sit on the spec-trace |
| C8 | Ptl | `SIGNOFF.md` is a blank template. No signature-only accept from Vũ Thế Quân |

---

## Test coverage — 30% (8 / 10)

| Use case | Happy-path test | `alt` test | G5 | SUT = I-4 |
|----------|-----------------|------------|----|-----------|
| Submit and Decide Loan Application | `test_T04_happy_path_offer_ready` | `test_T14_G6A02_…` CON.3; also T-13 / T-15 / T-08 | Pass — `Failed`, no `Approved` | HTTP. G6-S* are type-level |
| Disburse Approved Loan Application | `test_T11_happy_disbursement` | `test_T10_G6A04_…` / `test_T12_G6A05_…` | Pass — `Failed`; no DA send / reconciliation queued | HTTP. CON.4 validation mutates `._apps[…].payment_account_eligible` |
| Recommend Limit Increase | `test_happy_recommendation` | `test_T18_G6A06_…` / `test_T19_G6A07_…` | Pass — 422, no offer | HTTP |

| # | Mark | Comment |
|---|------|---------|
| T1 | Ptl | 39 run. G6-A01…A07 via HTTP. G6-S01…S12 on the aggregate |
| T2 | Ptl | UC files name Lab 10 SUTs in comments. State-machine tests do not use the participant = SUT map |
| T3 | Ptl | `test_I5_cannot_approve_before_scoring` is type-level. `test_I5_cannot_disburse_before_approval` calls `LAS.disburse()`; `POST …/disbursement` on `OfferReady` would be 500 |
| T4 | P | `test_I9_direct_mobile_app_to_core_banking_is_rejected`; `test_I9_mobile_app_cannot_perform_credit_evaluation`; fake rejects non-ESB caller |
| T5 | P | CON.* status + `error_code` asserted |
| T6 | P | In-process fakes |

**Do not demo** a disbursement call before agreement as I-5 evidence (it is not HTTP). Demo CON.3, CON.4 posting, CON.2 limit-increase, and the I-9 403.

Lab 3 EX-05 also asked for security evidence on Audit Log. `test_EX05_submit_requires_authentication` asserts no Decision Record; the 401 path writes nothing.

---

## Principles — evidence only

| Principle | Mark | Feeds |
|-----------|------|--------|
| Models win | **Partial** — they follow the later Lab 10 “no AVS → Core Banking” decision and flag Lab 9. They do **not** follow Lab 10 `Mobile App → AVS` / `AVS → DA`, and they add UC3 scoring the Lab 10 canvas does not draw | Architecture / Design |
| Do not invent | Pass — no extra I-4 / I-6 / product; `ASSUMPTION` used | Architecture / Code |
| Hard rules impossible | **Partial** — I-9 attempted. I-5 skip is not on the HTTP surface | Test |
| Before pack is archive | Pass — Labs 1–6 not restyled. `list.md` move is the leftover | Code |
| One sitting, one slice | Pass — N/A listed, not built | Design |
| Human A accepts | **Partial** — unsigned. Test **C** landed the sitting | Design / Code |

---

## Demo (10 min) — not observed live

`scripts/demo.py` is the right order: I-1 goal → Submit-and-Decide sequence → live happy submit/accept/disburse → live CON.3 / CON.4 / CON.2 → pytest.

Run it from the **inner** folder (`capstone-implementation/capstone-implementation/`), not the parent.

| Tick | Observed |
|------|----------|
| [ ] | I-1 goal stated |
| [ ] | One I-11 sequence on screen (Lab 10 names) |
| [ ] | Live happy path |
| [ ] | Live named `alt` / CON.* |
| [ ] | Test report shown |

**Notes:** Script exists; not watched in this review. Do not claim Lab 10 AVS edges from the live run. Do not treat repo-root `capstone-scoring.md` as this score.

---

## Done when

| Rule | Result |
|------|--------|
| All Output rows present | Pass |
| G1–G3 still hold on the after pack | **Partial** — names / externals / states hold. Lab 10 coupling does not |
| G4–G6 pass **on the runtime** | Pass as executed tests. G6-S grain is the type, not the Lab 10 SUT |
| Human **A** accepts | Partial — blank `SIGNOFF.md` |

**Weighted total: 7.80 / 10.** Architecture 8 × 0.25 = 2.00 · Design 8 × 0.25 = 2.00 · Code quality 7 × 0.20 = 1.40 · Test coverage 8 × 0.30 = 2.40.

---

## Close this sitting (remaining, not a new landscape)

1. **Models win (A3 / A5).** Either implement Lab 10 as drawn (`Mobile App → Account Validation Service`, `AVS → Disbursement Adapter`; Recommend Limit Increase with **no** Credit Scoring Adapter) **or** SA updates Lab 10 / Lab 9 first, then retie the spec-trace. Do not leave the pack and the runtime on different graphs.
2. **C8 / D9.** Dev **R** (Nguyễn Thanh Hải) lands remaining code. SA **A** (Vũ Thế Quân) signs in a **signature-only** commit or fills `SIGNOFF.md` from that identity. Test **C** does not accept.
3. **G6-S through the Lab 10 SUT.** Keep the type guards. Add (or move) G6-S01…S12 so the named I-4 performs the transition — at least via LAS / Decision Engine / AVS / Disbursement Adapter, not only `LoanApplication.to_*()`.
4. **I-5 on HTTP.** `POST /loan-applications/{id}/disbursement` before `Approved` must reject with a documented body (not 500). Attempt the skip on the wire.
5. **EX-05 evidence.** Unauthenticated call writes Audit Log (Lab 3: deny **and** retain security evidence).
6. **Pack hygiene.** Flatten the nested folder so parent README commands run. Restore `list.md` to repo root (or `labs/`). Delete instructor `capstone.md` / `capstone-scoring.md` from the trainee tree. Wire `Eligibility Evaluator` or drop it from the name map.

Do not restyle Labs 1–10 to match the code. Do not invent a second landscape. Do not treat this file as a pack artifact if it is copied into the repo.
