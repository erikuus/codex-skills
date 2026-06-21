# Adaptive Question Bank

Ask one question at a time. Always include a recommended answer and a brief consequence. Skip a question when repository or runtime evidence answers it conclusively.

## Contents

- Source authority and fidelity
- Prototype evidence and runtime constraints
- Initial, empty, and demo-data states
- Stubbed outcomes, validation, and dirty state
- State persistence, routes, and browser behavior
- Responsive and design-system authority
- Imports, divergence, refactoring, and verification

## Source Authority

**Trigger:** Multiple plans, prototype instructions, visual references, or source implementations disagree.

**Decision:** Which source controls domain behavior, visible presentation, demonstrated interaction, and implementation-time conflict resolution?

**Recommended default:** Make rendered/source prototype evidence authoritative for explicit UI and interaction; make product evidence authoritative for domain rules and real outcomes; make `IMPLEMENT.md` authoritative for resolved conflicts.

**Skip when:** Existing repository rules state the complete hierarchy without contradiction.

## Fidelity Level

**Trigger:** The user says “based on,” “inspired by,” “match,” “clone,” or “parity” without precision.

**Decision:** Is the implementation required to reproduce explicit prototype behavior exactly or only preserve design intent?

**Recommended default:** Require exact parity wherever the prototype is explicit and ask before visible divergence.

**Skip when:** The plan or agent rules already define exact parity and approval policy.

## Prototype Evidence Gaps

**Trigger:** Only screenshots, mockups, inaccessible URLs, or incomplete source evidence exist.

**Decision:** What interactions, responsive transformations, validation, and hidden states are intended?

**Recommended default:** Treat only visible evidence as authoritative; require explicit decisions for hidden behavior.

**Skip when:** Runnable/source evidence demonstrates the behavior.

## Stack And Runtime

**Trigger:** No implementation stack is specified or multiple stacks are mentioned.

**Decision:** What runtime, rendering model, data store, storage system, and required environment constraints apply?

**Recommended default:** Do not choose a stack for the user; ask for the minimum required architecture decision.

**Skip when:** Repository evidence establishes the production stack and configuration.

## Demo Data Versus Production Defaults

**Trigger:** The prototype initializes sample records, selections, filters, counts, or form values.

**Decision:** Which values are presentation fixtures and which are real defaults or seed data?

**Recommended default:** Treat showcase records and preselection as demo-only unless product evidence explicitly requires them.

**Skip when:** Source comments or product rules classify every value clearly.

## Clean Initial State

**Trigger:** A main screen or flow depends on data, selection, filters, panels, or previous navigation.

**Decision:** What is the exact clean state on first entry and re-entry?

**Recommended default:** Define navigation state, data visibility, selections, panels, filters, and form defaults explicitly.

**Skip when:** Product and prototype evidence agree and no demo data contaminates the state.

## Zero Data Versus Filtered Empty

**Trigger:** Production may start empty or the prototype uses one empty state for multiple causes.

**Decision:** Should zero records and zero filtered matches have separate presentation and actions?

**Recommended default:** Separate them when the recovery action differs; define icon, heading, body, CTA, surrounding controls, and destination.

**Skip when:** Both states are explicitly demonstrated or product-approved as identical.

## Stubbed Actions

**Trigger:** Create, edit, duplicate, delete, upload, pagination, or filtering is simulated or non-persistent.

**Decision:** What real outcome must replace the stub, and does it need additional visible states?

**Recommended default:** Preserve demonstrated presentation while implementing the product-required persisted outcome; ask before adding visible UI.

**Skip when:** Product evidence fully defines the result and no new visible state is needed.

## Validation And Failure States

**Trigger:** Required fields or domain constraints exist without complete prototype validation.

**Decision:** Where and how are errors, blocked actions, and failures presented?

**Recommended default:** Reuse an explicitly demonstrated validation pattern; otherwise require a product decision before adding visible states.

**Skip when:** Every applicable error state is demonstrated and domain rules agree.

## Dirty State

**Trigger:** A multi-step or modal flow can be abandoned after edits.

**Decision:** What starts dirty state, which exits trigger warnings, and what resets after discard or save?

**Recommended default:** Opening alone is clean; user changes make it dirty; internal step movement stays in-flow; app navigation uses the demonstrated confirmation; refresh/back/close use native browser warning where appropriate.

**Skip when:** Source and product evidence define the complete lifecycle.

## State Persistence

**Trigger:** Filters, scroll, queries, focused records, or selections should survive navigation.

**Decision:** What survives focus changes, internal navigation, reload, session restart, and app reopen?

**Recommended default:** Preserve only the lifetime explicitly required by product evidence; do not infer durable persistence from prototype in-memory state.

**Skip when:** Required lifetime is explicit.

## Routes And Browser History

**Trigger:** Prototype navigation is state-only, while the real app may use routes or history.

**Decision:** Which screens or focused records need addressable URLs and browser back/forward behavior?

**Recommended default:** Follow explicit product/runtime routing requirements and preserve visible navigation flow.

**Skip when:** The production routing contract already exists.

## Responsive Authority

**Trigger:** Styles contain media queries or screenshots show multiple widths.

**Decision:** Must source responsive rules be ported exactly, or is only responsive intent authoritative?

**Recommended default:** When strict parity and source styles exist, preserve every responsive rule and breakpoint unchanged.

**Skip when:** The contract already states the authority and deviation policy.

## Markup And Design-System Substitution

**Trigger:** The production framework supplies components, forms, icons, resets, or utility conventions.

**Decision:** May framework defaults replace prototype markup or styling?

**Recommended default:** Prohibit substitution during the parity pass; correct markup rather than compensate with divergent CSS.

**Skip when:** Existing rules already prohibit it.

## Imports And Classification

**Trigger:** Initial data requires normalization, image matching, derived families, relationships, or other semantic mapping.

**Decision:** Which transformations are deterministic, and what ambiguity must stop the import?

**Recommended default:** Allow only unambiguous transformations; report ambiguous normalization, matching, or classification instead of guessing.

**Skip when:** A complete mapping table or deterministic rule exists.

## Visible Divergence

**Trigger:** Technical constraints, accessibility concerns, defects, or framework behavior could motivate changing the UI.

**Decision:** Who approves visible divergence, and when?

**Recommended default:** Require user approval before implementation; documentation afterward is not approval.

**Skip when:** The repository already has this policy.

## Post-Parity Refactoring

**Trigger:** The workflow permits cleanup or refactoring after parity.

**Decision:** Which verified properties must remain invariant?

**Recommended default:** Preserve DOM nesting, classes, stylesheet rules, media queries, visible behavior, and interaction flow unless a change is approved.

**Skip when:** Existing refactoring rules are equally strict.

## Verification

**Trigger:** Acceptance says only “looks close,” “manual QA,” or lists a few widths.

**Decision:** What evidence proves parity and real functionality?

**Recommended default:** Require state-based side-by-side checks plus real persistence/domain verification; treat screenshots as samples rather than the responsive definition.

**Skip when:** Acceptance gates are already objective and complete.
