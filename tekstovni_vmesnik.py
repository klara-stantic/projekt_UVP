from model import Model, Dogodek, Zapisek, Sklop_vaj, Vaja, Skladba

DATOTEKA = "model.json"
try:
    moj_model = Model.preberi_iz_datoteke(DATOTEKA)
except FileNotFoundError:
    moj_model = Model()


# MOZNOSTI

DODAJ_SKLOP = 10
POBRISI_SKLOP = 11
ZAMENJAJ_SKLOP = 12
UREDI_SKLOP = 13

DODAJ_SKLADBO = 20
POBRISI_SKLADBO = 21
ZAMENJAJ_SKLADBO = 22
UREDI_SKLADBO = 23
NAUCI_SE = 24

DODAJ_ZAPISEK = 30
POBRISI_ZAPISEK = 31
ZAMENJAJ_ZAPISEK = 32
UREDI_ZAPISEK = 33

DODAJ_DOGODEK = 40
POBRISI_DOGODEK = 41
ZAMENJAJ_DOGODEK = 42
UREDI_DOGODEK = 43

DODAJ_VAJO = 50
POBRISI_VAJO = 51
ZAMENJAJ_VAJO = 52
UREDI_VAJO = 53

ZAKLJUCI = 6


def preberi_stevilo():
    """Funkcija, ki prebere vnos števila iz konzole."""
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


def izberi_moznost(moznosti):
    """Uporabniku našteje možnosti ter vrne izbrano."""
    for i, (_moznost, opis) in enumerate(moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        i = preberi_stevilo()
        if 1 <= i <= len(moznosti):
            moznost, _opis = moznosti[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(moznosti)}.")


# PRIKAZOVANJE OBJEKTOV

def prikaz_dogodkov(model):
    vsi = model.stevilo_dogodkov()
    pretekli = model.stevilo_preteklih()
    if model.dogodki:
        if model.stevilo_preteklih() > 0:
            return (f"DOGODKI: {vsi}\n" + f"Pretekli: {pretekli}")
        else:
            return f"DOGODKI: {vsi}"
    else:
        return "Ni dogodkov."


def prikaz_dogodka(dogodek):
    if dogodek.preteklost():
        return f"{dogodek.kaj} - pretekel"
    else:
        return f"{dogodek.kaj} - {dogodek.kdaj}"


def prikaz_zapiskov(model):
    stevilo = model.stevilo_zapiskov()
    if model.zapiski:
        return f"ZAPISKI: {stevilo}"
    else:
        return "Ni zapiskov."


def kratek_prikaz_zapiska(zapisek):
    return f"{zapisek.predmet}, {zapisek.datum}"


def prikaz_sklopov(model):
    stevilo = model.stevilo_sklopov()
    if model.sklopi_vaj:
        return f"SKLOPI VAJ: {stevilo}"
    else:
        return "Ni sklopov vaj."


def prikaz_sklopa(sklop):
    vaje = sklop.stevilo_vaj()
    if sklop.vaje:
        return f"VAJE: {vaje}"
    else:
        return "Ta sklop nima vaj."


def prikaz_vaje(vaja):
    return f"{vaja.opis}"


def prikaz_skladb(model):
    stevilo = model.stevilo_skladb()
    naucene = model.stevilo_naucenih()
    if model.skladbe:
        procenti = model.razmerje()
        return (f"SKLADBE: {stevilo}\n" +
                f"Naučene: {naucene} ({procenti})")
    else:
        return "Ni skladb."


def prikaz_skladbe(skladba):
    if skladba.nauceno:
        return f"{skladba.naslov}, {skladba.avtor} - naučena"
    else:
        return f"{skladba.naslov}, {skladba.avtor}"


def prikazi_vsebino(model):
    niz = (prikaz_dogodkov(model) + "\n" + prikaz_zapiskov(model) +
           "\n" + prikaz_sklopov(model) + "\n" + prikaz_skladb(model))
    return niz

# IZBIRE


def izberi_dogodek(model):
    return izberi_moznost([(dogodek, prikaz_dogodka(dogodek)) for dogodek in model.dogodki])


def izberi_zapisek(model):
    return izberi_moznost([(zapisek, kratek_prikaz_zapiska(zapisek)) for zapisek in model.zapiski])


def izberi_sklop(model):
    return izberi_moznost([(sklop, prikaz_sklopa(sklop)) for sklop in model.sklopi_vaj])


def izberi_vajo(model):
    return izberi_moznost([(vaja, prikaz_vaje(vaja)) for vaja in model.aktualen_sklop.vaje])


def izberi_skladbo(model):
    return izberi_moznost([(skladba, prikaz_skladbe(skladba)) for skladba in model.skladbe])

# TEKSTOVNI VMESNIK


def tekstovni_vmesnik():
    pozdravi()
    while True:
        prikazi_vsebino(moj_model)
        vnos = izberi_moznost([
            (DODAJ_SKLOP, "Dodaj sklop vaj"),
            (POBRISI_SKLOP, "Pobriši sklop vaj"), 
            (ZAMENJAJ_SKLOP), "Zamenjaj sklop",
            (UREDI_SKLOP), "Uredi sklop",
            
            (DODAJ_ZAPISEK, "Dodaj zapisek iz lekcije"),
            (POBRISI_ZAPISEK, "Pobriši zapisek"),
            (ZAMENJAJ_ZAPISEK, "Zamenjaj zapisek"),
            (UREDI_ZAPISEK, "Uredi zapisek"),
            
            (DODAJ_DOGODEK, "Dodaj dogodek"),
            (POBRISI_DOGODEK, "Pobriši dogodek"),
            (ZAMENJAJ_DOGODEK, "Zamenjaj dogodek"),
            (UREDI_DOGODEK, "Uredi dogodek"),
            
            (DODAJ_VAJO, "Dodaj vajo"),
            (POBRISI_VAJO, "Pobriši vajo"),
            (ZAMENJAJ_VAJO, "Zamenjaj vajo"),
            (UREDI_VAJO, "Uredi vajo"),
            
            (DODAJ_SKLADBO, "Dodaj skladbo"),
            (POBRISI_SKLADBO, "Pobriši skladbo"),
            (ZAMENJAJ_SKLADBO, "Zamenjaj skladbo"),
            (UREDI_SKLADBO, "Uredi skladbo"),
            (NAUCI_SE, "Nauci se skladbo"),
            
            (ZAKLJUCI, "Zakljuci"),
        ])
        if vnos == DODAJ_SKLOP:
            dodaj_sklop()
        elif vnos == POBRISI_SKLOP:
            pobrisi_sklop()
        elif vnos == ZAMENJAJ_SKLOP:
            zamenjaj_sklop()
        elif vnos == UREDI_SKLOP:
            uredi_sklop()
        elif vnos == DODAJ_ZAPISEK:
            dodaj_zapisek()
        elif vnos == POBRISI_ZAPISEK:
            pobrisi_zapisek()
        elif vnos == ZAMENJAJ_ZAPISEK:
            zamenjaj_zapisek()
        elif vnos == UREDI_ZAPISEK:
            uredi_zapisek()
        elif vnos == DODAJ_DOGODEK:
            dodaj_dogodek()
        elif vnos == POBRISI_DOGODEK:
            pobrisi_dogodek()
        elif vnos == ZAMENJAJ_DOGODEK:
            zamenjaj_dogodek()
        elif vnos == UREDI_DOGODEK:
            uredi_dogodek()
        elif vnos == DODAJ_VAJO:
            dodaj_vajo()
        elif vnos == POBRISI_VAJO:
            pobrisi_vajo()
        elif vnos == ZAMENJAJ_VAJO:
            zamenjaj_vajo()
        elif vnos == UREDI_VAJO:
            uredi_vajo()
        elif vnos == DODAJ_SKLADBO:
            dodaj_skladbo()
        elif vnos == POBRISI_SKLADBO:
            pobrisi_skladbo()
        elif vnos == ZAMENJAJ_SKLADBO:
            zamenjaj_skladbo()
        elif vnos == UREDI_SKLADBO:
            uredi_skladbo()
        elif vnos == NAUCI_SE:
            nauci_se()
        elif vnos == ZAKLJUCI:
            moj_model.shrani_v_datoteko(DATOTEKA)
            print("Nasvidenje!")
            break

#POMOZNE FUNKCIJE:
def pozdravi():
    print("Pozdravljeni v svoji beležki!")


def dodaj_sklop():
    print("Vnesi podatke za nov sklop vaj!")
    ime = input("Ime: ")
    opis = input("Opis: ")
    nov_sklop = Sklop_vaj(ime, opis)
    moj_model.dodaj_sklop(nov_sklop)



def dodaj_skladbo():
    print("Vnesi podatke za novo skladbo!")
    naslov = input("Naslov: ")
    avtor = input("Avtor: ")
    nova_skladba = Skladba(naslov, avtor)
    moj_model.dodaj_skladbo(nova_skladba)


def dodaj_dogodek():
    print("Vnesi podatke za nov dogodek!")
    kaj = input("Ime dogodka: ")
    kdaj = input("Datum: ")
    kje = input("Lokacija: ")
    nov_dogodek = Dogodek(kaj, kdaj, kje)
    moj_model.dodaj_dogodek(nov_dogodek)


def dodaj_zapisek():
    print("Vnesi podatke za nov zapisek!")
    datum = input("Datum naj bo formata LLLL/MM/DD! Datum: ")
    predmet = input("Predmet: ")
    ucitelj = input("Ucitelj: ")
    vsebina = input("Vsebina: ")
    nov_zapisek = Zapisek(datum, predmet, ucitelj, vsebina)
    moj_model.dodaj_zapisek(nov_zapisek)
