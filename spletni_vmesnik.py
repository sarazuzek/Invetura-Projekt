import bottle 
from model import Inventura

DATOTEKA_S_STANJEM = 'stanje.json'
try:
    inventura = Inventura.nalozi_stanje(DATOTEKA_S_STANJEM)
except:
    inventura = Inventura()


@bottle.get('/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', inventura=inventura, vse_OK=vse_OK, sporocilo=sporocilo)

@bottle.post('/dodaj_izdelek/')
def dodaj_izdelek():
    kategorija = bottle.request.forms["kategorija"]
    izdelek = bottle.request.forms["izdelek"]
    nabavna = float(bottle.request.forms["nabavna"])
    prodajna = float(bottle.request.forms["prodajna"])
    kolicina = int(bottle.request.forms["kolicina"])
    inventura.dodaj_izdelek(kategorija, izdelek, nabavna, prodajna, kolicina)
    bottle.redirect('/')

@bottle.post('/sestej/')
def sestej():
    global vse_OK, sporocilo
    kategorija = bottle.request.forms["kategorija_sestej"]
    izdelek = bottle.request.forms["izdelek_sestej"]
    try:
        inventura.sestej_kolicine(kategorija, izdelek)
        vse_OK = True
        sporocilo = "Vse štima."
    except ValueError:
        vse_OK = False
        sporocilo = "Izdelek {} iz {} je nekdo ukradel.".format(kategorija, izdelek)
    bottle.redirect('/')



vse_OK = None
sporocilo = ""


bottle.run(debug = True, reloader=True)
    