# IOUSBFamily-424.4.1 PPC source selection

## Exact source and comparison

- First-party Mac OS X 10.6.8 member: `IOUSBFamily-424.4.1`, Apple OSS tag object `f966932ce517bd4e1690c29dcd3290ade66733ce`, commit `c42e9bfb5fcc1803dd13e147b71d26e51e4fb20c` in `apple-oss-distributions/IOUSBFamily`.
- Immutable comparison tree: `src/releases/10.6.8/IOUSBFamily-424.4.1/`, Git tree `e32592374f0a601b680edc764cb84c1f5a845100`.
- Leopard 10.5.8 donor comparison: `IOUSBFamily-349.4.3`, Apple OSS tag object `2e2a84dc576929c206b2cfe4f70c594fee52575f`, commit `d64918a99e5e80ec3731d5eaf442a2da73034a65`. Its Xcode project admits `ppc` in all three configurations of the same 15 targets. No donor source file was copied.
- Apple source license and contributor notices remain in the component source tree.

## Working-source mutation

The 10.6.8 project still lists `ppc` in its `ARCHS_STANDARD_32_64_BIT_PRE_XCODE_3_1` and 32-bit architecture settings, and retains PPC-specific code guards in EHCI, OHCI and UHCI sources. Yet target-level `VALID_ARCHS` excludes PPC from Deployment, Logging and kprintf for `IOUSBFamily`, `AppleUSBOHCI`, `AppleUSBEHCI`, `AppleUSBUHCI`, `AppleUSBHub`, `IOUSBHIDDriverSafeBoot`, `AppleUSBMergeNub`, `AppleUSBOpticalMouse`, `IOUSBCompositeDriver`, `IOUSBHIDDriver`, `IOUSBUserClient`, `KLog`, `USB Prober`, `IOUSBUserClient_embedded` and `IOUSBFamily_embedded`. Add `ppc` to those 45 target settings in the complete tracked working project file. The previously restored `usbtracer` target is unchanged. The exact edit is `patches/IOUSBFamily-424.4.1-core-ppc.patch`; the release snapshot stays pristine.

This restores PPC32 source eligibility, not a proven USB stack. XNU IOKit interfaces, the IOPCIFamily dependency, other USB drivers, boot ordering, DMA assumptions and PPC hardware behavior still require build, ABI, link and hardware checks. The target and donor configuration maps and retained PPC guards were reviewed through authenticated GitHub API. Before this mutation, the working project differed from the release copy only by the earlier `usbtracer` PPC change. No compilation or device testing occurred on this host.
