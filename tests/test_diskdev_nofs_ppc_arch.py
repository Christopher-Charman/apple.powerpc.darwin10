"""Check the diskdev_cmds nofs utility is selected for PowerPC."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = 'diskdev_cmds-491.6'
WORKING = ROOT / 'src/powerpc' / COMPONENT / 'nofs.tproj/Makefile'
UPSTREAM = ROOT / 'src/releases/10.6.8' / COMPONENT / 'nofs.tproj/Makefile'
PARENT = ROOT / 'src/powerpc' / COMPONENT / 'Makefile'


class DiskdevNofsPowerPCArchitectureTests(unittest.TestCase):
    def test_nofs_is_a_subproject_with_ppc_release_selection(self):
        parent = PARENT.read_text()
        self.assertRegex(parent, r'\bnewfs_hfs\.tproj nofs\.tproj\\\n')
        target = WORKING.read_text()
        self.assertEqual(re.findall(r'^RC_ARCHS\s*=\s*(.*)$', target, re.M), ['ppc i386 x86_64'])
        self.assertIn('include $(MAKEFILEPATH)/CoreOS/ReleaseControl/BSDCommon.make', target)
        makefiles = ROOT / 'src/powerpc/CoreOSMakefiles-63/ReleaseControl'
        bsd = (makefiles / 'BSDCommon.make').read_text()
        common = (makefiles / 'Common.make').read_text()
        self.assertIn('include $(MAKEFILEPATH)/CoreOS/ReleaseControl/Common.make', bsd)
        self.assertIn('CC_Archs      = $(RC_ARCHS:%=-arch %)', common)
        self.assertIn('$(RC_ARCHS:ppc=powerpc)', common)

    def test_exact_official_release_delta(self):
        upstream = UPSTREAM.read_text()
        self.assertEqual(upstream.count('RC_ARCHS = i386 x86_64\n'), 1)
        self.assertEqual(WORKING.read_text(), upstream.replace('RC_ARCHS = i386 x86_64\n',
                                                             'RC_ARCHS = ppc i386 x86_64\n'))


if __name__ == '__main__':
    unittest.main()
