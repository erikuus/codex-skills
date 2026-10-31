# Integration and component contracts

## Placement and configuration

There are two destinations. Copy `assets/app/` relative to the target web root and `assets/extensions/` relative to the **resolved Yii `ext` alias**. The resulting PHP directory is `<ext>/components/tailwind/`, normally `protected/extensions/components/tailwind/` in these upgraded apps, but potentially a shared extension tree. Never relocate it to `protected/components/joyful` or change an established `ext` alias just for this theme.

Resolve the alias from actual config/entrypoint/runtime before staging; the script requires `--extensions-root`. Preserve a shared library's existing consumers and version compatibility. The payload targets 1.1.33-dev and must not be dropped into a still-used 1.1.8 runtime without considering those consumers. Do not automatically overwrite shared implementations. Class names remain `XT*`; remove old application imports/copies only after updating all consumers and verifying that the extension implementation is the one loaded.

Merge these entries into the real web application configuration:

```php
// Relevant entries only; preserve all existing configuration.
'theme'=>'joyful',
'import'=>array(
    'ext.components.tailwind.*',
),
'components'=>array(
    'widgetFactory'=>array('enableSkin'=>true),
),
```

Setting `Yii::app()->theme='joyful'` before rendering is equivalent. No preferences/routes logic is needed. A custom widget factory may override Yii skin handling; inspect it before relying on this configuration. Yii's native factory uses theme skins over application skins and merges explicit widget properties over the skin. Remove obsolete explicit `cssFile`/style options where they defeat the theme, but retain functional options. Class names of skins must match the concrete widget class; parent skins are not automatically inherited by custom subclasses.

Theming controller views mirrors `protected/views/`; module views use `themes/joyful/views/<module>/<controller>/`; widget views use `themes/joyful/views/<ConcreteWidgetClass>/`. Explicit filesystem includes and view aliases can bypass theme lookup. Audit those separately. Native APIs and precedence were checked in the local 1.1.33-dev `CTheme`, `CWidget`, and `CWidgetFactory`, and agree with the [Yii theming guide](https://www.yiiframework.com/doc/guide/1.1/en/topics.theming) and [widget-factory API](https://www.yiiframework.com/doc/api/1.1/CWidgetFactory).

## What is bundled

| File/class | Role and upgrade |
| --- | --- |
| `XTHtml` | Joyful links/buttons and error-summary appearance; delegates core markup, POST/CSRF/click handling and default error escaping to the current `CHtml`. Fixes `focus-visible::` typo. CSS class arguments append to defaults; conflicting Tailwind utilities do not have guaranteed last-string-wins precedence. |
| `XTActiveForm` | Styled labels, inputs, selects, radio/check boxes, checkbox lists and error summary. Inherits a bundled `XTDynamicForm`, preserving dynamic-area APIs. Uses parent `CActiveForm::errorSummary()` for summary registration and escaping. Standard inherited methods such as file fields retain core behavior. |
| `XTDynamicForm` | Namespaced-by-class-name copy of source `XDynamicForm`, avoiding collision with an existing legacy base. Uses `joyful.js` for scoped modern events and disables inactive dropdown inputs on every change while preserving pre-disabled inputs. The historical `enableChecboxToggle` spelling remains supported. Radio/checkbox toggles preserve the source visibility-only behavior. |
| `XTButtonColumn` | Current `CButtonColumn` handles default actions and click registration; only SVG rendering/appearance changes. Supports custom `icon`, `url`, `visible`, `options`, and parent `imageUrl` fallback. Adds accessible names. |
| `XTCheckBoxColumn` | Overrides current `getHeaderCellContent()` and preserves `headerTemplate`, blank headers, independent selection modes, and the `select-on-check-all` hook. Fixes the original unreachable select-all output. Row checkbox behavior stays in current `CCheckBoxColumn`. |
| `XTFlagColumn` | Now derives from current `CDataColumn` instead of old `XFlagColumn`; keeps sorting, `name`, SVG yes/no flags, `flagClass` / `flagClasses`, and callback parameters `pk`, `name`, `value`. Uses POST+CSRF and scoped updates. Old inherited bitmap `icons` mode is intentionally not provided; adapt such a target explicitly. |
| `XTReorderColumn` | Uses current grid content getters and current provider keys; retains up/down SVG, `callbackUrl`, `triggerCssClass`, and `reorderVisible`; sends `id`/`move` via the same callback URL with POST+CSRF. |
| `XTGridAction` + `assets/joyful.js` | Shared event registration for flag/reorder actions; separate event namespace per grid/column, delegation across AJAX row replacement, no duplicate registration, visible errors and `joyful:action-error` hook. Prevents concurrent duplicate clicks on a link. |
| `XTStepBar` | Responsive step progress display. Filters invisible steps before calculating connectors and HTML-encodes labels by default; use `encodeLabel=false` only for trusted markup. |
| `XTLinkPager` | Small subclass of current `CLinkPager`, replacing VAU's full copied 1.1.11 pager. Preserves flat links inside `<nav>`, core range calculations, current-page state and disabled controls. Uses its own skin. |

The seven original `components/tailwind/*.php` files are all represented. The three extra PHP classes supply dependencies/current-framework adaptation, not domain behavior. All local dependencies are in the same folder; optional third-party widget implementations are not bundled.

### Mutation endpoints

A theme must not invent flag or reorder functionality. Use those columns only when the target already has corresponding actions and permission checks. Flag's original base performed a mutation with GET; this bundle uses POST. Verify the existing endpoint accepts POST, enforces authorization and CSRF, and preserves its parameters. Do not add a permissive `save(false)` controller action copied from old extension examples. Flag expects JSON; reorder accepts a successful response. Adapt the response contract deliberately if the target differs. Core `CButtonColumn` delete is separate and retains its existing confirmation/handler logic.

### Skin inventory

Always useful: `CGridView`, `CListView`, `CDetailView`, `CBreadcrumbs`, `XTLinkPager`.

Conditional: `CJuiDatePicker`, `CJuiAutoComplete`, `CMaskedTextField`, `CCaptcha`; extensions `XAlert`, `XDateSelect`, `XGroupGridView`, `XSelect2`, `XTagInput`. The extra skin files do not instantiate those widgets. Before enabling an existing extension's skin, inspect its supported properties and version. Select2 CSS is the source's older Select2 appearance; it is not compatible by assumption with Select2 4.x. Preserve the target's search thresholds, callbacks, date formats, locale and captcha action. The bundled captcha skin omits VAU's `joyfulCaptcha` action override.

Theme URLs use `Yii::app()->theme->baseUrl`, not VAU's `XHtml::cssUrl()` or a hardcoded `/vau` prefix. JavaScript for dynamic forms/actions is published by Yii's asset manager from the component's `assets/`; it uses Yii-managed jQuery. Ensure the normal asset directory is writable and its generated URLs load. Do not load a second jQuery copy.

## CSS and assets

Read [the Tailwind build contract](tailwind-build.md). The runtime stylesheet is generated by the pinned modern build from the playground preset and source integration rules. Historical CSS is bundled under `assets/reference/` exclusively for visual comparison. Do not deploy a frozen snapshot as the target's final stylesheet or maintain a second handwritten theme beside the generated file.

Keep the footer from `advanced-layout-alt.html` verbatim: `_footer.php` is the exact subtree, including feedback behavior, link labels/destinations, postal address, phone/email and social links. Main loads the local Alpine core once to support that footer and the reference drawer. No target-specific replacements or copyright/app-name additions belong in this footer.

Theme CSS URLs use `Yii::app()->theme->baseUrl`. `gridview.css` supplies sort arrows and depends on bundled `up.gif`/`down.gif`; it is only a supplement to the generated typography/decorator styling. Select2's old relative sprite URL points at the bundled `../images/select2.png`. Optional plugin styles are version-specific and need checking against the target. Local fonts remain under `css/fonts/`.

Do not load legacy `960.css`, old main/form CSS or old grid skins globally with the new shell. Preserve narrowly scoped plugin structural rules and domain viewers/maps. Use source utility markup for common appearance; if a generated class is missing, fix source detection or v4 syntax and rebuild before adding CSS. Add focused widget integration rules in the build sources only when the reference/target behavior requires them, using preset values rather than invented approximations.
