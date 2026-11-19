<?php
/** Disposable loopback harness: actual probe + Yii error handler/route, no DB component. */
if(PHP_SAPI!=='cli-server' || getenv('KAARDID_MONITORING_TEST')!=='1') {
    http_response_code(404);exit;
}
$state=__DIR__;
$app=getenv('KAARDID_MONITORING_APP');
if(!is_string($app) || !is_file($app.'/index.php')) {http_response_code(404);exit;}
define('YII_DEBUG',false);
require $app.'/protected/load_composer_autoload.php';
require dirname($app,2).'/yii/yii-1.1.33-dev/yii.php';
require $state.'/XSentryProbeAction.php';
require $state.'/config/Environment.php';
class KaardidMonitoringProbeController extends CController
{
    public function actions() {
        return array('sentryProbe'=>array('class'=>'XSentryProbeAction',
            'token'=>getenv('SENTRY_PROBE_TOKEN'),'marker'=>getenv('SENTRY_PROBE_MARKER')));
    }
    public function actionError() {http_response_code(500);header('Content-Type: text/plain');echo 'Expected monitoring probe.';}
}
$route=require $state.'/config/sentry.php';
if(!$route) {http_response_code(503);exit;}
// These accelerators apply to this disposable harness, never to production.
$route['throttleWindowSeconds']=10;
$route['summaryThreshold']=3;
$route['includeRequestContext']=false;
$application=Yii::createWebApplication(array(
    'basePath'=>$app.'/protected','runtimePath'=>$state.'/runtime',
    'extensionPath'=>$app.'/protected/extensions','preload'=>array('log'),
    'controllerMap'=>array('site'=>array('class'=>'KaardidMonitoringProbeController')),
    'components'=>array(
        'cache'=>array('class'=>'CFileCache'),
        'session'=>array('class'=>'CHttpSession','savePath'=>$state.'/sessions'),
        'urlManager'=>array('urlFormat'=>'path','showScriptName'=>true),
        'errorHandler'=>array('errorAction'=>'site/error'),
        'log'=>array('class'=>'CLogRouter','routes'=>array($route)),
    ),
));
// Even accidental database use must fail: this harness has no DB/AU components.
$application->run();
