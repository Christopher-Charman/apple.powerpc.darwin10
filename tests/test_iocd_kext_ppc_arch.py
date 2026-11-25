"""Source-only regression for the IOCDStorageFamily PPC KEXT target."""
import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'IOCDStorageFamily-47.1/IOCDStorageFamily.xcodeproj/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8' / PROJECT
WORKING = ROOT / 'src/powerpc' / PROJECT
PATCH = ROOT / 'patches/IOCDStorageFamily-47.1-ppc-kext-arch.patch'
KEXT_CONFIGS = ('60218FA5095B74720026C3D8 /* Debug */',
                '60218FA6095B74720026C3D8 /* Release */')
HEADER_CONFIGS = ('60FD68270D40299C000D088D /* Debug */',
                  '60FD68280D40299C000D088D /* Release */')


def add_ppc_arch(text, configurations):
    for config in configurations:
        marker = ('\t\t' + config + ' = {\n\t\t\tisa = XCBuildConfiguration;\n'
                  '\t\t\tbuildSettings = {\n')
        if text.count(marker) != 1:
            raise AssertionError(f'Expected one build configuration: {config}')
        text = text.replace(marker, marker + '\t\t\t\tARCHS = ppc;\n')
    return text


def settings(text, config):
    match = re.search(r'\t\t' + re.escape(config) +
                      r' = \{\n\t\t\tisa = XCBuildConfiguration;\n'
                      r'\t\t\tbuildSettings = \{\n(.*?)\t\t\t\};', text, re.S)
    if not match:
        raise AssertionError(f'Missing settings for {config}')
    return match.group(1)


class IOCDKextPPCArchitectureTests(unittest.TestCase):
    def test_official_snapshot_and_exact_working_delta(self):
        raw = UPSTREAM.read_bytes()
        blob = b'blob ' + str(len(raw)).encode() + b'\0' + raw
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         'e639234d6deb3dfc543aa3130a0b8c1cef936f99')
        upstream = raw.decode('utf-8')
        previous = add_ppc_arch(upstream, HEADER_CONFIGS)
        expected = add_ppc_arch(previous, KEXT_CONFIGS)
        self.assertEqual(WORKING.read_text(), expected)
        self.assertEqual(upstream.count('ARCHS = ppc;'), 0)

    def test_native_target_and_headers_select_ppc(self):
        working = WORKING.read_text()
        target = re.search(r'60218FA4095B74720026C3D8 /\* Build configuration list '
                           r'for PBXNativeTarget "IOCDStorageFamily" \*/ = \{(.*?)\n\t\t\};',
                           working, re.S)
        self.assertIsNotNone(target)
        for config in KEXT_CONFIGS:
            self.assertIn(config, target.group(1))
            self.assertEqual(settings(working, config).count('ARCHS = ppc;'), 1)
        for config in HEADER_CONFIGS:
            self.assertEqual(settings(working, config).count('ARCHS = ppc;'), 1)
        self.assertEqual(working.count('ARCHS = ppc;'), 4)

    def test_incremental_patch_matches_source(self):
        previous = add_ppc_arch(UPSTREAM.read_text(), HEADER_CONFIGS)
        path = 'src/powerpc/' + PROJECT
        expected = ''.join(difflib.unified_diff(
            previous.splitlines(keepends=True),
            WORKING.read_text().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual(PATCH.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
