import bottle
import os
from datetime import date
from model import Model, Zapisek, Dogodek, Sklop_vaj, Skladba, Vaja


def nalozi_uporabnikov_model():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime:
        return Model.preberi_iz_datoteke(uporabnisko_ime)
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

#PRVA STRAN
@bottle.get('/')
def osnovna_stran():
    moj_model = nalozi_uporabnikov_model()
    return bottle.template(
        "prva_stran.html",
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
        skladbe = moj_model.skladbe if moj_model.skladbe else [], 
        st_skladb = moj_model.stevilo_skladb(),
        st_naucenih = moj_model.stevilo_naucenih(),
        sklopi = moj_model.sklopi_vaj if moj_model.sklopi_vaj else [], 
        st_sklopov = moj_model.stevilo_sklopov(),
        dogodki = moj_model.dogodki if moj_model.dogodki else [],
        st_dogodkov = moj_model.stevilo_dogodkov(),
        zapiski = moj_model.zapiski if moj_model.zapiski else[],
        st_zapiskov = moj_model.stevilo_zapiskov(),
    )


@bottle.get('/zapiski/')
def zapiski():
    return bottle.template(
        "zapiski.html",
    )

@bottle.get('/skladbe/')
def skladbe():
    return bottle.template(
        "skladbe.html",
    )

@bottle.get('/dogodki/')
def dogodki():
    return bottle.template(
        "dogodki.html",
    )

@bottle.get('/vaje/')
def vaje():
    return bottle.template(
        "vaje.html",
    )





@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)
