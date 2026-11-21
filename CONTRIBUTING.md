# Contributing to Snow Leopard PowerPC

This is a community reconstruction of Darwin 10 / Mac OS X 10.6.8 for PowerPC. Contributions from the MacRumors community and other developers are welcome. The [development forum](https://forums.macrumors.com/threads/10-6-snow-leopard-powerpc-development.2439769/) is the public project discussion; GitHub Issues and Pull Requests track reproducible engineering changes.

## Where to work

- `PowerPC`: canonical PowerPC development branch. Branch from this for component fixes, dependency restoration, toolchain changes, tests and documentation.
- `main`: public landing/reference branch. Do not target source changes here.
- Keep upstream Apple source provenance and immutable historical snapshots separate from patched working trees.
- Search existing issues and PRs first, particularly the open source-graph integration PRs, to avoid parallel conflicting source imports.

## Start a change

1. Choose one component or one reproducible failure. Record the target build/image (10.6.8/A5, 10A432, etc.) and its exact source release/tag.
2. Establish a known baseline, including binary architecture, ABI, dependencies, symbols and consumer behaviour.
3. Identify the Apple OSS release, separately published developer-tool source, historical donor or missing Root/header producer. Document the source URL, checksum or commit, license and why that version is required.
4. Make a minimal, reviewable change in a component branch. Prefer adapting incompatible Darwin 10 changes over wholesale rollback to Leopard.
5. Run source graph and historical lock validation when relevant. Record build commands and toolchain/SDK versions, first error on failure, and Mach-O architecture/dependency inspection on success.
6. Open a PR targeting `PowerPC` using the template. State what is verified and what remains untested.

## Evidence and testing

A compile is not proof of a working OS component. Distinguish source-only validation, PPC compilation/link, integration into the target image, and verified G4/G5 runtime results. Report machine identifier, CPU, RAM, GPU, storage/controller, kernel, source and binary hashes, changed files, expected/actual results, a control test and relevant logs.

Do not test experimental images on irreplaceable data. Use a spare disk/partition and backups. Preserve original system files, permissions and metadata, and provide a reversible installation procedure.

## Review and licensing

All contributions should preserve Apple and third-party license notices and original author attribution. Do not submit proprietary Apple binaries, private SDKs, credentials, copyrighted forum attachments without permission, or other material you lack rights to redistribute. Link external acquisition instructions instead.

Maintainers review source provenance, patch rationale, compatibility and evidence. Do not merge a component solely because a manifest check passes. For changes affecting ABI, kernel, KEXTs, security services or boot, seek independent technical review and hardware validation where available. A reviewer may accept an explicitly experimental patch without implying full system compatibility.

Be constructive and precise. Challenge technical claims with reproducible evidence; credit historical contributors and distinguish their results from new validation.
