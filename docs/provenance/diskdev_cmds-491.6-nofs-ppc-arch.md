# diskdev_cmds-491.6 nofs PowerPC release selection

`diskdev_cmds-491.6` is the official Apple 10.6.8 release member in `source-releases/10.6.8.json`; its source is under APSL 2.0. The pristine `src/releases/10.6.8/diskdev_cmds-491.6/nofs.tproj/Makefile` blob is `d745db28a3d16897b6bd946091a0b3f707ab28a2` and remains unchanged. The working Makefile was identical before this patch.

The parent `diskdev_cmds` Makefile includes `nofs.tproj`, a filesystem utility that uses DiskArbitration, CoreFoundation, IOKit and SystemConfiguration interfaces. Its release-control `RC_ARCHS` explicitly omitted `ppc`, preventing a PowerPC source selection for this target. The patch adds `ppc` to that single list. It preserves the target's source, resources and all other upstream Makefile settings. Availability of the private DiskArbitration interface and runtime behavior on the target system remain to be verified.

Patch: `patches/diskdev_cmds-491.6-nofs-ppc-arch.patch`. Source-only regression: `tests/test_diskdev_nofs_ppc_arch.py`. No compilation, linking, build or hardware testing was performed or authorized.
