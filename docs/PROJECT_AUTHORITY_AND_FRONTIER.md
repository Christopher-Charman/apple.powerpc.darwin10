# PowerPC Darwin 10 — project authority and engineering frontier

This repository is the **versioned source and engineering evidence owner** for the PowerPC Darwin 10 / Snow Leopard reconstruction project. It is **not** the deployment repository for powerpc-darwin.org.

## Authoritative project records

The current project-owned ChatGPT Library workspace is `/Project Workspaces/powerpc.apple.darwin/`:

| Record | Role |
| --- | --- |
| `PROJECT_GOVERNANCE.md` | Adopted project methodology, target-specific evidence rules |
| `PROJECT_MANIFEST.json` | Project classification, verified historical baseline, current-build frontier |
| `PROJECT_CONTINUITY.md` | Non-authoritative recovery/navigation |
| `COMMUNITY_ISSUE_EVIDENCE_LEDGER.md` | Primary normalized forum issue and claim provenance |
| `10.6.8_A5_EVIDENCE_RECONCILED_BACKLOG.md` | Derived A5 issue families A5-R01 onward |
| `10A222_EVIDENCE_RECONCILED_BACKLOG.md` | Separate 10A222 evidence and controls |
| `SLPPC_RUN_CHECKPOINT.md` | Bounded 10A432 OSS inventory and prerequisite research |
| `SLPPC_10_6_8_POWERPC_TECHNICAL_PROGRESSION_CHRONOLOGY_V3_2026-09-05.md` | Historical build chronology and contributor lineage |
| `SLPPC_ATTACHMENT_CENSUS_MASTER_2026-09-03.md` | Attachment identity census, not proof of payload inspection |

These Library files are not silently replaced by GitHub copies. This document is a **dated navigation projection**, not a competing project manifest. Verify the current owner records before changing technical conclusions.

## Historical engineering facts and distinctions

- Community `10A190_PPC` is not stock Apple 10A190. 10A096, 10A190_PPC, modified 10A222, 10A432 and 10.6.8 A5 require separate provenance and validation.
- Patched 10A222 boot-to-Aqua on selected G4 hardware, subsequent 10A432 recovery and the public **10.6.8 Alpha 5 release on 2025-01-30** are historical achievements, not new current-build acceptance.
- A5-associated project logs record Darwin 10.8.0 / XNU 1504.15.3 PPC and subsystem errors, but a log alone does not bind the currently available image and machine.
- Distinguish original ChrisCharman BUILD.zip/150+ source-project methodology, later Educovas modifications and shims, and individual contributors' testing and validation. Do not conflate attribution stages.
- A5 network issues are separate DHCP, DNS/UDP, ALF, file-sharing/discovery and NFS test families. A workaround or preserved repair package is not a validated fix.
- The 10A432 retail source-release inventory is a **scoped inventory target**, not an automatic selection of the project's universal kernel/build target.

## Adopted engineering procedure

`PROVENANCE -> TARGET/FREEZE -> DIFF -> CLASSIFY -> CONTRACT -> IMPLEMENT -> COMPILE -> LINK/ARTEFACT_VERIFY -> BOOT -> RUNTIME/SEMANTIC VALIDATE`

For dependency inventory: establish the exact OS release, source membership, installed artefact identity, source coverage and producer/consumer edges before claiming required build prerequisites. PPC capability of a compiler is distinct from host support, selected target architectures and the correct component build.

Record evidence states separately: historical report, source-tested, boot-observed, runtime-verified and independently accepted. Preserve negative results and contradicted/superseded hypotheses. Avoid publication of proprietary Apple images, unlicensed donor binaries, private attachments, personal exports or credentials.

## Current engineering frontier

As of the Library project manifest verified **2026-09-29**, `current_build_manifest=NOT_ESTABLISHED`. No newer exact hash-pinned build/image/hardware acceptance is established by this projection. Do not mark #3 or #2 complete based on historical A5 logs or a GitHub commit.

- [#3](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/3): exact current source/build/image/hardware manifest and G4/G5 acceptance, with evidence-classified A5 issue backlog and the November 2026 Xbench allocator report.
- [#1](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/1): executable experiment/provenance contract, proposed in [PR #7](https://github.com/Christopher-Charman/apple.powerpc.darwin10/pull/7).
- [#2](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/2): first **fresh** diagnostic only after #1 and the current identity gate.
- [#4](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/4): historical attribution and attachment lineage closure; separate from present-day runtime acceptance.

The November 2026 A5-vs-Leopard Xbench memory-allocation report is a **new reproducibility hypothesis**, not a confirmed allocator root cause. In particular, the suggested `posix_memalign` link is unverified until the exact Xbench call path and loaded libraries are identified.

## Completion standard

A new build claim needs the exact image and source hashes, toolchain versions, machine model/firmware/CPU/GPU, bootloader, installed component manifest, reproducible procedure, logs, negative controls, boot results and runtime semantic tests. Every acceptance claim must link to the evidence that supports its exact scope. Library and GitHub alignment must be checked against the latest owner records rather than this dated projection.
