"""Source-only regression for the Libinfo 32-bit IPv6 Teredo prefix check."""
import difflib
import hashlib
import os
import re
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("PPC_LIBINFO_TEST_ROOT", Path(__file__).resolve().parents[1]))
REL = Path("src/releases/10.6.8/Libinfo-330.10/lookup.subproj/si_getaddrinfo.c")
WORK = Path("src/powerpc/Libinfo-330.10/lookup.subproj/si_getaddrinfo.c")
PATCH = Path("patches/Libinfo-330.10-ppc-teredo-prefix.patch")
OLD = "sa6->sin6_addr.__u6_addr.__u6_addr32[0] == ntohs(TEREDO_PREFIX_32)"
NEW = "sa6->sin6_addr.__u6_addr.__u6_addr32[0] == ntohl(TEREDO_PREFIX_32)"


class LibinfoTeredoPrefixTests(unittest.TestCase):
    def test_pristine_release_and_exact_patch(self):
        original = (ROOT / REL).read_bytes()
        working = (ROOT / WORK).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(original)).encode() + b"\0" + original).hexdigest()
        self.assertEqual(blob, "780a13368aca539601acc6e6f2a9bc528cfe0b89")
        self.assertEqual(original.count(OLD.encode()), 1)
        self.assertEqual(working, original.replace(OLD.encode(), NEW.encode()))
        expected = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            working.decode().splitlines(keepends=True),
            fromfile="a/" + str(WORK), tofile="b/" + str(WORK)))
        self.assertEqual((ROOT / PATCH).read_text(), expected)

    def test_32_bit_prefix_semantics_for_both_endian_orders(self):
        source = (ROOT / WORK).read_text()
        match = re.search(r"#define TEREDO_PREFIX_32\s+(0x[0-9a-fA-F]+)", source)
        self.assertIsNotNone(match)
        prefix = int(match.group(1), 16)
        self.assertEqual(prefix, 0x20010000)
        self.assertIn(NEW, source)
        self.assertIn("__u6_addr16[0] == ntohs(V6TO4_PREFIX_16)", source)
        for order in ("big", "little"):
            converted = int.from_bytes(prefix.to_bytes(4, "big"), order)
            self.assertEqual(int.from_bytes(bytes.fromhex("20010000"), order), converted)
            self.assertNotEqual(int.from_bytes(bytes.fromhex("00000000"), order), converted)
            self.assertNotEqual(int.from_bytes(bytes.fromhex("20010001"), order), converted)
            # The former 16-bit conversion dropped the high prefix bits.
            self.assertNotEqual(converted, int.from_bytes((prefix & 0xffff).to_bytes(2, "big"), order))


if __name__ == "__main__":
    unittest.main()
