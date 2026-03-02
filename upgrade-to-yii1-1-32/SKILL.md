---
name: upgrade-to-yii1-1-32
description: Plan and execute upgrades of legacy Yii 1.1.x apps to Yii 1.1.32 with a complete frontend/backend checklist and concrete code changes. Use when the user asks for "Upgrade to Yii1.1.32", "Yii 1.1.8 to 1.1.32", PHP 5.6 to PHP 8.x compatibility for Yii 1.1 apps, or jQuery/jQuery UI compatibility updates caused by Yii 1.1.32.
---

# Upgrade to Yii 1.1.32

## Goal

Produce a project-specific migration plan and actionable change list that covers:
- backend: Yii core compatibility, PHP compatibility, configs, runtime behavior
- frontend: jQuery/jQuery UI compatibility and extension breakages
- validation: what to test manually before rollout

## Required trigger behavior

Treat these requests as direct triggers for this skill:
- `Upgrade to Yii1.1.32`
- `Upgrade Yii 1.1.8 to 1.1.32`
- `Yii 1.1.32 migration`

## Workflow

1. Confirm target matrix and scope
- Confirm source and target: Yii `1.1.8 -> 1.1.32`, PHP `5.6 -> 8.x`, jQuery `1.6.1 -> 1.12.4`, jQuery UI `1.8.x -> 1.12.1`.
- Ask if DB upgrade (`PostgreSQL 10 -> 17`) is in the same change window or separate.

2. Run automated surface scan first
- Execute `scripts/scan_upgrade_surface.sh <repo-root>`.
- Use the results as the initial backlog of frontend/backend work.

3. Build the upgrade checklist in two sections
- `Backend changes` and `Frontend changes`.
- For each item include: file path, what changes, why it changes, and how to verify.

4. Apply high-confidence mandatory changes
- Update framework entrypoint references from old Yii path to `yii-1.1.32`.
- Replace jQuery `.live()` usages with delegated `.on()`.
- Normalize script URL overrides in `clientScript.scriptMap` (avoid accidental `//js/...` URLs; use `rtrim(dirname($_SERVER['SCRIPT_NAME']), '/')` before appending asset paths).
- Keep changes surgical; avoid broad refactors.

5. Flag medium/high-risk items that require targeted testing
- legacy 3rd-party widgets/plugins bound to old jQuery APIs
- custom jQuery UI themes relying on old class names or old widget options/events
- PHP 5-era language patterns that are incompatible with PHP 7/8

6. Execute fix-test-repeat loop
- Update old code where needed.
- Run automated tests.
- Fix failing cases with minimal patches.
- Run tests again.
- Repeat until tests pass or blocker cap is reached.

7. Verify and report
- Provide a punch list of completed edits, deferred risks, and test evidence.

## Yii-specific upgrade checks

Always review these framework-level behavior changes while upgrading old Yii 1.1.x apps:
- `CModel::createValidators()` constructor arguments changed since 1.1.11.
- `CDbMigration::safeUp()/safeDown()` transaction behavior changed since 1.1.13.
- `CHtml::activeId()` naming behavior changed since 1.1.13.
- `CGridView` URL/filter handling caveat in path-format URLs since 1.1.14.

If custom code depends on old behavior, adapt app code instead of patching framework files.

## Frontend compatibility checks

Always check these first:
- jQuery deprecated/removed APIs from old code (`.live()`, `.die()`, `.andSelf()`, `$.browser`, legacy event shortcuts on dynamic elements).
- jQuery UI widget API differences across 1.8 -> 1.12 (especially Tabs/Dialog/Datepicker/autocomplete wrappers).
- Theme/CSS drift (old classes like `ui-tabs-selected` and custom overrides targeting removed markup).
- Bundled/legacy plugins (fancybox 1.3.x, old select2 wrappers, tree widgets) for jQuery 1.12 behavior.

Mandatory dialog/overlay check:
- Verify `.ui-front` stacking exists in loaded CSS; if missing, add fallback CSS so dialogs are above overlay (example: `.ui-front { z-index: 10000 }` and `.ui-widget-overlay.ui-front { z-index: 9999 }`).
- If tree/dialog clicks fail in E2E with "overlay intercepts pointer events", treat as frontend z-index regression first, not test flakiness.

## Plugin upgrade path (Select2, Fancybox, similar)

Do not bulk-update all JS assets at once. Use a staged adapter-first approach.

1. Freeze baseline behavior
- Capture before-upgrade screenshots and short flow notes for pages using each plugin.

2. Inventory wrappers and call sites
- Identify Yii wrappers and views that use each plugin (example: `XSelect2.php`, Fancybox widget classes, inline JS event handlers).

3. Compatibility pass first (no major plugin jump yet)
- Fix app-level API removals (`.live()`, `$.browser`) and retest with current plugin assets.
- If needed, use `jquery-migrate` temporarily.

4. Upgrade one plugin at a time
- Keep wrapper public API stable; change internals/assets behind wrapper.
- Pin explicit plugin versions; never pull "latest".
- Commit assets with checksums/version notes.

5. Validate plugin-specific behavior
- Select2: open/search/select/clear/multi-select/AJAX events.
- Fancybox: open/close/image/iframe/navigation/keyboard/escape.
- Verify both admin and public flows.

6. Remove temporary shims
- Remove `jquery-migrate` and compatibility hacks only after passing plugin tests.

Output rule:
- Always include a `Plugin upgrade matrix` section listing each plugin with: current version, target version, wrapper files, risk level, and test cases.

## PHP compatibility checks

Treat Yii upgrade and PHP upgrade as coupled work.

Run compatibility scans and fix blockers before deployment:
- removed/deprecated PHP APIs from 5.x era
- stricter type/notice behavior in PHP 7/8
- fatal-on-warning edge cases in old code paths

Prefer incremental remediation with frequent syntax and smoke checks.

Mandatory PHP 8 null-safety pass:
- Scan for null-unsafe calls that were tolerated in PHP 5.6 (`trim`, `strip_tags`, similar string funcs) in models/forms/validators.
- Explicitly review Yii filter validators using `filter => 'trim'`; replace with null-safe callbacks where nullable input is possible (for example `array('XStringFilter','trim')`).
- If `convertWarningsToExceptions` is enabled in PHPUnit, treat deprecations as blockers and patch app code, not test expectations.

PostgreSQL 10 -> 17 runtime check:
- Validate DB-backed session behavior (`CDbHttpSession` or custom session class) against actual session table column types.
- If pgsql writes `\x...` payloads but session table stores text, add compatibility handling (text-safe write/read decode) before continuing E2E auth flows.
- Re-test login persistence across multiple requests after session patching.

Access-control parity check (mandatory):
- For AJAX actions used from admin pages, ensure access rules allow authenticated admin role, not only IP-based allow lists.
- Verify both direct page loads and background AJAX endpoints (`display*`, helper actions, lookup endpoints) in the same flow.

## Missing mcrypt in PHP 8 (mandatory)

When `mcrypt_*` hits are found, always produce a dedicated remediation plan with one of these paths.

1. Preferred path: switch VAU integration to protocol/security manager 2.1+
- This avoids the legacy `mcrypt` branch entirely.
- Use the maintained reference implementation in `yii2-vauid2-extension` (`VauSecurityManager.php`) where `version > 2.0` bypasses `mcrypt`.
- Include explicit config action in plan: set security manager version to `2.1` and validate full VAU login round-trip.
- For this repo, inspect and replace legacy Yii1 VAU crypto points first:
  - `protected/extensions/components/vauid/XVauSecurityManager.php`
  - `protected/extensions/behaviors/XCryptBehavior.php` (if still used for VAU-like payloads)

2. If protocol cannot be switched immediately: controlled compatibility bridge
- Use compatibility only as a temporary bridge with an expiry date.
- Acceptable short-term options:
  - `phpseclib/mcrypt_compat` shim
  - PECL `mcrypt` extension (legacy only)
- Mark this as technical debt and schedule removal in the same upgrade program.

3. For non-VAU local encrypted data: migrate, do not freeze legacy crypto
- Do not assume `mcrypt` Rijndael-256 ECB is wire-compatible with OpenSSL AES defaults.
- Build one-time migration flow:
  - decrypt old payload with compatibility bridge
  - re-encrypt with supported primitive (`openssl`/`sodium`) and authenticated envelope
  - add versioned ciphertext marker (e.g. `v1:`, `v2:`) for dual-read during rollout

4. Output requirement when mcrypt is present
- Always include a `mcrypt removal` section with:
  - exact files using `mcrypt`
  - chosen path (`protocol 2.1`, `temporary bridge`, or `data migration`)
  - cutover test cases and rollback/dual-read strategy

## Making tests runnable on PHP 8.4 (mandatory)

Use this section whenever legacy `phpunit.phar` fails under PHP 8.4.

Runner selection rule (must be explicit):
- Try legacy PHAR first from `protected/tests`.
- If PHAR fails, switch to Composer PHPUnit and continue the same loop with Composer commands.
- Always report which runner is active (`phar` or `composer`).

1. Validate current (legacy) runner commands first
- From `protected/tests`, these are correct legacy commands:
  - `php phpunit.phar --configuration phpunit.xml --testsuite Unit`
  - `php phpunit.phar --configuration phpunit.xml --testsuite Integration`

2. Detect incompatibility symptoms
- Typical blocker: fatal from old PHAR internals (example: `Cannot acquire reference to $GLOBALS`).
- If legacy PHAR fails, do not spend time patching PHAR internals.

3. Migrate test runner to a PHP 8.4-compatible PHPUnit setup
- Add Composer-managed PHPUnit compatible with PHP 8.4.
- Keep old tests but adapt compatibility points:
  - `PHPUnit_Framework_TestCase` -> `PHPUnit\Framework\TestCase` (or temporary class alias in bootstrap)
  - lifecycle signatures: `setUp(): void`, `tearDown(): void`
  - assertion renames when needed (for example string contains checks)
- Keep test suite structure (`Unit`, `Integration`) and run both after migration.

4. Ensure Playwright command is runnable from repo root
- Baseline command:
  - `cd ~/dev/php/kaardid; npx playwright test --workers=1`
- Mandatory bootstrap when missing prerequisites:
  - if `node`/`npm` is missing, install Node LTS in the environment first
  - if `package.json` is missing, create minimal Node project metadata in repo root
  - install Playwright dependency and browser binaries (`npm install`, `npx playwright install`)
  - if missing, add required config (`playwright.config.js`) before using command in CI
- Ensure app server is running and base URL is explicit for local runs:
  - start server (example): `php -S 127.0.0.1:8000 -t .`
  - run tests with base URL: `PLAYWRIGHT_BASE_URL=http://127.0.0.1:8000/index-test.php/ npx playwright test --workers=1`
- The model must perform this setup automatically when absent; do not stop at "missing dependency".

Playwright reliability guard:
- Scope interactions to active dialogs/widgets (for example query within `.ui-dialog:has(#place-dialog)`) to avoid hidden/background element matches.
- For legacy localized pages, assertions should support localized result text variants (`Leiti` / `Found`) when CSS selectors differ across views.

Command reference (this repo):
- Legacy PHAR (from `protected/tests`):
  - `php phpunit.phar --configuration phpunit.xml --testsuite Unit`
  - `php phpunit.phar --configuration phpunit.xml --testsuite Integration`
- Playwright (from repo root):
  - `cd ~/dev/php/kaardid; npx playwright test --workers=1`

## Verification and repair loop (mandatory)

When tests exist, run an iterative loop until all active stages pass. In Full Access mode, do not stop early unless a hard external blocker is reached.

1. Execute test stages
- Preflight: ensure required runtimes/tools exist; install missing ones (PHP extensions, Composer deps, Node/Playwright deps) before test execution.
- PHPUnit Unit: run with the active runner (`phar` or `composer`) using the `Unit` suite.
- PHPUnit Integration: run with the active runner (`phar` or `composer`) using the `Integration` suite.
- Playwright/E2E (from repo root):
  - `cd ~/dev/php/kaardid; npx playwright test --workers=1`
- If Playwright reports connection refused, automatically start local app server and rerun with `PLAYWRIGHT_BASE_URL` before classifying as blocker.

2. Collect and classify failures
- Group by root cause, not by symptom.
- Prioritize blockers affecting auth, data integrity, and core CRUD/search flows.

3. Apply minimal fix
- Make smallest safe patch that resolves one root cause class.
- Avoid unrelated refactors during the loop.

4. Re-run tests
- Re-run failing subset first for quick feedback.
- Then re-run full active suite (`Unit` + available `Integration` + available `Playwright`).

5. Repeat until green
- Repeat steps 2-4 until all active stages pass.
- Every 5 iterations, emit a concise checkpoint (what improved, what still fails, next root-cause target) and continue.

6. Hard-blocker stop rule
- Stop only for hard external blockers that cannot be solved in-code (for example missing secrets/certs, unavailable external service, denied permissions, missing test data controlled outside repo).
- When blocked, output exact blocker, evidence, and smallest unblocking action; otherwise continue iterating.

7. Stall guard (infinite-loop prevention)
- Track a failure fingerprint per full iteration (`suite + test + error class/message family`).
- Treat as stalled if any condition is met:
  - same fingerprint and failing count for 3 consecutive full iterations
  - A/B oscillation pattern across 4+ consecutive full iterations
  - 10 full iterations with no net reduction in failing tests
- On stall, run one diagnostic escalation pass (single-test isolation, verbose logs, and stricter root-cause split) and apply one targeted fix batch.
- If still stalled after diagnostic escalation, stop with a blocker report instead of looping indefinitely.

8. Harvest learnings every iteration
- If project has `learnings.md`, append durable entries:
  - `symptom`
  - `root cause`
  - `fix`
  - `verification`
- Keep entries concise and reusable.

9. Refactor skill from learnings only at milestones
- Do not rewrite the skill every iteration.
- Refactor the skill only after a successful cycle or when explicitly requested.

## Output contract

When using this skill, return:
- a concrete checklist split by `Backend` and `Frontend`
- exact file references for required changes
- risk-ranked testing checklist (smoke, regression, admin flows, search/forms, ajax)
- explicit go/no-go blockers
- when applicable, a dedicated `mcrypt removal` plan
- when applicable, a `Plugin upgrade matrix`
- loop status: iteration count, latest failing/passing stage, and harvested learnings summary
- active runner declaration: `phar` or `composer`, with reason for selection
- if blocked: hard-blocker evidence and exact unblocking action required
- if stalled: stall fingerprint summary, diagnostic escalation result, and next unblocking action

## References

Read `references/upgrade-sources.md` for official docs and version-specific notes.

Read `references/mcrypt-php8-vau.md` when PHP 8 upgrade scope includes VAU or any `mcrypt_*` usage.

Read `references/plugin-upgrade-path.md` when Select2/Fancybox/legacy frontend plugins are in scope.

Read `references/test-loop.md` for loop execution and learnings capture format.

## Field learnings (Kaardid, Yii 1.1.8 -> 1.1.32)

Capture these as default checks for similar legacy Yii upgrades:

1. Debug stack trace behavior changed by app error handler wiring
- Symptom: `YII_DEBUG=true` is set, but browser shows friendly error page without stack trace.
- Root cause: `errorHandler.errorAction` still points to `site/error`, which intercepts exceptions.
- Fix: in debug mode set `errorAction` to `null` (for example `(defined('YII_DEBUG') && YII_DEBUG) ? null : 'site/error'`).
- Verify: trigger a known exception and confirm native Yii debug stack trace is rendered.

2. PHP 8.1+ deprecations from null passed into string functions
- Symptom: logs contain deprecations like `mb_strlen(): Passing null ... is deprecated`.
- Root cause: legacy helpers assume nullable values are always strings.
- Fix: add null-safety and string-casting in shared helpers before calling `mb_*`/string functions.
- Verify: re-run affected page/action and confirm error log no longer records that deprecation.

3. Fancybox opens correctly in grid view but not list view
- Symptom: clicking image thumbnail in `vmode=list` navigates to image URL instead of opening modal.
- Root cause: Fancybox binding targets only one markup variant or is lost after dynamic list refresh.
- Fix: bind Fancybox via delegated handler covering both grid and list thumbnail selectors; avoid per-node inline assumptions.
- Verify: both `vmode=grid` and `vmode=list` open the same modal behavior after AJAX refresh.

4. jQuery UI dialog close button breaks after 1.12 markup changes
- Symptom: close button shows visible `Close` text, wrong border/background, or tiny/misaligned icon.
- Root cause: legacy theme CSS (1.8-era) styles no longer match 1.12 button markup.
- Fix: patch loaded jUI theme file under `css/yiithemes/*` (not global app CSS) with 1.12-compatible `.ui-dialog-titlebar-close` rules.
- Verify: close button in all dialogs has correct icon size, no visible text label, and no unwanted button chrome.

5. Remove dead PHP <5.6 bootstrap conditionals
- Symptom: obsolete entrypoint blocks for old `mbstring.internal_encoding`/`mbstring.http_input`.
- Root cause: historical compatibility code path retained after runtime moved to PHP 8.x.
- Fix: delete unreachable `<5.6` branches from entry scripts.
- Verify: app boots normally on PHP 8.x and no mbstring startup warnings appear.

6. Legacy hardcoded app path in DB-stored HTML (`/kaardid/...`)
- Symptom: images/links in CMS/help content break after moving app from subfolder to web root (or vice versa).
- Root cause: stored HTML contains environment-specific absolute paths instead of portable URLs.
- Fix: add render-time normalization that rewrites legacy base paths (for example `/kaardid`) to current `Yii::app()->baseUrl` in shared content rendering paths.
- Implementation rule: make legacy prefixes config-driven (for example `params['legacyBasePaths']`) so future path moves do not require DB rewrites.
- Verify: same DB content renders valid links when app is served both from `/` and from a subfolder path.

7. VAU `remoteUrl` missing non-default dev port
- Symptom: VAU login/logout callback URL resolves to `https://localhost/...` without required dev port.
- Root cause: callback URL built from request host defaults and does not respect external reverse-proxy/dev port setup.
- Fix: introduce a shared callback URL builder that can use configurable absolute base (for example `params['externalCallbackBaseUrl']`) and apply it consistently for VAU login and logout callback generation.
- Implementation rule: keep default fallback to Yii `createAbsoluteUrl()` when override is empty, so production behavior stays unchanged.
- Verify: with `externalCallbackBaseUrl='https://localhost:8443'`, generated VAU `remoteUrl` and logout callback include `:8443`; with empty override, URLs use normal environment host.

8. App-level subclasses of Yii core classes may be obsolete after upgrade
- Symptom: project has classes under `application/components` that extend Yii core classes (for example providers/widgets/helpers) originally created to patch old Yii behavior.
- Root cause: local shims were needed in old Yii versions but overlap with native Yii 1.1.32 features.
- Fix: audit each subclass against Yii 1.1.32 core implementation and remove/replace with native core class where behavior is equivalent.
- Implementation rule: keep only subclasses that provide app-specific behavior not available in core; migrate call sites to core class first, then delete obsolete shims.
- Verify: no remaining runtime references to removed subclass, syntax/tests pass, and affected flow (for example paging/count/sorting) behaves identically.

9. Remove custom DB session handler when PostgreSQL session schema is normalized
- Symptom: app uses custom `XDbHttpSession` shim to handle legacy `tbl_session.data` text storage.
- Root cause: Yii `CDbHttpSession` on pgsql writes `bytea`, but legacy schema stored `data` as `text`, causing incompatibility workarounds.
- Fix: migrate `tbl_session.data` to `bytea`, switch session component to native `CDbHttpSession`, then remove custom shim.
- Implementation rule: conversion SQL should preserve old rows, including `\\x...` hex-encoded payloads (`decode(...)`) and plain text payloads (`convert_to(...,'UTF8')`).
- Verify: schema reports `bytea` in both main and test DBs, login/logout session persistence works, and no runtime references to removed custom session class remain.

10. Zii translations may stop applying after framework upgrade due to key drift
- Symptom: app-local translations in `protected/messages/<lang>/zii.php` are ignored and English strings appear in widgets.
- Root cause: Yii 1.1.32 uses updated `Yii::t('zii', ...)` source strings (for example singular|plural forms and revised wording), so old keys no longer match.
- Fix: re-sync local `zii.php` keys with Yii 1.1.32 source strings while keeping existing translated values.
- Implementation rule: compare keys against framework usage (search for `Yii::t('zii', ...)`) and add missing/new keys instead of only editing values.
- Verify: translated text appears for updated keys (for example delete confirmation, list summary, total summary) and no fallback English remains in those UI paths.

11. PHP 8 breaks legacy stats aggregation when rows mix labels and numbers
- Symptom: statistics pages (for example crosstab totals) fail with `Unsupported operand types: int + string`.
- Root cause: legacy totalization loops sum all row fields, including first text label column (`Fond`/`Users`) that was loosely tolerated before.
- Fix: aggregate only numeric cells (`is_numeric`) and explicitly skip non-numeric label columns; keep row and column totals typed as integers.
- Implementation rule: when building totals for query result arrays, identify label key first and never include it in arithmetic.
- Verify: stats page renders without TypeError and totals row/column values are present and numerically correct.
