---
name: vau-dev-purchase
description: Run and adapt VAU development/staging purchase and enquiry workflows to the user’s requested payment method, integration/API variant and test outcomes, with VAU/ERPLY verification. Covers copy, interarchival and shop orders plus personal-interest and rights-certification enquiries; excludes general VAU administration.
---

# VAU development purchases and enquiries

Use Computer Use with stable page, label and control targets. Read [shared.md](references/shared.md) first, then the requested guide. Resolve relative VAU routes against its single `VAU_BASE_URL` setting. Includes the demonstrated order/enquiry lifecycle: staff routing, response preparation, billing/payment notices and VAU/ERPLY verification. Keep general VAU administration in its separate skill.

| Workflow | Guide | Status |
| --- | --- | --- |
| Copy order | [copy-order.md](references/copy-order.md) | Demonstrated: digital copy + staff test preparation + bill/payment + VAU/ERPLY checks |
| Interarchival order | [interarchival-order.md](references/interarchival-order.md) | Demonstrated: eligible item + paid researcher path + staff routing/bill + VAU/ERPLY + final dashboard checks |
| Shop order | [shop-order.md](references/shop-order.md) | Demonstrated: pickup + card payment + VAU/manager checks; ERPLY list rule clarified by user |
| Personal-interest enquiry | [personal-interest-enquiry.md](references/personal-interest-enquiry.md) | Demonstrated: submission + staff response + bill/notice/payment + completion/VAU/ERPLY checks |
| Rights-certification enquiry | [rights-certification-enquiry.md](references/rights-certification-enquiry.md) | Demonstrated: rights-purpose submission + state-fee notice/payment + Makstud/VAU/ERPLY checks |

## Adapt to the invocation

Use the five workflow guides as the EveryPay baseline. For a Swedbank Pay run, also read [the Swedbank Pay guide](references/swedbank-pay.md) for checkout, callbacks, and the separate staging evidence.

Treat the invocation as the test brief. Read [request-driven payment testing](references/shared.md#payment-methods-and-scenarios) and adapt the relevant workflow to the requested provider/method, API variant, outcome, data and scope. The recordings are successful card-payment examples: “Mastercard Visa”, particular test-card data and “Yes” are **not fixed requirements**. Current user instructions select the scenario; preserve the workflow's domain prerequisites and traceable identifiers.

For example, “Use this skill to test Swedbank Pay with every supported payment API variant, including success and failure” calls for discovering the supported cases and testing their expected outcomes. It does not call for repeating the recorded card/Yes branch. Do not run all five workflows unless the request calls for that scope. Where scope can reasonably be inferred, state the assumption and proceed; ask only when a missing choice materially affects the test.

Recorded evidence limits do not prohibit testing a new branch. Inspect the current UI, relevant implementation/configuration and authoritative provider test documentation to establish it; never invent controls, test credentials, API variants or status mappings. Label new observations separately from the original demonstrations.

## Recording and refinement

Use Record & Replay for one complete workflow per recording. The user operates the browser; do not perform orders, enquiries, payments or ERPLY changes during recording. Start only when the user is ready, then yield until they finish. Stop and inspect the captured events. Keep only relevant VAU, payment and ERPLY actions; exclude unrelated tabs and copy/paste detours. Never copy passwords, tokens, cookies, payment credentials or secret-bearing URLs into this skill.

After each recording, update this same skill, extract common steps into shared.md and identify material gaps before the next workflow. Distinguish recorded actions, later read-only observations and user explanations. Convert example values into inputs; do not invent unseen steps or branches. Incomplete guides do not authorize guessed replay.

## Recover interrupted browser control

- When an unattended run crosses between VAU, a payment provider or a bank simulator, keep the test window on the active, unlocked desktop. Before a submission, record the workflow, VAU order/application/bill ID, available payment reference and the action about to be taken. Keep checkout URLs with session tokens out of the checkpoint.
- If a snapshot times out or a redirect leaves the URL uncertain, treat the last click as possibly applied. Refresh the browser inventory and reacquire the actual tab or window using its current title, host and visible case details. Check the same attempt in VAU, the provider UI and, when available, the payment trace and ERPLY. A stale tab handle or a missing immediate log entry is insufficient evidence to resubmit. Resume once the case state is known.
- Use native Computer Use for known, authorized VAU confirmation dialogs or an observed file picker when browser control cannot reach them. If the dialog is absent from the main window snapshot, inspect the returned window inventory for the modal. Read the prompt, act once and refresh the state to verify the result.
- If a hosted Swedbank Pay form remains blank while Chrome debugging is attached, detach using Chrome’s visible debugging banner and reobserve the same checkout with native controls. This recovered the embedded form in November 2026. Use the existing payment/authentication handoff if needed. A provider error that also occurs without debugging needs its own payment evidence.
- Refresh the binding after a stale handle or lost connection. If the runtime explicitly ends Computer Use for the turn, stop app input and resume from the checkpoint on the next authorized turn. Use a browser or app restart for a persistent lost connection, then reacquire the original case before taking any action.

## Execution and validation

Follow the user's current authorization for submissions and payments; this skill does not supply authorization. For every tested workflow, apply the [shared ERPLY Laekumised check](references/shared.md#erply-receipt-checks-for-all-workflows) according to the scenario: confirm settlement for success, and check for incorrect settlement on non-success outcomes. Hand payment credentials/authentication to the user. If a submission result is uncertain, inspect its status before retrying to avoid duplicate records. ERPLY verification is read-only.

Validate revisions with skill-creator's `scripts/quick_validate.py`. After all five demonstrations, validate the complete skill and review each guide's inputs, actions, success criteria and ERPLY applicability. Structural validation does not prove replay or compatibility with another environment.
