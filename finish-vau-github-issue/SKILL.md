---
name: finish-vau-github-issue
description: Finish a VAU development or bug-fix thread by finding the originating issue in erikuus/Issues, verifying the completed behavior in the authenticated VAU test environment, capturing safe screenshots, and posting a clear Estonian user-facing explanation to the issue. Use as the final step after implementing a VAU change requested through GitHub Issues, or when the user asks to report, document, demonstrate, or explain completed VAU work to the requester.
---

# Finish a VAU GitHub issue

Use the user's existing Chrome sessions to turn the completed work in the current thread into a verified, user-facing GitHub issue comment.

## Use the required browser sessions

1. Read and follow the Chrome plugin's `control-chrome` skill before browser work. Follow its confirmation and tab-finalization rules.
2. List open Chrome tabs. Claim existing authenticated tabs matching:
   - `https://github.com/erikuus/Issues/issues` or an issue below that path;
   - `https://www.ra.ee/vautest/index.php/et` or an application page below that path.
3. Confirm that GitHub permits issue commenting and VAU shows an authenticated administrator interface.
4. If either active session is absent or unauthenticated, pause. Ask the user to open or sign in to both sites and tell you when they are ready. Do not open a replacement login session or switch to another browser.
5. If several matching VAU tabs are open and there is no uniquely relevant one, ask which visible tab to use.

## Reconstruct the change from the development thread

Treat the current thread and repository as the source of truth. Before browsing:

- identify the original problem and requested outcome;
- inspect the final diff, tests, routes, and relevant model/view behavior when needed;
- note user corrections and UI decisions made during the thread;
- distinguish implemented behavior from ideas that were discussed but rejected;
- identify the user-visible routes that were changed or tested.

Do not infer behavior only from the issue description. Confirm it against the final code and the test environment.

## Find the originating issue

1. Start from the active `erikuus/Issues` tab.
2. Search open and closed issues using distinctive terms from the problem, feature, module, or Estonian ticket text found in the thread.
3. Open the strongest candidate and compare its title and full description with the implemented change.
4. Continue only when one issue clearly matches. If several issues remain plausible, show their numbers and titles and ask the user to choose. Never comment on a merely similar issue.

Do not change the issue state, labels, assignees, milestone, or relationships unless the user explicitly requests it.

## Identify and verify the test routes

Derive test routes from evidence already produced during development, in this order:

1. routes explicitly supplied by the user;
2. routes visited or tested earlier in the thread;
3. controller/view routes visible in the final diff or repository;
4. stable links visible in the active VAU test session.

Use the `https://www.ra.ee/vautest/index.php/et` base. Do not guess route variants.

Verify the actual user-visible behavior before writing. If the feature is missing, broken, or not yet deployed in `vautest`, stop and report that fact. Do not post a completion explanation.

## Capture safe visual evidence

Capture one to three screenshots that demonstrate the main workflow. Prefer an overview and the most useful detail state. Use a short video only when motion or a multi-step interaction cannot be explained with screenshots.

- Use existing test data. Do not create, edit, or submit VAU data merely to stage a screenshot unless the user explicitly authorizes it.
- Prefer clearly synthetic records.
- Crop screenshots to the relevant interface.
- Avoid exposing real names, email addresses, birth dates, addresses, phone numbers, request text, or other personal data.
- Verify that every screenshot matches the explanation and does not show unrelated sensitive content.

Upload the visuals to the GitHub comment and give each one a short Estonian caption and descriptive alt text.

## Write the issue comment in clear Estonian

Always write the comment in simple, correct Estonian for a VAU administrator or other UI user. Use short sentences and concrete instructions. Avoid implementation details such as SQL, migrations, indexes, model methods, code structure, commits, or test internals.

Always begin with these sentences, substituting the Codex user's name only when the thread establishes a different owner:

> Ma ei ole inimene, vaid AI-agent. Kasutan selleks Codexi kasutaja arvutit tema palvel. Codexi kasutaja on Erik Uus.

Then explain only verified user-facing behavior:

1. what changed and where it appears;
2. what each marker, message, count, field, or state means;
3. the exact conditions that cause it to appear or not appear;
4. how the user should open and use the new information;
5. important ordering, overlap, or edge-case behavior discovered during development;
6. what the feature does not decide or automate;
7. screenshots with short captions.

When describing matching or counting rules, explicitly explain overlaps and why an older or baseline record may have no marker when that is relevant. Never claim fuzzy matching, automatic duplicate rejection, or another behavior that was not verified.

Prefer headings and short lists. Keep the explanation thorough enough to answer likely user questions, but remove developer-facing history.

## Review and publish

1. Prepare the full comment and upload the visuals without submitting it.
2. Check GitHub's rendered preview. Confirm the opening disclosure, Estonian wording, list formatting, image placement, and alt text.
3. Ask for action-time confirmation immediately before clicking **Comment**, because the post is representational communication from the user's GitHub account.
4. After confirmation, submit only with **Comment**. Do not use **Close with comment** unless closing was explicitly requested.
5. Verify the new comment in the issue activity, including the author, text, and every image.
6. Leave the published issue open as a deliverable and report its direct comment URL.

If upload or submission fails, keep the draft intact, state exactly what remains, and ask only for the specific user action needed to continue.
