<?php

return array(
	'components'=>array(
		'log'=>array(
			'class'=>'CLogRouter',
			'routes'=>array(
				array(
					'class'=>'ext.components.log.XSentryLogRoute',
					'levels'=>'error',
					'dsn'=>getenv('SENTRY_DSN') ?: null,
					'environment'=>getenv('SENTRY_ENVIRONMENT') ?: 'prod',
					'release'=>getenv('SENTRY_RELEASE') ?: '<app>-prod',
					'serverName'=>getenv('SENTRY_SERVER_NAME') ?: php_uname('n'),
					'sampleRate'=>1.0,
					'sendDefaultPii'=>false,
					'includeUserContext'=>false,
					'includeRequestContext'=>true,
					'ignoreCategories'=>array(
						'exception.CHttpException.400',
						'exception.CHttpException.401',
						'exception.CHttpException.403',
						'exception.CHttpException.404',
					),
					'ignoreHttpStatusCodes'=>array(400, 401, 403, 404),
					'throttleWindowSeconds'=>900,
					'throttleMaxInitialEvents'=>1,
					'summaryThreshold'=>25,
					'cacheID'=>'cache',
				),
			),
		),
		'cache'=>array(
			'class'=>'CDbCache',
		),
	),
);
