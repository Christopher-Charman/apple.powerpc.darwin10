# Optical storage families: PPC build selection

Official 10.6.8 Apple OSS snapshots: IOBDStorageFamily-10, IOCDStorageFamily-47.1, IODVDStorageFamily-30. Each Xcode project has project-wide Debug and Release configurations without explicit architecture selection. The three isolated release-bound patches select `ARCHS = ppc` in those project-wide configurations, preserving target-specific settings, headers and pristine Apple release sources. This is source-only architecture selection; no build, linkage, kernel ABI, device or media validation has been performed.
