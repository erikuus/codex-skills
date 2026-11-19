# Deployment and recovery

Use the lifecycle in the bundled Kaardid builder, deployer, promoter and tests. Adapt identity guards, paths, database commands and HTTP checks in one target-specific implementation. Preserve normal entry points and existing callers.

Use [first rehearsal bootstrap](bootstrap.md) to establish the initial release/pointer. Use [the setup sequence](setup-sequence.md) for prerequisites and [consistent recovery](recovery.md) for DB/content/checkpoint restore commands.

## Artifact and promotion

Build from a pushed commit. Routine actions require updated pushed main and reject dirty/unpushed or wrong-branch selections according to the target's documented contract. Record the app commit, repository, framework/dependency hashes, config-template hash and archive checksum. Build from Git-tracked source and a deliberately selected pinned runtime/dependency set.

Exclude private config, development/test entry points, docs/tooling and temporary artifacts from the release. Shared writable/private paths are connected separately. Verify archive path/type/duplicate/link constraints before extraction and reject conflicting existing release identities.

Rehearsal tests the normal app or API. Save its successful deployment receipt and artifact. Production preparation verifies the exact active tested rehearsal release, receipt and every shipped byte under the relevant locks. Copy the same artifact and preserve original provenance. Production keeps its own shared links.

## Routine lifecycle

1. Stage and verify immutable code while the existing release serves requests.
2. Acquire deployment serialization and the same environment operation lock used by cooperating jobs. Check target identity before any maintenance, backup or migration.
3. Enable maintenance and verify ordinary GET/POST requests receive HTTP 503 with no-store. Remember whether the operator already enabled maintenance.
4. For a managed database, make a private custom-format dump, checksum it and read every archive payload with `pg_restore --file=/dev/null`. Save pending-outcome metadata before migrating. Clean temporary password files on all exits. An external-database service uses its explicit backup/migration ownership agreement.
5. Run the app's migration preview/apply/post-check against only that environment. Yii migration history commands can create tables. Standalone PHP uses its verified native equivalent.
6. Atomically switch the live pointer, retaining the immediate predecessor. Check the incoming release while ordinary visitors remain closed.
7. Revoke the temporary health capability, reopen deployment-owned maintenance and repeat ordinary visitor checks. Preserve pre-existing manual maintenance.
8. Record success, retain recovery material and apply the eligible retention rules. Cleanup failure reports a warning while keeping the healthy release.

A private health capability is short-lived, release-bound, GET/read-route limited, loopback-only and header authenticated. Revoke it on success, failure, signal and timeout. Loopback alone allows ordinary SSH-tunnel visitors through. Test both permitted probes and unauthorized requests.

Database-free apps still use immutable artifacts, locks, maintenance, migration applicability checks, health verification, code rollback and durable files. Represent database operations as explicitly inapplicable.

## Failures and recovery

Backup or migration failure prevents activation and leaves maintenance for inspection. Earlier/nontransactional migration effects may remain. Health failure after switching restores prior code and closes the site. Failed first activation removes the incoming pointer and stays closed. A post-reopen health failure closes traffic again.

Automatic rollback changes code. Database rollback or restore needs deliberate recovery using the matching dump, uploads/editable files and checkpoint. The previous code must work with the remaining schema before reopening. Maintenance closes new web requests and cooperating job locks prevent overlap. Account for already running requests and other writers during a real data restore.

Provide a manual retained-code rollback command for each environment or a documented safe equivalent. Verify the selected retained artifact, serialize with the same jobs, enable maintenance, switch, health-check and preserve the failed candidate for diagnosis. A repeated deployment of the same SHA retains the earlier useful predecessor.

## Retention

Keep the active release plus its immediate predecessor. Protect all active pointers and shared trees. Prune only owned, identified managed releases and bundles after success. Refuse ambiguous/symlinked/corrupt cleanup candidates.

Keep the latest three verified pre-deploy dumps from successful/resolved attempts for each environment. Preserve pending, failed, interrupted, incomplete and unknown-outcome attempts in addition. Review an unresolved attempt before marking it resolved. Determine retention from recorded snapshot time, environment, checksum and outcome. The active SHA alone cannot classify an old attempt.

Report exact paths and creation purpose in the dashboard/workflow. Pre-deploy database dumps cover the database at deployment time. Off-VM backups cover their separately confirmed scope and schedule.

## First activation and public cutover

First activation checks include the approved data/media/checkpoint, isolated service accounts, backend/TLS/proxy policy, dependencies, authentication and legacy writer handover. Record actual evidence and outstanding owner actions. Restricted activation can precede public opening when authorized. Do all available configuration/parity checks behind the final hostname.

A valid active production installation uses routine automatic preflight thereafter. Generate one-time cutover confirmations only when a new installation needs them. Routine releases retain backup, target identity, artifact, migration, health and rollback checks.

Batch related small changes and test them together. For these human-operated archive apps, prefer around 18:00 Europe/Tallinn after editors finish, with the operator available to verify/recover. Coordinate dependent-service changes with their consumers.

Before the final data export, confirm the old application's edits/uploads and updater are stopped. Preserve the matching original checkpoint. Validate an isolated restore and documented corrections before refreshing selected targets. Verify public access and legacy redirect behavior with representative homepages, path-info routes, languages, encoded paths and query parameters. Keep the old installation for the agreed recovery window.

