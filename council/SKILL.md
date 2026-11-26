---
name: council
description: Convene three Codex subagents for the same review or decision, then have them deliberate toward a shared solution. Use when the user asks for a council or invokes $council.
---

# Council

The parent thread chairs the council. Use native Codex subagents on OpenAI models. Give all three the same assignment and evidence, including the same scope and criteria. Each member reviews the whole task. Use separate agent contexts for independent judgments.

## Prepare the brief

- For a branch review, identify the requested base and merge base. For a review against `main`, prefer the local `main` ref and disclose any fallback to `origin/main`. Record the branch and base revisions, flag pre-existing working-tree edits, and follow the user's scope for those edits. Run relevant checks and share their results. Include the parent's later fixes in the verification diff even if they are uncommitted.
- For a decision, give everyone the same question, constraints, and evidence. Ask what they recommend and what would change their recommendation.
- Ask members to inspect and report. The parent owns file changes and external actions. Keep review inputs stable while members are working on them.

## Run up to three rounds

Default to one `gpt-6.2-astra` and two `gpt-6.2-sol` members at high reasoning effort. Honor an explicitly requested Codex roster. When a default setting is unavailable, use an available OpenAI Codex model and supported effort. All three seats can use the same model. Use fresh contexts supported by the harness for explicit model overrides and send the complete common brief. If a seat remains unfilled, identify it, report the available independent reviews, and end the consensus process.

1. **Independent review.** Spawn the three members in parallel. Share their findings only after all available members have responded. Ask each for the concrete plan they endorse, its supporting evidence, and any blockers with file and line references where applicable. For code reviews, also ask for a score out of 10.
2. **Deliberation.** Once the initial positions are in, verify material claims against the source. Send the same digest of proposals, evidence, objections, and any candidate plan to the same three members. Ask each to explicitly endorse a concrete plan or identify the specific objection preventing endorsement. If the first round already has three explicit endorsements of materially the same plan, record agreement there and skip deliberation.
3. **Final deliberation.** Run this only when the second round produced new evidence or movement toward a shared plan and an objection remains. Give the same three members the narrower open question and ask for final positions. If the second round produced neither new evidence nor movement, stop after it.

Agreement requires three clear endorsements of the same concrete plan, including a shared conclusion that no action is needed when applicable. Members may still prefer another approach. Keep the evidence and exact point of disagreement if agreement is partial or absent. After the third round, report any unresolved disagreement and its practical consequence.

## Act on the result

- For a review request, report the verified findings and the council's conclusion. When the user also asks for fixes, the parent verifies and applies the agreed fixes, then reruns the relevant checks. If only part of the plan has unanimous support, apply only the verified fixes that can stand on their own and report the remaining disputed items.
- If the user requests a fresh review, run one separate verification pass with three fresh agents on the resulting diff and current check results. Run it even if the first review found no blockers. Give the fresh agents the same brief and ask for independent findings. Report any remaining or newly discovered blockers.
- Report the models used by seat, the number and outcome of rounds, the agreed solution or outstanding objections, and any changes and checks completed. Include the reviewers' actual scores for code review passes. Use `no score` for a missing score. Put the summary in the PR description when updating it is part of the task.

Example invocation: `$council Review this branch against main. Fix verified blockers and run a fresh round.`
