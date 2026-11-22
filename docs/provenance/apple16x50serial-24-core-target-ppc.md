# Apple16X50Serial-24 PowerPC core target separation

## Source and scope

Apple's Mac OS X 10.6.8 release manifest names `Apple16X50Serial-24` (upstream annotated tag peels to commit `39d89a56fe9fc50b02a7b3385c3512ff63985587`). Its pristine project remains `src/releases/10.6.8/Apple16X50Serial-24/Apple16X50Serial.xcodeproj/project.pbxproj`, Git blob `ecf43504733f782be1760c9bc8cd75024a4d094e`. Apple's 10.5.8 release manifest names `Apple16X50Serial-19.3` (tag commit `dbc9278411440d5b6fade06722607a05543f3dc5`). The 19.3 PCI source and generic `IOPCIDevice` personality are predecessors for comparison; its removal of no PowerPC-specific PCI code does not justify replacing the newer driver. The 24 source retains the PCI path and later bounded-string and pointer-width corrections. The older PCCard target was removed upstream; no PCCard dependency closure or affected-machine evidence supports reinstating it here.

The prior `Apple16X50Serial-24-core-ppc.patch` selects `ppc` for the core Development and Deployment configurations. In the same Xcode project, the core target still depends on the separate `Apple16X50ACPI` target. That plug-in's personality requires `IOACPIPlatformDevice` and `IOACPIFamily`; its Development configuration retains `$(ARCHS_STANDARD_32_64_BIT)`. Xcode's target dependency therefore selects the ACPI plug-in when the core PCI driver is selected, despite the separate platform contract. The core DEBUG, ASSERT and DEBUG & ASSERT configurations also lacked an explicit `ppc` selection, so their PowerPC architecture depended on external project defaults.

## PowerPC correction

`patches/Apple16X50Serial-24-core-target-ppc.patch` is the exact patch against the current tracked working file. It removes only the core-to-ACPI target dependency and its now-unused proxy/dependency objects, and selects `ARCHS = ppc` for the three remaining core configurations. The ACPI and embedded targets, source files, personalities and pristine Apple snapshot are unchanged. The native core target's copy-files phase has no plug-in entries, so decoupling does not remove a copied core payload. ACPI remains an independently selectable target for a platform that supplies its provider and dependency.

## Validation boundary

`tests/test_apple16x50serial_ppc_target.py` checks the pinned pristine project blob, all five core architecture configurations, the absence of the core-to-ACPI edge and preservation of the embedded edge. It is run by the `source-graph` GitHub workflow using Python source inspection only. No compilation, linking, build tooling, runtime or hardware validation was performed or authorised. PPC compatibility of the driver and its IOPCI/IOSerial dependencies remains unverified.
