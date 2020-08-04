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
        self.zacetno_stanje = []
        self.kategorije = []
        self.izdelki = []
        self.inventura = {}
        self.vsi_racuni = {}
        self.izdelki_v_kategoriji = {}
        self._izdelki_po_imenih = {}
        self._kategorije_po_imenih = {}

    def dodaj_izdelke(self, ime, nabavna_cena, prodajna_cena, kolicina):
        if ime in self._izdelki_po_imenih:
            raise ValueError('Izdelk s tem imenom že obstaja!')
        nov = Izdelek(ime, nabavna_cena, prodajna_cena, kolicina, self)
        self.izdelki.append(nov)
        self._izdelki_po_imenih[ime] = nov
        return nov

    def dodaj_kategorijo(self, kategorija):
        if ime in self._kategorije_po_imenih:
            raise ValueError('Kategorija s tem imenom že obstaja!')
        nova = Kategorija(ime, self)
        self.izdelki.append(nov)
        self._izdelki_po_imenih[ime] = nov
        return nov

    def dodaj_izdelek_v_kategorijo(self, izdelek, kategorija):
        if izdelek in self.izdelki_v_kategoriji[kategorija]:
            raise ValueError(f'{izdelek} je že v kategoriji {kategorija}!')
        self.izdelki_v_kategoriji[kategorija].append(izdelek)

    def odstrani_kategorijo(self, kategorija):
        self._preveri_kategorijo(kategorija)
        self.kategorije.remove(kategorija)
        del self.izdelki_v_kategoriji[kategorija]

    def _preveri_kategorijo(self, kategorija):
        if self.izdelki_v_kategoriji[kategorija] is not None:
            raise ValueError('Kategorije ne morete odstraniti, saj so v njej izdelki')

    def prenesi_izdelek(self, kat1, kat2, izdelek):
        self._preveri_izdelek_v_kategoriji(izdelek, kat1)
        if izdelek in self.izdelki_v_kategoriji[kat2]:
            raise ValueError(f'izdelek je že v kategoriji {kat2}!')
        self.izdelki_v_kategoriji[kat2].append(izdelek)
        self.izdelki_v_kategoriji[kat1].remove(izdelek)

    def _preveri_izdelek_v_kategoriji(self, izdelek, kategorija):
        if izdelek not in self.izdelki_v_kategoriji[kategorija]:
            raise ValueError(f'{izdelek} ni v kategoriji {kategorija}')

    #def dodaj_racun

    #def popravi_racun

    #def dodaj_inventuro

class Izdelek:
    def __init__(self, ime, nabavna_cena, prodajna_cena, kolicina):
        self.ime = ime
        self.nabavna_cena = nabavna_cena
        self.prodajna_cena = prodajna_cena
        self.kolicina = kolicina

class Kategorija:
    def __init__(self, ime):
        self.ime = ime

class Racun:
    def __init__(self, izdelek, kolicina, cena):
        self.izdelek = izdelek
        self.kolicina = kolicina
        self.cena = cena





