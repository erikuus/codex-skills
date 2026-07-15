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

Before implementing or changing the overview renderer, also read [references/overview-template-contract.md](references/overview-template-contract.md) and use [assets/overview.html.template](assets/overview.html.template) as the required visual and interaction baseline.

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
overview.template.html
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
4. Copy and minimally adapt `assets/overview.html.template` to project-root `overview.template.html`; preserve its structure, visual system, data element, controls, and responsive behavior.
5. Write a deterministic Python CLI using only the standard library unless the project already uses another runtime.
6. Add creator and evaluator automation instructions as explicit Markdown files.
7. Add tests and run them.
8. Render or refresh `overview.html`.

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

Use the bundled overview template instead of inventing a new dashboard. The template establishes the `my-life`-style warm editorial presentation:

- compact header with loop title and freshness/count metadata
- searchable, sortable candidate list in a narrow left pane
- calm reading pane for the selected candidate
- serif candidate prose with restrained sans-serif operational metadata
- status dots, winner/shortlist markers, score bars, rationale, warnings, and file paths
- loop metadata popover with full input/criteria hashes and queue counts
- responsive single-column behavior below `800px`

The project CLI must render `overview.html` from project-root `overview.template.html`, replacing `__LOOP_TITLE__` and `__OVERVIEW_DATA_JSON__` exactly as specified in the overview template contract. Do not make generated projects depend on the installed skill path at runtime. Preserve the content-security-safe rules: HTML-escape the title, JSON-encode the payload, replace `</` with `<\/`, and render all payload strings through the template's `esc()` helper.

Adapt nouns and optional fields to the loop, but do not remove search, time/score sorting, candidate selection, metadata visibility, empty states, or mobile layout. Keep it dependency-free and usable when opened directly as a local file. Polling for refreshed content may fail under `file:` URLs and must fail silently.

Regenerate it after candidate submission, evaluation recording, promotion, invalidation/staleness changes, and manual `render-overview`.

## Validation

Before reporting completion, run relevant tests. Minimum expected tests:

- malformed candidate rejected
- malformed evaluation rejected
- evaluation for unknown candidate rejected
- stale candidate/evaluation cannot replace winner
- strictly higher score promotes
- lower or tied score preserves incumbent
- pending queue advances
- overview template tokens are fully replaced and the embedded JSON cannot break out of its script element
- `overview.html` renders and contains winner/shortlist, candidate, hash, score, verdict, status, rationale, and pending/invalid/stale data
- overview search, time/score sort, selection, empty state, and narrow-screen layout remain present

## Completion response

Return links to `LOOP.md`, the CLI, automation files, tests, and `overview.html`. State exactly what was validated. If automations are present but not scheduled/enabled, say so directly.
