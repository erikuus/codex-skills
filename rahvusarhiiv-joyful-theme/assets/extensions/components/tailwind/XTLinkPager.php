<?php
/** Flat link markup from VAU, with pagination calculated by the current Yii core. */
class XTLinkPager extends CLinkPager
{
	public function run()
	{
		$this->registerClientScript();
		$buttons=$this->createPageButtons();
		if(empty($buttons))
			return;
		$options=$this->htmlOptions;
		if(!isset($options['aria-label']))
			$options['aria-label']=Yii::t('ui','Pagination');
		echo $this->header;
		echo CHtml::tag('nav',$options,implode("\n",$buttons));
		echo $this->footer;
	}

	protected function createPageButton($label,$page,$class,$hidden,$selected)
	{
		$options=array('class'=>$class);
		if($hidden)
		{
			$options['class'].=' '.$this->hiddenPageCssClass;
			$options['aria-disabled']='true';
			return CHtml::tag('span',$options,$label);
		}
		if($selected)
		{
			$options['class'].=' '.$this->selectedPageCssClass;
			$options['aria-current']='page';
		}
		return CHtml::link($label,$this->createPageUrl($page),$options);
	}
}
