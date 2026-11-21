"""Guard the two PowerPC static-library architecture selections in dyld."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "src/powerpc/dyld-132.13/dyld.xcodeproj/project.pbxproj"
ORIGINAL = ROOT / "src/releases/10.6.8/dyld-132.13/dyld.xcodeproj/project.pbxproj"

class DyldStaticArchitectureTests(unittest.TestCase):
    def test_static_architectures_pinned(self):
        text = P.read_text()
        self.assertNotIn('ARCHS = "$(NATIVE_ARCH_ACTUAL)";', text)
        self.assertNotIn('ARCHS = "$(ARCHS_STANDARD_32_64_BIT)";', text)
        self.assertIn('PRODUCT_NAME = dyldapis;', text)
        self.assertIn('PRODUCT_NAME = dsc;', text)
    def test_official_snapshot_unchanged(self):
        text = ORIGINAL.read_text()
        self.assertEqual(text.count('ARCHS = "$(NATIVE_ARCH_ACTUAL)";'), 1)
        self.assertGreaterEqual(text.count('ARCHS = "$(ARCHS_STANDARD_32_64_BIT)";'), 2)

if __name__ == "__main__":
    unittest.main()
