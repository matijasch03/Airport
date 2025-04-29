from common import konstante
from functools import reduce
from datetime import datetime
from korisnici import korisnici
from konkretni_letovi import konkretni_letovi
import csv

"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
sledeci_broj_karte = 1

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs
) -> (dict, dict):

    ima_slobodnih = False
    br_sedista=br_reda=0
    for red in slobodna_mesta:
        for sediste in red:
            if not sediste:
                ima_slobodnih = True
                br_sedista=red.index(sediste)
                br_reda=slobodna_mesta.index(red)
                svi_konkretni_letovi[sifra_konkretnog_leta]['zauzetost'][br_reda][br_sedista]=True
                konkretni_letovi.sacuvaj_kokretan_let('spisak_konkretnih.csv', '|', svi_konkretni_letovi)
                break
        if ima_slobodnih:
            break

    if not ima_slobodnih:
        print('\nGreska! Nema slobodnih mesta.')
        raise Exception('Greska! Nema slobodnih mesta.')

    if sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise Exception("Greska! Ovaj konkretan let ne postoji.")

    br_karte=1
    for karta in sve_karte:
        br_karte = br_karte + 1

    br_reda+=1
    br_sedista+=1
    karta = {'broj_karte': br_karte, 'putnici': putnici, 'sifra_konkretnog_leta': sifra_konkretnog_leta,
                 'status': konstante.STATUS_NEREALIZOVANA_KARTA, 'kupac': kupac, 'prodavac': kwargs['prodavac'],
                 'datum_prodaje': kwargs['datum_prodaje'], 'obrisana': False, 'sediste': str(br_reda)+'. red, '+str(br_sedista)+'. sediste'}
    sve_karte[br_karte]=karta
    return karta, sve_karte


def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter):

    lista_nerealizovanih_karata = []
    for i in sve_karte:  # i je recnik s podacima jedne karte
        if i['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
            for j in i['putnici']:  # u kolekciji i['putnici'] nalaze se recnici korisnika
                if j == korisnik:  # j je jedan od njih
                    lista_nerealizovanih_karata.append(i)
    return lista_nerealizovanih_karata

"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,    #broj karte koju treba izmeniti
    nova_sifra_konkretnog_leta: int=None,
    nov_datum_polaska: datetime=None,
    sediste=None        #vrednosti koje treba izmeniti karti sa datim brojem
) -> dict:
    for key in svi_konkretni_letovi:
        if svi_konkretni_letovi[key]['sifra']==nova_sifra_konkretnog_leta:
            if nov_datum_polaska:
                svi_konkretni_letovi[key]['datum_i_vreme_polaska']=nov_datum_polaska

    for key in sve_karte:
        if sve_karte[key]['broj_karte']==broj_karte:
            if nova_sifra_konkretnog_leta:
                sve_karte[key]['sifra_konkretnog_leta']=nova_sifra_konkretnog_leta
            if sediste:
                sve_karte[key]['sediste']=sediste

    return sve_karte

"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:

    ima_karte=False
    indeks_karte_u_dict=0
    for key in sve_karte:
        if sve_karte[key]['broj_karte']==broj_karte:
            ima_karte=True
            indeks_karte_u_dict=key
            break
    if not ima_karte:
        print('\nGreska! Uneli ste nepostojeci broj karte.')
        raise Exception

    uloga_osobe=korisnik['uloga']
    if uloga_osobe==konstante.ULOGA_KORISNIK:
        print('\nGreska! Korisnik nema pravo da brise kartu.')
        raise Exception
    elif uloga_osobe==konstante.ULOGA_PRODAVAC:
        sve_karte[indeks_karte_u_dict]['obrisana']=True
    else: #uloga osobe je menadzer
        del sve_karte[indeks_karte_u_dict]

    return sve_karte

"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: datetime="",
                             korisnicko_ime_putnika: str="")->list:
    lista_karata=[]
    for key in svi_letovi:
        if (not polaziste or polaziste==svi_letovi[key]['sifra_polazisnog_aerodroma']) and \
                (not odrediste or odrediste == svi_letovi[key]['sifra_odredisnog_aerodorma']):
            for konkretan_key in svi_konkretni_letovi:
                if key==svi_konkretni_letovi[konkretan_key]['broj_leta']:
                    if (not datum_polaska or datum_polaska==svi_konkretni_letovi[konkretan_key]['datum_i_vreme_polaska']) and \
                            (not datum_dolaska or datum_dolaska == svi_konkretni_letovi[konkretan_key]['datum_i_vreme_dolaska']):
                        for card_key in sve_karte:
                            if konkretan_key==sve_karte[card_key]['sifra_konkretnog_leta']:
                                if not korisnicko_ime_putnika:
                                    lista_karata.append(sve_karte[card_key])
                                else:
                                    for i in sve_karte[card_key]['putnici']:
                                        if i==korisnicko_ime_putnika:
                                            lista_karata.append(sve_karte[card_key])
                                            break #da ne bi dodao istu kartu u kolekciju, jer je za vise putnika ista karta
    return lista_karata

"""
Funkcija čuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja, 'a') as fajl:
        for kljuc in sve_karte:
            fajl.write(str(sve_karte[kljuc]['broj_karte'])+separator+
                           str(sve_karte[kljuc]['sifra_konkretnog_leta']) + separator+
                           str(sve_karte[kljuc]['kupac'])+separator+str(sve_karte[kljuc]['prodavac'])+
                           separator+str(sve_karte[kljuc]['sediste']) + separator +
                           sve_karte[kljuc]['datum_prodaje'] + separator + str(sve_karte[kljuc]['obrisana'])+
                           separator+str(sve_karte[kljuc]['putnici'])+separator+sve_karte[kljuc]['status']+'\n')
            # moras uraditi i iducu funkciju da bi test radio :)

def azuriraj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja, 'w') as fajl:
        for kljuc in sve_karte:
            fajl.write(str(sve_karte[kljuc]['broj_karte'])+separator+
                           str(sve_karte[kljuc]['sifra_konkretnog_leta']) + separator+
                           str(sve_karte[kljuc]['kupac'])+separator+str(sve_karte[kljuc]['prodavac'])+
                           separator+str(sve_karte[kljuc]['sediste']) + separator +
                           sve_karte[kljuc]['datum_prodaje'] + separator + str(sve_karte[kljuc]['obrisana'])+
                           separator+str(sve_karte[kljuc]['putnici'])+separator+sve_karte[kljuc]['status']+'\n')

"""
Funkcija učitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
"""

def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    recnik = {}
    with open(putanja, 'r') as fajl:
        for red in fajl:
            items = red.split(separator)
            obrisana = False
            if items[6] == 'True':
                obrisana = True
            recnik[int(items[0])] = {'broj_karte': int(items[0]), 'sifra_konkretnog_leta': int(items[1]),
                                     'kupac': eval(items[2]), 'prodavac': eval(items[3]), 'sediste': items[4],
                                     'datum_prodaje': items[5], 'obrisana': obrisana, 'putnici':eval(items[7]),
                                     'status': items[8].strip()}
    return recnik
