# Approved PRD: implementation mapping

This is a build acceptance record, not a study of student outcomes.

| Requirement | Implementation | Evidence to inspect |
| --- | --- | --- |
| One persistent work object | A circled note is the primary object; an optional context card keeps its title, starting condition, and status visible. | Screens 3, 6, 9, 11, 12; all five UI path tests. |
| Find a starting point without a score | Five self-selected conditions, with a concrete fallback question. | Screen 3; work-card schema. |
| Model before independent use | The Figma task produces an actual measurement brief used again for the README and outreach. | Screens 4, 7, 11; `measurement-brief.md`. |
| Shared practice before application | CSIS scope discussion and clarifying-question exercise precede individual bridges and explanations. | Screens 5–6 and 8–9. |
| Support fades rather than accumulates | Task-only by default, optional nudge, optional worked example; next exercise defaults to task-only. | Seven help panels; state-specific nudge tests. |
| No finished project assumed | Planned/in-progress/observed status is explicit; plan language is supported. | Model brief, README after version, card validation, prompts. |
| Same communication framework | Problem; approach and contribution; result/current progress and meaning. | Before/after criteria and individual explanation. |
| Final independent explanation | Peer test has no help panel and asks the author to explain a choice without a sentence stem. | Screen 13; cue sheet; solo alternative. |
| Meaningful room participation | 28 of 40 planned minutes are activity/application/peer blocks; longer option adds work and peer time. | Session data and timing tests. This is planned time, not observed engagement. |
| Host need not teach code | Technical implementation questions go to course staff, official docs, or externally authored exercises. | Facilitator setup and guide; no custom SQL lab. |
| Depth without more lecture | Ten work options, eight guide topics, full Artifact collection and writing kit. | Reference views; initial routing narrows choices. |
| Clear exit and portability | Save/next-action close; Markdown worksheet, guide, outlines and prompts; JSON card export. | Download and import tests. Exports do not save other apps' work. |
| Safe publishing boundary | No workbook or learner content in public output; original Artifact provenance excluded from publishing. | Source/build checks and directory separation. |
| Prime presentation behavior | Chapter/Contents navigation, focus-aware keyboard control, eight timers, Present mode, contextual return links. | UI report; projected-layout captures. |
| No runtime model spend | No API call, key, server, analytics, or account integration; prompts are text. | Runtime network observation and CSP/source checks. |

## What still requires people

The actual facilitator should test the projector and downloads on the teaching laptop. A first session will reveal whether some learners need more time or different hints. A correct data model, effective measurement plan, or technically sound implementation requires the relevant expertise; this workshop does not award that judgment automatically.
