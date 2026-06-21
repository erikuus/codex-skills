# Implementation Contract

Build the real application defined by the product evidence and prototype sources in this repository.

## Goal

State the production outcome, parity level, and distinction between the prototype and runtime app.

## Source Of Truth

List sources in strict priority order.
Classify normative prototype evidence, descriptive guidance, product/domain evidence, and implementation constraints.
Define the stop rule for unresolved conflicts.

## Explicit Resolutions

Record each resolved conflict or prototype ambiguity under a descriptive heading.
Use exact initial states and step-by-step interaction behavior where drift is likely.

## Platform Requirements

Record only project-supplied runtime, rendering, database, storage, authentication, deployment, or environment requirements.

## Data, Import, And Asset Contract

Define production startup data, demo-data exclusions, migrations/import boundaries, asset locations, normalization rules, and ambiguity handling.

## Asset And UI Contract

Define authoritative markup, styles, icons, fonts, assets, component restrictions, global-style restrictions, and prior approval for visible divergence.

## Prototype Presentation Versus Real Outcomes

Protect demonstrated presentation and interaction.
Map simulated or non-persistent prototype actions to required real outcomes.
Require a decision before adding undemonstrated visible states.

## Domain Scope

List included first-version capabilities and explicit non-goals.

## Execution Order

Order work in complete, reviewable slices that include data flow, UI, behavior, and verification.

## Screen And Flow Fidelity

Require preservation of applicable spacing, hierarchy, copy, controls, states, transitions, navigation, and browser behavior.

## Responsive Fidelity

Define whether source rules or design intent is authoritative.
Protect breakpoints and media queries when exact parity applies.

## Acceptance Gates

Require real persistence/domain behavior, working assets, applicable state coverage, runtime comparison, and responsive verification.

## Non-Goals During Parity Work

Prohibit redesign, speculative abstraction, design-system replacement, unrelated infrastructure, and retrospective justification of visible divergence.

## Working Style

Require small verified slices, escalation of material ambiguity, durable non-visual decisions, and prior approval for visible changes.
