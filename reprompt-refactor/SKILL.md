---
name: reprompt-refactor
description: Rebuild project-root SPEC.md from PLAN.md, DEVLOG.md, and current repo truth. Use when the user wants to synthesize the current implemented specification, rebuild SPEC.md, or reconcile the original plan with what the app actually became.
---

# Reprompt Refactor

## Role

Act as a project specification synthesizer.
Rebuild `SPEC.md` from the original plan, the append-only development log, and current repo validation.
Do not rewrite `PLAN.md`.
Do not curate or prune `DEVLOG.md`.

## Input

Use:

- `PLAN.md`
- `DEVLOG.md`
- Current repo truth as needed, including code, tests, routes, schemas, configs, `README.md`, and walkthrough docs

## Output Target

Rewrite `SPEC.md` from scratch.
Treat `PLAN.md` as initial intent, `DEVLOG.md` as change history, and repo truth as the final arbiter of what currently exists.

## Refactoring Rules

1. Start from `PLAN.md` to understand the original target product and terminology.
2. Read `DEVLOG.md` chronologically and treat later entries as superseding earlier ones when they conflict.
3. Inspect the repo to validate what is actually implemented now.
4. Prefer repo truth over plan or devlog when they diverge.
5. Include only implemented current-state behavior.
6. Exclude features that were planned but never built.
7. Exclude features that were added and later removed.
8. Mention explicit exclusions only when needed to prevent old plan assumptions from reappearing.

## SPEC Shape

Ensure `SPEC.md` covers:

- Purpose and audience
- Implemented user roles and access model
- Current product flows and feature behavior
- Key business rules and constraints
- Current data concepts and important admin or content entities
- Key technical invariants that materially affect behavior

Keep the document product-facing and implementation-aware, not a code walkthrough.

## Workflow

1. Resolve the target project root and confirm `PLAN.md` and `DEVLOG.md` exist.
2. Read `PLAN.md` for intended scope and vocabulary.
3. Read `DEVLOG.md` for chronological change history and supersessions.
4. Inspect repo truth only as needed to settle what is currently implemented.
5. Rewrite `SPEC.md` from scratch in a clean, stable structure.
6. Do not copy `PLAN.md` or `DEVLOG.md` verbatim.
7. Do not rewrite `PLAN.md` or `DEVLOG.md`.

## Design Principle

Prefer current truth over historical intention.
Prefer stable, high-signal statements over changelog prose.
Prefer concise completeness over exhaustive implementation detail.

## Validation Check

Before finalizing, verify:

- `SPEC.md` reflects current implemented behavior rather than the original plan alone.
- Any devlog conflicts were resolved by preferring later entries, then validating against the repo when needed.
- Unbuilt plan items are absent.
- Removed or superseded features are absent unless mentioned as explicit non-features to avoid confusion.
- The document can serve as a strong first-pass build spec for recreating the current app.

If any check fails, refine again.

## Output

Return the full new `SPEC.md`.
No commentary.
No explanation.
