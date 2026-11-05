# Shop order

Status: **Demonstrated — pickup in Tartu, card payment, post-ERPLY VAU checks and webshop-manager verification.** ERPLY list verification is based on the user's explicit clarification. Read [shared.md](shared.md) for URLs, sessions and environment differences. Use Computer Use; find controls by label and product context rather than recorded coordinates.


Apply the current request's [payment method and scenario](shared.md#payment-methods-and-scenarios). The payment choices and results below are the recorded successful-card baseline, not fixed replay instructions. Substitute the requested supported method/API case/test data. Paid/receipt/completion checks apply only to expected success; for failure, cancellation or pending cases use the shared outcome checks instead of proceeding through success-only steps.

## Inputs and starting state

Start signed in at `index.php/et`. The demonstrated shop cart initially showed “Ostukorv ( 0 )”. Check existing cart contents before adding: the main menu's “Veebipood4” badge was present even with an empty cart and is not the cart count.

| Input | Demonstrated example / field behavior |
| --- | --- |
| `CATEGORY`, `PRODUCT` | “Monograafiad” → “Riigivanem Juhan Kukk” (Riigivanemad; Küllo Arjakas). Example catalog ID 374; resolve the requested product in the current environment. |
| `QUANTITY` | 1. Adding once produced quantity 1; changing quantity was not demonstrated. |
| `FIRST_NAME`, `LAST_NAME` | Account-derived; required “Eesnimi” and “Perekonnanimi” fields were disabled. |
| `EMAIL`, `PHONE` | Required “E-post” and “Telefon”; prefilled and editable. Use current user-provided values, not demonstration contact data. |
| `DELIVERY_METHOD`, `PICKUP_LOCATION` | “Tulen ise järele” → required “Aadress” → “Tartu, Nooruse 3”. |
| `PAYMENT_METHOD` | “Maksan krediitkaardi või pangalingiga” → “Mastercard Visa”. |
| `ORDER_NUMBER` | Generated result, example 100681; capture anew for ERPLY and final VAU verification. |
| `PAYMENT_DOCUMENT` | Generated accounting reference, example VPA2026-00004; capture from “Veebimaksed”. Do not derive it from `ORDER_NUMBER`. |
| Total | Example €30.00; verify the live product/cart/checkout/payment amount rather than fixing this price. |

Delivery/payment were initially unselected and terms unchecked in the preliminary checkout observation. These are observed states, not guaranteed defaults. Other visible choices were “Pakiautomaadiga”, “Postipakiga aadressil” and “Maksan arve alusel”; their branches were not demonstrated. No additional rationale for the selected branch was given.

## VAU actions

1. From the home page, choose “Veebipood” (`MainMenu_Shop`); confirm the shop page at `index.php/et/shop/home/index`.
2. Choose “Monograafiad” in the demonstration (`index.php/et/shop/product/index?menuId=20`). For reuse, use `CATEGORY` and locate `PRODUCT` in its product card.
3. Choose that card's “Lisa ostukorvi”. Confirm “Lisati ostukorvi”, the correct product and “Toote kogus ostukorvis: 1”.
4. Choose “Vaata ostukorvi”. At `index.php/et/shop/cart/index`, check product, quantity, unit price and “Maksumus kokku”.
5. Choose “Vormista tellimus” (`index.php/et/shop/order/create`). Check the same line/total and required contact fields.
6. Choose “Tulen ise järele”; select `PICKUP_LOCATION` in “Aadress”. Both “Tallinn, Madara 24” and “Tartu, Nooruse 3” were visible; Tartu was the final selection, not a fixed default.
7. Choose the checkout option for `PAYMENT_METHOD` (the demonstration used “Maksan krediitkaardi või pangalingiga”), accept “Nõustun … müügitingimustega” under the user's authorization, then choose “Saada”.
8. On “Makse sooritamine”, capture `ORDER_NUMBER` from “Tellimus nr …”. Confirm the payment-method selector (“Palun vali makseviis ja jätka” in the demonstration), then select the requested `PAYMENT_METHOD`; “Mastercard Visa” was the recorded example. Bank links were visible but not used.

## Payment and success

1. Follow [request-driven payment handling](shared.md#payment-methods-and-scenarios) for the requested method/outcome; use the shared card example only when applicable. The example amount was €30.00; the user completed the provider payment and demo 3-D Secure step.
2. Confirm the return to VAU and **“Makse kinnitatud. Aitäh!”**, with the same order number, product/quantity/total, selected payment method and pickup location. Order 100681 / one book / €30.00 / Tartu was confirmed read-only after the first recording and in the recorded follow-up. Reaching the provider alone is not payment success.

## ERPLY actions and matching

Applicability: **Applies.** In ERPLY, open the correct customer and choose **“Tellimused”**. Use `ORDER_NUMBER` from VAU and the expected total to identify the corresponding order. The user confirmed that list verification is sufficient; opening the document and checking product-title fields are not required.

Then perform [shared Laekumised verification](shared.md#erply-receipt-checks-for-all-workflows), as requested for every workflow. Match receipt amount/date/method and order association. If the current list omits the order number or the receipt link shows only “Tellimus”, report the identity limitation rather than claiming a match from €30 alone. The explicit VAU receipt checks below remain part of the demonstrated verification.

## VAU checks after ERPLY

These are read-only purchase checks within this skill, not a general administration workflow. They require access to the accounting pages; minimum role was not established.

1. Return to the VAU tab. Confirm “Makse kinnitatud. Aitäh!” and `ORDER_NUMBER` on the payment result.
2. Choose “Arvestus” (`index.php/et/accounting/admin`, “Raamatupidamise üldotsing”), then “Veebimaksed” (`index.php/et/payment/admin`, title “Maksed”). The older accounting shell may label its navigation “Arvestused, arved ja maksed”.
3. Locate the payment row and check “Summa”, “Makseviis”, “Olek”, “Aeg” and “Maksja”. Demonstration: VPA2026-00004, €30.00, “Krediitkaart”, **“Valideeritud”**, 05.11.2026 16:15, the ordering customer. Capture `PAYMENT_DOCUMENT`; a recent date alone is not sufficient to identify the payment. The next step provides the exact order link. Filter controls were visible but their use was not demonstrated.
4. Open the row's “Maksedokument” link. On “Vaata tellimust” (`index.php/et/shop/order/view?id=2261` in the example), confirm “Arvestus nr” matches `PAYMENT_DOCUMENT`, the ordered product/quantity, selected payment/pickup and total. Use the clicked link; the detail ID is environment-specific.
5. Verify the three values the user highlighted: **“ERPLY nr” equals `ORDER_NUMBER`**, **“ERPLY laekumine” is “Jah”**, and **“Maksumus kokku” matches the paid total**. Example: 100681 / Jah / €30.00. “Veebimakse aeg” and “ERPLY laekumise aeg” both showed 05.11.2026 16:15; “ERPLY tellimuse loomisaeg” showed 05.11.2026 16:13. The displayed order “Olek” was “Saabunud”; do not confuse order state with payment validation or receipt.

Do not choose “Muuda olekut” or alter records. Do not copy transaction tooltips or payment-provider payloads; they can contain credentials/session links and personal data. Report mismatched numbers, totals or absent receipt as a failed/incomplete verification.

## Webshop manager: verify the paid order

Use an existing session with webshop-manager access. This is a read-only check of the purchase; role assignment and minimum permissions were not demonstrated.

1. Home → **“Veebipood”** (`index.php/et/shop/home/index`). Open the shop management-menu button (displayed **“”** in the recording), then choose **“Halda tellimusi”** (`index.php/et/shop/order/admin`).
2. Identify the row by **“Arvestus nr” = `PAYMENT_DOCUMENT`** and **“ERPLY nr” = `ORDER_NUMBER`**, checking “Tellija” and “Koostatud”. Example: **VPA2026-00004 / 100681 / 05.11.2026 16:13**. Filters including “Arvestus nr” and “ERPLY nr” were visible but not used in the demonstration; do not invent a filter-submission sequence.
3. Confirm **“laekunud”** appears beneath the ERPLY number. The separate **“Olek”** column was **“Saabunud”**; a paid order is not thereby fulfilled or collected.
4. Open the row's **“Koostatud”** date/time link to “Vaata tellimust” (example `index.php/et/shop/order/view?id=2261`). Confirm the same accounting/order identifiers, product/quantity/total and pickup details using the [VAU checks above](#vau-checks-after-erply), including **“ERPLY laekumine: Jah”**. Example: one “Riigivanem Juhan Kukk”, €30.00, Tartu pickup, receipt 05.11.2026 16:15. Do not choose “Muuda olekut”; this follow-up only verifies the existing state.

## Evidence and coverage limits

Recording ID and time are in shared.md. Event IDs: 4–9 home/shop/category/cart/checkout; 10–17 pickup/payment/terms/submission; 18 VAU number/payment choice; 65/88/110/145 EveryPay form; 151 payment submission; 152 3-D Secure; 164–166 customer → “Tellimused”. The later document-opening detour is omitted from the reusable procedure at the user's request. Unrelated tabs and copy/paste detours are excluded.

Follow-up recording `139E07EB-5345-451E-B186-D06112F632CA`: events 193–196 capture confirmation → “Arvestus” → “Veebimaksed” → accounting document; selections 208/214/229 highlight ERPLY number, receipt “Jah” and total.

Manager follow-up `2E2EC901-81D6-40B4-8B55-4E4E74B1027A`, 2026-11-05 17:30:02–17:30:34 Europe/Tallinn: events 1247–1249 show shop → management menu → “Halda tellimusi”, including the matched row’s “laekunud” indicator and “Saabunud” state; event 1250 opens its detail and confirms receipt.

Shown purchase and manager-verification path is documented. Not demonstrated: logged-out login/minimum role, quantity changes, other delivery/payment branches, failure/retry handling and local-environment compatibility. The captured Shop receipt link did not expose its order number; the shared receipt check records that limitation. The intended ERPLY verification remains list-only.
