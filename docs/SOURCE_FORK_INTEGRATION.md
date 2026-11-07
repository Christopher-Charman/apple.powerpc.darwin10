# Owned source-fork integration — 2026-11-07

This source import is an **engineering input**, not a claim of Snow Leopard 10.6.8 build, compatibility or live boot acceptance. Keep the project governance and current-build manifest in the native ChatGPT Library as the methodology/current-state authority.

| Namespace | Owned fork | Imported revision | Integration type |
| --- | --- | --- | --- |
| `src/xnu/` | [Christopher-Charman/xnu](https://github.com/Christopher-Charman/xnu) | `f6e430874477e7537ccfc8766b8842d0a9bc4507` | Full tracked source snapshot |
| `toolchains/darwin-xtools/` | [Christopher-Charman/darwin-xtools](https://github.com/Christopher-Charman/darwin-xtools) | `4defc01b9b7021a758ada5a73f848a71a5a5313a` (`darwin-xtools-2-2-4`) | Full tracked source snapshot |
| `src/apple-distributions-macos11/` | [Christopher-Charman/distribution-macOS-PowerPC](https://github.com/Christopher-Charman/distribution-macOS-PowerPC) | `0d630ff4a33e8c13df2e6b0ccfcc0d78c1360c90` | Source superproject snapshot with 229 pinned gitlink components |

The XNU fork is a later-generation kernel tree with a PowerPC machine-header patch file; **do not infer it is the historical XNU 1504.15.3 10.6.8 A5 source**. The Darwin xtools fork contains a modified PPC/PPC64 cctools/ld64 toolchain; its component versions must be reconciled with the era-specific Xcode 3.2.6, cctools and linker evidence before selecting it for a target build. The Apple distribution graph's latest recorded release is **macOS 11.0.1**, not 10.6.8. Its 229 gitlinks are pinned references, not vendored source bytes. They remain in their own namespace rather than being overlaid on the XNU source.

## Working with the sources

The XNU and Darwin xtools source snapshots are present immediately after a clone. The distribution components require explicit retrieval; for a selected component:

```sh
git submodule update --init -- src/apple-distributions-macos11/Libc
```

Do not run a recursive 229-component download by default; select only the dependency and release required by the target contract. The root `.gitmodules` records the prefixed paths and original Apple source repository URLs. Never rewrite a gitlink to a newer revision implicitly.

## Reproducible refresh policy

1. Capture the fork URL, branch/tag and exact source commit; check upstream licensing and preserved notices.
2. Import a new candidate on a review branch in its **existing namespace**, preserving the previous snapshot for comparison through Git history.
3. Compare exact source/build/ABI and platform relevance before making any PPC compatibility claim.
4. Keep original Apple sources, third-party modifications, experimental patches and boot/runtime test results distinguishable.
5. Require independent source review and exact target acceptance before merging a component into a build profile.

Historical 10A190, 10A222, 10A432 and 10.6.8 A5 source/release reconstruction remains separately scoped. The owner project's current-build manifest is not established by importing these sources.
