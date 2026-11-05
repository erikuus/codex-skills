# Rights-certification enquiry

Status: **Demonstrated — “Muu” rights-certification branch, archive assignment, state-fee notice, card payment and “Makstud”/VAU/ERPLY verification.** The recording stops after payment; processing/certifying the answer is not demonstrated. Read [shared.md](shared.md) first. Use Computer Use with current labels and the same application throughout. Submissions and notices require the user's current authorization.


Apply the current request's [payment method and scenario](shared.md#payment-methods-and-scenarios). The payment choices and results below are the recorded successful-card baseline, not fixed replay instructions. Substitute the requested supported method/API case/test data. Paid/receipt/completion checks apply only to expected success; for failure, cancellation or pending cases use the shared outcome checks instead of proceeding through success-only steps.

## Inputs and starting state

Start signed in at `index.php/et`; the session also had staff enquiry permissions. No login or researcher role switch was shown.

| Variable | Demonstrated value / behavior |
| --- | --- |
| `ENQUIRY_FORM` | “Muu” (`index.php/et/enquiry/application/create?type=8` in this environment). |
| Applicant identity / contact | Account-prefilled, disabled “Eesnimi *”, “Perekonnanimi *”, “Sünnikuupäev *”. Review current country/contact/address fields; some controls were offscreen in the capture. Do not retain example personal data. |
| `PURPOSE` | **“Õiguste ja tehingute tõendamine või ametialane toiming”**. The resulting record confirms this selection; do not use the Personal-interest service-fee branch. |
| `CERTIFICATE_DESTINATION` | Required **“Asutus, kuhu arhiiviteatis esitatakse”** appeared for this purpose. A placeholder institution was entered; use the user's intended test institution. |
| `DELIVERY_METHOD` | **“E-postiga (digitaalselt allkirjastatud teatis)”** in the resulting record. “Postiga” and “Tulen ise järele” were visible alternatives; initial radio defaults were not clearly captured. |
| `ENQUIRY_TEXT` | Required **“Missugust infot ja/või mille jaoks arhiivist otsite?”**; a short test value was entered. Use the requested test content. |
| `ARCHIVE_UNIT` | “Tartu”. |
| `STATE_FEE` | Observed **€25.00**, populated by this branch. This is a dated UI observation, not a current legal-fee determination. No service quantity was edited and no Personal-interest response-fee acknowledgement was used. |
| `APPLICATION_ID` | Generated example 116080. No staff registration/ARP number was generated in this recorded segment. |
| `PAYMENT_NOTICE_REFERENCE` | Generated **APM2026-00001** (“Makseteatis nr”), distinct from an APA service bill. |
| `ERPLY_ORDER_NUMBER` | Generated **100685**. |

## Applicant: submit

1. Home → **“Arhiivipäringud”** (`index.php/et/enquiry/form/index`) → **“Muu”**. Review prefilled identity/contact fields.
2. Choose/check `PURPOSE`, fill required `CERTIFICATE_DESTINATION`, choose/check `DELIVERY_METHOD`, and enter `ENQUIRY_TEXT`. Verify the final preview values instead of assuming defaults. The form described state-fee payment before processing the certificate; do not copy the other branch's service-bill/response-first sequence.
3. Choose **“Edasi”** and follow [shared email confirmation](shared.md#researcher-email-confirmation), then review the **“Esita päring”** preview (`index.php/et/enquiry/application/preview`). The preview explicitly said **“Päring ei ole veel esitatud!”** until submission.
4. Choose **“Esita päring”**; confirm **“Päring on esitatud”**. Additional applicant-file upload was not demonstrated.

## Staff: assign and send the fee notice

1. Staff **“Päring”** → **“Halda päringuid”** (`index.php/et/enquiry/application/admin`). Open the newly submitted applicant/form/time row and capture `APPLICATION_ID` (`index.php/et/enquiry/application/view?id=APPLICATION_ID`). Distinguish this application from earlier matching-name/contact enquiries; the page displayed duplicate-data warnings.
2. Select `ARCHIVE_UNIT` in **“Vali arhiiviüksus”** and choose **“Määra”**. On the admin list, set **“Päringu olek: Määratud”**, choose **“Otsi”**, and reopen the same application. Verify purpose, delivery and institution.
3. Choose **“Saada makseteade”**. Follow the [shared enquiry notice steps](shared.md#enquiry-payment-notices). Here the prefilled subject/preview was **“Arhiiviteatise riigilõivu makseteade”** and the notice requested **€25**. No response upload, processor forwarding or “Lisa teenuste arvestus” action occurred first.
4. Review **“Saaja aadress”**, subject and required message, choose **“Edasi”**, review the preview and choose **“Saada”** within the authorized test. The preview contained freshly generated payment, notice and application links. No custom message edits were observed; do not store their access codes or reuse captured links.
5. Filter **“Päringu olek: Makse ootel” → “Otsi”** and reopen the same application. In **“Andmed päringu kohta”**, capture **“Makseteatis nr”**, **“Maksesumma”** and **“ERPLY nr”**; verify archive unit. The example showed APM2026-00001 / €25.00 / 100685. History showed **“Loodi ERPLY tellimus!”** and **“Saada makseteade”**, both targeting “Makse ootel”, at 05.11.2026 17:56.

## Pay and verify the recorded endpoint

1. In the sent notice's history entry, choose **“Vaata”** and open its generated payment link (`index.php/et/pay`). This was shown from VAU history; receiving/opening the email in an inbox was not demonstrated.
2. Confirm the enquiry identity and **“Tasuda: 25,00 €”** under “Makse sooritamine”. Select the requested `PAYMENT_METHOD` and follow [request-driven payment handling](shared.md#payment-methods-and-scenarios). The recorded card example used “Mastercard Visa” with a generated `paymentEnquiryApplication/submit` action. The user chose **“Maksa 25,00 €”** and completed the demo 3-D Secure step.
3. Follow [shared VAU payment-list checks](shared.md#vau-payment-list). Match `PAYMENT_NOTICE_REFERENCE` with **€25.00 / Krediitkaart / Valideeritud / 05.11.2026 17:58** and open its “Maksedokument”, returning to this application.
4. Verify **“Päringu olek: Makstud”**, the same notice reference and amount, **“Veebimakse aeg”**, **“ERPLY nr” = `ERPLY_ORDER_NUMBER`**, **“ERPLY laekunud: Jah”**, and **“ERPLY laekumise aeg”**. Example creation 17:56, payment/receipt 17:58. History recorded **“Klient maksis pangalingiga”** → “Makstud”; this generic history wording does not override the observed card choice and “Krediitkaart” payment-row method.
5. Return to **“Halda päringuid”**, filter **“Päringu olek: Makstud” → “Otsi”**, and reopen the same application to confirm its paid state. A detour through “Lõpetatud” did not establish completion; do not require “Lõpetatud” for this recorded endpoint or mark it completed manually.

## ERPLY checks

ERPLY **applies** to this state-fee notice. Use shared customer lookup and select the correct test customer (the second of the two “Uus, Erik” matches in this environment; observed ID 2866). Match **`ERPLY_ORDER_NUMBER` / `STATE_FEE`** in **“Tellimused”** without opening/editing the document. The recorded navigation reached that tab before the additional receipt check.

Then perform [shared Laekumised verification](shared.md#erply-receipt-checks-for-all-workflows). The loaded receipt list was inspected read-only after recording: **05.11.2026 / Krediitkaardiga / 25,00 EUR / Tellimus 100685**, with matching invoice date. This directly ties the receipt to this order. The “Kommentaar” text **“makstud 14 päeva varem”** is a relative due-date comment, not the identifier or a required fixed result.

## Evidence and coverage limits

Recording `236E357F-8638-4A36-9404-4ECFB6B1C224`, 2026-11-05 17:54:56–18:00:16 Europe/Tallinn. Events 1645–1656 form/submission; 1657–1685 assignment/notice/waiting state; 1686–1687/1822–1823 payment; 1824–1892 VAU accounting/paid-state checks; 1893–1906 ERPLY customer/orders/receipts. The fully loaded “Laekumised” row was inspected read-only afterward. Unrelated tabs, credential copy/paste and private enquiry details are excluded.

Shown paid-notice path is documented. Not demonstrated: subsequent registration/processor assignment, response drafting/upload, digital signing/certification, answer delivery, final enquiry completion, minimum roles/login, some offscreen contact controls, alternative payment/delivery branches and local compatibility. The PDF test-response option authorized for Personal-interest enquiry does not establish a signed certificate workflow here.
