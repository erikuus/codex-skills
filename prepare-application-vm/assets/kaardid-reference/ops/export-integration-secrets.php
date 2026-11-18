<?php
// Copy only the existing signing keys needed by this app. Never print their values.
umask(0077);
if(PHP_SAPI!=='cli' || $argc!==2 || file_exists($argv[1]))
    throw new RuntimeException('Provide a new private output filename.');
$repo=dirname(__DIR__);
require dirname($repo,2).'/yii/yii-1.1.33-dev/yii.php';
$config=require $repo.'/protected/config/main.php';
$secrets=array(
    'vauValidationKey'=>$config['components']['vauSecurityManager']['validationKey'],
    'imageSignatureSecret'=>$config['params']['imageSignatureSecret'],
);
foreach($secrets as $value)
    if(!is_string($value) || $value==='')
        throw new RuntimeException('Missing an existing integration signing key.');
file_put_contents($argv[1],json_encode($secrets,JSON_PRETTY_PRINT)."\n");
chmod($argv[1],0600);
echo 'Integration signing keys exported to the private file; values omitted.'.PHP_EOL;
