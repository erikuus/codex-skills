<?php
return array(
	'default'=>array(
		'cssFile'=>Yii::app()->theme->baseUrl.'/css/gridview.css',
		'rowCssClass'=>array('hover:bg-green-50', 'hover:bg-green-50'),
		'pager'=>array('class'=>'ext.components.tailwind.XTLinkPager'),
		'summaryCssClass'=>'summary text-right mr-1',
		'pagerCssClass'=>'pager mt-2',
	)
);
