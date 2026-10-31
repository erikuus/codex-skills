<?php
/** Register scoped grid actions for Joyful flag and reorder columns. */
class XTGridAction
{
	public static function register($column,$triggerClass,$dataType=null)
	{
		$request=Yii::app()->request;
		$data=array();
		if($request->enableCsrfValidation)
			$data[$request->csrfTokenName]=$request->getCsrfToken();
		$options=CJavaScript::encode(array(
			'grid'=>$column->grid->id,
			'column'=>$column->id,
			'trigger'=>$triggerClass,
			'data'=>$data,
			'dataType'=>$dataType,
			'errorMessage'=>Yii::t('ui','The action could not be completed. Please try again.'),
		));
		$assets=Yii::app()->assetManager->publish(dirname(__FILE__).'/assets');
		Yii::app()->clientScript->registerCoreScript('jquery');
		Yii::app()->clientScript->registerScriptFile($assets.'/joyful.js',CClientScript::POS_HEAD);
		Yii::app()->clientScript->registerScript(__CLASS__.'#'.$column->grid->id.'#'.$column->id,"window.joyfulGridAction($options);");
	}
}
