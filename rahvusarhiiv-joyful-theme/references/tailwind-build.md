# Tailwind: source findings and supported build

## What the playground actually configures

Inspected `/Users/erikuus/Documents/Github/tailwindui-playground/`:

- `tailwind.config.js` loads `rahvusarhiiv.preset.js`, specifies `mode:'jit'`, scans `views/**/*.html`, only top-level `views/*.php`, and `index.html`, and registers forms, typography, aspect-ratio and line-clamp plugins.
- `postcss.config.js` uses the old `tailwindcss` PostCSS plugin and Autoprefixer.
- `tailwind.css` contains v3 `@tailwind` directives, body defaults, local `@font-face`, generic jQuery UI/Fancybox overrides, and VAU-specific order/status rules.
- `rahvusarhiiv.preset.js` replaces colors, spacing, radii, shadows, font families, font sizes and breakpoints; extends 90rem `xxl`, gradient backgrounds and typography. Its values are the design, not optional decorations. `rounded` means 8px; `rounded-sm` means 4px. Its shadows are large multi-layer institutional shadows, not Tailwind defaults.
- Committed `style.css` identifies Tailwind **3.1.8**. The checkout has **no package.json or lockfile**, despite the README mentioning npm commands. Do not claim that the original checkout can be rebuilt with `npm ci` or that its PHP scan covers an application/extension library.

Original source/config snapshots are in `assets/reference/`. Runtime output must be rebuilt from source. The earlier frozen-CSS/handwritten-adapter approach prevented reliable utility generation and encouraged visual substitutions; do not repeat it.

## Pinned modern implementation

`assets/app/themes/joyful/tailwind/` includes:

- Tailwind and CLI **4.3.3**, forms **0.5.11**, typography **0.5.20**, plus a committed npm lockfile. The selector-parser override pins **6.1.5**, avoiding the vulnerable transitive `<6.1.5` version. No browser runtime depends on npm.
- `input.css`: `@import "tailwindcss" source(none)`, explicit source registration, `@config`, forms/typography `@plugin`, body/default border/placeholder compatibility, and local font faces.
- `tailwind.config.cjs` and `rahvusarhiiv.preset.cjs`: an explicit v4 compatibility bridge for the source design preset. JavaScript config is supported but is not automatically discovered in v4. Keeping this preset avoids accidental token changes during migration; it is not the old v3 build pipeline.
- `widgets.css`: only the source's generic widget appearance rules, ported to v4 syntax. VAU order/status rules are omitted. Keep the target plugin's structural stylesheet and inspect cascade interactions; do not assume appearance overrides implement dialogs.
- `yii.css`: small layout/validation/responsiveness integration rules using the preset. This is not permission to rebuild the design with arbitrary hex values or broad app-selector overrides.
- `build.mjs`: resolves the app relative to itself, requires the actual extension root, creates local `sources.generated.css`, and invokes the pinned local CLI. Generated source paths and `node_modules` are ignored. CSS goes to `themes/joyful/css/style.css`.

From the target theme's `tailwind/` directory:

```sh
npm ci
npm run build -- --extensions-root /absolute/path/to/extensions
npm run dev -- --extensions-root /absolute/path/to/extensions
```

`JOYFUL_EXTENSIONS_ROOT` can supply the same path. For a nonstandard rendering directory, append `--source /absolute/extra/views`. Inspect the actual generated source manifest. All template, skin, PHP widget and JavaScript class sources must participate, including shared extensions outside the repository and files ignored by Git. Automatic scanning is intentionally disabled. Do not scan database exports, uploads, vendor packages or the historical reference snapshots to make missing classes appear by accident.

Use complete class strings in PHP: an explicit status-to-class map, not `'bg-'.$status.'-50'`. For unavoidable generated markup, declare a bounded `@source inline()` set in input.css and test it. Never blanket-safelist every color/spacing combination.

The CLI handles imports/prefixing in this pipeline. Do not copy the old PostCSS plugin configuration, obsolete `mode:'jit'`, or the old aspect-ratio/line-clamp plugins into it. If the app already uses PostCSS, integrate through **`@tailwindcss/postcss`** as a deliberate alternative instead of running two CSS pipelines. Use one generated stylesheet, not both the old snapshot and the new build.

## Preserve source appearance while changing versions

The [explicit header-gradient override](layout-standard.md#header-gradient-override) is the only intentional palette difference: `theme-vau` now uses the linked basic template’s `theme-ais` gradient values. Preserve the remaining preset and the historical snapshots; the visual check tests this gradient against the approved source value while retaining its other parity assertions.

- Custom radii and shadow names come from the retained preset. Do **not** blindly apply the stock v3→v4 `rounded-sm`/`shadow-sm` rename table; that table describes default scales. The bundled parity check confirms this preset's names retain the original computed values.
- The source `xxl` value contained `!important`; the port uses a valid `90rem` token and the same responsive utility. The source typography preset referenced nonexistent `colors.info.DEFAULT`; the port resolves it to `blue.600`.
- The variable Raleway font declares weight range `100 900`, instead of the original fixed 400 declaration.
- V4 changes order-sensitive stacked variants. The grid decorator uses `prose-tr:odd:bg-gray-50`, `prose-tr:hover:bg-green-50`, `prose-td:first:rounded-l`, and `prose-td:last:rounded-r`. Keeping v3's `odd:prose-tr:*` order can target the wrong element.
- `@apply` important utilities use trailing `!` in the v4 port. Fix `focus-visible::` typos, use `focus:outline-hidden` where preserving v3's accessible outline behavior, and use `shrink-0`/`grow-0` instead of removed aliases.
- Convert prototype opacity helpers, e.g. `bg-gray-600 bg-opacity-75` → `bg-gray-600/75`, when implementing the drawer. The exact footer snapshot is preserved verbatim; do not rewrite its information or behavior during other conversions.
- Keep explicit border colors, ring widths/colors and forced-color focus behavior. Base rules retain source border/placeholder defaults. Check plugin/preflight differences and computed geometry after building.
- V4 hover rules are conditional on hover-capable devices. Compare desktop hover and touch behavior separately.

The modern build targets browsers supported by Tailwind v4 (Safari 16.4+, Chrome 111+, Firefox 128+). If the actual target requires older browsers, use an explicitly agreed Tailwind 3.4 compatibility build with the same preset, comprehensive `content` globs and a lockfile; do not silently mix v3 directives with v4 packages.

Official references: [CLI installation](https://tailwindcss.com/docs/installation/tailwind-cli), [explicit source detection](https://tailwindcss.com/docs/detecting-classes-in-source-files), [v4 migration and browser requirements](https://tailwindcss.com/docs/upgrade-guide), [config and directives](https://tailwindcss.com/docs/functions-and-directives). The shipped build was actually compiled and checked; the old source config was inspected, not falsely claimed to have been rebuilt.
