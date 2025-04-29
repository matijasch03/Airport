import common.konstante
from common import konstante

"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
    if not korisnicko_ime:
        print("\nGreska! Niste uneli korisnicko_ime.")
        raise Exception("Greska! Niste uneli korisnicko_ime.")

    if uloga not in [konstante.ULOGA_ADMIN, konstante.ULOGA_KORISNIK, konstante.ULOGA_PRODAVAC]:
        print("Greska! Niste uneli ispravnu ulogu.")
        raise Exception("Greska! Niste uneli ispravnu ulogu.")

    if not lozinka:
        print("\nGreska! Niste uneli lozinku.")
        raise Exception("Greska! Niste uneli lozinku.")

    if not ime:
        print("\nGreska! Niste uneli ime.")
        raise Exception("Greska! Niste uneli ime.")

    if not prezime:
        print("\nGreska! Niste uneli prezime.")
        raise Exception("Greska! Niste uneli prezime.")

    if not email:
        print("\nGreska! Niste uneli email.")
        raise Exception("Greska! Niste uneli email.")

    if telefon == None:
        print("\nGreska! Niste uneli telefon.")
        raise Exception("Greska! Niste uneli telefon.")

    if email:
        if "@" not in email:
            print("\nGreska! Vas email ne sadrzi znak '@'.")
            raise Exception("Greska! Vas email ne sadrzi znak '@'.")
        else:
            niz = email.split("@")
            if len(niz) > 2:
                print("\nGreska! Vas email sadrzi vise od jednog znaka @.")
                raise Exception("Greska! Vas email sadrzi vise od jednog znaka @.")
            if "." not in niz[1]:
                print("\nGreska! Vas email ne sadrzi domen.")
                raise Exception("Greska! Vas email ne sadrzi domen.")
            delovi = niz[1].split('.')
            if len(delovi) > 2:
                print("\nGreska! Vas mejl ima vise od jednog domena.")
                raise Exception("Greska! Vas mejl ima vise od jednog domena.")

    if pasos:
        if pasos.isnumeric() == False:
            print("\nGreska! U broju pasosa smeju se pojaviti samo cifre.")
            raise Exception("Greska! U broju pasosa smeju se pojaviti samo cifre.")
        if len(pasos) != 9:
            print("\nGreska! Pasos treba da se sastoji od 9 cifara.")
            raise Exception("Greska! Pasos treba da se sastoji od 9 cifara.")

    if telefon != None and telefon.isnumeric() != True:
        print("\nGreska! Pri unosu broja telefona nisu koriscene cifre.")
        raise Exception("Greska! Pri unosu broja telefona nisu koriscene cifre.")

    if azuriraj:  # azuriranje postojeceg korisnika
        if staro_korisnicko_ime not in svi_korisnici:
            print("\nGreska! Uneto korisnicko ime nije pronadjeno!")
            raise Exception("Greska! Uneto korisnicko ime nije pronadjeno!")
        elif korisnicko_ime in svi_korisnici.keys() and korisnicko_ime != staro_korisnicko_ime:
            print("\nGreska! Novo korisnicko ime je vec u upotrebi.")
            raise Exception("Greska! Novo korisnicko ime je vec u upotrebi.")

        else:
            azurirani_korisnik = {korisnicko_ime: {
                'uloga': uloga,
                'korisnicko_ime': korisnicko_ime,
                'lozinka': lozinka,
                'ime': ime,
                'prezime': prezime,
                'email': email,
                'pasos': pasos,
                'drzavljanstvo': drzavljanstvo,
                'telefon': telefon,
                'pol': pol}}
            del svi_korisnici[staro_korisnicko_ime]
            svi_korisnici.update(azurirani_korisnik)
            return svi_korisnici

    else:  # dodaje se novi korisnik
        if korisnicko_ime in svi_korisnici:
                print("\nGreska! Uneto korisnicko ime vec postoji.")
                raise Exception("Greska! Uneto korisnicko ime vec postoji.")

        svi_korisnici[korisnicko_ime] = {}
        svi_korisnici[korisnicko_ime]['korisnicko_ime'] = korisnicko_ime
        svi_korisnici[korisnicko_ime]['uloga'] = uloga
        svi_korisnici[korisnicko_ime]['lozinka'] = lozinka
        svi_korisnici[korisnicko_ime]['ime'] = ime
        svi_korisnici[korisnicko_ime]['prezime'] = prezime
        svi_korisnici[korisnicko_ime]['email'] = email
        svi_korisnici[korisnicko_ime]['pasos'] = pasos
        svi_korisnici[korisnicko_ime]['drzavljanstvo'] = drzavljanstvo
        svi_korisnici[korisnicko_ime]['telefon'] = telefon
        svi_korisnici[korisnicko_ime]['pol'] = pol
        return svi_korisnici


"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    with open(putanja, "w") as file:
        for key in svi_korisnici:
            file.write(
                svi_korisnici[key]['ime'] + separator + svi_korisnici[key]['prezime'] + separator + svi_korisnici[key][
                    'korisnicko_ime'] + separator + svi_korisnici[key]['lozinka'] + separator + svi_korisnici[key][
                    'email'] + separator + svi_korisnici[key]['pasos'] + separator + svi_korisnici[key][
                    'drzavljanstvo'] + separator + svi_korisnici[key]['telefon'] + separator + svi_korisnici[key][
                    'pol'] + separator + svi_korisnici[key]['uloga'] + '\n')

"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    recnik = {}
    with open(putanja, 'r') as file:
        for red in file:
            items = red.split(separator)
            recnik[items[2]] = {"ime": items[0], 'prezime': items[1], 'korisnicko_ime': items[2], 'lozinka': items[3],
                                'email': items[4], 'pasos': items[5], 'drzavljanstvo': items[6], 'telefon': items[7],
                                'pol': items[8], 'uloga': items[9].strip()}
    return recnik

"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnicko_ime, lozinka)->dict:
    if korisnicko_ime in svi_korisnici.keys():
        if lozinka == svi_korisnici[korisnicko_ime]['lozinka']:
            return svi_korisnici[korisnicko_ime]
        else:
            print("Greska! Netacna lozinka.")
            raise Exception("Greska! Netacna lozinka.")
    else:
        print("Greska! Ne postoji korisnik sa datim korisnickim imenom.")
        raise Exception("Greska! Ne postoji korisnik sa datim korisnickim imenom.")

"""
Funkcija koja vrsi log out
*
"""
def logout(korisnicko_ime: str):
    pass

