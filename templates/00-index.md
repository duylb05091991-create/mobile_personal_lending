# 00 — Dossier index

**Pack:** Cover / governance  
**RACI:** EA **A**, SA **R**, Business Owner **A** (index & governance)  
**Handbook:** §3.1, §3.2, §3.3, §4.14  
**Glossary:** [20-appendix.md](20-appendix.md)

## Cover

| Field | Value |
| --- | --- |
| Initiative | `<PREFIX>-___` |
| Product | |
| Title | |
| Version | `v____` (semver on dossier, not on every box) |
| Status | Draft / Review / Approved |
| Date | |

## Owners

| Role | Name | Notes |
| --- | --- | --- |
| EA | | |
| SA | | |
| BA / PO | | |
| DA | | |
| Sec | | |
| Dev | | |
| Test | | |
| Ops | | |
| Business Owner | | |

## Changelog

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| `v0.1.0` | | | Copied from `templates/` |
| | | | |

## Naming (handbook §3.2)

| Item | Pattern | This dossier |
| --- | --- | --- |
| Initiative | `<PREFIX>-<nnn>` | |
| View title | `<Viewpoint> — <Product> — <As-Is\|To-Be>` | |
| Element ID | `LAYER.TYPE.Name` | e.g. `APP.CMP.<Container>` |
| Diagram file | `<PREFIX>-___-v<n>-<viewpoint>.<tool>` | |
| Version | Semver on dossier | |

## Name identity (fill once — use on every view)

ArchiMate Application Component **is** the C4 Container **is** the UML sequence participant **is** the test SUT.

| Kind | Names (this initiative) |
| --- | --- |
| Person / Business Actor | |
| System-in-focus (C4 L1) | |
| System_Ext | |
| Containers (C4 L2) | |
| Key data objects | |

Do not fork these strings on later views.

## File inventory

Missing files are **N/A** with owner sign-off — not omitted.

| File | Pack | Status (Draft / Review / Approved / N/A) | Owner |
| --- | --- | --- | --- |
| [00-index.md](00-index.md) | Cover | | |
| [adr/](adr/) | Cover | folder always present | |
| [01-motivation-strategy.archimate.md](01-motivation-strategy.archimate.md) | Business | | |
| [02-business-process.archimate.md](02-business-process.archimate.md) | Business | | |
| [03-organization-product.archimate.md](03-organization-product.archimate.md) | Business | | |
| [04-information-structure.archimate.md](04-information-structure.archimate.md) | Business | | |
| [05-c4-context.md](05-c4-context.md) | Solution | | |
| [06-c4-container.md](06-c4-container.md) | Solution | | |
| [07-c4-deployment.md](07-c4-deployment.md) | Solution | | |
| [08-application-cooperation.archimate.md](08-application-cooperation.archimate.md) | Architecture | | |
| [09-c4-component.md](09-c4-component.md) (rename `<container>`) | Design | | |
| [10-uml-domain-class.md](10-uml-domain-class.md) | Design | | |
| [11-uml-sequence.md](11-uml-sequence.md) (copy per use case) | Design | | |
| [12-uml-activity-state.md](12-uml-activity-state.md) | Design | | |
| [13-technology-deployment.archimate.md](13-technology-deployment.archimate.md) | Architecture | | |
| [14-layered-realization.archimate.md](14-layered-realization.archimate.md) | Architecture | | |
| [15-risk-compliance.archimate.md](15-risk-compliance.archimate.md) | Governance | | |
| [16-migration-plateau.archimate.md](16-migration-plateau.archimate.md) | Implementation | | |
| [17-nfr-and-constraints.md](17-nfr-and-constraints.md) | Architecture | | |
| [18-traceability.md](18-traceability.md) | Governance | | |
| [19-role-handoff.md](19-role-handoff.md) | Cover | | |
| [20-appendix.md](20-appendix.md) | Cover | copy then add initiative-only terms | |

## N/A register

| File | Reason | Owner | Date | Sign-off |
| --- | --- | --- | --- | --- |
| | | | | |

## Mandatory vs optional views

Mark what this initiative requires. Defaults below are typical; adjust and sign.

| View | This initiative (Mandatory / Optional / N/A) |
| --- | --- |
| Motivation / Strategy | |
| Business Process | |
| Organization / Product | |
| Information Structure | |
| C4 Context | |
| C4 Container | |
| C4 Deployment | Mandatory if runtime topology changes |
| C4 Component (1 container) | Mandatory for each touched container |
| UML Sequence (critical path) | Mandatory per in-scope use case |
| UML State (one business/data object) | |
| Technology (ArchiMate) | Mandatory if runtime changes |
| Risk & Compliance | |
| Migration / Plateau | If replacing as-is |
| `adr/` folder | Always present; individual ADRs as needed |
| Appendix (`20`) | Always present |

## Cross-language consistency checklist

| Check | Pass? |
| --- | --- |
| Every C4 Person exists as ArchiMate Business Actor or Role | |
| Every C4 System_Ext is an ArchiMate Application Component or Actor (external) | |
| Sequence participants ⊆ C4 Containers (name-identity list on this file) | |
| State machine is for one Business/Data Object named in Information Structure | |
| APIs on sequence = Application Interfaces | |
| Deployment nodes realize the containers they host | |
| Constraints on Motivation appear on process / sequence decision branches | |
