# Source integration and release selection

The authoritative working source selection is [Darwin 9–10 source policy](DARWIN_9_10_SOURCE_POLICY.md).

The branch now vendors full tracked Apple OSS source trees for XNU 1228.15.4, 1456.1.26 and 1504.15.3, and Libc 498.1.7 and 594.9.1 under `src/releases/`. `historical/SOURCE_LOCK.json` independently tracks additional Leopard/Snow Leopard upstream source gitlinks. The owned `darwin-xtools` fork is imported under `toolchains/darwin-xtools/` at `4defc01b9b7021a758ada5a73f848a71a5a5313a` as a separately qualified PPC/PPC64-capable toolchain candidate.

Earlier commits on this PR branch temporarily imported a modern `Christopher-Charman/xnu` snapshot and the macOS 11.0.1 `distribution-macOS-PowerPC` superproject. **Both are removed from the branch tip** because whole-tree post-10.7 compatibility was not demonstrated. Their historical commits remain in Git history; they are not target build inputs. The user's owned fork URLs remain discoverable for individually proven architecture-neutral or PPC-compatible changes.

This source inventory is not a complete current community build/image manifest. The native ChatGPT Library retains project methodology and historical provenance authority. Preserve upstream notices and record build, link, boot and semantic validation independently.
