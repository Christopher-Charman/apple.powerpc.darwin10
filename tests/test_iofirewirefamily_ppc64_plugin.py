"""Source-only regression for the IOFireWireLib PPC64 plugin selection."""
import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'IOFireWireFamily-426.4.1/IOFireWireFamily.xcodeproj/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8' / PROJECT
WORKING = ROOT / 'src/powerpc' / PROJECT
PATCH = ROOT / 'patches/IOFireWireFamily-426.4.1-ppc64-plugin.patch'
PLUGIN_CONFIGS = {
    '4D39F6D70992E12B006C2040': 'Development',
    '4D39F6D80992E12B006C2040': 'Deployment',
    '4D39F6D90992E12B006C2040': 'FireLog',
    '4D39F6DA0992E12B006C2040': 'Default',
}


def git_blob_sha(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


class IOFireWireFamilyPPC64PluginTests(unittest.TestCase):
    def test_exact_official_release_delta(self):
        raw = UPSTREAM.read_bytes()
        self.assertEqual(git_blob_sha(raw),
                         '1abdf348a65a577863cdb50eaae8ddc6d940b209')
        expected = raw.decode()
        for config_id, name in PLUGIN_CONFIGS.items():
            marker = (f'\t\t{config_id} /* {name} */ = {{\n'
                      '\t\t\tisa = XCBuildConfiguration;\n'
                      '\t\t\tbuildSettings = {\n'
                      '\t\t\t\tARCHS = (\n'
                      '\t\t\t\t\ti386,\n'
                      '\t\t\t\t\tppc,\n')
            self.assertEqual(expected.count(marker), 1)
            expected = expected.replace(marker, marker + '\t\t\t\t\tppc64,\n')
        self.assertEqual(WORKING.read_text(), expected)

    def test_plugin_target_and_architectures(self):
        source = WORKING.read_text()
        native = re.search(
            r'4D4C313A05F6702100D8DB71 /\* IOFireWireLib.plugin \*/ = \{'
            r'(.*?)\n\t\t\};', source, re.S)
        self.assertIsNotNone(native)
        self.assertIn('isa = PBXNativeTarget;', native.group(1))
        self.assertIn('buildConfigurationList = 4D39F6D60992E12B006C2040',
                      native.group(1))
        self.assertIn('productType = "com.apple.product-type.bundle";',
                      native.group(1))
        config_list = re.search(
            r'4D39F6D60992E12B006C2040 /\* Build configuration list for '
            r'PBXNativeTarget "IOFireWireLib.plugin" \*/ = \{(.*?)\n\t\t\};',
            source, re.S)
        self.assertIsNotNone(config_list)
        for config_id, name in PLUGIN_CONFIGS.items():
            self.assertIn(config_id + f' /* {name} */', config_list.group(1))
            config = re.search(
                rf'{config_id} /\* {name} \*/ = \{{(.*?)\n\t\t\}};',
                source, re.S)
            self.assertIsNotNone(config)
            self.assertIn('\t\t\t\t\tppc,\n\t\t\t\t\tppc64,\n',
                          config.group(1))
        self.assertEqual(source.count('\t\t\t\t\tppc64,\n'), 4)

    def test_patch_is_exact_working_delta(self):
        path = 'src/powerpc/' + PROJECT
        expected = ''.join(difflib.unified_diff(
            UPSTREAM.read_text().splitlines(keepends=True),
            WORKING.read_text().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual(PATCH.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
