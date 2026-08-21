# Lab 8 — ArchiMate After Pack

**Status:** Draft after-pack; requires Lab 7 adoption and review.

## Required views

| View | Owner / RACI | Evidence |
| --- | --- | --- |
| Motivation / Strategy | EA R; Owner A; SA/BA/Sec C | Goal, outcome, CON.1-CON.5 |
| Business Process | BA R; Owner A; EA/SA/Sec/Test C | I-5 happy path and constraint branches |
| Application Cooperation | SA R; EA A; DA/Sec/Dev C | I-4 names only; external boundaries explicit |
| Technology / Deployment | Ops R; SA A; Sec/Dev C | I-9 locations and forbidden path |

## Language controls

These are ArchiMate views. They do not contain C4 protocol labels, UML messages, JDBC, pods, or container internals on Motivation or Process. Application Cooperation uses the exact I-4 strings. Core Banking, ESB Integration Layer, and Credit Scoring System remain external.

## Existing diagram evidence

- [../Motivation-Strategy.md](../Motivation-Strategy.md)
- [../Business-Process.md](../Business-Process.md)
- [../Application-Architecture.md](../Application-Architecture.md)
- [../Technology-Architecture.md](../Technology-Architecture.md)

PlantUML sources are in [../puml/](../puml/).
