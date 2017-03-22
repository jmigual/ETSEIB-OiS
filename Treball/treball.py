#!/usr/bin/env python3

import random
import abc
import logging
import numpy


class ComptadorEstadistic:
    def __init__(self):
        self.desviacio = 1
        self.llista_espera = []

    def error(self):
        if len(self.llista_espera) < 10:
            return None

        # Calcular la desviació estandard dels ultims 10 elements
        desviacio = numpy.std(self.llista_espera[-10:])
        return abs(self.desviacio - desviacio) / self.desviacio

    def imprimir_resultats(self):
        logger = logging.getLogger()
        logger.info("Total de clients    : {:= 10n}", len(self.llista_espera))
        logger.info("Temps mitja d'espera: {:= 10n}")


class Estat:
    def __init__(self, facturadors=12):
        self.llista_persones_espera = []
        self.facturador_lliure = [True] * facturadors
        self.rellotge = 0
        self.stat = ComptadorEstadistic()


class Esdeveniment(metaclass=abc.ABCMeta):
    def __init__(self, tipus, rellotge):
        self.tipus = tipus
        self.rellotge = rellotge

    def __lt__(self, other):
        return self.rellotge < other.rellotge

    def __str__(self):
        return "{0:5.1} {1}".format(self.rellotge, self.tipus)

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
        estat.rellotge = self.rellotge

        if len(estat.llista_persones_espera) <= 0:
            estat.facturador_lliure[self.facturador] = True
            return []

        persona = estat.llista_persones_espera.pop(0)
        estat.stat.llista_espera.append(estat.rellotge - persona)

        return [EsdevenimentFinalitzacio(self.rellotge + Simulacio.get_temps_facturacio(), self.facturador)]


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
        facturadors_lliures = [i for i, x in enumerate(estat.facturador_lliure) if x]
        p = min(len(facturadors_lliures), self.nombre_passatgers)
        estat.llista_persones_espera += [estat.rellotge] * (self.nombre_passatgers - p)

        finalitzats = []
        for i in range(p):
            estat.facturador_lliure[facturadors_lliures[i]] = False
            temps_f = self.rellotge + Simulacio.get_temps_facturacio()
            finalitzats.append(EsdevenimentFinalitzacio(temps_f, facturadors_lliures[i]))

        return [EsdevenimentArribada(self.rellotge + random.expovariate(1))] + finalitzats


class Simulacio:
    TEMPS_MAXIM_SIMULACIO = 100.0
    ERROR_MINIM = 0.01
    simulacio_amb_maquines_autofacturacio = False

    def __init__(self):
        self.temps_inicial = 0.0
        self.llista_esdeveniments = []
        self.estat = Estat()
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
        return esdeveniment.rellotge > self.TEMPS_MAXIM_SIMULACIO or error < self.ERROR_MINIM

    def executa(self):
        esdeveniment = self.obtenir_esdeveniment_proper()
        while not self.finalitzar(esdeveniment):
            # Executar l'esdevniment i afegir els nous esdeveniments que aquest genera a la llista
            # d'esdeveniments
            self.llista_esdeveniments += esdeveniment.esdevenir(self.estat)
            self.escriure_informacio(esdeveniment)

        self.estat.stat.imprimir_resultats()

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
        self.logger.info(str(esdeveniment) + " " + str(self.estat.facturador_lliure))
        pass


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


def main():
    logger = logging.getLogger()
    logger.info("Programa iniciat")
    sim = Simulacio()
    logger.info("Variables inicialitzades")
    sim.executa()


if __name__ == "__main__":
    configure_default_logger()
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt, finishing")
        logging.info("Thanks for the ride!")
