import json

class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, inventura):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.inventura = inventura

    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Vnesli ste napačno geslo. Poizkusite znova.')

    def shrani_stanje(self, ime_datoteke):
        slovar_stanja = {
            'uporabnisko_ime' : self.uporabnisko_ime,
            'zasifrirano_geslo' : self.zasifrirano_geslo
            'inventura' : self.inventura.slovar_s_stanjem()
        }
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            json.dump(slovar_stanja, datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_stanja = json.load(datoteka)
        uporabnisko_ime = slovar_stanja['uporabnisko_ime']
        zasifrirano_geslo = slovar_stanja['zasifrirano_geslo']
        inventura = Inventura.nalozi_iz_slovarja(slovar_stanja['inventura'])
        return cls(uporabnisko_ime, zasifrirano_geslo, inventura)


class Inventura: 
    def __init__(self):
        self.inventura = {}
        self.vsi_racuni = {}
        self.izdelki = {} #slovar bo izgledal takole: self.izdelki = {("kat", "ime"): (nab, prod, kolicina)}

    def dodaj_izdelek(self, kategorija, ime, nabavna_cena, prodajna_cena, kolicina):
        try:
            int(nabavna_cena)
            int(prodajna_cena)
        except:
            raise TypeError('Vnesli ste napačen tip!') 
        if nabavna_cena > prodajna_cena:
            raise TypeError('Nabavna cena na more biti večja od prodajne cene!')
        if type(kolicina) != int:
            raise TypeError('Količina mora biti celo število!')
        if (kategorija, ime) in self.izdelki:
            self.izdelki[(kategorija, ime)][2] += kolicina
        else:
            self.izdelki[(kategorija, ime)] = (nabavna_cena, prodajna_cena, kolicina)
            #print('Dodajam novo kategorijo:', kategorija)

    def izdelki_po_kategorijah(self):   
        kategorije = {}
        for k,v in self.izdelki.items():
            kategorija = k[0]
            ime = k[1]
            nabavna_cena = v[0]
            prodajna_cena = v[1]
            kolicina = v[2]
            kategorije[kategorija] = (ime, nabavna_cena, prodajna_cena, kolicina)
        return kategorije

    def odstrani_izdelek(self, kategorija, ime):
        if (kategorija, ime) in self.izdelki:
            del self.izdelki[(kategorija, ime)]
        else:
            raise ValueError(f'{ime} ni v kategoriji {kategorija}.')

    def prenesi_izdelek(self, kategorija1, kategorija2, ime): #prenesli bomo iz kategorije1 v kategorijo2
        kategorije = self.izdelki_po_kategorijah()
        self._preveri_izdelek_v_kategoriji(ime, kategorija1, kategorije) #vrne error, če izdelka ni v kategoriji1
        self._preveri_izdelek_v_kategoriji(ime, kategorija2, kategorije) #vrne error, če je izdelek že v kategoriji2
        del self.izdelki[(kategorija1, ime)]
        nabavna_cena = kategorije[kategorija1][1]
        prodajna_cena = kategorije[kategorija1][2]
        kolicina = kategorije[kategorija1][3]
        self.izdelki[(kategorija2, ime)] = (nabavna_cena, prodajna_cena, kolicina)  

    def _preveri_izdelek_v_kategoriji(self, ime, kategorija, kategorije):
        if ime not in kategorije[kategorija]:
            raise ValueError(f'{ime} ni/je že v kategoriji {kategorija}!')

    def dodaj_racun(self, kategorija, izdelek, kolicina, popust=0, prodaj_po_nabavni=False):
        self._preveri_stevilke(kolicina, popust)
        self._preveri_izdelek(kategorija, izdelek, kolicina) #vrne error če izdelk ni ali ga ni dovolj na zalogi
        nabavna_cena = izdelki[(kategorija, izdelek)][0]
        prodajna_cena = izdelki[(kategorija, izdelek)][1]
        if prodaj_po_nabavni:
            skupna_vrednost = kolicina * nabavna_cena
        else:
            skupna_vrednost = kolicina * prodajna_cena * (1 - popust / 100)
        if (kategorija, izdelek) in self.vsi_racuni:
            self.vsi_racuni[(kategorija, izdelek)].append((kolicina, skupna_vrednost))
        self.vsi_racuni[(kategorija, izdelek)] = [(kolicina, skupna_vrednost)]
        self.izdelki[(kategorija, izdelek)][2] -= kolicina

    def _preveri_stevilke(self, kolicina, popust=0):
        if type(popust) != int:
            raise TypeError('Popust mora biti celo število!')
        if type(kolicina) != int:
            raise TypeError('Količina mora biti celo število večje ali enako 0!')
        if not (0 <= popust <= 100):
            raise ValueError('Popust mora biti celo število med 0 in 100!')
        if not (0 < kolicina):
            raise ValueError('Količina mora biti celo število večje ali enako 0!')

    def _preveri_izdelek(self, kategorija, izdelek, kolicina=0):
        if (kategorija, izdelek) not in self.izdelki:
            raise ValueError('Željeni izdelek ne obstaja, inventura/dodajanje računa zanj ni mogoča/e!')
        zaloga = self.izdelki[(kategorija, izdelek)][2]
        if kolicina > zaloga:
            raise ValueError(f'Ni dovolj zaloge za izdelek {izdelek}.')

    def storniraj_racun(self, kategorija, izdelek, popravljna_kolicina, popravljena_popust=0):
        #ta funkcija popravi zadnji vnešen račun za izdelek v kategoriji (če se zmotiš pri vnosu)
        if (kategorija, izdelek) in self.vsi_racuni:
            self.vsi_racuni[(kategorija, izdelek)].pop()
        else:
            raise ValueError(f'Izdelka {izdelek} ni med računi!')
        self.dodaj_racun(kategorija, izdelek, popravljna_kolicina, popravljen_popust)
        
    def dodaj_inventuro(self, kategorija, izdelek, kolicina):
        self._preveri_izdelek(kategorija, izdelek) #preveri ali izdelek obstaja na seznamu vseh izdelkov
        self._ze_dodani_izdelki(kategorija, izdelek) #preveri ali je inventura že bila dodana
        self.inventura[(kategorija, izdelek)] = kolicina

    def _ze_dodani_izdelki(self, kategorija, izdelek):
        if (kategorija, izdelek) in self.inventura:
            raise ValueError(f'Izdelek {izdelek}, je že v inventuri!')

     def sestej_kolicine(self, kategorija, izdelek):
        self._preveri_(kategorija, izdelek)
        inventura = self.inventura[(kategorija, izdelek)]
        na_zacetku = self.izdelki[(kategorija, izdelek)][2]
        if invetura != na_zacetku:
            raise ValueError(f'Pri izdelku {izdelek} se nekaj ne ujema!')
    
    def _preveri_(self, kategorija, izdelek):
        self._preveri_izdelek(kategorija, izdelek)
        self._preveri_inventuro(kategorija, izdelek)
    
    def _preveri_inventuro(self, kategorija, izdelek):
        if (kategorija, izdelek) not in self.inventura:
            raise ValueError(f'Izdelka {izdelek} še ni v inventuri!')

    def dobicek_na_izdelku(self, kategorija, izdelek):
        self._preveri_(kategorija, izdelek)
        prodaja = self._zasluzek_prodaja(kategorija, izdelek) #dobiček od prodaje izdelka
        nabavna_cena = self.izdelki[(kategorija, izdelek)][0]
        kolicina = self._kolicina_prodanih_izdelkov(kategorija, izdelek) #število prodanih izdelkov
        placano = kolicina * nabavna_cena 
        dobicek = prodaja - placano

    def _zasluzek_prodaja(self, kategorija, izdelek):
        vsota = 0
        for racun in self.vsi_racuni[(kategorija, izdelek)]:
            vrednost = racun[1]
            vsota += vrednost
        return vsota

    def _kolicina_prodanih_izdelkov(self, kategorija, izdelek):
        vsota = 0
        for racun in self.vsi_racuni[(kategorija, izdelek)]:
            kolicina = racun[0]
            vsota += kolicina
        return vsota

    def dobicek_na_kategorijo(self, kategorija):
        kategorije = self.izdelki_po_kategorijah()
        if kategorija not in kategorije:
            raise ValueError(f'Kategorija {kategorija} ne obstaja!')
        dobicek = 0
        for izdelek in kategorije[kategorija]:
            ime_izdelka = izdelek[0]
            dobicek += self.dobicek_na_izdelku(kategorija, ime_izdelka)
        return dobicek

    def celoten_dobicek(self):
        dobicek = 0
        kategorije = self.izdelki_po_kategorijah()
        for kategorija in kategorije.keys():
            dobicek += self.dobicek_na_kategorijo(kategorija)
        return dobicek






