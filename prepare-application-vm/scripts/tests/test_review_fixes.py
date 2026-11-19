"""Focused regressions for writable shared state, storage deadlines and Python."""
import grp
from contextlib import nullcontext
import json
import os
from pathlib import Path
import pwd
import runpy
import stat
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import test_skill as fixtures

ROOT = Path(__file__).resolve().parents[2]


class SharedStateTest(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.BootstrapTest(methodName="runTest")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.content = self.fixture.target/"shared/content"
        self.owner = pwd.getpwuid(os.geteuid()).pw_name
        self.group = grp.getgrgid(self.content.stat().st_gid).gr_name
        self.fixture.mapping["apps/example/content"] = {
            "target":"content","owner":self.owner,"group":self.group,"mode":"2770"}
        self.content.chmod(0o2770)
        # Some macOS filesystems strip setgid. Preserve real group-write coverage.
        self.actual_mode = stat.S_IMODE(self.content.stat().st_mode)
        self.fixture.mapping["apps/example/content"]["mode"] = format(self.actual_mode,"04o")

    def test_declared_group_writable_directory_stages_and_reuses(self):
        self.assertFalse(self.fixture.run_stage()["reused"])
        self.assertTrue(self.fixture.run_stage()["reused"])
        self.assertEqual(self.actual_mode, stat.S_IMODE(self.content.stat().st_mode))
        self.assertEqual("Operator-edited introduction",(self.content/"introduction.html").read_text())

    def test_declared_application_identity_is_independent_of_deployer(self):
        # Exercise foreign runtime metadata without creating local system accounts.
        actual_lstat = Path.lstat
        content = self.content.resolve()
        runtime_uid, runtime_gid = os.geteuid()+10000, os.getegid()+10000
        def runtime_metadata(path):
            info = actual_lstat(path)
            if path == content:
                fields = list(info)
                fields[0] = stat.S_IFDIR|0o2770
                fields[4], fields[5] = runtime_uid, runtime_gid
                return os.stat_result(fields)
            return info
        self.fixture.mapping["apps/example/content"].update(owner="fixture-app",group="fixture-app",mode="2770")
        with patch.object(Path,"lstat",autospec=True,side_effect=runtime_metadata), patch(
                "pwd.getpwnam",return_value=SimpleNamespace(pw_uid=runtime_uid)), patch(
                "grp.getgrnam",return_value=SimpleNamespace(gr_gid=runtime_gid)):
            self.assertFalse(self.fixture.run_stage()["reused"])

    def test_wrong_owner_group_mode_and_world_writes_stop(self):
        policy = self.fixture.mapping["apps/example/content"]
        for kind in ("owner","group","mode","world"):
            with self.subTest(kind=kind):
                changed = dict(policy)
                if kind == "owner":
                    changed["owner"] = "fixture-wrong"
                    context = patch("pwd.getpwnam",return_value=SimpleNamespace(pw_uid=os.geteuid()+1))
                elif kind == "group":
                    changed["group"] = "fixture-wrong"
                    context = patch("grp.getgrnam",return_value=SimpleNamespace(gr_gid=os.getegid()+10000))
                elif kind == "mode":
                    changed["mode"] = "2750"
                    context = nullcontext()
                else:
                    changed["mode"] = "2777"
                    self.content.chmod(0o2777)
                    context = nullcontext()
                self.fixture.mapping["apps/example/content"] = changed
                with context, self.assertRaises(ValueError):
                    self.fixture.run_stage()
                self.content.chmod(0o2770)
        self.fixture.mapping["apps/example/content"] = policy

    def test_shared_symlink_and_mutable_release_root_still_rejected(self):
        outside = self.fixture.base/"outside"
        outside.mkdir()
        self.content.rename(self.fixture.target/"shared/retained-content")
        self.content.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.fixture.run_stage()
        self.content.unlink()
        (self.fixture.target/"shared/retained-content").rename(self.content)
        (self.fixture.target/"releases").chmod(0o2770)
        with self.assertRaises(ValueError):
            self.fixture.run_stage()


class StorageDeadlineTest(unittest.TestCase):
    def setUp(self):
        self.module = runpy.run_path(str(ROOT/"assets/runtime/check_storage.py"))

    def test_fifo_is_rejected_without_opening(self):
        with tempfile.TemporaryDirectory() as temporary:
            mount = Path(temporary).resolve()
            os.mkfifo(mount/"blocked")
            data = {"filesystems":[{"source":"archive:/images","target":str(mount),
                                   "fstype":"nfs4","options":"ro"}]}
            result = subprocess.CompletedProcess([],0,stdout=json.dumps(data))
            with patch("subprocess.run",return_value=result), patch("os.open") as opened:
                with self.assertRaisesRegex(ValueError,"must be regular"):
                    self.module["_inspect"](str(mount),"archive:/images","nfs4","blocked")
                opened.assert_not_called()

    def test_entire_worker_deadline_covers_stalled_io(self):
        original = subprocess.Popen
        def stalled_worker(command, **kwargs):
            return original([sys.executable,"-c","import time; time.sleep(30)"],**kwargs)
        started = time.monotonic()
        with patch("subprocess.Popen",side_effect=stalled_worker):
            with self.assertRaisesRegex(ValueError,"deadline exceeded"):
                self.module["verify"]("/unused","archive:/images","nfs4","known",timeout=0.15)
        self.assertLess(time.monotonic()-started,2)

    def test_stalled_findmnt_and_fifo_are_bounded_through_real_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            mount = Path(temporary).resolve()
            finder = mount/"findmnt"
            fifo = mount/"blocked"
            os.mkfifo(fifo)
            record = {"filesystems":[{"source":"archive:/images","target":str(mount),
                                      "fstype":"nfs4","options":"ro"}]}
            env = {**os.environ,"PATH":str(mount)+os.pathsep+os.environ["PATH"]}
            command = [sys.executable,str(ROOT/"assets/runtime/check_storage.py"),
                       "--mount",str(mount),"--source","archive:/images","--fstype","nfs4",
                       "--known-file","blocked","--timeout","0.5"]
            for body in ("import time; time.sleep(30)", "import sys; sys.stdout.write("+repr(json.dumps(record))+")"):
                finder.write_text("#!"+sys.executable+"\n"+body+"\n")
                finder.chmod(0o750)
                result = subprocess.run(command,env=env,text=True,capture_output=True,timeout=3)
                self.assertEqual(1,result.returncode)
                self.assertIs(False,json.loads(result.stdout)["mountVerified"])
                self.assertNotIn("checkedAt",json.loads(result.stdout))

    def test_public_success_receipt_with_fake_mount_command(self):
        with tempfile.TemporaryDirectory() as temporary:
            mount = Path(temporary).resolve()
            (mount/"known").write_bytes(b"image")
            record = {"filesystems":[{"source":"archive:/images","target":str(mount),
                                      "fstype":"nfs4","options":"ro"}]}
            finder = mount/"findmnt"
            finder.write_text("#!"+sys.executable+"\nprint("+repr(json.dumps(record))+")\n")
            finder.chmod(0o750)
            env = {**os.environ,"PATH":str(mount)+os.pathsep+os.environ["PATH"]}
            with patch.dict(os.environ,env):
                result = self.module["verify"](str(mount),"archive:/images","nfs4","known",timeout=2)
            self.assertTrue(result["mountVerified"])
            self.assertIn("checkedAt",result)


class PythonPreflightTest(unittest.TestCase):
    def test_supported_and_older_versions(self):
        check = runpy.run_path(str(ROOT/"scripts/check_python.py"))["require_python"]
        for version in ((3,12),(3,14),(4,0)):
            self.assertEqual(version,check(version))
        for version in ((3,10),(3,11)):
            with self.assertRaisesRegex(RuntimeError,"3.12"):
                check(version)

    def test_staging_and_storage_fail_before_work_on_older_python(self):
        for script in ("scripts/stage_release.py","assets/runtime/check_storage.py"):
            with self.subTest(script=script), patch.object(sys,"version_info",(3,11,0)), self.assertRaisesRegex(SystemExit,"3.12"):
                runpy.run_path(str(ROOT/script))


if __name__ == "__main__":
    unittest.main()

