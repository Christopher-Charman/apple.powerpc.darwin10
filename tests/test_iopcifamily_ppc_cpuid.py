"""Source-only regression for the PowerPC PCI configurator root range."""

import difflib
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("IOPCIFamily-144/IOPCIConfigurator.cpp")
SOURCE = ROOT / "src/powerpc" / RELATIVE
SNAPSHOT = ROOT / "src/releases/10.6.8" / RELATIVE
PATCH = ROOT / "patches/IOPCIFamily-144-ppc-configurator-cpuid.patch"
X86_GUARD = "#if defined(__i386__) || defined(__x86_64__)"


class PCIConfiguratorPowerPCTests(unittest.TestCase):
    def test_exact_patch_and_pristine_apple_snapshot(self):
        original = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(original)).encode() + b"\0" + original
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "059bec1d17194bcf822e8d1ca8f2e1c71e0225a8")
        expected = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            SOURCE.read_text().splitlines(keepends=True),
            fromfile="a/src/powerpc/IOPCIFamily-144/IOPCIConfigurator.cpp",
            tofile="b/src/powerpc/IOPCIFamily-144/IOPCIConfigurator.cpp"))
        self.assertEqual(PATCH.read_text(), expected)
        self.assertEqual(expected.count("\n@@ -"), 3)

    def test_x86_only_cpuid_range_and_host_bridge_resources(self):
        source = SOURCE.read_text()
        create_root = source.split("bool CLASS::createRoot(void)", 1)[1].split(
            "IOReturn CLASS::addHostBridge(", 1)[0]
        self.assertEqual(create_root.count(X86_GUARD), 2)
        guard_body = create_root.split(X86_GUARD, 2)[2].split("#endif", 1)[0]
        self.assertIn("cpuid_info()->cpuid_address_bits_physical", guard_body)
        self.assertIn("root->ranges[kIOPCIRangeBridgeMemory] = range;", guard_body)
        self.assertEqual(source.count("cpuid_info()"), 1)
        add_host_bridge = source.split("IOReturn CLASS::addHostBridge(", 1)[1].split(
            "void CLASS::free(", 1)[0]
        self.assertIn("hostBridge->reserved->rangeLists[type]", add_host_bridge)
        self.assertIn("IOPCIRangeListAddRange(&fRoot->ranges[BRN(type)]", add_host_bridge)


if __name__ == "__main__":
    unittest.main()
