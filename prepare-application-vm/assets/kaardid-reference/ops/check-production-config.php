<?php
/** Read private values internally; print only configuration and read-only DB checks. */
if(PHP_SAPI!=='cli' || $argc<2 || $argc>3)
    exit(2);
ini_set('display_errors','0');
error_reporting(E_ALL);
try {
    $app=realpath($argv[1]);
    if(!$app || !preg_match('~^/srv/kaardid-production/releases/[a-f0-9]{40}/apps/kaardid$~D',$app))
        throw new RuntimeException('Unexpected candidate path.');
    $_SERVER['SCRIPT_NAME']='/index.php';
    $_SERVER['HTTP_HOST']='kaardid.ra.ee';
    $_SERVER['HTTPS']='on';
    require dirname($app,2).'/yii/yii-1.1.33-dev/yii.php';
    require $app.'/protected/config/Environment.php';
    $s=KaardidEnvironment::settings();
    $expected=array('environment'=>'production','databaseFile'=>'/etc/kaardid-production/app-db.json',
        'migrationDatabaseFile'=>'/home/erik/.config/kaardid/production-migration-db.json',
        'runtimePath'=>'/srv/kaardid-production/shared/runtime',
        'consoleRuntimePath'=>'/srv/kaardid-production/shared/runtime-console',
        'assetsPath'=>'/srv/kaardid-production/shared/assets','externalCallbackBaseUrl'=>'https://kaardid.ra.ee');
    foreach($expected as $key=>$value)
        if(($s[$key]??null)!==$value) throw new RuntimeException('Unexpected production selector.');
    $profiles=($argv[2]??'all')==='web' ? array('production','cron') : array('production','console','cron');
    $result=array();
    foreach($profiles as $profile) {
        $c=require $app.'/protected/config/'.$profile.'.php';
        $db=$c['components']['db'];
        $user=$profile==='console' ? 'kaart_prod_migrate' : 'kaart_prod_app';
        if($db['connectionString']!=='pgsql:host=127.0.0.1;port=5432;dbname=kaart_prod' || $db['username']!==$user)
            throw new RuntimeException('Profile selected an unexpected database.');
        if($profile==='console' && ($db['initSQLs']??array())!==array('SET ROLE kaart_prod_owner'))
            throw new RuntimeException('Migration owner role missing.');
        if(isset($c['modules']['gii'])) throw new RuntimeException('Gii must not be available in production.');
        $pdo=new PDO($db['connectionString'],$db['username'],$db['password'],array(PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION));
        $pdo->beginTransaction();
        try {
            $pdo->exec('SET TRANSACTION READ ONLY');
            $pdo->exec("SET LOCAL statement_timeout='5s'");
            if($profile==='console') $pdo->exec('SET ROLE kaart_prod_owner');
            $row=$pdo->query("SELECT current_database() AS database, current_user AS role,
                current_setting('transaction_read_only') AS read_only,
                has_database_privilege(current_user,'kaart','CONNECT') AS rehearsal_access")->fetch(PDO::FETCH_ASSOC);
            if($row['database']!=='kaart_prod' || $row['role']!==($profile==='console'?'kaart_prod_owner':'kaart_prod_app')
                || $row['read_only']!=='on' || $row['rehearsal_access'])
                throw new RuntimeException('Read-only database identity/isolation check failed.');
            $result[$profile]=array('database'=>$row['database'],'role'=>$row['role'],'readOnlyCheck'=>true,'rehearsalAccess'=>false);
        } finally {$pdo->rollBack();}
    }
    Yii::setPathOfAlias('ext',$app.'/protected/extensions');
    require $app.'/protected/extensions/components/vauid/XVauSecurityManager.php';
    $keys=KaardidEnvironment::integrations();
    $security=new XVauSecurityManager;
    $security->version=2.1;$security->setValidationKey($keys['vauValidationKey']);$security->init();
    $message='kaardid-private-config-probe';
    if($security->decrypt($security->encrypt($message))!==$message)
        throw new RuntimeException('Local VAU cryptography check failed.');
    echo json_encode(array('profiles'=>$result,'callbackBaseUrl'=>$s['externalCallbackBaseUrl'],
        'vauCryptoRoundtrip'=>true,'externalVauLoginVerified'=>false,
        'imageSecretPresent'=>strlen($keys['imageSignatureSecret'])>=32,
        'sentryConfigured'=>!empty($keys['sentryDsn'])),JSON_PRETTY_PRINT).PHP_EOL;
} catch(Throwable $e) {
    fwrite(STDERR,'Production configuration check failed ('.get_class($e).'). Values omitted.'.PHP_EOL);
    exit(1);
}
