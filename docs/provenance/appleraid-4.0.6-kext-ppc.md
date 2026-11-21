# AppleRAID-4.0.6 PowerPC kernel extension architecture

The official 10.6.8 AppleRAID Xcode project has three `AppleRAIDKext` target configurations with `VALID_ARCHS = "i386 x86_64"`, while the companion `AppleRAIDLib` target explicitly allows `ppc i386 x86_64`. The patch adds PPC to the kext's three valid-architecture lists, without modifying the `artest` target or upstream release source. The source-level inconsistency motivates this limited change; actual PPC kernel ABI, linking and RAID device behavior remain unverified. No compilation permitted on PowerPC-Darwin.org.
