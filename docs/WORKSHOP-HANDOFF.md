# Make Your Work Visible: practical workshop handoff

**Owner:** Reggie Leonard, SDS Career Services, UVA School of Data Science.  
**Release:** 2.0.0 · October 7, 2026.  
**Latest direction:** The practical career workshop supersedes the earlier scaffolding PRD for the live experience.

## Governing purpose

Orient students enough to begin, show relevant examples, and give them time to work and ask questions. This should feel like a GitHub and portfolio counterpart to a career-services résumé workshop, made specific to a school of data science. It is not a technical lab, adaptive lesson sequence, or compulsory project-development curriculum.

## What remains

Fluency, legibility, and reach are the introductory concepts. Keep the sentence “The work builds fluency. The explanation builds legibility.” Students should see how work creates understanding, how evidence makes contribution recognizable, and how an introduction can bring a specific project into a relevant conversation.

Keep a concrete Post-it exercise, the Figma internship-task example, a related README before/after, project diversity, About/profile options, permissions, sharing examples, In practice, the field guide, and the complete integrated Artifact collection.

## What must not return

No student-facing times, countdowns, pacing ranges, speaker cues, or Watch/Model/Apply labels. No diagnostic, persistent work-card, required same-object flow, help-level selector, or mandatory reader test. No music-recommendation measurement brief or bespoke SQL lab. Do not simply hide these behind another mode; the current app does not contain them.

Students may use an existing assignment, start with a question, write an About section, select an external guided practice resource, or work privately. There is no assumption that a finished project exists on arrival.

## Sequence and pacing

Eleven screens: opening; concepts; Post-its; Figma task/bridge; project diversity; README; presence and platform choices; permissions; project introductions; work and questions; close.

The 40-minute presenter plan uses 16 minutes for the opening, examples, and table discussion, 22 for work/questions including a short shared Q&A, and two for closing. The 45-minute version adds five to the work/question block. These timings belong only in presenter source and print materials.

Each screen has one canonical speaker sentence in `content/session.json`. Keep the session flexible: questions and individual work are the purpose, not an interruption to a long scripted sequence.

## Figma example and factual boundaries

The Data Science Intern (2027) page was rechecked October 7, 2026 and displayed an application form. It describes product use, meaningful metrics, and product recommendations. Our practice suggestion is an illustrative feature-adoption measurement brief. It is neither Figma's assignment nor a completed Figma project. The stronger README explicitly labels the plan as complete and the analysis as not yet performed.

Database, cloud, collaboration, and open-source examples broaden the evidence students might show. Do not claim any one tool or project guarantees distinction, interviews, or employment. Technical peers, faculty, documentation, and externally authored practice resources are appropriate places to evaluate technical choices.

## Student experience

The session is linear and light. In practice offers 12 activities with simple category filters. These are convenience filters, not learner diagnoses. The field guide has ten topics, including new project-selection and platform-comparison chapters. The Artifact entry point uses the same collection and writing data as the workshop.

No student editor or autosave exists. No model is called. Prompts and templates can be copied or downloaded. Browser navigation remembers the current view via its URL fragment, not a learner profile.

## Writing and design

Use literal, complete explanations instead of stacked slogans. Keep UVA navy/orange, cream backgrounds, generous type, and the Artifact editorial style. The office name is SDS Career Services. Avoid em dashes, “one useful move,” work that “travels,” “not a gate,” and internal design terminology in student copy.

## Artifacts and build

`build.py` builds print documents, both HTML files, student guide, and speaker notes. It explicitly whitelists number/title/theme when serializing session metadata to the public app. Timings/actions/transitions are excluded. Only the student worksheet is embedded; facilitator PDFs are generated under `docs/print`.

The previous approved PRD remains a historical artifact, not a requirement to restore complexity. Original Artifact selections and reviewed annotations are preserved. See ARTIFACT-MIGRATION.md for original-source provenance.

## Publication and validation

The intended repository remains `thatssoreg/make-your-work-visible`. Do not use the separate private Artifact repository as a substitute. Do not change visibility or enable paid hosting without instruction.

Read QA.md and machine-readable test results for actual results and environment. Automated checks cannot certify classroom pacing, student outcomes, the projector, or assistive-technology use on real devices.
