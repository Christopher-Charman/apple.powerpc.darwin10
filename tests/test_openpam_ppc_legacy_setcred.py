import difflib
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = Path('OpenPAM-11.1/compat')
PATCH = ROOT / 'patches/OpenPAM-11.1-ppc-legacy-setcred-flags.patch'
FILES = {
    'pam_shim.c': 'e5d7d164fc8d32e8c89b38124bc07302a17a4d3e',
    'pam_shim_setcred_flags.h': '67188a60f328390399afabd8df81aa59cf59cb27',
}


class OpenPAMLegacySetcredSourceTests(unittest.TestCase):
    def test_exact_apple_delta_and_pristine_snapshot(self):
        expected = ''
        for name, original_sha in FILES.items():
            relative = COMPONENT / name
            pristine = (ROOT / 'src/releases/10.6.8' / relative).read_bytes()
            working = (ROOT / 'src/powerpc' / relative).read_bytes()
            blob = b'blob ' + str(len(pristine)).encode() + b'\0' + pristine
            self.assertEqual(hashlib.sha1(blob).hexdigest(), original_sha)
            path = 'src/powerpc/' + str(relative)
            expected += ''.join(difflib.unified_diff(
                pristine.decode().splitlines(keepends=True),
                working.decode().splitlines(keepends=True),
                fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual(PATCH.read_text(), expected)

    def test_legacy_credential_operations_and_silent_bit(self):
        source = (ROOT / 'src/powerpc' / COMPONENT / 'pam_shim.c').read_text()
        flags = (ROOT / 'src/powerpc' / COMPONENT / 'pam_shim_setcred_flags.h').read_text()
        constants = (ROOT / 'src/powerpc/OpenPAM-11.1/openpam/include/security/pam_constants.h').read_text()

        setcred_body = source.split('pam_setcred(pam_handle_t *pamh, int flags)\n{', 1)[1].split('\n}', 1)[0]
        self.assertIn('int newflags = xlate_pam_shim_setcred_flags(flags);', setcred_body)
        self.assertNotIn('xlate_pam_shim_authenticate_flags(flags)', setcred_body)
        self.assertEqual(source.count('COMPAT_SETCRED_##oldname'), 2)
        self.assertRegex(source, r'COMPAT_SETCRED_##oldname = oldvalue,\s*enum \{\s*#include "pam_shim_setcred_flags.h"')

        rows = re.findall(r'^xlate\((PAM_\w+), (0x[0-9a-fA-F]+)U, \1, (.+)\)$', flags, re.M)
        self.assertEqual({name: int(old, 16) for name, old, _ in rows}, {
            'PAM_SILENT': 0x8000,
            'PAM_ESTABLISH_CRED': 0x0002,
            'PAM_DELETE_CRED': 0x0004,
            'PAM_REINITIALIZE_CRED': 0x0008,
            'PAM_REFRESH_CRED': 0x0010,
        })
        self.assertEqual(len(rows), 5)
        for name, value in [
            ('PAM_ESTABLISH_CRED', '0x1'),
            ('PAM_DELETE_CRED', '0x2'),
            ('PAM_REINITIALIZE_CRED', '0x4'),
            ('PAM_REFRESH_CRED', '0x8'),
        ]:
            self.assertRegex(constants, rf'\b{name}\s*=\s*{value}\s*,')
        self.assertRegex(constants, r'PAM_SILENT\s*=\s*\(-0x7fffffff - 1\)')
        self.assertIn('if (flags & COMPAT_SETCRED_##oldname) newflags |= newname;', source)

        legacy_to_current = {
            int(old, 16): 0x80000000 if name == 'PAM_SILENT' else int(new, 16)
            for name, old, new in rows
        }
        self.assertEqual(legacy_to_current, {
            0x8000: 0x80000000, 0x0002: 0x1, 0x0004: 0x2,
            0x0008: 0x4, 0x0010: 0x8,
        })
        combined = 0x8000 | 0x0004
        mapped = 0
        for old, current in legacy_to_current.items():
            if combined & old:
                mapped |= current
        self.assertEqual(mapped, 0x80000002)


if __name__ == '__main__':
    unittest.main()
