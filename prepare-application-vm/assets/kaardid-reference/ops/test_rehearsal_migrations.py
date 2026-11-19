"""Backup/migration failure gates; optional real PostgreSQL/Yii integration test."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('deployment', Path(__file__).with_name('deploy-rehearsal.py'))
deployment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment)


class MigrationBackupTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.app = self.root/'releases'/('c'*40)/'apps/kaardid'
        self.app.mkdir(parents=True)
        self.stage = self.root/'stage';self.stage.mkdir()
        self.backups = self.root/'backups'
        self.credentials = self.root/'db.json'
        self.credentials.write_text(json.dumps({'host':'127.0.0.1','port':5432,'database':'kaart',
            'user':'kaart_migrate','role':'kaart_owner','password':'fixture:pass\\word'}))
        self.credentials.chmod(0o600)
        self.calls = []
        self.previews = 0

    def command(self, args, **kwargs):
        self.calls.append(args)
        if args[0] == 'pg_dump':
            self.assertNotIn('PGPASSWORD', kwargs['env'])
            self.assertNotIn('PGOPTIONS', kwargs['env'])
            passfile = Path(kwargs['env']['PGPASSFILE'])
            self.assertEqual(0o600, passfile.stat().st_mode & 0o777)
            self.assertIn('fixture\\:pass\\\\word', passfile.read_text())
            kwargs['stdout'].write(b'fixture dump')
            kwargs['stdout'].flush()
        elif args[0] == 'php' and args[-1] == 'new':
            self.previews += 1
            kwargs['stdout'].write('Found 1 new migration:\n' if self.previews == 1
                                   else 'No new migrations found.\n')
        return subprocess.CompletedProcess(args, 0)

    def deploy_database(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return deployment.backup_and_migrate(self.app, self.stage, self.backups, self.credentials)

    def test_backup_precedes_migrations_and_is_private_checksummed_and_secret_free(self):
        with patch.dict(os.environ, {'PGPASSWORD':'do not inherit','PGOPTIONS':'do not inherit'}):
            with patch.object(deployment.subprocess, 'run', side_effect=self.command):
                backup = self.deploy_database()
        self.assertEqual(['pg_dump','pg_restore','php','php','php'], [c[0] for c in self.calls])
        self.assertEqual(['up','--interactive=0'], self.calls[3][-2:])
        self.assertEqual(0o600, backup.stat().st_mode & 0o777)
        self.assertEqual(0o700, backup.parent.stat().st_mode & 0o777)
        metadata = json.loads((backup.parent/'backup.json').read_text())
        self.assertEqual(hashlib.sha256(b'fixture dump').hexdigest(), metadata['sha256'])
        self.assertEqual('c'*40, metadata['target_commit'])
        self.assertEqual('pending', metadata['deployment_status'])
        self.assertFalse((backup.parent/'.pgpass').exists())
        self.assertNotIn('fixture:pass', ''.join(p.read_text() for p in backup.parent.iterdir()))

    def test_dump_failure_prevents_all_migration_commands_and_removes_password_file(self):
        def fail(args, **kwargs):
            self.calls.append(args)
            return subprocess.CompletedProcess(args, 1)
        with patch.object(deployment.subprocess, 'run', side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, 'backup failed'):self.deploy_database()
        self.assertEqual(['pg_dump'], [c[0] for c in self.calls])
        self.assertFalse(list(self.backups.rglob('.pgpass')))
        self.assertFalse(list(self.backups.rglob('kaart.dump')))

    def test_corrupt_archive_prevents_migrations(self):
        def corrupt(args, **kwargs):
            result = self.command(args, **kwargs)
            return subprocess.CompletedProcess(args, 1) if args[0] == 'pg_restore' else result
        with patch.object(deployment.subprocess, 'run', side_effect=corrupt):
            with self.assertRaisesRegex(RuntimeError, 'archive check failed'):self.deploy_database()
        self.assertEqual(['pg_dump','pg_restore'], [c[0] for c in self.calls])
        self.assertFalse(list(self.backups.rglob('.pgpass')))

    def test_migration_failure_retains_backup_and_stops_before_postcheck(self):
        def fail(args, **kwargs):
            result = self.command(args, **kwargs)
            return subprocess.CompletedProcess(args, 2) if '--interactive=0' in args else result
        with patch.object(deployment.subprocess, 'run', side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, 'Database changes may remain'):self.deploy_database()
        self.assertEqual(4, len(self.calls))
        self.assertEqual(1, len(list(self.backups.rglob('kaart.dump'))))

    def test_remaining_migration_prevents_activation(self):
        def pending(args, **kwargs):
            result = self.command(args, **kwargs)
            if args[-1] == 'new' and self.previews == 2:
                kwargs['stdout'].write('')
                kwargs['stdout'].seek(0);kwargs['stdout'].truncate()
                kwargs['stdout'].write('Found 1 new migration:\n')
            return result
        with patch.object(deployment.subprocess, 'run', side_effect=pending):
            with self.assertRaisesRegex(RuntimeError, 'Pending migrations remain'):self.deploy_database()

    def test_timeout_removes_password_file_and_prevents_migrations(self):
        with patch.object(deployment.subprocess, 'run', side_effect=subprocess.TimeoutExpired('pg_dump',900)):
            with self.assertRaisesRegex(RuntimeError, 'backup could not complete'):self.deploy_database()
        self.assertFalse(list(self.backups.rglob('.pgpass')))

    def test_production_database_is_rejected_before_backup(self):
        db = json.loads(self.credentials.read_text());db['database']='kaart_prod'
        self.credentials.write_text(json.dumps(db))
        with patch.object(deployment.subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'Unexpected rehearsal'):self.deploy_database()
        run.assert_not_called()

    def test_existing_backup_symlink_is_rejected(self):
        outside = self.root/'outside';outside.mkdir()
        self.backups.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Backup directory'):self.deploy_database()
        self.assertEqual([], list(outside.iterdir()))



@unittest.skipUnless(os.environ.get('KAARDID_TEST_PG_BIN') and os.environ.get('KAARDID_TEST_YII'),
                     'Set KAARDID_TEST_PG_BIN and KAARDID_TEST_YII for disposable PostgreSQL/Yii integration')
class PostgreSQLMigrationTest(unittest.TestCase):
    def test_real_backup_restore_and_automatic_yii_migration(self):
        self.exercise_backup_restore('rehearsal')

    def test_real_production_backup_restore_and_automatic_yii_migration(self):
        self.exercise_backup_restore('production')

    def exercise_backup_restore(self, target):
        pg = Path(os.environ['KAARDID_TEST_PG_BIN'])
        yii = Path(os.environ['KAARDID_TEST_YII'])
        settings=deployment.TARGETS[target]
        database,owner,user=(settings[key] for key in ('database','role','user'))
        with tempfile.TemporaryDirectory(prefix='kaardid-migrate-', dir='/private/tmp') as temp:
            root = Path(temp)
            with socket.socket() as sock:
                sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            subprocess.run([str(pg/'initdb'),'-D',str(root/'data'),'-A','trust','-U','fixture_admin',
                            '--no-locale'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            subprocess.run([str(pg/'pg_ctl'),'-D',str(root/'data'),'-l',str(root/'server.log'),
                '-o',f'-p {port} -h 127.0.0.1 -k {root}','-w','start'],check=True,stdout=subprocess.DEVNULL)
            try:
                def sql(statement, database='postgres'):
                    result = subprocess.run([str(pg/'psql'),'-X','-h',str(root),'-p',str(port),
                        '-U','fixture_admin','-d',database,'-At','-v','ON_ERROR_STOP=1','-c',statement],
                        check=True,text=True,capture_output=True)
                    return result.stdout.strip()
                sql(f"CREATE ROLE {owner} NOLOGIN; CREATE ROLE {user} LOGIN PASSWORD 'fixture-only'; GRANT {owner} TO {user}")
                sql(f'CREATE DATABASE {database} OWNER {owner}')
                sql(f"SET ROLE {owner}; CREATE TABLE example(id integer PRIMARY KEY); INSERT INTO example VALUES (1)",database)
                app = root/'releases'/('d'*40)/'apps/kaardid'
                protected = app/'protected';(protected/'migrations').mkdir(parents=True)
                (protected/'runtime').mkdir()
                config = {'host':'127.0.0.1','port':port,'database':database,'user':user,
                          'role':owner,'password':'fixture-only'}
                credentials=root/'db.json';credentials.write_text(json.dumps(config));credentials.chmod(0o600)
                php = "<?php\nrequire "+json.dumps(str(yii/'yii.php'))+";\n"+"$db=json_decode(file_get_contents("+json.dumps(str(credentials))+"),true);\n"
                php += "$app=Yii::createConsoleApplication(array('basePath'=>__DIR__, 'components'=>array('db'=>array('class'=>'CDbConnection','connectionString'=>'pgsql:host=127.0.0.1;port='.$db['port'].';dbname='.$db['database'],'username'=>$db['user'],'password'=>$db['password'],'initSQLs'=>array('SET ROLE '.$db['role'])))));\n$app->commandRunner->addCommands(YII_PATH.'/cli/commands');\n$app->run();\n"
                (protected/'yiic.php').write_text(php)
                migration=protected/'migrations/m261029_120000_example.php'
                migration.write_text("<?php class m261029_120000_example extends CDbMigration { public function safeUp() { $this->addColumn('example','feature','integer NOT NULL DEFAULT 7'); } }")
                stage=root/'stage';stage.mkdir()
                with patch.dict(os.environ, {'PATH':str(pg)+os.pathsep+os.environ['PATH']}):
                    with contextlib.redirect_stdout(io.StringIO()):
                        try:
                            backup=deployment.backup_and_migrate(app,stage,root/'backups',credentials,target=target)
                        except RuntimeError as error:
                            diagnostics='\n'.join(p.read_text() for p in (root/'backups').rglob('migration-*.txt'))
                            raise AssertionError('Disposable fixture failed:\n'+diagnostics) from error
                self.assertEqual('7',sql('SELECT feature FROM example WHERE id=1',database))
                self.assertEqual('1',sql("SELECT count(*) FROM tbl_migration WHERE version='m261029_120000_example'",database))
                sql(f'CREATE DATABASE kaart_restore OWNER {owner}')
                subprocess.run([str(pg/'pg_restore'),'-h',str(root),'-p',str(port),'-U','fixture_admin',
                    '--exit-on-error','-d','kaart_restore',str(backup)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
                self.assertEqual('1',sql('SELECT count(*) FROM example','kaart_restore'))
                self.assertEqual('0',sql("SELECT count(*) FROM information_schema.columns WHERE table_name='example' AND column_name='feature'",'kaart_restore'))
            finally:
                subprocess.run([str(pg/'pg_ctl'),'-D',str(root/'data'),'-m','immediate','-w','stop'],
                               check=True,stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    unittest.main()
