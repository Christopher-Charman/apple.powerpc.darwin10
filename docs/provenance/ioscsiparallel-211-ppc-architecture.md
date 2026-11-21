# IOSCSIParallelFamily-211.0.0 PPC project architecture

Apple 10.6.8 release reference: `src/releases/10.6.8/IOSCSIParallelFamily-211.0.0`. Its project-wide Development, Deployment and Default Xcode configurations have empty build settings. The patch selects `ARCHS = ppc` in these three project-wide configurations; target settings and official release source remain unchanged. This is a source-only configuration restoration, not a successful compilation or tested SCSI hardware implementation.
