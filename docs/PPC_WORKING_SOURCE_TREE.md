# Tracked PowerPC development sources: 10.6.8

`src/powerpc/` is the **tracked, editable PowerPC working source tree**. It initially includes all 326 project directories from the exact official 10.6.8 release snapshot, with the 17 existing source-bound architecture patches materialized in their actual Xcode project files. This is a real Git tree of ordinary files and directories, **not gitlinks or a patch-only catalogue**. Git object sharing avoids duplicating unchanged upstream blobs.

The pristine upstream comparison tree is `src/releases/10.6.8/`. Its Git tree object is `a706ce871183ebfe4b3ea9f9220b65e21475314d`. The development source was created by copying that tree as a Git tree, then applying each `patches/*.patch` independently to its corresponding working file with strict zero-fuzz application. The patch catalogues and source-pinned manifests remain historical provenance, not substitutes for the working files.

**Current coverage:** 326 baseline source-project directories; 17 materialized patch files across 16 projects (including both IOUSBFamily project files). Other projects are still upstream-identical and are **not yet PPC-adapted** merely because they appear here. In particular, architecture settings alone do not restore code paths, APIs, ABI compatibility or dependencies. Separately published and unavailable sources still require dependency closure.

**Restriction:** No compilation is permitted on PowerPC-Darwin.org. All changes here are source-only; do not claim build, link or hardware validation from source checks. Subsequent development must edit `src/powerpc/` and retain provenance, updating patch metadata when appropriate.
