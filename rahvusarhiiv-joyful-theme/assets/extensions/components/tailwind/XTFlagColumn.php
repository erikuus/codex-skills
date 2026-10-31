<?php
/** Joyful boolean toggle; preserves the XFlagColumn callback parameter contract. */
Yii::import('zii.widgets.grid.CDataColumn');
require_once dirname(__FILE__).'/XTGridAction.php';
class XTFlagColumn extends CDataColumn
{
	public $callbackUrl=array('flag');
	public $flagClass='flag-link';
	public $htmlOptions=array('class'=>'flag-column');
	public $flagClasses=' flex h-8 w-8 shrink-0 items-center justify-center rounded-full hover:bg-green-100';

	public $yesFlag = '<svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="m424-312 282-282-56-56-226 226-114-114-56 56 170 170ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg>';

	public $noFlag = '<svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Z"/></svg>';

	public function init()
	{
		parent::init();
		XTGridAction::register($this,$this->flagClass,'json');
	}

	public function getDataCellContent($row)
	{
		$data=$this->grid->dataProvider->data[$row];
		$value=CHtml::value($data,$this->name);
		$params=$this->callbackUrl;
		$params['pk']=$this->grid->dataProvider->keys[$row];
		$params['name']=$this->name;
		$params['value']=(int)empty($value);
		$label=Yii::t('ui',empty($value) ? 'Set to yes' : 'Set to no');
		return CHtml::link(empty($value) ? $this->noFlag : $this->yesFlag,$params,array(
			'class'=>$this->flagClass.' '.$this->flagClasses,
			'title'=>$label,
			'aria-label'=>$label,
			'data-joyful-column'=>$this->id,
		));
	}
}
