"""Source-only guard for WebKit's Snow Leopard PowerPC architecture selection."""

import difflib
import os
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("PPC_SOURCE_ROOT", Path(__file__).resolve().parents[1]))
COMPONENT = "WebKit-7533.21.1"
RELATIVE = Path(COMPONENT) / "mac/Configurations/DebugRelease.xcconfig"
UPSTREAM = ROOT / "src/releases/10.6.8" / RELATIVE
WORKING = ROOT / "src/powerpc" / RELATIVE
COMPONENT_ROOT = ROOT / "src/powerpc" / COMPONENT
PATCH = ROOT / "patches/WebKit-7533.21.1-ppc-debugrelease-arch.patch"
OLD = "ARCHS_1060 = $(ARCHS_STANDARD_32_64_BIT);"
NEW = "ARCHS_1060 = ppc ppc64 $(ARCHS_STANDARD_32_64_BIT);"


class WebKitPowerPCDebugReleaseArchitectureTests(unittest.TestCase):
    def test_exact_release_delta_and_patch(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        self.assertEqual(upstream.count(OLD), 1)
        self.assertEqual(working, upstream.replace(OLD, NEW, 1))
        expected_patch = "".join(difflib.unified_diff(
            upstream.splitlines(keepends=True), working.splitlines(keepends=True),
            fromfile="a/src/powerpc/" + str(RELATIVE),
            tofile="b/src/powerpc/" + str(RELATIVE),
        ))
        self.assertEqual(PATCH.read_text(), expected_patch)

    def test_mac_configuration_consumes_ppc_and_retains_other_targets(self):
        config = WORKING.read_text()
        base = (COMPONENT_ROOT / "mac/Configurations/Base.xcconfig").read_text()
        exports = (COMPONENT_ROOT / "mac/Configurations/WebKit.xcconfig").read_text()
        project = (COMPONENT_ROOT / "WebKit.xcodeproj/project.pbxproj").read_text()
        self.assertIn("ARCHS = $(ARCHS_$(TARGET_MAC_OS_X_VERSION_MAJOR));", config)
        self.assertIn(NEW, config)
        self.assertIn("ARCHS_1050 = $(NATIVE_ARCH);", config)
        self.assertIn("ARCHS_1070 = $(ARCHS_STANDARD_32_64_BIT);", config)
        self.assertIn("MACOSX_DEPLOYMENT_TARGET_1060 = 10.6;", config)
        self.assertIn("VALID_ARCHS = i386 ppc x86_64 ppc64;", base)
        self.assertIn("EXPORTED_SYMBOLS_FILE_ppc = mac/WebKit.exp;", exports)
        self.assertIn("EXPORTED_SYMBOLS_FILE_ppc64 = $(BUILT_PRODUCTS_DIR)/DerivedSources/WebKit/WebKit.LP64.exp;", exports)
        self.assertEqual(project.count("baseConfigurationReference = 1C904FD40BA9DD0F0081E9D0 /* DebugRelease.xcconfig */;"), 2)


if __name__ == "__main__":
    unittest.main()
