# DSTools-134: restore PPC target eligibility

## Exact target and donor

- 10.6.8 first-party member: `DSTools-134`, Apple OSS tag object `782b7d082d4544c282c4a2b756391be811f501da`, commit `b96161659c499146a8c6a7fa6670390bfa19f6dc` in `apple-oss-distributions/DSTools`.
- Immutable local comparison tree: `src/releases/10.6.8/DSTools-134/`, Git tree `bedc2b39650e6a49565ec918f5b18b38e39f3370`.
- Leopard 10.5.8 donor comparison: official `DSTools-112.1`, Apple OSS tag object `ae6c87171354a9ae92eac10d2df7f888accbf1f4`, commit `cca81286f366187ba9b92d9b445e5cea6f82c9c5`. Its project allowed `ppc` for the same ten native targets in at least one configuration. No donor source file was copied.
- License and attribution stay in the original Apple source tree and headers.

## Working source mutation

The 10.6.8 Xcode project excludes PPC in all three Development, Deployment and Default configurations of these ten targets: `dsconfigldap`, `dseditgroup`, `dsenableroot`, `dsperfmonitor`, `dirt`, `DSCacheInspector`, `dscacheutil`, `dserr`, `dsmemberutil` and `pwpolicy`. Add `ppc` to their 30 `VALID_ARCHS` settings in `src/powerpc/DSTools-134/DSTools.xcodeproj/project.pbxproj`, preserving the existing Intel entries. This restores PPC32 source selection for directory-service administration and diagnostic tools. `dscl` was handled separately and is unchanged here. The exact edit is in `patches/DSTools-134-remaining-tools-ppc.patch`; the release snapshot remains untouched.

The target mapping was read from the 10.6.8 and 10.5.8 Xcode configuration lists. The source files of all ten affected targets were reviewed for explicit architecture guards; no Intel-only guard was found in those inspected files. Source selection does not establish interface compatibility. These tools consume DirectoryService/OpenDirectory, Security, CoreFoundation and related private interfaces; their PPC32 build, ABI, links and runtime behavior remain unverified. The working project file matched the immutable release copy except for the prior `dscl` PPC edit before this mutation. No compilation or hardware validation was performed on this host.
