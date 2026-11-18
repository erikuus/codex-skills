# Data and integrations

## Approved snapshots and corrections

Discover the target's data-import documentation and existing scripts before choosing restore commands. Record snapshot/checksum/source/version, migration baseline, counts and durable media/checkpoint manifest. The user chooses which environments receive which snapshot. Initial rehearsal can use an approved test copy while cutover uses a frozen live snapshot.

Select a PostgreSQL client compatible with the source archive and target server. Check required extensions such as `fuzzystrmatch` for Nimeregister and PostGIS only for apps using spatial data. Validate against an isolated restore. Inspect unsupported old extension objects and dependencies before any omission and record every justified exception.

Restore as the intended owner with transactional error handling where supported, preserve migration history, apply grants and verify counts/schema facts without publishing row contents. Refuse populated unexpected targets. Preserve the previous database until the verified switch and recovery plan are complete.

Run app-specific correction/import commands in documented order and test their idempotence. Kaardid's image selections, AU transformations and HTML corrections are examples of discovering a domain procedure. Other apps need their own documented transformations. SQL NULLs, contributor ownership and editable files must survive.

Transfer media separately with content checksum and service-account/read permissions checks. Freeze all writers needed for a consistent final dataset, including editable HTML, uploads and jobs. Record the real updater checkpoint supplied with the export. Replacing it with today's time can skip work.

## DGS, SOAP and other dependencies

When a target uses DGS, VM rehearsal/production call `https://kristjan.arhiiv.ee/dgs-api/api/v1/dip/`. Mac development uses `https://www.ra.ee/dgs-api/api/v1/dip/`. Derive this from the installation once and apply it across web, console and jobs. Verify TLS certificate and hostname normally.

Check the deployed effective endpoint and perform a known read operation as the actual service account. HTTP 400/403 alone does not identify the rejecting layer. Ask the provider to confirm the observed client IP and request validation. Trace transport peer, forwarded headers and address actually checked by the allowlist. Keep proxy header trust separate from user authorization.

For SOAP verify a known operation, returned metadata and actual image/content when relevant. A WSDL/homepage response establishes less than an actual operation. Compare Mac, rehearsal and production sources with the same inputs and record each endpoint/target. Services tests may default to the deployed legacy backend. Preserve declared targets and report their scope. Local demo success through a remote SOAP URL does not verify a newly deployed service.

## Services and iipsrv

Services can run without a local application database while connecting to external AIS/kmooduli stores. Discover the existing configuration contract and use appropriate separate credentials/permissions for production and rehearsal. Keep rehearsal's dependency calls read-only unless an isolated approved test target supports writes. Avoid running migrations/imports against administrator-owned external databases.

Verify `/mnt/uuskasutus` availability persistently and test file reads as PHP and iipsrv. Preserve file-server data. Test image preview/tile/full-file routes, UID authorization, limits, timeouts, PDF behavior and caching. Use the actual production URL layout, including any removed legacy `/services` prefix.

Adapt iipsrv/FCGI process management and cache roots per environment. A production iipsrv process or cache can be shared only when the read-only contract and configuration are intentionally common and tested. Distinct rehearsal processes/sockets/caches are the default for independently changing service code. Bound CPU/memory and local cache/temp space within the agreed VM budget.

Check clients' configured URLs, WSDL-generated addresses, redirects and iframe/mixed-content behavior before moving consumers. Treat dependency readiness and DNS/public opening as owner handoffs recorded with evidence.

## Authentication and private data

Preserve the app's VAU authorization model and callback cryptography. Configure callback origins for the final HTTPS host and test real return/login/logout with a user identity when needed. Trusted IP guest controls and authenticated editor rights are separate checks. Ask the user to enter passwords and identity credentials directly in their own app/browser.

Store integration secrets separately per installation and preserve approved reuse decisions. A first setup can reuse a particular existing key only with the user's authorization. Resume without rotating keys. Keep copies and diagnostics private and exclude them from Git, Pages, artifacts and command arguments.

