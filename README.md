Tietokantasovellus: PAKO-app (Pois Arjesta, Keskity Olennaiseen)

Eskapistinen sovellus tapahtumien kollektiiviseen järjestämiseen, jossa kirjautunut käyttäjä voi olla osana tapahtuman järjestämistä. Osallistuessaan tapahtumaan, käyttäjä voi ottaa osaa keskusteluun, äänestyksiin ja suoritettavien tehtävien jakoon. 

Sovellus on testattavissa osoitteessa https://tsoha-pako.fly.dev ja koodia voi tarkastella GitHubissa osoitteessa https://github.com/aleksiskela/tsoha-pako.

Kuvaus sovelluksen keskeisimmistä toiminnoista:
- Käyttäjä voi luoda tilin sekä kirjautua sisään ja ulos
- Käyttäjä voi luoda itse tapahtumia (event) tai osallistua (enrol) muiden luomiin tapahtumiin
    - Tapahtuman luoja/järjestäjä voi muokata perustietoja, poistaa tapahtuman, muuttaa osallistujan muokkausoikeuksia, poistaa äänestyksiä ja poistaa tehtäviä.
    - Tapahtuman vieras voi osallistua keskusteluun ja poistaa omia viestäjään, luoda äänestyskohteita ja äänestää, luoda tehtäviä ja osallistua niiden jakamiseen.
- Tapahtumalle voidaan antaa nimi, kuvaus, aikataulu, paikkatieto sekä määrittää tapahtuma yksityiseksi, jolloin tapahtumalle voi määrittää yksityisen kutsukoodin.
- Yksityinen tapahtuma ei näy etusivun Julkiset tapahtumat-osiossa vaan on löydettävissä kutsukoodin avulla
- Keskustelu (messages) on yksinkertainen html-chat.
- Äänestys (voting):
    - Äänestyskohteille voidaan antaa puoltava tai vastustava ääni. Ääntä voi muuttaa.
    - Suosituimmat kohteet näytetään ylimpänä.
- Tehtävät (tasks):
    - Tehtävään voi ilmoittautua vapaaehtoiseksi tai perääntyä tehtävästä
    - Tehtävät voidaan myös jakaa satunnaisesti. Valittavissa on jakaa täyttämättömät tehtävät tai jakaa kaikki.
    - Satunnaisjako jakaa tehtävät tasan kaikkien osallistujien kesken.

Kuvaus keskeisimmistä sivupohjista:
- Vasemman yläkulman "Home"-linkki johtaa aina etusivulle.
- Etusivulla käyttäjä näkee tulevat tapahtumat. Tapahtumat on jaettu käyttäjän perustamiin, käyttäjän osallistumiin ja julkisiin tapahtumiin. Menneisiin tapahtumiin johtava linkki löytyy sivun lopusta. Lisäksi käyttäjä voi syöttää yksityisen tapahtuman kutsukoodin hakukenttään, jonka kautta käyttäjä löytää muuten näkymättömän yksityisen tapahtuman.
- Tapahtuman-sivulla käyttäjä voi navigoida eri toimintojen välillä. Oletuksena oleva Tiedot-sivu näyttää tapahtuman perustiedot ja osallistujat sekä mm. countdown laskurin tapahtumaan.

Sovelluslogiikka keskittyy routes.py-moduuliin, joka käsittelee tietoa sivupohjien ja tietokannan välillä. Tietokanta koostuu seitsemästä tietokantataulusta, joita käsitellään erillisissä moduuleissa. Tietokanta määritellään db.py-moduulissa. Sovelluksen tietoturva-asiat on toteutettu kurssin ohjeiden mukaisesti. 

Sovelluksen ulkoasu on viimeistelty static/main.css-tiedostossa. Ulkoasun suunnittelussa on panostettu mobiili-versioon. Etusivun PAKO-logo on luotu OpenAI:n DALL-E 2-palvelun avulla (https://openai.com/dall-e-2/). DALL-E:n Terms of Use myöntää oikeuden sen tuottamien kuvien käyttämiseen omissa projekteissa (https://openai.com/terms/).

Lopuksi vielä seuraavia mahdollisia välittömiä askeleita sovelluksen kehityksessä:
- Käyttäjätunnuksen poistaminen
- Salasanan vaihtaminen sekä menetelmä unohtuneen salasanan palauttamiselle
- Yksityisen tapahtuman rajaus siten, että vain perustaja, osallistujat ja kutsukoodin syöttäneet voivat nähdä tapahtuman. Nykyisessä versiossa käyttäjä pääsee yksityiseen tapahtumaan url-kentän kautta, mikä tulisi estää.
- Perustajalle/järjestäjälle mahdollisuus estää osallistuja
- Useita ulkoasu-parannuksia, mm. taulukoiden ulkoasu.
- Koodin refaktorointi. Turhaa koodia on kertynyt oppimisprosessin myötä ja esimerkiksi routes.py on kasvanut liian laajaksi ja voisi näin ollen olla jaettavissa useammaksi tiedostoksi.
