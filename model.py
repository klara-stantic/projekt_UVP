from datetime import date
#import calendar


class Model:
    def __init__(self):
        self.sklopi_vaj = []
        self.aktualen_sklop = None
        self.oznake = []
        self.aktualna_oznaka = None
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
        self.sklopi_vaj.remove(sklop)

    def zamenjaj_sklop(self, sklop):
        self.aktualen_sklop = sklop

    def dodaj_vajo(self, vaja):
        self.aktualen_sklop.dodaj_vajo(vaja)

    def izbrisi_vajo(self, vaja):
        self.aktualen_sklop.izbrisi_vajo(vaja)

    # OZNAKE

    def dodaj_oznako(self, oznaka):
        self.oznake.append(oznaka)
        if not self.aktualna_oznaka:
            self.aktualna_oznaka = oznaka

    def izbrisi_oznako(self, oznaka):
        self.oznake.remove(oznaka)

    def zamenjaj_oznako(self, oznaka):
        self.aktualna_oznaka = oznaka

    # ZAPISKI

    def dodaj_zapisek(self, nov_zapisek):
        self.zapiski.append(nov_zapisek)
        if not self.aktualen_zapisek:
            self.aktualen_zapisek = nov_zapisek

    def izbrisi_zapisek(self, zapisek):
        self.zapiski.remove(zapisek)

    def zamenjaj_zapisek(self, zapisek):
        self.aktualen_zapisek = zapisek

    # DOGODKI

    def dodaj_dogodek(self, dogodek):
        self.dogodki.append(dogodek)
        if not self.aktualen_dogodek:
            self.aktualen_dogodek = dogodek

    def izbrisi_dogodek(self, dogodek):
        self.dogodki.remove(dogodek)

    def zamenjaj_dogodek(self, dogodek):
        self.aktualen_dogodek = dogodek

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
            "aktualen_dogodek": self.zapiski.index(self.aktualen_zapisek)
            if self.aktualen_zapisek
            else None,
            "oznake": [oznaka.v_slovar() for oznaka in self.oznake],
            "aktualen_dogodek": self.oznake.index(self.aktualna_oznaka)
            if self.aktualna_oznaka
            else None,
            "sklopi_vaj": [sklop_vaj.v_slovar() for sklop_vaj in self.sklopi_vaj],
            "aktualen_dogodek": self.sklopi_vaj.index(self.aktualen_sklop)
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
        model.oznake = [
            Oznaka.iz_slovarja(oznaka_slovar) for oznaka_slovar in slovar["oznake"]
        ]
        if slovar["aktualna_oznaka"] is not None:
            model.aktualna_oznaka = model.oznake[slovar["aktualna_oznaka"]]
        model.sklopi_vaj = [
            Sklop_vaj.iz_slovarja(sklop_slovar) for sklop_slovar in slovar["sklopi_vaj"]
        ]
        if slovar["aktualen_sklop"] is not None:
            model.aktualen_sklop = model.sklopi_vaj[slovar["aktualen_sklop"]]
        return model


class Sklop_vaj:
    def __init__(self, ime, opis):
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


class Oznaka:
    def __init__(self, ime, mapa):
        self.ime = ime
        self.mapa = mapa  # custom, obdobje, zasedba
        self.skladbe = []

    def __str__(self):
        niz = f"Oznaka {self.ime} v mapi {self.mapa}"
        return niz

    def dodaj_skladbo(self, skladba):
        self.skladbe.append(skladba)

    def izbrisi_skladbo(self, skladba):
        self.skladbe.remove(skladba)

    def stevilo_skladb(self):
        return len(self.skladbe)

    def stevilo_naucenih(self):
        naucene = 0
        for skladba in self.skladbe:
            if skladba.nauceno:
                naucene += 1
        return naucene

    def razmerje(self):
        procenti = (int(self.stevilo_naucenih()) * 100) / \
            int(self.stevilo_skladb())
        return f"{procenti:.3}%"

    def v_slovar(self):
        return {
            "ime": self.ime,
            "mapa": self.mapa,
            "skladbe": [
                skladba.v_slovar() for skladba in self.skladbe
            ],
        }

    @staticmethod
    def iz_slovarja(slovar):
        oznaka = Oznaka(slovar["ime"], slovar["mapa"])
        oznaka.skladbe = [
            Skladba.iz_slovarja(skladba_slovar) for skladba_slovar in slovar["skladbe"]
        ]
        return oznaka


class Skladba:
    def __init__(self, naslov, avtor):
        self.naslov = naslov
        self.avtor = avtor
        self.link = ""
        self.opombe = ""
        self.pazi = ""
        self.nauceno = False

    def __str__(self):
        niz = f"{self.naslov} avtorja {self.avtor}"
        return niz

    def nauci_se(self):
        self.nauceno = True

    def v_slovar(self):
        return {
            "naslov": self.naslov,
            "avtor": self.avtor,
            "link": self.link,
            "opombe": self.opombe,
            "pazi": self.pazi,
            "nauceno": self.nauceno,
        }

    @staticmethod
    def iz_slovarja(slovar):
        skladba = Skladba(slovar["naslov"], slovar["avtor"])
        skladba.link = slovar["link"]
        skladba.pazi = slovar["pazi"]
        skladba.opombe = slovar["opombe"]
        skladba.nauceno = slovar["nauceno"]
        return skladba


class Dogodek:
    def __init__(self, kaj, kdaj, kje, opombe=None):
        self.kaj = kaj
        self.kdaj = kdaj
        self.kje = kje
        self.skladbe = []
        self.opombe = opombe

    def __str__(self):
        niz = "{self.kaj}"
        return niz

    def preteklost(self):
        return self.kdaj and self.kdaj < date.today()

    def dodaj_skladbo(self, skladba):
        self.skladbe.append(skladba)

    def v_slovar(self):
        return {
            "kaj": self.kaj,
            "kdaj": self.kdaj,
            "kje": self.kje,
            "opombe": self.opombe,
            "skladbe": [skladba.v_slovar() for skladba in self.skladbe],
        }

    @staticmethod
    def iz_slovarja(slovar):
        dogodek = Dogodek(slovar["kaj"], slovar["kdaj"],
                          slovar["kje"], slovar["opombe"])
        dogodek.skladbe = [
            Skladba.iz_slovarja(skladba_slovar) for skladba_slovar in slovar["skladbe"]
        ]
        return dogodek
