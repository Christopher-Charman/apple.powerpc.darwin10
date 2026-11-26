import difflib
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = Path('OpenSSH-142/openssh/openbsd-compat/port-tun.c')
PATCH = ROOT / 'patches/OpenSSH-142-ppc-tun-alignment.patch'
APPLE_BLOB = 'ddc92d0f3f5562bbf36c274d2b86f950025632f7'


class OpenSSHTunAlignmentSourceTests(unittest.TestCase):
    def test_exact_apple_delta_and_pristine_snapshot(self):
        pristine = (ROOT / 'src/releases/10.6.8' / COMPONENT).read_bytes()
        working = (ROOT / 'src/powerpc' / COMPONENT).read_bytes()
        blob = b'blob ' + str(len(pristine)).encode() + b'\0' + pristine
        self.assertEqual(hashlib.sha1(blob).hexdigest(), APPLE_BLOB)
        path = 'src/powerpc/' + str(COMPONENT)
        expected = ''.join(difflib.unified_diff(
            pristine.decode().splitlines(keepends=True),
            working.decode().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual(PATCH.read_text(), expected)

    def test_darwin_filter_avoids_unaligned_word_and_header_access(self):
        source = (ROOT / 'src/powerpc' / COMPONENT).read_text()
        body = source.split('sys_tun_infilter(struct Channel *c, char *buf, int len)\n{', 1)[1].split('\n}', 1)[0]
        self.assertNotIn('(u_int32_t *)ptr', body)
        self.assertNotIn('(struct ip *)', body)
        self.assertIn('switch ((u_char)ptr[sizeof(af)] >> 4)', body)
        self.assertIn('memcpy(&af, ptr, sizeof(af));', body)
        self.assertEqual(body.count('memcpy(ptr, &af, sizeof(af));'), 2)
        self.assertIn('if (len <= 0 || len > (int)(sizeof(rbuf) - sizeof(af)))', body)
        self.assertIn('if (len < (int)sizeof(af))', body)

    def test_filter_is_selected_for_darwin_tunnels(self):
        base = ROOT / 'src/powerpc/OpenSSH-142/openssh'
        configure = (base / 'configure.ac').read_text()
        darwin = configure.split('*-*-darwin*)', 1)[1].split(';;', 1)[0]
        self.assertIn('AC_DEFINE(SSH_TUN_PREPEND_AF, 1,', darwin)
        self.assertIn('AC_DEFINE(SSH_TUN_COMPAT_AF, 1,', darwin)
        header = (base / 'openbsd-compat/port-tun.h').read_text()
        self.assertIn('# define SSH_TUN_FILTER', header)
        for filename in ('clientloop.c', 'serverloop.c'):
            self.assertIn('sys_tun_infilter,', (base / filename).read_text())


if __name__ == '__main__':
    unittest.main()
