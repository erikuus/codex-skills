<?php
// One web-reporting policy; real DSNs remain in private integrations.json.
require_once __DIR__.'/Environment.php';
$environment=KaardidEnvironment::settings();
$integrations=KaardidEnvironment::integrations();
$dsn=getenv('SENTRY_DSN') ?: ($integrations['sentryDsn'] ?? null);
if(!$dsn) return null;
$label=getenv('SENTRY_ENVIRONMENT') ?: $environment['environment'];
// Retain the existing Kaardid project's prod alerts across both PHP versions.
if($label==='production') $label='prod';
$release=basename(dirname(__DIR__,4));
return array(
    'class'=>'ext.components.log.XSentryLogRoute','levels'=>'error','dsn'=>$dsn,
    'environment'=>$label,
    'release'=>getenv('SENTRY_RELEASE') ?: (preg_match('/^[a-f0-9]{40}$/D',$release) ? $release : 'kaardid'),
    'serverName'=>getenv('SENTRY_SERVER_NAME') ?: php_uname('n'),
    'sampleRate'=>1.0,'sendDefaultPii'=>false,'includeUserContext'=>false,'includeRequestContext'=>true,
    'ignoreCategories'=>array('exception.CHttpException.400','exception.CHttpException.401','exception.CHttpException.403','exception.CHttpException.404'),
    'ignoreHttpStatusCodes'=>array(400,401,403,404),
    'throttleWindowSeconds'=>(int)(getenv('SENTRY_THROTTLE_WINDOW_SECONDS') ?: 900),
    'throttleMaxInitialEvents'=>(int)(getenv('SENTRY_THROTTLE_MAX_INITIAL_EVENTS') ?: 1),
    'summaryThreshold'=>(int)(getenv('SENTRY_SUMMARY_THRESHOLD') ?: 25),'cacheID'=>'cache',
);
