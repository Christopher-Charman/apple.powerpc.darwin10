import importlib.util
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ppc_cross', str(ROOT / 'tools/qualify_ppc_cross_compile.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CrossCompileGateTests(unittest.TestCase):
    def test_sources_exist(self):
        for name in module.SOURCES:
            self.assertTrue((ROOT / 'src/releases/10.6.8/Libcpp_kext-8' / name).is_file())

    def test_elf_header_values(self):
        header = bytearray(52)
        header[:6] = b'\x7fELF\x01\x02'
        struct.pack_into('>HH', header, 16, 1, 20)
        self.assertEqual(struct.unpack_from('>H', header, 18)[0], 20)


if __name__ == '__main__':
    unittest.main()
