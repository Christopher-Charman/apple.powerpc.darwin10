"""Source checks for DTrace's PowerPC architecture path and project targets."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = 'dtrace-78'
WORKING = ROOT / 'src/powerpc' / COMPONENT
UPSTREAM = ROOT / 'src/releases/10.6.8' / COMPONENT
PRODUCTS = ('dtrace', 'ctf', 'elf', 'libdtrace', 'plockstat',
            'ctfmerge', 'ctfdump', 'dwarf', 'ctfconvert')


class DTracePowerPCArchitectureTests(unittest.TestCase):
    def test_architecture_names_and_host_mapping(self):
        header = (WORKING / 'head/arch.h').read_text()
        for name, cpu in (('PPC_STRING', 'CPU_TYPE_POWERPC'),
                          ('PPC64_STRING', 'CPU_TYPE_POWERPC64')):
            self.assertRegex(header, r'case ' + cpu + r':\s+return ' + name + r';')
            self.assertRegex(header, r'strcmp\(string, ' + name + r'\)\)\s+return ' + cpu + r';')
        self.assertRegex(header, r'#if defined\(__ppc64__\)\s+#define host_arch CPU_TYPE_POWERPC64\s+#elif defined\(__ppc__\)\s+#define host_arch CPU_TYPE_POWERPC')
        self.assertIn('case CPU_TYPE_POWERPC64:', header)
        options = (WORKING / 'libdtrace/dt_options.c').read_text()
        self.assertRegex(options, r'case CPU_TYPE_POWERPC:\s+case CPU_TYPE_POWERPC64:\s+dtp->dt_arch = arch;')
        cli = (WORKING / 'cmd/dtrace_1.c').read_text()
        self.assertIn('target_arch = arch_for_string(arch_string);', cli)
        self.assertIn('string_for_arch(target_arch)', cli)
        toolchain = (ROOT / 'src/powerpc/cctools-750/libstuff/arch.c').read_text()
        self.assertIn('"ppc64",     CPU_TYPE_POWERPC64', toolchain)
        self.assertIn('"ppc",    CPU_TYPE_POWERPC', toolchain)

    def test_project_and_all_nine_targets_allow_ppc(self):
        project = (WORKING / 'dtrace.xcodeproj/project.pbxproj').read_text()
        self.assertEqual(project.count('VALID_ARCHS = "ppc armv6 i386 x86_64";'), 2)
        entries = re.findall(r'/\* (Debug|Release) \*/ = \{\s+isa = XCBuildConfiguration;\s+buildSettings = \{(.*?)\};\s+name = \1;', project, re.S)
        for product in PRODUCTS:
            matching = [(name, settings) for name, settings in entries if 'PRODUCT_NAME = %s;' % product in settings
                        and re.search(r'VALID_ARCHS = "[^"]*\bppc\b[^"]*";', settings)]
            self.assertEqual(sorted(name for name, _ in matching), ['Debug', 'Release'], product)
        original = (UPSTREAM / 'dtrace.xcodeproj/project.pbxproj').read_text()
        self.assertEqual(original.count('VALID_ARCHS = "armv6 i386 x86_64";'), 2)
        self.assertEqual(original.count('VALID_ARCHS = "x86_64 i386";'), 16)
        self.assertEqual(original.count('VALID_ARCHS = "i386 x86_64";'), 2)
        expected = original.replace('VALID_ARCHS = "armv6 i386 x86_64";', 'VALID_ARCHS = "ppc armv6 i386 x86_64";')
        expected = expected.replace('VALID_ARCHS = "x86_64 i386";', 'VALID_ARCHS = "x86_64 i386 ppc";')
        expected = expected.replace('VALID_ARCHS = "i386 x86_64";', 'VALID_ARCHS = "ppc i386 x86_64";')
        self.assertEqual(project, expected)


if __name__ == '__main__':
    unittest.main()
