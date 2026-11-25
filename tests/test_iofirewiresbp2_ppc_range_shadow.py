"""Source-only regression for the SBP2 PPC32 kernel range conversion."""

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("IOFireWireSBP2-406.4.1/IOFireWireSBP2/IOFireWireSBP2ORB.cpp")
SOURCE = ROOT / "src/powerpc" / RELATIVE
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
USER_CLIENT = (ROOT / "src/powerpc/IOFireWireSBP2-406.4.1/IOFireWireSBP2"
               / "IOFireWireSBP2UserClient.cpp")
OLD = b"\t\tIOAddressRange * address_ranges = IONew( IOAddressRange, withCount );"
NEW = b"\t\taddress_ranges = IONew( IOAddressRange, withCount );"


class SBP2RangeShadowTests(unittest.TestCase):
    def test_pristine_apple_blob_and_exact_source_delta(self):
        original = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "91bc958b50811de5768e16146a655f57a300e6f7")
        self.assertEqual(original.count(OLD), 1)
        self.assertEqual(SOURCE.read_bytes(), original.replace(OLD, NEW))

    def test_one_array_is_allocated_used_and_freed(self):
        body = SOURCE.read_bytes().split(
            b"IOFireWireSBP2ORB::setCommandBuffersAsRanges(", 1)[1].split(
            b"IOFireWireSBP2ORB::setCommandBuffersAsRanges64(", 1)[0]
        self.assertEqual(body.count(b"IOAddressRange * address_ranges"), 1)
        self.assertIn(b"IOAddressRange * address_ranges = NULL;", body)
        self.assertIn(NEW, body)
        self.assertIn(b"address_ranges[i].address = ranges[i].address;", body)
        self.assertIn(b"withAddressRanges( address_ranges, withCount", body)
        self.assertIn(b"IODelete( address_ranges, IOAddressRange, withCount );", body)
        self.assertIn(b"if( withCount == 0 )", body)

    def test_user_client_uses_separate_64_bit_route(self):
        self.assertIn(b"orb->setCommandBuffersAsRanges64(", USER_CLIENT.read_bytes())


if __name__ == "__main__":
    unittest.main()
