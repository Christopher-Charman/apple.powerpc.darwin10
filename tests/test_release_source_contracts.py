"""Regression checks for recovered PowerPC source comparisons."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('compare_ppc_sources', str(ROOT / 'tools/compare_ppc_sources.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourceComparisonTests(unittest.TestCase):
    def test_rejects_nonhistorical_source(self):
        with self.assertRaisesRegex(ValueError, 'outside historical'):
            module.compare('src/xnu', 'src/releases/10.6/notify-23')

    def test_rejects_missing_source(self):
        with self.assertRaisesRegex(ValueError, 'not committed'):
            module.compare('src/releases/10.6/not-real', 'src/releases/10.6/notify-23')

    def test_notify_successor_delta(self):
        result = module.compare('src/releases/10.6/notify-23', 'src/releases/10.6.8/notify-25.1')
        self.assertEqual(result['changed_files'], 4)
        self.assertEqual(result['runtime_parity'], 'not_assessed')

    def test_kext_successor_delta(self):
        result = module.compare('src/releases/10.6/kext_tools-177', 'src/releases/10.6.8/kext_tools-180.2.1')
        self.assertEqual(result['changed_files'], 10)

    def test_directory_service_delta(self):
        result = module.compare('src/releases/10.6/DirectoryService-621', 'src/releases/10.6.8/DirectoryService-621.12')
        self.assertEqual(result['changed_files'], 18)


if __name__ == '__main__':
    unittest.main()
