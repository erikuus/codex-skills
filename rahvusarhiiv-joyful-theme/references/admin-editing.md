# Contextual admin editing and Imperavi Redactor

## Admin pencil controls beside content titles

VAU's Joyful page/news/shop views expose editing in the content itself when the existing module authorization permits it. Follow that pattern for equivalent editable content:

- Put a small **pencil icon immediately after the title it edits**, in the same `flex gap-x-1.5 items-center` title group: a 6px gap, not a detached toolbar at the page edge. Shop product detail uses `items-end` for multiline product titles. Allow the title to wrap without shrinking or overlapping the control.
- Use a **32×32px circular hit area**: `flex w-8 h-8 shrink-0 items-center justify-center rounded-full text-base text-gray-200 hover:text-gray-800 hover:bg-gray-50`. Shop product surfaces use `hover:bg-gray-100`; preserve the source variant appropriate to that surface. Add visible keyboard focus (for example `focus-visible:ring-2 focus-visible:ring-green-300`).
- The source draws `<span class="fi-pencil"></span>` using its loaded Foundation icon font at `text-base` (16px). Keep that glyph if the target already loads the font, otherwise supply an equivalent **16px inline pencil SVG** with `aria-hidden="true"`; a bare `fi-pencil` class without its font produces no icon. Keep the icon-only link's translated `title` and an accessible name (`aria-label` or `sr-only` text).
- Preserve the existing authorization predicate such as `$this->isAdminAccess()`. The source module predicate checks guest state and its admin/RBAC policy; reuse the target's policy, not a new test based on the presence of a username, a CSS class or the active theme. Do not show the control to readers and rely on the edit action to reject them. Existing server-side action authorization must remain in place.
- Preserve the precise update route, record ID, return stack and fragment (`#article<ID>` / `#product<ID>` where present). Editing one card must return to that card. Do not nest the edit anchor inside the title's navigation anchor.
- News/shop cards use a stretched main link (`absolute inset-0`) and put the edit link above it with `z-30` on the flex item. Keep the edit link independently clickable and keyboard reachable; if the target's stacking context differs, use a positioned edit link and verify actual clicks. The rest of the card must still navigate normally.

Source map (paths relative to VAU):

| Source | Pattern |
| --- | --- |
| `themes/joyful/views/page/article/index.php` | Multiple article sections: admin pencil beside each heading; a single section has no repeated article heading, so its edit control remains by that section. Do not invent a duplicate title just to attach a pencil. |
| `themes/joyful/views/page/article/_admin.php` | Page/menu-level edit, manage-articles and add-article icons, rendered under the controller's admin check. Keep these separate from editing an individual article. |
| `themes/joyful/views/news/article/{_view,view}.php` | Pencil adjacent to article title in both list and detail; list uses `z-30` above its stretched link. |
| `themes/joyful/views/shop/{home,product}/_view.php` | Pencil beside the product title on cards, with return fragment and independent click layer. |
| `themes/joyful/views/shop/product/{index,view}.php` | Menu edit near the category title; product edit next to the product title in both detail layouts. |
| `protected/modules/{page,news,shop}/components/*Controller.php` | Actual admin predicates and returnable behavior. |

These small contextual edit icons are different from a page-level Add button or Print/help title-row links. Preserve their respective placement rules; do not turn every pencil into a large primary button or move it into global navigation.

## Required editor choice and scope

**Use Imperavi Redactor for rich-text editing in every Joyful implementation, replacing xhEditor.** This is a functional widget/integration change, not a CSS skin selection. A skin cannot turn `XHeditor` into `ImperaviRedactor` or change its upload protocol.

Update the shared/default-theme form and supporting module/application integration when they own the editor. Both default and Joyful presentations of the migrated form must use Imperavi. If a separate Joyful form exists, update both or share the smallest editor partial/configuration so they do not initialize different editors for the same field. Do not leave the underlying default form on xhEditor and declare the migration complete because a theme-only override looks correct. Theme-specific spacing and colors may differ; editor engine, model binding and endpoint contracts must agree.

This applies to actual rich-text fields, including extension-provided Help forms and multilingual fields—not every plain textarea. In VAU, `protected/modules/page/views/article/_form.php`, `page/views/menu/_form.php`, `news/views/article/_form.php`, and `shop/views/product/_form.php` already call Imperavi in the **default/shared view tree**. The shop's plain title textareas and the news annotation textarea remain plain. Some old xhEditor template routes/scripts and module option comments still exist, so their presence alone does not prove which editor a form runs; trace actual callers.

## Inspect and integrate the real extension

The inspected implementation is `/Users/erikuus/dev/yii/extensions-1.1.8/widgets/redactor/ImperaviRedactor.php`, wrapper version **1.2.22**, with local **Redactor 9.2.5** assets. Those are source observations, not a recommendation to downgrade another app or assume the API of a newer Redactor release. Resolve the target's actual `ext` alias and inspect its wrapper, assets and existing compatible copy first. Keep the implementation in `<ext>/widgets/redactor`, not application components or theme assets. This skill does not bundle the editor runtime; use the target's provisioned Redactor implementation and accompanying assets.

The observed wrapper extends `CInputWidget` and accepts **`model`, `attribute`, `options`, `htmlOptions`**, plus `selector`, `package` and `plugins` support. It generates a bound textarea when `selector` is null, publishes its assets, registers one `imperavi-redactor` package dependent on Yii-managed jQuery, and initializes `.redactor(...)` at `POS_READY`.

Migration mapping:

| xhEditor setting | Imperavi integration |
| --- | --- |
| `model`, `modelAttribute` | Same model, **`attribute`** with the same field name |
| `config` | **`options`**, with names supported by the actual Redactor version |
| `config.id` | Preserve the textarea ID via `htmlOptions['id']`; let model binding preserve its name |
| `tools` string | An explicitly mapped `options.buttons` array; not a copied xhEditor toolbar string |
| `width`, `height` | Responsive wrapper/textarea styling and supported `minHeight`/`maxHeight` options |
| `upImgUrl`, `upLinkUrl` | Redactor-compatible `imageUpload`, `fileUpload` routes |
| `loadCSS` | Inspect whether styles must target the editing surface or an iframe; use supported editor content-CSS options/module CSS, not a mechanical rename |

Minimal shared-form pattern, adapted to the actual attribute and required toolbar:

```php
<?php echo $form->labelEx($model,$attribute); ?>
<?php $this->widget('ext.widgets.redactor.ImperaviRedactor',array(
    'model'=>$model,
    'attribute'=>$attribute,
    'options'=>array(
        'minHeight'=>150,
        'pastePlainText'=>true,
        'buttons'=>array('bold','italic','unorderedlist','orderedlist','link','html'),
    ),
    'htmlOptions'=>array('class'=>'w-full'),
)); ?>
<?php echo $form->error($model,$attribute); ?>
```

Do not render a second textarea with the same ID. If using `selector` on an existing textarea instead, keep its binding and initialize it once. Preserve validators, scenarios, required/disabled state, hidden-field semantics, multilingual attributes, save/cancel/preview actions and submitted HTML. `pastePlainText` affects paste behavior; do not reinterpret it as permission to flatten existing stored HTML.

VAU toolbar/height examples: page article 500px with table/image/file/link/bold/italic/lists/HTML; page menu content 285px with the same tools, highlight content at least 100px with basic formatting; news content at least 150px with basic formatting/link/HTML; shop short content at least 150px with bold/italic/lists/HTML, long content 500px with image/file/link/bold/italic/HTML. These show different field needs—do not impose the full upload toolbar or 500px height on every field. Preserve needed template/plugin functionality by adapting it explicitly, rather than leaving a live xhEditor dependency or silently dropping a feature.

## JavaScript, uploads and editor appearance

- **One jQuery runtime.** VAU's old forms replace `scriptMap` with jQuery 1.8.3 and jQuery UI 1.9.2 mappings because its older framework needed them. Do not copy that downgrade or overwrite the target's scriptMap. Inspect package overrides and `jQuery.fn.jquery` in the rendered app. The inspected Yii 1.1.33-dev checkout itself contains jQuery 1.12.4; apps may override it. Redactor 9.2.5 contains `.size()` and `.load(handler)` calls that fail on jQuery versions where those APIs were removed. Use a compatible Redactor integration or update its local compatibility code deliberately, including debug and minified assets; do not load a second jQuery or broadly monkey-patch globals to mask problems. Test real toolbar and upload interactions, not just initialization.
- **Assets and language.** The wrapper selects `redactor.js` in debug and `redactor.min.js` otherwise. Verify both exist and behave consistently. It appends a language asset for a non-English `options.lang`; check the file exists before setting it (the inspected source has no `lang/et.js`). Do not point to a nonexistent locale merely because the app language is Estonian. Preserve a usable supported localization/fallback.
- **Upload contracts differ.** VAU uses separate `uploadRedactorImage` / `uploadRedactorFile` actions backed by `ext.actions.XRedactorUpload`; module `uploadImage` / `uploadFile` settings supply the routes. This action expects multipart field **`file`** and responds with JSON **`filelink`** or **`error`**. xhEditor's action defaults to **`filedata`** and an `err`/`msg` response. Do not reuse an xhEditor URL without adapting the request and response. The old upload action's docblock incorrectly shows `modelAttribute`/`config`; follow the actual Imperavi wrapper API above.
- Preserve the target's upload authorization, allowed formats/size limits, storage and public URL conventions. VAU's RequestController protects its editor upload actions with module roles; adapt the target's real permissions, not VAU role names. The inspected legacy XRedactorUpload checks the client-supplied MIME value, so it is a protocol reference rather than a reason to replace a stronger target uploader. Keep server-side content/type validation. Pass the current Yii CSRF name/token through supported extra upload fields (`options.uploadFields` in the inspected version) when CSRF validation is enabled; do not disable CSRF to make uploads work. Preserve existing callers of shared legacy endpoints until they are migrated.
- Surface upload errors as VAU does via `imageUploadErrorCallback` / `fileUploadErrorCallback`. Verify that the chosen plugin version consumes the actual response for images and files. Never fake successful insertion on an error response.
- **Keep structural Redactor CSS and plugins.** Style the surrounding Joyful field/label/error layout, responsive editor width and necessary editor-specific rules through scoped styles. Keep toolbars/popups usable and out of broad `prose` or text-input overrides. Inspect the actual DOM: local 9.2.5 uses `.redactor_box`, `.redactor_editor`, `.redactor_toolbar`; some VAU module CSS still targets `.redactor_content` and forces Verdana, so copying that CSS does not guarantee the right surface or Joyful typography. Adapt content typography to the target's rendered content without changing stored HTML.
- After migration, remove duplicate initialization and unused xhEditor scripts/options from the affected forms; search shared/default views, theme overrides, extension modules, controller actions, asset registrations and plugins. Do not delete shared legacy files still used by unrelated callers. For hidden panels, dialogs or AJAX-rendered forms, verify initialization, teardown and textarea synchronization without duplicate toolbars/handlers.

## Acceptance

Check guest, authorized editor and non-editor accounts: pencil visibility matches permissions; the pencil opens the intended edit form, the title/card link still opens content, and saving/canceling returns to the correct item/fragment. Compare 32px circular controls, 16px glyphs, 6px title gap, hover/focus and long-title wrapping.

For **both Joyful and default/shared forms**, verify the active editor is Imperavi and there is no xhEditor initialization on those fields. Exercise load → edit → save → reopen, source/HTML mode, formatting, links/lists/tables required by the target, validation failure with content retained, and multiple/multilingual editors. Exercise image/file uploads and errors where enabled, CSRF and permission rejection, existing content with old media URLs, modal/AJAX lifecycle and narrow layouts. Inspect browser console/network and both debug/production asset paths. Report any unavailable upload/service test explicitly; do not claim completion from a toolbar screenshot alone.
