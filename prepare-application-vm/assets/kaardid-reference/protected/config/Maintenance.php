<?php
/** Keep visitors in maintenance while the deployer checks the incoming release. */
final class KaardidMaintenance
{
    public static function catchAllRequest()
    {
        if(!file_exists(__DIR__.'/private/.maintenance'))
            return null;

        // SSH preview visitors also arrive from loopback: an IP alone is not a bypass.
        $routes=array('/','/index.php/map/search','/index.php/map/searchAdvanced','/index.php/test/login');
        // Authorization is scrubbed by Sentry; also consume it before Yii can
        // include $_SERVER in an exception log. Never put this token in a URL.
        $authorization=$_SERVER['HTTP_AUTHORIZATION'] ?? '';
        $token=is_string($authorization) && preg_match('/\ABearer ([a-f0-9]{64})\z/D',$authorization,$match)
            ? $match[1] : '';
        if($token!=='') unset($_SERVER['HTTP_AUTHORIZATION']);
        if(($_SERVER['REQUEST_METHOD'] ?? '')==='GET'
            && in_array($_SERVER['REMOTE_ADDR'] ?? '',array('127.0.0.1','::1'),true)
            && in_array($_SERVER['REQUEST_URI'] ?? '',$routes,true)
            && $token!=='')
        {
            $file=__DIR__.'/private/.deployment-probe.json';
            if(!is_link($file) && is_file($file) && (fileperms($file) & 0027)===0)
            {
                $probe=json_decode(file_get_contents($file),true);
                if(is_array($probe) && is_string($probe['token'] ?? null)
                    && is_int($probe['expiresAt'] ?? null) && $probe['expiresAt']>time()
                    && ($probe['appPath'] ?? null)===realpath(dirname(__DIR__,2))
                    && hash_equals($probe['token'],$token))
                    return null;
            }
        }
        return array('maintenance/index');
    }
}
