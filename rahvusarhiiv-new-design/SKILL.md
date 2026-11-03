---
name: rahvusarhiiv-new-design
description: Apply the exact Rahvusarhiiv Joyful-derived design to plain HTML and server-rendered templates in existing apps, including standalone PHP apps such as nimeregister. Provides a pinned Tailwind 4 build, institutional preset/fonts, exact footer, responsive shell, tables, narrow detail views and action SVGs. Preserves the app’s backend and existing editors; does not require Yii, theme engines or editor migration.
---

# Rahvusarhiiv New Design

Implement the established design through the target's existing HTML templates and assets. This is the framework-neutral counterpart of `rahvusarhiiv-joyful-theme`, not a new visual direction or a backend migration. It is self-contained: no other installed skill is needed. Keep URLs, permissions, data, forms, AJAX contracts, translations and existing editor behavior. Do not install or replace a rich-text editor as part of this skill.

Copy the [example prompt](example-prompt.md) when starting a target implementation.

## Inspect and scope

Read the target's AGENTS.md and actual rendering/asset pipeline. Identify full pages, shared header/footer includes, admin pages, partial/iframe/dialog responses, print/export layouts, table generators and scripts that depend on markup. Map corresponding surfaces before editing. Prefer existing templates/helpers over introducing a theme engine or component framework. In PHP, retain existing escaping and trusted-HTML boundaries.

Use [integration](references/integration.md), including the read-only Nimeregister findings. Do not copy that app's domain content into another app. Modify the app only when asked to apply the skill; creating or reviewing this skill does not authorize an app migration.

## Build from the packaged design

- Read [Tailwind setup](references/tailwind.md). Stage/merge `assets/starter/` into the target's normal asset location and run its pinned build with explicit source directories/files. No Yii paths, widget skins, PHP adapters, CDN compiler or frozen stylesheet installation.
- Keep the supplied preset, fonts, radii, shadows, spacing and type scale. The runtime header gradient is `linear-gradient(96.04deg, rgba(247, 227, 204, 0.65) -17.14%, #ECDDF4 94.45%)`; the retained `bg-theme-vau` token is a style name, not application branding.
- [shell.html](assets/html/shell.html) and [components.html](assets/html/components.html) are readable HTML specimens. Extract their structure into real target templates; replace specimen labels, links, IDs, sample forms and data with the app's actual output. Their comment markers are for the preview renderer, not a new runtime template system.
- [footer.html](assets/html/footer.html) is the exact approved footer subtree. Preserve its information, links, artwork, markup and feedback action. Load the bundled Alpine once for that action, or preserve equivalent behavior with the existing runtime when syntax prevents direct reuse; verify exact information and popup options in either case. The default is the byte-identical HTML fragment.

## Apply the visual contract

Read [design and HTML patterns](references/design.md) for dimensions, source evidence and usage:

- Keep the 48px institutional header, gradient application header, nested white content panel and exact footer. Use the real app identity/navigation, responsive 80rem/90rem shell and supplied mobile drawer pattern. Never invent language/authentication/menu actions.
- Omit Home/Avaleht from desktop and corresponding mobile main menus even if the old menu contains it. Retain the app-logo home link and breadcrumb home icon. Place existing enabled bookmark/helpdesk utilities at the top right, preserving their integration.
- Render breadcrumbs once on the gradient above the white content panel. Omit redundant standalone Back controls when breadcrumbs exist; keep Cancel and workflow navigation.
- Reproduce the source table surface, padding, alternating rows, green hover, rounded end cells and shadow with semantic HTML. Preserve sorting, filters, pagination, selection, action handlers and empty states. Scroll only a table's own region when necessary, without a universal minimum width.
- Record-detail pages share one narrower title/action/detail container (default maximum 46rem). Keep labels close to values and visible on phones. Preserve room for genuinely wide viewers/maps/grids; no dividers between titled detail groups.
- Form pages share a narrower title/action/body container (default maximum 36rem). Group headings stay outside `xl:mx-6` field bodies. Ranges and measurements use compact wrappers with endpoints/units on one line; errors remain below. Read [forms and optional behavior](references/forms.md).
- Add/New uses a dark compact plus + text button at the title's right. Print/help uses unboxed icon + text there. Small admin pencils sit beside the title they edit, permission-gated. Table row actions use 32px circular controls and 20px SVGs; preserve operation semantics and confirmation/CSRF behavior.
- Login includes the exact VAU account-circle icon. Secondary buttons stay white at rest and become preset gray-100 on hover. Existing field tips, including bulb images, use the small circled-i at the label row's right above the field, retaining their real help action.
- Preserve existing dialog libraries and their structural CSS. Apply only the relevant [dialog guidance](references/integration.md#existing-dialogs); a Thickbox app must not acquire a fake Fancybox close control.

**Small-screen fading text is optional.** Before collapsing identified text, ask whether the user wants it collapsed and how many rendered lines must remain visible. Keep full text until both choices are explicit. General design approval is insufficient. Reuse existing explicit approval for the same blocks/count; continue unrelated work while waiting. See [optional text disclosure](references/forms.md#optional-fading-text).

## Verify the result

Use [verification](references/verification.md). Build in a disposable skill copy for baseline checks; keep generated CSS/dependencies out of the installed skill. Compare actual screenshots and computed design values, not merely class names or lack of overflow. Exercise the target's real public/admin/detail/form/dialog interactions and print behavior. Keep source and target screenshots at matched widths.

Report migrated surfaces, checks and visual comparisons, plus unavailable routes/services. Do not declare completion with specimen navigation/data, broken assets or untested behavior. Preserve the current target technology and editor; no framework or editor upgrade is implied.
