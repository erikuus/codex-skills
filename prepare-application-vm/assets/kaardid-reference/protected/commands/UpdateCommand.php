<?php
require_once __DIR__.'/UpdateRunHistory.php';

/**
 * Saves new map data and missing thumbnails
 *
 * Run with cron.php update; VM scheduling is managed in ops/systemd/.
 * The runtime/update.log checkpoint must be installed deliberately at handover.
 */

class UpdateCommand extends CConsoleCommand
{
	public $dgsapiComponentName='dgsapi';

	public $unit;
	public $fond;
	public $inventory;
	public $item;

	private $_trace=true;
	private $_soapClient;
	private $_run;

	public function run($args)
	{
		$runtime=Yii::app()->runtimePath;
		$path=$runtime.'/operations.lock';
		$this->_run=array(
			'startedAt'=>time(),
			'source'=>getenv('TRIGGER_UNIT')==='kaardid-update.timer'?'timer':'manual',
			'outcome'=>'failed',
			'stage'=>'lock',
			'intervalFrom'=>null,
			'checkpointAfter'=>null,
			'counts'=>null,
		);
		$lock=false;
		$failure=null;
		try
		{
			if(is_link($path))
				throw new RuntimeException('Unsafe updater/deployment lock.');
			$mask=umask(0007);
			try { $lock=@fopen($path,'c'); }
			finally { umask($mask); }
			if($lock===false)
				throw new RuntimeException('Cannot open updater/deployment lock.');
			$info=fstat($lock);
			if(($info['mode']&0170000)!==0100000 || ($info['mode']&0007))
				throw new RuntimeException('Unsafe updater/deployment lock permissions.');
			if(!flock($lock,LOCK_EX|LOCK_NB))
			{
				$this->_run['outcome']='skipped';
				fwrite(STDERR,"Updater skipped: another updater or deployment holds the lock.\n");
				return 75;
			}
			$this->_run['counts']=array_fill_keys(UpdateRunHistory::COUNTS,0);
			ini_set('memory_limit','2G');
			$this->syncMapData();
			$this->_run['stage']='thumbnails';
			$this->saveMissingThumbs(500);
			$this->_run['outcome']=$this->_run['counts']['thumbnailFailures']>0?'warning':'completed';
			$this->_run['stage']=$this->_run['outcome']==='warning'?'thumbnails':null;
			return 0;
		}
		catch(Throwable $error)
		{
			$failure=$error;
			throw $error;
		}
		finally
		{
			try
			{
				$this->_run['finishedAt']=time();
				UpdateRunHistory::append($runtime,$this->_run);
			}
			catch(Throwable $error)
			{
				if($failure===null && $this->_run['outcome']!=='skipped')
					throw new RuntimeException('Could not record updater outcome.',0,$error);
				fwrite(STDERR,"Could not record updater outcome.\n");
			}
			finally
			{
				$this->_run=null;
				if($lock!==false) fclose($lock);
			}
		}
	}

	public function syncMapData()
	{
		$runtime=time();
		if($this->_run!==null) $this->_run['stage']='checkpoint';
		$lastRuntime=$this->getLastRuntime();

		if($this->_run!==null)
		{
			$this->_run['intervalFrom']=$lastRuntime;
			$this->_run['stage']='additions';
		}
		$this->addNewMapData($lastRuntime, $runtime);
		if($this->_run!==null) $this->_run['stage']='deletions';
		$this->cleanUpMapData($lastRuntime, $runtime);

		if($this->_run!==null) $this->_run['stage']='checkpoint';
		$this->saveRuntime($runtime);
		if($this->_run!==null) $this->_run['checkpointAfter']=$runtime;
	}

	public function addNewMapData($lastRuntime, $runtime)
	{
		$rows=$this->getNewMapData($lastRuntime, $runtime);

		if(isset($rows['error']))
		{
			throw new RuntimeException('DGS map synchronization returned an error.');
		}
		else
		{
			if($this->_run!==null) $this->_run['counts']['dgsPages']=count($rows);
			foreach($rows as $row)
			{

				$mapId=$this->getMapId($row['refcode'], $row['page_no']);
				if($mapId)
					$this->insertImages($mapId, $row['uid']);
				else
				{
					$this->setRefcodeParts($row['refcode']);
					$mapId=$this->insertMap($this->unit, $this->fond, $this->inventory, $this->item, $row['page_no']);
					if($mapId)
						$this->insertImages($mapId, $row['uid']);
					else
						$this->trace("Id not returned saving ".$row['refcode']);
				}
			}
		}
	}

	public function cleanUpMapData($lastRuntime, $runtime)
	{
		$uids=$this->getDeletedImages($lastRuntime, $runtime);

		if(isset($uids['error']))
		{
			throw new RuntimeException('DGS deleted-image synchronization returned an error.');
		}
		else
		{
			foreach($uids as $uid)
				$this->deleteImage($uid);

			$this->cleanDigitized();
		}
	}

	public function getLastRuntime()
	{
		$file=Yii::app()->runtimePath.'/update.log';
		$value=is_file($file) ? @file_get_contents($file) : false;
		if($value===false || !preg_match('/^[0-9]{1,10}$/D',trim($value))
			|| (int)$value<1 || (int)$value>time())
			throw new RuntimeException('Missing or invalid update.log checkpoint; install a reviewed checkpoint before running the updater.');
		return (int)$value;
	}

	public function saveRuntime($runtime)
	{
		return $this->saveCheckpoint('update.log', (string)$runtime);
	}

	private function saveCheckpoint($name, $value)
	{
		$folder=Yii::app()->runtimePath;
		$temporary=@tempnam($folder,'.update-');
		if($temporary===false)
			throw new RuntimeException('Could not create updater checkpoint '.$name.'.');
		try
		{
			$result=@file_put_contents($temporary,$value,LOCK_EX);
			if(dirname($temporary)!==$folder || $result!==strlen($value)
				|| !@chmod($temporary,0660) || !@rename($temporary,$folder.'/'.$name))
				throw new RuntimeException('Could not save updater checkpoint '.$name.'.');
			return $result;
		}
		finally { if(is_file($temporary)) unlink($temporary); }
	}

	/**
	 * @return for example:
	 * array(
	 *   array(
	 *     'refcode'=>'eaa.1424.1.130',
	 *     'page_no'=>'1',
	 *     'uid'=>array(
	 *       '411207d6-c5fa-50e7-b35d-56142e233dfd',
	 *       '11d2e968-e870-5702-a408-a30c7bc445ca',
	 *       '59124601-6272-5251-9a5e-66e664c0f48a',
	 *       '27c339d4-3007-5667-9c26-9b2b878710b8'
	 *     )
	 *   )
	 * )
	 */
	public function getNewMapData($startCreatedTime, $endCreatedTime)
	{
		try
		{
			$dgsapi=Yii::app()->getComponent($this->dgsapiComponentName);
			$response=$dgsapi->request('get-refcode-page-uid-by-interval', array(
				'startCreatedTime'=>$startCreatedTime,
				'endCreatedTime'=>$endCreatedTime,
				'applicationName'=>'kaardid'
			));
			return $this->normalizeSyncResponse($response);
		}
		catch(Exception $e)
		{
			Yii::log('Failed to get-refcode-page-uid-by-interval'.PHP_EOL.
				'startCreatedTime: '.$startCreatedTime.PHP_EOL.
				'endCreatedTime: '.$endCreatedTime.PHP_EOL.
				'errorMessage: '.$e->getMessage(),
				CLogger::LEVEL_ERROR
			);
			throw $e;
		}
	}

	public function getMapId($refcode, $page)
	{
		$refcode=mb_strtolower($refcode);
		$page=mb_strtolower($page);

		return Yii::app()->db->createCommand("
			SELECT id
			FROM kaart
			WHERE LOWER(refcode)='$refcode'
			AND LOWER(leht)='$page'
		")->queryScalar();
	}

	public function insertImages($mapId, $uids)
	{
		$digitized=false;
		foreach($uids as $uid)
		{
			if($this->insertImage($mapId, $uid) && $digitized===false)
				$digitized=$this->updateMapDigitized($mapId);
		}
	}

	public function insertImage($mapId, $uid)
	{
		$affected=0;
		if($this->_checkImageExists($mapId, $uid)===false)
		{
			$affected=Yii::app()->db->createCommand("
				INSERT INTO pilt (kaart_id, uid) VALUES ($mapId, '$uid')
			")->execute();
		}

		if($affected)
		{
			$id=Yii::app()->db->getLastInsertID('pilt_id_seq');
			if($this->_run!==null) $this->_run['counts']['imagesAdded']+=$affected;
			$this->trace("Insert IMAGE: $uid (mapId=$mapId)");
			return true;
		}
		else
			return false;
	}

	private function _checkImageExists($mapId, $uid)
	{
		return Yii::app()->db->createCommand("
			SELECT id
			FROM pilt
			WHERE kaart_id=$mapId
			AND uid='$uid'
		")->queryScalar();
	}

	public function updateMapDigitized($id)
	{
		$affected=Yii::app()->db->createCommand("
			UPDATE kaart
			SET digiteeritud=TRUE
			WHERE id=$id
		")->execute();

		if($affected)
		{
			$this->trace("Update MAP: digitized true (id=$id)");
			return true;
		}
		else
			return false;
	}

	public function setRefcodeParts($refcode)
	{
		$parts=explode('.', $refcode);
		if($this->_validateRefcodeParts($parts))
		{
			$this->unit=mb_strtoupper($parts[0]);
			$this->fond=$parts[1];
			$this->inventory=$parts[2];
			$this->item=$parts[3];
		}
	}

	private function _validateRefcodeParts($parts)
	{
		$valid=(count($parts)==4) ? true : false;
		foreach($parts as $part)
			$valid=$valid && $part;
		return $valid;
	}

	public function insertMap($unit, $fond, $inventory, $item, $page)
	{
		$affected=Yii::app()->db->createCommand("
			INSERT INTO kaart (yksus, fond, nimistu, sailik, leht, alternatiivne_id, digiteeritud, kirjeldatud)
			VALUES ('$unit', '$fond', '$inventory', '$item', '$page', '', false, false)
		")->execute();

		if($affected)
		{
			$id=Yii::app()->db->getLastInsertID('kaart_id_seq');
			if($this->_run!==null) $this->_run['counts']['mapsAdded']+=$affected;
			$this->trace("Insert MAP: $unit.$fond.$inventory.$item:$page (id=$id)");
			return $id;
		}
		else
			return false;
	}



	/**
	 * @return for example:
	 * array(
	 *   '411207d6-c5fa-50e7-b35d-56142e233dfd',
	 *   '11d2e968-e870-5702-a408-a30c7bc445ca',
	 *   '59124601-6272-5251-9a5e-66e664c0f48a',
	 *   '27c339d4-3007-5667-9c26-9b2b878710b8'
	 * )
	 */
	public function getDeletedImages($startTime, $endTime)
	{
		try
		{
			$dgsapi=Yii::app()->getComponent($this->dgsapiComponentName);
			$response=$dgsapi->request('get-deleted', array(
				'startCreatedTime'=>$startTime,
				'endCreatedTime'=>$endTime,
				'applicationName'=>'kaardid'
			));
			return $this->normalizeSyncResponse($response);
		}
		catch(Exception $e)
		{
			Yii::log('Failed to get-deleted'.PHP_EOL.
				'startCreatedTime: '.$startTime.PHP_EOL.
				'endCreatedTime: '.$endTime.PHP_EOL.
				'errorMessage: '.$e->getMessage(),
				CLogger::LEVEL_ERROR
			);
			throw $e;
		}
	}

	private function normalizeSyncResponse($response)
	{
		if(!is_array($response))
			throw new UnexpectedValueException('Invalid DGS synchronization response.');
		// The legacy API represents an empty interval with this specific error.
		if(isset($response['error'], $response['error_message']) &&
			(string)$response['error']==='1' && $response['error_message']==='Faile ei leitud')
			return array();
		return $response;
	}

	public function deleteImage($uid)
	{
		$affected=Yii::app()->db->createCommand("
			DELETE FROM pilt
			WHERE uid='$uid'
		")->execute();

		if($affected)
		{
			if($this->_run!==null) $this->_run['counts']['imagesRemoved']+=$affected;
			$this->trace("Delete IMAGE: $uid");
			return true;
		}
		else
			return false;
	}

	public function cleanDigitized()
	{
		$affected=Yii::app()->db->createCommand("
			UPDATE kaart t SET digiteeritud=FALSE
			WHERE t.digiteeritud IS TRUE
			AND NOT EXISTS (SELECT 1 FROM pilt WHERE kaart_id=t.id)
		")->execute();
		if($affected)
			$this->trace("Update MAP: digitized false ($affected maps)");
		return $affected>0;
	}

	public function saveMissingThumbs($limit)
	{
		if(!is_numeric($limit) || (int)$limit<1 || (int)$limit!=$limit)
			throw new InvalidArgumentException('Thumbnail batch limit must be a positive integer.');
		$cursorFile=Yii::app()->runtimePath.'/thumbnail-cursor.txt';
		$cursor=0;
		if(is_link($cursorFile))
			throw new RuntimeException('Unsafe thumbnail cursor.');
		if(file_exists($cursorFile))
		{
			$value=@file_get_contents($cursorFile);
			$cursor=$value===false ? false : filter_var(trim($value), FILTER_VALIDATE_INT, array('options'=>array('min_range'=>0)));
			if($cursor===false)
				throw new RuntimeException('Invalid thumbnail cursor; remove thumbnail-cursor.txt to restart the queue.');
		}

		$rows=Yii::app()->db->createCommand("
			SELECT id, uid
			FROM pilt
			WHERE uid IS NOT NULL
			AND (pisipilt IS NULL OR pisipilt='')
			ORDER BY CASE WHEN id>:cursor THEN 0 ELSE 1 END, id
			LIMIT ".(int)$limit
		)->queryAll(true, array(':cursor'=>$cursor));

		foreach($rows as $row)
		{
			// Persist before the service call so a failed/interrupted request yields its turn.
			// Ordering wraps around, retrying failures without starving later image IDs.
			$this->saveCheckpoint('thumbnail-cursor.txt', (string)$row['id']);
			$thumbFileContents=$this->_getThumbFileContents($row['uid']);
			if($thumbFileContents)
			{
				$base64Thumb=base64_encode($thumbFileContents);
				$this->updateImage($row['id'], $base64Thumb);
			}
			elseif($this->_run!==null)
				$this->_run['counts']['thumbnailFailures']++;
		}
	}

	protected function _getThumbFileContents($uid)
	{
		try
		{
			$contents=$this->_getSoapClient()->getFileContents(null, $uid, 100, 100, 90);
			return $contents;
		}
		catch(SoapFault $fault)
		{
			Yii::log('Failed to get thumbnail'.PHP_EOL.
				'uid: '.$uid.PHP_EOL.
				'errorMessage: '.$fault->faultstring,
				CLogger::LEVEL_ERROR
			);
			return false;
		}
	}

	protected function _getSoapClient()
	{
		if($this->_soapClient===null)
			$this->_soapClient=new SoapClient(Yii::app()->params['binServicesUrl']);

		return $this->_soapClient;
	}

	public function updateImage($id, $base64Thumb)
	{
		$affected=Yii::app()->db->createCommand("
			UPDATE pilt
			SET pisipilt='$base64Thumb'
			WHERE id=$id
		")->execute();

		if($affected)
		{
			if($this->_run!==null) $this->_run['counts']['thumbnailsSaved']+=$affected;
			$this->trace("Update IMAGE: set thumbnail (id=$id)");
			return true;
		}
		else
			return false;
	}

	public function deleteNotMaps()
	{
		$undescribedMaps=Yii::app()->db->createCommand("
			SELECT id, refcode, leht FROM kaart WHERE kirjeldatud IS FALSE
		")->queryAll();

		foreach($undescribedMaps as $undescribedMap)
		{
			$id=$undescribedMap['id'];
			$refcode=$undescribedMap['refcode'];
			$page=$undescribedMap['leht'];

			try
			{
				$response=Yii::app()->dgsapi->request('get-unique-identifier', array(
					'fnsRefcode'=>$refcode,
					'pages'=>$page,
					'applicationName'=>'kaardid'
				));

				if(isset($response['error']))
				{
					echo "$refcode $page\n";

					$affected=Yii::app()->db->createCommand("
						DELETE from kaart
						WHERE id=$id
					")->execute();

					if($affected)
						$this->trace("Delete Not Map: deleted ($refcode $page)");
				}
			}
			catch(Exception $e)
			{
				$this->trace("Delete Not Map: get-unique-identifier exception ($refcode $page)");
			}
		}
	}

	public function trace($message)
	{
		if($this->_trace===true)
			Yii::log($message,CLogger::LEVEL_TRACE,'update');
		else
			echo $message."\n";
	}
}
