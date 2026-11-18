<?php
require_once(__DIR__.'/Environment.php');
$environment=KaardidEnvironment::settings();
$integrations=KaardidEnvironment::integrations();
return array_replace(array(
    'pageSize' => 20,
    'sessionTimeoutCountdown' => 60,
    'vauBookmark' => true,
    'vauHelpdesk' => true,
    'analytics' => $environment['analytics'],
    'analyticsTracker' => 'f42c9956-53db-44c1-a779-be986f3c7a3a',
    'externalCallbackBaseUrl' => $environment['externalCallbackBaseUrl'],
    'aisServicesUrl' => 'http://www.ra.ee/services/index.php?r=ais/service',
    'binServicesUrl' => 'http://www.ra.ee/services/index.php?r=bin/service',
    'vauLoginServiceUrl' => 'https://www.ra.ee/vau/index.php/site/login?v=2.1&s=user_role&remoteUrl=',
    'vauLogoutServiceUrl' => 'https://www.ra.ee/vau/index.php/site/logout?remoteUrl=',
    'vauOrderUrl' => 'https://www.ra.ee/vau/index.php/et/order/index?scope=clientDraft&ref=',
    'adminVauId' => 1,
    'imageSignatureSecret' => $integrations['imageSignatureSecret'],
    'downloadSignatureExpiry' => 86400,
    'downloadRateLimit' => 10,
    'downloadRateWindow' => 300,
    'legacyBasePaths' => array(
        '/kaardid',
    ),
),$environment['params']);
