---
name: rahvusarhiiv-joyful-theme
description: Apply the Rahvusarhiiv Joyful design to Yii 1.1.33-dev apps using the advanced-layout-alt reference, exact reference footer, a reproducible Tailwind 4 build with the institutional preset, and shared ext.components.tailwind widgets. Use for apps such as pitserid, kaardid, haldusyksused, or aadresslehed while preserving their routes, permissions and domain behavior. Excludes per-user theme selection and route-based theme switching.
---

# Rahvusarhiiv Joyful theme

Implement the existing design faithfully. Enable it for the entire web application with `Yii::app()->theme='joyful'` or configuration `'theme'=>'joyful'`. Keep the target's business logic, routes, permissions, inputs and integrations; theme preferences and route allowlists are out of scope.

## Read the design and build contracts first

- [Layout standard](references/layout-standard.md): `advanced-layout-alt.html` is authoritative for the shell. **Preserve its footer information and behavior exactly.** The bundled `_footer.php` is the complete original footer subtree.
- [Tailwind build](references/tailwind-build.md): build CSS from the playground's institutional preset using the supplied pinned Tailwind 4 pipeline. Frozen VAU CSS is comparison evidence only.
- [View patterns](references/patterns.md): VAU supplies the breadcrumb, grid, detail, form and widget adaptations missing from the generic shell. The generic shell's absence of breadcrumbs does not mean relocate them into white content.
- [Integration](references/integration.md): reusable PHP classes belong under the resolved **extension root's `components/tailwind/`**, imported as `ext.components.tailwind.*`.

Do not replace the preset with approximate colors/shadows/radii or rewrite reference utility markup as an independent handwritten theme. A successful behavioral test or absence of horizontal overflow does not establish visual fidelity.

## Inspect the application

Read its AGENTS.md, entrypoint/config, resolved `ext` alias, framework version, widget factory, layouts, portlets, module views and client scripts. Inspect referenced `X*`/`ext.*` implementations in that extension root. This payload targets Yii 1.1.33-dev; framework migration is separate work.

Make a compact coverage map of main/nested layouts, navigation, breadcrumb ownership, public search and results, admin grid, detail, create/update forms, shared dialogs, module views, print/export/error layouts. Inspect the same source and target surfaces before editing. Capture representative target pages and corresponding reference pages when a browser is available; preserve evidence in the work area. See [evidence](references/evidence.md) for source paths and the diagnosed Pitserid failure.

## Stage components and build CSS

1. Run `python3 scripts/stage_assets.py /absolute/app --extensions-root /resolved/ext`. Review its two destinations; use `--apply` to copy nonconflicting files. It never guesses or changes the `ext` alias and never overwrites an existing shared implementation.
2. Merge existing components deliberately. Use **`<ext>/components/tailwind`**, not an application component directory. Inspect other consumers before changing a shared library. Remove a previous application copy/import only after all its callers have moved and the target extension implementation has been verified.
3. Add `ext.components.tailwind.*` to imports; enable `components.widgetFactory.enableSkin`, retaining existing settings and concrete-class allowlists. Skin properties can be overridden by explicit widget configuration, so remove obsolete visual overrides case by case.
4. In `themes/joyful/tailwind`, run `npm ci`, then `npm run build -- --extensions-root /resolved/ext`. Use `npm run dev -- --extensions-root /resolved/ext` while editing. Commit source files and lockfile; follow the target's asset-release convention for the generated `css/style.css`. No CDN compiler or runtime npm is needed.
5. Rebuild after changing PHP/HTML/JS class strings, including extension PHP. The builder scans theme views/JS, application views/portlets/components/modules, and extension widgets/modules/Tailwind components. Add `--source` for any rendering directory outside those roots. Explicit literal class strings must be present; PHP string interpolation does not create detectable utilities.

## Integrate the actual views

Preserve the source shell's utility classes, surface nesting, widths, spacing, header/menu positioning and footer. Fill the starter's application navigation/account/language/logo slots from real target data, implement the reference mobile drawer, and preserve its actual script hooks. Do not leave empty placeholder sections and call the layout complete. Footer slots are not customizable: render the bundled exact `_footer.php`. If `XVauBookmark` and/or `XVauHelpdesk` exist in the target, render the available enabled widgets as icons in the **top-right of the 48px institutional header**, where VAU places its language picker. Preserve their settings and popup behavior; see [header utilities](references/layout-standard.md#top-right-utility-icons).

Render breadcrumbs once **on the gradient, after the application header and before the white content panel**, using the bundled `CBreadcrumbs` skin (home icon tile, SVG separators, source padding/type). Remove duplicate presentation calls from nested layouts while preserving their breadcrumb data. **When a page has breadcrumbs, omit its standalone Back button.** Keep form cancellation, dialog dismissal and workflow Previous actions that have a separate purpose.

Keep grid providers, columns, custom actions, filtering, sorting, pager configuration and AJAX hooks. Wrap the grid in `shadowGrid`; use its typography variants and the concrete `CGridView` skin together. Preserve `grid-view`, `items`, `summary`, `pager`, action/selection hooks and custom button IDs. Use the upgraded XT columns where appropriate. Scroll the items region only when necessary; do not impose a universal fixed/minimum table width or restyle every table through broad selectors.

For a single search field with Go/Search and Cancel/Clear controls, use the [compact shop-search pattern](references/patterns.md#single-field-search), with icon actions in one rounded search bar above the existing menu.

Use `XTActiveForm`/`XTHtml` as described in the patterns reference, preserving validation, IDs, names, form method/action, uploads, hidden values and callbacks. Keep detail labels intelligible on mobile. Retain structural jQuery UI/plugin CSS and existing dialog behavior; style its appearance through the compiled integration layer. Follow [the explicit close-control rules](references/dialog-close-buttons.md): Fancybox 2 retains its 36px sprite button at -18px top/right; CJuiDialog uses the 20px SVG at a 16px right inset, with the current jQuery UI pseudo-element compatibility fix. Keep print/export documents separate from the web shell.

Apply these presentation rules consistently:

- **Secondary buttons, including Cancel, are white at rest and light gray on hover**: `bg-white hover:bg-gray-100`, with `text-gray-900` and `border-gray-200` retained. Follow [form controls](references/form-controls.md); avoid conflicting primary button defaults.
- **Form-page titles, their actions and underline share the form’s narrower container**: wrap the title row and form body together, not only `_form`. Keep group-field indentation inside this outer column; see [form-page width ownership](references/patterns.md#form-pages-title-and-body-share-one-width).
- **Titled form groups keep their heading at the outer edge and inset their field body on large screens** using the enquiry form’s `space-y-6 xl:mx-6`; see [grouped forms](references/form-controls.md#grouped-forms-inset-fields-below-an-outdented-heading).
- **Ranges and measurements are compact exceptions to full-width inputs**: keep start/end fields with their dash on one line and measurement units immediately after a suitably sized input; use [compact wrappers and examples](references/form-controls.md#compact-fields-ranges-and-measurements) to avoid conflicting `XTActiveForm` width classes.
- **Every existing field tip/help control, including bulb images, becomes a small circled-i at the right of the label row above the input**, following “Koosta tellimus” in `order/index?scope=clientDraft`. Preserve its help content, URL or tooltip behavior; see [field-tip placement and migration](references/form-controls.md#field-tips-info-icon-on-the-right-of-the-label-row).
- **Radio groups follow bookmark/link/update**: stacked radio + inline-label rows with dependent fields indented below the selected option. Preserve the dynamic helper’s sibling structure and submission behavior; see [radio group layout](references/form-controls.md#radio-groups-bookmarklinkupdate-pattern).
- **Login includes the VAU account-circle icon before its translated text**, using the compact dark button in [login styling](references/layout-standard.md#login-button).
- **Titled groups in detail views have no horizontal separators**: distinguish groups through headings and spacing, not `<hr>`, dividing borders or an underline on every group heading.
- **Page-level Add/New/Create buttons belong on the right of the title row**, with a plus icon before the translated label and the compact dark primary style from `bookmark/link/admin`. Place related secondary controls immediately before Add; see [Add buttons](references/patterns.md#addnew-buttons-in-the-title-row).
- **Page-level Print and help actions sit to the right of the page title as icon + text**, following `order/index?scope=clientDraft` and the supplied screenshot. Use the [title action row](references/patterns.md#page-title-and-utility-actions); retain the single shared page-title underline.

For left navigation and menus extending `XPortlet` (such as `ManageMenu`), read [left menus and extension skins](references/left-menus.md). Match VAU's uppercase underlined group titles and rounded green active/hover links. Apply a skin for the **concrete class**, disabling its legacy CSS and setting supported presentation properties; preserve the existing menu data, visibility and route logic. An `XPortlet.php` skin alone does not skin `ManageMenu`.

For editable page/news/shop-style content, put the authorized admin pencil immediately beside the content title using the [contextual editing pattern](references/admin-editing.md#admin-pencil-controls-beside-content-titles). Preserve edit permissions, routes and return fragments.

**Rich-text editing must use Imperavi Redactor instead of xhEditor.** Follow [the editor migration contract](references/admin-editing.md#required-editor-choice-and-scope): migrate shared/default-theme forms and supporting widget/upload integration as needed, so the editor choice is consistent across both themes. This is explicitly part of applying Joyful, not a skin-only change. Keep plain-text fields plain and preserve stored content and form behavior.

## Verify before reporting completion

Follow [verification](references/verification.md). Run PHP/PHPCS checks, build CSS, exercise relevant application behavior, and **compare actual screenshots and computed design values with the references** at phone, tablet and desktop sizes. Inspect the header, breadcrumb, grid, form, detail and exact footer, not just a homepage. The package supplies real Yii render probes and source-CSS parity checks; they validate the reusable baseline but do not substitute for testing the integrated application.

Report surfaces migrated, commands/checks run and actual visual comparisons, plus unverified routes or service-dependent behavior. Do not claim a finished migration while menus are placeholders, the CSS was not rebuilt, only structural assertions passed, or any reference difference is unexplained.
