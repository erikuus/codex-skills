<?php
/**
 * XTActiveForm class file.
 *
 * XTActiveForm extends XTDynamicForm adding Tailwind CSS classes to labels and fields
 *
 * @author Erik Uus <erik.uus@gmail.com>
 * @version 1.0.0
 */
require_once dirname(__FILE__).'/XTDynamicForm.php';
require_once dirname(__FILE__).'/XTHtml.php';
class XTActiveForm extends XTDynamicForm
{
	public $enableRadioToggle=false;

	public $enableChecboxToggle=false;

	public $errorMessageCssClass='errorMessage mt-2 text-sm text-red-500';

	public $labelCssClass='mb-2 block text-base font-semibold leading-6 text-gray-800';

	public $fieldCssClass='block w-full rounded border border-gray-200 px-4 py-3 text-gray-900 hover:border-gray-300 focus:border-gray-500 focus:outline-hidden focus:ring-2 focus:ring-green-300 sm:text-base sm:leading-6 disabled:bg-gray-50 disabled:text-gray-400 disabled:border-gray-100
	';

	public $radioCssClass='h-4 w-4 -mt-0.5 mr-3 text-green-500 focus:ring-offset-0 focus:ring-2 border-gray-200 hover:border-gray-300 focus:border-gray-500 focus:ring-green-300 focus:ring-green-300';

	public $checkboxCssClass='h-4 w-4 -mt-0.5 rounded-sm text-green-500 focus:ring-offset-0 focus:ring-2 border-gray-200 hover:border-gray-300 focus:border-gray-500 focus:ring-green-300 focus:ring-green-300';

	public $htmlOptions=array('class'=>'space-y-6');


	public function label($model,$attribute,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->labelCssClass);
		return XTHtml::activeLabel($model,$attribute,$htmlOptions);
	}

	public function labelEx($model,$attribute,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->labelCssClass);
		return XTHtml::activeLabelEx($model,$attribute,$htmlOptions);
	}

	public function textField($model,$attribute,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->fieldCssClass);
		return XTHtml::activeTextField($model,$attribute,$htmlOptions);
	}

	public function passwordField($model,$attribute,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->fieldCssClass);
		return XTHtml::activePasswordField($model,$attribute,$htmlOptions);
	}

	public function textArea($model,$attribute,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->fieldCssClass);
		return XTHtml::activeTextArea($model,$attribute,$htmlOptions);
	}

	public function dropDownList($model,$attribute,$data,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->fieldCssClass);
		return XTHtml::activeDropDownList($model,$attribute,$data,$htmlOptions);
	}

	public function radioButton($model,$attribute,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->radioCssClass);
		return XTHtml::activeRadioButton($model,$attribute,$htmlOptions);
	}

	public function radioButtonList($model,$attribute,$data,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->radioCssClass);
		return XTHtml::activeRadioButtonList($model,$attribute,$data,$htmlOptions);
	}

	public function checkBox($model,$attribute,$htmlOptions=array())
	{
		$htmlOptions=$this->assignClass($htmlOptions, $this->checkboxCssClass);
		return XTHtml::activeCheckBox($model,$attribute,$htmlOptions);
	}

	public function dynamicDropDownList($model,$attribute,$data,$htmlOptions=array())
	{
		return parent::dynamicDropDownList($model,$attribute,$data,$this->assignClass($htmlOptions,$this->fieldCssClass));
	}

	public function checkBoxList($model,$attribute,$data,$htmlOptions=array())
	{
		return parent::checkBoxList($model,$attribute,$data,$this->assignClass($htmlOptions,$this->checkboxCssClass));
	}

	public function errorSummary($models,$header=null,$footer=null,$htmlOptions=array())
	{
		if($header===null)
			$header='<p class="'.XTHtml::$errorSummaryHeaderCss.'">'.Yii::t('yii','Please fix the following input errors:').'</p>';
		$htmlOptions=$this->assignClass($htmlOptions,XTHtml::$errorSummaryCss);
		$html=parent::errorSummary($models,$header,$footer,$htmlOptions);
		return str_replace("\n<ul>","\n<ul class=\"".XTHtml::$errorSummaryListCss."\">",$html);
	}

	protected function assignClass($htmlOptions, $class)
	{
		if(isset($htmlOptions['class']))
			$htmlOptions['class'].=' '.$class;
		else
			$htmlOptions = array_merge($htmlOptions, array('class'=>$class));

		return $htmlOptions;
	}
}
