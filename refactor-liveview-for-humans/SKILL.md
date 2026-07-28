---
name: refactor-liveview-for-humans
description: Refactor AI-generated or difficult Elixir Phoenix LiveView code to reduce human cognitive load while preserving behavior. Use when Codex must inspect, diagnose, review, or simplify LiveViews, LiveComponents, function components, HEEx templates, contexts, changesets, routes, PubSub flows, streams, assigns, event handlers, hooks, helpers, tests, or generated component collections; especially for lifecycle duplication, unclear state ownership, misplaced domain or UI logic, excessive helpers, speculative abstractions, duplicated markup, unused artifacts, tangled params or navigation, and broad AI rewrites.
---

# Refactor LiveView for Humans

Make one real maintenance or debugging task easier across the complete Phoenix LiveView interaction. Count success in fewer navigation jumps, remembered rules, state owners, coordinated edits, and caller-visible contracts. Do not use line count, callback length, file size, or component count as quality measures.

## Establish authority and scope

Read repository instructions, implementation contracts, tests, `mix.exs`, `mix.lock`, formatter configuration, router setup, web macros, and nearby conventions before proposing a design. Identify the installed Elixir, Phoenix, LiveView, and Ecto versions. Use official documentation for those versions when lifecycle, component, HEEx, stream, form, or framework behavior is uncertain.

Treat official correctness, security, lifecycle, and data-handling requirements as constraints rather than optional style tradeoffs. Distinguish those requirements from architectural heuristics and personal conventions. Preserve authorization, tenant or scope filtering, CSRF boundaries, validation, and data integrity throughout the refactor.

Apply guidance in this order:

1. Repository instructions and verified behavior.
2. Official guidance for the installed framework versions.
3. Established conventions in the repository.
4. The human-maintainability defaults in this skill.

Determine whether the user wants diagnosis, recommendations, implementation, or review. Do not edit for a diagnosis-only request. Do not rewrite unrelated code solely to impose style.

For implementation, read [references/human-friendly-liveview.md](references/human-friendly-liveview.md) before reorganizing `.ex` or `.heex` files.

## Trace behavior before proposing

Choose a concrete task such as “add a filter,” “change this validation,” “reuse this page header,” “find why a patch resets state,” or “remove this obsolete component.” Trace it through the relevant vertical slice:

1. Router scope, pipeline, `live_session`, and `on_mount` hooks.
2. Disconnected and connected `mount/3`, `handle_params/3`, navigation, events, messages, and async callbacks.
3. LiveView assigns, streams, forms, uploads, and LiveComponent state.
4. HEEx, function components, DOM IDs, client hooks, and event targets.
5. Context operations, schemas, changesets, queries, transactions, external I/O, and PubSub.
6. Tests, configuration, and dynamically discovered framework entry points.

Record:

- the ordered files, callbacks, functions, and client events a developer must follow;
- the owner of each fact and each mutable state representation;
- what each boundary adds: policy, validation, transformation, I/O, state, recovery, or only forwarding;
- duplicated defaults, params, field lists, URLs, message shapes, markup, DOM contracts, and error mappings;
- branches created by flags, modes, optional assigns, fallbacks, and special cases;
- details callers must know about socket state, component state, changesets, storage, or client hooks;
- artifacts that appear unused or that the proposed design would supersede.

State root causes as concrete dependencies. Prefer “`handle_event/3` must know the storage field names because the context returns raw persistence data” over “the LiveView is coupled.”

## Keep one owner for each concern

Use these defaults unless repository evidence requires another boundary:

- Let the router, pipelines, `live_session`, and `on_mount` own route lifecycle, session scope, and authentication entry points.
- Let the LiveView own page orchestration, URL policy, socket state, navigation, and incoming UI events.
- Let a function component own repeated stateless presentation through explicit attributes and slots.
- Use a LiveComponent only when independent state and event handling justify its lifecycle. Do not use it merely to shorten a LiveView.
- Let a context expose application operations, persistence coordination, authorization rules, transactions, and domain outcomes.
- Let schemas and changesets own data shape, casting, validation, and database constraints.
- Let a helper module own a demonstrated reusable algorithm or transformation. Do not use helpers as a dumping ground for socket code.
- Let a JavaScript hook own browser-only behavior behind a small explicit event and DOM contract.

Do not bypass a context and call `Repo` from the web layer merely because the current context operation is short. A context can be a meaningful application boundary even when its implementation is small. Conversely, do not add context wrappers that merely rename another context operation or leak the same persistence details.

## Apply the matching refactor

### 1. Lifecycle duplication and callback fragmentation

Look for initialization, normalization, queries, subscriptions, or navigation repeated between disconnected mount, connected mount, `handle_params/3`, and events. Look for one operation scattered across tiny helpers that make readers jump without hiding a meaningful concern.

Choose one owner for each lifecycle responsibility. Keep URL-driven state in `handle_params/3` when patches must reproduce it. Guard connected-only work explicitly. Inline or merge single-use helpers when the callback becomes easier to read top-to-bottom; retain helpers that hide a real rule, reusable transformation, substantial state transition, or independently tested algorithm.

### 2. Competing and duplicated state

Look for the same fact stored in URL params, ordinary assigns, streams, LiveComponent assigns, forms, client data attributes, and persistence. Look for derived assigns that can drift or for parent LiveViews and LiveComponents updating separate copies of one entity.

Select one source of truth. Derive or reload secondary representations deliberately. Pass explicit data into contexts and pure helpers instead of the whole socket. Allow a socket-transforming helper only when it owns one coherent UI transition and its name makes that return shape clear.

### 3. Params, URLs, forms, and navigation

Look for parsing, defaults, allowlists, validation, canonicalization, pagination, sorting, filtering, URL construction, or form conversion repeated across callbacks and templates.

Choose one owner for normalization and one canonical representation. Keep public params untrusted. Make invalid combinations impossible where practical. Preserve deep-linking, back/forward behavior, reconnect behavior, validation actions, and patch versus navigate semantics.

### 4. Components and repeated presentation

Look for substantially equivalent HEEx structures in different views. Compare semantic purpose, DOM structure, classes, accessibility, responsive behavior, event policy, and expected change cadence.

At the second meaningful occurrence, evaluate a function component and normally extract it when both instances represent one UI concept that should change together. At the third occurrence, require extraction unless there is a concrete reason the instances must evolve independently. Use `attr/3` and `slot/3` to expose a small explicit contract. Keep caller-specific events, navigation, authorization, and content policy in the caller.

Do not extract one-use markup merely to shorten `render/1`. Do not create a collection of anticipated components. Do not combine different concepts through variants, boolean flags, or broad `:rest` contracts when separate local markup is easier to understand.

### 5. HEEx and render complexity

Keep data loading, persistence, substantial transformation, and side effects out of HEEx. Preserve LiveView change tracking by using assigns and documented component interfaces rather than hidden template variables or generic assign manipulation.

Keep directly understandable presentation local. Extract repeated presentation or a stable screen-level concept, not every HTML fragment. Preserve verified DOM structure, IDs, class names, `phx-*` bindings, hook attributes, focus behavior, and selectors during extraction.

### 6. Context and helper boundaries

Look for web concepts in contexts, persistence details in LiveViews, caller-specific lower-level APIs, pass-through modules, socket-aware general helpers, and duplicated application rules.

Keep UI policy in the web layer and application policy in contexts. Prefer explicit maps, structs, changesets, and tagged tuples. Move a sequence behind a function only when callers can forget meaningful details such as validation, transaction order, cleanup, query composition, or error translation. Generalize only across demonstrated current needs.

### 7. Events, messages, PubSub, async work, and hooks

Look for inconsistent event names, ambiguous tuple shapes, duplicated payload conversion, scattered subscriptions, unnecessary processes, copied sockets in async tasks, and client hooks that own server rules.

Use one explicit protocol per interaction. Keep PubSub topics and message shapes consistent and namespaced when introducing a new internal protocol. Use processes only for runtime properties such as concurrency, isolation, shared resources, or lifecycle. Pass only required values into async work. Keep browser-only mechanics in hooks and domain outcomes on the server.

### 8. Options, failures, and special cases

Remove options with one real value. Prefer a sensible default over requiring every caller to choose. Represent genuinely different cases with explicit data or separate entry points instead of interacting booleans.

Prevent invalid state before translating errors. Let changesets own data validation, contexts own domain and persistence outcomes, and LiveViews own user-facing recovery, navigation, and feedback. Do not catch and rewrap errors at every boundary.

### 9. Orphaned artifacts and speculative code

Do not create components, helpers, templates, wrappers, modules, hooks, or alternate implementations without current callers. Migrate callers when introducing an abstraction. Remove artifacts introduced by the task that remain unused and old paths made obsolete by the refactor.

Audit affected public and private functions, imports, aliases, assigns, callbacks, event handlers, message handlers, templates, components, tests, CSS rules, hooks, assets, and configuration. Use search, compiler warnings, dependency information, routing and configuration inspection, and behavioral tests together. Do not treat a missing text match as proof: Phoenix may discover templates, callbacks, configured modules, layouts, and other entry points by convention or dynamically.

Report unrelated pre-existing candidates rather than expanding a focused change. If an apparently unused artifact remains, identify its concrete caller, framework convention, generator contract, or removal condition. Do not keep it for hypothetical future flexibility.

### 10. Rewrite temptation

Identify the smallest boundary where the root cause can be removed. Preserve verified behavior and make one coherent change. Do not replace a subsystem, invent an architecture, or clean unrelated areas to solve a local problem. Accept a slightly imperfect local result when the alternative adds migration risk without demonstrated maintenance benefit.

## Design twice

For an important change, compare at least two designs. Make one the smallest safe improvement. Trace the original maintenance task through each design and count:

- files and callbacks visited;
- facts and lifecycle rules remembered;
- state owners and representations;
- places changed together;
- component attrs, slots, events, messages, return shapes, options, and errors callers learn;
- details callers can forget;
- invalid states and failure paths removed or introduced;
- migration and behavioral risk;
- artifacts added, superseded, or removed.

Reject a design whose main benefit is shorter callbacks, smaller files, more components, more patterns, or hypothetical flexibility. Choose the design that simplifies the traced task with the least new machinery.

Read [references/liveview-complexity-checklist.md](references/liveview-complexity-checklist.md) when a component, state-owner, context, or URL design choice is unclear.

## Implement safely

Before editing, state:

- behavior and DOM contracts that must remain unchanged;
- the root cause being removed;
- the owner of each affected rule and state;
- what callers will do afterward;
- what callers will no longer need to know;
- the narrow tests that protect the interaction.

Keep the diff focused. Follow the repository's formatter, build aliases, and testing instructions. Apply the ordering, naming, documentation, state-update, component, and PubSub defaults from [references/human-friendly-liveview.md](references/human-friendly-liveview.md) to touched code when they do not conflict with higher-priority guidance.

Run the narrowest relevant tests first, then broader available checks. Cover affected disconnected and connected mounts, params, patches, events, messages, component targets, invalid input, authorization, persistence failures, streams, reconnect behavior, async failures, hooks, and responsive DOM contracts as applicable.

Review the diff by repeating the original task. Verify that it requires fewer jumps, remembered facts, state owners, or coordinated edits. Verify that every new abstraction has current callers and every superseded artifact is removed or explicitly justified.

## Report evidence

Report:

1. The traced maintenance or debugging task.
2. The concrete symptom and root cause.
3. The designs compared and the concrete reason for the choice.
4. Files changed, ownership after the refactor, and behavior preserved.
5. Before-and-after evidence: paths visited, callbacks crossed, state owners, rule owners, caller-visible contracts, options, and failure states.
6. Components and other artifacts added, reused, removed, retained, or found unrelated.
7. Tests and checks run, plus anything not verified.

Do not claim success from line count, callback count, or component count alone.
