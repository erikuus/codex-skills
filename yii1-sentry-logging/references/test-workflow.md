# Two-email test workflow

Use this workflow when proving the setup end-to-end.

## Goal

Verify all of this against the real app:

- first occurrence creates one Sentry issue
- first occurrence sends one email
- repeats in the same fixed throttle window do not create another issue
- summary event increments the same issue event count
- Rule 2 eventually sends the second email

## Marker naming

Use a stable unique marker in the temporary exception message:

- `YII1_SENTRY_RULE_TEST_YYYYMMDD_A`

Examples:

- `YII1_SENTRY_RULE_TEST_20260525_A`
- `YII1_SENTRY_RULE_TEST_20260525_B`

Search the exact marker in both Sentry and Gmail before starting.

## Temporary probe pattern

Do not assume the natural failure path already creates an `error`-level `500`.

If needed:

1. add a temporary env-gated probe in the target code path
2. gate it by an env var such as `YII1_SENTRY_PROBE_MARKER`
3. when the env var is present, throw a `CException`
4. include the stable marker in the exception message
5. remove the probe after the test

This gives:

- a real `500`
- deterministic grouping
- easy Sentry/Gmail search

## Browser test pattern

Pick a repeatable browser path that hits the same failing code path over and over.

Examples:

- open one broken page repeatedly
- crawl paginated search results and visit the same type of attachment/image view
- hit one image/file endpoint repeatedly through the real UI

The path does not matter as much as these properties:

- each request reaches the same error fingerprint
- the page is easy to automate
- raw occurrence count can be advanced on purpose

## Expected fixed-window progression

For the recommended route:

- `throttleWindowSeconds = 900`
- `throttleMaxInitialEvents = 1`
- `summaryThreshold = 25`

The issue should evolve like this:

- event `1`: first occurrence, creates the issue, email `1`
- event `2`: summary at raw occurrence `#25`, same issue, count `2`
- event `3`: first occurrence in next `15` minute window, same issue, count `3`
- event `4`: summary in next window, same issue, count `4`
- event `5`: first occurrence in third window, same issue, count `5`, email `2`

Important:

- only event `1` creates the issue in the feed
- later events stay on the same issue and only increase event count
- verify Rule 2 against issue event count, not “new issue count”

## Sentry verification queries

Use the Sentry helper/plugin to verify:

- one issue exists for the marker
- issue count grows `1 -> 2 -> 3 -> 4 -> 5`
- no duplicate issue is created for the same marker

## Gmail verification queries

Search for:

- `from:noreply@md.getsentry.com "<MARKER>"`

Expected result:

- one email after event `1`
- still one email after event `2`
- two emails after event `5`

Delivery lag rule:

- if Sentry shows the matching alert fired but Gmail does not show the message yet, treat the state as pending
- wait `2` minutes and rerun the same Gmail search
- keep rechecking for up to `10` minutes total before concluding the mailbox proof failed
- only call the verification partial or failed after those rechecks are exhausted

## Cleanup

After the test:

1. remove the temporary probe
2. restore the original code path
3. stop any special local server/env setup
4. resolve or archive the temporary Sentry issue
