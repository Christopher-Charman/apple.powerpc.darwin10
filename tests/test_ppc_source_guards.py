import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scan_ppc_source_guards', str(ROOT / 'tools/scan_ppc_source_guards.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PPCSourceGuardsTests(unittest.TestCase):
    def test_recovered_architecture_guard_evidence(self):
        rows = module.scan()
        self.assertEqual(len(rows), 51)
        self.assertTrue(any('IONDRVFramebuffer.cpp' in row['file'] and row['ppc_mentioned'] for row in rows))
        self.assertTrue(any(row['intel_mentioned'] for row in rows))


class CPANInternalPowerPCFlagsTests(unittest.TestCase):
    """Source-only contract for CPAN's RC_ARCHS to RC_CFLAGS fallback."""

    def test_pristine_release_and_exact_working_diff(self):
        import difflib
        import hashlib

        relative = Path('CPANInternal-62/Makefile')
        pristine = (ROOT / 'src/releases/10.6.8' / relative).read_bytes()
        working = (ROOT / 'src/powerpc' / relative).read_bytes()
        blob = b'blob ' + str(len(pristine)).encode() + b'\0' + pristine
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         'b38eb673184e4c9fa648818fa7593ee2d3b708d0')
        path = 'src/powerpc/' + str(relative)
        expected = ''.join(difflib.unified_diff(
            pristine.decode().splitlines(keepends=True),
            working.decode().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual((ROOT / 'patches/CPANInternal-62-ppc-arch-flags.patch').read_text(),
                         expected)
        self.assertEqual(expected.count('@@ -'), 1)

    def test_architecture_flags_are_exported_without_overriding_caller(self):
        source = (ROOT / 'src/powerpc/CPANInternal-62/Makefile').read_text()
        predecessor = (ROOT / 'src/powerpc/perl-63/Makefile').read_text()
        fallback = ('ifndef RC_ARCHS\n'
                    'export RC_ARCHS = $(shell arch)\n'
                    'endif\n'
                    'ifndef RC_CFLAGS\n'
                    'export RC_CFLAGS = $(foreach A,$(RC_ARCHS),-arch $(A)) $(RC_NONARCH_CFLAGS)\n'
                    'endif\n')
        self.assertIn(fallback, source)
        self.assertIn('export RC_CFLAGS = $(foreach A,$(RC_ARCHS),-arch $(A)) $(RC_NONARCH_CFLAGS)', predecessor)
        self.assertLess(source.index(fallback), source.index('# set up ARCHFLAGS'))
        self.assertIn('ARCHFLAGS = $(RC_CFLAGS)', source)
        self.assertNotIn('ifndef RC_CFLAGS', (ROOT / 'src/releases/10.6.8/CPANInternal-62/Makefile').read_text())

    def test_xs_module_configuration_consumes_exported_flags(self):
        maker = (ROOT / 'src/powerpc/CPANInternal-62/add_rc_constants.pl').read_text()
        pathtools = (ROOT / 'src/powerpc/CPANInternal-62/PathTools/Build.PL').read_text()
        version = (ROOT / 'src/powerpc/CPANInternal-62/PatchFiles/version.diff').read_text()
        self.assertIn('$ENV{RC_CFLAGS} $optFlags', maker)
        self.assertIn('$ENV{RC_CFLAGS} $dlib->{OTHERLDFLAGS}', maker)
        self.assertIn('split " ", $ENV{RC_CFLAGS}', pathtools)
        self.assertIn(r'extra_compiler_flags => \@compiler_flags', pathtools)
        self.assertIn(r'extra_linker_flags => \@linker_flags', pathtools)
        self.assertIn('+    extra_compiler_flags => "$ENV{RC_CFLAGS} -Os"', version)
        self.assertIn('+    extra_linker_flags => $ENV{RC_CFLAGS}', version)


class IOGraphicsClamshellTests(unittest.TestCase):
    """Source-only PPC PMU result declaration and exact Apple delta."""

    def test_pristine_snapshot_and_exact_working_diff(self):
        import difflib
        import hashlib

        relative = Path('IOGraphics-392.1/IOGraphicsFamily/IOFramebuffer.cpp')
        pristine = (ROOT / 'src/releases/10.6.8' / relative).read_bytes()
        working = (ROOT / 'src/powerpc' / relative).read_bytes()
        blob = b'blob ' + str(len(pristine)).encode() + b'\0' + pristine
        self.assertEqual(hashlib.sha1(blob).hexdigest(),
                         '61909b23a44d09f5e84a84360e1a3eff5284c94c')
        old = b'    ret = ApplePMUSendMiscCommand(readExtSwitches, 0, NULL, &iLen, &bootEnvIntData[0]);'
        new = b'    IOReturn ret = ApplePMUSendMiscCommand(readExtSwitches, 0, NULL, &iLen, &bootEnvIntData[0]);'
        self.assertEqual(pristine.count(old), 1)
        self.assertEqual(working, pristine.replace(old, new))
        path = 'src/powerpc/' + str(relative)
        expected = ''.join(difflib.unified_diff(
            pristine.decode().splitlines(keepends=True),
            working.decode().splitlines(keepends=True),
            fromfile='a/' + path, tofile='b/' + path))
        self.assertEqual((ROOT / 'patches/IOGraphics-392.1-ppc-clamshell-ret.patch').read_text(),
                         expected)
        self.assertEqual(expected.count('@@ -'), 1)

    def test_ppc_branch_uses_declared_result(self):
        source = (ROOT / 'src/powerpc/IOGraphics-392.1/IOGraphicsFamily/IOFramebuffer.cpp').read_text()
        function = source.split('void IOFramebuffer::readClamshellState()', 1)[1].split(
            'extern "C" IOReturn\nIOGetHardwareClamshellState', 1)[0]
        ppc = function.split('#if __ppc__', 1)[1].split('#elif defined(__i386__) || defined(__x86_64__)', 1)[0]
        self.assertIn('IOReturn ret = ApplePMUSendMiscCommand(', ppc)
        self.assertIn('if (kIOReturnSuccess == ret)', ppc)
        self.assertLess(ppc.index('IOReturn ret ='), ppc.index('if (kIOReturnSuccess == ret)'))
        self.assertIn('gIOFBLastClamshellState = bootEnvIntData[0];', ppc)


if __name__ == '__main__':
    unittest.main()
