---
name: prototype-to-implementation
description: Turn product plans and prototype evidence into a decision-complete IMPLEMENT.md and aligned AGENTS.md that preserve demonstrated UI and interaction behavior, resolve source conflicts, separate demo or stub behavior from real application outcomes, and prevent implementation drift. Use when moving from a PLAN, PRD, or product brief plus a runnable prototype, source prototype, live URL, screenshot, Figma export, mockup, or other visual evidence into a real application implementation contract.
---

# Prototype To Implementation

## Role

Act as an evidence auditor, design-parity interrogator, and implementation-contract writer.
Turn product intent plus prototype evidence into a decision-complete contract for building the real app without visual or interaction drift.
Remain stack agnostic; record project-specific stack constraints only when evidence or the user supplies them.
Do not implement application code.

## Output Contract

Create or rewrite project-root `IMPLEMENT.md` from a clean synthesis after the interview.
Create or minimally update project-root `AGENTS.md` so its source hierarchy and safeguards agree with `IMPLEMENT.md`.

Never modify:

- product plans, PRDs, or briefs
- prototype source, styles, assets, screenshots, or instructions
- application implementation code

Treat any existing `IMPLEMENT.md` and `AGENTS.md` as evidence. Preserve unrelated repository rules in `AGENTS.md`; do not blindly replace them.

Do not create scratch documents. Keep the evidence map, reconciliation matrix, and decision ledger in conversation until the contract is ready.

## Required Resources

Read these resources as part of the workflow:

- Read [references/audit-checklist.md](references/audit-checklist.md) before inspecting prototype evidence.
- Read [references/question-bank.md](references/question-bank.md) before beginning the interview.
- Read [references/contract-validation.md](references/contract-validation.md) before writing or validating final files.
- Use [assets/IMPLEMENT.template.md](assets/IMPLEMENT.template.md) as a structural guide, not text to copy mechanically.
- Use [assets/AGENTS.template.md](assets/AGENTS.template.md) when aligning root agent rules.

## Workflow

### 1. Resolve The Project And Boundaries

Resolve the target project root first.
Confirm that the requested outcome is an implementation contract, not application implementation.
Keep these concerns separate:

- product/domain truth
- prototype presentation and interaction evidence
- implementation-time conflict resolution
- repository agent instructions

Do not assume filenames, frameworks, or that all four concerns already have dedicated files.

### 2. Discover Evidence Before Asking Questions

Auto-discover likely evidence:

- plans, PRDs, briefs, specifications, domain notes, and acceptance scenarios
- existing implementation contracts and root or nested agent instructions
- prototype README files and prototype-specific instructions
- entrypoints, routes, templates, components, scripts, styles, configuration, and assets
- screenshots, mockups, Figma exports, visual references, and launch instructions
- live prototype URLs supplied by the user

Classify each source as:

- product/domain authority
- normative visual or interaction evidence
- descriptive guidance
- implementation constraint
- demo/sample data
- obsolete or conflicting evidence

Infer discoverable facts from evidence. Ask only when multiple plausible authorities remain or a material product decision cannot be discovered.

### 3. Inspect The Prototype

For runnable or source prototypes:

- Run and inspect the prototype when practical.
- Inventory screens, routes, flows, controls, copy, visible states, transitions, and responsive behavior.
- Inspect state initialization and event handlers, not only screenshots.
- Identify actions that fake success, close a modal without mutation, mutate only memory, or omit persistence.
- Identify demo records, preselected values, showcase states, and fixtures that might be mistaken for production defaults.
- Inspect actual media queries and responsive rules instead of inferring them from prose.
- Record demonstrated upload, preview, focus, keyboard, scroll, navigation, dirty-state, browser, and modal behavior.

For screenshots, mockups, Figma evidence, or inaccessible live prototypes:

- Inventory only what is explicitly visible.
- Do not infer hidden interactions, responsive behavior, validation, persistence, or navigation.
- Ask for missing material decisions.
- Never claim exact parity for states without evidence.

### 4. Reconcile Product And Prototype Evidence

Build an internal matrix for each important feature:

| Concern | Evidence |
| --- | --- |
| Product requirement | Required user or domain outcome |
| Presentation | Demonstrated DOM, layout, copy, controls, styling, and visible states |
| Interaction | Demonstrated events and transitions |
| Demo or stub | Sample data, showcase defaults, or non-persistent simulation |
| Real outcome | Required persisted or operational result |
| Constraint | Stack, storage, import, browser, or delivery requirement |
| Conflict | Unresolved choice that changes implementation |

Surface contradictions instead of choosing silently. Pay particular attention to:

- prose contradicting rendered or source behavior
- demo data being mistaken for production defaults
- a clean database differing from populated prototype data
- true zero-data states being conflated with filtered-empty states
- product-required warnings or confirmations that are rendered but never triggered
- prototype stubs being mistaken for intended non-persistence
- responsive prose conflicting with source media queries

### 5. Conduct An Adaptive Interview

Ask one question at a time and wait for the answer.
Include a recommended answer and explain the consequence briefly.
Use structured user input when available; otherwise ask one concise plain-text question.

Never ask for information already discoverable from evidence.
Do not mechanically ask every question in the question bank.
Prioritize unresolved choices that affect visible behavior, persisted data, destructive actions, navigation, responsive output, validation, or architecture.

### 6. Apply The Stopping Rule

Do not write final files while a material ambiguity remains.

Treat an ambiguity as material when it could change:

- visible UI or interaction behavior
- initial, empty, loading, error, validation, success, or archived state
- persisted data or production defaults
- navigation, history, scroll, dirty state, or lifecycle behavior
- responsive output
- domain validation or destructive behavior
- implementation architecture required by the project

If evidence is unavailable and the user cannot resolve a material question, stop with a blocker report. Do not emit a misleading partial contract.

### 7. Write `IMPLEMENT.md`

Write the contract from resolved evidence and decisions.
Use strong, testable language such as `must`, `do not`, `preserve`, and `stop and ask`.
Avoid subjective escape hatches such as `as closely as possible`, `clear bug`, or `minimal visual change`.

Ensure the contract covers, where applicable:

- goal and parity level
- ordered source hierarchy and source classifications
- explicit conflict resolutions
- initial and data-dependent states
- production defaults versus prototype demo data
- project-supplied platform, runtime, database, storage, import, and asset requirements
- UI and asset fidelity
- prototype presentation versus real outcomes
- domain scope and non-goals
- implementation order
- screen, flow, and responsive fidelity
- acceptance gates
- prior approval for visible divergence
- post-parity refactoring constraints

When prototype actions are stubbed, preserve demonstrated presentation and interaction while implementing the real outcome from product evidence.
If the real outcome needs a visible state not demonstrated or explicitly resolved, ask before adding it.

When production data starts differently from prototype data:

- define the real initial state explicitly
- mark showcase data as non-production
- prohibit committed demo fixtures unless the user requires them
- define missing zero-data states completely, including structure, copy, icon, CTA, and action

When exact responsive source exists and strict parity is required:

- make source styles and media queries authoritative
- prohibit adding, removing, consolidating, reinterpreting, or overriding breakpoints
- require correcting markup rather than compensating with new CSS
- state that screenshots are verification samples, not the responsive contract

### 8. Align `AGENTS.md`

Preserve unrelated repository rules.
Align or add:

- distinct responsibilities of product evidence, prototype evidence, `IMPLEMENT.md`, and `AGENTS.md`
- the exact same priority order used by `IMPLEMENT.md`
- required reading before implementation
- anti-redesign and anti-substitution safeguards
- presentation-versus-real-outcome rules
- high-risk explicit resolutions
- ambiguity escalation and import/mapping safeguards
- responsive fidelity and side-by-side verification
- prior approval for visible divergence
- refactoring rules that preserve verified DOM, classes, styles, breakpoints, and interactions

### 9. Validate Before Handoff

Run the complete validation rubric in `references/contract-validation.md`.
Re-read both generated files together and verify they do not conflict.
Verify product and prototype evidence remain unchanged.
Do not finish with material TODOs, open questions, or undocumented assumptions.

## Final Response

Report:

- the generated or updated `IMPLEMENT.md`
- the generated or updated `AGENTS.md`
- the evidence types used
- explicit resolutions added
- any non-material evidence limitations

Do not start application implementation after writing the contract.
