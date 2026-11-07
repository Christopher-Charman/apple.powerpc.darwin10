import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_ppc_dependency_sources', str(ROOT / 'tools/verify_ppc_dependency_sources.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourceDependencyTests(unittest.TestCase):
    def test_recovered_dependency_coverage(self):
        result = module.main()
        self.assertEqual(len(result['dependencies']), 26)
        self.assertTrue(any('Libsystem-125.2.11' in x['official_source_tags'] for x in result['dependencies']))
        self.assertTrue(any('net_snmp-127' in x['official_source_tags'] for x in result['dependencies']))
        self.assertTrue(any(x['source_availability'] == 'external_or_closed_source' for x in result['dependencies']))
        self.assertTrue(all(x['source_availability'] == 'release_exact_vendored' for x in result['dependencies'] if x['official_source_tags']))

    def test_unclassified_dependency_rejected(self):
        release = json.loads((ROOT / 'source-releases/10.6.8.json').read_text(encoding='utf-8'))
        inventory = {'macho_magic_candidates': [{'contains_ppc': True, 'cpu_types': [18],
                     'slice_load_commands': [{'dependencies': ['/unknown/libunexpected.dylib']}]}]}
        with self.assertRaisesRegex(ValueError, 'unclassified'):
            module.resolve(inventory, release)

    def test_missing_source_family_rejected(self):
        inventory = {'macho_magic_candidates': [{'contains_ppc': True, 'cpu_types': [18],
                     'slice_load_commands': [{'dependencies': ['/usr/lib/libSystem.B.dylib']}]}]}
        with self.assertRaisesRegex(ValueError, 'source family missing'):
            module.resolve(inventory, {'release': 'test', 'projects': []})


if __name__ == '__main__':
    unittest.main()
