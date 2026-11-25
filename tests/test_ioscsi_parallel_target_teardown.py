"""Source-only regression for the IOSCSIParallelFamily final target teardown."""

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("IOSCSIParallelFamily-211.0.0/IOSCSIParallelInterfaceController.cpp")
SOURCE = ROOT / "src/powerpc" / RELATIVE
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
OLD = b"for ( index = 0; index < fHighestSupportedDeviceID; index++ )"
NEW = b"for ( index = 0; index <= fHighestSupportedDeviceID; index++ )"


def git_blob_sha(contents):
    return hashlib.sha1(b"blob " + str(len(contents)).encode() + b"\0" + contents).hexdigest()


class SCSIParallelTargetTeardownTests(unittest.TestCase):
    def test_pristine_apple_blob_and_exact_source_delta(self):
        pristine = SNAPSHOT.read_bytes()
        self.assertEqual(git_blob_sha(pristine),
                         "e693f1c8a8d67001807288c9bb750732e50f49e8")
        self.assertEqual(pristine.count(OLD), 1)
        self.assertEqual(SOURCE.read_bytes(), pristine.replace(OLD, NEW))

    def test_last_target_is_created_accepted_and_destroyed(self):
        source = SOURCE.read_text()
        self.assertRegex(source, re.compile(
            r"for \( UInt32 index = 0; index <= fHighestSupportedDeviceID; index\+\+ \)"
            r"\s*\{\s*CreateTargetForID \( index \);", re.M))
        self.assertRegex(source, re.compile(
            r"IOSCSIParallelInterfaceController::willTerminate \(.*?"
            r"for \( index = 0; index <= fHighestSupportedDeviceID; index\+\+ \)"
            r"\s*\{\s*DestroyTargetForID \( index \);", re.S))
        self.assertIn("require ( ( targetID <= fHighestSupportedDeviceID ), INVALID_PARAMETER_FAILURE );", source)
        self.assertIn("victimDevice->DestroyTarget ( );", source)
        self.assertIn("victimDevice->terminate ( );", source)


if __name__ == "__main__":
    unittest.main()
