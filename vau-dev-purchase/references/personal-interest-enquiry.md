# Personal-interest enquiry

Status: **Demonstrated — “Muu” / “Isiklik huvi”, staff assignment and response upload, service bill, payment notice, card payment and completion/VAU/ERPLY checks.** Read [shared.md](shared.md) first. Use Computer Use with current labels and the same enquiry throughout. Notifications, registration and uploads are mutations and require the user's current authorization; recording them is not permission to send them again.


Apply the current request's [payment method and scenario](shared.md#payment-methods-and-scenarios). The payment choices and results below are the recorded successful-card baseline, not fixed replay instructions. Substitute the requested supported method/API case/test data. Paid/receipt/completion checks apply only to expected success; for failure, cancellation or pending cases use the shared outcome checks instead of proceeding through success-only steps.

## Inputs and starting state

Start signed in at `index.php/et`; the demonstration session also had staff enquiry permissions. No separate login or researcher role switch was shown for this enquiry.

| Variable | Demonstrated value / behavior |
| --- | --- |
| `ENQUIRY_FORM`, `PURPOSE` | “Muu” → **“Isiklik huvi”**. Do not use the separate rights-certification branch for this workflow. |
| Applicant identity / contact | “Eesnimi *”, “Perekonnanimi *”, “Sünnikuupäev *” were account-prefilled and disabled. Review current country/contact/address fields; not all were exposed in the capture. Store no example birth date, address, phone or email. |
| `DELIVERY_METHOD` | **“E-postiga”** in the resulting record; “Postiga” and “Tulen ise järele” were visible alternatives. No selection-click or initial radio default was clearly captured. |
| `ENQUIRY_TEXT` | Required “Missugust infot ja/või mille jaoks arhiivist otsite?”; a short test value was entered. Use user-provided test content, not personal historical details from another enquiry. |
| Fee acknowledgement | Required **“Olen teadlik, et vastuskirja teenustasu on 30 eurot”** was checked. €30 is the observed service unit price, not a guaranteed current price or final total. |
| `ARCHIVE_UNIT`, `PROCESSOR` | “Tartu” and a selected staff recipient in “Saaja”. Names/addresses are inputs; use the intended authorized test recipient, not a copied demo email. |
| `RESPONSE_FILE` | A PDF was uploaded as the answer; its private filename/path/content are omitted. Use a supplied test PDF, or create a small PDF with fictional test response text as the user explicitly allowed. Verify that the generated PDF opens before upload. |
| `SERVICE`, `SERVICE_QUANTITY` | “Uurimistöö ja isikliku teabevajaduse eesmärgil esitatud päringule vastamine [30 EUR]”. Quantity initially **1**, deliberately changed to **2**, producing **€60.00**. No rationale for quantity 2 was stated; it is an example variable, not the normal required quantity. |
| `APPLICATION_ID`, `REGISTRATION_NUMBER` | Generated example 116079 / ARP2026-00002. |
| `BILL_REFERENCE`, `ERPLY_ORDER_NUMBER` | Generated APA2026-00001 / 100684. Keep these distinct from application/registration numbers. |

## Applicant: submit the enquiry

1. Home → **“Arhiivipäringud”** (`index.php/et/enquiry/form/index`) → **“Muu”** (`index.php/et/enquiry/application/create`). This form is for a request outside the named thematic forms; do not substitute a different form without the user's intent.
2. Review the account-prefilled applicant/contact fields. Choose/check **“Kasutuseesmärk: Isiklik huvi”** and **“Kättesaamise viis ja koht: E-postiga”**, enter `ENQUIRY_TEXT`, and check the fee acknowledgement. The form explained that a personal-interest payment notice follows completion of the work; treat quoted price/timing as the observed UI, not a verified legal or service guarantee.
3. Choose **“Edasi”**. Review the email dialog (“Makseteade / vastus saadetakse siia”), then **“Kinnitan, et see e-posti aadress on kasutusel”**. Email editing was not demonstrated.
4. On **“Esita päring”** (`index.php/et/enquiry/application/preview`), review the request and choose **“Esita päring”**. Confirm **“Päring on esitatud”**. Applicant attachments on this preview were not demonstrated.

## Staff: assign, register and prepare the response

1. Staff **“Päring”** / **“Arhiivipäringud”** → **“Halda päringuid”** (`index.php/et/enquiry/application/admin`). Open the new matching applicant/form/time row. Capture `APPLICATION_ID` from the record route (`index.php/et/enquiry/application/view?id=APPLICATION_ID`). “Uus” in recorded row clicks was the applicant's surname, not a state or action to hardcode.
2. The detail page displayed warnings about earlier enquiries with matching identity/contact data. Distinguish this new test enquiry by its ID and creation time; do not open or process an older namesake request.
3. In **“Vali arhiiviüksus”**, select `ARCHIVE_UNIT` and choose **“Määra”**. Confirm **“Päring määratud!”**. On the admin list, set **“Päringu olek” = “Määratud”**, choose **“Otsi”**, and reopen the same enquiry.
4. Choose **“Edasta”** (`enquiry/application/forward?id=APPLICATION_ID`). Required fields were **“Saaja”**, **“Saatja”**, **“Teema”**; **“Sõnum”** was also visible. Select `PROCESSOR` using **“Vali”**, review the prefilled sender/subject and the **“Määra päringule registreerimisnumber”** option, then **“Saada”**. The registration option's initial checkbox state was not captured; the prompt **“Kas oled kindel, et soovid selle päringu registreerida?”** and the resulting history establish registration. Its dialog-accept input was not captured. Confirm **“Päring edastatud!”**.
5. Filter the list to **“Töösse võetud” → “Otsi”** and open the same record. Capture `REGISTRATION_NUMBER` and check archive unit/processor. In **“Päringu menetlemise ajalugu”**, open **“Vaata”** for **“Edasta ja määra registreerimisnumber”** and follow its freshly generated response-management link to **“Koosta vastus”** (`index.php/et/enquiry/file/admin`). Do not save/reuse its access code.
6. Prepare `RESPONSE_FILE`: use the supplied test PDF or generate a small valid PDF with fictional test response text and verify that it opens. AI generation is a user-authorized option; it was not an action in the recording. Use **“Klõpsa siin, et valida üks fail, või lohista siia oma arvutist mitu faili korraga”** / file chooser to upload `RESPONSE_FILE`. Confirm the uploaded row under “Failinimi”, “Maht”, “Töötaja”, “Aeg”. Choose **“Märgi vastus valminuks”**; the prompt was **“Kas oled kindel, et vastus on valmis?”**. Its accept input was not captured, but **“Vastus on märgitud valminuks!”** and state **“Valmis”** were observed.
7. The session displayed a special-permission warning that files could still be edited although the enquiry was already “Valmis”. Do not assume ordinary staff have that override or modify the completed response as part of verification.

## Bill and send the payment notice

1. Return to staff enquiries, filter **“Päringu olek: Valmis” → “Otsi”**, and reopen the same application. Choose **“Lisa teenuste arvestus”** (`index.php/et/enquiry/invoice/create?applicationId=APPLICATION_ID`).
2. Verify required **“Teenus”** and **“Kogus”**. Use `SERVICE_QUANTITY`; in the demonstration **1 → 2** at €30 produced €60. Choose **“Salvesta”**; confirm **“Teenuste arvestus lisatud.”** and capture `BILL_REFERENCE`.
3. Choose **“Saada makseteade”** (`index.php/et/enquiry/application/notify`, through the generated action). Review **“Malli pealkiri”**, **“Saaja aadress”**, **“E-kirja teema”** (example **“Vastuskirja makseteade”**) and required **“E-kirja sõnum”**. Confirm bill service/quantity/total and the intended recipient.
4. Choose **“Edasi”**, review the preview, then **“Saada”** within the current authorization. The preview said the answer was ready and would be sent after payment, and contained generated payment/invoice links. No custom message edits were observed. Do not copy the recipient or secret-bearing links into the skill.
5. Filter **“Päringu olek: Makse ootel” → “Otsi”** and reopen the same enquiry. Confirm history **“Loodi ERPLY tellimus!”** and **“Saada makseteade”**, both targeting **“Makse ootel”**. Capture the bill's **“ERPLY nr”** as `ERPLY_ORDER_NUMBER`; sending the notice and creating the ERPLY order were recorded at 17:37.

## Pay and verify completion

1. In the notice's history entry, choose **“Vaata”** and open the freshly generated payment link (`index.php/et/pay`). This route was demonstrated from VAU history; inbox receipt/opening was not demonstrated. Check `BILL_REFERENCE`, payer, service, quantity and total.
2. Select the requested `PAYMENT_METHOD` and follow [request-driven payment handling](shared.md#payment-methods-and-scenarios); “Mastercard Visa” was the recorded example. The demonstration payment button was **“Maksa 60,00 €”**; the user completed the demo 3-D Secure step.
3. Return to staff **“Päring”**, filter **“Päringu olek: Lõpetatud” → “Otsi”**, and reopen `APPLICATION_ID`. The loaded detail was checked read-only after recording: **“Lõpetatud”**, `REGISTRATION_NUMBER`, **“Maksesumma” €60.00**, and history **“Server saatis allalaadimise lingi e-kirjaga”** at 05.11.2026 17:39. No manual **“Märgi lõpetatuks”** click was made. The log proves a recorded send event, not inbox delivery or actual download.
4. Follow [shared VAU payment-list checks](shared.md#vau-payment-list). Match **`BILL_REFERENCE` / €60.00 / Krediitkaart / Valideeritud / 05.11.2026 17:39**. Open that “Maksedokument”, which returns to this enquiry rather than an order-service-bill route.
5. In **“Teenuste arvestus nr …”**, verify reference, service, quantity/total, **“ERPLY nr” = `ERPLY_ORDER_NUMBER`**, **“ERPLY laekunud: Jah”** and **“ERPLY laekumise aeg”**. Exact receipt label here is **“ERPLY laekunud”**, unlike the order guides' “ERPLY laekumine”. Example: APA2026-00001 / 100684 / €60.00; creation 17:37, receipt 17:39.
6. ERPLY applies. Search **“Otsi”** by `CUSTOMER_NAME`. The user clarified that, of the two **“Uus, Erik”** matches, **the second is the correct demonstrated customer** (observed customer ID 2866). Open that customer and **“Tellimused”**. Confirm **“Number” = `ERPLY_ORDER_NUMBER`** and **“Summa”** matches the bill; the loaded list was checked read-only and showed **100684 / €60.00**, “Kinnit.” = “jah”, “Staatus” = “kinnit.”. Match the expected order as well as the name because search ordering/IDs may differ in another environment. Do not treat document-confirmation columns as receipt or open/edit the ERPLY document as a required step.

Also perform [shared Laekumised verification](shared.md#erply-receipt-checks-for-all-workflows) for this same customer and generated ERPLY order, matching receipt date, method, total/currency and linked order. This additional check was demonstrated in the Rights-certification recording and explicitly requested by the user for all workflows.

## Evidence and coverage limits

Recording `932CFD53-8360-4923-91DE-215B10FDBBB1`, 2026-11-05 17:33:12–17:40:55 Europe/Tallinn. Events 1265–1276 form/submission; 1277–1312 archive assignment/registration/forwarding; 1335–1344 response upload/readiness; 1354–1458 bill/notice/waiting state; 1459–1460/1586–1587 payment; 1588–1606 completed-list/payment checks; 1619–1621 ERPLY customer/orders. Final loaded enquiry detail and ERPLY row were inspected read-only afterward. The second-customer rule is the user's explicit explanation. The user also explicitly permitted AI generation of a small PDF for this test upload. Unrelated tabs, credential copy/paste detours and private enquiry/file details are excluded.

Shown path is documented. Coverage limits: logged-out login/minimum roles, some offscreen prefilled contact/address controls, initial purpose/delivery radio defaults, two dialog-accept inputs, alternative enquiry/delivery/payment branches, mailbox delivery, actual download and local compatibility. Quantity 2 is a test example; the reason was not stated. Do not generalize the €60 total or special-permission file override.
