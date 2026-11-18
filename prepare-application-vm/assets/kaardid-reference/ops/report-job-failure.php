<?php
/** No app bootstrap, database, command output, environment dump or journal collection. */
function kaardidFailureMetadata($unit, $environment)
{
    if(!is_string($unit) || !preg_match('/\A(?:kaardid-update|kaardid-monitoring-probe-[A-Za-z0-9_-]+)\.service\z/D',$unit))
        throw new RuntimeException('Unexpected monitored unit.');
    if(($environment['MONITOR_UNIT']??null)!==$unit)
        throw new RuntimeException('Missing matching systemd failure context.');
    $metadata=array('unit'=>$unit);
    foreach(array('MONITOR_SERVICE_RESULT','MONITOR_EXIT_CODE','MONITOR_EXIT_STATUS','MONITOR_INVOCATION_ID') as $key) {
        $value=$environment[$key]??null;
        // Failures before a process starts can have no exit code/status.
        if($value===null && in_array($key,array('MONITOR_EXIT_CODE','MONITOR_EXIT_STATUS'),true)) {
            $metadata[strtolower(substr($key,8))]=null;
            continue;
        }
        if(!is_string($value) || !preg_match('/\A[A-Za-z0-9_-]{1,64}\z/D',$value))
            throw new RuntimeException('Missing or invalid systemd failure metadata.');
        $metadata[strtolower(substr($key,8))]=$value;
    }
    if($metadata['service_result']==='success') throw new RuntimeException('Refusing a successful-job failure alert.');
    return $metadata;
}

function kaardidSendFailure($transport, $metadata)
{
    $event=\Sentry\Event::createEvent();
    $event->setMessage('Kaardid scheduled job failed: '.$metadata['unit']);
    $event->setLevel(\Sentry\Severity::error());
    $event->setEnvironment('prod');
    $event->setRelease('kaardid-monitoring-v1');
    $event->setServerName('kaardid-vm');
    $event->setFingerprint(array('kaardid-systemd-failure',$metadata['unit']));
    $event->setTags(array('monitoring.kind'=>'scheduled-job-failure','systemd.unit'=>$metadata['unit']));
    $event->setExtra($metadata);
    $result=$transport->send($event);
    // A non-null SDK event ID alone does not prove a successful HTTP response.
    if($result->getStatus()!==\Sentry\Transport\ResultStatus::success())
        throw new RuntimeException('Sentry did not accept the notification.');
    return (string)$event->getId();
}

if(realpath($_SERVER['SCRIPT_FILENAME']??'')!==__FILE__) return;
try {
    if(PHP_SAPI!=='cli' || $argc!==2) exit(2);
    $metadata=kaardidFailureMetadata($argv[1],getenv());
    $path='/srv/kaardid-production/shared/config/integrations.json';
    if(is_link($path) || !is_file($path) || (fileperms($path)&0027))
        throw new RuntimeException('Unsafe monitoring configuration.');
    $private=json_decode(file_get_contents($path),true,512,JSON_THROW_ON_ERROR);
    if(empty($private['sentryDsn'])) throw new RuntimeException('Sentry DSN is not configured.');
    require __DIR__.'/sdk/autoload.php';
    $builder=\Sentry\ClientBuilder::create(array('dsn'=>$private['sentryDsn'],'environment'=>'prod','release'=>'kaardid-monitoring-v1',
        'server_name'=>'kaardid-vm','send_default_pii'=>false,'default_integrations'=>false,
        'attach_stacktrace'=>false,'max_breadcrumbs'=>0,'http_timeout'=>10.0));
    $event=kaardidSendFailure($builder->getTransport(),$metadata);
    $directory='/srv/kaardid-production/shared/runtime/monitoring';
    $receipt=array_merge($metadata,array('event_id'=>(string)$event,'submitted_at'=>gmdate('c')));
    $temporary=tempnam($directory,'.receipt-');
    if($temporary===false) throw new RuntimeException('Cannot create monitoring receipt.');
    try {
        chmod($temporary,0640);
        if(file_put_contents($temporary,json_encode($receipt,JSON_THROW_ON_ERROR)."\n")===false
            || !rename($temporary,$directory.'/'.$metadata['unit'].'.json'))
            throw new RuntimeException('Cannot publish monitoring receipt.');
    } finally {if(is_file($temporary)) unlink($temporary);}
    echo 'Kaardid job-failure event submitted; receipt recorded.'.PHP_EOL;
} catch(Throwable $error) {
    // SDK exceptions can include DSNs or payloads. Keep them out of journald.
    fwrite(STDERR,'Kaardid job-failure notification failed; details omitted.'.PHP_EOL);
    exit(1);
}
