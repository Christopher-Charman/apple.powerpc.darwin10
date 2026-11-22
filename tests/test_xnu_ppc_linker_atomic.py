"""Source-script regression for PPC kernel export output replacement."""
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'src/powerpc/xnu-1504.15.3/config/generate_linker_exports.sh'
class XnuLinkerAtomicTests(unittest.TestCase):
    def test_success_replaces_old_output_without_temporary_residue(self):
        with tempfile.TemporaryDirectory(prefix='ppc linker ') as t:
            root=Path(t)
            exports=root/'Mach.ppc.exports'
            exports.write_text('_ppc_symbol\n_ppc_symbol\n')
            out=root/'kernel-kpi.exp'
            out.write_text('old\n')
            run=subprocess.run(['sh',str(SCRIPT),str(out),str(exports)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(out.read_text(),'_ppc_symbol\n')
            self.assertEqual(list(root.glob('.kernel-kpi.exp.*')),[])
    def test_missing_input_preserves_output_and_no_temp(self):
        with tempfile.TemporaryDirectory(prefix='ppc linker ') as t:
            root=Path(t)
            out=root/'kernel-kpi.exp'
            out.write_text('old\n')
            run=subprocess.run(['sh',str(SCRIPT),str(out),str(root/'missing.ppc.exports')],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertEqual(out.read_text(),'old\n')
            self.assertEqual(list(root.glob('.kernel-kpi.exp.*')),[])
if __name__=='__main__': unittest.main()
