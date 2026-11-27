---
name: verification-skill
description: Create or maintain a project-local Codex skill for proving user journeys on the running application. Use for a new verification workflow, a pilot, a changed-journey review, or a full verifier audit.
---

# Verification skill

First establish whether the request is to create a verifier, run an existing journey, or audit the verifier itself. An ordinary request to test a change can use the existing project verifier directly.

## Create and pilot

1. Interview the checkout. Read its agent instructions, acceptance contract, runbook, test configuration and actual specs. Identify the entry point a user exercises and follow it to the system that handles the request. A local page can call a deployed service. Read the effective URL, backend selection, database or fixture, auth prerequisite and isolation rules.
2. Inventory working commands. Prefer an existing browser spec, service client, CLI, fixture, or query. Add a small helper only when a recurring operation is missing or fragile. Respect the repo's worker count, shared database and test transport. If startup or data is unavailable, record the missing prerequisite and the coverage still possible.
3. Write or update the repo's verifier in place. For a new Codex verifier use `.agents/skills/verify-<app>/SKILL.md`. Include launch, a read-only readiness and target check, how to drive the real entry point, the expected side effect, evidence location and teardown. Map a few important journeys to the canonical requirements and runnable commands. Link to existing QA material and retain its authority. Short maps can live in the skill itself.
4. Pilot one mapped journey. Capture the action and the user-visible result. For a save, check a fresh read and the stored row or file. Record any external boundary exercised through a fake. If the named target cannot be driven, qualify any result from a substitute. Stop the processes you started, remove only your fixtures, and verify both cleanup and the continued availability of evidence.
5. Report the exact journey, target, observation and proof location, plus the bounds of coverage. A feature in the map is only a candidate until exercised. For a bug follow [reproduce and retest](references/reproduction.md). For a performance claim use [measure a change](references/performance.md).

## Maintain

For a changed-journey review, use the diff since the relevant revision and follow affected links, entry points and test helpers. For a requested full audit, enumerate every mapped journey, reconcile the index against the current app, and give each journey a live result or a specific blocker. Use one browser driver for shared state. Reuse setups across compatible checks.

Compare the written requirement, current implementation and observed outcome. Correct stale instructions or a broken verifier under its own ownership, and re-run the corrected recipe. If observed behavior violates an acceptance criterion, report a product regression separately. Preserve the criterion. Describe which journeys ran, which could not run and why. Keep branch, PR and recurring-schedule choices with the task that requested them.
