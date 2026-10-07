# Privacy and runtime behavior

Release 2.0.0 removes the learner work card and all local-storage functionality. No student notes, files, accounts, or repository contents are received or stored by this app. URL fragments select a page or slide; they do not contain learner information.

Both entry points are static HTML. There are no model APIs, credentials, analytics, backend functions, remote fonts, or external runtime libraries. The content security policy denies connections, form submissions, objects, and base changes and allows only the hashed application script. External links are deliberate user actions. External products have their own terms, access conditions, and potential costs.

Downloads are generated from bundled text or PDFs. Prompts do not execute. The user's original Artifact source is preserved separately for provenance, not executed by the release.

Presenter files are outside `public/` and are not embedded in the student app. The repository itself is public: the folder boundary is not a confidentiality mechanism. Never add private student work, credentials, employer material, or the internal job-board workbook to this repository.

These observations and automated checks are not an independent security audit.
