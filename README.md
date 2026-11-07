# apple.powerpc.darwin10

PowerPC restoration and reconstruction of Darwin 10 (Snow Leopard).

## Project authority and current engineering work

[Project governance, historical evidence, exact-build frontier and issue ownership](docs/PROJECT_AUTHORITY_AND_FRONTIER.md)

[Owned architecture context and historical source boundaries](docs/OWNED_ARCHITECTURE_CONTEXT.md)

The canonical project methodology and historical evidence reside in the native ChatGPT Library workspace `/Project Workspaces/powerpc.apple.darwin/`. The repository owns versioned technical source and engineering results; its dated summaries do not replace current Library governance or establish a verified current boot image.

## Engineering workflow

Follow the provenance-to-runtime validation sequence in the project authority document. [Issue #3](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/3) owns the exact current image/hardware baseline; [issue #1](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/1) owns the reproducible experiment contract; [issue #2](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/2) owns the first fresh diagnostic; [issue #4](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/4) owns historical attribution/attachment closure.

For proposed experiment receipts, run `python3 tools/validate_experiment.py run.json` after the validator is merged. A passing schema check does not prove the asserted hardware/image facts or replace independent evidence review.

## First current diagnostic

[Operator procedure for collecting actual image/source/toolchain hashes and running a bounded, falsifiable diagnostic](docs/FIRST_CURRENT_DIAGNOSTIC.md). The read-only `tools/hash_input.py` helper computes SHA-256 for regular files; its output must be paired with independent hardware and boot evidence. Both helpers have regression tests in the bounded `experiment-contract` workflow.
