"""Source-only bounds regression for PowerPC password record references."""

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("DSPasswordServerPlugin-281.1/AuthFile.mm")
SOURCE = ROOT / "src/powerpc" / RELATIVE
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
OLD = "\tfor ( idx = 0; idx < len; idx++ ) {\n"
NEW = "\tfor ( idx = 0; idx < len / 2; idx++ ) {\n"


class PasswordReferenceDecodeTests(unittest.TestCase):
    def test_exact_apple_source_delta(self):
        original = SNAPSHOT.read_bytes()
        blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         "ebcea052ae353a8778b4acd73a80c58c0c3368eb")
        original = original.decode()
        start = original.index("static inline void ConvertHexToBinaryFastWithNtoHL")
        end = original.index("//\tpwsf_stringToPasswordRecRef", start)
        decoder = original[start:end]
        self.assertEqual(decoder.count(OLD), 1)
        self.assertEqual(SOURCE.read_text(), original[:start] + decoder.replace(OLD, NEW) + original[end:])

    def test_big_endian_loop_matches_reference_width(self):
        source = SOURCE.read_text()
        decoder = source.split("static inline void ConvertHexToBinaryFastWithNtoHL", 1)[1].split(
            "//\tpwsf_stringToPasswordRecRef", 1)[0]
        big_endian = decoder.split("#if TARGET_RT_BIG_ENDIAN", 1)[1].split("#else", 1)[0]
        self.assertIn(NEW, big_endian)
        self.assertRegex(big_endian, re.escape("*inHex++") + r"[\s\S]*" + re.escape("*inHex++"))
        self.assertIn("ConvertHexToBinaryFastWithNtoHL( inRefStr, 32, (unsigned char *)outPasswordRec );", source)
        header = (ROOT / "src/powerpc/DSPasswordServerPlugin-281.1/AuthFile.h").read_text()
        fields = header.split("typedef struct PWFileEntry {", 1)[1].split("BSDTimeStructCopy creationDate", 1)[0]
        self.assertEqual(len(re.findall(r"\bUInt32\s+\w+;", fields)), 4)
        hex_digits = "0123456789abcdeffedcba9876543210"
        record = bytearray(b"\xaa" * 32)
        for index in range(len(hex_digits) // 2):
            record[index] = int(hex_digits[index * 2:index * 2 + 2], 16)
        self.assertEqual(record[:16], bytes.fromhex(hex_digits))
        self.assertEqual(record[16:], b"\xaa" * 16)


if __name__ == "__main__":
    unittest.main()
