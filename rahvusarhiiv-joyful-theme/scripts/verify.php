<?php
/** Run against an explicit Yii 1.1.33-dev yii.php; no database or application config. */
if($argc!==2)
	throw new RuntimeException('Usage: php verify.php /path/to/yii-1.1.33-dev/yii.php');
define('YII_ENABLE_EXCEPTION_HANDLER',false);
define('YII_ENABLE_ERROR_HANDLER',false);
ob_start();
require $argv[1];
$root=dirname(__DIR__).'/assets/app';
$temporary=sys_get_temp_dir().'/joyful-verify-'.getmypid();
mkdir($temporary);
mkdir($temporary.'/runtime');
mkdir($temporary.'/assets');
$_SERVER['SCRIPT_FILENAME']=$root.'/index.php';
$_SERVER['SCRIPT_NAME']='/index.php';
$_SERVER['HTTP_HOST']='localhost';
$_SERVER['REQUEST_URI']='/index.php';
$app=Yii::createWebApplication(array(
	'basePath'=>$temporary,
	'runtimePath'=>$temporary.'/runtime',
	'aliases'=>array('ext'=>dirname(__DIR__).'/assets/extensions'),
	'import'=>array('ext.components.tailwind.*'),
	'components'=>array(
		'assetManager'=>array('basePath'=>$temporary.'/assets','baseUrl'=>'/assets'),
		'themeManager'=>array('basePath'=>$root.'/themes','baseUrl'=>'/themes'),
		'widgetFactory'=>array('enableSkin'=>true),
		'request'=>array('enableCsrfValidation'=>true),
	),
	'theme'=>'joyful',
));
if(strpos(Yii::getVersion(),'1.1.33')!==0)
	throw new RuntimeException('Expected Yii 1.1.33-dev; got '.Yii::getVersion());
$controller=new CController('fixture');
$app->controller=$controller;
function verify($condition,$message)
{
	if(!$condition)
		throw new RuntimeException($message);
	echo "PASS $message\n";
}
class JoyfulFixtureModel extends CFormModel
{
	public $name;
	public $choice;
	public function rules()
	{
		return array(array('name','required'));
	}
}
$model=new JoyfulFixtureModel;
$model->addError('name','<script>unsafe()</script>');
$html=XTHtml::errorSummary($model);
verify(strpos($html,'&lt;script&gt;')!==false && strpos($html,'<script>')===false,'error summary encodes errors');
verify(strpos(XTHtml::errorSummary($model,null,null,array('encode'=>false)),'<script>')!==false,'explicit raw-error opt-in preserved');
verify(strpos(XTHtml::button('Save',array('name'=>null)),'name=')===false,'null button name respected');
$form=$app->widgetFactory->createWidget($controller,'ext.components.tailwind.XTActiveForm',array('id'=>'fixture-form','enableClientValidation'=>true));
$html=$form->errorSummary($model);
verify(strpos($html,'id="fixture-form_es_"')!==false && strpos($html,'&lt;script&gt;')!==false,'client summary ID and encoding preserved');
$model->clearErrors();
verify(strpos($form->errorSummary($model),'display:none')!==false,'empty client summary remains available');
verify(strpos($form->checkBox($model,'choice'),'type="hidden"')!==false,'unchecked checkbox hidden value preserved');
verify(strpos($form->checkBoxList($model,'choice',array(1=>'One')),'text-green-500')!==false,'checkbox lists receive Joyful styling');
$model->name='';
$model->validate();
verify(strpos($form->textField($model,'name'),'error')!==false,'invalid input retains Yii error class');
$provider=new CArrayDataProvider(array(array('id'=>1,'name'=>'A','flag'=>1),array('id'=>2,'name'=>'B','flag'=>0)),array('pagination'=>array('pageSize'=>1,'route'=>'/fixture/index')));
$grid=$app->widgetFactory->createWidget($controller,'zii.widgets.grid.CGridView',array('id'=>'fixture-grid','dataProvider'=>$provider,'selectableRows'=>2,'columns'=>array('name')));
verify($grid->pager['class']==='ext.components.tailwind.XTLinkPager','theme skin resolves and configures pager');
$grid->init();
$column=new XTCheckBoxColumn($grid);
$column->id='selection';
$html=$column->getHeaderCellContent();
verify(strpos($html,'select-on-check-all')!==false && strpos($html,'type="checkbox"')!==false,'inherited multiple selection renders select-all');
$column->headerTemplate='Before {item} After';
verify(strpos($column->getHeaderCellContent(),'Before <input')===0,'checkbox header template honored');
$column->selectableRows=2;
verify(strpos($column->getHeaderCellContent(),'select-on-check-all')===false,'independent multiple-selection mode preserved');
$column->selectableRows=1;
verify(strpos($column->getHeaderCellContent(),'type="checkbox"')===false,'single selection has no select-all');
$column->headerTemplate='';
verify($column->getHeaderCellContent()===$grid->blankDisplay,'empty checkbox header template respected');
$buttons=new XTButtonColumn($grid);
$buttons->id='actions';
$buttons->template='{custom}';
$buttons->buttons=array('custom'=>array('label'=>'Edit row','icon'=>'<svg></svg>','url'=>'array("edit","id"=>$data["id"])','options'=>array('class'=>'existing-hook')));
$buttons->init();
$html=$buttons->getDataCellContent(0);
verify(strpos($html,'existing-hook')!==false && strpos($html,'aria-label="Edit row"')!==false && strpos($html,'id=1')!==false,'custom button URL, hook and accessible label preserved');
$buttons->buttons['custom']['visible']='false';
verify($buttons->getDataCellContent(0)==='','button visibility expressions preserved');
$reorder=new XTReorderColumn($grid);
$reorder->id='reorder';
$reorder->init();
$html=$reorder->getDataCellContent(0);
verify(strpos($html,'move=up')!==false && strpos($html,'move=down')!==false,'current grid getter renders reorder actions');
$flag=new XTFlagColumn($grid);
$flag->id='flag';
$flag->name='flag';
$flag->init();
$html=$flag->getDataCellContent(0);
verify(strpos($html,'pk=1')!==false && strpos($html,'value=0')!==false,'flag preserves callback parameters');
$pager=$app->widgetFactory->createWidget($controller,'ext.components.tailwind.XTLinkPager',array('pages'=>$provider->pagination));
$pager->init();
ob_start(); $pager->run(); $html=ob_get_clean();
verify(strpos($html,'<nav')!==false && strpos($html,'aria-current="page"')!==false && strpos($html,'aria-disabled="true"')!==false,'pager uses core ranges and accessible flat markup');
$step=new XTStepBar($controller);
$step->steps=array(array('label'=>'<b>First</b>','active'=>true),array('label'=>'Hidden','visible'=>false));
ob_start(); $step->run(); $html=ob_get_clean();
verify(strpos($html,'&lt;b&gt;First')!==false && strpos($html,'Hidden')===false && strpos($html,'flex-auto border-t-2')===false,'step labels encoded and hidden final step has no connector');
$html='<html><head></head><body></body></html>';
$app->clientScript->render($html);
verify(strpos($html,'YII_CSRF_TOKEN')!==false,'grid action registration includes CSRF token');
verify(strpos($html,'.live(')===false,'rendered component scripts avoid removed jQuery API');
$reference=file_get_contents(dirname(__DIR__).'/assets/reference/advanced-layout-alt.html');
$footerStart=strpos($reference,'    <!-- Neljas valge ala -->');
$footerEnd=strpos($reference,'  </body>',$footerStart);
verify(file_get_contents($root.'/themes/joyful/views/layouts/_footer.php')===substr($reference,$footerStart,$footerEnd-$footerStart),'footer is the exact reference subtree');
CFileHelper::removeDirectory($temporary);
ob_end_flush();
echo 'Verified against Yii '.Yii::getVersion().' / PHP '.PHP_VERSION."\n";
