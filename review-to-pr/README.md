# Review to PR

`review-to-pr` takes a finished, committed topic branch through one independent code review, verified repairs, focused tests, a normal push, and a draft pull request. It then hands the merge decision back to the human.

It is intended for a workflow where humans want to review decisions, evidence, and residual risk without coordinating several AI reviewers or reading every changed line.

## Why this exists

Two useful workflows solve different parts of branch closeout:

- A PR shepherd can coordinate several remote reviewers until everything is merge-ready, but repeated polling, duplicated findings, and review rounds can make that workflow slow and expensive.
- `autoreview` provides a strong isolated review primitive, but intentionally stops at review: it does not define the complete branch-repair, test, commit, push, PR, and CI handoff.

`review-to-pr` keeps the strong isolation of `autoreview` and adds a small, opinionated landing workflow around it. It uses one reviewer by default, verifies findings before changing code, caps repair cycles, creates a draft PR, and never merges.

## The autoreview foundation

This skill depends on the upstream [`autoreview`](https://github.com/openclaw/agent-skills/tree/main/skills/autoreview) skill by ***Peter Steinberger***.

`autoreview` is an excellent piece of practical agent-workflow engineering. In particular, it treats review as an isolated, adversarial check rather than another prompt inside the implementation conversation. It provides:

- a frozen and validated change bundle;
- an isolated reviewer with structured findings;
- mandatory TruffleHog secret scanning before model invocation;
- read-only execution that cannot modify the reviewed repository;
- scope controls that resist speculative rewrites;
- bounded handling of large diffs;
- Codex review by default, with optional Claude or Pi reviewers;
- explicit rules for verifying findings instead of blindly applying them.

The installed dependency is kept unchanged and pinned to a reviewed upstream commit. `review-to-pr` does not reimplement or weaken its isolation, scanning, validation, or review contract.

## The important mental model

A skill is a reusable set of workflow instructions. Calling `$review-to-pr` does not replace the current task agent with a reviewer. Instead, the current agent becomes the coordinator and launches a separate, headless reviewer process at the review stage.

Even when both use Sol with high reasoning, they operate from different positions:

| Current task agent | Isolated review agent |
| --- | --- |
| Knows the complete implementation conversation | Does not receive the conversation |
| Knows why implementation decisions were made | Sees the frozen change bundle |
| Can inspect and modify the real repository | Runs read-only in an empty temporary workspace |
| May be influenced by its previous decisions | Starts without the implementation narrative |
| Verifies findings, edits code, tests, and publishes | Produces structured advisory findings only |
| Can commit, push, and create the draft PR | Cannot modify code, push, or create a PR |

This is contextual independence, not model diversity. The fresh reviewer can challenge assumptions without inheriting the implementer's reasoning. Because both agents may use the same model, correlated blind spots remain possible; a second model can be requested explicitly for unusually risky work.

## What happens behind the scenes

When the implementation is committed on a named topic branch and you invoke `$review-to-pr`:

1. **The current agent establishes the landing lane.** It inspects the branch, status, remotes, commits, repository guidance, existing PR, and intended base. It freezes the original scope and preserves unrelated local work.
2. **It selects objective proof.** It runs formatting when needed and chooses focused tests for the changed behavior.
3. **It constructs the review target.** The complete committed branch diff is compared with the actual PR base, an explicitly supplied base, or the remote default branch.
4. **`autoreview` validates the input.** It snapshots the relevant changes, omits security-sensitive paths according to its contract, and runs TruffleHog before invoking a model. Unsafe input fails closed.
5. **A separate Codex process starts.** By default this is `gpt-5.6-sol` with high reasoning. It runs in an empty, read-only workspace, ignores the implementation conversation, project instructions, skills, rules, and ordinary user configuration, and receives only the validated review bundle. Web search remains available for checking upstream dependency contracts.
6. **The reviewer returns structured findings.** `review-to-pr` asks for findings through P1. The reviewer performs a general code review covering correctness, regressions, normal flows, contracts, error handling, data loss, crashes, integration risks, and concrete security issues.
7. **The current agent verifies every finding.** It checks the real code path, adjacent files, tests, and dependency behavior. Each finding is accepted in scope, rejected with evidence, deferred as a follow-up, or escalated because it would change the task contract.
8. **Accepted fixes are proven again.** The current agent applies only small in-scope repairs, reruns affected tests, and launches a fresh complete review. Review and CI repairs share a two-cycle convergence limit.
9. **The current agent prepares the handoff.** It commits review fixes intentionally, pushes normally, opens or reuses one draft PR, observes required CI, and reports the result. It does not merge.

The isolated reviewer never fixes its own findings. Separation of roles is deliberate: the reviewer reports; the context-rich task agent verifies and acts.

## Review scope

The review is general, not security-only. It looks for material problems involving:

- correctness and logic;
- regressions and broken normal flows;
- API, storage, and data-contract violations;
- error handling and failure behavior;
- crashes and data loss;
- integration and dependency assumptions;
- concrete security vulnerabilities or removed safety checks.

Security is always included, and secret scanning is a separate mandatory prerequisite. The review intentionally avoids style preferences, unrealistic edge cases, speculative risks, and broad refactoring proposals.

Source review and tests still do not prove every user-visible behavior. Important UI, CLI, API, or generated-artifact changes may also need behavioral validation in the running product.

## What review-to-pr adds to autoreview

`autoreview` is the review engine and can be used independently for local changes, individual commits, branches, reviewer panels, and custom review configurations. Its default threshold is P0, and it does not push merely because a review was requested.

`review-to-pr` adds only the opinionated branch-to-PR orchestration:

| Concern | `autoreview` | `review-to-pr` |
| --- | --- | --- |
| Primary responsibility | Produce isolated structured review findings | Take a completed topic branch to a reviewed draft PR |
| Default target | Local changes, commit, or branch as selected | Complete committed topic-branch diff against its resolved base |
| Default severity | P0 blockers | P0 and P1 findings |
| Default reviewers | One Codex reviewer; panels optional | Exactly one Codex reviewer unless explicitly expanded |
| Finding handling | Requires the caller to verify and decide | Requires verification, classification, and only in-scope repairs |
| Tests | Can run supplied parallel tests | Selects focused proof and reruns it after repairs |
| Repair loop | Provides scope and convergence rules | Orchestrates the loop and stops after two non-converging cycles |
| Git publication | Does not push unless separately requested | Commits review fixes and normally pushes the topic branch |
| Pull request | No complete PR handoff policy | Opens or reuses one draft PR with findings and proof |
| CI | Outside the core review primitive | Observes required CI and handles only branch-caused failures in scope |
| Merge | Not implied by review | Explicitly forbidden during the invocation |

In short: use `autoreview` when you want a review. Use `review-to-pr` when implementation is finished and you want review, repair, proof, publication, and a human merge handoff as one bounded operation.

## Recommended workflow

1. Implement the change on a named topic branch.
2. Run implementation-time tests and commit the intended change.
3. Stay in the same Codex task so the coordinator retains the original intent and repository context.
4. Invoke `$review-to-pr` explicitly.
5. Let it review, verify findings, repair in scope, test, push, create the draft PR, and inspect required CI.
6. Read the final decision package: scope, proof, accepted and rejected findings, deferred work, CI state, residual risk, and PR link.
7. Perform any additional human review or testing you consider material.
8. Give a separate, explicit merge instruction only when satisfied.

A new Codex task is not required for independent review. The reviewer is already isolated by the `autoreview` helper; remaining in the implementation task gives the coordinator better context for deciding whether findings are real and in scope.

## What invocation authorizes

Calling `$review-to-pr` without additional instructions authorizes the current agent to:

- apply verified, in-scope review fixes;
- run relevant formatting and tests;
- create intentional review-fix commits;
- push the current named topic branch without force;
- open or update one draft PR;
- inspect required CI and repair branch-caused failures within scope.

It does not authorize:

- merging;
- force-pushing, rebasing, or rewriting history;
- discarding or absorbing unrelated work;
- broad refactors or unrelated fixes;
- replacing or patching the pinned `autoreview` dependency;
- starting a multi-reviewer panel unless explicitly requested.

The skill requires explicit invocation, so ordinary implementation prompts do not accidentally publish a branch.

## Prompt examples

### Standard closeout

```text
$review-to-pr
```

This runs the complete default workflow and creates or updates a draft PR. It does not merge.

### Specify the base

```text
$review-to-pr Review against origin/release-2.4. Fix only verified in-scope
findings, run the relevant tests, and open a draft PR. Do not rebase or merge.
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
in-scope findings, rerun proof, push normally, update the draft PR, and report
required CI. Do not create a duplicate PR or merge.
```

### Use blockers-only review

```text
$review-to-pr Take this small branch to a draft PR using P0-only autoreview.
Run the focused test, report consciously rejected findings, and do not merge.
```

### Request model diversity for exceptional risk

```text
$review-to-pr This branch changes an authentication boundary. Run the normal
P1 Codex review plus one explicitly requested second-model review. Verify every
finding and stop for my decision if the reviewers disagree. Do not merge.
```

### Report reviewer token usage

```text
$review-to-pr Run autoreview with --stream-engine-output and include input,
cached-input, output, and reasoning token usage in the final report.
```

## Prerequisites

- A named Git topic branch containing the committed implementation.
- A resolvable remote base branch.
- Git and authenticated GitHub access for pushing and draft-PR creation.
- Codex CLI authentication for the default reviewer.
- TruffleHog for mandatory pre-review secret scanning.
- The pinned sibling `autoreview` installation recorded in [`references/autoreview-dependency.md`](references/autoreview-dependency.md).

If review isolation, authentication, secret scanning, push, PR creation, or CI access fails, the workflow reports the exact blocker instead of silently weakening its guarantees.

## Dependency maintenance

`review-to-pr/SKILL.md` owns the landing policy. The upstream OpenClaw `autoreview` dependency owns review isolation, secret scanning, bundle construction, engine invocation, and structured validation.

Do not modify the installed upstream copy locally. To update it:

1. Select and inspect a specific upstream commit.
2. Replace the complete installed `autoreview` directory from that commit.
3. Update the commit and SHA-256 values in [`references/autoreview-dependency.md`](references/autoreview-dependency.md).
4. Run the upstream smoke tests and the skill validator.
5. Keep the dependency pinned rather than following a moving `main` branch.
