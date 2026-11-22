"""Check IOHIDFamily's PowerPC project configuration against the Apple source."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = 'IOHIDFamily-315.7.16'
WORKING = ROOT / 'src/powerpc' / COMPONENT / 'IOHIDFamily/IOHIDFamily.xcconfig'
UPSTREAM = ROOT / 'src/releases/10.6.8' / COMPONENT / 'IOHIDFamily/IOHIDFamily.xcconfig'
PROJECT = ROOT / 'src/powerpc' / COMPONENT / 'IOHIDFamily.xcodeproj/project.pbxproj'


class IOHIDFamilyPowerPCArchitectureTests(unittest.TestCase):
    def test_project_uses_config_for_both_desktop_configurations(self):
        project = PROJECT.read_text()
        config_ref = 'baseConfigurationReference = 3583ADBE0DFDF00D0003AEE2 /* IOHIDFamily.xcconfig */;'
        self.assertEqual(project.count(config_ref), 2)
        self.assertIn('/* Build configuration list for PBXProject "IOHIDFamily" */', project)
        self.assertIn('VALID_ARCHS = "ppc i386 x86_64";', project)

    def test_ppc_restored_with_exact_release_delta(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        self.assertEqual(upstream.count('ARCHS = i386 x86_64\n'), 1)
        self.assertEqual(upstream.count('VALID_ARCHS = armv6 i386 x86_64\n'), 1)
        expected = upstream.replace('ARCHS = i386 x86_64\n', 'ARCHS = ppc i386 x86_64\n')
        expected = expected.replace('VALID_ARCHS = armv6 i386 x86_64\n', 'VALID_ARCHS = ppc armv6 i386 x86_64\n')
        self.assertEqual(working, expected)


if __name__ == '__main__':
    unittest.main()
