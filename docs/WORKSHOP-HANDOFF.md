# Make Your Work Visible: release handoff

**Owner:** Reggie Leonard, SDS Career Services, UVA School of Data Science.  
**Release:** 1.0.0, based on the approved Scaffolding Architecture PRD.  
**Session:** 40 minutes after a 15–20 minute faculty opening. The 45-minute option adds four minutes to independent work and one to peer review.

## Governing design

A student keeps one personally chosen assignment, project, question, or job task throughout the session. It is not a collection of unrelated exercises. The sequence moves from a worked example to shared practice, individual application, and an independent explanation. Extra support is selectable and fades; it is not an automatically generated “adaptive” score.

The organizing concepts are fluency, legibility, and reach. Preserve Reggie's sentence: **The work builds fluency. The explanation builds legibility.** Fluency is grounded understanding of work, not jargon, accent, charisma, or an insider identity. Legibility is recognizable capability and contribution, not only polished writing. Reach provides honest context for a relevant person to engage with a project or question.

The facilitator is a career professional, not the technical grader. Do not reintroduce the bookstore SQL lab, custom implementation exercises, technical correctness claims, a mastery score, or mandatory public posting.

## What the build actualizes

Five starting conditions narrow a ten-option activity collection. Seven exercises have task-only, nudge, and worked-example states. A context card can preserve the selected work's title and status, but the student's substantive answers stay in their own file or tool. Eight timers are independently started, paused, reset, and preset. Leaving an activity pauses its timer. The final reader exercise removes help controls and asks for an explanation without a sentence stem.

The Figma task becomes a small music-recommendation measurement brief, not a simulated employment accomplishment. The actual brief is included and reused for the README and outreach models. The CSIS task provides a second shared-practice example. Before/after project explanations use identical questions: problem; approach and contribution; result or current progress and meaning. Plans and untested assumptions remain visible.

The 14-screen sequence, timings, cue lines, actions, and transitions are canonical in `content/session.json`. Numbered Markdown files hold visible copy. The build synchronizes session text exports, one-line speaker notes, and facilitator materials. Do not independently rewrite PDF speaker notes without changing their source.

## Artifact integration

The supplied `artifact_v2_html.html` is now the source basis for the collection and writing kit, not just screenshots. All 12 portfolio selections, five six-part writing guides, and nine reading selections are retained. Their annotations have been reviewed; career-stage limits and unverified original claims are documented. One original reading page could not be rechecked and remains visibly labeled.

The original's CDN, icon, remote-font, and Prism dependencies are not used at runtime. The new gallery uses semantic buttons, keyboard-accessible dialogs, explicit close/focus behavior, working filters, search, and clipboard fallbacks. The untouched source and extracted originals are retained only in the owner's provenance archive. The public edition uses reviewed content. See `ARTIFACT-MIGRATION.md` for the differences.

Both HTML entry points use the same `src` and `content` inputs. `artifact.html` simply starts in the collection. Do not fork the collection into two manually maintained versions. No Gemini link or embedded Gemini app is required.

## Voice and appearance

The office name is **SDS Career Services** everywhere in the current release. Keep the cream/navy/orange editorial style, readable hierarchy, and complete, literal sentences. Avoid slogan piles, “one useful move,” “not a gate,” “work travels,” and “a link is a location; a story is an invitation.” Do not make scaffolding visible as a large framework diagram the student has to decode.

The live deck is paced around what students do. The field guide and Artifact hold the depth. Preserve the distinction between “planned instructional time” and observed learning. A peer can report what they understand; the workshop cannot certify technical competence.

## File architecture

- `src/index.template.html`, `src/style.css`, and `src/app.js`: UI source.
- `content/session.json`, `content/slides/*.md`: canonical session and slide copy.
- `content/resources.json`: routing, scaffolds, models, original Artifact selections, reviewed guides, prompts, and templates.
- `content/guide-*.md`, `content/sources.json`, `content/measurement-brief.md`: reference and example sources.
- `build.py`: creates self-contained main/Artifact HTML and synchronized text exports.
- `build_print.py`: creates a nine-page facilitator guide, one-page run sheet, and two-page worksheet.
- `public/`: publishable static output. It does not contain the job-board workbook or learner work.
- `docs/`: Markdown guides, QA, acceptance mapping, migration notes, privacy, and deployment instructions.
- `tests/`: content checks, the document-injection UI suite, and a separate native-browser smoke suite where available.

The authoring helper scripts used during initial creation are not canonical build dependencies. Edit the content files directly and run the two build scripts. The untouched approved PRD remains a separate design artifact; it is not rewritten to claim new evidence.

## State, privacy, and dependencies

The default work card is in memory. Persistence requires an explicit checkbox and is limited to a title, one of five starting conditions, and one of three work-status labels. JSON imports have a size limit, schema checks, and escaped rendering. Exports do not retrieve work from another app. Context should be nonsensitive. Present mode hides personal work titles and selection controls.

No backend, model API call, key, telemetry, external runtime library, remote font, or student-account connection exists. The content security policy blocks connections, forms, objects, and base-URL changes, and hashes the executable script. Links to external services are intentional user actions; their terms and costs are separate. Do not advertise this as an independent security audit.

## Release and future changes

Read `QA.md` and the machine-readable reports for the actual test scope. The original environment blocked file and HTTP navigation, so its broad UI suite used document injection and a clearly labeled storage test double. Native browser smoke tests, when run elsewhere, are recorded separately rather than retroactively changing that description. Neither suite certifies the real projector, actual students, or every assistive technology.

Run all relevant checks after changing copy or timing, because longer text can affect projected layouts. Update sources before using this material in a later recruiting season. Product offers, job status, and portfolio content are date-sensitive.

The intended GitHub destination is `thatssoreg/make-your-work-visible`. It was accessible and already public when this build began; its visibility was not changed. The private Artifact repository is not a substitute destination. No hosting service, paid plan, or custom domain should be silently enabled.
