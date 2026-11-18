<?php
class MaintenanceController extends CController
{
	public function actionIndex()
	{
		$app=Yii::app();
		// Yii skips URL parsing for catch-all requests, including language selection.
		if(isset($app->catchAllRequest[0]))
			$app->urlManager->parseUrl($app->request);

		http_response_code(503);
		header('Cache-Control: no-store');
		$this->renderPartial("index");
	}

	public function actionMnt()
	{
		$this->renderPartial("mnt");
	}

	public function actionPass()
	{
		Yii::import('ext.helpers.Cookie');
		Cookie::set('pass', 'kaardid');
		$this->redirect(array('/site/index'));
	}
}
