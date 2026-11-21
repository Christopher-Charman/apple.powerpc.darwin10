# AppleFileSystemDriver-13 PPC project architecture

The official 10.6.8 AppleFileSystemDriver project selects `ARCHS_STANDARD_32_64_BIT` in its project-wide Debug and Release configurations. That standard macro does not select PowerPC in Xcode 3.2. The isolated patch replaces the project-wide architecture with `ppc` in both configurations. Target-specific source, the `setbootuuid` utility and pristine Apple release source remain unchanged. Source-only; no compilation or runtime validation on PowerPC-Darwin.org.
