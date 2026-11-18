<!doctype html>
<html lang="<?php echo CHtml::encode(Yii::app()->language); ?>">
<head>
	<meta charset="utf-8" />
	<title><?php echo CHtml::encode(Yii::app()->name)?></title>
	<style>
		body, h1, h2, h3, h4, h5 {
			font-family: "Helvetica Neue","Helvetica",Helvetica,Arial,sans-serif;
			font-weight: 300;
			color: #444;
		}
		p {
			line-height: 1.5;
		}
		.wrapper {
			margin:100px auto;
			max-width:800px
		}
	</style>
</head>
<body>
	<div class="wrapper">
		<h1><?php echo CHtml::encode(Yii::app()->name)?></h1>

		<h2><?php echo Yii::t('er','This service is currently under maintenance'); ?></h2>
		<p><?php echo Yii::t('er','Please try again later. Thank you for your patience.'); ?></p>
	</div>
</body>
</html>
