# IOFireWireSerialBusProtocolTransport-210.0.0 PPC architecture pin

Official 10.6.8 source: `src/releases/10.6.8/IOFireWireSerialBusProtocolTransport-210.0.0/`, preserved without modification. Before the change, the editable PowerPC project file was byte-for-byte identical to this immutable release file.

All three project build configurations explicitly permit `ppc` in `VALID_ARCHS`, but their `ARCHS` values used `$(NATIVE_ARCH_ACTUAL)`, selecting the compilation host CPU rather than a PPC target. Pin the three `ARCHS` settings to `ppc` in the working tree. The exact patch is `patches/IOFireWireSerialBusProtocolTransport-210.0.0-ppc-arch.patch`.

This change only establishes consistent PPC32 source-target selection. FireWire family dependencies, ABI/linking, runtime and hardware behavior remain unverified. No compilation or build was performed on the host.
