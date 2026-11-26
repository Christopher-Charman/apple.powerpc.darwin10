"""Source-only checks for MySQL-55 PowerPC ABI config templates."""
import difflib
import hashlib
import tarfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'src/powerpc/MySQL-55'
SNAPSHOT = ROOT / 'src/releases/10.6.8/MySQL-55'
ARCHIVE = SNAPSHOT / 'mysql-5.0.92-apple.tar.gz'
MACROS = {'config.h.in': ('SIZEOF_CHARP', 'SIZEOF_LONG'),
          'innobase/ib_config.h.in': ('SIZEOF_LONG', 'SIZEOF_VOIDP')}


class MySQLPowerPCConfigTests(unittest.TestCase):
    def test_official_archive_and_pristine_makefile(self):
        self.assertEqual(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
                         '80f59a00c127bbb97934cea3616770eff1b9d22fff69478cb4afc1899fd9b856')
        self.assertEqual(SNAPSHOT.joinpath('Makefile').read_text().count(
            'APPLE_PRECONFIG_FILES_TO_PATCH'), 0)

    def test_makefile_applies_both_templates_after_google_before_configure(self):
        make = PROJECT.joinpath('Makefile').read_text()
        self.assertIn('APPLE_PRECONFIG_FILES_TO_PATCH = config.h.in innobase/ib_config.h.in', make)
        pre = make.split('configure-do-pre-patch:\n', 1)[1].split('\nconfigure-do-config:', 1)[0]
        self.assertLess(pre.index('GOOGLE_PRECONFIG_FILES_TO_PATCH'),
                        pre.index('APPLE_PRECONFIG_FILES_TO_PATCH'))
        self.assertIn('$(PATCH) -u $(cur_file) $(APPLE_PATCH_BASE_DIR)/$(cur_file).patch', pre)
        self.assertLess(make.index('configure-do-pre-patch:'), make.index('configure-do-config:'))

    def test_exact_working_source_patch(self):
        paths = ['src/powerpc/MySQL-55/Makefile',
                 'src/powerpc/MySQL-55/patch/apple/config.h.in.patch',
                 'src/powerpc/MySQL-55/patch/apple/innobase/ib_config.h.in.patch']
        diff = []
        for path in paths:
            old = SNAPSHOT.joinpath('Makefile').read_text() if path.endswith('/Makefile') else ''
            new = ROOT.joinpath(path).read_text()
            diff.append('diff --git a/' + path + ' b/' + path + '\n')
            if not old:
                diff.append('new file mode 100644\n')
            diff.extend(difflib.unified_diff(
                old.splitlines(keepends=True), new.splitlines(keepends=True),
                fromfile='a/' + path if old else '/dev/null', tofile='b/' + path))
        self.assertEqual(ROOT.joinpath('patches/MySQL-55-ppc-config-abi.patch').read_text(),
                         ''.join(diff))

    def test_patches_match_archive_and_select_each_abi(self):
        with tarfile.open(ARCHIVE, 'r:gz') as archive:
            for name, macros in MACROS.items():
                with self.subTest(name=name):
                    original = archive.extractfile('mysql-5.0.92/' + name).read().decode()
                    patch = PROJECT.joinpath('patch/apple', name + '.patch').read_text()
                    # The patch is generated against the exact archived template.
                    target = self._apply_simple_unified_patch(original, patch)
                    expected = ''.join(difflib.unified_diff(
                        original.splitlines(keepends=True), target.splitlines(keepends=True),
                        fromfile='a/' + name, tofile='b/' + name))
                    self.assertEqual(patch, expected)
                    for macro in macros:
                        self.assertNotIn('#undef ' + macro + '\n', target)
                        self.assertIn('# define ' + macro + ' 8', target)
                        self.assertIn('# define ' + macro + ' 4', target)
                    self.assertIn('#if defined(__BIG_ENDIAN__) && __BIG_ENDIAN__', target)
                    self.assertIn('# define WORDS_BIGENDIAN 1', target)
                    self.assertIn('# undef WORDS_BIGENDIAN', target)
                    self.assertNotIn('#if defined AC_APPLE_UNIVERSAL_BUILD', target)

    @staticmethod
    def _apply_simple_unified_patch(original, patch):
        """Apply context hunks as text; never invoke configure or a compiler."""
        lines = original.splitlines(keepends=True)
        result = []
        cursor = 0
        import re
        hunks = patch.splitlines(keepends=True)[2:]
        index = 0
        while index < len(hunks):
            match = re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@', hunks[index])
            if not match:
                raise AssertionError('unexpected patch hunk')
            start = int(match.group(1)) - 1
            result.extend(lines[cursor:start])
            cursor = start
            index += 1
            while index < len(hunks) and not hunks[index].startswith('@@ '):
                line = hunks[index]
                if line[0] in ' -':
                    if cursor >= len(lines) or lines[cursor] != line[1:]:
                        raise AssertionError('patch context differs from archived source')
                    cursor += 1
                if line[0] in ' +':
                    result.append(line[1:])
                index += 1
        result.extend(lines[cursor:])
        return ''.join(result)


if __name__ == '__main__':
    unittest.main()
