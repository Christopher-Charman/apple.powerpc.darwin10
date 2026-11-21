# IOUSBFamily-424.4.1 usbtracer PPC architecture eligibility

Official baseline: `src/releases/10.6.8/IOUSBFamily-424.4.1/IOUSBFamily.xcodeproj/project.pbxproj`.
The `usbtracer` target has three build configurations (Logging, Deployment, kprintf) explicitly limited to `VALID_ARCHS = "i386 x86_64"`, despite G5 model tuning in the same configurations and other IOUSBFamily configurations retaining `ppc`. The isolated patch restores `ppc` to the three valid-architecture lists, without modifying the Apple source snapshot or changing any USB driver implementation.

This only restores architecture selection eligibility, not compilation or runtime compatibility. Verify usbtracer source dependencies and link behavior with the era-correct PPC SDK/compiler; do not infer that USB tracing or the rest of IOUSBFamily is tested on PPC.
