import importlib.util
import struct
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('inspect_ppc_macho', str(ROOT / 'tools/inspect_ppc_macho.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MachOTests(unittest.TestCase):
    def inspect_bytes(self, data):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'binary'
            p.write_bytes(data)
            return module.inspect(p)

    def test_thin_ppc(self):
        self.assertTrue(self.inspect_bytes(b'\xfe\xed\xfa\xce' + struct.pack('>II', 18, 0) + b'\0' * 20)['contains_ppc'])

    def test_thin_intel(self):
        self.assertFalse(self.inspect_bytes(b'\xce\xfa\xed\xfe' + struct.pack('<II', 7, 3) + b'\0' * 20)['contains_ppc'])

    def test_fat_ppc_intel(self):
        header = b'\xca\xfe\xba\xbe' + struct.pack('>I', 2)
        header += struct.pack('>IIIII', 18, 0, 48, 16, 0)
        header += struct.pack('>IIIII', 7, 3, 64, 16, 0)
        result = self.inspect_bytes(header + b'X' * 32)
        self.assertEqual({x['cpu'] for x in result['architectures']}, {'ppc', 'i386'})

    def test_rejects_out_of_bounds(self):
        header = b'\xca\xfe\xba\xbe' + struct.pack('>I', 1) + struct.pack('>IIIII', 18, 0, 999, 20, 0)
        with self.assertRaisesRegex(ValueError, 'bounds'):
            self.inspect_bytes(header)

    def test_rejects_non_macho(self):
        with self.assertRaisesRegex(ValueError, 'not Mach-O'):
            self.inspect_bytes(b'not macho data')


if __name__ == '__main__':
    unittest.main()
