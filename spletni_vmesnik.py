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

@bottle.post('/dodaj-izdelek/')
def dodaj_izdelek():
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    nabavna = float(bottle.request.forms["nabavna"])
    prodajna = float(bottle.request.forms["prodajna"])
    kolicina = int(bottle.request.forms["kolicina"])
    inventura.dodaj_izdelek(kategorija, izdelek, nabavna, prodajna, kolicina)
    bottle.redirect('/')

@bottle.post('/dodaj-racun/')  #ne doda med račune
def dodaj_racun():
    kategorija = bottle.request.forms.getunicode("kategorija_racun")
    izdelek = bottle.request.forms.getunicode("izdelek_racun")
    kolicina = int(bottle.request.forms["kolicina_racun"])
    popust = float(bottle.request.forms["popust"])
    inventura.dodaj_racun(kategorija, izdelek, kolicina, popust=0, prodaj_po_nabavni=False)
    bottle.redirect('/')

@bottle.post('/dodaj-inventuro/') 
def dodaj_inventuro():
    kategorija = bottle.request.forms.getunicode("kategorija_inv")
    izdelek = bottle.request.forms.getunicode("izdelek_inv")
    kolicina = int(bottle.request.forms["kolicina_inv"])
    inventura.dodaj_inventuro(kategorija, izdelek, kolicina)
    bottle.redirect('/')

@bottle.post('/sestej/')
def sestej():
    global vse_OK, sporocilo
    kategorija = bottle.request.forms.getunicode("kategorija_sestej")
    izdelek = bottle.request.forms.getunicode("izdelek_sestej")
    try:
        inventura.sestej_kolicine(kategorija, izdelek)
        vse_OK = True
        sporocilo = "Vse štima."
    except ValueError:
        vse_OK = False
        sporocilo = "Inventura za izdelek {} iz {} se ne ujema!".format(izdelek, kategorija)
    bottle.redirect('/')


vse_OK = None
sporocilo = ""


bottle.run(debug = True, reloader=True)
    