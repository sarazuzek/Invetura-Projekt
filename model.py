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

    def dodaj_izdelke(self, kategorija, ime, nabavna_cena, prodajna_cena, kolicina):
        if (kategorija, ime) in self.izdelki:
            raise ValueError('Ta izdelek pod to kategorijo je že dodan!')
        self.izdelki[(kategorija, ime)] = (nabavna_cena, prodajna_cena, kolicina)

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

    # def dodaj_kategorijo(self, kategorija):
    #     if ime in self._kategorije_po_imenih:
    #         raise ValueError('Kategorija s tem imenom že obstaja!')
    #     nova = Kategorija(ime, self)
    #     self.izdelki.append(nov)
    #     self._izdelki_po_imenih[ime] = nov
    #     return nov

    # def dodaj_izdelek_v_kategorijo(self, izdelek, kategorija):
    #     if izdelek in self.izdelki_v_kategoriji[kategorija]:
    #         raise ValueError(f'{izdelek} je že v kategoriji {kategorija}!')
    #     self.izdelki_v_kategoriji[kategorija].append(izdelek)

    # def odstrani_kategorijo(self, kategorija):
    #     self._preveri_kategorijo(kategorija)
    #     self.kategorije.remove(kategorija)
    #     del self.izdelki_v_kategoriji[kategorija]

    # def _preveri_kategorijo(self, kategorija):
    #     if self.izdelki_v_kategoriji[kategorija] is not None:
    #         raise ValueError('Kategorije ne morete odstraniti, saj so v njej izdelki')

    def odstrani_izdelek(self, kategorija, ime):
        if (kategorija, ime) in self.izdelki:
            del self.izdelki[(kategorija, ime)]
        raise ValueError(f'{ime} ni v kategoriji {kategorija}.')

    def prenesi_izdelek(self, kat1, kat2, ime):
        self._preveri_izdelek_v_kategoriji(ime, kat1)
        if ime in self.kategorije[kat2]:
            raise ValueError(f'izdelek je že v kategoriji {kat2}!')
        self.kategorije[kat2].append(izdelek)
        self.kategorije[kat1].remove(izdelek)
        del self.izdelki[(kategorija1, ime)]
        self.izdelki[(kategorija2, ime)] = (kategorije[kategorija1][1], kategorije[kategorija1][2], kategorije[kategorija1][3])  

    def _preveri_izdelek_v_kategoriji(self, izdelek, kategorija):
        if izdelek not in self.kategorije[kategorija]:
            raise ValueError(f'{izdelek} ni v kategoriji {kategorija}')


        
    def dodaj_racun(self, izdelek, kolicina, cena):
        if izdelek in self.vsi_racuni.keys():
            skupna_vrednost = kolicina * cena
            self.vsi_racuni[izdelek].append(skupna_vrednost)
        self.vsi_racuni[izdelek] = kolicina * cena

    def popravi_racun(self, izdelek, kolicina, cena):
        if izdelek in self.vsi_racuni.keys():
            self.vsi_racuni.pop(izdelek)
            self.vsi_racuni[izdelek].append(kolicina * cena)
        raise ValueError(f'Izdelka {izdelek} ni med računi!')

    def dodaj_inventuro(self, izdelek, kolicina):
        self._preveri_izdelek(izdelek)
        self._preveri_inventuro(izdelek)
        self.inventura[izdelek].append(kolicina)

    def _preveri_izdelek(self, izdelek):
        if izdelek not in self.izdelki:
            raise ValueError('Željeni izdelek ne obstaja, inventura zanj ni mogoča!')

    def _preveri_inventuro(self, izdelek):
        if izdelek in self.inventura.keys():
            raise ValueError('Ta izdelek, je že v inventuri!')


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





