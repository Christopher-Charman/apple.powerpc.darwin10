import difflib
import hashlib
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(os.environ.get('RUBYGEMS_TEST_ROOT', Path(__file__).resolve().parents[1]))
RELATIVE = Path('RubyGems-17.1/rubygems/lib/rubygems/platform.rb')
SOURCE = ROOT / 'src/powerpc' / RELATIVE
PRISTINE = ROOT / 'src/releases/10.6.8' / RELATIVE
PATCH = ROOT / 'patches/RubyGems-17.1-ppc-darwin10-platform.patch'
APPLE_BLOB = 'bfa8fca0ffaa46189b0ba7e493c4e8c49117541b'


class RubyGemsPPCPlatformTests(unittest.TestCase):
    def test_exact_apple_delta_and_pristine_snapshot(self):
        original = PRISTINE.read_bytes()
        blob = b'blob ' + str(len(original)).encode() + b'\0' + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(), APPLE_BLOB)
        path = 'src/powerpc/' + str(RELATIVE)
        expected = ''.join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual(PATCH.read_text(), expected)

    def test_darwin10_powerpc_and_universal_gem_matching(self):
        # Load only the historical platform source. No setup, gem installation,
        # extension build, or compiler is invoked.
        script = r'''
module Gem
  ConfigMap = {:arch => 'powerpc-darwin10.0'}
  def self.platforms
    [Gem::Platform::RUBY, Gem::Platform.local]
  end
end
load ARGV.fetch(0)
def check(label, condition)
  raise label unless condition
end
check('local Darwin 10', Gem::Platform.local.to_a == ['powerpc', 'darwin', '10'])
check('PowerPC Darwin 10', Gem::Platform.match('powerpc-darwin10.0'))
check('PowerPC Darwin 10 patch level', Gem::Platform.match('powerpc-darwin10.6.0'))
check('universal Darwin 10', Gem::Platform.match('universal-darwin10.0'))
check('unversioned PowerPC legacy gem', Gem::Platform.match('powerpc-darwin'))
check('reject Darwin 9 PowerPC', !Gem::Platform.match('powerpc-darwin9.8'))
check('reject Darwin 9 universal', !Gem::Platform.match('universal-darwin9.8'))
check('reject other CPU', !Gem::Platform.match('i686-darwin10.0'))
Gem::ConfigMap[:arch] = 'powerpc-darwin8.0'
Gem::Platform.instance_variable_set(:@local, nil)
check('Darwin 8 predecessor PowerPC', Gem::Platform.match('powerpc-darwin8.10.0'))
check('Darwin 8 predecessor universal', Gem::Platform.match('universal-darwin8.10.0'))
check('reject Darwin 10 on Darwin 8', !Gem::Platform.match('powerpc-darwin10.0'))
'''
        result = subprocess.run(
            ['ruby', '--disable-gems', '-e', script, str(SOURCE)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
