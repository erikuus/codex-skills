# Choose by information structure

Use this decision order in either operating mode. Automatic mode records choices and proceeds; guided mode offers the relevant alternatives with a recommendation. These are generic contracts, not a catalogue of source-domain pages.

## 1. Identify the regions before choosing a width

| Content relationship | Composition | Title belongs |
|---|---|---|
| One form, short list, reading page or review | ContentContainer with a documented width | Inside its width profile |
| Two substantial related regions, e.g. review + editable fields | SplitLayout, equal columns from1280 | Above both when naming the entire task |
| Persistent creation form + working records | WorkspaceLayout, unequal flex regions from1280 | Inside the working region, after the creation form in phone DOM order |
| Guidance + main form/review | Informational WorkspaceLayout | Inside the main region; helper normally left atdesktop,288/320px atxl/2xl; choose phone order deliberately |
| Two peer choices or identity panels | SplitLayout paired variant, two columns from1024 | Above the pair, with individual panel headings |
| Section navigation + article + contents | ArticleLayout | Inside article body, between left navigation and right TOC |
| Section navigation + browsing content without contents | SidebarLayout | In content region |
| Media/metadata accompanying prose | MediaDetail | Alongside media from640; do not place metadata as a full-width interruption below the pair |

The optional composer already places workspace/article titles correctly. Preserve this slot structure when porting. Do not render one unconditional title before every composition. Container width alone does not specify the composition.

## 2. Choose the data shape

| Information | Family | Preserve |
|---|---|---|
| Named properties of one entity | DetailSummary, plain or surfaced | Label/value associations, optional heading and grouped fields |
| Repeated records with comparable attributes | DataCollection, read-only or interactive | Column headings, row alignment, priority metadata, requested direct actions |
| Repeated items with unit/quantity/amount | LineItemTable | Item identity, description, aligned numbers, per-item phone labels, total after all items |
| Narrative summaries with excerpts | ContentList | Heading, metadata and excerpt rhythm |
| Choosing a destination/account | LinkCardGroup | Pill silhouette,64px leading icon, entire row link |

Interactivity is not what makes data tabular. A static line-item table remains tabular without selection, sorting or pagination. Never convert all three data families into the same gray definition list. A column may disappear only when its essential value has a labelled mobile location. Generate both presentations from the same record, never duplicate fixture data by hand in an app.

Expose only needed features: read-only records need no checkboxes; a simple editable list may use direct edit/remove icons; a large record collection may need an action menu and bulk selection. Search, domain filters and bulk controls are distinct capabilities. Do not substitute a generic status filter for requested folder/tag filters. Keep desktop headings even if the phone presentation looks like a list.

## 3. Choose controls and actions separately

Preserve requested field types and options. A select, radio group, searchable combobox and image choice are not interchangeable decoration. With an unspecified type, use select for a longer categorical list, radios for a few mutually exclusive options whose descriptions matter. Conditional fields belong to the selected state; do not show all branches together.

ActionGroup variants:
- `stacked`: full-width primary, then optional secondary/cancel below, at every width. Default for short form/profile tasks and compact review actions.
- `inline`: phone stack, auto-width right-aligned actions from768. For wider editing surfaces with space for peers.
- `workflow`: phone stack, equal-width peer actions from1280. For substantial review/confirm tasks.
- Workspace panel actions follow1→2→1 panel reflow: full width atbase, auto at768, full again at1280.

Add only actions the task calls for. A cancel action, required-fields note, helper sentence under every input, countdown or completed state is not a universal default. Define the requested initial state first, then reachable alternatives. Shared rendering must not insert unrelated domain fields into every summary.

## 4. Keep navigation, preview framing and assets explicit

Breadcrumbs express ancestry; route tabs express siblings. Select them from the route hierarchy and request, rather than adding/removing them to every screen blindly. If reconstruction prompts omit this context, record the assumption; missing breadcrumbs alone do not prove a component failure.

A standalone component specimen uses a neutral white preview host and enough padding to show its boundary. The host is not a rounded shadow card unless the component itself owns a card. Test the component at its intended available width as well as the viewport.

Use supplied institutional SVGs or the target app's consistent SVG icon set at16/20px. Do not approximate controls with emoji or tiny text glyphs. A label compressed on phones must have a visible icon and a preserved accessible name. Domain artwork remains caller data; permitted assets should be used, otherwise preserve the media geometry with an honest placeholder and record the limitation.

## 5. Calibrate a family before expanding it

For a batch, choose at least one dense collection, detail, line-item table, short form, workspace, progress flow and article if present. Inspect desktop and phone; inspect the intermediate breakpoint for workspace/article. Compare with the relevant bundled recipe/gallery, correct the shared component, then generate its siblings. Overflow checks alone cannot detect missing headers, clipped title actions, wrong title placement or flattening a table into a list.
