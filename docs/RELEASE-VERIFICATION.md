# Release verification: practical workshop 2.0.0

The practical revision was built and committed to `thatssoreg/make-your-work-visible` at `116aabc06974a70e80c53550f672c02e2361f723`.

GitHub Actions run `37628415340` completed successfully. Its native HTTP browser suite passed 145 of 145 checks with no uncaught JavaScript errors or automatic external requests. The report was read back through the connected repository tool; its Git blob SHA is `4a4fd25d31f342480d89dd7aef5002edbf7148ae`.

Native report: https://github.com/thatssoreg/make-your-work-visible/blob/116aabc06974a70e80c53550f672c02e2361f723/docs/NATIVE-TEST-RESULTS.json

The owner download retains the local 142-check document-injection report, explicitly labeled by environment. Those 142 local checks are separate from the repository's 145 native HTTP checks; no native-device certification is implied. The 28 build checks passed locally and in the repository workflow.

The remote BUILD-MANIFEST.json was read back and matches the downloadable HTML:

- `public/index.html`: SHA-256 `791c268b489aa543c347dac69114afc8a489a284d492416f79def971f190e25f`
- `public/artifact.html`: SHA-256 `845d0ed53484692b1a42b00230285e02742db08234751f26d41b565c03e6d942`

The first revision-import attempt stopped before modifying source because the prior owner's ZIP contained a release-verification document that had not been committed. The missing document was reconciled against the exact prior package, and the unchanged source delta then applied successfully under the original checksum checks.

The website was not newly deployed, repository visibility was not changed, and no paid service was enabled. Actual presenter hardware, real Safari/iPhone use, and manual screen-reader testing remain human preflight items.
