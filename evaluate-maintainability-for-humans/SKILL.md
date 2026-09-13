---
name: evaluate-maintainability-for-humans
description: Evaluate how maintainable a real repository is for a human by running live maintenance probes in isolated disposable worktrees, withholding location hints, interviewing the developer about navigation and cognitive load, inspecting the resulting change and verification, and producing an evidence-backed complexity diagnosis and refactor handoff. Use when Codex must measure change friction before or after a refactor, diagnose unclear ownership, duplication, coupling, obscurity, change amplification, cognitive load, or unknown-unknown risk, or compare whether one design is easier for developers to modify. Supports any language or framework and live-change, read-only walkthrough, retrospective, and before/after evaluation modes.
---

# Evaluate Maintainability for Humans

Measure how easily a developer can make a realistic change. Treat successful maintenance as the ability to find the right owner, understand only the necessary concepts, make few coordinated edits, and verify completeness with confidence.

Do not substitute static taste, code metrics, or agent confidence for a developer's experience. Do not use line count, function length, file count, abstraction count, or elapsed time alone as measures of maintainability.

## Preserve evaluation integrity

- Evaluate the code, never the developer.
- Let observed developer friction lead the diagnosis. Use static inspection to form hypotheses and a hidden answer key, not to overwrite the developer's report.
- Do not perform the selected change for the developer or reveal its likely location before the probe.
- Give at most one probe at a time. Pause after presenting it so the developer can attempt it.
- Record requested hints as evidence. Give only the smallest useful hint and do not shame the request.
- Treat a wrong first edit, missed location, or disproportionate confidence as diagnostic evidence rather than failure.
- Keep the evaluator independent. Do not refactor unless the user separately asks for implementation.
- Preserve existing work. Inspect repository instructions and worktree state before proposing a live change, and avoid probes that overlap unrelated edits.

## Isolate live probes

Run every live-change or repeat probe in a dedicated disposable Git worktree so the evaluated application and the user's normal checkout remain unchanged.

- Before presenting a live probe, confirm that the current task is attached to a new evaluation worktree created from the committed baseline being evaluated. Treat a branch name or ref as the baseline; record it for the report.
- If the current task is operating in the user's normal checkout, do not ask the developer to edit there. Ask them to start or fork the evaluation in a new worktree and pause. Do not switch branches, stash changes, or construct the worktree inside their normal checkout on their behalf.
- If the intended baseline includes uncommitted changes that cannot be represented safely in a new worktree, ask the user to choose a committed baseline or use a read-only walkthrough or retrospective instead. Never copy, stash, or commit those changes implicitly.
- Keep all probe edits, test artifacts, and experimental cleanup inside the evaluation worktree. Do not merge, cherry-pick, push, or present the probe as product work.
- Keep the worktree available until the debrief, diff inspection, verification inspection, and report are complete. Then state that the evaluation is complete and the disposable worktree may be deleted. Delete it only when the user explicitly asks.
- For an after-refactor probe, create a fresh disposable worktree from the refactored baseline. Do not reuse the before-probe worktree.

If the repository is not Git-backed or an isolated worktree cannot be used, do not run a live-change probe. Use a read-only walkthrough or retrospective and label the limitation.

Always read [references/complexity-diagnostics.md](references/complexity-diagnostics.md) before selecting questions or diagnosing results. Read [references/probe-design.md](references/probe-design.md) before constructing a live, read-only, or repeat probe. Read [references/reporting.md](references/reporting.md) before producing the final evaluation or a refactor handoff.

## Choose the evaluation mode

Use the least artificial mode that fits the user's circumstances:

1. **Live-change probe, preferred:** ask the developer to implement one small, reversible change in a dedicated disposable worktree while using their normal tools and workflow.
2. **Read-only walkthrough:** ask the developer to identify the owner, describe the edits, and explain verification without changing files.
3. **Retrospective:** evaluate a change the developer has just completed using their recollection, the diff, searches, and verification evidence.
4. **Before/after comparison:** run one probe before refactoring and a different but structurally comparable probe afterward.

If no human participant is available, perform only a static maintainability hypothesis. Label it explicitly as unvalidated and do not manufacture developer observations.

Record whether the developer is new to the repository, occasionally familiar, or a regular maintainer. Also record material unfamiliarity with the language, framework, tools, or domain so it is not mistaken for structural complexity.

## Build a hidden change model

Inspect repository instructions, nearby conventions, implementation, callers, tests, configuration, generated entry points, and worktree state. Before presenting a probe, determine privately:

- the behavior and product concept being changed;
- the likely owner and expected change surface;
- plausible but incorrect or incomplete locations;
- duplicated rules, coupled decisions, and non-obvious dependencies that may matter;
- the narrowest credible verification and signs of incomplete work;
- safety boundaries and behavior that must remain unchanged.

This is an evaluator's hypothesis, not ground truth. Revise it when the developer uncovers evidence the initial inspection missed. Do not expose file names, symbols, architecture labels, search terms, or tests that would reveal the path unless they are part of the public task or a requested hint.

## Select one maintenance probe

Choose a routine, product-realistic change that is normally completable in about 5–20 minutes. Prefer a probe that exercises ownership, propagation, or verification without requiring broad implementation.

The probe must be:

- precise enough to have observable acceptance criteria;
- bounded, reversible, and safe in the disposable evaluation worktree;
- representative of ordinary maintenance in this repository;
- dependent on understanding the code, not trivia or obscure framework knowledge;
- capable of revealing at least one of discoverability, change amplification, cognitive load, dependency, obscurity, or unknown-unknown risk;
- supported by a credible completion check.

Avoid mechanical renames, formatting, generated-file edits, dependency upgrades, broad migrations, speculative features, compiler-guided scavenger hunts, and tasks whose difficulty mainly comes from missing product requirements. Do not deliberately select the worst hotspot unless the user asks for a stress test.

## Present the probe and pause

Give the developer only:

1. The requested behavior in product or domain language.
2. Concrete acceptance criteria.
3. Explicit safety and scope constraints.
4. A request to report completion, inability to proceed, or a need for a hint.

Also state that the work is an evaluation-only experiment: all edits must remain in the disposable worktree and must not be merged or pushed.

Ask the developer to notice their first destination, backtracking, surprising discoveries, information held in memory, and confidence, but do not require continuous narration or impose a timer. Do not front-load the debrief questions.

End the turn after presenting the probe. Do not continue into diagnosis before the developer responds.

## Debrief without leading

Start with the fixed overall difficulty scale from [references/probe-design.md](references/probe-design.md). Then ask one high-signal question at a time, normally three to six questions total. Select questions from the developer's actual path rather than administering the entire question bank.

Prefer experiential wording:

- Ask where the developer first looked, not whether ownership was unclear.
- Ask what had to be remembered, not whether cognitive load was high.
- Ask what was discovered late, not whether unknown unknowns existed.
- Ask what a name suggested, not whether naming was poor.
- Ask which verification created confidence, not whether the tests were good.

Do not reveal the expected change surface until the developer has rated the experience and answered the relevant debrief questions.

## Inspect the result

After the subjective debrief, inspect the developer's diff, changed files, relevant tests, and other available verification. Compare them with the hidden change model and update that model when warranted.

Look for:

- expected and unexpected edit locations;
- repeated representations of one decision;
- edits made only to keep layers or formats synchronized;
- relevant behavior the developer missed or found late;
- verification that depends on broad manual confidence rather than a focused oracle;
- hints or failing checks that exposed hidden dependencies;
- unrelated tooling, environment, or domain obstacles that should be treated as confounders.

Do not treat a missing text search result as proof that no dynamic, generated, configured, or convention-based caller exists. Do not penalize a correct design merely because repository setup or external tooling failed.

## Diagnose from evidence

Map observations first to complexity symptoms—change amplification, cognitive load, and unknown-unknown risk—and then to likely causes such as dependency, obscurity, information leakage, shallow boundaries, mixed responsibilities, special cases, or misleading names.

State each finding as a causal chain:

`observation -> experienced difficulty -> concrete dependency or obscurity -> maintenance risk`

Example:

`The developer opened four plausible owners and edited one before finding the authoritative rule -> ownership was not discoverable -> the same policy is represented in the controller and domain module -> a future change can update only one path.`

Distinguish direct evidence, developer report, evaluator inference, and unresolved uncertainty. Do not diagnose a principle violation without explaining the maintenance effect it produced.

## Report and hand off

Produce the compact report defined in [references/reporting.md](references/reporting.md). Include:

1. Probe and developer context.
2. Evaluated baseline and worktree isolation.
3. Observed path and verification.
4. Overall difficulty plus dimension ratings.
5. Evidence-backed complexity findings.
6. Confounders and uncertainty.
7. A refactor handoff describing the experienced friction, concrete dependency, desired cognitive outcome, behavior to preserve, and how to retest.

Do not prescribe a new abstraction unless the evidence makes its responsibility clear. The evaluator should define what must become easier; the refactoring workflow should compare possible designs.

When the appropriate refactor skill is available, offer the handoff for use with it. Do not invoke or implement the refactor automatically.

## Re-evaluate after refactoring

Use a fresh probe with comparable scope and structural demands. Never repeat the same probe as the primary comparison because repository memory creates a learning effect.

Compare:

- correctness of the first destination;
- navigation and backtracking;
- facts held in memory;
- coordinated edit locations;
- late discoveries and missed paths;
- hint use;
- verification confidence.

Claim improvement only when the new evidence shows lower change friction. A changed score without supporting observations is not sufficient.
