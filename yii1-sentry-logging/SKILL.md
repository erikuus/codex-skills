---
name: yii1-sentry-logging
description: Install and verify Sentry logging in any Yii1 app using a frozen modern XSentryLogRoute baseline for PHP 7.2+ and a separate legacy PHP 5.6 branch, with Sentry REST API rule setup, Sentry plugin verification, and Gmail-based two-email proof workflow.
---

# Yii1 Sentry Logging

Use this skill when the user wants to:

- add Sentry logging to a Yii1 app
- replace Yii mail-per-error alerts with Sentry
- install `XSentryLogRoute`
- configure Sentry issue email rules for a Yii1 app
- prove end-to-end behavior by generating a temporary error and verifying two emails

## Runtime branch first

Before choosing an asset, detect the **target deployment PHP version**, not just the local CLI version.

Use this precedence:

1. `composer.json` `require.php`
2. `composer.lock` or installed package constraints
3. Dockerfile, CI, or deploy config
4. local `php -v` only as a last hint

If evidence conflicts, ask the user. If the target runtime is ambiguous, do not guess.

Choose the branch like this:

- PHP `>= 7.2`: use the **modern branch**
- PHP `<= 5.6`: use the **legacy branch**
- PHP `7.0` or `7.1`: stop and ask

Read `references/compatibility.md` before choosing a branch.

## Baseline assets

### Modern branch

Use these bundled assets as the default implementation for modern Yii1 deployments:

- `assets/XSentryLogRoute.php`
- `assets/production-config-snippet.php`
- `assets/test-sentry-config-snippet.php`

This modern branch was proved in Yii `1.1.32` + PHP `8.4` and should be treated as a frozen baseline. Do not redesign it casually.

### Legacy branch

Use these separate assets for PHP `5.6` style deployments:

- `assets/php56/XSentryLogRoute.php`
- `assets/php56/production-config-snippet.php`
- `assets/php56/test-sentry-config-snippet.php`

The legacy branch keeps the same throttling and issue/event behavior, but uses the old official `Raven_Client` SDK line instead of the modern `\Sentry\...` API surface.

## Workflow

Rerun policy:

- treat the Sentry project, environments, and alert rules as shared infrastructure
- when they already exist, reuse them and do not create duplicates
- use `test-sentry` only as a temporary proving environment when needed
- after proving, the final rule names/environment for the app should remain `new prod issue` and `persistent prod issue`
- when rerunning against the same app on another Yii/PHP branch, change the app integration as needed but keep the same Sentry project and `prod` rules unless the user explicitly asks otherwise

### 1. Inspect the app

Before changing anything, confirm:

- production web config file
- current `log` routes
- shared cache component name
- extension path for a custom log route
- whether Composer/autoload exists
- whether `sentry/sentry` is already installed
- target deployment PHP version using the branch rules above

If `sentry/sentry` is missing and Composer is available:

- modern PHP `>= 7.2`: install the modern `sentry/sentry` line that fits the target app
- legacy PHP `<= 5.6`: install `sentry/sentry` `1.11.0`

If the installed Sentry package line conflicts with the runtime branch, stop and ask before changing it.

### 2. Install the correct route

- modern PHP `>= 7.2`: copy the modern `assets/*` route into the target extension path
- legacy PHP `<= 5.6`: copy the `assets/php56/*` route into the target extension path

Preserve the target app's path conventions. Do not mix modern and legacy code in one route file.

### 3. Wire recommended config

Use the branch-matched production snippet as the template.

Default production settings:

- `environment=prod`
- `release=<app>-prod`
- `sendDefaultPii=false`
- `includeUserContext=false`
- `includeRequestContext=true`
- `throttleWindowSeconds=900`
- `throttleMaxInitialEvents=1`
- `summaryThreshold=25`

Require a shared cache component. Default assumption is `cache`.

Replace direct per-error production mail routes with `XSentryLogRoute`.

Use the branch-matched test snippet when the app needs a safe proving config first.

### 4. Set up Sentry

The local Sentry helper/plugin is read-only for issues and events.

For mutation:

- use `SENTRY_AUTH_TOKEN`
- use `scripts/create_or_update_sentry_rules.py`

For verification:

- use the Sentry plugin/helper to inspect issues and counts
- use the Gmail plugin to verify delivered emails

Create or update:

- Rule 1: `Notify {email}: new prod issue`
- Rule 2: `Notify {email}: persistent prod issue`

These Sentry-side rules stay the same for both runtime branches.

On reruns:

- first look for existing `prod` Rule 1 / Rule 2 and update them in place if needed
- only create rules when they do not already exist for the target app
- do not leave temporary `test-sentry` rules behind after verification unless the user explicitly wants them kept

If Sentry rejects an environment-scoped rule because the environment does not exist yet, seed one event in that environment first, then rerun rule creation.

For exact payloads and caveats, read `references/sentry-api-payloads.md`.

### 5. Run end-to-end verification

Use a temporary env-gated probe if the natural failure path does not already produce an `error`-level `500`.

Probe rules:

- stable marker in exception text
- deterministic grouping
- easy Gmail and Sentry search
- remove after verification

Use the browser to hit the failing path until:

- first email is observed
- summary event is observed
- second email is observed

Use `scripts/verify_two_email_flow.py` to compute checkpoints from the app's throttle settings.

For the expected scenario and browser-driven workflow, read:

- `references/scenario.md`
- `references/test-workflow.md`

## Generic defaults

When the user does not provide project-specific values, default to:

- project slug = repo or app name
- maintainer email = ask only if not discoverable
- environment names = `prod`, `test-sentry`, `local`
- cache component = `cache`
- release = `<app>-prod`

## Important verification rule

Only the first event creates the Sentry issue in the feed.

Later events stay on that same issue and only increase its event count.

Rule 2 must be verified against issue event count, not against “new issue count”.
