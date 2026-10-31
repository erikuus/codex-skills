<?php
$homeIcon='<svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19,9.3V4h-3v2.6L12,3L2,12h3v8h6v-6h2v6h6v-8h3L19,9.3z M17,18h-2v-6H9v6H7v-7.81l5-4.5l5,4.5V18z"/><path d="M10,10h4c0-1.1-0.9-2-2-2S10,8.9,10,10z"/></svg>';
return array('default'=>array(
	'tagName'=>'ol',
	'htmlOptions'=>array('class'=>'my-4 flex items-center rounded border-none text-sm backdrop-brightness-105'),
	'homeLink'=>CHtml::tag('li',array(),CHtml::link($homeIcon,Yii::app()->homeUrl,array(
		'class'=>'my-1 mr-4 inline-flex cursor-pointer items-center rounded bg-white p-2 text-base font-medium ring-4 ring-white hover:bg-green-50',
		'aria-label'=>Yii::t('zii','Home'),
	))),
	'separator'=>'<li class="shrink-0" aria-hidden="true"><svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg></li>',
	'activeLinkTemplate'=>'<li class="min-w-0 truncate"><a class="block rounded px-2 py-1.5 text-sm font-bold text-gray-900 hover:bg-green-50" href="{url}">{label}</a></li>',
	'inactiveLinkTemplate'=>'<li class="min-w-0 truncate"><span class="block px-3 py-2 text-sm text-gray-900" aria-current="page">{label}</span></li>',
));
