"""Disposable filesystem tests; no SSH, web requests or real releases touched."""
import contextlib
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


class RetentionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.releases = self.root/'releases'
        self.archived = self.root/'archived-releases'
        self.stages = self.root/'staging'
        for folder in (self.releases, self.archived, self.stages):
            folder.mkdir()
        self.old = self.make_release('a')
        self.current = self.make_release('b')
        self.incoming = self.make_release('c')
        self.link = self.root/'rehearsal'
        self.link.symlink_to(self.current, target_is_directory=True)
        self.report = self.root/'switch.txt'

    def make_release(self, letter, root=None):
        directory = (root or self.releases)/(letter*40)
        directory.mkdir()
        identity = {'commit':directory.name, 'purpose':'private-rehearsal'}
        (directory/'release.json').write_text(json.dumps(identity))
        stage = self.stages/('release-'+directory.name)
        stage.mkdir(exist_ok=True)
        (stage/'release-manifest.json').write_text(json.dumps(identity))
        (stage/(directory.name+'.tar.gz')).write_bytes(b'fixture bundle')
        (stage/'deployment-report.txt').write_text('keep audit report')
        return directory

    def prune(self):
        return deployment.prune_releases(self.releases, self.archived, self.stages,
                                         {self.current.name, self.incoming.name})

    def test_removes_old_releases_and_bundles_but_preserves_shared_targets_and_reports(self):
        archived = self.make_release('d', self.archived)
        shared = self.root/'shared';shared.mkdir()
        for name in ('runtime', 'upload', 'assets', 'backups', 'config'):
            target = shared/name;target.mkdir();(target/'sentinel').write_text('preserve')
            (self.old/name).symlink_to(target, target_is_directory=True)
        self.assertEqual((2, 2), self.prune())
        self.assertEqual({self.current.name, self.incoming.name}, {p.name for p in self.releases.iterdir()})
        self.assertFalse(archived.exists())
        for name in ('runtime', 'upload', 'assets', 'backups', 'config'):
            self.assertEqual('preserve', (shared/name/'sentinel').read_text())
        for directory in (self.old, archived):
            stage = self.stages/('release-'+directory.name)
            self.assertTrue((stage/'deployment-report.txt').exists())
            self.assertFalse((stage/(directory.name+'.tar.gz')).exists())
        for directory in (self.current, self.incoming):
            self.assertTrue((self.stages/('release-'+directory.name)/(directory.name+'.tar.gz')).exists())

    def test_removes_duplicate_archived_copy_of_retained_release(self):
        duplicate = self.make_release('b', self.archived)
        self.prune()
        self.assertFalse(duplicate.exists())
        self.assertTrue(self.current.exists())

    def test_handles_abbreviated_historical_bundle_directory(self):
        source = self.stages/('release-'+self.old.name)
        abbreviated = self.stages/'release-aaaaaaa';source.rename(abbreviated)
        self.prune()
        self.assertFalse((abbreviated/(self.old.name+'.tar.gz')).exists())
        self.assertTrue((abbreviated/'release-manifest.json').exists())

    def test_malformed_identity_aborts_before_any_deletion(self):
        invalid = self.make_release('d', self.archived)
        (invalid/'release.json').write_text(json.dumps({'commit':'wrong'}))
        with self.assertRaises(ValueError):self.prune()
        self.assertTrue(self.old.exists())
        self.assertTrue(invalid.exists())

    def test_unrecognized_directory_is_not_deleted(self):
        (self.releases/'manual-backup').mkdir()
        with self.assertRaises(ValueError):self.prune()
        self.assertTrue(self.old.exists())

    def test_malformed_artifact_metadata_aborts_before_any_deletion(self):
        manifest = self.stages/('release-'+self.old.name)/'release-manifest.json'
        manifest.write_text('[]')
        with self.assertRaises(ValueError):self.prune()
        self.assertTrue(self.old.exists())

    def test_symlink_instead_of_release_aborts_before_any_deletion(self):
        (self.releases/('d'*40)).symlink_to(self.root/'shared', target_is_directory=True)
        with self.assertRaises(ValueError):self.prune()
        self.assertTrue(self.old.exists())

    def test_artifact_symlink_is_rejected_without_deleting_target(self):
        bundle = self.stages/('release-'+self.old.name)/(self.old.name+'.tar.gz')
        bundle.unlink();outside=self.root/'backup.dump';outside.write_bytes(b'preserve')
        bundle.symlink_to(outside)
        with self.assertRaises(ValueError):self.prune()
        self.assertTrue(self.old.exists())
        self.assertEqual(b'preserve', outside.read_bytes())

    def test_other_live_pointer_protects_old_release(self):
        (self.root/'current').symlink_to(self.old, target_is_directory=True)
        with self.assertRaises(ValueError):self.prune()
        self.assertTrue(self.old.exists())

    def test_failed_health_check_restores_link_and_never_prunes(self):
        def fail():
            self.assertEqual(self.incoming, self.link.resolve())
            raise RuntimeError('simulated failed HTTP check')
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(RuntimeError):
                deployment.activate_release(self.incoming, self.link, self.current, fail, self.stages)
        self.assertEqual(self.current, self.link.resolve())
        self.assertTrue(self.old.exists())
        self.assertFalse((self.root/'previous').is_symlink())

    def test_success_sets_rollback_pointer_then_prunes(self):
        def healthy():
            self.assertTrue(self.old.exists())
            self.assertEqual(self.incoming, self.link.resolve())
            return ['HTTP checks passed']
        report = deployment.activate_release(self.incoming, self.link, self.current, healthy, self.stages)
        self.assertEqual(self.incoming, self.link.resolve())
        self.assertEqual(self.current, (self.root/'previous').resolve())
        self.assertFalse(self.old.exists())
        self.assertIn('KAARDID_REHEARSAL_SWITCH_COMPLETE', report)
        rollback = deployment.rollback_for_deploy(self.incoming, self.incoming,
                                                  self.root/'previous', self.report)
        deployment.activate_release(self.incoming, self.link, rollback, lambda:[], self.stages)
        self.assertEqual(self.current, (self.root/'previous').resolve())
        self.assertEqual(2, len(list(self.releases.iterdir())))

    def test_cleanup_failure_keeps_healthy_release_active(self):
        with patch.object(deployment, 'prune_releases', side_effect=OSError('simulated permission error')):
            with contextlib.redirect_stderr(io.StringIO()):
                report = deployment.activate_release(self.incoming, self.link, self.current, lambda:[], self.stages)
        self.assertEqual(self.incoming, self.link.resolve())
        self.assertEqual(self.current, (self.root/'previous').resolve())
        self.assertTrue(self.old.exists())
        self.assertTrue(any('Retention cleanup warning:' in line for line in report))

    def test_repeat_deploy_preserves_existing_rollback(self):
        pointer = self.root/'previous';pointer.symlink_to(self.old, target_is_directory=True)
        rollback = deployment.rollback_for_deploy(self.current, self.current, pointer, self.report)
        self.assertEqual(self.old, rollback)

    def test_first_repeat_deploy_reads_historical_report(self):
        self.report.write_text('Previous release retained: '+str(self.old)+'\n')
        rollback = deployment.rollback_for_deploy(self.current, self.current, self.root/'previous', self.report)
        self.assertEqual(self.old, rollback)

    def test_repeat_with_no_known_rollback_fails_safely(self):
        with self.assertRaises(ValueError):
            deployment.rollback_for_deploy(self.current, self.current, self.root/'previous', self.report)
        self.assertTrue(self.old.exists())


if __name__ == '__main__':
    unittest.main()
