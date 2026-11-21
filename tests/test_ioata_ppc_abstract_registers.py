"""Static regression checks for the PowerPC IOATA abstract register class fix."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/powerpc/IOATAFamily-251.0.1/IOATARegI386.cpp"
ORIGINAL = ROOT / "src/releases/10.6.8/IOATAFamily-251.0.1/IOATARegI386.cpp"

class IOATAPowerPCRegisterTests(unittest.TestCase):
    def test_abstract_classes_outside_x86_only_guard(self):
        text = SOURCE.read_text()
        guard = text.index("#if defined( __i386__ ) || defined( __x86_64__ )")
        for name in ("IOATAReg8", "IOATAReg16", "IOATAReg32"):
            definition = f"OSDefineMetaClassAndAbstractStructors( {name},"
            self.assertEqual(text.count(definition), 1)
            self.assertLess(text.index(definition), guard)
        self.assertGreater(text.index("#include <architecture/i386/pio.h>"), guard)
        self.assertGreater(text.index("OSDefineMetaClassAndStructors( IOATAIOReg8,"), guard)
        self.assertGreater(text.index("ImplementIOATAIOReg( 8,"), guard)
        self.assertTrue(text.rstrip().endswith("#endif /* __i386__ || __x86_64__ */"))

    def test_pristine_release_retains_original_guard(self):
        text = ORIGINAL.read_text()
        guard = text.index("#if defined( __i386__ ) || defined( __x86_64__ )")
        self.assertGreater(text.index("OSDefineMetaClassAndAbstractStructors( IOATAReg8,"), guard)

if __name__ == "__main__":
    unittest.main()
