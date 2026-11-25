"""Source-only regression for the IOFireWireAVCLib PPC64 plugin selection."""
import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'IOFireWireAVC-406.4.0/IOFireWireAVC.xcode/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8' / PROJECT
WORKING = ROOT / 'src/powerpc' / PROJECT
PATCH = ROOT / 'patches/IOFireWireAVC-406.4.0-ppc64-plugin.patch'
PLUGIN_CONFIGS = {
    '30EC568B0895F6B80057E458': 'Development',
    '30EC568C0895F6B80057E458': 'Deployment',
    '30EC568D0895F6B80057E458': 'FireLog',
    '30EC568E0895F6B80057E458': 'Default',
}


def git_blob_sha(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def restore_plugin_ppc64(upstream):
    result = upstream
    for config_id, name in PLUGIN_CONFIGS.items():
        marker = (f'\t\t{config_id} /* {name} */ = {{\n'
                  '\t\t\tisa = XCBuildConfiguration;\n'
                  '\t\t\tbuildSettings = {\n'
                  '\t\t\t\tARCHS = (\n'
                  '\t\t\t\t\tppc,\n')
        if result.count(marker) != 1:
            raise AssertionError(f'Expected one plugin architecture setting: {name}')
        result = result.replace(marker, marker + '\t\t\t\t\tppc64,\n')
    return result


class IOFireWireAVCPPC64PluginTests(unittest.TestCase):
    def test_exact_official_release_delta(self):
        raw = UPSTREAM.read_bytes()
        self.assertEqual(git_blob_sha(raw),
                         '1b04a38042ee90e893b9219de18be996e3e5e0f7')
        self.assertEqual(WORKING.read_text(), restore_plugin_ppc64(raw.decode()))

    def test_plugin_target_selects_ppc64_in_every_configuration(self):
        source = WORKING.read_text()
        native = re.search(
            r'7DDEC071064B0D6D001B4C4A /\* IOFireWireAVCLib \*/ = \{'
            r'(.*?)\n\t\t\};', source, re.S)
        self.assertIsNotNone(native)
        self.assertIn('buildConfigurationList = 30EC568A0895F6B80057E458',
                      native.group(1))
        config_list = re.search(
            r'30EC568A0895F6B80057E458 /\* Build configuration list for '
            r'PBXNativeTarget "IOFireWireAVCLib" \*/ = \{(.*?)\n\t\t\};',
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
        self.assertIn('buildConfigurationList = 30EC568F0895F6B80057E458',
                      source)

    def test_patch_is_exact_working_delta(self):
        path = 'src/powerpc/' + PROJECT
        expected = ''.join(difflib.unified_diff(
            UPSTREAM.read_text().splitlines(keepends=True),
            WORKING.read_text().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual(PATCH.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
