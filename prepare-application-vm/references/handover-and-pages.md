# Developer handover and Pages

Each project needs its own practical workflow Page and visual dashboard, even on a shared VM. Store their real Page IDs/links in `PROJECT_STATUS.md`. Reuse existing Pages and preserve human edits. Use the Pages write-page/maintain-space skills when available. If unavailable, finish repository tooling and keep the Page creation step explicit.

For Harald, complete this independently in Aadresslehed, Pitserid and Nimeregister's existing Codex projects. Services has its own project. Keep a compact per-project handover row with checkout/action-file path, deploy/status/refresh commands, workflow Page ID, dashboard Page ID and verified refresh result. A shared-host inventory can support all three apps while each project retains its own actions and Pages.

## Codex actions and access

Configure the target's local `.codex/environments/environment.toml` through the supported environment/action mechanism when available. Inspect existing actions first and preserve them. The command field should run a repository-owned executable with the correct working directory. For a direct file edit, preserve the file format, machine-specific paths and current definitions and verify the actions in Codex.

Create actions that work independently of this chat.

Preserve the existing development actions and ports discovered on 19 November: Aadresslehed PHP/8001, Pitserid PHP/8004, Nimeregister Run/8003 and Services PHP/8006 with its demo document root. Reinspect them before setup. Add operational actions to each project's TOML while preserving these definitions. Verify action working directories and that commands select their intended app/environment.

| Action | Contract |
| --- | --- |
| PHP | Target's local development entry point/router and unique local port |
| Deploy rehearsal | Pushed main artifact, backup/migrations when applicable, maintenance and health verification |
| Deploy production | Exact tested rehearsal SHA, routine preflight and separate production state |
| Rehearsal web tunnel | Unique loopback local port forwarded to that app's private rehearsal |
| Rehearsal database tunnel | Database tunnel when this app has a managed database |
| VM status | Read-only current app/environment/jobs/backups metadata |
| Refresh dashboard | One manual observation and verified save to the existing Page |

A tested reference production command is `bin/production-deploy --deploy "$(git rev-parse HEAD)"`. It works only when HEAD is the successfully tested rehearsal artifact. Provide an explicit full-SHA terminal alternative using the rehearsal Active release value from VM status. A native combined `--deploy` mode can wrap preparation then activation, preserving resumable lower-level commands. Keep first-cutover confirmations out of routine releases.

Configure intended desktop pgAdmin/SFTP access as needed. Verify actual database/current user/privileges. Have the user enter private passwords directly. A database tree label and the existence of a connection definition establish no read/write guarantee. Existing managed web pgAdmin requires its own reachable VM host and TLS policy. SFTP needs the verified SSH route, while web and database tunnels are independent.

## Everyday workflow Page

Use a concise human tutorial with the project's exact commands, URLs, database names and paths. Keep deploy sections action-oriented. Put the shared deployment lifecycle, maintenance, automatic code rollback and deliberate DB recovery explanation together once.

Cover starting local work, testing, branch/review/merge, deploying pushed main to rehearsal, feature testing, identifying the tested SHA, routine production deployment, manual rollback, log paths, private settings, trusted-IP rules when used, maintenance, media/editable data, dumps and their three-verified-plus-unresolved retention, applicable job checks and finishing work. Batch related releases and prefer after editors finish, around 18:00 Tallinn for these archive apps.

Keep long first-launch work in the dashboard's temporary numbered production steps. Remove completed launch items and the initial warning after public verification. Preserve a short durable workflow thereafter.

## Dashboard and manual refresh

Create one visual-first project dashboard with Development, Rehearsal and Production cards. Include jobs and pre-deploy backup cards where applicable. Show exact dump directories, what creates them and how retention works. Keep launch steps as a short numbered list while needed. A retired production preview does not need a current card.

The actual Kaardid Page HTML is bundled in `assets/dashboard/kaardid-status-overview.html`. Use it as the responsive implementation reference, adapting title, environments, job fields, hard-coded database/path/backup labels and health claims. It is a starting point for relevant cards. Apps without Kaardid-style updater metrics need an adapted view and clear inapplicability for local dumps. Use the Visualize skill's current creation guidance when changing its implementation.

Implement `bin/vm status` as a read-only app-scoped status command. A host may report all installed app timers, clearly tagged by owning app, while each project dashboard selects its own jobs. Include pointer/previous/maintenance, HTTP probes, prepared versus installed/enabled/running jobs, installed schedule, completed timestamped results/next run and local backup metadata. Read only allowlisted structured summaries. Avoid raw logs, private settings and application rows during monitoring.

The manual runner collects VM status once using the existing verified connection, then passes that receipt to a bounded Codex execution with Pages/GitHub tools. Keep its refresh instructions in `ops/dashboard/refresh-prompt.md` inside the target repository. The button must continue working when no scheduled task exists. Use automatic review for the scoped Page write when available and verify the save before reporting success.

Copy the revised `assets/runtime/refresh-dashboard` into the target bin directory and `assets/runtime/run_bounded.py` into ops. The runner gives the VM collection 60 seconds and bounds the whole observation/agent phase to about five minutes, with process-group cleanup. Check the CLI and connector availability early. Actual authenticated Pages/GitHub access is verified during the headless run and recorded in the receipt. Timeout/expired-auth results remain incomplete until saved state is read back. Preserve prior source success times on failures.

The runner transports an opaque receipt containing source, attemptedAt, succeeded and evidence. It supplies no application name, Page ID, repository, job schema or backup parsing. Those belong to the project's prompt.

For a new prompt use `assets/dashboard/refresh-prompt.md.template` with `scripts/create_refresh_prompt.py`. Supply the actual application, dashboard Page ID, verified owner/repository, visualization title and a status-interpretation text file. The helper creates `ops/dashboard/refresh-prompt.md` exclusively, preserving an existing file. For example, run `python3 <skill>/scripts/create_refresh_prompt.py --application <app> --page-id <actual-Page-ID> --repository <owner/repo> --overview "<app> status overview" --status-file <project-status-contract.txt> --output ops/dashboard/refresh-prompt.md`. Review the resolved destination before the first save.

Define parsing from the project's real VM status output. Include updater JSON, checkpoint and dump parsing only for apps exposing those observations. Services can describe external-store, mount and iipsrv health with local DB/updater capabilities marked inapplicable. Preserve compatible visual state fields without inventing unsupported metrics.

The original Kaardid refresh prompt is a provenance reference with its own Page ID/repository. Generate a fresh project prompt and verify destination isolation. Before marking each project's Codex handover verified, run its refresh from that project's action or absolute command and read back its own Page. Check all three Harald projects separately.

Store observation/source attempt and last-success timestamps as ISO UTC and display Europe/Tallinn. Update observation time even if values match. Preserve success times on source failure and mark dependent values unreachable/unknown. The visual marks evidence older than two hours stale. Distinguish Git main, local changes/worktrees, merged work, deployed SHA and tested behavior. Documentation/tooling ahead of deployed application code alone is compatible with a healthy deployment.

Read Page editing view, copy the full `metadata.visualization_state` envelope, change only `state.modelContent` and use guarded `set_block_metadata`. Preserve `file_id`, `privateContent`, unrelated fields/blocks and native edits. Read back to verify. An uncertain write requires reconciliation before retrying. Data refresh leaves HTML untouched.

Keep schemaVersion 1 when adapting the existing visual and preserve unknown fields. The reference has VM/repo/GitHub/Pages attempt/success/reachable fields, rehearsal, production, backups, development, timers, updater and `monitor`. Manual mode sets `monitor.active=false` and `cadence="Manual"`. Keep all updater counters, nulls and recent receipts exactly as observed. Match field names between status, refresh prompt and visual.

A Page prompt starts a chat. The existing Pages surface provides no verified generic button that directly executes a Mac shell command. Use the project action or an absolute terminal command in Page prose. Implement Page-triggered execution only through a supported, explicitly verified integration. Create schedules only at the user's request.

## Durable handover

Keep `AGENTS.md` routing new chats to `PROJECT_STATUS.md` and read-only VM status. The status owns the environment map, operational decisions, external owners and current remaining work. Avoid embedding a quickly stale release SHA there.

The runbook holds the exact setup, privilege, configuration, data, unit management, promotion, restore and diagnostic commands. Store private reports outside Git/Pages. Record each completed setup stage with time/evidence and the safe next command. Prepared, installed, active and verified remain separate states.

Use the source Pages as examples of practical voice and useful layout. Correct known historical drift when producing the new project's content. The old workflow still contains renamed-repository links and obsolete paused-hourly/unlimited-production-dump wording. The current commands, runbook and verified policy supply the updated behavior.

