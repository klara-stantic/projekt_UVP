from datetime import date
import json
#import calendar


class Model:
    def __init__(self):
        self.sklopi_vaj = []
        self.vaje = []
        self.aktualen_sklop = None
        self.skladbe = []
        self.aktualna_skladba = None
        self.zapiski = []
        self.aktualen_zapisek = None
        self.dogodki = []
        self.aktualen_dogodek = None

    def __str__(self):
        st_sklopov = len(self.sklopi_vaj)
        st_zapiskov = len(self.zapiski)
        st_dogodkov = len(self.dogodki)
        st_oznak = len(self.oznake)
        niz = f"""
            Model, ki ima {st_sklopov} sklopov vaj, 
            {st_dogodkov} dogodkov, {st_zapiskov} zapiskov 
            in {st_oznak} oznak."""
        return niz

    # SKLOPI VAJ

    def dodaj_sklop(self, sklop_vaj):
        self.sklopi_vaj.append(sklop_vaj)
        if not self.aktualen_sklop:
            self.aktualen_sklop = sklop_vaj

    def izbrisi_sklop(self, sklop):
        if sklop == self.aktualen_sklop:
            self.aktualen_sklop = None
        self.sklopi_vaj.remove(sklop)

    def zamenjaj_sklop(self, sklop):
        self.aktualen_sklop = sklop

    def dodaj_vajo(self, vaja):
        self.vaje.append(vaja)

    def izbrisi_vajo(self, vaja):
        for sklop in self.sklopi_vaj:
            if vaja in sklop.vaje:
                sklop.izbrisi_vajo(vaja)
        self.vaje.remove(vaja)

    def stevilo_sklopov(self):
        return len(self.sklopi_vaj)

    def stevilo_vaj(self):
        return len(self.vaje)

    # SKLADBE

    def dodaj_skladbo(self, skladba):
        self.skladbe.append(skladba)
        if not self.aktualna_skladba:
            self.aktualna_skladba = skladba

    def izbrisi_skladbo(self, skladba):
        if skladba == self.aktualna_skladba:
            self.aktualna_skladba = None
        self.skladbe.remove(skladba)

    def zamenjaj_skladbo(self, skladba):
        self.aktualna_skladba = skladba

    def stevilo_skladb(self):
        return len(self.skladbe)

    def stevilo_naucenih(self):
        naucene = 0
        for skladba in self.skladbe:
            if skladba.nauceno:
                naucene += 1
        return naucene

    def razmerje(self):
        if self.skladbe:
            procenti = (int(self.stevilo_naucenih()) * 100) / \
                int(self.stevilo_skladb())
            return f"{procenti:.3}"
        else:
            return 0

    # ZAPISKI

    def dodaj_zapisek(self, nov_zapisek):
        self.zapiski.append(nov_zapisek)
        if not self.aktualen_zapisek:
            self.aktualen_zapisek = nov_zapisek

    def preveri_zapisek(self, datum, predmet, ucitelj, vsebina):
        napake = {}
        if not predmet:
            napake["predmet"] = "Ta razdelek je obvezen."
        return napake

    def izbrisi_zapisek(self, zapisek):
        if zapisek == self.aktualen_zapisek:
            self.aktualen_zapisek = None
        self.zapiski.remove(zapisek)

    def zamenjaj_zapisek(self, zapisek):
        self.aktualen_zapisek = zapisek

    def stevilo_zapiskov(self):
        return len(self.zapiski)

    # DOGODKI

    def dodaj_dogodek(self, dogodek):
        self.dogodki.append(dogodek)
        if not self.aktualen_dogodek:
            self.aktualen_dogodek = dogodek

    def preveri_dogodek(self, kaj, kdaj, ura, kje, opombe):
        napake = {}
        if not kaj:
            napake["kaj"] = "Ta razdelek je obvezen."
        if not kaj:
            napake["kdaj"] = "Ta razdelek je obvezen."
        return napake

    def izbrisi_dogodek(self, dogodek):
        if dogodek == self.aktualen_dogodek:
            self.aktualen_dogodek = None
        self.dogodki.remove(dogodek)

    def zamenjaj_dogodek(self, dogodek):
        self.aktualen_dogodek = dogodek

    def stevilo_dogodkov(self):
        return len(self.dogodki)

    def stevilo_preteklih(self):
        pretekli = []
        for dogodek in self.dogodki:
            if dogodek.preteklost() or not dogodek.kdaj:
                pretekli.append(dogodek)
        return len(pretekli)

    def stevilo_prihajajocih(self):
        return self.stevilo_dogodkov() - self.stevilo_preteklih()

#    def razmerje_po_kriteriju(self, kriterij): #manjka ti iteracija po vseh objektih novih razredov!!!
#        selekcija_oznak = []
#        for oznaka in self.oznake:
#            if oznaka.mapa == kriterij:
#                selekcija_oznak += oznaka
#        slovar = {}
#        for oznaka in selekcija_oznak:
#            slovar[oznaka] = oznaka.stevilo_skladb() #lahko locis se naucene in nenaucene ko delas graf
#        return slovar

    def v_slovar(self):
        return {
            "dogodki": [dogodek.v_slovar() for dogodek in self.dogodki],
            "aktualen_dogodek": self.dogodki.index(self.aktualen_dogodek)
            if self.aktualen_dogodek
            else None,
            "zapiski": [zapisek.v_slovar() for zapisek in self.zapiski],
            "aktualen_zapisek": self.zapiski.index(self.aktualen_zapisek)
            if self.aktualen_zapisek
            else None,
            "skladbe": [skladba.v_slovar() for skladba in self.skladbe],
            "aktualna_skladba": self.skladbe.index(self.aktualna_skladba)
            if self.aktualna_skladba
            else None,
            "sklopi_vaj": [sklop_vaj.v_slovar() for sklop_vaj in self.sklopi_vaj],
            "vaje": [vaja.v_slovar() for vaja in self.vaje],
            "aktualen_sklop": self.sklopi_vaj.index(self.aktualen_sklop)
            if self.aktualen_sklop
            else None,
        }

    @staticmethod
    def iz_slovarja(slovar):
        model = Model()
        model.dogodki = [
            Dogodek.iz_slovarja(dogodek_slovar) for dogodek_slovar in slovar["dogodki"]
        ]
        if slovar["aktualen_dogodek"] is not None:
            model.aktualen_dogodek = model.dogodki[slovar["aktualen_dogodek"]]
        model.zapiski = [
            Zapisek.iz_slovarja(zapisek_slovar) for zapisek_slovar in slovar["zapiski"]
        ]
        if slovar["aktualen_zapisek"] is not None:
            model.aktualen_zapisek = model.zapiski[slovar["aktualen_zapisek"]]
        model.skladbe = [
            Skladba.iz_slovarja(skladba_slovar) for skladba_slovar in slovar["skladbe"]
        ]
        if slovar["aktualna_skladba"] is not None:
            model.aktualna_skladba = model.skladbe[slovar["aktualna_skladba"]]
        model.sklopi_vaj = [
            Sklop_vaj.iz_slovarja(sklop_slovar) for sklop_slovar in slovar["sklopi_vaj"]
        ]
        model.vaje = [
            Vaja.iz_slovarja(vaja_slovar) for vaja_slovar in slovar["vaje"]
        ]
        if slovar["aktualen_sklop"] is not None:
            model.aktualen_sklop = model.sklopi_vaj[slovar["aktualen_sklop"]]
        return model

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Model.iz_slovarja(slovar)


class Sklop_vaj:
    def __init__(self, ime, opis=None):
        self.ime = ime
        self.opis = opis
        self.vaje = []

    def __str__(self):
        st_vaj = len(self.vaje)
        niz = f"Sklop {st_vaj} vaj"
        return niz

    def dodaj_vajo(self, vaja):
        self.vaje.append(vaja)

    def izbrisi_vajo(self, vaja):
        self.vaje.remove(vaja)

    def stevilo_vaj(self):
        return len(self.vaje)

    def v_slovar(self):
        return {
            "ime": self.ime,
            "opis": self.opis,
            "vaje": [vaja.v_slovar() for vaja in self.vaje],
        }

    @staticmethod
    def iz_slovarja(slovar):
        sklop_vaj = Sklop_vaj(slovar["ime"], slovar["opis"])
        sklop_vaj.vaje = [
            Vaja.iz_slovarja(vaja_slovar) for vaja_slovar in slovar["vaje"]
        ]
        return sklop_vaj


class Vaja:
    def __init__(self, opis):
        self.opis = opis

    def v_slovar(self):
        return {
            "opis": self.opis,
        }

    @staticmethod
    def iz_slovarja(slovar):
        vaja = Vaja(slovar["opis"])
        return vaja


class Zapisek:
    def __init__(self, datum, predmet, ucitelj, vsebina):
        self.datum = datum
        self.ucitelj = ucitelj
        self.predmet = predmet
        self.vsebina = vsebina
        self.skladbe = []

    def __str__(self):
        niz = f"""Zapisek lekcije {self.predmet} pri {self.ucitelj} iz dne {self.datum}"""
        return niz

    def dodaj_skladbo_lekcija(self, skladba):
        self.skladbe.append(skladba)

    def v_slovar(self):
        return {
            "datum": self.datum,
            "ucitelj": self.ucitelj,
            "predmet": self.predmet,
            "vsebina": self.vsebina,
            "skladbe": [skladba.v_slovar() for skladba in self.skladbe],
        }

    @staticmethod
    def iz_slovarja(slovar):
        zapisek = Zapisek(slovar["datum"], slovar["ucitelj"],
                          slovar["predmet"], slovar["vsebina"])
        zapisek.skladbe = [
            Skladba.iz_slovarja(skladba_slovar) for skladba_slovar in slovar["skladbe"]
        ]
        return zapisek


# class Oznaka:
#    def __init__(self, ime, mapa):
#        self.ime = ime
#        self.mapa = mapa  # custom, obdobje, zasedba
#        self.skladbe = []
#
#    def __str__(self):
#        niz = f"Oznaka {self.ime} v mapi {self.mapa}"
#        return niz
#
#    def dodaj_skladbo(self, skladba):
#        self.skladbe.append(skladba)
#
#    def izbrisi_skladbo(self, skladba):
#        self.skladbe.remove(skladba)
#
#    def stevilo_skladb(self):
#        return len(self.skladbe)
#
#    def v_slovar(self):
#        return {
#            "ime": self.ime,
#            "mapa": self.mapa,
#            "skladbe": [
#                skladba.v_slovar() for skladba in self.skladbe
#            ],
#        }
#
#    @staticmethod
#    def iz_slovarja(slovar):
#        oznaka = Oznaka(slovar["ime"], slovar["mapa"])
#        oznaka.skladbe = [
#            Skladba.iz_slovarja(skladba_slovar) for skladba_slovar in slovar["skladbe"]
#        ]
#        return oznaka


class Skladba:
    def __init__(self, naslov, avtor):
        self.naslov = naslov
        self.avtor = avtor
        self.link = ""
        self.opombe = ""
        self.pazi = ""
        self.pdf = []
        self.nauceno = False
        self.oznake = []

    def __str__(self):
        niz = f"{self.naslov} avtorja {self.avtor}"
        return niz

    def nauci_se(self):
        self.nauceno = not self.nauceno

    def v_slovar(self):
        return {
            "naslov": self.naslov,
            "avtor": self.avtor,
            "link": self.link,
            "opombe": self.opombe,
            "pazi": self.pazi,
            "pdf": self.pdf,
            "nauceno": self.nauceno,
            "oznake": self.oznake,
        }

    @staticmethod
    def iz_slovarja(slovar):
        skladba = Skladba(slovar["naslov"], slovar["avtor"])
        skladba.link = slovar["link"]
        skladba.pazi = slovar["pazi"]
        skladba.pdf = slovar["pdf"]
        skladba.opombe = slovar["opombe"]
        skladba.nauceno = slovar["nauceno"]
        skladba.oznake = slovar["oznake"]
        return skladba


class Dogodek:
    def __init__(self, kaj, kdaj, ura, kje=None, opombe=None):
        self.kaj = kaj
        self.kdaj = kdaj
        self.ura = ura
        self.kje = kje
        self.skladbe = []
        self.opombe = opombe

    def __str__(self):
        niz = "{self.kaj}"
        return niz

    def preteklost(self):
        return self.kdaj and date.fromisoformat(self.kdaj) < date.today()

    def dodaj_skladbo(self, skladba):
        self.skladbe.append(skladba)

    def v_slovar(self):
        return {
            "kaj": self.kaj,
            "kdaj": self.kdaj,
            "ura": self.ura,
            "kje": self.kje,
            "opombe": self.opombe,
            "skladbe": [skladba.v_slovar() for skladba in self.skladbe],
        }

    @staticmethod
    def iz_slovarja(slovar):
        dogodek = Dogodek(slovar["kaj"], slovar["kdaj"], slovar["ura"],
                          slovar["kje"], slovar["opombe"])
        dogodek.skladbe = [
            Skladba.iz_slovarja(skladba_slovar) for skladba_slovar in slovar["skladbe"]
        ]
        return dogodek
