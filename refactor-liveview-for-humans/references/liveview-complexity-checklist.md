# Worked LiveView Refactoring Comparisons

Use these examples when comparing designs. Adapt the reasoning and measurements, not the names.

## Contents

- Lifecycle duplication
- Stateful component used for organization
- Repeated page header
- Socket-aware helper
- Context boundary that looks thin
- Competing state owners
- Comparison worksheet

## Lifecycle duplication

Current path:

`mount/3` parses query params, loads records, and assigns filters. `handle_params/3` repeats the same work after every patch with slightly different defaults.

### Design A: keep both paths and share smaller helpers

- Two lifecycle callbacks still coordinate initialization.
- A developer must remember which defaults apply in each path.
- More helpers reduce repeated lines but do not create one owner for URL state.
- Reconnect and patch behavior can still diverge.

### Design B: let `mount/3` establish non-URL state and `handle_params/3` own URL state

- One callback parses, validates, canonicalizes, queries, and assigns URL-driven state.
- Mount keeps subscriptions, uploads, static options, or other non-URL initialization.
- Initial load, reconnect, and patches use the same URL policy.

Choose B when the state must be reproducible from the URL. Keep work in mount when it is not URL-driven or must run only for a connected socket.

## Stateful component used for organization

Current path:

`CatalogLive` renders `ToolbarComponent`, `CounterComponent`, and `EmptyStateComponent`. Each LiveComponent receives parent assigns, has no independent state, and forwards events to the parent.

### Design A: keep the LiveComponents and document their message protocol

- Four lifecycle surfaces remain.
- Callers learn component IDs, `phx-target` behavior, update callbacks, and message shapes.
- The parent remains the true state owner.

### Design B: use local HEEx or function components

- Keep one-use markup local.
- Extract a function component only for a repeated stable presentation concept.
- Pass caller-owned event bindings through explicit attributes or slots.
- Remove component IDs and update/message protocols that no longer serve state ownership.

Choose B when the components exist only to shorten the parent. Keep a LiveComponent when independent state and event handling reduce the parent contract or the component is meaningfully reused with its own lifecycle.

## Repeated page header

Current markup in two LiveViews has the same container, eyebrow, title, description, responsive classes, and action region.

### Design A: keep both copies

- A visual or accessibility change requires two coordinated edits.
- Tests and selectors can drift.
- Each page remains locally obvious.

### Design B: add one app-specific function component

```elixir
attr :eyebrow, :string, required: true
attr :title, :string, required: true
attr :description, :string, required: true
slot :actions

def page_header(assigns) do
  ~H"""
  <header class="page-heading">
    <div>
      <span class="eyebrow">{@eyebrow}</span>
      <h1>{@title}</h1>
      <p>{@description}</p>
    </div>
    {render_slot(@actions)}
  </header>
  """
end
```

- One component owns the shared DOM and responsive contract.
- Each caller keeps its action event and policy in the slot.
- Three text attrs and one optional slot are the entire new interface.

Choose B when both headers are one UI concept expected to change together. Keep separate markup when the structures only look similar or are already diverging. Do not add variants to combine a page header with a wizard header.

## Socket-aware helper

Current API:

```elixir
Pagination.apply_options(socket, params, force_reset)
```

The helper reads several undocumented assigns, queries a context, updates streams, and sometimes pushes a patch.

### Design A: keep the socket helper and improve its name

- The name becomes clearer, but callers and tests must still construct a socket with hidden required assigns.
- Query, URL, and stream policy remain mixed.
- The helper is difficult to reuse outside this LiveView.

### Design B: separate the reusable decision from the page transition

```elixir
case Pagination.resolve(current_options, params, count, config) do
  {:reset, options, pagination} -> update_page(socket, options, pagination)
  {:keep, options} -> assign(socket, :options, options)
end
```

- The pure function owns conversion and pagination rules.
- The LiveView owns queries, assigns, streams, and navigation.
- Tagged outcomes make the state transition explicit.

Choose B when the pagination decision is reusable and independently meaningful. Keep one socket helper when it owns a cohesive page transition and splitting it would make every caller coordinate the same steps.

## Context boundary that looks thin

Current path:

`ItemLive.handle_event/3` → `Catalog.archive_item/2` → `Repo.update/2`

### Design A: call `Repo` from the LiveView

- One function disappears.
- The web layer now knows changeset and persistence details.
- Future authorization, transactions, broadcasts, or derived updates must be coordinated from callers.

### Design B: retain the context operation

- The LiveView requests the application outcome “archive item.”
- The context remains the owner of persistence and domain effects.
- The web layer handles only the success or error outcome.

Choose B when the context operation expresses application language and preserves the web/application boundary. Remove a wrapper when it merely renames another context call while leaking the same arguments, return types, and internal details.

## Competing state owners

Current path:

- A parent LiveView stores a streamed item.
- A LiveComponent stores another copy of the item.
- The component updates its copy after save.
- PubSub updates only the parent copy.

### Design A: synchronize both copies with more messages

- Every update path must notify both owners.
- More message shapes and ordering rules appear.
- Stale-state failures remain possible.

### Design B: select one owner

- If the parent owns the item, send the outcome to the parent and let rerendering update the component.
- If the component owns the item, pass an ID and load/update it there; let the parent own only collection membership and routing.
- Route PubSub updates through the selected owner.

Choose the owner that makes the traced user interaction cross fewer state representations. Do not keep two writable copies without a demonstrated synchronization requirement.

## Comparison worksheet

```text
Task being traced:
Current route and lifecycle path:
Current state owners:
Repeated facts or DOM contracts:
Internal details callers know:
Artifacts that appear obsolete:

Design A — smallest safe improvement:
- Files and callbacks visited:
- Facts and lifecycle rules remembered:
- State owners and representations:
- Places changed together:
- New attrs, slots, events, messages, options, and errors:
- Details hidden:
- Invalid states or failure paths:
- Artifacts added, superseded, or removed:
- Migration and behavior risk:

Design B — alternative:
- Files and callbacks visited:
- Facts and lifecycle rules remembered:
- State owners and representations:
- Places changed together:
- New attrs, slots, events, messages, options, and errors:
- Details hidden:
- Invalid states or failure paths:
- Artifacts added, superseded, or removed:
- Migration and behavior risk:

Choice:
Concrete reason:
Behavior and DOM contracts to preserve:
Protection tests:
```
