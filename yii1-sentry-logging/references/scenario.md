# What problem Sentry solves

Without Sentry, Yii can send one email per `error`. That is fine until one broken code path starts failing repeatedly.

Use this scenario as the baseline:

- `300,000` images exist
- thumbnail rendering breaks and throws `500`
- a bot crawls at `1` request every `0.5` seconds

That means:

- `300,000` raw failing requests
- about `41h 40m` of nonstop traffic

## Old Yii mail route

If Yii emails every `error`, then in the worst case:

- app produces about `300,000` identical failures
- mail route tries to send about `300,000` emails
- mailbox becomes noise
- normal outbound mail can be delayed

## New Sentry route

`XSentryLogRoute` suppresses most repeats locally before they even reach Sentry.

Recommended production values:

- `throttleWindowSeconds = 900`
- `throttleMaxInitialEvents = 1`
- `summaryThreshold = 25`

That creates a fixed `15` minute window per error fingerprint:

- raw occurrence `#1` is sent immediately
- raw occurrence `#25` sends one summary event
- all other identical repeats in that same window are suppressed locally

## What Sentry receives

With a bot sending about `1,800` failed requests per `15` minutes:

- raw failures per window: about `1,800`
- Sentry events per window: `2`
- locally suppressed per window: about `1,798`

Across `300,000` failures:

- raw failures: `300,000`
- Sentry events: about `334`
- locally suppressed: about `299,666`

Sentry creates the issue only on the first event. Later events stay on the same issue and only increase its event count:

- event `1`: first occurrence, creates the issue
- event `2`: summary for raw occurrence `#25`, same issue, event count becomes `2`
- event `3`: first occurrence in next `15` minute window, same issue, event count becomes `3`
- event `4`: summary in next window, same issue, event count becomes `4`
- event `5`: first occurrence in third window, same issue, event count becomes `5`

## What email rules should do

Rule 1:

- environment `prod`
- `A new issue is created`
- send one email immediately

Rule 2:

- environment `prod`
- `The issue is seen more than 4 times in 1h`
- send email
- frequency `480` minutes

Under nonstop bot traffic that gives:

- one immediate email when the issue starts
- one second email about `30` minutes later, when issue event count becomes `5`
- then at most one reminder every `8` hours while the issue is still active

That is why this setup is useful:

- low mailbox noise
- low Sentry quota usage
- one readable issue in the feed
- enough reminders that a long-running production problem stays visible
