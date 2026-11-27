"""Source-only guard for X11apps executable architecture selection."""

import difflib
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("PPC_SOURCE_ROOT", Path(__file__).resolve().parents[1]))
RELATIVE = Path("X11apps-30.1/build")
UPSTREAM = ROOT / "src/releases/10.6.8" / RELATIVE
WORKING = ROOT / "src/powerpc" / RELATIVE
PATCH = ROOT / "patches/X11apps-30.1-ppc32-exec-arch.patch"
MANIFEST = ROOT / "patches/X11apps-30.1-ppc32-exec-arch.json"
OLD = '            $arch_flags_exec .= " -arch $arch " unless $arch =~ /ppc/;'
NEW = '            $arch_flags_exec .= " -arch $arch " unless $arch =~ /ppc64/;'


class X11appsPowerPCExecutableArchitectureTests(unittest.TestCase):
    def test_exact_release_delta_and_patch(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        self.assertEqual(upstream.count(OLD), 1)
        self.assertEqual(working, upstream.replace(OLD, NEW, 1))
        expected_patch = "".join(difflib.unified_diff(
            upstream.splitlines(keepends=True), working.splitlines(keepends=True),
            fromfile="a/src/powerpc/" + str(RELATIVE),
            tofile="b/src/powerpc/" + str(RELATIVE),
        ))
        self.assertEqual(PATCH.read_text(), expected_patch)
        manifest = json.loads(MANIFEST.read_text())
        self.assertEqual(manifest["source_tree_sha"], "43531ce33f61a37652542c59433542890b986566")
        self.assertEqual(manifest["upstream_commit"], "0c764f59596b10773f667b7cc660d366cd8e0150")

    def test_architecture_filters_and_flag_consumers(self):
        working = WORKING.read_text()
        block = re.search(
            r'if\(\$ENV\{MACOSFORGE_RELEASE\} eq "YES"\) \{'
            r'(?P<release>.*?)\} else \{(?P<ordinary>.*?)\}',
            working, re.S,
        )
        self.assertIsNotNone(block)
        release = re.search(r'unless \$arch =~ /([^/]+)/;', block.group("release"))
        ordinary = re.search(r'unless \$arch =~ /([^/]+)/;', block.group("ordinary"))
        self.assertIsNotNone(release)
        self.assertIsNotNone(ordinary)
        self.assertEqual(release.group(1), "64")
        self.assertEqual(ordinary.group(1), "ppc64")
        selected = lambda pattern, arch: not re.search(pattern, arch)
        self.assertEqual(
            [a for a in ("ppc", "ppc64", "i386", "x86_64") if selected(ordinary.group(1), a)],
            ["ppc", "i386", "x86_64"],
        )
        self.assertEqual(
            [a for a in ("ppc", "ppc64", "i386", "x86_64") if selected(release.group(1), a)],
            ["ppc", "i386"],
        )
        self.assertIn('$ENV{CFLAGS}="-I$ENV{DSTROOT}$prefix/include -D__DEBUG__ -ggdb3 -Os -pipe $arch_flags_exec', working)
        self.assertIn('$ENV{LDFLAGS}="-pipe $arch_flags_exec";', working)
        self.assertIn('set_arch_exec();', working)


if __name__ == "__main__":
    unittest.main()
