# Executable Transformation Loops

Use this guide when the candidate is executed to produce outputs: code, a prompt-program, an agent workflow, a Codex skill, a migration rule set, or another transformer.

## Default architecture

```text
training evidence -> creator -> executable candidate package
candidate + selected source cases -> isolated runner -> produced outputs + telemetry
outputs + permitted references -> evaluator suite -> raw evidence
validated evidence + incumbent -> deterministic finalizer -> archive/promotion
hidden holdout -> promotion check or periodic audit
```

Evaluate both the produced outputs and how they were produced.

## Dataset boundaries

Split cases by role:

- **Development cases:** visible to candidate creators when examples are needed.
- **Validation cases:** executed repeatedly for candidate ranking; references remain hidden from candidates.
- **Holdout cases:** untouched during ordinary iteration and used for promotion or periodic audit.

Prefer splitting by meaningful structural families, not random files, so near-duplicates do not cross boundaries. Hash and version manifests. Never place hidden references in a workspace the candidate can inspect.

If the dataset is too small for a holdout, say so. Use cross-validation, synthetic cases, or human review, but do not pretend validation performance proves generalization.

## Candidate package

Define:

- entry point and invocation contract
- required skill or program structure
- dependencies and lockfiles
- permitted tools and network policy
- resource limits
- output schema and destination
- provenance and parent candidate IDs

Reject candidates that modify inputs, read prohibited paths, depend on undeclared state, or fail setup.

## Runner

Start each run from a clean source snapshot. Capture:

- exit status and categorized failures
- generated file tree and hashes
- stdout/stderr and tool traces as appropriate
- time, tokens, API cost, and system resources
- deterministic test results
- rendered screenshots or accessibility trees when visual output matters

Use timeouts and cleanup. Preserve evidence for failed candidates. Cache only when candidate, case, environment, and runner versions all match.

## Evaluation suite

Use layered evaluation rather than one similarity metric:

1. **Hard gates:** parses, compiles, renders, preserves required behavior, respects boundaries.
2. **Structural tests:** expected files, DOM/template structure, interfaces, content preservation.
3. **Behavioral tests:** user flows, runtime behavior, responsive states, accessibility.
4. **Reference comparison:** semantic, structural, visual, or task-specific similarity.
5. **Quality judgment:** maintainability, generality, elegance, and non-overfitting.
6. **Efficiency:** execution time, token usage, retries, and cost.

Reference similarity is evidence, not automatically the objective. A manual output may contain incidental choices or defects. Declare which properties are authoritative.

## Theme-conversion pattern

For old views `A`, manual new-theme views `B`, and a candidate conversion skill:

- Treat paired `A -> B` examples as a dataset, not as one monolithic prompt.
- Prevent the skill under test from reading reference `B` while producing its output.
- Compare generated `B'` with `B` using template validity, content preservation, DOM semantics, screenshots at representative widths, interaction tests, and accessibility checks.
- Include structurally different views in the holdout set.
- Penalize hardcoded page-specific output and undeclared manual intervention.
- Promote only after the candidate succeeds from a clean installation on holdout inputs.

Pixel similarity alone is insufficient: it can reward broken semantics and punish harmless rendering variance.

## Skill-candidate integrity

When optimizing a Codex skill:

- install or expose only the candidate skill and declared dependencies in the runner
- invoke it with realistic user prompts, not evaluator-specific instructions
- ensure candidate instructions cannot locate hidden expected outputs
- retain the generated files and complete run evidence
- test generalization with unseen project structures and naming
- distinguish generation quality from runner failures or dependency failures

## Minimum tests

- prohibited reference access is impossible or detected
- source inputs remain unchanged
- setup and execution timeouts are enforced
- failed candidates cannot win or block the queue
- environment changes start a new epoch
- cached results cannot cross candidate or case versions
- validation and holdout results remain separate
- promotion and rollback both work
- known hardcoded candidates fail unseen cases
