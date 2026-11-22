# IOHIDFamily-315.7.16 PowerPC project architecture

The source is the official Apple 10.6.8 release member `IOHIDFamily-315.7.16` (APSL 2.0), pinned in `source-releases/10.6.8.json`. The pristine `src/releases/10.6.8/IOHIDFamily-315.7.16/IOHIDFamily/IOHIDFamily.xcconfig` blob is `8ca7b270cbb226a587cffaf3cd525152eea49a5d` and remains unchanged. The working copy before this patch was identical.

The project's Development and Deployment configurations load `IOHIDFamily.xcconfig`. Its `ARCHS` and `VALID_ARCHS` omitted `ppc` even though the desktop IOHIDFamily kernel target accepts `ppc`. This prevents selection of the PowerPC kernel extension and inherited desktop targets. The patch adds `ppc` to both lists, preserving the other upstream settings and the separate embedded configuration. The affected source producer is IOHIDFamily; consumers include the HID kernel clients and the project's `hidd`/IOHIDLib integration, whose interface and runtime compatibility remain unverified.

Patch: `patches/IOHIDFamily-315.7.16-ppc-project-arch.patch`. Source-only regression: `tests/test_iohidfamily_ppc_arch.py`. No compilation, linking, build, CI build or hardware test was performed or requested.
