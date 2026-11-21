# IOATAFamily-251.0.1 PPC architecture pin

Official 10.6.8 source: `src/releases/10.6.8/IOATAFamily-251.0.1/`, preserved without modification. Before the change, the editable PowerPC project file was byte-for-byte identical to this immutable release file.

The project contained four `ARCHS = "$(NATIVE_ARCH_ACTUAL)"` settings and four `ARCHS = "$(NATIVE_ARCH)"` settings, selecting the host CPU rather than the PowerPC target. All eight architecture settings are pinned to `ppc` in the working source. The exact source diff is `patches/IOATAFamily-251.0.1-ppc-arch.patch`. This project does not define explicit `VALID_ARCHS` settings in its project file; no such claim is made.

This corrects PPC32 target selection only. ATA downstream transport dependencies, ABI/linking, runtime and hardware behavior remain unverified. No compilation or build was performed on the host.
