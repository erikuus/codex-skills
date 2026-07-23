---
name: refactor-for-humans
description: Refactor AI-generated or difficult repository code to reduce complexity and human cognitive load while preserving behavior. Use when Codex must inspect real code and simplify excessive files, tiny functions, thin wrappers, pass-through layers, shallow abstractions, caller-specific APIs, speculative patterns, duplicated rules, configuration flags, special cases, unclear ownership, tangled error handling, or broad AI rewrites; then compare designs, implement a focused refactor, and verify it with available tests.
---

# Refactor for Humans

Make a real maintenance task easier. A refactor is successful when a developer can change or debug behavior while opening fewer places, remembering fewer rules, and making fewer coordinated edits.

Do not use line count, function length, file size, or pattern count as measures of quality.

## Inspect before proposing

Read repository instructions and nearby conventions. Determine whether the user wants diagnosis, recommendations, implementation, or review. Do not edit for a diagnosis-only request.

Choose one concrete task that exposes the problem, such as “add a field,” “change this validation rule,” or “find why this request fails.” Trace it through implementation, callers, tests, configuration, and data transformations.

Record:

1. The ordered files and functions a developer must follow.
2. What each step actually adds: a decision, transformation, rule, I/O, or only forwarding.
3. Facts repeated in multiple places: field lists, defaults, formats, status rules, validation, or error mappings.
4. Branches introduced by flags, optional dependencies, fallbacks, special cases, and exception handling.
5. Internal details callers must know to use the code correctly.

State each root cause as a concrete dependency. Example: “The controller must know database column names because the repository exposes storage records.” Do not write only “the code is coupled” or “the abstraction is weak.”

## Apply the matching refactor

### 1. Too many tiny units

**Look for:** one operation split across many files or functions; units used once; names that merely restate one line; readers repeatedly jump away and back.

**Test:** remove the boundary mentally. Would anything important become mixed, or would the operation simply become readable in one place?

**Refactor:** inline or merge adjacent units until each remaining boundary hides a meaningful concern such as persistence, protocol handling, security, a transaction, a reusable algorithm, or an independently tested rule.

**Keep the boundary when:** it isolates a detail that changes independently or prevents callers from needing to understand that detail.

Do not split a sequential operation merely because a function is long.

### 2. Pass-through layers

**Look for:** methods that accept nearly the same arguments, call another method, and return the same result; chains such as controller → service → manager → repository where middle layers make no decision.

**Refactor:** remove the forwarding layer or move a real responsibility into it. A real responsibility might enforce authorization, define a transaction, translate between genuinely different models, select a strategy, or turn low-level failures into domain outcomes.

Renaming arguments, wrapping a return value in an equivalent type, or adding logging alone usually does not justify a layer.

### 3. Shallow abstractions

An interface is everything callers must learn: operations, arguments, return values, errors, call order, configuration, and assumptions. An abstraction is shallow when learning this interface costs almost as much as performing the work directly.

**Look for:** many narrow methods; callers assembling the same sequence; callers handling internal states; an interface larger than the work hidden behind it.

**Refactor:** move the sequence, state rules, validation, cleanup, and error handling inside the module. Expose one operation that completes the caller's goal.

Example: prefer `loadConfig(path)` when it can hide file reading, tokenization, parsing, validation, and source-aware errors. Do not require ordinary callers to connect `FileReader`, `Tokenizer`, `TokenStream`, `ParserContext`, and `ConfigValidator` unless they genuinely need independent control of those stages.

This is a deep module: callers learn a small operation and receive substantial completed work.

### 4. Information leakage and duplicated knowledge

**Look for:** the same field list, storage format, default, validation rule, status transition, or conversion in several modules; callers that know cache keys, table columns, wire fields, retry timing, or object layout.

**Test:** if this fact changes, which files must change together? If the answer is more than one, ask why each place must know it.

**Refactor:** choose one owner for the fact. The owner is the place a developer edits when the fact changes. Make other code request an outcome from that owner or derive their data from its authoritative representation.

Do not “centralize” knowledge in a new helper if every caller still understands and coordinates the same details.

### 5. Caller-specific lower-level APIs

**Look for:** a lower-level module with methods named after UI actions, endpoints, or individual use cases; each new feature adds another method or flag to that module.

**Refactor:** keep caller policy at the higher level. Give the lower module a small set of general operations expressed in its own domain.

Example: a text store should usually support inserting and deleting ranges, not `backspace`, `deleteSelection`, and `replaceSearchResult`. The UI can build its actions from the general text operations without teaching the store about UI features.

Generalize only across demonstrated current needs. Do not build a plugin system, strategy hierarchy, or framework for hypothetical consumers.

### 6. Configuration and special-case growth

**Look for:** boolean parameters, modes, nullable dependencies, fallback chains, environment switches, or repeated `if special_case` branches that multiply behavior combinations.

**Refactor in this order:**

1. Remove options that have one real value.
2. Choose a sensible default instead of making every caller decide.
3. Represent truly different cases with explicit data or separate entry points rather than interacting booleans.
4. Change the core rule when many exceptions are compensating for the wrong rule.

Do not move a branch from one file to another and call that simplification.

### 7. Error complexity

**Look for:** exceptions caught and rethrown unchanged, error types translated at every layer, partial state requiring cleanup, or callers that must remember prohibited call sequences.

**Refactor:** first try to make the failure impossible. Use construction that produces valid objects, atomic operations, idempotent behavior, defaults, or data types that exclude invalid combinations. If failure remains, handle it where the code has enough context to recover or describe a useful domain outcome.

Do not expose every low-level failure merely because it exists internally.

### 8. Obscurity

**Look for:** vague names, surprising side effects, important units or limits left implicit, inconsistent conventions, state changed far from its owner, or behavior discoverable only by reading implementation details.

**Refactor:** use precise names, conventional structure, explicit units and states, and unsurprising control flow. Put state changes beside the code responsible for them.

Comment guarantees, invariants, units, ownership, non-obvious constraints, and design reasons. Do not comment what the syntax already says.

### 9. Rewrite temptation

**Look for:** a proposal that replaces whole subsystems, introduces a new architecture, or cleans unrelated areas to solve a local problem.

**Refactor:** identify the smallest boundary where the root cause can be removed. Preserve behavior, make one coherent change, verify it, then reassess. Accept a slightly imperfect local result when the alternative requires a risky migration with no demonstrated benefit.

## Design twice

For an important change, compare at least two designs. One must be the smallest safe improvement. Use the concrete task from the inspection and answer for each design:

- Which files must the developer open?
- Which facts must the developer remember?
- Which places must change together?
- What new names, operations, arguments, call-order rules, configuration, and errors must callers learn?
- What implementation details can callers forget?
- Which new units perform a decision, transformation, rule, I/O, or substantial completed work?
- Which invalid states or failure paths disappear or appear?
- What behavior and migration risk does the design introduce?

Reject a design when its main benefit is smaller files, shorter functions, more patterns, future flexibility without a current use, or moving complexity behind new names.

Choose the design that makes the traced task simpler while adding the least new machinery. Explain the choice with counts or paths, not adjectives: “one rule owner instead of four,” “controller calls repository directly instead of crossing two forwarding services,” or “callers no longer know the cache-key format.”

See [references/complexity-checklist.md](references/complexity-checklist.md) for worked comparisons when the choice is unclear.

## Implement safely

Before editing, state:

- behavior that must remain unchanged;
- the root cause being removed;
- the new owner of each affected rule or state;
- what callers will do afterward;
- what callers will no longer need to know;
- tests that protect the behavior.

Keep the diff focused. Follow repository conventions. Avoid compatibility wrappers, new flags, duplicate paths, dependencies, and speculative extension points unless repository evidence requires them. If a temporary bridge is unavoidable, state its removal condition.

Run the narrowest relevant tests first, then broader available checks. Check affected callers, defaults, failure paths, and configuration.

Review the diff by repeating the original task. Verify that it now requires fewer jumps, fewer remembered facts, or fewer coordinated edits. If none of those changed, the refactor probably moved or renamed complexity instead of reducing it.

## Report evidence

Report:

1. The traced maintenance or debugging task.
2. The concrete symptom and its root cause.
3. The two designs considered and why one is simpler for that task.
4. Files changed and behavior preserved.
5. Before/after evidence: files visited, call hops, rule owners, caller-visible operations, configuration choices, or failure states.
6. Tests run and anything not verified.

Do not claim success from line count or unit count alone.
