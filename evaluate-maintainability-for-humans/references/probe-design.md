# Maintenance-probe design

Use this reference to construct a fair task that reveals repository complexity without testing developer cleverness.

## Contents

- [Calibrate the participant](#calibrate-the-participant)
- [Default probe profile](#default-probe-profile)
- [Useful probe families](#useful-probe-families)
- [Reject unfair probes](#reject-unfair-probes)
- [Hidden change-model template](#hidden-change-model-template)
- [User-facing probe template](#user-facing-probe-template)
- [Hint ladder](#hint-ladder)
- [Overall difficulty scale](#overall-difficulty-scale)
- [Dimension ratings](#dimension-ratings)
- [Debrief sequence](#debrief-sequence)
- [Read-only walkthrough mode](#read-only-walkthrough-mode)
- [Retrospective mode](#retrospective-mode)
- [Comparable repeat probes](#comparable-repeat-probes)

## Calibrate the participant

Record only context needed to interpret the result:

- repository familiarity: new, occasional, or regular maintainer;
- language and framework familiarity: unfamiliar, working, or strong;
- domain familiarity: unfamiliar, partial, or strong;
- evaluation mode: live change, read-only walkthrough, retrospective, or repeat evaluation.

Do not turn this into a personnel assessment. The purpose is to identify friction in the code for this developer context.

## Default probe profile

Prefer a routine change that:

- takes an informed maintainer roughly 5–20 minutes;
- changes one product concept;
- has a plausible authoritative owner;
- may cross boundaries only where responsibilities genuinely differ;
- has observable acceptance criteria and focused verification;
- is safe, reversible, and isolated from unrelated work;
- resembles work the repository is likely to receive again.

The exact duration is contextual. Do not use a stopwatch as the primary measure.

## Useful probe families

Adapt these to the repository rather than copying them mechanically.

### Change one rule

Examples: adjust a validation boundary, permission condition, status transition, retry rule, or display rule.

Reveals: ownership, duplicated knowledge, caller leakage, verification boundaries.

### Add one existing kind of thing

Examples: add one supported option, field, command, route variant, state, formatter, or rendering case following a current pattern.

Reveals: extension path, change amplification, special-case growth, generated or registered entry points.

### Change one representation

Examples: alter a label, serialized field, URL parameter, error presentation, unit, or date format wherever that concept appears.

Reveals: authoritative representation, information leakage, UI/domain/storage coupling.

### Change one interaction

Examples: adjust when an action is available, where navigation goes, or how a state transition responds.

Reveals: state ownership, lifecycle distribution, event or callback fragmentation.

### Explain and verify one failure

Examples: identify why a realistic input is rejected or why a request takes a fallback path, then name the smallest safe fix and test.

Reveals: error complexity, hidden dependencies, debugging affordances.

## Reject unfair probes

Reject a candidate when:

- the answer depends mostly on an undocumented product decision;
- success requires obscure third-party API knowledge rather than repository understanding;
- the compiler or a global search supplies the full solution mechanically;
- the task is so local that ownership and propagation are never exercised;
- the task is so broad that normal project management dominates the result;
- it requires destructive data changes, credentials, production access, or risky migrations;
- it overlaps unrelated uncommitted work;
- its primary purpose is to expose a hotspot already chosen by the evaluator;
- no credible completion oracle exists.

## Hidden change-model template

Prepare this privately before presenting the task:

```text
Product concept:
Expected owner:
Expected change locations and why each is legitimate:
Potential duplicated or leaked representations:
Plausible misleading destinations:
Dynamic, generated, configured, or convention-based entry points:
Behavior that must remain unchanged:
Focused completion oracle:
Likely incomplete solutions:
Safety constraints:
```

Treat this as a hypothesis. Do not expose it during the initial probe, and revise it when the developer finds better evidence.

## User-facing probe template

```text
Please make this small maintenance change:

<Requested behavior in product or domain language.>

Acceptance criteria:
- <Observable result 1>
- <Observable result 2>
- <Behavior that must remain unchanged>

Keep the change focused and avoid unrelated cleanup. Work in your normal way. You do not need to narrate continuously, but please notice where you looked first, where you backtracked, what surprised you, and how you decided the change was complete.

Reply when you are done, blocked, or want a hint. I will not reveal the expected location unless you request help.
```

Do not include likely file names, symbols, architecture terms, search terms, or test names when they reveal the answer. It is acceptable to state safety constraints and externally observable behavior.

## Hint ladder

When the developer asks for help, give the smallest useful level and record it:

1. **Concept hint:** restate which product concept owns the decision.
2. **Boundary hint:** identify the architectural area, not the file.
3. **Location hint:** identify the file or module.
4. **Symbol hint:** identify the function, callback, or data definition.
5. **Change hint:** explain the likely edit.

Stop after one level and let the developer continue. Do not silently escalate several levels in one answer.

## Overall difficulty scale

Ask for one selection before revealing the hidden model:

1. **Immediate:** the correct place and completion path were obvious.
2. **Straightforward:** minor navigation, with no meaningful uncertainty.
3. **Search-heavy:** several locations or concepts had to be inspected.
4. **Ambiguous:** multiple plausible owners, repeated backtracking, or weak confidence.
5. **Unsafe or blocked:** the developer could not complete the change confidently.

Accept a short explanation but do not require one before proceeding.

## Dimension ratings

Rate each from 1 to 5 using developer report plus observable evidence:

- **Discoverability:** how directly the developer found the responsible owner.
- **Locality:** how well related knowledge was kept together.
- **Change surface:** how many coordinated representations or owners had to change.
- **Mental load:** how many facts, states, exceptions, or sequencing rules had to be remembered.
- **Verification confidence:** how directly the developer could establish correctness and completeness.

Use `not observed` when evidence is insufficient. Never invent numerical precision by averaging these ratings into a pseudo-scientific score.

## Debrief sequence

Ask one question per turn when practical:

1. Request the overall difficulty selection.
2. Ask where the developer first looked and why.
3. Ask about the highest-signal observed friction: backtracking, memory burden, surprise, or uncertainty.
4. Ask what established completeness and confidence.
5. Ask one counterfactual question only if it will clarify a refactoring goal.

Inspect the diff after collecting the developer's experience so the expected solution does not lead their report. If operational constraints require inspecting earlier, do not reveal conclusions until debriefing is complete.

## Read-only walkthrough mode

Ask the developer to:

1. Identify the first place they would inspect.
2. Trace likely affected behavior.
3. Name expected edits without making them.
4. Explain how they would verify completeness.
5. Stop when they believe the plan is sufficient.

Rate discoverability, cognitive load, and unknown-unknown risk, but label change-surface and verification conclusions as predicted rather than observed.

## Retrospective mode

Start from the developer's unprompted narrative before inspecting the diff. Ask for:

- first destination;
- unexpected locations;
- backtracking or discarded approaches;
- information held in memory;
- final verification and confidence.

Use version-control evidence to reconstruct the change surface, but acknowledge that searches and abandoned paths may be unavailable.

## Comparable repeat probes

After refactoring, choose a different task with similar:

- expected effort and product familiarity;
- number and kinds of legitimate boundaries;
- need to locate an owner;
- propagation and verification demands;
- risk level.

Do not compare a cross-cutting rule change before refactoring with a local text edit afterward. Document why the probes are structurally comparable and note any familiarity advantage.
