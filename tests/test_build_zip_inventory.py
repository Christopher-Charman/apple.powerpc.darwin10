import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RecoveredBuildInventoryTests(unittest.TestCase):
    def test_exact_historical_inventory(self):
        data = json.loads((ROOT / 'docs/build_zip_direct_binary_inventory.json').read_text(encoding='utf-8'))
        self.assertEqual(data['archive_sha256'], 'a7bb2bab2112673dec9fe57e66221431b78d06a2ec134ac75ae0fc24b24fe77f')
        self.assertEqual(data['tome_sha256'], '0121ff2d17ce7492706b00eda1c9fdb04b803f54c0a33e11c1ce6a12a3d727ec')
        self.assertEqual(data['entries'], 5188)
        self.assertEqual(len(data['macho_magic_candidates']), 126)
        self.assertTrue(all(x['contains_ppc'] for x in data['macho_magic_candidates']))
        for artifact in data['macho_magic_candidates']:
            versions = [tuple((d['name'], d['current_version'], d['compatibility_version']) for d in item['dylib_versions']) for item in artifact['slice_load_commands']]
            self.assertEqual(len(set(versions)), 1, artifact['path'])
        self.assertEqual(len(set(x['path'] for x in data['macho_magic_candidates'])), 126)
        self.assertTrue(all(len(x['sha256']) == 64 for x in data['macho_magic_candidates']))


if __name__ == '__main__':
    unittest.main()
