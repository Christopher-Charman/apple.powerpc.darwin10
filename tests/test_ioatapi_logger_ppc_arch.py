"""Source-only regression for the ATAPI logger's PPC target architecture."""
import difflib
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = 'IOATAPIProtocolTransport-251.0.1'
LOGGER = 'ATAPILogger/ATAPILogger.xcodeproj/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8' / COMPONENT / LOGGER
WORKING = ROOT / 'src/powerpc' / COMPONENT / LOGGER
KEXT = ROOT / 'src/powerpc' / COMPONENT / 'IOATAPIProtocolTransport.xcodeproj/project.pbxproj'
PATCH = ROOT / 'patches/IOATAPIProtocolTransport-251.0.1-ppc-logger-arch.patch'
OLD_ARCHS = '\t\t\t\tARCHS = "$(ARCHS_STANDARD_32_64_BIT_PRE_XCODE_3_1)";'
NEW_ARCHS = '\t\t\t\tARCHS = ppc;'


class ATAPILoggerPowerPCArchitectureTests(unittest.TestCase):
    def test_official_snapshot_and_exact_source_delta(self):
        raw = UPSTREAM.read_bytes()
        git_blob = b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         '55e6c098d1c1d01baa75ad3253369bd4adeabaae')
        upstream = raw.decode('utf-8')
        self.assertEqual(upstream.count(OLD_ARCHS), 2)
        self.assertEqual(WORKING.read_text(), upstream.replace(OLD_ARCHS, NEW_ARCHS))

    def test_logger_configs_and_parent_dependency(self):
        working = WORKING.read_text()
        for config in ('1DEB923208733DC60010E9CD /* Debug */',
                       '1DEB923308733DC60010E9CD /* Release */'):
            self.assertIn(config, working)
        self.assertEqual(working.count(NEW_ARCHS), 2)
        self.assertIn('ARCHS_STANDARD_32_64_BIT_PRE_XCODE_3_1 = "x86_64 i386 ppc";',
                      UPSTREAM.read_text())
        kext = KEXT.read_text()
        self.assertEqual(kext.count(NEW_ARCHS), 3)
        self.assertIn('E6816C8F1092356200F524E7 /* PBXTargetDependency */', kext)
        self.assertIn('name = ATAPILogger;', kext)

    def test_patch_is_exact_working_delta(self):
        path = f'src/powerpc/{COMPONENT}/{LOGGER}'
        expected = ''.join(difflib.unified_diff(
            UPSTREAM.read_text().splitlines(keepends=True),
            WORKING.read_text().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual(PATCH.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
