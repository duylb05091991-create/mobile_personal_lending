# Team 4 — Lab 1 feedback

**To:** Nguyễn Cương Quyết (TN), Vũ Thế Quân, Lý Bá Duy, Nguyễn Thanh Hải, Nguyễn Minh Hoàng  
**Repo:** https://github.com/duylb05091991-create/mobile_personal_lending · `main` @ `310b83a` · `list.md` Input I-1–I-11  
**Rubric:** `Labs/list.md` — Lab 1 (I-1–I-11)  
**Verdict: Fail — not Done. Do not open Lab 2 until this index is locked.**

Lab 1 is the name-identity index. Every later view may use **only** these strings. Empty cells are not allowed. Names must not collide. In-scope and out-of-scope must not overlap.

Re-review after `git pull`: `e76f5c6` → `310b83a` (`Update lending architecture models`).

---

## What is already good

The bound form is now filled. I-1 through I-11 exist, in English, with:

- one system-in-focus (`Nopbai Personal Loan Platform`) and a measurable outcome (`ASSUMPTION: P95 <= 30 seconds`)
- I-2 as people (`Customer`, `Loan Operations Specialist`); I-3 as simulated externals (`Credit Scoring System`, `ESB Integration Layer`, `Core Banking`)
- I-4 containers that I-5 and I-11 actually use
- ESB / Core Banking / Credit Scoring System **not** listed as internal containers
- CON.1–CON.5, each with an effect on the process
- sync vs async examples, a forbidden path (`Mobile App` must not write `Core Banking`), and one I-11 container (`Decision Engine`)
- quality-gate files marked deferred until Lab 7; G1–G6 no longer live in `Analysis.md`

Keep that shape. Lock I-6 and freeze. Stop redrawing Lab 8 / Lab 9.

---

## Fail if — must fix before Lab 2

### 1. Later labs are still being worked while Lab 1 is not Done

Git:

| Commit | When | What landed |
|--------|------|-------------|
| `e76f5c6` | 21 Aug 14:11 | Blank I-1–I-11 **and** Domain / Requirement / Analysis, ArchiMate + RACI, C4 Context, custom AG/DG gates, templates, DTB samples. |
| `310b83a` | 21 Aug 14:42 | Filled I-1–I-11 **and** rewrote Motivation, Business Process, Application, Technology, Organization, C4 Context (still with header + RACI). Deferred the gate files. Copied the previous feedback. |

Lab 1 Fail-if: *any later lab started before this index is complete.* Pack fail: Guide / header / RACI applied before Lab 7.

`list.md` submit checklist Lab 1 is still unchecked. Lab 8 / Lab 9 files still carry RACI and diagram headers.

**Fix:** freeze Lab 1 only. Leave ArchiMate / C4 / `Requirement_Document.md` as accidental early drafts — do not keep editing them. Do not tick Lab 2–10. UML, C4 Container, and G1–G6 wait.

### 2. I-6 is not a lockable state machine

Done when: every Input field is filled; names do not collide. I-6 is filled, but the rows contradict I-5, I-10, and each other.

| Defect | What the table says |
|--------|---------------------|
| `OfferReady` is both terminal and not | One `OfferReady` row: Terminal? **No** → `Approved`. Next `OfferReady` row: Terminal? **Yes** → `Rejected`. Terminal? is a property of **this** state. `OfferReady` is not a terminal. |
| `Failed` is unreachable | `Failed` only lists `Failed` → `Failed`. No other state has Next = `Failed`. I-11 `alt CON.4` says record `Failed`. |
| CON.3 is not a transition | I-11 `alt CON.3` is scoring timeout. I-6 `Scoring` only moves to `OfferReady` when a score returns. Add `Scoring` → `Rejected` or `Failed`. |
| Customer accepts twice | I-5: accept agreement, **then** account validation, **then** disbursement. I-6: `OfferReady` + accept → `Approved`; later `AccountValidated` + accept **again** → `Disbursed`. One event, one transition. |
| Disbursement trigger is wrong | `AccountValidated` → `Disbursed` is triggered by accept, not by `Disbursement Adapter` / `Core Banking` confirmation. The `Disbursed` row then uses Core Banking confirm as a self-loop. |

**Fix:** one row per transition; `Terminal?` only on `Rejected`, `Disbursed`, `Failed`; `Failed` reachable from scoring timeout, account-validation failure, and accounting failure; happy-path order = I-5 (submit → score → offer → **accept** → validate → disburse → confirm).

---

## Should fix (Done when: names do not collide; in/out do not overlap)

1. **I-1 Group.** Use Team 4 and the five names above — not only “Team 4”.
2. **I-1 in-scope forks I-4.** Use the index strings: `Mobile App` not “mobile application”; `Credit Scoring Adapter` / `Credit Scoring System` not “scoring”; `Account Validation Service` not “account validation”; `Decision Store` and `Audit Log` not “decision traceability”.
3. **`Loan Offer`.** Organization / C4 / FR-06 use `Loan Offer`. I-7 has no such object (offer sits inside `Decision Record`). Either add `Loan Offer` to I-7 with one source of truth, or stop using that string.
4. **FR-08 limit increase.** It is in `Requirement_Document.md` and not in I-1 in-scope or I-11. Put it in I-1 / I-11, or move it to out of scope.
5. **CON.1 “escalates”.** I-6 has no review / escalate state. Either reject only, or add a named non-standard path that `Loan Operations Specialist` owns.
6. **Wrong-topic leftovers.** `puml/dtb-*.puml` and `templates/20-appendix.md` still talk VCB / NAPAS / Daily Transaction Banking. They are not this index.

I-5 and I-11 participants are ⊆ I-2 + I-3 + I-4. Keep it that way after the I-6 rewrite.

---

## Lab 2 starts only when

- every I-1–I-11 cell is filled with **one** spelling per name
- I-6 transitions match I-5 and CON.\*; `Failed` is reachable; `Terminal?` is consistent
- I-2 is people; I-3 is simulated externals; I-4 is your containers; no duplicated names
- I-1 in-scope uses the same strings as I-4
- G1–G6, diagram header, and RACI are **not** being added to Labs 1–6
- ArchiMate / C4 files are not being treated as Done or edited in parallel

Reply on the repo when Lab 1 is re-locked. Then Lab 2: requirements in **current language**, **no** G1–G6.
