<?php
// Adaptation of the authoritative advanced-layout-alt.html shell.
// Fill the marked application slots with existing routes, permissions and widgets.
$themeUrl=Yii::app()->theme->baseUrl;
$cs=Yii::app()->clientScript;
$cs->registerCoreScript('jquery');
$cs->registerCoreScript('yii');
$cs->registerCssFile($themeUrl.'/css/style.css');

?>
<!DOCTYPE html>
<html lang="<?php echo CHtml::encode(Yii::app()->language); ?>">
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<script defer src="<?php echo CHtml::encode($themeUrl.'/js/alpine.3.12.3.min.js'); ?>"></script>
	<title><?php echo CHtml::encode($this->pageTitle); ?></title>
</head>
<body class="flex min-h-screen flex-col bg-gray-50 font-body text-gray-900">
	<!-- First white surface. -->
	<div class="flex grow flex-col rounded-b bg-white shadow-md lg:m-2 lg:rounded">
		<header class="joyful-site-header flex h-12 flex-wrap content-center">
			<div class="2xl:max-w-xxl mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8">
				<div class="flex items-center justify-between">
					<a href="https://www.ra.ee/" target="_blank" rel="noopener">
						<?php echo CHtml::image($themeUrl.'/images/ra_logo.svg','Rahvusarhiiv',array('class'=>'h-7 opacity-70')); ?>
					</a>
					<div class="flex items-center">
						<?php // Application slot: existing enabled XVauBookmark / XVauHelpdesk as icons. ?>
						<?php // Keep real language controls and the mobile opener (lg:hidden) in this group. ?>
						<?php // See references/layout-standard.md: Top-right utility icons. ?>
					</div>
				</div>
			</div>
		</header>
		<!-- Gradient surface contains the application header AND the white content panel. -->
		<div class="bg-theme-vau flex grow flex-col rounded">
			<header class="joyful-site-header relative flex h-32 flex-wrap content-center z-0">
				<div class="2xl:max-w-xxl mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8">
					<div class="flex items-center justify-between">
						<?php // Use the target logo at h-11 sm:h-12 when available; otherwise its name. ?>
						<?php echo CHtml::link(CHtml::encode(Yii::app()->name),Yii::app()->homeUrl,array('class'=>'font-heading text-3xl font-bold')); ?>
						<nav class="hidden lg:flex lg:gap-x-4 xl:gap-x-8 2xl:gap-x-12 font-medium">
							<?php // Application slot: first group of existing primary navigation links. ?>
						</nav>
						<nav class="hidden lg:flex lg:gap-x-4 xl:gap-x-8 2xl:gap-x-12 font-medium">
							<?php // Application slot: second group when the target has one. ?>
						</nav>
						<div class="flex items-center gap-x-2">
							<?php // Application slot: existing sign-in/account control and permission checks. ?>
							<?php // Guest Login includes VAU account-circle SVG + text; see layout-standard.md. ?>
						</div>
					</div>
				</div>
				<?php // Add the standard's right-side mobile drawer, populated with the same authorized links. ?>
				<?php // See references/layout-standard.md for placement, focus and scroll-lock requirements. ?>
			</header>
			<?php if(isset($this->breadcrumbs) && $this->breadcrumbs): ?>
			<nav class="-mt-6 flex" aria-label="<?php echo CHtml::encode(Yii::t('ui','Breadcrumb')); ?>">
				<div class="2xl:max-w-xxl mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8">
					<?php $this->widget('zii.widgets.CBreadcrumbs',array('links'=>$this->breadcrumbs)); ?>
				</div>
			</nav>
			<?php endif; ?>
			<!-- Third white surface; retain it even when the route has little content. -->
			<div class="flex grow flex-col rounded rounded-b bg-white shadow-md">
				<main class="2xl:max-w-xxl mx-auto flex w-full max-w-7xl px-4 py-6 md:px-6 lg:px-8 xl:py-10">
					<div class="w-full min-w-0">
						<?php echo $content; ?>
					</div>
				</main>
			</div>
		</div>
	</div>
	<?php $this->renderPartial('//layouts/_footer'); ?>
</body>
</html>
