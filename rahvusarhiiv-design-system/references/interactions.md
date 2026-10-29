# Interaction contracts and source repairs

The repository README explicitly calls this a workbench, with some functional interactions and some deliberate placeholders. Preserve visual evidence; implement behavior for the target app.

## State ownership

| Owner | State | Required behavior |
|---|---|---|
| Shell navigation | current route, drawer open | same items at all sizes, focus return, scroll restoration |
| ArticleLayout | active section, contents drawer, section menu | one section model; anchor navigation + scroll tracking; mobile access to both navigation levels |
| DataCollection | filter draft/applied query, selected ids, page, page size, row menu | state changes reflect data; resetting/filtering reconciles page and selection |
| Disclosure/notice | expanded/dismissed | keyboard trigger, updated expanded state or removal |
| FileCollection | queued/uploading/complete/error | actual file control, reachable retry/removal, announce status |
| ChoiceGroup | selected value | keyboard-operable radio semantics, submit real value |

Component state belongs in the application's usual framework. Alpine3.12.3 is a source implementation detail, not a cross-stack requirement. Article source additionally uses Alpine intersect and a scroll helper; omitting either silently loses behavior. The bundled starter uses native dialog and vanilla JS to avoid CDN dependencies.

## Drawers/dialogs

Open from a real button; bind aria-expanded/controls. Move focus inside and keep background inert; trap keyboard focus. Close on visible close button, Escape, backdrop when appropriate, successful navigation, and crossing into a breakpoint where the drawer becomes inapplicable. Every close path restores scroll and returns focus to a visible trigger (or a logical fallback after navigation/resize). Use one owner for scroll locking if overlays can nest. Keep bottom items reachable on short landscape screens.

Source caveats: outside-click often sets open=false without clearing body overflow lock. Shell header z-index/stacking and fixed descendants need inspection. A zero-sized wrapper with fixed children can make a visibility assertion on the dialog wrapper misleading; assert the actual panel/close button and its on-screen bounds. Do not test only the boolean state.

## Article navigation

Use stable unique heading ids and real href anchors; support direct fragment URLs and keyboard activation. Desktop and mobile TOC use one section list. Active indication updates during scrolling without fighting an intentional TOC click. Smooth scrolling is optional and respects reduced-motion. Choose one breakpoint for TOC rail, compact trigger and drawer cleanup. Keep the section-navigation links reachable below1024 even when global navigation is disabled; a local section-menu trigger is sufficient.

## Prototype defects to repair on extraction

- Many templates omit viewport meta; generated apps include width=device-width, initial-scale=1. Desktop browser resizing alone does not verify true phone layout.
- `focus-visible::ring-*` uses an invalid doubled colon; correct focus style. `hover:focus:active` requires all states simultaneously; use deliberate independent states when the intended effect is ordinary hover/focus/active.
- Unsupported classes (`w-42`, `mx-42`, `rounded-md` with the replaced radius scale), `text-gar-600`, `y-1.5`, duplicated/conflicting margin declarations: inspect generated CSS instead of canonizing a typo.
- Nested anchors/buttons, repeated ids such as article1, static ARIA expanded state, unlabeled icon links, click divs, hidden radio controls: preserve geometry while repairing semantics.
- Preserve the observed Raleway registration unless deliberately changing heading weight; repair undefined prose info color as described in foundations.md.
- Source page-title floats can collide with long text; use wrapping layout. Source fixed footer/TOC heights can clip; allow growth/bounded internal scrolling.
- Row select-all toggling a panel is not selection logic. Empty hrefs and fake page counts must become real app operations or clearly marked preview data.
- File drop targets without inputs and external login/payment/signature blocks are integration examples only.
- Hardcoded popup geometry is suitable for the legacy feedback flow, but provide ordinary navigation if a popup is blocked. Do not send feedback during tests.
- Do not copy sample personal details, CSRF-like hidden fields, `/vau/index-dev.php` paths, or concrete order/status mappings.

## What is intentionally preserved

The standard footer's institutional destinations/contact content and SVG art are preserved as the requested reusable institution-wide component. Neutral header geometry, exact token values, container inset schedules, table data-relocation breakpoints, and one→two→one field/card layouts are preserved. Repairs should not become a gratuitous redesign.
