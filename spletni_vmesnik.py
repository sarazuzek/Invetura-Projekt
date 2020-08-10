import bottle 
from model import Inventura

DATOTEKA_S_STANJEM = 'stanje.json'
try:
    inventura = Inventura.nalozi_stanje(DATOTEKA_S_STANJEM)
except:
    inventura = Inventura()


@bottle.get('/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', 
                        inventura=inventura, 
                        vse_OK=vse_OK, 
                        sporocilo=sporocilo,
                        dobicek_kat=dobicek_kat,
                        dobicek_izd=dobicek_izd,
                        celoten_dobicek=celoten_dobicek
                        )

@bottle.post('/dodaj-izdelek/')
def dodaj_izdelek():
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    nabavna = float(bottle.request.forms["nabavna"])
    prodajna = float(bottle.request.forms["prodajna"])
    kolicina = int(bottle.request.forms["kolicina"])
    inventura.dodaj_izdelek(kategorija, izdelek, nabavna, prodajna, kolicina)
    bottle.redirect('/')

@bottle.post('/odstrani-izdelek/')
def odstrani_izdelek():
    kategorija = bottle.request.forms["kategorija"]
    ime = bottle.request.forms["kategorija"]
    inventura.odstrani_izdelek(kategorija, ime) 
    bottle.redirect('/')

@bottle.post('/prenesi-izdelek/')
def prenesi_izdelek():
    kategorija1 = bottle.request.forms["kategorija1"]
    kategorija2 = bottle.request.forms["kategorija2"]
    izdelek = bottle.request.forms["izdelek"]
    inventura.prenesi_izdelek(kategorija1, kategorija2, izdelek)
    bottle.redirect('/')


@bottle.post('/dodaj-racun/')  
def dodaj_racun():
    kategorija = bottle.request.forms.getunicode("kategorija_racun")
    izdelek = bottle.request.forms.getunicode("izdelek_racun")
    kolicina = int(bottle.request.forms["kolicina_racun"])
    popust = int(bottle.request.forms["popust"])
    inventura.dodaj_racun(kategorija, izdelek, kolicina, popust=popust)
    bottle.redirect('/')

@bottle.post('/storniraj-racun/')
def storniraj_racun():
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    kolicina = int(bottle.request.forms["kolicina"])
    popust = int(bottle.request.forms["popust"])
    inventura.storniraj_racun(kategorija, izdelek, kolicina, popust)
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

@bottle.post('/dobicek-izdelek/')  
def dobicek_izdelek():
    global dobicek_izd, sporocilo
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    dobicek_izd = True
    dobicek_st = inventura.dobicek_na_izdelku(kategorija,izdelek)
    sporocilo = "Na izdelku {} v kategoriji {} smo zaslužili {} €".format(izdelek, kategorija, str(round(dobicek_st,2)))
    bottle.redirect('/')

@bottle.post('/dobicek-kategorija/')
def dobicek_kategorija():
    global dobicek_kat, sporocilo
    kategorija = bottle.request.forms["kategorija"]
    dobicek_kat = True
    dobicek_st = inventura.dobicek_na_kategorijo(kategorija)
    sporocilo = "Na kategoriji {} smo zaslužili {} €".format(kategorija, str(round(dobicek_st,2)))
    bottle.redirect('/')

@bottle.post('/celoten-dobicek/')
def celoten_dobicek():
    global celoten_dobicek, sporocilo
    dobicek = inventura.celoten_dobicek()
    celoten_dobicek = True
    sporocilo = "Celoten dobicek znaša {} €".format(dobicek)
    bottle.redirect('/') 


vse_OK = None
sporocilo = ""
dobicek_kat = False
dobicek_izd = False
celoten_dobicek = False



bottle.run(debug = True, reloader=True)
    