# Release validation

**Release:** 1.0.0, built from the approved scaffolding PRD.  
**Review date:** October 6, 2026.  
**Office:** SDS Career Services.

## Completed in the build environment

The final content/build suite passed **59 of 59 checks**. It checks the 40/45-minute timing, persistent work references, five starting conditions, seven help panels, eight timers, ten routes, the 12/5/9 Artifact inventory, contextual source references, script hashes, security policy, absence of remote runtime dependencies, and generated release materials.

The final Chromium document-injection suite passed **252 of 252 checks**. It exercises all five starting paths, context continuity, routing, help levels, model states, identical README criteria, all Artifact filters and writing guides, all ten route templates, dialog focus, keyboard movement, return navigation, clipboard-denial fallback, imports/exports, the three embedded PDF downloads, timers, and 45-minute behavior.

All fourteen task-only screens fit without vertical or horizontal page overflow at 1366 × 768, 1440 × 900, and 1920 × 1080. At 375 × 812 and 768 × 1024, all fourteen screens and the Artifact collection/writing kit were checked for horizontal overflow. Longer mobile content and expanded help intentionally scroll. These are viewport tests, not tests on physical phones or a classroom projector.

No uncaught runtime errors, console errors, or automatic network requests occurred in the tested interactions. Imported markup remained escaped. Invalid schema input was rejected. Exporting an edited work-card form did not silently replace the active card.

The nine-page facilitator guide, one-page run sheet, and two-page student worksheet were rendered and visually reviewed. They contain no embedded student work or redistributed font files.

## Important scope distinction

This build environment blocks ordinary file and HTTP browser navigation. The 252-check suite loads the exact generated HTML through document injection. Native storage failure was tested as a fallback; opt-in persistence, restoration, and clearing were separately tested with an explicitly labeled storage test double. Those checks do **not** establish native browser storage durability.

`tests/test_native.py` is a separate real-HTTP Chromium suite for an environment that allows local navigation. It uses actual browser storage and reload, real downloads, direct URLs, and a temporary local server. Its result is reported separately in `docs/NATIVE-TEST-RESULTS.json` only after it completes. Do not treat the existence of the script as a passed test. The repository build workflow runs this suite before committing generated release files.

No manual VoiceOver/screen-reader session, actual Safari/iPhone run, classroom-projector rehearsal, or observed student-learning evaluation has been completed. The planned active/application blocks total 28 of 40 minutes; that is a schedule calculation, not an observed engagement statistic. The workshop offers levels of help but is not an adaptive proficiency model or technical grader.

## Last preflight on the teaching laptop

Open the HTML in a full browser. Advance a slide, reveal a nudge, start/reset a timer, open an Artifact detail, and save a worksheet. Check a real external resource while signed out. Use the 40-minute setting unless the faculty segment leaves 45 minutes. Have the one-page run sheet and Post-its ready.

Machine-readable reports, test code, build inputs, and source dates accompany the release. Hosting is separate from repository source delivery; no public-site URL is implied by this report.
