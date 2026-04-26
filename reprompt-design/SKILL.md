---
name: reprompt-design
description: Build project-root DESIGN.md and design-assets from screenshots, visual assets, styles, docs, and current app evidence as a stack-neutral visual source of truth for reimplementation. Use when the user wants to preserve or reconstruct an app's design, visual system, essential screens, responsive layouts, interaction states, or product-defining assets.
---

# Reprompt Design

## Role

Act as a design reconstruction synthesizer.
Build `DESIGN.md` as the long-lived visual source of truth that complements `SPEC.md`.
Treat code, screenshots, styles, and assets as evidence.
Do not modify `SPEC.md`, `PLAN.md`, or `DEVLOG.md`.

## Input

Use any available evidence:

- Project root
- `SPEC.md` when present, to understand essential workflows and roles
- Running app URL when available
- Login or test-access instructions when available
- Current code, routes, styles, templates, assets, docs, and existing screenshots

Prefer live screenshot evidence. If the app cannot be launched or authenticated, continue from static evidence and record the gap in `DESIGN.md`.

## Output Target

Write or rewrite:

- `DESIGN.md`
- `design-assets/screenshots/`
- `design-assets/source-assets/`

`DESIGN.md` is stack-neutral and rebuild-oriented. It should explain visual decisions and evidence clearly enough for another agent to recreate the app's design in a different stack.

## Capture Scope

Capture essential states, not every possible variant:

- primary public or guest view
- authenticated user views when applicable
- administrative or operator views when applicable
- core workflow screens
- important empty, error, success, complete, focused, expanded, modal, and loading states
- desktop and mobile breakpoints when the app is responsive
- tablet only when it has meaningfully distinct layout behavior

If a state matters but cannot be reached, document it from code or static evidence and mark missing screenshot evidence.

## Asset Policy

Inventory product-defining visual assets:

- backgrounds and hero imagery
- logos and marks
- icons and SVGs with product meaning
- fonts and type choices
- illustrations, textures, and major media
- reusable visual motifs that materially shape identity

Copy assets into `design-assets/source-assets/` only when copying is useful and safe.
Reference large, generated, numerous, or externally managed assets by path instead of archiving everything.
Do not preserve every static file by default.

## DESIGN.md Shape

Use this section order unless the project clearly needs another structure:

1. Title and design summary
2. View inventory
3. Screenshot evidence
4. Responsive behavior
5. Interaction states
6. Visual system
7. Asset inventory
8. Reconstruction requirements
9. Visual acceptance checks
10. Evidence gaps, only if relevant

Keep `DESIGN.md` visual and interaction-focused. Functional behavior belongs in `SPEC.md`.

## Evidence Filtering

Keep:

- visual identity, density, tone, and major layout principles
- screen structure, navigation placement, and information hierarchy
- responsive layout rules and breakpoint-level behavior
- meaningful interaction states and transitions
- colors, typography, spacing rhythm, icon style, shape language, elevation, borders, and motion where product-defining
- screenshots with viewport, state, route or view, and purpose
- product-defining asset roles and source paths
- stack-neutral visual acceptance checks

Usually drop:

- framework class names
- internal component names unless they clarify reusable UI patterns
- raw CSS dumps
- one-off numeric constants unless they materially define layout or identity
- test harness details
- transient experiments and superseded visual choices

If a detail might be noise, omit it unless removing it would make a rebuild visibly or interactively different.

## Workflow

1. Resolve the project root.
2. Read `SPEC.md` if present to identify essential workflows, roles, and states.
3. Discover routes, app entrypoints, styles, templates, asset directories, and existing docs.
4. Prefer live capture:
   - use the running app URL if provided
   - otherwise infer how to launch the app when practical
   - capture essential desktop and mobile screenshots into `design-assets/screenshots/`
5. If live capture fails or is incomplete, inspect code, styles, assets, docs, and existing screenshots instead.
6. Inventory product-defining assets and copy or reference them according to the asset policy.
7. Write `DESIGN.md` from scratch in a clean, stack-neutral structure.
8. Link screenshots and preserved assets with relative paths.
9. Record evidence gaps explicitly when runtime capture or state coverage is incomplete.

## Validation Check

Before finalizing, verify:

- `DESIGN.md` complements `SPEC.md` instead of repeating functional requirements.
- Essential views and states are represented by screenshots, static evidence, or explicit evidence gaps.
- Product-defining assets are inventoried without archiving the whole asset tree.
- Design rules are stack-neutral and can guide a reimplementation.
- Low-level implementation detail was excluded unless necessary for visual reconstruction.
- Visual acceptance checks are specific enough to verify a rebuilt interface.

## Output

Report the generated or updated `DESIGN.md`, screenshot directory, copied or referenced assets, and any evidence gaps.
