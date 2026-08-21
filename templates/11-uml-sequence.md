# 11 — UML Sequence

**Pack:** Design (UML)  
**RACI:** Dev **R**, SA **A**, BA/Sec/Test **C**  
**Handbook:** §3.1, §4.11  
**Language:** UML Sequence. Participants ⊆ C4 Container names from [00-index.md](00-index.md).  
**Glossary:** [20-appendix.md](20-appendix.md)

Copy this file to `11-uml-sequence-<use-case>.md` once per critical-path use case.

## Diagram header

```
Title:      ________________________________
Viewpoint:  ArchiMate / C4 / UML ___________
Layer(s):   Strategy / Business / App / Tech
As-Is | To-Be | Transition:  _______________
Owner:      Role ________  Name ____________
Version:    v____  Date ________  Status Draft|Review|Approved
Legend:     relationships listed
Scope:      in-scope systems / out-of-scope
```

## Status

| Field | Value |
| --- | --- |
| Status | Draft / Review / Approved / N/A |
| N/A reason | |
| Owner | |
| Date | |

## Use case

| Field | Value |
| --- | --- |
| Use case | |
| Happy path / alts in scope | |

```mermaid
sequenceDiagram
  autonumber
  actor Actor
  participant ContainerA
  %% participant ContainerB
  Note over Actor,ContainerA: Fill one use case — participants from name-identity list only
```
