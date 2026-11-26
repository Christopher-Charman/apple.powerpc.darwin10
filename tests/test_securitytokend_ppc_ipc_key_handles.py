"""Source-only guard for SecurityTokend IPC-to-native key handles."""

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = Path("SecurityTokend-36808/lib")
SOURCE = ROOT / "src/powerpc" / COMPONENT / "transition.cpp"
SNAPSHOT = ROOT / "src/releases/10.6.8" / COMPONENT / "transition.cpp"
TRANSIT_H = ROOT / "src/powerpc" / COMPONENT / "transit.h"
TRANSIT_CPP = ROOT / "src/powerpc" / COMPONENT / "transit.cpp"
OLD_WRAP = (b"    CSSM_HANDLE keyHandle = TokendHandleObject::findTDHandle(hSubjectKey);\n"
            b"\tCALL(wrapKey, (&context, hWrappingKey, wrappingKey, cred,\n")
NEW_WRAP = (b"    CSSM_HANDLE keyHandle = TokendHandleObject::findTDHandle(hSubjectKey);\n"
            b"\tCSSM_HANDLE wrapKeyHandle = TokendHandleObject::findTDHandle(hWrappingKey);\n"
            b"\tCALL(wrapKey, (&context, wrapKeyHandle, wrappingKey, cred,\n")
OLD_DERIVE = (b"    CSSM_HANDLE cssmKeyHandle;\n"
              b"\tCALL(deriveKey, (&context, hBaseKey, baseKey, cred, owner, &paramInput->baseData,\n")
NEW_DERIVE = (b"    CSSM_HANDLE cssmKeyHandle;\n"
              b"\tCSSM_HANDLE baseKeyHandle = TokendHandleObject::findTDHandle(hBaseKey);\n"
              b"\tCALL(deriveKey, (&context, baseKeyHandle, baseKey, cred, owner, &paramInput->baseData,\n")


class SecurityTokendKeyHandleTests(unittest.TestCase):
    def test_pinned_apple_blob_and_exact_two_call_site_delta(self):
        original = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "77784cf8d9421a751ca95d8bb1d2d4690067d40c")
        self.assertEqual(original.count(OLD_WRAP), 1)
        self.assertEqual(original.count(OLD_DERIVE), 1)
        self.assertEqual(SOURCE.read_bytes(),
                         original.replace(OLD_WRAP, NEW_WRAP)
                                 .replace(OLD_DERIVE, NEW_DERIVE))

    def test_native_handle_translation_at_both_server_calls(self):
        source = SOURCE.read_text()
        wrap = source.split("kern_return_t tokend_server_wrapKey(", 1)[1].split(
            "kern_return_t tokend_server_unwrapKey(", 1)[0]
        derive = source.split("kern_return_t tokend_server_deriveKey(", 1)[1].split(
            "kern_return_t tokend_server_getOwner(", 1)[0]
        self.assertIn("findTDHandle(hWrappingKey)", wrap)
        self.assertIn("CALL(wrapKey, (&context, wrapKeyHandle,", wrap)
        self.assertIn("findTDHandle(hBaseKey)", derive)
        self.assertIn("CALL(deriveKey, (&context, baseKeyHandle,", derive)
        self.assertIn("findTDHandle(hWrappingKey)", source.split(
            "kern_return_t tokend_server_unwrapKey(", 1)[1].split(
            "kern_return_t tokend_server_deriveKey(", 1)[0])

    def test_mapping_preserves_zero_and_native_width_contract(self):
        header = TRANSIT_H.read_text()
        implementation = TRANSIT_CPP.read_text()
        self.assertIn("typedef uint32_t TransitHandle", header)
        self.assertIn("static CSSM_HANDLE findTDHandle(TransitHandle thdl)", header)
        self.assertIn("if (!thdl)\n\t\treturn knownBadHandle;", implementation)
        self.assertIn("it->second->tokendHandle()", implementation)


if __name__ == "__main__":
    unittest.main()
