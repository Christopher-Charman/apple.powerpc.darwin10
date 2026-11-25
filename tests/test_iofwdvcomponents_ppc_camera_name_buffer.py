"""Source-only regression for the FireWire DV Pascal camera-name capacity."""

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("IOFWDVComponents-199.4.1/DVIsochComponent.c")
SOURCE = ROOT / "src/powerpc" / RELATIVE
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE


class CameraNameBufferTests(unittest.TestCase):
    def test_pristine_apple_snapshot_and_exact_source_delta(self):
        original = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "f7b7a38bb3baa5c19d2caa2b86ef620f09d1cd3f")
        old = b"name, sizeof(name), CFStringGetSystemEncoding()"
        new = b"name, sizeof(Str255), CFStringGetSystemEncoding()"
        self.assertEqual(original.count(old), 2)
        self.assertEqual(SOURCE.read_bytes(), original.replace(old, new))

    def test_pascal_buffer_contract(self):
        source = SOURCE.read_bytes()
        self.assertIn(b"Str255 cameraName;", source)
        self.assertIn(b"cameraNameLookup(deviceDescriptionPtr, cameraName)", source)
        function = source.split(b"static OSStatus cameraNameLookup(", 1)[1].split(
            b"static OSStatus postEvent(", 1)[0]
        self.assertEqual(function.count(b"CFStringGetPascalString"), 2)
        self.assertEqual(function.count(b"name, sizeof(Str255),"), 2)
        self.assertNotIn(b"sizeof(name)", function)


if __name__ == "__main__":
    unittest.main()
