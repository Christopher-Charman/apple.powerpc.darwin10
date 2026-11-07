# apple.powerpc.darwin10
PowerPC restoration and reconstruction of Darwin 10

## Architecture and project evidence

[Owned architecture context, implementation boundaries and historical evidence](docs/OWNED_ARCHITECTURE_CONTEXT.md). This dated reference does not substitute for current source, tests or live deployment acceptance.

## Owned source imports (review branch)

[Source integration and exact fork revisions](docs/SOURCE_FORK_INTEGRATION.md). The branch imports full XNU and Darwin PPC toolchain source snapshots, plus a pinned 229-component Apple OSS submodule graph. The macOS 11 source graph and later XNU tree are reference inputs, **not** the current 10.6.8 PPC/A5 target source. Preserve build-specific provenance and only fetch selected component submodules when needed.
