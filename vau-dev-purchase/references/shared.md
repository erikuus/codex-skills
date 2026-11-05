# Shared configuration and steps

## Environment configuration

```yaml
VAU_BASE_URL: https://www.ra.ee/vautest/
VAU_ENVIRONMENT: staging-user-confirmed
ERPLY_BASE_URL: https://t10.erply.com/2076
```

The user confirmed staging on 2026-11-05; it is also the originally requested target. Keep the active VAU base URL only here. Workflow guides use relative routes. The canonical skill directory is `/Users/erikuus/.agents/skills/vau-dev-purchase`.

## Login and sessions

Start with the user's existing VAU and ERPLY sessions. A VAU account menu and ERPLY “Rahvusarhiiv” / “VAU teenused” indicators were observed. VAU also displayed administrative controls; their presence does not establish that purchases require an administrator. Copy processing explicitly used “Klienditeenindaja” and “Koopiakeskuse töötaja” views in the existing session. Login, minimum account permissions and session recovery were not demonstrated. If sign-in is needed, let the user establish the session outside credential capture; do not invent a login sequence or assume the two services share authentication.

## Researcher and employee contexts

For the Interarchival paid test, the user explained that an employee's own order is exempt from payment. The successful recording used a separate researcher context for customer submission/payment, then the employee context for staff processing. Keep account/role choice explicit; do not assume two records with the same name have the same billing rules.

Demonstrated entry: staff “Uurija” / “Uurijad” (`index.php/et/client/admin`), search the customer-name column and press Enter, choose the correct record's **“Sisene kliendina”** icon (`client/loginAsClient`), and confirm the researcher “Minu tellimused” page/account menu. To return, open the researcher account button (example initials “EU”) and choose **“Sisene [employee name] rollis”** (`client/loginAsClientManager`). These are role switches in an existing authorized test session, not a recorded login or a grant to impersonate arbitrary users. Re-enter the same intended customer for payment.

## Researcher email confirmation

Copy and Interarchival confirmation showed an email review dialog after “Kinnita”: verify the displayed account address, then **“Kinnitan, et see e-posti aadress on kasutusel”**. The page warns that an invalid/unavailable mailbox can prevent billing/payment messages. Do not hardcode the address; the visible “Muuda konto e-posti” branch was not demonstrated. Submission success was **“Tellimus on esitatud!”**.

Both enquiry branches showed the same address-confirmation button after “Edasi”, with “Makseteade / vastus saadetakse siia”; their submission success was **“Päring on esitatud”**. Email editing was not demonstrated in any of these flows.

## Environment differences

| Environment | Evidence / remaining checks |
| --- | --- |
| Current staging | All five paid branches recorded. Personal-interest ends “Lõpetatud” with a response-link send log; Rights-certification ends “Makstud” before subsequent response/certification work. |
| Payment integration in this demonstration | EveryPay host `igw-demo.every-pay.com`; 3-D Secure host `3ds-mpi-everypay.staging.modirum.com`. These are observed demonstration endpoints, not hardcoded replay destinations. |
| VAU accounting pages | “Arvestus” / “Veebimaksed” and shop-order detail used an older administration shell with “TEST” visible. Access was demonstrated in the existing session; minimum permissions and local parity are unverified. |
| Copy preparation / FTP | Copy demonstration used existing digital copies, staff role views and the test checkbox “Loo FTP kaust käsitsi (märgi see, kui testimisel pole vaja kausta reaalselt luua)” to skip real folder creation. Do not generalize this to actual delivery. Establish local FTP behavior and the intended test mode separately. |
| Interarchival prerequisites | Requires an item displayed as “Hoidlas” and not digitized. Example source was Noora, destination Tallinn. Employee payment exemption was explained by the user; paid demonstration used researcher context. Recheck item availability, digitization, account billing and role-switch support in another environment. |
| Personal-interest enquiry | Demonstration used “Muu” / “Isiklik huvi”, response PDF upload, selected processor/registration, quantity 2 at €30 and a generated payment notice. A special-permission warning allowed file changes after “Valmis”; ordinary permissions and real mailbox/download behavior are unverified. Recheck processor/test-file availability, notification templates/recipients, pricing, response-access links and payment/completion callbacks locally. |
| Rights-certification enquiry | “Muu” rights purpose creates a state-fee notice (observed €25) before response work, not the Personal-interest service bill. Recheck notice templates, fee configuration, callback/status behavior and later certification requirements locally. No completed certificate was demonstrated. |
| Future local development | URL, sessions/roles, available products, routes/labels, payment callbacks and ERPLY integration are unverified. |

Changing the base URL alone does not establish compatibility. Record differences here when observed. On another environment, establish its payment mode and ERPLY destination before a mutating test; do not assume a staging name means sandbox behavior. Follow freshly generated payment links; never reuse captured payment/session URLs.

## ERPLY verification

Open the configured ERPLY session and the relevant customer, then “Tellimused”. Opening an existing customer link and choosing “Tellimused” were demonstrated. Copy and Interarchival orders demonstrated the sidebar “Otsi”: enter `CUSTOMER_NAME`, choose the matching customer, then “Tellimused”. Multiple similar customer entries may appear; identify the intended customer rather than choosing a fixed result position. The user explicitly clarified that for the demonstrated “Erik Uus” search, the **second of the two “Uus, Erik” entries** is correct; its observed customer ID is 2866. Preserve this test-data distinction and verify the expected ERPLY order, since row order and IDs are environment-dependent.

For Shop order, the user clarified that ERPLY list verification is sufficient without opening the document. Use the number from VAU “Tellimus nr …” to identify the order and the shared “Laekumised” step to inspect receipt. Do not require product-title or document-detail checks. If a list/link lacks an identifying number, retain the documented identity limitation rather than claiming payment-to-order linkage from amount alone.

If the number cannot be matched or the list does not establish payment, report the gap; do not infer success from a nearby date or create/edit an ERPLY record. Copy and Interarchival orders use the service bill’s “ERPLY nr” to match the customer-orders “Number” and bill total to “Summa”; see their guides. Both enquiry branches expose “ERPLY nr” and “ERPLY laekunud: Jah”: match the Personal-interest service bill or Rights-certification state-fee notice respectively. ERPLY applies to all five demonstrated paid branches.

For Shop order, follow ERPLY verification with the [VAU payment/accounting checks](shop-order.md#vau-checks-after-erply). The demonstrated document explicitly exposes “ERPLY nr” and “ERPLY laekumine”; retain those exact links and outcomes rather than inferring correspondence from amount alone. Copy order demonstrates the same payment-list entry point but opens a service bill at `index.php/et/invoice/view`; its exact receipt checks are in [copy-order.md](copy-order.md#verify-vau-and-erply). Interarchival uses the same service-bill checks; see [interarchival-order.md](interarchival-order.md#verify-vau-and-erply). Personal-interest enquiry opens the application itself from “Maksedokument”; see [personal-interest-enquiry.md](personal-interest-enquiry.md#pay-and-verify-completion). Rights-certification also returns to the application, with state-fee notice/paid-state fields; see [rights-certification-enquiry.md](rights-certification-enquiry.md#pay-and-verify-the-recorded-endpoint).

## Enquiry payment notices

Both enquiry branches used **“Saada makseteade”** from the current application. Review “Malli pealkiri”, “Saaja aadress”, “E-kirja teema” and required “E-kirja sõnum”; choose **“Edasi”**, review the rendered recipient/message/amount and generated links, then **“Saada”** only under the current authorization. No custom message editing was demonstrated. Use the application's current links, never saved access codes. Verify “Makse ootel” and the send/ERPLY-creation history before paying.

Personal-interest used **“Vastuskirja makseteade”** after response readiness and service billing. Rights-certification used **“Arhiiviteatise riigilõivu makseteade”** before response work. Do not interchange their timing, amounts, document references or terminal states.

## Payment methods and scenarios

The user clarified that **every recording used one particular online/card method, one test-data set and “Yes” to obtain a successful test payment**. These are demonstration choices. They do not fix the provider, card data, authentication response, payment API, outcome, amount or future execution sequence. Let the current request drive the test; use the guides as workflow/context references and successful baselines.

### Derive the test scope

Extract only the dimensions relevant to the request: `WORKFLOWS`, `PAYMENT_METHOD` / provider, `API_VARIANTS`, `EXPECTED_OUTCOMES`, `TEST_DATA_SOURCE`, environment and any limits or existing order/bill to reuse. These are invocation inputs, not new global URL settings. A named provider can offer several methods; establish which integration/method the request refers to instead of silently substituting the recorded EveryPay card route. Use ordinary successful checkout for an ordinary purchase request; do not impose success when the user requests failure or other payment tests.

For “every possible API variant”, inventory the cases actually supported by the requested integration and test environment. Inspect available provider test controls and relevant app/configuration, and consult current official provider test/API documentation where needed. Separate API versions/entry points from outcome simulations. Build a compact case matrix showing workflow/entry point, method, API variant, test-data set identifier, expected provider outcome and expected VAU/ERPLY effects. Cover documented supported success, rejection/failure, cancellation, pending/timeout or other cases **when they exist and are within scope**; do not invent a universal case list. Mark unsupported, unavailable or undocumented cases explicitly and report the coverage boundary. Do not promise “all variants” when the inventory is unknown.

If the request concerns the method across VAU, account for the distinct entry points in the selected workflows: Copy/Interarchival service bills, Shop order, Personal-interest enquiry bill and Rights-certification fee notice. Do not assume one successful endpoint proves all integrations. Equally, do not expand a single-workflow request into five workflows. A focused existing payable setup can be reused when its state permits an independent test; state reasonable scope assumptions and ask only for a materially ambiguous provider, scope or missing test capability.

### Execute the requested case

Use Computer Use for VAU setup and UI-dependent checks. When API-level tests are requested, use an available authorized test client/tool or repository implementation for those cases, retaining VAU/ERPLY verification; do not fake an API scenario by changing an ERPLY record or manually marking an order paid. The current brief may require a different VAU payment selector, provider page, test-data set or outcome control from those recorded. Discover and verify those targets in the current environment.

Choose the requested checkout/payment method and its documented test mechanism. **Do not automatically choose “Mastercard Visa”, reuse the demonstration card data or select “Yes”.** “Yes” was the successful demo outcome; for a different case use the provider's actual supported control/data/API response. If no supported way to induce the requested outcome is established, report that case as blocked/unavailable rather than forcing success. Credentials, authentication and any required user handoff remain governed by the current authorization and tools; do not store card data, codes, tokens or cookies in the skill or test report.

Keep case-specific application/order/bill/payment identifiers and capture the pre-test state. Use a fresh unpaid test entity when reusing a paid or failed attempt would contaminate the result; create only the test entities within the authorized scope. Follow generated payment links. Run one controlled attempt per case unless a retry is itself requested or justified by known state. For an uncertain/processing result, inspect status/callback evidence before retrying; use a bounded observation window appropriate to the documented asynchronous flow and report unresolved pending state. Do not keep resubmitting or automatically turn a failure/cancellation case into a successful payment. Do not switch environments, enable production payment modes or expand permissions merely to make a case run.

### Verify the expected outcome

The workflow guides' “Valideeritud”, “Jah”, “laekunud”, “Makstud”, “Lõpetatud” and paid-bill checks describe **recorded successful outcomes**. Apply them only to a scenario expected to settle successfully. For other outcomes, inspect the same linked provider/VAU/accounting/ERPLY records against the case's expected effects. Establish exact failure/pending labels and API-to-UI mappings from current evidence; they were not recorded. Preserve method-specific authentication/callback behavior rather than asserting the card flow for every provider.

| Scenario | Verification principle |
| --- | --- |
| Successful settlement | Verify provider result, matching VAU payment/receipt and the workflow-specific successful state; confirm the linked ERPLY receipt and amount. |
| Rejection, failure or cancellation | Verify the intended result actually occurred. For a fresh unpaid case, check that it did not incorrectly gain a settled payment, paid state, settled ERPLY receipt or success-only fulfilment/download-release event. Do not require a particular error label without evidence. |
| Pending, timeout or uncertain result | Record the observed provider/VAU state and any callbacks. Do not call it settled or permanently failed solely from a page timeout; check within the bounded observation window and report unresolved state if necessary. |

An ERPLY order may already exist before payment because submitting a bill/notice creates it. Its presence is not a failed negative test; compare **new settlement/receipt and state changes** to the baseline. An unsuccessful payment-attempt row may also be expected. Do not require all payment/order rows to disappear. If a case intentionally settles later or covers retry/reversal behavior, use its documented requested state sequence rather than these simple outcome summaries.

Report the case matrix with expected versus observed outcomes, non-secret record identifiers, the evidence for VAU/ERPLY effects, pass/fail/unresolved or blocked status, and uncovered variants. Distinguish a correctly simulated failure (test passed) from an unexpected failure (test failed). Keep new test observations separate from the recorded baseline; update reusable guidance only when supported by evidence or a user clarification.

## Card payment

**Recorded card example only; use it when it matches the requested case.** All five demonstrated paid branches chose “Mastercard Visa” on VAU's payment page and followed its freshly generated EveryPay link. Verify the amount and recipient “Rahvusarhiiv”. The provider fields are “Kaardi number”, “Kehtivuse lõpp”, “CVC”, “Nimi kaardil”; the user supplies credentials/authentication without storing them in the skill. The demonstrated user chose “Maksa [amount]”; processing showed “Teie makse töötlemine.” / “Palun ärge värskendage lehte.” Do not refresh/resubmit while processing.

For the demonstrated successful test, the demo 3-D Secure step included “Yes”, then “3-D Secure Processing” / “Please wait..”. This is evidence of that demo branch, not a reusable instruction to approve arbitrary authentication prompts. Verify the workflow-specific VAU result and accounting receipt after return; provider navigation alone is not payment success.

## VAU payment list

Choose “Arvestus” (`index.php/et/accounting/admin`, “Raamatupidamise üldotsing”) → “Veebimaksed” (`index.php/et/payment/admin`, title “Maksed”). In the older shell the accounting navigation may be “Arvestused, arved ja maksed”. Find the relevant payment row using its workflow-specific document reference plus amount, method, payer/time. For expected success, confirm “Olek” = “Valideeritud”; for other requested outcomes, apply the scenario checks above and verify the actual current label without forcing validation. Open “Maksedokument” for the workflow's bill/order and verify its exact identifier and receipt fields. No filter-entry sequence was demonstrated. Never copy provider-data tooltips or generated transaction/access links.

The Copy demonstration additionally exposed ERPLY list columns “Number”, “Kuupäev”, “Tähtaeg”, “Summa”, “Kinnit.” and “Staatus”. Do not label “Kinnit.” / “kinnit.” as payment receipt; report the matched row separately from VAU’s explicit “ERPLY laekumine: Jah”.

Shop also has a [webshop-manager paid-order check](shop-order.md#webshop-manager-verify-the-paid-order): the management list ties “Arvestus nr” to “ERPLY nr” and shows a separate “laekunud” receipt indicator alongside “Olek”. Keep payment receipt distinct from fulfilment state. The session already had management access; granting that access was not demonstrated.

## ERPLY receipt checks for all workflows

The user explicitly requested this extra check for **all five workflows** after demonstrating “Laekumised” in the Rights-certification recording. After the customer “Tellimused” match, choose the same customer's **“Laekumised”** tab. For expected success, match the settled receipt. For failure/cancellation/pending cases, compare against the pre-test baseline and check that no incorrect new settled receipt has appeared; an existing pre-payment order may remain. It is a read-only verification step; do not add or edit receipts.

Match **“Kuupäev”**, **“Liik”**, **“Summa”** and linked **“Arve”** to the workflow's payment date, method, total/currency and expected ERPLY order. The demonstrated card receipts read **“Krediitkaardiga”** and **“Tellimus [number]”**. Do not use “Kinnit.”, “kinnit.”, newest-row position or “makstud 14 päeva varem” as receipt identity.

The loaded receipt view was inspected read-only after the Rights recording. All rows below were dated 05.11.2026 and used “Krediitkaardiga”; these are successful-card evidence examples, not fixed method, data or outcome requirements:

| Workflow | Expected ERPLY order | Receipt amount | Visible linked Arve |
| --- | --- | --- | --- |
| Copy | 100682 | 20,00 EUR | Tellimus 100682 |
| Interarchival | 100683 | 3,00 EUR | Tellimus 100683 |
| Shop | 100681 | 30,00 EUR | “Tellimus”; the captured link label did not expose a number |
| Personal-interest | 100684 | 60,00 EUR | Tellimus 100684 |
| Rights-certification | 100685 | 25,00 EUR | Tellimus 100685 |

For reuse, substitute the generated order number and current total/date. The Shop row supports the customer's receipt amount/method/date, but its unnumbered link label alone does not prove the order link. Pair it with the explicit VAU order/receipt checks and report that ERPLY link-identity limitation if the current UI still does not expose enough information. Do not assert an exact receipt-to-order match from amount alone. No filter or receipt-detail navigation was demonstrated.

## Capture status

Shop order recording: `8BC0C129-A88E-4323-8C96-20D03E2C3423`, 2026-11-05 16:12:33–16:16:12 Europe/Tallinn. Primary evidence: the recorder's `events.jsonl`; VAU payment confirmation was checked read-only after stopping. Only sanitized instructions are stored here. Earlier snapshot checkpoints are superseded by this recording.

Shop follow-up recording: `139E07EB-5345-451E-B186-D06112F632CA`, 2026-11-05 16:24:12–16:24:55 Europe/Tallinn. Captured VAU payment confirmation and read-only accounting checks after ERPLY. This supplements the same Shop workflow.

Copy order recording: `D1DDDE3F-B3D6-4E9E-8611-B60CDAF30345`, 2026-11-05 16:33:08–16:38:31 Europe/Tallinn. Captured researcher submission, staff test preparation, service bill/payment and VAU checks; the loaded ERPLY list row was checked read-only afterward.

Interarchival order recording: `5162EE57-5BD8-4FFA-8B1F-CC3AA4F27CE4`, 2026-11-05 17:13:03–17:19:33 Europe/Tallinn. Captured item eligibility selection, researcher/employee switches, routing, billing, payment and VAU verification; the loaded ERPLY list row was checked read-only afterward. Cancelled attempts were excluded.

Interarchival dashboard follow-up: `6631EA42-ECF2-42BC-8937-2189B8E6A12A`, 2026-11-05 17:26:20–17:26:58 Europe/Tallinn. [Final dashboard verification](interarchival-order.md#final-order-dashboard-check) showed the same order awaiting dispatch with its service bill marked paid; the order-state timestamp preceded payment.

Shop manager follow-up: `2E2EC901-81D6-40B4-8B55-4E4E74B1027A`, 2026-11-05 17:30:02–17:30:34 Europe/Tallinn. Captured webshop-manager navigation, matching order/accounting references, the “laekunud” indicator and detail receipt.

Personal-interest enquiry recording: `932CFD53-8360-4923-91DE-215B10FDBBB1`, 2026-11-05 17:33:12–17:40:55 Europe/Tallinn. Captured submission, staff assignment/response, service bill/payment notice, card payment and completed-state/payment checks. Loaded enquiry and ERPLY row inspected read-only afterward. The user confirmed the second matching Erik Uus customer in ERPLY. For Personal-interest enquiry, the user also allowed the AI to generate a small PDF test response for upload; use fictional text and verify the PDF opens. This is an optional preparation step, not an observed recording action.

Rights-certification recording: `236E357F-8638-4A36-9404-4ECFB6B1C224`, 2026-11-05 17:54:56–18:00:16 Europe/Tallinn. Captured rights-purpose submission, state-fee notice/payment, paid-state and VAU/ERPLY checks. The loaded “Laekumised” view was inspected read-only afterward; the user requested that receipt check for every workflow.

All five requested guides now document their demonstrated paid paths. Coverage limits remain explicit in each guide; this does not establish local compatibility or successful autonomous replay. Do not require demonstration of every alternative branch to document the shown path.
