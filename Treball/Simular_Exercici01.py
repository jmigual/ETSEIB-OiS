'''
Created on 03/08/2014

@author: Ernest Benedito
'''
from Distribucions import uniforme_discreta


# Funcio principal
def Simular_Exercici01():
    global rellotge
    global estat
    global temps_funcionament

    iniciar_variables()
    iniciar_variables()

    esdeveniment = obtenir_esdeveniment_proper()
    while not finalitzar_simulacio(esdeveniment):

        # Avanca rellotge
        rellotge = esdeveniment[0]

        # Determina tipus d'esdeveniment
        tipus_esdeveniment = esdeveniment[1]

        # Actualitza l'estat del sistema i la llista de nous esdeveniments, depenent del tipus d'esdeveniment
        if tipus_esdeveniment == "Avaria component":
            esdeveniment_avaria()
        if tipus_esdeveniment == "Fi reparacio":
            esdeveniment_fi_reparacio()

        # Escriu informacio 
        escriure_informacio(estat, esdeveniment)

        # Determina el proper event
        esdeveniment = obtenir_esdeveniment_proper()

    return (temps_funcionament, estat)


def escriure_informacio(estat, esdeveniment):
    print('{0:5.1f} {1:15} {2:2d}'.format(esdeveniment[0], esdeveniment[1], estat))


# Procesa l'esdeveniment del tipus avaria
def esdeveniment_avaria():
    global temps_funcionament
    global rellotge
    global estat
    global maxim_maquines_avariades

    # Actualitza l'estat del sistema
    estat += 1

    # Actualitza comptadors
    if estat == maxim_maquines_avariades:
        temps_funcionament += rellotge

    # Afegeix nous esdeveniments
    afegir_esdeveniment_fi_reparacio(rellotge)
    afegir_esdeveniment_avaria(rellotge)


# Procesa l'esdeveniment del tipus fi de reparacio
def esdeveniment_fi_reparacio():
    global estat

    # Actualitza l'estat del sistema
    estat += -1


def afegir_esdeveniment_fi_reparacio(rellotge):
    global llista_esdeveniments

    temps_reparacio = 2.5
    temps_esdeveniment = rellotge + temps_reparacio
    tipus_esdeveniment = 'Fi reparacio'

    nou_esdeveniment = temps_esdeveniment, tipus_esdeveniment

    # S'afegeix l'esdeveniment a la llista d'esdeveniments
    llista_esdeveniments += [nou_esdeveniment]


def afegir_esdeveniment_avaria(rellotge):
    global llista_esdeveniments

    temps_avaria = uniforme_discreta(1, 6)
    temps_esdeveniment = rellotge + temps_avaria
    tipus_esdeveniment = 'Avaria component'

    nou_esdeveniment = temps_esdeveniment, tipus_esdeveniment

    # S'afegeix l'esdeveniment a la llista d'esdeveniments
    llista_esdeveniments += [nou_esdeveniment]


def iniciar_variables():
    global maxim_temps
    global maxim_maquines_avariades
    global llista_esdeveniments
    global estat
    global temps_funcionament

    temps_inicial = 0.0

    # Hi ha 1 variable d'estat: nombre de maquines avariades
    maquines_avariades = 0
    estat = maquines_avariades
    llista_esdeveniments = []
    afegir_esdeveniment_avaria(temps_inicial)
    #    llista_esdeveniments = [(temps_inicial,"Fi reparacio")]

    maxim_temps = 100
    maxim_maquines_avariades = 2
    temps_funcionament = 0;


# Funcio per veure si finalitza la simulacio 
def finalitzar_simulacio(esdeveniment):
    global maxim_temps
    global maxim_maquines_avariades
    global estat
    temps_esdeveniment = esdeveniment[0]

    return (maxim_temps <= temps_esdeveniment or maxim_maquines_avariades <= estat)


# Funcio que obte proper esdeveniment
def obtenir_esdeveniment_proper():
    global llista_esdeveniments
    ordenar_llista_esdeveniments()
    esdeveniment_proper = llista_esdeveniments[0]
    esborrar_esdeveniment_proper()
    return esdeveniment_proper


# Funcio que esborra el primer esdeveniment un cop consultat
def esborrar_esdeveniment_proper():
    global llista_esdeveniments

    llista_esdeveniments = llista_esdeveniments[1:]


# Funcio per ordenar la llista d'esdeveniments segons el temps
def ordenar_llista_esdeveniments():
    global llista_esdeveniments

    llista_esdeveniments.sort(
        key=lambda tup: tup[0])  # El segon element de la tupla fa referencia al temps


Simular_Exercici01()
