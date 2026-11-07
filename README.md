# apple.powerpc.darwin10
PowerPC restoration and reconstruction of Darwin 10

## Architecture and project evidence

[Owned architecture context, implementation boundaries and historical evidence](docs/OWNED_ARCHITECTURE_CONTEXT.md). This dated reference does not substitute for current source, tests or live deployment acceptance.

## Owned source imports (review branch)

[Source integration and exact fork revisions](docs/SOURCE_FORK_INTEGRATION.md). The branch imports the exact Apple XNU 1504.15.3 source snapshot and the 353-component Mac OS X 10.6.8 source graph as the primary historical baseline; it also preserves a newer XNU fork, Darwin PPC toolchain sources and a separate 229-component macOS 11 reference graph. The macOS 11 source graph and later XNU tree are reference inputs, **not** the current 10.6.8 PPC/A5 target source. Preserve build-specific provenance and only fetch selected component submodules when needed.

## Historical Leopard and Snow Leopard sources

[Darwin 9 (10.5.x) and Darwin 10 (10.6.x) source inventory](docs/HISTORICAL_RELEASE_SOURCES.md) includes complete checked-in XNU 1228.15.4, 1456.1.26 and 1504.15.3 trees, plus 14 pinned upstream source component revisions across the two release families. Run `python3 tools/verify_historical_sources.py` to verify historical gitlink and source-lock consistency. The source inventory is not a bootable image or complete per-point-release build manifest.
