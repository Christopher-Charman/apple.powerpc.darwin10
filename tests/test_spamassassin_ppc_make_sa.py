"""Source-only guard for SpamAssassin's PowerPC-capable wrapper recipe."""

import difflib
import hashlib
import shlex
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path('src/powerpc/SpamAssassin-144.2/Makefile')
WORKING = ROOT / RELATIVE
SNAPSHOT = ROOT / 'src/releases/10.6.8/SpamAssassin-144.2/Makefile'
PATCH = ROOT / 'patches/SpamAssassin-144.2-ppc-make-sa-cflags.patch'
ORIGINAL_BLOB = 'ec88be5ca8d7d03bf8eb839c4eb30d0dfa0a78b9'


def make_sa_cflags_line(source):
    recipe = source.split('\nmake_sa :\n', 1)[1].split('\n\nmake_sa_install :', 1)[0]
    lines = [line.strip() for line in recipe.splitlines() if 'make CFLAGS=' in line]
    if len(lines) != 1:
        raise AssertionError('expected one make_sa CFLAGS command')
    return lines[0]


def tokenized_recipe(line, cflags):
    # Expand only the known variables as text; never execute the command.
    expanded = (line.replace('$(SILENT)', '')
                    .replace('$(CD)', 'cd')
                    .replace('$(SRCROOT)', '/source')
                    .replace('$(CFLAGS)', cflags).strip())
    if not (expanded.startswith('(') and expanded.endswith(')')):
        raise AssertionError('recipe group must have both parentheses')
    return shlex.split(expanded[1:-1])


class SpamAssassinPowerPCMakeSaTests(unittest.TestCase):
    def test_exact_patch_and_pristine_apple_snapshot(self):
        pristine = SNAPSHOT.read_bytes()
        blob = b'blob ' + str(len(pristine)).encode() + b'\0' + pristine
        self.assertEqual(hashlib.sha1(blob).hexdigest(), ORIGINAL_BLOB)
        working = WORKING.read_bytes()
        expected = ''.join(difflib.unified_diff(
            pristine.decode().splitlines(keepends=True),
            working.decode().splitlines(keepends=True),
            fromfile='a/' + str(RELATIVE), tofile='b/' + str(RELATIVE)))
        self.assertEqual(PATCH.read_text(), expected)

    def test_apple_recipe_exposes_unclosed_quote(self):
        line = make_sa_cflags_line(SNAPSHOT.read_text())
        with self.assertRaises(ValueError):
            tokenized_recipe(line, '-Os -arch ppc')

    def test_default_recipe_preserves_powerpc_flags_as_one_argument(self):
        line = make_sa_cflags_line(WORKING.read_text())
        for arch in ('ppc', 'ppc64'):
            with self.subTest(arch=arch):
                flags = '-Os -arch ' + arch
                self.assertEqual(tokenized_recipe(line, flags), [
                    'cd', '/source/SpamAssassin', '&&', 'make', 'CFLAGS=' + flags])


if __name__ == '__main__':
    unittest.main()
