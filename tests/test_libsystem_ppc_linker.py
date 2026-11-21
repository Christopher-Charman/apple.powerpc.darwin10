"""Check the PowerPC Libsystem linker command has no misspelled sysroot variable."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/powerpc/Libsystem-125.2.11/Makefile'
O=ROOT/'src/releases/10.6.8/Libsystem-125.2.11/Makefile'
class LibsystemLinkerTests(unittest.TestCase):
    def test_linker_uses_defined_sdkroot(self):
        text=P.read_text()
        self.assertNotIn('$(SKDROOTLDFLAGS)',text)
        self.assertIn('$(MYCC) -dynamiclib -arch $(A) -pipe $(SDKROOTLDFLAGS)',text)
        self.assertIn('SEG1ADDR_ppc = 0xffff8000',text)
    def test_upstream_preserved(self):
        self.assertEqual(O.read_text().count('$(SKDROOTLDFLAGS)'),1)
if __name__=='__main__': unittest.main()
