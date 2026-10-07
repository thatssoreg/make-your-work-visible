# Repository release 2.0.0

The practical revision replaces the scaffolded live interface. Canonical source remains in `src/` and `content/`; generated files are built and verified before the workflow commits them. Release transport files, when used by the connected GitHub tool, are checksum-checked and applied only to enumerated source paths.

The prior release remains in Git history. No repository visibility, paid plan, or domain setting is changed. Presenter PDFs are generated under `docs/print`; the student static output is under `public/`.

Use the latest successful workflow result and BUILD-MANIFEST.json to identify the generated version. See QA.md and the machine-readable reports for testing scope.
