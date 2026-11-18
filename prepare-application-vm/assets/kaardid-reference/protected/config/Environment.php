<?php
/** Private installation values; application configuration stays in PHP/Git. */
class KaardidEnvironment
{
    private static $settings;
    private static $files=array();

    public static function settings()
    {
        if(self::$settings===null)
        {
            $settings=self::read(__DIR__.'/private/environment.json');
            if(!isset($settings['environment']) || !in_array($settings['environment'],array('local','rehearsal','production'),true))
                throw new RuntimeException('Private environment.json must identify local, rehearsal or production.');
            foreach(array('name','databaseFile','integrationsFile','externalCallbackBaseUrl') as $key)
                if(!isset($settings[$key]) || !is_string($settings[$key]))
                    throw new RuntimeException('Missing private environment setting: '.$key);
            if(!isset($settings['analytics']) || !is_bool($settings['analytics']))
                throw new RuntimeException('Private environment.json must specify analytics as true or false.');
            if($settings['environment']!=='production' && $settings['analytics'])
                throw new RuntimeException('Analytics must be disabled outside public production.');
            $settings+=array(
                'runtimePath'=>dirname(__DIR__).'/runtime',
                'consoleRuntimePath'=>dirname(__DIR__).'/runtime',
                'assetsPath'=>dirname(__DIR__,2).'/assets',
                'params'=>array(), 'developmentParams'=>array(), 'testParams'=>array(), 'consoleParams'=>array(),
            );
            $settings['dgsApiUrl']=$settings['environment']==='local'
                ? 'https://www.ra.ee/dgs-api/api/v1/dip/'
                : 'https://kristjan.arhiiv.ee/dgs-api/api/v1/dip/';
            self::$settings=$settings;
        }
        return self::$settings;
    }

    public static function requireLocal()
    {
        if(self::settings()['environment']!=='local')
            throw new RuntimeException('Development and test configurations are available only on a local installation.');
    }

    public static function integrations()
    {
        $values=self::read(self::settings()['integrationsFile']);
        foreach(array('vauValidationKey','imageSignatureSecret') as $key)
            if(empty($values[$key]) || !is_string($values[$key]))
                throw new RuntimeException('Missing private integration setting: '.$key);
        return $values;
    }

    public static function database($profile='production')
    {
        $db=self::connection($profile);
        $config=array(
            'class'=>'CDbConnection',
            'connectionString'=>'pgsql:host='.$db['host'].';port='.$db['port'].';dbname='.$db['database'],
            'username'=>$db['user'], 'password'=>$db['password'],
            'schemaCachingDuration'=>3600, 'enableProfiling'=>false, 'enableParamLogging'=>false,
        );
        if(isset($db['role']))
        {
            if(!preg_match('/^[a-z][a-z0-9_]*$/D',$db['role']))
                throw new RuntimeException('Invalid database role in private configuration.');
            $config['initSQLs']=array('SET ROLE '.$db['role']);
        }
        return $config;
    }

    private static function connection($profile)
    {
        $settings=self::settings();
        if(!in_array($profile,array('production','development','test','console','cron'),true))
            throw new RuntimeException('Unknown database configuration profile.');
        if($profile==='test' || $profile==='development')
            self::requireLocal();
        $key=$profile==='test' ? 'testDatabaseFile' : ($profile==='console' ? 'migrationDatabaseFile' : 'databaseFile');
        if(empty($settings[$key]) || !is_string($settings[$key]))
            throw new RuntimeException('Missing private environment setting: '.$key);
        $db=self::read($settings[$key]);
        foreach(array('host','database','user','password') as $field)
            if(!isset($db[$field]) || !is_string($db[$field]) || $db[$field]==='')
                throw new RuntimeException('Missing database setting: '.$field);
        if(!isset($db['port']) || !is_int($db['port']) || $db['port']<1 || $db['port']>65535)
            throw new RuntimeException('Invalid database port in private configuration.');
        $expected=$profile==='test' ? 'kaart_test' : array('local'=>'kaart_dev','rehearsal'=>'kaart','production'=>'kaart_prod')[$settings['environment']];
        if($db['database']!==$expected)
            throw new RuntimeException('Database does not match the selected environment/profile.');
        return $db;
    }

    private static function read($file)
    {
        if(!is_string($file) || $file==='')
            throw new RuntimeException('Missing private JSON filename.');
        if($file[0]!=='/')
            $file=__DIR__.'/private/'.$file;
        if(!array_key_exists($file,self::$files))
        {
            if(!is_file($file) || !is_readable($file) || (fileperms($file)&0007))
                throw new RuntimeException('Private JSON file is missing, unreadable or accessible to other users: '.basename($file));
            $content=@file_get_contents($file);
            $data=json_decode($content===false ? '' : $content,true);
            if(!is_array($data) || array_is_list($data))
                throw new RuntimeException('Invalid private JSON object: '.basename($file));
            self::$files[$file]=$data;
        }
        return self::$files[$file];
    }
}
