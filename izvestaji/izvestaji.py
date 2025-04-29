from datetime import datetime, date, timedelta

"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: str) -> list:
    lista=[]
    for key in sve_karte:
        if sve_karte[key]['datum_prodaje']==dan:
            lista.append(sve_karte[key])
    return lista

"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    lista=[]
    for key in sve_karte:
        konkretna_sifra=sve_karte[key]['sifra_konkretnog_leta']
        if konkretna_sifra in svi_konkretni_letovi:
            if svi_konkretni_letovi[konkretna_sifra]['datum_i_vreme_polaska'].date()==dan:
                lista.append(sve_karte[key])
    return lista

"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""
def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: str, prodavac: str) -> list:
    lista=[]
    for key in sve_karte:   #tip dana je ipak datetime, ne date
        if sve_karte[key]['prodavac']['korisnicko_ime']==prodavac and sve_karte[key]['datum_prodaje']==dan:
            lista.append(sve_karte[key])
    return lista

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: str
) -> tuple:
    broj_prodatih = suma = 0
    for key in sve_karte:
        if sve_karte[key]['datum_prodaje'] == dan:
            broj_prodatih += 1
            konkretna_sifra = sve_karte[key]['sifra_konkretnog_leta']
            broj_leta = svi_konkretni_letovi[konkretna_sifra]['broj_leta']
            suma += svi_letovi[broj_leta]['cena']

    return broj_prodatih, suma


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_polaska(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date
) -> tuple:
    broj_prodatih = suma = 0
    for key in sve_karte:
        konkretna_sifra=sve_karte[key]['sifra_konkretnog_leta']
        if svi_konkretni_letovi[konkretna_sifra]['datum_i_vreme_polaska'].date()==dan:
            broj_prodatih+=1
            broj_leta=svi_konkretni_letovi[konkretna_sifra]['broj_leta']
            suma+=svi_letovi[broj_leta]['cena']

    return broj_prodatih, suma

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
    sve_karte: dict,
    konkretni_letovi: dict,
    svi_letovi: dict,
    dan: str,
    prodavac: str
) -> tuple:
    broj_prodatih = suma = 0
    for key in sve_karte:
        if sve_karte[key]['prodavac']['korisnicko_ime'] == prodavac and sve_karte[key]['datum_prodaje']==dan:
            broj_prodatih += 1
            konkretna_sifra = sve_karte[key]['sifra_konkretnog_leta']
            broj_leta = konkretni_letovi[konkretna_sifra]['broj_leta']
            suma += svi_letovi[broj_leta]['cena']

    return broj_prodatih, suma

"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict
) -> dict: #ubc znaci ukupan broj i cena
    recnik={}
    danas=date.today()
    granicni_datum=danas-timedelta(days=30)
    lista_prodavaca=[]
    broj_prodatih=[]
    suma=[]

    for key in sve_karte:
        if sve_karte[key]['prodavac']['korisnicko_ime'] not in lista_prodavaca:
            lista_prodavaca.append(sve_karte[key]['prodavac']['korisnicko_ime'])
            broj_prodatih.append(0)
            suma.append(0)
        sve_karte[key]['datum_prodaje']=datetime.strptime(sve_karte[key]['datum_prodaje'], "%d.%m.%Y.").date()


    for key in sve_karte:
        if sve_karte[key]['datum_prodaje'] >= granicni_datum:
            index = lista_prodavaca.index(sve_karte[key]['prodavac']['korisnicko_ime'])
            broj_prodatih[index]+=1
            konkretna_sifra = sve_karte[key]['sifra_konkretnog_leta']
            broj_leta = svi_konkretni_letovi[konkretna_sifra]['broj_leta']
            suma[index] += svi_letovi[broj_leta]['cena']

    for i in lista_prodavaca:
        index = lista_prodavaca.index(i)
        recnik[i]={'broj_prodatih': broj_prodatih[index], 'suma': suma[index]}

    return recnik
