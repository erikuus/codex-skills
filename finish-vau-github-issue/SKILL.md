---
name: finish-vau-github-issue
description: Finish a VAU development or bug-fix thread by finding the originating issue in erikuus/Issues through the connected GitHub app, using authenticated vautest to verify behavior and capture screenshots, normalizing its VAU project status with gh, and posting a concise, complete Estonian user-facing explanation. Use as the final step after implementing a VAU change requested through GitHub Issues, or when the user asks to report, document, demonstrate, or explain completed VAU work to the requester.
---

# Finish a VAU GitHub issue

Use a connector-first hybrid workflow to turn the completed work in the current thread into a verified, user-facing GitHub issue comment:

- use the connected GitHub app for issue search, reading, and structured verification;
- use `gh api graphql` only for GitHub Projects v2 membership and status fields;
- use the user's authenticated Chrome session for `vautest`, screenshots, native GitHub image upload, and rendered-preview checks.

Do not use the GitHub web UI for semantic issue work when the GitHub app or `gh` covers the operation.

## Prepare the required tools and sessions

1. Read and follow the GitHub plugin's `github` skill before GitHub work.
2. Confirm that the connected GitHub app can access `erikuus/Issues`. If it is unavailable or unauthenticated, pause and ask the user to connect GitHub. Do not replace it with GitHub web-page search.
3. Before browser work, read and follow the Chrome plugin's `control-chrome` skill. Follow its confirmation and tab-finalization rules.
4. Use an authenticated Chrome tab matching `https://www.ra.ee/vautest/index.php/et` or an application page below that path. Confirm that VAU shows an authenticated administrator interface.
5. If the VAU session is absent or unauthenticated, ask the user to open or sign in to `vautest` and tell you when it is ready. If several matching VAU tabs are open and there is no uniquely relevant one, ask which visible tab to use.

Do not require or inspect a GitHub browser tab at the start. Use GitHub in the browser only later if native screenshot attachment or rendered-preview work requires it.

## Reconstruct the change from the development thread

Treat the current thread and repository as the source of truth. Before browsing:

- identify the original problem and requested outcome;
- inspect the final diff, tests, routes, and relevant model/view behavior when needed;
- note user corrections and UI decisions made during the thread;
- distinguish implemented behavior from ideas that were discussed but rejected;
- identify the user-visible routes that were changed or tested.

Do not infer behavior only from the issue description. Confirm it against the final code and the behavior visible in `vautest`. Treat `vautest` as the verification and screenshot surface, not as evidence of which environment the change was deployed to.

## Find the originating issue

1. Search open and closed issues in `erikuus/Issues` through the connected GitHub app, using distinctive terms from the problem, feature, module, or Estonian ticket text found in the thread.
2. Fetch the strongest candidate through the GitHub app and compare its title, full description, and relevant comments with the implemented change.
3. Record its issue number and direct URL for later browser attachment work.
4. Continue only when one issue clearly matches. If several issues remain plausible, show their numbers and titles and ask the user to choose. Never comment on a merely similar issue.

Do not search for or inspect candidate issues through the GitHub web UI unless the user explicitly asks for UI inspection.

Do not change the issue state, labels, assignees, milestone, or relationships except for the required VAU project membership and project status below, unless the user explicitly requests another change.

## Normalize the VAU project status

Use authenticated `gh api graphql` for this section because the GitHub app does not expose GitHub Projects v2 fields.

1. Confirm `gh` authentication and access to the repository owner's projects.
2. Query the project, field, option, issue, and existing project-item IDs. Resolve them from GitHub; do not hardcode IDs from an earlier run.
3. If the issue is not in the **VAU** project, add it to that project.
4. Inspect its **Status** field in the VAU project. If the value is anything other than **Ülevaatamisel**, change it to **Ülevaatamisel**.
5. Query the project item again and verify both the VAU project membership and the **Ülevaatamisel** status.

Do not close or reopen the issue as part of this normalization.

If `gh` is unavailable, unauthenticated, lacks the required project scope, or cannot resolve the project unambiguously, stop and report the exact blocker. Do not silently fall back to editing project fields through the GitHub web UI.

## Identify and verify routes in vautest

Derive test routes from evidence already produced during development, in this order:

1. routes explicitly supplied by the user;
2. routes visited or tested earlier in the thread;
3. controller/view routes visible in the final diff or repository;
4. stable links visible in the active VAU test session.

Use the `https://www.ra.ee/vautest/index.php/et` base for verification and screenshots, including when the completed change has already been uploaded to production. Do not guess route variants.

Verify the actual user-visible behavior before writing. If the feature is missing or broken in `vautest`, stop and report that it could not be verified there. Do not infer from this that it is missing from production, and do not post a completion explanation.

## Capture visual evidence

Capture one to three screenshots that demonstrate the main workflow. Prefer an overview and the most useful detail state. Use a short video only when motion or a multi-step interaction cannot be explained with screenshots.

- Use existing test data. Do not create, edit, or submit VAU data merely to stage a screenshot unless the user explicitly authorizes it.
- Crop screenshots to the interface area relevant to the issue.
- Preserve personal information visible in that relevant area. Do not blur, cover, anonymize, replace, or crop out names, email addresses, birth dates, addresses, phone numbers, request text, or other personal information unless the user's prompt explicitly instructs you to hide or redact it.
- Verify that every screenshot matches the explanation and does not include unrelated interface content.

Keep the screenshot files locally until the full comment is ready. Give each one a short Estonian caption and descriptive alt text. Upload them later through GitHub's native comment UI; do not commit screenshot files to a repository merely to obtain image URLs.

## Write the issue comment in clear Estonian

Always write the comment in simple, correct Estonian for a VAU administrator or other UI user. Use short sentences and concrete instructions. Avoid implementation details such as SQL, migrations, indexes, model methods, code structure, commits, or test internals.

Always begin with exactly one introduction sentence in this form:

> Ma olen AI-agent, kes kasutab arvutit, mille omanik on Erik Uus.

Treat **Erik Uus** as a variable. Replace it with the full name of the user currently signed in to Codex. Use the name available from the current Codex session or thread context. If the name cannot be established reliably, ask the user before drafting the comment; do not guess. Do not add the previous multi-sentence disclosure or another generic introduction.

Then explain only verified user-facing behavior that is relevant to this issue. Include every applicable detail needed to understand and use the feature, but omit inapplicable items:

1. what changed and where it appears;
2. what each marker, message, count, field, or state means;
3. the exact conditions that cause it to appear or not appear;
4. how the user should open and use the new information;
5. important ordering, overlap, or edge-case behavior discovered during development;
6. what the feature does not decide or automate;
7. screenshots with short captions.

Describe the change without claiming that it was implemented, released, or deployed in a test environment. The use of `vautest` for verification and screenshots must not determine the deployment wording. If the thread reliably establishes a production deployment and that fact is useful to the requester, describe it accurately; otherwise keep the explanation environment-neutral. Do not label screenshot captions as evidence of a test-environment implementation.

When describing matching or counting rules, explicitly explain overlaps and why an older or baseline record may have no marker when that is relevant. Never claim fuzzy matching, automatic duplicate rejection, or another behavior that was not verified.

Assume readers skim. Lead with the outcome, use short headings and compact lists, and remove repetition. Stay strictly within the issue's scope: omit generic product information, general advice, unaffected behavior, speculative edge cases, and developer-facing history. Completeness means covering every relevant detail of this feature, not expanding into surrounding topics.

## Review and publish

1. Prepare the complete Markdown comment outside the GitHub web UI.
2. Only after the issue is identified and the comment is ready, use or navigate an authenticated Chrome tab directly to the recorded issue URL. Do not browse the issue list or repeat issue discovery in the UI.
3. Place the prepared comment in the comment editor and upload the screenshots as native GitHub attachments without submitting it.
4. Check GitHub's rendered preview. Confirm the opening disclosure, Estonian wording, list formatting, image placement, captions, and alt text.
5. Ask for action-time confirmation immediately before clicking **Comment**, because the post is representational communication from the user's GitHub account.
6. After confirmation, submit only with **Comment**. Do not use **Close with comment** unless closing was explicitly requested.
7. Verify the published comment's author and text through the GitHub app, and verify every rendered image in the browser.
8. Leave the published issue open as a deliverable and report its direct comment URL.

If the user explicitly requests no screenshots, skip the GitHub browser steps and, after action-time confirmation, publish the prepared Markdown through the GitHub app. Verify the resulting comment through the app.

If upload or submission fails, keep the draft intact, state exactly what remains, and ask only for the specific user action needed to continue.
