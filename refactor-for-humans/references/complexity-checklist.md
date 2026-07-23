# Worked Refactoring Comparisons

Use these examples to make design comparisons concrete. Adapt the reasoning, not the names.

## Forwarding service

Current path:

`OrderController.create` → `OrderService.create` → `OrderManager.create` → `OrderRepository.insert`

The service and manager pass the same order object forward and return the repository result. Neither applies a rule or owns a transaction.

### Design A: keep the layers and improve their names

- Four files remain on the path.
- A developer must still inspect each layer to discover that it does nothing.
- The names change, but no knowledge or dependency disappears.

### Design B: controller calls the repository operation

- Two files remain on the path.
- The controller owns request policy; the repository owns persistence.
- If creation later needs a transaction spanning multiple writes, introduce an operation that owns that transaction then—not an empty layer now.

Choose B unless repository conventions or a demonstrated boundary require the service.

## Many feature-specific methods

Current text API:

```text
backspace(cursor)
deleteForward(cursor)
deleteSelection(selection)
replaceSearchResult(result, text)
```

Each UI feature adds another method. The text module must know UI concepts such as cursors, selections, and search results.

### Design A: add the next UI method

- Small immediate diff.
- The API grows with every feature.
- UI knowledge continues to leak into the text module.

### Design B: expose range operations

```text
insert(position, text)
delete(start, end)
```

- The UI translates its actions into positions and ranges.
- The text module owns text mutation without knowing UI features.
- New UI operations can reuse the same two methods.

Choose B when current UI operations are naturally expressible as range edits. Do not generalize further into a command framework without another demonstrated need.

## Split validation pipeline

Current caller code:

```text
reader = FileReader(path)
tokens = Tokenizer(reader).tokenize()
context = ParserContext(tokens, defaults)
config = Parser(context).parse()
ConfigValidator(schema).validate(config)
```

Every caller must know the pipeline order, intermediate types, defaults, and cleanup/error behavior.

### Design A: add a facade but keep all components public

- The common path becomes shorter only if callers voluntarily use the facade.
- Two supported paths now exist.
- The old components remain knowledge the team may need to maintain.

### Design B: make `loadConfig(path)` the supported operation

- The module owns reading, parsing, validation, defaults, and source-aware errors.
- Callers provide a path and receive a valid configuration or one documented domain error.
- Keep an internal stage separate only when it is independently complex or tested, not because every step needs a public class.

Choose B if callers do not need to customize individual stages.

## Boolean growth

Current API:

```text
send(message, retry=true, async=false, durable=false)
```

The booleans create eight combinations, some invalid. Call sites such as `send(msg, true, false, true)` are hard to interpret.

### Design A: replace booleans with an options object

- Names become clearer.
- The same combinations and invalid states remain.
- Complexity is moved, not removed.

### Design B: identify real supported operations

For example, make ordinary sending reliable by default and expose a separate queue operation only if queued delivery is genuinely different.

- Callers stop choosing internal mechanisms.
- Invalid combinations disappear.
- The module owns retry and durability policy.

Choose B after confirming which behaviors are actually required.

## Comparison worksheet

For the real code under review, write:

```text
Task being traced:
Current path:
Repeated facts:
Internal details callers know:

Design A — smallest safe change:
- Files visited:
- Facts remembered:
- Places changed together:
- New caller-visible concepts:
- Details hidden:
- New failure states or migration risk:

Design B — alternative:
- Files visited:
- Facts remembered:
- Places changed together:
- New caller-visible concepts:
- Details hidden:
- New failure states or migration risk:

Choice:
Concrete reason:
Behavior-protection tests:
```
