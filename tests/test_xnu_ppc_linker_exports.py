"""Test XNU PPC kernel export generation against real shell execution."""
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'src/powerpc/xnu-1504.15.3/config/generate_linker_exports.sh'
ORIGINAL=ROOT/'src/releases/10.6.8/xnu-1504.15.3/config/generate_linker_exports.sh'
class XnuLinkerExportTests(unittest.TestCase):
    def test_architecture_specific_symbols_and_deduplication(self):
        with tempfile.TemporaryDirectory(prefix='ppc exports ') as t:
            directory=Path(t)
            common=directory/'Mach.exports'
            ppc=directory/'Mach.ppc.exports'
            out=directory/'kernel-kpi.exp'
            common.write_text('_shared\n_shared\n_alias:__target\n')
            ppc.write_text('_ppc_only\n_symbol:__target\n')
            result=subprocess.run(['sh',str(SCRIPT),str(out),str(common),str(ppc)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(set(out.read_text().splitlines()), {'_shared','__target','_ppc_only'})
            self.assertEqual(len(out.read_text().splitlines()),3)
    def test_missing_ppc_input_preserves_previous_output(self):
        with tempfile.TemporaryDirectory() as t:
            directory=Path(t)
            common=directory/'Mach.exports'
            common.write_text('_shared\n')
            out=directory/'kernel-kpi.exp'
            out.write_text('previous valid exports\n')
            result=subprocess.run(['sh',str(SCRIPT),str(out),str(common),str(directory/'Mach.ppc.exports')],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('Missing kernel export input:',result.stderr)
            self.assertEqual(out.read_text(),'previous valid exports\n')
    def test_upstream_preserved(self):
        self.assertIn('( grep -h -v ":" "$@"; grep -h ":" "$@"',ORIGINAL.read_text())
if __name__=='__main__': unittest.main()
