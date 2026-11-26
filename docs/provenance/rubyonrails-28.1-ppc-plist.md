# RubyOnRails-28.1: valid OpenSourceVersions plist for PowerPC 10.6.8

## Source pins

- The first-party Mac OS X 10.6.8 manifest pins `RubyOnRails-28.1`. Apple's [official tag](https://github.com/apple-oss-distributions/RubyOnRails/tree/RubyOnRails-28.1) resolves to commit `b51e7fe7e64dae4de480201a434d13d8dabd9278` and tree `327757ce8c539e84947c6860e94d09e06f90b403`. Both the initial `src/powerpc/RubyOnRails-28.1/` and pristine `src/releases/10.6.8/RubyOnRails-28.1/` have that tree ID.
- Apple's [10.5.8 predecessor](https://github.com/apple-oss-distributions/RubyOnRails/tree/RubyOnRails-25.2) closes the plist root. The immediately preceding `RubyOnRails-28` lacks that closure. The related 10.6.8 `RubyGems-17.1/rubygems.plist` also closes its root.
- Original Apple blobs: `RubyOnRails.plist` `5d55787f54c760a4e10d82b4a3ae9357ad64dd4c`; `gen_plist.rb` `34e5e235b5ba33be67f1ca6349d6096f59a97191`.

## Defect and correction

The 28.1 `RubyOnRails.plist` ends at `</array>` without closing `<plist version="1.0">`. A plist parser rejects this installed OpenSourceVersions record. `gen_plist.rb` emits the same incomplete document, so changing the checked-in plist alone would allow the defect to recur. The PowerPC working source now adds `</plist>` to both the checked-in metadata and the generator output. The exact source delta is `patches/RubyOnRails-28.1-ppc-plist.patch`; the official release snapshot and all 37 gem archives remain unchanged.

This is a release-metadata correction in the PowerPC working source. It does not establish native-extension or runtime compatibility on PowerPC.

## Source-only verification

`python3 -m unittest discover -s tests -p 'test_rubyonrails_ppc_plist.py' -v` verifies both pristine Apple blob pins and the exact patch, parses the installed plist and checks one entry for each bundled gem, and runs the generator with an empty gem directory to verify it emits a complete plist. The dedicated CI workflow runs only these source-script tests. No compilation, linking, build, gem installation, extension build, or hardware test is performed.
