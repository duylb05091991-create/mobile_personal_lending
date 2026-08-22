# Team 4 — Capstone feedback (pass 2)

**Official score:** [`capstone-scoring.md`](capstone-scoring.md)  
**To:** Nguyễn Cương Quyết (TN), Vũ Thế Quân, Lý Bá Duy, Nguyễn Thanh Hải, Nguyễn Minh Hoàng  
**Repo:** https://github.com/duylb05091991-create/mobile_personal_lending · `main` @ `f2d4b18` · `runtime/`  
**Rubric:** `Labs/capstone.md` · scoring `Labs/rubrics/capstone-scoring.md`  
**Lab 10:** Pass (`9ed974d`) · Labs 1–10 not edited this sitting  
**Prior:** `117f813` · `capstone-implementation/capstone-implementation/` · **7.8 / 10** · Sitting Done, not pass  
**RACI:** Dev **R** Nguyễn Thanh Hải · SA **A** Vũ Thế Quân · Test **C** Lý Bá Duy  
**This commit:** `f2d4b18` *Capstone project v2* — author **`ly duy <duylb05091991@gmail.com>`** (Test **C**, not Dev **R**, not SA **A**)  
**Suite:** `python3 -m unittest discover -s tests -p 'test_*.py'` in `runtime/` — **38/38 pass**, 0.006s  
**Verdict: Sitting Done. No automatic fail. Weighted total 8.25 / 10. Not pass.**

This sitting is **implement what you designed**. Source of truth is **this team’s** Lab 1 index and after pack (Labs 8–10), plus Lab 3 register / exception / test spec and Lab 7 G1–G6. I-11 only. Models win.

**Done ≠ pass.** Pass / follow-on is **≥ 9.0 / 10**. This HEAD does not meet that bar.

The scored tree is **`runtime/`**. The old FastAPI tree at `capstone-implementation/` is leftover, not this sitting. Labs 1–10 were not restyled. Independent re-run: **38/38**.

---

## What you fixed (vs `117f813`)

| Must-fix (pass 1) | Now (`f2d4b18` `runtime/`) |
|-------------------|----------------------------|
| #1 Lab 10 coupling | **Closed.** `Mobile App` holds `Account Validation Service`. AVS → DA. No AVS → Core Banking. UC3 calls `Decision Engine.recommend_offer` with **no** Credit Scoring Adapter / C-01 (`ASSUMPTION-08`) |
| #3 G6-S through SUT | **Partial.** `CAP-S01…S12` run on HTTP (or Mobile App methods) and assert LAS history pairs. The `SUT=` argument is a `subTest` label only — it does not check which I-4 performed the write. `Scoring → OfferReady` is still LAS `_mark_offer_ready`, labelled Decision Engine |
| #4 I-5 on HTTP | **Closed.** `CAP-N02` `POST …:disburse` on a missing id → `422 CON.4`. Limit-increase `OfferReady` cannot auto-approve → `422 CON.4`, ESB untouched |
| #5 EX-05 evidence | **Closed.** `CAP-N07` → `403 CON.5` and Audit Log `access-denied` |
| #6 Pack hygiene | **Partial.** New sibling `runtime/` is flat and runs. Nested FastAPI tree, repo-root `capstone.md` / `capstone-scoring.md`, and moved `list.md` are still there. `Eligibility Evaluator` is now called |
| #2 C8 / D9 SA sign | **Not closed.** `SA-ACCEPTANCE.md` is `ACCEPTED` for Vũ Thế Quân, date 2026-08-22, **accepted commit “Not provided”**, evidence = *“Explicit user confirmation in this Codex thread: `SA đã ký`”*. Same Test **C** commit ticked every box |

They also copied the instructor pass-1 file into `feedback/team4_capstone_feedback.md`. Leftover. Not Output.

**Regression:** pass-1 I-9 posted the **real** C-01 / C-03 routes with `X-Caller: Mobile App` → 403. This sitting’s `CAP-N05` / `CAP-N06` POST invented paths (`/mobile-app:credit-evaluate`, `/core-banking:post-from-mobile-app`) and accept 404. Public `POST /integration/credit-scoring:get-credit-score` has **no caller guard**.

---

## Automatic fail

None ticked. Same twelve clauses. C8 is a lens row, not a Fail-if tick. A Codex “`SA đã ký`” recorded by Test **C** is not a fabricated git author (that was Team 5). It is also not a signature-only accept from SA.

| Tick | Fail if | Hit? |
|------|---------|------|
| [ ] | Lab 10 not Done | No |
| [ ] | Forked or invented names | No — Lab 1 strings; `ASSUMPTION-01…08` |
| [ ] | Missing I-11 use case or named `alt` | No |
| [ ] | Real I-3 or production credentials | No — `CAP-I3-01` patches sockets |
| [ ] | OpenAPI missing or drifted from runtime | No — `CAP-OAS-01` vs `openapi.json` |
| [ ] | Extra I-4 / I-6 / product as a new identity | No |
| [ ] | Extra deployable without collapse | No on `runtime/`. **Smell:** leftover FastAPI tree still claims to be a runtime |
| [ ] | I-5 / I-9 violation possible (no attempt) | No — attempts exist. **Smell:** I-9 is 404 on invented URLs; C-01 is callable without being CSA |
| [ ] | I-7 ownership shared or moved | No — snapshots; LAS owns transitions |
| [ ] | Domain rules outside I-7 owner | No — CON.1 in Policy Engine; CON.2 in LAS |
| [ ] | Code not on the spec-trace | No for the six ops |
| [ ] | Implementation inside modeling packs | No — `runtime/` is a sibling |

---

## Bound form / pack contents

| File that counts | Result |
|------------------|--------|
| Runnable I-11 | Pass — stdlib `python3 -m nopbai` on `:8080`. Six POST ops |
| OpenAPI | Pass — committed `openapi.json` 3.0.3; `CAP-OAS-01` parity |
| Automated tests | Pass — 38 executed here (`CAP-I11-*`, `CAP-A*`, `CAP-S*`, `CAP-N*`, `CAP-C*`, `CAP-OAS-01`, `CAP-I3-01`, `CAP-P95-01`) |
| Name-identity map | Pass — nine I-4, four I-9 locations (including customer mobile device), Lab 9 coupling table, `ASSUMPTION-08` |
| Spec-trace | Pass — path → `operationId` → test id |
| I-3 mock list | Pass — three fakes; queue + counters |
| Collapse mapped | Pass — one process / in-memory / in-process bus |

Leftover, not Output: `capstone-implementation/` (entire pass-1 tree); repo-root `capstone.md`, `capstone-scoring.md`; `capstone-implementation/list.md`; `feedback/team4_capstone_feedback.md`.

---

## I-11 (copy Lab 1 strings)

| Use case (Lab 1) | Happy | Named `alt` | G5 |
|------------------|-------|-------------|----|
| Submit and Decide Loan Application | Pass — `200`, `OfferReady`, `Loan Offer` in Decision Store | Pass — **CON.3** `503` / `Failed` (`CAP-A02`). Also CON.2 / CON.1 | Pass — CSA + DE; no approval; audit retained |
| Disburse Approved Loan Application | Pass — `200`, `Disbursed`, Core Banking reference | Pass — **CON.4** validation `422` / posting `502` | Pass — AVS sends nothing; DA reconciles. **Smell:** public `disburse` also performs agreement accept when state is `OfferReady` |
| Recommend Limit Increase | Pass — existing `Loan Offer`; no Recommendation type | Pass — **CON.2** `422` before DE. Also CON.1 | Pass — LAS before DE; no C-01 |

I-1 in-scope that is not I-11, listed N/A in `SPEC-TRACE.md`: Loan Ops workflow, decline as a fourth route, secured/SME/branch/manual, live I-3, products/cluster.

---

## Architecture — 25% (9 / 10)

Was 8. A3 / A5 / A7 / A8 / A9 moved.

| # | Mark | Comment |
|---|------|---------|
| A1 | P | CON.1–CON.5 true |
| A2 | Ptl | Nine states, twelve transitions recorded. One submit POST still lands `OfferReady`. Accept is not a public op — it is folded into `:disburse` |
| A3 | **P** | Lab 10: `Mobile App → AVS`, `AVS → DA`. No AVS → Core Banking |
| A4 | P | One process documented |
| A5 | **P** | Coupling = name-map Lab 9 table. UC3 has no CSA edge |
| A6 | P | `runtime/` is one process |
| A7 | **P** | Device / lending runtime / evidence store / external zone all have rows |
| A8 | **P** | Six L3 names inside Decision Engine; `Eligibility Evaluator` is called |
| A9 | **P** | Collapse, not a second landscape. Old FastAPI folder is leftover, not a second score |
| A10 | P | Three fakes. No cluster |

Deduct: mid-states / accept still collapse in one handler.

---

## Design — 25% (8 / 10)

Was 8. D6 moved a little; D9 did not.

| # | Mark | Comment |
|---|------|---------|
| D1 | P | Three use cases, happy + named `alt`, seven Lab 10 alts |
| D2 | P | Exactly six POST operations |
| D3 | P | Stable `{constraint, reason, state}` body; 422 / 503 / 502 / 403 |
| D4 | P | `SPEC-TRACE.md` 1:1 |
| D5 | P | N/A table. Decline is `CAP-S08`, not a fourth route |
| D6 | Ptl | Typed aggregate; LAS is the only live owner. G6-S SUT labels are not proven |
| D7 | P | Lab 1 language. CON.* in I-7 owners |
| D8 | P | Each `CAP-A*` asserts compensate, not status alone |
| D9 | Ptl | Spec is Labs 1–10 + OpenAPI + G6. Human **A** is a chat line in a Test **C** file. `Accepted commit: Not provided` |

---

## Code quality — 20% (8 / 10)

Was 7. C3 / C6 moved.

| # | Mark | Comment |
|---|------|---------|
| C1 | P | `identities.py` one spelling |
| C2 | P | Collapse + eight `ASSUMPTION` rows, including device and UC3-without-C-01 |
| C3 | **P** | L3 used. AVS / DA / Mobile App have one reason each. LAS remains the I-7 writer |
| C4 | P | Six ops; unknown path 404 |
| C5 | P | No secret, no host. `NOPBAI_HOST` / `NOPBAI_PORT` are bind only |
| C6 | Ptl | `runtime/` is outside packs. Pass-1 tree + instructor brief + this feedback copy remain |
| C7 | P | Six routes on the trace |
| C8 | Ptl | `SA-ACCEPTANCE.md` checked by the builder. No Quân git identity. No commit hash |

---

## Test coverage — 30% (8 / 10)

Was 8. T3 closed. T4 got worse.

| Use case | Happy-path test | `alt` test | G5 | SUT = I-4 |
|----------|-----------------|------------|----|-----------|
| Submit and Decide Loan Application | `CAP-I11-01` | `CAP-A01…A03` | Pass | HTTP. G6-S labels only |
| Disburse Approved Loan Application | `CAP-I11-02` | `CAP-A04` / `CAP-A05` | Pass — no ESB / reconciliation | HTTP. Accept is inside the same POST |
| Recommend Limit Increase | `CAP-I11-03` | `CAP-A06` / `CAP-A07` | Pass — no offer on reject; no C-01 | HTTP |

| # | Mark | Comment |
|---|------|---------|
| T1 | Ptl | 38 run. G6-A via HTTP. G6-S via history pairs after a collapsed call |
| T2 | Ptl | `subTest(SUT=…)` does not assert the named module wrote the transition |
| T3 | **P** | `CAP-N01` / `CAP-N02` / `CAP-N03` / `CAP-N04` on the wire |
| T4 | Ptl | Invented-path 404. Real C-01 is open. Do **not** demo `CAP-N05` / `CAP-N06` as I-9 |
| T5 | P | CON.* envelope asserted |
| T6 | P | Fakes; socket patched in `CAP-I3-01` |

**Do not demo** `CAP-N05` or `CAP-N06`. Demo CON.3, CON.4 posting, CON.2 recommend, and `CAP-N07`.

---

## Principles — evidence only

| Principle | Mark | Feeds |
|-----------|------|--------|
| Models win | **Pass** — Lab 10 AVS edges and UC3-without-score now match the runtime. Packs were not rewritten | Architecture / Design |
| Do not invent | Pass — `ASSUMPTION-08` covers UC3 lifecycle reuse | Architecture / Code |
| Hard rules impossible | **Partial** — I-5 on HTTP. I-9 is 404 theater | Test |
| Before pack is archive | Pass — Labs 1–10 untouched | Code |
| One sitting, one slice | **Partial** — `runtime/` is the slice. Pass-1 folder is still a second claimed runtime | Design / Code |
| Human A accepts | **Partial** — Codex line, not SA identity | Design / Code |

---

## Demo (10 min) — not observed live

`README.md` order is correct: I-1 goal → Lab 10 sequence → `python3 -m nopbai` happy submit → live CON.3 → 38/38.

| Tick | Observed |
|------|----------|
| [ ] | I-1 goal stated |
| [ ] | One I-11 sequence on screen (Lab 10 names) |
| [ ] | Live happy path |
| [ ] | Live named `alt` / CON.* |
| [ ] | Test report shown |

**Notes:** Script exists; not watched. Run from `runtime/`. Do not start the old FastAPI tree. Do not treat repo-root `capstone-scoring.md` as this score.

---

## Done when

| Rule | Result |
|------|--------|
| All Output rows present | Pass |
| G1–G3 still hold on the after pack | **Pass** on Lab 10 strings and AVS edges. G2 mid-states still collapse |
| G4–G6 pass **on the runtime** | Pass as executed tests. G6-S grain is history, not SUT |
| Human **A** accepts | Partial |

**Weighted total: 8.25 / 10.** Architecture 9 × 0.25 = 2.25 · Design 8 × 0.25 = 2.00 · Code quality 8 × 0.20 = 1.60 · Test coverage 8 × 0.30 = 2.40. Was 7.80.

---

## Close this sitting (remaining, not a new landscape)

1. **I-9 (T4).** Attempt the **real** C-01 / C-03 operations as Mobile App (or any non-CSA / non-ESB caller). Runtime rejects; fake call count unchanged. Delete `/mobile-app:credit-evaluate` and `/core-banking:post-from-mobile-app` as evidence.
2. **C8 / D9.** Dev **R** (Nguyễn Thanh Hải) lands remaining code. SA **A** (Vũ Thế Quân) signs in a **signature-only** commit from a distinct identity, with the accepted hash filled. A Codex `SA đã ký` is not that. Test **C** does not accept.
3. **G6-S SUT.** `assert_transition` must prove the named I-4 performed the step (call count / actor on the audit row), not only that LAS history contains the pair.
4. **One sitting.** Delete or archive `capstone-implementation/`. Restore `list.md` to repo root or `labs/`. Delete instructor `capstone.md` / `capstone-scoring.md` and `feedback/team4_capstone_feedback.md` from the trainee tree.
5. **Optional.** If SA wants accept as a visible I-6 step, add it on the after pack first; do not invent a seventh public route without that.

Do not restyle Labs 1–10. Do not invent a second landscape. Do not treat this file as a pack artifact if it is copied into the repo again.

---

# Pass 1 record (superseded)

**HEAD then:** `117f813` · `capstone-implementation/capstone-implementation/`  
**Suite then:** `pytest` **39/39**  
**Verdict then: Sitting Done. 7.8 / 10. Not pass.**

Honest FastAPI collapse. I-9 was a real caller-guard 403. Failures: Lab 10 `Mobile App → AVS` / `AVS → DA` not coded; UC3 called CSA; G6-S on the aggregate only; I-5 disbursement skip not on HTTP; EX-05 wrote no audit; nested folder; blank `SIGNOFF.md`; Test **C** authored the sitting.
