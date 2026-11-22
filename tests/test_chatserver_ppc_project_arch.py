"""Source-only check of ChatServer's PowerPC Xcode architecture restoration."""
import difflib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = 'ChatServer-326.5'
PROJECT = 'ChatServer2.xcodeproj/project.pbxproj'
UPSTREAM = ROOT / 'src/releases/10.6.8' / COMPONENT / PROJECT
WORKING = ROOT / 'src/powerpc' / COMPONENT / PROJECT
PATCH = ROOT / 'patches/ChatServer-326.5-ppc-project-arch.patch'
MAKEFILE = ROOT / 'src/powerpc' / COMPONENT / 'Makefile'


def expected_working(upstream):
    legacy_and_project = '\t\t\t\tARCHS = (\n\t\t\t\t\tx86_64,\n\t\t\t\t\ti386,\n\t\t\t\t);'
    library = '\t\t\t\tARCHS = (\n\t\t\t\t\ti386,\n\t\t\t\t\tx86_64,\n\t\t\t\t);'
    if upstream.count(legacy_and_project) != 2 or upstream.count(library) != 2:
        raise AssertionError('Apple 10.6.8 architecture baseline changed')
    result = upstream.replace(
        legacy_and_project,
        legacy_and_project.replace('\t\t\t\t\tx86_64,', '\t\t\t\t\tppc,\n\t\t\t\t\tx86_64,'),
    )
    return result.replace(
        library,
        library.replace('\t\t\t\t\ti386,', '\t\t\t\t\tppc,\n\t\t\t\t\ti386,'),
    )


class ChatServerPowerPCProjectArchitectureTests(unittest.TestCase):
    def test_four_active_architecture_settings_and_exact_release_delta(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        for config in (
            '1DEB919108733D9F0010E9CD /* Release */',  # legacy ChatServer2 target
            '1DEB919408733D9F0010E9CD /* Debug */',    # project
            '84B8C3970F58EB6200824D09 /* Debug */',    # libxmppodauth
            '84B8C3980F58EB6200824D09 /* Release */',  # libxmppodauth
        ):
            self.assertIn(config, working)
        self.assertEqual(working, expected_working(upstream))
        self.assertEqual(working.count('\t\t\t\t\tppc,\n'), 4)

    def test_patch_matches_source_delta(self):
        upstream = UPSTREAM.read_text()
        working = WORKING.read_text()
        path = f'src/powerpc/{COMPONENT}/{PROJECT}'
        expected = ''.join(difflib.unified_diff(
            upstream.splitlines(keepends=True), working.splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path,
        ))
        self.assertEqual(PATCH.read_text(), expected)

    def test_legacy_makefile_retains_ppc_path(self):
        makefile = MAKEFILE.read_text()
        self.assertIn('BUILD_ARCHS\t= ppc i386 x86_64', makefile)
        self.assertIn('BUILD_ARCH := ppc', makefile)
        self.assertIn('config_cache/glib/ppc', (ROOT / 'src/powerpc' / COMPONENT / PROJECT).read_text())


if __name__ == '__main__':
    unittest.main()
