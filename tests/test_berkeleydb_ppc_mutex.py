"""Source-only regression for BerkeleyDB's PowerPC test-and-set mutex."""

import difflib
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("BerkeleyDB-18/db/dbinc/mutex_int.h")
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
SOURCE = ROOT / "src/powerpc" / RELATIVE
PATCH = ROOT / "patches/BerkeleyDB-18-ppc-mutex.patch"
PATH = "src/powerpc/BerkeleyDB-18/db/dbinc/mutex_int.h"


class BerkeleyDBPowerPCMutexTests(unittest.TestCase):
    def test_pristine_snapshot_and_exact_patch(self):
        original = SNAPSHOT.read_bytes()
        blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         "79e42bf99905748e0720c578c31ed3654ca78fe2")
        before = original.decode().splitlines(keepends=True)
        after = SOURCE.read_text().splitlines(keepends=True)
        expected = "".join(difflib.unified_diff(
            before, after, fromfile="a/" + PATH, tofile="b/" + PATH))
        self.assertEqual(PATCH.read_text(), expected)
        self.assertEqual(expected.count("@@ -"), 1)

    def test_ppc_lock_word_and_result_are_independent_of_address(self):
        original = SNAPSHOT.read_text()
        source = SOURCE.read_text()
        start = source.index(" * PowerPC/gcc assembly.")
        end = source.index(" * OS/390 C", start)
        ppc = source[start:end]
        self.assertIn('"       stwcx.  %1,0,%1', original)
        self.assertIn('return (int)tsl;', original)
        self.assertIn("MUTEX_SET(tsl_t *tsl)", ppc)
        self.assertIn(': "=&r" (acquired)', ppc)
        self.assertIn(': "r" (tsl)', ppc)
        self.assertNotIn("return (int)tsl;", ppc)
        self.assertNotIn('"       stwcx.  %1,0,%1', ppc)
        instructions = [
            'lwarx   %0,0,%1', 'cmpwi   %0,0', 'bne-    1f',
            'li      %0,1', 'stwcx.  %0,0,%1', 'bne-    0b',
            'isync', 'b       2f', 'li      %0,0',
        ]
        positions = [ppc.index(instruction) for instruction in instructions]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('return acquired;', ppc)
        self.assertIn('asm volatile("sync" : : : "memory")', ppc)
        self.assertIn('return *tsl = 0;', ppc)

    def test_ppc64_address_fixture(self):
        address = 0x100000000
        old_stored_word = address & 0xffffffff
        corrected_stored_word = 1
        self.assertEqual(old_stored_word, 0)
        self.assertNotEqual(old_stored_word, corrected_stored_word)


if __name__ == "__main__":
    unittest.main()
