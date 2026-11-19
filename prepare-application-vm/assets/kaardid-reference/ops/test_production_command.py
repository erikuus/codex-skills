"""Run the real shell wrapper with a fake SSH transport; never contact the VM."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class ProductionCommandTest(unittest.TestCase):
    def run_command(self,mode,fail=False):
        repo=Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);fake=root/'ssh';log=root/'calls'
            fake.write_text('''#!/usr/bin/env python3
import hashlib,os,sys,shlex
from pathlib import Path
command=sys.argv[-1]
if 'mktemp -d' in command: print('.kaardid-setup/production-tooling.12345678')
elif command.startswith('cat >'): sys.stdin.buffer.read()
elif command.startswith('sha256sum '):
 name=Path(shlex.split(command)[1]).name
 print(hashlib.sha256((Path(os.environ['TEST_REPO'])/'ops'/name).read_bytes()).hexdigest())
elif 'python3 -B' in command:
 with open(os.environ['TEST_CALLS'],'a') as output: output.write(command+'\\n')
 if '--prepare' in command and os.environ['TEST_FAIL']=='1': sys.exit(9)
else: raise SystemExit('Unexpected fake SSH command: '+command)
''');fake.chmod(0o755)
            env=dict(os.environ,PATH=str(root)+os.pathsep+os.environ['PATH'],
                     TEST_REPO=str(repo),TEST_CALLS=str(log),TEST_FAIL='1' if fail else '0')
            sha=subprocess.check_output(['git','rev-parse','main'],cwd=repo,text=True).strip()
            result=subprocess.run(['bash',str(repo/'bin/production-deploy'),mode,sha],cwd=repo,
                                  env=env,text=True,capture_output=True)
            return result,log.read_text().splitlines() if log.exists() else []

    def test_combined_deploy_prepares_then_activates_the_same_release(self):
        result,calls=self.run_command('--deploy')
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertEqual(2,len(calls))
        self.assertIn('--prepare',calls[0]);self.assertIn('--activate',calls[1])
        self.assertEqual(calls[0].split()[-1],calls[1].split()[-1])

    def test_prepare_failure_prevents_activation_and_success_message(self):
        result,calls=self.run_command('--deploy',fail=True)
        self.assertEqual(9,result.returncode)
        self.assertEqual(1,len(calls));self.assertIn('--prepare',calls[0])
        self.assertNotIn('deployment completed',result.stdout)

    def test_rollback_does_not_prepare_or_activate(self):
        result,calls=self.run_command('--rollback')
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertEqual(1,len(calls));self.assertIn('--rollback',calls[0])


if __name__=='__main__': unittest.main()
