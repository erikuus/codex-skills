<?php
require_once(__DIR__.'/Environment.php');
KaardidEnvironment::requireLocal();
$config=CMap::mergeArray(require(__DIR__.'/main.php'),array(
    'components'=>array(
        'db'=>array_replace(KaardidEnvironment::database('test'),array(
            'enableProfiling'=>true,'enableParamLogging'=>true,
        )),
        'session'=>array('sessionName'=>'TESTKAARTSESSION'),
    ),
));
$config['params']=array_replace($config['params'],KaardidEnvironment::settings()['testParams']);
return $config;
