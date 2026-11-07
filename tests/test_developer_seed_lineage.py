import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_developer_seed_lineage', str(ROOT / 'tools/verify_developer_seed_lineage.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DeveloperSeedLineageTests(unittest.TestCase):
    def test_complete_seed_and_toolchain_lineage(self):
        self.assertEqual(module.verify(), (10, 6, 6))


if __name__ == '__main__':
    unittest.main()
