# dyld-132.13 PowerPC assembly ABI regression coverage

The canonical PowerPC working tree retains Apple's original PPC32/PPC64 loader startup and lazy binding helper implementations. The x86-only dyld_stub_binder.s is a separate implementation and must not be used as evidence of missing PowerPC lazy binding.

This CI guard verifies the PPC assembly conditional boundaries, project source membership, and immutability of the official 10.6.8 assembly snapshots. It complements the earlier architecture-selection fix; it does not substitute for linking dyld or booting on PPC hardware.

Test: tests/test_dyld_ppc_assembly_abi.py, executed in the required source-graph workflow.
