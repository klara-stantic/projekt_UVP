import bottle
#import os
#from datetime import date
#from model import Model, Zapisek, Dogodek, Sklop_vaj, Skladba, Vaja

#DATOTEKA = "model.json"
#try:
#    moj_model = Model.preberi_iz_datoteke(DATOTEKA)
#except FileNotFoundError:
#    moj_model = Model()

@bottle.get('/')
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html", 

    )


@bottle.error(404)
def error_404():
    return "Ta spletna stran ne obstaja!"

bottle.run(reloader=True, debug=True)
