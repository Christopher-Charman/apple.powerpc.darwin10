"""Source-only regression for the PowerPC USB CDC EEM header correction."""

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("AppleUSBCDCDriver-4005.4.2/AppleUSBCDCEEM/Classes/AppleUSBCDCEEM.cpp")
SOURCE = ROOT / "src/powerpc" / RELATIVE
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
BYTE_ORDER = ROOT / "src/releases/10.6.8/xnu-1504.15.3/libkern/libkern/OSByteOrder.h"


class AppleUSBCDCEEMPowerPCByteOrderTests(unittest.TestCase):
    def test_pristine_apple_snapshot_and_exact_source_delta(self):
        original = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "015757871a1457c800716e9ad20629d9c8e08131")
        expected = original.decode()
        expected = expected.replace("\tUInt16\t\t\t*EEMHeaderAddress = &EEMHeader;\n", "")
        expected = expected.replace(
            "\t\t\tEEMHeaderAddress[0] = pipeBuf->pipeInBuffer[i];\n"
            "\t\t\tEEMHeaderAddress[1] = pipeBuf->pipeInBuffer[i+1];",
            "\t\t\tEEMHeader = OSReadLittleInt16(pipeBuf->pipeInBuffer, i);")
        expected = expected.replace(
            "\tbcopy(&EEMHeader, fPipeOutBuff[indx].pipeOutBuffer, sizeof(EEMHeader));",
            "\tOSWriteLittleInt16(fPipeOutBuff[indx].pipeOutBuffer, 0, EEMHeader);")
        self.assertEqual(SOURCE.read_text(), expected)

    def test_darwin_header_has_architecture_aware_wire_helpers(self):
        header = BYTE_ORDER.read_text()
        self.assertIn("#define OSReadLittleInt16(base, byteOffset) OSReadSwapInt16(base, byteOffset)", header)
        self.assertIn("#define OSWriteLittleInt16(base, byteOffset, data) OSWriteSwapInt16(base, byteOffset, data)", header)
        self.assertIn("#define OSReadLittleInt16(base, byteOffset) _OSReadInt16(base, byteOffset)", header)
        self.assertIn("#define OSWriteLittleInt16(base, byteOffset, data) _OSWriteInt16(base, byteOffset, data)", header)

    def test_eem_header_wire_fixture(self):
        # Echo response command 0x8008 must occupy two little-endian USB bytes.
        wire = bytes((0x08, 0x80))
        self.assertEqual(int.from_bytes(wire, "little"), 0x8008)
        self.assertEqual((0x8008).to_bytes(2, "little"), wire)
        self.assertNotEqual(int.from_bytes(wire, "big"), 0x8008)


if __name__ == "__main__":
    unittest.main()
