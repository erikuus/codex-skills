# Foundations

Source: `rahvusarhiiv.preset.js` v1.1.1, `tailwind.css`, compiled `style.css`, and repeated approved templates. Values assume a 16px root size. These are not Tailwind's default palette/type scale.

## Visual hierarchy

Gray-50 canvas surrounds white rounded shell and footer surfaces. Header uses a soft gradient. Content is spacious but controls and data rows are compact. Page headings have a 2px gray-500 rule; secondary sections typically use body-font headings. Avoid replacing this with oversized hero type, heavily saturated primary buttons, large card radii, or shadows on every content block.

## Color tokens

| Shade | Gray | Green | Blue | Yellow | Red |
|---|---|---|---|---|---|
| 50 | #F0F3F6 | #E9F7EE | #E6F1FB | #FDF6EA | #FEECEB |
| 100 | #E8EBF0 | #C4ECD1 | #CCE3F7 | #FCEDD5 | #FDD9D7 |
| 200 | #D3D8DF | #A5D7B6 | #9AC8EF | #F8DBAB | #FBB4AF |
| 300 | #979FAB | #83C79A | #67ACE8 | #F5C882 | #F88E86 |
| 400 | #798492 | #61B77E | #3591E0 | #F1B658 | #F6695E |
| 500 | #6C7683 | #3FA864 | #0275D8 | #EEA42E | #F44336 |
| 600 | #5F6874 | #30834D | #025EAD | #BE8325 | #C3362B |
| 700 | #4E5863 | #205D36 | #014682 | #8F621C | #922820 |
| 800 | #3E4651 | #0F391F | #012F56 | #5F4212 | #621B16 |
| 900 | #242A30 | #001505 | #00172B | #302109 | #310D0B |

Semantic mapping: body gray-900; page heading gray-700; label gray-800; secondary gray-600/700; divider gray-200 or gray-100; page-heading divider gray-500; link blue-600 → blue-500 on hover → blue-700 active; primary action gray-900 → gray-700 hover, white text; selected control green-500, focus ring green-300; table row hover green-50. Pale success/error notices use 50 background + 700 text; warning commonly yellow-100 + yellow-800. Color alone never carries state.

Preserve `bg-gray-50/60` as a 60% opacity fill, not a different gray token. Validate text contrast when applying muted tokens to new roles. Reference use of pale disabled text is not evidence that it is suitable for enabled controls.

## Typography

| Token | Size | Configured line-height |
|---|---|---|
| xs | 11px | 120% |
| sm | 13px | 120% |
| base | 16px | 120% |
| lg | 19px | 120% |
| xl | 23px | 120% |
| 2xl | 28px | 120% |
| 3xl | 33px | 120% |
| 4xl | 40px | 120% |
| 5xl | 48px | 120% |

- Body: Roboto; heading: Raleway; fallback stacks in tokens.json/preset. Use bundled font files for offline output.
- Body's inherited base line-height is 1.5 in the compiled reset; `text-base` explicitly sets 1.2. Forms often override with `leading-6` (24px). Do not globally force all body text to the 120% utility value.
- Page heading: Raleway, 19px → 23px at sm, bold, gray-700. Article title stays 23px. Ordinary content section headings often Roboto 19px medium/bold.
- Labels: 16px semibold, 24px leading, margin-bottom 8px. Compact filter labels: 13px semibold, margin-bottom 4px.
- Long-form `prose` has its own line-height, spacing and color variables. Use explicit semantic prose tokens when porting. The source uses `.prose` and often `prose-h2:font-body prose-h2:text-lg max-w-none`, not uniformly `.prose-gray`.
- Source Raleway variable font is registered only at weight400 despite heading classes requesting700. Browser-rendered reference titles look lighter than a full variable-range700 registration. The bundled preview preserves this registration for visual fidelity. If intentionally enabling the full100–900 range, compare screenshots and agree the heavier resulting headings; this is a typography change, not an automatic repair.

## Geometry

- Spacing is a 4px rhythm with 2px/6px/10px/14px intermediates. Typical gaps: 8, 16, 24, 32, 40, 48, 64px. Larger layout gaps are explicit responsive schedules, not arbitrary scaling.
- Radius: `rounded-sm` 4px; `rounded` 8px; `rounded-full` pill/circle. The preset replaces the radius scale: `rounded-md`/`rounded-lg` are not defined there. Some source classes are ineffective; use the supported token intentionally.
- Surface shadows are multi-layer, soft, and unusually diffuse. Preserve exact `sm`, `md`, default, `lg`, and inner definitions in tokens.json. `sm` is used for collection cards/search; `md` for shell surfaces; larger shadows for overlays.
- Typical icon boxes: 16px inline, 20px actions, 24px menu/close; 40px footer social hit area with varying artwork dimensions. Use SVG with currentColor; preserve institutional/social artwork. Do not add icon-font dependencies just to render legacy `fi-*` classes.

## Breakpoints

| Prefix | Minimum width | Typical responsibilities |
|---|---:|---|
| xs | 320px | Defined, little structural usage; not a safe minimum-width clamp |
| sm | 640px | Footer columns, 23px title, title action labels, some media rows |
| md | 768px | 24px frame gutters, horizontal steps, paired form fields, first table metadata columns |
| lg | 1024px | 8px shell margins, 32px gutters, horizontal main nav, section menu, article contents rail |
| xl | 1280px | 40px content top/56px bottom, two-region workflows, denser desktop collections |
| 2xl | 1536px | Frame cap becomes 1440px, wider composition gaps |

Five useful visual categories are phone, small tablet, large tablet/compact laptop, desktop, and large desktop. The exact breakpoints—not the device names—control implementation. At 1920/4K retain the 1440px cap.

## Build and portability

The repository has no package.json or lockfile despite README npm instructions. The compiled stylesheet identifies **Tailwind CSS 3.4.19** in its banner. Its CommonJS preset, `@tailwind` directives, typography modifiers, and JIT config are consistent with that generation. The precise plugin dependency versions and reproducible npm build are not pinned in the checkout. For an existing modern Tailwind app, translate the tokens into that version's supported configuration and test; do not blindly paste a v3-era config into v4.

For a static preview the bundled compiled CSS is sufficient for existing recipes. New utility strings may not exist in it. Either compile all target templates with a compatible build, add explicit CSS for new rules, or use equivalent native component CSS. Dynamic class interpolation must not evade the target compiler's scan.

Original preset references `colors.info.DEFAULT` in prose links although no `info` palette exists. Resolve this to the system's blue-600 when porting; this is a repair, not an additional source token. Excluded widget specimens provide no additional design contracts. The portable stylesheet omits their dedicated lightbox and jQuery widget skins; generic utilities remain available for the retained recipes.

## Preserve tokens when porting

Copy the exact gradient angle and stops from tokens.json, including stops outside0–100% (green–lavender ends at158.87%). Normalizing to100% visibly overemphasizes lavender. Copy the complete multilayer shadow strings; a generic two-layer shadow is not equivalent. The runnable starter already uses the correct gradient; compiled style.css supplies the shadows. Main navigation is16px, utility navigation13px; typography tables14px, toolbar13px. Port scoped selectors rather than applying one small-text rule to all content.
