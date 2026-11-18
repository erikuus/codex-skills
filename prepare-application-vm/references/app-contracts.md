# App contracts

Write the resolved contract into the target's `ops/app-contract.json`. It documents the concrete commands the adapter implements. A capability has a boolean `applicable` and a reason when false. Unknown inputs are pending. Propagate this distinction through deployment, recovery and status.

| Contract section | Required decision |
| --- | --- |
| Artifact | Include/exclude paths, public document-root mapping, dependency locks and framework/tool source/digests |
| Runtime | Verified absolute runtime.pythonExecutable, minimum Python 3.12 and actual workstation/VM version evidence |
| Public handlers | Real PHP entry points, path-info/rewrites, private/media denial rules |
| Configuration | Each profile's selectors, private paths, environment variables and callback/cookie origin |
| Durable state | App-relative to shared-path map, writer account, recovery source and disposable cache/session policy |
| Database | Managed local, external or absent; exact identity and ownership; migration preview/apply/post-check command arrays |
| Maintenance | Marker, request behavior, private health capability and manual-state preservation |
| Health | Read-only route/method/expected status plus feature/API response validation |
| Jobs | Commands, locks, checkpoints, receipt fields, schedule and real writer ownership |
| Monitoring | App errors, applicable job/process/storage checks, delivery mechanism and recipient proof |
| Recovery | Coordinated components, capture/restore commands and reopen checks |

Use fixed argument arrays and validated identifiers for generated commands. Keep secrets in private config/credential files. Define inapplicable database/migration/job operations explicitly so ordinary code deployment still exercises locks, maintenance, artifact and route verification.

## Yii with a managed database

Adapt Kaardid's portable selectors and migration lifecycle to the actual app's Yii 1.1.33-dev snapshot, Composer lock/vendor directory and console configuration. Include the framework by verified content digest. Keep local dev/test separate from VM profiles. Confirm that migrations use the migration identity, while web and jobs use the app identity. Preserve existing session handlers.

## Standalone Nimeregister example

Artifact includes required root PHP handlers, `admin/`, `app/`, frontend assets, configuration readers, `database/migrations/` and any `bin/` commands required for operations. Discover exact handlers from source and tests. Yii is inapplicable. Composer is used only when the repository actually declares locked dependencies.

Map `content/` to durable shared editable HTML and seed its four introductions once. Map cache, sessions and import logs under separate per-environment shared paths. Keep private database/VAU files separate from committed examples.

The existing `bin/db-init` creates local dev/test databases. `bin/db-refresh` imports a snapshot. Neither is a routine production migration command. Implement a target-specific migration runner for the ordered SQL files with a recorded migration ledger/checksums, transaction/error handling, pending preview and post-check. Validate the imported baseline before marking existing migrations applied. Test the runner against a disposable PostgreSQL target before enabling the deployment hook.

Implement the app's shared maintenance/probe guard at the earliest common request bootstrap used by all public/admin handlers. Verify public search, login return, admin authorization/CSRF, contributions, editable introduction persistence and report-mail delivery. A deployment and retained-code rollback must preserve content and private state.

## Services with external databases example

Artifact includes the verified Yii/dependency snapshot, providers, file routes and required public assets. Managed local database provisioning, dump and migration hooks are inapplicable. External DB access remains applicable with separate approved identities and owner-managed recovery.

Discover all configured stores, including AIS, kmoodul, Saaga and any ODBC sources. Preserve external ownership and test effective configuration as the actual service account. Rehearsal uses read-only approved dependency access or an isolated fixture. Make the test target explicit.

Keep private config, runtime, sessions, iipsrv socket/cache/temp paths distinct per environment. Health includes known SOAP operations, known-file image/tile/PDF responses and storage/process readiness. Job capability can be inapplicable while process/storage monitoring remains applicable. See services.md for installation inputs and failure behavior.

## Shared-host provisioning contract

A host initializer owns shared package installation, the host setup lock and infrastructure inventory. An app initializer owns only its qualified service accounts, DB roles, roots, pools, sockets and units.

Reuse an existing personal PostgreSQL operator role as observed. Grant only the new app's intended group membership, preserving its password/global attributes and existing memberships. Creating a missing personal login is a separate host-level operation with private password input. App bootstrap receipts exclude personal roles from app-owned objects.

Hold a host-wide setup lock while changing shared config or host identities. Use an app/environment lock for deployment and jobs. A repeated run must reconcile recorded ownership with actual objects. Test first, second and third app provisioning with sentinel roles/grants/files unchanged for siblings.

Use `scripts/plan_app_roles.py` when adapting the DB bootstrap. Its input contains `operator`, `roles` (owner/migrate/app/readonly names), observed `existingRoles` and receipt-backed `managedRoles`. It emits a scoped transaction creating only missing app roles and granting intended memberships. It preserves the shared operator's password/global attributes. Apply it under the host lock after reconciling actual catalog state, then install app passwords from the private bootstrap state only for newly created identities. Reuse managed identities/secrets on resume.

