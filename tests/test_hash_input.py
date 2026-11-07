import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.hash_input import hash_file


class InputHashTests(unittest.TestCase):
    def test_hash_regular_file_without_modification(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.bin"
            payload = b"PowerPC Darwin test input\x00"
            path.write_bytes(payload)
            before = path.stat()
            result = hash_file(path)
            self.assertEqual(result["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(result["bytes"], len(payload))
            self.assertEqual(result["identifier"], str(path))
            self.assertEqual(path.read_bytes(), payload)
            self.assertEqual(path.stat().st_mtime_ns, before.st_mtime_ns)

    def test_reject_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                hash_file(Path(folder))

    def test_reject_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "target"
            target.write_bytes(b"x")
            link = Path(folder) / "link"
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                hash_file(link)


if __name__ == "__main__":
    unittest.main()
