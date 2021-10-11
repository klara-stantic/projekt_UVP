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
        st_dogodkov = len (self.dogodki)
        st_oznak = len(self.oznake)
        niz = f"""
            Model, ki ima {st_sklopov} sklopov vaj, 
            {st_dogodkov} dogodkov, {st_zapiskov} zapiskov 
            in {st_oznak} oznak."""
        return niz
    
    #SKLOPI VAJ

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
    
    #OZNAKE
    
    def dodaj_oznako(self, oznaka):
        self.oznake.append(oznaka)
        if not self.aktualna_oznaka:
            self.aktualna_oznaka = oznaka
    
    def izbrisi_oznako(self, oznaka):
        self.oznake.remove(oznaka)
    
    def zamenjaj_oznako(self, oznaka):
        self.aktualna_oznaka = oznaka
    

    
    #ZAPISKI

    def dodaj_zapisek(self, nov_zapisek):
        self.zapiski.append(nov_zapisek)
        if not self.aktualen_zapisek:
            self.aktualen_zapisek = nov_zapisek
    
    def izbrisi_zapisek(self, zapisek):
        self.zapiski.remove(zapisek)
    
    def zamenjaj_zapisek(self, zapisek):
        self.aktualen_zapisek = zapisek
    
    #DOGODKI

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

class Vaja:
    def __init__(self, opis):
        self.opis = opis

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

class Oznaka:
    def __init__(self, ime, mapa):
        self.ime = ime
        self.mapa = mapa #custom, obdobje, zasedba
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
        procenti = (int(self.stevilo_naucenih()) * 100) / int(self.stevilo_skladb())
        return  f"{procenti:.3}%"

    
class Skladba:
    def __init__(self, naslov, avtor, link=None):
        self.naslov = naslov
        self.avtor = avtor
        self.link = link
        self.opombe = ""
        self.pazi = ""
        self.nauceno = False
    
    def __str__(self):
        niz = f"{self.naslov} avtorja {self.avtor}"
        return niz
    
    def nauci_se(self):
        self.nauceno = True

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
