# dyld-132.13 PowerPC static-library architecture selection

Official upstream: `src/releases/10.6.8/dyld-132.13/dyld.xcodeproj/project.pbxproj`, unchanged; the working project already has earlier PPC-specific changes preserved here.

Two non-PowerPC-pinned static-library target configurations depended on the build host: `dyldapis` Debug used `$(NATIVE_ARCH_ACTUAL)`; `dsc` Release used `$(ARCHS_STANDARD_32_64_BIT)`. Set both to `ppc` for the PowerPC development tree. Other configurations and architecture selections remain untouched, including dyld's existing PPC-specific base address and exception-library settings. This patch does not claim a complete dyld PPC loader/ABI port.

Incremental diff: `patches/dyld-132.13-ppc-static-library-arch.patch`. No build on the hosting runtime; compile/link/boot verification outstanding.
