---
name: loop-creator
description: Create simple heartbeat candidate loops with exactly one input file, one criteria file, repeated candidate generation, repeated candidate evaluation, required creator/evaluator automations, and a static overview.html site. Use when the user wants a wit-loop or my-life-style loop where a creator produces candidates from input.md, an evaluator scores candidates against criteria.md, deterministic code archives results and updates the current best/shortlist, and an HTML overview shows progress. Do not use for complex executable transformation optimization or broad generic optimizer design.
---

# Loop Creator

## Scope

Create one simple heartbeat loop pattern:

```text
input.md -> creator automation -> candidate
candidate + criteria.md -> evaluator automation -> evaluation
evaluation -> deterministic finalizer -> state + overview.html
repeat
```

This skill is intentionally narrow. Do not design a universal optimizer, executable-transformation benchmark, hidden holdout system, relationship optimizer, or broad decision framework. If the user asks for those, state that this skill is not the right abstraction and switch to focused conversation outside this skill.

Use `/Users/erikuus/dev/philosophy/my-life/` as the local implementation standard for structure and operational behavior, simplified to one `input.md` and one `criteria.md`.

Before implementing a loop, read [references/heartbeat-standard.md](references/heartbeat-standard.md) for the compact operational standard.

## Required loop properties

Every generated loop must include:

- exactly one human-maintained `input.md`
- exactly one human-maintained `criteria.md`
- multiple immutable candidate files
- multiple immutable evaluation JSON files
- a deterministic CLI/helper script for submission, validation, winner/shortlist update, and overview rendering
- a creator automation prompt/workspace that can read `input.md` but not `criteria.md`, evaluations, state, or prior candidates unless the user explicitly allows mutation
- an evaluator automation prompt/workspace that can read one pending candidate and `criteria.md` but not winner state, prior scores, or unrelated candidates
- a static `overview.html` website showing input/criteria hashes, candidates, scores, current best or shortlist, pending count, and recent activity
- tests for candidate validation, evaluation validation, promotion, stale input/criteria hashes, and overview rendering

## Standard project layout

Use this layout unless the target project already requires a small naming adjustment:

```text
LOOP.md
input.md
criteria.md
overview.html
bin/<loop_name>_loop.py
creator/
  automation.md
  workspace/
    input.md
    candidate.template.md
evaluator/
  automation.md
  evaluation.template.json
  workspace/
    candidate.md
    criteria.md
candidates/
  README.md
  pending/
  archive/
evaluations/
  README.md
state/
  README.md
  loop_state.json
tests/
  test_<loop_name>_loop.py
```

Do not add `runner/`, dataset splits, holdouts, Pareto-frontier machinery, dependency sandboxes, or executable candidate support.

## Focused conversation

Ask only for facts needed to instantiate the heartbeat loop. If a reasonable default exists, propose it instead of blocking.

Ask at most one material question per turn. Prioritize in this order:

1. What is the candidate artifact? Example: “one witty sentence,” “one life scenario package,” “one product-name list.”
2. What must the candidate file structure be?
3. Should selection keep only a single best candidate or a small shortlist?
4. What score scale and promotion rule should be used?
5. What cadence should the creator and evaluator automations use?

Recommended defaults:

- candidate format: Markdown
- selection: single incumbent winner for scalar criteria; top 5 shortlist when criteria are multi-dimensional
- score scale: integer `0..100`
- promotion: strictly higher validated score replaces incumbent; ties preserve incumbent
- cadence: creator and evaluator both run repeatedly, but only after manual CLI tests pass

## Design rules

Keep creator and evaluator roles separate:

| Actor | May read | May write | Must not read |
|---|---|---|---|
| Creator automation | `input.md`, candidate template, public candidate contract | one new candidate draft/submission | `criteria.md`, `evaluations/`, `state/`, `overview.html`, prior candidates unless mutation is explicitly enabled |
| Evaluator automation | `criteria.md`, one pending candidate, evaluation template | one evaluation JSON | current winner, prior scores, unrelated candidates |
| Finalizer CLI | candidate archive, evaluation JSON, state | `state/loop_state.json`, `overview.html` | no cognitive restriction; deterministic code only |
| Human | all files | `input.md`, `criteria.md`, automation enable/disable decisions | none |

Enforce important boundaries with workspace files and helper commands, not prompt wording alone. The helper script should prepare narrow creator/evaluator workspaces.

## Implementation rules

When asked to implement a loop:

1. Inspect any provided project and existing files first.
2. Create or update the standard layout.
3. Write `LOOP.md` from `assets/LOOP.md.template`.
4. Write a deterministic Python CLI using only the standard library unless the project already uses another runtime.
5. Add creator and evaluator automation instructions as explicit Markdown files.
6. Add tests and run them.
7. Render or refresh `overview.html`.

The CLI should normally support:

```text
prepare-creator
submit-candidate --candidate <path>
next-pending-candidate
prepare-evaluator
record-evaluation --evaluation <path>
render-overview
show-state
```

State must include hashes of the current `input.md` and `criteria.md`. A candidate or evaluation created under old hashes must be archived but not allowed to win.

Candidate IDs should be content-addressed. Evaluation files should include candidate ID, input hash, criteria hash, raw scores, final score, verdict, rationale, and evaluator identity/version if known.

## Overview website

`overview.html` is a required first-class output, not an optional report. It should be static and self-contained. Include at minimum:

- loop name and last rendered time
- current input and criteria hashes
- current winner or shortlist
- all evaluated candidates with score, verdict, status, and links/paths
- pending candidates
- invalid/stale candidates
- recent evaluation rationale excerpts

Regenerate it after candidate submission, evaluation recording, promotion, and manual `render-overview`.

## Validation

Before reporting completion, run relevant tests. Minimum expected tests:

- malformed candidate rejected
- malformed evaluation rejected
- evaluation for unknown candidate rejected
- stale candidate/evaluation cannot replace winner
- strictly higher score promotes
- lower or tied score preserves incumbent
- pending queue advances
- `overview.html` renders and contains the winner/candidate data

## Completion response

Return links to `LOOP.md`, the CLI, automation files, tests, and `overview.html`. State exactly what was validated. If automations are present but not scheduled/enabled, say so directly.
