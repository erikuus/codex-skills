# Tailwind setup without framework assumptions

## Package and source ownership

`assets/starter/tailwind/` preserves the source skill's institutional preset and lockfile dependencies: Tailwind/CLI 4.3.3, forms 0.5.11, typography 0.5.20, selector-parser override 6.1.5. Use these pinned versions for the reproducible baseline, not an unbounded install. The custom preset is the design; stock Tailwind colors/type/radii are not equivalent.

Copy/merge the starter's `tailwind`, `fonts`, `images` and necessary `js` into one separate Joyful asset directory, retaining their relative relationships. Default output is sibling `css/style.css`; its font URLs resolve to `../fonts/`. The layout's example URLs assume this asset directory is the URL base; adapt them through the app's normal base-URL handling, including subdirectory deployments. Do not assume `/themes`, `/assets` or `/frontend` universally.

Read actual package files before merging into an existing build. Use a dedicated Joyful build or add a Joyful entry/output to the existing pipeline; preserve default build inputs/outputs, lockfiles and unrelated dependencies; never overwrite package.json blindly. The standalone CLI needs no PostCSS/autoprefixer config. A target's established PostCSS integration may use the compatible official Tailwind PostCSS package deliberately, but must preserve preset, plugins, scanning and output. Select theme assets from the same application setting as templates. Default pages load their existing styles; Joyful pages load the Joyful output. Do not load both global design stylesheets together or overwrite the default CSS.

## Build commands

From the copied Tailwind directory:

```sh
npm ci
npm run build -- --source /absolute/app/themes/joyful/views --source /absolute/app/public/assets/joyful/js
npm run dev -- --source /absolute/app/themes/joyful/views --source /absolute/app/public/assets/joyful/js
```

Each `--source` is an existing directory or individual file. Repeat it for rendering code outside the normal view tree, shared includes, icon partials and generated-markup scripts. Paths resolve from the command's working directory, are normalized and registered in ignored `sources.generated.css`. There is deliberately no inferred framework root. Missing sources fail before generation. Do not scan uploads, database exports, cache, historical reference snapshots, vendor trees or the skill's illustrative HTML to hide missing app classes.

For Nimeregister, first inspect the default `frontend/views`, `admin/views` and inline admin rendering, then create separate Joyful presentation. Scan the resulting Joyful view roots, Joyful scripts, explicitly shared compatible rendering files and any individual admin PHP files that still emit Joyful markup. Avoid scanning all of `admin/` just to pick up a few rendering files, as it also contains vendor editor code. These are examples, not hardcoded builder defaults.

`--out /absolute/path/style.css` changes output deliberately; fix font/image URLs accordingly. Commit build configuration, pinned lockfile and application markup. Follow the target's release convention for generated CSS. Keep node_modules, generated absolute source paths and preview files untracked. Document the Joyful build separately from the default build. Rebuild whenever Joyful template classes change, including plain PHP includes and action markup.

The input uses Tailwind 4 `@import`, explicit `source(none)`/`@source`, `@config` and forms/typography plugins. Complete literal classes must exist in scanned files. Do not construct `'bg-' + color` and expect generation; use a bounded explicit mapping, or a small deliberate inline source list when unavoidable. CSS custom properties suit numeric preview heights; do not interpolate utility names for user-selected line counts.

## Preserve the actual design

- `rounded` is 8px, `text-sm` is 13px, `text-lg` is 18px (1.125rem) and `text-xl` is 23px. [Design system PR 33](https://github.com/Rahvusarhiiv2/disainisysteem/pull/33) uses local Sora at 600 for `font-heading` and prose h1–h6. Bundle the supplied variable font and OFL. Keep Roboto for body text and use `assets/reference/fonts/` only for the historical comparison.
- Keep the preset's multi-layer shadow names and colors. Do not apply a generic Tailwind v3→v4 shadow/radius rename table to this custom scale.
- Typography table modifiers use v4 ordering: `prose-tr:odd:*`, `prose-tr:hover:*`, `prose-td:first:*` and `prose-td:last:*`.
- Keep explicit border colors and focus ring widths/colors. `focus:outline-hidden` retains forced-color visibility. Hover variants apply on hover-capable devices; test pointer and touch separately.
- Tailwind preflight/forms can affect existing plugins. Keep needed plugin structural CSS and scope conflicts deliberately. Only the target's relevant plugin rules belong in the app; this payload does not globally install legacy widget overrides.
- The header gradient is the sole palette exception to the historical green reference. `bg-theme-vau` already holds the approved warm gradient; do not change other tokens to approximate it.

To build the skill specimen in a disposable copy, run `npm ci --prefix assets/starter/tailwind`, then `npm run build --prefix assets/starter/tailwind -- --source "$PWD/assets/html" --source "$PWD/assets/starter/js"`, and `node scripts/render-preview.mjs`. This fixture command intentionally scans the specimen; an application build must scan the real application instead.
