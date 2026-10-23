# Verification on PHP 8.5

## Framework smoke

Use an identified PHP 8.5 executable. Default local paths:

```sh
php -d error_reporting=-1 -d display_errors=1 /Users/erikuus/.agents/skills/upgrade-to-yii1-1-33/scripts/smoke_framework.php /Users/erikuus/dev/yii/yii-1.1.33-dev yii.php
php -d error_reporting=-1 -d display_errors=1 /Users/erikuus/.agents/skills/upgrade-to-yii1-1-33/scripts/smoke_framework.php /Users/erikuus/dev/yii/yii-1.1.33-dev yiilite.php
```

The script uses no app configuration, external services or persistent database writes. Missing SQLite is an explicit skip; other missing functionality fails. It captures even suppressed runtime warnings for this isolated probe. Treat failures as evidence, not permission to patch the shared framework. Run the application's own CLI help/bootstrap separately.

## PHPUnit and Yii's legacy test bridge

Inspect configured runner and lockfile. Check it on PHP 8.5; if an old PHAR crashes internally, select a compatible pinned Composer runner instead of patching the PHAR. Do not install an arbitrary newest major without examining the suite. PHPUnit 12 requires PHP 8.3 or newer, but that alone does not make old tests compatible. [PHPUnit installation](https://docs.phpunit.de/en/12.5/installation.html).

**The target's `yiit.php` remains legacy.** It imports `CTestCase`, `CDbTestCase` and `CWebTestCase`. `CTestCase` expects `PHPUnit_Runner_Version`, PEAR-style `PHPUnit/…` files and `PHPUnit_Framework_TestCase`; the web bridge expects old Selenium integration. A TestCase alias alone does not fix this bootstrap.

For modern PHPUnit, use a project-owned bootstrap loading Composer, defining `YII_ENABLE_ERROR_HANDLER` and `YII_ENABLE_EXCEPTION_HANDLER` as false before Yii loads, then requiring target `yii.php`. Initialize the test application explicitly. Adapt project test bases to `PHPUnit\Framework\TestCase`, preserving fixtures and application state reset. Inspect `CDbTestCase::setUp()` before migrating fixture tests. Avoid importing the legacy bridge unless a complete tested compatibility layer already exists.

Adapt lifecycle return types, assertions, data providers, mocks, metadata and XML only as required by the selected runner. Preserve behavioral coverage. Existing supported browser tooling can replace reliance on the obsolete Selenium bridge.

Discover suite/configuration names: `Unit` and `Integration` are historical examples, not guaranteed conventions. Report active runner/version and commands. Use its supported warning/deprecation settings, not obsolete XML flags.

## Application verification and rollout

- Lint app/extensions under PHP 8.5, including compile-time deprecations. Runtime handlers cannot catch all compilation messages.
- Run unit/integration tests on disposable data. Verify real PDO drivers, schema, sessions and transactions; SQLite smoke cannot prove PostgreSQL/MySQL behavior.
- Use existing E2E configuration. Scope selectors to active widgets, preserve localization, and inspect overlay interception before calling it flakiness.
- Verify FPM and CLI/cron versions, extensions, configuration, asset URLs and logs. Avoid publishing phpinfo endpoints.
- Exercise sanitization with safe/unsafe fixtures. Do not relax HTMLPurifier rules to pass output comparisons.
- Prepare rollback of app and framework/runtime together. For data changes document reversibility or restore paths. Test 8.4 separately if supported.

Track stage/test/error family and failing counts. Fix one cause, rerun relevant tests and then affected full suites. Stop for demonstrated external prerequisites or the skill's stall limit, reporting exact evidence and the smallest unblocking action. Missing tests/services are unverified, never passing.
