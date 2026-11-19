"""Local regressions for per-project refresh transport and interpreter binding."""
import json
import os
from pathlib import Path
import re
import runpy
import shlex
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
render = runpy.run_path(str(ROOT/"scripts/create_refresh_prompt.py"))["render"]


class ProjectRefreshTest(unittest.TestCase):
    def test_four_project_prompts_and_saved_destinations_are_isolated(self):
        apps = ("aadresslehed", "pitserid", "nimeregister", "services")
        ids = {app:"page_"+format(index+1,"032x") for index,app in enumerate(apps)}
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for app in apps:
                with self.subTest(app=app):
                    checkout = base/app
                    for name in ("bin","ops/dashboard",".codex/environments"):
                        (checkout/name).mkdir(parents=True,exist_ok=True)
                    actions = checkout/".codex/environments/environment.toml"
                    actions.write_text('name = "'+app+'"\n[[actions]]\nname = "Run"\ncommand = "fixture local development"\n')
                    before = actions.read_bytes()
                    runner = checkout/"bin/refresh-dashboard"
                    runner.write_text((ROOT/"assets/runtime/refresh-dashboard").read_text())
                    (checkout/"ops/run_bounded.py").write_text((ROOT/"assets/runtime/run_bounded.py").read_text())
                    contract = ("No local managed database and no scheduled updater. "
                                "Interpret storage, externalDatabases and iipsrv observations.") if app=="services" else (
                                "No scheduled updater. Interpret this project's release, HTTP and database observations.")
                    prompt = render(app,ids[app],"Archive/"+app,app+" status overview",contract)
                    (checkout/"ops/dashboard/refresh-prompt.md").write_text(prompt)
                    calls = checkout/"calls"
                    vm = checkout/"bin/vm"
                    vm.write_text("#!"+sys.executable+"\nfrom pathlib import Path\nPath("+repr(str(calls))+").write_text('status called')\nprint('"+app+"-fixture-status')\n")
                    vm.chmod(0o750)
                    capture = checkout/"capture"
                    saved = checkout/"saved"
                    fake = checkout/"bin/codex"
                    fake.write_text("#!"+sys.executable+"\n"
                        "import json,os,pathlib,re,sys\n"
                        "prompt=sys.stdin.read()\n"
                        "pathlib.Path(os.environ['TEST_CAPTURE']).write_text(prompt)\n"
                        "destinations=set(re.findall(r'page_[0-9a-f]{32}',prompt))\n"
                        "assert destinations=={os.environ['TEST_PAGE']}\n"
                        "assert 'Kaardid' not in prompt\n"
                        "assert 'Production updater JSON:' not in prompt\n"
                        "assert 'modelContent.updater' not in prompt\n"
                        "assert os.environ['TEST_APP']+'-fixture-status' in prompt\n"
                        "assert pathlib.Path.cwd()==pathlib.Path(os.environ['TEST_CHECKOUT'])\n"
                        "pathlib.Path(os.environ['TEST_SAVED']).write_text(json.dumps({'page':os.environ['TEST_PAGE'],'app':os.environ['TEST_APP']}))\n"
                        "result=pathlib.Path(sys.argv[sys.argv.index('--output-last-message')+1])\n"
                        "result.write_text(json.dumps({'saved':True,'summary':'Fixture project Page verified'}))\n")
                    fake.chmod(0o750)
                    env = {**os.environ,"PATH":str(checkout/"bin")+os.pathsep+os.environ["PATH"],
                           "TEST_CAPTURE":str(capture),"TEST_PAGE":ids[app],"TEST_APP":app,
                           "TEST_CHECKOUT":str(checkout.resolve()),"TEST_SAVED":str(saved)}
                    result = subprocess.run([sys.executable,str(runner)],cwd=base,
                                            env=env,text=True,capture_output=True,timeout=5)
                    self.assertEqual(0,result.returncode,result.stderr)
                    self.assertEqual({"page":ids[app],"app":app},json.loads(saved.read_text()))
                    self.assertEqual(before,actions.read_bytes())
                    self.assertEqual("status called",calls.read_text())
                    captured = capture.read_text()
                    self.assertEqual({ids[app]},set(re.findall("page_[0-9a-f]{32}",captured)))
                    self.assertIn("VM observation receipt:",captured)
                    if app=="services":
                        self.assertIn("No local managed database",captured)
                        self.assertIn("storage, externalDatabases and iipsrv",captured)

    def test_prompt_inputs_are_resolved_and_single_destination(self):
        with self.assertRaises(ValueError):
            render("example","not-a-page","Archive/example","Overview","HTTP status")
        with self.assertRaises(ValueError):
            render("example","page_"+"1"*32,"Archive/example","Overview","Also edit page_"+"2"*32)
        with self.assertRaises(ValueError):
            render("{{APP}}","page_"+"1"*32,"Archive/example","Overview","HTTP status")

    def test_prompt_generator_preserves_existing_project_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            status = root/"status"
            status.write_text("No scheduled updater.")
            output = root/"refresh-prompt.md"
            output.write_text("Human-maintained instructions")
            result = subprocess.run([sys.executable,str(ROOT/"scripts/create_refresh_prompt.py"),
                "--application","example","--page-id","page_"+"1"*32,
                "--repository","Archive/example","--overview","Example overview",
                "--status-file",str(status),"--output",str(output)],
                text=True,capture_output=True)
            self.assertEqual(1,result.returncode)
            self.assertEqual("Human-maintained instructions",output.read_text())


class SelectedInterpreterTest(unittest.TestCase):
    def test_rendered_precheck_uses_selected_python_with_local_storage_fixture(self):
        template = (ROOT/"assets/systemd/iipsrv.service.template").read_text()
        command = next(line.split("=",1)[1] for line in template.splitlines() if line.startswith("ExecStartPre="))
        with tempfile.TemporaryDirectory(prefix="selected python ") as temporary:
            base = Path(temporary).resolve()
            marker = base/"interpreter.json"
            selected = base/"python-selected"
            selected.write_text("#!"+sys.executable+"\n"
                "import json,os,pathlib,sys\n"
                "pathlib.Path("+repr(str(marker))+").write_text(json.dumps({'argv':sys.argv[1:],'uid':os.geteuid()}))\n"
                "os.execv(sys.executable,[sys.executable,*sys.argv[1:]])\n")
            selected.chmod(0o750)
            storage = base/"storage"
            storage.mkdir()
            (storage/"known.tif").write_bytes(b"fixture image")
            checker = base/"check storage.py"
            checker.write_text((ROOT/"assets/runtime/check_storage.py").read_text())
            findmnt = base/"findmnt"
            record = {"filesystems":[{"source":"archive:/images","target":str(storage),
                                       "fstype":"nfs4","options":"ro"}]}
            findmnt.write_text("#!"+sys.executable+"\nprint("+repr(json.dumps(record))+")\n")
            findmnt.chmod(0o750)
            values = {"PYTHON_EXECUTABLE":str(selected),"PRIVATE_STORAGE_CHECK":str(checker),
                      "EXPECTED_SHARE_SOURCE":"archive:/images","EXPECTED_SHARE_TYPE":"nfs4",
                      "KNOWN_FILE_RELATIVE_PATH":"known.tif"}
            command = re.sub(r"\{\{([A-Z_]+)\}\}",lambda m:values[m[1]],command)
            arguments = shlex.split(command)
            # The live mountpoint is replaced only inside this disposable fixture.
            arguments[arguments.index("--mount")+1] = str(storage)
            env = {**os.environ,"PATH":str(base)+os.pathsep+os.environ["PATH"]}
            result = subprocess.run(arguments,env=env,text=True,capture_output=True,timeout=4)
            self.assertEqual(0,result.returncode,result.stderr)
            self.assertTrue(json.loads(result.stdout)["mountVerified"])
            self.assertEqual(str(selected),arguments[0])
            self.assertEqual(str(checker),json.loads(marker.read_text())["argv"][0])
            self.assertEqual(os.geteuid(),json.loads(marker.read_text())["uid"])


if __name__ == "__main__":
    unittest.main()

