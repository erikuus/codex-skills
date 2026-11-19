"""Exercise the deployment lifecycle with disposable releases and a fake database."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('deployment', Path(__file__).with_name('deploy-rehearsal.py'))
deployment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment)


class DeploymentMaintenanceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.stages = self.root/'staging';self.stages.mkdir()
        self.config = self.root/'shared/config';self.config.mkdir(parents=True)
        self.marker = self.config/'.maintenance'
        self.runtime = self.root/'shared/runtime';self.runtime.mkdir()
        self.probe = self.config/'.deployment-probe.json'
        self.releases = []
        for letter in 'abc':
            release = self.root/'releases'/(letter*40)
            (release/'apps/kaardid').mkdir(parents=True)
            (release/'release.json').write_text(json.dumps({'commit':release.name,'purpose':'private-rehearsal'}))
            self.releases.append(release)
        self.obsolete, self.current, self.incoming = self.releases
        self.link = self.root/'rehearsal';self.link.symlink_to(self.current)
        self.previous = self.root/'previous';self.previous.symlink_to(self.obsolete)
        self.stage = self.stages/'release-new';self.stage.mkdir()
        self.events = []
        self.tokens = []
        self.output = io.StringIO()
        self.errors = io.StringIO()
        self.backups = self.stages/'rehearsal-backups'

    def fetch(self, path, token=None):
        self.assertEqual('/',path)
        self.assertIsNone(token)
        self.events.append('visitor')
        return (503 if self.marker.exists() else 200), b'', ''

    def database(self, app, stage, backups, credentials):
        self.events.append('backup+migrate')
        self.assertTrue(self.marker.exists())
        self.assertEqual(0o640,self.marker.stat().st_mode & 0o777)
        self.assertFalse(self.probe.exists())
        self.assertEqual(self.current,self.link.resolve())
        backups.mkdir(mode=0o700, exist_ok=True)
        snapshot = Path(tempfile.mkdtemp(prefix='20261030T120000Z-'+self.incoming.name[:12]+'-',dir=backups))
        backup = snapshot/'kaart.dump';backup.write_bytes(b'fixture');backup.chmod(0o600)
        metadata = snapshot/'backup.json'
        metadata.write_text(json.dumps({'database':'kaart','target_commit':self.incoming.name,
            'sha256':hashlib.sha256(b'fixture').hexdigest(),'deployment_status':'pending'}))
        metadata.chmod(0o600)
        return backup

    def check(self, token=None):
        self.events.append('private-check' if token else 'public-check')
        self.assertEqual(self.incoming,self.link.resolve())
        # Retention may only run after both kinds of health checks succeed.
        self.assertTrue(self.obsolete.exists())
        if token:
            self.tokens.append(token)
            self.assertTrue(self.marker.exists())
            self.assertEqual(0o640,self.probe.stat().st_mode & 0o777)
            probe = json.loads(self.probe.read_text())
            self.assertEqual(token,probe['token'])
            self.assertEqual(str(self.incoming/'apps/kaardid'),probe['appPath'])
            self.assertGreater(probe['expiresAt'],deployment.time.time())
        else:
            self.assertFalse(self.marker.exists())
            self.assertFalse(self.probe.exists())
        return ['fixture checks passed']

    def deploy(self, database=None, check=None, fetch=None):
        with patch.object(deployment,'backup_and_migrate',side_effect=database or self.database):
            with patch.object(deployment,'health_check',side_effect=check or self.check):
                with patch.object(deployment,'fetch',side_effect=fetch or self.fetch):
                    with contextlib.redirect_stdout(self.output), contextlib.redirect_stderr(self.errors):
                        return deployment.deploy_with_maintenance(self.incoming,self.link,self.current,
                                                                 self.stage,self.root/'db.json')

    def assert_closed_failure(self, switched=False):
        self.assertTrue(self.marker.exists())
        self.assertFalse(self.probe.exists())
        self.assertEqual(self.current,self.link.resolve())
        self.assertEqual(self.obsolete,self.previous.resolve())
        self.assertTrue(all(release.exists() for release in self.releases))
        self.assertIn('maintenance remains ON',self.errors.getvalue())
        if switched:self.assertIn('previous rehearsal link restored',self.errors.getvalue())

    def test_success_closes_before_backup_checks_while_closed_then_reopens_and_prunes(self):
        report = self.deploy()
        self.assertEqual(['visitor','backup+migrate','private-check','visitor','public-check'],self.events)
        self.assertFalse(self.marker.exists())
        self.assertFalse(self.probe.exists())
        self.assertEqual(self.incoming,self.link.resolve())
        self.assertEqual(self.current,self.previous.resolve())
        self.assertFalse(self.obsolete.exists())
        self.assertTrue(any('Maintenance disabled' in line for line in report))
        self.assertTrue(any('Backup cleanup:' in line for line in report))
        self.assertEqual(['succeeded'],[json.loads(p.read_text())['deployment_status']
                                      for p in self.backups.glob('*/backup.json')])
        for token in self.tokens:
            self.assertNotIn(token,self.output.getvalue()+self.errors.getvalue()+'\n'.join(report))

    def test_held_updater_lock_stops_deployment_before_maintenance_or_database_work(self):
        with deployment.operation_lock(self.runtime):
            with self.assertRaisesRegex(RuntimeError,'no deployment work'):self.deploy()
        self.assertFalse(self.marker.exists())
        self.assertEqual([],self.events)

    def test_deployment_holds_shared_lock_through_backup_and_both_health_checks(self):
        def locked():
            with self.assertRaisesRegex(RuntimeError,'Updater or deployment'):
                with deployment.operation_lock(self.runtime):self.fail('Lock was not held.')
        def database(*args):
            locked();return self.database(*args)
        def check(token=None):
            locked();return self.check(token)
        self.deploy(database=database,check=check)
        with deployment.operation_lock(self.runtime):pass

    def test_success_preserves_existing_manual_maintenance_and_marker_contents(self):
        self.marker.write_text('operator message');self.marker.chmod(0o640)
        report = self.deploy()
        self.assertEqual('operator message',self.marker.read_text())
        self.assertNotIn('public-check',self.events)
        self.assertFalse(self.probe.exists())
        self.assertTrue(any('manual maintenance preserved' in line for line in report))

    def test_backup_or_migration_failure_keeps_old_code_and_maintenance(self):
        def fail(*args):
            self.database(*args)
            raise RuntimeError('database failure')
        with self.assertRaisesRegex(RuntimeError,'database failure'):self.deploy(database=fail)
        self.assert_closed_failure()
        self.assertEqual(['pending'],[json.loads(p.read_text())['deployment_status']
                                    for p in self.backups.glob('*/backup.json')])
        self.assertNotIn('private-check',self.events)

    def test_private_check_failure_rolls_back_code_revokes_probe_and_skips_cleanup(self):
        def fail(token):
            self.check(token)
            raise RuntimeError('private readiness failed')
        with patch.object(deployment,'prune_backups') as prune:
            with self.assertRaisesRegex(RuntimeError,'private readiness failed'):self.deploy(check=fail)
        prune.assert_not_called()
        self.assert_closed_failure(switched=True)

    def test_backup_cleanup_error_does_not_close_or_roll_back_healthy_site(self):
        with patch.object(deployment,'prune_backups',side_effect=OSError('fixture failure')):
            report = self.deploy()
        self.assertFalse(self.marker.exists())
        self.assertEqual(self.incoming,self.link.resolve())
        self.assertTrue(any('Backup cleanup warning:' in line for line in report))

    def test_failure_after_reopening_closes_site_again_and_rolls_back(self):
        def fail(token=None):
            self.check(token)
            if token is None:raise RuntimeError('public readiness failed')
            return []
        with self.assertRaisesRegex(RuntimeError,'public readiness failed'):self.deploy(check=fail)
        self.assert_closed_failure(switched=True)

    def test_cancellation_revokes_probe_and_rolls_back_without_reopening(self):
        def cancel(token):
            self.check(token)
            raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):self.deploy(check=cancel)
        self.assert_closed_failure(switched=True)

    def test_unconfirmed_maintenance_prevents_database_work(self):
        with self.assertRaisesRegex(RuntimeError,'no database work'):
            self.deploy(fetch=lambda *args:(200,b'', ''))
        self.assert_closed_failure()
        self.assertEqual([],self.events)

    def test_visitors_must_still_be_closed_after_private_checks(self):
        calls=0
        def escaped(path,token=None):
            nonlocal calls
            calls+=1
            return (503 if calls==1 else 200),b'',''
        with self.assertRaisesRegex(RuntimeError,'Visitors escaped maintenance'):
            self.deploy(fetch=escaped)
        self.assert_closed_failure(switched=True)

    def test_stale_private_probe_is_revoked_before_backup(self):
        self.probe.write_text('{"token":"stale"}');self.probe.chmod(0o640)
        self.deploy()
        self.assertFalse(self.probe.exists())

    def test_unsafe_probe_symlink_stops_before_maintenance_or_database_work(self):
        outside = self.root/'untouched';outside.write_text('preserve')
        self.probe.symlink_to(outside)
        with self.assertRaisesRegex(ValueError,'Unsafe deployment maintenance'):self.deploy()
        self.assertEqual('preserve',outside.read_text())
        self.assertFalse(self.marker.exists())
        self.assertEqual([],self.events)

    def test_marker_replaced_by_operator_is_preserved(self):
        def replace(token):
            report = self.check(token)
            other = self.config/'.operator-maintenance'
            other.write_text('keep closed');other.chmod(0o640)
            os.replace(other,self.marker)
            return report
        report = self.deploy(check=replace)
        self.assertEqual('keep closed',self.marker.read_text())
        self.assertTrue(any('manual maintenance preserved' in line for line in report))


if __name__ == '__main__':
    unittest.main()
