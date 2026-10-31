# Extraction evidence

Inspected on 2026-10-31. This is source-based reverse engineering; it is not a claim that the four comparison applications were themed or that their live pages were tested.

## Source priority and observed Pitserid failure

The user designated `advanced-layout-alt.html` as the shell standard and requires its footer information exactly. The bundled template/footer preserve that source. VAU's main layout and `vau-bookmark-list.html` supply the breadcrumb strip and table patterns absent from the generic shell; absence in that generic shell is not an instruction to restyle or move them.

The subsequent Pitserid working tree was inspected read-only. It showed:

- PHP widgets installed under `protected/components/joyful` and imported from `application.components.joyful`, following the earlier skill's wrong placement advice.
- No Tailwind build scripts in its package configuration; a frozen style.css with a large handwritten `joyful-adapters.css` layered on top.
- Source custom `rounded` (8px) replaced with .25rem, custom multi-layer shadows replaced with short default-like shadows, and colors such as `#43464a`, `#2463a6`, `#DCF4E5` replacing the institutional tokens.
- Breadcrumbs reduced to plain text/› separators in white content, rather than the gradient strip with the white home-icon tile and SVG separators.
- `shadowGrid` replaced by a plain wrapper and independently styled `.joyful-grid` rules, including a universal mobile 36rem minimum table width.
- The exact reference footer replaced with application-specific contacts/copyright/link selections.
- Tests mostly asserted header height, route hooks, visibility and viewport fit. Those assertions could pass with the wrong visual design.

These are source-code findings, not a claim of inspecting a running Pitserid instance. Its application repository was left unchanged. The revised skill removes those instructions, provides a source-based CSS build, restores concrete breadcrumb/grid examples, and adds actual Yii render/source-style comparisons. Browser probing of the reusable baseline is separate from reviewing the target's completed integration.

## Source locations

- VAU: `/Users/erikuus/dev/php/vau/themes/joyful/views`, corresponding `protected/views`, `protected/portlets/views`, and module views when relevant.
- Actual visual assets: VAU `css/themes/joyful`, `images/joyful/ra_logo.svg`, `images/select2.png`, `js/alpine.3.12.3.min.js`. The theme directory itself contains views only.
- Original adapters: `/Users/erikuus/dev/yii/extensions-1.1.8/components/tailwind/*.php`; inherited implementations inspected in `widgets/form/XDynamicForm.php`, `widgets/grid/flagcolumn/XFlagColumn.php`, and the relevant navbar/Foundation classes.
- Target core: `/Users/erikuus/dev/yii/yii-1.1.33-dev/` (this directory itself is the framework root; there is no nested `framework/`).
- Existing skill icons: `/Users/erikuus/.agents/skills/rahvusarhiiv-design-system/assets/RA_logo_Ikoon_must.{svg,png}`. Copied byte-for-byte for the requested shared icon.

`view-map.json` inventories 276 theme PHP views and identifies default-file candidates for 227. The remaining entries include new skins, decorators, new themed screens, and widgets/modules outside the simple path mapping. A candidate match is a discovery aid, not proof of equivalent behavior. The generic conclusions below come from reading paired implementations; domain-specific routes are deliberately excluded from the payload.

## Paired findings

| Default → Joyful evidence (relative to VAU) | Reusable conclusion | Excluded detail |
| --- | --- | --- |
| `protected/views/layouts/main.php` → `themes/joyful/views/layouts/main.php` | Fixed legacy shell becomes responsive nested surfaces, typography, gradient header and common container widths. | VAU menus, admin/sidebar visibility, account integrations, carousel, analytics and session-service configuration. |
| `protected/views/company/_form.php` → themed counterpart | Preserve fields, models and callbacks; substitute `XTActiveForm`, remove pixel widths, use spaced rows, group headings and full-width action buttons. | Company types, warranty/ERP metadata, attachment business rules. |
| `protected/views/company/create.php` → themed counterpart | Page title and narrow form wrapper surround the same partial invocation. | Company-specific labels and routes. |
| `protected/views/company/_view.php` → themed counterpart | Essentially identical data/attribute configuration (only a trailing comma changes); skin + decorator provide common detail styling. | Company data attributes. |
| `protected/views/company/view.php` → themed counterpart | Wrap related data sections and grids with typography/table decorators; retain permission expressions. | Invoice/ERPLY/company membership workflow. |
| `protected/views/order/_grid.php` → themed counterpart | Styled grid columns, action icons, responsive/typography wrappers and existing JS hooks must cooperate. | Large order-specific collapse/batch/selection logic; not a generic grid recipe. |
| `protected/portlets/views/mainMenuStatic.php` → `themes/joyful/views/MainMenuStatic/mainMenuStatic.php` | Widget-class theme resolution and responsive menu options. | Default is a stub; VAU's item slicing, helpdesk/FAQ APIs are not common contracts. |
| `protected/portlets/views/pageSizeMenu.php` → `themes/joyful/views/PageSizeMenu/pageSizeMenu.php` | Popover spacing and page-size control presentation. | Default is a stub; `createSetPagesizeUrl()` is VAU-specific. |
| `themes/joyful/views/skins/*`, `views/decorators/*` | Most reusable styling is centralized instead of rewriting every widget's data configuration. | Skins naming custom actions or unsupported extension properties need adaptation. |

## Cross-application triangulation

All four have `protected/views/layouts/main.php`, legacy fixed-width containers, ordinary Yii model forms and grids, plus menu/portlet PHP that can render independently of view files. They differ in domain tools and route behavior, so conversion must be structural rather than copying a VAU screen.

| App | Representative common surfaces inspected | Domain-specific parts to retain |
| --- | --- | --- |
| `pitserid` | `layouts/{main,leftbar,rightbar,sidebars,print}.php`; `seal/{_form,_search,_grid,view}.php`; `portlets/MainMenu.php`, search portlet | Seal image links/Fancybox, owner/figure highlighting and custom `showImage`, `updateSeal`, `deleteSeal` buttons. |
| `kaardid` | `layouts/{main,leftbar,plain,print}.php`; `institution/_form.php`; archive/institution/map grids; Search/SearchAdvanced/SearchExtended/SearchStat portlets | Map/image workflows, tabular and batch editing, updater/service code. Its main layout has jQuery UI stacking fixes that need preservation. |
| `haldusyksused` | `layouts/{main,leftbar,rightbar,sidebars,print}.php`; `unit/{_form,_search,index,admin}.php`; `type/{_form,admin}.php` | Unit hierarchy/breadcrumbs, tree dialog, Leaflet input map, autocomplete and batch operations. |
| `aadresslehed` | `layouts/{main,leftbar,rightbar,sidebars,error,print}.php`; `sheet/{_form,_grid}.php`; search portlet | Sheet viewer, draggable/slider controls, image-specific dimensions and custom update/delete dialog. Existing `ajaxUpdate=false` remains intentional. |

## Compatibility findings behind the upgrade

- Original `XTCheckBoxColumn::renderHeaderCellContent()` returns before echoing its inherited multi-select checkbox. The new implementation uses the current getter API and tests both selection modes and header templates.
- Original `XTHtml::errorSummary()` predates Yii's default error encoding. Delegating to current core prevents carrying that obsolete behavior forward.
- Original form/reorder code and inherited `XFlagColumn`/`XDynamicForm` call removed jQuery `.live()`. Simply changing the seven top-level files would leave broken inherited code, so the package includes the upgraded dependencies.
- Original dynamic dropdown disables inactive areas only at startup; subsequent changes can submit hidden fields. The bundled implementation recalculates disabled state each time.
- Original flag requests use GET and unscoped selectors; original reorder requests omit CSRF data. The portable handler is scoped per grid and column, uses POST and includes the active token. Target endpoint compatibility still needs checking.
- Source `LinkPager`/`Breadcrumbs` are full copies of Yii 1.1.11-era classes. Current core plus a small pager subclass/skin supplies the equivalent presentation without duplicating obsolete pagination/breadcrumb internals.
- Mobile detail headers are hidden in source decorators, and source drawer close paths do not all restore scroll. The reusable recipes preserve labels and specify complete close/focus behavior instead of codifying those defects.

[baseline-sha256.json](baseline-sha256.json) records the packaged assets and the inspected core-file fingerprints for reproducible comparison.
