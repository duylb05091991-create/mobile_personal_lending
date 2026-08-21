# Lab 7 - Hierarchy, focus matrix, quality gates, RACI

**R:** EA  
**A:** Owner  
**Status:** Lab 7 working draft - **READY** under the agreed scope: Lab 1, Lab 2, Lab 3, and Lab 4 are the primary sources. Lab 5 and Lab 6 are not required inputs for this Lab 7 artifact.

## 1. Scope and source authority

This Lab 7 artifact adopts the Guide for the after pack. It is based on the following primary sources:

| Source | Authority used in Lab 7 |
|--------|-------------------------|
| Lab 1 - Scopes | Names, actors, external systems, internal containers, process, states, source of truth, integrations, deployment, constraints, and named use cases |
| Lab 2 - Requirements Analysis | Requirements, analysis, exception paths, open questions, and traceability |
| Lab 3 - Implement architecture, design, and test | Build list, selected `Decision Engine` Component, sequence, contracts, exception specification, and planned tests |
| Lab 4 - Standardize following modeling-driven design | Cleaned identity, defect list, comparison note, and current naming decisions |
| Requirement Document | Supporting draft only; it cannot override Lab 1-4 or promote unresolved requirements into facts |

Lab 5 and Lab 6 are explicitly outside the required input scope for this Lab 7 artifact. Their absence does not block Lab 7.

## 2. Adoption record

### 2.1 Guide adoption statement

The team adopts the Guide in `list.md` as written from Lab 7 onward:

- ArchiMate aligns the enterprise view.
- C4 aligns the system and container build view.
- UML aligns behavior, lifecycle, and tests where later artifacts require it.
- G1-G6 are the only quality gates. No G7 or competing gate set is introduced.
- RACI is assigned per artifact, with exactly one R and one A.
- The person responsible for drawing an artifact does not approve that same artifact.
- Lab 1 identity remains the source of truth for names.
- Lab 4 cleanup is the current naming baseline for the after pack.
- Lab 5 and Lab 6 are not prerequisites for adopting the Guide in this scope.

### 2.2 Role roster

| Person | Role | Lab 7 responsibility |
|--------|------|----------------------|
| Nguyễn Cương Quyết (TN) | EA | Guide adoption, hierarchy, and gate evidence review |
| Vũ Thế Quân | SA | Solution/container identity and C4 handoff |
| Lý Bá Duy | BA / Test | Requirement mapping and state/test coverage review |
| Nguyễn Thanh Hải | Dev | Design evidence and contract handoff |
| Nguyễn Minh Hoàng | Owner | Accountable for adoption and gate decisions |

One person may hold two roles, but must not be both R and A on the same artifact.

## 3. Hierarchy and focus matrix

| Level | Language | Focus for Nopbai Personal Loan | Main readers | Planned evidence |
|-------|----------|-------------------------------|--------------|------------------|
| Top | ArchiMate | Goal, outcome, actors, capabilities, constraints, and business process | Owner, EA, BA | Motivation/Strategy and Business Process views |
| Middle | C4 plus ArchiMate Application/Technology | `Nopbai Personal Loan Platform`, containers, external systems, integrations, and deployment | SA, DA, Security, Ops | Context, Container, Application Cooperation, Technology views |
| Base | UML plus one C4 Component | Named behavior, `Loan Application` lifecycle, selected `Decision Engine` internals, and test coverage | Dev, Test, Ops | Later sequence, activity/state, and coverage artifacts |

### Focus rules

- One diagram answers one question.
- Do not mix enterprise motivation, C4 containers, and UML messages on one after-pack view.
- Each ArchiMate Application Component, C4 Container, sequence participant, and test SUT must resolve to an exact I-4 name.
- Internal module names are allowed only inside the selected `Decision Engine` Component view.
- `Loan Application` is the single lifecycle object; its states remain the exact I-6 strings.

## 4. Lab 2 requirements mapped to G1-G6

This mapping is a Lab 7 planning record. It does not itself pass a gate.

| Gate | Lab 2 evidence | Lab 1-4 evidence | Planned after-pack evidence | Pass status |
|------|----------------|------------------|----------------------------|-------------|
| G1 | Goal, outcome, FR-01 to FR-12, NFR-01 to NFR-05, `CON.1` to `CON.5` | I-1, I-10, Lab 4 identity baseline | Motivation or Strategy view | **Pending** Owner review |
| G2 | Requirement state/object effects and exception paths | I-5 process, I-6 states, Lab 3 planned transition tests | Business Process and state evidence | **Pending** BA/Test review |
| G3 | Container responsibilities and relevant NFRs | I-3 externals, I-4 containers, I-8 modes, I-9 deployment, Lab 4 identity check | C4 Context and Container views | **Pending** SA review |
| G4 | FR-03, FR-10, FR-11 integration requirements | Lab 3 C-01 to C-03 contract register | Contracts derived from Container relationships | **Pending** Dev/SA review |
| G5 | FR-02, FR-07, FR-09, FR-10 and `CON.*` exceptions | Lab 3 EX-01 to EX-05 and Lab 4 exception cleanup | Critical failure path evidence | **Pending** SA/Owner review |
| G6 | State/object effects and sequence alternatives | Lab 3 T-01 to T-15 | Planned coverage note for later behavior artifacts | **Pending** Test/SA review |

### 4.1 Requirements excluded from current facts

The supporting Requirement Document contains requirements that are not locked by Lab 1-4 and therefore are not promoted into the current gate evidence:

- Requirement Document NFR-02: availability target.
- Requirement Document NFR-07: capacity/scaling target.
- Requirement Document NFR-08: applicable regulatory obligations.

These remain open questions or future requirements. They do not become G1-G6 pass evidence without an approved change to the primary requirements baseline.

## 5. Quality-gate register

The following pass rules are adopted from the Guide without creating a parallel gate set.

| Gate | Blocks | Pass rule | Evidence artifact | Owner / reviewer | Pass? |
|------|--------|-----------|-------------------|------------------|-------|
| G1 - Strategy signed | Solution design | Goal, outcome, and `CON.*` are listed | Lab 1 I-1/I-10, Lab 2 scope, planned Motivation/Strategy view | Nguyễn Minh Hoàng / Nguyễn Cương Quyết (TN) | **Pending** |
| G2 - Process + states | Dev + Test design | Named states match the information/state view | Lab 1 I-5/I-6, Lab 2 trace, Lab 3 planned tests | Lý Bá Duy / Nguyễn Cương Quyết (TN) | **Pending** |
| G3 - C4 Context + Container | Implementation | No unnamed externals; sync/async labeled; names match the Input index | Lab 1 I-3/I-4/I-8, Lab 1 I-9, Lab 4 identity check | Vũ Thế Quân / Nguyễn Cương Quyết (TN) | **Pending** |
| G4 - Contracts | Coding of integrations | A contract exists for every Container relationship | Lab 3 C-01 to C-03 contract register | Nguyễn Thanh Hải / Vũ Thế Quân | **Pending** |
| G5 - Critical exception path | Production release | Compensating actions on the critical failure path are modeled | Lab 3 EX-01 to EX-05 and Lab 4 cleanup | Nguyễn Thanh Hải / Nguyễn Cương Quyết (TN) | **Pending** |
| G6 - Test coverage | UAT sign-off | All state transitions and sequence alternatives are mapped; participants are C4 names | Lab 3 T-01 to T-15 and later coverage evidence | Lý Bá Duy / Vũ Thế Quân | **Pending** |

`Pending` means the evidence is prepared but formal approval is not recorded. Pending is not Pass.

## 6. RACI standard

RACI is per artifact, not only per role.

| Letter | Meaning | Rule |
|--------|---------|------|
| R | Responsible | Draws or produces the artifact |
| A | Accountable | Approves or rejects; exactly one person |
| C | Consulted | Reviews and constrains before freeze |
| I | Informed | Reads after acceptance and does not redraw |

### 6.1 After-pack diagram header

Use this header on every after-pack artifact from Lab 7 onward:

```text
Title:      ________________________________
Viewpoint:  ArchiMate / C4 / UML ___________
Layer(s):   Strategy / Business / App / Tech
As-Is | To-Be | Transition:  ______ (circle one; this pack = To-Be
            unless the view is the Lab 2 as-is analysis)
Owner:      Role ________  Name ____________
RACI:       R ____  A ____  C ____  I ____
Version:    v____  Date ________  Status Draft|Review|Approved
Legend:     relationships listed
RACI legend: R = draws · A = approves · C = consulted · I = informed
Scope:      in-scope / out-of-scope
```

### 6.2 Planned artifact RACI

| Artifact | R | A | C | I |
|----------|---|---|---|---|
| Motivation / Strategy | Nguyễn Cương Quyết (TN) | Nguyễn Minh Hoàng | Lý Bá Duy; Vũ Thế Quân | Nguyễn Thanh Hải |
| Business Process | Lý Bá Duy | Nguyễn Minh Hoàng | Nguyễn Cương Quyết (TN); Vũ Thế Quân | Nguyễn Thanh Hải |
| Application Cooperation | Vũ Thế Quân | Nguyễn Cương Quyết (TN) | Nguyễn Thanh Hải; Lý Bá Duy | Nguyễn Minh Hoàng |
| Technology / Deployment | Nguyễn Thanh Hải | Vũ Thế Quân | Nguyễn Cương Quyết (TN); Lý Bá Duy | Nguyễn Minh Hoàng |
| C4 Context | Vũ Thế Quân | Nguyễn Minh Hoàng | Nguyễn Cương Quyết (TN); Lý Bá Duy | Nguyễn Thanh Hải |
| C4 Container | Vũ Thế Quân | Nguyễn Cương Quyết (TN) | Nguyễn Thanh Hải; Lý Bá Duy | Nguyễn Minh Hoàng |
| C4 Component - `Decision Engine` | Nguyễn Thanh Hải | Vũ Thế Quân | Lý Bá Duy | Nguyễn Minh Hoàng; Nguyễn Cương Quyết (TN) |
| Later UML behavior / coverage | Lý Bá Duy | Vũ Thế Quân | Nguyễn Thanh Hải; Nguyễn Cương Quyết (TN) | Nguyễn Minh Hoàng |

## 7. Lab 7 completion check

- [x] Lab 1 is the identity source.
- [x] Lab 2 requirements and trace are mapped to G1-G6.
- [x] Lab 3 design evidence and test specification are mapped to G1-G6.
- [x] Lab 4 cleanup is used as the naming baseline.
- [x] Lab 5 and Lab 6 are excluded from the Lab 7 input scope.
- [x] Guide adoption statement is recorded.
- [x] Role roster is recorded.
- [x] Hierarchy and focus matrix are recorded.
- [x] G1-G6 register is recorded with pass rules and evidence.
- [x] RACI standard and after-pack header are recorded.
- [x] No competing gate set or G7 is introduced.
- [ ] Owner and reviewers formally approve the pending G1-G6 decisions.

**Current result:** Lab 7 artifact is complete as a working deliverable under the agreed scope. G1-G6 remain `Pending` until their named reviewers approve the evidence. Lab 8 may start after the Lab 7 working deliverable is accepted by the Owner.
