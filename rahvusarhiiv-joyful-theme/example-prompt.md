# Apply Joyful to another application

Replace `/absolute/path/to/app` with the target application's root directory, then copy the prompt below. The installed skill and its references remain authoritative as they evolve.

```text
Use $rahvusarhiiv-joyful-theme to implement a complete Joyful theme for /absolute/path/to/app, starting from its default design. Apply all current skill rules, including the refinements developed while theming Pitserid.

Read the skill's SKILL.md and relevant references before editing. Inspect the app's AGENTS.md, framework version, layouts, views, modules, portlets, extension implementations and asset configuration. Compare default views with the corresponding VAU Joyful patterns. Implement the changes, not merely a plan. The skill targets Yii 1.1.33-dev; identify a framework mismatch before installing incompatible components, and keep a framework upgrade separate from this theming task.

Use these design sources:
- Shell and exact footer: /Users/erikuus/Documents/Github/tailwindui-playground/views/layouts/advanced-layout-alt.html
- Component and view patterns: /Users/erikuus/dev/php/vau/themes/joyful/views/
- The skill's upgraded Yii components, institutional preset and reproducible Tailwind 4 build.
Use the skill's bundled reference snapshots when the original source paths are unavailable. Follow its explicit current rules where historical source markup differs.

Enable Joyful globally with Yii::app()->theme='joyful' or equivalent application configuration. Do not implement route restrictions or user theme selection.

Cover all common application surfaces:
- Responsive shell, navigation, mobile drawer, gradient breadcrumbs and exact reference footer. Omit Home/Avaleht from desktop/mobile main header menus even when the default theme includes it; preserve the logo home link and breadcrumb home icon.
- Use the skill’s exact basic-layout header-gradient override; keep the advanced-layout-alt shell, footer and all other palette values unchanged.
- Login with the VAU account-circle icon; existing enabled XVauBookmark/XVauHelpdesk controls in the upper-right institutional header.
- Left menus with VAU geometry and active/hover states. Skin concrete XPortlet subclasses through supported properties, preserving their menu logic.
- Single-field search with the compact shop-search pattern above the existing menu, including submission and clear behavior.
- Grids, detail views, forms, validation, action rows, alerts and dialogs.
- Form-page title, actions, underline and body inside one shared narrower container. Keep error summaries within it.
- Group headings outside the large-screen field-body inset; compact year/century ranges and measurements with adjacent units.
- Existing field tips, including bulb images, replaced by the small circled-i at the right of the label row, preserving their content and behavior without widening compact fields.
- Stacked radio choices with correctly indented dependent panels and unchanged submission semantics.
- Secondary buttons transitioning from white to light gray on hover.
- Add/New buttons with plus icons at the right of the title row; Print/help as icon + text there. Remove standalone Back buttons when breadcrumbs exist, preserving Cancel and workflow navigation.
- Titled detail groups without horizontal separators.
- Correct Fancybox and CJuiDialog close controls.
- Permission-gated admin pencils beside editable content titles.
- Imperavi Redactor replacing xhEditor for actual rich-text fields, including default/shared forms and required upload integration. Preserve existing editing capabilities and keep plain-text fields plain.

Install reusable Tailwind PHP components under the resolved extension root's components/tailwind directory, never application components. Use the institutional preset and source scanning; rebuild CSS after view/skin changes.

For optional small-screen fading text, identify suitable blocks first. Ask whether each should collapse and how many rendered lines should remain visible. Wait for both choices before implementing; otherwise retain full text. Continue independent work while waiting. This general theming request does not authorize automatic text collapsing.

Preserve the target application's own routes, permissions, translations, data and workflows. Inspect and preserve its specialized viewers, maps, uploads, image controls, custom dialogs, AJAX settings and other integrations where present. Use Pitserid's lessons without copying its domain-specific fields or navigation. Apply conditional patterns only where the target has the corresponding functionality.

Verify representative public and admin pages, create/update forms, validation errors, menus, grids and dialogs at phone, tablet and desktop widths. Compare screenshots and computed geometry with the references, exercise actual interactions, and run appropriate PHP/build checks. Check print/export layouts separately.

Complete the implementation and report changed surfaces, verification results and any genuinely unverified behavior.
```
