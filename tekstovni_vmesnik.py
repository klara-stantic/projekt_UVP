from model import Model, Dogodek, Zapisek, Sklop_vaj, Vaja, Skladba, Oznaka

model = Model()

DODAJ_SKLOP = 1
DODAJ_OZNAKO = 2
DODAJ_ZAPISEK = 3
DODAJ_DOGODEK = 4
DODAJ_VAJO = 5
DODAJ_SKLADBO = 6
ST_SKLADB = 7
RAZMERJE_NAUCENIH_SKLADB = 8
NAUCI_SE = 9
DODAJ_SKLADBO_LEKCIJA = 10
PRETEKLOST = 11
ZAKLJUCI = 12

def tekstovni_vmesnik():
    pozdravi()
    while True:
        prikazi_vsebino()
        vnos = izberi_ukaz([
            (DODAJ_SKLOP, "Dodaj sklop vaj"),
            (DODAJ_OZNAKO, "Dodaj oznako"),
            (DODAJ_ZAPISEK, "Dodaj zapisek iz lekcije"),
            (DODAJ_DOGODEK, "Dodaj dogodek"),
            (DODAJ_VAJO, "Dodaj vajo"),
            (DODAJ_SKLADBO, "Dodaj skladbo"),
            (ST_SKLADB, "Prikazi stevilo skladb"),
            (RAZMERJE_NAUCENIH_SKLADB, "Prikazi razmerje med naucenimi in nenaucenimi skladbami"),
            (NAUCI_SE, "Nauci se skladbo"),
            (DODAJ_SKLADBO_LEKCIJA, "Dodaj skladbo v lekcijo"),
            (PRETEKLOST, "Preveri, ce je dogodek ze pretekel"),
            (ZAKLJUCI, "Zakljuci"),
        ])
        if vnos == DODAJ_SKLOP:
            dodaj_sklop()
        elif vnos == DODAJ_OZNAKO:
            dodaj_oznako()
        elif vnos == DODAJ_ZAPISEK:
            dodaj_zapisek()
        elif vnos == DODAJ_DOGODEK:
            dodaj_dogodek()
        elif vnos == DODAJ_VAJO:
            dodaj_vajo()
        elif vnos == DODAJ_SKLADBO:
            dodaj_skladbo()
        elif vnos == ST_SKLADB:
            st_skladb()
        elif vnos == RAZMERJE_NAUCENIH_SKLADB:
            razmerje_naucenih_skladb()
        elif vnos == NAUCI_SE:
            nauci_se()
        elif vnos == DODAJ_SKLADBO_LEKCIJA:
            dodaj_skladbo_lekcija()
        elif vnos == PRETEKLOST:
            preteklost()
        elif vnos == ZAKLJUCI:
            break 
        
def pozdravi():
    print("Pozdravljeni v svoji beležki!")

def dodaj_sklop():
    print("Vnesi podatke za nov sklop vaj!")
    ime = input("Ime: ")
    opis = input("Opis: ")
    nov_sklop = Sklop_vaj(ime, opis)
    model.dodaj_sklop(nov_sklop)

def dodaj_oznako():
    print("Vnesi podatke za novo oznako!")
    ime = input("Ime: ")
    mapa = input("Mapa: ")
    nova_oznaka = Oznaka(ime, mapa)
    model.dodaj_oznako(nova_oznaka)

def dodaj_dogodek():
    print("Vnesi podatke za nov dogodek!")
    kaj = input("Ime dogodka: ")
    kdaj = input("Datum: ")
    kje = input("Lokacija: ")
    nov_dogodek = Dogodek(kaj, kdaj, kje)
    model.dodaj_dogodek(nov_dogodek)

def dodaj_zapisek():
    print("Vnesi podatke za nov zapisek!")
    datum = input("Datum naj bo formata LLLL/MM/DD! Datum: ")
    predmet = input("Predmet: ")
    ucitelj = input("Ucitelj: ")
    vsebina = input("Vsebina: ")
    nov_zapisek = Zapisek(datum, predmet, ucitelj, vsebina)
    model.dodaj_zapisek(nov_zapisek)



