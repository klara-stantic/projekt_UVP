import bottle
import os
from datetime import date
from model import Model, Zapisek, Dogodek, Sklop_vaj, Skladba, Vaja


def nalozi_uporabnikov_model():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime:
        try:
            return Model.preberi_iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            bottle.redirect("/registracija/")
    else:
        bottle.redirect("/prijava/")


def shrani_uporabnikov_model(moj_model):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    moj_model.shrani_v_datoteko(uporabnisko_ime)


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime že obstaja."}
        return bottle.template("registracija.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        Model().shrani_v_datoteko(uporabnisko_ime)
        bottle.redirect("/")


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if not os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime ne obstaja."}
        return bottle.template("prijava.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        bottle.redirect("/")


@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    print("Piškotek je bil uspešno pobrisan.")
    bottle.redirect("/")


# PRVA STRAN
@bottle.get('/')
def osnovna_stran():
    if nalozi_uporabnikov_model():
        moj_model = nalozi_uporabnikov_model()
    else:
        moj_model = Model()
    return bottle.template(
        "prva_stran.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        skladbe=moj_model.skladbe if moj_model.skladbe else [],
        st_skladb=moj_model.stevilo_skladb(),
        st_naucenih=moj_model.stevilo_naucenih(),
        sklopi=moj_model.sklopi_vaj if moj_model.sklopi_vaj else [],
        st_sklopov=moj_model.stevilo_sklopov(),
        dogodki=moj_model.dogodki if moj_model.dogodki else [],
        st_dogodkov=moj_model.stevilo_prihajajocih(),
        zapiski=moj_model.zapiski if moj_model.zapiski else[],
        st_zapiskov=moj_model.stevilo_zapiskov(),
        razmerje=float(moj_model.razmerje()),
    )


@bottle.get('/zapiski/')
def zapiski():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "zapiski.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        zapiski=moj_model.zapiski if moj_model.zapiski else[],
        st_zapiskov=moj_model.stevilo_zapiskov(),
    )


@bottle.get("/dodaj_zapisek/")
def dodaj_zapisek():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "dodajanje_zapiska.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        skladbe=moj_model.skladbe
    )


@bottle.post("/dodaj_zapisek/")
def dodaj_zapisek():
    moj_model = nalozi_uporabnikov_model()
    predmet = bottle.request.forms.getunicode("predmet")
    ucitelj = bottle.request.forms.getunicode("ucitelj")
    vsebina = bottle.request.forms.getunicode("vsebina")
    if bottle.request.forms.getunicode("datum"):
        datum = bottle.request.forms.getunicode("datum")
    else:
        datum = None
    zapisek = Zapisek(datum, predmet, ucitelj, vsebina)
    izbira = bottle.request.forms.getall("skladbe_izbira")
    if izbira:
        for indeks in izbira:
            zapisek.skladbe.append(moj_model.skladbe[int(indeks)])
    moj_model.dodaj_zapisek(zapisek)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect('/zapiski/')


@bottle.post("/izbrisi_zapisek/")
def izbrisi_zapisek():
    indeks = bottle.request.forms.getunicode("indeks")
    moj_model = nalozi_uporabnikov_model()
    zapisek = moj_model.zapiski[int(indeks)]
    moj_model.izbrisi_zapisek(zapisek)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect("/zapiski/")


@bottle.get('/skladbe/')
def skladbe():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "skladbe.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        skladbe=moj_model.skladbe if moj_model.skladbe else [],
        st_skladb=moj_model.stevilo_skladb(),
        razmerje=float(moj_model.razmerje()),
    )


@bottle.get("/dodaj_skladbo/")
def dodaj_skladbo():
    return bottle.template(
        "dodajanje_skladbe.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime")
    )


@bottle.post("/dodaj_skladbo/")
def dodaj_skladbo():
    naslov = bottle.request.forms.getunicode("naslov")
    avtor = bottle.request.forms.getunicode("avtor")
    link = bottle.request.forms.getunicode("link")
    opombe = bottle.request.forms.getunicode("opombe")
    pazi = bottle.request.forms.getunicode("pazi")
    pdf = bottle.request.forms.getall("pdf")
    skladba = Skladba(naslov, avtor)
    skladba.link = link
    skladba.pazi = pazi
    skladbe.opombe = opombe
    skladba.pdf = pdf
    moj_model = nalozi_uporabnikov_model()
    moj_model.dodaj_skladbo(skladba)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect('/skladbe/')


@bottle.post("/nauceno/")
def nauceno():
    indeks = bottle.request.forms.getunicode("indeks")
    moj_model = nalozi_uporabnikov_model()
    skladba = moj_model.skladbe[int(indeks)]
    skladba.nauci_se()
    shrani_uporabnikov_model(moj_model)
    bottle.redirect("/skladbe/")


@bottle.post("/izbrisi_skladbo/")
def izbrisi_skladbo():
    indeks = bottle.request.forms.getunicode("indeks")
    moj_model = nalozi_uporabnikov_model()
    skladba = moj_model.skladbe[int(indeks)]
    moj_model.izbrisi_skladbo(skladba)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect("/skladbe/")


@bottle.get('/dogodki/')
def dogodki():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "dogodki.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        dogodki=moj_model.dogodki if moj_model.dogodki else [],
        st_dogodkov=moj_model.stevilo_prihajajocih(),
    )


@bottle.get("/dodaj_dogodek/")
def dodaj_dogodek():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "dodajanje_dogodka.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"), 
        skladbe=moj_model.skladbe
    )


@bottle.post("/dodaj_dogodek/")
def dodaj_dogodek():
    moj_model = nalozi_uporabnikov_model()
    kaj = bottle.request.forms.getunicode("kaj")
    kdaj = bottle.request.forms.getunicode("kdaj")
    kje = bottle.request.forms.getunicode("kje")
    ura = bottle.request.forms.getunicode("ura")
    opombe = bottle.request.forms.getunicode("opombe")
    dogodek = Dogodek(kaj, kdaj, ura, kje)
    dogodek.opombe = opombe
    izbira = bottle.request.forms.getall("skladbe_izbira")
    if izbira:
        for indeks in izbira:
            dogodek.skladbe.append(moj_model.skladbe[int(indeks)])    
    moj_model.dodaj_dogodek(dogodek)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect('/dogodki/')


@bottle.post("/izbrisi_dogodek/")
def izbrisi_dogodek():
    indeks = bottle.request.forms.getunicode("indeks")
    moj_model = nalozi_uporabnikov_model()
    dogodek = moj_model.dogodki[int(indeks)]
    moj_model.izbrisi_dogodek(dogodek)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect("/dogodki/")


@bottle.get('/sklopi/')
def sklopi():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "sklopi.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        sklopi=moj_model.sklopi_vaj if moj_model.sklopi_vaj else [],
        st_sklopov=moj_model.stevilo_sklopov(),
    )


@bottle.get("/dodaj_sklop/")
def dodaj_sklop():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "dodajanje_sklopov.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"), 
        vaje = moj_model.vaje,
    )


@bottle.post("/dodaj_sklop/")
def dodaj_sklop():
    moj_model = nalozi_uporabnikov_model()
    ime = bottle.request.forms.getunicode("ime")
    opis = bottle.request.forms.getunicode("opis")
    sklop = Sklop_vaj(ime, opis)
    izbira = bottle.request.forms.getall("vaje_izbira")
    if izbira:
        for indeks in izbira:
            sklop.vaje.append(moj_model.vaje[int(indeks)])
    moj_model.dodaj_sklop(sklop)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect('/sklopi/')


@bottle.post("/izbrisi_sklop/")
def izbrisi_sklop():
    indeks = bottle.request.forms.getunicode("indeks")
    moj_model = nalozi_uporabnikov_model()
    sklop = moj_model.sklopi_vaj[int(indeks)]
    moj_model.izbrisi_sklop(sklop)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect("/sklopi/")


@bottle.get('/vaje/')
def vaje():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "vaje.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        vaje = moj_model.vaje if moj_model.vaje else [],
        st_vaj = moj_model.stevilo_vaj(),
    )


@bottle.post("/dodaj_vajo/")
def dodaj_vajo():
    opis = bottle.request.forms.getunicode("opis")
    vaja = Vaja(opis)
    moj_model = nalozi_uporabnikov_model()
    moj_model.dodaj_vajo(vaja)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect('/vaje/')


@bottle.post("/izbrisi_vajo/")
def izbrisi_vajo():
    indeks = bottle.request.forms.getunicode("indeks")
    moj_model = nalozi_uporabnikov_model()
    vaja = moj_model.vaje[int(indeks)]
    moj_model.izbrisi_vajo(vaja)
    shrani_uporabnikov_model(moj_model)
    bottle.redirect("/vaje/")

@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True)
