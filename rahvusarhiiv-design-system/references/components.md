# Component families

Read only the families needed by the requested interface. Names are proposed reusable contracts, not claims about an existing component library. Source filenames below are provenance; do not expose their business semantics in shared component APIs.

## Recipe files

| Neutral recipe | Covers |
|---|---|
| [navigation.html](../assets/recipes/navigation.html) | Breadcrumbs, route tabs and section navigation |
| [layouts.html](../assets/recipes/layouts.html) | Container profiles, title options, split/workspace boundaries |
| [forms.html](../assets/recipes/forms.html) | Fields, invalid/disabled states, choice, responsive field grouping/actions |
| [data.html](../assets/recipes/data.html) | Collection toolbar, rows, metadata relocation, row actions, pagination, detail summary |
| [content.html](../assets/recipes/content.html) | List, pill-link cards, notices, empty state, disclosure |
| [line-items.html](../assets/recipes/line-items.html) | Static repeated items, labelled phone metadata, aligned amounts and total |
| [workflow.html](../assets/recipes/workflow.html) | Step progress and file collection |
| [media.html](../assets/recipes/media.html) | Media detail and choices |

Recipes contain neutral sample content and mark behavior that the application must supply. Copy a needed pattern, not the whole recipe file into every page. The runtime bundled with the composer handles shell drawers/TOC/feedback only; recipe business controls need their own integration.

## Navigation families

`Breadcrumbs`: ordered location path on the header gradient,13px type, pale backdrop-brightness105% surface, radius8, margin16px vertical. Source positions the region with -24px top overlap beneath the app header. Home action is white, padded8px with16px icon and white4px ring; separators16px. Parent route can be bold; current route plain text/aria-current=page. Use one anchor per interactive crumb. Source long-path truncation can hide context; the composer deliberately wraps instead. If reproducing the exact overlap, preserve its48px net vertical contribution and test a wrapped path rather than applying negative margins blindly.

`RouteTabs`: route-level sibling views attached to the bottom of the gradient immediately above the white content surface. Margin-top24px, gaps8px, rounded top8px; padding12px vertical and24px horizontal →32px atsm;13px type →16px atsm. Inactive tabs use brightened translucent background, hover green-50; active tab is white withshadow-md and visually joins the content. Optional counts hide belowsm in source; keep accessible counts if relevant. Source overflow-hidden can clip additional/long tabs: provide local horizontal scrolling or another explicit overflow strategy when the supplied items need it. These are navigation links, not ARIA tabs unless they truly control in-page tab panels. If implementing actual tabs, add selected state, panel association and keyboard arrow behavior together.

`SectionNavigation`: grouped headings (uppercase13px bold gray-700, bottomgray-500 border, padding10/16px), links with8/16px padding,8px radius, green-50 hover,4px vertical gaps.224px rail +40px gap in Sidebar/ArticleLayout. Current route derives from routing, never text matching. Mobile links must remain reachable through the owning composition's drawer. Groups and destinations are app data; headings such as reading rooms/services are not shared constants.

`ActionMenu`: compact13px white popup, gray-200 border, rounded8, soft shadow, right aligned; menuitems typically8px vertical and32px horizontal. Source row-size and overflow menus demonstrate geometry but not complete keyboard semantics. Its owner holds open state, active item and action callbacks; Escape/outside selection closes and returns focus. Don't impose menu-role semantics on an ordinary list of navigation links without the corresponding keyboard behavior.

## Actions and field controls

`Action`: primary, secondary (outline), quiet, link; normal/compact; optional icon; disabled/loading. Navigation uses anchors, state changes use buttons, form submission uses submit. Never nest a link inside a button as the source breadcrumbs do.

- Primary: rounded8, gray-900, white, medium; hover gray-700. Normal padding12px vertical/16px horizontal,16px type. Compact8/12px,13px type. Icon typically16/20px with6px gap.
- Secondary: same geometry, white with1px gray-200 border, gray-900 text, hover gray-100.
- Quiet: transparent, gray-900, hover gray-100/.6; icon-only utility actions often gray-600.
- Link: blue-600/500/700 normal/hover/active. Prose links can be underlined; don't strip all prose link distinctions.
- Fix source `focus-visible::ring-*` to one colon or equivalent native focus CSS. Keep focus visible for keyboard users. Disabled state must disable behavior, not only change color.

`Field`: label, control slot, required marker, hint, error, normal/compact size, disabled/read-only. Control types are native text/select/textarea, checkbox, radio, and specialized adapters. Don't require one mega-field component to implement every third-party widget.

Normal text control: `block w-full rounded border border-gray-200 px-4 py-3 text-gray-900 hover:border-gray-300 focus:border-gray-500 focus:outline-none focus:ring-2 focus:ring-green-300 sm:text-base sm:leading-6`. Disabled: gray-50 background, gray-400 text, gray-100 border. Invalid source examples use red-500 text, red-300 border → red-400 hover → red-600 focus with red-200 ring. Ensure invalid styles actually override normal rules; connect errors with aria-invalid/aria-describedby.

Compact filters: px12/py6,13px type at sm,24px leading, label13px semibold. Checkbox/radio:16px; checkbox radius4px; green-500 checked, gray-200 border,2px green-300 focus ring without ring offset. Group label/error belongs to a fieldset/legend for multiple choices.

`FieldGroup` owns responsive grouping. Default full form has space-y24. A workspace field group specifically uses one→two→one columns at base/md/xl; do not apply this schedule to an ordinary wide form. `ActionGroup`: choose `stacked` (full-width at every width; default for short forms), `inline` (auto-width from md), or `workflow` (equal-width peers from xl). Use the examples in patterns.html and the routing in composition.md; do not force all forms into an inline save/cancel pair. Preserve logical keyboard order when visual order changes.

Evidence: forms component, register, login, access-form, order-draft. Their model names, hidden ids, authentication flows and conditional business rules are excluded.

## Search, filtering, and data collections

`SearchControl` is one input+submit group, soft shadow-sm white surface, gray-50 button; include a real label (can be visually hidden). `FilterPanel` is part of its owning DataCollection and uses gray-50/.6 fill, padding24 horizontal/12–16 vertical, rounded8, underlined small heading and close control. Typical field grid:1 →3 atmd →4 atlg →7 atxl; narrow workspace collection caps at3. Number of fields is data, while the collection's available-width variant controls the grid. Clear, cancel and apply are distinct actions.

`DataCollection` contract: items with stable ids, column definitions with priority and mobile placement, row actions, optional selection, filters, range/total, page size and pagination. It owns:

- White rounded shadow-sm wrapper, padding8px; toolbar padding12px, gray-100 bottom divider.
- Tables inside the source typography surface render at14px (0.875em of16px), line-height about1.714; toolbar/utility text uses13px. Cells padding12px, labels/header emphasis. Explicit compact utility text remains13px; do not set the entire table to the toolbar size.
- `rows=divided` (gray-100 horizontal rules) or `striped` (alternate gray-50, no row rules, rounded edge cells). Hover green-50 in both. The source uses typography plugin table selectors; implement equivalent scoped table styles when porting.
- Dense collections use table-fixed and a full-width primary cell on phones; selection column40px, action column56px. Secondary columns appear atmd,lg,xl by priority. A fixed-width desktop table is not the mobile component.
- At phone sizes, move title/type/status and relevant actions inside the primary record cell; expose row menu at the edge. Atmd restore secondary description/type columns; atlg restore status; atxl restore dates where supported. Derive duplicate visual presentations from one record and hide the inactive representation from layout/accessibility. Do not discard data merely because its column is hidden.
- Overflow handling: min-width:0 for the record, truncate only secondary summaries that have a detail route, wrap important names/identifiers where needed; row actions remain reachable.
- Selection owns per-row ids, select-all/mixed state, selected count and bulk panel visibility. Source Alpine connects only a header checkbox to a panel; that is not complete selection logic.
- Toolbar range and page-size controls; pager centered beneath. Disabled first/previous are visibly muted and actually disabled; current page is distinguishable and aria-current=page. Connect navigation to real data or identify it as a prototype.

Don't split filter state, selection state and pagination into unrelated page-level flags. Optional inner implementations (`CollectionToolbar`, `RecordRow`, `Pager`) are useful only if they preserve the parent's coherent contract.

Evidence: order-archived/submitted/draft, bookmark-list/folder-list, access-files, shop-cart. These establish density and mobile relocation, not a shared order/bookmark model.

## DetailSummary

Separate from interactive DataCollection. Label/value or small record summary, often pale gray rounded surface; cells padding12px; label column144px on wider screens; dividers gray-100/200. On phones labels can move into the value region where source table headers disappear; preserve their associations. Use dl when more appropriate than a table. Optional totals or actions are slots; no payment-specific semantics.

Evidence: access-files data summary, confirmation pages, company view/invoice and payment pages. Use `plain` for an unboxed review and `surfaced` for a grouped pale-gray metadata panel. Labels use the same14px data scale; labels may remain side by side on phones if readable, otherwise stack. Avoid adding extra field labels or tall padding solely to fill space.

## LineItemTable

Repeated items with description, optional reference/unit, unit price, quantity and amount form a table even when completely read-only. It owns its header, rows, numeric alignment, mobile relocation and total. Use14px text,12px cells, restrained striping and a white rounded shadow-sm outer surface. Desktop columns appear from768 in the base recipe; below768 each item retains its labelled unit/price/quantity/amount inside the primary cell. Total remains a separate right-aligned footer, never a property of an unrelated summary. Optional editing/selection is supplied only when needed. See [line-items.html](../assets/recipes/line-items.html) and [patterns.css](../assets/patterns.css). Compute amounts from one item model; business currency/tax rules are caller data.

## Notice, empty state and status

`Notice`: tone neutral/info/success/warning/error, optional icon, heading, action, expandable details, dismissal. Common compact notices p12 and13px; larger notices p16/24 with icon badge. Neutral gray-50/gray-700; warning yellow-100/yellow-800; error red-50/red-700; success green-50/green-700. Body flexes/min-width0, close control doesn't shrink. Use role=status for routine updates, role=alert only when urgency warrants it. Dismissal changes local state rather than navigating to an empty href.

`EmptyState`: centered icon + 19px medium heading + explanatory content + optional action/help slot; rounded gray-50/.6 surface, padding56px vertical,24px horizontal (40 atmd). Full collection variant increases horizontal inset to128 atlg,256 atxl,320 at2xl; workspace variant resets to56 atxl. Extract as an available-width variant, not an empty-orders component. Don't reuse “no results”, “loading failed”, and “nothing created yet” copy interchangeably.

`Badge`: small rounded-full metadata/status, generally11px semibold; pale fill or1px outline. Always include a text label. Numeric `.type1/.type3/.type4/.type5` and access/status row-edge classes in tailwind.css are application mappings and are not foundation tokens.

## Disclosure and overlays

`Disclosure`: trigger + content + expanded state as one unit. FAQ-style fill gray-50/.6 → gray-50 hover, padding16, blue label, plus/minus indicator, body margin-left24 and vertical16. Use button/aria-expanded/aria-controls or details/summary, not an unkeyboardable click div.

`Dialog`/`Drawer` share focus lifecycle, close/Escape/backdrop behavior and scroll locking; their geometry differs. Institutional/mobile contents drawers belong to their navigation owner, while a dialog can host independent form/selection content.

## Progress and files

`StepProgress` owns one step data model and two presentations: horizontal atmd+ with40px circles,2px connectors,13px bold uppercase labels and vertical margins48px; phone vertical timeline with24px markers and thin connectors. Completed/current green-500, pending markers gray-200. The complete recipe retains numbered40px desktop circles and green connectors leading to reached steps; phone has24px outline check markers, small pending dots and continuous1px gray connectors. Pending labels use gray-600 in the portable recipe as an explicit readability repair for the very pale source text. Add an explicit current-step marker/aria-current=step; source doesn't sufficiently distinguish current from completed. Labels are supplied by the app, not hardcoded to five steps or a signing process. Retain meaningful text on mobile.

`FileCollection` owns the attachment prompt, chooser/drop target and file rows. Pale gray container, heading px24/py12 with bottom border; body p24; dashed gray-200 rounded drop region, vertical gap16/padding16; file rows white rounded, px12/py8,8px vertical gap. Long filenames truncate within min-width0 but retain full accessible names; action buttons remain fixed. Parameters: allowed types/size, multiple, existing files, upload states, remove/download callbacks. The template's10MB caption is not an institutional policy. Actual file input, drag/drop, progress, errors, retry and server integration are work to implement; the source drop zone is decorative.

## Content lists, cards, and grouped links

`ContentList`: entries with heading/link, optional metadata, excerpt, secondary actions;40px between entries. Source heading19px bold gray-700; metadata11px pale pill; excerpt bottom padding16 with2px gray-100 rule turning green-300 on hover. Whole-row link uses stretched hit target; keep secondary edit controls above it and keyboard accessible. News date/year semantics are caller data.

`LinkCardGroup`: rounded-full gray-50/.6 row, hovergray-100,64px circular leading visual, text px12/py8, grid gap20. Common grid1→2 atsm; inside ArticleLayout it becomes1 atlg when rails appear and2 again atxl. The enclosing composition owns this context variant. Generic account-picker and home/enquiry shortcuts show the same anatomy. Copy only appropriate institutional icons; illustrations tied to a subject are not universal tokens.

`ChoiceGroup`: radio cards with image/label/description and selected styling. Related panels stack until lg, then equal columns with widening gaps64/80/128. Image choices use4px borders, gray-300 with opacity.5 while unselected, green-300 with full opacity when selected/hovered, radius8 and labels below. Use real accessible radios (visually hidden, not display:none) and keyboard group behavior; source theme-choice radios are hidden. Theme choices, payment-provider buttons and account options are separate content supplied to a shared choice/linked-card family, not default capabilities of every app.

## Media and prose

`MediaDetail`: responsive media/metadata rail and prose body, described in layouts.md. No cart/price rules in its public API.

`RelatedMediaStrip`: desktop-only experimental carousel in carousel.html shows7 surrounding items and steps3. This is conditional enhancement, not essential navigation: source hides it belowlg and uses placeholder destinations. Repair wraparound for arbitrary counts before reuse. Preserve a reachable alternative for any essential content. No autoplay requirement is established.

`Prose`: body rhythm, proper h2/h3, links, lists, images, tables, captions. Use `.prose max-w-none` within the owning container, with body-font19px h2 as in article/news. Wide editorial tables may have a locally scrollable wrapper. Avoid moving global layout spacing into prose styles.

## Print adaptation

Print templates establish hidden controls, restored table metadata, simple document headings and print-friendly rows. Implement print behavior within the data/detail composition when requested; keep printing a user-triggered action.
