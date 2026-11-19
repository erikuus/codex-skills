# Consistent recovery

A deployment dump and a full recovery set have different scopes. Keep routine pre-deploy dumps and their three-verified-plus-unresolved retention. Use infrastructure backup references or explicit captures for the remaining durable components.

## Record a recovery set

For each app/environment record a private manifest with snapshot identifier/time, app release, database dump/checksum or external backup reference, durable media/content snapshot references, checkpoint value/file checksum, capture method, writer freeze boundaries and restore owner. Cache/session state can be deliberately disposable, with the user-visible consequence recorded.

For Nimeregister include editable `content/` and the database. For checkpointed jobs include the checkpoint that agrees with that database interval. For Services record remote DB and file-server owners plus version/backup references, along with local configuration/code and any durable app state.

## Capture and restore procedure

Generate project commands in the runbook for these concrete stages.

1. Identify the intended recovery set and confirm scope/authorization. Close web writers and pause applicable timers. Wait for current jobs to finish and acquire the operation lock. Account for other clients that can write the same data.
2. Capture database and durable files under the agreed consistency boundary, or obtain matching owner-managed snapshots. Save checksums and a manifest atomically. Resume writers only after capture verification.
3. Restore into a disposable database and separate content/runtime directories first. Apply grants and verify counts, migration ledger, representative content, media availability and checkpoint agreement. Record which components were actually restored.
4. For deliberate target recovery, repeat writer closure/lock ownership, preserve the current failed state, restore into replacement targets and verify them before switching. Use the retained compatible release and the selected recovery-set references. External DB/file-server restoration stays with its authorized owner.
5. Restore the real matching checkpoint atomically with correct ownership. Run read-only app/API checks under maintenance, verify editable content, migration compatibility and dependency health, then reopen web access. Reenable jobs only after the restored checkpoint/interval is reviewed and one supervised run is appropriate.

Record exact per-project commands and private manifest paths. Avoid an automatic database restore inside code rollback. Post-deployment writes may exist and need an operator decision.

Use a local disposable fixture for orchestration and preservation tests, then an isolated real DB/content restore when those inputs are available. Confirm off-VM coverage and restore evidence with Mihkel without assigning unconfirmed infrastructure work to the app deployer.

