<?php
return array(
	'default'=>array(
		'cssFile'=>Yii::app()->theme->baseUrl.'/css/gridview.css',
		'pager'=>array('class'=>'ext.components.tailwind.XTLinkPager'),
		'htmlOptions'=>array('class'=>'grid-view joyful-grid'),
		'summaryCssClass'=>'summary text-right mr-1',
		'pagerCssClass'=>'pager mt-2',
	)
);
