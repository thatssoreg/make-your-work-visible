# Verified first-import transport

These ordered UTF-8 base64 parts contain the reviewed source archive for release 1.0.0. The build workflow checks the joined archive's SHA-256 before restoring only allowed regular files, then builds and runs the content and native-browser checks before committing the expanded source and public release.

This transport exists because the connected repository tool accepts text, not local archive uploads. After import, maintain the ordinary files in `src/`, `content/`, `docs/`, and `tests/`; do not edit or regenerate these transport parts. Subsequent builds use those expanded source files directly.

No student data, job-board workbook, API keys, private account records, or font files are included. This workflow does not enable hosting or change repository visibility.
