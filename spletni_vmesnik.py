import bottle 
import random
import os
from model import Inventura

inventure = {}

for ime_datoteke in os.listdir('shranjene_inventure'):
    st_uporabnika, koncnica = os.path.splitext(ime_datoteke)
    inventure[st_uporabnika] = Inventura.nalozi_stanje(os.path.join
    ('shranjene_inventure', ime_datoteke))

def inventura_uporabnika():
    st_uporabnika = bottle.request.get_cookie('st_uporabnika')
    if st_uporabnika is None:
        st_uporabnika = str(random.randint(0, 2 ** 40))
        inventure[st_uporabnika] = Inventura()
        bottle.response.set_cookie('st_uporabnika', st_uporabnika, path='/')
    return inventure[st_uporabnika]

def shrani_inventuro_uporabnika():
    st_uporabnika = bottle.request.get_cookie('st_uporabnika')
    inventura = inventure[st_uporabnika]
    inventura.shrani_stanje(os.path.join('shranjene_inventure', f'{st_uporabnika}.json'))

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/izdelki/')
   
@bottle.get('/izdelki/')
def vsi_izdelki():
    inventura = inventura_uporabnika()
    return bottle.template('izdelki.html', 
                        inventura=inventura, 
                        vse_OK=vse_OK, 
                        sporocilo=sporocilo)

@bottle.get('/racuni/')
def raucni():
    inventura = inventura_uporabnika()
    return bottle.template('racuni.html', inventura=inventura)

@bottle.get('/dobicek/')
def dobicek():
    inventura = inventura_uporabnika()
    return bottle.template('dobicek.html', 
                        inventura=inventura, 
                        sporocilo=sporocilo, 
                        dobicek_kat=dobicek_kat, 
                        dobicek_izd=dobicek_izd, 
                        celoten_dobicek=celoten_dobicek)

@bottle.get('/pomoc/')
def pomoc():
    return bottle.template('pomoc.html')

@bottle.post('/dodaj-izdelek/')
def dodaj_izdelek():
    inventura = inventura_uporabnika() 
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    nabavna = float(bottle.request.forms["nabavna"])
    prodajna = float(bottle.request.forms["prodajna"])
    kolicina = int(bottle.request.forms["kolicina"])
    inventura.dodaj_izdelek(kategorija, izdelek, nabavna, prodajna, kolicina)
    shrani_inventuro_uporabnika()
    bottle.redirect('/')

@bottle.post('/odstrani-izdelek/')
def odstrani_izdelek():
    inventura = inventura_uporabnika()
    kategorija = bottle.request.forms["kategorija"]
    ime = bottle.request.forms["ime"]
    inventura.odstrani_izdelek(kategorija, ime) 
    shrani_inventuro_uporabnika()
    bottle.redirect('/')

@bottle.post('/prenesi-izdelek/')
def prenesi_izdelek():
    inventura = inventura_uporabnika()
    kategorija1 = bottle.request.forms.getunicode("kategorija1")
    kategorija2 = bottle.request.forms.getunicode("kategorija2")
    izdelek = bottle.request.forms.getunicode("izdelek")
    inventura.prenesi_izdelek(kategorija1, kategorija2, izdelek)
    shrani_inventuro_uporabnika()
    bottle.redirect('/')

@bottle.post('/dodaj-racun/')  
def dodaj_racun():
    inventura = inventura_uporabnika()
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    kolicina = int(bottle.request.forms["kolicina"])
    popust = int(bottle.request.forms["popust"])
    inventura.dodaj_racun(kategorija, izdelek, kolicina, popust=popust)
    shrani_inventuro_uporabnika()
    bottle.redirect('/racuni/')

@bottle.post('/storniraj-racun/')
def storniraj_racun():
    inventura = inventura_uporabnika()
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    kolicina = int(bottle.request.forms["kolicina"])
    popust = int(bottle.request.forms["popust"])
    inventura.storniraj_racun(kategorija, izdelek, kolicina, popust)
    shrani_inventuro_uporabnika()
    bottle.redirect('/racuni/')

@bottle.post('/dodaj-inventuro/') 
def dodaj_inventuro():
    inventura = inventura_uporabnika()
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    kolicina = int(bottle.request.forms["kolicina"])
    inventura.dodaj_inventuro(kategorija, izdelek, kolicina)
    shrani_inventuro_uporabnika()
    bottle.redirect('/')

@bottle.post('/sestej/')
def sestej():
    inventura = inventura_uporabnika()
    global vse_OK, sporocilo
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    try:
        inventura.sestej_kolicine(kategorija, izdelek)
        vse_OK = True
        sporocilo = "Vse štima."
    except ValueError:
        vse_OK = False
        sporocilo = "Inventura za izdelek {} iz {} se ne ujema!".format(izdelek, kategorija)
    bottle.redirect('/izdelki/')

@bottle.post('/dobicek-izdelek/')  
def dobicek_izdelek():
    inventura = inventura_uporabnika()
    global dobicek_izd, sporocilo
    kategorija = bottle.request.forms.getunicode("kategorija")
    izdelek = bottle.request.forms.getunicode("izdelek")
    dobicek_izd = True
    dobicek_st = inventura.dobicek_na_izdelku(kategorija,izdelek)
    sporocilo = "Na izdelku {} v kategoriji {} smo zaslužili {} €".format(izdelek, kategorija, str(round(dobicek_st,2)))
    bottle.redirect('/dobicek/')

@bottle.post('/dobicek-kategorija/')
def dobicek_kategorija():
    inventura = inventura_uporabnika()
    global dobicek_kat, sporocilo
    kategorija = bottle.request.forms["kategorija"]
    dobicek_kat = True
    dobicek_st = inventura.dobicek_na_kategorijo(kategorija)
    sporocilo = "Na kategoriji {} smo zaslužili {} €".format(kategorija, str(round(dobicek_st,2)))
    bottle.redirect('/dobicek/')

@bottle.post('/celoten-dobicek/')
def celoten_dobicek():
    inventura = inventura_uporabnika()
    global celoten_dobicek, sporocilo
    dobicek = inventura.celoten_dobicek()
    celoten_dobicek = True
    sporocilo = "Celoten dobicek znaša {} €".format(dobicek)
    bottle.redirect('/dobicek/') 


vse_OK = None
sporocilo = ""
dobicek_kat = False
dobicek_izd = False
celoten_dobicek = False



bottle.run(debug = True, reloader=True)
    