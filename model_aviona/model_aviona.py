
"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: str = "",
    pozicije_sedista: list = []
) -> dict:
    if not naziv or not broj_redova or not pozicije_sedista:
        raise Exception("Greska! Niste uneli neki od parametara.")

    id=0
    for i in svi_modeli_aviona:
        id+=1
    novi_model={'id': id, 'naziv': naziv, 'broj_redova': broj_redova, 'pozicije_sedista': pozicije_sedista}
    svi_modeli_aviona[id]=novi_model
    return svi_modeli_aviona

"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, 'a') as file:
        for key in svi_aerodromi:
            file.write(str(svi_aerodromi[key]['id']) + separator + svi_aerodromi[key]['naziv']
                       + separator + str(svi_aerodromi[key]['broj_redova']) + separator +
                       str(svi_aerodromi[key]['pozicije_sedista']) + '\n')

"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    recnik={}
    with open(putanja, 'r') as file:
        for row in file:
            items=row.split(separator)
            id=int(items[0])
            recnik[id]={'id': id, 'naziv': items[1], 'broj_redova': int(items[2]),
                        'pozicije_sedista': eval(items[3])}
    return recnik
