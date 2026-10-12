# Näidise üldistatud õppetunnid ja kontrollstsenaariumid

Oskus on tuletatud kohalooraporti nähtavast ülesehitusest ja allikakasutusest. Lähteraporti juhtumiandmeid ega privaatseid linke siin ei säilitata. Malli näide „Ranniku talu (endine Lepiku talu), Saluoja küla“ ning selle inimesed, daatumid ja allikakirjed on väljamõeldud. Võimalik nimekattuvus on juhuslik. See fail on arendusmaterjal, mitte tavauurimisel kohustuslik lisakontekst.

## Avalikud metoodikaallikad

- [VAU](https://www.ra.ee/vau/), [kohaajaloo juhend](https://www.ra.ee/vau/index.php/et/page/article/index?menuId=3), [kinnistute ja hoonete juhend](https://www.ra.ee/vau/index.php/et/page/article/index?menuId=4), [lugemine ja tõlkimine](https://www.ra.ee/vau/index.php/et/page/article/index?menuId=32).
- [RA Transkribuse teave](https://rahvusarhiiv.transkribus.eu/about): katvuse ja tuvastuse piirangud.

Need on tegelikud juhendiviited. Uurimise ajal kontrolli nende ajakohasust. Malli `example.invalid`-lingid seevastu on kohatäitjad ega avane.

## Mida saab väljundist tuletada

Nähtavast raportist saab tuletada allikate tööjaotuse, raporti struktuuri, käsikirjalugemise vajaduse ning võimalikke otsinguvigu. Teenuse sisemist prompti, API-sid, mudelijaotust, tokenikulu ega täpset otsingujärjekorda ei saa usaldusväärselt taastada. Ära eelda ligipääsu teenuse andmekoopiale või sisemistele tööriistadele.

Lühike nimepõhine sisend võib vajada asukoha täpsustamist. Kasutaja antud katastritunnus ja eriküsimused lisa uurimisplaani, kuid ära tuleta iga uue koha jaoks eelmise juhtumi küsimusi.

## Üldistatavad töövõtted

| Võimalik olukord | Töövõte |
|---|---|
| Esialgne ajaloolise valla oletus osutub valeks | Kontrolli halduskuuluvust uuritava aasta ja koha kohta; postiaadressist ei piisa |
| Hõre kaadrivalim jätab otsitava lehe vahele | Valim aitab leida struktuuri, mitte tõendada puudumist; asjakohane lõik kontrolli järjest |
| Mitmeleheküljeline dokument on ainult osaliselt loetud | Leiu leidmine ja lõpetatud lugemine on eri etapid; nimeta lugemata osad |
| Kataloogikoopias puudub digimärge, kuid köide avaneb | Kontrolli värsket digipildi olekut; erista kirjeldust ja tegelikku ligipääsu |
| Lehtede järjekorda oletatakse geograafiliseks | Kontrolli juhendit ja köite struktuuri; talundilehtede suurusrühmad võivad olla otsustavad |
| Küla vanim teade kantakse üle talu vanusele | Talu vanusele on vaja talu enda tõendit |
| Plaani dateering, allkirjad ja oletatud ostuaasta liidetakse | Lahuta mõõdistamise, allkirjastamise ja ostu kuupäevad |
| Viide viib ainult säiliku või otsinguni | Säilita ka originaalleht/kaader ning eelista konkreetset kirjet |
| Käsikirjalõikel puuduvad veerupäised | Kontrolli terviklehe konteksti ning säilita ebakindlus ka jutustuses |

Need õppetunnid ei kinnita ühegi konkreetse talu ajalugu. Väljamõeldud näite leidandmeid ei tohi kasutada päris otsingute lähtepunktina.

## Läbimängimise stsenaariumid

Need stsenaariumid ei tõenda iseenesest praktilist OCR/HTR täpsust ega eurokulu.

1. **„Ranniku talu, Saluoja küla — ajalugu“, mitu samanimelist kohta.** Töö algab koha samastamisest ja küsib vajaliku asukoha; eri valdade peresid ei ühendata.
2. **AISis puudub digimärge, Saaga näitab sisselogimist.** Seisuks jääb ligipääsu vajadus; „digiteerimata“ järeldust ei tehta. Avalik eeltöö jätkub.
3. **Otsitav leht jäi hõreda kaadrivalimi vahele.** Otsitakse nimekirja, jaoskonda ja suurusrühma, kontrollitakse asjakohast lõiku järjest. Valimist ei järeldata puudumist.
4. **Kuupäevaga rida on lõigatud ilma päisteta.** Enne väite tegemist hangitakse päis ja kontekst. Selge number ei tõenda selle tähendust.
5. **Mälestus ja selle ajaleheümbertrükk kattuvad.** Neid ei loeta kaheks sõltumatuks kinnituseks; põhjuslik väide jääb vajadusel oletuseks.
6. **Vanus ja sünnikanne ei klapi.** Mõlemad säilitatakse, kontrollitakse isikut ja veerge; puuduv lahendus esitatakse vastuoluna.
7. **Fiktiivne 1936. aasta majapidamisleht on leitud, kuid ainult esikülg loetud.** Hoonete ja elanike andmeid ei oletata; jätkatakse ülejäänud külgedega või nimetatakse täpne piirang. See vorminäide ei muuda tegelike ajalooliste loenduste aastaarve.
8. **Kasutaja kulu- või ajapiir täitub.** Säilivad päevik, kontrollitud raport ja jätkamiskoht; kvaliteeti ei asendata kindlama sõnastusega.
9. **Kaardivõrdluseks puudub usaldusväärne joondus.** Koostatakse märgistatud kõrvutus, mitte näiliselt täpne liugülekate.
10. **Uus tõend parandab ajaloolise valla.** Parandatakse kõik sõltuvad peatükid ja otsinguplaan, mitte ainult lõpu märkus.
