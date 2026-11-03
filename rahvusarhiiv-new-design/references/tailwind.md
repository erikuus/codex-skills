# Tailwind setup without framework assumptions

## Package and source ownership

`assets/starter/tailwind/` preserves the source skill's institutional preset and lockfile dependencies: Tailwind/CLI 4.3.3, forms 0.5.11, typography 0.5.20, selector-parser override 6.1.5. Use these pinned versions for the reproducible baseline, not an unbounded install. The custom preset is the design; stock Tailwind colors/type/radii are not equivalent.

Copy/merge the starter's `tailwind`, `fonts`, `images` and necessary `js` into one target asset directory, retaining their relative relationships. Default output is sibling `css/style.css`; its font URLs resolve to `../fonts/`. The layout's example URLs assume this asset directory is the URL base; adapt them through the app's normal base-URL handling, including subdirectory deployments. Do not assume `/themes`, `/assets` or `/frontend` universally.

Read actual package files before merging into an existing build. Integrate one build pipeline, retain its lockfile and unrelated dependencies; never overwrite package.json blindly. The standalone CLI needs no PostCSS/autoprefixer config. A target's established PostCSS integration may use the compatible official Tailwind PostCSS package deliberately, but must preserve preset, plugins, scanning and output. Do not load old and new global design stylesheets together.

## Build commands

From the copied Tailwind directory:

```sh
npm ci
npm run build -- --source /absolute/app/templates --source /absolute/app/scripts
npm run dev -- --source /absolute/app/templates --source /absolute/app/scripts
```

Each `--source` is an existing directory or individual file. Repeat it for rendering code outside the normal view tree, shared includes, icon partials and generated-markup scripts. Paths resolve from the command's working directory, are normalized and registered in ignored `sources.generated.css`. There is deliberately no inferred framework root. Missing sources fail before generation. Do not scan uploads, database exports, cache, historical reference snapshots, vendor trees or the skill's illustrative HTML to hide missing app classes.

For Nimeregister, inspect and include `frontend/views`, `admin/views`, relevant `frontend/js`/`admin/js`, and individual admin PHP files that actually emit markup. Avoid scanning all of `admin/` just to pick up a few rendering files, as it also contains vendor editor code. These are examples, not hardcoded builder defaults.

`--out /absolute/path/style.css` changes output deliberately; fix font/image URLs accordingly. Commit build configuration, pinned lockfile and application markup. Follow the target's release convention for generated CSS. Keep node_modules, generated absolute source paths and preview files untracked. Rebuild whenever template classes change, including plain PHP includes and action markup.

The input uses Tailwind 4 `@import`, explicit `source(none)`/`@source`, `@config` and forms/typography plugins. Complete literal classes must exist in scanned files. Do not construct `'bg-' + color` and expect generation; use a bounded explicit mapping, or a small deliberate inline source list when unavoidable. CSS custom properties suit numeric preview heights; do not interpolate utility names for user-selected line counts.

## Preserve the actual design

- `rounded` is 8px, `text-sm` is 13px, `text-lg` is 19px and `text-xl` is 23px. Roboto body text and Raleway headings use packaged local fonts; no font CDN required.
- Keep the preset's multi-layer shadow names and colors. Do not apply a generic Tailwind v3→v4 shadow/radius rename table to this custom scale.
- Typography table modifiers use v4 ordering: `prose-tr:odd:*`, `prose-tr:hover:*`, `prose-td:first:*` and `prose-td:last:*`.
- Keep explicit border colors and focus ring widths/colors. `focus:outline-hidden` retains forced-color visibility. Hover variants apply on hover-capable devices; test pointer and touch separately.
- Tailwind preflight/forms can affect existing plugins. Keep needed plugin structural CSS and scope conflicts deliberately. Only the target's relevant plugin rules belong in the app; this payload does not globally install legacy widget overrides.
- The header gradient is the sole palette exception to the historical green reference. `bg-theme-vau` already holds the approved warm gradient; do not change other tokens to approximate it.

To build the skill specimen in a disposable copy, run `npm ci --prefix assets/starter/tailwind`, then `npm run build --prefix assets/starter/tailwind -- --source "$PWD/assets/html" --source "$PWD/assets/starter/js"`, and `node scripts/render-preview.mjs`. This fixture command intentionally scans the specimen; an application build must scan the real application instead.
