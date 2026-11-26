"""Source-only regression guard for OpenDirectory-57.1 PowerPC64 framework slices."""

import difflib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = Path("OpenDirectory-57.1/OpenDirectory.xcodeproj/project.pbxproj")
UPSTREAM = ROOT / "src/releases/10.6.8" / REL
WORKING = ROOT / "src/powerpc" / REL
PATCH = ROOT / "patches/OpenDirectory-57.1-ppc64-framework-arch.patch"

CF_CONFIGS = (
    "6B0B4CEC0B74CF9E002D37C1",  # Development
    "6B0B4CED0B74CF9E002D37C1",  # Deployment
    "6B0B4CEE0B74CF9E002D37C1",  # Default
)
OD_CONFIGS = (
    "6B3E4C7108E5866D00BF138E",  # Development
    "6B3E4C7208E5866D00BF138E",  # Deployment
    "6B3E4C7308E5866D00BF138E",  # Default
)


def settings(project, ident):
    match = re.search(
        rf"\t\t{ident} /\* (?:Development|Deployment|Default) \*/ = \{{\n"
        rf"\t\t\tisa = XCBuildConfiguration;\n\t\t\tbuildSettings = \{{\n"
        rf"(.*?)\n\t\t\t\}};\n\t\t\tname = ",
        project,
        re.S,
    )
    if match is None:
        raise AssertionError(f"missing Xcode configuration {ident}")
    return match.group(1)


def architectures(project, ident):
    match = re.search(r"\t\t\t\tARCHS = \(\n(.*?)\t\t\t\t\);", settings(project, ident), re.S)
    if match is None:
        raise AssertionError(f"missing ARCHS in {ident}")
    return re.findall(r"\t\t\t\t\t([A-Za-z0-9_]+),", match.group(1))


class OpenDirectoryPowerPC64ArchitectureTests(unittest.TestCase):
    def test_frameworks_select_same_powerpc64_slice_in_every_configuration(self):
        project = WORKING.read_text()
        for ident in CF_CONFIGS + OD_CONFIGS:
            with self.subTest(configuration=ident):
                archs = architectures(project, ident)
                self.assertEqual(len(archs), len(set(archs)))
                self.assertEqual(set(archs), {"ppc", "ppc64", "i386", "x86_64"})
                self.assertIn("ppc64", settings(project, ident).split("VALID_ARCHS = ", 1)[1])

    def test_only_reviewed_framework_architecture_delta_and_exact_patch(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        for ident in CF_CONFIGS + (OD_CONFIGS[0], OD_CONFIGS[2]):
            self.assertNotIn("ppc64", architectures(upstream, ident))
        self.assertIsNone(re.search(r"^\s*ARCHS =", settings(upstream, OD_CONFIGS[1]), re.M))
        expected = upstream
        for ident in CF_CONFIGS + (OD_CONFIGS[0], OD_CONFIGS[2]):
            old = settings(expected, ident)
            new = old.replace("\t\t\t\t\tppc,\n", "\t\t\t\t\tppc,\n\t\t\t\t\tppc64,\n", 1)
            self.assertNotEqual(old, new)
            expected = expected.replace(old, new, 1)
        old = settings(expected, OD_CONFIGS[1])
        new = ("\t\t\t\tARCHS = (\n\t\t\t\t\ti386,\n\t\t\t\t\tppc,\n"
               "\t\t\t\t\tppc64,\n\t\t\t\t\tx86_64,\n\t\t\t\t);\n" + old)
        expected = expected.replace(old, new, 1)
        self.assertEqual(working, expected)
        diff = "".join(difflib.unified_diff(
            upstream.splitlines(keepends=True), working.splitlines(keepends=True),
            fromfile="a/src/powerpc/" + str(REL), tofile="b/src/powerpc/" + str(REL),
        ))
        self.assertEqual(PATCH.read_text(), diff)


if __name__ == "__main__":
    unittest.main()
