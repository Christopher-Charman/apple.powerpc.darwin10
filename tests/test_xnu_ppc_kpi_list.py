"""Execute XNU's PPC KPI export list generator against deterministic fixtures."""
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'src/powerpc/xnu-1504.15.3/config/list_supported.sh'
ORIGINAL=ROOT/'src/releases/10.6.8/xnu-1504.15.3/config/list_supported.sh'
COMPONENTS=('BSDKernel','Mach','IOKit','Libkern')
class XnuKpiListTests(unittest.TestCase):
    def test_ppc_and_all_with_spaces_in_paths(self):
        with tempfile.TemporaryDirectory(prefix='ppc kpi ') as t:
            directory=Path(t)/'source exports'
            directory.mkdir()
            for component in COMPONENTS:
                (directory/(component+'.ppc.exports')).write_text('_'+component+'_ppc:alias\n_'+component+'_common\n')
                (directory/(component+'.exports')).write_text('_'+component+'_all:alias\n')
            for arch in ('ppc','ALL'):
                out=Path(t)/('output '+arch+'.txt')
                run=subprocess.run(['bash',str(SCRIPT),str(directory),arch,str(out)],capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stderr)
                data=out.read_text()
                self.assertIn('com.apple.kpi.bsd',data)
                self.assertIn('com.apple.kpi.mach',data)
                self.assertIn('com.apple.kpi.iokit',data)
                self.assertIn('com.apple.kpi.libkern',data)
                for component in COMPONENTS:
                    self.assertIn(component+('_ppc' if arch=='ppc' else '_all'),data)
                    self.assertNotIn('_'+component+('_ppc' if arch=='ppc' else '_all')+':',data)
    def test_missing_ppc_exports_fails(self):
        with tempfile.TemporaryDirectory() as t:
            p=subprocess.run(['bash',str(SCRIPT),t,'ppc',str(Path(t)/'out')],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertIn('Missing KPI export source:',p.stderr)
    def test_upstream_preserved(self):
        text=ORIGINAL.read_text()
        self.assertIn('rm -f $TARGET_FILE',text)
        self.assertIn('if [  $ARCH == "ALL" ]',text)
if __name__=='__main__': unittest.main()
