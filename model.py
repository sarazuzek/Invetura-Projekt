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
        self._ze_dodano(kategorija, ime)
        self.izdelki[(kategorija, ime)] = (nabavna_cena, prodajna_cena, kolicina)
    
    def _ze_dodano(self, kategorija, ime):
        if (kategorija, ime) in self.izdelki:
            raise ValueError(f'Izdelek {ime} pod kategorijo {kategorija} že obstaja!')

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
        raise ValueError(f'{ime} ni v kategoriji {kategorija}.')

    def prenesi_izdelek(self, kategorija1, kategorija2, ime):
        self._preveri_izdelek_v_kategoriji(ime, kategorija1)
        if ime in self.kategorije[kategorija2]:
            raise ValueError(f'Izdelek je že v kategoriji {kategorija2}!')
        izdelek = self.kategorije[kategorija1]
        self.kategorije[kategorija2].append(izdelek)
        self.kategorije[kategorija1].remove(izdelek)
        del self.izdelki[(kategorija1, ime)]
        self.izdelki[(kategorija2, ime)] = (kategorije[kategorija1][1], kategorije[kategorija1][2], kategorije[kategorija1][3])  

    def _preveri_izdelek_v_kategoriji(self, izdelek, kategorija):
        if izdelek not in self.kategorije[kategorija]:
            raise ValueError(f'{izdelek} ni v kategoriji {kategorija}')

    def dodaj_racun(self, kategorija, izdelek, kolicina, popust=0, prodaj_po_nabavni=False):
        if type(kolicina) != int  or  type(popust) != int:
            raise TypeError('Količina in popust morata biti celo število')
        self._preveri_izdelek(kategorija, izdelek)
        prodajna_cena = izdelki[(kategorija, izdelek)][1]
        skupna_vrednost = kolicina * prodajna_cena * (1 - popust / 100)
        if (kategorija, izdelek) in self.vsi_racuni:
            self.vsi_racuni[(kategorija, izdelek)].append((kolicina, skupna_vrednost))
        self.vsi_racuni[(kategorija, izdelek)] = (kolicina, skupna_vrednost)

    def storniraj_racun(self, kategorija, izdelek, popravljna_kolicina, popravljena_cena):
        if (kategorija, izdelek) in self.vsi_racuni:
            self.vsi_racuni.pop((kategorija, izdelek))
            self.vsi_racuni[(kategorija, izdelek)].append((popravljena_kolicina * popravljena_cena))
        raise ValueError(f'Izdelka {izdelek} ni med računi!')

    def dodaj_inventuro(self, kategorija, izdelek, kolicina):
        self._preveri_izdelek(kategorija, izdelek)
        self._ze_dodani_izdelki(kategorija, izdelek)
        self.inventura[(kategorija, izdelek)] = kolicina

    def _preveri_izdelek(self, kategorija, izdelek):
        if (kategorija, izdelek) not in self.izdelki:
            raise ValueError('Željeni izdelek ne obstaja, inventura/dodajanje računa zanj ni mogoča/e!')

    def _ze_dodani_izdelki(self, kategorija, izdelek):
        if (kategorija, izdelek) in self.inventura:
            raise ValueError(f'Izdelek {izdelek}, je že v inventuri!')

     def sestej_kolicine(self, kategorija, izdelek):
        self._preveri_(kategorija, izdelek)
        inventura = self.inventura[(kategorija, izdelek)]
        racuni = self._kolicina_prodanih_izdelkov(kategorija, izdelek)
        na_zacetku = self.izdelki[(kategorija, izdelek)][2]
        if invetura + racuni != na_zacetku:
            raise ValueError(f'Pri izdelku {izdelek} se nekaj ne ujema!')
    
    def _preveri_(self, kategorija, izdelek):
        self._preveri_izdelek(kategorija, izdelek)
        self._preveri_racune(kategorija, izdelek)
        self._preveri_inventuro(kategorija, izdelek)

    def _preveri_racune(self, kategorija, izdelek):
        if (kategorija, izdelek) not in self.vsi_racuni:
            raise ValueError('Željnega izdelka še ni med računi!')
    
    def _preveri_inventuro(self, kategorija, izdelek):
        if (kategorija, izdelek) not in self.inventura:
            raise ValueError('Željenga izdelka še ni v inventuri!')

    def _kolicina_prodanih_izdelkov(self, kategorija, izdelek):
        vsota = 0
        for v in self.vsi_racuni[(kategorija, izdelek)][::2]:
            vsota += v
        return vsota
            
    def dobicek_na_izdelku(self, kategorija, izdelek):
        self._preveri_(kategorija, izdelek)
        nabavna_cena = self.izdelki[(kategorija, izdelek)][0]
        zacetek = self._stanje_zacetek(kategorija, izdelek)
        prodaja = self._zasluzek_prodaja(kategorija, izdelek)
        konec = self.inventura[(kategorija, izdelek)] * nabavna_cena
        dobicek = prodaja + konec - zacetek

    def _zasluzek_prodaja(self, kategorija, izdelek):
        vsota = 0
        for v in self.vsi_racuni[(kategorija, izdelek)][1::2]:
            vsota +=v
        return vsota

    def _stanje_zacetek(self, kategorija, izdelek):
        nabavna_cena = self.izdelki[(kategorija, izdelek)][0]
        kolicina = self.izdelki[(kategorija, izdelek)][2]
        return stanje_na_zacetku == nabavna_cena * kolicina

    def dobicek_na_kategorijo(self, kategorija):
        if kategorija not in self.kategorije:
            raise ValueError('Ta kategorija ne obstaja!')
        for v in self.kategorije[kategorija][::4]: 
            dobicek += self.dobicek_na_izdelku(kategorija, v)
        return dobicek

    def celoten_dobicek(self):
        dobicek = 0
        for k in self.kategorije.keys():
            dobicek += self.dobicek_na_kategorijo(v)
        return dobicek






