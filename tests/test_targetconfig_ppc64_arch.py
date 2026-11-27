"""Source-only regression guard for the TargetConfig 12.1 PPC64 declaration."""

import difflib
import plistlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = Path("TargetConfig-12.1/MacOSX.plist")
UPSTREAM = ROOT / "src/releases/10.6.8" / REL
WORKING = ROOT / "src/powerpc" / REL
PATCH = ROOT / "patches/TargetConfig-12.1-ppc64-arch.patch"
STANZA = ("\t\t<key>ppc64</key>\n"
          "\t\t<dict>\n"
          "\t\t\t<key>TARGET_CPU_PPC64</key>\n"
          "\t\t\t<true/>\n"
          "\t\t\t<key>TARGET_RT_64_BIT</key>\n"
          "\t\t\t<true/>\n"
          "\t\t\t<key>TARGET_RT_BIG_ENDIAN</key>\n"
          "\t\t\t<true/>\n"
          "\t\t</dict>\n")


class TargetConfigPowerPC64Tests(unittest.TestCase):
    def test_architecture_values_and_later_conditionals(self):
        upstream = plistlib.loads(UPSTREAM.read_bytes())
        working = plistlib.loads(WORKING.read_bytes())
        self.assertNotIn("ppc64", upstream["TargetArchitectures"])
        self.assertEqual(working["TargetArchitectures"]["ppc64"], {
            "TARGET_CPU_PPC64": True,
            "TARGET_RT_64_BIT": True,
            "TARGET_RT_BIG_ENDIAN": True,
        })
        expected = plistlib.loads(UPSTREAM.read_bytes())
        expected["TargetArchitectures"]["ppc64"] = working["TargetArchitectures"]["ppc64"]
        self.assertEqual(working, expected)
        self.assertTrue(working["TargetConditionals"]["TARGET_HAVE_QUARANTINE"])
        self.assertTrue(working["TargetConditionals"]["TARGET_HAVE_SANDBOX"])

    def test_only_reviewed_component_delta_and_exact_patch(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        marker = "\t\t<key>i386</key>"
        self.assertEqual(upstream.count(marker), 1)
        self.assertEqual(working, upstream.replace(marker, STANZA + marker, 1))
        release_dir = UPSTREAM.parent
        working_dir = WORKING.parent
        self.assertEqual(
            {p.relative_to(release_dir) for p in release_dir.rglob("*") if p.is_file()},
            {p.relative_to(working_dir) for p in working_dir.rglob("*") if p.is_file()},
        )
        for original in release_dir.rglob("*"):
            if original.is_file() and original != UPSTREAM:
                self.assertEqual((working_dir / original.relative_to(release_dir)).read_bytes(),
                                 original.read_bytes())
        diff = "".join(difflib.unified_diff(
            upstream.splitlines(keepends=True), working.splitlines(keepends=True),
            fromfile="a/src/powerpc/" + str(REL),
            tofile="b/src/powerpc/" + str(REL),
        ))
        self.assertEqual(PATCH.read_text(), diff)

    def test_architecture_consumers_read_target_dictionary(self):
        source = (WORKING.parent / "tconf.c").read_text()
        wrapper = (WORKING.parent / "bin/gcc").read_text()
        self.assertIn('CFSTR("TargetArchitectures")', source.split("cmd_archs(CFDictionaryRef config)", 1)[1])
        self.assertIn('CFSTR("TargetArchitectures")', source.split("lookup_arch_config(CFDictionaryRef config", 1)[1])
        self.assertIn('`tconf --archs`', wrapper)


if __name__ == "__main__":
    unittest.main()
