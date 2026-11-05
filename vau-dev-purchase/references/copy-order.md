# Copy order

Status: **Demonstrated — digital reproduction, whole archival unit, simulated FTP preparation, service bill and card payment.** “Koopia” means ordering reproductions, not duplicating an existing order. Read [shared.md](shared.md) first. Use Computer Use and current labels/row context; all IDs below are examples to replace with generated values.


Apply the current request's [payment method and scenario](shared.md#payment-methods-and-scenarios). The payment choices and results below are the recorded successful-card baseline, not fixed replay instructions. Substitute the requested supported method/API case/test data. Paid/receipt/completion checks apply only to expected success; for failure, cancellation or pending cases use the shared outcome checks instead of proceeding through success-only steps.

## Inputs and starting state

Start signed in at `index.php/et`. The demonstrated account could use researcher, customer-service and copy-centre views. These staff actions are part of this demonstrated purchase lifecycle; they do not grant permission for unrelated administration or authorize future staff changes.

| Variable | Demonstrated value / field |
| --- | --- |
| `ARCHIVE_REFERENCE` | Required “Leidandmed”: EAA.1.1.2. |
| `ORDER_TYPE` | Required “Tellimuse liik”: “Koopia”; initially disabled before entering the reference. |
| `COPY_SERVICE` | Digikoopia → “A2 kuni A0 formaadist, trükikvaliteediga (fotodest, kaartidest jms), kaader: 20,00 €”. Resolve current label/price. |
| `COPY_SCOPE` | “Kogu säilik”. Partial-copy input was not demonstrated. |
| `PURPOSE` | Required “Kasutuseesmärk”: “Teadustöö”. |
| Notes / keywords | “Tellija märkused” left empty; “Märksõnad” later showed “Puudub”. |
| Delivery / payment | “Interneti (ftp-serveri) kaudu” was the visible delivery option; selected payment was “Maksan krediitkaardi või pangalingiga (Swedbank, SEB, Luminor, LHV)”. |
| `ACCOUNT_EMAIL` | Confirm the displayed account address is in use; do not hardcode demonstration contact data. |
| `COPY_CENTRE` | Required “Koopiakeskus”: “Koopiakeskus B 310”. Other centre choices were visible but not used. |
| `SERVICE_QUANTITY` | Required “Kogus”: 1. Unit price €20; resulting total €20.00. Do not assume “Kogu säilik” fixes billable quantity in other orders. |
| Staff note / deadline | “Menetleja märkus” and “Koopiate valmimise tähtaeg” left blank. The note is explicitly visible to the researcher. |
| `FTP_FOLDER` | Generated required “Ftp” value retained without editing; never store its demonstrated value or access link in the skill. |
| `VAU_ORDER_ID` | Generated order number 1068808; use to follow the same request through staff views. |
| `BILL_REFERENCE` | Generated “Teenuste arvestus nr” KTA2026-00004; example detail ID 45830. |
| `ERPLY_ORDER_NUMBER` | Generated “Tellimus nr” / “ERPLY nr” 100682. This differs from `VAU_ORDER_ID`. |

## Researcher: create and submit

1. Home → **“Tellimused”** → “Koostamisel” (`index.php/et/order/index?scope=clientDraft`). In “KOOSTA TELLIMUS”, enter `ARCHIVE_REFERENCE` in “Leidandmed”.
2. Set “Tellimuse liik” to **“Koopia”**. In the service chooser (“Vali”), select `COPY_SERVICE` under “Digikoopia”; choose **“Kogu säilik”** and `PURPOSE` in “Kasutuseesmärk”. Choose **“Lisa”**.
3. Find the new draft by reference/type and choose its **“Kinnita”** (`index.php/et/order/confirmCopyOrder?id=VAU_ORDER_ID`). Check reference, service, scope and purpose; capture `VAU_ORDER_ID` from the heading.
4. Check the internet/FTP delivery branch and choose the checkout option for the requested `PAYMENT_METHOD` (the demonstration used card/bank-link payment). The page says downloads become available after payment and warns that service prices can be refined. Choose **“Kinnita”** under the user's authorization.
5. In the email review dialog, verify the displayed account address and choose **“Kinnitan, et see e-posti aadress on kasutusel”**. Confirm **“Tellimus on esitatud!”** and that the order moves out of drafts into submitted orders. Email editing was not demonstrated.

## Staff: prepare the copy and bill

Only perform these mutations when included in the user's current authorization. Stay on `VAU_ORDER_ID` and `ARCHIVE_REFERENCE` throughout; do not process a neighbouring row.

1. Use the staff **“Tellimus”** navigation → **“Klienditeenindaja” → “Laekunud”** (`index.php/et/orderManage/index?scope=clientManagerReceived`). Locate the submitted copy order; open its row action menu and choose **“Digikoopiad olemas”**. A brief “Fondihoidja” navigation detour is omitted.
2. On **“Määra koopiakeskus”** (`index.php/et/orderManage/clientManager?id=VAU_ORDER_ID`), select `COPY_CENTRE` and choose **“Saada”**. Confirm **“Toiming sooritatud!”** / the order's arrival in the next queue.
3. Choose **“Koopiakeskuse töötaja” → “Laekunud koopiatellimused”** (`scope=copyManagerRecievedCopyOrders`, spelling as observed). Verify the row's ID/reference, “Sihtruum” and **“Digikoopiad olemas”** state.
4. Row actions → **“Vormista”** (`index.php/et/orderManage/specify?id=VAU_ORDER_ID`). In “Hinnakiri”, check “Teenus”, set required **“Kogus”** to `SERVICE_QUANTITY`, and confirm “Kokku” / **“Tasuda: 20.00 €”** in this example. Initially the total was 0.00; after quantity 1 it became 20.00. Choose **“Salvesta ja pöördu tagasi”**.
5. Same row → **“Määra FTP”** (`index.php/et/orderManage/copyManager?id=VAU_ORDER_ID`). Retain the generated “Ftp” value. In the demonstrated test environment, check **“Loo FTP kaust käsitsi (märgi see, kui testimisel pole vaja kausta reaalselt luua)”**, then **“Salvesta”**. This intentionally skips real folder creation; see shared environment differences before reuse.
6. Same row → **“Koopiad valmis”**. The dialog **“Oled kindel, et soovid teha selle toimingu?”** offered “OK” / “Cancel”; the resulting **“Toiming sooritatud!”** and removal from the incoming queue establish completion, although the specific dialog-accept input was not captured.
7. **“Klienditeenindaja” → “Koopiad valmis”**. Find the same order and choose row action **“Koosta teenuste arvestus”** (`index.php/et/invoice/create`). Check payer, payment method, archival reference, service, quantity and total. “Postikulu” remained blank in this digital-delivery branch. Choose **“Salvesta”**.
8. Capture `BILL_REFERENCE` from **“Teenuste arvestus nr …”** (`index.php/et/invoice/view?id=BILL_ID`); initially **“Tasutud: Ei”**. Choose **“Esita arvestus”**. The subsequent researcher payment page establishes that the bill became payable; no separate submission toast was captured.

## Researcher: pay

1. **“Minu tellimused uurijana” → “Esitatud”**. Use the relevant order's **“Maksa”** action.
2. On `index.php/et/invoice/pay`, capture `ERPLY_ORDER_NUMBER` from **“Tellimus nr …”**; verify the same reference/service, quantity and **“Tasuda”** (€20.00 here).
3. Select the requested `PAYMENT_METHOD` and [execute its requested scenario](shared.md#payment-methods-and-scenarios). The recorded “Mastercard Visa” branch is described in the shared card example. The demonstrated provider button was **“Maksa 20,00 €”**; the user completed the demo 3-D Secure step. Do not store payment credentials or use captured payment links.

## Verify VAU and ERPLY

1. Follow [shared VAU payment-list checks](shared.md#vau-payment-list): **“Arvestus” → “Veebimaksed”**. Match `BILL_REFERENCE` with **“Summa” €20.00**, **“Makseviis” Krediitkaart**, **“Olek” Valideeritud**, payer and payment time.
2. Open that **“Maksedokument”** link to the service bill. Verify the reference, service/quantity/total, **“Tasutud: Jah”**, **“ERPLY nr” = `ERPLY_ORDER_NUMBER`**, and **“ERPLY laekumine: Jah”**. The example showed both payment and ERPLY receipt at 05.11.2026 16:37. The user highlighted ERPLY number 100682 and receipt “Jah”. These are the demonstrated payment-success criteria; no payment-confirmation toast was captured for this Copy order.
3. ERPLY applies. Search the existing ERPLY customer's sidebar **“Otsi”** by `CUSTOMER_NAME`, choose the correct customer, then **“Tellimused”**. Locate **“Number” = `ERPLY_ORDER_NUMBER`** and match **“Summa”** to the bill. Example 100682 / €20.00 was checked read-only after recording; list columns were “Number”, “Kuupäev”, “Tähtaeg”, “Summa”, “Kinnit.”, “Staatus”. The row showed “jah” / “kinnit.” in the last two columns. Those describe document confirmation; receipt is independently established by the VAU bill above. Opening an ERPLY document is not part of the demonstrated verification.

Also perform [shared Laekumised verification](shared.md#erply-receipt-checks-for-all-workflows) for this same customer and generated ERPLY order, matching receipt date, method, total/currency and linked order. This additional check was demonstrated in the Rights-certification recording and explicitly requested by the user for all workflows.

## Evidence and limits

Recording `D1DDDE3F-B3D6-4E9E-8611-B60CDAF30345`, 2026-11-05 16:33:08–16:38:31 Europe/Tallinn. Events 245–268: researcher submission; 269–298: staff copy preparation; 299–304: bill; 305–308/441–442: payment; 443–461: VAU checks; 468–474: ERPLY customer lookup/orders. The loaded ERPLY row was observed read-only after stopping. Retain only VAU/payment/ERPLY actions, omitting unrelated tabs and credential copy/paste detours.

Shown path is documented. Coverage limits: minimum roles/login, partial copies, other services/delivery/payment branches, real FTP folder creation, actual copying/upload/download and error recovery were not demonstrated. The generated FTP reference and “Koopiad valmis” state do not prove files exist or were delivered. One dialog-accept input was not captured; its prompt and successful outcome were. Local compatibility remains unverified.
