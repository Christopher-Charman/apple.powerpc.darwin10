# IOUSBMassStorageClass-267.0.1 PowerPC architecture pin

Source: Apple Mac OS X 10.6.8 IOUSBMassStorageClass-267.0.1, preserved byte-for-byte in `src/releases/10.6.8/IOUSBMassStorageClass-267.0.1/`.

The 10.6.8 working project matched the immutable release project before this change. Nine target/configuration settings used `ARCHS = "$(NATIVE_ARCH_ACTUAL)"`, which selects the build host CPU rather than the PowerPC target. All seven explicit `VALID_ARCHS` settings already include `ppc`. Pin the nine architecture selectors to `ppc` in the editable PowerPC development source only; do not modify the release snapshot.

The source-level edit is recorded in `patches/IOUSBMassStorageClass-267.0.1-ppc-arch.patch`. This is a cross-host PPC32 target selection correction, not proof of compilation, ABI, link, device functionality, or PPC64 support. No compilation was performed.
