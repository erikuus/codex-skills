# Provisioning and web

Read the selected public implementation files through the source map. The clean-host path and administrator-prepared path converge on the same verified app environments.

## Access and audit

Verify the SSH fingerprint independently, then reuse registered workstation keys and strict host-key checking. Keep separate private keys on separate workstations. Use the established Noora route when available. Kaardid's `noora-proxy` binds netcat to the current PPP interface and avoids route changes. Apply it only when the target needs that routing workaround.

A sandbox can hide macOS VPN status. Distinguish tool restrictions from actual network availability and use the supported scoped approval mechanism for a verified read-only command where allowed. Ask the user to connect the VPN when the actual required connection is unavailable.

Audit OS, package/PHP/PostgreSQL versions, modules, listeners, users, FPM pools, nginx configuration, mounted filesystems, existing databases/owners, jobs, disk space and backup ownership. Inspect metadata and redact private values. Keep administrator-managed pgAdmin and existing test sites intact during setup unless their alteration is in scope.

For sudo, prepare an idempotent wrapper in the app repository. Upload reviewed files under umask 077, verify checksums and invoke the precise helper through interactive SSH. Have the user enter the password privately in their Terminal. Verify a completion marker and inspect the actual installed result. Preserve private reports on failures so a resume can diagnose the specific failed stage. Reuse generated credentials and known managed objects.

## Filesystem and identities

The Kaardid default is `/srv/<app>` for rehearsal and `/srv/<app>-production` for production, each with `releases/<sha>`, a live pointer, a `previous` pointer and its own `shared/`. Rehearsal's live pointer is `rehearsal`; production uses `current`.

Adapt existing administrator paths deliberately. Harald's `/var/www/<app>/web` can remain the stable nginx document-root contract if it resolves to the correct release public tree with safe permissions. Check what occupies the path first and retain/recover the original site. Alternatively adjust just that app's managed vhost to a verified release root. Record the selected mapping. Discover which parts of each source tree are public before placing or linking files under `web`.

Each app/environment gets its own FPM service user/group, pool/socket, private configuration and writable state. The deployer owns immutable releases. PHP and nginx get sufficient read/traverse access without code-write access. The static reader can read public media/assets while private configuration and runtime remain inaccessible to it.

Kaardid uses code directories 02750, files 0640, private JSON 0640 to its intended reader group, migration credentials 0600 and private setup directories 0700. Reproduce the access contract through actual users and group traversal. Test new multipart uploads and fetch the inserted URL. A moved PHP upload can keep the wrong group. Copying into a setgid static-reader directory fixes inheritance while preserving 0640.

Separate local database roles per app/environment. Use a NOLOGIN object owner, a migration login allowed to SET ROLE owner, a DML app login and a read-only exploration role. Verify owner-specific default grants and cross-environment denial. Scope changes to databases and roles owned by this setup, preserving the cluster's other clients.

## Web configuration

Preserve working certificates, hostnames, proxy configuration and managed admin access after inspection. Install only app-required missing dependencies. Syntax-check before reload and verify sibling sites after shared-service changes. Back up touched configuration and support restoring that exact state if activation checks fail.

For every app, determine its actual executable entry points. Yii often uses only `index.php`. Nimeregister has several public/admin PHP handlers. Whitelist what the application's routes require and test it. Block uploads executing PHP and block HTTP access to private config, framework/internal directories, runtime, tooling, dotfiles and dev/test endpoints. nginx does not apply Apache `.htaccess`.

Use real-path FastCGI script identity so atomic release switches load the correct code. Verify assets, MIME types, nested uploads and intended path-info routing. Test existing direct and deep links.

The public edge and backend TLS are separate hops. Preserve backend certificate/SNI verification, HTTP-to-HTTPS redirects when part of the agreed topology and renewal ownership. A frontend response alone cannot establish backend verification policy.

Use the administrator-confirmed proxy address and overwritten client-IP header. Kaardid trusts `172.20.20.90` for `X-Real-IP`, confirmed by Mihkel. Verify these values for the target VM before use. nginx can resolve the client address with `set_real_ip_from` and `real_ip_header X-Real-IP`, while backend access restrictions use the original transport peer (for example `$realip_remote_addr`). Test an allowed client, an outside client and forged forwarded headers. Keep app trusted-client lists separate from proxy trust.

## Configuration adapters

Tracked PHP settings read private installation files. Local dev/test and VM rehearsal/production select separate credentials, writable paths and callbacks. Fail clearly on missing/wrong installation data. Keep placeholder examples in Git and actual secrets out of artifacts.

Yii adapters must cover web, console, migrations and jobs consistently. Standalone PHP adapters use that app's existing configuration and migration mechanisms. Preserve VAU cryptography/session behavior, including shared-host cookie names and paths. Test the final callback origin through the real HTTPS route.

Nimeregister's `content/` stores editable introduction HTML. Include it in durable shared data and backup/recovery. Its `tmp/cache`, `tmp/sessions` and `tmp/log` also need environment-specific writable paths. Treat other app-owned mutable files the same way.

For Services, preserve read-only archive data access and keep writable caches/temp files separate. Configure and test the file mount as the actual PHP/iipsrv users, with bounded cache size. Inspect optional ODBC/PDF/Imagick requirements in the current repository.

