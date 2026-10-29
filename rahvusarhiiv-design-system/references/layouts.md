# Responsive layout contracts

All dimensions below are recovered from source. Ownership/API names are the extracted design system. The bundled neutral recipes demonstrate the contracts; do not copy the source pages' application header.

## AppShell and InstitutionalFooter

Canonical evidence: `views/layouts/advanced-layout-alt.html`. `basic-layout.html` confirms the same geometry with placeholder content and the peach gradient.

```text
body: flex min-h-screen flex-col bg-gray-50
main shell: flex grow flex-col rounded-b bg-white shadow-md lg:m-2 lg:rounded
institution strip: flex h-12 flex-wrap content-center
gradient region: flex grow flex-col rounded + selected gradient
app header: relative flex h-32 flex-wrap content-center
white content surface: flex grow flex-col rounded rounded-b bg-white shadow-md
footer surface: mt-2 flex shrink flex-col rounded-t bg-white shadow-md
                lg:mx-2 lg:mb-2 lg:mt-0 lg:rounded
```

48px institution strip: RA logo left, optional language switch and mobile menu trigger right. Logo h-7/28px, opacity .7. App header is 128px high with app logo h-11/44px → h-12/48px at sm. The generic reference has two groups of horizontal links and a sign-in action; group structure is optional data, not fixed app semantics. Horizontal navigation uses16px medium body text (language/utility links use13px). Horizontal navigation begins at lg; its gaps are 16px → 32px at xl → 48px at 2xl. Drawer is full-width below sm, max-width 384px from sm, aligned right, white, internally scrollable, gray-600/.75 scrim. Use one route model for both views. In this preferred generic shell the menu trigger is in the institutional top strip, after the optional language switch, with16px separation and a20px icon. The gradient app header retains the app identity, horizontal links and optional account/sign-in action. Drawer state belongs to AppShell because trigger and panel cross header boundaries. The extracted trigger retains a padded keyboard/touch target while matching the source icon alignment. The nonpreferred `advanced-layout.html` variant puts the trigger in the app header; do not use that placement by default.

The shared footer card is defined in `assets/starter/footer.html` and wraps both standard and customized content. Its white background, rounded corners, shadow, responsive outer margins, landmark, inner frame, and nominal height are shell-owned. Custom content cannot replace the card with a bare strip on the page background. The composer gives custom content 24px vertical padding; standard content owns its responsive section padding. Explicitly choosing no footer omits the component entirely.

The standard footer is a complete component, not a placeholder strip. Base stacks links then contact; at sm it becomes a row with vertical divider, 48px contact inset, and nominal 256px height. Base section padding is 24px; divider 2px gray-700; service link vertical spacing 24px. The starter uses min-height at sm as a repair for translated/long content.

Standard content preserved in `assets/fragments/footer-standard.html`: Tagasiside; Rahvusarhiiv; Arhiivi infosüsteem; Virtuaalne uurimissaal; Nooruse 3, Tartu 50411; 738 7500; rahvusarhiiv@ra.ee; Facebook, institutional blog, Flickr, Instagram, Twitter reference destination, YouTube. These are template snapshot data, not a claim that every external service is currently reachable. Keep URLs configurable and verify them when deploying; don't silently replace institutional information from memory.

Feedback opens the original helpdesk endpoint in an 800×600 popup. The reference leaves `url=` blank. The extracted footer appends the current location via URLSearchParams and provides a normal link fallback if popups fail. This is a functional repair. Never submit feedback automatically.

## ContentContainer

The frame is shared by header, content, and footer:

```html
<div class="2xl:max-w-xxl mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8">
  <!-- Optional width-profile wrapper, then content -->
</div>
```

`max-w-7xl` = 1280px; `2xl:max-w-xxl` = 1440px (the original preset uses !important). Gutters: 16px base, 24px md, 32px lg. Content page adds `pt-6 pb-10 xl:pt-10 xl:pb-14` = top24/bottom40 → top40/bottom56. The minimal shell's demonstration uses `py-6 xl:py-10`; use the richer page rhythm for normal app screens.

Width profiles are **responsive insets inside the frame**, not fixed max-width labels:

| Profile | sm | lg | xl | 2xl | Authority / use |
|---|---:|---:|---:|---:|---|
| full | 0 | 0 | 0 | 0 | archived collection; dense data |
| narrow | 64px | 176px | 288px | 320px | news-list; reading and short lists |
| medium | 64px | 128px | 208px | 256px | access-files; substantial single-column form/records |
| form | 80px | 176px | 320px | 384px | register/password-change; short forms |
| summary | 64px | 128px | 256px | 288px | payment summaries; compact totals/details |

Each number is the margin on **each side**. Base is zero; sm remains active through md. Exact primary class recipes:

```text
narrow: sm:mx-16 lg:mx-44 xl:mx-72 2xl:mx-80
medium: sm:mx-16 lg:mx-32 xl:mx-52 2xl:mx-64
full: no inner inset
form: sm:mx-20 lg:mx-44 xl:mx-80 2xl:mx-96
summary: sm:mx-16 lg:mx-32 xl:mx-64 2xl:mx-72
```

At a 1440px frame, after 64px gutters: narrow is 736px, medium 864px, full 1376px, form 608px, summary 800px. Those widths do not apply at every breakpoint. Do not replace profiles with `max-w-prose`.

Other source adjustments (folder collection 64/112/192/256; bookmark collection begins at md; login's insets widen again at lg) are evidence of local tuning, not reasons to expose unlimited margins publicly. Use the closest core profile unless a real content requirement warrants a named, documented variant. Unsupported `mx-42` and duplicate conflicting xl margins are source defects, not tokens.

The container owns gutters **once**. Nested cards/sections own internal padding, never another global frame. A full-width container still respects the frame cap. Only the outer shell spans the viewport.

## PageTitle

Canonical plain recipe:

```text
font-heading mt-px border-b-2 border-gray-500 pb-2
text-lg font-bold text-gray-700 sm:mt-6 sm:text-xl xl:mt-0
```

After-title space is usually 40px; workflow headings often use 24px; collection headings use 24px → 40px at md. Expose a small spacing variant (`normal`/`compact`/`collection`) instead of page-level overrides. The original uses h1 and h2 inconsistently; select the semantic level independently of visual style.

The title is part of its owning content region: inside WorkspaceLayout working slot and ArticleLayout article body; above both SplitLayout slots only when it names the whole task.

Options: text; semantic heading level; spacing; list of actions (label, icon, href or handler, primary/secondary/quiet); `mobileLabels=icons|visible`. On phones icons remain and labels use visually hidden text. Button actions: compact 13px, 8px vertical /12px horizontal padding, 8px gap. Quiet utility actions: 13px gray-600, 16px gap. No actions is a first-class case.

Evidence: access-files plain; bookmark-folder-list outlined + solid right buttons; order-draft-empty quiet right links. In **both** action examples the text uses `hidden sm:inline`; the icons/actions stay on small screens. If a product requires labels to stay, choose the visible-label option explicitly.

Source floats work for short titles but can collide with long translations. Extracted recipe uses a wrapping flex row above one continuous divider, a shrinking title, and nonshrinking actions; this is a documented robustness adaptation. Do not truncate the page identity to keep utilities on one line.

## SplitLayout

Canonical source: order-copy-confirm and its batch/other confirmation siblings; also shop-form. This is a generic paired-region composition.

```text
root: flex w-full flex-col gap-x-4 gap-y-6 xl:flex-row
      lg:gap-x-10 xl:gap-x-16 2xl:gap-x-28
children: flex-1 min-w-0
optional first-region inner: xl:sticky xl:top-10
```

Vertical until 1280px, then equal regions; vertical gap24, horizontal gap64 at xl and112 at2xl. lg gap40 exists but has no visual effect while stacked. Keep title above both slots when it labels the whole task. Sticky wrapper belongs inside the first flex child so its containing block spans the second region's height. Do not put overflow:hidden on a sticky ancestor.

Allow mobile order only where the user's task needs it. Source label-management examples reverse the stack to put the action first; prefer a logical DOM/focus order and test any visual reorder. A distinct `paired` variant can collapse at lg with gaps64/80/128 for simple choice/identity panels; don't change the substantive form's xl collapse to lg by default.

## WorkspaceLayout

Use for a persistent form/help panel beside a larger working collection; it is not the equal SplitLayout.

- Root: `flex items-start w-full flex-col gap-x-4 gap-y-6 xl:flex-row xl:gap-x-10 2xl:gap-x-12`.
- Form panel: `flex-1 w-full pt-4 pb-6 px-6 rounded bg-gray-50/60 xl:flex-auto xl:w-16 2xl:w-28`.
- Working region: `flex-1 w-full pt-5 xl:flex-auto xl:w-80 2xl:w-96`.
- These widths are flex bases with growth, **not** a 64px rendered sidebar. Preserve the flex sizing model or verify an equivalent ratio against evidence.
- Nested field groups: one column → two at md (`gap-x-8`) → one at xl when the panel is beside the collection. The panel action similarly goes full → auto at md → full at xl.
- Informational variant (enquiry-form): helper on the left and main content on the right atdesktop; title belongs to main content. Pale yellow panel with base widths288/320 at xl/2xl and sticky top40. Preview/submitted examples put the helper region after the main region on small screens. Treat that ordering as a task choice, not an unconditional rule.

## ArticleLayout

Canonical source is `vau-page.html`. Keep one public composition with `sectionNavigation`, article sections (stable id, heading, body), title/actions, and optional in-article related links. Generate desktop and drawer contents from the same section data.

| Width | Section navigation | Article contents navigation |
|---|---|---|
| <640 | Hidden left rail; links available via mobile section menu | Full-width sticky top button opens right drawer |
| 640–1023 | Hidden left rail; links available via mobile section menu | 32px compact right trigger rail, sticky top24 |
| 1024–1279 | 224px left rail +40px right margin | 240px right TOC, 24px gap, sticky top40 |
| ≥1280 | Same 224px left rail | 288px right TOC, 48px gap |

Left rail is ordinary document flow, not fixed/sticky despite the source comment calling it fixed. Right TOC starts 80px below the article region's top; inner list scrolls while sticky. Use `max-height:calc(100dvh - 80px)` instead of source `h-screen + top-10`, which can clip the last entry. Main and article flex children require min-width:0 for long URLs/tables.

Article uses unbounded prose width within its allocated column, Roboto 19px section headings, rounded images, and responsive image caps512/576/672px at lg/xl/2xl. TOC active entry: 2px green-300 left border and bold type; other entries gray-100 border. Active section updates on scroll and clicks; headings remain actual anchor targets.

`vau-page-2`/`vau-page-3` defer the full TOC to xl. Retain as an alternative only when preserving more reading width at1024 is a requirement. Do not mix a lg rail, xl drawer visibility, and an unrelated breakpoint for its trigger. The canonical source's drawer visibility mismatch is repaired by using the same lg breakpoint for rail/trigger/drawer.

## Sidebar browsing and media/detail layouts

Not every sectioned page needs a TOC. A `SidebarLayout` uses the same224px left navigation and40px gap with a single content slot, plus mobile access to the same links. Source home and catalog pages establish this. Catalog adds outer insets96/128px at xl/2xl; do not force these into all sidebar pages.

Media detail (shop-product) stacks image/metadata then body below sm, uses a112px media column with16px body inset at sm+, and may move ancillary content before the detail on phones. Extract `MediaDetail` only for that relationship; price, cart, stock, ISBN, and checkout are caller content.

Home's 11-column composition is page assembly, not a universal dashboard primitive. Reuse its cards/list families and choose placement for the target information, rather than exporting a Home component.
