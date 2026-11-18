"""Private config creation and reruns against disposable, fake secrets only."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('production_config',Path(__file__).with_name('configure-production.py'))
config=importlib.util.module_from_spec(spec);spec.loader.exec_module(config)


class ProductionConfigTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.directory=self.root/'production';self.directory.mkdir(mode=0o750)
        self.gid=self.directory.stat().st_gid
        self.template=json.loads((Path(__file__).parent.parent/'protected/config/examples/environment.production.json').read_text())
        self.source=self.root/'rehearsal.json'
        self.source.write_text(json.dumps({'vauValidationKey':'fixture-vau-key','imageSignatureSecret':'fixture-rehearsal-image',
                                          'giiPassword':'fixture-local-gii','sentryDsn':'fixture-only-dsn'}))
        self.source.chmod(0o600)

    def configure(self,source=True):
        return config.configure(self.directory,self.template,self.gid,self.source if source else None)

    def test_environment_only_never_assumes_a_vau_key(self):
        result=self.configure(source=False)
        self.assertEqual(['environment.json'],result['created'])
        self.assertFalse(result['integrationsReady'])
        self.assertFalse((self.directory/'integrations.json').exists())
        self.assertEqual(self.template,json.loads((self.directory/'environment.json').read_text()))

    def test_reuses_only_chosen_vau_key_and_generates_independent_private_image_secret(self):
        result=self.configure()
        keys=json.loads((self.directory/'integrations.json').read_text())
        self.assertEqual('fixture-vau-key',keys['vauValidationKey'])
        self.assertRegex(keys['imageSignatureSecret'],r'^[a-f0-9]{64}$')
        self.assertNotEqual('fixture-rehearsal-image',keys['imageSignatureSecret'])
        self.assertNotIn('giiPassword',keys);self.assertIsNone(keys['sentryDsn'])
        self.assertEqual({'vauValidationKey','imageSignatureSecret','sentryDsn'},set(keys))
        for name in ('environment.json','integrations.json'):
            info=(self.directory/name).stat()
            self.assertEqual(0o640,info.st_mode&0o777)
            self.assertEqual(os.geteuid(),info.st_uid);self.assertEqual(self.gid,info.st_gid)
        self.assertNotIn('fixture-vau-key',json.dumps(result))
        self.assertNotIn(keys['imageSignatureSecret'],json.dumps(result))
        self.assertEqual(['environment.json','integrations.json'],sorted(p.name for p in self.directory.iterdir()))

    def test_rerun_preserves_secrets_and_operator_fields_without_rotation(self):
        self.configure()
        secret=self.directory/'integrations.json';before=secret.read_bytes()
        self.source.write_text('{"vauValidationKey":"different-fixture-key"}')
        settings=json.loads((self.directory/'environment.json').read_text())
        settings['params']={'pageSize':31}
        (self.directory/'environment.json').write_text(json.dumps(settings))
        result=self.configure()
        self.assertEqual([],result['created']);self.assertEqual(before,secret.read_bytes())
        self.assertEqual({'pageSize':31},json.loads((self.directory/'environment.json').read_text())['params'])

    def test_existing_wrong_environment_or_unsafe_file_stops_without_changing_secrets(self):
        self.configure()
        original=(self.directory/'integrations.json').read_bytes()
        path=self.directory/'environment.json';settings=json.loads(path.read_text());settings['environment']='rehearsal'
        path.write_text(json.dumps(settings))
        with self.assertRaisesRegex(ValueError,'settings differ'):self.configure()
        self.assertEqual(original,(self.directory/'integrations.json').read_bytes())

    def test_source_placeholder_or_symlink_is_rejected_without_writing_anything(self):
        self.source.write_text('{"vauValidationKey":"REPLACE_WITH_KEY"}')
        with self.assertRaisesRegex(ValueError,'unavailable'):self.configure()
        self.assertEqual([],list(self.directory.iterdir()))
        self.source.unlink();self.source.symlink_to(self.root/'missing')
        with self.assertRaisesRegex(ValueError,'Unexpected private file'):self.configure()

    def test_destination_symlink_or_world_readability_is_rejected(self):
        outside=self.root/'outside';outside.write_text('preserve')
        path=self.directory/'environment.json';path.symlink_to(outside)
        with self.assertRaisesRegex(ValueError,'Unexpected private file'):self.configure()
        self.assertEqual('preserve',outside.read_text())
        path.unlink();self.configure();path.chmod(0o644)
        with self.assertRaisesRegex(ValueError,'Unexpected private file'):self.configure()

    def test_unexpected_directory_or_template_is_rejected_before_write(self):
        self.directory.chmod(0o777)
        with self.assertRaisesRegex(ValueError,'directory'):self.configure()
        self.directory.chmod(0o750);self.template['databaseFile']='/etc/kaardid/app-db.json'
        with self.assertRaisesRegex(ValueError,'template'):self.configure()
        self.assertEqual([],list(self.directory.iterdir()))

    def test_exclusive_publish_does_not_replace_an_existing_file(self):
        path=self.directory/'integrations.json';path.write_text('preserve')
        with self.assertRaisesRegex(ValueError,'overwrite'):config.write_new(path,{},self.gid)
        self.assertEqual('preserve',path.read_text())


if __name__=='__main__':unittest.main()
