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


@bottle.get('/')
def osnovna_stran():
    return bottle.template(
        "baza.html",
    )


@bottle.get('/Zapiski/')
def zapiski():
    pass


@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)
