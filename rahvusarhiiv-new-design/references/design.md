# Exact design translated to HTML

Apply these visual rules within the separate Joyful theme only. Preserve the default presentation and select between them as described in [application-level themes](themes.md).

## Evidence and precedence

The design was extracted from `rahvusarhiiv-joyful-theme`; this package carries its relevant resources independently. The bundled `assets/reference/advanced-layout-alt.html` defines the shell/footer; `assets/reference/vau-frozen.css` is comparison evidence only. Current user rules below supersede historical markup defects. The approved gradient is from [basic-layout.html](https://erikuus.github.io/tailwindui-playground/views/layouts/basic-layout.html); the [account page](https://erikuus.github.io/tailwindui-playground/views/pages/vau-account.html) supplies narrow detail-page evidence. Original local sources are under `/Users/erikuus/Documents/Github/tailwindui-playground` and `/Users/erikuus/dev/php/vau/themes/joyful/views` when available. Do not deploy their placeholders, personal data, domain routes or old stylesheet.

Use `assets/html/shell.html` as a structural specimen and `assets/html/components.html` for the actual table/detail/form utility markup. The specimens contain deliberate demo labels and local fragment links. Transfer markup into the target's separate Joyful templates/loops; do not ship “Näidisrakendus”, hardcoded sample rows or `#form-example` as real operations. Read the target's current implementation rather than assuming a past app snapshot is current.

## Shell and footer

Preserve this nesting:

1. `body`: `flex min-h-screen flex-col bg-gray-50 font-body text-gray-900`.
2. White outer surface: `flex grow flex-col rounded-b bg-white shadow-md lg:m-2 lg:rounded`.
3. Institutional header: 48px (`h-12`), RA logo `h-7 opacity-70`, right-hand utilities.
4. Growing gradient surface: `bg-theme-vau flex grow flex-col rounded`, containing the 128px (`h-32`) application header, breadcrumbs when present, and white content panel.
5. White content panel: `flex grow flex-col rounded rounded-b bg-white shadow-md`; main has `py-6 xl:py-10` and inner content `w-full min-w-0`.
6. Exact footer: sibling of the outer surface, not inside the gradient or main content.

Horizontal container: `2xl:max-w-xxl mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8`. This means 80rem maximum, 90rem at 1536px, with 16/24/32px padding. Do not compensate for a wrong nested container with arbitrary margins. Form/detail width constraints belong inside main, not around the shell.

`bg-theme-vau` is exactly `linear-gradient(96.04deg, rgba(247, 227, 204, 0.65) -17.14%, #ECDDF4 94.45%)`. Retain other colors and geometry. This gradient-only override does not authorize replacing the shell/footer with the basic template.

Insert `assets/html/footer.html` as a shared partial/include with its original subtree intact. Preserve Tagasiside's popup URL/options, institution/service link labels and destinations, postal address, phone/email and social SVGs/URLs. Do not substitute app-specific copyright/contact details or modernize these links. Keep its Alpine handler working with exactly one Alpine runtime. In template languages where `@click`/`x-data` require escaping, output equivalent literal HTML and verify the resulting footer. Keep the narrowly scoped footer divider compatibility rules in `components.css`: Tailwind 4 otherwise moves the border onto the shorter links column. Print and dialog documents have separate layout contracts.

## Header navigation and breadcrumb ownership

Use the real app name/logo, route-aware menu data and authentication state. Keep the app logo/name linked to home. **Omit a separate Home/Avaleht item from desktop and corresponding mobile main navigation even when present in the old theme.** Identify that entry by purpose/route/translation; an unrelated URL containing “home” is not enough to remove it. Other authorized entries retain order, active rules and labels. Never add a fake language picker.

Existing enabled bookmark and helpdesk integrations move to the upper-right institutional header as icon controls, sharing space with real language controls and the mobile opener. Preserve each integration's generated URLs, callbacks, flags and popup behavior; retain distinct add-bookmark/list-bookmarks actions. Do not install services the app does not already use or replace generated controls with guessed links. Header utilities do not replace or modify the exact footer feedback action.

Breadcrumbs appear once **on the gradient**, after the application header and before the white panel. The HTML specimen preserves the home tile, white ring, chevron separators and spacing. Use an accessible `<nav>`/`<ol>`, current-item `aria-current="page"`, and encoded target labels/URLs. Allow wrapping for long paths; do not clip the current location. Preserve the breadcrumb home icon even though Home is omitted from the main menu. With breadcrumbs, omit a redundant standalone Back control; retain form Cancel, dialog Close and workflow Previous.

Desktop menus appear at `lg` (1024px). The optional `navigation.js` uses a native modal `<dialog>` for the reference right-side drawer: full width on phones, `sm:max-w-sm`, 48px header, gray backdrop, padded stacked links. It provides close/outside/Escape, scroll restoration, focus return and desktop-resize cleanup through native dialog behavior plus a small handler. Keep an existing equivalent drawer instead of adding competing bindings. Retain a usable no-JavaScript mobile navigation path; a hidden desktop menu alone is insufficient. Do not use the new drawer code to replace existing data-entry dialogs.

For an existing left sidebar, use 224px width and 40px gap at desktop, e.g. `grid gap-y-6 lg:grid-cols-[14rem_minmax(0,1fr)] lg:gap-x-10`, with `min-w-0` content. Group title: `mb-2 border-b border-gray-500 px-4 py-2.5 text-sm font-bold uppercase text-gray-700`. Links: `block rounded px-4 py-2 hover:bg-green-50`; current link `bg-green-50`, list `space-y-1`. No gray card, bullets, red active text or centered heading. Use semantic headings/lists; preserve permissions, nesting and actual active logic. Keep mobile access. Do not invent a sidebar; do not apply the article table-of-contents indicator style to a main side menu.

## Title rows and narrow content

Use one wrapping title row with one underline: `mb-10 flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-b-2 border-gray-500 pb-2`. Title: `min-w-0 max-w-full break-words font-heading text-lg text-gray-700 sm:text-xl`. Preserve appropriate semantic heading levels. Actions belong in the row above the shared rule, can wrap on phones, and must not duplicate a border on the heading.

Dedicated form pages: one parent `mx-auto w-full min-w-0 max-w-xl` (36rem) contains title/actions, required guidance, error summary, groups and form actions. No separate full-width title above a narrow form; no repeated narrowing inside a shared form partial. Keep error-summary margins inside the boundary.

Dedicated record-detail pages: one parent `mx-auto w-full min-w-0 max-w-[46rem]` contains title/actions, group headings and detail content. This is the bounded adaptation of the account reference's `sm:mx-16 lg:mx-44 xl:mx-72 2xl:mx-80`; do not apply both constraints. It keeps labels near values on wide screens. A `view` route containing a map, image viewer or large grid may need a wider working area; constrain its metadata independently rather than narrowing the entire workspace. Keep the page title with the working area and a metadata heading with its own panel.

Detail group headings use spacing such as `mb-6 font-heading text-lg text-gray-700` and `mt-12` on subsequent groups. **No horizontal group separators, `divide-y`, `<hr>`, or per-group underlines.** The single main title underline remains. Do not carry form-only `xl:mx-6` field-body indentation into read-only detail groups.

## Tables and detail views

The HTML table specimen preserves the original grid decorator's classes, not an approximation. Keep the outer `rounded shadow-sm p-2` surface, scoped typography and no outer row borders. Header cells have white backgrounds and 12px horizontal padding. Data cells use 12px padding, top alignment, rounded first/last cells, gray-50 alternating rows and green-50 hover. Retain meaningful numeric alignment and existing data formatting. `not-prose` protects action controls from content typography.

Use real `<table>`, `<thead>`, `<tbody>`, column `<th scope="col">`, optional caption, and rows from the target's existing loop. Preserve sort links/query parameters, active sort direction (`aria-sort` where appropriate), filters, column visibility, pagination and AJAX row identifiers. Keep summaries/pagers outside the horizontal scroll area; scroll only the items region as needed. Do not place a full layout around an AJAX replacement fragment, convert all values to raw HTML, add arbitrary minimum table widths, or change existing no-AJAX behavior.

The specimen's single current-page item is not a pagination algorithm: render the app's real page links, disabled/current states, counts and handlers. A grid action must keep its existing URL/method/confirmation/CSRF handling; do not add a new mutation endpoint while changing markup. Plain links navigate; existing destructive actions retain their actual POST/form/script contract.

The detail specimen uses the original tinted `prose-table:bg-gray-50/60` surface, 12px cells and one-third label column through scoped utilities. Preserve real label/value data, visibility and escaping. Apply `[overflow-wrap:anywhere]` to the detail content where long unbroken URLs/values need it. `components.css` stacks `.ra-detail` label/value cells below 768px **without hiding labels**. If the target uses a `<dl>`, reproduce the same label/value proportions, spacing, surface and mobile pairing with semantic `<dt>/<dd>`; do not force a backend widget conversion. Keep the supplied mobile overrides unlayered so typography utilities cannot restore a one-third label width or bottom padding. Scope styles to that detail block, not all tables.

## Icons and actions

Inline SVG sources are in `assets/icons/`. Inline them into the app's normal partial/helper system so `currentColor` works; external `<img>` SVGs do not inherit surrounding text color. Avoid adding an icon font or framework solely for these glyphs. Decorative SVGs use `aria-hidden="true"`; the enclosing action has visible text or an accessible name. Preserve titles, operation IDs/classes used by scripts, role/permissions and return context.

| Action | Placement and exact geometry |
| --- | --- |
| Guest Login | Account-circle glyph from `login.svg`, 12px with 6px text gap; compact dark link `py-2 pl-3 pr-4 text-sm`, in application header. |
| Add/New | Right of page title, plus 16px before text, 6px gap; `rounded bg-gray-900 px-3 py-2 text-sm font-medium text-white hover:bg-gray-700`. Related secondary management actions precede it. |
| Print/context help | Right of page title, 16px glyph + visible text, `inline-flex items-center gap-1 text-sm font-medium text-gray-600`; unboxed, action group gap16px. |
| Row View/Edit/Delete | 32px circular hit area, 20px SVG; `inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-gray-500 hover:bg-green-100 hover:text-gray-800`. View uses magnifier; Delete uses source × glyph, not a substituted trash can. |
| Contextual admin pencil | Immediately after the title it edits, 6px gap, 32px round control, 16px pencil; `text-gray-200 hover:text-gray-800 hover:bg-gray-50` (gray-100 on product surfaces). Independently clickable over any stretched card link. |
| Field help | Filled circled-i 23px in gray-600, right of label above input. Preserve the real help URL/popup/tooltip; not the page-title help action. |
| Header utilities | Existing bookmark/helpdesk glyphs20px, consistent inline-flex centered controls with visible focus. |

All controls retain visible focus, e.g. `focus-visible:ring-2 focus-visible:ring-green-300`. Primary normal form buttons use `py-3 px-4 text-base`, distinct from compact title buttons. Secondary/Cancel controls use `border border-gray-200 bg-white text-gray-900 hover:bg-gray-100`; the hover background is #E8EBF0, with dark text/border retained. Do not combine primary and secondary background utilities on one element.
