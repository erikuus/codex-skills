# Validation and acceptance

Validate the requested composition and its real data, not every unrelated recipe. Use source classes and the visual references to establish expectations before taking screenshots.

## Acceptance matrix

| Area | Checks |
|---|---|
| Foundations | Local fonts load; custom palette/type sizes/radius8; source heading weight appearance; soft surface shadows; chosen pastel gradient |
| Shell | Standard and custom footer contents share one white rounded card with shadow, responsive margins and inner frame; exactly one footer landmark when present; 48px institution strip; nominal128px app header; 16/24/32px frame gutters; 8px outer margins atlg; frame1280→1440 at2xl; footer follows long content and sits at bottom for short content |
| Navigation | Global menu trigger in institutional top strip beside optional language switch; correct horizontal/drawer/none choice; same routes on supported widths; current route; no orphan menu button; language/account actions only when functional |
| Footer | Standard/custom choice preserved; all standard service/social/contact links when standard; column/divider change at640; no clipped contact block; feedback popup + ordinary-link fallback |
| Container | Narrow/medium/full chosen by content; exact responsive inset schedule; no nested global gutters; no runaway width on4K |
| Title | Divider continuous; correct spacing; buttons or quiet actions; icon-only phone state keeps accessible names; long translated heading/actions wrap without collision |
| Split/workspace | Stack before1280, row after; correct gaps; sticky first region only in split desktop; workspace fields1→2→1 and main/form sizing |
| Article | Left rail and full TOC at1024; compact trigger640–1023; phone full-width trigger; mobile section links remain reachable; anchor URLs, active scroll tracking, heading focus; bounded TOC height |
| Collection | Essential metadata/actions remain on phone; column reappearance atmd/lg/xl; genuine selection/bulk/filter/page state; no hidden data loss; long identifiers/file names don't push actions offscreen |
| Forms/workflow | Required/invalid/disabled/selected/focused controls; label/error association; progress states; file input/drag/drop and error states if implemented |
| Overlays | Keyboard focus enters/stays/returns; Escape/close/backdrop/navigation/resize all clean up; no body left locked; short landscape remains usable |
| Content/media | Prose heading/list rhythm; linked cards retain secondary controls; disclosure keyboard behavior; media-detail sizing and image fit; motion respects preference |

Test representative widths **390,768,1024,1280,1600** plus320 stress case. Check either side of each changed breakpoint (e.g.639/640,767/768,1023/1024,1279/1280,1535/1536) when implementing that transition. Check1920 or wider to verify the cap. Use actual mobile emulation as well as desktop resizing: many source templates omit viewport meta, which must not be propagated.

Inspect screenshots as well as scrollWidth/clientWidth. An element can clip internally without horizontal document overflow. At minimum inspect the top, title/actions, densest content, footer, and opened overlays. Use realistic long translated strings, populated/empty collections, multiple attachments, errors and unavailable actions where relevant.

## Skill package validation

- Run the skill-creator `quick_validate.py` on the installed folder. It needs PyYAML; use an available environment or a temporary dependency target rather than modifying unrelated project dependencies.
- Check every relative Markdown link and bundled font/logo/CSS path exists.
- Run `python3 -m py_compile scripts/compose.py` and `node --check assets/starter/runtime.js`.
- Exercise the composer with single/split/workspace/article, standard/custom/no footer, both/drawer/no global navigation, preset/custom gradients, plain/button/quiet title actions, compressed/visible labels.
- Confirm unknown/incompatible settings fail, existing output is not overwritten, heading ids remain unique, and optional local article navigation survives global menu removal.
- Review automatic and guided workflow scenarios in composer.md. A syntax validator cannot prove the model will make sensible decisions; inspect the resulting component choices and whether the user was asked only relevant questions.

## Evidence from creation and shell preference correction (2026-10-28)

Current source coverage after cleanup: **101 HTML templates (92 pages, 6 component examples, 3 layouts)**, plus preset and CSS foundations. Active hashes and exclusions are in source-manifest.json. The observations below are historical checks of retained shell/page compositions; they do not expand the active template scope. The VAU layout remains excluded from generic extraction.

Browser evidence:

- Seven canonical content pages at390/768/1024/1280/1600:35 viewport observations, no document width exceeding viewport. These were desktop viewport resizes, not a claim of native mobile correctness for the original files.
- Approved generic shell rendered at1440 and390; menu open/close observed and scroll restored on the explicit close path.
- Eight generated compositions at320/390/640/768/1024/1280/1600/1920:64 cases with no horizontal document overflow; split/workspace change to row at1280; all1920 frames capped at1440.
- True mobile390×844: inner/client/scroll widths all390, article contents opened/closed. Desktop contents link navigation and scroll-driven active state passed.
- Eleven interaction checks passed: modal tab focus, Escape return/scroll cleanup, TOC anchor navigation, TOC resize cleanup, backdrop close, local navigation with global menu absent, custom footer/long visible labels, desktop drawer-only mode, feedback popup context, blocked-popup fallback, and local section deep-link focus after drawer close. Feedback destinations were intercepted in browser tests; no feedback was submitted and no external endpoint availability was asserted.
- Eleven composer checks passed: incompatible slots/widths, unreachable menu configuration, invalid URL scheme, unknown keys, duplicate content/shell ids, unsectioned article, invalid gradient, stable generated/explicit anchors, refusal to overwrite existing output.

The first popup assertion saw the intermediate about:blank page; it passed after waiting for the target URL. Native dialog close checks likewise await the close event before checking restored focus. These are test synchronization details, not unresolved interface defects.

Saved observations: [source-checks.json](../assets/evidence/source-checks.json), [generated-checks.json](../assets/evidence/generated-checks.json), [final-check-summary.json](../assets/evidence/final-check-summary.json), [interaction-checks.json](../assets/evidence/interaction-checks.json), [composer-checks.json](../assets/evidence/composer-checks.json).

Selected visual evidence:

| Capture | Size / state |
|---|---|
| [Generic source shell](../assets/evidence/shell-desktop.png) |1440×1000, institutional header/footer |
| [Source mobile shell](../assets/evidence/shell-mobile.png) |390×844 |
| [Source mobile menu](../assets/evidence/shell-menu.png) |390×844, open |
| [Source narrow content](../assets/evidence/vau-news-list-390.png) |390×1000 |
| [Source title actions](../assets/evidence/vau-bookmark-folder-list-390.png) |390×1000, compressed labels |
| [Source article](../assets/evidence/vau-page-1600.png) |1600×1000, three regions |
| [Generated article desktop](../assets/evidence/generated-article-desktop.png) |1600×1000 |
| [Generated true mobile article](../assets/evidence/generated-article-mobile.png) |390×844 |
| [Generated mobile footer](../assets/evidence/generated-footer-mobile.png) |390×844, scrolled |
| [Generated mobile data surface](../assets/evidence/generated-full-390.png) |390×1000 |

## Preferred shell correction

The canonical shell is now advanced-layout-alt.html. Source shell screenshots and selected generated screenshots above were refreshed. A fresh composer output with language and account links was checked at390/768/1023/1024/1600: menu trigger in the48px institutional strip, alongside language; account in the gradient header; trigger visible below1024 and hidden above; no horizontal overflow. Opening, Escape, scroll cleanup and focus return passed. Drawer-only desktop mode and no-global-menu mode were also checked. See [shell-alt-checks.json](../assets/evidence/shell-alt-checks.json) and [generated top-strip trigger](../assets/evidence/shell-alt-generated-mobile.png).

## Limits

Creation validated the composer and representative family geometry; it did not run an independent model conversation for each operating mode or exercise every original app state. Backend forms, collection filtering/selection, uploads, payments/signatures, authentication, external link availability and cross-browser compatibility remain target-app integration work. The static collection recipe is deliberately a visual pattern. Do not infer those capabilities from a rendered preview.

## Shared footer card correction

Standard and customized footer content now use one shell-owned card template. Verified at 390, 943, 1024, and 1600px: identical white background, 8px rounding, shadow, outer margins, card width, and responsive frame padding; one footer landmark and no horizontal overflow. Standard footer markup is unchanged apart from whitespace after composition. Standard/custom/none composer cases pass. Custom footer screenshots: [390px](../assets/evidence/generated-custom-footer-390.png), [943px](../assets/evidence/generated-custom-footer-943.png).

## Independent reconstruction lessons (attempt1, 2026-10-28)

The historical attempt1 evaluated 119 generated views before scope cleanup. That run retained coverage and broad responsive widths, but repeatedly flattened tables into summaries, put titles outside workspace/article regions, omitted intermediate article navigation, and defaulted every form to inline actions. Use composition.md and the runnable neutral patterns to prevent those decisions. Its original 46-of-48 table-to-nontable substitutions include the former broader scope and are not a current coverage score: judge retained relationships and accessibility, not the HTML tag alone. Missing artwork under restricted inputs is an asset limitation.

Before expanding a shared renderer, inspect representative families against the bundled patterns. Check headers and numeric alignment, phone metadata exactly once, title ownership, action size/label compression, complete progress connectors, initial state and field types. Inspect at640/768/1024/1280 transitions relevant to that family. Record prompt ambiguity separately from design-system mismatch. Maintainability or no-overflow results do not establish visual fidelity. Keep iteration inputs and earlier outputs immutable; a revised skill needs a fresh generation run to establish improvement.
