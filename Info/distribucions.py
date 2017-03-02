#!/usr/bin/env python3
import random
import math

def normal(mu, sigma):
  y1 = random.random()
  y2 = random.random()

  t = math.sqrt(-2*math.log(y1))*math.sin(2*math.pi*y2)
  return mu + t*sigma

def densTriang(a, b, c, x):
  if x < c:
    return 2*(x - a)/((b - a)*(c - a))
  return 2*(b - x)/((b - a)*(b - c))

def triangular(a, b, c):
  k = 2/(b - a)
  y = random.uniform(0, k)
  x = random.uniform(a, b)
  if y < densTriang(a, b, c, x):
    return x
  return triangular(a, b, c)

def bernoulli(p):
  return int(random.random() <= p) 

def binomial(n, p):
  s = 0
  for i in range(n):
    s += bernoulli(p)
  return s

def poisson(l):
  s = 1.0
  y = random.random()
  val = y*math.exp(l)
  k = 1
  while s < val:
    s += math.pow(l, k)/math.factorial(k)
    k += 1
  return k

def exponencial(l):
  y = random.random()
  return -1.*math.log(y)/l

def erlangk(k, mu):
  prod = 1
  for i in range(k):
    prod *= random.random()

  return -mu*math.log(prod)/k




n = 1000
suma = 0
for i in range(n):
   aux = erlangk(1, 2.0)
   suma += aux
   print(aux)

#print("mitjana:", suma/n)
