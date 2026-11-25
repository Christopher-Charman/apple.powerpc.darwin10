"""Source-only regression for zero-sized PPC KEXT nothrow array allocation."""

import hashlib
from difflib import unified_diff
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = Path("Libcpp_kext-8/new_opvnt.cc")
SOURCE = ROOT / "src/powerpc" / REL
SNAPSHOT = ROOT / "src/releases/10.6.8" / REL
COMPONENT = ROOT / "src/powerpc/Libcpp_kext-8"
XNU = ROOT / "src/releases/10.6.8/xnu-1504.15.3/libkern/c++/OSRuntime.cpp"
OLD = b"  return kern_os_malloc(sz);\n"
NEW = (b"  /* PowerPC Darwin 10 restoration, 2026-11-25: kern_os_malloc(0)\n"
       b"     returns NULL; match the scalar and kernel array operators. */\n"
       b"  if (sz == 0) sz = 1;\n"
       b"  return kern_os_malloc(sz);\n")


def blob_sha(contents):
    return hashlib.sha1(b"blob " + str(len(contents)).encode() + b"\0" + contents).hexdigest()


class KextZeroArrayTests(unittest.TestCase):
    def test_pristine_apple_blob_and_exact_patch(self):
        pristine = SNAPSHOT.read_bytes()
        self.assertEqual(blob_sha(pristine), "a86bd0f42a34dc930f6e3eb6d467ecf56665abb7")
        self.assertEqual(pristine.count(OLD), 1)
        self.assertEqual(SOURCE.read_bytes(), pristine.replace(OLD, NEW))

    def test_review_patch_is_exact_source_delta(self):
        old = SNAPSHOT.read_text().splitlines(keepends=True)
        new = SOURCE.read_text().splitlines(keepends=True)
        expected = "".join(unified_diff(
            old, new,
            fromfile="a/src/releases/10.6.8/Libcpp_kext-8/new_opvnt.cc",
            tofile="b/src/powerpc/Libcpp_kext-8/new_opvnt.cc"))
        patch = ROOT / "patches/Libcpp_kext-8-ppc-zero-array.patch"
        self.assertEqual(patch.read_text(), expected)

    def test_zero_allocation_contract_and_ppc_guard(self):
        xnu = XNU.read_text()
        self.assertRegex(xnu, re.compile(
            r"kern_os_malloc\(size_t size\).*?if \(size == 0\)\s*\{\s*return \(0\);",
            re.S))
        source = SOURCE.read_text()
        self.assertIn("#if defined(__i386__) || defined(__ppc__)", source)
        self.assertRegex(source, re.compile(
            r"operator new\[\] \(unsigned long sz, const std::nothrow_t&.*?"
            r"if \(sz == 0\) sz = 1;\s*return kern_os_malloc\(sz\);",
            re.S))
        self.assertRegex((COMPONENT / "new_opnt.cc").read_text(), re.compile(
            r"operator new \(unsigned long sz, const std::nothrow_t&\).*?"
            r"if \(sz == 0\)\s*sz = 1;\s*return kern_os_malloc\(sz\);",
            re.S))
        self.assertRegex((COMPONENT / "new_opv.cc").read_text(), re.compile(
            r"operator new\[\] \(unsigned long sz\).*?"
            r"if \(sz == 0\) sz = 1;\s*return kern_os_malloc\(sz\);",
            re.S))


if __name__ == "__main__":
    unittest.main()
