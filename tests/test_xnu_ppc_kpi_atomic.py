"""Source-only regression tests for PowerPC KPI report atomic replacement."""
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'src/powerpc/xnu-1504.15.3/config/list_supported.sh'
COMPONENTS=('BSDKernel','Mach','IOKit','Libkern')
class XnuKpiAtomicTests(unittest.TestCase):
    def test_success_replaces_prior_report_and_cleans_temp(self):
        with tempfile.TemporaryDirectory(prefix='ppc kpi ') as t:
            root=Path(t)
            for component in COMPONENTS:
                (root/(component+'.ppc.exports')).write_text('_'+component+'_ppc\n')
            out=root/'SupportedKPIs-ppc.txt'
            out.write_text('previous output\n')
            result=subprocess.run(['bash',str(SCRIPT),str(root),'ppc',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            for component in COMPONENTS:self.assertIn(component+'_ppc',out.read_text())
            self.assertNotIn('previous output',out.read_text())
            self.assertEqual(list(root.glob('.SupportedKPIs-ppc.txt.*')),[])
    def test_missing_last_export_preserves_prior_report(self):
        with tempfile.TemporaryDirectory(prefix='ppc kpi ') as t:
            root=Path(t)
            for component in COMPONENTS[:-1]:
                (root/(component+'.ppc.exports')).write_text('_valid\n')
            out=root/'SupportedKPIs-ppc.txt'
            out.write_text('previous output\n')
            result=subprocess.run(['bash',str(SCRIPT),str(root),'ppc',str(out)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(out.read_text(),'previous output\n')
            self.assertEqual(list(root.glob('.SupportedKPIs-ppc.txt.*')),[])
if __name__=='__main__': unittest.main()
