"""Source-only regression for the IODVDStorageFamily native PPC KEXT target."""
import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'IODVDStorageFamily-30/IODVDStorageFamily.xcodeproj/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8' / PROJECT
WORKING = ROOT / 'src/powerpc' / PROJECT
PATCH = ROOT / 'patches/IODVDStorageFamily-30-ppc-kext-arch.patch'
KEXT_CONFIGS = ('60218F94095B74720026C3D8 /* Debug */',
                '60218F95095B74720026C3D8 /* Release */')
HEADER_CONFIGS = ('60FD67F30D4026D7000D088D /* Debug */',
                  '60FD67F40D4026D7000D088D /* Release */')


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


class IODVDKextPPCArchitectureTests(unittest.TestCase):
    def test_official_snapshot_and_exact_working_delta(self):
        raw = UPSTREAM.read_bytes()
        blob = b'blob ' + str(len(raw)).encode() + b'\0' + raw
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         '54ac3a2893608802671d1e16aee5f43c04241ba3')
        upstream = raw.decode('utf-8')
        previous = add_ppc_arch(upstream, HEADER_CONFIGS)
        expected = add_ppc_arch(previous, KEXT_CONFIGS)
        self.assertEqual(WORKING.read_text(), expected)
        self.assertEqual(upstream.count('ARCHS = ppc;'), 0)

    def test_native_target_and_headers_select_ppc(self):
        working = WORKING.read_text()
        target = re.search(r'60218F93095B74720026C3D8 /\* Build configuration list '
                           r'for PBXNativeTarget "IODVDStorageFamily" \*/ = \{(.*?)\n\t\t\};',
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
