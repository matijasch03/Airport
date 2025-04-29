from datetime import datetime, timedelta

def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict):
    redni_broj=0 #primarni kljuc
    for redni_broj in svi_konkretni_letovi:
        redni_broj+=1

    podeli_vreme=let['vreme_poletanja'].split(':')
    sati=int(podeli_vreme[0])
    minuti=int(podeli_vreme[1])
    vreme_poletanja=60*sati+minuti #vreme koje treba dodati na polazak_date da bi se dobilo datum_i_vreme_poletanja
    polazak_date=let['datum_pocetka_operativnosti']-timedelta(minutes=let['datum_pocetka_operativnosti'].minute)\
                 -timedelta(hours=let['datum_pocetka_operativnosti'].hour)+timedelta(minutes=vreme_poletanja)
    dolazak_date=let['datum_pocetka_operativnosti']

    for i in let['dani']:
        redni_broj+=1
        novi_polazak_date = polazak_date + timedelta(days=i)
        novi_dolazak_date = dolazak_date + timedelta(days=i)
        novi_konkertan_let={'sifra': redni_broj, 'broj_leta': let['broj_leta'],
                            'datum_i_vreme_polaska': novi_polazak_date, 'datum_i_vreme_dolaska': novi_dolazak_date}
        svi_konkretni_letovi[redni_broj]=novi_konkertan_let

    return svi_konkretni_letovi

def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    with open(putanja, 'w') as file:
        for key in svi_konkretni_letovi:
            polazak_date=svi_konkretni_letovi[key]['datum_i_vreme_polaska'].strftime('%H:%M:%S %d.%m.%Y.')
            dolazak_date=svi_konkretni_letovi[key]['datum_i_vreme_dolaska'].strftime('%H:%M:%S %d.%m.%Y.')

            file.write(str(svi_konkretni_letovi[key]['sifra'])+separator+svi_konkretni_letovi[key]['broj_leta']
           +separator+polazak_date+separator+dolazak_date+separator+str(svi_konkretni_letovi[key]['zauzetost'])+'\n')

def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    dictionary = {}
    with open(putanja, 'r') as file:
        for row in file:
            items = row.split(separator)
            polazak_date=datetime.strptime(items[2], '%H:%M:%S %d.%m.%Y.')
            dolazak_date=datetime.strptime(items[3], '%H:%M:%S %d.%m.%Y.')

            dictionary[int(items[0])] = {'sifra': int(items[0]), 'broj_leta': items[1], 'datum_i_vreme_polaska': polazak_date,
                                    'datum_i_vreme_dolaska': dolazak_date, 'zauzetost': eval(items[4])}
    return dictionary
