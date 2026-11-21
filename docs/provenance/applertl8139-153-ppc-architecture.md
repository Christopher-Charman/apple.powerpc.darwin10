# AppleRTL8139Ethernet-153 PPC project configuration

Official Apple 10.6.8 source: `src/releases/10.6.8/AppleRTL8139Ethernet-153`. The Xcode PBXProject's Development, Deployment and Default configurations have empty build settings. This patch selects `ARCHS = ppc` in those three project-wide configurations. The target-specific settings, driver implementation and pristine source snapshot are unchanged. PPC compiler, driver dependencies and network adapter behavior have not been tested; no compilation on PowerPC-Darwin.org.
