# Kaardid implementation map

The public reference sources are bundled under `assets/kaardid-reference/`. They were copied from committed Kaardid source at the revision recorded in `manifest.json`. The responsive dashboard HTML was read from the actual Page and has separate source provenance there.

Read files selectively for the stage being implemented. Keep the originals as references and write the app adapter into the target repository. Verify the per-file hashes before using the snapshot if its integrity is in question.

Run `scripts/check_package.py` for package integrity and `scripts/validate_offline.py` for the declared local suite. See [validation.md](validation.md) and `assets/reference-requirements.json` for self-contained versus assembled-application tests and pinned external tool acquisition.

The maintained first-staging and host-lock helpers live in `scripts/stage_release.py` and `scripts/with_host_lock.py`. The revised bounded refresh runner lives in `assets/runtime/`. Adopt those revised helpers when creating target tooling. The unchanged Kaardid snapshot retains historical behavior for comparison.

## Adapter work

The source guards and constants are specific to Kaardid. Replace them deliberately from the validated inventory and tests.

| Concern | Values/callers to inspect |
| --- | --- |
| Identity | SSH alias, hostname guard, deployment user, app/repository identity and source branch rules |
| Runtime | Framework discovery, PHP executable, Composer location/vendor path, generated assets and entry points |
| Isolation | Unix accounts/groups, database/role selectors, shared roots, credentials and every profile |
| Deployment | Ports, maintenance implementation, operation/promotion locks, app-relative paths and health routes |
| Web | Actual public roots/handlers, nginx file ownership, TLS identity, private-route blocks and proxy trust |
| Recovery | Setup/backups paths, expected dump name, metadata identity, active/previous pointers and ownership checks |
| Monitoring | Unit allowlist, installed schedule parser, structured counters/checkpoint, expiry and Page labels/paths |

A global search-and-replace of the app name leaves incompatible behavioral assumptions. For example, Nimeregister needs its own migration and public/admin entry-point handling, durable editable HTML and standalone maintenance check. Services needs remote dependencies and iipsrv while local database backup/migration operations are inapplicable. PostgreSQL 18 requires the selected client and extension checks.

## Source groups

Paths in this section are relative to `assets/kaardid-reference/`.

| Stage | Read these sources and preserve the relevant contracts |
| --- | --- |
| Access/audit | `bin/vm`, `bin/noora-proxy`, `bin/server-audit`, `ops/server-audit.sh` |
| Privileged setup | `bin/server-prepare`, `ops/server-prepare.sh`, `bin/production-prepare`, `ops/production-prepare.sh` |
| Private selectors | `protected/config/Environment.php`, `ops/configure-production.py`, `ops/check-production-config.php`, `bin/production-configure` |
| Data | `bin/pg17`, `ops/snapshot-local.php`, `ops/restore-rehearsal.py`, `ops/export-integration-secrets.php` |
| Artifact | `ops/build-release.py`, `bin/rehearsal-deploy` |
| Deployment lifecycle | `ops/deploy-rehearsal.py`, `ops/promote-production.py`, `bin/production-deploy` |
| Maintenance | `protected/config/Maintenance.php`, `protected/controllers/MaintenanceController.php`, `protected/views/maintenance/index.php` |
| nginx/FPM first activation | `ops/activate-rehearsal.sh`, `bin/rehearsal-activate`, `ops/nginx/kaardid-rehearsal.conf`, `ops/nginx/kaardid-production.conf` |
| Backend TLS | `bin/production-backend-tls`, `ops/install-backend-tls.sh`, `ops/nginx/kaardid-backend-tls.conf` |
| Job isolation harness | `bin/updater-check`, `ops/check-updater.py`, `ops/check-updater.php` |
| Job definitions/history | `ops/systemd/kaardid-update.service`, `ops/systemd/kaardid-update.timer`, `protected/commands/UpdateRunHistory.php` |
| Failure notifier | `ops/install-monitoring.sh`, `ops/report-job-failure.php`, `ops/systemd/kaardid-job-failure@.service`, `bin/monitoring-install` |
| Sentry test | `bin/monitoring-probe`, `ops/test-sentry-probe.py`, `ops/sentry-probe-router.php`, `protected/extensions/actions/XSentryProbeAction.php` |
| Status and refresh | `ops/vm-status.py`, `bin/refresh-dashboard`, `ops/dashboard/refresh-prompt.md` |
| Local HTTP boundary | `dev-router.php` |

Historical staging/preview code is bundled only where needed by active tooling or regression fixtures. `ops/production-preview.py` is retained for the promotion lock regression test. The source `kaardid-backend-tls.conf` is a staging-only 503 template. Adapt the actual active app backend using its current runbook and inspection. The initial production loopback template provides private app routing. Preserve the administrator's currently working public backend/TLS/proxy when integrating these.

Source functions such as `backup_and_migrate`, `prune_backups`, `rollback_for_deploy`, `prune_releases`, `operation_lock`, `deploy_locked`, `verify_contents` and `tested_artifact` capture the tested mechanics. Match them to the target's commands and current callers before consolidating.

## Validation

Use the relevant bundled `ops/test_*.py` files as examples of behavior and failure injection. Run them from an adapted target with the required files and dependencies. Their original expected database names, paths and routes need adaptation along with the implementation.

Prioritize concrete failures and normal entry points.

- Wrong app/environment/database identity stops before write work.
- Concurrent updater/deployment and repeated same-SHA deployment preserve consistent state.
- Invalid archives, extra code, checksum mismatches and unsafe shared links prevent activation.
- Backup failure, migration failure, health failure before/after reopening and interrupted probes preserve the documented state.
- Manual maintenance survives successful deployment and rollback.
- Three-dump retention protects failed/pending/unknown attempts and cross-app roots.
- Code retention preserves the active artifact and immediate useful predecessor.
- Actual HTTP routes, assets and new uploads work, with private/config/dev/tooling paths blocked.
- Structured job completion/checkpoint/warnings and dashboard timestamps match observations.
- A deployment/recovery of one app preserves siblings on the same VM.
- Database-free and standalone-PHP adapters exercise their applicable behavior.

Use disposable directories/database copies and a temporary configured test server for destructive failure probes. Verify live features through normal entry points after deliberate installation. Record the environment and scope of every test.

The bundled Kaardid helpers contain application-specific staging/host guards and migration expectations. Their baseline tests demonstrate those original mechanics. New-host acceptance still requires the target adapter and live verification.

