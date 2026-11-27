"""Source-only guard for SmartCardServices PPC64 to PPC32 reader respawn."""

import difflib
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = Path("SmartCardServices-36160/src/PCSC")
SOURCE = ROOT / "src/powerpc" / COMPONENT / "pcscdaemon.c"
SNAPSHOT = ROOT / "src/releases/10.6.8" / COMPONENT / "pcscdaemon.c"
READER = ROOT / "src/powerpc" / COMPONENT / "readerfactory.c"
PATCH = ROOT / "patches/SmartCardServices-36160-ppc32-respawn.patch"
OLD = b"\tstatic cpu_type_t only32cpu[] = { CPU_TYPE_I386 };\n"
NEW = (b"#if defined(__ppc__) || defined(__ppc64__)\n"
       b"\tstatic cpu_type_t only32cpu[] = { CPU_TYPE_POWERPC };\n"
       b"#else\n"
       b"\tstatic cpu_type_t only32cpu[] = { CPU_TYPE_I386 };\n"
       b"#endif\n")


class SmartCardServicesRespawnTests(unittest.TestCase):
    def test_exact_delta_from_pinned_apple_source(self):
        original = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "a33281ea8bf27772e1b9393ea094bf5f15e383ca")
        self.assertEqual(original.count(OLD), 1)
        self.assertEqual(SOURCE.read_bytes(), original.replace(OLD, NEW))
        fromfile = "a/src/powerpc/SmartCardServices-36160/src/PCSC/pcscdaemon.c"
        tofile = "b/src/powerpc/SmartCardServices-36160/src/PCSC/pcscdaemon.c"
        expected_patch = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile=fromfile, tofile=tofile))
        self.assertEqual(PATCH.read_text(), expected_patch)

    def test_ppc64_reader_mismatch_reaches_matching_32_bit_slice(self):
        reader = READER.read_text()
        daemon = SOURCE.read_text()
        check = reader.split("static int ReaderCheckArchitecture(LPCSTR lpcLibrary)\n{", 1)[1]
        check = check.split("static int architectureMatch(const char *name)\n{", 1)[0]
        respawn = daemon.split("void tryRespawn()\n{", 1)[1]
        self.assertIn("if (! (cputype & CPU_ARCH_ABI64))", check)
        self.assertIn("if (architectureMatch(lpcLibrary))", check)
        self.assertIn("kill(pid, SIGUSR2)", check)
        self.assertIn("respawn = 1;", daemon)
        self.assertIn("tryRespawn();", daemon)
        self.assertIn(NEW.decode(), respawn)
        self.assertIn("posix_spawnattr_setbinpref_np(&attr, only32cpuSize, only32cpu", respawn)


if __name__ == "__main__":
    unittest.main()
