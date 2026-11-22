"""Source-only check for the CoreOSMakefiles PowerPC Xcode template."""
import difflib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = 'src/powerpc/CoreOSMakefiles-63/Xcode/BSD.xcconfig'
UPSTREAM = ROOT / 'src/releases/10.6.8/CoreOSMakefiles-63/Xcode/BSD.xcconfig'
WORKING = ROOT / REL
PATCH = ROOT / 'patches/CoreOSMakefiles-63-ppc-xcode-arch.patch'
ORIGINAL = 'ARCHS = $(ARCHS_STANDARD_32_64_BIT);'
ADAPTED = 'ARCHS = ppc $(ARCHS_STANDARD_32_64_BIT);'


class CoreOSMakefilesPowerPCXcodeArchitectureTests(unittest.TestCase):
    def test_exact_source_change_and_retained_settings(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        self.assertEqual(upstream.count(ORIGINAL), 1)
        self.assertEqual(working, upstream.replace(ORIGINAL, ADAPTED))
        self.assertEqual(working.count('ARCHS = '), 1)

    def test_patch_matches_entire_source_delta(self):
        expected = ''.join(difflib.unified_diff(
            UPSTREAM.read_text().splitlines(keepends=True),
            WORKING.read_text().splitlines(keepends=True),
            fromfile='a/' + REL, tofile='b/' + REL,
        ))
        self.assertEqual(PATCH.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
