# Base stack and active HTTPS

Support the demonstrated Ubuntu/systemd/nginx/PHP-FPM deployment model. Record OS release, package source and selected runtime majors before changing packages. Other OS/service managers need an explicit adapter.

Require Python 3.12 or newer on both the workstation and VM. This covers the selected hashing/archive helpers and the maintained POSIX process/locking utilities. Run `python3 scripts/check_python.py` locally before packaging. Copy that small preflight into the target's ops directory and run it with the selected VM interpreter before provisioning/deployment helpers. Record both interpreter paths/versions in the contract.

If the VM interpreter is older, use an administrator-approved distribution package or versioned interpreter and invoke that exact path. Inspect package candidates first and preserve unrelated system Python users. Resolve the interpreter before starting privileged setup. Run the preflight as the intended automation/deployment identity as well.

Record the resolved absolute path as runtime.pythonExecutable in each app contract. Render generated Python callers from that value. The iipsrv unit uses `{{PYTHON_EXECUTABLE}}` for its storage precheck. Run check_python.py and the rendered precheck with that exact executable as the service account before installing the unit. Verify executable/file traversal permissions under its service restrictions.

## Existing host

Inspect installed versions, package policy, pools, listeners, databases, vhosts and certificate files. Reuse Mihkel's verified PHP 8.5/PostgreSQL 18 preparation on Harald. Scope edits to managed app files and verify sibling sites after reloads. Keep existing operator/pgAdmin access and secrets.

## Clean host

1. Capture OS release/architecture and approved repositories. Check candidate availability with `apt-cache policy` for nginx, the required PHP-FPM/CLI/modules and PostgreSQL major/extension packages. PHP 8.5 availability depends on the approved package source. Resolve a missing source with the administrator before installing it.
2. Generate the exact install list from the app contract. A typical selected stack contains nginx, php8.5-fpm/cli/pgsql/mbstring/xml/gd/curl and PostgreSQL 18 plus the required extension package when local managed databases apply. Install SOAP, Imagick, ODBC, PostGIS or file-share clients only when discovered requirements use them.
3. Under the host setup lock install approved packages, validate their versions, configure the specific FPM pools and initialize only the selected managed PostgreSQL cluster if absent. The Services host can use libpq/PHP clients without a local PostgreSQL service.
4. Verify pool syntax, PostgreSQL connectivity/authentication/default grants, intended listeners and disk budget. A second app reuses the host stack. Keep per-app DB/bootstrap state independent of the shared operator role.
5. Record runtime/tool versions and acquisition provenance. For Yii use a supplied pinned source snapshot with its content hash. For Composer use the adapter's verified executable or the pinned original Git object described in `assets/reference-requirements.json`. Use the target's lockfile and vendor path.

Copy `scripts/with_host_lock.py` into the target ops directory. The privileged wrapper runs the reviewed setup helper with
`python3 ops/with_host_lock.py --lock /run/lock/application-vm-setup.lock -- /bin/bash <reviewed-host-helper>`.
The root-owned 0600 lock serializes shared changes. A busy lock returns 75. Keep the full shared mutation inside that command.

The original server-prepare.sh changes Kaardid's personal operator role attributes as part of its single-app bootstrap. Implement the shared-operator contract in app-contracts.md when adapting it. The app helper verifies an existing personal role and grants only the new app's intended membership.

## Active HTTPS backend

The old bundled TLS installer belongs to Kaardid's historical preview transition. New installs use the active template in `assets/nginx/active-backend.conf.template`.

Resolve template values from the approved inventory and app contract. Supply a certificate valid for the backend SNI hostname and its chain, private key path/modes and renewal owner. Inspect existing certificate metadata before copying replacements. Keep key contents private. Public edge TLS and backend TLS verification have separate owner evidence.

The active template serves the same app-specific location rules through private HTTPS and its loopback probe. Generate the included routes file from the app's real public handlers, shared paths, private-path blocks and FastCGI socket/realpath identity. Set PUBLIC_ORIGIN, backend address/hostname and verified proxy address/header deliberately. Restrict backend transport using the original peer when real-IP resolution is enabled.

Write candidate files beside retained originals, validate an isolated nginx candidate configuration, then back up only the touched managed files. Run nginx -t before graceful reload. Test certificate hostname/chain, redirect URI/query preservation, loopback health and the restricted public edge. Check sibling health before/after. Restore the saved app configuration and reload if validation fails.

Rehearsal, active production and restricted staging have different checks. A 503 staging response establishes staging closure. Active application health must pass the app's expected normal responses.

