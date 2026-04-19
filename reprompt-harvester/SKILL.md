---
name: reprompt-harvester
description: Harvest a finished coding thread into project-root DEVLOG.md for projects that keep PLAN.md, DEVLOG.md, and SPEC.md. Use when the user wants to finalize a thread into project docs, harvest a finished thread, or backfill a dev log from the current thread or archived Codex session .jsonl files.
---

# Reprompt Harvester

## Role

Act as a project change harvester.
Convert a finished thread into one append-only `DEVLOG.md` entry that captures what the thread actually delivered.
Do not write abstract learnings.
Do not inspect repo code.
Do not rewrite prior devlog entries.

## Input

- A target project root or explicit `PLAN.md` path
- One source thread:
  - the current live thread, or
  - one or more archived Codex session `.jsonl` files

The target project keeps these files at project root:

- `PLAN.md` - original vision, never rewritten here
- `DEVLOG.md` - append-only history, written here
- `SPEC.md` - current-state specification, never touched here

## Workflow

1. Resolve the target project path and locate `PLAN.md`.
2. Use thread content only. Do not inspect code, tests, or docs outside the supplied thread transcript.
3. If the source is an archived `.jsonl`, extract the session id, timestamp, and source path from the transcript metadata when available.
4. If the source is the live thread and no stable session id exists, require an explicit short user label for the entry.
5. Read existing `DEVLOG.md` only to preserve append-only formatting and prevent duplicate session ids or duplicate live-thread labels.
6. Harvest only the net durable outcome of the thread:
   - implemented additions or edits
   - explicit removals or narrowed behavior
   - accepted decisions that changed the product or documentation set
7. Ignore abandoned ideas, intermediate experiments, speculative discussion, and requests that were not clearly carried through by the end of the thread.
8. Append exactly one entry per harvested thread. If the thread produced no durable project change, append nothing.

## DEVLOG Entry Format

Append entries in this shape:

```md
## 2026-04-19 14:35 EEST - admin-ordering-pass

- Session ID: 019d87b3-bafc-7c03-bb52-63ce2518a20f
- Source: /Users/erikuus/.codex/archived_sessions/rollout-2026-04-13T19-36-36-019d87b3-bafc-7c03-bb52-63ce2518a20f.jsonl

### Summary
- Short factual outcome line.
- Short factual outcome line.

### Implemented
- Concrete shipped addition or edit.

### Changed or Removed
- Prior behavior or plan item that was replaced, narrowed, or removed.

### Affected Areas
- Feature, screen, domain, or doc area.

### Open Questions
- Include only if the thread ended with an explicit unresolved item.

### Spec Notes
- Normalized statement suitable for later synthesis into SPEC.md.
```

Omit `### Open Questions` when there was no explicit unresolved item.
If no stable session id exists, replace `Session ID` with `Label`.

## Extraction Rules

1. Write factual, current-language statements, not narrative recap.
2. Prefer what was finally accepted or delivered over what was merely discussed.
3. Record supersession explicitly in `Changed or Removed` when the thread altered or removed previous behavior.
4. Keep `Summary` to 2-5 short lines.
5. Keep `Spec Notes` normalized and synthesis-friendly.
6. Do not touch `PLAN.md` or `SPEC.md`.

## Quality Filter

Before appending an entry, verify all are true:

- The thread produced a durable project change.
- The entry reflects the final thread outcome rather than intermediate exploration.
- The entry is not a duplicate of an existing session id or live-thread label.
- The entry can be understood later without reopening the thread.

Discard uncertain or speculative candidates.

## End Condition

After appending, report whether `DEVLOG.md` changed and identify the appended entry label or session id.
