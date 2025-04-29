from datetime import datetime, date, timedelta
from common import konstante
"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
#fja vraca listu predstojecih (nerealizovanih) letova
#kriterij: da li se datum pocetka operativnosti nalazi u buducnosti
def pregled_nerealizoivanih_letova(svi_letovi: dict):
    lista_nerealizovanih_letova=[]
    for key in svi_letovi:
        if svi_letovi[key]['datum_pocetka_operativnosti']>datetime.now():
            lista_nerealizovanih_letova.append(svi_letovi[key])
    return lista_nerealizovanih_letova
"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    # konkretni_letovi sluze samo da bi bili vraceni u listu, prilikom provere se moze raditi samo sa svi_letovi
    lista_letova = []
    for key in svi_letovi:
        if (polaziste == svi_letovi[key]['sifra_polazisnog_aerodroma'] or not polaziste) and \
                (odrediste == svi_letovi[key]['sifra_odredisnog_aerodorma'] or not odrediste) and \
                (vreme_poletanja == svi_letovi[key]['vreme_poletanja'] or not vreme_poletanja) and \
                (vreme_sletanja == svi_letovi[key]['vreme_sletanja'] or not vreme_sletanja) and \
                (prevoznik == svi_letovi[key]['prevoznik'] or not prevoznik):
            for konkretan_key in konkretni_letovi:
                if konkretni_letovi[konkretan_key]['broj_leta'] == key:
                    if (datum_polaska == konkretni_letovi[konkretan_key][
                        'datum_i_vreme_polaska'] or datum_polaska == None or datum_polaska == '') and \
                            (datum_dolaska == konkretni_letovi[konkretan_key][
                                'datum_i_vreme_dolaska'] or datum_dolaska == None or datum_dolaska == ''):
                        lista_letova.append(konkretni_letovi[konkretan_key])

    return lista_letova

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str,
                     sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None ,
                    datum_kraja_operativnosti: datetime = None):
    if not broj_leta or not sifra_polazisnog_aerodroma or not sifra_odredisnog_aerodorma or not vreme_poletanja or not vreme_sletanja or sletanje_sutra == None or not prevoznik or not dani or not model or not cena:
        raise Exception('Greska! Niste uneli sve parametre.')

    let_int = int(broj_leta[2:4])
    if len(broj_leta) != 4 or let_int < 10 or let_int > 99:
        print('\nGreska! Broj leta nema odgovarajuci format.')
        raise Exception

    if cena < 0:
        print('\nGreska! Cena leta mora biti nenegativan broj.')
        raise Exception

    vr1 = vreme_poletanja.split(':')
    sati1 = int(vr1[0])
    min1 = int(vr1[1])
    if len(vr1) != 2 or sati1 < 0 or sati1 > 23 or min1 < 0 or min1 > 59:
        print('\nGreska! Vreme poletanja nije u odgovarajucem formatu.')
        raise Exception

    vr2 = vreme_sletanja.split(':')
    sati2 = int(vr2[0])
    min2 = int(vr2[1])
    if len(vr2) != 2 or sati2 < 0 or sati2 > 23 or min2 < 0 or min2 > 59:
        print('\nGreska! Vreme sletanja nije u odgovarajucem formatu.')
        raise Exception

    novi_let = {'broj_leta': broj_leta, 'sifra_polazisnog_aerodroma': sifra_polazisnog_aerodroma,
                'sifra_odredisnog_aerodorma': sifra_odredisnog_aerodorma, 'vreme_poletanja': vreme_poletanja,
                'vreme_sletanja': vreme_sletanja, 'sletanje_sutra': sletanje_sutra, 'prevoznik': prevoznik,
                'cena': cena, 'datum_pocetka_operativnosti': datum_pocetka_operativnosti,
                'datum_kraja_operativnosti': datum_kraja_operativnosti}
    svi_letovi[broj_leta] = novi_let
    return svi_letovi
"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(
    svi_letovi : dict,
    broj_leta: str,
    sifra_polazisnog_aerodroma: str,
    sifra_odredisnog_aerodorma: str,
    vreme_poletanja: str,
    vreme_sletanja: str,
    sletanje_sutra: bool,
    prevoznik: str,
    dani: list,
    model: dict,
    cena: float,
    datum_pocetka_operativnosti: datetime,
    datum_kraja_operativnosti: datetime
) -> dict:
    if broj_leta not in svi_letovi:
        raise Exception('Greska! Uneti broj leta je nepostojeci.')
    if not broj_leta or not sifra_polazisnog_aerodroma or not sifra_odredisnog_aerodorma or not vreme_poletanja or not vreme_sletanja or sletanje_sutra == None or not prevoznik or not dani or not model or not cena:
        raise Exception('Greska! Niste uneli sve parametre.')
    if len(sifra_odredisnog_aerodorma) != 3:
        raise Exception('Greska! Sifra odredista nema trazenu duzinu.')
    if len(sifra_polazisnog_aerodroma) != 3:
        raise Exception('Greska! Sifra polazista nema trazenu duzinu.')

    vr1 = vreme_poletanja.split(':')
    sati1 = int(vr1[0])
    min1 = int(vr1[1])
    if len(vr1) != 2 or sati1 < 0 or sati1 > 23 or min1 < 0 or min1 > 59:
        raise Exception('Greska! Vreme poletanja nije u odgovarajucem formatu.')

    vr2 = vreme_sletanja.split(':')
    sati2 = int(vr2[0])
    min2 = int(vr2[1])
    if len(vr2) != 2 or sati2 < 0 or sati2 > 23 or min2 < 0 or min2 > 59:
        raise Exception('Greska! Vreme sletanja nije u odgovarajucem formatu.')

    if not sletanje_sutra:
        if datum_pocetka_operativnosti >= datum_kraja_operativnosti:
            raise Exception('Greska! Nemoguce da je avion pre dosao nego sto je krenuo.')

    if cena < 0:
        raise Exception('Greska! Cena leta mora biti nenegativan broj.')

    for key in svi_letovi:
        if key == broj_leta:
            svi_letovi[key]['sifra_polazisnog_aerodroma'] = sifra_polazisnog_aerodroma
            svi_letovi[key]['sifra_odredisnog_aerodorma'] = sifra_odredisnog_aerodorma
            svi_letovi[key]['vreme_poletanja'] = vreme_poletanja
            svi_letovi[key]['vreme_sletanja'] = vreme_sletanja
            svi_letovi[key]['sletanje_sutra'] = sletanje_sutra
            svi_letovi[key]['prevoznik'] = prevoznik
            svi_letovi[key]['dani'] = dani
            svi_letovi[key]['model'] = model
            svi_letovi[key]['cena'] = cena
            svi_letovi[key]['datum_kraja_operativnosti'] = datum_kraja_operativnosti
            svi_letovi[key]['datum_pocetka_operativnosti'] = datum_pocetka_operativnosti
    return svi_letovi
"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, 'a') as fajl:
        for key in svi_letovi:

            sletanje_sutra = 'False'
            if svi_letovi[key]['sletanje_sutra']:
                sletanje_sutra = 'True'

            datum_pocetka=datum_kraja=''
            if svi_letovi[key]['datum_pocetka_operativnosti']:
                datum_pocetka=svi_letovi[key]['datum_pocetka_operativnosti'].strftime('%H:%M:%S %d.%m.%Y.')
            if svi_letovi[key]['datum_kraja_operativnosti']:
                datum_kraja=svi_letovi[key]['datum_kraja_operativnosti'].strftime('%H:%M:%S %d.%m.%Y.')

            fajl.write(
                svi_letovi[key]['broj_leta'] + separator + svi_letovi[key]['sifra_odredisnog_aerodorma'] + separator +
                svi_letovi[key]['sifra_polazisnog_aerodroma'] + separator + svi_letovi[key]['vreme_poletanja'] + separator +
                svi_letovi[key]['vreme_sletanja'] + separator + sletanje_sutra + separator + svi_letovi[key]['prevoznik'] +
                separator + str(svi_letovi[key]['cena']) + separator + datum_pocetka + separator + datum_kraja + '\n')

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    recnik = {}
    with open(putanja, 'r') as file:
        for row in file:
            items = row.split(separator)
            sletanje_sutra = False
            if items[5] == 'True':
                sletanje_sutra = True

            if items[8]:
                datum_pocetka=datetime.strptime(items[8], '%H:%M:%S %d.%m.%Y.')
            if items[9].strip():
                datum_kraja=datetime.strptime(items[9].strip(), '%H:%M:%S %d.%m.%Y.')

            recnik[items[0]] = {'broj_leta': items[0], 'sifra_odredisnog_aerodorma': items[1],
                                'sifra_polazisnog_aerodroma': items[2], 'vreme_poletanja': items[3],
                                'vreme_sletanja': items[4], 'sletanje_sutra': sletanje_sutra,
                                'prevoznik': items[6], 'cena': float(items[7]),
                                'datum_pocetka_operativnosti': datum_pocetka, 'datum_kraja_operativnosti': datum_kraja}
    return recnik

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi: dict, konkretni_let: dict):
    konkretni_let['zauzetost']=[]
    for broj_leta in svi_letovi:
        if broj_leta==konkretni_let['broj_leta']:
            for i in range(svi_letovi[broj_leta]['model']['broj_redova']):
                red = []
                for j in svi_letovi[broj_leta]['model']['pozicije_sedista']:
                    red.append(False)
                konkretni_let['zauzetost'].append(red)

"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretni_let: dict) -> list:
    return konkretni_let['zauzetost']

'''
Funkcija koja vraća listu od 10 najjeftinijih letova od određenog polazišta do odredišta
'''
def prikaz_10_najjeftinijih_letova(odrediste: str, polaziste: str, svi_letovi: dict)->list:
    cene=[]
    lista_10_letova=[]
    lista_10_sortiranih=[]
    for key in svi_letovi:
        if svi_letovi[key]['sifra_odredisnog_aerodorma']==odrediste and svi_letovi[key]['sifra_polazisnog_aerodroma']==polaziste:
            cene.append(svi_letovi[key]['cena'])
            lista_10_letova.append(svi_letovi[key])
    if not cene:
        print('\nNema letova na unesenoj relaciji.')
    else:
        if len(cene)>10:
            cene.sort()
            for i in range(10, len(cene)):
                cene.remove(cene[10])
        cene.sort(reverse=True)
        okidac_brejka=0 #uklanja visak elemenata sa najvisom cenom, da ako vise njih imaju najvisu najnizu cenu, samo jedan udje u listu
        for i in cene:
            for j in lista_10_letova:
                key=j['broj_leta']
                if svi_letovi[key]['cena']==i:
                    okidac_brejka+=1
                    lista_10_sortiranih.append(j)
                    lista_10_letova.remove(j)
                    if okidac_brejka==1:
                        break
    if len(lista_10_sortiranih)<10 and len(lista_10_sortiranih)>0:
        print('\nIma samo', str(len(lista_10_sortiranih)), 'let(ova) na datoj relaciji.')
    return lista_10_sortiranih
'''
#TEST ZA 10 NAJJEFTINIJIH LETOVA
l={1:{'broj_leta': 1, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':2},
   2:{'broj_leta': 2, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':1},
   3:{'broj_leta': 3, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':23},
   4:{'broj_leta': 4, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':5},
   5:{'broj_leta': 5, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':6},
   6:{'broj_leta': 6, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':4},
   7:{'broj_leta': 7, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':2},
   8:{'broj_leta': 8, 'sifra_odredisnog_aerodorma': 'a', 'sifra_polazisnog_aerodroma':'b', 'cena':5}}
p=prikaz_10_najjeftinijih_letova('a', 'b', l)
print(p)
'''
"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta, konkretni_let: dict, red: int, sediste: int) -> (dict, dict):
    sada=datetime.now()
    if konkretni_let['datum_i_vreme_polaska']-sada<=timedelta(days=2):
        if not konkretni_let['zauzetost'][red][sediste]:
            konkretni_let['zauzetost'][red][sediste]=True
            karta['status']=konstante.STATUS_REALIZOVANA_KARTA
        else: print('Ovo mesto je vec rezervisano. Molimo Vas da izaberete neko koje je slobodno.')
    else: print('Zao nam je, ali istekao je predvidjen rok od 48 sati za potvrdu leta.')
    return karta, konkretni_let

"""
Funkcija koja vraća listu letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""
def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    lista_poveznih_letova=[]
    polaziste = ''
    for key in svi_letovi:
        if key == konkretni_let['broj_leta']:
            polaziste = svi_letovi[key]['sifra_odredisnog_aerodorma']  # novo polaziste je staro odrediste
            vreme_sletanja=int(svi_letovi[key]['vreme_sletanja'].split(':')[0])*60+int(svi_letovi[key]['vreme_sletanja'].split(':')[1])
            break
    for key in svi_letovi:
        if svi_letovi[key]['sifra_polazisnog_aerodroma']==polaziste:
            vreme_poletanja=int(svi_letovi[key]['vreme_poletanja'].split(':')[0])*60+int(svi_letovi[key]['vreme_poletanja'].split(':')[1])
            if 0<(vreme_poletanja-vreme_sletanja)<=120:
                lista_poveznih_letova.append(svi_letovi[key])
    return lista_poveznih_letova


"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    lista_konk_letova=[]
    for key in svi_letovi:
        if svi_letovi[key]['sifra_polazisnog_aerodroma']==polaziste and svi_letovi[key]['sifra_odredisnog_aerodorma']==odrediste:
            for konkretni_key in konkretni_letovi:
                if konkretni_letovi[konkretni_key]['broj_leta']==key:
                    donja_gr_polaska=konkretni_letovi[konkretni_key]['datum_i_vreme_polaska'].date()-timedelta(days=broj_fleksibilnih_dana)
                    gornja_gr_polaska=konkretni_letovi[konkretni_key]['datum_i_vreme_polaska'].date()+timedelta(days=broj_fleksibilnih_dana)
                    donja_gr_dolaska=konkretni_letovi[konkretni_key]['datum_i_vreme_dolaska'].date()-timedelta(days=broj_fleksibilnih_dana)
                    gornja_gr_dolaska=konkretni_letovi[konkretni_key]['datum_i_vreme_dolaska'].date()+timedelta(days=broj_fleksibilnih_dana)

                    if datum_polaska>=donja_gr_polaska and datum_polaska<=gornja_gr_polaska and \
                        datum_dolaska>=donja_gr_dolaska and datum_dolaska<=gornja_gr_dolaska:
                        konkretni_letovi[konkretni_key]['cena']=round(svi_letovi[key]['cena'], 2)
                        lista_konk_letova.append(konkretni_letovi[konkretni_key])

    lista_sort = sorted(lista_konk_letova, key=lambda let: -let["cena"])

    return lista_sort

