# Sentry API payloads and caveats

Use direct Sentry REST API mutation for rule setup. The local Sentry helper/plugin is read-only for issues/events and should be used only for verification.

These Sentry-side rules are shared by both app-side runtime branches. Only the Yii route implementation changes between modern and legacy PHP runtimes.

Base URL:

- `https://sentry.io/api/0`

Required auth:

- `SENTRY_AUTH_TOKEN`

Common path:

- `POST /api/0/projects/{org_slug}/{project_slug}/rules/`
- `GET /api/0/projects/{org_slug}/{project_slug}/rules/`
- `PUT /api/0/projects/{org_slug}/{project_slug}/rules/{rule_id}/`

## Project setup assumptions

- Use one Sentry project per application
- Use environments inside the project: `prod`, `test-sentry`, `local`
- Use the project DSN in the Yii app config
- If the target environment does not exist yet, seed one event first so the environment becomes selectable in Sentry

In practice, creating the project in the Sentry UI is usually faster than mutating it through the API. This skill automates rule creation and verification after the project already exists.

## Rule 1: new issue

Recommended rule name:

- `Notify {email}: new {environment} issue`
- for the retained production rule, the exact environment segment must be `prod`
- do not substitute `test`, `test-sentry`, or a temporary marker in that retained production rule name

Payload shape:

```json
{
  "name": "Notify erik.uus@gmail.com: new prod issue",
  "actionMatch": "all",
  "filterMatch": "all",
  "frequency": 5,
  "conditions": [
    {
      "id": "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition"
    }
  ],
  "filters": [],
  "actions": [
    {
      "id": "sentry.mail.actions.NotifyEmailAction",
      "targetType": "Member",
      "targetIdentifier": "4578598",
      "fallthroughType": "ActiveMembers"
    }
  ],
  "environment": "prod"
}
```

Notes:

- In this account, the API rejected `frequency=0`, so the tested working value is `5`
- For a new-issue rule, `5` behaves fine in practice because only the first event creates the issue
- Sentry may normalize `fallthroughType` to `ActiveMembers` on create/update

## Rule 2: persistent issue

Recommended rule name:

- `Notify {email}: persistent {environment} issue`
- for the retained production rule, the exact environment segment must be `prod`
- do not substitute `test`, `test-sentry`, or a temporary marker in that retained production rule name

Payload shape:

```json
{
  "name": "Notify erik.uus@gmail.com: persistent prod issue",
  "actionMatch": "all",
  "filterMatch": "all",
  "frequency": 480,
  "conditions": [
    {
      "id": "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
      "value": 4,
      "interval": "1h"
    }
  ],
  "filters": [],
  "actions": [
    {
      "id": "sentry.mail.actions.NotifyEmailAction",
      "targetType": "Member",
      "targetIdentifier": "4578598",
      "fallthroughType": "ActiveMembers"
    }
  ],
  "environment": "prod"
}
```

Meaning:

- Rule 2 fires when the issue event count seen in the last hour becomes more than `4`
- With the fixed-window `900 / 1 / 25` route, that happens when the issue reaches event count `5`
- That is why the second email appears about `30` minutes into a sustained incident

## Verification

After mutation:

1. list rules with `GET /rules/`
2. verify exact names, environment, condition ids, and frequency
3. use the Sentry plugin/helper to verify issue/event behavior
4. use the Gmail plugin to verify actual notifications

Official docs:

- [Create an Issue Alert Rule for a Project](https://docs.sentry.io/api/alerts/create-an-issue-alert-rule-for-a-project/)
- [List a Project's Issue Alert Rules](https://docs.sentry.io/api/alerts/list-a-projects-issue-alert-rules/)
