"""Prevent XNU PPC KPI generation from destroying valid output on missing inputs."""
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'src/powerpc/xnu-1504.15.3/config/list_supported.sh'
class XnuKpiPreflightTests(unittest.TestCase):
    def test_missing_last_ppc_input_preserves_previous_output(self):
        with tempfile.TemporaryDirectory(prefix='ppc kpi ') as t:
            directory=Path(t)/'exports with spaces'
            directory.mkdir()
            for component in ('BSDKernel','Mach','IOKit'):
                (directory/(component+'.ppc.exports')).write_text('_valid\n')
            out=Path(t)/'previous valid output.txt'
            out.write_text('previous valid output\n')
            result=subprocess.run(['bash',str(SCRIPT),str(directory),'ppc',str(out)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('Libkern.ppc.exports',result.stderr)
            self.assertEqual(out.read_text(),'previous valid output\n')
    def test_complete_ppc_exports_succeed(self):
        with tempfile.TemporaryDirectory() as t:
            for component in ('BSDKernel','Mach','IOKit','Libkern'):
                (Path(t)/(component+'.ppc.exports')).write_text('_valid\n')
            out=Path(t)/'SupportedKPIs-ppc.txt'
            result=subprocess.run(['bash',str(SCRIPT),t,'ppc',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(out.read_text().count('valid'),4)
if __name__=='__main__': unittest.main()
