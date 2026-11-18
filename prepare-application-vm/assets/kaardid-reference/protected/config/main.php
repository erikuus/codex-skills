<?php
require_once(__DIR__.'/Environment.php');
require_once(__DIR__.'/Maintenance.php');
$environment=KaardidEnvironment::settings();
$integrations=KaardidEnvironment::integrations();

$basePath=dirname(__FILE__).DIRECTORY_SEPARATOR.'..';
$extensionPath=$basePath.DIRECTORY_SEPARATOR.'extensions';

// Uncomment the following to define a path alias
Yii::setPathOfAlias('ptl',dirname(__FILE__).'/../portlets');

// This is the main Web application configuration. Any writable
// CWebApplication properties can be configured here.
return array(
	'catchAllRequest'=>KaardidMaintenance::catchAllRequest(),
	'basePath'=>dirname(__FILE__).DIRECTORY_SEPARATOR.'..',
	'extensionPath'=>dirname(__FILE__).'/../extensions',
	'name'=>$environment['name'],
	'theme'=>'joyful',
	'runtimePath'=>$environment['runtimePath'],
	'defaultController'=>'Site',
	'language'=>'et',
	'timeZone'=>'Europe/Tallinn',

	// home url, needed for multilinqual app
	'homeUrl'=>array('/site/index'),

	// preloading 'log' component
	'preload'=>array('log'),

	// block ip address
	'onBeginRequest' => array('IpBlockFilter', 'applyFilter'),

	// autoloading model and component classes
	'import'=>array(
		'application.models.*',
		'application.models.behaviors.*',
		'application.components.*',
		'ext.components.tailwind.*',
		'ext.validators.*',
		'ext.filters.*',
		'ext.modules.help.models.*',
		'ext.modules.lookup.models.*',
		'ext.modules.au.models.*',
		'ext.helpers.*',
		'ext.widgets.portlet.XPortlet',
		'ext.components.database.XDbCriteria',
	),

	// modules
	'modules'=>array(
		'haldusyksused'=>array('class'=>'application.modules.haldusyksused.HaldusyksusedModule'),
		'lookup'=>array(
			'class'=>'ext.modules.lookup.LookupModule',
			'lookupLayout'=>'//layouts/leftbar',
			'lookupTable'=>'lookup',
			'messageCategory'=>'lu',
			'safeTypes'=>array(
				'teema',
				'kaart_vorm',
				'kaart_alusmaterjal',
				'kaart_originaalsus',
				'kaart_valmistusviis',
				'sailik_vorm',
				'sailik_vorm',
				'seose_liik',
				'kaardi_isik_roll'
			),
			'leftPortlets'=>array(
				'ptl.AdminMenu'=>array()
			),
			'buttonColumnClass'=>'ext.components.foundation.widgets.XFButtonColumn',
			'reorderColumnClass'=>'ext.components.foundation.widgets.XFReorderColumn',
			'rbac'=>'admin'
		),
		'help'=>array(
			'class'=>'ext.modules.help.HelpModule',
			'helpLayout'=>'//layouts/leftbar',
			'helpTable'=>'help',
			'leftPortlets'=>array(
				'ptl.AdminMenu'=>array()
			),
			'editorCSS'=>'editor.css',
			'uploadFile'=>'/request/uploadRedactorFile',
			'uploadImage'=>'/request/uploadRedactorImage',
			'buttonColumnClass'=>'ext.components.foundation.widgets.XFButtonColumn',
			'editOnPage'=>false,
			'rbac'=>'admin'
		),

		'au'=>array(
			'class'=>'ext.modules.au.AuModule',
			'auLayout'=>'//layouts/leftbar',
			'leftPortlets'=>array('ptl.AdminMenu'=>array()),
		),
	),

	// application components
	'components'=>array(
		'themeManager'=>array('basePath'=>dirname(__FILE__).'/../../themes'),
		'log'=>array(
			'class'=>'CLogRouter',
			'routes'=>array(
				array(
					'class' => 'application.components.LogRoute',
					//'class'=>'CFileLogRoute',
					'levels'=>'error',
					'logFile'=>'error.log',
				),
				array(
					'class'=>'CFileLogRoute',
					'levels'=>'warning',
					'logFile'=>'warning.log',
				),
			),
		),
		'dgsapi'=>array('class'=>'ext.components.dgsapi.XDgsApi','url'=>$environment['dgsApiUrl']),
		'assetManager'=>array('basePath'=>$environment['assetsPath'],'newDirMode'=>02750,'newFileMode'=>0640),
		'user' => array(
			'class' => 'WebUser',
			'authTimeout' => 2700, // 45 minutes of inactivity
		),
		'errorHandler'=>array(
			'errorAction'=>(defined('YII_DEBUG') && YII_DEBUG) ? null : 'site/error',
		),
		'coreMessages'=>array(
			'basePath'=>'protected/messages',
		),
		'clientScript'=>array(
			'scriptMap'=>array(
				'jquery-ui.css'=>rtrim(dirname($_SERVER['SCRIPT_NAME']), '/').'/css/yiithemes/jui/silver/jquery-ui.css',
				'jquery.treeview.async.js'=>rtrim(dirname($_SERVER['SCRIPT_NAME']), '/').'/js/jquery.treeview.async.js',
			),
		),
		'widgetFactory'=>array(
			'enableSkin'=>true,
			'skinPath'=>$extensionPath.DIRECTORY_SEPARATOR.'skins'.DIRECTORY_SEPARATOR.'silver',
		),
		'urlManager'=>array(
			'class'=>'ext.components.language.XUrlManager',
			'urlFormat'=>'path',
			'showScriptName'=>true,
			'appendParams'=>false,
			'rules'=>array(
				'<language:\w{2}>'=>'site/index',
				'<language:\w{2}>/<_c:\w+>'=>'<_c>',
				'<language:\w{2}>/<_c:\w+>/<_a:\w+>'=>'<_c>/<_a>',
				'<language:\w{2}>/<_m:\w+>'=>'<_m>',
				'<language:\w{2}>/<_m:\w+>/<_c:\w+>'=>'<_m>/<_c>',
				'<language:\w{2}>/<_m:\w+>/<_c:\w+>/<_a:\w+>'=>'<_m>/<_c>/<_a>',
			),
		),
		'session'=>getenv('SENTRY_VERIFY_LOCAL') ? array(
			'sessionName'=>'KAARTSESSION',
			'class'=>'CHttpSession',
			'timeout'=>3600,
		) : array(
			'sessionName'=>'KAARTSESSION',
			'class'=>'DbHttpSession',
			'connectionID'=>'db',
			'sessionTableName'=>'tbl_session',
			'autoCreateSessionTable'=>false,
			'timeout'=>3600, // Storage retention outlasts the authentication deadline.
		),
		'vauSecurityManager'=> array(
			'class'=>'ext.components.vauid.XVauSecurityManager',
			'validationKey'=>$integrations['vauValidationKey'],
			'version'=>2.1,
		),
	),

	// application-level parameters that can be accessed
	// using Yii::app()->params['paramName']
	'params'=>require(dirname(__FILE__).'/params.php'),
);
