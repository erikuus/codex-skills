# Contract Validation Rubric

Run every applicable check before finalizing `IMPLEMENT.md` and `AGENTS.md`.

## Source Integrity

- Every normative source is named and its responsibility is explicit.
- Descriptive prose cannot override demonstrated source/runtime behavior unless an explicit resolution says so.
- `IMPLEMENT.md` and `AGENTS.md` contain the same priority order.
- Existing nested agent instructions are accounted for.
- Product plans and prototype evidence were not modified.

## Conflict Resolution

- Every discovered contradiction is resolved explicitly or remains a blocker.
- No resolution is hidden in vague wording.
- High-risk interaction flows are stated step by step where necessary.
- Material decisions from the interview appear in the contract.
- No material TODO, open question, or undocumented assumption remains.

## Presentation And Real Outcomes

- Demonstrated DOM, controls, copy, layout, visible states, and interaction presentation are protected.
- Demo records, fake counts, preselection, and showcase defaults are separated from production behavior.
- Every stubbed create, update, duplicate, delete, upload, and loading action has a real outcome.
- Real outcomes do not silently introduce new visible states.
- Framework defaults, component libraries, icons, or global styles cannot replace the prototype during parity work unless approved.

## State Completeness

- Clean initial state is explicit for every major screen and flow.
- Production startup data is explicit.
- True zero-data and filtered-empty states are distinct where recovery differs.
- Applicable loading, error, validation, success, archived, disabled, focused, expanded, modal, drawer, and upload states are covered.
- Dirty-state start, exit triggers, discard, save, browser navigation, and reset behavior are explicit.
- Filter, selection, query, focus, scroll, and session lifetimes are explicit where material.

## Data And Destructive Behavior

- Required fields, minimum rules, relationships, archive behavior, and deletion constraints agree with product evidence.
- Import, normalization, matching, mapping, and ambiguity policies are explicit.
- Demo fixtures cannot become production data accidentally.
- Storage and asset paths are specified only when evidence or the user supplies them.
- Destructive actions have explicit confirmation and real outcomes.

## Responsive And Visual Fidelity

- Responsive authority is explicit.
- Exact media-query and breakpoint preservation is required when source evidence and strict parity apply.
- Screenshots are not treated as the complete responsive contract unless explicitly declared authoritative.
- Markup differences must be corrected rather than hidden with divergent CSS when exact parity applies.
- Fonts, icons, assets, element nesting, classes, and global styling are protected to the degree required for parity.
- Visible divergence requires approval before implementation.

## Delivery Discipline

- Implementation order supports complete, verifiable vertical slices.
- Each major screen or flow requires runtime comparison against the prototype.
- Acceptance gates verify both real data behavior and visible parity.
- Post-parity refactoring must preserve verified visual and interaction behavior.
- Agents cannot justify an unapproved divergence by documenting it afterward.

## Language Audit

Search for and remove or precisely qualify phrases such as:

- `as closely as possible`
- `as faithfully as possible`
- `clear bug`
- `minimal visual change`
- `where practical`
- `when reasonable`
- `matches closely`
- `technical reasons`

Use `must`, `must not`, `preserve`, `requires prior approval`, or `stop and ask` when the rule is mandatory.

## Final Cross-Read

Read `IMPLEMENT.md` and `AGENTS.md` together as if implementing the app with no conversation history.
Confirm an implementation agent can determine:

- what controls product behavior;
- what controls presentation and interaction;
- how conflicts are resolved;
- which prototype data or behavior is only demonstrative;
- what the real application must persist;
- which questions require escalation;
- how parity is verified;
- what may never be changed without prior approval.
