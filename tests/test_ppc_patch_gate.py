import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ppc_patch_gate', str(ROOT / 'tools/ppc_patch_gate.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PatchGateTests(unittest.TestCase):
    def test_modern_namespace_rejected_before_patch_read(self):
        class Stub:
            def read_text(self, encoding):
                return json.dumps(dict(target='10.6', source_tree='src/xnu', source_tree_sha='a'*40,
                                       patch='patches/any.patch', rationale='test', reviewer='independent'))
        with self.assertRaisesRegex(ValueError, 'outside Darwin'):
            module.inspect(Stub())

    def test_missing_review_rejected(self):
        class Stub:
            def read_text(self, encoding):
                return json.dumps(dict(target='10.6', source_tree='src/releases/10.6/xnu-1456.1.26',
                                       source_tree_sha='a'*40, patch='patches/any.patch', rationale='test'))
        with self.assertRaisesRegex(ValueError, 'reviewer'):
            module.inspect(Stub())

    def test_release_mismatch_rejected(self):
        class Stub:
            def read_text(self, encoding):
                return json.dumps(dict(target='10.5', source_tree='src/releases/10.6/xnu-1456.1.26',
                                       source_tree_sha='a'*40, patch='patches/any.patch', rationale='test', reviewer='independent'))
        with self.assertRaisesRegex(ValueError, 'release mismatch'):
            module.inspect(Stub())


if __name__ == '__main__':
    unittest.main()
