# Make Your Work Visible
## GitHub and portfolios · SDS Career Services

A practical workshop for data science students, led by Reggie Leonard at the UVA School of Data Science. Students explore what to include in a portfolio, how to explain a project, where to put it, and how to introduce it to other people. The session provides examples and then makes room for individual work and questions.

## Open the workshop

Open `index.html` in a full browser. It is self-contained and also includes the Artifact collection and writing kit. `artifact.html` opens directly into that collection. Both are generated from the same content, not maintained separately.

The public app has four views: The session, In practice, Field guide, and Artifact. It has no model API, backend, student accounts, telemetry, or automatic external requests. It does not store student work. External resources open only when selected.

## Release 2.0.0

This revision replaces the earlier scaffolded curriculum with a simpler career workshop. The 11-screen session has no timings, clocks, speaker notes, diagnostic, required work card, or instructional-stage labels. Ways to get started offers 12 activities without a required intake. Artifact retains all 12 original portfolio selections, all five writing guides, and all nine reading selections.

Fluency, legibility, and reach remain introductory concepts. The Figma internship is an example of reading a task and designing an appropriate practice project. There is no custom SQL lab or technical grading by Career Services.

## Presenter materials

- `docs/print/facilitator-guide.pdf`: seven-page facilitator guide.
- `docs/print/run-sheet.pdf`: one-page running order.
- `docs/FACILITATOR.md` and `docs/SPEAKER-NOTES.md`: editable/generated text counterparts.
- `public/downloads/student-worksheet.pdf`: optional student notes sheet, also embedded in the app.

Presenter timings and instructions are not embedded in the student HTML. The source repository is public, so files under `docs/` are not confidential. Keeping them outside `public/` separates delivery, not access permission.

## Build

```sh
python3 -m pip install -r requirements-build.txt
python3 build.py
python3 tests/test_build.py
```

`build.py` builds the PDFs, both HTML entry points, and synchronized Markdown exports. The generated HTML is committed; students need neither Python nor Node.

For browser checks:

```sh
python3 -m pip install -r requirements-test.txt
python3 -m playwright install --with-deps chromium
python3 tests/test_native.py
```

See `docs/QA.md` for the test scope and actual results. The suite uses a temporary local HTTP server where allowed. Environments that block local navigation are explicitly labeled as document-injection tests.

## Source layout

- `content/session.json`: sequence and private-to-the-presentation facilitation cues.
- `content/slides/*.md`: visible slide copy.
- `content/guide-*.md`: field guide chapters.
- `content/resources.json`: activities, prompts, examples, and Artifact data.
- `content/sources.json`: dated source register.
- `src/`: markup, styles, and JavaScript.
- `public/`: intended static website output only.
- `docs/`: guides, handoff, release notes, and QA.
- `tests/`: checks for source, rendered interactions, and downloads.

No paid hosting, domain, API, or public visibility setting is enabled by the build. Read `docs/DEPLOYMENT.md` before hosting.
