from datetime import date
#import calendar

class Model:
    def __init__(self):
        self.sklopi_vaj = []
        self.oznake = []
        self.zapiski = []
        self.dogodki = []

    def dodaj_sklop(self, sklop_vaj):
        self.sklopi_vaj.append(sklop_vaj)
    
    def dodaj_oznako(self, oznaka):
        self.oznake.append(oznaka)

    def dodaj_zapisek(self, nov_zapisek):
        self.zapiski.append(nov_zapisek)

    def dodaj_dogodek(self, dogodek):
        self.dogodki.append(dogodek)

    def razmerje_po_kriteriju(self, kriterij): #manjka ti iteracija po vseh objektih novih razredov!!!
        selekcija_oznak = []
        for oznaka in self.oznake:
            if oznaka.mapa == kriterij:
                selekcija_oznak += oznaka
        slovar = {}
        for oznaka in selekcija_oznak:
            slovar[oznaka] = oznaka.stevilo_skladb() #lahko locis se naucene in nenaucene ko delas graf
        return slovar       

class Sklop_vaj:
    def __init__(self, ime, opis, opombe):
        self.ime = ime
        self.opis = opis
        self.opombe = opombe
        self.vaje = []

    def dodaj_vajo(self, vaja):
        self.vaje.append(vaja)

class Zapisek:
    def __init__(self, datum, predmet, ucitelj, vsebina):
        self.datum = datum
        self.ucitelj = ucitelj
        self.predmet = predmet
        self.vsebina = vsebina
        self.skladbe = []

    def dodaj_skladbo(self, skladba):
        self.skladbe.append(skladba)  

class Oznaka:
    def __init__(self, ime, mapa):
        self.ime = ime
        self.mapa = mapa #custom, obdobje, zasedba
        self.skladbe = []

    def dodaj_skladbo(self, skladba):
        self.skladbe.append(skladba)

    def stevilo_skladb(self):
        return len(self.skladbe)
    
    def razmerje(self):
        naucene = 0
        for skladba in self.skladbe:
           if skladba.nauceno:
                naucene += 1 
        procenti = (naucene * 100) / int(self.stevilo_skladb())
        return  f"{procenti:.3}%"

    
class Skladba:
    def __init__(self, naslov, avtor, link=None, opombe=None, pazi=None):
        self.naslov = naslov
        self.avtor = avtor
        self.link = link
        self.opombe = opombe
        self.pazi = pazi
        self.nauceno = False
    
    def nauci_se(self):
        self.nauceno = True

class Dogodek:
    def __init__(self, kaj, kdaj, kje, skladbe=None, opombe=None):
        self.kaj = kaj
        self.kdaj = kdaj
        self.kje = kje
        self.skladbe = skladbe
        self.opombe = opombe
        
    def preteklost(self):
        return self.kdaj and self.kdaj < date.today()

