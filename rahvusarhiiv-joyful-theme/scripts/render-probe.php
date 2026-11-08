<?php
/** Render the real bundled Yii layout, skins and widgets without an application database. */
if($argc!==3)
	throw new RuntimeException('Usage: php render-probe.php /path/to/yii.php /absolute/output.html');
define('YII_ENABLE_EXCEPTION_HANDLER',false);
define('YII_ENABLE_ERROR_HANDLER',false);
require $argv[1];
$skill=dirname(__DIR__);
$root=$skill.'/assets/app';
$temporary=sys_get_temp_dir().'/joyful-probe-'.getmypid();
mkdir($temporary);
mkdir($temporary.'/assets');
$_SERVER['SCRIPT_FILENAME']=$root.'/index.php';
$_SERVER['SCRIPT_NAME']='/index.php';
$_SERVER['REQUEST_URI']='/index.php';
$_SERVER['HTTP_HOST']='localhost';
$app=Yii::createWebApplication(array(
	'basePath'=>$temporary,
	'name'=>'Application',
	'aliases'=>array('ext'=>$skill.'/assets/extensions'),
	'import'=>array('ext.components.tailwind.*'),
	'theme'=>'joyful',
	'components'=>array(
		'themeManager'=>array('basePath'=>$root.'/themes','baseUrl'=>'/themes'),
		'assetManager'=>array('basePath'=>$temporary.'/assets','baseUrl'=>'/assets'),
		'widgetFactory'=>array('enableSkin'=>true),
	),
));
class JoyfulProbeController extends CController
{
	public $breadcrumbs=array('Records'=>array('/probe/index'),'Current record');
	public function actionIndex()
	{
	}
}
$controller=new JoyfulProbeController('probe');
$controller->action=$controller->createAction('index');
$app->controller=$controller;
$data=array();
for($i=1;$i<=12;$i++)
	$data[]=array('id'=>$i,'name'=>'Record '.$i,'description'=>'Representative table content');
$provider=new CArrayDataProvider($data,array('pagination'=>array('pageSize'=>5,'route'=>'/probe/index')));
$grid=$controller->widget('zii.widgets.grid.CGridView',array(
	'id'=>'probe-grid',
	'dataProvider'=>$provider,
	'template'=>'{summary}<div class="joyful-table-scroll">{items}</div>{pager}',
	'columns'=>array(
		array('class'=>'ext.components.tailwind.XTCheckBoxColumn','selectableRows'=>2),
		'name',
		'description',
		array('class'=>'ext.components.tailwind.XTButtonColumn','template'=>'{view}','viewButtonUrl'=>'array("view","id"=>$data["id"])'),
	),
),true);
$content='<h1 class="font-heading mb-10 border-b-2 border-gray-500 pb-2 text-lg text-gray-700 sm:text-xl">Records</h1>';
$content.=$controller->renderFile($root.'/themes/joyful/views/decorators/shadowGrid.php',array('content'=>$grid),true);
$content.='<div class="mt-8"><a id="probe-link" href="#" class="hover:text-green-500">Link</a></div>';
$html=$controller->renderFile($root.'/themes/joyful/views/layouts/main.php',array('content'=>$content),true);
file_put_contents($argv[2],$html);
CFileHelper::removeDirectory($temporary);
echo "Rendered real Yii shell, breadcrumbs, grid and pager to ".$argv[2]."\n";
