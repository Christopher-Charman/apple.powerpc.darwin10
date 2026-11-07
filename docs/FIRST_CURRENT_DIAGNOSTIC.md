# First fresh PPC Darwin diagnostic — operator procedure

**Owner:** [current build/hardware gate #3](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/3) and [first diagnostic #2](https://github.com/Christopher-Charman/apple.powerpc.darwin10/issues/2). The Library `/Project Workspaces/powerpc.apple.darwin/PROJECT_GOVERNANCE.md` remains methodology authority.

## 1. Establish current target identity

On the machine actually hosting the candidate build, collect **observed** (not inferred from forum archives) image path/size/hash, source revision, XNU kernel build string, OS build, bootloader, firmware, model identifier, CPU, RAM, GPU, storage controller and network interface. Preserve command output as immutable evidence. If the machine is offline, capture locally and transfer only non-sensitive hashes/logs through an authorized project route.

```sh
python3 tools/hash_input.py /absolute/path/to/current-image.dmg
python3 tools/hash_input.py /absolute/path/to/source-archive.tar
python3 tools/hash_input.py /absolute/path/to/toolchain-archive.tar
```

The tool reads **regular files only** and prints the observed SHA-256 and byte count. Hash a deterministic source/toolchain archive or a versioned file manifest, **not** a directory name or an unverified package label. Hashing does not establish that an artefact was booted or that it is legally redistributable.

## 2. Pre-register the test

Create a local JSON receipt with these fields:

```json
{
  "run_id": "replace-with-unique-id",
  "target": "exact OS build and PPC target",
  "hypothesis": "specific falsifiable cause",
  "prediction": "observation expected if hypothesis is correct",
  "falsifier": "observation that contradicts hypothesis",
  "procedure": "exact bounded commands and controls",
  "source": {"identifier": "source archive/revision", "sha256": "64 lowercase hex characters"},
  "toolchain": {"identifier": "compiler/linker and toolchain archive", "sha256": "64 lowercase hex characters"},
  "image": {"identifier": "actual candidate image", "sha256": "64 lowercase hex characters"},
  "hardware": {"model": "actual machine model", "boot_rom": "actual firmware", "cpu": "actual CPU", "ram_bytes": 1},
  "results": {"verdict": "planned", "observations": [], "artifacts": []},
  "evidence_class": "historical"
}
```

The JSON above is a **field illustration**, not a valid identity manifest; never use its placeholder values as evidence. Before executing, run `python3 tools/validate_experiment.py run.json`. Store actual capture time, host, GPU, bus and kernel strings in the run's associated evidence files. Do not treat schema acceptance as an independent verification of content or hardware.

## 3. Execute one discriminating test

Choose the smallest current symptom with a direct observable control. For the A5 allocator report, first pin the **exact Xbench version, executable hash, hardware and image**, run both A5 and Leopard controls on the same machine, identify the allocation API and loaded `libSystem` implementation, and only then test `posix_memalign` versus `malloc/free` hypotheses. Do not change multiple framework/KEXT generations at once.

## 4. Preserve negative results and stage transitions

After execution, change `results.verdict` to `passed`, `failed`, `falsified`, `null` or `inconclusive`; add observations and hash-addressed log artefacts. Re-run the validator. A falsified or null result is retained, not rewritten into a new hypothesis. Changing the build, image, toolchain or hardware requires a new run ID and receipt.

**Separate gates:** source identification, compilation, link/Mach-O verification, boot, GUI/service function, independent semantic acceptance. Record the last observed gate only; do not promote historical A5 logs into present-day live acceptance.

## 5. Publish safely

Link non-sensitive receipts and test outputs to #2 and exact-image acceptance evidence to #3. Keep proprietary Apple binaries, personal exports, credentials and unlicensed attachments out of Git. Keep historical source/attachment attribution under #4.
