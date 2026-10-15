---
name: ai-kuluaruanne
description: Koosta Erik Uusi Rahvusarhiivi igakuine AI-kuluaruanne OpenAI ja Anthropicu arvetest ning Swedbanki maksetõenditest ja esita see RTIP-s. Kasuta ainult kasutaja selgesõnalisel kutsel ($ai-kuluaruanne); kulude või RTIP mainimine üksi ei käivita seda oskust.
---

# Igakuine AI-kuluaruanne

Kogu ühe kalendrikuu AI-kuludokumendid, seo arved tegelike euromaksetega ning koosta ja kasutaja tellitud ulatuses esita Rahvusarhiivi majanduskulude aruanne RTIP-s. Suhtle eesti keeles.

## Käivitamine ja ulatus

- Rakenda ainult kasutaja selgesõnalisel kutsel. `agents/openai.yaml` keelab automaatse rakendamise. Ära loo selle põhjal ajastatud ülesannet.
- Periood on üks kalendrikuu. Kui kuud pole nimetatud, lähtu eelmisest lõppenud kalendrikuust ning kontrolli, kas selle aruanne on juba esitatud; küsi ainult siis, kui periood jääb ebaselgeks.
- Teenused: **OpenAI ChatGPT Pro**, **OpenAI API**, **Anthropic API**. Hoia need kuluridades eristatuna. GitHub Copilot on lõpetatud ja jääb uute aruannete kogumisest välja.
- Kontode e-posti aadress: `erik.uus@gmail.com`. Tööandja: Rahvusarhiiv; töötaja: Erik Uus.
- Oskus ise ei laienda volitusi: kui kasutaja tellib koostamise ja esitamise, vii mõlemad lõpuni, kui andmed on kontrollitud. Ainult mustandi tellimisel jäta mustand. Varasem kirjade saatmise luba ei anna õigust tulevikus e-kirju saata.
- Kasuta Chrome'i ja sobivaid saadaolevaid ühendusi. Lase kasutajal vajaduse korral ise sisse logida ja autentimine lõpule viia. Ära salvesta oskusesse paroole, kontonumbreid ega seansitunnuseid.

## 1. Välista duplikaadid ja kogu arved

Vaata RTIP-s sama kuu olemasolevaid mustandeid ja esitatud aruandeid. Jätka sobivat mustandit, ära loo duplikaati. Võrdle ka varem hüvitatud arvenumbreid, eriti hilinenud pangakannete puhul.

Kogu originaalsed arve-PDF-id teenusepakkujate arvelduskeskkondadest. Gmail võib aidata neid leida, kuid kustutatud kirjade tõttu ei pruugi postkast olla täielik.

- ChatGPT: `https://chatgpt.com/settings/profile` → aktiivse paketi arveldamine ja arveajalugu.
- OpenAI API: `https://platform.openai.com/settings/organization/billing/overview` → õige organisatsiooni arved/arveldusajalugu.
- Anthropic API: `https://platform.claude.com/settings/billing` → õige tööruumi arved/arveldusajalugu.

Liigu nähtava kasutajaliidese järgi; menüüd võivad muutuda. Raamatupidaja Anneli Koll palus lisada **Invoice'id**, mitte eraldi **Receipt'id**. Ära lisa sama makse kohta mõlemat. Kui saadaval on üksnes Receipt, tuvasta erand ja selgita seda kasutajale; varasem GitHubi erand ei laiene automaatselt teistele teenustele.

Säilita arvenumbrid ja algsed PDF-id. Kontrolli kuupäeva, teenust, valuutat, maksu, krediite ja lõppsummat. Plaanivahetuse arvel võib kasutamata paketi krediit olla juba maha arvatud: ära arvesta seda teist korda.

## 2. Hangi pangast maksetõend ja sobita summad

Kasuta Swedbanki tegelikke kontolt maha kantud tehinguid. Erista konto väljavõtet, krediitkaardi broneeringuid ja krediitkaardi koondtagasimakset. Koondtagasimakset ei lisata teenusearvetele eraldi kuluna.

Koosta võimalusel **üks panga väljastatud ASiC-E väljavõte**, milles on asjaomased OpenAI ja Anthropicu tehingud. Vajaduse korral hõlma hilisem kuu, kui arve makse kajastub alles siis. Väljavõtte periood ja kuluaruande kuu ei pea kattuma. Kontrolli ekspordi sisu; PDF-i või ZIP-i laiendi muutmine `.asice`-ks ei loo panga väljavõtet.

Anneli kinnitas, et sama aastast väljavõtet võib kasutada mitme aruande juures. Eraldi kuuväljavõtet pole vaja, kui olemasolev fail juba tõendab kõiki makseid. Uute puuduvate maksete jaoks hangi neid kattev tõend.

Koosta kontrolltabel: teenus, arvenumber, arve kuupäev, teenuseperiood, algvaluuta ja arvesumma, panga kuupäev/viide, makse olek, EUR-summa, konverteerimistasu käsitlus ja failinimi.

- Kasuta tegelikku panga EUR-deebetit koos selles sisalduva konverteerimistasuga; ära lisa sama tasu uuesti ega asenda teadaolevat makset tänase valuutakursiga.
- Sama summa ja kuupäevaga arved võivad olla eraldi API-krediidi ostud. Kontrolli arvenumbreid ja tehinguviiteid; ära eemalda neid pelgalt sarnasuse tõttu.
- Krediidi ettemaksu arvet ja sama krediidi hilisemat kasutusaruannet ei hüvitata topelt.
- Seo kulu kuuga arve ja teenuseperioodi järgi. Hilisem pangakanne üksi ei tõsta kulu järgmisse kuusse. Vastuolu korral lahenda periood enne esitamist.
- Võrdle aruande summat valitud kulude maksetõenditega. Laiema väljavõtte kogusumma ei pea võrduma aruandega; põhjenda teiste perioodide ja väljajäetud ridu.

### Broneeringud

Broneering ei ole kontolt lõplikult maha kantud makse. Kontrolli hetkeseisu pangast; kuu lõpp ei muuda seda automaatselt tasutuks.

Näita broneeritud makseid kontrolltabelis eraldi. Kasutaja võib lubada need esitada koos broneeringutõendiga, nagu 2026. aasta III kvartalis. See varasem otsus ei ole kõigi tulevaste broneeringute kaasamise üldine luba. Kuni kaasamine pole otsustatud, kogu muud dokumendid ja valmista kontrollitav aruanne ette.

Kui broneeringud kaasatakse, tee üks PDF kokkuvõtte ja asjakohaste panga ekraanivaadetega. Märgi kontrollimise kuupäev, tehingupäev, teenus, EUR-summa, arvenumber ja olek „broneeritud”. Erista need aruandes tasutud maksetest. Teiste kuude makseid ei lisata PDF-i kogusumma tõttu aruandesse. Sama makset ei hüvitata hiljem lõpliku pangakande alusel uuesti.

## 3. Vormista RTIP-s kuu aruanne

Aadress: `https://www.riigitootaja.ee/rtip-client/secure/desktop`.

Anneli juhis: **Majanduskulud → Minu majanduskulud → Uus dokument → Majanduskulude aruanne**. Edaspidi iga kuu eraldi; kvartalite kaupa esitamine oli tagantjärele erand.

- Kululiik: **IT riist- ja tarkvara rent ja majutusteenus**. Varasem kood `[0055148000]`; kontrolli nähtavat nimetust, ära eelda koodi muutumatust.
- Iga arve eraldi kulureana; makseviis **Maksin ise**, valuuta **EUR**, summa kontrollitud panga EUR-summana.
- Selgitus: teenusepakkuja ja teenus, arvenumber ja -kuupäev, algvaluutas summa, pangamakse kuupäev/viide ja EUR-summa ning vajaduse korral konverteerimistasu või broneeringu selgitus.
- **Lisadokumendid**: selle kuu algsed arved, pangaväljavõtte ASiC-E ning lubatud broneeringute korral kokkuvõtte ja ekraanivaadete PDF. Kontrolltabel ei asenda algdokumente.
- Üldkommentaaris nimeta kuu, teenused ja kogusumma. Broneeringute korral erista tasutud ja broneeritud osad ning märgi kontrollimise kuupäev.
- Ära täida oletuste põhjal jaotist „Täidab finantstöötaja”.

Salvesta, oota laadimise lõppu ning kontrolli kuluridu, kogusummat ja manuseid. Vajaduse korral ava salvestatud aruanne uuesti, et kinnitada püsimine. RTIP reageeris varasemal kasutamisel aeglaselt: pärast klõpsu vaata värsket leheolekut, enne kui toimingut kordad.

## 4. Kontrolli ja esita

Enne esitamist peavad kuu, arvenumbrid, summad, makseolekud ja manused sobima ning duplikaadid olema välistatud. Lahendamata sisulise erinevuse korral säilita mustand ja ütle täpselt, milline tehing vajab selgitust.

Kui esitamine on tellitud, vali **Valmis esitamiseks**, kontrolli menetlusringi ja seejärel **Esitan dokumendi**. Varasem vaikimisi ring oli Anneli Koll (kooskõlastaja), Anu-Hannele Puskar (kinnitaja), Maire Kosk (raamatupidaja). Need on varasemad andmed, mitte käsk asendada tulevikus RTIP määratud isikuid. Sisulise ootamatu erinevuse korral selgita põhjus.

Kinnita nähtav olek **Kooskõlastamisel**. Nupu vajutamine või „Koostamisel” ei kinnita esitamist. Säilita aruande ID, periood, summa, kontrolltabel, dokumendid ja tulemuse ekraanipilt. Anna lühike kokkuvõte koos oleku ja võimalike broneeringutega.

## Varasemate kulude duplikaadikontroll

06.10.2026 esitati järgmised 2026 aruanded. Hilisem staatus tuleb vajaduse korral RTIP-st üle vaadata.

| Periood | Aruande ID | Summa |
|---|---|---|
| I kvartal | 543530 | 100,80 EUR |
| II kvartal | 543541 | 113,01 EUR |
| III kvartal | 543544 | 470,97 EUR |

III kvartalis sisaldus juba 151,25 EUR broneeringuid: Anthropic `939C1F97-0023` 21,60 EUR; OpenAI API `08FA4B95-0003` 10,82 EUR ja `08FA4B95-0004` 10,87 EUR; ChatGPT Pro `3AB618B6-0037` 107,96 EUR. Ära lisa neid hilisema pangakande tõttu uuesti.

01.10.2026 OpenAI API arve `08FA4B95-0005` broneering 11,07 EUR **ei sisaldunud** III kvartalis. Oktoobri aruandes kontrolli lõplikku makset ja seda, kas arve on vahepeal juba esitatud.

Varasemad failid asusid `/Users/erikuus/Documents/Codex/2026-10-05/ca/outputs/`, sh `RTIP-2026/kuluandmed.json`, algarved kaustas `AI-kulud-2026/` ning `Broneeritud-AI-maksed-2026-10-05.pdf`. Kontrolli olemasolu; need on ajalooline viide, mitte tulevaste kuude andmeallikas. Hoia uued tulemused kasutaja töökaustas kuu kaupa, mitte oskuse kaustas.
