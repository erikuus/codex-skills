# Fancybox 2 and CJuiDialog close controls

These are different designs with different owners. Preserve the actual plugin close element and event handler. Do not apply one generic `.close`, button or SVG rule to both. The values below were traced through local VAU/theme/extension sources; this is not a claim of a live VAU browser inspection.

## Fancybox 2: retain the plugin sprite and outside-corner placement

VAU's `ext.widgets.fancybox2.XFancyBox2` publishes Fancybox **2.1.5** JS and CSS. Its default `tpl.closeBtn` is an empty anchor with classes `fancybox-item fancybox-close` and title `Close`. After opening, the plugin appends it directly to `.fancybox-skin` and binds its close handler. It is not an inline SVG, text ×, CJuiDialog icon or Joyful utility button.

| Property | Required Fancybox 2 source value |
| --- | --- |
| Containing block | `.fancybox-skin { position: relative; }` |
| Close element | `position: absolute; width: 36px; height: 36px` |
| Placement | `top: -18px; right: -18px` (straddles the outside top-right corner) |
| Stacking/cursor | `z-index: 8040; cursor: pointer` |
| Artwork | `fancybox_sprite.png` background, supplied by plugin CSS |
| High-density artwork | At device pixel ratio ≥1.5, `fancybox_sprite@2x.png`, **`background-size: 44px 152px`** |

The 44×152 background size is the entire sprite sheet, not the close button dimensions. Do not set `background-size: contain`, resize the whole sheet to 36×36, add a second SVG, or move the button inside the panel. Keep both sprite files at the URLs resolved relative to the published plugin CSS; a missing sprite leaves a correctly positioned but invisible control.

Joyful's Fancybox-specific rules only give `.fancybox-skin` and `.fancybox-image` the preset's 8px `rounded` radius. They do **not** replace the close-control artwork, size or offsets. Preserve the plugin's structural stylesheet. After opening, Fancybox sets `.fancybox-wrap` overflow to `visible`; do not add `overflow-hidden` to the wrap/skin to achieve rounded corners, as it clips the outside close button. The content's `.fancybox-inner` may retain its own overflow behavior.

Respect intentional nondismissible configurations: VAU's company-selection flow sets `modal:true` and `closeBtn:false`. A theme must not reintroduce its close control or change dismissal rules. Apply these rules to Fancybox 2; inspect a different Fancybox version separately rather than assuming these selectors/assets exist.

## CJuiDialog: 20px SVG inside the title bar

VAU's compiled Joyful CSS and the playground's `tailwind.css` supply the following appearance overrides, already ported into the skill's `tailwind/widgets.css`:

| Selector/property | Original Joyful rule |
| --- | --- |
| `.ui-dialog .ui-dialog-titlebar-close .ui-icon` | `display: none !important` (hide the original sprite, only within this control) |
| `.ui-dialog .ui-dialog-titlebar-close::before` | `content: ""`, `display: inline-block !important`, **width/height `1.25rem` = 20px** at the reference 16px root size |
| Pseudo-element artwork | Original 24×24-viewBox SVG data URI, centered no-repeat background, `background-size: contain !important` |
| Pseudo-element original spacing | `margin-right: .5rem !important` (`mr-2`) |
| Close element placement | **`right: 1rem !important` = 16px**, relative to the title bar |
| Hover and focus stability | **`top: 50% !important; margin-top: -10px !important; padding: 1px !important`** |
| Title bar/content padding | `py-3 px-4`: 12px vertically, 16px horizontally |

The 24×24 SVG viewBox does not mean a 24px displayed icon. Keep the 20px CSS box. The pseudo-element draws the glyph; the existing anchor/button remains the interactive control.

Joyful does not supply all normal-state positioning: jQuery UI supplies the relatively positioned title bar and absolutely positioned close control, `top:50%`, `margin-top:-10px`, and `padding:1px`. The source's silver CSS has a legacy 19×18px control; current Yii 1.1.33-dev's bundled jQuery UI base CSS uses a 20×20px control. Do not confuse these button dimensions with the 20×20 glyph, or transplant the legacy dimensions over a newer plugin. Inspect which CSS the target actually registers, including `clientScript.scriptMap` and any theme URL overrides. This VAU checkout lacks its runtime `protected/config`, so the presence of both silver CSS versions does not prove which one every deployed route loads.

The hover/focus overrides are deliberate: the legacy silver stylesheet otherwise changes padding from 1px to 0 and makes the glyph jump. Keep its geometry stable in normal, hover, keyboard-focus and pressed states. Do not remove keyboard focus indication merely because old silver CSS suppressed it; preserve an accessible name and the plugin's own close/escape/cancellation behavior.

### Current jQuery UI compatibility: avoid an offscreen pseudo-element

The current bundled base CSS sets `.ui-button-icon-only { text-indent: -9999px; }`. Simply copying VAU's inline-block `::before` into that button moves the replacement glyph offscreen as well. This was reproduced with actual jQuery UI from Yii 1.1.33-dev, even though the button and pseudo-element reported the expected sizes.

The bundled `widgets.css` therefore adds this narrowly scoped adaptation after the original SVG rule:

```css
.ui-dialog .ui-dialog-titlebar-close.ui-button-icon-only::before {
  position: absolute !important;
  left: 50% !important;
  top: 50% !important;
  margin: 0 !important;
  transform: translate(-50%, -50%) !important;
}
```

It centers the same 20×20 SVG inside the modern control, replacing the legacy pseudo-element margin for this case. Keep the button's hidden text/title and native event binding intact. Do not globally reset `.ui-button-icon-only` text indentation, expose `Close` alongside the icon, hide every `.ui-icon`, or add another close element. The data-URI SVG's `currentColor` is internal to the image; do not assume setting the button's text color will recolor an external background SVG.

Keep these appearance rules in the compiled theme's integration sources, not application components or a second untracked stylesheet. The supplied rules use explicit `!important` where necessary to override plugin appearance even when Yii injects its unlayered CSS later. Retain plugin structural CSS and inspect computed styles if another theme introduces competing important rules.

## Acceptance checks

Open actual Fancybox and CJuiDialog instances, not just static imitation markup. Check desktop and narrow viewports:

- Fancybox: 36×36 control at -18px/-18px; visible outside the corner without clipping; sprite loads at device scale 1 and 2; high-density sheet uses 44×152 background size. Confirm click closes and configured Escape behavior survives. Do not require a close button for intentionally modal/nonclosable flows.
- CJuiDialog: exactly one visible 20×20 SVG, original sprite hidden, right inset 16px, title unobscured, and no movement between normal/hover/focus/pressed states. With current jQuery UI, verify the pseudo-element is actually visible inside the button, not merely that computed width is 20px. Check screenshot plus click and keyboard dismissal, including any existing before-close veto.
- Reopen after AJAX-loaded content; preserve the real close handler and accessible label. Inspect network requests, cascade order, overflow/clipping and both hit-area and glyph geometry if it fails.

## Source locations

- VAU `css/themes/joyful/style.css`: `.ui-dialog .ui-dialog-titlebar-close` rules around lines 1704–1727; Fancybox rules near the beginning of widget styling. Bundled reference: `assets/reference/vau-frozen.css`.
- Playground `tailwind.css`: original utility-based overrides. Bundled snapshot: `assets/reference/tailwind.css`; runtime port: `assets/app/themes/joyful/tailwind/widgets.css`.
- `/Users/erikuus/dev/yii/extensions-1.1.8/widgets/fancybox2/XFancyBox2.php` and `assets/jquery.fancybox.{css,js}`: publication, dimensions, sprite media query, default template, append/close binding and overflow restoration.
- VAU `css/themes/jui/silver/jquery-ui.css` and `jquery-ui-1.12.0.css`: inherited legacy title-bar/control geometry and state styles.
- `/Users/erikuus/dev/yii/yii-1.1.33-dev/web/js/source/jui/css/base/jquery-ui.css`: current control dimensions and icon-only text indentation.
