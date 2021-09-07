import argparse
import socket
import sys
import struct
import signal

parser = argparse.ArgumentParser(description = "Tablica ogłoszeń - klient.")

#argument niezbędny
parser.add_argument("port", type=int, help="server port")
parser.add_argument("host", help="server host")

#argumenty opcjonalne
parser.add_argument("-s", dest="nowa_wiadomosc", action="store_true", help="adding new messages", required=False)

args = parser.parse_args()

with socket.socket() as g:
    g.connect((args.host, args.port))

    #wyslanie ogloszenia do serwera
    if args.nowa_wiadomosc:
        print("Wprowadz ogloszenie.")
        wiadomosc = input('>')
        g.sendall(wiadomosc.encode())
        g.shutdown(socket.SHUT_WR)
    else:
        g.shutdown(socket.SHUT_WR)

        #odebranie danych od serwera
        dane = g.recv(1036)
        print("=============================")
        print("------Lista ogloszen------")
        print("=============================")
        wynik = ""

        #pobranie listy ogloszen
        while dane:
            wynik += dane.decode()
            dane = g.recv(1036)

        #zapis poszczególnych linii do tablicy tab_ogloszen
        tab_ogloszen = wynik.splitlines()

        numer_ogloszenia = 1

        #wyswietlanie ogłoszeń
        for x in tab_ogloszen:
            print("Ogłoszenie nr." + str(numer_ogloszenia) + " (długość-" + str(len(x)) + "):")
            numer_ogloszenia = numer_ogloszenia + 1
            print(x)

g.close()