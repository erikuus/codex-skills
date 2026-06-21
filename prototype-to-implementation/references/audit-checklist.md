# Prototype Evidence Audit Checklist

Use this checklist selectively but completely enough to find every implementation-changing gap. Mark evidence as demonstrated, product-required, inferred-but-low-risk, or unresolved.

## Contents

1. Source classification
2. Prototype reachability
3. Screen and flow inventory
4. Controls and events
5. Initial and default state
6. Demo data and production data
7. Data-dependent and empty states
8. Prototype stubs and real outcomes
9. Validation and destructive behavior
10. Dirty state and navigation
11. State lifetime and restoration
12. Uploads and previews
13. Responsive behavior
14. Visual system and assets
15. Acceptance evidence

## 1. Source Classification

- Locate product plans, PRDs, briefs, specifications, acceptance scenarios, and domain notes.
- Locate prototype instructions, README files, source entrypoints, routes, templates, scripts, styles, assets, screenshots, and mockups.
- Locate existing implementation contracts and root or nested agent rules.
- Classify each source as domain authority, normative presentation/interaction evidence, descriptive guidance, implementation constraint, demo data, or obsolete/conflicting evidence.
- Determine the provisional source priority.
- Find conflicts between prose, runtime behavior, source code, and styles.
- Confirm whether any generated mock, screenshot, or design file is declared authoritative.

## 2. Prototype Reachability

- Determine whether the prototype can be launched locally.
- Determine whether a live URL requires authentication or existing browser state.
- Identify available routes and navigation entrypoints.
- Record evidence that cannot be reached or inspected.
- Never infer hidden states from a single screenshot.

## 3. Screen And Flow Inventory

- Inventory top-level areas, screens, routes, overlays, drawers, panels, and wizard steps.
- Record default landing screen and navigation state.
- Record every demonstrated entry and exit path.
- Record primary and secondary actions.
- Distinguish full-page flows from inline controls, panels, drawers, and modals.
- Identify controls with similar appearance but different semantics.

## 4. Controls And Events

- Inventory buttons, links, form controls, autocomplete fields, filters, selectors, uploads, toggles, and editable display controls.
- Inspect click, input, change, focus, blur, keydown, drag/drop, scroll, history, and browser event handlers.
- Record open, close, select, clear, cancel, back, save, duplicate, archive, restore, and delete behavior.
- Record outside-click, Escape, Enter, Space, and focus-restoration behavior when demonstrated.
- Identify controls rendered without a real handler or handlers that only change prototype state.

## 5. Initial And Default State

- Record initial navigation, expanded/collapsed state, selection, filters, panels, modals, and form defaults.
- Check whether source initialization is production intent or showcase setup.
- Check whether revisiting a flow resets, preserves, or accumulates state.
- Check whether creation and editing share defaults incorrectly.
- Distinguish clean initial state from dirty state.

## 6. Demo Data And Production Data

- Identify hard-coded records, fixtures, seeded examples, fake counts, and selected sample values.
- Determine whether production starts empty, imports real data, or seeds examples.
- Distinguish visual reference data from required production data.
- Check whether example data is necessary only to reach parity-test states.
- Prevent demo records from silently becoming production seeds.
- Check whether imported classifications or mappings can be ambiguous.

## 7. Data-Dependent And Empty States

- Inventory true zero-record states.
- Inventory search-empty and filtered-empty states separately.
- Inventory no-options, all-selected, no-labels, no-upload, and no-related-record states.
- Record icon, heading, copy, CTA, CTA action, surrounding toolbar, and layout for each.
- Check whether a prototype incorrectly reuses a filtered-empty state for a clean database.
- Identify data-dependent pluralization and counts.

## 8. Prototype Stubs And Real Outcomes

- Identify create actions that show confirmation without inserting data.
- Identify edit actions that do not persist fields.
- Identify delete confirmations that only close.
- Identify duplicate actions that reuse references or omit storage behavior.
- Identify fake pagination, infinite-scroll text, fake usage counts, and static validation.
- Identify local object URLs or in-memory uploads that require real storage.
- Map each stub to the product-required real outcome.
- Check whether the real outcome needs a new visible state.

## 9. Validation And Destructive Behavior

- Inventory required fields, minimum/maximum rules, uniqueness, allowed file types, and relationship constraints.
- Record where and how errors appear.
- Record disabled controls and warning states.
- Inventory permanent deletion, archive/restore, cascading effects, and blocked deletion.
- Verify confirmation copy and post-action destination.
- Identify destructive actions without demonstrated failure handling.

## 10. Dirty State And Navigation

- Define the clean baseline for each creation/edit flow.
- Identify which user changes make the flow dirty.
- Record internal navigation, step navigation, modal dismissal, browser back, refresh, and close behavior.
- Distinguish application confirmation UI from native browser warnings.
- Determine what resets after discard, successful save, or re-entry.
- Check whether inline-created related data persists after the parent flow is discarded.

## 11. State Lifetime And Restoration

- Record filter, selection, focus, panel, query, scroll, and pagination persistence.
- Distinguish current visit, session, reload, and durable persistence.
- Inspect modal/drawer scroll restoration.
- Check behavior when active filters invalidate a selected record.
- Check ordering and tie-breaking after mutation.

## 12. Uploads And Previews

- Record accepted types, size/count limits, click and drag/drop behavior, preview timing, replacement, cancellation, and required-state validation.
- Distinguish item images, parent-record images, and generated assets.
- Record object-fit, cropping, rotation, and orientation behavior.
- Determine storage destination, naming, replacement cleanup, and orphan handling only from project evidence or user decisions.

## 13. Responsive Behavior

- Inspect actual media queries, container rules, and responsive utilities.
- Record breakpoints and layout changes at each breakpoint.
- Distinguish exact source rules from high-level phone usability intent.
- Inventory navigation transformations, hidden labels/columns, grid counts, panel overlays, stacking, sticky behavior, and modal sizing.
- Check whether screenshots are examples or the normative contract.
- Prevent framework markup differences from being patched with divergent CSS.

## 14. Visual System And Assets

- Record element nesting and class naming when strict parity depends on them.
- Inventory global resets, typography, fonts, icons, filled/regular icon variants, colors, spacing, radii, borders, shadows, motion, and image treatment.
- Locate CSS imports, asset packages, and static paths.
- Identify framework default styles that could override prototype styles.
- Identify component libraries, generated form markup, default icons, or utility rewrites that could change presentation.

## 15. Acceptance Evidence

- Define which states require runtime verification.
- Require side-by-side comparison where visual parity is required.
- Treat screenshots as samples unless explicitly declared authoritative.
- Verify all responsive source rules, not only selected widths.
- Verify real persistence, destructive behavior, imports, and asset paths.
- Require prior user approval for any visible divergence.
- Require post-parity refactors to preserve verified behavior and presentation.
