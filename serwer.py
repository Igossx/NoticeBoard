import argparse
import socket
import sys
import struct
import signal
import os
from pathlib import Path

parser = argparse.ArgumentParser(description = "Tablica ogłoszeń.")

#argument niezbędny
parser.add_argument("port", help="server port", type=int)
#argumenty opcjonalne
parser.add_argument("-n", dest="liczba_wiadomosci", default=20, type=int, help="number of messages (max 99)", required=False)
parser.add_argument("-c", dest="liczba_znakow", default=140, type=int, help="number of characters", required=False)

args = parser.parse_args()

#obsluga maksymalnej watosci dla liczby wiadomosci
if args.liczba_wiadomosci > 99 or args.liczba_wiadomosci < 1:
	parser.error("Maksymalna liczba wyswietlanych wiadomosci wynosi 99.")

if args.liczba_znakow < 0:
	parser.error("Liczba znakow nie moze byc ujemna.")

def funkcja_obslugi(signum, frame):
	raise SystemExit("Otrzymalem ctr c, - koncze dzialanie.")

signal.signal(signal.SIGINT, funkcja_obslugi)

with socket.socket() as g:
	g.bind(('', args.port))
	g.listen()

	#stworzenie tablicy
	lista = []

	#odczytanie danych z plikow txt do tablicy
	a = 1
	while Path("msg0" + str(a) + ".txt").exists():
		wyraz = open("msg0" + str(a) + ".txt", 'r', encoding="utf-8")
		lista.append(wyraz.read())
		a = a + 1

	while True:
		#nowe polaczenie z address
		gPol, address = g.accept()
		print('Polaczano z', address)

		#wiadomosc od klienta o dlugosci liczba_znakow
		odp = gPol.recv(args.liczba_znakow)

		if not odp:
			#wyslanie elementow tablicy do klienta w ilosci liczba_wiadomosci
			print("Wysylanie wiadomosci do klienta")
			for i in range(len(lista)):
				if i < args.liczba_wiadomosci:
					wyraz_do_wyslania = lista[i] + "\r\n"
					print(wyraz_do_wyslania)
					gPol.sendall(wyraz_do_wyslania.encode())
		else:
			print("Dodawanie elementu do listy")
			#decodowanie wiadomosci
			napis_do_listy = odp.decode()

			#dodanie wiadomosci do listy
			lista.append(napis_do_listy)

			#odwrocenie calej listy
			lista.reverse()

			#sprawdzanie czy lista ogłoszeń nie jest za długa, jeśli tak usunie ostatni element
			if len(lista) > 99:
				lista.pop()


		#zapis tablicy do plikow txt
		print("Zapisywanie wiadomosci do plikow txt")
		for i in range(len(lista)): 
			wyraz_do_zapisu_txt = lista[i]
			f = open("msg0" + str(i+1) + ".txt", "w")
			f.write(wyraz_do_zapisu_txt)
			f.close()

		gPol.shutdown(socket.SHUT_RDWR)
		gPol.close()

	g.close()



