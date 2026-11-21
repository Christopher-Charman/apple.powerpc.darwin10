# Libnotify-54.3 PowerPC Release architecture

The 10.6.8 Libnotify Release configuration selects `ARCHS_STANDARD_32_64_BIT`, an Intel-only standard macro in Xcode 3.2. The tracked working-source patch selects `ARCHS = ppc` for the Release target. The official source snapshot is preserved unchanged. The notification API's compatibility and its dependencies must be verified separately; no compilation on PowerPC-Darwin.org.
