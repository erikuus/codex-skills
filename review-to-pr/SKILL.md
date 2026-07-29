---
name: review-to-pr
description: Take a finished Git topic branch through one isolated autoreview, verified in-scope repairs, focused tests, intentional commits, push, draft pull-request creation, and required-CI handoff without merging. Use when the user explicitly invokes review-to-pr after implementation is committed and wants the branch reviewed and published as a concise, human-reviewable PR instead of entering a multi-reviewer polling loop.
---

# Review to PR

Turn a finished topic branch into a reviewed draft PR. Use one isolated reviewer by default, treat tests and required CI as proof, and reserve the merge decision for the human.

Explicit invocation authorizes in-scope edits, commits, a normal push, and draft-PR creation unless the user narrows the request. It never authorizes merge, force-push, history rewriting, destructive cleanup, or unrelated fixes.

## Load the review dependency

1. Locate the installed `autoreview` skill and read its complete `SKILL.md` before acting.
2. Use its bundled helper directly. Do not reimplement, edit, or bypass its isolation, secret scanning, structured output, scope governor, or engine selection.
3. Read [references/autoreview-dependency.md](references/autoreview-dependency.md) only when checking provenance, diagnosing a missing or changed dependency, or updating the pin.
4. Stop if the helper is unavailable, its required secret scanner is unavailable, or the review bundle fails closed. Report the exact prerequisite instead of replacing it with an ordinary in-repository reviewer.

## Establish the landing lane

1. Read applicable repository guidance and inspect the current branch, status, remotes, commits, and diff summary.
2. Require a named topic branch. If `HEAD` is detached or the current branch is the intended base, stop and ask for the landing branch rather than inventing one.
3. Preserve unrelated local changes. Never stash, reset, discard, or absorb them. Stop if they prevent a trustworthy branch review.
4. Resolve the base in this order: the base of an existing PR, an explicit user-provided base, then the remote default branch. Do not assume `main` when repository evidence says otherwise.
5. Refresh the remote base before review when network access is available. Never rebase or merge the base into the topic branch unless the user separately requests it.
6. Freeze the scope baseline required by `autoreview`: original request or issue, intended behavior, owner boundary, changed files, and non-test LOC.

## Prove and review the branch

1. Run formatting first when it can change reviewed line locations.
2. Select focused tests from repository guidance and the changed behavior. Run them before or in parallel with review when safe. Do not invent a passing proof when no relevant test exists.
3. Review the complete committed topic-branch diff against the resolved base with branch mode. Do not use local mode merely because the working tree is clean.
4. Request `--max-priority P1` unless the user explicitly selects another threshold. Use one Codex reviewer; never start a panel or wait for external AI reviewers unless the user explicitly asks.
5. Verify every reported finding against the real code path, adjacent files, tests, and dependency contracts. Classify it as:
   - accepted and in scope;
   - rejected, with a concrete reason;
   - valid follow-up outside this PR; or
   - stop-and-escalate because it changes the task contract or owner boundary.
6. Apply only accepted in-scope fixes. Prefer the smallest fix at the correct ownership boundary.
7. After code changes, rerun affected tests and the complete branch review. Follow `autoreview`'s scope-growth and two-cycle convergence limits. Do not keep editing to satisfy speculative findings.
8. Finish this stage only when the latest helper run is clean, or when every remaining finding is consciously rejected or deferred with evidence allowed by the `autoreview` contract.

## Prepare one publishable branch

1. Review the cumulative diff and status. Confirm no unrelated files entered the landing lane.
2. If review created changes, commit them intentionally. Use one coherent review-fix commit unless separate commits materially improve traceability. Never create an empty commit.
3. Re-run any proof invalidated by the commit-time state or formatting.
4. Push the named topic branch normally, setting its upstream when needed. Never force-push.
5. Reuse an existing PR for the same head and base. Otherwise open one draft PR. Never create a duplicate PR.
6. Build the PR body around decisions and proof rather than a file-by-file narration:
   - intended behavior and scope;
   - implementation summary;
   - tests and behavioral proof;
   - autoreview command, threshold, and final result;
   - accepted, rejected, and deferred findings;
   - residual risks or follow-ups.

## Check objective remote proof

1. Observe required CI for the pushed head commit. Do not request, coordinate, or relentlessly poll multiple AI reviewers.
2. If required CI fails because of the branch, diagnose the failure, make the smallest in-scope fix, rerun focused local proof and autoreview, commit, push, and check CI again.
3. Count CI-triggered code repair together with review repair for the two-cycle convergence limit. Stop when repeated repair no longer converges.
4. Treat infrastructure failures, unavailable credentials, protected-branch rules, required human reviews, and unrelated flaky checks as blockers to report, not reasons to change product code.
5. Do not wait for optional bots once required CI has reached a stable result. Report any still-running optional checks without entering a Shepherd-style polling loop.

## Hand off to the human

Return a compact decision package containing:

- PR link, branch, base, and pushed head SHA;
- behavior and scope summary;
- tests and behavioral proof;
- final autoreview command and clean/rejected result;
- accepted, rejected, and deferred findings;
- required-CI and mergeability status;
- blockers and residual risks;
- an explicit statement that the PR was not merged.

Never merge during the same invocation, even if the initial request says to ship or merge. A later, explicit, unambiguous human instruction may authorize a separate merge action after this handoff.
