"""Behavioral fixtures for topology, staging, locking and bounded execution."""
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
validate = runpy.run_path(str(ROOT/"scripts/check_topology.py"))["validate"]
stage = runpy.run_path(str(ROOT/"scripts/stage_release.py"))


class TopologyTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/"assets/topology.example.json").read_text())

    def test_single_shared_and_database_free(self):
        self.assertEqual((2, 4), validate(self.data))
        for index in (0, 3):
            data = deepcopy(self.data)
            data["apps"] = [data["apps"][index]]
            data["hosts"] = [h for h in data["hosts"] if h["id"] == data["apps"][0]["host"]]
            self.assertEqual((1, 1), validate(data))

    def test_missing_public_identity_leaves_preparation_available(self):
        self.data["apps"][0]["publicOrigin"] = None
        self.assertEqual((2, 4), validate(self.data))

    def test_unsafe_identities_paths_and_misspelled_allocations(self):
        for field, value in (("serviceUser","root"), ("root","/etc"),
                             ("setupRoot","/home/operator"), ("probeport",18090),
                             ("fpmSocket","/srv/seals/shared/socket")):
            with self.subTest(field=field):
                data = deepcopy(self.data)
                data["apps"][0]["environments"]["rehearsal"][field] = value
                with self.assertRaises(ValueError):
                    validate(data)

    def test_sibling_and_cross_environment_collisions(self):
        original = self.data["apps"][0]["environments"]["rehearsal"]
        for field in ("root", "setupRoot", "serviceUser", "fpmSocket", "probePort", "webTunnelPort", "dbTunnelPort"):
            data = deepcopy(self.data)
            data["apps"][1]["environments"]["production"][field] = original[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate(data)
        self.data["apps"][0]["environments"]["rehearsal"]["unitNames"] = ["example.service"]
        self.data["apps"][1]["environments"]["production"]["unitNames"] = ["example.service"]
        with self.assertRaises(ValueError):
            validate(self.data)

    def test_roles_and_database_collisions(self):
        original = self.data["apps"][0]["environments"]["rehearsal"]["database"]
        for field in ("name","appRole","migrationRole","ownerRole"):
            data = deepcopy(self.data)
            data["apps"][1]["environments"]["production"]["database"][field] = original[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate(data)


class BootstrapTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.target = self.base/"app"
        self.target.mkdir(mode=0o750)
        for path in ("releases","shared","shared/config","shared/content"):
            (self.target/path).mkdir(mode=0o750)
        (self.target/"shared/content/introduction.html").write_text("Operator-edited introduction")
        self.sha = "a"*40
        self.archive = self.base/"release.tar.gz"
        self.manifest = self.base/"manifest.json"
        self.mapping = {"apps/example/content":"content","apps/example/private":"config"}
        self.make_archive()

    def make_archive(self, extra=None):
        with tarfile.open(self.archive, "w:gz") as bundle:
            for name in ("", "apps", "apps/example", "apps/example/content", "apps/example/private"):
                entry = tarfile.TarInfo(self.sha+("/"+name if name else ""))
                entry.type = tarfile.DIRTYPE
                entry.mode = 0o750
                bundle.addfile(entry)
            entry = tarfile.TarInfo(self.sha+"/apps/example/index.php")
            entry.mode = 0o640
            entry.size = 5
            bundle.addfile(entry, io.BytesIO(b"<?php"))
            if extra:
                entry = tarfile.TarInfo(extra)
                entry.size = 1
                bundle.addfile(entry, io.BytesIO(b"x"))
        self.manifest.write_text(json.dumps({
            "commit":self.sha, "artifact_sha256":hashlib.sha256(self.archive.read_bytes()).hexdigest()}))

    def run_stage(self):
        return stage["prepare"](self.target, self.archive, self.manifest, self.mapping)

    def test_first_stage_retry_and_durable_content(self):
        first = self.run_stage()
        self.assertFalse(first["reused"])
        self.assertTrue(self.run_stage()["reused"])
        link = Path(first["release"])/"apps/example/content"
        self.assertEqual("Operator-edited introduction", (link/"introduction.html").read_text())
        self.assertFalse((self.target/"rehearsal").exists())

    def test_active_pointer_uses_routine_deployment(self):
        release = Path(self.run_stage()["release"])
        (self.target/"rehearsal").symlink_to(release)
        with self.assertRaisesRegex(ValueError, "already initialized"):
            self.run_stage()

    def test_tampered_stage_and_wrong_link_are_preserved(self):
        release = Path(self.run_stage()["release"])
        (release/"apps/example/index.php").write_text("changed")
        with self.assertRaisesRegex(ValueError, "content differs"):
            self.run_stage()
        self.assertEqual("changed", (release/"apps/example/index.php").read_text())

    def test_wrong_shared_link_is_rejected(self):
        release = Path(self.run_stage()["release"])
        link = release/"apps/example/content"
        link.unlink()
        link.symlink_to(self.target/"shared/config")
        with self.assertRaisesRegex(ValueError,"Unexpected shared link"):
            self.run_stage()

    def test_archive_links_are_rejected(self):
        with tarfile.open(self.archive,"w:gz") as bundle:
            entry = tarfile.TarInfo(self.sha+"/escape")
            entry.type = tarfile.SYMTYPE
            entry.linkname = "/etc"
            bundle.addfile(entry)
        data = json.loads(self.manifest.read_text())
        data["artifact_sha256"] = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,"Unsafe"):
            self.run_stage()

    def test_bad_checksum_traversal_and_populated_placeholder(self):
        self.archive.write_bytes(b"corrupt")
        with self.assertRaisesRegex(ValueError, "checksum"):
            self.run_stage()
        for extra in (self.sha+"/../escape", self.sha+"/apps/example/content/overwrite"):
            self.make_archive(extra)
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.run_stage()
        self.assertEqual([], list((self.target/"releases").iterdir()))

    def test_abandoned_attempt_and_siblings_are_preserved(self):
        abandoned = self.target/"releases/.bootstrap-abandoned"
        abandoned.mkdir()
        (abandoned/"sentinel").write_text("partial")
        sibling = self.base/"other-app"
        sibling.mkdir()
        (sibling/"state").write_text("keep")
        self.run_stage()
        self.assertEqual("partial", (abandoned/"sentinel").read_text())
        self.assertEqual("keep", (sibling/"state").read_text())

    def test_bootstrap_lock_excludes_concurrent_attempt(self):
        with stage["lock"](self.target):
            with self.assertRaises(BlockingIOError):
                self.run_stage()

    def test_content_survives_release_switch_and_return(self):
        first = Path(self.run_stage()["release"])
        self.sha = "b"*40
        self.make_archive()
        second = Path(self.run_stage()["release"])
        pointer = self.target/"rehearsal"
        pointer.symlink_to(first)
        for release in (second, first):
            temporary = self.target/"incoming"
            temporary.symlink_to(release)
            os.replace(temporary, pointer)
            self.assertEqual("Operator-edited introduction",
                             (pointer/"apps/example/content/introduction.html").read_text())


class RolePlanTest(unittest.TestCase):
    def test_second_third_app_and_rerun_preserve_operator_and_sibling_roles(self):
        plan = runpy.run_path(str(ROOT/"scripts/plan_app_roles.py"))["plan"]
        existing = ["operator", "first_app", "first_owner"]
        for app in ("second", "third"):
            roles = {kind:app+"_"+kind for kind in ("owner","migrate","app","readonly")}
            data = {"operator":"operator", "roles":roles, "existingRoles":existing, "managedRoles":[]}
            result = plan(data)
            self.assertEqual(set(roles.values()),set(result["createdRoles"]))
            self.assertNotIn("ALTER ROLE",result["sql"])
            self.assertNotIn("first_app",result["sql"])
            self.assertIn('TO "operator"',result["sql"])
            existing.extend(roles.values())
            data.update(existingRoles=existing,managedRoles=list(roles.values()))
            self.assertEqual([],plan(data)["createdRoles"])

    def test_unmanaged_role_and_missing_operator_stop(self):
        plan = runpy.run_path(str(ROOT/"scripts/plan_app_roles.py"))["plan"]
        roles = {kind:"example_"+kind for kind in ("owner","migrate","app","readonly")}
        data = {"operator":"operator","roles":roles,"existingRoles":[],"managedRoles":[]}
        with self.assertRaises(ValueError):
            plan(data)
        data["existingRoles"]=["operator","example_app"]
        with self.assertRaises(ValueError):
            plan(data)


class ProcessTest(unittest.TestCase):
    def call_bounded(self, command, timeout=0.2):
        return subprocess.run([sys.executable,str(ROOT/"assets/runtime/run_bounded.py"),
                               "--timeout",str(timeout),"--",*command],
                              text=True,capture_output=True,timeout=4)

    def test_normal_failure_timeout_and_missing_executable(self):
        self.assertEqual(0,self.call_bounded([sys.executable,"-c","pass"]).returncode)
        self.assertEqual(7,self.call_bounded([sys.executable,"-c","raise SystemExit(7)"]).returncode)
        self.assertEqual(124,self.call_bounded([sys.executable,"-c","import time; time.sleep(10)"]).returncode)
        self.assertEqual(127,self.call_bounded(["/nonexistent/skill-command"]).returncode)

    def test_timeout_closes_descendant_pipes(self):
        code = ("import subprocess,sys,time; "
                "subprocess.Popen([sys.executable,'-c','import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(10)']); "
                "time.sleep(10)")
        result = self.call_bounded([sys.executable,"-c",code])
        self.assertEqual(124,result.returncode)

    def test_signal_cleans_child_group(self):
        process = subprocess.Popen([sys.executable,str(ROOT/"assets/runtime/run_bounded.py"),
                                    "--timeout","10","--",sys.executable,"-c","import time; time.sleep(10)"],
                                   stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            time.sleep(0.15)
            process.send_signal(signal.SIGTERM)
            process.communicate(timeout=3)
            self.assertEqual(130,process.returncode)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

    def test_host_lock_contention_and_reuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock = Path(tmp)/"host.lock"
            context = runpy.run_path(str(ROOT/"scripts/with_host_lock.py"))
            import fcntl
            with lock.open("w") as held:
                lock.chmod(0o600)
                fcntl.flock(held,fcntl.LOCK_EX|fcntl.LOCK_NB)
                self.assertEqual(75,context["run"](lock,[sys.executable,"-c","pass"]))
            self.assertEqual(0,context["run"](lock,[sys.executable,"-c","pass"]))

    def test_foreground_helper_retains_host_lock_if_wrapper_dies(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock, ready = Path(tmp)/"host.lock", Path(tmp)/"ready"
            code = "import os,time; from pathlib import Path; Path("+repr(str(ready))+").write_text(str(os.getpid())); time.sleep(5)"
            wrapper = subprocess.Popen([sys.executable,str(ROOT/"scripts/with_host_lock.py"),
                                        "--lock",str(lock),"--",sys.executable,"-c",code])
            child = None
            try:
                for attempt in range(100):
                    if ready.exists():
                        break
                    time.sleep(0.01)
                self.assertTrue(ready.exists())
                child = int(ready.read_text())
                wrapper.kill()
                wrapper.wait(timeout=2)
                run = runpy.run_path(str(ROOT/"scripts/with_host_lock.py"))["run"]
                self.assertEqual(75,run(lock,[sys.executable,"-c","pass"]))
            finally:
                if wrapper.poll() is None:
                    wrapper.kill()
                    wrapper.wait()
                if child:
                    try:
                        os.kill(child,signal.SIGTERM)
                    except ProcessLookupError:
                        pass

    def test_manual_runner_with_fake_vm_and_codex(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for name in ("bin","ops/dashboard"):
                (base/name).mkdir(parents=True)
            runner = base/"bin/refresh-dashboard"
            runner.write_text((ROOT/"assets/runtime/refresh-dashboard").read_text())
            (base/"ops/run_bounded.py").write_text((ROOT/"assets/runtime/run_bounded.py").read_text())
            (base/"ops/dashboard/refresh-prompt.md").write_text("Preserve last-success times on failed checks.")
            vm = base/"bin/vm"
            vm.write_text("#!/bin/sh\necho fixture-vm-status\n")
            vm.chmod(0o750)
            codex = base/"bin/codex"
            codex.write_text("#!"+sys.executable+"\nimport json,pathlib,sys\nprompt=sys.stdin.read()\nassert 'fixture-vm-status' in prompt\np=pathlib.Path(sys.argv[sys.argv.index('--output-last-message')+1])\np.write_text(json.dumps({'saved':True,'summary':'Fixture save verified'}))\n")
            codex.chmod(0o750)
            result = subprocess.run([sys.executable,str(runner)],text=True,capture_output=True,
                                    env={**os.environ,"PATH":str(base/"bin")+os.pathsep+os.environ["PATH"]},timeout=5)
            self.assertEqual(0,result.returncode,result.stderr)
            self.assertIn("Fixture save verified",result.stdout)


class StorageTest(unittest.TestCase):
    def test_mount_identity_and_readability(self):
        verify = runpy.run_path(str(ROOT/"assets/runtime/check_storage.py"))["_inspect"]
        with tempfile.TemporaryDirectory() as tmp:
            mount = Path(tmp).resolve()
            (mount/"known.tif").write_bytes(b"IIfixture")
            record = {"source":"archive:/images","target":str(mount),"fstype":"nfs4","options":"ro,relatime"}
            response = subprocess.CompletedProcess([],0,stdout=json.dumps({"filesystems":[record]}))
            with patch("subprocess.run",return_value=response):
                self.assertTrue(verify(str(mount),"archive:/images","nfs4","known.tif")["mountVerified"])
            for field,value in (("target","/"),("source","local-root"),("options","rw,relatime")):
                wrong = {**record,field:value}
                response.stdout = json.dumps({"filesystems":[wrong]})
                with self.subTest(field=field), patch("subprocess.run",return_value=response), self.assertRaises(ValueError):
                    verify(str(mount),"archive:/images","nfs4","known.tif")
            response.stdout = json.dumps({"filesystems":[record]})
            with patch("subprocess.run",return_value=response), self.assertRaises(OSError):
                verify(str(mount),"archive:/images","nfs4","missing.tif")


if __name__ == "__main__":
    unittest.main()

