# Verification

## Disposable baseline checks

Copy this skill to a disposable work area before installing dependencies or generating CSS. From that copy:

```sh
npm ci --prefix assets/starter/tailwind
npm run build --prefix assets/starter/tailwind -- --source "$PWD/assets/html" --source "$PWD/assets/starter/js"
node scripts/render-preview.mjs
node scripts/verify-assets.mjs
PLAYWRIGHT_MODULE=/absolute/path/to/playwright CHROME_PATH=/absolute/path/to/chrome node scripts/verify-browser.cjs
```

`verify-assets.mjs` checks the retained source-asset hashes, exact footer subtree, and absence of unresolved assembly markers/PHP in the rendered specimen. `verify-browser.cjs` compares shell/table/detail/icon/typography values with the historical reference at 390/768/1024/1440/1600px, checking the approved gradient against the reference's `bg-theme-ais` value rather than restoring the old green gradient. It checks footer feedback interception (no real popup), drawer keyboard/close/resize behavior, mobile detail labels, title/detail/form bounds, compact controls and secondary hover.

The source has intentional differences documented by the skill: approved gradient, accessible mobile detail labels, functional drawer behavior, and no Home menu entry. Do not remove assertions or rebaseline visual mismatches without a source-based explanation. Specimen tests are not application acceptance.

Test the builder with an external template directory and an individual rendering file. A class used only there must be emitted after rebuilding; missing sources should fail, and generated file paths must remain local/ignored. Confirm unrelated vendor/cache/content files are not accidentally scanned. Check the lockfile, CSS/font/image URLs, duplicate runtime registration and console errors.

## Actual application acceptance

Capture source and target at matched viewport sizes and inspect them. Verify:

- White/gradient surface nesting, 48px/128px headers, responsive container sizes, local fonts, custom shadows/radii and approved gradient. Exact footer content/links/artwork/feedback behavior; no app-specific footer replacement.
- Actual target branding, authorized desktop/mobile links with no Home/Avaleht menu item, working logo home link, breadcrumb home icon, useful language/auth controls and existing bookmark/helpdesk integration. Test guest and permitted/restricted roles.
- Mobile navigation opens, closes by button/outside/Escape/link, restores scrolling/focus, survives desktop resize and remains available without JavaScript. No other dialogs are accidentally rebound.
- Tables retain values, numeric formatting, sort/query state, filters, pagers/counts, empty states, actions, selection and AJAX IDs. Only the table region scrolls when needed; controls keep their accessible names and preserved operation semantics.
- Detail title/actions/content share the narrow column; readable label/value gaps, no group separators, visible labels on phones, no overflow with long values/URLs. Wider viewers and metadata panels retain sensible independent widths.
- Form title/actions/body/summary share their column, group inset occurs only at 1280px+, compact ranges/units remain together, field-help links work, radio dynamic behavior and submitted values are unchanged. Required/readonly/disabled and error states remain clear.
- Existing dialogs retain correct close elements, focus and dismissal behavior; HTML fragments do not acquire duplicate layouts/scripts. Keep the actual plugin structural CSS and verify popup sizes on phones.
- Existing editors still initialize, synchronize, retain validation input and save unchanged content contracts; no new editor engine is introduced.
- Optional text collapse has explicit approval and line count. Verify both states, localized button labels, short content, resize/fonts, keyboard/touch and full text in print/without JS. Full text remains default when not approved.
- Print/export/iframe/email response contracts remain appropriate, without an accidental interactive shell.

Run the target's relevant tests and syntax/lint/build checks. Document service-dependent tests you could not run; do not label the whole migration verified from a static specimen or a single homepage screenshot. Creating this skill does not claim that Nimeregister has been themed or tested live.
