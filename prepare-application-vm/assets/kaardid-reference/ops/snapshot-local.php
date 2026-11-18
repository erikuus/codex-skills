<?php
// Private rehearsal snapshot of kaart_dev. Never copies local configuration files.
umask(0077);
if (PHP_SAPI !== 'cli' || $argc !== 2 || !is_dir($argv[1])) {
    fwrite(STDERR, "Usage: php ops/snapshot-local.php <existing private output directory>\n");
    exit(2);
}
$output = realpath($argv[1]);
if (file_exists($output.'/kaart_dev.dump') || file_exists($output.'/manifest.json')) {
    throw new RuntimeException('Snapshot destination already contains an artifact; refusing to overwrite it.');
}
$repo = dirname(__DIR__);
$framework = dirname($repo, 2).'/yii/yii-1.1.33-dev/yii.php';
require $framework;
$config = require $repo.'/protected/config/development.php';
$db = $config['components']['db'];
$pdo = new PDO($db['connectionString'], $db['username'], $db['password'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->beginTransaction();
$pdo->exec('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY');
$identity = $pdo->query("SELECT current_database() AS database, current_setting('server_version_num') AS version_num, pg_database_size(current_database()) AS bytes")->fetch(PDO::FETCH_ASSOC);
if ($identity['database'] !== 'kaart_dev' || (int)$identity['version_num'] < 170000 || (int)$identity['version_num'] >= 180000) {
    throw new RuntimeException('Expected the local PostgreSQL 17 kaart_dev database.');
}
if (!preg_match('/(?:^|;)host=([^;]+)/', substr($db['connectionString'], 6), $hostMatch)) {
    throw new RuntimeException('Explicit source host is required.');
}
$host = $hostMatch[1];
if (!in_array($host, ['localhost', '127.0.0.1', '::1'], true)) {
    throw new RuntimeException('This rehearsal snapshot must originate on this Mac.');
}
preg_match('/(?:^|;)port=([0-9]+)/', substr($db['connectionString'], 6), $portMatch);
$port = $portMatch[1] ?? '5432';
$snapshot = $pdo->query('SELECT pg_export_snapshot()')->fetchColumn();
$tables = $pdo->query("SELECT n.nspname AS schema,c.relname AS name FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname IN ('public','au') AND c.relkind='r' AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.classid='pg_class'::regclass AND d.objid=c.oid AND d.deptype='e') ORDER BY 1,2")->fetchAll(PDO::FETCH_ASSOC);
foreach ($tables as &$table) {
    $identifier = '"'.str_replace('"', '""', $table['schema']).'"."'.str_replace('"', '""', $table['name']).'"';
    $table['rows'] = $table['schema'] === 'public' && $table['name'] === 'tbl_session'
        ? 0 : (int)$pdo->query('SELECT count(*) FROM '.$identifier)->fetchColumn();
}
unset($table);
$manifest = [
    'purpose' => 'private-rehearsal', 'source' => $identity, 'created_utc' => gmdate('c'),
    'schemas' => ['public', 'au'], 'excluded_data' => ['public.tbl_session'], 'tables' => $tables,
    'extensions' => $pdo->query('SELECT extname,extversion FROM pg_extension ORDER BY extname')->fetchAll(PDO::FETCH_ASSOC),
];
$manifest['unused_legacy_shell_types'] = $pdo->query("SELECT n.nspname AS schema,t.typname AS name FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='public' AND t.typname='histogram2d' AND NOT t.typisdefined AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.refclassid='pg_type'::regclass AND d.refobjid=t.oid)")->fetchAll(PDO::FETCH_ASSOC);
$spatialCondition = $pdo->query("SELECT extcondition[1] FROM pg_extension WHERE extname='postgis'")->fetchColumn();
$manifest['custom_spatial_reference_rows'] = (int)$pdo->query('SELECT count(*) FROM public.spatial_ref_sys '.($spatialCondition ?: ''))->fetchColumn();
$manifest['unused_legacy_gist_aliases'] = $pdo->query("SELECT 'public' AS schema,c.opcname AS name FROM pg_opclass c JOIN pg_opfamily f ON f.oid=c.opcfamily WHERE c.opcnamespace='public'::regnamespace AND c.opcname='gist_geometry_ops' AND NOT c.opcdefault AND NOT EXISTS (SELECT 1 FROM pg_index i WHERE c.oid=ANY(i.indclass)) AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.refclassid='pg_opclass'::regclass AND d.refobjid=c.oid AND d.classid NOT IN ('pg_amproc'::regclass,'pg_amop'::regclass)) AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.refclassid='pg_opfamily'::regclass AND d.refobjid=f.oid AND d.classid NOT IN ('pg_opclass'::regclass,'pg_amproc'::regclass,'pg_amop'::regclass)) AND (SELECT count(*) FROM pg_opclass x WHERE x.opcfamily=f.oid)=1 AND NOT EXISTS (SELECT 1 FROM pg_proc p WHERE p.pronamespace='public'::regnamespace AND p.prokind IN ('f','p') AND p.prosrc LIKE '%gist_geometry_ops%')")->fetchAll(PDO::FETCH_ASSOC);
$passfile = tempnam(sys_get_temp_dir(), 'kaardid-pgpass-');
chmod($passfile, 0600);
register_shutdown_function(static function () use ($passfile) { if (is_file($passfile)) unlink($passfile); });
$escape = static fn($value) => str_replace(['\\', ':'], ['\\\\', '\\:'], $value);
file_put_contents($passfile, implode(':', array_map($escape, [$host, $port, 'kaart_dev', $db['username'], $db['password']]))."\n");
$command = [
    $repo.'/bin/pg17', 'pg_dump', '--format=custom', '--compress=6', '--no-owner', '--no-acl',
    '--host='.$host, '--port='.$port, '--username='.$db['username'], '--dbname=kaart_dev',
    '--schema=public', '--schema=au', '--exclude-table-data=public.tbl_session',
    '--snapshot='.$snapshot, '--file='.$output.'/kaart_dev.dump', '--no-password',
];
$process = proc_open($command, [0 => ['file', '/dev/null', 'r'], 1 => ['file', '/dev/null', 'w'],
    2 => ['file', $output.'/pg_dump.log', 'w']], $pipes, $repo,
    ['PATH' => '/usr/bin:/bin', 'LANG' => 'C', 'PGPASSFILE' => $passfile, 'PGCONNECT_TIMEOUT' => '10', 'PGAPPNAME' => 'kaardid-rehearsal-snapshot']);
if (!is_resource($process) || proc_close($process) !== 0) {
    throw new RuntimeException('Snapshot failed. Inspect the private pg_dump.log; no import was attempted.');
}
$pdo->commit();
unlink($passfile);
$manifest['dump_sha256'] = hash_file('sha256', $output.'/kaart_dev.dump');
$manifest['dump_bytes'] = filesize($output.'/kaart_dev.dump');
file_put_contents($output.'/manifest.json', json_encode($manifest, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES)."\n");
echo json_encode(['snapshot_directory' => $output, 'source' => 'kaart_dev', 'tables' => count($tables),
    'session_rows_copied' => 0, 'dump_bytes' => $manifest['dump_bytes'], 'dump_sha256' => $manifest['dump_sha256']], JSON_PRETTY_PRINT), "\n";
