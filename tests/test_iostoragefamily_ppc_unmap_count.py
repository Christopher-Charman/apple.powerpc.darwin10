"""Source-only regression for the PPC32 DKIOCUNMAP extent allocation bound."""

import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("IOStorageFamily-116.1.41/IOMediaBSDClient.cpp")
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
SOURCE = ROOT / "src/powerpc" / RELATIVE
STORAGE_H = ROOT / "src/releases/10.6.8/IOStorageFamily-116.1.41/IOStorage.h"
DISK_H = ROOT / "src/releases/10.6.8/xnu-1504.15.3/bsd/sys/disk.h"
IOLIB_H = ROOT / "src/releases/10.6.8/xnu-1504.15.3/iokit/IOKit/IOLib.h"
PATCH = ROOT / "patches/IOStorageFamily-116.1.41-ppc-unmap-count.patch"
PATH = "src/powerpc/" + str(RELATIVE)


class IOStorageFamilyPPCUnmapCountTests(unittest.TestCase):
    def test_pristine_snapshot_and_exact_patch(self):
        original = SNAPSHOT.read_bytes()
        blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         "6972e0e762ded99b7c94fe8628d8c456a4412299")
        expected = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile="a/" + PATH, tofile="b/" + PATH))
        self.assertEqual(PATCH.read_text(), expected)
        self.assertEqual(expected.count("@@ -"), 1)

    def test_32_bit_extent_contract_and_guard(self):
        disk = DISK_H.read_text()
        storage = STORAGE_H.read_text()
        iolib = IOLIB_H.read_text()
        self.assertRegex(disk, r"dk_extent_t;[\s\S]*?uint32_t\s+extentsCount;[\s\S]*?dk_unmap_t;")
        self.assertRegex(storage, r"struct IOStorageExtent\s*\{\s*UInt64 byteStart;\s*UInt64 byteCount;")
        self.assertRegex(iolib, r"#define IONew\(type,number\)\s+\(type\*\)IOMalloc\(sizeof\(type\) \* \(number\) \)")
        original = SNAPSHOT.read_text()
        source = SOURCE.read_text()
        old = "if ( request.extents == 0 )  { error = EINVAL;  break; }"
        new = ("if ( request.extents == 0 ||\n"
               "                 request.extentsCount > 0xFFFFFFFFU / sizeof(IOStorageExtent) )\n"
               "            {\n"
               "                error = EINVAL;\n"
               "                break;\n"
               "            }")
        self.assertIn(old, original)
        self.assertEqual(source, original.replace(old, new, 1))
        body = source.split("case DKIOCUNMAP:", 1)[1].split("case DKIOCREQUESTIDLE:", 1)[0]
        self.assertLess(body.index(new), body.index("extents = IONew"))

    def test_overflow_boundary(self):
        extent_bytes = 2 * 8  # IOStorageExtent and dk_extent_t each hold two UInt64 fields.
        largest_safe_count = (2**32 - 1) // extent_bytes
        self.assertEqual(largest_safe_count, 0x0FFFFFFF)
        self.assertEqual((largest_safe_count + 1) * extent_bytes % 2**32, 0)
        self.assertEqual((largest_safe_count + 2) * extent_bytes % 2**32, 16)


if __name__ == "__main__":
    unittest.main()
