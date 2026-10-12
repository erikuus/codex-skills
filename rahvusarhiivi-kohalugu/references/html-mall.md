# HTML-malli kasutamine

Lõppraporti vormistamiseks kasuta kaasasolevat malli. See toetab sisukorda, lühivastust, põhifakte, ajajoont, tabeleid, pilte, dokumendilugemeid ja allikaviiteid. Vali sisu ja peatükid uurimisülesande järgi.

Kaasasolev andmefail kasutab täielikult väljamõeldud juhtumit: Ranniku talu, endine Lepiku talu, Saluoja külas. Ka nimed, daatumid, dokumendipealkiri ja leidandmed on fiktiivsed; võimalik nimekattuvus on juhuslik. `NAIDIS`-tähised ja `example.invalid`-lingid ei osuta päris arhiivikirjetele. Ära otsi nende järgi ega esita neid kontrollitud allikatena.

## Genereerimine

1. Kopeeri `assets/report-data.example.json` uurimise töökausta failiks `report-data.json`.
2. Asenda näitetekstid kontrollitud sisuga. Kohanda peatükkide pealkirjad, valik ja järjekord ülesandele; tühjade `blocks`-loenditega peatükid jäetakse välja. Nummerda kasutatud peatükid loetavalt ning säilita unikaalsed ID-d. Eemalda kõik näidisallikad ja kasutamata viited.
3. Sea `demo` väärtuseks `false` alles siis, kui näidisandmed on asendatud. Lisa kuupäev, uurija nimi või koostamisviis ning tegelikud piirangud `method`-loendisse. Näidise märkuse eemaldamine ei kinnita automaatselt ajaloolist kvaliteeti.
4. Käivita, kasutades skilli tegelikku asukohta:

```sh
python3 /Users/erikuus/.agents/skills/rahvusarhiivi-kohalugu/scripts/render_report.py work/report-data.json outputs/raport.html
```

Skript kasutab ainult Pythoni standardteeki. Ta ei otsi allikaid, ei saada andmeid võrku ega telli teenuseid. Kohalikud PNG/JPEG/WebP-pildid pakitakse HTML-i sisse. Genereeritud faili saab avada otse brauseris, eraldi serverit või JavaScripti sisu kuvamiseks pole vaja. PDF-i jaoks vali nupust „Prindi / salvesta PDF“ brauseri PDF-väljund; nupu olemasolu ei tähenda, et PDF-fail on juba loodud.

## Andmestruktuur

Tekstiväljad on lihttekst, mitte HTML ega Markdown. Sisu HTML-märgid turvatakse automaatselt. Märgendite toetamist ära lisa üksikute rasvaste sõnade pärast: kasuta pealkirja, plokki või lühemat lõiku.

Ülataseme väljad:

- `title`, `date` ja `sections` on vajalikud; `subtitle`, `author`, `notice`, `footer` on valikulised tekstid.
- `demo: true` kuvab nähtava näidisehoiatuse ja lubab pildikohatäitjaid. Lõppraportis `false`.
- `facts`: objektid väljadega `label`, `value`, valikuline `note` ja `refs`. Silt peab täpsustama, millist kohta, aega või tunnust väärtus kirjeldab.
- `sections`: objektid `id` (`sec-` ja positiivne täisarv), `title` (koos jaotisenumbriga), `blocks`. Allikate osa lisatakse automaatselt `sources` põhjal ja nummerdatakse kuvatud peatükkide arvu järgi.
- `sources`: objektid `id` (nt `S1`), `title`, `url` (HTTP/HTTPS), valikulised `citation` (leidandmed, aasta, leht/kaader) ja `access` (mida kontrolliti, millal, ligipääsu seis).
- `method`: lihttekstide loend uurimise ulatuse ja piirangutega.

Viidatavat tekstiosa esitab string või objekt:

```json
{"text":"Kontrollitav väide.","status":"jareldus","refs":[{"source":"S1","locator":"lk 196, kaader 108"}]}
```

`refs` võib sisaldada ka lihtsalt allika ID-d, kui täpne asukoht on allikakirjes. `status` on valikuline ja võib olla `otsene`, `jareldus`, `oletus`, `ebakindel`, `kontrollimata`, `malestus`. See tähistab autori määratud tõendi liiki või piirangut, mitte automaatselt hinnatud tõenäosust. Ebakindluse sisu selgita ka tekstis.

## Sisuplokid

| `type` | Vajalik sisu | Valikulised väljad |
|---|---|---|
| `paragraph` | `text` | `status`, `refs` |
| `notice` | `text` | `title`, `tone: "warning"`, `status`, `refs` |
| `list` | `items`: stringid või tekstiobjektid | `ordered: true` |
| `table` | `columns`: veerunimed; `rows`: sama arvu lahtritega read | `caption`; lahter võib olla viidetega tekstiobjekt |
| `timeline` | `events`: objektid `date`, `text` | sündmusel `kind`, `status`, `refs` |
| `figure` | `title`, `image`, `alt`, `refs` | `caption` |
| `document` | `title`, `original`, `translation`, `note` | `refs`, `figure` (pildiploki objekt) |

Ajajoon säilitab sisendi järjekorra; kuupäevi ei arvata automaatselt numbriteks. Järjesta sündmused ise ning kasuta vahemikke ja `u`/`[?]` märgendeid. Tabelites esita rollid ning tõendatud ajavahemikud, mitte oletatud katkematu omandijada.

Pildifaili `image` on kohalik tee JSON-faili suhtes. Skript ei laadi kaugpilte ise alla. Lisa pildi pealkirja/`caption`-välja dateering, leht/kaader, allikas, kärpe selgitus ja vajadusel õiguste info. Lõppraporti pildiplokk ilma pildita annab vea; kui pilti ei ole, asenda plokk viidatud tekstiga. Pildid on alati täies proportsioonis, mitte kaadrit täitvalt kärbitud.

Kaartide täpset liugülekatet mall ei paku: võrdluseks kasuta järjestikuseid pildiplokke ja kirjelda asukohaseost. Nii ei teki kontrollimata geomeetriast näilist täpsust.

## Kontroll enne üleandmist

- Ava genereeritud HTML töölaua- ja kitsas vaates. Kontrolli sisukorra ankruid, tabelite keritavust ja allikaviiteid.
- Vaata eriti lühivastust, ajajoont ja dokumentide ebakindluse märgendeid. Mall ei kontrolli ajalooliste väidete tõesust.
- Kontrolli kõiki pilte; puuduvat või valet pilti ei tohi asendada ajaloolise muljega illustratsiooniga.
- Printimisel kaob külgmenüü, tabelipäised korduvad ning allikate URL-id jäävad nähtavaks. Pika raporti PDF-i väljund kontrolli eraldi lehekülgede kaupa, kui PDF on tellitud.
- Genereerija kontrollib tundmatuid viiteid, korduvaid ID-sid, tabeli veergude arvu, URL-protokolli ja pildifaili vormingut. See ei taga raporti sisulist täielikkust.
