<?php

/**
 * XTHtml class
 *
 * This class adds tailwind CSS to CHtml class.
 *
 * @author Erik Uus <erik.uus@gmail.com>
 * @version 1.0.0
 */
class XTHtml extends CHtml
{

	public static $errorSummaryCss='-mx-4 my-4 rounded bg-red-50 p-4 text-sm text-red-700';

	public static $errorSummaryHeaderCss='mb-4 font-medium';

	public static $errorSummaryListCss='ml-6 list-disc space-y-2';

	public static $errorCss='border-red-300 hover:border-red-400 focus:border-red-600 focus:ring-red-200 focus:ring-red-200';

	public static $linkCssClass='font-medium text-blue-600 hover:text-blue-500 focus:active:text-blue-700';

	public static $buttonCssClass='focus-visible:ring-2 focus-visible:ring-green-300 cursor-pointer rounded bg-gray-900 py-3 px-4 text-center text-base font-medium text-white hover:bg-gray-700';

	public static $buttonLinkCssClass='focus-visible:ring-2 focus-visible:ring-green-300 cursor-pointer border border-gray-200 rounded bg-white py-3 px-4 text-center text-base font-medium text-gray-900 hover:bg-gray-100';

	public static $labelCssClass='mb-2 block text-base font-semibold leading-6 text-gray-800';


	public static function link($text,$url='#',$htmlOptions=array())
	{
		return parent::link($text,$url,self::assignClass($htmlOptions,self::$linkCssClass));
	}

	public static function buttonLink($text,$url='#',$htmlOptions=array())
	{
		return parent::link($text,$url,self::assignClass($htmlOptions,self::$buttonLinkCssClass));
	}

	public static function button($label='button',$htmlOptions=array())
	{
		return parent::button($label,self::assignClass($htmlOptions,self::$buttonCssClass));
	}

	public static function submitButton($label='submit',$htmlOptions=array())
	{
		return parent::submitButton($label,self::assignClass($htmlOptions,self::$buttonCssClass));
	}

	public static function htmlButton($label='button',$htmlOptions=array())
	{
		return parent::htmlButton($label,self::assignClass($htmlOptions,self::$buttonCssClass));
	}

	public static function errorSummary($model,$header=null,$footer=null,$htmlOptions=array())
	{
		if($header===null)
			$header='<p class="'.self::$errorSummaryHeaderCss.'">'.Yii::t('yii','Please fix the following input errors:').'</p>';
		$html=parent::errorSummary($model,$header,$footer,self::assignClass($htmlOptions,self::$errorSummaryCss));
		return str_replace("\n<ul>","\n<ul class=\"".self::$errorSummaryListCss."\">",$html);
	}

	protected static function assignClass($htmlOptions,$class)
	{
		$htmlOptions['class']=isset($htmlOptions['class']) ? $htmlOptions['class'].' '.$class : $class;
		return $htmlOptions;
	}
}
