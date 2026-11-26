import difflib
import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = Path("OpenSSL098-35.1/bin/test_functions.sh")
PRISTINE = ROOT / "src/releases/10.6.8" / COMPONENT
WORKING = ROOT / "src/powerpc" / COMPONENT
PATCH = ROOT / "patches/OpenSSL098-35.1-ppc-test-arch.patch"
APPLE_BLOB = "dee2b677d3848a0f39591921293057567754e3c3"


class OpenSSL098PPCTestArchTests(unittest.TestCase):
    def test_exact_apple_delta_and_pristine_snapshot(self):
        pristine = PRISTINE.read_bytes()
        working = WORKING.read_bytes()
        blob = b"blob " + str(len(pristine)).encode() + b"\0" + pristine
        self.assertEqual(hashlib.sha1(blob).hexdigest(), APPLE_BLOB)
        path = "src/powerpc/" + str(COMPONENT)
        expected = "".join(difflib.unified_diff(
            pristine.decode().splitlines(keepends=True),
            working.decode().splitlines(keepends=True),
            fromfile="a/" + path, tofile="b/" + path))
        self.assertEqual(PATCH.read_text(), expected)

    def test_shell_probe_selects_only_runnable_architectures(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            fake_arch = directory / "arch"
            fake_arch.write_text("""#!/bin/sh
[ "$2" = /bin/sh ] || exit 2
case "$1" in
  -i386) printf 'YES\n' ;;
  -ppc) [ "$ALLOW_PPC" = 1 ] && printf 'YES\n' ;;
  *) exit 2 ;;
esac
""")
            fake_arch.chmod(0o755)
            for allow_ppc, expected in (("1", ["ppc", "i386"]),
                                        ("0", ["i386"])):
                with self.subTest(allow_ppc=allow_ppc):
                    objroot = directory / ("obj-" + allow_ppc)
                    objroot.mkdir()
                    env = os.environ.copy()
                    env.update(PATH=str(directory) + os.pathsep + env["PATH"],
                               OBJROOT=str(objroot), ARCHS="ppc i386",
                               ALLOW_PPC=allow_ppc, TEST_NO_SOURCE_DYLD="1")
                    result = subprocess.run(
                        ["bash", "-c", 'source "$1"; get_exec_arches',
                         "source-test", str(WORKING)],
                        env=env, text=True, capture_output=True, check=True)
                    self.assertEqual(result.stdout.split(), expected)


if __name__ == "__main__":
    unittest.main()
