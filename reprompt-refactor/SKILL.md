---
name: reprompt-refactor
description: Rebuild project-root SPEC.md from PLAN.md, DEVLOG.md, and current repo truth as a stack-neutral source-of-truth spec for reimplementation. Use when the user wants to synthesize the current implemented specification, rebuild SPEC.md, or reconcile the original plan with what the app actually became.
---

# Reprompt Refactor

## Role

Act as a project specification synthesizer.
Rebuild `SPEC.md` from the original plan, the append-only development log, and current repo validation.
Treat `SPEC.md` as the long-lived source of truth for rebuilding the same app even if the current codebase, framework, or language becomes unusable.
Treat code as disposable evidence, not as the final artifact to preserve.
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
Write `SPEC.md` as a reconstruction-grade, stack-neutral specification.

## Refactoring Rules

1. Start from `PLAN.md` to understand the original target product and terminology.
2. Parse `DEVLOG.md` as evidence, not as perfect structure.
3. Reconstruct a canonical change timeline from entry timestamps, labels, and content before synthesizing the spec.
4. If the log is malformed, interleaved, or out of file-order chronology, repair it mentally by grouping lines under the most plausible entry header before using it as evidence.
5. Group devlog evidence by feature area before writing `SPEC.md`, for example public or guest experience, authenticated user experience, administrative or operator workflows, domain data management, integrations, imports or exports, and operational constraints.
6. Within each feature area, treat later dated evidence as superseding earlier evidence when they conflict.
7. Inspect the repo to validate what is actually implemented now.
8. Prefer repo truth over plan or devlog when they diverge.
9. Include only implemented current-state behavior.
10. Exclude features that were planned but never built.
11. Exclude features that were added and later removed.
12. Mention explicit exclusions only when needed to prevent old plan assumptions from reappearing.
13. Preserve behavior, rules, data semantics, and acceptance criteria; do not preserve framework-specific mechanisms unless they are product-defining.
14. Translate implementation evidence into stack-neutral requirements whenever possible.

## Evidence Filtering

When deciding what belongs in `SPEC.md`, keep:

- stable user-visible behavior
- access rules and permissions
- business rules and constraints
- durable data concepts and domain entities
- relationships, state transitions, and lifecycle rules
- transformations, comparison logic, calculation rules, and other domain algorithms
- validation rules, limits, defaults, and ordering guarantees
- empty states, error behavior, and failure handling that affect the product contract
- external interfaces, imports, exports, and integration-facing behavior
- representative acceptance scenarios needed to verify a reimplementation
- technical invariants that materially affect externally observable behavior
- operational prerequisites that still matter for real use or deployment

Usually drop:

- one-off implementation fixes
- test-only details
- internal hook or component refactors
- exact CSS values, animation timings, and pixel thresholds
- library or icon choices unless they are part of the intended product specification
- framework, test-harness, and tool names unless they are product-defining or externally required
- exploratory or superseded UI micro-tuning

If a detail might be noise, omit it unless removing it would make the product behave differently when rebuilt.
If code or tests reveal important behavior, rewrite that evidence as stack-neutral requirements or acceptance scenarios instead of copying implementation vocabulary.

## SPEC Shape

Ensure `SPEC.md` covers:

- Purpose and audience
- Implemented user roles and access model
- Current product flows and feature behavior by role when relevant
- Current data concepts, important domain entities, and relationships
- Key business rules, algorithms, validations, and constraints
- Important states, transitions, edge cases, and failure behavior
- External interfaces, operational dependencies, and still-open prerequisites that affect reimplementation
- Acceptance scenarios sufficient to verify a reimplementation
- Explicit non-features or exclusions when needed to avoid rebuilding removed or never-built behavior

Use this section order unless the project clearly needs a different one:

1. Title and brief summary
2. Purpose and audience
3. Roles and access
4. Domain model
5. Role-based experiences and core workflows
6. Rules, algorithms, validations, and constraints
7. States, edge cases, and failure behavior
8. External interfaces and operational dependencies
9. Acceptance scenarios
10. Non-features, exclusions, and still-open operational notes

Keep the document product-facing and implementation-aware, not a code walkthrough.
Write in clear declarative prose with short bullets where enumeration helps readability.
Do not mirror the changelog structure.
Avoid framework-specific instructions unless the dependency is part of the product contract.

## Workflow

1. Resolve the target project root and confirm `PLAN.md` and `DEVLOG.md` exist.
2. Read `PLAN.md` for intended scope and vocabulary.
3. Read `DEVLOG.md` and first normalize it into a mental canonical evidence set:
   - identify each entry by header timestamp and label
   - detect malformed cases such as repeated section headings, split entries, or entries that appear out of chronological order in file position
   - reattach stray sections to the correct entry before drawing conclusions
4. Build a current-state feature map by clustering `PLAN.md` intent, devlog evidence, and repo evidence by subsystem or user flow.
5. Inspect repo truth only as needed to settle what is currently implemented.
6. Derive the persistent product contract from that evidence:
   - entities and relationships
   - role capabilities and restrictions
   - workflows and user-visible outcomes
   - rules, algorithms, validations, and defaults
   - failure behavior and non-features
7. Convert implementation-specific tests and code paths into stack-neutral acceptance scenarios when they capture behavior that a reimplementation must preserve.
8. Rewrite `SPEC.md` from scratch in a clean, stable structure.
9. Do not copy `PLAN.md`, `DEVLOG.md`, or code comments verbatim.
10. Do not rewrite `PLAN.md` or `DEVLOG.md`.

## Design Principle

Prefer current truth over historical intention.
Prefer stable, high-signal statements over changelog prose.
Prefer concise completeness over exhaustive implementation detail.
Prefer feature-level synthesis over entry-by-entry summarization.
Prefer behavioral contracts over implementation mechanisms.
Prefer a spec that another agent can rebuild from over a spec that merely describes the existing codebase.

## Validation Check

Before finalizing, verify:

- `SPEC.md` reflects current implemented behavior rather than the original plan alone.
- Any devlog conflicts were resolved by canonicalized chronology, then validated against the repo when needed.
- Malformed devlog structure did not leak into the final spec structure.
- Unbuilt plan items are absent.
- Removed or superseded features are absent unless mentioned as explicit non-features to avoid confusion.
- Low-level implementation noise and transient UI tuning were excluded unless they are necessary to reproduce current behavior.
- Framework-specific details were translated into product requirements unless they are externally required.
- The domain model, rules, validations, and failure behavior are explicit enough to rebuild the app without reading the original code.
- `SPEC.md` contains stack-neutral acceptance scenarios that can be used to verify a fresh implementation.
- The final document is organized by feature area and is easy to scan without knowledge of the devlog history.
- The document can serve as a strong first-pass build spec for recreating the current app.

If any check fails, refine again.

## Output

Return the full new `SPEC.md`.
No commentary.
No explanation.
