# Runnable composer and framework integration

`scripts/compose.py` creates a portable static starting page in a **new** directory. It uses bundled CSS/fonts/RA artwork, a generic text app wordmark, complete institutional footer, native modal drawers, and no CDN/runtime dependencies. Its global menu trigger follows `advanced-layout-alt.html`: in the narrow top strip next to the optional language link. It does not publish, install packages or overwrite existing output.

Use it to make decisions reviewable or start a plain-HTML screen. In an existing React/Vue/Phoenix/Yii/other project, translate the same contracts into the established component system; do not embed a second document/shell inside the app.

```sh
python3 /Users/erikuus/.agents/skills/rahvusarhiiv-design-system/scripts/compose.py \
  --config /absolute/path/design.json \
  --content /absolute/path/content.html \
  --output /absolute/path/new-preview-directory
```

Add `--secondary /absolute/path/secondary.html` for split/workspace. Content files are trusted local HTML fragments, not whole HTML documents. They are inserted verbatim, so this helper is not an HTML sanitizer for untrusted uploads. Route URLs/text in the JSON are validated/escaped. Local content images and attachments must be copied into the output by the caller; the helper only copies its own foundation assets.

The composer copies and loads `patterns.css` automatically, so line-item, detail, progress and action-group recipes retain their styles when placed in a content slot. These are visual components; application behavior still belongs to the target app.

## Configuration

```json
{
  "app_name": "Kogude portaal",
  "home_url": "./index.html",
  "lang": "et",
  "navigation": {
    "mode": "both",
    "items": [
      {"label": "Ülevaade", "href": "./index.html", "current": true},
      {"label": "Juhend", "href": "./guide.html"}
    ]
  },
  "footer": {"variant": "standard"},
  "gradient": "green-lavender",
  "layout": {"type": "single", "width": "medium"},
  "title": {
    "text": "Kirje andmed",
    "spacing": "normal",
    "mobile_labels": "icons",
    "actions": [
      {"label": "Lisa kirje", "href": "./new.html", "icon": "plus", "style": "primary"}
    ]
  }
}
```

Replace routes with real destinations; the helper doesn't create those other pages.

| Key | Supported choices / behavior |
|---|---|
| navigation.mode | both (lg horizontal + phone drawer), drawer (all widths), none. Default both if items exist, otherwise none. Empty menus and hidden item sets are rejected. Desktop-only requires manual integration with an explicit small-screen alternative. |
| gradient | green-lavender; peach-lavender; or `{ "start":"#CCEAD6", "end":"#ECDDF4", "angle":95.19 }`. Custom colors use0/100% stops; edit component CSS if custom stops are required. |
| footer | `{ "variant":"standard" }`, `{ "variant":"none" }`, or `{ "variant":"custom", "file":"footer.html" }`. Custom file is relative to the config file and contains trusted **inner content only**, without a `<footer>` or outer card/frame. Both standard and custom content are wrapped by `assets/starter/footer.html`, preserving the white card, shadow, rounding, margins, responsive frame, and nominal height. Custom content receives 24px vertical padding; for example `<p>Application help and contact links</p>`. |
| layout.type | single; split (equal columns atxl); workspace (form/helper + main atxl); article (coupled section nav/content/TOC). |
| layout.width | single: full/narrow/medium/form/summary. Other compositions require full and own column widths. |
| layout.sticky_first | split only, true by default. First content slot is sticky atxl. |
| title.spacing | normal40px; compact24px; collection24→40 atmd. |
| title.mobile_labels | icons hides labels visually below640 only for actions that have an icon; visible keeps labels and permits wrapping. |
| title.actions | Links with label/href, optional icon and style primary/secondary/quiet/link. Stateful actions must be integrated as framework/native buttons; don't use javascript: URLs. |
| icons | plus, back, print, help, external (menu/close reserved for navigation). Replace artwork/extend the local SVG map when needed; no icon-font dependency. |
| language / account | Optional `{ "label":"English", "href":"./en/index.html" }` or corresponding real account route. Omitted controls are absent. |
| breadcrumbs | Optional array of label/href/current items. Wraps rather than clipping long names. Current item uses aria-current=page. |
| section_navigation | Article only: array of label/href/current items, reused in left rail and a local mobile drawer. Remains available when global menu is none. |

Article content must contain h2 section headings. Existing quoted ids are preserved; missing ids are generated from text and deduplicated. Duplicate ids elsewhere, unknown configuration keys, invalid variants, unsafe URL schemes and incompatible slot/layout combinations fail before writing output. For complex HTML, pass explicitly quoted stable heading ids. The generated page's own title is h1; fragments should start at h2 or lower.

## Component adaptation

- Replace the generic wordmark with the target app's logo while retaining44→48px height and avoiding overflow. This is separate from the institutional mark in the top strip.
- Preserve the main shell and title/width contracts when converting to components. Map children/slots to trusted application render trees, not arbitrary innerHTML.
- Render navigation, article contents, table mobile/desktop metadata and step variants from one data model each.
- Expose properties such as width, action style and layout role; keep breakpoint rules private to the component. Avoid a public `className` requirement for basic responsiveness.
- `style.css` contains a finite Tailwind3.4.19 snapshot with excluded widget skins removed and some retained app rules; a production port should generate only its own used styles from the tokens. `system.css` supplies the explicitly extracted component rules and documented repairs.
- Runtime handles shell/local/TOC drawers, focus/scroll cleanup, article anchor/scroll indication, and feedback popup/fallback. It does **not** handle collection filtering, uploads, form submission, authentication, payments, language translation, or recipe controls. Integrate those before claiming a functioning app.

## Concrete requests to exercise the skill

Automatic: “Build a records browser for a different Rahvusarhiiv app. Decide the layout yourself.” Expected: infer the shell choices, use full-width DataCollection with actual small-screen metadata relocation, avoid VAU vocabulary, wire the requested browser controls.

Guided: “Build an institutional application screen and let me choose the design.” Expected: offer menu/footer/gradient choices first, then only consequential content-layout choices. Preserve answers in the generated result.

Article: “Build a multi-section help page, without a global menu.” Expected: ArticleLayout retains its local section-navigation and contents access on phone/tablet, even though the global shell menu is absent.

Adaptation: “Use this system inside our existing framework with a custom footer.” Expected: use native components/routes, extract only the needed contracts, ask for missing custom-footer content in guided mode or derive it from existing app content in automatic mode; never invent institutional facts. Retain the shared white footer card when adapting to native components; customization changes its contents, not its surface.
