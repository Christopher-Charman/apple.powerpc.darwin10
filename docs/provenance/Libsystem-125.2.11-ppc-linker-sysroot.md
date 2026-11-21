# Libsystem-125.2.11 linker sysroot variable correction

Upstream reference: `src/releases/10.6.8/Libsystem-125.2.11/Makefile` (immutable). The PowerPC working Makefile was identical before this edit.

The LINKDYLIB command already includes the defined `$(SDKROOTLDFLAGS)` before `-o`, but later expands misspelled, undefined `$(SKDROOTLDFLAGS)` after `$(ORDERFILES)`. Remove the dead typo expansion rather than adding a duplicate `-syslibroot` flag. The defined SDKROOTLDFLAGS and architecture-specific PPC linker settings remain unchanged. This is a source/build correctness cleanup, not a verified full Libsystem build.

Incremental diff: `patches/Libsystem-125.2.11-ppc-linker-sysroot.patch`. No compilation on the hosting runtime.
