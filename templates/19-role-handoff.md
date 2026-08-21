# 19 — Role handoff

**Pack:** Cover / governance  
**RACI:** EA **A**, SA **R** (dossier governance)  
**Handbook:** §3.1, §6.4, §6.5  
**Glossary:** [20-appendix.md](20-appendix.md) (RACI, G1–G6)

## Status

| Field | Value |
| --- | --- |
| Status | Draft / Review / Approved / N/A |
| N/A reason | |
| Owner | |
| Date | |

## Purpose

I/O per engineering role for **this** initiative. Fill names from [00-index.md](00-index.md).

## Per-role I/O

| Role | Name (this initiative) | Minimum input to start work | Minimum output to hand off | Next consumer |
| --- | --- | --- | --- | --- |
| EA | | Strategy, as-is landscape | Motivation, capabilities, plateaus, principles | SA, BA, Owner |
| BA/PO | | Goals, journeys | Process, product, use cases, activity | SA, Test, Owner |
| SA | | EA + BA packs | C4 L1–L2, app cooperation, interfaces, NFRs | Dev, DA, Sec, Ops, Test |
| DA | | Business objects + containers | Information structure, SoT, class sketch | Dev, Test, Sec |
| Sec | | Constraints + C4 + data class | Risk view, trust boundaries, control requirements | Dev, Test, SA |
| Dev | | C4 L2, contracts, sequence, states, controls | C4 L3, as-built sequence, APIs | Test, Ops, SA |
| Test | | Process, state, sequence, C4, constraints | Scenario catalog, coverage, defects | Dev, SA, Owner |
| Ops | | Tech view, containers, NFRs | Deployment, paths, runbooks | Dev, SA, Test (env) |

## Handoff quality gates

Block coding / UAT if red. Adjust pass rules to this product.

| Gate | Blocks | Pass rule | Pass? |
| --- | --- | --- | --- |
| G1 Strategy signed | Solution design | Goal, outcome, constraints listed | |
| G2 Process + states | Dev + Test design | Named states match Information Structure / state view | |
| G3 C4 Context + Container | Implementation | No unnamed externals; sync/async labeled; names match 00-index | |
| G4 Contracts | Coding of integrations | OpenAPI (or equivalent) for every Rel on Container diagram | |
| G5 Critical exception path | Production release | Compensating actions on the critical failure path are modeled and tested | |
| G6 Test coverage | UAT sign-off | All state transitions + sequence alts mapped; participants = C4 names | |
