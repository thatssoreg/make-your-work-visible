# Repository release verification

The reviewed source and generated release are committed to `thatssoreg/make-your-work-visible`. The repository was already public when accessed; this build did not change its visibility or enable a hosting service.

The first repository-native build completed successfully on October 6, 2026, local time, in GitHub Actions run `37559280400`. It restored the checksum-verified source, installed the pinned requirements, passed all 59 build checks and all 32 native-browser checks, then committed the expanded source and release at `66931aa2a5e44c54507f3b440fcc458d342166d1`.

The native report was read back from the repository and copied into this package with its Git blob SHA verified: `1b1cef2a0f449bb9ec4e4febe5cf8db989abcf04`. It is not a locally invented or simulated test report.

The original build environment's larger document-injection suite passed 252 checks. Its report and scope remain separate from native-browser checks. No real Safari/iPhone, manual screen-reader, projector, or student-learning evaluation is implied.

A subsequent build-only change sorts embedded PDF names so identical source produces consistent HTML ordering across file systems. It does not change the slide content, interface, or PDF bytes. That change passed the second repository build, run `37559621390`. The final remote `public/index.html` Git blob SHA is `ffa5065231faffc1aaa52b9c12ada83ae4e4f15f`, identical to the packaged HTML. Its SHA-256 is `48c31e05ee7e8e09fe49ddb2f3aed72ac66941a836ee5fbc6a4af97a3349ae27`.

The compressed `.release/` transport is a one-time repository-import mechanism. The expanded files in `src/`, `content/`, and the other documented source paths are the maintenance authority. The owner ZIP contains these ordinary files rather than requiring source-archive extraction.
