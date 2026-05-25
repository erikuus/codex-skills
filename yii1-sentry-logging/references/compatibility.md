# Runtime compatibility

This skill has two separate app-side branches on purpose.

## Modern branch

Use the modern assets when target deployment PHP is `>= 7.2`:

- `assets/XSentryLogRoute.php`
- `assets/production-config-snippet.php`
- `assets/test-sentry-config-snippet.php`

This branch was tested directly in Yii `1.1.32` + PHP `8.4` and should be treated as the trusted baseline.

## Legacy branch

Use the legacy assets when target deployment PHP is `<= 5.6`:

- `assets/php56/XSentryLogRoute.php`
- `assets/php56/production-config-snippet.php`
- `assets/php56/test-sentry-config-snippet.php`

This branch is designed for Yii1 apps that still run on PHP `5.6` and the old official Sentry PHP SDK line.

Documented package baseline:

- `sentry/sentry` `1.11.0`

Its official package metadata requires:

- `php: ^5.3|^7.0`

and exposes the old `Raven_*` API surface.

## Why the branches must stay separate

The modern route is not PHP `5.6` safe because it depends on newer runtime and SDK concepts:

- `Throwable`
- modern `\Sentry\init`
- modern `\Sentry\captureMessage`
- modern scope/severity APIs

The legacy route avoids those and uses `Raven_Client` directly.

Do not try to make one route file polymorphic across both runtimes. Keep duplication if needed and preserve the modern proven path.

## Detection rule

Detect the **target deployment PHP version**, not just local CLI PHP.

Use this precedence:

1. `composer.json` `require.php`
2. `composer.lock` / installed package constraints
3. Dockerfile / CI / deploy config
4. local `php -v` only as a last hint

If evidence conflicts, ask the user.

If target PHP is:

- `>= 7.2`: use modern
- `<= 5.6`: use legacy
- `7.0` or `7.1`: stop and ask

## Validation limit in this workspace

This workspace has only PHP `8.4` available locally.

So:

- modern branch can be syntax-checked locally
- legacy branch can only be statically reviewed for PHP `5.6` safety here
- if a real PHP `5.6` binary becomes available later, lint the legacy route with it
