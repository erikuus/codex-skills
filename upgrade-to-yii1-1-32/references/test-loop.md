# Iterative test-fix loop

Use this when the repository has automated tests.

## Active stages

1. Unit (mandatory if present)
2. Integration (when available)
3. Playwright/E2E (when available)

## Baseline commands

Legacy PHPUnit runner commands are correct when executed from `protected/tests`:

- `php phpunit.phar --configuration phpunit.xml --testsuite Unit`
- `php phpunit.phar --configuration phpunit.xml --testsuite Integration`

Playwright baseline command from repo root:

- `cd ~/dev/php/kaardid; npx playwright test --workers=1`

## Preflight prerequisite bootstrap

Before running any stage, the model must verify required tools are installed and bootstrap missing ones automatically:

- PHP test runner dependencies for the chosen runner (`phar` or `composer`)
- Node.js + npm for Playwright stage
- Playwright package and browser binaries (`npm install`, `npx playwright install`)
- Missing test config files required by the repo (for example `playwright.config.js`)

Do not stop at reporting missing prerequisites; install or scaffold them, then continue the loop.

## Runner selection rule

1. Try legacy PHAR first from `protected/tests`.
2. If PHAR fails on PHP 8.4, switch to Composer-managed PHPUnit and continue the loop.
3. Always report which runner is active (`phar` or `composer`).

## PHP 8.4 compatibility rule

If legacy `phpunit.phar` fails on PHP 8.4 (for example fatal errors from old PHAR internals), migrate to a Composer-managed PHPUnit compatible with PHP 8.4 and adapt old tests as needed:

- class namespace migration (`PHPUnit_Framework_TestCase` to `PHPUnit\\Framework\\TestCase` or temporary alias)
- lifecycle method signatures (`setUp(): void`, `tearDown(): void`)
- assertion updates where modern PHPUnit behavior differs

Do not patch old PHAR internals.

## Loop template

1. Run stage(s).
2. Parse failures.
3. Group by root cause.
4. Apply minimal patch.
5. Re-run failing subset.
6. Re-run full active stages.
7. Record durable learning.
8. Repeat until all active stages pass.

## Blocker rule

Do not stop based on iteration count alone.

- Continue iterating until all active stages pass.
- Every 5 iterations, emit a checkpoint summary and continue.
- Stop only for hard external blockers that cannot be fixed in-code (missing secrets/certs, unavailable external systems, denied permissions, or absent externally managed test data).
- When blocked, output evidence and the smallest concrete unblocking action.

## Stall guard (infinite-loop prevention)

Track a failure fingerprint per full iteration (`suite + test + error class/message family`).

Treat as stalled if any condition is met:
- same fingerprint and failing count for 3 consecutive full iterations
- A/B oscillation pattern across 4+ consecutive full iterations
- 10 full iterations with no net reduction in failing tests

When stalled:
1. Run one diagnostic escalation pass (single-test isolation, verbose logs, stricter root-cause split).
2. Apply one targeted fix batch.
3. Re-run full stages.
4. If still stalled, stop with blocker output (do not loop forever).

## Learnings.md entry format

Use one compact block per resolved root cause:

```markdown
## YYYY-MM-DD - <short title>
- Symptom: ...
- Root cause: ...
- Fix: ...
- Verification: <command and result>
```

Keep only durable patterns.
