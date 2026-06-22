# Simple Artifact Loops

Use this guide when the candidate can be judged directly: prose, a plan, a prompt, an image, a configuration, a design concept, or another bounded artifact.

## Default architecture

```text
versioned input -> blind creator -> immutable candidate
immutable candidate + rubric -> blind evaluator -> raw evaluation
raw evaluation + incumbent -> deterministic finalizer -> archive/promotion
```

The materialization runner is an identity or normalization step. Keep it explicit so the architecture can later support rendering or execution without changing candidate history.

## Candidate contract

Specify:

- exact file type or schema
- required and forbidden content
- normalization rules
- size limits
- whether explanations are part of the candidate
- whether one attempt produces one candidate or a batch

Do not allow free-form output when deterministic parsing matters.

## Evaluation

Prefer absolute evaluation against anchored criteria when comparison to the incumbent would bias judgment. Use direct pairwise comparison only when absolute scoring is demonstrably unreliable and document the resulting exposure.

Rubric dimensions should be:

- observable in the candidate
- distinct enough to justify separate scores
- behaviorally anchored at weak and strong levels
- weighted only when the tradeoff is defensible

Keep hard constraints outside the quality score. Recompute arithmetic and validate schemas in code.

## When scalar replacement works

Strictly higher-score replacement is appropriate when there is one stable objective, calibrated scores, low evaluator variance, and little value in retaining alternatives. Otherwise keep a top-K set or Pareto frontier.

## Personal decision variants

For trips and career paths, the candidate should be a plan or hypothesis, not “the future.” Include:

- assumptions about the user
- hard feasibility constraints
- predicted benefits and costs
- uncertainty
- reversible experiments
- information the user should gather

Rank only after exposing tradeoffs. Let actual feedback start a new epoch rather than quietly rewriting historical criteria.

For relationships, optimize self-knowledge, compatibility hypotheses, discovery questions, and healthy actions. Never model a person as an artifact to acquire or automate consequential interpersonal action.

## Minimum tests

- empty and malformed candidates are rejected
- wrong candidate IDs cannot be finalized
- input or criteria changes make candidates stale
- malformed or inconsistent scores cannot change state
- ties follow the declared policy
- failed evaluation does not block the next candidate
- archives retain raw evidence and incumbent-before state
