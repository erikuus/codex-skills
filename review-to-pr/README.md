# Review to PR

`review-to-pr` takes a finished topic branch from committed implementation to a reviewed draft pull request. It is designed for a workflow where the human wants to inspect decisions, evidence, and residual risk rather than read every changed line.

## Rationale

Two common review approaches leave an awkward gap:

- PR shepherding waits for several remote AI reviewers, fixes their comments, pushes again, and repeats. It can reach merge-ready state, but duplicate feedback and remote review queues make it slow.
- Local autoreview gives one strong, isolated review before publication. It is faster and safer, but intentionally does not own the complete commit, push, PR, and CI handoff.

This skill combines their useful boundaries without combining their complexity:

- use the pinned upstream `autoreview` helper for isolated review, secret scanning, structured findings, and scope control;
- use one reviewer with P1 coverage by default;
- verify findings before editing;
- run focused tests and required CI as objective proof;
- commit and push only the reviewed landing lane;
- open or reuse one draft PR;
- stop before merge and hand the decision to the human.

It deliberately does not coordinate several AI reviewers or poll optional review bots until they agree.

## Recommended workflow

1. Implement the change on a named topic branch.
2. Run implementation-time tests and commit the intended change.
3. Stay in the same Codex task so the implementing agent retains useful intent and repository context.
4. Invoke `$review-to-pr` explicitly.
5. Let the skill:
   - resolve and refresh the actual base branch;
   - freeze the intended scope;
   - run focused tests;
   - review the complete branch diff with the isolated autoreviewer;
   - verify, classify, and fix accepted in-scope findings;
   - rerun affected proof and autoreview;
   - stop after two non-converging repair cycles;
   - commit review fixes;
   - push normally and open or reuse a draft PR;
   - observe required CI without entering an optional-reviewer polling loop.
6. Read the final decision package: behavior, proof, findings, CI, residual risk, and PR link.
7. Review or test anything you consider material, then give a separate explicit merge instruction if satisfied.

The isolated reviewer receives a validated change bundle in a fresh environment. Running the workflow in the implementation task therefore preserves useful implementation context without weakening reviewer isolation.

## What invocation authorizes

Explicitly invoking `$review-to-pr` authorizes the workflow to:

- apply verified, in-scope review fixes;
- create intentional commits;
- push the current named topic branch without force;
- open or update its draft PR.

It does not authorize:

- merging;
- force-pushing or rewriting history;
- discarding unrelated work;
- broad refactors or out-of-scope fixes;
- silently replacing the pinned autoreviewer;
- running a multi-reviewer panel unless requested explicitly.

Implicit invocation is disabled, so ordinary coding prompts cannot accidentally publish a branch.

## Prompt examples

### Standard review and draft PR

```text
$review-to-pr Review the current topic branch and take it through verified
autoreview, focused tests, and a draft PR. Do not merge.
```

### Specify the base branch

```text
$review-to-pr Review the current branch against origin/release-2.4, fix only
verified in-scope P1 findings, run the relevant tests, and open a draft PR.
Do not merge or rebase.
```

### Review and repair without publishing

```text
$review-to-pr Review the current branch against origin/main with P1 coverage.
Verify and fix accepted findings and rerun focused tests, but stop before
committing, pushing, or creating a PR.
```

### Update an existing PR

```text
$review-to-pr Re-review the branch for its existing PR, address verified
in-scope findings, rerun proof, push normally, update the existing draft PR,
and report required CI. Do not create a duplicate PR or merge.
```

### Small, reversible change with blockers-only review

```text
$review-to-pr Take this small branch to a draft PR using P0-only autoreview.
Run the focused test, report any consciously rejected findings, and do not merge.
```

### Explicit second-model escalation

```text
$review-to-pr This branch changes authentication boundaries. Use the normal P1
review plus one explicitly requested second-model review, verify all findings,
and stop for my decision if the reviewers disagree. Do not merge.
```

## Prerequisites

- A named Git topic branch with the intended implementation committed.
- A resolvable remote base branch.
- Git and authenticated GitHub access for push and PR creation.
- Codex CLI authentication for the default reviewer.
- TruffleHog for mandatory pre-review secret scanning.
- The pinned sibling `autoreview` skill described in
  [`references/autoreview-dependency.md`](references/autoreview-dependency.md).

If review, authentication, secret scanning, push, or CI access fails closed, the skill reports the prerequisite or blocker instead of silently weakening the workflow.

## Maintenance model

Our `SKILL.md` owns the workflow policy. The OpenClaw dependency owns review isolation and bundle validation. Do not modify the installed upstream copy locally.

When updating autoreview:

1. Select and inspect a specific upstream commit.
2. Replace the complete installed `autoreview` directory from that commit.
3. Update the commit and SHA-256 values in the dependency reference.
4. Run upstream self-tests and the skill validator.
5. Keep the dependency pinned; do not follow a moving `main` checkout.
