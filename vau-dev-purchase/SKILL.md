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

Treat the invocation as the test brief. Read [request-driven payment testing](references/shared.md#payment-methods-and-scenarios) and adapt the relevant workflow to the requested provider/method, API variant, outcome, data and scope. The recordings are successful card-payment examples: “Mastercard Visa”, particular test-card data and “Yes” are **not fixed requirements**. Current user instructions select the scenario; preserve the workflow's domain prerequisites and traceable identifiers.

For example, “Use this skill to test Swedbank Pay with every supported payment API variant, including success and failure” calls for discovering the supported cases and testing their expected outcomes. It does not call for repeating the recorded card/Yes branch. Do not run all five workflows unless the request calls for that scope. Where scope can reasonably be inferred, state the assumption and proceed; ask only when a missing choice materially affects the test.

Recorded evidence limits do not prohibit testing a new branch. Inspect the current UI, relevant implementation/configuration and authoritative provider test documentation to establish it; never invent controls, test credentials, API variants or status mappings. Label new observations separately from the original demonstrations.

## Recording and refinement

Use Record & Replay for one complete workflow per recording. The user operates the browser; do not perform orders, enquiries, payments or ERPLY changes during recording. Start only when the user is ready, then yield until they finish. Stop and inspect the captured events. Keep only relevant VAU, payment and ERPLY actions; exclude unrelated tabs and copy/paste detours. Never copy passwords, tokens, cookies, payment credentials or secret-bearing URLs into this skill.

After each recording, update this same skill, extract common steps into shared.md and identify material gaps before the next workflow. Distinguish recorded actions, later read-only observations and user explanations. Convert example values into inputs; do not invent unseen steps or branches. Incomplete guides do not authorize guessed replay.

## Execution and validation

Follow the user's current authorization for submissions and payments; this skill does not supply authorization. For every tested workflow, apply the [shared ERPLY Laekumised check](references/shared.md#erply-receipt-checks-for-all-workflows) according to the scenario: confirm settlement for success, and check for incorrect settlement on non-success outcomes. Hand payment credentials/authentication to the user. If a submission result is uncertain, inspect its status before retrying to avoid duplicate records. ERPLY verification is read-only.

Validate revisions with skill-creator's `scripts/quick_validate.py`. After all five demonstrations, validate the complete skill and review each guide's inputs, actions, success criteria and ERPLY applicability. Structural validation does not prove replay or compatibility with another environment.
