# Default → Joyful transformation patterns

## Shell and responsive structure

Use [advanced-layout-alt.html as the authoritative shell](layout-standard.md). Its nested structure is: gray-50 body → rounded white outer surface with a 48px institutional header → growing gradient surface with a 128px application header **and a nested rounded white content panel** → separate white footer. The content panel must remain inside the gradient wrapper. Its main container is `mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8 2xl:max-w-xxl` (80rem, then 90rem at 1536px). Main content spacing is `py-6 xl:py-10`, with the standard's `flex` container and a width-constrained inner content element. The footer uses a mobile stacked / desktop split links-and-contact structure, with `sm:h-64` and responsive dividers. Do not substitute the old compact copyright-only footer or VAU's different bottom padding.

Use Roboto body text and Raleway headings from the supplied local font files. The source gradient is `linear-gradient(95.19deg, #CCEAD6 0.8%, #ECDDF4 158.87%)`. `bg-theme-vau` is retained as a CSS token, not as an instruction to brand the target VAU. The app's name, logo, menus and content come from that app.

Typical page title: `font-heading mb-10 mt-px border-b-2 border-gray-500 pb-2 text-lg font-bold text-gray-700 sm:mt-6 sm:text-xl xl:mt-0`. Narrow create/update pages in VAU use several breakpoint margins (`sm:mx-20 lg:mx-36 xl:mx-80 2xl:mx-96`); use the equivalent bounded `.joyful-form` for target forms so intermediate widths remain usable. Wide editors need their own content width.

The sample apps' `leftbar`, `rightbar`, and `sidebars` layouts call `$this->beginContent()` and loop through controller portlets. Preserve that nesting and those loops. Replace the 960-grid markup, for example:

```php
<?php $this->beginContent(); ?>
<div class="joyful-columns joyful-columns-left">
    <aside><?php foreach($this->leftPortlets as $class=>$properties) $this->widget($class,$properties); ?></aside>
    <section><?php echo $content; ?></section>
</div>
<?php $this->endContent(); ?>
```

Use `joyful-columns-right` or `joyful-columns-both` for corresponding layouts. Preserve print branches before changing markup; do not nest main twice. Main owns the single gradient breadcrumb strip between the application header and white content panel. Nested layouts keep their breadcrumb data but omit duplicate rendering. The payload uses the current `CBreadcrumbs` with a skin, not VAU's copied 1.1.11 `Breadcrumbs` class.

## Page title and utility actions

Place existing page-level Print and contextual help actions **to the right of the page title as icon + visible text**, as in VAU `themes/joyful/views/order/index.php` for `scope=clientDraft` and the user's screenshot (“Kinnitamata tellimused” with “Prindi”, “Värvid”, “Toimingud”). Keep them in the same heading row above one shared bottom rule; do not scatter them below the title, turn them into large boxed buttons, or move these page-specific actions to the global header. Preserve each target's existing actions and translations; do not invent order-specific help entries.

Source details: action wrapper `float-right flex gap-x-4 mt-2`; each link `inline-flex items-center text-center text-sm font-medium text-gray-600`; printer or circled-question SVG `h-4 w-4` (16px), with a small gap before the label. The title uses `font-heading text-lg font-bold text-gray-700 sm:text-xl`, and its row has `border-b-2 border-gray-500 pb-2 mb-6 md:mb-10`.

For long translated headings, a flex row is a robust equivalent of the source float: use a wrapping `flex items-center justify-between gap-x-4 gap-y-2` row carrying the shared border/padding/margins; the heading itself has no second bottom border, and actions use `ml-auto flex flex-wrap items-center gap-x-4 gap-y-2`. Each link retains its icon/text together (`inline-flex items-center gap-x-1 whitespace-nowrap`), with the SVG `shrink-0` and `aria-hidden="true"`. At narrow widths, wrap the action group below the heading within the same title block instead of overlapping or truncating it. **Keep visible text alongside icons** as requested; the original source hides text below `sm`, but that part is not the requested rule.

Keep actual print URLs, `rel`/target behavior, visibility conditions, help routes and `openhelp`/dialog hooks. Hide these interactive utilities in print output as the source does. Preserve genuine row/batch/workflow actions in their own controls; this rule concerns page-level print/help utilities.

## Add/New buttons in the title row

Place a page-level **Add/New/Create action on the right, in line with the page title**, following VAU `themes/joyful/views/bookmark/link/admin.php` and the user's “Minu lingid / Halda kaustu / + Uus link” reference. The title stays on the left; related secondary management buttons precede the primary Add button, which is rightmost. Keep the whole row above **one shared bottom underline**. Do not put the creation button in a separate row below the heading, next to search filters, or in the global header when it belongs to this page.

The source builds `titleBarClip` with an action wrapper `float-right flex gap-x-2 -mt-2 sm:-mt-1.5`, then the heading. Match that visible alignment and 8px action gap. A wrapping flex title row, as described above, is a robust equivalent: align title and controls vertically, put the border/padding on the shared row, and remove the heading's duplicate border. Keep Add distinct from the unboxed Print/help utility links: Add is a compact filled primary button.

Required Add styling:

```text
focus-visible:ring-2 focus-visible:ring-green-300 inline-flex cursor-pointer items-center rounded bg-gray-900 py-2 px-3 text-center text-sm font-medium text-white hover:bg-gray-700
```

- A **white plus SVG before the translated action label**, displayed at **16×16px** (`h-4 w-4 shrink-0`) with a **6px gap** (`mr-1.5` or `gap-x-1.5`, not both). Use `aria-hidden="true"` on the decorative icon. Retain visible text such as the target's “New link” or “Add record”; do not copy bookmark wording into another domain.
- Source glyph: `viewBox="0 0 24 24"`, `fill="currentColor"`, path `M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z`.
- Compact title-row padding **`py-2 px-3`**, `text-sm font-medium`, preset 8px `rounded`, white text, and dark `bg-gray-900` → `hover:bg-gray-700`. Do not use the larger form-submit padding or add primary classes to a secondary helper. The source uses `CHtml::link()` with the explicit classes; `XTHtml` button helpers append their own defaults, so avoid conflicting padding/size classes.
- Optional preceding management actions use the same compact geometry, their own meaningful icon, and the [secondary white → gray hover style](form-controls.md#secondary-buttons-white-to-gray-on-hover): `border border-gray-200 bg-white text-gray-900 hover:bg-gray-100`. Do not copy the source's redundant/conflicting `p-3` alongside `py-2 px-3`; keep one padding definition.

Preserve the target's existing create route, permission/visibility checks, return URL, selected parent/collection context, modal or click handlers, and link/button semantics. In the source, New Link uses `createReturnableUrl('create', array('collectionId'=>$model->collection_id))`; retain the corresponding target context rather than hardcoding that route or parameter. Keep the title/action area intact after any existing AJAX/clip replacement. Do not duplicate an old Add button elsewhere after moving it.

At narrow widths, allow the action group to wrap within the title block above the shared rule, without overlap or horizontal overflow. Preserve icon + visible text when wrapping; the original hides labels below `sm`, but readable wrapped controls are the portable default. Keep the primary action last. Hide interactive creation controls in print output. This rule is for page-level creation entry points; inline “add another row” controls and Create/Save submit buttons stay with their form or repeater.

## Single-field search

When a search form consists of one query field plus Go/Search and Cancel/Clear, use the Joyful shop search pattern instead of a regular stacked form and a separate button row. The desktop source for `/shop/home/index` is **`themes/joyful/views/ShopMenuWidget/shopMenuWidget.php`**, immediately above its menu; `themes/joyful/views/shop/home/index.php` contains the mobile form, and `themes/joyful/views/shop/product/search.php` shows its mobile clear action.

- One horizontal wrapper: `flex items-center space-x-2 rounded bg-white shadow-sm`.
- Growing input: source `w-full px-3 py-2 text-gray-700 bg-white border border-transparent rounded`; add `min-w-0` for narrow layouts. Preserve a translated accessible label. Port the old `focus:outline-none` to modern syntax and retain a visible keyboard focus indication on the field or surrounding control.
- Clear/Cancel: an × SVG `w-4 h-4`, in `flex shrink-0 items-center justify-center p-1 text-gray-800 bg-gray-50 border border-transparent rounded-full hover:bg-gray-100`. Keep it inside the search bar, between input and submit. Show it when a query/filter is active, including a valid query of `"0"`; do not rely on PHP truthiness. Use the target's existing clear/cancel URL or behavior, not the shop's `array('index')` by assumption. Clearing must update the results, not merely reset the input's DOM value.
- Search/Go: real submit button with magnifier SVG `w-5 h-5`, in `flex shrink-0 items-center justify-center p-2.5 text-gray-800 bg-gray-50 border border-transparent rounded hover:bg-gray-100`. Enter submits the same form. Give both icon controls translated accessible names (`aria-label` or `sr-only` text), with decorative SVGs `aria-hidden="true"` and visible keyboard focus.
- Desktop placement is above the existing side menu, with `mb-4`; source uses `hidden lg:block` and `lg:-ml-4` to align with that particular menu. Only retain the negative margin when the target has matching menu padding. Below `lg`, make the search available above results/content (`mb-6`), as in the source mobile form. Prefer one responsive form where practical; if separate desktop/mobile forms are needed, give them unique IDs and keep query state synchronized. Never create a sidebar just to house search.

Keep the existing action, method, query parameter name, current value, hidden scope parameters, submit name/value when used by the controller, and clear semantics. Do not hardcode `/shop/product/search`, `q` or `sbmt` into another app. This rule targets a single-field search; retain the structure of multi-field/advanced filters. The × here clears search and is unrelated to removing a redundant page Back button.

## Forms and button rows

Read [secondary buttons and radio groups](form-controls.md) for the explicit white-to-gray hover contract, correct helper choice, and the bookmark form’s stacked/indented radio layout and dynamic DOM requirements.

VAU's `company/_form.php` preserves model bindings and callbacks while replacing `XDynamicForm` with `XTActiveForm`, `.simple` with plain spaced rows, and inline widths with full-width controls. Group titles become `text-lg font-medium pt-6 border-t border-gray-50`. Required-field guidance uses `text-gray-700 text-sm`. The error summary moves within the same form; its presence and validation registration matter more than its location.

```php
<?php $form=$this->beginWidget('ext.components.tailwind.XTActiveForm',array(
    'id'=>'existing-form-id',
    'enableAjaxValidation'=>false, // Keep the target's actual setting and callbacks.
    'htmlOptions'=>array('class'=>'space-y-6'),
)); ?>
<div class="joyful-field">
    <?php echo $form->labelEx($model,'existingAttribute'); ?>
    <?php echo $form->textField($model,'existingAttribute'); ?>
    <?php echo $form->error($model,'existingAttribute'); ?>
</div>
<div class="joyful-form-actions">
    <?php echo XTHtml::submitButton(Yii::t('ui','Save')); ?>
    <?php echo XTHtml::buttonLink(Yii::t('ui','Cancel'),$existingReturnUrl); ?>
</div>
<?php echo $form->errorSummary($model); ?>
<?php $this->endWidget(); ?>
```

Keep `maxlength`, placeholders, `readonly`, `disabled`, upload settings, scenarios, validators, hidden fields and form submission unchanged. `size`/pixel width can usually go; height may express a real editor requirement. A custom form subclass is not automatically replaceable: inspect its methods and preserve its behavior when adding Joyful styling. Client validation still needs `$form->error()` calls to register fields. Use fieldsets/legends for radio groups and keep checkbox labels associated.

The original toggles default to disabled in `XTActiveForm`, unlike `XDynamicForm`; explicitly retain `enableRadioToggle` / the historical spelling `enableChecboxToggle` when a form uses them. `dynamicDropDownList()` and `beginDynamicAreaDdl()` retain case-insensitive PHP compatibility with older calls. Scope dependent areas to the form. Inactive dropdown areas must disable their inputs on every change; originally disabled inputs remain disabled when their area becomes active.

On pages with breadcrumbs, omit the standalone Back action and remove its wrapper if it becomes empty. Do not remove other toolbar actions or reinterpret a form Cancel, dialog Close, or workflow Previous as that redundant Back action.

Standalone toolbar/action menus use `.joyful-actions`; narrow form submit/cancel rows use `.joyful-form-actions`. Preserve `submit`, `confirm`, `params`, `csrf`, `ajax`, and click handlers on links. An anchor containing an SVG needs an accessible name. Do not put a link inside a button as the source breadcrumb templates do.

## Grids, lists and detail views

### Titled detail groups: spacing, no horizontal separators

When a detail page groups attributes under section titles, separate the groups with heading hierarchy and vertical space. **Do not insert `<hr>`, `divide-y`, top/bottom separator borders, bordered spacer rows, or an underline beneath each group heading.** A source rhythm is `mt-12 mb-6 text-lg font-bold text-gray-700`, used for secondary headings in VAU `themes/joyful/views/company/view.php`; adapt the first group's top margin to avoid excess space. Preserve the groups, attribute labels, values, visibility and ordering.

Use a heading and its detail table/content as a coherent section. Remove inherited legacy rules and prose-generated borders that create separators between these groups; scope corrections to the grouped-detail wrapper rather than stripping borders from every table or heading. The page's main title row may retain its single shared underline, including the right-aligned Print/help actions described above. This rule does not remove form input borders, grid styling or meaningful cell structure merely because the page also contains detail groups.


The source leaves most data attributes intact: `company/_view.php` is functionally identical across themes. The visual work lives in skins and its surrounding `detailTable` decorator. `CDetailView` skin disables its legacy CSS; decorator typography styles the table. Keep labels visible on phones. The portable decorator stacks label/value cells instead of copying VAU's hidden-mobile-header behavior.

```php
<?php $this->beginContent('//decorators/detailTable'); ?>
<?php $this->widget('zii.widgets.CDetailView',array('data'=>$model,'attributes'=>$existingAttributes)); ?>
<?php $this->endContent(); ?>
```

For grids, `shadowGrid` adds soft shadow, zebra rows, green hover, padded cells and rounded outer cells through typography variants. `gridview.css` supplies sorting arrows only; it is not a standalone table design. The skin selects `XTLinkPager`, summary spacing, and disables the old visual defaults through its replacement CSS. Keep `grid-view`, `items`, `summary`, `pager`, `filters` and other Yii/JS hooks.

```php
<?php $this->beginContent('//decorators/shadowGrid'); ?>
<?php $this->widget('zii.widgets.grid.CGridView',array(
    'id'=>'existing-grid-id',
    'dataProvider'=>$existingProvider,
    'filter'=>$existingFilter,
    'template'=>'{summary}<div class="joyful-table-scroll">{items}</div>{pager}',
    'columns'=>$existingColumns,
)); ?>
<?php $this->endContent(); ?>
```

Adapt that template to the original: preserve top/bottom pagers, custom sections, empty text, item count, `ajaxUpdate=false`, selection/batch operations and `afterAjaxUpdate`. Do not replace application `type=>'raw'` expressions blindly or make plain-text output raw to match appearance. Custom grouped grids need their exact-class skin and existing extension implementation.

`CListView` retains its `itemView`, model data, callbacks and templates. Restyle the item wrapper only. Applying `prose` around an entire interactive interface can affect buttons, SVGs and filters; use `not-prose` for toolbars/pagers or keep typography scoped to content.

Custom `XTButtonColumn` buttons use **trusted SVG HTML**, whereas `XFButtonColumn` expects icon class names. Convert `fi-photo`, `fi-pencil`, `fi-x`, etc. individually and preserve custom IDs (`showImage`, `updateSeal`, `deleteSheet`), visibility, URL expressions, `options.class` hooks and click callbacks. Standard delete handling stays in the current Yii parent class. Do not replace a custom modal confirmation with the parent's default delete behavior.

Keep the source table surface, padding, zebra colors, rounded end cells and custom shadow. Do not replace `shadowGrid` with an empty `.joyful-grid-surface` wrapper and a different CSS table design. The bundled decorator already uses Tailwind 4's correct variant order; after altering it, compare computed styles with the original. A class name containing `prose-*` is not evidence its CSS exists: the typography plugin and the decorator's PHP file must both participate in the build.

The source PageSizeMenu is new Joyful-only functionality: its default view is a stub and its themed view depends on `createSetPagesizeUrl()`. It demonstrates popover styling, not a universally available page-size API. Reuse only a target's real page-size mechanism. Likewise, order grids contain domain-specific column-collapsing and batching code that is not a generic theme requirement.

## Navigation and portlets

Yii maps a widget's view by **class name**, not its source directory. Example: `protected/portlets/views/search.php`, rendered by `Search`, becomes `themes/joyful/views/Search/search.php`. A menu class that directly invokes `XNavBar` never looks for `mainMenu.php`. For these, keep its item-building/authorization logic and adjust supported widget options, or extract its existing rendering into a view with unchanged data.

Desktop navigation in VAU is hidden below `lg`; mobile uses a drawer under Alpine. Keep item visibility, active-route logic, translations, badges and account state from the target. Follow the standard's right-side modal drawer rather than substituting a different navigation pattern. Implement Escape/outside/close behavior, focus trapping, focus return, background inertness and scroll-lock cleanup on every close path and desktop resize. VAU's original outside-click path does not reliably clear scroll lock; do not replicate it. The payload contains Alpine 3.12.3 core as a local asset; load it once with `defer` when implementing the standard's Alpine drawer. Its Persist/Intersect plugins are not required for basic navigation and are not bundled.

## Dialogs, alerts and special layouts

Read [dialog close controls](dialog-close-buttons.md) before styling Fancybox or CJuiDialog. It specifies exact artwork, dimensions, offsets, inherited plugin CSS, hover/focus stability and the current jQuery UI offscreen-glyph fix.

Distinguish full HTML pages/iframes (`layouts/dialog.php`) from `renderPartial()` responses inserted into `CJuiDialog` or Fancybox. AJAX partials must not add a document, duplicate jQuery or register the entire shell. Retain dialog IDs, open/close callbacks, confirmation actions, width limits and keyboard/focus behavior. Keep the target's jQuery UI runtime CSS (including overlay positioning/z-index); the Joyful CSS contains appearance overrides, not every plugin's structural rules.

The `XAlert` skin supplies green/yellow/red surfaces and icon appearance, but requires an existing compatible `XAlert`. Preserve flash keys, consumption and dismiss behavior. Its SVG close content needs an accessible label on the actual interactive close element. The simple `alertGreen`, `alertYellow`, and `alertRed` decorators are another option for existing messages; keep escaped text versus trusted HTML explicit and choose appropriate live-region semantics.

Adapt minimal/plain/error layouts from the same shell pieces without importing VAU services. Print/PDF layouts are independent contracts: preserve their typography, headers, page breaks, export CSS, and absence of web navigation. All routes may use the theme while print output still has its own layout; this needs no route-level theme switch.
