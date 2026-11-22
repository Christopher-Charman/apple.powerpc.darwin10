"""Verify the 10.6.8 autofs project selects its existing PowerPC source paths."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKING = ROOT / 'src/powerpc/autofs-154/autofs.xcode/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8/autofs-154/autofs.xcode/project.pbxproj'
ARCHS_OLD = 'ARCHS = (\n\t\t\t\t\ti386,\n\t\t\t\t\tx86_64,\n\t\t\t\t);'
ARCHS_PPC = ARCHS_OLD.replace('\t\t\t\t\ti386,', '\t\t\t\t\tppc,\n\t\t\t\t\ti386,')
PRODUCTS = ('autofs', 'mount_autofs', '"autofs-package"', 'files',
            'mount_url', 'automountd', 'automount', 'autofsd')


class AutofsPowerPCArchitectureTests(unittest.TestCase):
    def test_all_project_products_select_ppc(self):
        working = WORKING.read_text()
        configs = re.findall(r'/\* (Debug|Release) \*/ = \{\s+isa = XCBuildConfiguration;\s+buildSettings = \{(.*?)\};\s+name = \1;', working, re.S)
        selected = [(name, settings) for name, settings in configs if 'PRODUCT_NAME =' in settings]
        self.assertEqual(len(selected), 16)
        for product in PRODUCTS:
            matches = [(name, settings) for name, settings in selected if 'PRODUCT_NAME = %s;' % product in settings]
            self.assertEqual(sorted(name for name, _ in matches), ['Debug', 'Release'])
            for _, settings in matches:
                self.assertIn(ARCHS_PPC, settings)
                self.assertIn('VALID_ARCHS = "ppc i386 x86_64";', settings)

    def test_existing_ppc_code_paths_and_exact_release_delta(self):
        source = ROOT / 'src/powerpc/autofs-154'
        self.assertIn('#if defined(__ppc__)', (source / 'automountlib/auto_subr.c').read_text())
        self.assertIn('CPU=powerpc', (source / 'automountd/autod_main.c').read_text())
        upstream = UPSTREAM.read_text()
        self.assertEqual(upstream.count(ARCHS_OLD), 16)
        self.assertEqual(upstream.count('VALID_ARCHS = "i386 x86_64";'), 16)
        expected = upstream.replace(ARCHS_OLD, ARCHS_PPC)
        expected = expected.replace('VALID_ARCHS = "i386 x86_64";', 'VALID_ARCHS = "ppc i386 x86_64";')
        self.assertEqual(WORKING.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
