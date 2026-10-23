# Conditional checks inherited from the 1.1.32 skill

Read for sources below Yii 1.1.32/PHP 8.4 or when these integrations occur. These are investigation cues, not instructions to reproduce every historical Kaardid patch.

## Cumulative Yii and PHP changes

Read the target's full `UPGRADE` between the actual source and target. For old Yii sources inspect validator construction (1.1.11), migration transactions and active input IDs (1.1.13), path-format grid filtering (1.1.14), and jQuery UI updates (1.1.24). Audit custom overrides and serialized/cached data affected by intervening releases.

For PHP 5/7 sources audit removed `mysql_*`, `each`, `create_function`, `ereg/split`, mcrypt, old constructors, curly-brace offsets, old callbacks and incompatible signatures. Include PHP 8 type errors, undefined keys, numeric/string arithmetic, null passed to internal functions, dynamic properties and interface return types. Read relevant guides including their deprecations:

- [PHP 7.0](https://www.php.net/manual/en/migration70.php), [7.1](https://www.php.net/manual/en/migration71.php), [7.2](https://www.php.net/manual/en/migration72.php), [7.3](https://www.php.net/manual/en/migration73.php), [7.4](https://www.php.net/manual/en/migration74.php)
- [PHP 8.0](https://www.php.net/manual/en/migration80.php), [8.1](https://www.php.net/manual/en/migration81.php), [8.2](https://www.php.net/manual/en/migration82.php), [8.3](https://www.php.net/manual/en/migration83.php)

## Frontend migration

Inventory loaded assets, `clientScript.scriptMap`, wrappers and CDN overrides. Do not infer effective versions from Yii alone.

- For old jQuery, replace `.live()`/`.die()` with delegated `.on()`/`.off()` using a stable ancestor and equivalent event semantics. Inspect `$.browser` and plugin dependencies. `.bind()`, `.andSelf()` and `.size()` are review cues, not all removed in jQuery 1.12.4.
- Test Tabs/Dialog/Datepicker/autocomplete and themes across jQuery UI 1.8–1.12. Inspect `.ui-front`, overlays and titlebar close markup before adjusting scoped CSS; avoid universal z-index patches without a reproduced problem.
- Inspect radio/checkbox-list wrappers and broad descendant label selectors. Narrow CSS first. A helper splitting generated markup may need local `'container' => ''`; avoid global framework overrides.
- Normalize script URLs when subfolder deployment produces accidental `//js/...` paths. Test root and subfolder layouts when both are supported.
- Test grid/list AJAX refresh and plugin rebinding, especially Fancybox links in both layouts.

For plugins: capture baseline behavior, inventory wrappers/call sites, fix compatibility first, then upgrade one pinned plugin at a time as needed. Preserve wrapper APIs. Temporary jquery-migrate is diagnostic support with an explicit removal plan.

| Plugin | Behavioral checks when present |
| --- | --- |
| Select2 | Open/search/select/clear, keyboard, multiselect, AJAX and dependent fields |
| Fancybox | Image/iframe open/close, navigation/ESC, overlay, focus/scroll, AJAX rebinding |
| Tree/dialog/editor | Clickability, stacking, initialization after refresh, stored-content round-trip |

Sources: [jQuery 1.9](https://jquery.com/upgrade-guide/1.9/), [jQuery UI 1.9](https://jqueryui.com/upgrade-guide/1.9/), [1.10](https://jqueryui.com/upgrade-guide/1.10/), [1.11](https://jqueryui.com/upgrade-guide/1.11/), [1.12](https://jqueryui.com/upgrade-guide/1.12/).

## mcrypt and VAU

Inventory actual call sites, protocols and persisted ciphertext. Framework compatibility does not restore bundled mcrypt.

For VAU inspect the installed integration and `/Users/erikuus/dev/yii/yii2-vauid2-extension/VauSecurityManager.php` plus its README. The older skill identifies protocol/security-manager 2.1 as a path avoiding legacy mcrypt. Verify the actual peer and payload format; do not copy a Yii2 class into Yii1 unchanged or switch protocol configuration without end-to-end evidence.

For persisted data use a versioned envelope and tested dual-read migration when needed. Rijndael-256 ECB is not interchangeable with OpenSSL AES defaults. For a temporary bridge verify PHP 8.5 support and known ciphertext vectors, define retirement conditions, and preserve recoverability before rewriting data. Protocol upgrades and stored-data migrations are distinct tasks.

Report exact files, chosen protocol/bridge/data-migration approach, callback tests, old-data round-trip and rollback. Check callback scheme/host/port behind proxies, preserving defaults unless a configured external base is needed.

## Database/session and application parity

- PostgreSQL sessions: inspect the real `CDbHttpSession` table and driver. Text/bytea and mixed plain/hex payloads need evidence-based conversion. Do not prescribe a database major upgrade or blanket SQL. Test reversible migrations on copies first.
- Authorization: compare intended access for pages and admin AJAX; do not widen roles merely to pass tests.
- Error rendering: inspect `errorHandler.errorAction` when local debug traces disappear; preserve production error behavior.
- Stats: exclude label columns and define numeric aggregation; avoid indiscriminate casts hiding bad values.
- Zii translations: compare source keys with local translations when English fallback appears.
- Stored HTML: investigate hardcoded base paths in rendering/editors when root/subfolder deployment changes; do not rewrite the DB merely because a prefix appears.
- Remove obsolete bootstrap branches/subclasses only after proving they no longer provide required behavior.
