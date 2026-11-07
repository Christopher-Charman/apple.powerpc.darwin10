# Release-bound PPC patches

Store reviewable unified diffs under `patches/` and a companion JSON manifest per patch. Required fields: `target` (exact historical release, e.g. 10.5.8, 10.6.2 or 10.6.8), `source_tree`, `source_tree_sha` (Git tree object SHA), `patch`, `rationale`, `reviewer`.

Run `python3 tools/ppc_patch_gate.py patches/<manifest>.json` before review. This read-only gate validates the pinned source tree, rejects cross-release and post-10.7 paths, and reports whether a patch applies or cleanly reverses. It **does not** apply or revert edits; source modifications must occur in a separately reviewed commit/PR, with independent semantic approval and build/ABI tests. Revert the approved commit using Git, not by rewriting pristine historical source snapshots.

A `reviewer` field is metadata only, not evidence of independent approval. Approval must be verified through the PR review system.
