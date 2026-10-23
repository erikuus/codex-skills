<?php
/** Isolated, strict framework probe; no app config or external DB writes. */
if (PHP_SAPI !== 'cli' || $argc < 2 || $argc > 3) {
    fwrite(STDERR, "Usage: php smoke_framework.php <framework-dir> [yii.php|yiilite.php]\n");
    exit(2);
}
$framework = realpath($argv[1]);
$bootstrap = $argv[2] ?? 'yii.php';
if (!$framework || !in_array($bootstrap, ['yii.php', 'yiilite.php'], true)
    || !is_file($framework . '/' . $bootstrap)) {
    fwrite(STDERR, "Invalid framework directory/bootstrap.\n");
    exit(2);
}
error_reporting(E_ALL);
ini_set('display_errors', '1');
define('YII_ENABLE_ERROR_HANDLER', false);
define('YII_ENABLE_EXCEPTION_HANDLER', false);
set_error_handler(static function ($severity, $message, $file, $line) {
    // Intentionally include @-suppressed messages in this isolated smoke test.
    throw new ErrorException($message, 0, $severity, $file, $line);
});
function checkSmoke($condition, $label) {
    if (!$condition) {
        throw new RuntimeException('Failed: ' . $label);
    }
}

try {
    require $framework . '/' . $bootstrap;
    checkSmoke(Yii::getVersion() === '1.1.33-dev', 'expected target version');
    $checks = ['bootstrap'];
    checkSmoke(CMap::mergeArray(['a' => 1], ['b' => 2]) === ['a' => 1, 'b' => 2], 'CMap merge');
    $column = new CDbColumnSchema();
    $column->type = 'integer';
    checkSmoke($column->typecast('42') === 42, 'integer column conversion');
    $column->type = 'boolean';
    checkSmoke($column->typecast('1') === true, 'boolean column conversion');
    checkSmoke(CJavaScript::encode(42) === '42', 'JavaScript integer encoding');
    $checks[] = 'collections/schema/encoding';

    // No init/save: exercise assignment keys without a persistent auth file.
    $auth = new CPhpAuthManager();
    $auth->createRole('smokeReader');
    checkSmoke(!$auth->isAssigned('smokeReader', null), 'guest starts unassigned');
    $auth->assign('smokeReader', null);
    checkSmoke($auth->isAssigned('smokeReader', ''), 'null key retains empty-string semantics');
    checkSmoke(!$auth->isAssigned('smokeReader', 7), 'guest assignment does not grant user role');
    checkSmoke($auth->revoke('smokeReader', null), 'null-key revocation');
    $auth->assign('smokeReader', 7);
    checkSmoke($auth->isAssigned('smokeReader', '7'), 'numeric/string user key parity');
    $checks[] = 'RBAC assignment keys';

    // Register and round-trip a custom handler without touching disk sessions.
    class UpgradeSmokeSession extends CHttpSession {
        private $rows = [];
        public function getUseCustomStorage() { return true; }
        public function openSession($path, $name) { return true; }
        public function closeSession() { return true; }
        public function readSession($id) { return $this->rows[$id] ?? ''; }
        public function writeSession($id, $data) { $this->rows[$id] = $data; return true; }
        public function destroySession($id) { unset($this->rows[$id]); return true; }
        public function gcSession($maxLifetime) { return 0; }
    }
    ini_set('session.use_cookies', '0');
    session_cache_limiter('');
    $session = new UpgradeSmokeSession();
    $session->autoStart = false;
    $session->setSessionID('yii-upgrade-smoke');
    $session->open();
    checkSmoke(session_status() === PHP_SESSION_ACTIVE, 'session opens');
    $_SESSION['probe'] = 'preserved';
    $session->close();
    $_SESSION = [];
    $session->open();
    checkSmoke(($_SESSION['probe'] ?? null) === 'preserved', 'session round-trip');
    $session->destroy();
    $session->close();
    $checks[] = 'custom sessions';

    // No serializer cache: keep the probe read-only with respect to the framework.
    require_once $framework . '/vendors/htmlpurifier/HTMLPurifier.standalone.php';
    $purifier = new HTMLPurifier(['Cache.DefinitionImpl' => null]);
    $clean = $purifier->purify('<p>Hello <strong>world</strong><script>alert(1)</script></p>');
    checkSmoke(str_contains($clean, '<strong>world</strong>'), 'allowed HTML preserved');
    checkSmoke(!str_contains($clean, '<script'), 'script element removed');
    checkSmoke(HTMLPurifier::VERSION === '4.19.1', 'bundled HTMLPurifier version');
    $checks[] = 'HTMLPurifier';

    $skipped = [];
    if (class_exists('PDO') && in_array('sqlite', PDO::getAvailableDrivers(), true)) {
        $db = new CDbConnection('sqlite::memory:');
        $db->setActive(true);
        $db->createCommand('CREATE TABLE probe (id INTEGER PRIMARY KEY, label TEXT)')->execute();
        $db->createCommand()->insert('probe', ['id' => 1, 'label' => 'ok']);
        checkSmoke($db->createCommand('SELECT label FROM probe WHERE id=1')->queryScalar() === 'ok', 'SQLite round-trip');
        $db->setActive(false);
        $checks[] = 'SQLite';
    } else {
        $skipped[] = 'SQLite (pdo_sqlite unavailable)';
    }
    echo json_encode([
        'php' => PHP_VERSION, 'yii' => Yii::getVersion(), 'bootstrap' => $bootstrap,
        'passed' => $checks, 'skipped' => $skipped,
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
} catch (Throwable $error) {
    fwrite(STDERR, get_class($error) . ': ' . $error->getMessage() . "\n"
        . $error->getFile() . ':' . $error->getLine() . "\n");
    exit(1);
}
