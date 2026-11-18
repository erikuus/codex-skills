# First rehearsal bootstrap

The original routine Kaardid deployer expects an existing rehearsal pointer. Implement this first-install wrapper separately in the target repository as `bin/rehearsal-bootstrap`. Its contract is artifact creation, verified transfer/staging, privileged initial activation, then receipt verification.

## Preparation

Complete host provisioning first. The deployment account owns the rehearsal root, releases directory and shared container. Individual shared targets use the app contract's identities and modes, including application-owned writable runtime/media directories. The correct FPM pool/socket exists and is running. Private configuration is readable by that app account. Approved initial data, migrations and shared writable directories are ready. The public site stays on its existing host.

The adapter supplies archive content paths, shared placeholder mappings, probe routes and the actual nginx root. Write generated configuration and the privileged activation helper before asking for private sudo input.

## Wrapper flow

1. Build the selected pushed main commit into a private local artifact directory. Save `release-manifest.json` containing its full commit and `artifact_sha256`. The app contract specifies framework/Composer inputs and artifact inclusions.
2. Create a private remote directory under the app's setup root with `umask 077`. Transfer archive, manifest, shared-map JSON and the reviewed staging helper over verified SSH. Compare local/remote SHA256 for every uploaded file. Record the exact paths.
3. Run the bundled `scripts/stage_release.py`, copied into the target's `ops/`, as the deployment account. For example, after adapting the filenames and roots,
   `python3 ops/stage_release.py --target /srv/example --archive <private-artifact.tar.gz> --manifest <release-manifest.json> --shared-map <shared-map.json>`.
   It validates archive entries/checksum, stages immutable files, connects only empty declared shared placeholders, preserves an identical existing stage and refuses an active rehearsal pointer. It performs no migration, HTTP activation or service operation.
   The wrapper then acquires the app operation lock and runs the contract's initial DB hook against the staged artifact: verify the isolated restored target identity, save/verify its pre-migration dump, apply pending migrations and record the post-check. Reuse the adapted `backup_and_migrate` mechanics for Yii or the standalone ledger runner. An inapplicable local database skips this hook with its recorded reason. Keep the target private and stop before activation on failure.
4. Have the user run the target's reviewed activation wrapper with interactive SSH/sudo. It verifies the staged release, shared links and FPM account/config access, backs up only the app's managed nginx files, syntax-checks and installs the private rehearsal listener. Activate the initial `rehearsal` pointer atomically and run the adapted HTTP/API/static/private-path checks. Restore touched config and the prior pointer state on failure.
5. Read back the pointer, route behavior and completion receipt. Save archive/manifest and successful health evidence in the location expected by the routine deployer/promoter. Subsequent `bin/rehearsal-deploy` uses its normal path.

The supplied Kaardid activation source provides permission, nginx rollback and health-check mechanics. Its fixed paths/health routes require the target adapter. The new wrapper must include artifact staging before calling it.

## Shared-map shape

A shared-map object maps each archive-relative empty directory to an explicit shared target policy. For example,

```json
{
  "apps/example/protected/runtime": {
    "target": "runtime",
    "owner": "example-production",
    "group": "example-production",
    "mode": "2770"
  }
}
```

Resolve owner/group names on the VM and match the declared exact mode. Deployment staging leaves those shared identities/modes intact. Immutable release roots/code retain their deployment-owner and no-group-write checks. Shared targets stay under the environment's ordinary shared container, with symlink and world-write rejection.

Legacy string mappings retain the earlier deployer-owned restricted-directory behavior. Use explicit policies for application-owned or group-writable paths. Prepare and seed targets first. Exclude durable content from the immutable artifact and retain empty placeholders.

## Interruption handling

Before staging completion, retain partial directories for diagnosis and retry in a fresh private stage. A complete existing release must match archive bytes, permissions and shared links exactly before reuse. Conflicting stages stop the operation. The helper serializes first staging with an app-local lock.

After successful initial activation, a retry checks the saved receipt/live pointer and uses routine status/deployment. It must preserve the initialized data, secrets and predecessor. A first activation health failure has no prior app release to invent. Keep rehearsal closed and retain diagnostics.

Exercise first staging, identical retry, interruption, bad checksum, unsafe archive, conflicting content, wrong links and successful initial activation against disposable fixtures before use on a new VM.

