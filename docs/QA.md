# Quality checks: practical workshop 2.0.0

## Completed locally

- 28 source/build checks passed.
- 142 browser checks passed in Chromium using document injection because this environment denies local HTTP navigation.
- All 11 screens and interactive example states were checked at 1440 by 900; the short-height projector layout was additionally checked at 1366 by 768, including the alternate Figma, README, presence, and sharing panels.
- Mobile-width checks used 375 by 812. This is a browser viewport test, not an actual iPhone.
- The seven-page facilitator guide, one-page run sheet, and one-page student worksheet were rendered and visually inspected.

The browser suite checks the absence of timing/presenter controls, all 12 activities, all ten field-guide sections, source filtering, both main and alternate examples, Markdown and PDF downloads, all 12 Artifact portfolios, five six-part writing guides, nine reading selections, return navigation, keyboard navigation, horizontal overflow, projector/footer clearance, uncaught errors, and automatic external requests.

## Native-browser evidence

`NATIVE-TEST-RESULTS.json` records the environment and results of the latest run. The test uses a real temporary HTTP server when permitted and labels document injection explicitly when the environment denies navigation. Native HTTP adds standalone Artifact entry, direct-slide URL, and actual reload checks. Never describe an injection run as a hosted or native-device test.

## Remaining human checks

The actual presenter laptop, classroom projector, real Safari/iPhone hardware, and manual screen-reader use need a human preflight. Pacing and student learning cannot be certified by these tests. The site has not been newly deployed as part of this revision.

## Source checks

New platform and portfolio guidance uses official GitHub, Wix, Squarespace, and Open Source Guides references. The Figma listing was checked on October 7, 2026. Existing Artifact and tool-offer references keep their individual check dates; they were not all revalidated during this edit.
