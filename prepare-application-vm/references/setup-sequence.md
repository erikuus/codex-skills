# Inputs, sequence and resume

This is the authoritative setup order. Read it before adapting commands. Later references describe a stage's mechanics.

## Resolve inputs early

| Input | Discover or obtain | Owner and handling |
| --- | --- | --- |
| VM, OS, keys, fingerprint, sudo | Administrator handover, verified SSH and metadata audit | Admin supplies identity, user enters passwords privately |
| Apps and topology | Repositories, entry points, existing vhosts/pools and sibling status | Codex records allocations and preserves unmanaged objects |
| Runtime/build inputs | Python 3.12+ on workstation/VM, PHP/PostgreSQL requirements, locked dependencies, pinned Yii source when used | Run check_python.py with both selected interpreters before helpers; reuse verified tools or acquire from the approved source |
| Data and durable files | Approved dump/source version, media, editable files, corrections and matching job checkpoint | User chooses data source and confirms final writer freeze |
| External stores | Every active DB/ODBC/API dependency, share server/export/protocol and known test file | Administrator supplies grants/mount details and secret-file locations |
| Public identity | Final hostname, backend TLS/SNI/certificates, edge source/header policy, VAU callbacks | Admin owns DNS/proxy/certificates; user completes identity login |
| Monitoring/delivery | Sentry project/integration, notification recipient, app mail transport, critical processes | Discover configured routes and verify delivery to the intended owner |
| Handover tools | Codex CLI, available Pages/GitHub connectors and existing Page IDs | Verify tools early; keep independent repository setup moving |
| Recovery | Database, media/content/checkpoint scope, retention and infrastructure backup owner | Record confirmed coverage and exercise an available disposable restore |

Summarize missing inputs once, grouped by owner. Keep secrets outside this matrix. Null public/DNS or storage details leave unrelated stages available. Resolve a dependency before starting the stage that consumes it.

## Stage order

| Stage | Entry conditions and execution | Completion evidence | Resume/failure rule |
| --- | --- | --- | --- |
| 1. Audit and allocate | Read-only SSH; inspect supplied host and sibling apps | Host identity, occupied resources and validated inventory | Reinspect and preserve existing ownership |
| 2. Prepare host | Approved package plan; sudo for shared dependencies/identities | Versions, pools, sockets, DB privileges and sibling checks | Reuse verified host/operator objects and existing secrets |
| 3. Prepare app | Contract, portable config, durable paths and approved data | Isolated restore/corrections, actual-account file/DB checks | Preserve imports and verify receipts before repeating |
| 4. Bootstrap rehearsal | Built checksum-verified artifact and prepared FPM/config | Initial pointer, HTTP/API health and feature verification | Follow bootstrap.md; routine deploy starts only after this |
| 5. Prepare observation and alerts | Working rehearsal dependency artifact and production identities | Static notifier probe/delivery and per-project action/workflow/dashboard/refresh verification | Complete this separately for every project before dependent activation/timer checks |
| 6. Establish production data | Cutover plan and user confirmation of required writer freeze | Consistent source/checkpoint/content and owner handover | Rehearsal-copy staging can continue while real writers remain elsewhere |
| 7. Verify restricted production | Exact tested artifact and activation inputs from stages 2–6 | Restricted final-host parity, authentication, maintenance and recovery evidence | Public access and production jobs remain separately controlled |
| 8. Start production jobs, if applicable | Production-data writer ownership, dependency checks, fresh backup and dashboard | Supervised completed receipt/checkpoint, then enabled timer and next run | Timer stays disabled until supervised result is verified; check first scheduled run |
| 9. Verify public routing | Owner opens final hostname and legacy redirects | Public features and deep-link/query preservation | Keep recovery window and report unresolved owner actions |

Stage 6 applies before the first production write. A user may authorize restricted production configuration with test data first, with real jobs disabled. Record that data identity and verify the final consistent import before starting production writers.

Routine releases use the established preflight/deployment lifecycle. First-install evidence is recorded once and rechecked when relevant infrastructure changes.

For a multi-project invocation, report each project's Codex handover separately. Verify its TOML actions, repository commands, AGENTS/status/runbook, workflow Page, own dashboard destination and saved refresh. Host setup progress alone leaves those project tasks pending.

## State and retry records

In PROJECT_STATUS.md keep one compact row per app/stage with state, evidence date/location, next command and missing owner input. Use planned, prepared, verified or blocked. Verify actual installed/active state separately. Private reports can contain richer operation receipts.

Scripts save managed object identity and completed-step receipts atomically. On resume, compare receipt, live object and expected parameters. An interrupted restore/import requires inspection or an isolated restart before selection. An interrupted staging extraction can be retried in a fresh private staging directory. An active pointer requires the routine deployment path. Existing secrets retain their values.

Use these readiness levels in the final handover, with evidence per app.

- Host prepared.
- Rehearsal verified.
- Restricted production verified, with data identity recorded.
- Public production verified.
- Recovery and monitoring verified for their recorded scope.

Outstanding infrastructure-owner work retains its owner and evidence gap. Report the achieved level explicitly.

