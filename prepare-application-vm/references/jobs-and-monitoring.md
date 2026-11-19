# Jobs and monitoring

Discover whether this app actually has scheduled work. Create commands/cards for applicable jobs and show intentional absence clearly. Rehearsal stays unscheduled by default.

Install first-use alerting after rehearsal is verified and before production activation when using the original notifier installer. Create the dashboard before a supervised-job result must be verified there. Follow the shared setup sequence.

## Job lifecycle

Inventory the legacy command, account, working directory, runtime, schedule/timezone, side effects, state/checkpoint, outputs and current owner. Prepare app-qualified units. A service definition supplies a proposal. The live status command reports installation and actual behavior.

Use the production active release, production service identity, bounded runtime/resources, restricted writable paths and meaningful failure exits. Missing/invalid checkpoints must fail before work. An unrun oneshot's default success result cannot verify a completed run.

Jobs and deployment share the exact same environment lock contract, including across PHP and Python implementations. Test updater/updater and updater/deployment exclusion in both directions. Kaardid uses exit 75 for a busy updater. A blocked deployment must leave maintenance/database/backup state untouched. Use atomic checkpoint replacement and preserve the old value on API, parse, transport and database failure.

Verify inserts, removals, empty intervals, failure/retry and checkpoint behavior on an isolated database/runtime copy first. For externally hosted data, use fixture or approved disposable targets. Then check real dependencies as the production service account, create a fresh recovery backup and run one supervised production service invocation when authorized. Keep the timer disabled until the durable completion receipt and dashboard agree. Verify the next run and first unattended completion after enabling.

Keep jobs scoped per app on a shared host. Unit installation and schedule changes use their separate privileged command. Routine web deployment leaves unit management to that command. Disabling a timer leaves any currently running service to its own lifecycle. Explain `Persistent=true` catch-up behavior and validate the installed timezone and next execution.

## Structured run summaries

Persist a bounded allowlisted JSON receipt independently of raw diagnostic logs. Include source/manual or timer, started/finished times, outcome/stage, interval/checkpoint before/after, additions/removals or other meaningful work counts and warning counts. Keep a short recent history and aggregates such as the consecutive successful no-additions streak.

Distinguish zero work, unavailable history, failure, skipped lock and running/unfinished work. Show the completed scheduled receipt separately from a manual test. Detect missed triggers and missed completion from the installed schedule and service timeout. Kaardid's daily Tallinn calculation is application-specific. Adapt it for the new schedule and daylight-saving behavior before claiming missed-run coverage.

Checkpoint files are durable job state even when their legacy name ends in `.log`. Rotation applies to diagnostic files according to their configured writer. Keep service reports and deployment console logs at documented private paths.

## Alerts

Reuse an existing Sentry project/rules when appropriate. Preserve the app's environment mapping and filtering and keep secrets private. If the relevant installed Sentry skill/tools are available, use them for setup/verification. Discover actual log routes and avoid replacing them with unrelated defaults.

Use a static systemd failure notifier independent of the app's database/release. Exercise `OnFailure` with a disposable intentionally failing unit and confirm actual accepted delivery/recording. A generated event ID alone cannot prove transport success. Verify the currently installed SDK contract and failed-transport behavior.

Provision the selected locked Sentry SDK explicitly for an app without an existing integration, or use its approved existing error-delivery mechanism. Verify one real application-error probe, backend recording and actual notification to the intended recipient. Record SDK/runtime acquisition and installed notifier ownership separately. A static notifier test does not verify the web route.

Discover application mail use. Nimeregister's report action needs a configured local sendmail-compatible transport or its selected relay integration. Reuse administrator-provided mail settings, configure approved sender/relay details privately, and send a harmless marked test through the real application to the intended recipient. Record transport acceptance and recipient receipt.

For apps with no scheduled job, monitor web errors and their critical processes/storage. Services needs mount identity/known-file and iipsrv/socket visibility. Each check records its observation time, result, owner and whether detection is manual or independently alerted.

Document owners and coverage. Manual dashboard refresh can flag missed runs at observation time. Independent uptime/missed-run alerts require their own configured mechanism. Add such automation when requested or part of the agreed setup scope and record what it actually checks.

## Backups

Mihkel's November email states whole-VM backups plus separate database backups. Preserve that owner confirmation as policy evidence. Confirm specific coverage for uploads/editable content, external mounts, checkpoints, retention and exercised restores separately. A locally readable deployment dump proves local archive readability. Record each level of evidence precisely and keep infrastructure-owned backup work assigned to its owner.

