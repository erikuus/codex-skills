# Integrating into an existing HTML-rendering app

## Adapt rendering, preserve behavior

Inspect the real output owners: shared header/footer includes, full documents, view fragments, admin entry points, AJAX responses, iframe/modal content and print/export views. Move shared shell ownership once; do not wrap each fragment in another document. Preserve head metadata, per-page assets, charset/language, URL prefix handling, CSRF fields, form methods/names/IDs, scripts and callbacks. The sample HTML's labels/URLs are specimen data, never a replacement for real routes.

Use the target's escaping helper for text/attribute/URL output and existing sanitization for trusted HTML. Changing layout must not change permissions, query semantics, return URLs or accepted values. Shared templates/partials may be factored where they reduce repetition, but do not introduce a framework, a generic renderer, a new theme engine or a directory per tiny fragment merely to host this design. Do not copy Yii PHP classes, skins, imports or `Yii::app()` setup into a non-Yii app.

Merge the asset starter into the app's normal asset location. Replace obsolete global layout CSS deliberately, retaining needed plugin structural CSS and narrowly scoped domain rules. Rebuild using the actual rendering sources. Check cascade ordering and preflight effects instead of layering a second handcrafted theme over the preset. Preserve zoom accessibility (`width=device-width, initial-scale=1`); do not carry over `user-scalable=0`/maximum-scale restrictions from old layouts.

The exact footer can be included by plain PHP, another server template engine, or compiled static HTML. `scripts/render-preview.mjs` only assembles a disposable specimen; it is not an application runtime dependency. Include the local Alpine core once to support its existing feedback action, and use the optional drawer script only when the app needs that drawer. Keep the app's own jQuery/plugin runtime where used; no duplicate jQuery or new jQuery dependency is required by the design.

## Nimeregister findings and migration boundaries

Inspected read-only at `/Users/erikuus/dev/php/nimeregister` while creating this skill. Verify current files before applying; these are integration clues, not a patch plan or claim of a migrated app.

- It is standalone PHP 8.5 with PostgreSQL and VauID, not a Yii application. Public PHP entry points include `frontend/views/_header.php`, a body view and `_footer.php`; the shared head receives `pageTitle`, `pageStyles`, optional `pageScripts`/`pageExternalScripts`/`pageDescription`.
- Existing public pages contain their own outer table-based layouts; `frontend/views/result.php` also renders the actual results table. Remove obsolete layout tables when introducing the shell, but preserve real data tables and row loops. Avoid nesting two full-page shells.
- Sorting/pagination links and result rows come from existing controller data. Preserve search/wildcard/year/county/parish filters, result anchors, summary counts, `tag` IDs, contribution ownership, and Saaga archive/image URLs. Pagination markup is in `_pagination.php`.
- VAU bookmark markup and initialization are already generated; move available controls to the header while retaining the actual script hooks, not guessed service URLs.
- `add.php`, `report.php` and related controls use existing Thickbox and tooltip behavior. A CSS migration must preserve full-document versus partial/iframe contracts, response shape, validation, CAPTCHA, return context and popup dimensions. Inspect `thickbox.js` before changing its hooks.
- Admin forms have their own entry points/views, authorization and CSRF checks. Inspect both public and admin rendering, including PHP files outside `admin/views` that emit markup. Do not change the VauID flow, configuration, private overrides, database or stored data for design work.
- Introduction editing uses locally bundled Quill 2.0.3 and `frontend/css/content.css`. **Keep that editor and content behavior.** This skill has no Imperavi requirement or editor-migration assets. Preserve `content/` files and editor synchronization/escaping; style only the surrounding form where appropriate.

Running tests may need PostgreSQL, php-cgi or external authentication. Report blocked checks specifically and still finish independent source/build/visual checks. Do not mutate the database or contact external users as a substitute for testing markup.

## Existing dialogs

Preserve each installed dialog library, original close handler, accessible name, focus behavior and structural stylesheet. Do not install Fancybox or jQuery UI simply because the reference app uses them. Plain HTML `<dialog>` is supplied only for the optional navigation drawer, not a universal replacement for domain dialogs.

When the target already has **Fancybox 2**, preserve its native sprite close button: 36×36px at top/right -18px, with overflow visible on the skin/wrap; retina sprite background size 44×152px. Keep plugin assets and configured nondismissible behavior. Joyful adds rounded 8px surfaces, not a different close glyph.

When the target already has **jQuery UI Dialog**, follow the source geometry: 20px close glyph at a 16px right inset, stable hover/focus positioning and titlebar/content padding 12px×16px. Preserve its structural CSS and existing dismiss vetoes. If replacing the glyph through a pseudo-element on `.ui-button-icon-only`, center it absolutely so the plugin's negative text indent does not send it offscreen. Scope overrides to that close control; do not hide all `.ui-icon` elements.

For **Thickbox or another library**, inspect and retain its own DOM/asset/close contract. Transfer shared type, palette and surface styling where supported, then verify actual close/cancel/keyboard behavior. Never assign Fancybox dimensions/selectors to an unrelated control. Keep AJAX fragments free of duplicate layouts and runtime scripts.
