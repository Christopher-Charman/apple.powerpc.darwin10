"""Source-only regression for ioreg's registry entry ID success guard."""

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("IOKitTools-78/ioreg.tproj/ioreg.c")
SOURCE = ROOT / "src/powerpc" / RELATIVE
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE


class EntryIDGuardTests(unittest.TestCase):
    def test_pristine_apple_snapshot_and_exact_source_delta(self):
        original = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "a7f48e31ff3e150143eb89fca0fe2ed0e777d3bf")
        old = b"        if (status == KERN_SUCCESS);\n"
        new = b"        if (status == KERN_SUCCESS)\n"
        self.assertEqual(original.count(old), 1)
        self.assertEqual(SOURCE.read_bytes(), original.replace(old, new, 1))

    def test_entry_id_is_printed_only_after_successful_lookup(self):
        source = SOURCE.read_text()
        state_block = source.split("if (options.state)", 1)[1].split(
            "// Print out the busy state", 1)[0]
        self.assertRegex(state_block, re.compile(
            r"status = IORegistryEntryGetRegistryEntryID\(service, &entryID\);"
            r"\s*if \(status == KERN_SUCCESS\)\s*\{"
            r"\s*print\(\", id 0x%llx\", entryID\);\s*\}", re.S))
        self.assertNotIn("if (status == KERN_SUCCESS);", state_block)


if __name__ == "__main__":
    unittest.main()
