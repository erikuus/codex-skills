# Topology and discovery

Use one inventory for the shared host and reference its exact path from each application's handover. Keep it in the agreed coordinating repository. Each app owns its deploy/status commands and documentation. When setup is called from a single project, discover its siblings from the administrator's handover and read their instructions before planning shared-host changes.

## Inventory

Use `assets/topology.example.json` as a shape example and replace every project-specific choice. Schema version 1 contains `hosts[]` and `apps[]`.

A host has `id`, `sshAlias`, `setupLock` under /run/lock, `capacity` (observed or null), optional `operatorRole` and non-secret `notes`. Use the verified SSH alias and preserve strict host-key checking. Capacity is a host budget for all pools and services combined.

An app has `id`, `host`, `repository`, `framework` (`yii1`, `standalone-php` or `custom`), `publicOrigin`, and `environments.rehearsal/production`. Each environment declares `root`, `setupRoot`, `serviceUser`, `fpmSocket`, `probePort`, `unitNames` and `database` (null for an app with no local managed database). Optional `webTunnelPort` and `dbTunnelPort` are unique across the workstation. Unit names, sockets, roots, setup paths and probe ports are checked per host. A local database declares `cluster`, `name`, `ownerRole`, `migrationRole` and `appRole`. Cluster identity is host plus cluster name.

Unknown fields are rejected to catch misspelled allocations. Put explanatory text in `notes` and detailed app behavior in `ops/app-contract.json`. The validator supports app roots under /srv or /var/www, private setup roots under /home or /srv, and sockets under /run or /var/run. It rejects reserved runtime identities and cross-resource overlaps. Add and test an explicit schema change for another required layout.

Record these remaining resolved facts in the app contract and runbook.

- VM private/public identities, approved SSH fingerprint, sudo owner and VPN dependency.
- nginx site files, actual document roots, production backend origin/SNI, certificate paths and renewal ownership.
- Entry points and URL layout, FPM version, dependencies, web/migration/job commands, private file paths and health routes.
- Distinct rehearsal/production ports, service identities, sockets, roots, locks, backup roots, unit names and database privileges.
- Mutable files, uploads, cache, sessions, editable HTML, image mounts, checkpoints and remote dependency selectors.
- Existing Page IDs, local action commands and external handoffs.

Keep passwords, DSNs containing passwords, API tokens, keys, secret links and real private configuration in protected files. The inventory contains only names, paths and decisions.

Use null for an unresolved public origin while independent rehearsal preparation continues. Resolve and verify it before configuring final callbacks or public activation. The allocation validator permits this incomplete input and does not certify readiness.

## Shared host

Use the same model for either topology. Adding applications adds isolated app/environment allocations, while nginx, PHP packages and PostgreSQL clusters remain host-managed resources. A deployment of Pitserid must preserve the Aadresslehed and Nimeregister pointers, configuration, data, jobs and live behavior.

Reserve two loopback probe ports per app and distinct local tunnel ports so several rehearsals can stay open together. Check existing listeners and SSH forwards. Reuse an existing safe allocation on resume. Use app/environment-qualified pool, socket, unit, logfile, backup and setup-report names.

Allocate FPM concurrency from measured process memory and the total VM budget, including PostgreSQL, iipsrv, caches and the OS. Sum all pools before choosing limits. Rehearsal can use small/on-demand pools. Treat adding packages, changing PostgreSQL authentication and reloading nginx/FPM as shared-host work with sibling checks.

Use per-app operation locks for deployment/updaters and a host setup lock for serialized shared configuration changes. Document a consistent order if promotion needs both rehearsal and production locks. Avoid acquiring the same lock twice through nested helpers. A busy lock is a recoverable retry after the owning operation completes.

## Scope and decision handling

Resolve predictable implementation choices from the handover and repository. Ask only about missing choices that affect data, endpoint identity, shared resources, publication or authorization. Bundle questions and continue independent stages.

A new deployment instruction usually authorizes setup of the named app or apps. Include sibling discovery and read-only checks. Installing this skill alone requests creation of reusable tooling. Deployments happen on a later explicit invocation.

Read the current repository configuration before choosing the PostgreSQL major or a migration framework. Inspect custom extension/client compatibility on an isolated restore. A host with PostgreSQL 18 needs an appropriate client and extensions. Kaardid's `bin/pg17` provides the client-selection pattern.

Treat live administration portals and desktop pgAdmin registrations independently. A server tree label conveys no privilege guarantee. Query the selected database/current user and verify that user's actual connect/read/write rights.

