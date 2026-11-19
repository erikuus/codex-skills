<?php
require_once(__DIR__.'/Environment.php');
$environment=KaardidEnvironment::settings();
return array(
    'basePath'=>dirname(__DIR__),
    'extensionPath'=>dirname(__DIR__).'/extensions',
    'runtimePath'=>$environment['consoleRuntimePath'],
    'name'=>'Kaardid migration console',
    'timeZone'=>'Europe/Tallinn',
    'commandMap'=>array(
    'exportUnits'=>array('class'=>'application.modules.haldusyksused.commands.ExportUnitsCommand'),
    'clean' => array(
        'class' => 'ext.commands.XCleanCommand',
        'webroot' => dirname(__DIR__,2),
    ),
    'compress' => array(
        'class' => 'ext.commands.compress.XCompressCommand',
        'dir' => dirname(__DIR__,2).'/css/',
        'files' => array(
            '960.css',
            'main.css',
            'form.css',
            'app.css',
        ),
        'options' => array(
            'type' => 'css',
        ),
        'paramsFile' => __DIR__.'/params.php',
        'param' => 'compressedCss',
    ),
),
    'import'=>array(
        'application.components.*','application.models.*','application.models.behaviors.*',
        'ext.validators.*','ext.filters.*','ext.modules.au.models.*','ext.models.XFileForm',
    ),
    'preload'=>array('log'),
    'components'=>array(
        'db'=>KaardidEnvironment::database('console'),
        'user'=>array('class'=>'ConsoleUser'),
        'authManager'=>array('class'=>'CPhpAuthManager'),
        'log'=>array('class'=>'CLogRouter','routes'=>array(
            array('class'=>'CFileLogRoute','levels'=>'error, warning','logFile'=>'console.log'),
        )),
        'dgsapi'=>array('class'=>'ext.components.dgsapi.XDgsApi','url'=>$environment['dgsApiUrl']),
    ),
    'modules'=>array('au'=>array('class'=>'ext.modules.au.AuModule')),
    'params'=>array_replace(require(__DIR__.'/params.php'),$environment['consoleParams']),
);
