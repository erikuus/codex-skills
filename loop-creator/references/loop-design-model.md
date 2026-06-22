# Loop Design Model

Use this reference to make a loop decision-complete. The same model applies whether a candidate is one line of prose or an executable skill.

## Universal objects

### Competition epoch

An epoch is a period in which candidates are comparable. Its identity should hash or otherwise version:

- objective and candidate contract
- fixed input snapshot
- criteria and evaluator versions
- execution environment when relevant
- aggregation and promotion policy

A material change starts a new epoch. In-flight candidates from an older epoch are stale.

### Candidate

Every candidate needs:

- unique ID
- epoch ID
- immutable payload or content-addressed artifact
- creator identity/version
- creation time
- parent IDs when mutated or recombined
- generation settings needed for reproducibility

The payload may be text, structured data, files, code, a skill directory, or a reference to a versioned artifact.

### Run

A run materializes a candidate against zero or more cases. A direct artifact uses an identity run. An executable candidate uses a controlled runner.

Record:

- candidate and case IDs
- environment identity
- start/end time and resource use
- status and failure category
- output artifacts
- logs, diffs, screenshots, or traces

### Evaluation

An evaluation binds raw evidence and judgments to exact candidate, run, criteria, and evaluator versions. Never store only the final score.

Use four layers where applicable:

1. **Validity gates:** required shape, safety, compilation, runtime success, invariant preservation.
2. **Deterministic metrics:** tests, structural similarity, latency, cost, coverage, accessibility checks.
3. **Judged dimensions:** semantic quality, elegance, usefulness, visual coherence, novelty.
4. **Human decision:** required for consequential action or unresolved tradeoffs.

### Decision

A deterministic finalizer should apply the declared selection policy to validated evaluations. Policies include:

- scalar incumbent replacement
- lexicographic ordering after hard gates
- Pareto frontier maintenance
- tournament comparison
- shortlist plus human selection
- statistical promotion after repeated runs

Record the incumbent before the decision, outcome, reason, evidence IDs, and policy version.

## Actor visibility matrix

Define explicit read/write permissions for each actor:

| Actor | Typical reads | Typical writes | Usually hidden |
|---|---|---|---|
| Creator | permitted input, public contract | candidate package | incumbent, scores, hidden references |
| Runner | candidate, selected cases, environment | outputs and telemetry | unrelated cases, decision state |
| Evaluator | candidate outputs, allowed references, rubric | raw evaluation | incumbent and prior scores |
| Finalizer | validated evaluations, policy, incumbent | decision and state | nothing needed for cognition; use code |
| Human | blueprint and evidence | approvals or preference updates | secrets not needed for the decision |

Blindness is optional, but every exposure should be intentional. Separate workspaces and narrow helper commands reduce accidental leakage. They are not an OS security boundary when all actors share one account.

## Choosing a ranking model

Use a scalar score only when:

- dimensions have defensible weights
- small numeric differences are meaningful enough for promotion
- the evaluator is calibrated consistently
- hard failures are rejected before scoring

Use Pareto selection when multiple dimensions represent real tradeoffs. Use lexicographic selection when some qualities dominate others. Use human selection when preferences cannot be honestly encoded. Use repeated evaluation or statistical promotion when execution or judgment is noisy.

Tie policy must be explicit. Preserving the incumbent is the safest default.

## Evaluator validity

Before trusting an evaluator:

- create anchors spanning weak, acceptable, and strong results
- introduce known-bad mutations for each hard gate
- repeat some evaluations blind to estimate variance
- test whether irrelevant presentation changes alter scores
- test whether candidates can exploit rubric wording
- compare proxy gains with downstream outcomes

Do not let the same model’s confidence substitute for validation. Multiple model evaluators are correlated, not independent ground truth.

## Exploration strategy

Independent blind sampling maximizes diversity and is a strong initial default. Mutation of winners can accelerate local improvement but risks convergence and evaluator exploitation. Hybrid strategies may allocate attempts among:

- independent creation
- mutation of recent winners
- repair of specific failures
- recombination of complementary candidates
- adversarial attempts to break the evaluator

Track lineage so apparent progress can be audited.

## Stopping conditions

Declare at least a hard budget and one quality-based stop:

- accepted target reached
- no meaningful improvement over a fixed number of valid candidates
- confidence interval or evaluator variance makes further ranking meaningless
- holdout performance declines
- proxy gaming is detected
- cost or time budget is exhausted
- user chooses among the Pareto frontier

Automation cadence is not a stopping condition.

## Failure modes to surface

- **Goodharting:** candidate improves the metric while worsening the real outcome.
- **Leakage:** creator learns references or holdout data and memorizes them.
- **Overfitting:** validation improves while unseen cases regress.
- **Evaluator drift:** scores change because the model, rubric, or environment changed.
- **False precision:** arbitrary weights produce unjustified rankings.
- **Survivorship bias:** only successful runs are archived.
- **Non-stationarity:** user preferences or external facts change during an epoch.
- **Unsafe autonomy:** winning a benchmark automatically triggers consequential action.
- **Cost blindness:** quality gains ignore inference, execution, or human-review cost.

Design controls for the relevant failures rather than adding machinery indiscriminately.
