"""Exercise shared PHP configuration against disposable, fake private JSON."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest

REPO=Path(__file__).resolve().parent.parent
YII=REPO.parent.parent/'yii/yii-1.1.33-dev/yii.php'


class ConfigurationTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.config=Path(self.temp.name)/'protected/config';self.config.mkdir(parents=True)
        for path in (REPO/'protected/config').glob('*.php'):
            shutil.copyfile(path,self.config/path.name)
        (self.config/'private').mkdir(mode=0o700)
        self.settings={'environment':'local','name':'Fixture','databaseFile':'database.json',
            'testDatabaseFile':'test-db.json','migrationDatabaseFile':'migration-db.json',
            'integrationsFile':'integrations.json','analytics':False,'externalCallbackBaseUrl':'http://localhost:8000'}
        self.db={'host':'127.0.0.1','port':5432,'database':'kaart_dev','user':'fixture_app','password':'fixture-only-secret'}
        self.write('environment.json',self.settings);self.write('database.json',self.db)
        self.write('test-db.json',dict(self.db,database='kaart_test'))
        self.write('migration-db.json',dict(self.db,user='fixture_migrate',role='kaart_owner'))
        self.write('integrations.json',{'vauValidationKey':'fixture-validation','imageSignatureSecret':'fixture-signing','giiPassword':'fixture-gii'})

    def write(self,name,data):
        path=self.config/'private'/name;path.write_text(json.dumps(data));path.chmod(0o600)

    def evaluate(self,profile='production',expect_ok=True,environment=None):
        php="""<?php
        $_SERVER['SCRIPT_NAME']='/index.php';$_SERVER['HTTP_HOST']='localhost:8000';
        require %s;
        try {
            $c=require %s;
            echo json_encode(array('dsn'=>$c['components']['db']['connectionString'],
                'dgsApiUrl'=>$c['components']['dgsapi']['url'],
                'user'=>$c['components']['db']['username'],
                'initSQLs'=>$c['components']['db']['initSQLs'] ?? array(),
                'pageSize'=>$c['params']['pageSize'],
                'logFiles'=>array_column($c['components']['log']['routes'],'logFile'),
                'sentry'=>array_values(array_map(function($r) {return array_intersect_key($r,array_flip(array('environment','release','sendDefaultPii','includeUserContext','throttleWindowSeconds','summaryThreshold')));},
                    array_filter($c['components']['log']['routes'],function($r) {return ($r['class']??'')==='ext.components.log.XSentryLogRoute';})))));
        } catch(Throwable $e) {fwrite(STDERR,$e->getMessage());exit(1);}
        """ % (json.dumps(str(YII)),json.dumps(str(self.config/(profile+'.php'))))
        env=dict(os.environ);env.pop('SENTRY_DSN',None)
        for key in ('SENTRY_ENVIRONMENT','SENTRY_RELEASE','SENTRY_THROTTLE_WINDOW_SECONDS','SENTRY_SUMMARY_THRESHOLD'):env.pop(key,None)
        env.update(environment or {})
        result=subprocess.run(['php','-d','display_errors=0'],input=php,text=True,capture_output=True,env=env)
        self.assertEqual(0 if expect_ok else 1,result.returncode,result.stderr)
        self.assertNotIn('fixture-only-secret',result.stdout+result.stderr)
        return json.loads(result.stdout) if expect_ok else result.stderr

    def test_same_public_configuration_selects_local_rehearsal_and_production_values(self):
        for installation,database in [('local','kaart_dev'),('rehearsal','kaart'),('production','kaart_prod')]:
            with self.subTest(installation=installation):
                self.write('environment.json',dict(self.settings,environment=installation))
                self.write('database.json',dict(self.db,database=database))
                c=self.evaluate()
                self.assertIn('dbname='+database,c['dsn'])
                self.assertEqual('fixture_app',c['user'])
                self.assertEqual(['error.log','warning.log'],c['logFiles'])

    def test_one_parameter_change_is_used_by_every_web_profile(self):
        params=self.config/'params.php';text=params.read_text()
        self.assertIn("'pageSize' => 20",text)
        params.write_text(text.replace("'pageSize' => 20","'pageSize' => 41"))
        for profile in ('development','test','production'):
            self.assertEqual(41,self.evaluate(profile)['pageSize'])

    def test_dgs_endpoint_matches_installation_in_every_entry_point(self):
        for installation,database,host in [('local','kaart_dev','www.ra.ee'),
                ('rehearsal','kaart','kristjan.arhiiv.ee'),
                ('production','kaart_prod','kristjan.arhiiv.ee')]:
            self.write('environment.json',dict(self.settings,environment=installation,
                consoleDgsApiUrl='https://obsolete.example.invalid/',
                dgsApiUrl='https://obsolete.example.invalid/'))
            self.write('database.json',dict(self.db,database=database))
            self.write('migration-db.json',dict(self.db,database=database,user='fixture_migrate'))
            profiles=('production','console','cron')
            if installation=='local':
                profiles+=('development','test')
            for profile in profiles:
                with self.subTest(installation=installation,profile=profile):
                    self.assertEqual('https://'+host+'/dgs-api/api/v1/dip/',
                                     self.evaluate(profile)['dgsApiUrl'])

    def test_test_profile_uses_only_test_database(self):
        self.assertIn('dbname=kaart_test',self.evaluate('test')['dsn'])
        self.write('test-db.json',self.db)
        self.assertIn('Database does not match',self.evaluate('test',False))

    def test_development_and_test_profiles_reject_server_installation(self):
        self.write('environment.json',dict(self.settings,environment='rehearsal'))
        for profile in ('development','test','unittest'):
            self.assertIn('only on a local installation',self.evaluate(profile,False))

    def test_console_uses_migration_credentials_and_web_uses_app_credentials(self):
        console=self.evaluate('console')
        self.assertEqual('fixture_migrate',console['user'])
        self.assertEqual(['SET ROLE kaart_owner'],console['initSQLs'])

        web=self.evaluate()
        self.assertEqual('fixture_app',web['user'])
        self.assertEqual([],web['initSQLs'])

    def test_missing_json_does_not_fall_back_to_another_database(self):
        (self.config/'private/database.json').unlink()
        error=self.evaluate(expect_ok=False)
        self.assertIn('database.json',error)

    def test_production_sentry_uses_existing_prod_alert_environment_and_keeps_privacy_throttling(self):
        self.write('environment.json',dict(self.settings,environment='production'))
        self.write('database.json',dict(self.db,database='kaart_prod'))
        self.write('integrations.json',{'vauValidationKey':'fixture','imageSignatureSecret':'fixture',
                                       'sentryDsn':'https://offline-key@sentry.invalid/1'})
        route=self.evaluate(environment={'SENTRY_ENVIRONMENT':'production'})['sentry'][0]
        self.assertEqual('prod',route['environment'])
        self.assertFalse(route['sendDefaultPii']);self.assertFalse(route['includeUserContext'])
        self.assertEqual(900,route['throttleWindowSeconds']);self.assertEqual(25,route['summaryThreshold'])
        self.assertEqual('prod',self.evaluate()['sentry'][0]['environment'])

    def test_sentry_stays_disabled_without_dsn_and_rehearsal_does_not_use_prod_alerts(self):
        self.assertEqual([],self.evaluate()['sentry'])
        self.write('environment.json',dict(self.settings,environment='rehearsal'))
        self.write('database.json',dict(self.db,database='kaart'))
        self.assertEqual('rehearsal',self.evaluate(environment={'SENTRY_DSN':'https://offline-key@sentry.invalid/1'})['sentry'][0]['environment'])

    def test_deployment_token_cannot_be_used_from_non_loopback_or_forwarded_address(self):
        token='a'*64
        (self.config/'private/.maintenance').touch()
        self.write('.deployment-probe.json',{'token':token,'expiresAt':int(time.time())+600,
                                            'appPath':str(self.config.parent.parent.resolve())})
        php="""<?php
        require %s;
        $_SERVER=array('REQUEST_METHOD'=>'GET','REQUEST_URI'=>'/',
            'REMOTE_ADDR'=>'203.0.113.5','HTTP_X_FORWARDED_FOR'=>'127.0.0.1',
            'HTTP_AUTHORIZATION'=>%s);
        $route=KaardidMaintenance::catchAllRequest();
        echo json_encode(array($route,isset($_SERVER['HTTP_AUTHORIZATION'])));
        """ % (json.dumps(str(self.config/'Maintenance.php')),json.dumps('Bearer '+token))
        result=subprocess.run(['php'],input=php,text=True,capture_output=True,check=True)
        self.assertEqual([['maintenance/index'],False],json.loads(result.stdout))

    def test_world_readable_private_json_is_rejected(self):
        (self.config/'private/database.json').chmod(0o644)
        self.assertIn('accessible to other users',self.evaluate(expect_ok=False))

    def test_analytics_cannot_be_enabled_on_rehearsal_or_mac(self):
        self.write('environment.json',dict(self.settings,analytics=True))
        self.assertIn('Analytics must be disabled',self.evaluate(expect_ok=False))

    def test_local_router_blocks_private_json_including_encoded_and_repeated_slashes(self):
        paths=['/protected/config/private/database.json','//protected/config/private/environment.json',
               '/%70rotected/config/private/database.json','/protected%2fconfig/private/database.json',
               '/index.php/../protected/config/private/database.json','/.git/config',
               '/PROTECTED/config/private/database.json','/ops/build-release.py']
        for path in paths+['/index-dev.php/et','/assets/example.css']:
            php="<?php $_SERVER['REQUEST_URI']="+json.dumps(path)+";ob_start();$r=require "+json.dumps(str(REPO/'dev-router.php'))+";ob_end_clean();echo json_encode(array($r,http_response_code() ?: 200));"
            result=subprocess.run(['php'],input=php,text=True,capture_output=True,check=True)
            self.assertEqual([True,404] if path in paths else [False,200],json.loads(result.stdout),path)


if __name__=='__main__':unittest.main()
