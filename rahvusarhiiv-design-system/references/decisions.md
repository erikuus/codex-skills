# Automatic and human-guided decisions

## Guided opening

Ask the unanswered choices together when the UI supports it, or one at a time otherwise. State the recommendation and its practical effect. Do not ask questions already answered in the request or established app.

1. **Navigation:** “Do you need a horizontal menu and a mobile menu?”
   - Both: horizontal links at 1024px+, drawer below with its trigger in the institutional top strip; recommended for a multi-section app.
   - Drawer at every width: appropriate when many links would crowd the header.
   - Neither: appropriate for a self-contained screen with no global destinations.
   A desktop-only menu can be a deliberate custom choice, but retain an equivalent route path on smaller screens. Local section navigation and article contents are separate from global navigation.
2. **Footer:** “Use the complete standard Rahvusarhiiv footer or a customized footer?”
   - Standard (recommended for institutional apps): preserve all four service links, contact block, six social destinations, responsive divider, and feedback popup with fallback.
   - Customized: ask what links/contact information/branding must change. Customize only the content inside the same white footer card; its rounded corners, shadow, responsive margins, and frame are invariant. Inner content can use a different arrangement.
   - No footer is a valid explicit user choice, not the institutional default.
3. **Header gradient:** “Which colors should the header gradient use?”
   - Green–lavender: `linear-gradient(95.19deg, #CCEAD6 0.8%, #ECDDF4 158.87%)`.
   - Peach–lavender: `linear-gradient(96.04deg, rgba(247,227,204,.65) -17.14%, #ECDDF4 94.45%)`.
   - Custom: obtain start/end colors and optionally angle/stops. Keep the result pale enough for dark header text and show a preview. Gradient colors do not automatically recolor links, controls, or status colors.

Then resolve the app title/logo, available routes and current route, language switching, and sign-in/account controls from the target app. Ask only for missing product decisions. Do not insert an inert “English” or “Sisene” control merely because it exists in the reference.

## Automatic defaults and decision rules

| Decision | Default / selection rule |
|---|---|
| Institutional chrome | Use the generic shell and standard Rahvusarhiiv footer for a Rahvusarhiiv app |
| App identity | Existing app name/logo; text wordmark if no asset exists; never VAU's colored-dot mark |
| Navigation | Both views when real top-level routes exist; none for a self-contained page; drawer-only for a dense hierarchy |
| Gradient | Preserve an established app gradient; otherwise green–lavender |
| Language/account | Render only when a destination or handler exists |
| Single-column width | Narrow for reading/list summaries; medium for multi-field workflows and compact records; full for dense collections |
| Two related regions | Split at xl (1280px) for detail + substantial form; lg (1024px) only for genuinely smaller paired regions |
| Sticky region | First summary at top 40px on split desktop, only when it fits usefully; never sticky across stacked phone content |
| Guided long-form content | ArticleLayout with section nav + content + TOC; normal ContentContainer when no hierarchy/sections exist |
| Page title | Plain by default; buttons for primary creation/navigation; quiet links for utilities |
| Label compression | Hide action labels visually below sm only when an icon identifies each action; keep the accessible name |
| Tables | Move important hidden columns into primary cell at smaller widths; reserve horizontal scroll for inherently wide content |
| Alerts/status | Choose by message meaning; do not reuse VAU-specific status/type color mappings |
| Integration | Use the target app's components and routing; reuse visual contracts, not legacy widget internals |

Offer only meaningful options. “Narrow / medium / full / two-region / article” describes structure; “news / orders / permissions” describes a past application and is not a component API.

## Record decisions

For a significant screen, keep a compact record alongside the implementation or in the response:

```json
{
  "mode": "automatic",
  "shell": {"navigation": "both", "footer": "standard", "gradient": "green-lavender"},
  "content": {"layout": "single", "width": "medium"},
  "title": {"actions": "buttons", "mobileLabels": "icons"},
  "reason": "A multi-field workflow with two page actions and existing global routes."
}
```

This is a decision record, not the composer's exact schema. See composer.md for executable configuration.

## Reconsideration

If realistic labels, translated text, record density, or available width break the initial choice, repair the component's layout before adding page-specific exceptions. In guided mode explain a material change to an agreed structure and obtain the user's choice; routine wrapping, accessible names, and focus fixes do not need a new design decision.
