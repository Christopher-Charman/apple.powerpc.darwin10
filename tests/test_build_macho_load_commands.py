import importlib.util
import struct
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
spec = importlib.util.spec_from_file_location('inspect_build_zip', str(ROOT / 'tools/inspect_build_zip.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sample(command=None):
    commands = command or b''
    return b'\xfe\xed\xfa\xce' + struct.pack('>IIIIII', 18, 0, 2, 1 if command else 0, len(commands), 0) + commands


class MachOLoadCommandTests(unittest.TestCase):
    def test_dylib_dependency(self):
        name = b'/usr/lib/libSystem.B.dylib\0'
        command = struct.pack('>IIIIII', 0xc, 24 + len(name), 24, 0, 0, 0) + name
        data = sample(command)
        self.assertEqual(module.macho_load_commands(data, 0, len(data))['dependencies'], ['/usr/lib/libSystem.B.dylib'])
        self.assertEqual(module.macho_load_commands(data, 0, len(data))['dylib_versions'][0]['compatibility_version'], 0)

    def test_rejects_overflow(self):
        data = sample(struct.pack('>II', 0xc, 999))
        with self.assertRaisesRegex(ValueError, 'load command bounds'):
            module.macho_load_commands(data, 0, len(data))

    def test_rejects_bad_name_offset(self):
        data = sample(struct.pack('>IIIIII', 0xc, 24, 100, 0, 0, 0))
        with self.assertRaisesRegex(ValueError, 'install name offset'):
            module.macho_load_commands(data, 0, len(data))


if __name__ == '__main__':
    unittest.main()
