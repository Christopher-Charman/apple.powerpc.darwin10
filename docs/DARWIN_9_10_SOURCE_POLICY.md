# Darwin 9–10 source selection policy

**Primary target:** PowerPC Leopard 10.5.x and Snow Leopard 10.6.x, including the community 10.6.8/A5 restoration. Never treat the existence of Apple OSS source as proof of a bootable community image.

## Release-bound source trees

| Target | Full tracked snapshot | Apple OSS tag | Commit |
| --- | --- | --- | --- |
| 10.5.x (Darwin 9) | `src/releases/10.5/xnu-1228.15.4/` | `xnu-1228.15.4` | `083332250d12f1d698a5c3282a18fee46847ec92` |
| 10.5.x | `src/releases/10.5/Libc-498.1.7/` | `Libc-498.1.7` | `7198b93dbba0617e5927ff5a5e783f0e54ff957b` |
| 10.6.x (Darwin 10) | `src/releases/10.6/xnu-1456.1.26/` | `xnu-1456.1.26` | `3ca3bd5593ac4736fb236ffd68a7ccb91ee6c0f0` |
| 10.6.x | `src/releases/10.6/Libc-594.9.1/` | `Libc-594.9.1` | `f7af6c31cc3078243c2d2e320e6af30e2de9813d` |
| 10.6.8-era kernel candidate | `src/releases/10.6.8/xnu-1504.15.3/` | `xnu-1504.15.3` | `99c11f3f90a18f35d3692ea77444b51fd972a4f4` |

The pinned `src/apple-darwin-10.6.8/` source superproject contains **353 Apple OSS gitlinks**, with root `.gitmodules` mappings restored for selective component checkout. These references are not all downloaded source bytes, and exact 10.6.8/A5 image membership remains unproven. The separately maintained `historical/SOURCE_LOCK.json` indexes **additional upstream components** as pinned gitlinks, including Libsystem, cctools, dyld, ld64, XNU and a different 10.6 Libc patch version. Those gitlinks are not full source snapshots. Preserve their exact revisions and reconcile candidate release membership with the real target build before promotion.

## Post-10.7 retention rule

Source after 10.7 is eligible **only** where a concrete component or isolated change is demonstrated architecture-neutral, or explicitly PPC/PPC64 compatible and relevant to Darwin 9/10. The proof must name the upstream commit, affected paths, target compiler/ABI, PPC architecture assumptions, dependencies and a bounded build or source-level verification. Otherwise exclude it from the project tree. Modern monolithic XNU and the macOS 11 Apple OSS distribution superproject are **not retained** in this branch; their upstream GitHub repositories remain available externally.

`toolchains/darwin-xtools/` is retained as a **separate modified PPC/PPC64-capable candidate**, not a drop-in 10.5/10.6 toolchain. Its README explicitly documents PPC/PPC64 support. Validate against era-specific cctools/ld64 before adoption.

## Source discipline

Keep pristine Apple release snapshots unchanged. Put porting patches in reviewable, separately attributed paths; do not overwrite an upstream tree in place. Preserve Apple and third-party license notices. A release-specific source candidate is distinct from community patch output, installed image contents, and actual PPC hardware runtime validation.

For the current build, establish source revision, compiler/linker, OS build, image digest, hardware model and boot ROM, then execute the [first diagnostic](FIRST_CURRENT_DIAGNOSTIC.md) and publish only evidence-backed gate transitions.

## Source parity recovered from project chronology

The project chronology records first-party source builds of **cups-218** (printing) and **libxml2-21** (XML runtime) on the modified 10A190_PPC line. Their complete official Apple OSS source trees are now imported at `src/releases/10.6/cups-218/` and `src/releases/10.6/libxml2-21/`, from exact upstream commits `254894616d00a03a51a36e2873c2928be4d050ed` and `1727d2fb2f5fad56a3dad1f1244143a23958f19b`. These are source-parity recoveries, not a reproduction of the historical binaries. Original contributor credit and source-built runtime evidence remain separate.

Other project-era components such as BootX, 10.6PPC KEXT donors, `OSInstall_10A190.mpkg`, `notifyd`, ImageIO and the A5 file-sharing/ALF remediation require distinct licensing, binary/source and version reconciliation before inclusion. Do not publish proprietary binaries or assume upstream OSS is equivalent to the modified runtime payload.

## Official release membership and toolchain parity

The `source-releases/` directory contains Apple's first-party `release.json` records for **all 10.5.1–10.5.8 and 10.6.0–10.6.8**. `python3 tools/verify_release_parity.py` compares these 17 manifests against pinned historical candidates. Candidate source tags that are not a member of the relevant first-party release must remain separately labelled; the 10.6.8 published toolchain is **cctools-750 and ld64-95.2.12**, not cctools-773/ld64-97.17. The exact 10.6.8 `Libc-594.9.5`, `cctools-750`, and `ld64-95.2.12` source trees are now fully vendored under `src/releases/10.6.8/`. This is a reproducible source baseline, not proof of a PPC-built runtime.

## XNU regression-comparison checkpoints

Additional complete official XNU snapshots are available at `src/releases/10.6.2/xnu-1486.2.11/` and `src/releases/10.6.3/xnu-1504.3.12/`. These permit direct, release-specific source comparison of the early Snow Leopard XNU transition before the 10.6.8 A5-associated baseline. A source delta alone is not evidence of PPC runtime regression or a justified reversion.

## Notification-service source uplift

The recovered 10A222 project evidence identifies the later Snow Leopard `notify-23` source rebuild as an important PPC-compatible successor-contract intervention when the older 10A190 notifier was insufficient. Exact Apple OSS sources now coexist for `notify-16` (10.5.8), `notify-23` (10.6.0), and `notify-25.1` (10.6.8) under their release-specific directories. The three source versions are suitable for contract and regression comparison. This does not recover Educovas' original compiled notifier, patches or boot logs, nor independently validate PPC runtime behaviour.

### Verified notify successor source delta

`docs/notify_23_to_25_1_source_delta.json` records four changed paths and review findings. The 10.6.8 daemon changes `_notify_lib_notify_state_new(0)` to `_notify_lib_notify_state_new(0, 1024)`, a concrete successor library-contract difference; the MIG definition also moves to the SDK. This makes unqualified reversion to the earlier daemon unsafe as an automatic operation. Reconcile Libnotify and SDK-generated IPC interfaces before PPC build/boot acceptance.
