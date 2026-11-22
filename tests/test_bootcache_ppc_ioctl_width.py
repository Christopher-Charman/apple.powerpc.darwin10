"""Source-only regression for BootCache's 64-bit disk ioctl result on PPC."""

import difflib
import hashlib
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("BootCache-64.2/kext.c")
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
SOURCE = ROOT / "src/powerpc" / RELATIVE
DISK_H = ROOT / "src/releases/10.6.8/xnu-1504.15.3/bsd/sys/disk.h"
PATCH = ROOT / "patches/BootCache-64.2-ppc-ioctl-width.patch"
PATH = "src/powerpc/BootCache-64.2/kext.c"


class BootCachePPCIOCTLWidthTests(unittest.TestCase):
    def test_pristine_snapshot_and_exact_patch(self):
        original = SNAPSHOT.read_bytes()
        blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         "6ee5d4c5cde2f72bb5c0f7f664f0df0228692bfd")
        expected = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile="a/" + PATH, tofile="b/" + PATH))
        self.assertEqual(PATCH.read_text(), expected)
        self.assertEqual(expected.count("@@ -"), 1)

    def test_ioctl_contract_and_matching_storage(self):
        disk_h = DISK_H.read_text()
        self.assertRegex(disk_h, r"#define\s+DKIOCGETMAXBYTECOUNTREAD\s+_IOR\('d',\s*70,\s*uint64_t\)")
        original = SNAPSHOT.read_text()
        source = SOURCE.read_text()
        start = source.index("BC_init_cache(size_t length, user_addr_t uptr, u_int64_t blocksize)\n{")
        body = source[start:source.index("\n/*\n *", start)]
        self.assertIn("int error, max_byte_count;", original)
        self.assertRegex(body, r"\bu_int64_t\s+max_byte_count\s*;")
        self.assertNotRegex(body, r"\bint\s+error\s*,\s*max_byte_count\s*;")
        self.assertRegex(body, r"DKIOCGETMAXBYTECOUNTREAD\s*,\s*\(caddr_t\)&max_byte_count")
        self.assertRegex(body, r"c_maxread\s*>\s*max_byte_count\s*&&\s*max_byte_count\s*>\s*0")

    def test_big_endian_result_requires_eight_bytes(self):
        sample_limit = 0x10000
        returned = struct.pack(">Q", sample_limit)
        self.assertEqual(len(returned), 8)
        self.assertEqual(struct.unpack(">I", returned[:4])[0], 0)
        self.assertEqual(struct.unpack(">Q", returned)[0], sample_limit)


if __name__ == "__main__":
    unittest.main()
