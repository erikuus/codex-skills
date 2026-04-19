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
2. Parse `DEVLOG.md` as evidence, not as perfect structure.
3. Reconstruct a canonical change timeline from entry timestamps, labels, and content before synthesizing the spec.
4. If the log is malformed, interleaved, or out of file-order chronology, repair it mentally by grouping lines under the most plausible entry header before using it as evidence.
5. Group devlog evidence by feature area before writing `SPEC.md`, for example learner catalog, learner exercise workspace, authentication, admin management, uploads, seeding, and testing.
6. Within each feature area, treat later dated evidence as superseding earlier evidence when they conflict.
7. Inspect the repo to validate what is actually implemented now.
8. Prefer repo truth over plan or devlog when they diverge.
9. Include only implemented current-state behavior.
10. Exclude features that were planned but never built.
11. Exclude features that were added and later removed.
12. Mention explicit exclusions only when needed to prevent old plan assumptions from reappearing.

## Evidence Filtering

When deciding what belongs in `SPEC.md`, keep:

- stable user-visible behavior
- access rules and permissions
- business rules and constraints
- durable data concepts and content entities
- technical invariants that materially affect externally observable behavior
- operational prerequisites that still matter for real use or deployment

Usually drop:

- one-off implementation fixes
- test-only details
- internal hook or component refactors
- exact CSS values, animation timings, and pixel thresholds
- library or icon choices unless they are part of the intended product specification
- exploratory or superseded UI micro-tuning

If a detail might be noise, omit it unless removing it would make the product behave differently when rebuilt.

## SPEC Shape

Ensure `SPEC.md` covers:

- Purpose and audience
- Implemented user roles and access model
- Current product flows and feature behavior
- Key business rules and constraints
- Current data concepts and important admin or content entities
- Key technical invariants that materially affect behavior
- Current operational dependencies or unresolved production prerequisites that still hold

Use this section order unless the project clearly needs a different one:

1. Title and brief summary
2. Purpose and audience
3. Roles and access
4. Learner experience
5. Admin experience
6. Data and content model
7. Rules and constraints
8. Technical invariants
9. Operational notes or current non-features, only if still relevant

Keep the document product-facing and implementation-aware, not a code walkthrough.
Write in clear declarative prose with short bullets where enumeration helps readability.
Do not mirror the changelog structure.

## Workflow

1. Resolve the target project root and confirm `PLAN.md` and `DEVLOG.md` exist.
2. Read `PLAN.md` for intended scope and vocabulary.
3. Read `DEVLOG.md` and first normalize it into a mental canonical evidence set:
   - identify each entry by header timestamp and label
   - detect malformed cases such as repeated section headings, split entries, or entries that appear out of chronological order in file position
   - reattach stray sections to the correct entry before drawing conclusions
4. Build a current-state feature map by clustering `PLAN.md` intent, devlog evidence, and repo evidence by subsystem or user flow.
5. Inspect repo truth only as needed to settle what is currently implemented.
6. Rewrite `SPEC.md` from scratch in a clean, stable structure.
7. Do not copy `PLAN.md` or `DEVLOG.md` verbatim.
8. Do not rewrite `PLAN.md` or `DEVLOG.md`.

## Design Principle

Prefer current truth over historical intention.
Prefer stable, high-signal statements over changelog prose.
Prefer concise completeness over exhaustive implementation detail.
Prefer feature-level synthesis over entry-by-entry summarization.

## Validation Check

Before finalizing, verify:

- `SPEC.md` reflects current implemented behavior rather than the original plan alone.
- Any devlog conflicts were resolved by canonicalized chronology, then validated against the repo when needed.
- Malformed devlog structure did not leak into the final spec structure.
- Unbuilt plan items are absent.
- Removed or superseded features are absent unless mentioned as explicit non-features to avoid confusion.
- Low-level implementation noise and transient UI tuning were excluded unless they are necessary to reproduce current behavior.
- The final document is organized by feature area and is easy to scan without knowledge of the devlog history.
- The document can serve as a strong first-pass build spec for recreating the current app.

If any check fails, refine again.

## Output

Return the full new `SPEC.md`.
No commentary.
No explanation.
