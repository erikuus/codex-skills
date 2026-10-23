# Yii 1.1.32 versus the local 1.1.33-dev snapshot

Investigated 2026-10-23 by comparing `/Users/erikuus/dev/yii/yii-1.1.32/` and `/Users/erikuus/dev/yii/yii-1.1.33-dev/`, including source hunks, bundled assets and version constants. This describes these local trees; it does not certify the older tree is an untouched upstream release.

## Provenance

Target `INSTALL-SOURCE.txt` records upstream `yiisoft/yii`, commit `ecfb82af5acdb59a5de9823661eacf512e433a30` (2026-10-15), installed 2026-10-22. Its README declares support through PHP 8.5; `YiiBase::getVersion()` returns `1.1.33-dev`. Recheck local evidence if the installation changes.

`YiiBase.php` SHA-256 at investigation:

- 1.1.32: `ba946301a964e7188419290f407fc3658b3ae11068b9010a7494864c46e5b458`
- target: `4ec7bf1c47b1c93a4c0c9352fab65ca2352aa78cdde37fd01f9c97673b429cf3`

These identify individual files, not whole-tree integrity. Pin the full upstream commit/archive in deployment records.

## Verified changes and consequences

| Area | Difference in target | Application checks |
| --- | --- | --- |
| `web/CHttpSession.php`, `yiilite.php` | Removes the relative `require_once` of `CHttpSessionHandler.php`, relying on Yii autoloading. Fixes loading from the flattened yiilite location. | Test custom/DB sessions under the actual bootstrap and multi-request authentication. The object-style PHP 8.4 handler was already introduced in 1.1.32. |
| `db/ar/CActiveFinder.php` | String-casts scalar primary keys used to index related records in lazy loading and `findWith`. | Exercise unsaved/null-key records, persisted IDs and custom relations. Do not cast all app array keys indiscriminately. |
| `web/auth/CPhpAuthManager.php` | String-casts user IDs used as assignment keys in lookup, assignment and revocation. | Verify guest/null-ID, numeric/string-ID and default-role access. This is the file-based manager, not `CDbAuthManager`. |
| Schema/helpers/request parsing | Canonical casts replace `(integer)`, `(boolean)`, `(double)` in `CDbColumnSchema`, `CPropertyValue`, `CTimestamp`, `CTypeValidator`, `CJSON`, `CHttpRequest` and matching yiilite code. | Check DB coercion, validators, JSON, Accept headers and copied app implementations. |
| `vendors/Net_IDNA2/Net/IDNA2.php` | `(binary)` becomes `(string)` in byte-length fallback. | Retest internationalized domains if used. |
| `web/widgets/captcha/CCaptchaAction.php` | Removes `imagedestroy()` after PNG output. | Request CAPTCHA through HTTP with GD; verify response and logs. Audit app image wrappers separately. |
| `gii/components/Pear/Text/Diff.php` | `trigger_error(..., E_USER_ERROR)` becomes thrown `Exception`. | Test Gii preview/diff if used. This addresses PHP 8.4, not a new 8.5 deprecation. |
| HTMLPurifier | Bundled 4.15.0 becomes 4.19.1, including standalone code and schema. Target changelog notes PHP 5.6 minimum for this dependency. | Test allowed rich text and rejected unsafe content, custom definitions, iframe rules and generated caches. Preserve sanitization policy. |
| Integer predicates | `is_integer()` becomes `is_int()` in CMap, CActiveRecord, CDbCriteria, CJavaScript, CListView and yiilite equivalents. | Changelog labels this preparation for PHP **8.6**. Do not misreport `is_integer()` as an 8.5 deprecation. |

There are 54 JS/CSS files in each tree, with matching paths and bytes. jQuery remains 1.12.4; jQuery UI remains 1.12.1. No Zii translation or CHtml markup changes appear in this local delta. Older-source cumulative changes still apply.

The target's `UPGRADE` section for 1.1.32 lists no significant changes. That does not replace application-level PHP 8.5 testing. Framework PHP compatibility also does not modernize `test/CTestCase.php`, `CDbTestCase.php`, `CWebTestCase.php` or `yiit.php` and their old PHPUnit integration.

Intervening HTMLPurifier releases include PHP 8.4/8.5 and null-handling fixes, CSS/iframe support and filtering changes. Compare representative sanitized output, not just whether the class loads. [HTMLPurifier 4.19.1 release history](https://raw.githubusercontent.com/ezyang/htmlpurifier/v4.19.1/NEWS).

## Sources and repeatable comparison

Primary evidence: local target `INSTALL-SOURCE.txt`, `CHANGELOG`, `UPGRADE`, `UPSTREAM-README.md`, and source diff. The upstream raw changelog URL was unavailable during investigation; local files supplied the version-specific evidence.

- [Pinned upstream tree](https://github.com/yiisoft/yii/tree/ecfb82af5acdb59a5de9823661eacf512e433a30)
- [1.1.32 upstream changelog](https://github.com/yiisoft/yii/blob/1.1.32/CHANGELOG)
- [Pinned cumulative upgrade notes](https://github.com/yiisoft/yii/blob/ecfb82af5acdb59a5de9823661eacf512e433a30/UPGRADE)

Use `diff -qr <old-framework> <target-framework>` for inventory (exit 1 means differences), then inspect relevant `diff -u` hunks. For ignored installations use `rg --no-ignore` with deliberate scope. Compare complete vendor directories; avoid transplanting isolated vendor fixes.

## Verification performed when creating this skill

On 2026-10-23, the supplied smoke script passed under local PHP 8.5.12 with both `yii.php` and `yiilite.php`: bootstrap, collections/schema/encoding, null and numeric RBAC assignment keys, custom-session round-trip, HTMLPurifier allowed/unsafe HTML, and SQLite CRUD. No checks were skipped. PHP 8.4 and application-specific flows were not executed during skill creation.

The scanner was exercised against temporary fixtures covering ignored PHP files, paths with spaces, dependency/cache exclusions, vendor opt-in, plugin assets, empty trees and invalid arguments. Skill validation and local reference-link checks passed.
