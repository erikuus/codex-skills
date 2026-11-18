"""Exercise backup deletion and recovery protection using disposable snapshots."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('deployment', Path(__file__).with_name('deploy-rehearsal.py'))
deployment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment)


class BackupRetentionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.backups = self.root/'rehearsal-backups';self.backups.mkdir(mode=0o700)
        self.snapshots = [self.snapshot(day) for day in range(1, 7)]
        self.current = self.snapshots[-1]/'kaart.dump'
        self.status(self.snapshots[-1], 'pending')

    def snapshot(self, day, status='succeeded', *, database='kaart'):
        snapshot = self.backups/f'202610{day:02}T120000Z-{"a"*12}-fixture_'
        snapshot.mkdir(mode=0o700)
        dump = snapshot/(database+'.dump');dump.write_bytes(b'fixture dump');dump.chmod(0o600)
        metadata = snapshot/'backup.json'
        metadata.write_text(json.dumps({'database':database,'target_commit':'a'*40,
            'sha256':hashlib.sha256(b'fixture dump').hexdigest(),'deployment_status':status}))
        metadata.chmod(0o600)
        (snapshot/'migration-apply.txt').write_text('fixture diagnostic')
        return snapshot

    def status(self, snapshot, status):
        metadata = snapshot/'backup.json';data = json.loads(metadata.read_text())
        if status is None:data.pop('deployment_status')
        else:data['deployment_status'] = status
        metadata.write_text(json.dumps(data))

    def prune(self):
        return deployment.prune_backups(self.backups, self.current)

    def test_keeps_newest_three_successful_backups_and_removes_old_diagnostics(self):
        self.assertEqual((3, 0),self.prune())
        self.assertEqual(self.snapshots[-3:],sorted(self.backups.iterdir()))
        self.assertEqual('succeeded',json.loads((self.current.parent/'backup.json').read_text())['deployment_status'])
        self.assertEqual(0o600,(self.current.parent/'backup.json').stat().st_mode & 0o777)
        self.assertEqual((0, 0),self.prune())

    def test_failed_interrupted_and_legacy_attempts_are_extra_protected_backups(self):
        self.status(self.snapshots[0],'pending')
        self.status(self.snapshots[1],'failed')
        self.status(self.snapshots[2],None)
        partial = self.backups/'20261007T120000Z-aaaaaaaaaaaa-partial_'
        partial.mkdir(mode=0o700);(partial/'kaart.dump.partial').write_bytes(b'incomplete')
        self.assertEqual((0, 4),self.prune())
        self.assertTrue(all(p.exists() for p in self.snapshots))

    def test_explicit_resolution_makes_old_failed_backup_eligible_again(self):
        self.status(self.snapshots[0],'pending')
        self.assertEqual((2, 1),self.prune())
        self.assertTrue(self.snapshots[0].exists())
        self.status(self.snapshots[0],'resolved')
        self.assertEqual((1, 0),self.prune())
        self.assertFalse(self.snapshots[0].exists())

    def test_uses_snapshot_time_instead_of_file_modification_time(self):
        import os
        os.utime(self.snapshots[0],(2000000000,2000000000))
        self.prune()
        self.assertFalse(self.snapshots[0].exists())

    def test_corrupt_old_dump_prevents_all_deletions(self):
        (self.snapshots[1]/'kaart.dump').write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):self.prune()
        self.assertTrue(all(p.exists() for p in self.snapshots))

    def test_production_cleanup_keeps_three_and_leaves_pending_and_rehearsal_alone(self):
        rehearsal = self.backups
        self.backups = self.root/'production-backups'
        self.backups.mkdir(mode=0o700)
        pending = self.snapshot(1, 'pending', database='kaart_prod')
        production = [self.snapshot(day, database='kaart_prod') for day in range(2, 7)]
        (production[-1]/'kaart_prod.dump').write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):
            deployment.prune_backups(self.backups, target='production')
        self.assertEqual([pending, *production], sorted(self.backups.iterdir()))
        (production[-1]/'kaart_prod.dump').write_bytes(b'fixture dump')
        self.assertEqual((2, 1), deployment.prune_backups(self.backups, target='production'))
        self.assertEqual([pending, *production[-3:]], sorted(self.backups.iterdir()))
        self.assertEqual(self.snapshots, sorted(rehearsal.iterdir()))

    def test_production_or_mismatched_snapshot_identity_prevents_deletion(self):
        metadata = self.snapshots[0]/'backup.json'
        data = json.loads(metadata.read_text());data['database'] = 'kaart_prod'
        metadata.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'Unexpected backup identity'):self.prune()
        self.assertTrue(all(p.exists() for p in self.snapshots))

    def test_dump_symlink_is_never_followed_or_deleted(self):
        outside = self.root/'outside';outside.write_bytes(b'preserve')
        dump = self.snapshots[0]/'kaart.dump';dump.unlink();dump.symlink_to(outside)
        with self.assertRaisesRegex(ValueError,'Unsafe backup path'):self.prune()
        self.assertEqual(b'preserve',outside.read_bytes())
        self.assertTrue(all(p.exists() for p in self.snapshots))

    def test_root_symlink_or_public_permissions_are_rejected(self):
        alias = self.root/'alias';alias.symlink_to(self.backups,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'Unsafe backup path'):
            deployment.prune_backups(alias,alias/self.current.parent.name/'kaart.dump')
        self.backups.chmod(0o755)
        with self.assertRaisesRegex(ValueError,'Unsafe backup path'):self.prune()


if __name__ == '__main__':
    unittest.main()
