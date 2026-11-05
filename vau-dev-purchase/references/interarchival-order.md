# Interarchival order

Status: **Demonstrated — eligible item selection, non-employee researcher submission, staff routing, service bill, card payment, VAU/ERPLY checks and final dashboard verification.** The VAU order type is “Kauglaenutus”. Read [shared.md](shared.md) first; use Computer Use with current labels and the correct order row. Physical transport/return was not demonstrated.


Apply the current request's [payment method and scenario](shared.md#payment-methods-and-scenarios). The payment choices and results below are the recorded successful-card baseline, not fixed replay instructions. Substitute the requested supported method/API case/test data. Paid/receipt/completion checks apply only to expected success; for failure, cancellation or pending cases use the shared outcome checks instead of proceeding through success-only steps.

## Required inputs and starting state

Start at `index.php/et` in the authorized employee test session, which can inspect items and enter a researcher context. For the paid customer path, use a non-employee researcher context: the user explained that an employee's own order is payment-exempt. Do not confuse the same displayed name across employee/researcher records with identical billing behavior.

| Variable | Demonstrated value / behavior |
| --- | --- |
| `SOURCE_STORAGE_FILTER` | `noora*` in an unlabeled item-table filter; exact filter-column label was not captured. Verify resulting storage/location columns. |
| `ARCHIVE_REFERENCE` | Selected `eaa.1.1.3`; entered as `EAA.1.1.3` in “Leidandmed *”. Example storage: Noora:A205.A1.1.1; current room/repository Noora:A205. |
| Item eligibility | **“Asukoht” = “Hoidlas” and item is not digitized.** This is a user-required prerequisite, not merely an example preference. |
| `CUSTOMER_NAME`, `RESEARCHER_ACCOUNT` | The intended non-employee test researcher; namesake entries existed. Use the permitted “Sisene kliendina” action for the correct record, not a fixed row position. |
| `DESTINATION_ROOM` | Required “Sihtruum”: “Tallinna uurimissaal” was already selected after choosing the order type; no destination change was demonstrated. |
| `PURPOSE` | Required “Kasutuseesmärk”: “Teadustöö”. |
| Notes / keywords | “Tellija märkused” left empty; “Märksõnad” showed “Puudub”. |
| Payment / email | Required payment choice: “Maksan krediitkaardi või pangalingiga (Swedbank, SEB, Luminor, LHV)”; confirm current account email without retaining its example value. |
| `VAU_ORDER_ID` | Generated 1068811; use through staff queues. |
| Bill service / quantity / total | “Arhiivisäiliku kauglaenutamine”, unit “tk”, quantity 1, €3.00. Already populated on bill creation; no quantity/price edit was demonstrated. Verify current charges. |
| `BILL_REFERENCE`, `BILL_ID` | Generated KTA2026-00005 / example detail ID 45831. |
| `ERPLY_ORDER_NUMBER` | Generated 100683 from “Tellimus nr …” and bill “ERPLY nr”; distinct from `VAU_ORDER_ID`. |

## Select an eligible reference before ordering

1. Home → staff **“Säilik”** / **“Säilikud”** (`index.php/et/item/admin?scope=all`).
2. Filter **“Asukoht” to “Hoidlas”**. The demonstration also entered `noora*` in a table filter and pressed Enter; use the current storage-filter control and confirm the intended Noora results. The AX capture did not name that text field, so do not hardcode a guessed field selector.
3. In the chosen row, check “Leidandmed”, “Hoidla info”, “Asukoht”, “Hetke ruum” and “Hoidla”. The selected example was in Noora and **“Hoidlas”**.
4. Check the row's digitization indicator before copying the reference. The selected row lacked **“Ava digitud säilik”**, while the neighbouring EAA.1.1.1 row had that action. This visible contrast is the demonstrated non-digitized check; no AIS/DGS detail page was opened. Treat this as VAU's displayed indication, not proof of the absence of every possible digital copy outside VAU.
5. Copy the eligible row's reference as `ARCHIVE_REFERENCE`. The user selected lowercase `eaa.1.1.3` and changed the prefix to uppercase in the order form. Do not reuse this example without rechecking its current availability/digitization.

## Researcher: create and submit

1. Use the [shared role-switching steps](shared.md#researcher-and-employee-contexts) to enter the correct non-employee researcher context. The demonstrated entry opened **“Minu tellimused” → “Koostamisel”**, initially with no drafts.
2. In **“KOOSTA TELLIMUS”** (`index.php/et/order/index?scope=clientDraft`), enter `ARCHIVE_REFERENCE` in **“Leidandmed *”**. “Tellimuse liik” was disabled/blank before entering a valid reference.
3. Set **“Tellimuse liik” to “Kauglaenutus”**. Verify required **“Sihtruum” = `DESTINATION_ROOM`**, choose `PURPOSE`, and choose **“Lisa”**.
4. Find the new draft and choose its **“Kinnita”** (`index.php/et/order/confirmInterArchivalLoanOrder?id=VAU_ORDER_ID`). Verify reference, “Kauglaenutus”, destination, item title and purpose. Capture `VAU_ORDER_ID` from the heading.
5. Choose the checkout option for the requested `PAYMENT_METHOD` (card/bank-link in the demonstration), then **“Kinnita”**. Follow [shared email confirmation](shared.md#researcher-email-confirmation). Confirm **“Tellimus on esitatud!”**, removal from drafts and appearance under “Esitatud”. Cash and invoice payment were visible alternatives but not demonstrated.

## Staff: route and bill the order

Perform these staff mutations only within the user's current authorized test. Switch back to the employee context using the shared role-switching steps; remain on `VAU_ORDER_ID` and `ARCHIVE_REFERENCE` in every queue.

1. **“Klienditeenindaja” → “KL otsuse ootel”** (`index.php/et/orderManage/index?scope=clientManagerIALRequested`). Verify order ID, reference, “Kauglaenutus” and destination. Row actions → **“Edasta hoidlasse”**.
2. The confirmation prompt was **“Oled kindel, et soovid teha selle toimingu?”**, with “OK” / “Cancel”. The successful result showed **“Toiming sooritatud!”** and the row left this queue. The actual dialog-accept input was not captured.
3. **“Fondihoidja” → “Hoidlast tellitud”** (`scope=repositoryManagerRequestFromRepository`). Find the same row and verify its repository information and destination. Row actions → **“Märgi väljastatuks KL-sse”**. The same confirmation prompt and successful queue removal were observed; its accept input was not captured.
4. **“Klienditeenindaja” → “KL-sse saatmise ootel”** (`scope=clientManagerIALToBeDelivered`). Same row → **“Koosta teenuste arvestus”** (`index.php/et/invoice/create`). “Saada kauglaenutusse” was available but was not chosen in this recording.
5. Check payer, selected payment method, `VAU_ORDER_ID`, reference and “Arhiivisäiliku kauglaenutamine”; verify quantity/total. Leave “Märkused” blank as in the demonstration and choose **“Salvesta”**.
6. On **“Teenuste arvestus nr …”** (`index.php/et/invoice/view?id=BILL_ID`), capture `BILL_REFERENCE`; initially **“Tasutud: Ei”**. Choose **“Esita arvestus”**. Subsequent researcher payment establishes that the bill became payable; a separate submission toast was not captured.

## Researcher: pay

1. Re-enter the same researcher account through the shared client entry point and choose **“Esitatud”**. Find the relevant order and choose **“Maksa”**.
2. At `index.php/et/invoice/pay`, capture `ERPLY_ORDER_NUMBER` from **“Tellimus nr …”**. Verify reference, service, quantity and **“Tasuda”** (€3.00 here).
3. Select the requested `PAYMENT_METHOD` and [execute its requested scenario](shared.md#payment-methods-and-scenarios); the recorded card branch is only an example. The user chose **“Maksa 3,00 €”** and completed the demo 3-D Secure step.
4. The return at `index.php/et/invoice/paid` showed **“Tellimus nr 100683”**, the selected archival reference and **“Menetluses”**. This is an order-processing state; verify actual payment receipt below.

## Verify VAU and ERPLY

1. Return to employee context. Follow [shared VAU payment-list checks](shared.md#vau-payment-list): “Arvestus” → “Veebimaksed”. The demonstrated `BILL_REFERENCE` row showed **€3.00 / Krediitkaart / Valideeritud** at 05.11.2026 17:17.
2. Open that “Maksedokument”. Match the bill reference, archival reference, service, quantity and total. Confirm **“Tasutud: Jah”**, **“ERPLY nr” = `ERPLY_ORDER_NUMBER`**, **“ERPLY laekumine: Jah”** and its receipt time. The user highlighted **100683**, **Jah**, and **05.11.2026 17:17**. ERPLY creation time was 17:15; payment/receipt 17:17.
3. ERPLY applies. Use the shared **“Otsi” → correct customer → “Tellimused”** route. Multiple matching names were opened in the recording; one namesake showed an unrelated old order. Identify the correct customer by the expected order; do not assume the first same-name entry is correct.
4. Match the list **“Number” = `ERPLY_ORDER_NUMBER`** and **“Summa” = bill total**. The loaded list was checked read-only after recording and showed **100683 / €3.00**, with “Kinnit.” = “jah” and “Staatus” = “kinnit.”. These last columns are document confirmation; the VAU bill above supplies explicit payment-receipt evidence. Opening an ERPLY document is unnecessary for the demonstrated check.

Also perform [shared Laekumised verification](shared.md#erply-receipt-checks-for-all-workflows) for this same customer and generated ERPLY order, matching receipt date, method, total/currency and linked order. This additional check was demonstrated in the Rights-certification recording and explicitly requested by the user for all workflows.

## Final order-dashboard check

After VAU/ERPLY payment verification, return to the employee order dashboard and validate the same order, rather than stopping at the bill.

1. From the paid bill page, choose staff **“Tellimus”** (`index.php/et/order/redirect`). In **“Klienditeenindaja”**, choose **“KL-sse saatmise ootel”** (`index.php/et/orderManage/index?scope=clientManagerIALToBeDelivered`). Ignore the variable queue count.
2. Find `VAU_ORDER_ID` and `ARCHIVE_REFERENCE` with the expected destination/customer, then click the order row to expand its details. Demonstrated: **1068811 / EAA.1.1.3 / Tallinna uurimissaal**.
3. Confirm **“Olek” = “Kauglaenutusse saatmise ootel”**, **“Asukoht” = “H<>KL”**, and **“Teenuste arvestus (makstud)”** followed by the same `BILL_REFERENCE` (KTA2026-00005 here). The user highlighted the paid bill text. This ties the verified payment back to the order dashboard.
4. Compare the current state with the earlier **“KL otsuse ootel”** processing stage and capture **“Olek muudetud”**. In this demonstration it was **05.11.2026 17:15**; payment/receipt was at 17:17. The order had already reached the awaiting-dispatch queue before payment. The paid-bill label is the payment-related result; do not assert that payment itself changed the order state or that “Kauglaenutusse saadetud” has been reached.

These are read-only checks. Do not choose a state-changing action to make the displayed result match. If the order, bill or state differs, report the observed values and the mismatch.

## Evidence and coverage limits

Recording `5162EE57-5BD8-4FFA-8B1F-CC3AA4F27CE4`, 2026-11-05 17:13:03–17:19:33 Europe/Tallinn. Events 851–894 item eligibility/reference; 895–933 researcher entry/submission/employee return; 934–952 staff routing/bill; 953–967/1092–1094 researcher payment; 1096–1138 VAU accounting checks; 1139–1153 ERPLY lookup. The fully loaded ERPLY list row was observed read-only afterward. Cancelled attempts were not used.

Dashboard follow-up recording `6631EA42-ECF2-42BC-8937-2189B8E6A12A`, 2026-11-05 17:26:20–17:26:58 Europe/Tallinn: events 1168–1170 return to staff orders, select the awaiting-dispatch queue and expand the same row; selection 1230 highlights its paid bill; event 1241 retains the expanded details.

Shown paid path and final dashboard check are documented. Remaining coverage limits: exact unlabeled storage-filter field, two dialog-accept inputs, minimum permissions, employee-exempt order behavior, other repositories/destinations/payment branches, physical dispatch/arrival/return and local compatibility. No physical transfer or completion of the loan is established by billing/payment alone.
