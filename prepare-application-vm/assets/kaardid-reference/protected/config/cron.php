<?php
require_once(__DIR__.'/Environment.php');
$environment=KaardidEnvironment::settings();
return array(
    'basePath'=>dirname(__DIR__),
    'extensionPath'=>dirname(__DIR__).'/extensions',
    'runtimePath'=>$environment['runtimePath'],
    'name'=>$environment['name'].' update',
    'timeZone'=>'Europe/Tallinn',
    'preload'=>array('log'),
    'components'=>array(
        'db'=>KaardidEnvironment::database('cron'),
        'dgsapi'=>array('class'=>'ext.components.dgsapi.XDgsApi','url'=>$environment['dgsApiUrl']),
        'log'=>array('class'=>'CLogRouter','routes'=>array(
            array('class'=>'CFileLogRoute','levels'=>'error, warning','logFile'=>'cron_error.log',
                'chmod'=>0640,'maxFileSize'=>10240,'maxLogFiles'=>10),
            array('class'=>'CFileLogRoute','levels'=>'trace','categories'=>'update','logFile'=>'update_trace.log',
                'chmod'=>0640,'maxFileSize'=>10240,'maxLogFiles'=>10),
        )),
    ),
    'params'=>require(__DIR__.'/params.php'),
);
