import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / 'tools'))
spec = importlib.util.spec_from_file_location('verify_ppc_artifact_manifest', str(ROOT / 'tools/verify_ppc_artifact_manifest.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ArtifactManifestTests(unittest.TestCase):
    def test_verified_ppc_and_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            binary = b'\xfe\xed\xfa\xce' + struct.pack('>II', 18, 0) + b'\0' * 20
            (root / 'binary').write_bytes(binary)
            data = {'archive_sha256': 'a' * 64, 'artifacts': [{'path': 'binary', 'sha256': hashlib.sha256(binary).hexdigest()}]}
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps(data), encoding='utf-8')
            self.assertEqual(len(module.verify(manifest, root)['verified']), 1)
            (root / 'binary').write_bytes(binary + b'X')
            with self.assertRaisesRegex(ValueError, 'byte mismatch'):
                module.verify(manifest, root)

    def test_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps({'archive_sha256': 'a'*64, 'artifacts': [{'path': '../other', 'sha256': 'a'*64}]}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'artifact path'):
                module.verify(manifest, root)


if __name__ == '__main__':
    unittest.main()
