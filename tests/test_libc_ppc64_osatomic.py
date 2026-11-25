"""Source-only regression for Libc PowerPC64 OSAtomic 32-bit returns."""

import difflib
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("Libc-594.9.5/ppc/sys/OSAtomic.s")
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
SOURCE = ROOT / "src/powerpc" / RELATIVE
DONOR = ROOT / "src/releases/10.5/Libc-498.1.7/ppc/sys/OSAtomic.s"
PPC64_SOURCES = ROOT / "src/powerpc/Libc-594.9.5/ppc64/sys/Makefile.inc"
PATCH = ROOT / "patches/Libc-594.9.5-ppc64-osatomic.patch"
PATH = "src/powerpc/Libc-594.9.5/ppc/sys/OSAtomic.s"


def section(source, start, end):
    return source[source.index(start):source.index(end)]


class LibcPPC64OSAtomicTests(unittest.TestCase):
    def test_pristine_snapshot_and_exact_two_hunk_patch(self):
        original = SNAPSHOT.read_bytes()
        blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         "24858e901e314c389dfaa153470ef83c30da571b")
        expected = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile="a/" + PATH, tofile="b/" + PATH))
        self.assertEqual(PATCH.read_text(), expected)
        self.assertEqual(expected.count("@@ -"), 2)

    def test_ppc64_uses_ppc_atomic_source(self):
        makefile = PPC64_SOURCES.read_text()
        self.assertIn(".PATH: ${.CURDIR}/ppc/sys ${.CURDIR}/ppc64/sys", makefile)
        self.assertIn("MDSRCS+= OSAtomic.s", makefile)
        self.assertFalse((PPC64_SOURCES.parent / "OSAtomic.s").exists())

    def test_restore_exact_apple_ppc64_return_paths(self):
        source = SOURCE.read_text()
        donor = DONOR.read_text()
        for start, end in (
            ("/* int32_t\tOSAtomicAdd32(", "/* int32_t\tOSAtomicOr32("),
            ("/* int32_t\tOSAtomicAdd32Barrier(",
             "/* int32_t\tOSAtomicOr32Barrier("),
        ):
            self.assertEqual(section(source, start, end), section(donor, start, end))
        add = section(source, "/* int32_t\tOSAtomicAdd32(",
                      "/* int32_t\tOSAtomicOr32(")
        barrier = section(source, "/* int32_t\tOSAtomicAdd32Barrier(",
                          "/* int32_t\tOSAtomicOr32Barrier(")
        self.assertIn("ba      _COMM_PAGE_ATOMIC_ADD32", add)
        self.assertIn("bla\t    _COMM_PAGE_ATOMIC_ADD32", add)
        self.assertIn("extsw   r3,r3", add)
        self.assertIn("mr      r3,r4", barrier)
        self.assertIn("extsw   r3,r4", barrier)


if __name__ == "__main__":
    unittest.main()
