# Apple16X50Serial-24 core kext PPC architecture

The `Apple16X50Serial` kernel extension's Development and Deployment Xcode configurations use the Intel-oriented `ARCHS_STANDARD_32_64_BIT` macro. This tracked working-source change selects `ppc` for those **core serial-driver** configurations. The distinct `Apple16X50ACPI` plug-in remains untouched: its platform assumptions must be reviewed independently, rather than indiscriminately enabling ACPI-specific hardware support on PowerPC. The official release snapshot is unchanged. No compilation on PowerPC-Darwin.org.
