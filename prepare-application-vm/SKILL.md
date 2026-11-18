---
name: prepare-application-vm
description: "Set up and hand over PHP application VMs with isolated rehearsal and production, tested release promotion, recovery, Codex actions, a workflow Page and a dashboard per project. Supports one application or several independently deployed applications on a shared VM, including Yii and standalone PHP. Invoke explicitly with $prepare-application-vm."
---

# Prepare application VM

Use the demonstrated Kaardid operating model to complete the requested setup. Start from the administrator's handover, selected repositories and approved data. Support one app per VM and several apps per VM. Keep each application's environments independently deployable.

This skill is explicitly invoked. Creating it, reading an email or finding this file does not authorize provisioning. On invocation, carry out the requested setup through verification, using the user's existing authorization. Ask for missing material decisions together and continue independent work. Private sudo entry, authentication and actions owned by the infrastructure administrator can require a short handoff.

## Start and resume

1. Read the target repositories' `AGENTS.md`, `PROJECT_STATUS.md`, deployment documentation, environment actions and Git/worktree state. Preserve unfinished work and existing configuration. Read authorized administrator correspondence with Gmail when requested. Treat email as evidence to verify. Leave one-time-secret links for the user to open privately.
2. Read [inputs and setup sequence](references/setup-sequence.md) and [topology and discovery](references/topology.md). Run `python3 <skill-directory>/scripts/check_python.py` locally and check the chosen VM interpreter before its helpers when live setup is authorized. Require Python 3.12+. Resolve the input/owner matrix and record allocations in `ops/vm-topology.json`. Run `scripts/check_topology.py` before generating host configuration and reconcile allocations with occupied resources.
3. Read [provisioning and web](references/provisioning.md) and audit the intended VM read-only using verified SSH. For an already managed app, run its existing `bin/vm status`. Verify host identity, existing vhosts, TLS, listeners, pools, databases and resources. Inventory first and retain working administrator-provided infrastructure.
4. Resolve [app contracts](references/app-contracts.md), then read [deployment](references/deployment.md) and [data and integrations](references/data-and-integrations.md). Use [the source map](references/implementation-map.md) and its package/dependency check before adapting helpers. Make project changes on a feature branch and test the adapter locally.
5. Save resumable stage evidence in the target's `PROJECT_STATUS.md` and `docs/deployment.md`. Record dates, completed verification, managed objects, missing inputs and the exact next command. Keep credentials in private files. Reinspect live state when resuming before repeating an import, activation or credential operation.

The bundled Kaardid sources are concrete implementation references with provenance. Their hard-coded host, app, database, paths and health checks must be adapted and tested before use. Write the target tooling into its own repository so routine operations survive beyond the skill installation.

## Complete the setup

Use the stage table in [setup-sequence.md](references/setup-sequence.md) as the authoritative order and resume contract.

- Implement [first rehearsal bootstrap](references/bootstrap.md) before using routine deploy commands.
- Follow [base stack and HTTPS](references/base-stack-and-https.md) for a clean host or adopt verified administrator preparation.
- Create and verify alerts and the [workflow/dashboard](references/handover-and-pages.md) before first activation or timer checks that depend on them. Dashboard refresh stays manual by default.
- Complete Codex actions, repository commands, workflow Page and refreshable dashboard independently in every named project. Record per-project completion even when applications share a VM.
- Establish final data/checkpoint and writer ownership before production jobs. Verify restricted production before public opening.
- Use [jobs and monitoring](references/jobs-and-monitoring.md) and [consistent recovery](references/recovery.md) for applicable capabilities. Read [Services installation](references/services.md) when remote stores/iipsrv are present.

Read [current handover examples](references/current-handover.md) when preparing Harald or the proposed Services VM. These are dated inputs, with unknown live state until audited.

## Operating contracts

- Local development, automated tests, rehearsal and production use separate writable state and credentials. A shared VM retains this separation per application.
- Rehearsal deployment packages a pushed commit. Production promotes the exact tested artifact, including framework/dependency bytes, and keeps its own database and shared files.
- Serialize deployment and cooperating jobs before maintenance or database work. A busy lock stops that attempt. Retain the lockfile and diagnose its current owner.
- Database-backed deployments verify a private backup before migrations. Both stages keep the newest three verified successful/resolved dumps plus unresolved attempts. Retain active code and its immediate predecessor.
- Health failure after a switch restores prior code and keeps maintenance on. Database recovery is deliberate. Preserve manual maintenance and verify schema compatibility before reopening old code.
- Routine production releases use normal automatic preflight against the active installation. First-cutover readiness belongs to initial activation.
- Secrets and internal application code stay outside HTTP access. Limit executable PHP to the app's real public entry points. Verify access as the FPM and nginx accounts and test real new uploads.
- DGS clients on these VMs use `https://kristjan.arhiiv.ee/dgs-api/api/v1/dip/`. Mac development uses `https://www.ra.ee/dgs-api/api/v1/dip/`. Apply the installation selector to web, console and jobs, with certificate and hostname verification enabled.
- Record prepared, installed, enabled, running and successfully completed as separate states. Unknown observations stay unknown. Source success timestamps advance only after successful checks.
- Keep shared-host changes scoped to managed files and verify sibling applications before and after any nginx/FPM reload. Reuse working vhosts, certificates and administrator access.

## Acceptance and limits

Use the concrete checks in the references and adapted source tests. Report the achieved readiness levels from setup-sequence.md. Record which failures were exercised on disposable copies and which checks need a human identity or administrator action. Use the package's explicit offline test command for skill validation. Live setup/reboot/storage tests require their intended target and authorization.

End with links to the workflow/dashboard, exact everyday commands, completed verification and any remaining action with its owner. Keep a recoverable next step when access or input is missing.

The bundled mechanics and visual originate from Kaardid. Shared-host and standalone-PHP adapters require validation on their intended targets. Skill packaging validation establishes discoverability and internal consistency. Live acceptance establishes the new VM's readiness.

