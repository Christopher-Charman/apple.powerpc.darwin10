"""Source-only check for the 10.6.8 JavaScriptGlue PowerPC architecture delta."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = "JavaScriptGlue-7533.19.1"
RELATIVE = Path(COMPONENT) / "Configurations/DebugRelease.xcconfig"
UPSTREAM = ROOT / "src/releases/10.6.8" / RELATIVE
WORKING = ROOT / "src/powerpc" / RELATIVE
BASE = ROOT / "src/powerpc" / COMPONENT / "Configurations/Base.xcconfig"
OLD = "ARCHS_1060 = $(ARCHS_STANDARD_32_64_BIT);"
NEW = "ARCHS_1060 = ppc $(ARCHS_STANDARD_32_64_BIT);"


class JavaScriptGluePowerPCArchitectureTests(unittest.TestCase):
    def test_exact_release_delta(self):
        upstream = UPSTREAM.read_bytes()
        working = WORKING.read_bytes()
        self.assertEqual(upstream.count(OLD.encode()), 1)
        self.assertEqual(working, upstream.replace(OLD.encode(), NEW.encode()))

    def test_1060_architecture_and_deployment_settings(self):
        config = WORKING.read_text()
        base = BASE.read_text()
        self.assertIn("ARCHS = $(ARCHS_$(TARGET_MAC_OS_X_VERSION_MAJOR));", config)
        self.assertIn(NEW, config)
        self.assertIn("ARCHS_1070 = $(ARCHS_STANDARD_32_64_BIT);", config)
        self.assertIn("MACOSX_DEPLOYMENT_TARGET_1060 = 10.6;", config)
        self.assertIn("VALID_ARCHS = i386 ppc x86_64 ppc64;", base)


if __name__ == "__main__":
    unittest.main()
