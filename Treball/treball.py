#!/usr/bin/env python3

import random
import abc
import logging
import numpy
import csv
import getopt
import sys


class ComptadorEstadistic:
    def __init__(self, nom_arxiu):
        self.llista_espera = []
        self.nom_arxiu = nom_arxiu
        csvfile = open("resultats_" + self.nom_arxiu, 'w')
        self.csv = csv.writer(csvfile, delimiter=',')
        self.iteration = 1

    def error(self):
        if len(self.llista_espera) < 20:
            return None

        # Calcular la desviació estandard dels ultims 10 elements
        desviacio = numpy.std(self.llista_espera[-10:])
        desviacio_total = numpy.std(self.llista_espera)
        error = abs(desviacio_total - desviacio) / (desviacio_total + 0.0001)
        return error

    def imprimir_resultats(self, estat):
        mitjana = numpy.mean(self.llista_espera)
        desviacio = numpy.std(self.llista_espera)
        clients = len(self.llista_espera)

        logger = logging.getLogger()
        logger.info("Temps final         : {:9.4f}".format(estat.rellotge))
        logger.info("Total de clients    : {:9.4f}".format(clients))
        logger.info("Temps mitjà d'espera: {:9.4f}".format(mitjana))
        logger.info("Desviació std dades : {:9.4f}".format(desviacio))
        logger.info("Files al CSV        : {:9.4f}".format(self.iteration))

        # Intentem aproximar les dades linealment per poder veure si el sistema es estable
        polinomi = numpy.polyfit(range(clients), self.llista_espera, 1)
        logger.info("Regressió a+b*x     :")
        logger.info("    a : {:9.7f}".format(polinomi[1]))
        logger.info("    b : {:9.7f}".format(polinomi[0]))

        with open(self.nom_arxiu, mode='a') as file:
            csv_results = csv.writer(file, delimiter=',')
            csv_results.writerow([mitjana, desviacio, clients, polinomi[0], polinomi[1]])

    def imprimir_estadistiques(self, estat):
        self.iteration += 1
        self.csv.writerow([self.iteration, numpy.sum(self.llista_espera), self.llista_espera[-1],
                           len(estat.llista_persones_espera), estat.rellotge])


class Estat:
    def __init__(self, nom_arxiu, facturadors=12):
        self.llista_persones_espera = []
        self.facturador_lliure = [True] * facturadors
        self.rellotge = 0
        self.stat = ComptadorEstadistic(nom_arxiu)


class Esdeveniment(metaclass=abc.ABCMeta):
    """Classe abstracta Esdeveniment conté els mètodes necessaris per implementar un esdeveniment
    """

    def __init__(self, tipus, rellotge):
        self.tipus = tipus
        self.rellotge = rellotge

    def __lt__(self, other):
        return self.rellotge < other.rellotge

    def __str__(self):
        return "Temps: {0:5.1f} {1:<25}".format(self.rellotge, self.tipus)

    @abc.abstractmethod
    def esdevenir(self, estat):
        """
        Executar esdeveniment i crear els esdeveniments derivats
        :param estat: Estat del sistema
        :return: Llista d'esdeveniments creats
        """
        return []


class EsdevenimentFinalitzacio(Esdeveniment):
    def __init__(self, rellotge, facturador):
        super(EsdevenimentFinalitzacio, self).__init__("Finalitzacio facturacio", rellotge)
        self.facturador = facturador

    def esdevenir(self, estat):
        """
        Implementació de la funció esdevenir per la finalització d'una facturació,
        si hi ha més clients a la llista d'espera s'elimina un i es crea un nou
        EsdevenimentFinalització
        :param estat: Estat actual del sistema
        :return: Es retorna una llista d'esdeveniments creats per aquest esdeveniment
        """
        estat.rellotge = self.rellotge

        if len(estat.llista_persones_espera) <= 0:
            estat.facturador_lliure[self.facturador] = True
            return []

        persona = estat.llista_persones_espera.pop(0)
        estat.stat.llista_espera.append(estat.rellotge - persona)
        estat.stat.imprimir_estadistiques(estat)

        return [EsdevenimentFinalitzacio(self.rellotge + Simulacio.get_temps_facturacio(),
                                         self.facturador)]


class EsdevenimentArribada(Esdeveniment):
    def __init__(self, rellotge):
        super(EsdevenimentArribada, self).__init__("Arribada grup passatgers", rellotge)
        y = random.random()
        if y < 0.25:  # Probabilitat 0.25
            n = 1
        elif y < 0.6:  # Probabilitat 0.35
            n = 2
        elif y < 0.85:  # Probabilitat 0.25
            n = 3
        elif y < 0.95:  # Probabilitat 0.10
            n = 4
        else:  # Probabilitat 0.05
            n = 5
        self.nombre_passatgers = n

    def esdevenir(self, estat):
        """
        Implementació de la funció esdevenir per l'arribada de nous passatgers, si hi ha n
        facturadors disponibles es generaran n EsdevenimentFinalitzacio i a part també es genera
        un nou EsdevenimentArribada seguint les probabilitats especificades en quan al temps i a
        la mida del grup que arriba
        :param estat: Estat del sistema
        :return: Llista amb els esdeveniments generats
        """
        facturadors_lliures = [i for i, x in enumerate(estat.facturador_lliure) if x]
        p = min(len(facturadors_lliures), self.nombre_passatgers)
        estat.llista_persones_espera += [estat.rellotge] * (self.nombre_passatgers - p)

        estat.stat.llista_espera += [0]*p
        finalitzats = []
        for i in range(p):
            estat.facturador_lliure[facturadors_lliures[i]] = False
            temps_f = self.rellotge + Simulacio.get_temps_facturacio()
            finalitzats.append(EsdevenimentFinalitzacio(temps_f, facturadors_lliures[i]))

        return [EsdevenimentArribada(self.rellotge + random.expovariate(1))] + finalitzats


class Simulacio:
    TEMPS_MAXIM_SIMULACIO = 2000.0
    ERROR_MINIM = 0.005
    simulacio_amb_maquines_autofacturacio = False

    def __init__(self, nom_arxiu, maquines, facturadors):
        Simulacio.simulacio_amb_maquines_autofacturacio = maquines
        self.nom_arxiu = nom_arxiu
        self.temps_inicial = 0.0
        self.llista_esdeveniments = []
        self.estat = Estat(nom_arxiu, facturadors=facturadors)
        self.logger = logging.getLogger()

        # Afegir esdeveniment inicial arribada
        self.llista_esdeveniments.append(EsdevenimentArribada(self.temps_inicial))

    # Returns a bool
    def finalitzar(self, esdeveniment):
        error = self.estat.stat.error()
        if error is None:
            return False

        # La simulació s'acaba s'ha arribat al maxim de temps o quan l'error relatiu d'una
        # simulació a l'altra és molt petit
        return esdeveniment.rellotge > self.TEMPS_MAXIM_SIMULACIO #or error < self.ERROR_MINIM

    def executa(self):
        esdeveniment = self.obtenir_esdeveniment_proper()
        while not self.finalitzar(esdeveniment):
            # Executar l'esdevniment i afegir els nous esdeveniments que aquest genera a la llista
            # d'esdeveniments
            self.llista_esdeveniments += esdeveniment.esdevenir(self.estat)
            self.escriure_informacio(esdeveniment)

            # Obtenir el següent esdeveniment
            esdeveniment = self.obtenir_esdeveniment_proper()

        self.estat.stat.imprimir_resultats(self.estat)

    @staticmethod
    def get_temps_facturacio():
        if Simulacio.simulacio_amb_maquines_autofacturacio:
            return random.uniform(4, 10)
        else:
            return numpy.clip(random.gauss(4.0, 1.0), 2, 6)

    def obtenir_esdeveniment_proper(self):
        self.llista_esdeveniments.sort()
        return self.llista_esdeveniments.pop(0)

    def escriure_informacio(self, esdeveniment):
        self.logger.debug(str(esdeveniment) + " " + str(self.estat.facturador_lliure))


def configure_default_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter("[{asctime}s] ({levelname}) {message}", style="{")
    handler_s = logging.StreamHandler()
    handler_f = logging.FileHandler("info.log")
    handler_s.setFormatter(formatter)
    handler_f.setFormatter(formatter)
    log.addHandler(handler_s)
    log.addHandler(handler_f)


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

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "n:i:dfm")
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
        else:
            assert False, "unhandled option"

    logger = logging.getLogger()
    tipus = "maquines" if maquines else "agents"
    logger.info("Tipus facturadors    : {}".format(tipus))
    logger.info("Nombre de facturadors: {}".format(facturadors))
    logger.info("Nombre d'iteracions  : {}".format(iteracions))

    nom_arxiu = "simulacio_{}_{}_{}.csv".format(tipus, facturadors, iteracions)
    logger.info("Resultats a          : {}".format(nom_arxiu))

    with open(nom_arxiu, mode='w') as file:
        csv_file = csv.writer(file, delimiter=',')
        csv_file.writerow(["Mitjana", "Desviació", "Clients", "b", "a"])

    for i in range(iteracions):
        logger.info("***************************")
        logger.info("Simulació {} iniciada".format(i))
        sim = Simulacio(nom_arxiu, maquines, facturadors)
        logger.info("Variables inicialitzades")
        sim.executa()
        logger.info("Simulació {} finalitzada".format(i))
    logger.info("")
    logger.info("")


configure_default_logger()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt, finishing")
        logging.info("Thanks for the ride!")
