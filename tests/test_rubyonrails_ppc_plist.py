import difflib
import hashlib
import os
import plistlib
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(os.environ.get('ROR_PLIST_TEST_ROOT', Path(__file__).resolve().parents[1]))
RELATIVE = Path('RubyOnRails-28.1')
SOURCE = ROOT / 'src/powerpc' / RELATIVE
PRISTINE = ROOT / 'src/releases/10.6.8' / RELATIVE
PATCH = ROOT / 'patches/RubyOnRails-28.1-ppc-plist.patch'
APPLE_BLOBS = {
    'RubyOnRails.plist': '5d55787f54c760a4e10d82b4a3ae9357ad64dd4c',
    'gen_plist.rb': '34e5e235b5ba33be67f1ca6349d6096f59a97191',
}


class RubyOnRailsPPCPlistTests(unittest.TestCase):
    def test_exact_apple_delta_and_pristine_snapshot(self):
        diffs = []
        for name, apple_blob in APPLE_BLOBS.items():
            original = (PRISTINE / name).read_bytes()
            blob = b'blob ' + str(len(original)).encode() + b'\0' + original
            self.assertEqual(hashlib.sha1(blob).hexdigest(), apple_blob)
            relative = 'src/powerpc/' + str(RELATIVE / name)
            diffs.extend(difflib.unified_diff(
                original.decode().splitlines(keepends=True),
                (SOURCE / name).read_text().splitlines(keepends=True),
                fromfile='a/' + relative,
                tofile='b/' + relative,
            ))
        self.assertEqual(PATCH.read_text(), ''.join(diffs))

    def test_installed_plist_parses_and_covers_each_gem_once(self):
        records = plistlib.loads((SOURCE / 'RubyOnRails.plist').read_bytes())
        self.assertIsInstance(records, list)
        names = [r['OpenSourceProject'] + '-' + r['OpenSourceVersion'] for r in records]
        gems = {p.stem for p in (SOURCE / 'gems').rglob('*.gem')}
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), gems)
        self.assertEqual(len(gems), 37)

    def test_generator_emits_complete_plist_without_gems(self):
        # An empty gem directory avoids external gem, openssl, and SVN commands.
        # This runs only the Ruby source script; it never builds an extension.
        with tempfile.TemporaryDirectory() as empty_dir:
            result = subprocess.run(
                ['ruby', '--disable-gems', str(SOURCE / 'gen_plist.rb')],
                cwd=empty_dir, capture_output=True, text=True, check=True,
            )
        self.assertEqual(plistlib.loads(result.stdout.encode()), [])


if __name__ == '__main__':
    unittest.main()
