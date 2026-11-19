<?php
// Run with: php -S localhost:8000 dev-router.php
// The built-in server does not apply nginx's private-directory restrictions.
$path=rawurldecode(explode('?',$_SERVER['REQUEST_URI'],2)[0]);
$path=preg_replace('~/+~','/',$path);
if($path==='' || $path[0]!=='/' || preg_match('~(?:^|/)\.|^/(?:protected|ops|bin|node_modules|test-results|playwright-report)(?:/|$)~i',$path))
{
    http_response_code(404);
    header('Content-Type: text/plain; charset=utf-8');
    echo "Not found\n";
    return true;
}

// PHP's development server ignores Range on static files. Allow video seeking locally.
if($_SERVER['REQUEST_METHOD']==='GET'
    && preg_match('~^/upload/videos/[a-z0-9_-]+\.mp4$~D', $path)
    && !isset($_SERVER['HTTP_IF_RANGE'])
    && preg_match('~^bytes=(\d*)-(\d*)$~D', $_SERVER['HTTP_RANGE'] ?? '', $range)
    && ($range[1]!=='' || $range[2]!==''))
{
    $file=__DIR__.$path;
    if(!is_file($file) || !is_readable($file) || ($video=fopen($file, 'rb'))===false)
        return false;

    $size=fstat($video)['size'];
    $start=$range[1]==='' ? max(0, $size-(int)$range[2]) : (int)$range[1];
    $end=$range[1]==='' || $range[2]==='' ? $size-1 : min($size-1, (int)$range[2]);

    header('Accept-Ranges: bytes');
    if($start>$end)
    {
        http_response_code(416);
        header('Content-Range: bytes */'.$size);
        header('Content-Length: 0');
    }
    else
    {
        $length=$end-$start+1;
        http_response_code(206);
        header('Content-Type: video/mp4');
        header("Content-Range: bytes $start-$end/$size");
        header('Content-Length: '.$length);
        $output=fopen('php://output', 'wb');
        stream_copy_to_stream($video, $output, $length, $start);
        fclose($output);
    }
    fclose($video);
    return true;
}

return false;
