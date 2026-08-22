# Team 4 — Lab 6 feedback (re-review)

**To:** Nguyễn Cương Quyết (TN), Vũ Thế Quân, Lý Bá Duy, Nguyễn Thanh Hải, Nguyễn Minh Hoàng  
**Repo:** https://github.com/duylb05091991-create/mobile_personal_lending · `main` @ `1fea9c9` · `labs/Lab-6-Integration ecosystem (model, do not build).md`  
**Rubric:** `Labs/list.md` — Lab 6 (before-pack ecosystem; product names as labels; do not install; no Guide)  
**Prior review:** Fail @ `7eaf0fb` (archive skipped)  
**Lab 5:** Pass (`37d168d`) · **Labs 1–4, 7–9:** Pass (unchanged; blobs match `7eaf0fb`)  
**Lab 10:** deleted this sitting (`3cd41a6`) — still not Done; restore and audit Lab 5 later  
**Exception:** Labs 5–6 were not required to open Lab 7. Lab 6 has **no** fail-if “Lab 7 started already.”  
**Verdict: Fail — still not Done. Archive skipped.**

Lab 6 is the **before pack**: gateway / event bus / adapter **as I-4 containers** if they exist. Product names are labels, not boxes. Do not install. Do not apply the Guide. Every I-8 pattern must be visible. Then **archive Labs 1–6**.

`1fea9c9` (*Update Lab-6-Integration ecosystem…*) is this sitting. The sketch was already the right grain at `7eaf0fb`. This commit **reticks** archive and claims `archive/before-pack-labs-1-6-2026-08-22/` is “tracked and committed in Git.” That path is still **not** in the tree.

---

## What changed since `7eaf0fb`

| Prior fail | Now |
|------------|-----|
| No `archive/` / `before-pack/` in git; live `labs/` only | Unchanged. `git ls-tree HEAD` is still `Requirement_Document.md`, `feedback/`, `labs/`, `list.md`. No archive directory, no SHA-256 manifest file. |
| §8 claimed a snapshot | §8 now says the copies are verified **and committed**. Still a claim, not a blob. |
| Return arrows unlabeled on outcome edges | Outcome edges now repeat protocol + Sync/Async. Fine; not the fail-if. |
| Lab 10 Fail file in tree | **Deleted** (`3cd41a6`). That does not archive Labs 1–6. Do not delete after-pack files to close Lab 6. |

Fail-ifs that stayed clean: no Guide header; no Kong / Keycloak / Kafka stack; no IAM box.

---

## Fail-if

| Rule | Hit? | Evidence |
|------|------|----------|
| Guide applied | No | Before-pack heading; no after-pack header / RACI |
| Running Kong / Keycloak / Kafka stack | No | Labels refused; commit is markdown only |
| IAM added as a new system while AuthN is on the gateway | No | No gateway; no IAM box |
| **Archive skipped** | **Yes** | §8 / §9 ticked; snapshot path named; **zero archive files in git**. Live Labs 1–6 are not an archive. Git history is not an archive. A checkbox is not an archive. |

Same grain as the first Fail and as Team 1 / Team 3 first Lab 6 Fail: the sketch may be Done; **Done when** still requires a recoverable **committed copy** of Labs 1–6.

---

## Fix before a Pass (same as last sitting)

**Add the files.** Commit a directory that actually contains copies of Labs 1–6. Then the §8 ticks can stay.

Do not rewrite Labs 1–5. Do not restyle the copies to the Guide. Do not tick “committed in Git” until `git ls-tree` lists those paths.

Suggested freeze (directory name may differ):

| Live (leave in place) | Must appear as a **second** path in git |
|------------------------|------------------------------------------|
| `labs/Lab-1-Scopes.md` | e.g. `archive/before-pack-labs-1-6-2026-08-22/Lab-1-Scopes.md` |
| `labs/Lab-2-Requirements-Analysis.md` | same tree |
| `labs/Lab-3-Implement architecture, design, and test.md` | same tree |
| `labs/Lab-4-Standardize following modeling-driven design.md` | same tree |
| `labs/Lab-5-Low-level design (UML).md` | Lab 5 Pass file (`37d168d`), messy |
| `labs/Lab-6-Integration ecosystem (model, do not build).md` | first-written Lab 6 (`7eaf0fb` is fine) |

SHA-256 manifest is optional. The copies are the fail-if.

Keep live `labs/`. Lab 10, when you restore it, restyles **Lab 5** in a **new** after-pack file. It must not overwrite the archived Lab 5.

---

## Sketch (already good — do not restyle)

I-4 adapters only; no invented gateway / bus; ESB stays I-3; C-01 HTTPS Sync; C-02/C-03 message Async; no product-system; nothing installed; AVS → Core Banking HTTPS not drawn. Leave leftovers (CON.2 two owners, G6 accept SUT, CON.1 clamp vs reject) to Lab 10.

---

## Lab 10 (not this Fail, but do not lose the draft)

`3cd41a6` removed `labs/Lab-10-UML low-level design for named C4 use cases.md`. That sitting was already Fail (Lab 5 skipped at the time). Restore from `8bf9787` when you reopen Lab 10; then fill comparison §9 against **this** Lab 5 file. Deleting it does not Pass Lab 6 and does not Pass Lab 10.

---

## Pack

| Lab | Status |
|-----|--------|
| 1–5 | Pass (live; **still not archived**) |
| **6** | **Fail** — archive skipped (`1fea9c9` reticked the claim; still no copies) |
| 7–9 | Pass (unchanged) |
| 10 | Not in tree; last scored Fail @ `8bf9787` |

No Lab 11. Independent capstone is `Labs/capstone.md` after Lab 10 Done. Do not install anything.

Reply on the repo when `git ls-tree` lists the before-pack copies of Labs 1–6.
