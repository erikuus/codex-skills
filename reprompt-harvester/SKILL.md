---
name: reprompt-harvester
description: Extract durable, reusable structural reasoning principles from a completed thread and append them to learnings.md without duplication. Use when the user message is exactly "finalize thread".
---

# Reprompt Harvester

## Role

Act as a structural learning extractor.
Convert a completed thread into durable, reusable reasoning principles.
Do not summarize the thread.
Do not preserve case-specific content.
Extract only generalizable reasoning lessons.

## Input

Use the full conversation history of the current thread.

## Output Target

Append new principles to `learnings.md`.
Do not overwrite existing content.
Do not duplicate existing principles.
Do not modify `AGENTS.md`.

## Extraction Rules

1. Extract only structural reasoning improvements.
2. Ignore domain-specific facts, one-off corrections, emotional tone, style preferences, and formatting adjustments.
3. Keep each lesson reusable, structural, concise, and phrased as an operating principle in one sentence.
4. Append nothing if no structural insight is found.
5. Extract no more than 5 principles per thread.

## Format

Append principles as a flat bullet list:

- Principle text.
- Principle text.
- Principle text.

Output only bullets in the file append operation.
Include no commentary, headers, or explanations.

## Quality Filter

Before appending each principle, verify all are true:

- The principle is general.
- The principle is structural.
- The principle would improve first-shot performance in future tasks.

Discard uncertain candidates.

## End Condition

After appending, output exactly:

Thread finalized. Structural learnings harvested.
