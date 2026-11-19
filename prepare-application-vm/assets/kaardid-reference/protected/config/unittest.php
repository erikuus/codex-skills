<?php

return CMap::mergeArray(
	require(dirname(__FILE__).'/test.php'),
	array(
		'components'=>array(
			'assetManager'=>array(
				'basePath'=>dirname(__FILE__).'/../tests/assets',
				'baseUrl'=>'/assets',
			),
			'fixture'=>array(
				'class'=>'system.test.CDbFixtureManager',
				'basePath'=>dirname(__FILE__).'/../tests/fixtures',
			),
			'mockDgsApiEmptyMapData'=> array(
				'class'=>'application.tests.components.MockDgsApi',
				'url'=>'SaveEmptyMapData.php'
			),
			'mockDgsApiNewMapData'=> array(
				'class'=>'application.tests.components.MockDgsApi',
				'url'=>'SaveNewMapData.php'
			),
			'mockDgsApiNewImageData'=> array(
				'class'=>'application.tests.components.MockDgsApi',
				'url'=>'SaveNewImageData.php'
			),
			'log'=>array(
				'class'=>'CLogRouter',
				'routes'=>array(
					array(
						'class'=>'CFileLogRoute',
						'logFile'=>'test_update_trace.log',
						'levels'=>'trace',
						'categories'=>'update',
						'logPath'=>dirname(__FILE__).'/../runtime'
					),
				),
			),
		),
	)
);
