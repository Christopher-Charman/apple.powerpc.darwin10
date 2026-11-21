"""Regression checks for dyld's PowerPC loader assembly and project wiring."""
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src/powerpc/dyld-132.13/src"
PROJECT = ROOT / "src/powerpc/dyld-132.13/dyld.xcodeproj/project.pbxproj"
UPSTREAM = ROOT / "src/releases/10.6.8/dyld-132.13/src"
class DyldPowerPCAssemblyTests(unittest.TestCase):
    def test_startup_contains_ppc32_ppc64_entry(self):
        text = (SRC / "dyldStartup.s").read_text()
        self.assertIn("#if __ppc__ || __ppc64__", text)
        self.assertIn("#if __ppc__", text)
        self.assertIn("#endif /* __ppc__ */", text)
    def test_lazy_binding_helper_has_ppc_entry(self):
        text = (SRC / "stub_binding_helper.s").read_text()
        guard = text.index("#if __ppc__ || __ppc64__")
        entry = text.index("_stub_binding_helper_interface:", guard)
        self.assertLess(guard, entry)
        self.assertLess(entry, text.index("#endif /* __ppc__ */", entry))
    def test_project_wires_ppc_assembly(self):
        text = PROJECT.read_text()
        self.assertIn("dyldStartup.s in Sources", text)
        self.assertIn("stub_binding_helper.s in Sources", text)
    def test_x86_only_stub_binder_not_mistaken_for_ppc(self):
        text = (SRC / "dyld_stub_binder.s").read_text()
        self.assertIn("#ifdef __i386__", text)
        self.assertIn("#if __x86_64__", text)
        self.assertNotIn("#if __ppc__", text)
        self.assertNotIn("#if __ppc__ || __ppc64__", text)
    def test_pristine_assembly_unmodified(self):
        for name in ("dyldStartup.s", "stub_binding_helper.s", "dyld_stub_binder.s"):
            self.assertEqual((SRC / name).read_bytes(), (UPSTREAM / name).read_bytes())
if __name__ == "__main__":
    unittest.main()
