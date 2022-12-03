PAKO-app (Pois Arjesta, Keskity Olennaiseen)

Sovellus yhteisiä tapahtumia varten.

Sovelluksen tarkoitus on antaa käyttäjälle mahdollisuus luoda ja osallistua yksityisten tai julkisten tapahtumien suunnitteluun.

Kuvaus sovelluksen lopputavoitteesta. Lopussa tilannekatsaus:

- Käyttäjä voi luoda tilin ja kirjautua profiiliinsa.
- Käyttäjän kirjauduttua sisään, tämä näkee tulevat tapahtumat (+ mm tietoa osallitujamäärästä, countdown-laskuri, muutoksia-ilmoitus).
- Julkisia tapahtumia voi selata listasta ja niitä voi seurata/liittyä mukaan, jolloin tapahtuma ilmestyy omalle etusivulle
- Julkisia tapahtumia voi tarkastella ilman sisään kirjautumista
- Yksityiseen tapahtumaan liitytään kutsukoodilla.
- Tapahtuman isännällä on mahdollisuus poistaa/blokata käyttäjiä sekä antaa/poistaa muokkausoikeuksia. Idea on kuitenkin se, että tapahtumien muokkaus olisi osallistujille avointa.

- Tapahtuman etusivu näyttää mm. tapahtuman nimen ja kuvauksen, osallistujalistan, countdownin, sijainnin sekä dynaamisen suunnitteluosion josta lisää seuraavissa kohdissa
- Äänestykset: käyttäjä voi luoda ehdotuksen tms, ja kaikki käyttäjät voivat antaa ehdotuksella äänensä. Eniten ääniä saaneet ehdotukset nousevat listassa ylös. Äänet ovat nimettömiä.
- Askareet: tapahtuman järjestämiseen tai tapahtuman aikasten tehtävien hoitoon tarkoitettu osio. Askareen kohdalle voi ilmoittautua, tai askareet voidaan arpoa osallistujien kesken.
- Hankinta-/tarve-/ostoslista: Lista tarpeista. Checkbox hoidettua kohtaa varten. 
- Chat: yksinkertainen vapaa keskusteluikkuna
- Muita ominaisuuksia lisätään mahdollisuuksien mukaan

Sovellus soveltuu esimerkiksi juhlien, matkojen, keikkojen tai urheilutapahtumien yhteisorganisointiin.


### (Välipalautus 2 tilanne (20.11.2022): 
### Sovelluksen pohjatyö on pääosin valmis. Tiedostorakenne on kesken. Tietokantaoperaatiot ja ohjelmalogiikka on tarkoitus siirtää omiin tiedostoihinsa seuraavassa vaiheessa. Tietokantatauluja on vasta kaksi: users ja events. Lisää tauluja luodaan seuraavassa vaiheessa. Pylintia ei olla vielä otettu käyttöön.

### Tässä vaiheessa käyttäjä voi nähdä luodut tapahtumat, luoda käyttäjätunnuksen, kirjautua sisään ja ulos, sisäänkirjautuneena luoda tapahtuman ja antaa tapahtumalle nimen ja kuvauksen. Sovellusta pääsee kokeilemaan osoitteessa https://tsoha-pako.fly.dev ja koodia voi tarkastella githubissa https://github.com/aleksiskela/tsoha-pako.)


Välipalautus 3 tilanne (4.12.2022):
Sovellus on olennaisimmilta osiltaan valmis. Käyttäjä voi nyt luoda tilin, tapahtumia (julkisia tai yksityisiä), osallistua tapahtumaan, osallistua äänestyksiin, osallistua tehtävien luontiin ja jakoon ja kirjoittaa viestejä keskusteluun. 

Sovelluksessa on käytössä seitsemän tietokantataulua: users, events, messages, votables, votes, tasks ja enrolments.

Tietoturva on toteutettu kurssin ohjeiden mukaisesti. 

Lopuksi tullaan vielä muokkaamaan ulkoasua, etusivun rakennetta, mahdollistamaan käyttäjätunnuksen poistaminen, salasanan vaihtaminen, äänestysten ja tehtävien poistaminen. Muita ominaisuuksia ja muutoksia palautteen ja ajan mukaan.

Sovellusta pääsee testaamaan osoitteessa https://tsoha-pako.fly.dev ja koodia voi tarkastella githubissa https://github.com/aleksiskela/tsoha-pako.)