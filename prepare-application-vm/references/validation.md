# Offline validation

Run `python3 scripts/validate_offline.py` from the installed skill directory. This command checks package integrity, local links and allocations, runs the new disposable fixture tests and the declared self-contained Kaardid regression subset. It uses temporary local directories and child processes, with no live SSH, sudo, service-manager or database operations.

The local suite covers first artifact staging/reuse/conflict, unsafe archives, shared links, active-pointer rejection, lock exclusion, app-role planning across siblings, topology collisions, storage identity/read probes, process deadlines/cleanup and the manual runner using fake VM/Codex executables. It also verifies that the standalone content mapping survives simulated release promotion and rollback.

Focused regressions cover writable shared modes and simulated foreign runtime UID/GID metadata, while immutable roots retain their strict checks. Storage tests include FIFOs and stalled worker/mount commands under the real CLI deadline. Interpreter preflight tests exercise accepted/older versions. Actual separate Unix accounts and network-storage kernel behavior remain Linux integration checks.

Project-handover tests run the generic runner in four isolated project checkouts with fake VM/Codex executables. They verify the selected Page/repository, working directory, evidence transport and absence of forced updater/local-backup parsing for Services. Prompt generation preserves existing human-maintained files. A rendered iipsrv precheck executes a selected local interpreter shim against fake mount metadata and a local image, including executable/script paths containing spaces.

The referenced Kaardid subset covers retention, deployment maintenance/rollback, artifact promotion, updater status and private-configuration generation with fixtures. `assets/reference-requirements.json` distinguishes these tests from assembled-application tests that need a complete Git checkout, framework/runtime or an explicitly disposable database.

Use `scripts/check_package.py` alone for the source hashes, required files, dependency declarations and skill links. It reports unresolved external runtime dependencies rather than pretending to execute them.

## Target acceptance after adaptation

The skill's offline validation establishes helper/package behavior. Before using generated host scripts, test their target-specific configuration and command contracts in an isolated environment.

For shared-host provisioning, create the first app then two siblings and rerun setup. Verify the personal operator role/password/global flags and the first app's roles/grants/files/pools are unchanged. Verify two concurrent setup attempts serialize under the host lock.

For standalone PHP, exercise a complete artifact, real public/admin handlers, migration ledger, editable content/session persistence and mail delivery. For external-data Services, exercise the actual approved dependencies and storage/iipsrv failure contract. Use the approved read-only or disposable targets.

Reboot, real storage loss and recovery-set restore need their own intended test environment and authorization. Record those tests as pending until performed. Skill maintenance or review instructions that prohibit live access take precedence over the normal live setup workflow.

