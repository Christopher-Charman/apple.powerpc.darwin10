"""Source-pinned qualification for historical OSXCross Darwin 10 PPC selection."""
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATCH = ROOT / 'third_party/patches/osxcross-ppc-test-darwin10.patch'


class Darwin10Patch(unittest.TestCase):
    def test_patch_changes_only_legacy_darwin10_selector(self):
        content = PATCH.read_text()
        self.assertIn('-  10.6*) TARGET=darwin10 ;;', content)
        self.assertIn('+  10.6*) TARGET=darwin10; APPLY_LD64_ADD_PPC_SUPPORT_PATCH=1; ;;', content)
        self.assertEqual(content.count('\n@@ '), 1)
        self.assertEqual(content.count('\n+  10.6*'), 1)

    def test_patch_is_valid_git_diff(self):
        result = subprocess.run(['git', 'apply', '--stat', str(PATCH)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 0, result.stderr.decode())


if __name__ == '__main__':
    unittest.main()
