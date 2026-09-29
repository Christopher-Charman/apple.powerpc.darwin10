# SLPPC Chat-History Reconciliation — 2026-09-29

Status: HISTORICAL ENGINEERING/PROVENANCE RECEIPT — NOT CURRENT BUILD MANIFEST

This document records the implementation spine recovered from current durable project evidence plus archived ChatGPT history. It preserves what was built/researched without promoting historical state to the present live image.

## Recovered engineering spine

- 10A190 remains the primary Snow-Leopard-proximate PowerPC engineering baseline and was demonstrated booting on real G4/G5 hardware with substantial Leopard/PPC component restoration.
- 10A222 reaches userspace but fails around the login path; its behavior is dependency-chain evidence rather than a kernel-only result.
- Later 10A432/GM and 10.6.8/A5 work includes PPC XNU/AOSS rebuilding, hybrid donor reconstruction, DarwinBuild/toolchain recovery and broad component testing.
- Concrete native toolchain lineage includes Xcode 3.2.6, darwin-developer-tools 1.1.0, PPC ld64 97.17 with the relevant LTO limitation/workaround, and Apple gnumake 3.81.
- Community/thread/wiki chronology, attribution/provenance work and public Post #2/#3 reconciliation were completed in depth.
- Chris-authored pre-GPT control artefacts remain editorial provenance and should not be overwritten by later assistant summaries.

## Currentness boundary

The historical evidence corpus is rich but does not identify the exact current build/image/hardware target by itself.

`HISTORICAL_PROVENANCE != CURRENT_BUILD_STATE`

Before the next engineering mutation, recover/create a compact current target/build manifest from fresh build/runtime evidence and bind all conclusions to that exact target.

## Cross-project synchronization

The cross-project reconciliation index is versioned in `Christopher-Charman/repository-prime` at:
`architecture/control-plane/IMPLEMENTATION_HISTORY_RECONCILIATION_2026-09-29.md`.

That cross-project document is routing/history evidence only; this repository remains primary source authority for SLPPC implementation where established.
