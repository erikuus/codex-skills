<?php
/**
 * XTCheckBoxColumn class file.
 *
 * Inserts checkbox column based on Tailwind CSS Framework.
 *
 * @author Erik Uus <erik.uus@gmail.com>
 * @version 1.0
 */

Yii::import('zii.widgets.grid.CCheckBoxColumn');

class XTCheckBoxColumn extends CCheckBoxColumn
{
	public $htmlOptions=array('class'=>'w-4');

	public $headerCheckBoxHtmlOptions=array(
		'class'=>'ml-2 h-4 w-4 rounded-sm text-green-500 focus:ring-offset-0 focus:ring-2 border-gray-200 hover:border-gray-300 focus:border-gray-500 focus:ring-green-300 focus:ring-green-300',
		'aria-label'=>'Select all'
	);

	public $checkBoxHtmlOptions=array(
		'class'=>'ml-2 h-4 w-4 rounded-sm text-green-500 focus:ring-offset-0 focus:ring-2 border-gray-200 hover:border-gray-300 focus:border-gray-500 focus:ring-green-300 focus:ring-green-300',
		'aria-label'=>'Select row'
	);


	public function getHeaderCellContent()
	{
		if(trim($this->headerTemplate)==='')
			return $this->grid->blankDisplay;
		$options=$this->headerCheckBoxHtmlOptions;
		if($this->selectableRows===null && $this->grid->selectableRows>1)
		{
			$options['class']=(isset($options['class']) ? $options['class'].' ' : '').'select-on-check-all';
			$item=CHtml::checkBox($this->id.'_all',false,$options);
		}
		elseif($this->selectableRows>1)
			$item=CHtml::checkBox($this->id.'_all',false,$options);
		else
			return parent::getHeaderCellContent();
		return strtr($this->headerTemplate,array('{item}'=>$item));
	}
}
