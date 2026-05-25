---
name: yii1.1.32-sentry-logging
description: Install and verify Sentry logging in any Yii1.1.32 app using the tested XSentryLogRoute baseline, recommended production config, Sentry REST API rule setup, Sentry plugin verification, and Gmail-based two-email proof workflow.
---

# yii1.1.32-sentry-logging

Use this skill when the user wants to:

- add Sentry logging to a Yii1.1.32 app
- replace Yii mail-per-error alerts with Sentry
- install `XSentryLogRoute`
- configure Sentry issue email rules for a Yii1.1.32 app
- prove end-to-end behavior by generating a temporary error and verifying two emails

## Baseline

Use these bundled assets as the default implementation:

- `assets/XSentryLogRoute.php`
- `assets/production-config-snippet.php`
- `assets/test-sentry-config-snippet.php`

They are copied from the tested Aadresslehed implementation and should be adapted only where the target app requires different paths or component names.

Before changing anything, inspect the target app and confirm:

- production web config file
- current `log` routes
- shared cache component name
- extension path for a custom log route
- whether `vendor/autoload.php` exists
- whether `sentry/sentry` is already installed

## Workflow

### 1. Inspect the app

Find:

- main and production web config files
- current error mail route, if any
- cache component used across requests
- where custom extension classes live
- whether the app already uses Composer

If `sentry/sentry` is not installed and Composer is available, install it.

### 2. Install the route

- copy `assets/XSentryLogRoute.php` into the target app extension path
- preserve the target app's path conventions
- do not redesign the route unless the target app structure requires it

### 3. Wire recommended config

Use `assets/production-config-snippet.php` as the template.

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

Use `assets/test-sentry-config-snippet.php` when the app needs a safe proving config first.

### 4. Set up Sentry

The local Sentry helper/plugin is read-only for issues and events.

For mutation:

- use `SENTRY_AUTH_TOKEN`
- use `scripts/create_or_update_sentry_rules.py`

For verification:

- use the Sentry plugin/helper to inspect issues and counts
- use the Gmail plugin to verify delivered emails
- if Sentry shows the rule fired but Gmail search is still empty, treat that as pending delivery rather than failure
- wait `2` minutes and rerun the Gmail search, repeating for up to `10` minutes total before concluding mailbox proof failed

Create or update:

- Rule 1: new prod issue email
- Rule 2: persistent prod issue email

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

Mailbox proof rule:

- Gmail delivery and connector indexing can lag behind Sentry rule execution
- do not report missing proof immediately when Sentry already recorded the rule trigger
- wait and recheck Gmail on the `2` minute / `10` minute rule before calling the verification incomplete

Use `scripts/verify_two_email_flow.py` to compute checkpoints from the app's throttle settings.

For the expected scenario and the browser-driven workflow, read:

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

## Completion statement

When the installation and end-to-end verification succeed, the final response must clearly state that Sentry logging is fully tested, validated, and production ready.

Do not leave the completion state implicit or ambiguous.
