# Tracked PowerPC development sources: 10.6.8

`src/powerpc/` is the **tracked, editable PowerPC working source tree**. It began with all 326 project directories from the exact official 10.6.8 release snapshot, with the initial source-bound architecture patches materialized in their actual Xcode project files. Subsequent reviewed PowerPC commits have modified additional project configurations, source files and build scripts. This is a real Git tree of ordinary files and directories, **not gitlinks or a patch-only catalogue**. Git object sharing avoids duplicating unchanged upstream blobs.

The pristine upstream comparison tree is `src/releases/10.6.8/`. Its Git tree object is `a706ce871183ebfe4b3ea9f9220b65e21475314d`. The development source was created by copying that tree as a Git tree, then applying each `patches/*.patch` independently to its corresponding working file with strict zero-fuzz application. The patch catalogues and source-pinned manifests remain historical provenance, not substitutes for the working files.

**Current coverage:** 326 baseline source-project directories, plus incremental PowerPC modifications with per-change patches, provenance and regression tests. The original 17 materialized patches across 16 projects (including both IOUSBFamily project files) describe the initial import only, not the current total. Many projects remain upstream-identical and are **not yet PPC-adapted** merely because they appear here. In particular, architecture settings alone do not restore code paths, APIs, ABI compatibility or dependencies. Separately published and unavailable sources still require dependency closure.

**Restriction:** No compilation is permitted on PowerPC-Darwin.org. All changes here are source-only; do not claim build, link or hardware validation from source checks. Subsequent development must edit `src/powerpc/` and retain provenance, updating patch metadata when appropriate.

## Continuing source-level restoration

The PowerPC branch is the authoritative integration target. New changes must retain the upstream comparison, exact working-tree diff and source provenance; regression tests belong in the required source-graph workflow. The IOATA register guard, dyld architecture and assembly checks, Libsystem linker correction and XNU PPC KPI export generator are examples of subsequent work, not evidence of complete boot readiness.

The existing dependency-source inventory distinguishes release-exact vendored sources from external or closed-source dependencies. Source-tree project count is not a dependency-closure or successful-build metric. Full PPC32/PPC64 ABI checks, hardware drivers, kernel link and boot verification remain acceptance requirements.
