# Team 4 — Lab 1 feedback

**To:** Nguyễn Cương Quyết (TN), Vũ Thế Quân, Lý Bá Duy, Nguyễn Thanh Hải, Nguyễn Minh Hoàng  
**Repo:** https://github.com/duylb05091991-create/mobile_personal_lending · `main` @ `e76f5c6` · `list.md` Input I-1–I-11  
**Rubric:** `Labs/list.md` — Lab 1 (I-1–I-11)  
**Verdict: Fail — not Done. Do not treat Lab 2 (or any later lab) as started until this index is locked.**

Lab 1 is the name-identity index. Every later view may use **only** these strings. Empty cells are not allowed. Names must not collide. In-scope and out-of-scope must not overlap.

---

## What is already good

The topic is usable: a mobile unsecured personal loan for existing salaried customers (age 22–35), auto decision, personalized limit/rate, immediate disbursement, accounting via an integration layer. `Requirement_Document.md` already has a readable in/out split (no secured/SME, no branch onboarding, no manual underwriting on the standard path) and a 100,000,000 VND cap.

Keep that product story. Put it into I-1–I-11 **once**, with one spelling per name, then stop. Do not keep drawing ArchiMate / C4 / gates until the index is Done.

---

## Fail if — must fix before Lab 2

### 1. I-1–I-11 is empty

`list.md` is the bound form. The Input tables are still blank: Group, system-in-focus, I-2–I-11 cells, I-6 object, CON.1–CON.3, I-11 use cases, and the one I-11 container. The submit checklist Lab 1 row is unchecked.

Lab 1 Done when: *every Input field is filled; names do not collide; in/out do not overlap.* Empty cells are not allowed.

**Fix:** fill I-1–I-11 in `list.md` (or a dedicated Lab 1 file that is the only name-identity index). Invent simulated values and mark `ASSUMPTION` where you lack a number. Do not leave “the system”, “SLA TBD”, or “BA to define CON.*”.

### 2. Later labs started before this index is complete

Git on `main` is **one** commit:

| Commit | When | What landed |
|--------|------|-------------|
| `e76f5c6` | 21 Aug 14:11 | Blank `list.md` Input **and** Domain / Requirement / Analysis, ArchiMate views with header + RACI, C4 Context, custom quality-gate files, `templates/`, and `puml/` (including another topic’s DTB samples). |

Lab 1 Fail-if: *any later lab started before this index is complete.* Pack fail: Lab 7 before Labs 1–6 archived; Guide / header / RACI applied on Labs 1–6.

Same sitting already has:

- Lab 2-shaped files (`Requirement_Document.md`, `Analysis.md`) that map to the Guide and propose a **G1–G6** register
- Lab 7-shaped custom gates (`Quality-Gates-Architecture.md` AG-*, `Quality-Gates-Design.md` DG-*) — not G1–G6 as written, and too early
- Lab 8 ArchiMate (`Motivation-Strategy.md`, `Business-Process.md`, `Application-Architecture.md`, `Technology-Architecture.md`, `Organization-Product.md`) with diagram headers and RACI
- Lab 9 C4 Context (`C4-Context.md`, `puml/nopbai-c4-context.puml`)

**Fix:** freeze Lab 1. Treat those files as accidental early drafts, not as Done. Remove G1–G6 from the Lab 2 sitting (gates are Lab 7). Do not continue those sittings until Lab 1 is Done.

### 3. Vague system and forked identity (no index to lock them)

Fail-if: *vague system (“the new app”)*. Without I-1, downstream files already disagree on the system-in-focus and on runnable names:

| You wrote | Where |
|-----------|--------|
| `Nopbai Personal Loan Platform` | C4 Context |
| `Mobile Loan Platform` | Quality-Gates-Architecture A1 |
| `Mobile Personal Loan Product` | Motivation / Technology titles |
| `Mobile Personal Loan` | Organization-Product |
| `Sản phẩm cho vay cho khách hàng cá nhân trên Mobile App` | Domain.md (not English) |
| `Loan Application Service` vs `Loan Service` | Application Architecture vs Business Process / Organization |
| `Decision Store` vs `Loan Decision Store` | Application Architecture vs Quality-Gates A2 |
| `Account Validation` vs `Account Validation Service` | Quality-Gates vs Business Process |
| `accounting adapter` vs `Disbursement Adapter` | Analysis / Quality-Gates A2 vs Application Architecture |

**Fix:** pick **one** English string per thing in I-1 / I-4. Copy that string everywhere. Domain.md must be English.

### 4. Process steps name containers that are not in the index

I-5 and later process tables already name `Mobile App`, `Loan Service`, `Scoring Adapter`, `Policy Engine`, `Decision Engine`, `ESB / Core Banking`, `Audit Log / Decision Store`. I-4 is empty, so none of those are listed containers.

Fail-if: *process steps that name containers not listed*.

**Fix:** list every runnable name in I-4 first. I-5 steps and I-11 happy paths use **only** I-2 + I-3 + I-4 strings.

### 5. Two masters for the same thing

Fail-if: *two masters for one data object* — here also two homes for the same **system**.

- **ESB Integration Layer** is an I-3 external on C4 Context **and** an internal application component / C4 container on Application Architecture and Technology. Pick one: external **or** I-4 container, not both.
- **Core Banking** is a Business Actor, an External System, and an Application Component. Keep it in I-3 only (simulated name).
- **Credit Scoring System** is a Business Actor and an External System. I-2 is people. Keep it in I-3 only.
- Analysis tells you to “design all external integrations (Credit Scoring, Core Banking, ESB) as explicit C4 Containers.” Externals stay I-3. Adapters that **you** build are I-4 (`Credit Scoring Adapter`, `Disbursement Adapter`). Do not promote the external itself to a container.

---

## Should fix (Done when: names do not collide; in/out do not overlap)

1. **I-1 Group.** Use Team 4 and the five names above. Do not keep “Nopbai” as the product identity unless you lock that exact string in I-1.
2. **I-2 is people.** `Customer` stays. `Bank`, `Core Banking`, `Credit Scoring System`, `Loan Operations` as systems do not. Internal ops/risk as a Person is fine if they have a role on an exception path you actually keep.
3. **I-6 worksheet.** Restore columns State / Trigger / Next / Terminal?. One object (likely `LoanApplication` — not a container). Quality-Gates-Design already invents `Submitted`, `Scoring`, `OfferReady`, `Approved`, `Rejected`, `Disbursed`, `Failed`, `Reviewed`. Those strings only exist after you publish them in I-6. Every machine needs at least one terminal.
4. **CON.\* in I-10, not only MOT.CON.** Motivation already has MOT.CON.01–04 (cap, segment, scoring latency, security). Copy them into I-10 as `CON.1`… with an **effect on the process**. Add a CON for “no disbursement before approval and account validation” if that is a hard rule.
5. **Measurable outcome.** “Near real-time” is not I-1 Outcome. Pick a simulated number (e.g. decision P95 ≤ Ns) and mark `ASSUMPTION`.
6. **I-11.** Name a few use cases (submit + score + decide; disburse + post), each with one `alt` that cites a CON.*. Circle **one** I-4 container for optional C4 Component.
7. **I-8 / I-9.** Sync vs async examples; locations; one forbidden path (channel must not write Core Banking / ledger). Product names (Kafka, Kong, …) are labels later — not I-4 identity strings.
8. **Wrong-topic samples.** `puml/dtb-*.puml` and `templates/20-appendix.md` still talk VCB / NAPAS / Daily Transaction Banking. That is another brief and uses production-style names. Do not treat them as this team’s Lab 1 index.
9. **English only.** Domain.md title and scope narrative must match the filled I-1 strings.

I-1 in-scope / out-of-scope in `Requirement_Document.md` is close. After you fill I-1, in-scope containers must use the **same** I-4 strings.

---

## Lab 2 starts only when

- every I-1–I-11 cell is filled with **one** spelling per name
- I-2 is people; I-3 is simulated externals; I-4 is your containers; no duplicated names
- I-5 and I-11 participants ⊆ I-2 + I-3 + I-4
- I-6 has one named object, trigger/next/terminal columns, and at least one terminal
- CON.1–CON.n live in I-10
- G1–G6, diagram header, and RACI are **not** in the Lab 1–6 files (those are Lab 7+)
- ArchiMate / C4 / custom AG-DG checklists are not being treated as Done in parallel

Reply on the repo when Lab 1 is re-locked. Then Lab 2: requirements in **current language**, **no** G1–G6.
