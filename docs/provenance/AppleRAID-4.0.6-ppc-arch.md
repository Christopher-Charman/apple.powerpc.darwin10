# AppleRAID-4.0.6 PPC architecture pin

Official Apple 10.6.8 source: `src/releases/10.6.8/AppleRAID-4.0.6/`. The PowerPC working project already differs from the immutable Apple snapshot: nine `VALID_ARCHS` settings explicitly include PPC. Preserve those existing edits.

Twelve build configurations still used `ARCHS = "$(NATIVE_ARCH_ACTUAL)"`, selecting the host architecture rather than the intended PowerPC build target. Replace those twelve selectors with `ARCHS = ppc`, without changing the existing PPC-inclusive `VALID_ARCHS` settings. The exact incremental patch is `patches/AppleRAID-4.0.6-ppc-arch.patch`.

This is PPC32 source-target selection only. RAID kernel and userspace dependencies, ABI, linking, runtime and hardware behavior remain unverified. No compilation was performed on the host.
