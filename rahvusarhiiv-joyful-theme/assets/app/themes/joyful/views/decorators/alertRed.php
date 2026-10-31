<?php if($visible): ?>
<div class="mb-6 rounded p-3 bg-red-100 text-red-800">
	<div class="flex items-center">
		<div class="shrink-0 mr-3 rounded-full bg-red-200 p-2">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" fill="currentColor" class="w-5 h-5">
				<path d="m40-120 440-760 440 760H40Zm138-80h604L480-720 178-200Zm302-40q17 0 28.5-11.5T520-280q0-17-11.5-28.5T480-320q-17 0-28.5 11.5T440-280q0 17 11.5 28.5T480-240Zm-40-120h80v-200h-80v200Zm40-100Z"></path>
			</svg>
		</div>
		<div class="flex-1 text-sm">
			<?php  echo $content; ?>
		</div>
	</div>
</div>
<?php endif; ?>
