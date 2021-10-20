from model import Model, Dogodek, Zapisek, Sklop_vaj, Vaja, Skladba

DATOTEKA = "model.json"
try:
    moj_model = Model.preberi_iz_datoteke(DATOTEKA)
except FileNotFoundError:
    moj_model = Model()

# MOZNOSTI
UREJAJ_SKLOPE = 1
UREJAJ_SKLADBE = 2
UREJAJ_DOGODKE = 3
UREJAJ_ZAPISKE = 4
ZAKLJUCI = 5

DODAJ_SKLOP = 10
POBRISI_SKLOP = 11
ZAMENJAJ_SKLOP = 12
#UREDI_SKLOP = 16
DODAJ_VAJO = 13
POBRISI_VAJO = 14
#UREDI_VAJO = 17
ZAKLJUCI_SKLOP = 15

DODAJ_SKLADBO = 20
POBRISI_SKLADBO = 21
ZAMENJAJ_SKLADBO = 22
#UREDI_SKLADBO = 24
NAUCI_SE = 23
ZAKLJUCI_SKLADBO = 25

DODAJ_ZAPISEK = 30
POBRISI_ZAPISEK = 31
ZAMENJAJ_ZAPISEK = 32
#UREDI_ZAPISEK = 34
ZAKLJUCI_ZAPISEK = 33

DODAJ_DOGODEK = 40
POBRISI_DOGODEK = 41
ZAMENJAJ_DOGODEK = 42
#UREDI_DOGODEK = 44
ZAKLJUCI_DOGODEK = 43


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
    for i, (moznost, opis) in enumerate(moznosti, 1):
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
    ime = sklop.ime
    if sklop.vaje:
        return f"{ime}; vaje: {vaje}"
    else:
        return f"{ime}: Ta sklop nima vaj."


def prikaz_vaje(vaja):
    return f"{vaja.opis}"


def prikaz_skladb(model):
    stevilo = model.stevilo_skladb()
    naucene = model.stevilo_naucenih()
    if model.skladbe:
        procenti = model.razmerje()
        return (f"SKLADBE: {stevilo}\n" +
                f" - Naučene: {naucene} ({procenti})")
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
    print(niz)
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
            (UREJAJ_SKLOPE, "Urejaj sklope"),
            (UREJAJ_SKLADBE, "Urejaj skladbe"),
            (UREJAJ_DOGODKE, "Urejaj dogodke"),
            (UREJAJ_ZAPISKE, "Urejaj zapiske"),
            (ZAKLJUCI, "Zakljuci"),
        ])
        if vnos == UREJAJ_SKLOPE:
            urejanje_sklopov()
        elif vnos == UREJAJ_SKLADBE:
            urejanje_skladb()
        elif vnos == UREJAJ_DOGODKE:
            urejanje_dogodkov()
        elif vnos == UREJAJ_ZAPISKE:
            urejanje_zapiskov()
        elif vnos == ZAKLJUCI:
            moj_model.shrani_v_datoteko(DATOTEKA)
            print("Nasvidenje!")
            break

# POMOZNE FUNKCIJE:


def pozdravi():
    print("Pozdravljeni v svoji beležki!")


def urejanje_sklopov():
    while True:
        print(prikaz_sklopov(moj_model))
        if moj_model.aktualen_sklop:
            print("Aktualen sklop: " + prikaz_sklopa(moj_model.aktualen_sklop))
        vnos = izberi_moznost([
            (DODAJ_SKLOP, "Dodaj sklop vaj"),
            (POBRISI_SKLOP, "Pobriši trenuten sklop vaj"),
            (ZAMENJAJ_SKLOP, "Zamenjaj sklop vaj"),
            (DODAJ_VAJO, "Dodaj vajo"),
            (POBRISI_VAJO, "Pobriši vajo"),
            (ZAKLJUCI_SKLOP, "Zakljuci urejanje sklopov vaj"),
        ])
        if vnos == DODAJ_SKLOP:
            dodaj_sklop()
        elif vnos == POBRISI_SKLOP:
            pobrisi_sklop()
        elif vnos == ZAMENJAJ_SKLOP:
            zamenjaj_sklop()
        elif vnos == DODAJ_VAJO:
            dodaj_vajo()
        elif vnos == POBRISI_VAJO:
            pobrisi_vajo()
        elif vnos == ZAKLJUCI_SKLOP:
            break


def dodaj_sklop():
    print("Vnesite podatke novega sklopa.")
    ime = input("Ime: ")
    opis = input("Opis: ")
    nov_sklop = Sklop_vaj(ime, opis)
    moj_model.dodaj_sklop(nov_sklop)


def pobrisi_sklop():
    sklop = moj_model.aktualen_sklop
    moj_model.izbrisi_sklop(sklop)


def zamenjaj_sklop():
    print("Izberite sklop, na katerega bi preklopili.")
    sklop = izberi_sklop(moj_model)
    moj_model.zamenjaj_sklop(sklop)


def dodaj_vajo():
    print("Vnesite podatke o novi vaji.")
    opis = input("Opis: ")
    nova_vaja = Vaja(opis)
    moj_model.dodaj_vajo(nova_vaja)


def pobrisi_vajo():
    print("Izberite vajo, ki bi jo radi izbrisali.")
    vaja = izberi_vajo(moj_model)
    moj_model.izbrisi_vajo(vaja)

# def uredi_vajo():
#    print("Izberite vajo, ki bi jo radi uredili.")
#    vaja = izberi_vajo(moj_model)


def urejanje_skladb():
    while True:
        print(prikaz_skladb(moj_model))
        if moj_model.aktualna_skladba:
            print("Aktualna skladba: " +
                  prikaz_skladbe(moj_model.aktualna_skladba))
        vnos = izberi_moznost([
            (DODAJ_SKLADBO, "Dodaj skladbo"),
            (POBRISI_SKLADBO, "Pobriši trenutno skladbo"),
            (ZAMENJAJ_SKLADBO, "Zamenjaj trenutnoskladbo"),
            (NAUCI_SE, "Nauči se trenutno skladbo"),
            (ZAKLJUCI_SKLADBO, "Zakljuci urejanje skladb"),
        ])
        if vnos == DODAJ_SKLADBO:
            dodaj_skladbo()
        elif vnos == POBRISI_SKLADBO:
            pobrisi_skladbo()
        elif vnos == ZAMENJAJ_SKLADBO:
            zamenjaj_skladbo()
        elif vnos == NAUCI_SE:
            nauci_se()
        elif vnos == ZAKLJUCI_SKLADBO:
            break


def dodaj_skladbo():
    print("Vnesite podatke nove skladbe.")
    naslov = input("Naslov: ")
    avtor = input("Avtor: ")
    nova_skladba = Skladba(naslov, avtor)
    moj_model.dodaj_skladbo(nova_skladba)


def pobrisi_skladbo():
    skladba = moj_model.aktualna_skladba
    moj_model.izbrisi_skladbo(skladba)


def zamenjaj_skladbo():
    print("Izberite skladbo, na katero bi preklopili.")
    skladba = izberi_skladbo(moj_model)
    moj_model.zamenjaj_skladbo(skladba)


def nauci_se():
    skladba = moj_model.aktualna_skladba
    skladba.nauci_se()


tekstovni_vmesnik()
