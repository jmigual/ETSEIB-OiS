#!/usr/bin/env python3

import Distribucions
import random
import abc


class Estat:
    def __init__(self, facturadors=12):
        self.llista_persones_espera = []
        self.facturador_lliure = [True]*facturadors


class Esdeveniment:
    def __init__(self, tipus, rellotge):
        self.tipus = tipus
        self.rellotge = rellotge

    def __lt__(self, other):
        return self.rellotge < other.rellotge

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
        return []


class EsdevenimentArribada(Esdeveniment):
    def __init__(self, rellotge):
        y = random.random()
        if y < 0.25:    # Probabilitat 0.25
            n = 1
        elif y < 0.6:   # Probabilitat 0.35
            n = 2
        elif y < 0.85:  # Probabilitat 0.25
            n = 3
        elif y < 0.95:  # Probabilitat 0.10
            n = 4
        else:           # Probabilitat 0.05
            n = 5
        self.nombre_passatgers = n
        super(EsdevenimentArribada, self).__init__("Arribada grup passatgers", rellotge)

    def esdevenir(self, estat):
        # try:
        #     estat.index(True)
        # except ValueError:
        #
        # estat.llista_persones_espera += [rellotge] * self.nombre_passatgers
        #
        # return [EsdevenimentArribada(self.rellotge + random.expovariate(1))]

        return []


class Simulacio:
    def __init__(self):
        self.temps_inicial = 0.0
        self.llista_esdeveniments = []
        self.temps_maxim_simulacio = 100.0
        self.estat = Estat()

        # Afegir esdeveniment inicial arribada
        self.llista_esdeveniments.append(EsdevenimentArribada(self.temps_inicial))

    # Returns a bool
    def finalitzar(self, esdeveniment):
        return True

    def executa(self):
        esdeveniment = self.obtenir_esdeveniment_proper()
        while not self.finalitzar(esdeveniment):

            # Executar l'esdevniment i afegir els nous esdeveniments que aquest genera a la llista
            # d'esdeveniments
            self.llista_esdeveniments += esdeveniment.esdevenir(self.estat)

    def obtenir_esdeveniment_proper(self):
        self.llista_esdeveniments.sort()
        return self.llista_esdeveniments.pop(0)

    def escriure_informacio(self, esdeveniment):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
