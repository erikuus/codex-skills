# Services and iipsrv installation

Collect the actual infrastructure inputs before mounting or launching services. Keep independent app packaging/rehearsal preparation moving while these are pending.

| Input | Evidence required |
| --- | --- |
| File share | Server/export or share, NFS/CIFS protocol/version, approved mount options and expected source identity |
| Access | PHP/iipsrv reader accounts, UID/GID mapping, private credential-file path where required |
| Content probe | Known readable TIFF/pyramid UID/path, expected safe type/dimensions and authorization |
| Remote stores | Every DB/ODBC source from active configuration, server/database/role, TLS policy and approved read probe |
| iipsrv | Approved package or pinned source revision/release and checksum, required codecs, launcher and expected FCGI protocol |
| Operations | Service owners, failure response, cache/temp limits, notification path and storage recovery owner |

The handover alone does not supply share export details or a verified iipsrv build. Obtain these from the administrator/current installation and record the source/version. Keep passwords and share credentials in root/service-readable private files.

## Install and verify

1. Inspect existing mount units/fstab, package versions and service configuration. Adopt verified working objects. On a clean host install the selected protocol's client package and the approved iipsrv package, or build the pinned source with the recorded dependencies/codecs. Verify binary version and image support.
2. Create the mountpoint with no application write permission while unmounted. Install an app-owned named systemd mount configuration or a scoped fstab entry using the approved source/options. External image storage is read-only to these service accounts. Use `RequiresMountsFor=/mnt/uuskasutus` for consumers as appropriate.
3. Verify `findmnt --target /mnt/uuskasutus --output SOURCE,FSTYPE,TARGET,OPTIONS` against the expected exact target/source/protocol and read a known file as each consumer account. Check mount identity plus the known file. Directory existence alone is insufficient.
4. Install separate rehearsal/production iipsrv units/sockets and caches where independent configuration is required. Use the approved binary's actual FCGI invocation and options, fixed reader identity, socket group/mode, restricted writable cache/temp locations and bounded resources. Add startup dependency on the verified mount and a readiness precheck using the same mount/known-file contract.
5. Wire nginx to the exact socket and route and configure PHP dependencies. Syntax-check, start only the intended service and verify known SOAP, tile/image and PDF responses as appropriate. Check file access as PHP/iipsrv and client-IP authorization through the proxy.
6. Run storage health probes in isolated processes outside web request handling. Store the latest bounded result atomically on local disk. Readiness/status handlers consume that receipt with a default maximum age of 60 seconds, adapted to the actual probe interval. Missing, failed or stale evidence returns HTTP 503 or the documented dependency fault. Preserve the last successful timestamp separately. A cached image response follows its own documented cache policy.
7. Test with local fake mount/process probes first. During an agreed target maintenance window verify actual restart/reboot and file-server-loss behavior. Keep storage disruption tests away from a shared live mount.

Use bounded cache/temp directories with documented size/expiry cleanup that preserves source images. Exercise full-cache/no-space behavior on disposable directories and confirm failures keep the service responsive and produce useful diagnostics. Test iipsrv process failure and missing socket without changing another environment's process.

The concrete starting points are `assets/runtime/check_storage.py` and `assets/systemd/iipsrv.service.template`. Install the checker on local disk at a private service-readable path. Its public entry point puts mount discovery, path resolution, metadata lookup and file reads inside a worker with a five-second deadline. Non-regular probe files, including FIFOs, are rejected before open; regular file descriptors are checked again. An empty unmounted directory fails.

Invoke the public CLI with `--timeout 5` for background/manual observations and service startup. The unit also has `TimeoutStartSec=15s`. Readiness handlers read the cached local receipt and perform no remote filesystem I/O. The internal worker is an implementation detail. Keep at most one probe attempt active per environment.

Resolve the unit's PYTHON_EXECUTABLE from runtime.pythonExecutable in the verified app contract. Validate the rendered ExecStartPre with that interpreter and service identity. An older system Python can coexist with the selected versioned interpreter.

Timeout cleanup sends a kill to the worker process group. Kernel-blocked network I/O can remain pending until the kernel releases it. The parent still returns an unavailable result within its deadline and short cleanup allowance. Record persistent blocked-worker/storage failures for the infrastructure owner and avoid accumulating new probes.

Resolve the unit's foreground FCGI invocation from the approved binary and verify systemd supervision. Real mount/reboot/failure behavior remains an integration test on the intended disposable Linux target.

Sentry/error monitoring covers PHP errors. Status/dashboard additionally reports mount identity/known-file probe, iipsrv process/socket health and applicable remote-store checks, with attempt/success times. Record the alert owner and verify actual delivery using an approved synthetic failure.

