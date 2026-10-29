# Tõenduspäevik

Hoia uurimise seisu töökaustas; kasutajale mõeldud lõpptulemused väljundikaustas. Väikese töö puhul piisab ühest Markdown-failist, pikemal tööl sobib JSON/JSONL. Ära loo keerukat andmebaasi, kui tabelitest piisab.

## 1. Koht ja uurimisküsimused

Salvesta sisend sõnasõnalt, uurimise kuupäev, küsimused ning kandidaadid. Iga koha kohta: praegune nimi/aadress, katastritunnus, koordinaadid koos koordinaatsüsteemiga (kui teada), ajaloolised nimed, mõis/kihelkond/vald ajavahemike ja allikatega, samastamise põhjendus ning vastuargumendid.

Väldi isikunimede ühendamist pelgalt nimekuju järgi. Isiku ID ja koha ID võivad olla lihtsad `P01`, `L01`; eraldi kandidaadid säilivad kuni samastus on põhjendatud.

Lisa põhiküsimuste katvustabel ja uuenda seda oluliste leidude järel:

| Põhiküsimus | Sobiv allikas | Tehtud otsing / loetud lehed | Vastus või takistus | Järgmine samm / lõpetamisalus |
|---|---|---|---|---|
| Nimi, talu vanim tõend, peremehed/elanikud, maad või hooned | Konkreetne register/säilik | Tegelik ulatus | Tõend või konkreetne puudus | Miks jätkata või miks see suund lõpetada |

„Otsimata“ ei ole lõpetamisalus. Kui kasutaja küsimus mõnd suunda ei hõlma, märgi see ülesandeväliseks.

## 2. Allikad

Iga allikas saab ID `S001` ja järgmised väljad:

| Väli | Sisu |
|---|---|
| Leidandmed | Arhiiv, fond.nimistu.säilik; säiliku pealkiri |
| Täpne asukoht | Originaalleht ja pöördel vajadusel p; digikaader; artikli lk/veerg või registrikirje ID |
| Link | Kontrollitud kirje/püsiviide; vajadusel eraldi vaaturilink |
| Aeg | Dokumendi dateering; sündmuse aeg eraldi; kontrollimise kuupäev |
| Liik ja sõltuvus | Algdokument, kataloogikirje, mälestus, ümbertrükk, OCR/HTR; millist allikat kordab |
| Ligipääs | Täpne digipildi olek juhendist, mitte oletus; Saaga puhul AISi kirje URL, „Vaata allikat“ nupu seis ja kontrollkuupäev |
| Tegelikult vaadatud | Kirjeldus / tervikpilt / konkreetne lõik / kõik kande lehed |
| Kohalik tõend | Pildifail ja lõikeinfo, lugemi asukoht/versioon, kui salvestatud |
| Panus ja piirang | Millisele küsimusele vastab; mis jäi lugemata |

Kaader pole sama mis originaalleht. Üks kaader võib sisaldada kaht lehekülge; säilita nii originaali leheküljenumber kui ka digikaadri number.

## 3. Väited

| ID | Väide | Allikas + täpne koht | Alus | Kindlus | Vastuolu / puuduv lüli |
|---|---|---|---|---|---|
| C001 | Üks kontrollitav väide | S001, kaader/leht | otsene / järeldus / mälestus / oletus | kindel / tõenäoline / ebakindel | Milline kontroll lahendaks? |

Järelduse puhul kirjuta nähtavale vahepealne põhjendus: näiteks kaart näitab sama õue ja samu naabreid, aga nimi on muutunud. Väite kindlus ei tohi ületada nõrgima vajaliku lüli kindlust. Tõendi puudumine pole vastupidise väite tõend.

Vastuolu ära kirjuta üle. Hoia mõlemad lugemid/allikad, kontrolli isikusamasust, veerge, kuupäevade kalendrit ja allikate omavahelist sõltuvust. Kui lahendus puudub, esita mõlemad koos piiranguga.

## 4. Otsingud ja kaetuse logi

```text
Andmebaas / säilik:
Päring ja filtrid:
Põhjus:
Vaadatud kirjed või kaadrid:
Meetod: register / sihtotsing / järjestikune vaatamine / valim
Tulemus:
Vahele jäänud alad ja ligipääsutõkked:
Järgmine samm:
```

Näiteks „kaadrid 1, 40, 80, 120; valim“ ei tohi muutuda kokkuvõtteks „köide 1–120 läbi vaadatud“. „Otsing ei andnud vasteid“ peab nimetama päringu, filtrid ja andmebaasi. „Kogu kontrollitud lõigus ei leitud“ eeldab, et lõigus polnud vaatamata kaadreid ning pildi kvaliteet võimaldas otsitavat tunnust lugeda.

## 5. Jätkamine ja parandused

Salvesta vahekokkuvõte: kinnitatud kohaankrud, kesksete allikate ID-d, lahtised küsimused, järgmine säilik/kaader, kasutatud töömaht. Nii ei pea järgmine sessioon allikaid uuesti läbi lugema.

Kui uus tõend muudab väidet, paranda kõik sellest sõltuvad raportiosad: lühivastus, narratiiv, ajajoon, isikute tabel, pildiallkirjad ja edasised tööd. Säilita uurimispäevikus eelmine järeldus ja paranduse alus.
