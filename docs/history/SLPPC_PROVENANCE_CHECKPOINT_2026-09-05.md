# SLPPC Provenance Checkpoint — 2026-09-05

**Status:** MIGRATED HISTORICAL EVIDENCE — NOT CURRENT BUILD/IMAGE STATE  
**Project:** PowerPC Apple/Darwin / SLPPC  
**Source evidence:** Shared Library `SLPPC_CONSOLIDATED_BUILD_PROVENANCE_REPORT_2026-09-05.pdf` and comparative provenance report lineage.

## Purpose
Preserve the high-value provenance conclusions from the September evidence reconstruction in the dedicated PowerPC/Darwin repository so future agents do not have to recover them from old chats or an unindexed PDF before making source/image attribution claims.

## NFS/autofs provenance conclusion at this boundary
Direct archive inventory did not establish a recovered community rebuild of Snow Leopard NFS userspace. Apple source lineage was known (`NFS-42` for 10.6 and `NFS-42.1` for 10.6.8), but the installed A5 implementation still required direct fingerprinting before lineage could be assigned.

`autofs` was the adjacent exception: community build evidence attributed an autofs build to Educovas, while exact integration into the A5 image remained unresolved.

Kernel/NFS-VFS attribution likewise required binding the exact installed A5 kernel generation. Educovas had exact GM-era PPC XNU output in the evidence lineage, but later kernel work was a separate lineage and could not be silently projected onto A5.

Separate file-sharing remediation material contained NetFS/AppleShare/smbfs artefacts. Those were architecturally adjacent to Finder/network mounts but were not evidence of an NFS implementation rebuild.

## Required empirical sequence
The preserved controlled sequence was:

- **A — Original author-held A5:** fingerprint binaries, services, kernel generation and residual network/user configuration before intervention.
- **B — Sanitized A5 only:** determine which symptoms are caused by residual development-machine state.
- **C — Sanitized A5 + minimal validated NFS remediation:** isolate the functional effect of the remediation.
- **D — Restore B and reapply C:** establish reproducibility rather than accepting a one-off state transition.

Do not skip the original-A5 evidence capture by applying a repair first.

## Provenance promotion discipline
The evidence model distinguished:
`COMPILED -> OUTPUT_RETAINED -> ARCHIVED_OR_DISTRIBUTED -> BYTE_RECOVERED -> INSTALLED_IN_IMAGE -> RUNTIME_VALIDATED`.

A stronger state requires evidence for that state; source/build/community attribution alone does not prove image installation or runtime validation.

## Highest-value closure work recorded
1. Capture exact original A5 hashes/versions and residual configuration before sanitation.
2. Recover Educovas' 231-project archive and preserved modified-source corpus.
3. Recover the 14-Oct and 18-Oct Replaced Files archives and bind per-file image use.
4. Recover the exact `projects to build.txt` attachment.
5. Compare retained BUILD outputs against donor/source/replacement corpora and A5 filesystem hashes.
6. Fingerprint NFS/autofs/XNU/NetFS/SystemConfiguration/Finder-facing components and execute the controlled sanitation/remediation sequence above.

## Currentness rule
This checkpoint is historical provenance evidence. Newer project manifests, recovered bytes, image fingerprints and real-hardware validation supersede it where they provide stronger evidence. Do not infer current A5/10A190/10A222 state from this file alone.
