import random

from prettytable import PrettyTable
from aerodromi import aerodromi
from common import konstante
from izvestaji import izvestaji
from karte import karte
from konkretni_letovi import konkretni_letovi
from korisnici import korisnici
from letovi import letovi
from model_aviona import model_aviona
from datetime import datetime, date, timedelta

def menu():
    print('\n***** ***** *****\n')
    print('Postovani, \nDobro dosli u meni kompanije "Dvavago"! \n')

    print('1. opcija: Prijava na sistem')
    print('2. opcija: Registracija novog korisnika')
    print('0. opcija: Izlazak iz aplikacije')

def korisnicki_meni():
    print('\n***** ***** *****\n')
    print('Dobro dosli u korisnicki meni!')

    print('1. opcija: Izmena Vasih vlastitih podataka u bazi')
    print('2. opcija: Pregled nerealizovanih letova')
    print('3. opcija: Pretraga letova po kriterijumu')
    print('4. opcija: Prikaz 10 najjeftinijih letova na relaciji po Vasem izboru')
    print('5. opcija: Prikaz fleksibilnih letova')
    print('0. opcija: Izlazak iz korisnickog menija (odjava)')

def specificni_meni(uloga):
    print('_'*10)
    if uloga==konstante.ULOGA_KORISNIK:
        print('6. opcija: Kupovina karte')
        print('7. opcija: Pregled nerealizovanih karata')
        print('8. opcija: Potvrda leta 48 sati pre polaska (check in)')
    elif uloga==konstante.ULOGA_PRODAVAC:
        print('6. opcija: Prodaja karata')
        print('7. opcija: Check in za kupca')
        print('8. opcija: Izmena karte')
        print('9. opcija: Brisanje karte')
        print('10. opcija: Pretraga prodatih karata')
    elif uloga==konstante.ULOGA_ADMIN:
        print('6. opcija: Pretraga prodatih karata')
        print('7. opcija: Registrovanje novog prodavca')
        print('8. opcija: Kreiranje novog leta')
        print('9. opcija: Brisanje karata')
        print('10. opcija: Izvestaj za dan prodaje')
        print('11. opcija: Izvestaj za dan polaska')
        print('12. opcija: Izvestaj za dan prodaje i prodavca')
        print('13. opcija: Ukupan broj i cena (ubc) za dan prodaje')
        print('14. opcija: Ubc za dan polaska')
        print('15. opcija: Ubc za dan prodaje i prodavca')
        print('16. opcija: Ubc u poslednjih 30 dana')

    else:
        print('\nGreska! Korisnik nema adekvatnu ulogu.')

#ISPIS KORISNICKOG MENIJA
def prikazi_korisnicki_meni(logovani_korisnik):
    korisnicki_meni()
    specificni_meni(logovani_korisnik['uloga'])
    opcija = input('Molimo izaberite neku od opcija iz korisnickog menija: ')
    while opcija !='0':
        if opcija=='1': azuriranje_podataka()
        elif opcija=='2': pregled_nerealizovanih_letova()
        elif opcija=='3': pretraga_letova()
        elif opcija=='4': prikaz_10_najjeftinijih_letova()
        elif opcija=='5': fleksibilni_polasci()
        else:
            if logovani_korisnik['uloga']==konstante.ULOGA_KORISNIK:
                if opcija=='6':
                    try:
                        sifra_konkretnog_leta = int(input('Molimo Vas unesite sifru zeljenog konkretnog leta: '))
                    except:
                        print('Uneta vrednost sifre mora biti broj.')
                        prikazi_korisnicki_meni(logovani_korisnik)
                    prodavac = {'korisnicko_ime': random.choice(['prodavac_1', 'prodavac_2', 'prodavac_3']), 'uloga': 'prodavac'}
                    kupovina_karte(logovani_korisnik, logovani_korisnik, sifra_konkretnog_leta, 'ste to Vi', prodavac)

                elif opcija=='7': pregled_nerealizovanih_karata(logovani_korisnik)
                elif opcija=='8':
                    sve_karte = karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
                    lista_nerealizovanih_karata = []
                    for key in sve_karte:
                        if sve_karte[key]['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
                            if sve_karte[key]['kupac']['korisnicko_ime'] == logovani_korisnik['korisnicko_ime']:
                                lista_nerealizovanih_karata.append(sve_karte[key]['broj_karte'])
                    print('Lista nerealizovanih karata: ', lista_nerealizovanih_karata)
                    try:
                        broj_karte = int(input('Izaberite broj karte za koju zelite da obavite check in: '))
                    except:
                        print("Greska. Uneti broj karte nije u listi.")
                        pregled_nerealizovanih_karata(logovani_korisnik)
                    checkin(logovani_korisnik, broj_karte, lista_nerealizovanih_karata)

            elif logovani_korisnik['uloga']==konstante.ULOGA_PRODAVAC:
                if opcija=='6': prodaja_karata(logovani_korisnik)
                elif opcija=='7': checkin_prodavac(logovani_korisnik)
                elif opcija=='8': izmena_karte(logovani_korisnik)
                elif opcija=='9': brisanje_karte(logovani_korisnik)
                elif opcija=='10': pretraga_karata(logovani_korisnik)


            elif logovani_korisnik['uloga']==konstante.ULOGA_ADMIN:
                if opcija=='6': prodaja_karata(logovani_korisnik)
                elif opcija=='7': registracija('njegovo', 'njegov', logovani_korisnik)
                elif opcija=='8': kreiranje_leta(logovani_korisnik)
                elif opcija=='9': brisanje_karte_admin(logovani_korisnik)
                elif opcija=='10': izvestaj_dan_prodaje(logovani_korisnik)
                elif opcija=='11': izvestaj_dan_polaska(logovani_korisnik)
                elif opcija=='12': izvestaj_prodavac_i_dan_prodaje(logovani_korisnik)
                elif opcija=='13': ubc_dan_prodaje(logovani_korisnik)
                elif opcija=='14': ubc_dan_polaska(logovani_korisnik)
                elif opcija=='15': ubc_prodavac_i_dan_prodaje(logovani_korisnik)
                elif opcija=='16': ubc_30_dana()

            else: print('\nUneli ste nepostojecu opciju. Molimo Vas da pokusate ponovo.\n')

        korisnicki_meni()
        specificni_meni(logovani_korisnik['uloga'])
        opcija = input('Molimo izaberite neku od opcija iz korisnickog menija: ')
    print(f'Postovani korisnice {logovani_korisnik["korisnicko_ime"]}, uspesno ste se izlogovali.')


#1. OPCIJA OPSTEG MENIJA
def login():
    print('\n')
    korisnicko_ime=input('Molimo unesite Vase korisnicko ime: ')
    lozinka=input('Molimo unesite Vasu lozinku: ')
    svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('ljudi.csv', '|')

    try:
        logovani_korisnik=korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        prikazi_korisnicki_meni(logovani_korisnik)
    except:
        print('\nDoslo je do greske.')

#koristi se za moguce none vrednosti kod registracije
def none_operand(vase_sta)->str:
    operand=''
    mozda = int(input(
        f'Da li ste voljni da unesete {vase_sta}?\nUkoliko jeste, pritisnite 1. U suprotnom pritisnite 0: '))
    if mozda == 1:
        operand = input(f'Molimo unesite {vase_sta}: ')
        return operand
    elif mozda==0:
        return operand

#2. OPCIJA OPSTEG MENIJA
def registracija(txt1, txt2, logovani_korisnik):
    print('\n')
    svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('ljudi.csv', '|')
    korisnicko_ime=input(f'Molimo unesite {txt1} korisnicko ime: ')
    lozinka=input(f'Molimo unesite {txt2}u lozinku: ')
    ime=input(f'Molimo unesite {txt1} ime: ')
    prezime=input(f'Molimo unesite {txt1} prezime: ')
    email=input(f'Molimo unesite {txt2} email: ')
    telefon=input(f'Molimo unesite {txt2} telefon: ')
    try:
        pasos=none_operand(f'{txt2} devetocifreni broj pasosa')
        drzavljanstvo=none_operand(f'{txt1} drzavljanstvo')
        pol=none_operand(f'{txt2} pol')
    except:
        print('\nPogresno unet broj za neku od neobaveznih vrednosti (pasos, drzavljanstvo, pol)')

    try:
        if txt1=='Vase':
            novi_svi_korisnici=korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, '',
                                                           korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        elif txt1=='njegovo':
            novi_svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_PRODAVAC, '',
                                                             korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        korisnici.sacuvaj_korisnike('ljudi.csv', '|', novi_svi_korisnici)
        if txt1=='Vase': print('\nPostovani', korisnicko_ime + ', uspesno ste se registrovali.\n')
        else: print('\nPostovani administratoru, uspesno ste registrovali prodavca', korisnicko_ime+'.\n')
        if txt1=='Vase':
            logovani_korisnik = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        prikazi_korisnicki_meni(logovani_korisnik)
    except:
        print('\nMolimo pokusajte ponovo.\n\n')

#1. OPCIJA KORISNICKOG MENIJA
def azuriranje_podataka():
    print('\n')
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('ljudi.csv', '|')
    staro_korisnicko_ime = input('Molimo unesite Vase trenutno korisnicko ime: ')
    korisnicko_ime=input('Molimo unesite Vase novo korisnicko ime: ')
    lozinka = input('Molimo unesite Vasu novu lozinku: ')
    ime = input('Molimo unesite Vase novo ime: ')
    prezime = input('Molimo unesite Vase novo prezime: ')
    email = input('Molimo unesite Vas novi email: ')
    telefon = input('Molimo unesite Vas novi telefon: ')
    try:
        uloga=svi_korisnici[staro_korisnicko_ime]['uloga']
    except:
        print('Uneto korisnicko ime ne postoji.')
        azuriranje_podataka()

    try:
        pasos = none_operand('Vas devetocifreni broj pasosa')
        drzavljanstvo = none_operand('Vase drzavljanstvo')
        pol = none_operand('Vas pol')
    except:
        print('Pogresno unet broj za neku od neobaveznih vrednosti (pasos, drzavljanstvo, pol)')

    try:
        novi_svi_korisnici=korisnici.kreiraj_korisnika(svi_korisnici, True, uloga, staro_korisnicko_ime, korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        korisnici.sacuvaj_korisnike('ljudi.csv', '|', novi_svi_korisnici)
        print('\nVasi licni podaci su uspesno izmenjeni.\n')
        logovani_korisnik = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        if logovani_korisnik['uloga'] == konstante.ULOGA_KORISNIK:
            prikazi_korisnicki_meni(korisnicko_ime)
    except:
        print('\nMolimo pokusajte ponovo.\n\n')

#2. OPCIJA KORISNICKOG MENIJA
def pregled_nerealizovanih_letova():
    svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    lista_nerealizovanih_letova=letovi.pregled_nerealizoivanih_letova(svi_letovi)
    print('Broj leta   Cena       Datum pocetka op.       Datum kraja op.')
    for i in lista_nerealizovanih_letova:
        poc_datum=i['datum_pocetka_operativnosti'].strftime('%H:%M:%S %d.%m.%Y.')
        kraj_datum=i['datum_kraja_operativnosti'].strftime('%H:%M:%S %d.%m.%Y.')

        print(i['broj_leta'], '      ', str(round(i['cena'], 2)), '   ', poc_datum, '  ', kraj_datum)

#3. OPCIJA KORISNICKOG MENIJA
def pretraga_letova():
    print('\nUkoliko zelite da pretrazujete po nekom od kriterijuma, ukucajte njihove vrednosti u naznacena polja.')
    print('U suprotnom pritisnite enter i nece se uzeti u obzir dati kriterijum.')

    svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')

    polaziste=input('Sifra polazisnog aerodroma: ')
    odrediste=input('Sifra odredisnog aerodroma: ')
    datum_polaska=input('Datum polaska: ')
    datum_dolaska=input('Datum dolaska: ')
    vreme_poletanja=input('Vreme poletanja: ')
    vreme_sletanja=input('Vreme sletanja: ')
    prevoznik=input('Prevoznik: ')

    try:
        if datum_polaska:
            datum_polaska=datetime.strptime(datum_polaska, '%H:%M:%S %d.%m.%Y.')
        else: datum_polaska=None
    except:
        print('Nije unesen datum u odgovarajucem formatu sat:min:sek dan.mes.god.')

    try:
        if datum_dolaska:
            datum_dolaska=datetime.strptime(datum_dolaska, '%H:%M:%S %d.%m.%Y.')
        else: datum_dolaska=None
    except:
        print('Nije unesen datum u odgovarajucem formatu sat:min:sek dan.mes.god.')

    lista_letova=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
    if not lista_letova:
        print('\nNepostoji nijedan ovakav let.')
    else:
        print('Sifra   Broj leta      Vreme polaska             Vreme dolaska')
        for i in lista_letova:
            if int(i['sifra'])<10:
                print(i['sifra'], '     ', i['broj_leta'], '         ', i['datum_i_vreme_polaska'], '     ', i['datum_i_vreme_dolaska'])
            else:
                print(i['sifra'], '    ', i['broj_leta'], '         ', i['datum_i_vreme_polaska'], '     ', i['datum_i_vreme_dolaska'])

#4. OPCIJA KORISNICKOG MENIJA
def prikaz_10_najjeftinijih_letova():
    polaziste=input('Unesite sifru aerodroma sa kog zelite da podjete: ')
    odrediste=input('Unesite sifru aerodroma na koji zelite da dodjete: ')
    svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    lista_10_letova=letovi.prikaz_10_najjeftinijih_letova(odrediste, polaziste, svi_letovi)
    if lista_10_letova:
        print('\nBroj leta    Cena     Vreme poletanja   Vreme sletanja')
        for i in lista_10_letova:
            print(i['broj_leta'], '       ', round(i['cena'], 2), ' ', i['vreme_poletanja'], '           ', i['vreme_sletanja'])


#5. OPCIJA KORISNICKOG MENIJA
def fleksibilni_polasci():
    polaziste = input('Unesite sifru aerodroma sa kog zelite da podjete: ')
    odrediste = input('Unesite sifru aerodroma na koji zelite da dodjete: ')

    try:
        flex_dani = int(input('Molimo Vas da unesete broj fleksibilnih dana za malocas unete datume: '))
    except:
        while True:
            print('Greska! Morate koristiti brojcanu vrednost pri unosu fleksibilnih dana.\n')
            flex_dani = input('Molimo Vas da unesete broj fleksibilnih dana za malocas unete datume: ')
            if flex_dani.isnumeric():
                break

    flex_dani=int(flex_dani)
    print('Molimo da datume unosite iskljucivo u formatu: DD.MM.GGGG.')
    try:
        datum_polaska=datetime.strptime(input('Unesite datum polaska: '), '%d.%m.%Y.').date()
        datum_dolaska=datetime.strptime(input('Unesite datum dolaska: '), '%d.%m.%Y.').date()
    except:
        print('Datumi nisu uneseni u odgovarajucem formatu. Molimo Vas da pokusate ponovo.\n')
        fleksibilni_polasci()

    svi_letovi = letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    lista_konkretnih=letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi,
                                                polaziste, odrediste, datum_polaska, flex_dani, datum_dolaska)
    if not lista_konkretnih:
        print('Postovani, ne postoji nijedan konkretan let na datoj relaciji u dato vreme.')
    else:
        print('Sifra leta   Cena      Datum polaska  Datum dolaska')
        for i in lista_konkretnih:
            if i['sifra'] > 9:
                print(i['sifra'], '         ', i['cena'], '  ', i['datum_i_vreme_polaska'].strftime('%Y-%m-%d'),
                      '   ', i['datum_i_vreme_dolaska'].strftime('%Y-%m-%d'))
            else:
                print(i['sifra'], '          ', i['cena'], '  ', i['datum_i_vreme_polaska'].strftime('%Y-%m-%d'),
                      '   ', i['datum_i_vreme_dolaska'].strftime('%Y-%m-%d'))

#6. OPCIJA KUPACA
def kupovina_karte(logovani_korisnik: dict, onaj_koji_kupuje: dict, sifra_konkretnog_leta: int, t1: str, prodavac: dict):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    try:
        slobodna_mesta=svi_konkretni_letovi[sifra_konkretnog_leta]['zauzetost']
    except:
        print('\nGreska! Ne postoji konkretni let sa ovom sifrom.')
        prikazi_korisnicki_meni(onaj_koji_kupuje)

    putnici=[]
    for key in sve_karte:
        if sve_karte[key]['sifra_konkretnog_leta']==sifra_konkretnog_leta:
            putnici=sve_karte[key]['putnici']

    ime=ime_zagrade='' #u slucaju kupovanja karte za drugu osobu
    print(f'\nZa koga kupujete kartu? Ukoliko {t1}, pritisnite 1.')
    karta_za_sebe=input('U suprotnom pritisnite bilo koji drugi taster: ')
    if karta_za_sebe!='1':
        ime=input('Unesite ime i prezime osobe za koju kupujete kartu: ')
        ime_zagrade='('+ime+')'
    kupac=logovani_korisnik
    kwargs={'prodavac': prodavac, 'datum_prodaje': datetime.now()}

    try:
        karta, n_sve_karte=karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, putnici, slobodna_mesta, kupac, **kwargs)
        karta['putnici'].append(logovani_korisnik['korisnicko_ime']+ime_zagrade)
        karta['datum_prodaje'] = karta['datum_prodaje'].strftime('%d.%m.%Y.')
        karte.sacuvaj_karte({karta['broj_karte']: karta}, 'spisak_karata.csv', '|')
        if not ime:
            if onaj_koji_kupuje==logovani_korisnik:
                print('\nPostovani', onaj_koji_kupuje['korisnicko_ime'], 'uspesno ste kupili kartu.')
            else: print('\nPostovani', onaj_koji_kupuje['korisnicko_ime'], 'uspesno ste kupili kartu korisniku', logovani_korisnik['korisnicko_ime']+'.')

        else:
            print('\nPostovani', onaj_koji_kupuje['korisnicko_ime'], 'uspesno ste kupili kartu osobi', ime+'.')

        print('\nPostovani', logovani_korisnik['korisnicko_ime']+ime_zagrade,'da li zelite da kupite kartu i za saputnika?')
        saputnik = input('Ukoliko je Vas odgovor "da", pritisnite 1. U suprotnom pritisnite neki drugi taster: ')
        if saputnik == '1':
            kupovina_karte(logovani_korisnik, onaj_koji_kupuje, sifra_konkretnog_leta, t1, prodavac)

        svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', "|")

        odrediste=fly_key=''
        for key in svi_letovi:
            if key==svi_konkretni_letovi[sifra_konkretnog_leta]['broj_leta']:
                fly_key=key
                odrediste=svi_letovi[key]['sifra_odredisnog_aerodorma']
                break

        print('\nPostovani', logovani_korisnik['korisnicko_ime']+ime_zagrade, 'da li zelite da posle sletanja na odrediste', odrediste, 'poletite sa tog aerodroma na neko drugo mesto?')
        povezani_let=input('Ukoliko je Vas odgovor potvrdan, pritisnite 1. U suprotnom pritisnite neki drugi taster: ')
        if povezani_let=='1':
            lista_povezanih_letova=letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[sifra_konkretnog_leta])
            if lista_povezanih_letova:
                print('\nAvion slece u', odrediste, 'u', svi_letovi[fly_key]['vreme_sletanja'])
                print('Ovo su letovi koji polecu sa ovog aerodroma u roku od 120 minuta: ')
                print('Sifra    Polaziste    Odrediste    Vreme polaska    Vreme dolaska')
                lista_sifara=[]
                for i in lista_povezanih_letova:
                    for kk in svi_konkretni_letovi:
                        if svi_konkretni_letovi[kk]['broj_leta']==i['broj_leta']:
                            print(kk,  '     ', odrediste, '         '+i['sifra_odredisnog_aerodorma']+
                                  '          '+i['vreme_poletanja']+'            '+i['vreme_sletanja'])
                            lista_sifara.append(kk)
                            break
                try:
                    sifra_povezanog_k_leta=int(input('Unesite sifru nekog od povezanih letova sa spiska: '))
                    if sifra_povezanog_k_leta in lista_sifara:
                        kupovina_karte(logovani_korisnik, onaj_koji_kupuje, sifra_povezanog_k_leta, t1, prodavac)
                    else:
                        print('Ova sifra se ne nalazi u povezanim letovima.')
                except: print('Ova sifra se ne nalazi u povezanim letovima.')

            else:
                print('Nema letova sa ovog aerodroma u narednih 120 minuta.')

        else: print('\nOdlucili ste da ne zelite povezani let za', logovani_korisnik['korisnicko_ime']+ime_zagrade+'.')
    except: print()

#7. OPCIJA KUPACA
def pregled_nerealizovanih_karata(logovani_korisnik):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    lista_nerealizovanih_karata = []
    for key in sve_karte:
        if sve_karte[key]['status']==konstante.STATUS_NEREALIZOVANA_KARTA:
            for j in sve_karte[key]['putnici']:
                if j == logovani_korisnik['korisnicko_ime']:
                    lista_nerealizovanih_karata.append(sve_karte[key])
    svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    if lista_nerealizovanih_karata:
        print('Sifra   Polaziste   Odrediste    Datum polaska        Datum dolaska')
        for i in lista_nerealizovanih_karata:
            for konkretni_key in svi_konkretni_letovi:
                if i['sifra_konkretnog_leta']==konkretni_key:
                    for key in svi_letovi:
                        if svi_konkretni_letovi[konkretni_key]['broj_leta']==key:
                            print(konkretni_key, '    ', svi_letovi[key]['sifra_polazisnog_aerodroma'], '       ',
                                  svi_letovi[key]['sifra_odredisnog_aerodorma'], '        ', (svi_konkretni_letovi[konkretni_key]['datum_i_vreme_polaska']).strftime('%H:%M %d.%m.%Y.'),
                                  '  ', (svi_konkretni_letovi[konkretni_key]['datum_i_vreme_dolaska']).strftime('%H:%M %d.%m.%Y.'))
    else: print('Ne postoji nijedna nerealizovana karta s Vasim imenom.')

#8. OPCIJA KUPACA
def checkin(logovani_korisnik, broj_karte, lista_nerealizovanih_karata):
    sve_karte = karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    try:
        if lista_nerealizovanih_karata:
            if broj_karte not in lista_nerealizovanih_karata:
                print("Molimo pokusajte ponovo. Uneti broj karte nije u listi.")
                prikazi_korisnicki_meni(logovani_korisnik)
            else:
                svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
                sifra=sve_karte[broj_karte]['sifra_konkretnog_leta']
                matrica=svi_konkretni_letovi[sifra]['zauzetost']
                dodeljena_pozicija = sve_karte[broj_karte]['sediste'].split(',')
                dodeljen_red = int(dodeljena_pozicija[0].split('.')[0])
                dodeljeno_sediste = int(dodeljena_pozicija[1].split('.')[0])
                dostupne_pozicije=[]
                index_i=1
                for i in matrica:
                    print('Red', index_i, ':', end=' ')
                    index_j=1
                    for j in i:
                        if not j or (dodeljen_red==index_i and dodeljeno_sediste==index_j):
                            print(index_j, end=' ')
                            dostupne_pozicije.append([index_i, index_j])
                        else: print('X ', end='')
                        index_j+=1
                    index_i+=1
                    print()
                try:
                    broj_reda=int(input('Izaberite broj zeljenog reda: '))
                    broj_sedista=int(input('Izaberite broj zeljenog sedista: '))
                except:
                    print("Greska! Nisu unesene brojne vrednosti.")
                    checkin(logovani_korisnik, broj_karte, lista_nerealizovanih_karata)
                if [broj_reda, broj_sedista] not in dostupne_pozicije:
                    print('Greska! Uneto mesto je vec rezervisano. Molimo Vas da izaberete neko od slobodnih mesta.')
                    checkin(logovani_korisnik, broj_karte, lista_nerealizovanih_karata)
                elif svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'] - datetime.now() <= timedelta(days=2):
                    svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('ljudi.csv', '|')
                    korisnicko_ime=logovani_korisnik['korisnicko_ime']
                    if not svi_korisnici[korisnicko_ime]['pasos'] or not svi_korisnici[korisnicko_ime]['drzavljanstvo'] or not svi_korisnici[korisnicko_ime]['pol']:
                        print('Da biste dovrsili check in, neophodno je da unesete broj pasosa, drzavljanstvo i pol, ukoliko to niste uradili.')

                        if not svi_korisnici[korisnicko_ime]['pasos']:
                            pasos=input('Molimo Vas unesite broj pasosa: ')
                            while len(pasos)!=9 or not pasos.isnumeric():
                                print('Greska! Broj pasosa nije unesen u odgovarajucem formatu. Molimo pokusajte ponovo.')
                                pasos = input('Molimo Vas unesite broj pasosa: ')
                            svi_korisnici[korisnicko_ime]['pasos']=pasos

                        if not svi_korisnici[korisnicko_ime]['drzavljanstvo']:
                            drzavljanstvo=input('Molimo unesite Vase drzavljanstvo: ')
                            while not drzavljanstvo:
                                drzavljanstvo = input('Molimo unesite Vase drzavljanstvo: ')
                            svi_korisnici[korisnicko_ime]['drzavljanstvo']=drzavljanstvo

                        if not svi_korisnici[korisnicko_ime]['pol']:
                            pol=input('Molimo unesite Vas pol: ')
                            while not pol:
                                pol = input('Molimo unesite Vas pol: ')
                            svi_korisnici[korisnicko_ime]['pol']=pol

                        korisnici.sacuvaj_korisnike('ljudi.csv', '|', svi_korisnici)

                    if broj_sedista!=dodeljeno_sediste and broj_reda!=dodeljen_red:
                        svi_konkretni_letovi[sifra]['zauzetost'][broj_reda-1][broj_sedista-1]=True
                        svi_konkretni_letovi[sifra]['zauzetost'][dodeljen_red-1][dodeljeno_sediste-1]=False

                    sve_karte[broj_karte]['status'] = konstante.STATUS_REALIZOVANA_KARTA
                    sve_karte[broj_karte]['sediste']=str(index_i)+'. red, '+str(index_j)+'. sediste'
                    karte.azuriraj_karte(sve_karte, 'spisak_karata.csv', '|')
                    konkretni_letovi.sacuvaj_kokretan_let('spisak_konkretnih.csv', '|', svi_konkretni_letovi)
                    print('Uspesno ste obavili check in za kartu broj', str(broj_karte)+'.')

                    print('\nDa li zelite da uradite check in karte i za nekog od saputnika?')
                    saputnik=input('Ukoliko je Vas odgovor "da", pritisnite 1. U suprotnom pritisnite bilo koji drugi taster: ')
                    if saputnik=='1':
                        lista_nerealizovanih_karata.remove(broj_karte)
                        if lista_nerealizovanih_karata:
                            print('Lista nerealizovanih karata: ', lista_nerealizovanih_karata)
                            try:
                                nova_karta=int(input('Unesite naredni broj karte: '))
                            except:
                                print('Uneti broj karte ne postoji u listi.')
                                prikazi_korisnicki_meni(logovani_korisnik)
                            if nova_karta in lista_nerealizovanih_karata:
                                checkin(logovani_korisnik, nova_karta, lista_nerealizovanih_karata)
                            else: print('Uneti broj karte ne postoji u listi.')

                    print('\nDa li zelite da uradite check in i za neki od poveznih letova karte', str(broj_karte)+'?')
                    povezan=input('Ukoliko je Vas odgovor "da", pritisnite 1. U suprotnom pritisnite bilo koji drugi taster: ')
                    if povezan=='1':
                        svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
                        lista_povezanih_letova=letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[sifra])
                        lista_povezanih_karata=[]
                        for i in lista_povezanih_letova:
                            for konkretan_key in svi_konkretni_letovi:
                                if svi_konkretni_letovi[konkretan_key]['broj_leta']==i['broj_leta']:
                                    for key in sve_karte:
                                        if sve_karte[key]['sifra_konkretnog_leta']==konkretan_key:
                                            lista_povezanih_karata.append(key) #broj karte ciji je let povezan sa prethodnim
                        if lista_povezanih_karata:
                            print('Brojevi karata povezanih letova:', lista_povezanih_karata)
                            try:
                                povezana_karta=int(input('Unesite novi broj karte iz liste za koju zelite da uradite check in: '))
                            except:
                                print('Greska! Ovaj broj karte se ne nalazi u listi.')
                                checkin(logovani_korisnik, broj_karte, lista_povezanih_karata)
                            checkin(logovani_korisnik, povezana_karta, lista_povezanih_karata)
                        else: print('Niste kupili nijednu kartu sa povezanim letom.')
                else: print('Predvidjeno vreme od 48 sati pre leta za potvrdu karte je isteklo.')

        else:
            print('Ne postoji nijedna nerealizovana karta s Vasim imenom sa ovim brojem.')
            prikazi_korisnicki_meni(logovani_korisnik)
    except: print('Izgleda da je doslo do greske.')

#6. OPCIJA PRODAVACA
def prodaja_karata(logovani_prodavac):
    prikaz_konkretnih=input('Da li zelite da pretrazite konkretni let pomocu kriterijuma? (1 za "da"): ')
    svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')

    if prikaz_konkretnih=='1':
        broj_leta=input('Broj leta: ')
        datum_i_vreme_polaska=input('Datum i vreme polaska: ')
        if datum_i_vreme_polaska:
            datum_i_vreme_polaska=datetime.strptime(datum_i_vreme_polaska, '%H:%M:%S %d.%m.%Y.')
        datum_i_vreme_dolaska=input('Datum i vreme dolaska: ')
        if datum_i_vreme_dolaska:
            datum_i_vreme_dolaska=datetime.strptime(datum_i_vreme_dolaska, '%H:%M:%S %d.%m.%Y.')
        print("Lista sifara konkretnih letova: ", end='')
        for key in svi_konkretni_letovi:
            if (broj_leta==svi_konkretni_letovi[key]['broj_leta'] or not broj_leta) and \
                (datum_i_vreme_polaska==svi_konkretni_letovi[key]['datum_i_vreme_polaska'] or not datum_i_vreme_polaska) and\
                (datum_i_vreme_dolaska==svi_konkretni_letovi[key]['datum_i_vreme_dolaska'] or not datum_i_vreme_dolaska):
               print(key, end=' ')
        print()

    try:
        sifra=int(input('\nUnesite sifru zeljenog konkretnog leta: '))
    except:
        print("Sifra moze da sadrzi samo cifre.\n")
        prodaja_karata(logovani_prodavac)
    if sifra not in svi_konkretni_letovi:
        print("\nUneta sifra ne postoji. Molimo Vas da pokusate ponovo.")
        prodaja_karata(logovani_prodavac)

    ima_slobodnih=False
    for i in svi_konkretni_letovi[sifra]['zauzetost']:
        for j in i:
            if not j:
                ima_slobodnih=True
                break
        if ima_slobodnih: break
    if not ima_slobodnih:
        print("Postovani, ovaj let nema slobodnih mesta. Stoga Vas molimo da odaberete drugi.")
        prodaja_karata(logovani_prodavac)

    svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('ljudi.csv', '|')
    novi_korisnik = input('Da li zelite da kreirate novog korisnika? (1 za "da"): ')
    if novi_korisnik=='1':
        print('\n')
        korisnicko_ime = input('Molimo unesite njegovo korisnicko ime: ')
        lozinka = input('Molimo unesite njegovu lozinku: ')
        ime = input('Molimo unesite njegovo ime: ')
        prezime = input('Molimo unesite njegovo prezime: ')
        email = input('Molimo njegov Vas email: ')
        telefon = input('Molimo unesite njegov telefon: ')
        try:
            pasos = none_operand('njegov devetocifreni broj pasosa')
            drzavljanstvo = none_operand('njegovo drzavljanstvo')
            pol = none_operand('njegov pol')
        except:
            print('Pogresno unet broj za neku od neobaveznih vrednosti (pasos, drzavljanstvo, pol)')

        try:
            novi_svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, '', korisnicko_ime, lozinka,
                                                             ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
            korisnici.sacuvaj_korisnike('ljudi.csv', '|', novi_svi_korisnici)
            trazeni_korisnik={'ime': ime, 'prezime': prezime, 'korisnicko_ime': korisnicko_ime, 'lozinka': lozinka, 'email': email,
                              'pasos': pasos, 'drzavljanstvo': drzavljanstvo, 'telefon': telefon, 'pol': pol, 'uloga': 'korisnik'}
        except:
            print('Greska! Molimo pokusajte ponovo.')
            prodaja_karata(logovani_prodavac)

    else:
        korisnicko_ime = input('Izaberite korisnicko ime kupca za koga zelite da ostvarite kupovinu: ')
        if korisnicko_ime not in svi_korisnici:
            print('Uneto korisnicko ime ne postoji. Pokusajte ponovo.')
            prodaja_karata(logovani_prodavac)
        for key in svi_korisnici:
            if key==korisnicko_ime:
                trazeni_korisnik=svi_korisnici[key]
                break
    prodavac={'korisnicko_ime': logovani_prodavac['korisnicko_ime'], 'uloga': 'prodavac'}
    kupovina_karte(trazeni_korisnik, logovani_prodavac, sifra, 'je to korisnik koga ste prijavili', prodavac)
    print('\nUspesno ste izasli iz 6. opcije prodavaca.')

#7. OPCIJA PRODAVACA
def checkin_prodavac(logovani_prodavac):
    lista_nerealizovanih_karata=[]
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    for key in sve_karte:
        if sve_karte[key]['status']==konstante.STATUS_NEREALIZOVANA_KARTA:
            lista_nerealizovanih_karata.append(key)
    print('Lista nerealizovanih karata: ', lista_nerealizovanih_karata)
    try:
        broj_karte=int(input('Molimo unesite broj karte za koju zelite da obavite check in: '))
    except:
        print('Greska! Nije unesena brojna vrednost.')
        checkin_prodavac(logovani_prodavac)

    if broj_karte in lista_nerealizovanih_karata:
        checkin(logovani_prodavac, broj_karte, lista_nerealizovanih_karata, )
    else: print('Greska! Ovaj broj karte ne pripada listi.')

#8. OPCIJA PRODAVACA
def izmena_karte(logovani_kupac):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    lista_karata=[]
    print('Lista brojeva karata: ')
    for key in sve_karte:
        print(key, end=' ')
        lista_karata.append(key)
    print()
    try:
        broj_karte=int(input('\nPostovani, molimo Vas da unesete broj karte iz liste koju zelite da promenite: '))
    except:
        print(Exception('\nGreska! Morate uneti brojcanu vrednost.'))
        prikazi_korisnicki_meni(logovani_kupac)

    broj_karte=int(broj_karte)
    if broj_karte not in lista_karata:
        print(Exception('\nGreska! Karta sa ovakvim brojem ne postoji. Molimo da odaberete broj iz liste.'))
        prikazi_korisnicki_meni(logovani_kupac)

    else:
        svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
        for kk in svi_konkretni_letovi:
            if kk == sve_karte[broj_karte]['sifra_konkretnog_leta']:
                sifra_leta = kk

        print('Ovo su trenutne vrednosti karte koje Vi mozete da izmenite: ')
        print('Sifra leta:', sifra_leta)
        print('Datum i vreme polaska:', svi_konkretni_letovi[sifra_leta]['datum_i_vreme_polaska'])
        print('Sediste:', sve_karte[broj_karte]['sediste'])

        print('\nOvde mozete izmeniti neku od vrednosti. Ukoliko neku zelite da ostavite nepromenjenu, kliknite "enter".')
        nova_sifra = input('Nova sifra konkretnog leta: ')
        if nova_sifra:
            try:
                nova_sifra=int(nova_sifra)
            except:
                print(Exception('\nGreska! Morate uneti brojcanu vrednost.\n'))
                prikazi_korisnicki_meni(logovani_kupac)

            if nova_sifra not in svi_konkretni_letovi:
                print(Exception('\nGreska! Izabrana sifra ne postoji.\n'))
                prikazi_korisnicki_meni(logovani_kupac)

        nov_datum=input('Novi datum polaska (formata HH:MM:SS DD.MM.GGGG.): ')
        if nov_datum:
            try:
                nov_datum=datetime.strptime(nov_datum, '%H:%M:%S %d.%m.%Y.')
            except:
                print(Exception('Greska! Niste uneli datum u odgovarajucem formatu.'))
                prikazi_korisnicki_meni(logovani_kupac)

        broj_reda = input('Unesite novi broj reda: ')
        broj_sedista = input('Unesite novi broj sedista: ')
        novo_sediste=None
        if broj_sedista and broj_reda:
            try:
                broj_reda=int(broj_reda)
                broj_sedista=int(broj_sedista)
                novo_sediste = str(broj_reda) + '. red, '+ str(broj_sedista) + '. sediste'
            except:
                print(Exception('\nGreska! Morate uneti brojcanu vrednost.'))
                prikazi_korisnicki_meni(logovani_kupac)

        try:
            sve_karte=karte.izmena_karte(sve_karte, svi_konkretni_letovi, broj_karte, nova_sifra, nov_datum, novo_sediste)
            karte.azuriraj_karte(sve_karte, 'spisak_karata.csv', '|')
            konkretni_letovi.sacuvaj_kokretan_let('spisak_konkretnih.csv', '|', svi_konkretni_letovi)
            print('\nPostovani, uspeno ste izmenili podatke karte broj', str(broj_karte)+'.')
        except: print('Greska! Ovaj broj karte ne postoji.')

#9. OPCIJA PRODAVACA
def brisanje_karte(logovani_prodavac):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    lista_karata = []
    print('Lista brojeva neobrisanih karata: ')
    for key in sve_karte:
        if not sve_karte[key]['obrisana']:
            print(key, end=' ')
            lista_karata.append(key)
    print()
    try:
        broj_karte=int(input('Unesite broj karte koju zelite da obrisete: '))
    except:
        print('Greska! Nije uneta brojna vrednost.')
        prikazi_korisnicki_meni(logovani_prodavac)
    sve_karte=karte.brisanje_karte(logovani_prodavac, sve_karte, broj_karte)
    karte.azuriraj_karte(sve_karte, 'spisak_karata.csv', '|')
    print('Uspesno ste podneli zahtev za brisanje karte broj '+ str(broj_karte)+'.')

#10. OPCIJA PRODAVACA
def pretraga_karata(logovani_prodavac):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    print('Unesite parametre po kojima zelite da pronadjete kartu.')
    print('Ukoliko ne zelite da pretrazujete po odredjenom parametru, pritisnite "enter".')
    polaziste=input('Sifra polazisnog aerodroma: ')
    odrediste=input('Sifra odredisnog aerodroma: ')
    dat_polaska=input('Datum i vreme polaska (formata HH:MM:SS DD.MM.GGGG.): ')
    dat_dolaska=input('Datum i vreme dolaska (formata HH:MM:SS DD.MM.GGGG.): ')
    korisnicko_ime=input('Korisnicko ime putnika: ')
    if dat_polaska:
        try:
            dat_polaska=datetime.strptime(dat_polaska, '%H:%M:%S %d.%m.%Y.')
        except:
            print(Exception('Greska! Datumi nisu odgovarajuceg formata.'))
            prikazi_korisnicki_meni(logovani_prodavac)
    if dat_dolaska:
        try:
            dat_dolaska=datetime.strptime(dat_dolaska, '%H:%M:%S %d.%m.%Y.')
        except:
            print(Exception('Greska! Datumi nisu odgovarajuceg formata.'))
            prikazi_korisnicki_meni(logovani_prodavac)
    try:
        lista_karata=karte.pretraga_prodatih_karata(sve_karte, svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                                dat_polaska, dat_dolaska, korisnicko_ime)
    except:
        print(Exception('Izgleda da je doslo do greske.'))
        prikazi_korisnicki_meni(logovani_prodavac)
    tabela=PrettyTable()
    tabela.field_names=['Broj karte', 'Sifra leta', 'Sediste', 'Prodavac', 'Datum prodaje']
    nove_karte={}
    for i in lista_karata:
        broj_karte=i['broj_karte']
        nove_karte[broj_karte]={'broj_karte': broj_karte, 'sifra': i['sifra_konkretnog_leta'],
                         'sediste': i['sediste'], 'prodavac': i['prodavac']['korisnicko_ime'], 'datum_prodaje': i['datum_prodaje']}
    for key in nove_karte:
        tabela.add_row(nove_karte[key].values())

    print(tabela)

    if not nove_karte: print('Ne postoji nijedna karta sa ovakvim parametrima.')

#8. OPCIJA MENADZERA
def kreiranje_leta(logovani_korisnik):
    print('\nMolimo Vas da unesete potrebne atribute leta: ')
    broj_leta=input('Broj leta (formata SlovoSlovoCifraCifra): ')
    sifra_polazisnog_aerodroma=input('Sifra polazisnog aerodroma: ')
    sifra_odredisnog_aerodroma=input('Sifra odredisnog aerodroma: ')
    vreme_poletanja=input('Vreme poletanja (formata HH:MM): ')
    vreme_sletanja=input('Vreme sletanja (formata HH:MM): ')
    sletanje_sutra=input('Sletanje sutra (upisati ili "da" ili "ne"): ')
    datum_pocetka_operativnosti=input('Datum pocetka operativnosti (formata HH:MM:SS DD.MM.GGGG.): ')
    datum_kraja_operativnosti=input('Datum kraja operativnosti (formata HH:MM:SS DD.MM.GGGG.): ')
    prevoznik=input('Prevoznik: ')
    dani=input('Dani (upisati brojeve 1-7 koji oznacavaju dan u nedelji sa znakom razmaka): ')

    svi_modeli = model_aviona.ucitaj_modele_aviona('spisak_modela.csv', '|')
    print('Lista dostupnih id-ova modela aviona: ', end='')
    for i in svi_modeli:
        print(i, end=' ')
    id_modela=input('\nID modela: ')
    try:
        cena=float(input('Cena: '))
    except:
        print('Pri unosu cene smeju biti korisceni samo brojevi.')
        prikazi_korisnicki_meni(logovani_korisnik)

    if sletanje_sutra=="da": sletanje_sutra=True
    elif sletanje_sutra=="ne": sletanje_sutra=False
    else:
        print(Exception('\nGreska! "Sletanje sutra" nije u odgovarajucem formatu.'))
        prikazi_korisnicki_meni(logovani_korisnik)

    if datum_pocetka_operativnosti:
        try:
            datum_pocetka_operativnosti=datetime.strptime(datum_pocetka_operativnosti, '%H:%M:%S %d.%m.%Y.')
        except:
            print('Greska! Datumi nisu uneseni u dobrom formatu.')
            prikazi_korisnicki_meni(logovani_korisnik)

    if datum_kraja_operativnosti:
        try:
            datum_kraja_operativnosti=datetime.strptime(datum_kraja_operativnosti, '%H:%M:%S %d.%m.%Y.')
        except:
            print('Greska! Datumi nisu uneseni u dobrom formatu.')
            prikazi_korisnicki_meni(logovani_korisnik)

    try:
        items=dani.split(' ')
        dani=[]
        for i in items:
            if int(i) not in[1, 2, 3, 4, 5, 6, 7]:
                print('Greska! Dani nisu ispravno uneseni.')
                prikazi_korisnicki_meni(logovani_korisnik)
            else: dani.append(int(i)-1)
    except:
        print('Greska! Dani nisu ispravno uneseni.')
        prikazi_korisnicki_meni(logovani_korisnik)

    try:
        id_modela=int(id_modela)
        if id_modela not in svi_modeli:
            raise Exception
        else: model=svi_modeli[id_modela]
    except:
        print('\nGreska! Odabrali ste nepostojeci model aviona.')
        prikazi_korisnicki_meni(logovani_korisnik)

    svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    try:
        svi_letovi=letovi.kreiranje_letova(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodroma,
                            vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena,
                            datum_pocetka_operativnosti, datum_kraja_operativnosti)
        letovi.sacuvaj_letove('spisak_letova.csv', '|', {broj_leta: svi_letovi[broj_leta]})
        print('Postovani, uspesno ste kreirali let', broj_leta+'.')
    except:
        print(Exception('Molimo pokusajte ponovo.\n'))
        prikazi_korisnicki_meni(logovani_korisnik)

#9. OPCIJA MENADZERA
def brisanje_karte_admin(logovani_korisnik):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    print('\nLista karata sa zahtevom za brisanje: ', end='')
    for key in sve_karte:
        if sve_karte[key]['obrisana']:
            print(key, end=' ')
    print()
    print('Ispisite brojeve karte koju zelite da obrisete. Ukoliko ih ima vise,')
    lista_za_brisanje=input('razdvojite ih znakom razmaka: ')
    if lista_za_brisanje:
        lista_za_brisanje=lista_za_brisanje.split(' ')
        for i in lista_za_brisanje:
            try:
                i=int(i)
                sve_karte=karte.brisanje_karte(logovani_korisnik, sve_karte, i)
            except:
                print('Greska! Kao broj karte smeju se pojaviti samo cifre.')
                prikazi_korisnicki_meni(logovani_korisnik)
        print('Uspesno ste izvrsili brisanje.\n')

    lista_oslobodjenih=input('Unesite karte koje zelite da razresite brisanja: ')
    if lista_oslobodjenih:
        lista_oslobodjenih=lista_oslobodjenih.split(' ')
        for i in lista_oslobodjenih:
            try:
                i=int(i)
                if i not in sve_karte:
                    raise Exception
                sve_karte[i]['obrisana']=False
            except:
                print('\nGreska! Ovaj broj karte nije u listi.')
                prikazi_korisnicki_meni(logovani_korisnik)
        print('Uspesno ste sacuvali karte od brisanja.')

    karte.azuriraj_karte(sve_karte, 'spisak_karata.csv', '|')

#10. ADMIN
def izvestaj_dan_prodaje(logovani_korisnik):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    dan_prodaje=input('\nUnesite zeljeni datum prodaje (DD.MM.GGGG.): ')
    try:
        dan_prodaje=datetime.strptime(dan_prodaje, '%d.%m.%Y.')
        dan_prodaje=dan_prodaje.strftime('%d.%m.%Y.')

        lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, dan_prodaje)
        print('Lista prodatih karata: ', end='')
        for i in lista:
            print(i['broj_karte'], end=' ')
    except:
        print('Greska! Pogresno unesen format datuma.')
        prikazi_korisnicki_meni(logovani_korisnik)

#11. ADMIN
def izvestaj_dan_polaska(logovani_korisnik):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    svi_konkretni=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    dan_polaska=input('\nUnesite zeljeni datum polaska (DD.MM.GGGG.): ')
    try:
        dan_polaska=datetime.strptime(dan_polaska, '%d.%m.%Y.').date()
        lista = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni, dan_polaska)
        print('Lista prodatih karata: ', end='')
        for i in lista:
            print(i['broj_karte'], end=' ')
    except:
        print('Greska! Pogresno unesen format datuma.')
        prikazi_korisnicki_meni(logovani_korisnik)


#12. ADMIN
def izvestaj_prodavac_i_dan_prodaje(logovani_korisnik):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    prodavac=input('\nUnesite ime prodavca: ')
    dan_prodaje=input('Unesite zeljeni datum prodaje (DD.MM.GGGG.): ')
    try:
        dan_prodaje=datetime.strptime(dan_prodaje, '%d.%m.%Y.')
        dan_prodaje=dan_prodaje.strftime('%d.%m.%Y.')

        lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, dan_prodaje, prodavac)
        print('Lista prodatih karata: ', end='')
        for i in lista:
            print(i['broj_karte'], end=' ')
    except:
        print('Greska! Pogresno unesen format datuma.')
        prikazi_korisnicki_meni(logovani_korisnik)

#13. ADMIN
def ubc_dan_prodaje(logovani_korisnik):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    svi_konkretni=konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    svi_letovi=letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    dan_prodaje=input('\nUnesite zeljeni datum prodaje (DD.MM.GGGG.): ')
    try:
        dan_prodaje=datetime.strptime(dan_prodaje, '%d.%m.%Y.')
        dan_prodaje=dan_prodaje.strftime('%d.%m.%Y.')

        broj_prodatih, suma = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte, svi_konkretni,
                                                                                    svi_letovi, dan_prodaje)
        suma=round(suma, 2)
        print('\nUkupno je prodato', broj_prodatih, 'karata, a cena svih tih karata je', str(suma) + '$.')
    except:
        print('Greska! Pogresno unesen format datuma.')
        prikazi_korisnicki_meni(logovani_korisnik)

#14. ADMIN
def ubc_dan_polaska(logovani_korisnik):
    sve_karte = karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    svi_konkretni = konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    svi_letovi = letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    dan_polaska = input('\nUnesite zeljeni datum polaska (DD.MM.GGGG.): ')
    try:
        dan_polaska = datetime.strptime(dan_polaska, '%d.%m.%Y.').date()

        broj_prodatih, suma = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni,
                                                                                    svi_letovi, dan_polaska)
        suma = round(suma, 2)
        print('\nUkupno je prodato', broj_prodatih, 'karata, a cena svih tih karata je', str(suma) + '$.')
    except:
        print('Greska! Pogresno unesen format datuma.')
        prikazi_korisnicki_meni(logovani_korisnik)

#15. ADMIN
def ubc_prodavac_i_dan_prodaje(logovani_korisnik):
    sve_karte=karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    svi_konkretni = konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    svi_letovi = letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    prodavac=input('\nUnesite ime prodavca: ')
    dan_prodaje=input('Unesite zeljeni datum prodaje (DD.MM.GGGG.): ')
    try:
        dan_prodaje=datetime.strptime(dan_prodaje, '%d.%m.%Y.')
        dan_prodaje=dan_prodaje.strftime('%d.%m.%Y.')

        broj_prodatih, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, svi_konkretni,
                                                                                 svi_letovi, dan_prodaje, prodavac)
        cena=round(cena, 2)
        print('\nUkupno je prodato', broj_prodatih, 'karata, a cena svih tih karata je', str(cena) + '$.')
    except:
        print('Greska! Pogresno unesen format datuma.')
        prikazi_korisnicki_meni(logovani_korisnik)

#16. ADMIN
def ubc_30_dana():
    sve_karte = karte.ucitaj_karte_iz_fajla('spisak_karata.csv', '|')
    svi_konkretni = konkretni_letovi.ucitaj_konkretan_let('spisak_konkretnih.csv', '|')
    svi_letovi = letovi.ucitaj_letove_iz_fajla('spisak_letova.csv', '|')
    recnik=izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte, svi_konkretni, svi_letovi)
    for key in recnik:
        cena=round(recnik[key]['suma'], 2)
        print('Prodavac', key, 'je u poslednjih 30 dana prodao', recnik[key]['broj_prodatih'], 'karata, po ukupnoj ceni od', str(cena)+'$.')


#ISPIS OPSTEG MENIJA
menu()
opcija=input('Postovani, molimo Vas da unesete redni broj zeljene opcije: ')

while opcija!='0':
    if opcija=='1':
        login()
    elif opcija=='2':
        registracija('Vase', 'Vas', {}) #znak da se registruje KUPAC
    else:
        print('\nUneli ste nepostojecu opciju. Molimo Vas da pokusate ponovo.\n')
    menu()
    opcija=input('Postovani, molimo Vas da unesete redni broj zeljene opcije: ')

print('\nUspesno ste zatvorili aplikaciju. Hvala Vam sto ste deo nase price.')

