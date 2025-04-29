# BP Project 2022

The Airport application is a console-based program developed in Python 3.10 as part of the Basics of Programming course. It offers various functionalities for three user roles: user, seller, and admin.
The main purpose of the application is to allow users to easily search for flights based on their desired routes.
All functionalities implemented in the project are described in the file dokumentacija.pdf, written in Serbian.
The application uses a simple CSV-based database to store and manage data.
Below is the rest of the README file, created mostly with the help of an assistant. It provides instructions and expectations regarding the project structure and testing.

This repository contains the project skeleton and test suite for the Introduction to Programming course (academic year 2022/23).

## Project Structure
The project structure must strictly follow the provided official skeleton.
Function definitions must not be modified.
You may add helper functions, data structures, modules, or variables as needed.

Note: Part of the grading is automated. Deviating from the given structure may result in loss of points.

## Tests
Your grade depends on how many tests pass. Each test verifies a specific functionality.
The final test result determines the number of points you can get during the defense (which must be done in front of an assistant).
The scoring table is available in the project specification.

Tests are located in the test package. You can run them in three ways:

All tests: Right-click the test or package file → Run (Debug) Python tests in...

Individual tests: Right-click the specific test function → Run (Debug) Python tests in...

CLI (official method for grading): Run python -m unittest from the project root in the terminal.

## Main File and Application Overview
The main entry point of the application is menu.py. This file provides a login interface and grants access to various features of the airport console application, including:

Viewing flight schedules

Booking or canceling tickets

Registering or managing users

Accessing logs or administrative functions (if logged in as admin)

## Instalation
Clone the repository: git clone https://github.com/matijasch03/Airport.git

Navigate to the project directory: cd your-repository

Run the main file called menu: python menu.py

The app will start in the console, where you can log in and interact with the system based on your role (user, seller, or admin).


# Projekat OP 2022

Ovaj repozitorijum sadrži kostur projekat i testove za predmet Osnove programiranja u školskoj godini 2022/23.

## Struktura projekta
- Struktura projekta mora strogo pratiti kostur projekta koji je dostupan online.
- Definicija funkcija iz kostura projekta mora ostati nepromenjena. 
- Po potrebi je moguće dodavati pomoćne funkcije, strukture podataka, module, promenljive itd.
Deo ocenjivanja je automatizovan i odstupanje od strukture projekta može dovesti do gubljenja bodova.

## Testovi
Broj osvojenih bodova na projektu zavisi od količine testova koji prođu. Svaki test testira određenu
funkcionalnost. Ukupan rezultat pokazuje koliko je bodova moguće dobiti na odbrani: projekat se svakako
mora odbraniti pred asistentom.
Tabelu bodovanja možete videti u specifikaciji projekta.

Testovi se nalaze u paketu test. Pokretanje testova je moguće na tri načina:
1. Svi testovi: desni klik na test ili paket fajl > Run (Debug) Pythin tests in...
2. Pojedinačni testovi: desni klik na funkciju sa individualnim testom > Run (Debug) Pythin tests in...
3. Svi testovi (CLI): Pozivom `python -m unittest` u komandnoj liniji pozicioniranoj u korenu projekta. **Za krajnje ocenjivanje se koristi ovaj metod.**
