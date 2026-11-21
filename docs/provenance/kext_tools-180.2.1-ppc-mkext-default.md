# kext_tools-180.2.1: restore PPC kextcache mkext selection

## Exact source and donor

- Target: Apple Mac OS X 10.6.8 OSS release member `kext_tools-180.2.1`, upstream annotated tag `e14d621a5e3fb38adaaddc1218a7c13a92f56c8b`, commit `02f62e8e0ee729ceca91f359a2d818a49938cb63` in `apple-oss-distributions/kext_tools`.
- Immutable local comparison tree: `src/releases/10.6.8/kext_tools-180.2.1/`, Git tree `191e8d87a847864dde821469ffd23b10315e31c2`.
- Earlier PowerPC-capable comparison: Leopard 10.5.8 release member `kext_tools-117.4`, upstream tag `2b3eaf0641bb3053e6ce9ed77d357ad9dcefcec9`, commit `7288a48ef299e8efb85f68ae102475ccb3f3b03c`. Its `kextcache_main.c` used a generic mkext when no architecture was specified and selected the local architecture for kernel cache creation. This is behavioral evidence, not a file copied into the 10.6.8 tree.
- License: Apple Public Source License 2.0, retained in `APPLE_LICENSE` and the source header.

## Working-source mutation

`src/powerpc/kext_tools-180.2.1/kextcache_main.c` previously selected only `i386` and `x86_64` for an mkext without explicit `-arch`, even on a PPC host. Its existing mkext path already has PPC filtering and an Open Firmware size guard, but those paths were unreachable by default. The change selects the generic `ppc` slice on a PPC32 kernel and `ppc64` on a PPC64 kernel. If the IOKit registry query returns an unknown architecture, the code falls back to `NXGetLocalArchInfo()`, the host architecture API used by the Leopard donor. The existing Intel default and explicit `-arch` behavior remain as written.

The project-wide `VALID_ARCHS` in `src/powerpc/kext_tools-180.2.1/kext_tools.xcodeproj/project.pbxproj` excluded both PPC architectures in Development, Deployment and Default. These three settings now admit `ppc` and `ppc64`; target-specific architecture lists still determine which products are requested. The exact source edits are in `patches/kext_tools-180.2.1-ppc-mkext-default.patch`. The release snapshot remains untouched.

## Dependency and evidence boundary

`kextcache` consumes the `OSKextGetRunningKernelArchitecture` interface from `IOKitUser-514.16.50` (whose source may return an unknown architecture record on registry lookup failure), Mach CPU types from the XNU/SDK headers, and Mach-O architecture metadata from `cctools-750`; its mkext is consumed by the boot path and kernel extension loader. Those interfaces and the full dependency closure still need PPC32/PPC64 build, link and hardware checks.

Source-only checks: the working files exactly matched their immutable release counterparts before this edit; one architecture-default branch and three project-level architecture settings were changed. The donor and exact release tag were inspected through authenticated GitHub API. No compilation or boot validation was performed on this host.
