import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_darwinbuild_context', str(ROOT / 'tools/verify_darwinbuild_context.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DarwinBuildContextTests(unittest.TestCase):
    def test_build_index_inheritance(self):
        builds = module.inspect()
        self.assertEqual(len(builds), 9)
        self.assertEqual(builds[0]['build'], '10A432')
        self.assertEqual(builds[-1]['build'], '10K540')
        self.assertEqual(builds[0]['default_architectures'], ['i386', 'x86_64'])
        self.assertTrue(all(builds[i]['inherits'] == builds[i-1]['build'] for i in range(1, len(builds))))


if __name__ == '__main__':
    unittest.main()
