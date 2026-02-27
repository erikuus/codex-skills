# mcrypt on PHP 8: VAU-focused handling

## Why this matters

`mcrypt` was deprecated in PHP 7.1 and removed from core in PHP 7.2+. Any remaining `mcrypt_*` calls break on PHP 8.

## Known project hotspots

- Yii1 VAU component:
  - `protected/extensions/components/vauid/XVauSecurityManager.php`
- Generic legacy crypto behavior:
  - `protected/extensions/behaviors/XCryptBehavior.php`

Both currently use:
- `mcrypt_get_iv_size`
- `mcrypt_create_iv`
- `mcrypt_encrypt`
- `mcrypt_decrypt`

## Preferred migration for VAU

Use VAU protocol/security manager `2.1` path and remove dependency on old `mcrypt` branch.

Reference implementation available locally:
- `/Users/erikuus/dev/yii/yii2-vauid2-extension/VauSecurityManager.php`

Reference usage notes:
- `/Users/erikuus/dev/yii/yii2-vauid2-extension/README.md`
- README explicitly states: for PHP >= 7.2, use security manager `version => 2.1`.

## Important compatibility note

Do not assume `mcrypt` Rijndael-256 ECB ciphertext is equivalent to OpenSSL AES-256 defaults.
If you must preserve old encrypted payloads, use a dual-read migration strategy and versioned ciphertext markers.

## Suggested rollout pattern

1. Switch VAU flow to 2.1-compatible manager path.
2. Keep temporary compatibility decrypt path only for legacy payload replay (time-boxed).
3. Re-encrypt persisted local secrets to supported crypto and remove compatibility bridge.
4. Remove all `mcrypt_*` calls before PHP 8 cutover.

## Validation checklist

- VAU login round-trip succeeds end-to-end.
- `decrypt()` handles real VAU callback payload in staging.
- No runtime errors containing `Call to undefined function mcrypt_*`.
- Audit grep over codebase returns zero `mcrypt_` hits in active code.
