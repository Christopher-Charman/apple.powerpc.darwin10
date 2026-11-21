# IOStorageFamily-116.1.41 PPC build architecture

Official Apple 10.6.8 source reference: `src/releases/10.6.8/IOStorageFamily-116.1.41`. Its PBXProject configuration list points to the empty Debug and Release configurations `60CD8A38...` and `60CD8A39...`. The patch selects `ARCHS = ppc` only in those project-wide settings. It does not alter the IOStorageFamily_Embedded target's Aspen SDK reference or the upstream source snapshot. No compilation, linking, storage ABI or hardware test performed.
