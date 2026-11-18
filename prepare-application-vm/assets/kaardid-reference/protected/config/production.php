<?php
// Normal web mode on Mac, rehearsal and public production; JSON selects the installation.
require_once(__DIR__.'/Environment.php');
$config=CMap::mergeArray(require(__DIR__.'/main.php'),array(
    'components'=>array('db'=>KaardidEnvironment::database(),'cache'=>array('class'=>'CFileCache')),
));
$sentry=require __DIR__.'/sentry.php';
if($sentry) $config['components']['log']['routes'][]=$sentry;
return $config;
