<!doctype html>
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
		a, a:hover, a:focus {
			color: #3AD;
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

		<h2>Digitaalsed kujutised ei ole kättesaadavad</h2>
		<p>Meil on tehniline probleem kettamassiiviga, kus hoitakse digiteeritud faile. Otsime probleemile lahendust, aga hetkel ei oska veel öelda, kui palju meil selleks aega kulub.<br />Vabandame ebamugavuste pärast!</p>
		<p><?php echo CHtml::link('Ava rakendus sellele vaatamata', array('pass'));?></p>

		<h2>Digital images are currently unavailable</h2>
		<p>We're working to resolve the technical problems and hope to finish soon but can't commit to a firm time.<br />We apologize for the downtime.</p>
		<p><?php echo CHtml::link('Open application anyway', array('pass'));?></p>

	</div>
</body>
