# Evaluation reporting

Use this format after the developer debrief and result inspection. Keep evidence distinct from interpretation.

## Contents

- [Maintainability evaluation](#maintainability-evaluation)
- [Before/after comparison](#beforeafter-comparison)
- [Example finding](#example-finding)

## Maintainability evaluation

### Probe

- Requested change:
- Evaluation mode:
- Developer context: repository, language/framework, and domain familiarity
- Safety or scope constraints:

### Observed experience

- First destination and reason:
- Navigation and backtracking:
- Information held in memory:
- Surprises or late discoveries:
- Hints requested:
- Changed locations:
- Verification used:
- Developer confidence:

Mark each item as developer-reported, directly observed, or evaluator-reconstructed when the distinction matters.

### Ratings

- Overall difficulty: 1–5
- Discoverability: 1–5 or not observed
- Locality: 1–5 or not observed
- Change surface: 1–5 or not observed
- Mental load: 1–5 or not observed
- Verification confidence: 1–5 or not observed

For each rating above 2, give one sentence of evidence. Do not calculate a combined score.

### Complexity findings

For each material finding, use:

```text
Observation:
Experienced symptom:
Concrete cause:
Maintenance risk:
Evidence strength: direct | reported | inferred | uncertain
```

Prefer two strong findings over a long inventory of static red flags.

### Confounders and uncertainty

State language, framework, domain, tooling, environment, prior-familiarity, task-selection, and incomplete-observation effects. State what cannot be concluded.

### Refactor handoff

```text
Experienced friction:
Concrete dependency or obscurity:
Desired cognitive outcome:
Behavior and contracts to preserve:
Evidence the refactor must improve:
Constraints and non-goals:
Comparable follow-up probe:
```

Define the outcome without prematurely prescribing a class, service, helper, component, pattern, or file split. A useful outcome is concrete, such as “make this policy discoverable through one authoritative owner and remove the need for callers to know storage field names.”

### Recommendation

Choose one:

- No refactor justified by this probe.
- Gather another probe before deciding.
- Refactor the evidenced boundary.
- Address a verification gap before structural work.
- Resolve a tooling, requirements, or knowledge confounder first.

## Before/after comparison

Report both probes and explain why they are comparable. Compare observations rather than only ratings:

```text
First destination: before -> after
Backtracking: before -> after
Remembered facts: before -> after
Coordinated edit locations: before -> after
Late discoveries or missed paths: before -> after
Hints: before -> after
Verification confidence: before -> after
```

Classify the result as:

- **Improved:** multiple relevant observations show lower friction with no material new burden.
- **Mixed:** some friction moved or improved while another dimension worsened.
- **No demonstrated improvement:** evidence is unchanged, incomparable, or too weak.

Do not claim success because files, functions, lines, or layers decreased unless the developer's task became easier as a result.

## Example finding

```text
Observation: The developer opened four plausible modules and changed one before a focused test revealed the authoritative rule elsewhere.
Experienced symptom: Obscurity and unknown-unknown risk.
Concrete cause: The same policy is represented in both request handling and the domain operation, with neither location identifying the other as authoritative.
Maintenance risk: A future edit can update one path while leaving the other behavior unchanged.
Evidence strength: Direct, supported by the diff, test failure, and developer report.
```

Example handoff:

```text
Experienced friction: The developer could not identify one owner for the policy and needed a failing test to find the second representation.
Concrete dependency or obscurity: Request handling knows and repeats a domain rule.
Desired cognitive outcome: A developer changing the policy should find one authoritative owner and should not need request-layer implementation knowledge.
Behavior and contracts to preserve: Existing accepted inputs, rejection messages, authorization, and public API behavior.
Evidence the refactor must improve: One policy owner, no synchronized policy edit in request handling, and a focused test that establishes completeness.
Constraints and non-goals: Do not redesign unrelated request flow or introduce speculative extension points.
Comparable follow-up probe: Change a different policy enforced through the same boundary and observe whether the first destination is correct.
```
