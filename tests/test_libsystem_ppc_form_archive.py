"""Source-only regression for Libsystem's per-form libc wrapper scan."""

import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("Libsystem-125.2.11/libsys/build-libc.pl")
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
SOURCE = ROOT / "src/powerpc" / RELATIVE
PATCH = ROOT / "patches/Libsystem-125.2.11-ppc-form-archive.patch"
LIBSYS_MAKEFILE = ROOT / "src/powerpc/Libsystem-125.2.11/libsys/Makefile"
PLATFORM = ROOT / "src/powerpc/Libsystem-125.2.11/Platforms/MacOSX/Makefile.inc"


class LibsystemFormArchiveTests(unittest.TestCase):
    def test_pristine_snapshot_and_exact_patch(self):
        original = SNAPSHOT.read_bytes()
        blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         "f74a0300ec189ef597f09dacc1f70e16666ec884")
        path = "src/powerpc/" + RELATIVE.as_posix()
        diff = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile="a/" + path, tofile="b/" + path))
        self.assertEqual(PATCH.read_text(), diff)
        self.assertEqual(diff.count("@@ -"), 2)

    def test_each_form_scans_its_own_partial_archive(self):
        source = SOURCE.read_text()
        forms = dict((form, archive_suffix) for form, _, archive_suffix in
                     re.findall(r"^\s*(debug|dynamic|profile) => \['([^']+)', '([^']*)'\]",
                                source, re.MULTILINE))
        self.assertEqual(forms, {"debug": "_debug", "dynamic": "",
                                 "profile": "_profile"})
        self.assertIn("sub processLibc {\n    my($arch, $dir, $sufname) = @_;", source)
        self.assertIn('File::Spec->join($dir, "libc-partial$sufname.a")', source)
        self.assertIn("processLibc($arch, $usr_local_lib_system, $sufname);", source)
        self.assertEqual({form: f"libc-partial{suffix}.a"
                          for form, suffix in forms.items()},
                         {"debug": "libc-partial_debug.a",
                          "dynamic": "libc-partial.a",
                          "profile": "libc-partial_profile.a"})

    def test_caller_selects_form_and_powerpc_architecture(self):
        makefile = LIBSYS_MAKEFILE.read_text()
        self.assertIn(".for A in $(RC_ARCHS)", makefile)
        self.assertIn(".for F in $(FORMS)", makefile)
        self.assertIn("NAME = libc", makefile)
        self.assertIn("$(NAME)-partial$(SUFFIX$(F)).a", makefile)
        self.assertIn("'$(OBJROOT)/$(A)/$(F)'", makefile)
        self.assertIn("'$(SRCROOT)/libsys/build-libc.pl'", makefile)
        platform = PLATFORM.read_text()
        self.assertIn("FEATURE_DEBUG_DYLIB = 1", platform)
        self.assertIn("FEATURE_PROFILE_DYLIB = 1", platform)


if __name__ == "__main__":
    unittest.main()
