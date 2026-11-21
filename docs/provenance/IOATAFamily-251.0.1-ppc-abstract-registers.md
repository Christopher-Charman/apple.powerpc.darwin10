# IOATAFamily-251.0.1 PowerPC abstract ATA register classes

Apple 10.6.8 pristine reference: `src/releases/10.6.8/IOATAFamily-251.0.1/IOATARegI386.cpp` (unchanged). The editable source was identical before this change.

The source file defines three architecture-neutral abstract OSObject register classes (`IOATAReg8`, `IOATAReg16`, `IOATAReg32`), but the enclosing x86-only conditional excluded their metaclass and constructor definitions on PowerPC. The shared declarations are in `IOATARegI386.h` and used by ATA controller code. Move only the shared header and three abstract class definitions outside the x86 guard, leaving the x86 port-I/O header and `IOATAIOReg*` implementations protected by the original x86 guard. This avoids introducing unsupported x86 I/O-port instructions on PowerPC.

The exact incremental source diff is `patches/IOATAFamily-251.0.1-ppc-abstract-registers.patch`. Build, ABI and runtime verification remain outstanding; no host compilation was performed.
