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

## Exact Snow Leopard 10.6.8 source baseline — verified 2026-11-07

The owner's [distribution-macOS-PowerPC](https://github.com/Christopher-Charman/distribution-macOS-PowerPC) fork also contains **`rel/macOS-10.6`** at `86ab567c039a242214b544439b5f08a8cf012d4a` (commit message: *Mac OS X 10.6.8*). Its source graph has **353 pinned component gitlinks**, imported under `src/apple-darwin-10.6.8/`. The `xnu` gitlink resolves to **`99c11f3f90a18f35d3692ea77444b51fd972a4f4`**, Apple's `xnu-1504.15.3` release commit.

The complete **3,386-file XNU 1504.15.3 source snapshot** from that exact commit is also checked in under `src/xnu-1504.15.3/`, so kernel-source analysis does not depend on a submodule fetch. This is the original Apple source, **not** a verified reconstruction of the community's modified 10.6.8 A5 kernel, image or firmware. Apply and verify PPC changes as separately attributed patches; never silently overwrite the original baseline.

The root `.gitmodules` names are release-qualified (`snowleopard/` and `macos11/`) to prevent collisions for components appearing in both graphs. Both sets preserve their original pinned gitlink commits and upstream URLs. To fetch a single 10.6.8 component, run:

```sh
git submodule update --init -- src/apple-darwin-10.6.8/Libc
```

The macOS 11 component graph and the newer XNU fork remain separately retained as reference/porting inputs, not the target build. Build selection must resolve against `src/apple-darwin-10.6.8/` and `src/xnu-1504.15.3/` before examining later branches.
