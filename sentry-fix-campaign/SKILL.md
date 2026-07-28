---
name: sentry-fix-campaign
description: Triage and remediate a set of related unresolved Sentry errors as one backward-compatible coding campaign on one Git branch with one eventual pull request. Use when Codex must inspect multiple errors for the current project, cluster duplicate or overlapping root causes, check whether earlier campaign commits already cover later issues, implement only missing fixes, add regression tests, and create intentional commits without separate implementation worktrees or branches per Sentry issue.
---

# Sentry Fix Campaign

Run one coordinated remediation campaign. Parallelize read-only diagnosis; serialize all code changes through one main agent, one branch, and one working tree.

## Establish the campaign

1. Read and follow the available `sentry:sentry` skill for authentication, read-only API access, redaction, and issue/event retrieval.
2. Derive the Sentry project slug from the current Codex project name. Assume they match exactly; do not ask for a separate Sentry project name. Use the configured `SENTRY_ORG` and `SENTRY_AUTH_TOKEN`. If the matching project cannot be read, stop instead of guessing another project.
3. Confirm the repository guidance, current branch, base branch, Git status, runtime versions, and relevant test commands before editing.
4. Preserve unrelated user changes. Never stash, reset, discard, or absorb them into the campaign.
5. Create or reuse one dedicated branch named `codex/sentry-fixes-YYYY-MM-DD`, unless the user specifies another branch. Keep every campaign commit on it. If the current checkout cannot safely host the branch, use one dedicated campaign worktree; do not create one worktree per issue.
6. Treat Sentry as read-only. Do not resolve, assign, ignore, or mutate Sentry issues unless the user separately requests it.

## Triage before writing

1. Retrieve the user-specified unresolved issue set. If no range or issue list is given, inspect unresolved production issues from the last 14 days, up to 50.
2. Inspect representative events and local stack paths without printing PII, raw stack traces, tokens, or hostile payloads unnecessarily.
3. Cluster issues by root cause, not by Sentry group. Consider endpoint, exception chain, stack, malformed parameter shape, and timing. Treat wrapper and underlying framework exceptions from one request as one cluster.
4. Order clusters by dependency: shared boundary or validation fixes first, endpoint-specific fixes later.
5. Maintain an in-context ledger with these columns:

   `Sentry issue | root-cause cluster | reproduction | status | test | covering commit`

6. When there are two or more independent clusters, delegate bounded read-only diagnosis to subagents. Give each subagent issue evidence and a cluster, and require exact code paths, backward-compatibility risks, and proposed tests. Subagents must not edit, commit, create branches, hand off, or mutate Sentry. The main agent consolidates their summaries.

## Enforce backward compatibility

Backward compatibility is a release gate, not a preference.

Before implementing a cluster:

- Identify the valid legacy requests, response shape, HTTP status, permissions, side effects, translations, and supported PHP/Yii/runtime versions affected by the path.
- Prefer validation at the earliest application trust boundary. Reject only malformed, invalidly encoded, unauthorized, or structurally impossible input.
- Preserve all valid scalar values and established user workflows.
- Preserve public method signatures, JSON/HTML response schemas, routes, database schema, configuration keys, and error behavior for valid requests unless the user explicitly authorizes a change.
- Use syntax and APIs supported by the repository's existing minimum runtime. Do not upgrade PHP, Yii, dependencies, or infrastructure as part of the fix.
- Reuse established repository validation and exception patterns.
- Do not hide the symptom only through Sentry filters, logging suppression, broad exception swallowing, rate limiting, or WAF rules. Those may be defense-in-depth but cannot replace the code-level prevention.

If valid historical behavior cannot be established or the safe fix would intentionally break it, stop and ask for the user's decision before editing.

## Implement through one writer

Process clusters sequentially on the campaign branch:

1. Re-read the latest branch state, relevant commits, and tests before each cluster. Earlier campaign commits may have changed the answer.
2. Reproduce or encode the malicious input in a focused regression test.
3. Check whether current `HEAD` already prevents the exception while preserving the positive legacy case.
4. If already covered, make no redundant change. Record the covering commit and tests for every affected Sentry issue.
5. Otherwise implement the smallest root-boundary fix.
6. Add or update tests that prove both:
   - the reported malformed input no longer reaches framework/database internals or produces a 500; and
   - representative valid legacy input retains its previous result and side effects.
7. Run focused negative and positive tests plus nearby regression tests.
8. Review the diff for accidental behavior, API, runtime, or dependency changes.
9. Commit one root cause at a time. Reference every covered Sentry short ID in the commit body. Do not create empty commits for issues already covered.
10. Update the ledger with the commit SHA and test evidence.

Never allow parallel agents to write to the campaign checkout. Never hand individual issue threads between Local and Worktree to integrate their changes.

## Verify and hand off

After all clusters:

1. Run the broadest relevant test suite available.
2. Compare the cumulative branch diff and commit log against the base branch.
3. Confirm the working tree contains no unintended or uncommitted changes.
4. Perform a final backward-compatibility review across valid inputs, routes, response schemas, permissions, runtime support, and side effects.
5. Present the completed ledger, including issues fixed transitively by earlier commits.
6. Prepare one pull-request summary organized by root cause, with issue-to-commit and issue-to-test mappings plus residual risks.
7. Push or open the pull request only when the user explicitly requested that external action. Otherwise stop with the branch ready.

## Completion criteria

Do not call the campaign complete until every issue is either:

- fixed and mapped to a tested commit;
- proven covered by an earlier tested campaign commit; or
- documented as intentionally deferred with a concrete blocker or user decision.

The final branch must remain backward-compatible for valid legacy behavior and contain no duplicate fixes for the same root cause.
