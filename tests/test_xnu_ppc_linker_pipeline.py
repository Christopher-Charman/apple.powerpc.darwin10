"""Source-only XNU PPC kernel export normalization and error handling."""
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'src/powerpc/xnu-1504.15.3/config/generate_linker_exports.sh'
class XnuLinkerPipelineTests(unittest.TestCase):
    def test_normalization_matches_original_colon_semantics(self):
        with tempfile.TemporaryDirectory(prefix='ppc symbols ') as t:
            root=Path(t)
            source=root/'PPC.exports'
            source.write_text('_normal\n_symbol:_mapped:ignored\n_symbol:_mapped:ignored\n_colon:second\n')
            out=root/'kernel-kpi.exp'
            result=subprocess.run(['sh',str(SCRIPT),str(out),str(source)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(set(out.read_text().splitlines()),{'_normal','_mapped','second'})
            self.assertEqual(len(out.read_text().splitlines()),3)
    def test_unreadable_directory_input_does_not_replace_prior_output(self):
        with tempfile.TemporaryDirectory(prefix='ppc symbols ') as t:
            root=Path(t)
            directory=root/'PPC.exports'
            directory.mkdir()
            out=root/'kernel-kpi.exp'
            out.write_text('previous valid list\n')
            result=subprocess.run(['sh',str(SCRIPT),str(out),str(directory)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(out.read_text(),'previous valid list\n')
            self.assertEqual(list(root.glob('.kernel-kpi.exp.*')),[])
if __name__=='__main__': unittest.main()
