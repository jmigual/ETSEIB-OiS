#!/usr/bin/env python3

import Distribucions
import random


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


class EsdevenimentFinalitzacio(Esdeveniment):
    def __init__(self, rellotge):
        super(EsdevenimentFinalitzacio, self).__init__("Finalitzacio facturacio", rellotge)


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


class Simulacio:
    def __init__(self):
        self.temps_inicial = 0.0
        self.llista_esdeveniments = []
        self.temps_maxim_simulacio = 100.0
        self.estat = Estat()

        # Afegir esdeveniment inicial arribada
        self.llista_esdeveniments.append(EsdevenimentArribada(self.temps_inicial))

    # Returns a bool
    def finalitzar(self):
        return True

    def executa(self):
        while not self.finalitzar():
            print("Not ending")

    def obtenir_esdeveniment_proper(self):
        self.llista_esdeveniments.sort()
        return self.llista_esdeveniments.pop(0)


def main():
    pass


if __name__ == "__main__":
    main()
