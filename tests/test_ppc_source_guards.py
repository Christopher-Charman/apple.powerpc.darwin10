import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scan_ppc_source_guards', str(ROOT / 'tools/scan_ppc_source_guards.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PPCSourceGuardsTests(unittest.TestCase):
    def test_recovered_architecture_guard_evidence(self):
        rows = module.scan()
        self.assertEqual(len(rows), 51)
        self.assertTrue(any('IONDRVFramebuffer.cpp' in row['file'] and row['ppc_mentioned'] for row in rows))
        self.assertTrue(any(row['intel_mentioned'] for row in rows))


if __name__ == '__main__':
    unittest.main()
