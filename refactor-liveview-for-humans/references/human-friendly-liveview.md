# Human-Friendly LiveView Conventions

Use these conventions as defaults for touched code after repository instructions, framework correctness, and established local conventions. Apply them to reduce navigation and remembered rules, not to create unrelated style churn.

These defaults were distilled from the maintainer's conventions in `/Users/erikuus/dev/elixir/phoenix-playground-18/lib/live_playground_web/controllers/page_html/rules.html.heex`. Treat that file as provenance and optional local calibration, not as a runtime dependency of this skill.

## Contents

- Organize LiveView functions in reading order
- Keep code comments and documentation useful
- Order assigns and streams coherently
- Choose concise or expanded code deliberately
- Name helpers by responsibility and return shape
- Extract repeated presentation without creating component collections
- Keep PubSub protocols recognizable
- Remove orphaned artifacts

## Organize LiveView functions in reading order

Prefer this order in a touched LiveView module:

1. `@moduledoc`, `use`, imports, aliases, and module attributes.
2. `mount/3`, followed by helpers used only by mount.
3. `handle_params/3`, followed by helpers used only by parameter handling.
4. `render/1`, when defined.
5. Local function components called by render, in rendering order. Place each component's `attr` and `slot` declarations immediately before its function.
6. All `handle_event/3` clauses.
7. All `handle_async/3` clauses.
8. All `handle_info/2` clauses.
9. `handle_call/3` and `handle_cast/2`, when genuinely required.
10. `terminate/2`, when present.
11. Remaining helpers for rendering, events, messages, and shared behavior.

Keep every clause of one function and arity contiguous. Follow step-down order within each section: place a private helper immediately after its sole high-level caller when this does not break the lifecycle sequence. Place helpers shared by distant callbacks in the final shared-helper section. Place helpers shared by other helpers after the highest-level shared helper that introduces the sequence.

Do not extract a helper solely to satisfy ordering. Do not reorder an otherwise coherent untouched module as collateral work.

## Keep code comments and documentation useful

Prefer precise modules, functions, variables, pattern matches, tagged tuples, and module attributes over comments that restate syntax.

Use `@moduledoc` and `@doc` for public context operations and reusable helper or component APIs when callers need to understand guarantees, inputs, outputs, errors, units, side effects, or examples. Use code comments for:

- invariants and ownership;
- non-obvious framework constraints;
- units, ordering, or concurrency guarantees;
- workarounds and their removal conditions;
- reasons a simpler-looking implementation would be incorrect.

Delete comments that narrate the next line or describe code that no longer exists.

## Order assigns and streams coherently

Within one socket transition, establish ordinary and derived UI state before applying stream operations unless behavior requires another order.

```elixir
socket
|> assign(:options, options)
|> assign(:count, count)
|> stream(:items, items, reset: true)
```

Read the sequence as “establish page state, establish derived state, update the rendered collection.” Keep related assigns together. Do not claim that `stream/4` inherently depends on preceding assigns; use the order to make the state transition readable and predictable.

Avoid writable duplicate collections in ordinary assigns and streams. Keep side metadata only when it has a clear owner and cannot be derived safely from the authoritative state.

## Choose concise or expanded code deliberately

Use a concise pipeline for one linear operation whose intermediate results add no useful names.

```elixir
socket
|> assign(:items, Catalog.list_items(params))
```

Bind named intermediate values when the code computes several related facts, branches, validates, queries, or updates multiple parts of state.

```elixir
options = Pagination.convert_params(params)
count = Catalog.count_items()
valid_options = Pagination.validate_options(options, count)

socket =
  socket
  |> assign(:options, valid_options)
  |> assign(:count, count)
  |> stream(:items, Catalog.list_items(valid_options), reset: true)
```

Do not compress important decisions into nested calls or a pipeline whose stages hide branching and failure outcomes. Do not expand a single obvious expression into ceremonial variables.

## Name helpers by responsibility and return shape

Choose names that let a reader predict what kind of value comes back:

- Use action-oriented verbs such as `apply_*`, `assign_*`, `put_*`, `reset_*`, or `load_*` for coherent socket transitions.
- Use transformation verbs such as `convert_*`, `normalize_*`, `validate_*`, `build_*`, or `resolve_*` for data transformations.
- Use `get_*`, `list_*`, `count_*`, or `fetch_*` according to the retrieval contract and repository convention.
- End predicates in `?`.
- Use `!` for raising variants when consistent with the surrounding API.

Avoid vague helpers such as `process/2`, `handle_data/1`, `do_work/1`, or `prepare/1` unless the surrounding domain makes the outcome unambiguous. Avoid names that conceal whether a function performs I/O, navigation, persistence, or a socket update.

## Extract repeated presentation without creating component collections

Keep first-use HEEx local while the design is evolving. At the second meaningful occurrence of the same UI concept, evaluate and normally extract a function component. At the third occurrence, extract unless the instances have a concrete reason to evolve independently.

Preserve the shared DOM, classes, accessibility, responsive behavior, and stable semantics in the component. Expose content and caller policy through a small set of typed attrs and named slots. Keep caller-specific events, navigation, authorization, and conditions in the caller.

Do not:

- extract one-use markup merely to shorten `render/1`;
- create anticipated headers, cards, modals, or form controls without callers;
- use a stateful LiveComponent for generic DOM organization;
- combine different concepts with `variant`, `compact`, `mode`, or other option growth;
- pass all assigns when the component needs only a few explicit values.

Prefer an app-specific component over forcing application markup through a generated core component with a different DOM or visual contract.

## Keep PubSub protocols recognizable

For a new internal PubSub protocol, prefer a message that identifies its producing module:

```elixir
{Catalog, {:updated, item}}
```

Inside the producer, construct it as:

```elixir
{__MODULE__, {event, resource}}
```

Keep the topic, producer, event vocabulary, payload, publisher, handlers, tests, and documentation consistent. Preserve an established repository protocol unless ambiguity, collisions, or duplicated handling are part of the refactoring problem.

Use a struct or another explicit message type when the protocol carries enough fields, versions, or variants that nested tuples become difficult to understand.

## Remove orphaned artifacts

After a refactor, inspect all affected components, helpers, templates, aliases, imports, assigns, callbacks, events, messages, hooks, styles, tests, and modules.

Remove task-created artifacts without callers and old paths superseded by the refactor. Check text references, compiled dependencies, routes, configuration, supervision, callbacks, Phoenix template conventions, dynamic dispatch, tests, hook names, DOM selectors, and CSS classes before declaring an artifact unused.

Do not retain a compatibility wrapper, alternate component, or generic helper for hypothetical future use. If an apparent orphan remains, record its concrete caller, convention, generator contract, or removal condition.
