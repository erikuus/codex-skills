# Separate themes selected at application level

## Required behavior

Preserve the existing design as `default` and implement the new design as `joyful`. Use those names unless the app already has suitable theme identifiers. The skill name is not a required runtime identifier. All design rules and packaged visual assets apply to Joyful only: the default keeps its original header/footer, menus, styles and behavior.

Select the active theme once through trusted application configuration, shared by every web entry point. For example, in an app's existing PHP configuration array:

```php
// Application-wide setting; use 'default' to restore the original design.
$config['theme'] = 'joyful';
```

This is a configuration example, not a standalone bootstrap. Adapt it to the target's configuration format. An unset setting uses `default`, preserving existing deployments; an invalid configured value must produce a clear configuration error rather than form a file path. To deliver the new design, set the intended application's configuration to `joyful` using its existing configuration conventions, while documenting the one-setting rollback. Do not change unrelated configuration or deployed environments unless authorized.

No user preferences, account fields, sessions, cookies, query parameters, request headers, browser storage or UI theme picker. No controller/action/URL allowlist, route-based choice or automatic fallback that selects another theme for a page. Public and admin bootstrap files, AJAX endpoints and dialog/iframe requests read the same application setting. Existing authentication and language choices remain independent of it.

## Template and asset ownership

Reuse an existing configuration-driven theme facility if present. Otherwise implement only the small centralized selector the app needs: an allowlisted theme value and a fixed mapping to view roots and asset URLs. Do not add a theme framework, a plugin registry or business-logic forks.

An illustrative layout for a plain PHP app is:

```text
frontend/views/                    existing default views, preserved
admin/views/                       existing default admin views, preserved
themes/joyful/views/frontend/       Joyful public layouts/views/partials
themes/joyful/views/admin/          Joyful admin layouts/views/partials
public/assets/joyful/               Joyful CSS, fonts, images, JS and build inputs
```

These paths are examples: adapt them to actual document roots and include conventions. Default views need not be moved into a new directory. Keep default asset URLs/files and their build outputs intact. Render controllers, queries, validation, permissions and editor logic through their existing shared owners; duplicate presentation only where the markup differs. Avoid copying controller code into a theme view or scattering theme tests through each page.

Route logical view names through the selected view root and render the same data contracts in either theme. Every changed presentation fragment must resolve consistently: a Joyful body must not accidentally hardcode default header/footer/partial includes. Audit includes inside views as well as entry-point includes. Use the app's established helpers where possible and preserve the variable scope required by plain PHP includes. Do not run a header renderer twice.

A shared fragment may be reused explicitly when its markup and assets are compatible with both themes. Do not silently fall back to a default full page or incompatible legacy fragment when a Joyful view is missing. Supply its Joyful presentation or report the missing template clearly; incomplete coverage is not a reason to switch themes by route.

Load only the selected theme's layout CSS and theme-specific JS. Keep genuinely shared plugin/editor assets shared, preserving their behavior. Tailwind preflight, fonts, the exact reference footer and drawer initialization must not leak into default pages. The Joyful build must never overwrite the default stylesheet or alter the default build's output. If the app already has a build system, add a separate Joyful output/entry rather than replacing its default entry.

Print, exports, email and data-only responses retain their existing document contracts; choosing a response layout is not permission to select a different theme. A JSON response needs no visual shell; a Joyful dialog fragment must use Joyful-compatible markup without a full page wrapper. Full-document iframes resolve the same application theme and load appropriate assets once.

## Verification and handoff

Capture the default design before editing. Test the same representative URLs with `default`, then `joyful`, then `default` again by changing application configuration only. Verify public/admin views, nested partials, AJAX updates, dialogs and editors under both values. Compare the restored default with its original screenshots and interactions. Check actual CSS/JS requests, not only classes in markup.

Where rendered-page/fragment caches exist, include the active theme in cache identity or invalidate them when the setting changes. Preserve existing tenant/language/auth cache boundaries. Document any configuration cache/restart step needed for the app's normal deployment model; switching must not require template/controller edits, asset replacement or rebuilding default CSS.

Verify there is no request/user/route override and no missing-view theme fallback. Report the exact setting, allowed values, selected value, affected view roots, build command and switch-back procedure. Do not claim complete theming from a homepage alone. See [verification](verification.md) for the full acceptance checks.
