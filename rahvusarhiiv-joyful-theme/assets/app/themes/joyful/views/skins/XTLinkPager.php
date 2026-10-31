<?php
return array(
	'default'=>array(
		'cssFile'=>false,
		'header'=>'',
		'htmlOptions'=>array(
			'class'=>'yiiPager flex justify-center gap-x-1.5 text-gray-700 not-prose print:hidden'
		),
		'firstPageCssClass'=>'first py-1.5 px-2 2xl:py-2 2xl:px-3 rounded hover:bg-green-50',
		'lastPageCssClass'=>'last py-1.5 px-2 2xl:py-2 2xl:px-3 rounded hover:bg-green-50',
		'previousPageCssClass'=>'previous py-1.5 px-2 2xl:py-2 2xl:px-3 rounded hover:bg-green-50',
		'nextPageCssClass'=>'next py-1.5 px-2 2xl:py-2 2xl:px-3 rounded hover:bg-green-50',
		'internalPageCssClass'=>'hidden md:block py-1.5 px-3 2xl:py-2 2xl:px-4 rounded hover:bg-green-50',
		'hiddenPageCssClass'=>'text-gray-200 hover:bg-gray-50',
		'selectedPageCssClass'=>'bg-green-50 font-bold',
		'firstPageLabel'=>'
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <polygon points="17.59,18 19,16.59 14.42,12 19,7.41 17.59,6 11.59,12"></polygon><polygon points="11,18 12.41,16.59 7.83,12 12.41,7.41 11,6 5,12"></polygon>
            </svg>
            <span class="sr-only">First Page</span>
		',
		'prevPageLabel'=>'
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"></path>
            </svg>
            <span class="sr-only">Previous Page</span>
		',
		'nextPageLabel'=>'
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"></path>
            </svg>
            <span class="sr-only">Next Page</span>
		',
		'lastPageLabel'=>'
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <polygon points="6.41,6 5,7.41 9.58,12 5,16.59 6.41,18 12.41,12"></polygon><polygon points="13,6 11.59,7.41 16.17,12 11.59,16.59 13,18 19,12"></polygon>
            </svg>
            <span class="sr-only">Last Page</span>
		',
	)
);
