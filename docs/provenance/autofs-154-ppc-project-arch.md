# autofs-154 PowerPC project selection

`autofs-154` is the official Apple 10.6.8 source member in `source-releases/10.6.8.json`, under the Apple Public Source License 2.0. The pristine `src/releases/10.6.8/autofs-154/autofs.xcode/project.pbxproj` blob is `323b5617e3f279887bfb7d10e66a5d3a61f5eeac` and remains unchanged. The working project file matched it before this patch.

All eight autofs products (`autofs`, `mount_autofs`, `autofs-package`, `files`, `mount_url`, `automountd`, `automount`, `autofsd`) had Debug and Release configurations selecting only `i386` and `x86_64`. The 10.6.8 source still contains explicit `__ppc__` handling for automounter ISA and CPU naming. This patch restores `ppc` to the 16 selected- and valid-architecture lists without altering other project settings or the existing PowerPC code paths. The autofs kernel module and userland helpers are source producers for automounting; XNU/IOKit, DiskArbitration, launchd and filesystem services remain dependency interfaces to verify.

Patch: `patches/autofs-154-ppc-project-arch.patch`. Regression: `tests/test_autofs_ppc_arch.py`, run as source-only Python assertions. PPC compilation, linking, build and hardware behavior remain unverified and are prohibited in this work session.
