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

The separately maintained `historical/SOURCE_LOCK.json` indexes **additional upstream components** as pinned gitlinks, including Libsystem, cctools, dyld, ld64, XNU and a different 10.6 Libc patch version. Those gitlinks are not full source snapshots. Preserve their exact revisions and reconcile candidate release membership with the real target build before promotion.

## Post-10.7 retention rule

Source after 10.7 is eligible **only** where a concrete component or isolated change is demonstrated architecture-neutral, or explicitly PPC/PPC64 compatible and relevant to Darwin 9/10. The proof must name the upstream commit, affected paths, target compiler/ABI, PPC architecture assumptions, dependencies and a bounded build or source-level verification. Otherwise exclude it from the project tree. Modern monolithic XNU and the macOS 11 Apple OSS distribution superproject are **not retained** in this branch; their upstream GitHub repositories remain available externally.

`toolchains/darwin-xtools/` is retained as a **separate modified PPC/PPC64-capable candidate**, not a drop-in 10.5/10.6 toolchain. Its README explicitly documents PPC/PPC64 support. Validate against era-specific cctools/ld64 before adoption.

## Source discipline

Keep pristine Apple release snapshots unchanged. Put porting patches in reviewable, separately attributed paths; do not overwrite an upstream tree in place. Preserve Apple and third-party license notices. A release-specific source candidate is distinct from community patch output, installed image contents, and actual PPC hardware runtime validation.

For the current build, establish source revision, compiler/linker, OS build, image digest, hardware model and boot ROM, then execute the [first diagnostic](FIRST_CURRENT_DIAGNOSTIC.md) and publish only evidence-backed gate transitions.
