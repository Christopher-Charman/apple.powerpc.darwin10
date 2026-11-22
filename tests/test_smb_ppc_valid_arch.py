"""Check PowerPC validity for the SMB filesystem target and its helpers."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = 'smb-431.11'
WORKING = ROOT / 'src/powerpc' / COMPONENT / 'smb.xcodeproj/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8' / COMPONENT / 'smb.xcodeproj/project.pbxproj'
SERVICE = ROOT / 'src/powerpc' / COMPONENT / 'launchd/com.apple.smbfs_load_kext.plist'
PRODUCTS = ('mount_smbfs', 'smbutil', 'smbfs', 'load_smbfs')
CONFIGS = ('Development', 'Deployment', 'DevelopmentRosetta', 'DeploymentRosetta')


class SMBPowerPCValidArchitectureTests(unittest.TestCase):
    def test_four_products_allow_existing_ppc_selection(self):
        text = WORKING.read_text()
        entries = re.findall(r'/\* ([^*]+) \*/ = \{\s+isa = XCBuildConfiguration;\s+buildSettings = \{(.*?)\};\s+name = [^;]+;', text, re.S)
        for product in PRODUCTS:
            configs = [(name, settings) for name, settings in entries if 'PRODUCT_NAME = %s;' % product in settings
                       and name in CONFIGS and 'VALID_ARCHS = "ppc i386 x86_64";' in settings]
            self.assertEqual(sorted(name for name, _ in configs), sorted(CONFIGS), product)
            for _, settings in configs:
                if product == 'load_smbfs':
                    self.assertNotRegex(settings, r'(?m)^\s*ARCHS =')
                else:
                    self.assertIn('ARCHS = "$(ARCHS_STANDARD_32_64_BIT_PRE_XCODE_3_1)";', settings)
                    self.assertIn('ARCHS_STANDARD_32_64_BIT_PRE_XCODE_3_1 = "ppc i386 ppc64 x86_64";', settings)
        project_ids = ('45A29CF609DC5046005888E7', '45A29CF709DC5046005888E7',
                       '45CE6E1E0F5B558B00FE9345', '45CE6E2E0F5B559C00FE9345')
        for project_id in project_ids:
            match = re.search(project_id + r' /\* [^*]+ \*/ = \{\s+isa = XCBuildConfiguration;\s+buildSettings = \{(.*?)\};', text, re.S)
            self.assertIsNotNone(match)
            self.assertIn('ARCHS_STANDARD_32_64_BIT_PRE_XCODE_3_1 = "ppc i386 ppc64 x86_64";', match.group(1))
            self.assertIn('VALID_ARCHS = "i386 ppc x86_64";', match.group(1))
        self.assertIn('smbfs.kext/Contents/Resources/load_smbfs', SERVICE.read_text())

    def test_exact_official_release_delta(self):
        original = UPSTREAM.read_text()
        self.assertEqual(original.count('VALID_ARCHS = "i386 x86_64";'), 16)
        expected = original.replace('VALID_ARCHS = "i386 x86_64";', 'VALID_ARCHS = "ppc i386 x86_64";')
        self.assertEqual(WORKING.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
