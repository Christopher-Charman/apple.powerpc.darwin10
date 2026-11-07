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
        self.assertTrue(self.inspect_bytes(b'\xfe\xed\xfa\xce' + struct.pack('>II', 18, 0) + struct.pack('>IIII', 1, 0, 0, 0))['contains_ppc'])

    def test_thin_intel(self):
        self.assertFalse(self.inspect_bytes(b'\xce\xfa\xed\xfe' + struct.pack('<II', 7, 3) + struct.pack('<IIII', 1, 0, 0, 0))['contains_ppc'])

    def test_fat_ppc_intel(self):
        header = b'\xca\xfe\xba\xbe' + struct.pack('>I', 2)
        header += struct.pack('>IIIII', 18, 0, 48, 28, 0)
        header += struct.pack('>IIIII', 7, 3, 76, 28, 0)
        ppc = b'\xfe\xed\xfa\xce' + struct.pack('>IIIIII', 18, 0, 1, 0, 0, 0)
        intel = b'\xce\xfa\xed\xfe' + struct.pack('<IIIIII', 7, 3, 1, 0, 0, 0)
        result = self.inspect_bytes(header + ppc + intel)
        self.assertEqual({x['cpu'] for x in result['architectures']}, {'ppc', 'i386'})

    def test_rejects_truncated_thin_header(self):
        with self.assertRaisesRegex(ValueError, 'truncated Mach-O header'):
            self.inspect_bytes(b'\xfe\xed\xfa\xce' + struct.pack('>II', 18, 0))

    def test_rejects_invalid_load_command_bounds(self):
        header = b'\xfe\xed\xfa\xce' + struct.pack('>IIIIII', 18, 0, 1, 1, 16, 0)
        with self.assertRaisesRegex(ValueError, 'load-command bounds'):
            self.inspect_bytes(header)

    def test_rejects_invalid_load_command_size(self):
        header = b'\xfe\xed\xfa\xce' + struct.pack('>IIIIII', 18, 0, 1, 1, 8, 0)
        with self.assertRaisesRegex(ValueError, 'load command size'):
            self.inspect_bytes(header + struct.pack('>II', 1, 4))

    def test_accepts_bounded_load_command(self):
        header = b'\xfe\xed\xfa\xce' + struct.pack('>IIIIII', 18, 0, 1, 1, 8, 0)
        self.assertTrue(self.inspect_bytes(header + struct.pack('>II', 2, 8))['contains_ppc'])

    def test_rejects_wrong_fat_cpu_even_if_named_ppc(self):
        header = b'\xca\xfe\xba\xbe' + struct.pack('>I', 1)
        header += struct.pack('>IIIII', 18, 0, 28, 28, 0)
        intel = b'\xce\xfa\xed\xfe' + struct.pack('<IIIIII', 7, 3, 1, 0, 0, 0)
        with self.assertRaisesRegex(ValueError, 'architecture does not match'):
            self.inspect_bytes(header + intel)

    def test_rejects_invalid_filetype(self):
        header = b'\xfe\xed\xfa\xce' + struct.pack('>IIIIII', 18, 0, 0, 0, 0, 0)
        with self.assertRaisesRegex(ValueError, 'file type'):
            self.inspect_bytes(header)

    def test_rejects_load_command_padding_mismatch(self):
        header = b'\xfe\xed\xfa\xce' + struct.pack('>IIIIII', 18, 0, 1, 1, 16, 0)
        with self.assertRaisesRegex(ValueError, 'size mismatch'):
            self.inspect_bytes(header + struct.pack('>II', 2, 8) + b'\0' * 8)

    def test_rejects_fake_fat_slice(self):
        header = b'\xca\xfe\xba\xbe' + struct.pack('>I', 1) + struct.pack('>IIIII', 18, 0, 28, 16, 0)
        with self.assertRaisesRegex(ValueError, 'not a Mach-O'):
            self.inspect_bytes(header + b'X' * 16)

    def test_rejects_out_of_bounds(self):
        header = b'\xca\xfe\xba\xbe' + struct.pack('>I', 1) + struct.pack('>IIIII', 18, 0, 999, 20, 0)
        with self.assertRaisesRegex(ValueError, 'bounds'):
            self.inspect_bytes(header)

    def test_rejects_non_macho(self):
        with self.assertRaisesRegex(ValueError, 'not Mach-O'):
            self.inspect_bytes(b'not macho data')


if __name__ == '__main__':
    unittest.main()
