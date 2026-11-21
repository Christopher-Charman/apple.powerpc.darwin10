# IONetworkingFamily-65.2.1 PowerPC architecture selection

Official 10.6.8 release source: `src/releases/10.6.8/IONetworkingFamily-65.2.1`. The project-wide Development, Deployment and Default build configurations contain empty settings and do not explicitly select PPC. This reviewable patch sets `ARCHS = ppc` in those three configurations, preserving the release snapshot and per-target settings. Validate with the era-correct PPC compiler/SDK, networking kernel extension ABI, driver dependencies and actual PowerPC hardware before treating it as a working port.
