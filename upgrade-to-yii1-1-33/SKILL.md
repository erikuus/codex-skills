---
name: upgrade-to-yii1-1-33
description: Plan and execute Yii 1.1 application upgrades to the pinned local yii-1.1.33-dev framework on PHP 8.5. Use for Yii 1.1.32 to 1.1.33-dev migrations, older Yii 1 applications moving to this target, and PHP 8.4/8.5 compatibility work coupled to that upgrade. Keep explicit Yii 1.1.32 targets with the separate 1.1.32 skill.
---

# Upgrade to Yii 1.1.33 on PHP 8.5

Upgrade the application to `/Users/erikuus/dev/yii/yii-1.1.33-dev/`, preserving its behavior and making its tests runnable on PHP 8.5. This is a separate successor to `upgrade-to-yii1-1-32`; its older-app and frontend lessons are retained conditionally in [legacy-upgrades.md](references/legacy-upgrades.md).

## Target and scope

- Default target: Yii `1.1.33-dev`, upstream commit `ecfb82af5acdb59a5de9823661eacf512e433a30`, recorded in local `INSTALL-SOURCE.txt`. It is an **unreleased development snapshot**, not a stable 1.1.33 release. Recheck installed provenance before each migration; never silently substitute moving `master` or another release.
- The directory contains framework files directly: bootstrap is `yii-1.1.33-dev/yii.php`, **not** `yii-1.1.33-dev/framework/yii.php`.
- Infer source Yii/PHP versions, dependencies, deployment paths and database from the project. Do not assume every application starts on Yii 1.1.8/PHP 5.6 or requires a PostgreSQL major upgrade.
- For a planning request, produce the plan. For an implementation request, apply and verify the changes. Database upgrades, plugin major upgrades and deployment are separate scope decisions unless requested or necessary to resolve an observed compatibility failure.

## Inspect and establish evidence

1. Read [yii-version-diff.md](references/yii-version-diff.md) and the target's `INSTALL-SOURCE.txt`, `CHANGELOG`, and cumulative `UPGRADE`. Compare app-specific framework patches and subclasses with the target before replacing them.
2. Find every web, test, CLI, cron and worker bootstrap, including `yiilite.php`, `yiit.php`, environment overrides and deployment configuration. Record the actually loaded Yii path/version, not just directory names.
3. Identify the PHP 8.5 executable explicitly. Record `php -v`, `php --ini`, required extensions and PDO drivers; inspect web/FPM separately. A CLI upgrade does not change FPM or scheduled jobs. Check Composer's real platform requirements without bypass flags; an emulated `config.platform.php` is not runtime evidence.
4. Run `bash <skill-dir>/scripts/scan_upgrade_surface.sh <app-root>`. This read-only heuristic report is a backlog, not a compatibility certification. It excludes Composer dependencies by default; repeat with `--include-vendor` when needed. Inspect external/symlinked extensions separately.
5. Capture existing test results and representative UI flows when the old runtime is available. Mark unavailable baselines explicitly and distinguish inherited failures from upgrade regressions.

## Apply the migration

### Framework and PHP

- Update all active bootstrap/config references coherently. Keep deployment path conventions; map the pinned framework into production/container paths rather than embedding the developer's macOS path everywhere. Keep a recoverable reference to the previous framework/runtime pair.
- Audit app and extension code against [php84-85.md](references/php84-85.md). Apply both versions' checks if the source predates 8.4; if already on 8.4, verify existing fixes and concentrate on the 8.5 delta. For earlier PHP versions, also use the cumulative guides in the legacy reference.
- Fix semantic causes: preserve nullability, missing-key behavior, validation, CSV dialects, authorization outcomes and persisted formats. Do not suppress warnings to get green tests, blindly cast all keys, or rewrite strings containing `integer`/`boolean`.
- Do not patch the shared framework installation during an app migration. Prefer application fixes, compatible dependency releases and narrow app-level adapters. For a remaining core defect, document a reproducible case and versioned patch proposal instead of changing every app sharing the directory.
- Remove obsolete subclasses only after call sites and regression coverage establish equivalence with core.
- Refresh only the application's generated framework assets/caches through its existing mechanism. Preserve uploads and persistent data; do not recursively erase an ambiguous `assets` or `runtime` directory.

### Frontend and older applications

The inspected 1.1.32 and target have identical JS/CSS assets: jQuery 1.12.4 and jQuery UI 1.12.1. A 1.1.32 migration still needs frontend smoke tests but does not itself require a JS version jump.

For older sources, changed asset overrides, legacy widgets, mcrypt/VAU, PostgreSQL sessions, or prior Kaardid-style customizations, read [legacy-upgrades.md](references/legacy-upgrades.md). Preserve the original skill's backend/frontend coverage without making historical project fixes universal mandatory edits.

## Verify and repair

Read [verification.md](references/verification.md) before adapting test runners or declaring readiness.

1. Run the supplied framework smoke script with the actual PHP 8.5 binary and target directory; run `yii.php` and `yiilite.php` in separate processes. It checks bootstrap, collections, schema conversion, RBAC assignment keys, custom sessions, HTMLPurifier and optional SQLite. It does not test the application or a real database server.
2. Lint app PHP on PHP 8.5 with `error_reporting=-1`, then run unit and integration suites. Resolve old PHPUnit/bootstrap compatibility as described in the reference; the target still contains legacy Yii test classes.
3. Run existing browser tests with the actual project root/base URL and disposable test data. Start the intended local server if needed. Supply missing project-local dependencies within scope; do not reuse the old skill's `~/dev/php/kaardid` path for another app.
4. Exercise login/logout and session persistence over multiple requests, guest/admin access and AJAX authorization, CRUD/search/filter/sort/pagination, nullable inputs, uploads/CAPTCHA, CSV, sanitized HTML, translations and console/cron paths as applicable. Inspect PHP/FPM/Yii logs and browser errors with deprecations visible in tests and logs.
5. Group failures by root cause, patch minimally, rerun the affected subset, then active full suites. Track failure fingerprints. After three unchanged full iterations or four oscillating iterations, perform one focused diagnostic pass; if still stalled, report evidence and the missing prerequisite. Do not repeat passing checks without a new change or unresolved risk.

If PHP 8.4 remains in the supported rollback/runtime matrix, also test the new app/framework pair on 8.4. Otherwise do not claim 8.4 compatibility from an 8.5 run. Do not deploy automatically from a request to prepare an upgrade.

## Deliverable

Return a concise migration report with:

- source/target Yii and PHP versions, pinned provenance, actual runtime/bootstrap paths;
- backend and frontend changes with file references and verification evidence;
- active test runner/version, commands/results, skipped checks and unresolved deprecations;
- plugin version/wrapper/test matrix when plugins change; mcrypt/ciphertext cutover and rollback plan when applicable;
- remaining go/no-go blockers and rollback steps, distinguishing framework smoke success from application readiness.

Append durable symptom/cause/fix/verification notes to an existing project learnings file when useful. Updating this skill itself is separate work unless requested.
