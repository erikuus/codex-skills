---
name: reprompt-refactor
description: Refactor AGENTS.md from structural patterns in learnings.md, then prune learnings.md into a curated remainder memory. Use only when manually selected by the user (explicitly requested by name or explicitly asking to refactor AGENTS.md from learnings.md).
---

# Reprompt Refactor

## Role

Act as a reasoning-architecture refactorer.
Evolve the global reasoning scaffold from accumulated structural learnings.
After scaffold refactoring, clean up memory to prevent drift and bloat.

## Input

Use:

- `learnings.md`
- Current `AGENTS.md`

## Output Target

Rewrite `AGENTS.md` completely.
Then rewrite `learnings.md` as a curated remainder: keep only principles not already embedded in `AGENTS.md`, deduplicated, normalized, and capped at 30 bullets.
Preserve clarity and minimalism.

## Refactoring Rules

1. Identify recurring themes in `learnings.md`.
2. Merge overlapping principles.
3. Remove redundancy.
4. Keep the reasoning scaffold compact with 5-8 ordered steps maximum.
5. Maintain logical flow.
6. Avoid verbosity.

## Cleanup Rules

1. Remove any learning now explicitly covered in `AGENTS.md`.
2. Merge duplicates into one canonical phrasing.
3. Drop one-off and domain-specific learnings.
4. Keep only high-signal principles worth retaining as memory.
5. Keep some residual high-signal "raw wisdom" that does not belong in scaffold steps.
6. Cap `learnings.md` at 30 bullets maximum.

## Constraints

- Do not copy `learnings.md` verbatim.
- Do not create bloated checklists.
- Do not add domain-specific instructions.
- Do not exceed necessary complexity.

## Structure Template

Ensure `AGENTS.md` contains:

1. A clear role statement.
2. Ordered reasoning steps.
3. An explicit verification step.
4. A reference to `learnings.md` as supporting memory.

## Design Principle

Prefer architectural improvements over additive rules.
Prefer structural clarity over completeness.
Prefer minimal durable systems over reactive patching.

## Validation Check

Before finalizing, verify:

- `AGENTS.md` is shorter or clearer than before.
- `AGENTS.md` embeds recurring structural corrections.
- `AGENTS.md` reduces reliance on reactive fixes.
- `learnings.md` contains only residual, non-overlapping, high-signal memory.
- `learnings.md` is deduplicated, normalized, and within the 30-bullet cap.

If any check fails, refine again.

## Output

Return full new `AGENTS.md`.
Return full new `learnings.md`.
No commentary.
No explanation.
