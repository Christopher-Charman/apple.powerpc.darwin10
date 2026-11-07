# apple.powerpc.darwin10
PowerPC restoration and reconstruction of Darwin 10

## Architecture and project evidence

[Owned architecture context, implementation boundaries and historical evidence](docs/OWNED_ARCHITECTURE_CONTEXT.md). This dated reference does not substitute for current source, tests or live deployment acceptance.

## Owned source imports (review branch)

[Source integration and exact fork revisions](docs/SOURCE_FORK_INTEGRATION.md). The branch contains release-specific Leopard and Snow Leopard XNU/Libc source snapshots, a 353-component Mac OS X 10.6.8 Apple OSS source graph, and separately qualified PPC/PPC64-capable Darwin toolchain sources. The newer XNU whole-tree snapshot and macOS 11 graph have been removed from the branch tip. [Darwin 9–10 source selection policy](docs/DARWIN_9_10_SOURCE_POLICY.md) excludes post-10.7 sources unless an individual change is architecture-neutral or PPC-compatible. Preserve build-specific provenance and fetch only selected component submodules when needed.

## Historical Leopard and Snow Leopard sources

[Darwin 9 (10.5.x) and Darwin 10 (10.6.x) source inventory](docs/HISTORICAL_RELEASE_SOURCES.md) includes complete checked-in XNU 1228.15.4, 1456.1.26 and 1504.15.3 trees, plus 14 pinned upstream source component revisions across the two release families. Run `python3 tools/verify_historical_sources.py` to verify historical gitlink and source-lock consistency. The source inventory is not a bootable image or complete per-point-release build manifest.
