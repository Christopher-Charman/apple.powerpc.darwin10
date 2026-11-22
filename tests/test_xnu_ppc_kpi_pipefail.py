"""Verify XNU PPC KPI generator propagates source read failures."""
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'src/powerpc/xnu-1504.15.3/config/list_supported.sh'
COMPONENTS=('BSDKernel','Mach','IOKit','Libkern')
class XnuKpiPipefailTests(unittest.TestCase):
    def test_normalization_of_ppc_exports(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for component in COMPONENTS:
                (root/(component+'.ppc.exports')).write_text('_alpha:ignored\n_beta\n')
            out=root/'SupportedKPIs-ppc.txt'
            run=subprocess.run(['bash',str(SCRIPT),str(root),'ppc',str(out)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(out.read_text().count('alpha'),4)
            self.assertEqual(out.read_text().count('beta'),4)
            self.assertNotIn('ignored',out.read_text())
    def test_directory_as_input_preserves_prior_report(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for component in COMPONENTS:
                path=root/(component+'.ppc.exports')
                if component=='Libkern':path.mkdir()
                else:path.write_text('_valid\n')
            out=root/'SupportedKPIs-ppc.txt'
            out.write_text('prior valid report\n')
            run=subprocess.run(['bash',str(SCRIPT),str(root),'ppc',str(out)],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertEqual(out.read_text(),'prior valid report\n')
            self.assertEqual(list(root.glob('.SupportedKPIs-ppc.txt.*')),[])
if __name__=='__main__': unittest.main()
