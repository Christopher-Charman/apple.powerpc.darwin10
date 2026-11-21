# Snow Leopard 10.6.8 for PowerPC — Darwin 10 source development

Community reconstruction of Mac OS X 10.6.8 / Darwin 10 for PowerPC G4 and G5 Macs. The goal is a **reproducible, fully PowerPC-adapted source tree**, with validated kernel, userland, libraries, services, build tools and supported drivers, leading to a functional, independently tested system.

**Development branch:** [`PowerPC`](../../tree/PowerPC) is the canonical PowerPC development tree. **`main`** is a repository reference/landing branch, not the completed patched source distribution. See the [development-tree contract](../../blob/PowerPC/docs/POWERPC_DEVELOPMENT_TREE.md) and [Darwin 9–10 source selection policy](../../blob/PowerPC/docs/DARWIN_9_10_SOURCE_POLICY.md).

## Community project and historical releases

The [MacRumors Snow Leopard PowerPC WikiPost and testing hub](https://forums.macrumors.com/threads/10-6-snow-leopard-powerpc-development.2439769/) is the community-facing source for public images, installation guidance, hardware reports, historical engineering, developer tools and known issues. Its posts #1–3 distinguish the testing hub, engineering lineage and Xcode/developer-tools work. The [earlier Developer Preview discussion](https://forums.macrumors.com/threads/snow-leopard-on-unsupported-powerpc-macs.2232031/) covers separate preview investigations.

The historical sequence includes the 10A096 and 10A190 Developer Previews, community-modified `10A190_PPC` and 10A222 configurations, reconstructed 10A432/GM systems, intermediate updates and 10.6.8 Alpha releases. **Alpha 5 (A5), published 30 January 2025, remains the common public testing image**, not a certification that this Git branch builds or reproduces that image. Local A5 modifications, graphics variants and historical source-built components must retain separate identities and provenance.

The WikiPost documents selected boot-to-Aqua and hardware-specific graphics results, alongside unresolved or build-specific issues involving networking/DHCP, Finder/DiskImages/notifyd, acceleration/IOSurface, sleep, Security/Authorization, DirectoryService, Spotlight, printing, audio, and allocator performance. Do not generalize a result from one machine, image or donor set to every G4/G5 system.

## Source-tree engineering

The `PowerPC` branch preserves pinned official Apple Darwin 9/10 release inputs and historical donor sources. Its 10.6.8 Apple OSS graph contains 353 component gitlinks; **gitlinks are not patched, checked-out working trees**. Full official release snapshots and manifests support source-level comparison. These inputs are distinct from the future integrated PowerPC-patched output.

For each component:
1. Establish the exact official release member and upstream revision; compare successive Apple releases with the Leopard PowerPC baseline and community modifications.
2. Identify removed PPC/PPC64 paths, build-system exclusions, Mach-O/ABI and big-endian assumptions, kernel/KEXT contracts, framework symbols and cross-component API/IPC changes.
3. Restore or adapt only demonstrated PowerPC-incompatible changes while retaining compatible later security, correctness and interface fixes. Avoid blanket Leopard rollback.
4. Commit the **actual complete patched component source** in a tracked working tree, retaining upstream lineage, licenses, patch rationale, contributor attribution and reproducible build instructions.
5. Validate PPC32 and PPC64 where applicable, linking and dependencies, then test integrated userland, boot and relevant G4/G5 hardware. Record failures and unverified components explicitly.

Source inventory, compatibility probes and historical boot logs are useful evidence, but are **not** proof that all 10.6.8 sources have been patched or that a new bootable release exists.

## Build and testing evidence

The [historical source inventory](../../blob/PowerPC/docs/HISTORICAL_RELEASE_SOURCES.md), [source integration record](../../blob/PowerPC/docs/SOURCE_FORK_INTEGRATION.md) and [native PowerPC CI guidance](../../blob/PowerPC/docs/NATIVE_POWERPC_CI.md) provide current starting points. Validate the historical source lock with `python3 tools/verify_historical_sources.py` and official release membership with `python3 tools/verify_release_parity.py` from the `PowerPC` checkout.

For reproducible reports include exact source and image revisions/checksums, machine identifier, CPU/GPU/bus, firmware, boot method, changed components, test commands, logs and observed behavior. Separate **historical result**, **source-only check**, **patched build**, and **hardware-verified result**.

## Experimental software and provenance

Public experimental disk images may damage data or fail to boot. Use a spare disk/partition and backups; do not indiscriminately apply ordinary Apple updates. Follow the WikiPost's restore instructions and hardware-specific cautions. Preserve Apple and third-party licensing and attribution. Do not commit unauthorized proprietary system binaries, private archives or credentials.

This repository is the source-development owner; it is separate from the `powerpc-darwin.org` hosting/runtime service. [Project history and evidence](docs/OWNED_ARCHITECTURE_CONTEXT.md) provide historical context, not a live build certificate.
