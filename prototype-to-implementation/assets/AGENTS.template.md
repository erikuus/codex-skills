# Implementation Agent Rules

## Distinct Sources Of Truth

- Product evidence defines domain rules and real application outcomes.
- Prototype evidence defines demonstrated UI, interaction presentation, and responsive behavior.
- `IMPLEMENT.md` defines implementation-time conflict resolutions and execution requirements.
- `AGENTS.md` tells implementation agents how to apply those sources without drift.

Do not collapse these responsibilities into one document.

## Priority Order

List the exact priority order from `IMPLEMENT.md`.
If evidence conflicts and `IMPLEMENT.md` does not resolve it, stop and ask.

## Core Safeguards

- Build the real application; do not ship the prototype as the runtime app.
- Do not redesign, modernize, simplify, or substitute the visual system before parity.
- Preserve required DOM nesting, classes, styles, icons, assets, media queries, and interaction behavior.
- Implement real product outcomes without changing demonstrated presentation.
- Require prior approval for visible divergence.
- Preserve verified parity during refactoring.

## Required Reading

List the implementation contract, product evidence, normative prototype sources, descriptive prototype sources, and relevant nested agent instructions.

## Explicit High-Risk Resolutions

Repeat only the initial states, interaction rules, demo-data exclusions, and lifecycle decisions most likely to drift.

## Data And Assets

Record production startup data, import/storage rules, demo-fixture exclusions, and ambiguity escalation requirements.

## Delivery Discipline

- Implement complete, reviewable slices.
- Compare each major screen and flow with the prototype.
- Verify all authoritative responsive rules.
- Treat screenshots as samples unless declared normative.
- Record non-visual decisions when needed; obtain approval before visible changes.
