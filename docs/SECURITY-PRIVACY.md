# Privacy and runtime review

The reviewed app has no API key, model endpoint, backend, account connection, third-party runtime script, remote font, analytics, or automatic external request. The HTML embeds its CSS, JavaScript, content, and text downloads. Its CSP hashes the executable script and denies connection, object, form-submission, and base-URL capabilities.

The only learner context is an optional title, starting condition, and work-status value. It defaults to memory. The learner can opt into browser storage, export a JSON card, import a validated card, and clear the current and saved card. The app does not store substantive answers or read from GitHub, Handshake, or the device's other files.

Imports are limited to 32 KB and a versioned schema. Title length and enumerated values are checked. User-provided text is escaped before it appears in markup. Exporting a form does not silently commit its edits to the active card. Existing cards require confirmation before replacement or clearing.

All reference links are HTTPS and open with `noopener noreferrer`. They are intentionally chosen by the user and then follow the destination's own policies. An external portfolio's code, content, or host is not independently audited by this workshop.

Source and build checks verify the stated properties, and the UI suite observed no automatic network requests during tested interactions. This is a scoped review, not a claim of universal security certification. The untouched original Artifact app is not served by the new release; it used CDN assets, which have been removed from the execution path.
