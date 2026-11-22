# dtrace-78 PowerPC architecture path

`dtrace-78` is the official Apple 10.6.8 release member in `source-releases/10.6.8.json` under APSL 2.0. The pristine release blobs are `a9809564398e789eda345e040aaade2846b638c2` (`head/arch.h`) and `57c60bcea2b530b00c0522d537af16a65dbc1089` (`dtrace.xcodeproj/project.pbxproj`); both remain unchanged. Their `src/powerpc/` working files matched before this patch.

The DTrace CLI accepts an `-arch` value through `arch_for_string()` and passes `string_for_arch()` to libdtrace. `dt_options.c` already accepts `CPU_TYPE_POWERPC` and `CPU_TYPE_POWERPC64`, but `head/arch.h` had neither text mapping and raised `#error Unsupported architecture` for a PowerPC host. The patch adds `ppc` and `ppc64` mappings consistent with the pinned 10.6.8 `cctools-750/libstuff/arch.c` names, and selects the appropriate `host_arch` for PowerPC and PowerPC64. This also lets `dt_ld.m` use its existing byte-swap decision for PowerPC hosts.

The project-level architecture macro already includes `ppc`, but both project configurations and the Debug/Release configurations of nine DTrace and CTF products reject it through `VALID_ARCHS`. The patch adds `ppc` to those 20 lists, retaining all other settings. The target lists do not enable `ppc64`; the parser recognizes that target name because libdtrace already accepts it, but a 64-bit host build remains unverified. DTrace kernel interfaces, symbol/relocation handling, toolchain stages and runtime tracing still require independent verification.

Patch: `patches/dtrace-78-ppc-arch.patch`. Regression: `tests/test_dtrace_ppc_arch.py`. All checks are source-only; no compilation, linking, builds or hardware tests were performed or authorized.
