"""Production promotion and recovery against disposable files and fake services."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('promotion',Path(__file__).with_name('promote-production.py'))
promotion=importlib.util.module_from_spec(spec)
spec.loader.exec_module(promotion)
deployment=promotion.deployment
spec=importlib.util.spec_from_file_location('preview',Path(__file__).with_name('production-preview.py'))
preview=importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class ProductionPromotionTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()
        self.rehearsal=self.root/'rehearsal-root'
        self.production=self.root/'production-root'
        self.stages=self.root/'stages';self.stages.mkdir(mode=0o700)
        self.sha='c'*40
        for root in (self.rehearsal,self.production):
            (root/'releases').mkdir(parents=True)
            for name in ('runtime','config','assets','upload'):
                (root/'shared'/name).mkdir(parents=True)
                (root/'shared'/name/'sentinel').write_text(root.name)
        build=self.root/'build'/self.sha
        app=build/'apps/kaardid'
        for name in promotion.SHARED:
            (app/name).mkdir(parents=True,exist_ok=True)
        (app/'index.php').write_text('<?php /* exact shipped bytes */')
        (app/'protected/migrations').mkdir()
        (app/'protected/migrations/m261030_120000_feature.php').write_text('<?php /* migration */')
        (build/'yii').mkdir();(build/'yii/framework.php').write_text('<?php /* pinned framework */')
        self.manifest={'commit':self.sha,'purpose':'private-rehearsal','yii_content_sha256':'fixture'}
        (build/'release.json').write_text(json.dumps(self.manifest))
        self.source=self.stages/('release-'+self.sha);self.source.mkdir()
        self.archive=self.source/(self.sha+'.tar.gz')
        with tarfile.open(self.archive,'w:gz') as bundle:bundle.add(build,arcname=self.sha)
        self.manifest['artifact_sha256']=promotion.digest(self.archive)
        (self.source/'release-manifest.json').write_text(json.dumps(self.manifest))
        (self.source/'deployment-report.txt').write_text('Active release: '+self.sha+'\nKAARDID_REHEARSAL_SWITCH_COMPLETE\n')
        with tarfile.open(self.archive) as bundle:bundle.extractall(self.rehearsal/'releases',filter='data')
        self.tested=self.rehearsal/'releases'/self.sha
        for name,target in promotion.SHARED.items():
            path=self.tested/'apps/kaardid'/name;path.rmdir()
            path.symlink_to(self.rehearsal/'shared'/target)
        (self.rehearsal/'rehearsal').symlink_to(self.tested)

    def prepare(self):
        with patch.object(deployment,'health_check',return_value=['fresh rehearsal healthy']) as health:
            result=promotion.prepare(self.rehearsal,self.production,self.stages,self.sha,os.getegid())
        health.assert_called_once_with()
        return result

    def test_prepare_copies_exact_archive_and_only_relinks_environment_data(self):
        with patch.object(deployment,'backup_and_migrate') as backup, patch.object(deployment,'deploy_locked') as activate:
            release,stage,plan=self.prepare()
        backup.assert_not_called();activate.assert_not_called()
        self.assertFalse((self.production/'current').exists())
        self.assertFalse((self.production/'shared/config/.maintenance').exists())
        self.assertEqual(self.manifest['artifact_sha256'],promotion.digest(stage/self.archive.name))
        self.assertEqual((self.tested/'release.json').read_bytes(),(release/'release.json').read_bytes())
        self.assertEqual((self.tested/'apps/kaardid/index.php').read_bytes(),(release/'apps/kaardid/index.php').read_bytes())
        self.assertIsNone(plan['expected_current']);self.assertFalse(plan['activated'])
        for name,target in promotion.SHARED.items():
            self.assertEqual(str(self.production/'shared'/target),os.readlink(release/'apps/kaardid'/name))
            self.assertEqual(self.rehearsal.name,(self.rehearsal/'shared'/target/'sentinel').read_text())
            self.assertEqual(self.production.name,(self.production/'shared'/target/'sentinel').read_text())

    def test_prepare_is_repeatable_without_rebuilding_dependencies(self):
        first,_,_=self.prepare()
        original=(first/'apps/kaardid/index.php').stat().st_ino
        second,_,_=self.prepare()
        self.assertEqual(original,(second/'apps/kaardid/index.php').stat().st_ino)

    def test_preview_prepares_in_child_while_parent_keeps_both_real_locks(self):
        tooling=self.root/'tooling';tooling.mkdir()
        for name in ('promote-production.py','deploy-rehearsal.py'):
            (tooling/name).write_bytes((Path(__file__).parent/name).read_bytes())
        # Exercise the real artifact preparation in another process. Only the
        # unrelated live HTTP probe is replaced for this filesystem fixture.
        with (tooling/'promote-production.py').open('a') as script:
            script.write('''
deployment.health_check=lambda: []
original_prepare=prepare
def prepare(rehearsal,production,*args):
    for root in (rehearsal,production):
        with (root/'shared/runtime/operations.lock').open('rb') as lock:
            try:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:
                pass
            else:
                raise AssertionError('Parent must retain both locks during preparation.')
    return original_prepare(rehearsal,production,*args)
''')
        with deployment.operation_lock(self.rehearsal/'shared/runtime'):
            with deployment.operation_lock(self.production/'shared/runtime'):
                preview.prepare_locked_release(tooling,self.rehearsal,self.production,self.stages,
                                               self.sha,os.getegid(),[])
                # Child exit must not release the parent's locks.
                with self.assertRaisesRegex(RuntimeError,'Updater or deployment is running'):
                    with deployment.operation_lock(self.rehearsal/'shared/runtime'): pass
                with self.assertRaisesRegex(RuntimeError,'Updater or deployment is running'):
                    with deployment.operation_lock(self.production/'shared/runtime'): pass
        self.assertTrue((self.production/'releases'/self.sha/'release.json').is_file())
        self.assertFalse((self.production/'current').exists())
        with deployment.operation_lock(self.rehearsal/'shared/runtime'): pass
        with deployment.operation_lock(self.production/'shared/runtime'): pass

    def test_rejects_wrong_sha_before_staging(self):
        with self.assertRaisesRegex(ValueError,'not the active tested'):
            promotion.prepare(self.rehearsal,self.production,self.stages,'b'*40,os.getegid())
        self.assertEqual([],list((self.production/'releases').iterdir()))

    def test_rejects_corrupt_archive_or_modified_tested_code(self):
        (self.tested/'apps/kaardid/index.php').write_text('changed after testing')
        with self.assertRaisesRegex(ValueError,'bytes differ'):self.prepare()
        self.assertEqual([],list((self.production/'releases').iterdir()))

    def test_rejects_extra_code_or_shared_link_to_wrong_environment(self):
        extra=self.tested/'unexpected.php';extra.write_text('extra')
        with self.assertRaisesRegex(ValueError,'additional files'):self.prepare()
        extra.unlink()
        path=self.tested/'apps/kaardid/protected/config/private';path.unlink()
        path.symlink_to(self.production/'shared/config')
        with self.assertRaisesRegex(ValueError,'shared-data link'):self.prepare()

    def test_maintenance_or_missing_success_receipt_prevents_promotion(self):
        marker=self.rehearsal/'shared/config/.maintenance';marker.touch()
        with self.assertRaisesRegex(ValueError,'in maintenance'):self.prepare()
        marker.unlink();(self.source/'deployment-report.txt').write_text('failed')
        with self.assertRaisesRegex(ValueError,'evidence is missing'):self.prepare()

    def test_live_rehearsal_failure_does_not_prepare_candidate(self):
        with patch.object(deployment,'health_check',side_effect=RuntimeError('rehearsal unhealthy')):
            with self.assertRaisesRegex(RuntimeError,'unhealthy'):
                promotion.prepare(self.rehearsal,self.production,self.stages,self.sha,os.getegid())
        self.assertEqual([],list((self.production/'releases').iterdir()))

    def test_changed_prepared_code_is_not_overwritten_or_activated(self):
        release,_,_=self.prepare()
        (release/'apps/kaardid/index.php').write_text('tampered')
        with self.assertRaisesRegex(ValueError,'bytes differ'):self.prepare()

    def test_existing_plan_symlink_is_rejected_without_touching_its_target(self):
        _,stage,_=self.prepare()
        outside=self.root/'untouched';outside.write_text('preserve')
        plan=stage/'promotion-plan.json';plan.unlink();plan.symlink_to(outside)
        with self.assertRaisesRegex(ValueError,'Unsafe deployment path'):self.prepare()
        self.assertEqual('preserve',outside.read_text())

    def test_missing_readiness_identifies_the_file_before_deploying(self):
        release,stage,_ = self.prepare()
        readiness = self.root/'missing-readiness.json'
        with patch.object(deployment,'deploy_locked') as deploy:
            with self.assertRaisesRegex(promotion.ReadinessError, 'confirmation is missing:') as error:
                promotion.activate(release,self.production,stage,readiness,self.root/'missing-nginx',self.root/'missing-db')
        self.assertIn(str(readiness),str(error.exception))
        deploy.assert_not_called()

    def test_unconfirmed_readiness_blocks_before_database_or_config_loading(self):
        release,stage,_=self.prepare()
        readiness=self.root/'readiness.json'
        readiness.write_text(json.dumps(dict(release=self.sha,**{k:False for k in promotion.READINESS})))
        readiness.chmod(0o600)
        with patch.object(deployment,'backup_and_migrate') as backup, patch.object(promotion.subprocess,'run') as run:
            with self.assertRaisesRegex(ValueError,'readiness is incomplete'):
                promotion.activate(release,self.production,stage,readiness,self.root/'missing-nginx',self.root/'missing-db')
        backup.assert_not_called();run.assert_not_called()
        self.assertFalse((self.production/'shared/config/.maintenance').exists())

    def test_restricted_evidence_does_not_satisfy_the_normal_activation_gate(self):
        release,stage,_=self.prepare()
        readiness=self.root/'readiness.json'
        readiness.write_text(json.dumps(dict(release=self.sha,**{key:True for key in promotion.RESTRICTED_READINESS})))
        readiness.chmod(0o600)
        site=self.root/'missing-nginx'
        with self.assertRaisesRegex(ValueError,'readiness is incomplete'):
            promotion.activation_preflight(release,self.production,stage,readiness,site)
        with self.assertRaises(FileNotFoundError):
            promotion.activation_preflight(release,self.production,stage,readiness,site,restricted=True)
        (self.production/'current').symlink_to(release)
        with self.assertRaisesRegex(ValueError,'before the first production release'):
            promotion.activation_preflight(release,self.production,stage,readiness,site,restricted=True)

    def test_restricted_preflight_checks_backend_digest_and_uninstalled_updater(self):
        release,stage,_=self.prepare()
        site=self.root/'sites-available'/'kaardid-production'
        site.parent.mkdir()
        enabled=self.root/'sites-enabled';enabled.mkdir()
        (enabled/site.name).symlink_to(site)
        site.write_text((Path(__file__).with_name('nginx')/'kaardid-production.conf').read_text())
        readiness=self.root/'readiness.json'
        confirmation=dict(release=self.sha,**{key:True for key in promotion.RESTRICTED_READINESS})
        readiness.write_text(json.dumps(confirmation));readiness.chmod(0o600)
        real_lstat=Path.lstat
        def lstat(path):
            info=real_lstat(path)
            return SimpleNamespace(st_mode=info.st_mode,st_uid=0) if path==site else info
        with patch.object(Path,'lstat',lstat), patch.object(promotion.subprocess,'run') as run, \
             patch.object(promotion.subprocess,'check_output',return_value='loaded\n') as systemctl:
            with self.assertRaisesRegex(ValueError,'differs from the reviewed'):
                promotion.activation_preflight(release,self.production,stage,readiness,site,restricted=True)
            systemctl.assert_not_called()
            confirmation['backendConfigSha256']=hashlib.sha256(site.read_bytes()).hexdigest()
            readiness.write_text(json.dumps(confirmation))
            with self.assertRaisesRegex(ValueError,'Keep the updater'):
                promotion.activation_preflight(release,self.production,stage,readiness,site,restricted=True)
            run.assert_not_called()

    def test_vpn_preview_blocks_cutover_before_readiness_or_database_access(self):
        release,stage,_=self.prepare()
        (self.production/'preview').symlink_to(release)
        with patch.object(deployment,'backup_and_migrate') as backup:
            with self.assertRaisesRegex(ValueError,'Remove the VPN test-data preview'):
                promotion.activation_preflight(release,self.production,stage,None,None)
        backup.assert_not_called()

    def test_stale_prepared_current_guard_stops_before_configuration_or_backup(self):
        release,stage,_=self.prepare()
        (self.production/'current').symlink_to(release)
        with self.assertRaisesRegex(ValueError,'changed since preparation'):
            promotion.activation_preflight(release,self.production,stage,None,self.root/'missing-nginx')

    def test_routine_activation_checks_backend_and_configuration_without_readiness_file(self):
        current = self.production/'releases'/('a'*40)
        current.mkdir()
        (self.production/'current').symlink_to(current)
        release,stage,_ = self.prepare()
        site = self.root/'sites-available'/'kaardid-production'
        site.parent.mkdir()
        enabled = self.root/'sites-enabled'
        enabled.mkdir()
        (enabled/site.name).symlink_to(site)
        site.write_text((Path(__file__).with_name('nginx')/'kaardid-production.conf').read_text())
        real_lstat = Path.lstat

        def lstat(path):
            info = real_lstat(path)
            return SimpleNamespace(st_mode=info.st_mode, st_uid=0) if path==site else info

        with patch.object(Path,'lstat',lstat), patch.object(promotion.subprocess,'run') as run:
            run.return_value.returncode = 0
            self.assertEqual(current, promotion.activation_preflight(
                release, production=self.production, stage=stage,
                readiness=self.root/'missing-readiness.json', site=site))
            run.assert_called_once()
            run.return_value.returncode = 1
            with self.assertRaisesRegex(ValueError,'configuration preflight failed'):
                promotion.activation_preflight(release,self.production,stage,None,site)
            site.write_text('unmanaged')
            with self.assertRaisesRegex(ValueError,'Reviewed production nginx backend'):
                promotion.activation_preflight(release,self.production,stage,None,site)

    def test_archive_path_traversal_symlinks_and_duplicate_files_are_rejected(self):
        for name,kind in [(self.sha+'/../outside',tarfile.REGTYPE),
                          (self.sha+'/escape',tarfile.SYMTYPE),('/absolute',tarfile.REGTYPE)]:
            archive=self.root/'unsafe.tar'
            with tarfile.open(archive,'w') as bundle:
                entry=tarfile.TarInfo(name);entry.type=kind;entry.linkname='/tmp'
                bundle.addfile(entry)
            with tarfile.open(archive) as bundle:
                with self.assertRaisesRegex(ValueError,'Unsafe'):promotion.archive_entries(bundle,self.sha)
        with tarfile.open(archive,'w') as bundle:
            for _ in range(2):bundle.addfile(tarfile.TarInfo(self.sha+'/duplicate'))
        with tarfile.open(archive) as bundle:
            with self.assertRaisesRegex(ValueError,'duplicate'):promotion.archive_entries(bundle,self.sha)


class ProductionLifecycleTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()
        self.stages=self.root/'stages';self.stages.mkdir()
        self.stage=self.stages/('production-'+'c'*40);self.stage.mkdir()
        self.production=self.root/'production'
        self.config=self.production/'shared/config';self.config.mkdir(parents=True)
        self.runtime=self.production/'shared/runtime';self.runtime.mkdir()
        self.marker=self.config/'.maintenance'
        self.probe=self.config/'.deployment-probe.json'
        self.link=self.production/'current'
        self.releases=[]
        for letter in 'abc':
            path=self.production/'releases'/(letter*40)
            (path/'apps/kaardid').mkdir(parents=True)
            (path/'release.json').write_text(json.dumps({'commit':path.name,'purpose':'private-rehearsal'}))
            self.releases.append(path)
        self.obsolete,self.old,self.incoming=self.releases
        self.link.symlink_to(self.old)
        (self.production/'previous').symlink_to(self.obsolete)
        self.events=[]

    def backup(self, app, stage, backups, credentials, *, target):
        self.assertEqual('production',target)
        self.assertEqual(self.stages/'production-backups',backups)
        if self.link.is_symlink():
            self.assertEqual(self.old,self.link.resolve())
        else:
            self.assertFalse(self.link.exists())
        self.assertTrue(self.marker.exists())
        with self.assertRaisesRegex(RuntimeError,'Updater or deployment'):
            with deployment.operation_lock(self.runtime):self.fail('unlocked')
        self.events.append('backup+migrations')
        backups.mkdir(mode=0o700, exist_ok=True)
        snapshot=backups/('20261116T120000Z-'+self.incoming.name[:12]+'-fixture_')
        snapshot.mkdir(mode=0o700)
        backup=snapshot/'kaart_prod.dump'
        backup.write_bytes(b'pre-migration production backup')
        backup.chmod(0o600)
        metadata=snapshot/'backup.json'
        metadata.write_text(json.dumps({'database':'kaart_prod','target_commit':self.incoming.name,
            'sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'deployment_status':'pending'}))
        metadata.chmod(0o600)
        return backup

    def fetch(self,path,token=None,*,target):
        self.assertEqual('production',target)
        self.events.append('visitor')
        return (503 if self.marker.exists() else 200),b'',''

    def health(self,token=None,*,target):
        self.assertEqual('production',target)
        self.assertEqual(self.incoming,self.link.resolve())
        self.assertEqual(bool(token),self.marker.exists())
        if token:self.assertEqual(token,json.loads(self.probe.read_text())['token'])
        self.events.append('private-health' if token else 'public-health')
        with self.assertRaisesRegex(RuntimeError,'Updater or deployment'):
            with deployment.operation_lock(self.runtime):self.fail('unlocked')
        return ['healthy']

    def run_deploy(self,backup=None,health=None,rollback=True,reopen_after_cutover=False):
        with patch.object(deployment,'backup_and_migrate',side_effect=backup or self.backup), \
             patch.object(deployment,'fetch',side_effect=self.fetch), \
             patch.object(deployment,'health_check',side_effect=health or self.health), \
             contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            with deployment.operation_lock(self.runtime):
                return deployment.deploy_locked(self.incoming,self.link,self.old if rollback else None,
                    self.stage,self.root/'prod-db.json',target='production',reopen_after_cutover=reopen_after_cutover)

    def test_success_uses_production_db_checks_and_shared_backup_retention(self):
        # A rehearsal artifact must survive production cleanup even if its SHA
        # differs from both production pointers.
        rehearsal=self.stages/('release-'+'d'*40);rehearsal.mkdir()
        (rehearsal/'release-manifest.json').write_text(json.dumps({'commit':'d'*40,'purpose':'private-rehearsal'}))
        artifact=rehearsal/('d'*40+'.tar.gz');artifact.write_bytes(b'preserve')
        report=self.run_deploy()
        self.assertTrue(artifact.exists());self.assertFalse(self.obsolete.exists())
        self.assertEqual(['visitor','backup+migrations','private-health','visitor','public-health'],self.events)
        self.assertEqual(self.old,(self.production/'previous').resolve())
        self.assertFalse(self.marker.exists());self.assertFalse(self.probe.exists())
        self.assertIn('KAARDID_PRODUCTION_SWITCH_COMPLETE',report)
        self.assertTrue(any(line.startswith('Backup cleanup: removed 0') for line in report))
        metadata, = (self.stages/'production-backups').glob('*/backup.json')
        self.assertEqual('succeeded',json.loads(metadata.read_text())['deployment_status'])

    def test_busy_updater_stops_before_maintenance_backup_and_migrations(self):
        with deployment.operation_lock(self.runtime):
            with self.assertRaisesRegex(RuntimeError,'no deployment work'):self.run_deploy()
        self.assertEqual([],self.events);self.assertFalse(self.marker.exists())

    def rollback(self,health=None):
        def healthy(token=None,*,target):
            self.assertEqual(self.obsolete,self.link.resolve())
            self.assertEqual(bool(token),self.marker.exists())
            with self.assertRaisesRegex(RuntimeError,'Updater or deployment'):
                with deployment.operation_lock(self.runtime): pass
            return ['healthy']
        with patch.object(deployment,'fetch',side_effect=self.fetch), \
             patch.object(deployment,'health_check',side_effect=health or healthy), \
             patch.object(deployment,'backup_and_migrate') as database, \
             contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            report=promotion.rollback_code(self.obsolete,self.production,self.stage)
        database.assert_not_called()
        return report

    def test_manual_rollback_switches_retained_code_without_database_work(self):
        report=self.rollback()
        self.assertEqual(self.obsolete,self.link.resolve())
        self.assertEqual(self.old,(self.production/'previous').resolve())
        self.assertFalse(self.marker.exists());self.assertFalse(self.probe.exists())
        self.assertIn('Manual code rollback complete; database and migrations unchanged.',report)

    def test_manual_rollback_health_failure_restores_original_code_and_stays_closed(self):
        def fail(*args,**kwargs): raise RuntimeError('old code incompatible')
        with self.assertRaisesRegex(RuntimeError,'incompatible'): self.rollback(fail)
        self.assertEqual(self.old,self.link.resolve())
        self.assertTrue(self.marker.exists());self.assertFalse(self.probe.exists())

    def test_manual_rollback_preserves_existing_maintenance(self):
        self.marker.touch(mode=0o640)
        self.rollback()
        self.assertTrue(self.marker.exists());self.assertFalse(self.probe.exists())

    def test_manual_rollback_public_check_failure_recloses_before_restoring_code(self):
        def fail_public(token=None,*,target):
            if token: return ['private healthy']
            raise RuntimeError('public health failed')
        with self.assertRaisesRegex(RuntimeError,'public health failed'): self.rollback(fail_public)
        self.assertEqual(self.old,self.link.resolve())
        self.assertTrue(self.marker.exists());self.assertFalse(self.probe.exists())

    def test_manual_rollback_rejects_busy_lock_wrong_release_and_preview(self):
        with deployment.operation_lock(self.runtime):
            with self.assertRaisesRegex(RuntimeError,'Updater or deployment'): self.rollback()
        with self.assertRaisesRegex(ValueError,'retained previous'):
            promotion.rollback_code(self.incoming,self.production,self.stage)
        (self.production/'preview').symlink_to(self.incoming)
        with self.assertRaisesRegex(ValueError,'VPN preview'): self.rollback()
        self.assertFalse(self.marker.exists())

    def test_migration_failure_leaves_old_code_closed_and_backup_pending(self):
        def fail(*args,**kwargs):self.backup(*args,**kwargs);raise RuntimeError('migration failed')
        with self.assertRaisesRegex(RuntimeError,'migration failed'):self.run_deploy(backup=fail)
        self.assertEqual(self.old,self.link.resolve());self.assertTrue(self.marker.exists())
        self.assertTrue(self.obsolete.exists());self.assertFalse(self.probe.exists())
        metadata, = (self.stages/'production-backups').glob('*/backup.json')
        self.assertEqual('pending',json.loads(metadata.read_text())['deployment_status'])

    def test_private_or_public_health_failure_rolls_back_only_code_and_preserves_backup(self):
        for phase in ('private-health','public-health'):
            with self.subTest(phase=phase):
                def fail(token=None,*,target):
                    result=self.health(token,target=target)
                    if self.events[-1]==phase:raise RuntimeError('health failed')
                    return result
                with self.assertRaisesRegex(RuntimeError,'health failed'):self.run_deploy(health=fail)
                self.assertEqual(self.old,self.link.resolve());self.assertTrue(self.marker.exists())
                self.assertTrue(self.obsolete.exists());self.assertFalse(self.probe.exists())
                backup=self.stages/'production-backups'/('20261116T120000Z-'+self.incoming.name[:12]+'-fixture_')
                self.assertTrue((backup/'kaart_prod.dump').exists())
                self.assertEqual('pending',json.loads((backup/'backup.json').read_text())['deployment_status'])
                self.marker.unlink();(backup/'kaart_prod.dump').unlink();(backup/'backup.json').unlink();backup.rmdir()

    def test_first_activation_failure_unlinks_candidate_and_stays_closed(self):
        self.link.unlink();(self.production/'previous').unlink()
        def backup(app,stage,backups,credentials,*,target):
            self.assertFalse(self.link.exists())
            self.events.append('backup+migrations')
            snapshot=backups/'first';snapshot.mkdir(parents=True)
            (snapshot/'backup.json').write_text('{"deployment_status":"pending"}')
            result=snapshot/'kaart_prod.dump';result.write_bytes(b'first backup');return result
        def fail(token=None,*,target):
            self.health(token,target=target)
            raise RuntimeError('first health failed')
        with self.assertRaisesRegex(RuntimeError,'first health failed'):
            self.run_deploy(backup=backup,health=fail,rollback=False)
        self.assertFalse(self.link.is_symlink());self.assertTrue(self.marker.exists())
        self.assertFalse((self.production/'previous').is_symlink());self.assertFalse(self.probe.exists())
        self.assertTrue(self.incoming.exists())

    def test_first_activation_success_has_no_invented_previous_release(self):
        self.link.unlink();(self.production/'previous').unlink()
        def backup(app,stage,backups,credentials,*,target):
            self.assertFalse(self.link.exists())
            snapshot=backups/'first';snapshot.mkdir(parents=True)
            (snapshot/'backup.json').write_text('{"deployment_status":"pending"}')
            result=snapshot/'kaart_prod.dump';result.write_bytes(b'first backup');return result
        self.run_deploy(backup=backup,rollback=False)
        self.assertEqual(self.incoming,self.link.resolve())
        self.assertFalse((self.production/'previous').is_symlink())
        self.assertFalse(self.marker.exists());self.assertFalse(self.probe.exists())
        self.assertEqual([self.incoming],list((self.production/'releases').iterdir()))

    def test_repeat_first_activation_preserves_absence_of_rollback(self):
        self.link.unlink();self.link.symlink_to(self.incoming)
        (self.production/'previous').unlink()
        (self.stage/'deployment-report.txt').write_text('Previous release retained: None\nKAARDID_PRODUCTION_SWITCH_COMPLETE\n')
        def preflight(*args, **kwargs):
            with self.assertRaisesRegex(RuntimeError,'Updater or deployment'):
                with deployment.operation_lock(self.runtime):self.fail('preflight not locked')
            return self.incoming
        with patch.object(promotion,'activation_preflight',side_effect=preflight), \
             patch.object(deployment,'deploy_locked',return_value=['KAARDID_PRODUCTION_SWITCH_COMPLETE']) as deploy:
            promotion.activate(self.incoming,self.production,self.stage,None,None,None)
        self.assertIsNone(deploy.call_args.args[2])
        self.assertEqual('production',deploy.call_args.kwargs['target'])
        self.assertEqual('succeeded',json.loads((self.stage/'activation-attempt.json').read_text())['status'])

    def test_operator_maintenance_is_preserved_after_success(self):
        self.marker.write_text('operator closed');self.marker.chmod(0o640)
        report=self.run_deploy()
        self.assertEqual('operator closed',self.marker.read_text())
        self.assertNotIn('public-health',self.events)
        self.assertTrue(any('manual maintenance preserved' in row for row in report))

    def test_restricted_activation_reopens_only_after_private_health_checks(self):
        self.link.unlink();(self.production/'previous').unlink()
        self.marker.touch(mode=0o640)
        self.run_deploy(rollback=False,reopen_after_cutover=True)
        self.assertEqual(['visitor','backup+migrations','private-health','visitor','public-health'],self.events)
        self.assertFalse(self.marker.exists())

    def test_failed_restricted_activation_keeps_cutover_maintenance(self):
        self.link.unlink();(self.production/'previous').unlink()
        self.marker.touch(mode=0o640)
        def fail(token=None, *, target):
            self.health(token,target=target)
            raise RuntimeError('health check failed')
        with self.assertRaisesRegex(RuntimeError,'health check failed'):
            self.run_deploy(health=fail,rollback=False,reopen_after_cutover=True)
        self.assertFalse(self.link.is_symlink())
        self.assertTrue(self.marker.is_file())
        self.assertFalse(self.probe.exists())


class ProductionDatabaseIdentityTest(unittest.TestCase):
    def test_rehearsal_credentials_rejected_for_production_before_pg_dump(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);credentials=root/'db.json'
            credentials.write_text(json.dumps({'host':'127.0.0.1','port':5432,'database':'kaart',
                'user':'kaart_migrate','role':'kaart_owner','password':'fixture-only'}));credentials.chmod(0o600)
            with patch.object(deployment.subprocess,'run') as run:
                with self.assertRaisesRegex(ValueError,'Unexpected production'):
                    deployment.backup_and_migrate(root/'app',root,root/'backups',credentials,target='production')
            run.assert_not_called()

    def test_probe_uses_production_port_host_and_rejects_unrelated_backend(self):
        with patch.object(deployment.http.client,'HTTPConnection') as connection:
            response=connection.return_value.getresponse.return_value
            response.status=200;response.read.return_value=b'healthy'
            response.getheader.side_effect=lambda name,default=None: {'X-Kaardid-Environment':'production','Content-Type':'text/html'}.get(name,default)
            self.assertEqual(200,deployment.fetch('/',target='production')[0])
            connection.assert_called_with('127.0.0.1',18081,timeout=30)
            connection.return_value.request.assert_called_with('GET','/',headers={'Host':'kaardid.ra.ee'})
            response.getheader.side_effect=lambda *args: None
            with self.assertRaisesRegex(RuntimeError,'unexpected nginx backend'):
                deployment.fetch('/',target='production')

    def test_production_checks_allow_analytics_but_rehearsal_rejects_it(self):
        def fetch(path,token=None,*,target='rehearsal'):
            if path=='/':return 200,b'analytics.ra.ee/js/script.js /assets/site.css','text/html'
            if path=='/assets/site.css':return 200,b'css','text/css'
            return (200 if path in ('/index.php/map/search','/index.php/map/searchAdvanced') else 404),b'','text/html'
        with patch.object(deployment,'fetch',side_effect=fetch):
            self.assertTrue(deployment.health_check(target='production'))
            with self.assertRaisesRegex(RuntimeError,'analytics must be disabled'):
                deployment.health_check()


if __name__=='__main__':unittest.main()
