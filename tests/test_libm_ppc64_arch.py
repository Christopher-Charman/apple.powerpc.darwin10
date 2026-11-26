"""Source-only regression checks for Libm-315 desktop PPC64 project settings."""

import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path('Libm-315/Libm.xcodeproj/project.pbxproj')
UPSTREAM = ROOT / 'src/releases/10.6.8' / RELATIVE
WORKING = ROOT / 'src/powerpc' / RELATIVE
PATCH = ROOT / 'patches/Libm-315-ppc64-arch.patch'
OFFICIAL_BLOB = '6c528fb180814171f0c38889e53e31b3b55b51b8'


def git_blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def configurations(text):
    blocks = re.findall(r'^\t\t([0-9A-F]{24}) /\* .*? \*/ = \{\n(.*?)^\t\t\};', text, re.M | re.S)
    return {key: body for key, body in blocks if 'isa = XCBuildConfiguration;' in body}


class LibmPPC64ArchitectureTests(unittest.TestCase):
    def test_exact_source_delta_and_patch(self):
        upstream = UPSTREAM.read_bytes()
        working = WORKING.read_bytes()
        self.assertEqual(git_blob_sha(upstream), OFFICIAL_BLOB)
        delta = ''.join(difflib.unified_diff(
            upstream.decode().splitlines(keepends=True),
            working.decode().splitlines(keepends=True),
            fromfile='a/src/powerpc/' + str(RELATIVE),
            tofile='b/src/powerpc/' + str(RELATIVE), n=3))
        self.assertEqual(delta, PATCH.read_text())
        additions = [line[1:] for line in delta.splitlines()
                     if line.startswith('+') and not line.startswith('+++')]
        removals = [line[1:] for line in delta.splitlines()
                    if line.startswith('-') and not line.startswith('---')]
        self.assertEqual(len(additions), 20)
        self.assertTrue(all('ppc64' in line for line in additions))
        self.assertEqual(len(removals), 10)
        self.assertTrue(all('VALID_ARCHS =' in line and 'ppc64' not in line for line in removals))

    def test_desktop_configurations_restore_ppc64(self):
        configs = configurations(WORKING.read_text())
        project_ids = ('1DEB914F08733D8E0010E9CD', '1DEB915008733D8E0010E9CD')
        for key in project_ids:
            body = configs[key]
            self.assertRegex(body, r'ARCHS = \(\s*armv6,\s*ppc,\s*ppc64,')
            self.assertIn('VALID_ARCHS = "ppc ppc64 i386 x86_64 armv5 armv6 armv7";', body)
            for setting in ('PER_ARCH_CFLAGS_ppc64', 'PER_ARCH_EXPORTED_SYMBOLS_FILE_ppc64',
                            'PER_ARCH_HEADER_PATH_ppc64', 'PER_ARCH_SRCROOT_ppc64'):
                self.assertIn(setting + ' = ', body)
        desktop_target_ids = (
            '3B3049E50ABF8AD800994776', '3B304B110ABF964E00994776',
            '3B304B3F0ABF970E00994776', '3B304BFF0ABFAB1F00994776',
            '3B304C2E0ABFAD7500994776', '3B304C690ABFB03F00994776',
            '3B304C7D0ABFB0C700994776', '3BE6DC500ABF55B600B91802')
        for key in desktop_target_ids:
            self.assertIn('VALID_ARCHS = "i386 ppc ppc64 x86_64";', configs[key])
        self.assertIn('ARCHS = (\n\t\t\t\t\tarmv5,\n\t\t\t\t\tarmv6,\n\t\t\t\t\tarmv7,',
                      configs['63127BF00E92DB8500B061BB'])


if __name__ == '__main__':
    unittest.main()
