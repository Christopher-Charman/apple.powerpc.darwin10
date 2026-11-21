# IOGraphics-392.1: PowerPC project build architecture

Target: Mac OS X 10.6.8 / IOGraphics-392.1.
Source: exact release source at `src/releases/10.6.8/IOGraphics-392.1`.
Reference: Apple's 10.6.8 release and surviving PowerPC-specific code in `IOGraphicsFamily/IOFramebuffer.cpp` and IONDRV support sources.

The release project has three empty project-wide build configurations (Development, Deployment, Default) and does not specify a PowerPC architecture. With an Intel-only host/SDK default, its targets can silently select an incompatible architecture. The separately reviewable `patches/IOGraphics-392.1-ppc-arch.patch` sets `ARCHS = ppc` in those three project-level configurations; the tracked Apple release source remains pristine. Apply the patch to a separate working copy before building. This is a PowerPC-only development tree; it is not a claim that Apple's 10.6.8 release shipped native PPC graphics kexts.

Verification: the unified diff contains exactly three architecture-setting additions and is intended to apply to the pinned 10.6.8 source. Native Xcode 3.2.x PowerPC compilation, kernel-extension linking, graphics/IONDRV runtime and hardware testing remain required. Do not distribute or install a resulting kext without those tests. The untouched Apple release can be compared against the original project file in the Apple OSS release.
