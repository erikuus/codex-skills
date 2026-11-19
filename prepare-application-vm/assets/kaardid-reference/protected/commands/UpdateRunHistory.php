<?php

/** Bounded, sanitized updater receipts shared with the read-only VM status check. */
class UpdateRunHistory
{
    public const COUNTS = array(
        'dgsPages', 'mapsAdded', 'imagesAdded', 'imagesRemoved', 'thumbnailsSaved', 'thumbnailFailures',
    );

    public static function append($runtime, array $run)
    {
        $path=$runtime.'/updater-runs.json';
        $lockPath=$runtime.'/updater-runs.lock';
        $mask=umask(0007);
        try { $lock=is_link($lockPath) ? false : @fopen($lockPath,'c'); }
        finally { umask($mask); }
        if($lock===false)
            throw new RuntimeException('Could not open the updater history lock.');
        try
        {
            $info=fstat($lock);
            if(($info['mode']&0170000)!==0100000 || ($info['mode']&0007) || !flock($lock,LOCK_EX))
                throw new RuntimeException('Could not lock updater history.');
            $history=array('version'=>1,'runs'=>array(),'lastScheduledRun'=>null,
                'lastAdditionAt'=>null,'lastCheckpointAt'=>null,'noAdditionsStreak'=>null);
            if(is_link($path))
                throw new RuntimeException('Unsafe updater history path.');
            if(file_exists($path))
            {
                $stored=json_decode(file_get_contents($path),true,512,JSON_THROW_ON_ERROR);
                if(($stored['version']??null)!==1 || !is_array($stored['runs']??null))
                    throw new RuntimeException('Unsupported updater history.');
                $history=$stored;
            }
            if($run['source']==='timer')
                $history['lastScheduledRun']=$run;
            if($run['checkpointAfter']!==null)
                $history['lastCheckpointAt']=$run['checkpointAfter'];
            if(in_array($run['outcome'],array('completed','warning'),true))
            {
                if($run['counts']['mapsAdded']>0 || $run['counts']['imagesAdded']>0)
                {
                    $history['lastAdditionAt']=$run['finishedAt'];
                    $history['noAdditionsStreak']=0;
                }
                else
                    $history['noAdditionsStreak']=($history['noAdditionsStreak']??0)+1;
            }
            elseif($run['outcome']==='failed')
                $history['noAdditionsStreak']=null;
            array_unshift($history['runs'],$run);
            $history['runs']=array_slice($history['runs'],0,7);

            $temporary=tempnam($runtime,'.updater-runs-');
            if($temporary===false)
                throw new RuntimeException('Could not stage updater history.');
            try
            {
                $contents=json_encode($history,JSON_THROW_ON_ERROR)."\n";
                if(dirname($temporary)!==$runtime
                    || file_put_contents($temporary,$contents)!==strlen($contents)
                    || !chmod($temporary,0640) || !rename($temporary,$path))
                    throw new RuntimeException('Could not save updater history.');
            }
            finally { if(is_file($temporary)) unlink($temporary); }
        }
        finally { fclose($lock); }
    }
}
