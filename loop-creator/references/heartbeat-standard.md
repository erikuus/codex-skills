# Heartbeat Loop Standard

Use this only as a compact implementation reference. The canonical local example is `/Users/erikuus/dev/philosophy/my-life/`, but new loops should be simpler: one root `input.md`, one root `criteria.md`, one queue, one state file, and one `overview.html`.

## Heartbeat

One cycle is:

1. `prepare-creator` copies/summarizes only allowed creator context into `creator/workspace/`.
2. Creator automation writes one candidate.
3. `submit-candidate` validates, IDs, archives, and queues it.
4. `next-pending-candidate` or `prepare-evaluator` exposes exactly one queued candidate plus `criteria.md`.
5. Evaluator automation writes one JSON evaluation.
6. `record-evaluation` validates, archives, updates winner/shortlist, advances queue, and refreshes `overview.html`.

## State model

Keep state small:

```json
{
  "schema_version": 1,
  "input_hash": "...",
  "criteria_hash": "...",
  "winner": null,
  "shortlist": [],
  "pending": [],
  "evaluated": [],
  "invalid": []
}
```

If `input.md` or `criteria.md` changes, the helper script should detect hash drift. Old candidates remain archived but cannot win under the new hashes.

## Promotion

Default scalar rule:

- reject hard failures first
- accept only evaluations with valid schema and integer `final_score` from `0..100`
- promote only when `final_score` is strictly higher than the incumbent
- preserve incumbent on ties

For multi-dimensional criteria, keep a top 5 shortlist sorted by final score, with ties preserving earlier candidates. Do not introduce Pareto logic unless the user explicitly leaves this simple heartbeat skill.

## Automation files

`creator/automation.md` should say:

- read only prepared files in `creator/workspace/`
- produce exactly one candidate
- do not inspect project state, criteria, evaluations, overview, or archive
- submit through the CLI command provided by the loop

`evaluator/automation.md` should say:

- read only prepared evaluator files
- judge the one candidate against `criteria.md`
- output JSON matching `evaluation.template.json`
- do not inspect winner state, previous evaluations, or other candidates
- record through the CLI command provided by the loop

## Overview

Copy `assets/overview.html.template` from the skill to project-root `overview.template.html` and follow `references/overview-template-contract.md`. The finalizer renders the self-contained `overview.html`; the generated project must not read the installed skill directory at runtime.

The overview should be useful without reading raw JSON. It should show:

- winner/shortlist
- score history
- pending/evaluated/invalid counts
- candidate excerpts
- rationale excerpts
- hash/version warnings

Keep it static. Do not require a web server.
