# Make Your Work Visible

A scaffolded GitHub and portfolio workshop by **Reggie Leonard, SDS Career Services, UVA School of Data Science**.

The learner chooses one assignment, project, question, or job task and keeps developing it through **fluency, legibility, and reach**. Shared examples model a move; learners try it together, apply it to their own work, then explain a decision without a template. The core session takes 40 minutes after a 15–20 minute faculty opening. A 45-minute setting extends practice and peer review rather than lecture.

## Use the release

Open `index.html` in a full browser, or publish only the `public/` folder through a static host. Open `artifact.html` to begin with the collection instead of the workshop. Both HTML entry points are self-contained: no package installation, server, remote font, or runtime network connection is needed. GitHub's file preview displays source; it is not the running application.

Printable materials are in `public/downloads/`: a nine-page facilitator guide, one-page run sheet, and two-page student worksheet. The complete student guide and one-line speaker notes are in `docs/` as Markdown.

No hosting service is enabled by this repository. A public repository and a deployed website are different things.

## What is included

- Fourteen screens following the approved scaffolded sequence, five starting conditions, seven selectable help panels, and eight independent timers.
- A small optional work card, with opt-in browser storage and JSON export/import. It stores a title, starting condition, and status, not project answers or repository data.
- Ten work options narrowed to three relevant suggestions before showing the complete menu.
- Artifact's 12 original portfolio selections, all five six-part writing guides, and nine original reading selections, with reviewed annotations and visible evidence limits.
- A coherent music-recommendation measurement brief used across the employer-task model, README comparison, and sharing examples.
- GitHub guidance, writing models, student resources, AI coaching prompts, and a dated source register.

Student work stays in the learner's own repository, notebook, document, or paper notes. This application is not a technical grader, an employability score, or another project editor.

## Build and check

Requires Python 3.10 or newer for the build. The generated HTML needs only a browser.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-build.txt
python3 build.py
python3 tests/test_build.py
```

On Windows, use `py` and the environment's `Scripts` activation path as appropriate.

The browser-test scripts use Playwright. `tests/test_ui.py` records the original document-injection suite and its storage-test-double limitations. `tests/test_native.py` is for environments that permit ordinary local HTTP navigation. See `docs/QA.md` for the exact results and scope, not just a test count.

## Edit the right source

`content/session.json` defines timing, speaker notes, actions, and transitions. The numbered files in `content/slides/` contain the visible slide copy. `content/resources.json` holds the starting conditions, help, activity routes, Artifact data, prompts, and templates. `content/guide-*.md` and `content/sources.json` hold reference content. `src/` contains the interface implementation.

Run the build after editing. Generated files, including the public HTML, Markdown exports, and PDFs, should not become a competing content source.

## Privacy and attribution

There are no model API calls, API keys, analytics, student-account connections, or backend services. External links open only when selected. The content security policy explicitly denies API/network connections from the app. Optional browser storage belongs to that browser and can be unavailable or cleared. Use a brief, nonsensitive work title.

The original Artifact source was used with the owner's approval. The reviewed public release preserves its selections and guide structures, while replacing unsupported outcome claims and fictional template metrics with bounded annotations and placeholders. The untouched source is retained in the owner's separate provenance archive, not executed by this release. See `docs/ARTIFACT-MIGRATION.md`.

Public portfolio and article authors retain rights to their work. Links and editorial annotations are not claims of endorsement or technical validation. An opportunity being visible on the review date does not guarantee that it remains open.
