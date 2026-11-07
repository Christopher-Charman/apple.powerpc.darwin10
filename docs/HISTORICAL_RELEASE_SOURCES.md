# Darwin 9 / Darwin 10 historical source tracks

The historical source trees are **actual Apple OSS upstream tag commit references**, stored as pinned Git submodules in `historical/10.5/` and `historical/10.6/`. Each path maps to an exact Git commit in `historical/SOURCE_LOCK.json` and the root `.gitmodules`. This is distinct from the later XNU fork under `src/xnu/` and the modified PPC toolchain under `toolchains/darwin-xtools/`.

## Pinned components

- **Leopard / Darwin 9 (10.5.x)**: `xnu-1228.15.4`, `Libc-498.1.7`, `Libsystem-111.1.1`, `dyld-95.3`, `cctools-667.8.0`, `ld64-77.1`.
- **Snow Leopard / Darwin 10 (10.6.x)**: `xnu-1456.1.26`, `xnu-1504.3.12`, `xnu-1504.15.3`, `Libc-594.9.5`, `Libsystem-125.2.11`, `dyld-132.13`, `cctools-773`, `ld64-97.17`.

These are version-specific **candidate source snapshots**, not a proven per-point-release complete bill of materials. In particular, XNU 1504.15.3 is the historical A5-associated kernel lineage; the upstream source alone is not the modified community kernel. Do not conflate stock upstream code with ChrisCharman's original work, Educovas' modifications, 10A190_PPC, patched 10A222, 10A432, or A5 installation evidence.

## Materialize one historical component

```sh
git submodule update --init -- historical/10.6/xnu/xnu-1504.15.3
python3 tools/verify_historical_sources.py
```

The first command fetches the exact upstream commit into the project checkout; the second checks the committed lock, gitlink and URL mappings. Neither compiles the kernel or validates a boot image. Do not indiscriminately fetch the macOS 11 component graph. Add further 10.5–10.6.x components only after checking exact Apple OSS tags, licenses, release correspondence and dependency edges; keep candidate vs verified image provenance separate.

## Fully vendored XNU source trees

The three critical kernel generations are additionally checked in as **complete tracked source files**, not only submodule pointers:

| Source tree | Tracked files | Verified Git tree SHA |
| --- | ---: | --- |
| `historical-vendored/xnu-1228.15.4/` | 3,156 | `9d80f9528906753d682f9d65d56a0276bad56b4d` |
| `historical-vendored/xnu-1456.1.26/` | 3,379 | `46708ce5a6d4a42164ddb67a90fa6fbc7f986430` |
| `historical-vendored/xnu-1504.15.3/` | 3,386 | `0ffff24afe52ed47d20c5a06f07a10200f89f32b` |

Each imported tree SHA was compared directly against the corresponding pinned Apple OSS upstream commit tree and matched. This permits offline source analysis without submodule initialization. Other 10.5/10.6 components remain pinned submodule references pending per-component source/ABI selection; they are **not** falsely represented as already vendored.
