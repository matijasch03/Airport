

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    if not skracenica or not pun_naziv or not grad or not drzava:
        raise Exception('Greska! niste uneli neki od parametara.')

    nov_aerodrom={'skracenica': skracenica, 'pun_naziv': pun_naziv, 'grad': grad, 'drzava': drzava}
    svi_aerodromi[skracenica]=nov_aerodrom
    return svi_aerodromi

"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, 'a') as file:
        for key in svi_aerodromi:
            file.write(svi_aerodromi[key]['skracenica']+separator+svi_aerodromi[key]['pun_naziv']+separator+
                       svi_aerodromi[key]['grad']+separator+svi_aerodromi[key]['drzava']+'\n')

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    dictionary={}
    with open(putanja, 'r') as file:
        for row in file:
            items=row.split(separator)
            dictionary[items[0]]={'skracenica': items[0], 'pun_naziv': items[1], 'grad': items[2], 'drzava':items[3].strip()}
    return dictionary