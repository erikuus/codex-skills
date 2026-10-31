<?php
$themeUrl=Yii::app()->theme->baseUrl;
Yii::app()->clientScript->registerCoreScript('jquery');
Yii::app()->clientScript->registerCoreScript('yii');
Yii::app()->clientScript->registerCssFile($themeUrl.'/css/style.css');

?>
<!DOCTYPE html>
<html lang="<?php echo CHtml::encode(Yii::app()->language); ?>">
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<title><?php echo CHtml::encode($this->pageTitle); ?></title>
</head>
<body class="bg-white font-body text-gray-900">
	<main class="px-4 pt-6 pb-10"><?php echo $content; ?></main>
</body>
</html>
