# PowerPC development tree contract

The `PowerPC` branch is the canonical, evolving PowerPC Darwin 10 source development tree. `main` remains a reference branch. This supersedes any description of `PowerPC` as a source-import-only review branch.

## Source layout and integration

- `src/releases/`, `historical-vendored/` and `source-releases/` are immutable, provenance-preserving upstream comparison inputs, not the patched development output.
- `src/apple-darwin-10.6.8/` contains pinned Apple component gitlinks; a gitlink is not an in-repository patch or a checked-out source file.
- Integrate PowerPC modifications into full, tracked working component trees, with their upstream version, provenance, dependencies, license and patch rationale retained. Do not treat a manifest, patch catalogue, build probe, or submodule pointer as a substitute for a patched source tree.
- Analyse successive official Apple Darwin 9/10 releases at file and semantic levels. Identify removed PPC/PPC64 code, architecture-specific compiler/build restrictions, ABI and endianness assumptions, Mach-O/loader changes, kernel and driver dependencies, and cross-component API/IPC changes.
- Revert only incompatibilities proven by source comparison and bounded tests. Preserve compatible security, correctness and API updates. A blanket rollback to Leopard is not acceptable.
- Reconcile the historical Snow Leopard PowerPC development work and donor changes with official release-specific source; retain attribution and do not import unauthorized proprietary binaries.
- Prefer a complete, reproducible PowerPC-patched 10.6.8 component graph, including kernel, userland, libraries, services, build tools and supported drivers. Record unpatched or unverified components explicitly rather than claiming completeness.

## Acceptance

A component is integrated only when its actual patched source is tracked on `PowerPC`, its upstream reference is pinned, the patch is reviewable, and PPC32/PPC64 (where applicable) build, ABI, linking and relevant runtime checks are recorded. System completion additionally requires a reproducible full build and hardware boot/userland verification. Existing historical Aqua boots and A5 evidence remain historical evidence, not a new build certificate.

## Baseline recovery

On 2026-11-21 `PowerPC` was fast-forwarded from `d1874f14bc2bf84f54c2a8d606d4ab0eb752ba9e` to `c8581a47125b4c2f885e7026a89f20982da17949` (139 existing commits), restoring the combined integration, release source inventories and qualification tooling. This operation did not itself apply new PowerPC patches to every component. The source integration objective remains active.
