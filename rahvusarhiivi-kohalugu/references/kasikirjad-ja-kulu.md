# Käsikirjade lugemine ja kulude juhtimine

## Otsing ei ole transkriptsioon

Suurim sääst tuleb õige lehe leidmisest enne süvalugemist. Kasuta kirjeldust, köite registrit, nimeregistrit, asjakohast olemasolevat HTR-teksti ja ristviiteid. OCR/HTR on otsinguabi, kuni oluline lugem on pildiga võrreldud.

Ära eelda tavalise OCR-i head tulemust gooti käsikirjas. Kurrent on käekiri, fraktuur trükikiri; sobimatu tuvastus võib toota usutavat mõttetust. Masintuvastuse puudumine ei takista multimodaalset lugemist, kuid mudeli enesekindlus pole tõend.

## Neljaastmeline pilditöö

1. **Orientiir.** Vaata terviklehe pealkirja, veerge, nummerdust ja kannete piire. Märgi keel/kiri ning vajalik ala. Väike ülevaade ei sobi peenkirja lõplikuks lugemiseks.
2. **Sihtlõik.** Ava originaali suurem versioon või suurenda vajalikku ala. Säilita veerupäised või nende eraldi kontrollitud lugem, naaberread, servamärkused ja tabeli vasaku/parema poole seos. Ära loe sünnikuupäeva surmaveerust ega vanust valest revisjoniveerust.
3. **Lugem.** Loe esmalt nähtavad märgid; tõlge ja tõlgendus tulevad eraldi. Säilita nimede algkuju, lühendid, reavahetused ja tähtsad parandused. Piirdu küsimusele vastava kandega.
4. **Kontroll.** Võrdle kesksete väidete nimesid, aastaid, summasid, sugulussuhteid ja talunumbreid uuesti originaaliga. Kasuta sama kirjutaja kindlaid tähekujusid, kõrvallehte või sõltumatut allikat. Sama pildi korduv küsimine ilma uue teabeta pole sõltumatu kontroll.

Arhiivipilte võib lugemiseks deterministlikult kärpida, pöörata või mõõdukalt kontrasti muuta, säilitades originaali ja teisenduse kirjelduse. Ära kasuta generatiivset pildiparandust ega teksti taastamist ajalooallika tõendina. Suurendamine ei taasta kadunud detaile; eelista algfaili suuremat eraldusvõimet.

Lõike juures säilita allika ID, säilik, kaader, originaalleht/külg, pildi mõõtmed, piirkond (pikslites või protsentides, süsteem märgitud), töötlus ja lugemi versioon. Vaaturi ekraanipilti ära nimeta originaalskanniks.

## Lugemi väljund

```text
Allikas/asukoht: S012, säilik ..., kaader ..., lk ..., vasak alumine kanne
Pildi kvaliteet ja puuduv kontekst: ...
Originaallugu: ...
Normaliseeritud nimed ja tõlge: ...
Kindlad väljad: ...
Ebakindlad väljad: sõna/number, võimalikud lugemid, põhjus
Seos uuritava kohaga: tõendatud / tõenäoline / kontrollimata, põhjendus
Järgmine vajalik kontroll: ...
```

Märgistus: `[loetamatu]`, `Ranniku[?]`, `[Ranniku / Ranniko]`, `d[essen]` kindla lühendi avamiseks. Tõlge säilitab ebakindluse. Allkirju, parandusi ja muid märke kirjelda esmalt nähtaval kujul; nende tähendus vajab konteksti või lisatõendit.

Kindlus anna väljade kaupa (kindel / tõenäoline / ebakindel), mitte lehele ühe protsendina. Selge nime, kuid ebaselge aastaarvu korral kasuta nime ja piira ajalist väidet. Vanusest arvutatud sünd on hinnang. Vana/uue kalendri teisendus vajab ajastule sobivat kontrolli, mitte alati sama päevade arvu liitmist.

## Tabelid ja kaardid

- Hingeloendis kontrolli eelmist/praegust vanust, pere-/talunumbrit, meeste/naiste lehe seost ja liikumismärkusi. Inimeste arv kontrolli ridade ja suhete järgi.
- Personaalraamatus kontrolli pealkirja, leheküljeviiteid, pereliikmete rühmitust ja hilisemaid lisandeid. Külas sündimine ei tõenda sama õue asukohta.
- Plaanil loe eraldi pealkiri, koostamisaeg, kõlvikutabel, naabrid ja allkirjad. Mõõdistamise aeg ei pruugi olla allkirjade aeg.
- Säilita algühikud. Vakamaa, kapp, adramaa ja rahaühikud vajavad piirkonna/perioodi kontrolli; ära kasuta universaalset hektaritegurit. Summad kontrolli deterministlikult, kuid ära muuda lugemit selleks, et summa klapiks.

## Praktiline kulukontroll

- Laadi ainult etapis vajalik skilli viitefail. Tekst loe DOM-ist; pilt ava siis, kui fakt sõltub pildist. Väldi täispika lehe korduvat väljastamist.
- Hoia lubatud pildid ja lugemid lokaalses vahemälus. Kordused tuvasta säiliku+kaadri järgi; kohalikel failidel võib kasutada kontrollsummat. Raport kirjuta päevikust.
- Köite struktuuri leidmise järel vaata järjestikuste kaadrite päiseid väikeste partiidena. Kontaktleht ei tohi muuta nimesid loetamatuks; selle negatiivne tulemus ei välista vastet.
- Kui eri mudelid on tegelikult saadaval ja lubatud, kasuta odavamat lihtsaks kirjete järjestamiseks ja tõestatult sobivat nägemismudelit keeruka kirja jaoks. Ära väida hinna-/kvaliteedieelist mõõtmiseta. Vaikimisi piisab ühest uurijast; mitme agendi kogu köite lugemine pole säästumeetod.
- Enne uut kallist pildilugemist määra üks küsimus: millise olulise väite see lahendab? Selge vastuse puudumisel täpsusta registriotsingut või jäta kõrvalharu edasiseks.
- Tundmatu käekirja korral proovi tüüpilist lõiku enne hulgituvastust. Halva tulemuse korral muuda pildikvaliteeti või meetodit; ära korda seda sadadel lehtedel.
- Kui suurendatud lõik ja kontekst ei lahenda olulist lugemit, jäta see ebakindlaks või soovita paleograafi kontrolli. Uus tõend õigustab uut kontrolli; sama pildi lõputu ümberlugemine mitte.
- Teenuselimiidi korral salvesta jätkamiskoht ja kasuta sõltumatut allikat. Ära väldi piirangut kontovahetuse või ligipääsukontrolli ületamisega.

Kulupäevik: uued kaadrid, süvalugemised, korduvlugemised koos põhjusega ja lahendatud põhiküsimused. Tegelikud tokeni-/hinnamõõdikud lisa ainult nende olemasolul; muidu on need töömahu näitajad, mitte eurokulu hinnang. Jäta töömahtu lõpukontrolliks.

Abi: [RA lugemine ja tõlkimine](https://www.ra.ee/vau/index.php/et/page/article/index?menuId=32), [paleograafia](https://www.ra.ee/apps/paleograafia/), [Transkribuse katvus](https://rahvusarhiiv.transkribus.eu/about). Välisesse HTR-teenusesse üleslaadimine ja tasuline transkriptsioon ei ole vaikimisi töövoog; kontrolli andmete sobivust ja kasutaja volitust.
