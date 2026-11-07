# Snow Leopard PowerPC — historical evidence integration

This repository reconstructs the original owner's historical PowerPC Snow Leopard development. Historical material is evidence, not an instruction to substitute third-party builds or to claim runtime acceptance.

## Independent provenance planes

- **Source release:** Apple official 10.6–10.6.8 release manifests and exact tagged source trees under `source-releases/` and `src/releases/`.
- **Build recipe:** original MacOSForge Darwinbuild under `tooling/darwinbuild/`, including build plists, source transformations, header staging and build-root machinery. The 10A432 stock `RC_ARCHS` is Intel-only; PowerPC must be selected deliberately.
- **Build environment:** historical Apple Darwinbuild Roots and generated headers. The original 10A432 Roots were referenced in the owner's 2022 development discussion, including a reported Apple-built PPC-containing `ld`. **Root bytes are not yet recovered or validated**; this is distinct from the owner's `BUILD.zip`.
- **Owner-built binary evidence:** original `BUILD.zip` archive digest and embedded Tome digest, with 5,188 entries and 126 Mach-O binaries containing PPC slices, verified and hashed in `docs/build_zip_direct_binary_inventory.json`. This is not evidence that these binaries shipped in retail Snow Leopard.
- **Shipping state:** untouched installation/seed captures, separate from Darwinbuild Roots and owner builds. No retail PPC parity claim follows from the preceding planes.
- **Independent contributions:** Educovas's XNU/kernel and installation work must retain separate authorship and validation; do not relabel as owner-compiled binaries.

## Historical sequence and build gates

10A096 / 10A190 early PowerPC developer previews → 10A222 patching → 10A432 GM-era source and kernel experiments → 10B504 updates → 10K540 (10.6.8) source reconstruction. This is a historical progression, **not** proof of one continuous fully bootable PPC image.

The owner's historical documentation records successful PPC component rebuilds and the independent Educovas kernel work. A particularly useful *directly checked* first-party path is `src/releases/10.6.8/CF-550.43/BuildCFLite`: it specifies `-arch ppc` and chooses `CFUnicodeData-B.mapping` on PowerPC. CFLite is **not** interchangeable with shipping CoreFoundation/Foundation/Cocoa; do not use its build path to assert system ABI parity.

## Archived primary-source routes

- Original owner archive: `BUILD.zip`, retained in the owner's archive storage (not committed wholesale to Git).
- Owner historical Darwinbuild evidence classification and Snow Leopard PPC history: recovered from the owner's 2026 project conversations and records.
- Official Darwinbuild: `https://github.com/macosforge/darwinbuild`.
- Official Apple release index: `https://opensource.apple.com/releases/`.
- Original historical Darwinbuild Roots/Patches paths: `https://opensource.apple.com/darwinbuild/Roots/10A432/` and `https://opensource.apple.com/darwinbuild/Patches/` (historical addresses; current availability is not assumed).

## Acceptance

Source provenance, build recipes, root products, binary slices, SDK/private headers, linker compatibility, kernel boot and graphical runtime must be verified independently. The repo may contain complete source manifests without having recovered every corresponding source tree or achieved runtime parity.
