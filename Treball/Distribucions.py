import random


def uniforme_discreta(a,b):
    return int(a + (b+1-a)*random.random())

def bernoulli(p,v1,v2):
    if random.random() < p:
        return v1
    return v2