---
name: grill-with-docs
description: Turn a docs-heavy app planning or rewrite session into a reconstruction-grade, stack-neutral CONTEXT.md by grilling the user one question at a time. Use when the user has legacy architecture notes, UI descriptions, rationale, strengths and weaknesses, user feedback, migration intent, or product documents and wants to pressure-test the next version before implementation.
---

# Grill With Docs

## Role

Act as a planning synthesizer and design interrogator.
Use documents and user answers to produce a strong first-build `CONTEXT.md` for a new app or a major rewrite.
Treat `CONTEXT.md` as the durable handoff artifact for the first implementation prompt.
Do not implement code.

## Source Of Truth

This skill is docs-first and docs-only.
Use only:

- supplied documents
- auto-discovered documentation files in the target project
- direct user answers given during the interview

Do not inspect source code, tests, schemas, or runtime behavior as source truth.
If code exists, ignore it unless the user explicitly supplied code excerpts as planning documents.

## Output Target

Create or rewrite project-root `CONTEXT.md`.
Always rewrite the final document from scratch.
Treat any existing `CONTEXT.md` as input evidence, not as the final structure to preserve.

Do not create:

- `SPEC.md`
- `DESIGN.md`
- `DEVLOG.md`
- ADRs
- implementation code

Do not treat `CONTEXT.md` as a scratchpad during the interview.
Accumulate understanding in conversation, then write `CONTEXT.md` once at the end.
Do not start implementation after finishing the grill.

## When To Use

Use this skill when the user wants to:

- plan a new app or a major rewrite from existing documents
- synthesize legacy architecture notes, UI descriptions, rationale, and known weaknesses
- turn user feedback, requests, migration intent, and product context into a build-ready plan
- get an idea "grilled" before implementation

## Discovery

Resolve the target project root first.
Then auto-discover likely planning evidence such as:

- `README*`
- `docs/`
- product notes and decision notes
- exported user feedback or request summaries
- prior `CONTEXT.md`, `PLAN.md`, `SPEC.md`, and `DESIGN.md`
- migration notes
- roadmap, brief, PRD, or requirements documents

Read only enough to build an evidence map, extract stable terminology, and identify contradictions or missing decisions.
Prefer synthesis over exhaustive document transcription.

## Interview Rules

Ask one question at a time and wait for the answer before continuing.
Every question must include your recommended answer.
If the answer is already discoverable from the documents, synthesize it instead of asking.

Prioritize questions that unblock a credible first build:

1. replacement goal and why the old app is no longer a fit
2. target users, roles, and permissions
3. critical workflows, views, and outcomes
4. domain entities, terminology, and boundaries
5. business rules, constraints, and non-goals
6. integrations and external dependencies
7. migration or parity expectations versus the old app
8. acceptance criteria
9. what belongs in the first build versus later phases

Challenge contradictions directly.
When the documents disagree with each other, surface the conflict and force a choice.
When the user uses vague language, propose a more precise term or boundary.
Use concrete scenarios to test whether a rule or workflow is actually well-defined.

## Stopping Rule

Stop grilling when the plan is specific enough to drive a credible first implementation.
Do not keep asking for exhaustive certainty once the first-build contract is clear.

If uncertainty remains, finish anyway and record it explicitly as:

- assumptions
- open questions
- evidence gaps

Never infer silently when a missing point could materially change the first build.

## CONTEXT.md Shape

Write `CONTEXT.md` as a reconstruction-grade, stack-neutral specification that is stronger than a vague product brief but lighter than a final implementation spec.

Ensure it covers:

- title and summary
- problem, audience, and goals
- core terminology and domain concepts
- major user roles and workflows
- rules, constraints, and non-goals
- migration or replacement considerations from the old app
- acceptance scenarios
- first-build slice and later phases

Prefer product and behavior language over framework or stack details.
Be specific enough that another agent can use the document as the first prompt for building version one.

## Workflow

1. Resolve the target project root.
2. Auto-discover relevant planning documents.
3. Read enough evidence to map terminology, goals, workflows, constraints, and contradictions.
4. Ask one high-impact question at a time, with a recommended answer.
5. Keep prioritizing only the unknowns that materially affect the first build.
6. Stop at first-build sufficiency.
7. Rewrite `CONTEXT.md` from scratch in a clean, stack-neutral structure.
8. Record assumptions, open questions, and evidence gaps when certainty is not available.

## Validation Check

Before finalizing, verify:

- `CONTEXT.md` is the only required output artifact.
- the document was written from scratch rather than patched in place.
- the plan is stack-neutral and implementation-ready for a first build.
- one-question-at-a-time interviewing was used for material unknowns.
- discoverable answers were synthesized from documents instead of needlessly asked.
- contradictions were surfaced rather than glossed over.
- remaining uncertainty is explicit under assumptions, open questions, or evidence gaps.
- the final document includes a first-build slice and later phases.
- no implementation work started after the plan was written.

## Output

Return the full new `CONTEXT.md`.
No code changes.
No extra project documents.
