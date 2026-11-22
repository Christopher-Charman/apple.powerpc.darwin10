"""Source-only regression for CF's PowerPC64 HALT definition."""

import difflib
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("CF-550.43/CFInternal.h")
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
SOURCE = ROOT / "src/powerpc" / RELATIVE
PATCH = ROOT / "patches/CF-550.43-ppc64-halt.patch"
RUNTIME = ROOT / "src/powerpc/CF-550.43/CFRuntime.c"
PATH = "src/powerpc/CF-550.43/CFInternal.h"


class CFPowerPC64HaltTests(unittest.TestCase):
    def test_pristine_release_and_exact_patch(self):
        original = SNAPSHOT.read_bytes()
        blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         "7f8d9a6e01ab538f1d7f74b2c0d26b0ba04a9706")
        expected = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile="a/" + PATH, tofile="b/" + PATH))
        self.assertEqual(PATCH.read_text(), expected)
        self.assertEqual(expected.count("@@ -"), 1)

    def test_both_powerpc_modes_reach_the_existing_trap(self):
        original = SNAPSHOT.read_text()
        source = SOURCE.read_text()
        self.assertIn("#if defined(__ppc__)\n    #define HALT", original)
        self.assertIn("#if defined(__ppc__) || defined(__ppc64__)\n"
                      "    #define HALT do {asm __volatile__(\"trap\");", source)
        self.assertIn("#elif defined(__i386__) || defined(__x86_64__)", source)
        self.assertIn("if (NULL == cf) HALT;", RUNTIME.read_text())


if __name__ == "__main__":
    unittest.main()
