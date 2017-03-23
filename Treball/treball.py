#!/usr/bin/env python3

import getopt
import sys
import os
from simulator import *
from logger import *


def usage():
    print("Usage: ")
    print("python3 treball.py [-n nombre][-i nombre][-f|-m][-d]")
    print("-i    Nombre de vegades que s'ha d'executar la simulació")
    print("-n    Nombre facturadors o màquines facturadores")
    print("-f    Usar agents facturadors")
    print("-m    Usar màquines facturadores")
    print("-d    Activar mode debug")


def main():
    iteracions = 1
    maquines = False
    facturadors = 12

    # Parsejar els arguments del programa
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hn:i:dfm", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "-i":
            iteracions = int(a)
        elif o == "-d":
            logging.getLogger().setLevel(logging.DEBUG)
        elif o == "-n":
            facturadors = int(a)
        elif o == "-f":
            maquines = False
        elif o == "-m":
            maquines = True
        elif o in ["-h", "--help"]:
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    carpeta_sortida = "resultats/"
    if not os.path.exists(carpeta_sortida):
        os.makedirs(carpeta_sortida)

    total_file_name = carpeta_sortida + "simulation_results.csv"

    if not os.path.exists(total_file_name):
        csv_file = open(total_file_name, 'w')
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(["facturadors", "mitjana", "desviacio", "clients", "b", "a"])
        csv_file.close()

    logger = logging.getLogger()
    tipus = "maquines" if maquines else "agents"
    logger.info("Tipus facturadors    : {}".format(tipus))
    logger.info("Nombre de facturadors: {}".format(facturadors))
    logger.info("Nombre d'iteracions  : {}".format(iteracions))

    nom_arxiu = carpeta_sortida + "simulacio_{}_{}_{}.csv".format(tipus, facturadors, iteracions)
    logger.info("Resultats a          : {}".format(nom_arxiu))

    with open(nom_arxiu, mode='w') as file:
        csv_file = csv.writer(file, delimiter=',')
        csv_file.writerow(["Mitjana", "Desviació", "Clients", "b", "a"])

    resultats = []
    for i in range(iteracions):
        logger.info("***************************")
        logger.info("Simulació {} iniciada".format(i))
        sim = Simulacio(nom_arxiu, maquines, facturadors)
        logger.info("Variables inicialitzades")
        resultats.append([facturadors] + sim.executa())
        logger.info("Simulació {} finalitzada".format(i))

    with open(total_file_name, 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for resultat in resultats:
            csv_writer.writerow(resultat)

    logger.info("")
    logger.info("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt, finishing")
        logging.info("Thanks for the ride!")
