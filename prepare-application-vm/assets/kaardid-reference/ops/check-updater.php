<?php
// Invoked only by check-updater.py against its private, disposable PostgreSQL cluster.
$mode=$argv[1];$appRoot=$argv[2];$runtime=$argv[3];$socket=$argv[4];$candidate=$argv[5];
ini_set('display_errors','0');
ini_set('default_socket_timeout','10');
require($appRoot.'/protected/load_composer_autoload.php');
require(dirname($appRoot,2).'/yii/yii-1.1.33-dev/yii.php');
require($candidate);

class ProbeDgsApi extends CApplicationComponent
{
    public $newRows=array();public $deleted=array();public $failDeleted=false;public $intervals=array();
    public function request($request,$parameters=array()) {
        $this->intervals[]=array((int)$parameters['startCreatedTime'],(int)$parameters['endCreatedTime']);
        if($request==='get-deleted') {
            if($this->failDeleted) throw new RuntimeException('injected deleted-image failure');
            return $this->deleted;
        }
        return $this->newRows;
    }
}

class ProbeUpdateCommand extends UpdateCommand
{
    public $mode;
    public $thumbnailAttempts=array();
    public $failedThumbnailIds=array(1,2);
    public function syncMapData() {
        if($this->mode==='hold') {
            file_put_contents(Yii::app()->runtimePath.'/held','1');
            $deadline=time()+20;
            while(!is_file(Yii::app()->runtimePath.'/release') && time()<$deadline) usleep(50000);
            probeAssert(time()<$deadline,'lock test released in time');
            return;
        }
        parent::syncMapData();
    }
    public function saveMissingThumbs($limit) {
        if($this->mode!=='hold') parent::saveMissingThumbs($limit);
    }
    protected function _getThumbFileContents($uid) {
        if($this->mode==='thumbnail-queue') {
            $id=(int)substr($uid,-12);
            $this->thumbnailAttempts[]=$id;
            return in_array($id,$this->failedThumbnailIds,true) ? false : 'queue fixture thumbnail';
        }
        if($this->mode==='fixture-warning') return false;
        return $this->mode==='fixture' ? 'isolated fixture thumbnail' : parent::_getThumbFileContents($uid);
    }
}


$phase='bootstrap';
try {
    $config=require($appRoot.'/protected/config/cron.php');
    $config['runtimePath']=$runtime;
    $config['components']['db']=array('class'=>'CDbConnection',
        'connectionString'=>'pgsql:host='.$socket.';port=55439;dbname=kaart_updater_probe',
        'username'=>'updater_probe_app','password'=>'','schemaCachingDuration'=>0);
    $app=Yii::createConsoleApplication($config);
    set_error_handler(function($severity,$message,$file,$line) {
        if(!(error_reporting()&$severity)) return false;
        throw new ErrorException('PHP warning in isolated probe',0,$severity,$file,$line);
    });
    $db=$app->db;
    $identity=$db->createCommand('SELECT current_database() AS db, current_user AS role, inet_server_addr() AS address')->queryRow();
    probeAssert($identity['db']==='kaart_updater_probe' && $identity['role']==='updater_probe_app'
        && $identity['address']===null,'isolated connection identity');
    $phase=$mode;
    $command=new ProbeUpdateCommand('update',new CConsoleCommandRunner);
    $command->mode=$mode;
    if($mode==='hold') {
        probeAssert($command->run(array())===0,'holder exit');
        emitProbe(array('lockReleased'=>true));
    } elseif($mode==='blocked') {
        $before=file_get_contents($runtime.'/update.log');
        probeAssert($command->run(array())===75,'busy exit 75');
        probeAssert(file_get_contents($runtime.'/update.log')===$before,'busy checkpoint unchanged');
        $run=history($runtime)['runs'][0];
        probeAssert($run['outcome']==='skipped' && $run['counts']===null,'lock skip recorded');
        emitProbe(array('busyExit'=>75,'checkpointUnchanged'=>true,'skipRecorded'=>true));
    } elseif($mode==='fixture') {
        $api=new ProbeDgsApi;
        $app->setComponent('probeDgs',$api);
        $command->dgsapiComponentName='probeDgs';
        $map=$command->insertMap('EAA','UPDATERPROBE','1','1','1');
        $deletedUid='00000000-0000-4000-a000-000000000001';
        $command->insertImage($map,$deletedUid);
        $api->newRows=array(array('refcode'=>'EAA.UPDATERPROBE.1.2','page_no'=>'1',
            'uid'=>array('00000000-0000-4000-a000-000000000002')));
        $api->deleted=array($deletedUid);
        for($i=3;$i<6;$i++) {
            $id=$command->insertMap('EAA','UPDATERPROBE','1',(string)$i,'1');
            $command->updateMapDigitized($id);
        }
        $checkpoint=time()-3600;
        file_put_contents($runtime.'/update.log',(string)$checkpoint);
        $missingBefore=(int)$db->createCommand("SELECT count(*) FROM pilt WHERE uid IS NOT NULL AND (pisipilt IS NULL OR pisipilt='')")->queryScalar();
        probeAssert($command->run(array())===0,'successful command');
        probeAssert($api->intervals[0][0]===$checkpoint,'checkpoint used as interval start');
        probeAssert($command->getLastRuntime()>$checkpoint,'successful checkpoint advances');
        probeAssert((int)$db->createCommand("SELECT count(*) FROM pilt WHERE uid='$deletedUid'")->queryScalar()===0,'deleted image removed');
        probeAssert((int)$db->createCommand("SELECT count(*) FROM pilt WHERE uid='00000000-0000-4000-a000-000000000002'")->queryScalar()===1,'new map/image inserted');
        $stale=(int)$db->createCommand('SELECT count(*) FROM kaart t WHERE digiteeritud IS TRUE AND NOT EXISTS (SELECT 1 FROM pilt WHERE kaart_id=t.id)')->queryScalar();
        probeAssert($stale===0,'all empty maps lose digitized flag');
        $missingAfter=(int)$db->createCommand("SELECT count(*) FROM pilt WHERE uid IS NOT NULL AND (pisipilt IS NULL OR pisipilt='')")->queryScalar();
        probeAssert($missingAfter===max(0,$missingBefore-500),'missing thumbnails filled');
        $run=history($runtime)['runs'][0];
        probeAssert($run['outcome']==='completed' && $run['source']==='manual'
            && $run['intervalFrom']===$checkpoint && $run['checkpointAfter']===$command->getLastRuntime()
            && $run['counts']===array('dgsPages'=>1,'mapsAdded'=>1,'imagesAdded'=>1,'imagesRemoved'=>1,
                'thumbnailsSaved'=>$missingBefore-$missingAfter,'thumbnailFailures'=>0),'successful run counts');
        $lastAdditionAt=$run['finishedAt'];
        file_put_contents($runtime.'/update.log',(string)$checkpoint);
        $api->failDeleted=true;
        try { $command->run(array());throw new LogicException('Injected failure was not propagated.'); }
        catch(RuntimeException $error) { probeAssert($error->getMessage()==='injected deleted-image failure','expected transport failure'); }
        probeAssert($command->getLastRuntime()===$checkpoint,'failed checkpoint unchanged');
        $run=history($runtime)['runs'][0];
        probeAssert($run['outcome']==='failed' && $run['stage']==='deletions'
            && $run['checkpointAfter']===null,'failed stage and checkpoint recorded');
        $api->failDeleted=false;
        probeAssert($command->run(array())===0,'retry success');
        probeAssert((int)$db->createCommand("SELECT count(*) FROM pilt WHERE uid='00000000-0000-4000-a000-000000000002'")->queryScalar()===1,'retry does not duplicate image');
        probeAssert(history($runtime)['noAdditionsStreak']===1,'no additions after duplicate input');
        $api->newRows=array();
        $db->createCommand("UPDATE pilt SET pisipilt=NULL WHERE uid='00000000-0000-4000-a000-000000000002'")->execute();
        $command->mode='fixture-warning';
        putenv('TRIGGER_UNIT=kaardid-update.timer');
        try { probeAssert($command->run(array())===0,'thumbnail warning remains retryable'); }
        finally { putenv('TRIGGER_UNIT'); }
        $history=history($runtime);
        $run=$history['runs'][0];
        probeAssert($run===$history['lastScheduledRun'] && $run['source']==='timer'
            && $run['outcome']==='warning' && $run['stage']==='thumbnails'
            && $run['checkpointAfter']===$command->getLastRuntime()
            && $run['counts']['dgsPages']===0 && $run['counts']['thumbnailFailures']>0
            && $run['counts']['thumbnailsSaved']===0,'scheduled thumbnail warning and counts');
        probeAssert($history['noAdditionsStreak']===2 && $history['lastAdditionAt']===$lastAdditionAt,'quiet streak and last addition');
        emitProbe(array('copyWrites'=>true,'checkpointInterval'=>true,'checkpointAdvances'=>true,
            'failedCheckpointPreserved'=>true,'idempotentRetry'=>true,'allDigitizedFlagsClean'=>true,
            'structuredCounts'=>true,'failureRecorded'=>true,'scheduledWarningRecorded'=>true,'noAdditionsStreak'=>2,
            'thumbnailsFilled'=>$missingBefore-$missingAfter));
    } elseif($mode==='thumbnail-queue') {
        $cursorFile=$runtime.'/thumbnail-cursor.txt';
        $originalCursor=is_file($cursorFile) ? file_get_contents($cursorFile) : null;
        $transaction=$db->beginTransaction();
        try {
            // Connection-local table; never changes the restored images or a live database.
            $db->createCommand('CREATE TEMP TABLE pilt (id integer PRIMARY KEY, uid uuid, pisipilt text) ON COMMIT DROP')->execute();
            foreach(array(1=>null,2=>'',3=>'',4=>null,5=>'existing',6=>null) as $id=>$thumbnail)
                $db->createCommand()->insert('pilt',array('id'=>$id,
                    'uid'=>$id===6 ? null : sprintf('00000000-0000-0000-0000-%012d',$id),
                    'pisipilt'=>$thumbnail));
            file_put_contents($cursorFile,'0');
            foreach(array(array(1,2),array(3,4),array(1,2)) as $expected) {
                $batch=new ProbeUpdateCommand('update',new CConsoleCommandRunner);
                $batch->mode='thumbnail-queue';
                $batch->saveMissingThumbs(2);
                probeAssert($batch->thumbnailAttempts===$expected,'bounded rotation persists across command restarts');
            }
            probeAssert((int)$db->createCommand("SELECT count(*) FROM pilt WHERE id IN (3,4) AND pisipilt=:thumb")
                ->queryScalar(array(':thumb'=>base64_encode('queue fixture thumbnail')))===2,'NULL and empty thumbnails repaired behind failures');
            $batch=new ProbeUpdateCommand('update',new CConsoleCommandRunner);
            $batch->mode='thumbnail-queue';
            $batch->failedThumbnailIds=array(2);
            $batch->saveMissingThumbs(500);
            probeAssert($batch->thumbnailAttempts===array(1,2),'each failed image retried once after recovery');
            probeAssert($db->createCommand('SELECT pisipilt FROM pilt WHERE id=1')->queryScalar()===base64_encode('queue fixture thumbnail'),'recovered thumbnail saved');
            probeAssert($db->createCommand('SELECT pisipilt FROM pilt WHERE id=5')->queryScalar()==='existing','stored thumbnail unchanged');
        } finally {
            $transaction->rollback();
            if($originalCursor===null) unlink($cursorFile);
            else file_put_contents($cursorFile,$originalCursor);
        }
        emitProbe(array('nullAndEmptyRepaired'=>true,'fullFailureBatchYields'=>true,
            'cursorSurvivesRestarts'=>true,'failuresRetried'=>true,'storedAndMissingUidSkipped'=>true));
    } elseif($mode==='external') {
        $result=array('dgs'=>false,'soap'=>false);
        try {
            $rows=$command->getNewMapData(time()-3600,time());
            $deleted=$command->getDeletedImages(time()-3600,time());
            probeAssert(!isset($rows['error']) && !isset($deleted['error']),'DGS interval responses');
            $result['dgs']=true;$result['mapRows']=count($rows);$result['deletedRows']=count($deleted);
        } catch(Throwable $error) {
            $result['dgsErrorClass']=get_class($error);
            if(preg_match('/returned error: (\d{3})/',$error->getMessage(),$match)) $result['dgsHttp']=(int)$match[1];
        }
        try {
            $soap=new SoapClient($app->params['binServicesUrl'],array('connection_timeout'=>10,'cache_wsdl'=>WSDL_CACHE_NONE));
            $uid=$db->createCommand('SELECT uid FROM pilt WHERE uid IS NOT NULL LIMIT 1')->queryScalar();
            $bytes=$soap->getFileContents(null,$uid,100,100,90);
            $result['soap']=is_string($bytes) && strlen($bytes)>0;
            $result['thumbnailBytes']=is_string($bytes)?strlen($bytes):0;
        } catch(Throwable $error) { $result['soapErrorClass']=get_class($error); }
        emitProbe($result);
    } elseif($mode==='live') {
        $before=$command->getLastRuntime();
        probeAssert($command->run(array())===0,'live command exit');
        probeAssert($command->getLastRuntime()>$before,'live checkpoint advance');
        $run=history($runtime)['runs'][0];
        probeAssert(in_array($run['outcome'],array('completed','warning'),true)
            && $run['checkpointAfter']===$command->getLastRuntime(),'live summary recorded');
        emitProbe(array('liveUpdaterCompleted'=>true,'checkpointAdvanced'=>true,
            'outcome'=>$run['outcome'],'counts'=>$run['counts']));
    } else throw new RuntimeException('Unknown probe mode.');
} catch(Throwable $error) {
    // Do not expose copied rows, configuration, request payloads or exception traces.
    echo json_encode(array('ok'=>false,'phase'=>$phase,'errorClass'=>get_class($error),
        'check'=>$error instanceof LogicException?$error->getMessage():null,
        'source'=>basename($error->getFile()).':'.$error->getLine()))."\n";
    exit(1);
}

function probeAssert($condition,$label) { if(!$condition) throw new LogicException($label); }
function emitProbe($result) { echo json_encode(array('ok'=>true,'result'=>$result))."\n"; }
function history($runtime) { return json_decode(file_get_contents($runtime.'/updater-runs.json'),true,512,JSON_THROW_ON_ERROR); }
